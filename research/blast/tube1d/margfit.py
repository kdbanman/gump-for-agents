#!/usr/bin/env python3
"""One curve for the marginal price of emptying one more unit of a loop^2-12 tube: bands in a living 144-cell tube
(`tube1d bandp`, widths 2.5-6 units) and whole tubes (anchors, 5-9 units).  S(l) = a + 12 c l - 12 B xi exp(-l/xi),
so the price between l1 and l2 is c + B xi (exp(-l1/xi) - exp(-l2/xi)) / (l2 - l1).
    python3 margfit.py BANDP_FILE"""
import sys, math
import numpy as np
pts = []      # (l1, l2, price per cell, err, source)
if sys.argv[1].endswith('.slopes'):      # pooled slopes with errors from independent runs (bandcombine.py --out=...)
    for l in open(sys.argv[1]):
        if l[0].isdigit():
            a, b, p, e = map(float, l.split())
            if a >= 2.5 and b <= 7.5: pts.append((a, b, p, max(e, 0.0005), 'band'))
else:
    rows = [l.split() for l in open(sys.argv[1]) if l.strip() and l[0].isdigit()]
    w = [float(r[0]) for r in rows]; y = [float(r[4]) for r in rows]; e = [float(r[5]) for r in rows]
    for i in range(1, len(rows)):
        if w[i - 1] >= 2.5 and w[i] <= 6.5: pts.append((w[i - 1], w[i], (y[i] - y[i - 1]) / (12 * (w[i] - w[i - 1])), max(math.hypot(e[i], e[i - 1]) / 6, 0.0007), 'band'))
T = [(5, 12.4166, 0.0031), (6, 14.8753, 0.0140), (7, 17.3175, 0.0031), (8, 19.7405, 0.0059), (9, 22.1557, 0.0121)]
for i in range(1, len(T)): pts.append((T[i - 1][0], T[i][0], (T[i][1] - T[i - 1][1]) / 12, math.hypot(T[i][2], T[i - 1][2]) / 12, 'tube'))
def chi(c, B, xi, sel=None):
    s = 0; out = []
    for l1, l2, m, er, src in pts:
        if sel and src != sel: continue
        p = c + B * xi * (math.exp(-l1 / xi) - math.exp(-l2 / xi)) / (l2 - l1); s += ((m - p) / er) ** 2; out.append((l1, l2, m, er, p, src))
    return s, out
for sel in (None, 'band', 'tube'):
    best = None
    for xi in np.arange(0.8, 6.01, 0.05):
        # linear least squares in (c, B) at fixed xi
        P = [p for p in pts if not sel or p[4] == sel]
        X = np.array([[1, xi * (math.exp(-p[0] / xi) - math.exp(-p[1] / xi)) / (p[1] - p[0])] for p in P]); yy = np.array([p[2] for p in P]); er = np.array([p[3] for p in P])
        b, *_ = np.linalg.lstsq(X / er[:, None], yy / er, rcond=None); c2 = float((((yy - X @ b) / er) ** 2).sum())
        if best is None or c2 < best[0]: best = (c2, xi, b[0], b[1], len(P))
    c2, xi, c, B, n = best
    # interval of xi with chi2 within +1
    lo = hi = xi; cs = []
    for x2 in np.arange(0.8, 6.01, 0.05):
        P = [p for p in pts if not sel or p[4] == sel]
        X = np.array([[1, x2 * (math.exp(-p[0] / x2) - math.exp(-p[1] / x2)) / (p[1] - p[0])] for p in P]); yy = np.array([p[2] for p in P]); er = np.array([p[3] for p in P])
        b, *_ = np.linalg.lstsq(X / er[:, None], yy / er, rcond=None); cc = float((((yy - X @ b) / er) ** 2).sum())
        if cc <= c2 + 1: lo = min(lo, x2); hi = max(hi, x2); cs.append(b[0])
    print(f"{sel or 'band + tube':12s}: chi2 {c2:6.2f} / {n - 3}   asymptotic price c = {c:.5f} (range over chi2+1: {min(cs):.5f} .. {max(cs):.5f})   B = {B:.4f}   xi = {xi:.2f} ({lo:.2f} .. {hi:.2f}) lattice units")
    if sel is None:
        for l1, l2, m, er, p, src in chi(c, B, xi)[1]: print(f"     {src}  {l1:4.1f} -> {l2:4.1f}   measured {m:.5f} +- {er:.5f}   curve {p:.5f}   ({(m - p) / er:+.1f} s)")
        print("     curve at 10, 12, 16, 20 units:", ' '.join(f"{c + B * math.exp(-x / xi):.5f}" for x in (10, 12, 16, 20)),
              f";  ln tau(120-cell tube) = 22.1557 + 12 x price(9 -> 10) = {22.1557 + 12 * (c + B * xi * (math.exp(-9 / xi) - math.exp(-10 / xi))):.3f}")
# Alternative: a power-law prefactor, S(l) = a + 12 c l + p ln l, price between l1 and l2 = c + p ln(l2/l1) / (12 (l2 - l1)).
print("\npower-law prefactor instead (price = c + p ln(l2/l1)/(12 (l2 - l1))):")
for sel in (None, 'band', 'tube'):
    P = [p for p in pts if not sel or p[4] == sel]
    X = np.array([[1, math.log(p[1] / p[0]) / (12 * (p[1] - p[0]))] for p in P]); yy = np.array([p[2] for p in P]); er = np.array([p[3] for p in P])
    b, *_ = np.linalg.lstsq(X / er[:, None], yy / er, rcond=None); res = (yy - X @ b) / er
    cov = np.linalg.inv((X / er[:, None]).T @ (X / er[:, None]))
    print(f"{sel or 'band + tube':12s}: chi2 {float((res**2).sum()):6.2f} / {len(P) - 2}   c = {b[0]:.5f} +- {cov[0,0]**0.5:.5f}   p = {b[1]:.3f} +- {cov[1,1]**0.5:.3f}"
          + (f"   120-cell tube: {22.1557 + 12 * b[0] + b[1] * math.log(10 / 9):.3f};  L = 12, 16, 20, 30: " + ' '.join(f"{22.1557 + 12 * b[0] * (x - 9) + b[1] * math.log(x / 9):.2f}" for x in (12, 16, 20, 30)) if sel != 'band' else ''))
    if sel is None: print("     residuals (sigma):", ' '.join(f"{r:+.1f}" for r in res))
