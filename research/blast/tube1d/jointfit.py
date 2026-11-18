#!/usr/bin/env python3
"""The trace reading (PI, after agent `image`): one constrained transfer operator for bands and closed tubes.
  tube (levels, anchors, L = 5..9):  ln tau(L) = a_t + s L - ln(1 + K_t exp(-L/xi)),  K_t an integer if the trace reading holds
  band (slopes between consecutive widths, pooled over five runs, errors from the runs):
                                      S(w)      = a_b + s w - ln(1 + K_b exp(-w/xi)),  K_b free
One s = 12 c_inf and one xi for both.   python3 jointfit.py data/band_g12_pooled.slopes [WMIN]
"""
import sys, math
import numpy as np
WMIN = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
T = [(5, 12.4166, 0.0031), (6, 14.8753, 0.0140), (7, 17.3175, 0.0031), (8, 19.7405, 0.0059), (9, 22.1557, 0.0121)]
B = [tuple(map(float, l.split())) for l in open(sys.argv[1]) if l[0].isdigit()]
B = [(a, b, p, max(e, 0.0005)) for a, b, p, e in B if a >= WMIN and b <= 7.0]
def fit(Kt, Kb, xi, sep=False):
    """weighted linear least squares in (a_t, s) [and a separate s_b if sep]"""
    rows = []; rhs = []
    for L, y, e in T: rows.append([1 / e, L / e] + ([0] if sep else [])); rhs.append((y + math.log1p(Kt * math.exp(-L / xi))) / e)
    for a, b, p, e in B:
        d = 12 * (b - a) * e
        r = [0, 0, (b - a) / d] if sep else [0, (b - a) / d]
        rows.append(r); rhs.append((p * 12 * (b - a) + math.log1p(Kb * math.exp(-b / xi)) - math.log1p(Kb * math.exp(-a / xi))) / d)
    X = np.array(rows); z = np.array(rhs); c, *_ = np.linalg.lstsq(X, z, rcond=None); res = z - X @ c
    return float((res ** 2).sum()), c, res
XI = np.arange(0.8, 6.01, 0.05); KB = np.exp(np.arange(-3, 5.01, 0.1))
print(f"# tubes: 5 anchors (levels); bands: {len(B)} slopes from {WMIN} to 7 units; one s and one xi unless stated")
for Kt in (1.0, 2.0, 3.0, None):
    best = None
    for xi in XI:
        for Kb in KB:
            for K in ([Kt] if Kt else np.exp(np.arange(-2, 3.01, 0.1))):
                c2, c, res = fit(K, Kb, xi)
                if best is None or c2 < best[0]: best = (c2, xi, Kb, K, c, res)
    c2, xi, Kb, K, c, res = best
    lo = min(x for x in XI for kb in KB if fit(K if Kt else K, kb, x)[0] <= c2 + 1); hi = max(x for x in XI for kb in KB if fit(K, kb, x)[0] <= c2 + 1)
    npar = 4 if Kt else 5
    f = lambda L: c[0] + c[1] * L - math.log1p(K * math.exp(-L / xi))
    print(f"K_tube {'fixed' if Kt else 'free '} = {K:4.2f}: chi2 {c2:6.2f} / {len(T) + len(B) - npar}   c_inf = {c[1]/12:.5f}  xi = {xi:.2f} ({lo:.2f} .. {hi:.2f})  K_band = {Kb:.2f}"
          f"   tubes at 10, 12, 16, 20 units: {f(10):.3f} {f(12):.3f} {f(16):.3f} {f(20):.3f}")
    print("      residuals (sigma): tubes " + ' '.join(f"{r:+.1f}" for r in res[:len(T)]) + " | bands " + ' '.join(f"{r:+.1f}" for r in res[len(T):]))
# do band and tube want the same xi and the same s?  separate fits
bt = None
for xi in XI:
    for K in (1.0, 2.0):
        rows = [[1 / e, L / e] for L, y, e in T]; rhs = [(y + math.log1p(K * math.exp(-L / xi))) / e for L, y, e in T]
        c, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None); c2 = float(((np.array(rhs) - np.array(rows) @ c) ** 2).sum())
        print_it = False
        if bt is None or c2 < bt[0] - 1e-12: bt = (c2, xi, K, c)
print(f"tubes alone (K = 1 or 2): chi2 {bt[0]:.2f} / 2 at K = {bt[2]:.0f}, xi = {bt[1]:.2f}, c_inf = {bt[3][1]/12:.5f}")
for K in (1.0, 2.0):
    ok = [(xi, np.linalg.lstsq(np.array([[1 / e, L / e] for L, y, e in T]), np.array([(y + math.log1p(K * math.exp(-L / xi))) / e for L, y, e in T]), rcond=None)) for xi in XI]
    good = []
    for xi, (c, *_r) in ok:
        c2 = sum(((y + math.log1p(K * math.exp(-L / xi)) - c[0] - c[1] * L) / e) ** 2 for L, y, e in T)
        good.append((c2, xi, c[1] / 12))
    m = min(good); rng = [g for g in good if g[0] <= m[0] + 1]
    print(f"   tubes alone, K = {K:.0f}: best chi2 {m[0]:.2f} at xi = {m[1]:.2f}, c_inf = {m[2]:.5f}; chi2+1: xi {min(r[1] for r in rng):.2f} .. {max(r[1] for r in rng):.2f}, c_inf {min(r[2] for r in rng):.5f} .. {max(r[2] for r in rng):.5f}")
bb = None
for xi in XI:
    for Kb in KB:
        rows = []; rhs = []
        for a, b, p, e in B:
            d = 12 * (b - a) * e; rows.append([(b - a) / d]); rhs.append((p * 12 * (b - a) + math.log1p(Kb * math.exp(-b / xi)) - math.log1p(Kb * math.exp(-a / xi))) / d)
        c, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None); c2 = float(((np.array(rhs) - np.array(rows) @ c) ** 2).sum())
        if bb is None or c2 < bb[0]: bb = (c2, xi, Kb, c[0] / 12)
        if 'allb' not in dir(): allb = []
        allb.append((c2, xi, c[0] / 12))
rng = [g for g in allb if g[0] <= bb[0] + 1]
print(f"bands alone: chi2 {bb[0]:.2f} / {len(B) - 3} at xi = {bb[1]:.2f}, K_band = {bb[2]:.2f}, c_inf = {bb[3]:.5f}; chi2+1: xi {min(r[1] for r in rng):.2f} .. {max(r[1] for r in rng):.2f}, c_inf {min(r[2] for r in rng):.5f} .. {max(r[2] for r in rng):.5f}")
