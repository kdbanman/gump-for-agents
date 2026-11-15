#!/usr/bin/env python3
"""The equilateral tori together: pooled ln tau_face per torus from the committed rows, local slopes, weighted
straight-line fits from a lower area up, and residuals from the forecast line of PREDICTIONS.md block 3.

  python research/gpu-local/eq_fit.py [AMIN ...]      # default: fits from A >= 63, 75, 81

CPU only; reads research/data/gpu_local_eqtorus/eqtorus_*.csv.
"""
import csv, glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

pts = []
for path in glob.glob(os.path.join(ROOT, 'research', 'data', 'gpu_local_eqtorus', 'eqtorus_*.csv')):
    rows = list(csv.DictReader(open(path)))
    E = sum(int(r['exposure']) for r in rows); F = sum(int(r['face']) for r in rows)
    pts.append((int(rows[0]['A']), rows[0]['torus'], math.log(2 * E / F), 1 / math.sqrt(F), F))
pts.sort()
A = np.array([p[0] for p in pts], float); y = np.array([p[2] for p in pts]); s = np.array([p[3] for p in pts])
print('  A  lattice     face deaths   ln tau_face           minus 13.1622 + 0.2084 (A - 63)')
for (a, t, v, e, F) in pts:
    print(f'{a:4d}  ({t:8s}) {F:10d}   {v:.4f} +- {e:.4f}    {v - 13.1622 - 0.2084 * (a - 63):+.4f}')
print('local slopes:')
for i in range(len(pts) - 1):
    print(f'  {int(A[i]):3d} -> {int(A[i + 1]):3d}: {(y[i + 1] - y[i]) / (A[i + 1] - A[i]):.5f} +- '
          f'{math.hypot(s[i], s[i + 1]) / (A[i + 1] - A[i]):.5f}')
for amin in [int(x) for x in sys.argv[1:]] or [63, 75, 81]:
    m = A >= amin
    w = 1 / s[m] ** 2
    X = np.vstack([np.ones(m.sum()), A[m] - 63]).T
    C = np.linalg.inv(X.T @ (w[:, None] * X)); b = C @ X.T @ (w * y[m])
    r = y[m] - X @ b
    print(f'line through A >= {amin}: ln tau = {b[0]:.4f} (+- {C[0, 0] ** .5:.4f}) + {b[1]:.5f} (+- {C[1, 1] ** .5:.5f}) (A - 63), '
          f'chi2 = {(r ** 2 * w).sum():.1f} on {m.sum() - 2}')
    print('   residuals: ' + ', '.join(f'{int(a)}: {x:+.4f} ({x / e:+.1f})' for a, x, e in zip(A[m], r, s[m])))
