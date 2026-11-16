#!/usr/bin/env python3
"""Attacks on the wrapping law with the data on file (research/wrap).  python3 research/wrap/attack.py [--corr] [--wrap]

1. W3 on file: free discounts for loop^2 21, 25, 27, 28 (LAW form, A0 profiled).
2. The equal-area pairs (SH2, SH4, SH6): law difference against measured difference.
3. Separate A0 per loop length vs common A0, and a pair term for two short directions.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fit as Fm  # noqa: E402

corr = '--corr' in sys.argv
pts = Fm.select('all', corr, wrap='--wrap' in sys.argv)
print(f'{len(pts)} faces, corr={corr}')
for qs in (Fm.QS, Fm.QS + [21], Fm.QS + [21, 25], Fm.QS + [21, 25, 27, 28]):
    chi, a0, b, cov, r = Fm.fitmodel(pts, 'LAW', qs)
    e = np.sqrt(np.diag(cov))
    print(f'LAW k for {qs}: chi2 {chi:.1f} on {len(pts) - 3 - len(qs)}, A0 = {a0}; ' +
          ' '.join(f'k{q}={x:.5f}({ee:.5f})' for q, x, ee in zip(qs, b[2:], e[2:])))
for qs in (Fm.QS + [21], Fm.QS + [21, 25, 27, 28]):
    chi, a0, b, cov, r = Fm.fitmodel(pts, 'OFF2', qs)
    print(f'OFF2 with {qs}: chi2 {chi:.1f} on {len(pts) - 2 - 2 * len(qs)}')

# pairs: same A, both members measured
def find(A, g):
    for p in pts:
        if p['A'] == A and p['g'] == g:
            return p
pairs = [(48, (12, 0, 16), (12, 12, 19), 'SH2 A=48 (12,16) - (12,19,19)'),
         (48, (16, 16, 16), (12, 12, 19), 'SH4 4x4 - (12,19,19)'),
         (60, (16, 4, 19), (16, 12, 21), 'SH2 A=60 (16,19) - 4x5 (16)'),
         (60, (12, 0, 25), (12, 12, 28), 'W6 A=60 loop12 pair'),
         (72, (16, 0, 27), (16, 8, 28), 'SH6 T01-type (1,6,24)-(2,4,12)'),
         (72, (16, 16, 31), (16, 8, 28), 'SH6 (1,5,24)-(2,4,12)'),
         (72, (12, 0, 36), (12, 12, 39), 'SH6 N72 loop12 pair')]
chi, a0, b, cov, r = Fm.fitmodel(pts, 'LAW')
X = Fm.design(pts, 'LAW', a0)
fitv = {(p['A'], p['g']): v for p, v in zip(pts, X @ b)}
for A, g1, g2, lab in pairs:
    p1, p2 = find(A, g1), find(A, g2)
    if not (p1 and p2):
        continue
    dm = p1['y'] - p2['y']; de = math.hypot(p1['se'], p2['se'])
    dl = Fm.frozen(p1) - Fm.frozen(p2)
    print(f'{lab:36s} measured {dm:+.4f} ± {de:.4f}   frozen law {dl:+.4f}   ({(dm - dl) / de:+.1f} se)')
