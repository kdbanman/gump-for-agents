#!/usr/bin/env python3
"""null.py (review of dying round 4): what the company C would read if a lever rule held exactly.

Lever-rule null: a remnant at relative density p_t occupying a compact region of the face (a graph ball around a
random cell, grown in distance order with random tie-breaks until its stationary mass sum(rho) reaches k/p_t), whose
cells are those of a random stationary face inside the region, thinned to exactly k. Everything outside is empty.
C, V and the shell profile are computed exactly as in ana.py (the study's registered definitions). Compared, at the
same fixed k = L(p), with st4's faces sampled at a random moment with P = L(p) (the .lvl records; time-weighted).

    python3 research/audit/dying4/null.py r11 11 31.29     # -> research/audit/dying4/null_r11.txt
    python3 research/audit/dying4/null.py r13 13 42.49
    python3 research/audit/dying4/null.py r15 15 55.14
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geom
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying4')
tag, R, PBAR = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
V = geom.Vessel(R); A = V.A; Dg = V.D
rng = np.random.default_rng(31)
OUT = open(os.path.join(HERE, f'null_{tag}.txt'), 'w')
PS = [0.6, 0.45, 0.3, 0.15]; LV = [int(math.floor(p * PBAR)) for p in PS]


def say(s=''):
    print(s, flush=True); OUT.write(s + '\n'); OUT.flush()


def bits(words):
    b = np.unpackbits(np.ascontiguousarray(words).view(np.uint8).reshape(-1, 16), axis=1, bitorder='little')
    return b[:, :A].copy()


smp = np.fromfile(os.path.join(SCR, tag + '.smp'), np.uint8).reshape(-1, 32)
SX = bits(smp[:, 16:].copy().view(np.uint64))
if len(SX) > 600000: SX = SX[rng.choice(len(SX), 600000, replace=False)]
rho = SX.mean(0)
lvl = np.fromfile(os.path.join(SCR, tag + '.lvl'), np.uint8).reshape(-1, 32)
lh = lvl[:, :16].copy().view(np.int32); LX = bits(lvl[:, 16:].copy().view(np.uint64))
M2 = ((Dg >= 1) & (Dg <= 2)).astype(float); M2s = (Dg <= 2).astype(float)
shells = [(Dg == q).astype(float) for q in (1, 2, 3)] + [(Dg >= 4).astype(float)]


def CN(X, M=M2):
    Xf = X.astype(float); return (Xf * (Xf @ M)).sum() / (Xf @ (M @ rho)).sum()


S = CN(SX[:200000]); Ssh = [CN(SX[:200000], m) for m in shells]
order_bfs = [np.argsort(Dg[c0] + rng.random(A) * 0.5) for c0 in range(A)]
cum = np.cumsum(rho[np.array(order_bfs)], axis=1)


def null(k, pt, n):
    out = np.zeros((n, A), np.uint8); t = 0
    while t < n:
        c0 = rng.integers(A); m = int(np.searchsorted(cum[c0], k / pt)) + 1
        reg = order_bfs[c0][:m]; s_ = SX[rng.integers(len(SX))]; cand = reg[s_[reg] > 0]
        if len(cand) >= k:
            out[t, rng.choice(cand, k, replace=False)] = 1; t += 1
    return out


def desc(X):
    v = 1 - ((X.astype(float) @ M2s) > 0).mean(1)
    return CN(X) / S, v.mean(), [CN(X, m) / Ssh[q] for q, m in enumerate(shells)]


say(f'# {tag}: A {A}, levels {dict(zip(PS, LV))}, S {S:.4f}; fixed k = L(p)')
res = {}
for j, (p, k) in enumerate(zip(PS, LV)):
    sl = lh[:, 2] == j
    if sl.sum() >= 100:
        c, v, pr = desc(LX[sl]); res[('lvl', p)] = c
        say(f'at level  p {p} k {k} (n {sl.sum()}): C {c:.3f} V {v:.3f} profile ' + ' '.join(f'{z:.3f}' for z in pr))
    for pt in (0.45, 0.55, 0.65, 0.8):
        c, v, pr = desc(null(k, pt, 6000)); res[(pt, p)] = c
        say(f'  null p_t {pt}: C {c:.3f} V {v:.3f} profile ' + ' '.join(f'{z:.3f}' for z in pr))
say()
for key in ['lvl', 0.45, 0.55, 0.65, 0.8]:
    if (key, 0.15) in res and (key, 0.45) in res:
        say(f'{key}: C(L0.15)/C(L0.45) = {res[(key, 0.15)] / res[(key, 0.45)]:.3f}   C(L0.3)/C(L0.45) = {res[(key, 0.3)] / res[(key, 0.45)]:.3f}')
