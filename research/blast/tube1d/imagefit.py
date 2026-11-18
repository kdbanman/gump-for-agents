#!/usr/bin/env python3
"""Does one image sum over the period lattice describe the wrapped faces?  (blast/tube1d, 2026-11-18)

Rows: PERIODIC entries of research/constant/out/points.txt with shortest loop^2 >= QMIN, at most FWMAX % of lives
ended by a firewall and A >= AMIN, replaced or completed by the anchors of research/blast/BRIEF-COMMON.md.

  M0 (the wrapping law on file):  ln tau = a + c A - kappa A F,          F = sum over +-v of f(|v|^2)
  M1 (M0 + image sum):            ln tau = a + c A - kappa A F - ln(1 + sum over v != 0 of exp(-|v|/xi))
  M2 (image sum alone):           ln tau = a + c A               - ln(1 + sum over v != 0 of exp(-|v|/xi))

    python3 imagefit.py [AMIN] [QMIN] [FWMAX]
"""
import re, sys, math
import numpy as np
AMIN = int(sys.argv[1]) if len(sys.argv) > 1 else 57
QMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 12
FWMAX = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0
FTAB = {9: 0.006267, 12: 0.002317, 13: 0.001605, 16: 0.000768, 19: 0.000275, 21: 0.000181, 25: 0.000079, 27: 0.000029, 28: 0.000029}
def Q(x, y): return x * x + x * y + y * y
def vecs(h, k, d, R=30):
    out = []
    for m in range(-R, R + 1):
        for j in range(-6 * R, 6 * R + 1):
            x, y = m * h, m * k + j * d
            if x == 0 and y == 0: continue
            q = Q(x, y)
            if q <= 3600: out.append(q)
    return np.array(sorted(out))
def F(qs): return sum(FTAB.get(int(q), 0.0) for q in qs) / 2      # one per +-v
def S(qs, xi): return float(np.exp(-np.sqrt(qs) / xi).sum())
rows = {}
pat = re.compile(r'^\s*(\d+)\s+\((\d+), (\d+), (\d+)\)\s+\((\d+), (\d+), (\d+)\)\s+(\S+x\S+)?\s*([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)')
for l in open('../../constant/out/points.txt'):
    if l.startswith('HULL'): break
    m = pat.match(l)
    if not m: continue
    A, q1, b2, q2, h, k, d = map(int, m.group(1, 2, 3, 4, 5, 6, 7)); y, se, fw = float(m.group(9)), float(m.group(10)), float(m.group(12))
    if A < AMIN or q1 < QMIN or fw > FWMAX: continue
    rows[(A, q1, b2, q2)] = (A, h, k, d, y, se, 'table')
def gram(h, k, d):
    qs = vecs(h, k, d, 14); return int(qs[0])
anch = [(57, 1, 7, 19, 11.8751, 0.0004), (63, 1, 4, 21, 13.1622, 0.0007), (75, 1, 3, 25, 15.5250, 0.0028), (75, 1, 9, 25, 15.6442, 0.0030),
        (78, 1, 4, 26, 16.2884, 0.0033), (84, 1, 12, 28, 17.3175, 0.0031), (84, 1, 4, 28, 17.5387, 0.0031), (96, 1, 17, 32, 19.7405, 0.0059),
        (108, 1, 16, 36, 22.1557, 0.0121), (108, 6, 0, 6, 22.5405, 0.0074)]
for A, h, k, d, y, se in anch:
    if A < AMIN: continue
    qs = vecs(h, k, d, 14); key = (A, int(qs[0]), 'anchor', h * 1000 + k)
    for kk in list(rows):
        if kk[0] == A and kk[1] == int(qs[0]) and rows[kk][1:4] == (h, k, d): del rows[kk]
    rows[key] = (A, h, k, d, y, se, 'anchor')
R = sorted(rows.values())
V = [vecs(h, k, d) for A, h, k, d, y, se, src in R]
y = np.array([r[4] for r in R]); se = np.array([max(r[5], 0.003) for r in R]); Aa = np.array([r[0] for r in R], float)
Fv = np.array([F(v[v <= 28]) for v in V])
def fit(cols, off):
    X = np.column_stack(cols) / se[:, None]; b, *_ = np.linalg.lstsq(X, (y - off) / se, rcond=None)
    res = (y - off) - np.column_stack(cols) @ b; return b, res, float(((res / se) ** 2).sum())
one = np.ones_like(Aa)
b0, r0, c0 = fit([one, Aa, -Aa * Fv], 0 * y)
print(f"{len(R)} faces (A >= {AMIN}, shortest loop^2 >= {QMIN}, firewall share <= {FWMAX}%; errors floored at 0.003)")
print(f"M0  a + cA - kappa A F:            chi2 {c0:8.1f} / {len(R)-3}   a {b0[0]:+.4f} c {b0[1]:.5f} kappa {b0[2]:.3f}   rms residual {np.sqrt((r0**2).mean()):.4f}")
best = {}
for name, cols in (('M1', lambda: [one, Aa, -Aa * Fv]), ('M2', lambda: [one, Aa])):
    bx = None
    for xi in np.arange(0.6, 6.01, 0.05):
        off = -np.log1p(np.array([S(v, xi) for v in V]))
        b, r, c = fit(cols(), off)
        if bx is None or c < bx[0]: bx = (c, xi, b, r)
    best[name] = bx
    c, xi, b, r = bx
    extra = f" kappa {b[2]:.3f}" if len(b) > 2 else ""
    print(f"{name}  ... - ln(1 + sum exp(-|v|/xi)):  chi2 {c:8.1f} / {len(R)-len(b)-1}   a {b[0]:+.4f} c {b[1]:.5f}{extra} xi {xi:.2f}   rms residual {np.sqrt((r**2).mean()):.4f}")
print("\n   A  lattice        shortest  ln tau    se     M0 resid  M1 resid  M2 resid  src")
for i, (A, h, k, d, yy, s, src) in enumerate(R):
    print(f" {A:4d}  ({h},{k}),(0,{d})".ljust(22) + f" {int(V[i][0]):3d}   {yy:8.4f} {s:.4f}   {r0[i]:+.4f}   {best['M1'][3][i]:+.4f}   {best['M2'][3][i]:+.4f}   {src}")
print("\nforecasts (faces not in the fit):")
for A, h, k, d, note in ((120, 1, 18, 40, 'tube loop^2 12, blind'), (96, 1, 3, 32, 'loop^2 13'), (96, 1, 8, 32, 'loop^2 16'), (96, 4, 0, 8, 'loop^2 16, 4x8'), (144, 1, 22, 48, 'tube 12, L=12'),
                         (192, 1, 30, 64, 'tube 12, L=16'), (240, 1, 38, 80, 'tube 12, L=20'), (360, 1, 58, 120, 'tube 12, L=30'), (111, 1, 10, 37, 'wide'), (126, 6, 0, 7, 'wide 6x7'), (147, 7, 0, 7, 'wide 7x7')):
    v = vecs(h, k, d); f = F(v[v <= 28]); out = [b0[0] + b0[1] * A - b0[2] * A * f]
    for name in ('M1', 'M2'):
        c, xi, b, r = best[name]; out.append(b[0] + b[1] * A - (b[2] * A * f if len(b) > 2 else 0) - math.log1p(S(v, xi)))
    print(f"  {A:4d} ({h},{k}),(0,{d}) {note:24s} M0 {out[0]:8.3f}   M1 {out[1]:8.3f}   M2 {out[2]:8.3f}")
