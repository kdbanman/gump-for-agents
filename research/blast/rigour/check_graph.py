#!/usr/bin/env python3
"""Check geom.py's face-layer graph against reference/oracle.py (the ground truth).

The oracle's torus of side H = 2n (doubled coordinates) carries the layer x+y+z = 1 (mod H) as the wrapped face
(n,0),(0,n); with n >= 3 the other layers are dead and stay dead when only this layer is seeded (each of their
cells sees at most 3 cells of it), so the oracle then runs the one-layer automaton: the surrogate with no coins.
Compared: (i) the one-step image of 2,000 random one-layer states (densities 0.1..0.9), state for state;
(ii) 1,000 generations from 20 random states; (iii) negative control: one neighbour swapped must fail;
(iv) the layer histogram of the 12 offsets (6 in-layer, 2 at -2, 1 at -4) and the coin counts of hull faces.

    python3 check_graph.py
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'reference'))
import oracle
import geom


def run(n, swap=False, seed=0):
    H = 2 * n
    nb, m = geom.torus(n, 0, n)
    A = len(nb)
    cells = [(o, a, b) for a in range(n) for b in range(n) for o in range(3)]
    coords = [tuple(c % H for c in geom.ab_cell(o, a, b, 1)) for (o, a, b) in cells]
    assert len(set(coords)) == A
    if swap:
        j = nb[5][0]
        nb[5][0] = [x for x in range(A) if x not in nb[5] and x != 5][0]
    NB = np.array(nb)
    msk = oracle.masks(H)
    rng = np.random.default_rng(seed)

    def mine(x):
        k = x[NB].sum(1)
        return ((x == 1) & (k >= 3) & (k <= 5)) | ((x == 0) & ((k == 4) | (k == 5)))

    def orc(x):
        h = np.zeros((H, H, H), np.int8)
        for i, c in enumerate(coords):
            h[c] = x[i]
        h2 = oracle.step(h, msk)
        out = np.array([h2[c] for c in coords])
        assert h2.sum() == out.sum(), 'oracle left the layer'
        return out
    bad = 0
    for t in range(2000):
        x = (rng.random(A) < rng.uniform(0.1, 0.9)).astype(np.int8)
        if not np.array_equal(mine(x).astype(np.int8), orc(x)):
            bad += 1
    gens = 0
    for t in range(20):
        x = (rng.random(A) < 0.5).astype(np.int8)
        for g in range(1000):
            y1, y2 = mine(x).astype(np.int8), orc(x)
            if not np.array_equal(y1, y2):
                bad += 1
            x = y2; gens += 1
    return bad, gens


if __name__ == '__main__':
    for n in (3, 4):
        bad, gens = run(n)
        print('torus (%d,0),(0,%d), %d cells: one-step mismatches %d (2000 random states + %d trajectory generations)'
              % (n, n, 3 * n * n, bad, gens))
        assert bad == 0
        bad, _ = run(n, swap=True)
        print('  negative control (one neighbour swapped): %d mismatches (must be > 0)' % bad)
        assert bad > 0
    for a in range(3):
        hist = {}
        for o in geom.OFF[a]:
            hist[sum(o)] = hist.get(sum(o), 0) + 1
        assert hist == {0: 6, 2: 2, -2: 2, 4: 1, -4: 1}, hist
    print('layer histogram of the 12 offsets: 6 in-layer, 2 at -2, 1 at -4, for each orientation: ok')
    for R in (3, 5, 7, 9):
        nb, m, cells = geom.hull(R)
        k = (R + 1) // 2
        assert len(nb) == 3 * k * (k + 1) // 2
        degs = sorted(len(l) for l in nb)
        coins = {}
        for (m1, m2) in m:
            coins[(m1, m2)] = coins.get((m1, m2), 0) + 1
        print('hull R=%d: A=%d, in-layer degrees %s, coin counts (m1,m2): %s' % (R, len(nb),
              {d: degs.count(d) for d in set(degs)}, coins))
