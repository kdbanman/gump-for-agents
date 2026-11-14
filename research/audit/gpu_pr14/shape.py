#!/usr/bin/env python3
"""PR 14 review: firewall-resolved face channels (m = 8) against the slab line, by in-plane shape.

CPU: research/peeling/slab_fw.csv (ln tau_face = ln(2 E / peel-first), firewall-first lives censored at the firewall);
GPU: the PR's fwslab totals (research/scratch/pr14/*.json, from the branch); optional own CPU runs (cpu_channels.py).
    python3 research/audit/gpu_pr14/shape.py
"""
import csv, glob, json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
line = lambda A: -0.091 + 0.2088 * A
rows = []
for r in csv.DictReader(open(os.path.join(ROOT, 'research', 'peeling', 'slab_fw.csv'))):
    if r['m'] == '8' and int(r['A']) >= 27 and int(r['peel_first']) >= 20:
        N1, N2, A, pe, E = int(r['N1']), int(r['N2']), int(r['A']), int(r['peel_first']), float(r['exposure'])
        rows.append(('CPU', N1, N2, A, math.log(2 * E / pe), 1 / math.sqrt(pe), int(r['fw_first']) / (int(r['fw_first']) + pe)))
for p in sorted(glob.glob(os.path.join(ROOT, 'research', 'scratch', 'pr14', 'fwslab*.json'))):
    r = json.load(open(p)); N1, N2, _ = r['slab']
    rows.append(('GPU', N1, N2, 3 * N1 * N2, math.log(2 * r['exposure'] / r['face']), 1 / math.sqrt(r['face']), r['fw'] / (r['fw'] + r['face'])))
rows.sort(key=lambda x: (min(x[1], x[2]), x[3]))
print('src  slab  A   min side  ln tau_face        line    resid   fw share')
for s, N1, N2, A, y, e, sh in rows:
    print(f'{s}  {N1}x{N2:<2} {A:4d}  {min(N1, N2):3d}   {y:7.3f} +- {e:.3f}  {line(A):7.3f}  {y - line(A):+.3f}   {sh:.1%}')

# Is the offset at A = 108, 126 (min side 6) a slope change or a min-side effect? Fit the CPU rows (min side 3-5,
# excluding the 2- and 3-wide elongated 2x8, 3x8) with and without a min-side term, predict min side 6.
import numpy as np
cpu = [r for r in rows if r[0] == 'CPU' and (r[1], r[2]) not in ((2, 8), (3, 8))]
A = np.array([r[3] for r in cpu], float); S = np.array([min(r[1], r[2]) for r in cpu], float)
y = np.array([r[4] for r in cpu]); w = 1 / np.array([r[5] for r in cpu]) ** 2
for name, X, x108, x126 in [('a + bA', np.c_[np.ones_like(A), A], [1, 108], [1, 126]),
                            ('a + bA + c minside', np.c_[np.ones_like(A), A, S], [1, 108, 6], [1, 126, 6])]:
    cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y))
    chi2 = float((w * (y - X @ beta) ** 2).sum())
    pr = [(float(np.dot(x, beta)), math.sqrt(np.dot(x, cov @ x))) for x in (np.array(x108), np.array(x126))]
    print(f'{name}: beta {np.round(beta, 4).tolist()} +- {np.round(np.sqrt(np.diag(cov)), 4).tolist()}, chi2 {chi2:.1f}/{len(y) - X.shape[1]};'
          f' predicts 6x6x8 {pr[0][0]:.3f} +- {pr[0][1]:.3f}, 6x7x8 {pr[1][0]:.3f} +- {pr[1][1]:.3f}')
