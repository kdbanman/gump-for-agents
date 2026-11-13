#!/usr/bin/env python3
"""Does the tail of a living face's stationary distribution predict its death rate?

For every qsd_*.npz with deaths: the per-face hazard h (per generation; for symmetric states the whole 8-face family,
which dies at once), and the quasi-stationary distribution p_k of the outer-layer count n. Three predictions of ln h:
  (a) "endpoint": h = p_0, with p_0 the continuation of ln p_k to k = 0 by a straight line through the lowest
      measured decade of ln p_k (where the small-A data show ln p_k is linear down to k = 1);
  (b) "cut": only the part of the distribution with x = n/A >= XCUT is used (as one would have to at large A), and
      ln P(n <= xA) is extrapolated to x = 0 with a quadratic in x fitted over [XCUT, XCUT + 0.15];
  (c) "gauss": exp(-mu^2/2v) per face (the Gaussian with the measured mean and variance).
  python3 research/fluct/analyze_tail.py [XCUT]
"""
import glob, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl

XCUT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.10
rows = []
print(f'{"run":24s} {"A":>4s} {"deaths":>7s} {"ln h":>8s} {"(a) endpoint":>13s} {"(b) cut x>=%.2f" % XCUT:>15s} {"(c) gauss":>10s}   lowest x measured')
for f in sorted(glob.glob(os.path.join(fl.SCR, 'qsd_*.npz'))):
    z = np.load(f); tag = os.path.basename(f)[4:-4]
    d, e = int(z['deaths'][0]), int(z['expo'][0])
    H = z['H'].astype(float); A = len(H) - 1; N = H.sum()
    if N == 0: continue
    nf = len(z['fdeaths'])
    h = d / e / nf if d else None
    k = np.arange(A + 1); mu = (k * H).sum() / N; var = ((k - mu) ** 2 * H).sum() / N
    p = H / N
    good = np.nonzero(H >= 30)[0]; kmin = good.min()
    # (a) endpoint: line through ln p_k over the lowest decade of measured p_k (k with H>=30, up to p = 10 * p_kmin)
    sel = good[(p[good] <= 10 * p[kmin]) & (good <= kmin + max(4, A // 20))]
    if len(sel) >= 3:
        cf = np.polyfit(sel, np.log(p[sel]), 1); a_pred = cf[1] + cf[0] * (0 - 0)   # value at k = 0 (k counts cells)
    else:
        a_pred = None
    # (b) cumulative, x >= XCUT only, quadratic extrapolation in x
    cum = np.cumsum(H) / N; x = k / A
    s2 = np.nonzero((x >= XCUT) & (x <= XCUT + 0.15) & (np.cumsum(H) >= 30))[0]
    if len(s2) >= 4 and kmin / A <= XCUT:
        cf2 = np.polyfit(x[s2], np.log(cum[s2]), 2); b_pred = float(np.polyval(cf2, 0.0))
    else:
        b_pred = None
    g_pred = -mu * mu / (2 * var)
    lh = math.log(h) if h else None
    fmt = lambda v: f'{v:13.2f}' if v is not None else f'{"-":>13s}'
    print(f'{tag:24s} {A:4d} {d:7d} {lh if lh is not None else float("nan"):8.2f} {fmt(a_pred)} {fmt(b_pred):>15s} {g_pred:10.2f}   {kmin / A:.3f} (k={kmin})')
    rows.append((tag, A, d, lh, a_pred, b_pred, g_pred, kmin / A))
