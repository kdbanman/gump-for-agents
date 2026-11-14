#!/usr/bin/env python3
"""Adversarial review of research/shape/: geometry of the twisted slabs, from scratch.

    python3 research/audit/shape/geom_check.py          # lattices, classes, layer periods, graph vs tslab, embedding

1. Every index-20 and index-24 lattice (all HNFs (a,k),(0,b)), its systole^2 by brute force, and its class under the
   slab's in-plane point group. The point group is generated here from O_h directly: the 48 signed permutations of
   R^3, kept if they map the slab normal (1,1,1) to +-(1,1,1); each acts on in-plane cube vectors (x, y, -x-y).
   (-1 maps every lattice to itself, so the slab flip adds nothing beyond the six coordinate permutations.)
   Classes are compared with "same reduced Gram matrix" (flat-torus isometry), which is what research/shape uses.
2. Transverse layer periods by brute force: P_d = gcd of d.(2 v) over *all* short lattice vectors v (not just the
   two generators), and the number of distinct layers actually present on the quotient.
3. The neighbour graph of the twisted slab built from AUTOMATON.md's cube-index table (not from offsets), compared
   cell by cell with research/shape/tslab.py's graph (only tslab's cell list and neighbour array are read).
4. The cubic-torus embedding used by tslab validate: N Z^2 in Lambda for N = 24 (index 24) and N = 20 (index 20).
"""
import itertools, math, os, sys
from math import gcd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

TORI72 = [(3, 0, 8), (8, 2, 3), (4, 4, 6), (2, 5, 12), (4, 3, 6), (4, 5, 6), (3, 1, 8), (4, 0, 6), (4, 2, 6),
          (6, 1, 4), (6, 3, 4), (2, 3, 12), (4, 1, 6)]
TORI60 = [(4, 0, 5), (5, 0, 4), (5, 1, 4), (2, 3, 10), (4, 2, 5), (4, 3, 5), (2, 2, 10)]
M = 8


