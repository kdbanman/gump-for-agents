#!/usr/bin/env python3
"""Graph of the hull dice chain for hd.c (research/blast/split-hull, "Dice under the hull").

    python3 hullgeom.py R out.bin        prints: R A NR ND   (int32 LE file: n, A, nbr[n * 12]; n = "outside, dead")

Cells: doubled coordinates with exactly one odd, |x| + |y| + |z| <= R (the hull), and depth
r = (R - (x + y + z)) / 2 <= 7 beneath the watched face x + y + z = R.  Order: the watched face (r = 0, A cells),
then r = 1..5 (true rule; NR cells with the face), then r = 6, 7 (dice; ND cells).  A rule cell's neighbours are
the oracle's twelve; one outside the hull is dead (index n); none can be deeper than r = 7 (T1).  Dice cells have
no neighbours in the table (they are never stepped).
"""
import sys
import numpy as np


def offsets(axis):
    a = axis; b, c = [i for i in range(3) if i != a]; offs = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs


def build(R, WDEPTH=6):
    cells = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if (x % 2) + (y % 2) + (z % 2) == 1 and abs(x) + abs(y) + abs(z) <= R:
                    r = (R - (x + y + z)) // 2
                    if r <= WDEPTH + 1:
                        cells.append((0 if r == 0 else 1 if r < WDEPTH else 2, x, y, z))
    cells.sort()
    idx = {c[1:]: i for i, c in enumerate(cells)}
    n = len(cells); A = sum(c[0] == 0 for c in cells); NR = sum(c[0] < 2 for c in cells)
    nbr = np.full((n, 12), n, np.int32)
    for i, (cls, x, y, z) in enumerate(cells):
        if cls == 2:
            continue
        a = 0 if x % 2 else 1 if y % 2 else 2
        for t, o in enumerate(offsets(a)):
            q = (x + o[0], y + o[1], z + o[2])
            if abs(q[0]) + abs(q[1]) + abs(q[2]) <= R:
                assert q in idx, (cells[i], q)
                nbr[i, t] = idx[q]
    return A, NR, n - NR, nbr, cells


if __name__ == '__main__':
    R = int(sys.argv[1])
    A, NR, ND, nbr, cells = build(R)
    with open(sys.argv[2], 'wb') as f:
        np.array([NR + ND, A], np.int32).tofile(f); nbr.astype(np.int32).tofile(f)
    print(R, A, NR, ND)
