#!/usr/bin/env python3
"""Slab geometry for research/blast/split-slab, written from docs/AUTOMATON.md and reference/oracle.py only.

Vessel: 8 consecutive {111} layers, cube index (i, j, k) with layer l = i + j + k in 0..7 (doubled coordinates
p = 2 (i, j, k) + e_a, s = x + y + z = 2 l + 1), periodic in the plane under the cube translations (x, y, -x - y)
for (x, y) in the lattice spanned by (H, K) and (0, D)  (|(x, y)|^2 = x^2 + x y + y^2).  Cells outside the 8
layers are dead for ever (T2 from both sides).  A = 3 H D cells per layer, n = 8 A cells.

Cell id = ((l * H * D + i' * D + j') * 3 + a), (i', j') the reduced in-plane index (0 <= i' < H, 0 <= j' < D).
So layer l is the id range [l A, (l + 1) A): face 0 is [0, A), face 1 is [7 A, 8 A).

    python3 geom.py H K D out.bin        # int32 LE: n, A, nbr[n * 12]  (n = "outside, dead")
"""
import sys
import numpy as np

M = 8


def offsets(axis):
    """12 neighbour offsets in doubled coordinates of a face with normal `axis` (AUTOMATON.md section 2)."""
    a = axis
    b, c = [i for i in range(3) if i != a]
    offs = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs


def reduce(i, j, H, K, D):
    q = i // H
    return i - q * H, (j - q * K) % D


def cid(l, i, j, a, H, K, D):
    i, j = reduce(i, j, H, K, D)
    return (l * H * D + i * D + j) * 3 + a


def build(H, K, D):
    A = 3 * H * D
    n = M * A
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
                        odd = [x for x in range(3) if q[x] % 2]
                        assert len(odd) == 1
                        a2 = odd[0]; q[a2] -= 1
                        i2, j2, k2 = q[0] // 2, q[1] // 2, q[2] // 2
                        l2 = i2 + j2 + k2
                        if 0 <= l2 < M:
                            nbr[me, t] = cid(l2, i2, j2, a2, H, K, D)
    # sanity: the neighbour relation is symmetric (with multiplicity), and T1's layer histogram holds
    lay = np.arange(n) // A
    for c in range(n):
        dl = sorted(int(lay[x]) - int(lay[c]) for x in nbr[c] if x < n)
        full = [-2, -1, -1, 0, 0, 0, 0, 0, 0, 1, 1, 2]
        want = [d for d in full if 0 <= lay[c] + d < M]
        assert dl == want, (c, dl, want)
    cnt = {}
    for c in range(n):
        for x in nbr[c]:
            if x < n:
                cnt[(c, int(x))] = cnt.get((c, int(x)), 0) + 1
    assert all(cnt.get((y, x), 0) == v for (x, y), v in cnt.items())
    return A, n, nbr


def write(H, K, D, path, swap=False):
    A, n, nbr = build(H, K, D)
    if swap:   # negative control: one neighbour entry replaced by another cell of the same layer
        c = n // 2 + 5
        nbr = nbr.copy()
        nbr[c, 0] = (int(nbr[c, 0]) + 3) % n if nbr[c, 0] < n else 0
    with open(path, 'wb') as f:
        np.array([n, A], np.int32).tofile(f)
        nbr.astype(np.int32).tofile(f)
    return A, n, nbr


def step_graph(x, nbr):
    """numpy reference stepper on the neighbour table (x: uint8 array of n cells)."""
    xe = np.append(x, 0).astype(np.int16)
    c = xe[nbr].sum(1)
    return (((x == 0) & ((c == 4) | (c == 5))) | ((x == 1) & (c >= 3) & (c <= 5))).astype(np.uint8)


def loops(H, K, D, cap=40, R=20):
    out = []
    for m in range(0, R + 1):
        for j in range(-R, R + 1):
            if m == 0 and j <= 0:
                continue
            x, y = m * H, m * K + j * D
            q = x * x + x * y + y * y
            if q <= cap:
                out.append(q)
    return sorted(out)


if __name__ == '__main__':
    H, K, D = map(int, sys.argv[1:4])
    A, n, nbr = write(H, K, D, sys.argv[4], swap=(len(sys.argv) > 5 and sys.argv[5] == 'swap'))
    print(f'lattice ({H},{K}),(0,{D}): A = {A}, n = {n}, loops^2 <= 40: {loops(H, K, D)}')
