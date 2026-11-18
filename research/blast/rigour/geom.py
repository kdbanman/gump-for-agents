#!/usr/bin/env python3
"""Face-layer graphs for the one-layer dice surrogate of a gump face (blast/rigour).

Built from the 12 neighbour offsets of docs/AUTOMATON.md section 2, in doubled coordinates, for the {111} layer
s = x + y + z = C.  A face cell has 6 in-layer neighbours (offsets with zero sum), 2 neighbours one layer in
(offset sum -2) and 1 neighbour two layers in (offset sum -4).

  torus  H K D     wrapped face, period lattice (H,K),(0,D) in the hexagonal basis E1 = (2,-2,0), E2 = (2,0,-2)
                   (|aE1 + bE2|^2 / 8 = a^2 + ab + b^2), 3HD cells; neighbours counted with multiplicity
  hull   R         rimmed triangular face of the octahedral hull |x|+|y|+|z| <= R (R odd): x,y,z >= 0, sum R;
                   A = 3k(k+1)/2 with R = 2k - 1; cells beneath outside the hull do not exist (no coin)
  hull2  R         the same face, but a coin that is a cell of ANOTHER face's own layer (|x|+|y|+|z| = R) is coded
                   as a ten in m1 or m2: mc.c gives those coins a third density (a rim held by a second face)
  strip  W D       W unit cells wide (free rim, dead outside), D long and periodic: unit cells (a, b), 0 <= a < W,
                   b mod D; every cell keeps its three coins
  patch  W D       W x D unit cells, free rim all round; every cell keeps its three coins

Output (stdout): A; then per cell "m1 m2 deg n1 ... ndeg" (m1, m2 = number of coins one and two layers in;
neighbour list with repetition); then an elimination order for the transfer product (A ints).
"""
import sys
import itertools


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; out.append(tuple(v))
    return out


OFF = [offsets(a) for a in range(3)]


def axis(p):
    par = [c % 2 for c in p]
    assert sum(par) == 1, p
    return par.index(1)


def cell_ab(p, C):
    """p in layer C  ->  (orientation o, a, b) with p = base_o + a E1 + b E2"""
    o = axis(p)
    base = [(C, 0, 0), (C - 1, 1, 0), (C - 1, 0, 1)][o]
    a = -(p[1] - base[1]) // 2
    b = -(p[2] - base[2]) // 2
    assert (base[0] + 2 * a + 2 * b, base[1] - 2 * a, base[2] - 2 * b) == tuple(p), (p, base, a, b)
    return o, a, b


def ab_cell(o, a, b, C):
    base = [(C, 0, 0), (C - 1, 1, 0), (C - 1, 0, 1)][o]
    return (base[0] + 2 * a + 2 * b, base[1] - 2 * a, base[2] - 2 * b)


def torus(H, K, D, C=1):
    def red(o, a, b):
        q, a2 = divmod(a, H)
        return (o, a2, (b - q * K) % D)
    cells = [(o, a, b) for a in range(H) for b in range(D) for o in range(3)]
    ix = {c: i for i, c in enumerate(cells)}
    nb, m = [], []
    for (o, a, b) in cells:
        p = ab_cell(o, a, b, C)
        l = []
        for off in OFF[o]:
            if sum(off) == 0:
                q = tuple(p[i] + off[i] for i in range(3))
                l.append(ix[red(*cell_ab(q, C))])
        assert len(l) == 6
        nb.append(l); m.append((2, 1))
    return nb, m