def hnfs(n):
    for a in range(1, n + 1):
        if n % a == 0:
            for k in range(n // a):
                yield (a, k, n // a)


def in_lat(v, L):
    a, k, b = L
    x, y = v
    return x % a == 0 and (y - (x // a) * k) % b == 0


def lat_vecs(L, R=40):
    a, k, b = L
    for p in range(-R, R + 1):
        for q in range(-R, R + 1):
            if (p, q) != (0, 0):
                yield (p * a, p * k + q * b)


def norm2(v):  # |x u1 + y u2|^2 / 2
    x, y = v
    return x * x + x * y + y * y


def systole2(L):
    return min(norm2(v) for v in lat_vecs(L))


def second2(L):
    """squared length of the shortest vector independent of a shortest one"""
    vs = sorted(lat_vecs(L), key=norm2)
    u = vs[0]
    return next(norm2(v) for v in vs if u[0] * v[1] - u[1] * v[0] != 0)


def point_group():
    """In-plane linear maps (as 2x2 integer matrices on (x, y)) from the signed permutations preserving +-(1,1,1)."""
    G = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            g = lambda v, perm=perm, sg=sg: tuple(sg[i] * v[perm[i]] for i in range(3))
            n = g((1, 1, 1))
            if n not in [(1, 1, 1), (-1, -1, -1)]:
                continue
            cols = []
            for e in [(1, 0, -1), (0, 1, -1)]:
                w = g(e)
                assert sum(w) == 0
                cols.append((w[0], w[1]))
            G.append(cols)
    assert len(G) == 12
    return G


def hnf_of(gens, n):
    """HNF of the lattice spanned by gens (index n) by brute force membership."""
    for L in hnfs(n):
        if all(in_lat(g, L) for g in gens) and True:
            # same index and contains the gens => equal
            return L


def image(L, g, n):
    a, k, b = L
    gens = []
    for v in [(a, k), (0, b)]:
        gens.append((g[0][0] * v[0] + g[1][0] * v[1], g[0][1] * v[0] + g[1][1] * v[1]))
    return hnf_of(gens, n)


def gram_class(L):
    """Gauss-reduced Gram, own implementation (sorted lengths of a reduced basis and |inner product|)."""
    vs = sorted(lat_vecs(L), key=norm2)
    u = vs[0]
    v = next(w for w in vs if u[0] * w[1] - u[1] * w[0] != 0)
    ip = lambda p, q: 2 * p[0] * q[0] + p[0] * q[1] + p[1] * q[0] + 2 * p[1] * q[1]  # = 2 B
    return (norm2(u), abs(ip(u, v)) // 1, norm2(v))


def periods(L):
    out = []
    for d in [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
        g = 0
        for (x, y) in itertools.islice(lat_vecs(L, 6), None):
            g = gcd(g, 2 * (d[0] * x + d[1] * y + d[2] * (-x - y)))
        out.append(g)
    return out


# ---- the graph from AUTOMATON.md's cube-index table --------------------------------------------------------
# entries: (axis of neighbour, di, dj, dk) for each axis of the cell (0 = X, 1 = Y, 2 = Z)
TABLE = {
    0: [(0, 0, 1, 1), (0, 0, 1, -1), (0, 0, -1, 1), (0, 0, -1, -1),
        (1, 0, 0, 0), (1, 0, -1, 0), (1, 1, 0, 0), (1, 1, -1, 0),
        (2, 0, 0, 0), (2, 0, 0, -1), (2, 1, 0, 0), (2, 1, 0, -1)],
    1: [(1, 1, 0, 1), (1, 1, 0, -1), (1, -1, 0, 1), (1, -1, 0, -1),
        (2, 0, 0, 0), (2, 0, 0, -1), (2, 0, 1, 0), (2, 0, 1, -1),
        (0, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, -1, 1, 0)],
    2: [(2, 1, 1, 0), (2, 1, -1, 0), (2, -1, 1, 0), (2, -1, -1, 0),
        (0, 0, 0, 0), (0, -1, 0, 0), (0, 0, 0, 1), (0, -1, 0, 1),
        (1, 0, 0, 0), (1, 0, -1, 0), (1, 0, 0, 1), (1, 0, -1, 1)],
}


def reduce_ij(i, j, L):
    a, k, b = L
    q = i // a
    return i - q * a, (j - q * k) % b


def my_slab(L, m=M):
    """cells (ax, i, j, t) with i in [0,a), j in [0,b); neighbours from TABLE; outside the slab: None."""
    a, k, b = L
    cells = [(ax, i, j, t) for t in range(m) for i in range(a) for j in range(b) for ax in range(3)]
    idx = {c: n for n, c in enumerate(cells)}
    nb = []
    for (ax, i, j, t) in cells:
        kk = t - i - j
        row = []
        for (bx, di, dj, dk) in TABLE[ax]:
            I, J, K = i + di, j + dj, kk + dk
            T = I + J + K
            if not 0 <= T < m:
                row.append(None)
                continue
            I2, J2 = reduce_ij(I, J, L)
            row.append(idx[(bx, I2, J2, T)])
        nb.append(row)
    return cells, idx, nb


def doubled(c):
    ax, i, j, t = c
    p = [2 * i, 2 * j, 2 * (t - i - j)]
    p[ax] += 1
    return tuple(p)


def compare_with_tslab(L):
    sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
    import tslab
    v = tslab.tslab(*L)
    cells, idx, nb = my_slab(L)
    # map tslab index -> my index via doubled coordinates of the fundamental-domain representative
    mine_by_p = {doubled(c): n for n, c in enumerate(cells)}
    tmap = [mine_by_p[tuple(p)] for p in v.cells]
    assert len(set(tmap)) == len(cells) == len(v.cells)
    bad = 0
    dup = 0
    for tn, p in enumerate(v.cells):
        n = tmap[tn]
        theirs = sorted(tmap[x] for x in v.nb[tn] if x >= 0)
        mine = sorted(x for x in nb[n] if x is not None)
        bad += theirs != mine
        dup += len(set(mine)) != len(mine)
    # layer sets: their transverse layers vs mine (s mod P computed from my periods)
    P = periods(L)
    lay_bad = 0
    for d, dv in enumerate([(-1, 1, 1), (1, -1, 1), (1, 1, -1)]):
        mine_l = {}
        for n, c in enumerate(cells):
            p = doubled(c)
            mine_l.setdefault((sum(dv[x] * p[x] for x in range(3))) % P[d], set()).add(n)
        theirs_l = {s: {tmap[x] for x in ids} for (dd, s), ids in v.layers if dd == d + 1}
        lay_bad += mine_l != theirs_l
    return bad, dup, lay_bad, v.P == P


def embed_ok(L, N):
    """N Z^2 subset of Lambda, and N >= m + 3 (dead band of >= 3 d0 layers between slab copies)."""
    return in_lat((N, 0), L) and in_lat((0, N), L) and N >= M + 3


if __name__ == '__main__':
    G = point_group()
    for n in (20, 24):
        allL = list(hnfs(n))
        cls = {}
        for L in allL:
            orb = min(image(L, g, n) for g in G)
            cls.setdefault(orb, []).append(L)
        gram = {}
        for L in allL:
            gram.setdefault(gram_class(L), []).append(L)
        print(f'index {n}: {len(allL)} lattices, {len(cls)} point-group classes, {len(gram)} Gram classes; '
              f'partitions equal: {sorted(map(sorted, cls.values())) == sorted(map(sorted, gram.values()))}')
    print()
    print('torus           index sys2 2nd  Gram          class-rep     periods      layers  embedN')
    for A, tori, N in [(72, TORI72, 24), (60, TORI60, 20)]:
        n = A // 3
        for L in tori:
            a, k, b = L
            orb = min(image(L, g, n) for g in G)
            P = periods(L)
            print(f'({a},{k}),(0,{b})'.ljust(16) + f'{a * b:5d} {systole2(L):4d} {second2(L):4d} {str(gram_class(L)):13s} '
                  f'{str(orb):13s} {str(P):12s} {str([p // 2 for p in P]):8s} {embed_ok(L, N)}')
    print()
    for L in [(4, 1, 6), (5, 1, 4), (4, 0, 5), (2, 5, 12), (8, 2, 3), (4, 4, 6), (2, 2, 10), (2, 3, 10)]:
        bad, dup, lay_bad, pe = compare_with_tslab(L)
        print(f'graph {L}: cells whose neighbour set differs from tslab: {bad}; cells with repeated neighbours: {dup}; '
              f'transverse layer partitions differing: {lay_bad}; periods equal: {pe}')
