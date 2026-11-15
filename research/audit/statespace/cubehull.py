#!/usr/bin/env python3
"""Tight diagonal hull of the closed cube of side n (cells with every doubled coordinate in [1, 2n+1]), its cell
count and the cell count of its outermost {111} layer on each of the 8 signed diagonals.  cubehull.py n..."""
import sys
import numpy as np
AX = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)])
for n in map(int, sys.argv[1:]):
    lo, hi = 1, 2 * n + 1
    r = np.arange(lo, hi + 1); G = np.array(np.meshgrid(r, r, r, indexing='ij')).reshape(3, -1).T
    seed = G[(G & 1).sum(1) == 1]
    s = seed @ AX.T; b = [(int(s[:, d].min()), int(s[:, d].max())) for d in range(4)]
    R = 8 * n; r = np.arange(-R, R + 1); G = np.array(np.meshgrid(r, r, r, indexing='ij')).reshape(3, -1).T
    G = G[(G & 1).sum(1) == 1]; t = G @ AX.T
    ins = np.all([(t[:, d] >= b[d][0]) & (t[:, d] <= b[d][1]) for d in range(4)], 0)
    faces = [int((ins & (t[:, d] == b[d][k])).sum()) for d in range(4) for k in (0, 1)]
    print(f'side {n}: seed {len(seed)} cells (3n^2(n+1) = {3*n*n*(n+1)}), hull bounds {b}, hull cells {int(ins.sum())}, '
          f'outer-layer cells per face {sorted(set(faces))}')