def hull(R, second=False):
    cells = [(x, y, R - x - y) for x in range(R + 1) for y in range(R + 1 - x)
             if (x % 2) + (y % 2) + ((R - x - y) % 2) == 1]
    ix = {c: i for i, c in enumerate(cells)}
    nb, m = [], []
    for p in cells:
        o = axis(p)
        l, m1, m2 = [], 0, 0
        for off in OFF[o]:
            q = tuple(p[i] + off[i] for i in range(3))
            inside = sum(abs(c) for c in q) <= R
            if sum(off) == 0 and q in ix:
                l.append(ix[q])
            onface = sum(abs(c) for c in q) == R        # a cell of another face's own layer
            if sum(off) == -2 and inside:
                m1 += 10 if (second and onface) else 1
            if sum(off) == -4 and inside:
                m2 += 10 if (second and onface) else 1
        nb.append(l); m.append((m1, m2))
    return nb, m, cells


def strip(W, D, periodic=True, C=1):
    cells = [(o, a, b) for a in range(W) for b in range(D) for o in range(3)]
    ix = {c: i for i, c in enumerate(cells)}
    nb, m = [], []
    for (o, a, b) in cells:
        p = ab_cell(o, a, b, C)
        l = []
        for off in OFF[o]:
            if sum(off) == 0:
                q = tuple(p[i] + off[i] for i in range(3))
                o2, a2, b2 = cell_ab(q, C)
                if periodic:
                    b2 %= D
                if (o2, a2, b2) in ix:
                    l.append(ix[(o2, a2, b2)])
        nb.append(l); m.append((2, 1))
    return nb, m


def peak_bits(nb, order):
    """peak number of binary variables of the transfer product for this elimination order (as qsd.c runs it)"""
    A = len(nb)
    dep = [set([i]) for i in range(A)]          # dep[i] = cells whose update reads old_i
    for c in range(A):
        for j in nb[c]:
            dep[j].add(c)
    done, n, peak, alive = set(), A, A, set(range(A))
    for c in order:
        done.add(c)
        freed = [i for i in alive if dep[i] <= done]
        if freed:
            n -= len(freed) - 1
        else:
            n += 1
            peak = max(peak, n)
        for i in freed:
            alive.discard(i)
    return peak


def best_order(nb, tries=400, seed=1):
    """greedy orders (free as many old variables as possible, then stay close to what is already processed),
    from every start cell and with random tie-breaks; return the order with the smallest peak"""
    import random
    rnd = random.Random(seed)
    A = len(nb)
    dep = [set([i]) for i in range(A)]
    for c in range(A):
        for j in nb[c]:
            dep[j].add(c)
    best = None
    starts = list(range(A)) + [rnd.randrange(A) for _ in range(max(0, tries - A))]
    for st in starts:
        done, order = set(), []
        c = st
        while True:
            done.add(c); order.append(c)
            if len(order) == A:
                break
            cand = []
            for x in range(A):
                if x in done:
                    continue
                d2 = done | {x}
                freed = sum(1 for i in range(A) if dep[i] <= d2 and not dep[i] <= done)
                touch = sum(1 for j in nb[x] if j in done)
                cand.append((-freed, -touch, rnd.random(), x))
            c = min(cand)[3]
        pk = peak_bits(nb, order)
        if best is None or pk < best[0]:
            best = (pk, order)
    return best


def emit(nb, m, order, f=sys.stdout):
    print(len(nb), file=f)
    for l, (m1, m2) in zip(nb, m):
        print(m1, m2, len(l), *l, file=f)
    print(*order, file=f)


def build(kind, *args):
    if kind == 'torus':
        nb, m = torus(*args)
    elif kind == 'hull':
        nb, m, _ = hull(*args)
    elif kind == 'hull2':
        nb, m, _ = hull(*args, second=True)
    elif kind == 'strip':
        nb, m = strip(*args)
    elif kind == 'patch':
        nb, m = strip(*args, periodic=False)
    else:
        raise SystemExit(__doc__)
    return nb, m


if __name__ == '__main__':
    kind = sys.argv[1]
    args = [int(x) for x in sys.argv[2:]]
    nb, m = build(kind, *args)
    pk, order = best_order(nb)
    print('# %s %s  A=%d  peak bits %d' % (kind, args, len(nb), pk), file=sys.stderr)
    emit(nb, m, order)
