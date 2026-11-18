#!/usr/bin/env python3
"""Referee's own slab graph (agent ref-slab), from docs/AUTOMATON.md section 2 only.

Vessel: 8 consecutive {111} layers of gump (doubled coordinates p, exactly one odd; s = x + y + z = 2 l + 1,
l = 0..7), everything outside dead for ever (T2), periodic under the cube translations (X, Y, -X - Y) for (X, Y) in
the lattice spanned by (H, K) and (0, D).  A = 3 H D cells per layer.

Cells are numbered layer by layer in the order in which a scan of doubled coordinates meets a new class (NOT the
closed formula of split-slab's geom.py); neighbours come from the doubled offsets directly.

    python3 rgeom.py H K D out.graph [swap]      # int32: n, A, then n*12 neighbour ids (n = dead outside)
"""
import sys
import numpy as np

NL = 8


def nbr_offsets(a):
    """section 2: 4 coplanar corner-touching (+-2 e_b +- 2 e_c), 8 perpendicular edge-sharing (+-e_a +- e_b, +-e_a +- e_c)."""
    b, c = [(a + 1) % 3, (a + 2) % 3]
    out = []
    for u in (-2, 2):
        for v in (-2, 2):
            o = [0, 0, 0]; o[b] = u; o[c] = v; out.append(o)
    for u in (-1, 1):
        for w in (b, c):
            for v in (-1, 1):
                o = [0, 0, 0]; o[a] = u; o[w] = v; out.append(o)
    return out


def canon(p, H, K, D):
    """class of the doubled point p under the translations 2 (X, Y, -X - Y), (X, Y) in <(H, K), (0, D)>: the
    representative with 0 <= x < 2H and then 0 <= y < 2D (z follows from s)."""
    x, y, z = p
    s = x + y + z
    m = x // (2 * H)                    # remove m (H, K)
    x -= 2 * H * m; y -= 2 * K * m
    y %= 2 * D                          # remove multiples of (0, D)
    return (x, y, s - x - y)


def build(H, K, D):
    A = 3 * H * D
    ids = {}
    cells = []
    for l in range(NL):
        s = 2 * l + 1
        for x in range(2 * H):
            for y in range(2 * D):
                z = s - x - y
                if (x % 2) + (y % 2) + (z % 2) == 1:
                    assert canon((x, y, z), H, K, D) == (x, y, z)
                    ids[(x, y, z)] = len(cells); cells.append((x, y, z))
        assert len(cells) == (l + 1) * A, (len(cells), l, A)
    n = len(cells)
    nb = np.full((n, 12), n, np.int32)
    for c, p in enumerate(cells):
        a = [t for t in range(3) if p[t] % 2][0]
        for t, o in enumerate(nbr_offsets(a)):
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            l2 = (sum(q) - 1) // 2
            if 0 <= l2 < NL:
                nb[c, t] = ids[canon(q, H, K, D)]
    # T1 for interior layers, symmetry of the relation
    lay = np.arange(n) // A
    for c in range(n):
        if 2 <= lay[c] <= 5:
            h = sorted(int(lay[x] - lay[c]) for x in nb[c])
            assert h == [-2, -1, -1, 0, 0, 0, 0, 0, 0, 1, 1, 2], h
        for x in nb[c]:
            if x < n:
                assert (nb[x] == c).sum() == (nb[c] == x).sum()
    return A, n, nb, cells, ids


def step_np(x, nb):
    xe = np.append(x, 0).astype(np.int16)
    c = xe[nb].sum(1)
    return (((x == 0) & ((c == 4) | (c == 5))) | ((x == 1) & (c >= 3) & (c <= 5))).astype(np.uint8)


if __name__ == '__main__':
    H, K, D = map(int, sys.argv[1:4])
    A, n, nb, cells, ids = build(H, K, D)
    if len(sys.argv) > 5 and sys.argv[5] == 'swap':      # negative control: one neighbour entry replaced
        c = 3 * A + 7
        nb[c, 5] = (nb[c, 5] + 2) % n
    with open(sys.argv[4], 'wb') as f:
        np.array([n, A], np.int32).tofile(f); nb.astype(np.int32).tofile(f)
    print(f'({H},{K}),(0,{D}): A = {A}, n = {n}')
