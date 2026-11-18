#!/usr/bin/env python3
"""Referee's own graph of the hull dice chain, written from docs/AUTOMATON.md section 2 (doubled coordinates).

    python3 geom.py R WD out.bin [SWAP]   -> prints: R A NRULE NDICE n
       WD   = number of rule layers (depth 0..WD-1 true rule; depth WD, WD+1 coins; deeper cells absent).
              WD = 99: the whole hull, no coins (the deterministic vessel, for validation against the oracle).
       SWAP = 1: negative control, one neighbour of one face cell replaced by a wrong cell.
    File: int32 n, A, NRULE, then int32 nbr[NRULE*12] (index n = outside the hull, dead), then int32 xyz[n*3].
Depth of a cell: r = (R - (x+y+z))/2 beneath the watched face x+y+z = R.  Order: depth 0, 1, 2, ...
"""
import sys
import numpy as np


def nbrs(p):
    """12 neighbours of a face with odd (normal) coordinate a: 4 coplanar corner-touching, 8 perpendicular edge-sharing."""
    a = [i for i in range(3) if p[i] % 2][0]
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (-2, 2):
        for sc in (-2, 2):
            q = list(p); q[b] += sb; q[c] += sc; out.append(tuple(q))
    for sa in (-1, 1):
        for t in (b, c):
            for st in (-1, 1):
                q = list(p); q[a] += sa; q[t] += st; out.append(tuple(q))
    return out


def build(R, WD, swap=0):
    cells = []
    rng = range(-R, R + 1)
    for x in rng:
        for y in rng:
            for z in rng:
                if (x & 1) + (y & 1) + (z & 1) != 1 or abs(x) + abs(y) + abs(z) > R:
                    continue
                r = (R - (x + y + z)) // 2
                if WD < 99 and r > WD + 1:
                    continue
                cells.append((r, x, y, z))
    cells.sort()
    n = len(cells)
    idx = {c[1:]: i for i, c in enumerate(cells)}
    A = sum(1 for c in cells if c[0] == 0)
    NRULE = n if WD >= 99 else sum(1 for c in cells if c[0] < WD)
    nbr = np.full((NRULE, 12), n, np.int32)
    for i in range(NRULE):
        p = cells[i][1:]
        for t, q in enumerate(nbrs(p)):
            if abs(q[0]) + abs(q[1]) + abs(q[2]) <= R:
                nbr[i, t] = idx[q]          # KeyError here would mean a rule cell reaches below the coins
    if swap:
        i = A // 2; old = nbr[i, 5]; nbr[i, 5] = (old + 7) % NRULE
    xyz = np.array([c[1:] for c in cells], np.int32)
    return n, A, NRULE, nbr, xyz


if __name__ == '__main__':
    R = int(sys.argv[1]); WD = int(sys.argv[2])
    n, A, NRULE, nbr, xyz = build(R, WD, int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    with open(sys.argv[3], 'wb') as f:
        np.array([n, A, NRULE], np.int32).tofile(f); nbr.tofile(f); xyz.tofile(f)
    print(R, A, NRULE, n - NRULE, n)
