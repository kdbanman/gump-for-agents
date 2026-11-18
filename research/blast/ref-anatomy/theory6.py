#!/usr/bin/env python3
"""The fall with its measured law in place of the Gaussian: one-step histogram of (P', B') from a box round the
peak of the minimum-action route, against the Gaussian with the histogram's own mean and covariance, at the
route's landing point after the fall.  Needs map_t48peak.txt, map_t63peak.txt (see run3.sh).
   python3 theory6.py -> out/theory6.txt"""
import os, math
os.environ['THEORY_OUT'] = 'theory6.txt'
import numpy as np, theory as th
for name, land in (('t48peak', (12, 5)), ('t63peak', (16, 7))):
    d = th.load(name); A = d['A']; J = np.zeros((128, 128))
    for (p, b), k in d['jump'].items(): J[p, b] = k
    tot = J.sum(); ps = np.arange(128)
    mp = (J.sum(1) * ps).sum() / tot; mb = (J.sum(0) * ps).sum() / tot
    vp = (J.sum(1) * ps * ps).sum() / tot - mp * mp; vb = (J.sum(0) * ps * ps).sum() / tot - mb * mb
    cpb = (J * np.outer(ps, ps)).sum() / tot - mp * mb; det = vp * vb - cpb ** 2
    PP, BB = np.meshgrid(ps, ps, indexing='ij')
    G = np.exp(-0.5 * (vb * (PP - mp) ** 2 - 2 * cpb * (PP - mp) * (BB - mb) + vp * (BB - mb) ** 2) / det) / (2 * math.pi * math.sqrt(det))
    th.pr(f'{name} (A = {A}): {tot:.0f} steps from the peak box ({d["hd"]["PS"]}+-1, {d["hd"]["BS"]}+-2); next mean ({mp:.2f}, {mb:.2f}), var {vp:.2f}, {vb:.2f}, cov {cpb:.2f}; dead next generation: {J[0].sum():.0f}')
    p, b = land
    for lab, sl in (('on the landing point', (slice(p, p + 1), slice(b, b + 1))), ('3 x 3 round it', (slice(p - 1, p + 2), slice(b - 1, b + 2))),
                    ('5 x 5 round it', (slice(p - 2, p + 3), slice(b - 2, b + 3))), ('quadrant below it (P\' <= p, B\' <= b, P\' >= 1)', (slice(1, p + 1), slice(0, b + 1))),
                    ('P\' <= p alone', (slice(1, p + 1), slice(0, 128)))):
        m = J[sl].sum(); g = G[sl].sum()
        if m > 0:
            th.pr(f'   landing ({p},{b}), {lab}: measured -ln {-math.log(m / tot):.2f} ({m:.0f} steps, +- {1/math.sqrt(m):.2f}), Gaussian {-math.log(g):.2f}, excess {-math.log(m / tot) + math.log(g):+.2f}')
        else:
            th.pr(f'   landing ({p},{b}), {lab}: none seen in {tot:.0f}; Gaussian {-math.log(g):.2f}')
th.out.close()
