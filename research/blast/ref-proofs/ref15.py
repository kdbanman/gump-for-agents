#!/usr/bin/env python3
"""blast/ref-proofs: the 15-cell tube (1,1),(0,5) (or any torus 1 K D) exactly, by lumping the dense kernel over
the D translations along the tube (a symmetry of the chain; the population is constant on orbits, so the
half-fall marker lumps too).  usage: ref15.py K D"""
import sys, math, itertools
import numpy as np
import ref
K, D = int(sys.argv[1]), int(sys.argv[2]); r1, r2 = 0.44, 0.42
nb, m = ref.g_torus(1, K, D); A = len(nb); N = 1 << A
sh = lambda i: (i + 3) % A
assert all(sorted(sh(j) for j in nb[i]) == sorted(nb[sh(i)]) for i in range(A)), 'translation is not an automorphism'
idx = np.arange(N, dtype=np.int64)
bits = ((idx[:, None] >> np.arange(A)[None, :]) & 1).astype(np.int64)
al = np.zeros((N, A))
for i in range(A):
    k = np.zeros(N, dtype=np.int64)
    for j in nb[i]: k += bits[:, j]
    tab = np.array([[ref.p_alive(x, kk, 2, 1, r1, r2) for kk in range(7)] for x in (0, 1)])
    al[:, i] = tab[bits[:, i], k]
rot = lambda x: ((x << 3) | (x >> (A - 3))) & (N - 1)
canon = idx.copy(); y = idx.copy()
for _ in range(D - 1):
    y = rot(y); canon = np.minimum(canon, y)
reps, orb = np.unique(canon, return_inverse=True)
M = len(reps); pop = bits.sum(1); popo = pop[reps]
order = np.argsort(orb, kind='stable'); starts = np.searchsorted(orb[order], np.arange(M))
PL = np.zeros((M, M))
B = 512
for s in range(0, M, B):
    rr = reps[s:s + B]
    P = np.ones((len(rr), 1))
    for i in range(A):
        a = al[rr, i][:, None]
        P = np.concatenate([P * (1 - a), P * a], axis=1)
    PL[s:s + B] = np.add.reduceat(P[:, order], starts, axis=1)
assert np.allclose(PL.sum(1), 1, atol=1e-12) and reps[0] == 0 and PL[0, 0] == 1
Q = PL[1:, 1:]; v = np.full(M - 1, 1.0 / (M - 1)); lam = 0
for it in range(5000):
    w = v @ Q; l2 = w.sum(); w /= l2
    done = abs(l2 - lam) < 1e-15 and np.abs(w - v).max() < 1e-15
    v, lam = w, l2
    if done: break
d = PL[1:, 0]; h = float(v @ d)
print('== torus_1_%d_%d A %d  orbits %d  iterations %d' % (K, D, A, M, it))
print('h %.13e  1-lambda %.13e  lntau %.12f  density %.12f' % (h, 1 - lam, -math.log(h), float(v @ popo[1:]) / A))
flux = v * d / h
print('death_from_1,2,3 %.6e %.6e %.6e' % tuple(flux[popo[1:] == n].sum() for n in (1, 2, 3)))
half = (A + 1) // 2
Pn = np.where(popo[:, None] - popo[None, :] < half, PL, 0.0); Qn = Pn[1:, 1:]; dn = Pn[1:, 0]
u = v.copy(); out = []
for KK in range(1, 11):
    out.append((KK, 1 - float(u @ dn) / (lam ** (KK - 1) * h))); u = u @ Qn
print('halffall_share (fall >= %d): ' % half + '  '.join('K=%d: %.6f' % o for o in out))
print('  share with the DEATH step itself a half-fall: %.6f' % (flux[popo[1:] >= half].sum()))
E = -np.log(PL[1:, 0])
for s in (0, 0.1, 0.2, 0.3, 0.5, 1.0):
    ms = v * np.exp(-s * E); ms /= ms.sum()
    print('  s %.1f <E>/A %.4f density %.4f P(pop=n): %s' % (s, float(ms @ E) / A, float(ms @ popo[1:]) / A,
          ' '.join('%.3f' % ms[popo[1:] == n].sum() for n in range(A + 1))))
