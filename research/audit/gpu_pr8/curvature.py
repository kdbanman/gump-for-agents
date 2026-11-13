#!/usr/bin/env python3
"""Audit of PR 8, claim 2: is the upward curvature of the asymmetric face law real, and does it depend on which points
are used?  python3 research/audit/gpu_pr8/curvature.py

Points: CPU-verified ln tau_face at A = 30, 45, 63, 84 (research/theory/swarm/critic/board.md E2), GPU values at
A = 63, 84, 108, 135 (re-derived by rederive.py from the PR's committed JSON). For each subset: fits of linear,
a + bA + c sqrt(A) (rim term) and quadratic forms; prediction for A = 108 from the fit to A <= 84 only.
"""
import math
import numpy as np
CPU = {30: (6.804, .003), 45: (9.819, .003), 63: (13.633, .008), 84: (18.077, .054)}
GPU = {63: (13.635, .001), 84: (18.141, .005), 108: (23.376, .031), 135: (29.341, .250)}


def fit(pts, form):
    A = np.array([p[0] for p in pts], float); y = np.array([p[1] for p in pts]); s = np.array([p[2] for p in pts])
    X = {'linear': np.c_[np.ones_like(A), A], 'rim a+bA+c*sqrtA': np.c_[np.ones_like(A), A, np.sqrt(A)],
         'quad a+bA+cA^2': np.c_[np.ones_like(A), A, A * A]}[form]
    w = 1 / s
    beta, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)
    cov = np.linalg.inv((X * w[:, None]).T @ (X * w[:, None]))
    chi2 = float((((y - X @ beta) * w) ** 2).sum())
    return beta, cov, chi2, len(A) - X.shape[1], X


def row(A, form):
    return {'linear': [1, A], 'rim a+bA+c*sqrtA': [1, A, math.sqrt(A)], 'quad a+bA+cA^2': [1, A, A * A]}[form]


sets = {
    'CPU 30,45,63,84': [(a, *CPU[a]) for a in (30, 45, 63, 84)],
    'CPU 30-84 + GPU 108': [(a, *CPU[a]) for a in (30, 45, 63, 84)] + [(108, *GPU[108])],
    'CPU 30-84 + GPU 108,135': [(a, *CPU[a]) for a in (30, 45, 63, 84)] + [(108, *GPU[108]), (135, *GPU[135])],
    'CPU 30,45 + GPU 63-135': [(a, *CPU[a]) for a in (30, 45)] + [(a, *GPU[a]) for a in (63, 84, 108, 135)],
    'GPU 63,84,108': [(a, *GPU[a]) for a in (63, 84, 108)],
    'GPU 63-135': [(a, *GPU[a]) for a in (63, 84, 108, 135)],
    'CPU 45,63,84 + GPU 108 (drop 30)': [(a, *CPU[a]) for a in (45, 63, 84)] + [(108, *GPU[108])],
}
for name, pts in sets.items():
    print(f'== {name}')
    for form in ('linear', 'rim a+bA+c*sqrtA', 'quad a+bA+cA^2'):
        if len(pts) <= len(row(1, form)) - 0:
            if len(pts) < len(row(1, form)):
                continue
        b, cov, chi2, dof, _ = fit(pts, form)
        se = np.sqrt(np.diag(cov))
        extra = ''
        if form != 'linear':
            extra = f'  c = {b[2]:.4g} +- {se[2]:.2g} ({b[2] / se[2]:+.1f} sigma)'
        pr = ''
        if 108 not in [p[0] for p in pts]:
            r = np.array(row(108, form)); pv = r @ b; ps = math.sqrt(r @ cov @ r)
            pr = f'  -> A=108: {pv:.3f} +- {ps:.3f} (GPU 23.376 +- 0.031; diff {23.376 - pv:+.3f})'
        slope_inf = f'  b = {b[1]:.4f} +- {se[1]:.4f}' if form != 'quad a+bA+cA^2' else ''
        print(f'  {form:18s} chi2 {chi2:7.2f}/{dof}{slope_inf}{extra}{pr}')
print('\nlocal slopes, verified CPU then GPU:')
seq = [(30, *CPU[30]), (45, *CPU[45]), (63, *CPU[63]), (84, *CPU[84]), (108, *GPU[108]), (135, *GPU[135])]
for (a1, l1, s1), (a2, l2, s2) in zip(seq, seq[1:]):
    print(f'  {a1}->{a2}: {(l2 - l1) / (a2 - a1):.4f} +- {math.hypot(s1, s2) / (a2 - a1):.4f}')
print('  84->108 with GPU 84:', f'{(23.376 - 18.141) / 24:.4f} +- {math.hypot(.005, .031) / 24:.4f}')
print('  rim-free slab slope (board E2): 0.2088 +- 0.0009')
