#!/usr/bin/env python3
"""PR 16 review: the width fits on subsets and alternative models; where the chi^2 lives; the conjecture's b(inf).
  python3 research/audit/gpu_pr16/fits.py <dir with fwslab*.json>
"""
import glob, json, math, sys
import numpy as np
D = sys.argv[1]
by = {}
for p in sorted(glob.glob(f'{D}/fwslab*.json')):
    r = json.load(open(p)); by.setdefault(tuple(r['slab'][:2]), []).append(r)
P = []
for (N1, N2), rs in sorted(by.items()):
    E = sum(r['exposure'] for r in rs); F = sum(r['face'] for r in rs); W = sum(r['fw'] for r in rs)
    P.append(dict(N1=N1, N2=N2, s=min(N1, N2), M=max(N1, N2), A=3 * N1 * N2, y=math.log(2 * E / F), se=1 / math.sqrt(F), sh=W / (F + W)))

def fit(pts, cols, name, show=False):
    y = np.array([p['y'] for p in pts]); w = np.array([p['se'] ** -2 for p in pts])
    X = np.array([[c(p) for c in cols] for p in pts], float)
    cov = np.linalg.inv(X.T @ (X * w[:, None])); b = cov @ (X.T @ (w * y)); r = y - X @ b
    chi2 = float((w * r * r).sum()); dof = len(y) - X.shape[1]
    print(f'  {name}: chi2 {chi2:.1f} / {dof}' + ('  coefs ' + ', '.join(f'{x:.4f}±{math.sqrt(cov[i,i]):.4f}' for i, x in enumerate(b)) if show else ''))
    return b, cov, r

one = lambda p: 1.0; A = lambda p: p['A']
ind = lambda s: (lambda p: float(p['s'] == s)); indA = lambda s: (lambda p: p['A'] * (p['s'] == s))
for label, sel in [('all 15 points (6x4 separate)', lambda p: True), ('s >= 4', lambda p: p['s'] >= 4),
                   ('s >= 4 without 6x4 (orientation duplicate)', lambda p: p['s'] >= 4 and (p['N1'], p['N2']) != (6, 4)),
                   ('s = 4, 5', lambda p: p['s'] in (4, 5)), ('s >= 4, A <= 105 (no 4x9, 5x8, 6x6, 6x7)', lambda p: p['s'] >= 4 and p['A'] <= 105)]:
    pts = [p for p in P if sel(p)]; S = sorted({p['s'] for p in pts})
    print(f'{label}: {len(pts)} points, s in {S}')
    fit(pts, [one, A], 'A  a + bA', True)
    fit(pts, [ind(s) for s in S] + [A], 'O  a(s) + bA', True)
    if all(sum(p['s'] == s for p in pts) >= 2 for s in S):
        fit(pts, [ind(s) for s in S] + [indA(s) for s in S], 'W  a(s) + b(s)A', True)
    fit(pts, [one, A, lambda p: p['M']], 'a + bA + c*M (a deficit per unit of long side)', True)
    fit(pts, [one, A, lambda p: p['M'], lambda p: p['s']], 'a + bA + c*M + d*s', True)
# b(s) consistency and the conjecture
print('\nb(s) from W on all points; is b(4) = b(5) = b(6)?')
S = [3, 4, 5, 6]
b, cov, r = fit(P, [ind(s) for s in S] + [indA(s) for s in S], 'W')
bb = b[4:]; cc = cov[4:, 4:]
sub = [1, 2, 3]
ws = 1 / np.diag(cc)[sub]; m = (bb[sub] * ws).sum() / ws.sum(); chi = ((bb[sub] - m) ** 2 * ws).sum()
print(f'  weighted mean b(4..6) = {m:.4f} ± {ws.sum()**-0.5:.4f}, chi2 {chi:.2f} / 2')
for target in (0.216, 0.221):
    print(f'  b(6) - {target} = {bb[3]-target:+.4f} ± {math.sqrt(cc[3,3]):.4f}; b(5) - {target} = {bb[2]-target:+.4f} ± {math.sqrt(cc[2,2]):.4f}')
# b(s) = binf - c/s with s = 3..6, and with s = 4..6
for ss in ([0, 1, 2, 3], [1, 2, 3]):
    X = np.array([[1, -1 / S[i]] for i in ss]); w = 1 / np.diag(cc)[ss]; y = bb[ss]
    cv = np.linalg.inv(X.T @ (X * w[:, None])); be = cv @ (X.T @ (w * y)); chi = float((w * (y - X @ be) ** 2).sum())
    print(f'  b(s) = binf - c/s over s = {[S[i] for i in ss]}: binf {be[0]:.4f} ± {math.sqrt(cv[0,0]):.4f}, c {be[1]:.4f} ± {math.sqrt(cv[1,1]):.4f}, chi2 {chi:.1f} / {len(ss)-2}')
print('\nresiduals from the s-family lines vs firewall share:')
for p, ri in zip(P, r):
    print(f'  {p["N1"]}x{p["N2"]}: resid {ri:+.4f} ({ri/p["se"]:+.1f}σ), firewall share {p["sh"]:.1%}')
