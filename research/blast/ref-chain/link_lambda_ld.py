#!/usr/bin/env python3
"""ref-chain (second review): lambda of the five certified 9-cell faces in extended precision (numpy longdouble,
exact rational alive probabilities), against the 19-digit intervals of LinkFaces.lean.
  python3 research/blast/ref-chain/link_lambda_ld.py      (about 1 min)
"""
import os, sys
from fractions import Fraction as Fr
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_numbers import face, tables
from oracle import BIRTH, SURVIVE
R1, R2 = Fr(11, 25), Fr(21, 50)
LD = np.longdouble
def ap(m1, m2, k, s):
    return sum(comb(m1, j) * R1**j * (1 - R1)**(m1 - j) * comb(m2, l) * R2**l * (1 - R2)**(m2 - l)
               for j in range(m1 + 1) for l in range(m2 + 1) if (k + j + l) in (SURVIVE if s else BIRTH))
fl = lambda f: LD(f.numerator) / LD(f.denominator)
CLAIM = {'hull 3': ('0.9165673655948901373', '0.9165673655948901374'), 'torus 1 0 3': ('0.9664099275695942426', '0.9664099275695942427'),
         'torus 1 1 3': ('0.9324323935928482210', '0.9324323935928482211'), 'strip 1 3': ('0.9391216736592712685', '0.9391216736592712686'),
         'patch 1 3': ('0.8474738060566295030', '0.8474738060566295031')}
print(f"longdouble eps = {np.finfo(LD).eps}")
for name, kind, args in (('hull 3', 'hull', (3,)), ('torus 1 0 3', 'torus', (1, 0, 3)), ('torus 1 1 3', 'torus', (1, 1, 3)),
                         ('strip 1 3', 'strip', (1, 3)), ('patch 1 3', 'patch', (1, 3))):
    cells, red, coin = face(kind, *args)
    nb, m1, m2 = tables(cells, red, coin)
    A = len(cells); n = 1 << A
    a = np.zeros((n, A), dtype=LD)
    for x in range(n):
        for i in range(A):
            k = sum((x >> j) & 1 for j in nb[i])
            a[x, i] = fl(ap(m1[i], m2[i], k, (x >> i) & 1))
    P = np.ones((n, n), dtype=LD)
    for y in range(n):
        for i in range(A):
            P[:, y] *= a[:, i] if (y >> i) & 1 else (1 - a[:, i])
    Q = P[1:, 1:]
    mu = np.full(n - 1, LD(1) / (n - 1))
    for it in range(4000):
        nu = mu @ Q; lam = nu.sum(); nu /= lam
        if np.abs(nu - mu).max() < LD(1e-19): break
        mu = nu
    lo, hi = CLAIM[name]
    print(f"{name}: lambda = {np.format_float_positional(lam, precision=20)}  claimed [{lo}, {hi}]  "
          f"distance to the interval ~ {float(max(LD(lo) - lam, lam - LD(hi), 0)):.1e}  ({it} iterations)")
