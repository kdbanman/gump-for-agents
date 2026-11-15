#!/usr/bin/env python3
"""Face hazard in three age bins of equal exposure, from this study's event files (research/scratch/wrap/ev_*).
    python3 research/wrap/hazard.py H K D"""
import glob, math, sys
import numpy as np
h, k, d = sys.argv[1:4]
ages, isF = [], []
for f in glob.glob(f'research/scratch/wrap/ev_{h}_{k}_{d}_s*.txt'):
    for line in open(f):
        t, a = line.split(); ages.append(int(a)); isF.append(t == 'F')
A = np.array(ages, float); F = np.array(isF)
E = A.sum(); edges = [0.0]
for frac in (1 / 3, 2 / 3):
    lo, hi = 0.0, A.max()
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if np.minimum(A, mid).sum() < frac * E else (lo, mid)
    edges.append(lo)
edges.append(A.max() + 1)
out = []
for lo, hi in zip(edges[:-1], edges[1:]):
    ex = (np.clip(A, lo, hi) - lo).sum(); n = int((F & (A >= lo) & (A < hi)).sum())
    out.append(f'{math.log(2 * ex / n):.4f} ± {1 / math.sqrt(n):.4f} (ages {int(lo)}-{int(hi)})')
print(f'({h},{k},{d}) lives {len(A)}: ' + '; '.join(out))
