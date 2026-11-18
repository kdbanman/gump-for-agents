#!/usr/bin/env python3
"""ln tau_face of loop^2-12 tubes against length L = cells/12 (data: research/constant/out/points.txt and the
anchors of BRIEF-COMMON.md), three forms:
  line      a + s L
  two-route a + s L - ln(1 + K exp(-L/xi))      i.e. 1/tau = r_d exp(-s L) + r_b exp(-(s + 1/xi) L), K = r_b/r_d
    python3 tubefit.py"""
import numpy as np, math
D = [(5, 12.4166, 0.0031), (6, 14.8753, 0.0140), (7, 17.3175, 0.0031), (8, 19.7405, 0.0059), (9, 22.1557, 0.0121)]
L = np.array([d[0] for d in D], float); y = np.array([d[1] for d in D]); se = np.array([d[2] for d in D])
def lin(off):
    X = np.column_stack([np.ones_like(L), L]) / se[:, None]; b, *_ = np.linalg.lstsq(X, (y - off) / se, rcond=None)
    r = y - off - b[0] - b[1] * L; return b, float(((r / se) ** 2).sum())
b, c = lin(0 * L); print(f"line:                 chi2 {c:6.1f} / 3   a {b[0]:.4f}  s {b[1]:.4f} per unit = {b[1]/12:.5f} per cell;  L=10: {b[0]+10*b[1]:.3f}")
print("local prices per cell:", ' '.join(f"{(y[i+1]-y[i])/12:.5f}+-{math.hypot(se[i],se[i+1])/12:.5f}" for i in range(4)))
best = None
for K in (1.0, 2.0, 4.0, None):
    for xi in np.arange(0.8, 6.01, 0.05):
        for KK in ([K] if K else np.exp(np.arange(-2, 4.01, 0.1))):
            off = -np.log1p(KK * np.exp(-L / xi)); b, c = lin(off)
            if best is None or c < best[0]: best = (c, xi, KK, b)
    c, xi, KK, b = best; best = None
    f = lambda x: b[0] + b[1] * x - math.log1p(KK * math.exp(-x / xi))
    print(f"two-route, K {'free' if K is None else 'fixed'} = {KK:5.2f}: chi2 {c:6.2f} / {2 if K else 1}   xi {xi:.2f}  s {b[1]:.4f} = {b[1]/12:.5f} per cell  a {b[0]:.4f};"
          f"  L=10: {f(10):.3f}  12: {f(12):.3f}  16: {f(16):.3f}  20: {f(20):.3f}  30: {f(30):.3f};  share of the dearer route at L=5,7,9: "
          + ' '.join(f"{KK*math.exp(-x/xi)/(1+KK*math.exp(-x/xi)):.2f}" for x in (5, 7, 9)))
# profile of chi2 in xi for K = 2
for xi in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
    off = -np.log1p(2 * np.exp(-L / xi)); b, c = lin(off); print(f"   K = 2, xi = {xi}: chi2 {c:.2f}, asymptotic price {b[1]/12:.5f}, L=10: {b[0]+10*b[1]-math.log1p(2*math.exp(-10/xi)):.3f}")
# power-law prefactor: ln tau = a + s L + p ln L  (tau ~ L^p exp(s L)); p = 1/2 is the prefactor of the tail of a sum
for p in (0.5, 1.0, None):
    if p is None:
        X = np.column_stack([np.ones_like(L), L, np.log(L)]) / se[:, None]; b, *_ = np.linalg.lstsq(X, y / se, rcond=None)
        r = y - b[0] - b[1] * L - b[2] * np.log(L); c = float(((r / se) ** 2).sum()); pp = b[2]; dof = 2
        cov = np.linalg.inv(X.T @ X); extra = f" +- {cov[2,2]**0.5:.2f}"
    else:
        b, c = lin(p * np.log(L)); pp = p; dof = 3; extra = " (fixed)"
    f = lambda x: b[0] + b[1] * x + pp * math.log(x)
    print(f"power law, p = {pp:.2f}{extra}: chi2 {c:6.2f} / {dof}   s {b[1]:.4f} = {b[1]/12:.5f} per cell;  L=10: {f(10):.3f}  12: {f(12):.3f}  16: {f(16):.3f}  20: {f(20):.3f}  30: {f(30):.3f}")
