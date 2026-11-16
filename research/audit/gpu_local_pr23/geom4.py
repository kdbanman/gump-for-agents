#!/usr/bin/env python3
"""Own graph of the 8-layer slab on the in-plane torus (4,0),(0,4) (cube coordinates), built from docs/AUTOMATON.md's
doubled-coordinate offsets only (nothing imported from research/). Writes the graph file read by t4.c.

Nodes: cube (i, j, k) with t = i + j + k in [0, 8), (i, j) mod 4 (the lattice translations (4,0,-4), (0,4,-4) keep t),
three faces per cube (2(i,j,k) + e_a). Layers: face layers t = 0 and t = 7; for each transverse diagonal
d in (-1,1,1), (1,-1,1), (1,1,-1) the index s = d.p mod 16 (8 odd residues, a ring of 8 layers of 48 cells).
    python3 research/audit/gpu_local_pr23/geom4.py OUT.bin
"""
import sys
import numpy as np

A_, B_, M = 4, 4, 8
TD = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]


def nodes():
    out = []
    for t in range(M):
        for i in range(A_):
            for j in range(B_):
                k = t - i - j
                for ax in range(3):
                    p = [2 * i, 2 * j, 2 * k]; p[ax] += 1
                    out.append(tuple(p))
    return out


CELLS = nodes()


def key(p):
    ax = [x % 2 for x in p].index(1)
    c = [(p[x] - (x == ax)) // 2 for x in range(3)]
    t = sum(c)
    if not 0 <= t < M:
        return None
    return (t, c[0] % A_, c[1] % B_, ax)


INDEX = {key(p): n for n, p in enumerate(CELLS)}


def offsets(p):
    a = [x % 2 for x in p].index(1)
    b, c = [x for x in range(3) if x != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(o)
    for sa in (1, -1):
        for e in (b, c):
            for se in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[e] = se; out.append(o)
    return out


def graph():
    n = len(CELLS)
    nb = np.full((n, 12), -1, np.int32)
    for i, p in enumerate(CELLS):
        for s, o in enumerate(offsets(p)):
            k = key(tuple(p[x] + o[x] for x in range(3)))
            nb[i, s] = -1 if k is None else INDEX[k]
    return nb


def layers():
    P = np.array(CELLS)
    t = (P.sum(1) - 1) // 2
    face = [np.nonzero(t == 0)[0], np.nonzero(t == M - 1)[0]]
    trans = []
    for d in TD:
        s = (P @ np.array(d)) % 16
        trans.append([np.nonzero(s == r)[0] for r in range(1, 16, 2)])
    return face, trans


def selfcheck(nb):
    n = len(CELLS)
    P = np.array(CELLS)
    # every row has distinct entries (no multigraph at 4x4), and symmetry of adjacency
    dup = sum(len(set(x for x in r if x >= 0)) != (r >= 0).sum() for r in nb)
    asym = sum(1 for i in range(n) for j in nb[i] if j >= 0 and i not in nb[j])
    # T1 on each transverse diagonal mod 16: neighbour s-differences in {0, +-2, +-4}
    bad = 0
    for d in TD:
        s = (P @ np.array(d)) % 16
        for i in range(n):
            for j in nb[i]:
                if j >= 0 and ((s[j] - s[i]) % 16) not in (0, 2, 4, 12, 14):
                    bad += 1
    print(f'nodes {n}, dead slots {(nb < 0).sum()}, duplicate neighbours {dup}, asymmetric pairs {asym}, T1 violations {bad}')
    return dup == 0 and asym == 0 and bad == 0


def write(path):
    nb = graph()
    assert selfcheck(nb)
    face, trans = layers()
    with open(path, 'wb') as f:
        np.array([len(CELLS)], np.int32).tofile(f)
        nb.astype(np.int32).tofile(f)
        for L in face:
            np.array([len(L)], np.int32).tofile(f); L.astype(np.int32).tofile(f)
        for d in trans:
            for L in d:
                np.array([len(L)], np.int32).tofile(f); L.astype(np.int32).tofile(f)


if __name__ == '__main__':
    write(sys.argv[1])
