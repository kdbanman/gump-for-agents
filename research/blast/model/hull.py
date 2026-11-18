#!/usr/bin/env python3
"""hull.py (blast/model): can the hull faces carry the wrapped price? ln tau of the hull faces of k = 4..8 unit
cells a side (A = 3k(k+1)/2 = 30..108) fitted with the wide wrapped price c = 0.2086 held fixed plus terms of an
expansion in the side, against "two prices" (a free price per cell). Rows: research/constant/out/points.txt (30, 45,
63, 84 cells) and BRIEF-COMMON.md (108 cells: 23.3392 +- 0.0099).

    python3 research/blast/model/hull.py
"""
import math
import numpy as np
H = [(4, 30, 6.8054, 0.0029), (5, 45, 9.8202, 0.0027), (6, 63, 13.6346, 0.0011), (7, 84, 18.1407, 0.0054),
     (8, 108, 23.3392, 0.0099)]
C = 0.2086
one = lambda k, A: 1.0; kk = lambda k, A: k; lnA = lambda k, A: math.log(A); AA = lambda k, A: A
lnk = lambda k, A: math.log(k); ik = lambda k, A: 1 / k


def fit(cols, pts, label):
    X = np.array([[f(k, A) for f in cols] for k, A, y, s in pts]); y = np.array([y - C * A for k, A, y, s in pts])
    w = 1 / np.array([s for *_, s in pts])
    th, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None); z = (X @ th - y) * w

    def pred(k):
        A = 3 * k * (k + 1) // 2
        return float(np.array([f(k, A) for f in cols]) @ th + C * A)
    print(f'  {label:44s} chi2 {float(z @ z):8.1f} on {len(pts) - len(th)}  coefficients {np.round(th, 4)}  z {np.round(z, 1)}')
    print(f'  {"":44s} forecasts: 135 cells {pred(9):.3f}, 165 cells {pred(10):.3f}, 198 cells {pred(11):.3f}')


for pts, lab in ((H[1:], 'k = 5..8 (45-108 cells)'), (H, 'k = 4..8 (30-108 cells)')):
    print(lab)
    fit([one, kk], pts, 'c A + b k + d (rim linear in the side)')
    fit([one, kk, AA], pts, '(c + dc) A + b k + d (two prices)')
    fit([one, kk, lnA], pts, 'c A + b k + d + m ln A (prefactor power)')
    fit([one, kk, lnk], pts, 'c A + b k + d + m ln k')
    fit([one, kk, ik], pts, 'c A + b k + d + e/k (next term in 1/k)')
