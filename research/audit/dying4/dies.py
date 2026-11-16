#!/usr/bin/env python3
"""dies.py: dying against recovering faces at the catch, count-matched, with a bootstrap (A = 63, st4 run r11).
Within each live count k the pooled C (study's definition) of dying and of recovering faces; the difference averaged
with the dying faces' k weights. 200 Poisson resamples of faces.

    python3 research/audit/dying4/dies.py      # -> research/audit/dying4/dies_out.txt
"""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geom
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying4')
V = geom.Vessel(11); A = V.A; Dg = V.D; rng = np.random.default_rng(5)
M2 = ((Dg >= 1) & (Dg <= 2)).astype(float)


def bits(w):
    return np.unpackbits(np.ascontiguousarray(w).view(np.uint8).reshape(-1, 16), axis=1, bitorder='little')[:, :A]


smp = np.fromfile(os.path.join(SCR, 'r11.smp'), np.uint8).reshape(-1, 32)
SX = bits(smp[:400000, 16:].copy().view(np.uint64)).astype(float); rho = SX.mean(0)
S = (SX * (SX @ M2)).sum() / (SX @ (M2 @ rho)).sum()
cat = np.fromfile(os.path.join(SCR, 'r11.cat'), np.uint8).reshape(-1, 116)
ch = cat[:, :36].copy().view(np.int32); cw = cat[:, 36:].copy().view(np.uint64).reshape(-1, 5, 2)
out = open(os.path.join(HERE, 'dies_out.txt'), 'w')
for j, p in ((2, 0.3), (3, 0.15)):
    sel = ((ch[:, 4] >> j) & 1).astype(bool)
    X = bits(cw[sel, j]).astype(float); en = ch[sel, 2]; ks = X.sum(1).astype(int)
    N = (X * (X @ M2)).sum(1); D = X @ (M2 @ rho)
    dead = en == 2; rec = en == 1
    kk = [k for k in np.unique(ks[dead]) if k >= 2 and (rec & (ks == k)).sum() >= 20]

    def stat(w):
        dsum = rsum = wt = 0.0
        for k in kk:
            md = dead & (ks == k); mr = rec & (ks == k)
            wd = (w[md]).sum()
            dsum += wd * (w[md] @ N[md]) / (w[md] @ D[md]); rsum += wd * (w[mr] @ N[mr]) / (w[mr] @ D[mr]); wt += wd
        return dsum / wt / S, rsum / wt / S
    d0, r0 = stat(np.ones(len(X)))
    bs = np.array([stat(rng.poisson(1.0, len(X)).astype(float)) for _ in range(200)])
    diff = bs[:, 1] - bs[:, 0]
    s = (f'A 63 p {p}: dying {dead.sum()} recovering {rec.sum()} (k = {kk[0]}..{kk[-1]}, k = 1 left out); '
         f'matched C dying {d0:.4f} +- {bs[:, 0].std():.4f}, recovering {r0:.4f} +- {bs[:, 1].std():.4f}, '
         f'difference {r0 - d0:.4f} +- {diff.std():.4f}; unmatched {N[dead].sum() / D[dead].sum() / S:.4f} vs {N[rec].sum() / D[rec].sum() / S:.4f}')
    print(s); out.write(s + '\n')
