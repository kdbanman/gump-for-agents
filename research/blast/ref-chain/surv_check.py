#!/usr/bin/env python3
"""ref-chain (third review): hull3_complete's constants.  P_x(T > t) on hull 3 at (11/25, 21/50) by iterating my
own kernel (link_numbers.py), against 0.72 * lam_lo^t (claimed for the full face, state 511) and 1384 * lam_hi^t
(claimed for every living x), t = 0..3000.   OMP_NUM_THREADS=1 python3 research/blast/ref-chain/surv_check.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_numbers import face, tables, alive_prob
cells, red, coin = face('hull', 3)
nb, m1, m2 = tables(cells, red, coin)
A = 9; n = 512
X = ((np.arange(n)[:, None] >> np.arange(A)[None, :]) & 1)
a = np.zeros((n, A))
for i in range(A):
    k = X[:, nb[i]].sum(1)
    tab = np.array([[alive_prob(m1[i], m2[i], kk, s) for kk in range(7)] for s in (0, 1)])
    a[:, i] = tab[X[:, i], k]
P = np.ones((n, 1))
for i in reversed(range(A)):
    P = (P[:, :, None] * np.stack([1 - a[:, i], a[:, i]], axis=1)[:, None, :]).reshape(n, -1)
Q = P[1:, 1:]
lo, hi = 0.9165673655948901373, 0.9165673655948901374
s = np.ones(n - 1); rmin_full = np.inf; rmin_all = np.inf; argmin = None; rmax = 0; argmax = None
for t in range(3001):
    r = s / lo ** t
    if r[510] < rmin_full: rmin_full = r[510]; tmin = t
    if r.min() < rmin_all: rmin_all = r.min(); argmin = (t, int(r.argmin()) + 1)
    ru = s / hi ** t
    if ru.max() > rmax: rmax = ru.max(); argmax = (t, int(ru.argmax()) + 1)
    s = Q @ s
print(f"full face (state 511): min_t P(T>t)/lam_lo^t = {rmin_full:.4f} at t = {tmin}  (claimed >= 0.72)")
print(f"over all living starts: min_t,x P_x(T>t)/lam_lo^t = {rmin_all:.4f} at (t, x) = {argmin}  (0.72 holds for every start: {rmin_all >= 0.72})")
print(f"max_t,x P_x(T>t)/lam_hi^t = {rmax:.4f} at (t, x) = {argmax}  (claimed <= 1384)")
