#!/usr/bin/env python3
"""Slab torus for the wrapped-face rows (third task, item 4), written from docs/AUTOMATON.md and reference/oracle.py.

8 consecutive {111} layers: cubes (i, j, k) with l = i + j + k in 0..7, a cell = the face of cube (i, j, k) on its +a
side, doubled coordinates p = 2 (i, j, k) + e_a. Periodic in the plane under the cube translations (x, y, -x - y) for
(x, y) in the lattice spanned by (H, K) and (0, D); A = 3 H D cells a layer; everything outside the 8 layers dead
(T2 keeps it so). Cell id = (l H D + i' D + j') 3 + a. Layer 0 (the watched face) is ids [0, A), layer 7 [7A, 8A).
The construction follows research/blast/split-slab/geom.py (same ids), re-derived here; validate_slab.py checks the
stepper built on it against the oracle on a covering cubic torus.

    python3 slabgeom.py H K D out.bin        # int32: n, A, then nbr[n][12] (n = outside, dead)
"""
import sys
import numpy as np
M = 8


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


def reduce(i, j, H, K, D):
    q = i // H
    return i - q * H, (j - q * K) % D


def cid(l, i, j, a, H, K, D):
    i, j = reduce(i, j, H, K, D)
    return (l * H * D + i * D + j) * 3 + a


def build(H, K, D):
    A = 3 * H * D; n = M * A
    nbr = np.full((n, 12), n, np.int32)
    for l in range(M):
        for i in range(H):
            for j in range(D):
                k = l - i - j
                for a in range(3):
                    me = cid(l, i, j, a, H, K, D)
                    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
                    for t, o in enumerate(offsets(a)):
                        q = [p[0] + o[0], p[1] + o[1], p[2] + o[2]]
                        a2 = [x for x in range(3) if q[x] % 2][0]
                        c = [(q[x] - (1 if x == a2 else 0)) // 2 for x in range(3)]
                        l2 = c[0] + c[1] + c[2]
                        if 0 <= l2 < M:
                            nbr[me, t] = cid(l2, c[0], c[1], a2, H, K, D)
    return A, n, nbr


def write(H, K, D, path, swap=False):
    A, n, nbr = build(H, K, D)
    if swap:
        c = n // 2 + 5; nbr = nbr.copy(); nbr[c, 0] = (int(nbr[c, 0]) + 3) % n
    with open(path, 'wb') as f:
        np.array([n, A], np.int32).tofile(f); nbr.astype(np.int32).tofile(f)
    return A, n, nbr


if __name__ == '__main__':
    H, K, D = map(int, sys.argv[1:4]); A, n, _ = write(H, K, D, sys.argv[4]); print(f'A {A} n {n}')
