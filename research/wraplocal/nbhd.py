#!/usr/bin/env python3
"""Exact neighbourhood geometry of a wrapped face (research/wraplocal).

A face torus (h, k, d) is the 8-layer slab t = 0..7 (t = i + j + k, cube index), periodic under the in-plane
translations m (h, k) + j (0, d), (X, Y) -> doubled offset 2 (X, Y, -X-Y); |w|^2 = Q(X, Y) = X^2 + XY + Y^2
(lattices.py's units).  Neighbour offsets from docs/AUTOMATON.md section 2.

For every translation w with Q(w) <= QMAX (one per +-w) and every cell type (normal axis a, layer t) this prints
  dist   graph distance from p to p + w in the infinite slab (two copies of a cell are that many steps apart)
  walks  number of shortest walks
  dist6  the same inside the face layer alone (the 6 in-layer neighbours)
and the walk counts N_m(w) = number of walks of length m from p to p + w, m <= MMAX, in the slab graph.

    python3 research/wraplocal/nbhd.py            # table by loop^2
    python3 research/wraplocal/nbhd.py --offsets  # in-plane projections of the 12 offsets, by layer step
"""
import sys
from collections import defaultdict

M = 8
QMAX = 31
MMAX = 6


def Q(x, y):
    return x * x + x * y + y * y


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (1, -1):
        for sc in (1, -1):
            o = [0, 0, 0]; o[b] = 2 * sb; o[c] = 2 * sc; out.append(tuple(o))
    for sa in (1, -1):
        for e in (b, c):
            for se in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[e] = se; out.append(tuple(o))
    return out


OFF = {a: offsets(a) for a in range(3)}


def axis(p):
    return [i for i in range(3) if p[i] % 2][0]


def layer(p):
    return (sum(p) - 1) // 2


def nbrs(p, slab=True):
    a = axis(p)
    t = layer(p)
    for o in OFF[a]:
        q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
        tq = layer(q)
        if slab and not 0 <= tq < M:
            continue
        if not slab and tq != t:
            continue
        yield q


def walks_from(p, mmax, slab=True):
    """dict m -> {endpoint: number of walks of length m}"""
    cur = {p: 1}
    out = {0: dict(cur)}
    for m in range(1, mmax + 1):
        nxt = defaultdict(int)
        for q, c in cur.items():
            for r in nbrs(q, slab):
                nxt[r] += c
        cur = nxt
        out[m] = dict(cur)
    return out


def base(a, t):
    """a cell of axis a in layer t: doubled coords with exactly one odd, sum 2t+1"""
    p = [0, 0, 0]
    p[a] = 1
    p[(a + 1) % 3] = 2 * t
    return tuple(p)


def trans(p, w):
    X, Y = w
    return (p[0] + 2 * X, p[1] + 2 * Y, p[2] - 2 * X - 2 * Y)


def vecs(qmax):
    out = []
    R = 7
    for X in range(-R, R + 1):
        for Y in range(-R, R + 1):
            if (X, Y) == (0, 0) or Q(X, Y) > qmax:
                continue
            if (X, Y) < (-X, -Y):
                continue
            out.append((Q(X, Y), X, Y))
    return sorted(out)


def table():
    W = {}
    MM = 9
    for a in range(3):
        for t in range(M):
            W[(a, t)] = walks_from(base(a, t), MM)
    W6 = {a: walks_from(base(a, 0), MM, slab=False) for a in range(3)}
    print('loop^2  w        per axis a=0,1,2: [dist slab, face layer t=0 | interior t=3]  shortest walks (t=0)  dist6 (face alone)')
    rows = []
    for q, X, Y in vecs(QMAX):
        res = []
        for a in range(3):
            def dist(t, src=W):
                tgt = trans(base(a, t), (X, Y))
                ww = src[(a, t)] if src is W else src[a]
                for m in range(MM + 1):
                    if tgt in ww[m]:
                        return m, ww[m][tgt]
                return None, 0
            d0, n0 = dist(0)
            d3, _ = dist(3)
            tgt = trans(base(a, 0), (X, Y))
            d6 = next((m for m in range(MM + 1) if tgt in W6[a][m]), None)
            res.append((d0, d3, n0, d6))
        rows.append((q, X, Y, res))
        print(f'{q:5d}  ({X:2d},{Y:2d})  ' + '   '.join(f'[{r[0]}|{r[1]}] n={r[2]:<4d} d6={r[3]}' for r in res))
    return rows


def offs():
    for a in range(3):
        p = base(a, 3)
        print(f'axis {a}, cell {p}:')
        for o in OFF[a]:
            ds = sum(o) // 2
            print(f'   offset {o}  layer step {ds:+d}')


if __name__ == '__main__':
    if '--offsets' in sys.argv:
        offs()
    else:
        table()
