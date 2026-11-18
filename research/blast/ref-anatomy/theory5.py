#!/usr/bin/env python3
"""The jump with its measured law in place of the Gaussian (what the PI asked for if the Gaussian action fails).
For each face: the one-step histogram of (P', B') from the launch box (fd2.c), against the Gaussian with that
histogram's own mean and covariance, at the landing point of the minimum-action route (equal fillings on every
size) and on the quadrant beyond it.   python3 theory5.py -> out/theory5.txt"""
import os, math
os.environ['THEORY_OUT'] = 'theory5.txt'
import numpy as np, theory as th
LAND = {'t48': (35, 32), 't63': (46, 42), 't84': (61, 56), 'tube60': (44, 40), 'tube84': (61, 56), 't60': None}
S_G = {'t48': 7.776, 't63': 10.052, 't84': 13.653}
rows = {}
for name in ('t48', 't63', 't84', 'tube60', 'tube84'):
    d = th.load(name); A = d['A']; J = np.zeros((128, 128))
    for (p, b), k in d['jump'].items(): J[p, b] = k
    tot = J.sum(); ps = np.arange(128)
    mp = (J.sum(1) * ps).sum() / tot; mb = (J.sum(0) * ps).sum() / tot
    vp = (J.sum(1) * ps * ps).sum() / tot - mp * mp; vb = (J.sum(0) * ps * ps).sum() / tot - mb * mb
    cpb = (J * np.outer(ps, ps)).sum() / tot - mp * mb; det = vp * vb - cpb ** 2
    PP, BB = np.meshgrid(ps, ps, indexing='ij')
    G = np.exp(-0.5 * (vb * (PP - mp) ** 2 - 2 * cpb * (PP - mp) * (BB - mb) + vp * (BB - mb) ** 2) / det) / (2 * math.pi * math.sqrt(det))
    p, b = LAND[name]
    th.pr(f'{name} (A = {A}): {tot:.0f} steps from the box ({d["hd"]["PS"]}+-1, {d["hd"]["BS"]}+-2); next mean ({mp:.2f}, {mb:.2f}), var {vp:.2f}, {vb:.2f}, cov {cpb:.2f}')
    out = []
    for lab, sl in (('on the landing point', (slice(p, p + 1), slice(b, b + 1))), ('3 x 3 round it', (slice(p - 1, p + 2), slice(b - 1, b + 2))),
                    ('5 x 5 round it', (slice(p - 2, p + 3), slice(b - 2, b + 3))), ('quadrant beyond it', (slice(p, 128), slice(b, 128)))):
        m = J[sl].sum(); g = G[sl].sum()
        if m > 0:
            dm = -math.log(m / tot) + math.log(g); out.append(dm)
            th.pr(f'   landing ({p},{b}) = fillings ({p/A:.3f}, {b/A:.3f}), {lab}: measured -ln {-math.log(m / tot):.2f} ({m:.0f} steps, +- {1/math.sqrt(m):.2f}), Gaussian {-math.log(g):.2f}, excess {dm:+.2f}')
        else:
            out.append(float('nan')); th.pr(f'   {lab}: none seen; Gaussian {-math.log(g):.2f}')
    rows[name] = out
th.pr('== the jump\'s excess over the Gaussian (5 x 5 round the landing point; quadrant), and the minimum action with it')
for n in ('t48', 't63', 't84'):
    A = {'t48': 48, 't63': 63, 't84': 84}[n]
    th.pr(f'   {n}: excess {rows[n][2]:+.2f} (5x5), {rows[n][3]:+.2f} (quadrant); Gaussian S {S_G[n]:.2f}; with the measured jump {S_G[n] + rows[n][2]:.2f} = {(S_G[n] + rows[n][2]) / A:.4f} per cell (5x5), {S_G[n] + rows[n][3]:.2f} = {(S_G[n] + rows[n][3]) / A:.4f} (quadrant)')
for k, lab in ((2, '5x5'), (3, 'quadrant')):
    y = [S_G[n] + rows[n][k] for n in ('t48', 't63', 't84')]
    sl = np.polyfit([48, 63, 84], y, 1)
    th.pr(f'   slope of the minimum action with the measured jump ({lab}): {sl[0]:.4f} per cell, intercept {sl[1]:+.2f}; between 63 and 84 alone: {(y[2] - y[1]) / 21:.4f}; excess alone grows by {(rows["t84"][k] - rows["t63"][k]) / 21:.4f} per cell (63 to 84), {(rows["t63"][k] - rows["t48"][k]) / 15:.4f} (48 to 63)')
th.out.close()
