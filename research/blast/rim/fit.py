#!/usr/bin/env python3
"""Fits to the symmetric prisms (w,w,L,0), w >= 8 even, L >= 4 (data/runs.csv), and the hull's own values.
   python3 research/blast/rim/fit.py
 (1) ln tau = a0 + c*A - alpha*w                (three numbers)
 (2) ln tau = a0 + c*A - alpha*w + beta*L       (four numbers; exact when only four points)
 The hull: ln tau(k) = a + b*k + c*A(k), A = 3k(k+1)/2, on k = 5..8, and its extrapolation to k = 9, 10."""
import csv, math, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
P = collections.OrderedDict()
for r in csv.DictReader(open(os.path.join(HERE, 'data', 'runs.csv'))):
    k = (r['vessel'], r['faces'], int(r['cells'])); e, d = P.get(k, (0.0, 0)); P[k] = (e + float(r['exposure']), d + int(r['first_deaths']))
pts = []
for (v, f, c), (e, d) in P.items():
    p = v.split('_')
    if p[0] == 'prism' and p[1] == p[2] and p[4] == '0' and int(p[1]) % 2 == 0 and int(p[1]) >= 8 and int(p[3]) >= 4 and d:
        pts.append((int(p[1]), int(p[3]), c, math.log(4 * e / d), 1 / math.sqrt(d)))
pts.sort(); w, L, A, y, s = map(np.array, zip(*pts))


def wls(X, y, s):
    Xw = X / s[:, None]; yw = y / s
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None); cov = np.linalg.inv(Xw.T @ Xw)
    chi2 = float(((yw - Xw @ beta) ** 2).sum()); return beta, np.sqrt(np.diag(cov)), chi2


for name, X in (('a0 + c A - alpha w', np.stack([np.ones(len(y)), A, -w], 1)),
                ('a0 + c A - alpha w + beta L', np.stack([np.ones(len(y)), A, -w, L], 1))):
    if len(y) < X.shape[1]: continue
    b, e, chi2 = wls(X.astype(float), y, s)
    print(f'{name}: ' + ', '.join(f'{v:.4f} +- {u:.4f}' for v, u in zip(b, e)) + f'   chi2 {chi2:.1f} on {len(y) - X.shape[1]}')
    for wi, Li, yi, si, fi in zip(w, L, y, s, X @ b): print(f'    w {wi:2d} L {Li}: {yi:.4f} +- {si:.4f}  fit {fi:.4f}  ({(yi - fi) / si:+.1f} sigma)')
hk = np.array([4, 5, 6, 7, 8]); hy = np.array([6.8054, 9.8202, 13.6346, 18.1407, 23.3392]); hs = np.array([0.0029, 0.0027, 0.0011, 0.0054, 0.0099])
hA = 1.5 * hk * (hk + 1)
b, e, chi2 = wls(np.stack([np.ones(4), hk[1:], hA[1:]], 1), hy[1:], hs[1:])
print(f'hull k = 5..8: a {b[0]:.4f} +- {e[0]:.4f}, b {b[1]:.4f} +- {e[1]:.4f} per unit k, c {b[2]:.4f} +- {e[2]:.4f}, chi2 {chi2:.2f} on 1')
for k in (9, 10): print(f'   k = {k} (A = {int(1.5 * k * (k + 1))}): {b[0] + b[1] * k + b[2] * 1.5 * k * (k + 1):.3f}')
d2 = hy[2:] - 2 * hy[1:-1] + hy[:-2]; e2 = np.sqrt(hs[2:] ** 2 + 4 * hs[1:-1] ** 2 + hs[:-2] ** 2)
print('hull second differences at k = 5, 6, 7: ' + ', '.join(f'{v:.4f} +- {u:.4f}' for v, u in zip(d2, e2)))
print('hull first differences (a row pair of length k+1 added): ' + ', '.join(f'{v:.4f}' for v in np.diff(hy)))
