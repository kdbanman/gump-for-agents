#!/usr/bin/env python3
"""blast/ref-proofs: population law under the tilted measure mu_s ~ mu * exp(-s E), by reweighting simulated
quasi-stationary states (replicas older than `burn` generations since a fair start).  E(x) = -sum_i ln P(i dead next | x).
usage: tiltmc.py <kind> <args...> [steps=240]     (validated against the exact law on 12 cells: `tiltmc.py torus 1 1 4`)"""
import sys, math
import numpy as np
import ref
kind = sys.argv[1]; args = []; steps = 240
for a in sys.argv[2:]:
    if a.startswith('steps='): steps = int(a[6:])
    else: args.append(int(a))
nb, m = ref.build(kind, args); A = len(nb); r1, r2 = 0.44, 0.42
rng = np.random.default_rng(777)
tabs = [np.array([[ref.p_alive(x, kk, m[i][0], m[i][1], r1, r2) for kk in range(7)] for x in (0, 1)]) for i in range(A)]
nbarr = [np.array(l, dtype=np.int64) for l in nb]
R = 200000; burn = 40
X = (rng.random((R, A)) < 0.5).astype(np.int8); age = np.zeros(R, dtype=np.int64)
S = (0.0, 0.1, 0.2, 0.3, 0.5, 1.0)
H = np.zeros((len(S), A + 1)); W1 = np.zeros(len(S)); W2 = np.zeros(len(S)); ES = np.zeros(len(S))
for t in range(steps):
    k = np.stack([X[:, nbarr[i]].sum(1) for i in range(A)], axis=1)
    pa = np.stack([tabs[i][X[:, i], k[:, i]] for i in range(A)], axis=1)
    old = age >= burn
    if old.any():
        E = -np.log(1 - pa[old]).sum(1); pop = X[old].sum(1)
        for j, s in enumerate(S):
            w = np.exp(-s * E)
            H[j] += np.bincount(pop, weights=w, minlength=A + 1); W1[j] += w.sum(); W2[j] += (w * w).sum(); ES[j] += (w * E).sum()
    Y = (rng.random((R, A)) < pa).astype(np.int8)
    age += 1
    dead = Y.sum(1) == 0; nd = int(dead.sum())
    Y[dead] = (rng.random((nd, A)) < 0.5).astype(np.int8); age[dead] = 0
    X = Y
print('== %s %s A %d: tilted population law from %d sampled steps of %d replicas' % (kind, args, A, steps - burn, R))
for j, s in enumerate(S):
    p = H[j] / W1[j]
    print('  s %.1f  eff.sample %.2e  <E>/A %.4f  density %.4f  P(pop=n), n=1..A: %s' %
          (s, W1[j] ** 2 / W2[j], ES[j] / W1[j] / A, (p * np.arange(A + 1)).sum() / A, ' '.join('%.3f' % x for x in p[1:])))
