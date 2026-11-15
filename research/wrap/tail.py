#!/usr/bin/env python3
"""Is there a discount beyond loop^2 19?  HAZ (models.py) with extra loop lengths whose share is constant in A (one
parameter each), on the faces with A >= 48 (on file + new).   python3 research/wrap/tail.py"""
import os, sys
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fit as Fm  # noqa: E402
pts = [p for p in Fm.select('all', True) if p['A'] >= 48]
A = np.array([p['A'] for p in pts], float); x = A - 63
y = np.array([p['y'] for p in pts]); se = np.array([p['se'] for p in pts])
for extra in ([], [21], [21, 25], [21, 25, 27, 28]):
    qs = [12, 13, 16, 19] + extra
    N = np.array([[sum(1 for q in p['loops'] if q == Q) for Q in qs] for p in pts], float)
    def f(th):
        r, g = th[2:2 + len(qs)], np.concatenate([th[2 + len(qs):], np.zeros(len(extra))])
        return th[0] + th[1] * x - np.log1p((N * r * np.exp(np.outer(x, g))).sum(1))
    th0 = [13.16, 0.2086, 0.13, 0.10, 0.055, 0.013] + [0.0] * len(extra) + [0.035, 0.032, 0.025, 0.02]
    res = least_squares(lambda th: (y - f(th)) / se, th0, method='lm', max_nfev=20000)
    cov = np.linalg.inv(res.jac.T @ res.jac); e = np.sqrt(np.diag(cov))
    print(f'HAZ + constant shares for {extra}: chi2 {res.fun @ res.fun:.1f} on {len(pts) - len(th0)}; ' +
          ' '.join(f'r{q}={res.x[2 + i]:.4f}±{e[2 + i]:.4f}' for i, q in enumerate(qs)))
