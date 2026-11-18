#!/usr/bin/env python3
"""Does the passage below 0.6 P-bar get dearer at 135 cells than the trend of 45..108 cells?

    python3 research/blast/split-hull/bend.py

c(p1 -> p2) = ln nu(p1 P-bar) - ln nu(p2 P-bar) is the cost of the passage from p1 P-bar down to p2 P-bar (it is also
ln q(p2) - ln q(p1)); plain-running tables only (runs/brute_R*.txt, pooled as in levels.py), no lifetime needed.
For each passage: the values at R = 9..15, their weighted straight line in the area, and the measured value at
R = 17 and 19 minus that line. If -ln q(0.6) bends up by 0.18 at 135 cells, the excess must show in these passages
or below the deepest level plain running reaches there (0.4 P-bar).
"""
import glob, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'runs')
AREA = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165, 21: 198}


def brute(R):
    cnt, expo, bases = {}, {}, []
    for f in sorted(glob.glob(os.path.join(RUNS, f'brute_R{R}.txt')) + glob.glob(os.path.join(RUNS, f'brute_R{R}_*.txt'))):
        tab, base = {}, None
        for line in open(f):
            t = line.split()
            if t[:2] == ['#', 'PBAR']:
                base = {k: float(v) for k, v in zip(t[1::2], t[2::2])}
            elif t and t[0] == 'E':
                tab[int(t[4])] = float(t[6])
        if base is None or not tab:
            continue
        bases.append(base)
        for L in range(0, max(tab) + 1):
            cnt[L] = cnt.get(L, 0.0) + tab.get(L, 0.0); expo[L] = expo.get(L, 0.0) + base['exposure']
    E = sum(b['exposure'] for b in bases)
    return sum(b['PBAR'] * b['exposure'] for b in bases) / E, cnt, expo


def lnnu(R, p):
    P, cnt, expo = T[R]; x = p * P; lo = int(math.floor(x))
    if cnt.get(lo, 0) < 20 or cnt.get(lo + 1, 0) < 20:
        return None
    a = math.log(cnt[lo] / expo[lo]); b = math.log(cnt[lo + 1] / expo[lo + 1])
    return a + (x - lo) * (b - a), 1 / math.sqrt(cnt[lo])


T = {R: brute(R) for R in AREA}
for p1, p2 in ((0.85, 0.6), (0.6, 0.5), (0.5, 0.4), (0.4, 0.3), (0.6, 0.4)):
    pts = {}
    for R in AREA:
        a, b = lnnu(R, p1), lnnu(R, p2)
        if a and b:
            pts[R] = (a[0] - b[0], math.sqrt(a[1] ** 2 + b[1] ** 2 + 2 * 0.004 ** 2))
    fitR = [R for R in (9, 11, 13, 15) if R in pts]
    if len(fitR) < 3:
        continue
    x = np.array([AREA[R] for R in fitR], float); y = np.array([pts[R][0] for R in fitR]); w = np.array([1 / pts[R][1] ** 2 for R in fitR])
    X = np.vstack([np.ones(len(x)), x]).T; C = np.linalg.inv(X.T @ (w[:, None] * X)); co = C @ X.T @ (w * y)
    chi2 = float((w * (y - X @ co) ** 2).sum())
    s = f'passage {p1} -> {p2}: ' + ', '.join(f'{pts[R][0]:.3f}' for R in fitR) + f' at R = {fitR[0]}..{fitR[-1]}; line slope {co[1]:.5f} per cell (chi2 {chi2:.1f} on {len(fitR) - 2})'
    for R in (17, 19, 21):
        if R in pts:
            xx = np.array([1.0, AREA[R]]); pred = float(xx @ co); e = math.sqrt(float(xx @ C @ xx) + pts[R][1] ** 2)
            s += f';  R = {R}: {pts[R][0]:.3f}, line {pred:.3f}, excess {pts[R][0] - pred:+.3f} +- {e:.3f}'
    print(s)
