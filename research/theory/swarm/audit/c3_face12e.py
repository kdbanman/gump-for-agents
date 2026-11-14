#!/usr/bin/env python3
"""Audit of the counting line, face12e: claims 21 (Proposition F), 22 (Proposition G, the example Pi_1),
23 (the lone cell), and the face12e half of claim 6.

  python3 c3_face12e.py            (about 2 minutes, one core)

face12e (PROBLEM.md): gump's cells and rule B45/S345, but the four coplanar neighbours are the ones that share
an edge (+-2e_b, +-2e_c). p0_lib.neighbours(p, coplanar="edge") builds exactly that from reference/oracle.py's
perpendicular offsets. A wall is the plane z = Z (odd); everything above is dead for ever.
"""
import itertools, math, sys, time
from fractions import Fraction as F
import numpy as np
from p0_lib import Vessel, neighbours

t00 = time.time()
Z = 7


def section(s):
    print(f"\n=== {s}  [{time.time() - t00:.0f} s]")


def bits(nb, lo, hi):
    idx = np.arange(lo, hi, dtype=np.int64)
    return ((idx[:, None] >> np.arange(nb)) & 1).astype(np.int8)


class Wall:
    """Periodic wall nx x ny of top cubes, slab 1 <= z <= Z (three cubes deep)."""
    def __init__(self, nx, ny, zmin=1):
        self.nx, self.ny = nx, ny
        wrap = lambda p: (p[0] % (2 * nx), p[1] % (2 * ny), p[2])
        cells = [(x, y, z) for x in range(2 * nx) for y in range(2 * ny) for z in range(zmin, Z + 1)
                 if (x % 2) + (y % 2) + (z % 2) == 1]
        self.V = V = Vessel(cells, coplanar="edge", wrap=wrap)
        ix = lambda p: V.index[wrap(p)]
        self.sig = lambda i, j: ix((2 * i, 2 * j, Z))
        self.h = lambda i, j: ix((2 * i + 1, 2 * j, Z - 1))
        self.v = lambda i, j: ix((2 * i, 2 * j + 1, Z - 1))
        self.beta = lambda i, j: ix((2 * i, 2 * j, Z - 2))
        self.rh = lambda i, j: ix((2 * i + 1, 2 * j, Z - 3))
        self.rv = lambda i, j: ix((2 * i, 2 * j + 1, Z - 3))
        self.S = [i for i, p in enumerate(V.cells) if p[2] == Z]
        self.B = [i for i, p in enumerate(V.cells) if p[2] == Z - 1]
        self.bot = [i for i, p in enumerate(V.cells) if p[2] == Z - 2]
        self.rr = [i for i, p in enumerate(V.cells) if p[2] == Z - 3]
        self.band = self.S + self.B


def dead_next(s, n):
    return not (n in ((3, 4, 5) if s else (4, 5)))


def main():
    section("claim 21, Proposition F.1-F.3: what the band reads (offsets)")
    W = Wall(4, 5)
    V = W.V
    ok = True
    for i, j in itertools.product(range(4), range(5)):
        # sheet cell: four sheet neighbours and the four side faces of its cube; nothing else in the vessel
        got = sorted(V.nlist[W.sig(i, j)])
        want = sorted([W.sig(i + 1, j), W.sig(i - 1, j), W.sig(i, j + 1), W.sig(i, j - 1),
                       W.h(i, j), W.h(i - 1, j), W.v(i, j), W.v(i, j - 1)])
        ok &= got == want
        # h(i, j): in-layer h(i, j+-1), v(i, j), v(i, j-1), v(i+1, j), v(i+1, j-1); sheet of both cubes; both bottoms; r
        got = sorted(V.nlist[W.h(i, j)])
        want = sorted([W.h(i, j + 1), W.h(i, j - 1), W.v(i, j), W.v(i, j - 1), W.v(i + 1, j), W.v(i + 1, j - 1),
                       W.sig(i, j), W.sig(i + 1, j), W.beta(i, j), W.beta(i + 1, j), W.rh(i, j)])
        ok &= got == want
        got = sorted(V.nlist[W.v(i, j)])
        want = sorted([W.v(i + 1, j), W.v(i - 1, j), W.h(i, j), W.h(i - 1, j), W.h(i, j + 1), W.h(i - 1, j + 1),
                       W.sig(i, j), W.sig(i, j + 1), W.beta(i, j), W.beta(i, j + 1), W.rv(i, j)])
        ok &= got == want
        # who reads a bottom, who reads an r, within the band
        band = set(W.band)
        ok &= sorted(set(V.nlist[W.beta(i, j)]) & band) == sorted([W.h(i, j), W.h(i - 1, j), W.v(i, j), W.v(i, j - 1)])
        ok &= sorted(set(V.nlist[W.rh(i, j)]) & band) == [W.h(i, j)]
        ok &= sorted(set(V.nlist[W.rv(i, j)]) & band) == [W.v(i, j)]
    print(f"  wall 4 x 5: neighbour lists of every sheet cell, every side face, every bottom and every r as in the journal: {ok}")
    assert ok
    # the plane is sealed: a dead cell above the wall sees at most 3 cells with z <= Z
    mx = max(sum(1 for q in neighbours(p, "edge") if q[2] <= Z) for p in [(1, 0, Z + 1), (0, 1, Z + 1), (0, 0, Z + 2), (1, 0, Z + 3)])
    print(f"  a cell above the wall has at most {mx} neighbours with z <= Z (sealed: < 4)")
    assert mx == 3
    rng = np.random.default_rng(1)
    X = (rng.random((20000, V.N)) < 0.5).astype(np.int8)
    X[:, W.band] = 0
    Y = V.step(X)
    print(f"  F.2: band empty, random below (20000 states): band cells alive next: {int(Y[:, W.band].sum())}")
    assert Y[:, W.band].sum() == 0
    X = np.zeros((1, V.N), np.int8)
    X[0, [W.h(0, 0), W.h(-1, 0), W.v(0, 0), W.v(0, -1)]] = 1
    Y = V.step(X)
    print(f"  F.2: sheet empty, one cube with four live sides: its top is born: {bool(Y[0, W.sig(0, 0)])}")
    assert Y[0, W.sig(0, 0)] == 1
    res = []
    for b3 in itertools.product((0, 1), repeat=3):
        X = np.zeros((1, V.N), np.int8)
        X[0, W.S] = 1
        X[0, [W.beta(0, 0), W.beta(1, 0), W.rh(0, 0)]] = b3
        res.append((sum(b3), int(V.step(X)[0, W.h(0, 0)])))
    print(f"  F.2 (as corrected in entry 17): layer empty, full sheet: (cells beneath alive, born) = {sorted(set(res))}")
    assert all(born == (b >= 2) for b, born in res)
    X1 = (rng.random((20000, V.N)) < 0.5).astype(np.int8)
    X2 = (rng.random((20000, V.N)) < 0.5).astype(np.int8)
    X2[:, W.band] = X1[:, W.band]
    same = (V.step(X1)[:, W.S] == V.step(X2)[:, W.S]).all()
    print(f"  F.3: same band, different cells below (20000 pairs): same sheet next: {bool(same)}")
    assert same

    section("claim 21, F.4: the sheet over an empty layer")
    X = (rng.random((20000, V.N)) < 0.5).astype(np.int8)
    X[:, W.B] = 0
    Y = V.step(X)
    bad = 0
    for i, j in itertools.product(range(4), range(5)):
        m = X[:, W.sig(i + 1, j)] + X[:, W.sig(i - 1, j)] + X[:, W.sig(i, j + 1)] + X[:, W.sig(i, j - 1)]
        bad += int((Y[:, W.sig(i, j)] != ((m + X[:, W.sig(i, j)]) >= 4)).sum())
    print(f"  periodic wall, layer empty: sigma next = [live sheet neighbours + sigma >= 4] fails in {bad} cases of 400000")
    assert bad == 0

    def box_vessel(n, depth=2):
        cubes = [(2 * i, 2 * j, Z - 1 - 2 * l) for i in range(n) for j in range(n) for l in range(depth)]
        cells = set()
        for c in cubes:
            for a in range(3):
                for sgn in (1, -1):
                    p = list(c); p[a] += sgn; cells.add(tuple(p))
        return Vessel(cells, coplanar="edge")
    for n in range(1, 8):
        Vb = box_vessel(n)
        sheet = {(i, j): Vb.index[(2 * i, 2 * j, Z)] for i in range(n) for j in range(n)}
        layer = [i for i, p in enumerate(Vb.cells) if p[2] == Z - 1]
        d = {(i, j): min(i, n - 1 - i) + min(j, n - 1 - j) for i in range(n) for j in range(n)}
        X = np.zeros((1, Vb.N), np.int8)
        X[0, list(sheet.values())] = 1
        okd = True
        steps_to_empty = None
        for t in range(1, n + 2):
            X[0, layer] = 0                                  # the layer is kept empty; the rest evolves by the rule
            below = [i for i, p in enumerate(Vb.cells) if p[2] < Z - 1]
            X[0, below] = rng.random(len(below)) < 0.5       # whatever lies below
            X = Vb.step(X)
            alive = {q for q, i in sheet.items() if X[0, i]}
            okd &= alive == {q for q in d if d[q] >= t}
            if not alive and steps_to_empty is None:
                steps_to_empty = t
        print(f"  box wall {n} x {n} (true rule, layer held empty, random below): Theta^j(full) = {{d >= j}} for all j: {okd}; "
              f"empty after {steps_to_empty} steps (max d = {max(d.values())})")
        assert okd and steps_to_empty <= n and steps_to_empty == max(d.values()) + 1
    # monotone: Theta^n(any) is empty on the box (n <= 4: every sheet configuration)
    for n in (2, 3, 4):
        allS = bits(n * n, 0, 1 << (n * n)).reshape(-1, n, n).astype(np.int8)
        Xs = allS
        for t in range(n):
            P = np.pad(Xs, ((0, 0), (1, 1), (1, 1)))
            m = P[:, :-2, 1:-1] + P[:, 2:, 1:-1] + P[:, 1:-1, :-2] + P[:, 1:-1, 2:]
            Xs = ((m + Xs) >= 4).astype(np.int8)
        print(f"  Theta^{n} of every one of the 2^{n * n} sheets on the box {n} x {n}: cells left {int(Xs.sum())}")
        assert Xs.sum() == 0
    # periodic wall: two adjacent rows persist
    X = np.zeros((1, V.N), np.int8)
    X[0, [W.sig(i, j) for i in range(4) for j in (0, 1)]] = 1
    Y = X.copy()
    for _ in range(5):
        Y[0, W.B] = 0
        Y = V.step(Y)
    print(f"  periodic wall 4 x 5, two adjacent rows of the sheet over a layer held empty: still there after 5 steps: "
          f"{bool((Y[0, W.S] == X[0, W.S]).all())}")

    section("claim 21, F.5 and F.6: the layer under an empty sheet")
    X = (rng.random((40000, V.N)) < rng.choice([0.2, 0.4, 0.6], size=(40000, 1))).astype(np.int8)
    X[:, W.S] = 0
    Y = V.step(X)
    bad5 = bad5b = 0
    four = np.zeros(40000, bool)
    for i, j in itertools.product(range(4), range(5)):
        sides = X[:, W.h(i, j)] + X[:, W.h(i - 1, j)] + X[:, W.v(i, j)] + X[:, W.v(i, j - 1)]
        four |= sides == 4
        bad5 += int((Y[:, W.sig(i, j)] != (sides == 4)).sum())
    inlayer = {p: [q for q in V.nlist[p] if q in set(W.B)] for p in W.B}
    below = {p: [q for q in V.nlist[p] if V.cells[q][2] < Z - 1] for p in W.B}
    assert all(len(v) == 6 for v in inlayer.values()) and all(len(v) == 3 for v in below.values())
    for p in W.B:
        n = X[:, inlayer[p]].sum(axis=1) + X[:, below[p]].sum(axis=1)
        nxt = np.where(X[:, p] == 1, (n >= 3) & (n <= 5), (n == 4) | (n == 5))
        bad5b += int((Y[:, p] != nxt).sum())
    print(f"  F.5: sheet empty (40000 states): 'top born iff four live sides' fails {bad5} times; "
          f"'layer cell follows B45/S345 on k (6 in-layer) + 2 bottoms + 1 below' fails {bad5b} times")
    assert bad5 == 0 and bad5b == 0
    onE = ~four
    eq = ((Y[onE][:, W.band].sum(axis=1) == 0) == (Y[onE][:, W.B].sum(axis=1) == 0)).all()
    print(f"  F.6: on E (sheet empty, no cube with four live sides; {int(onE.sum())} states): band empty next iff layer empty next: {bool(eq)}")
    assert eq

    section("claim 22, the table of allowed m = beta_q + beta_q' (r_p free)")
    names = {(0, 1, 2): 'free', (0, 1): 'not both', (0, 2): 'equal', (1, 2): 'at least one', (0,): 'both dead', (2,): 'both alive', (): 'never'}
    tab = {}
    for s in (0, 1):
        for a in range(0, 9):
            allowed = tuple(m for m in (0, 1, 2) if any(dead_next(s, a + m + r) for r in (0, 1)))
            tab[s, a] = allowed
    print("  dead:", {a: names[tab[0, a]] for a in range(9)})
    print("  live:", {a: names[tab[1, a]] for a in range(9)})
    want = {(0, 0): 'free', (0, 1): 'free', (0, 2): 'not both', (0, 3): 'equal', (0, 4): 'at least one', (0, 5): 'free',
            (1, 0): 'free', (1, 1): 'not both', (1, 2): 'both dead', (1, 3): 'both alive', (1, 4): 'at least one', (1, 5): 'free'}
    for a in (6, 7, 8):
        want[0, a] = want[1, a] = 'free'
    assert all(names[tab[key]] == val for key, val in want.items())
    print("  agrees with the journal's table for every (state, a), a = 0..8; every class is a 2-SAT constraint")

    section("claim 22 (a): the vertex-model formula against every state, periodic wall 2 x 2")
    W2 = Wall(2, 2)
    V2 = W2.V
    A = 4
    band, bot, rr = W2.band, W2.bot, W2.rr
    assert len(band) == 12 and len(bot) == 4 and len(rr) == 8
    order = band + bot + rr
    brute = np.zeros(1 << 12, np.int64)
    for lo in range(0, 1 << 24, 1 << 18):
        b = bits(24, lo, lo + (1 << 18))
        X = np.zeros((1 << 18, V2.N), np.int8)
        X[:, order] = b
        Y = V2.step(X)
        dead = Y[:, band].sum(axis=1) == 0
        np.add.at(brute, (np.arange(lo, lo + (1 << 18)) & 0xFFF)[dead], 1)
    # formula
    adj = V2.adj
    bandconf = bits(12, 0, 1 << 12)
    Xb = np.zeros((1 << 12, V2.N), np.int8)
    Xb[:, band] = bandconf
    S1 = V2.step(Xb)[:, W2.S].sum(axis=1) == 0              # S(1) depends on the band only (F.3)
    a_all = Xb @ adj[:, band].T[band].T if False else None
    formula = np.zeros(1 << 12, np.int64)
    Bcells = W2.B
    a_p = (Xb[:, band].astype(np.int64) @ adj[np.ix_(band, Bcells)])        # live band neighbours of each layer cell (multiplicity)
    cubes_of = [[bot.index(q) for q in V2.nlist[p] if q in bot] for p in Bcells]
    assert all(len(c) == 2 and c[0] != c[1] for c in cubes_of)
    Dd = lambda s, n: dead_next(s, n)
    for c in range(1 << 12):
        if not S1[c]:
            continue
        tot = 0
        for beta in itertools.product((0, 1), repeat=4):
            pr = 1
            for t, p in enumerate(Bcells):
                s = int(Xb[c, p]); a = int(a_p[c, t]); m = beta[cubes_of[t][0]] + beta[cubes_of[t][1]]
                pr *= int(Dd(s, a + m)) + int(Dd(s, a + m + 1))            # = 2 W_p(m)
                if pr == 0:
                    break
            tot += pr
        formula[c] = tot
    print(f"  all 2^24 states of (band, bottoms, cells below the layer): band empty next in {int(brute.sum())}; "
          f"formula sum = {int(formula.sum())}; equal for each of the 4096 band configurations: {bool((brute == formula).all())}")
    assert (brute == formula).all()
    print(f"  lambda(T <= 1) on the 2 x 2 wall = {int(brute.sum())}/2^24 = {brute.sum() / 2 ** 24:.6f}")

    section("claim 22, the example Pi_1 on walls n x 4")
    for n in (3, 4):
        Wn = Wall(n, 4)
        Vn = Wn.V
        X0 = np.zeros(Vn.N, np.int8)
        live = [Wn.h(i, 1) for i in range(n)] + [Wn.v(i, 0) for i in range(n)] + [Wn.v(i, 1) for i in range(n)] \
            + [Wn.sig(i, 1) for i in range(n)]
        X0[live] = 1
        bandn = Wn.band
        nbot = 4 * n
        botn = [Wn.beta(i, j) for j in range(4) for i in range(n)]          # bit i + n*j
        # a_p and the journal's classes
        adjn = Vn.adj
        cls = {}
        for nm, f in (('h', Wn.h), ('v', Wn.v)):
            for j in range(4):
                vals = set()
                for i in range(n):
                    p = f(i, j)
                    a = int(sum(X0[q] for q in Vn.nlist[p] if q in set(bandn)))
                    vals.add((int(X0[p]), a))
                cls[nm, j] = vals
        print(f"  n = {n}: (state, a) of h(i,j), j = 0..3: {[sorted(cls['h', j]) for j in range(4)]}; of v(i,j): {[sorted(cls['v', j]) for j in range(4)]}")
        assert cls['h', 0] == {(0, 3)} and cls['h', 2] == {(0, 3)} and cls['h', 1] == {(1, 6)} and cls['h', 3] == {(0, 0)}
        assert cls['v', 0] == {(1, 5)} and cls['v', 1] == {(1, 5)} and cls['v', 2] == {(0, 0)} and cls['v', 3] == {(0, 0)}
        # count: for each pattern of bottoms, the layer cells' fate with r = 0 and with r = 1 (r_p is read by p only: F.1)
        pat = bits(nbot, 0, 1 << nbot)
        Xa = np.tile(X0, (1 << nbot, 1)); Xa[:, botn] = pat
        Ya0 = Vn.step(Xa)
        Xa[:, Wn.rr] = 1
        Ya1 = Vn.step(Xa)
        assert Ya0[:, Wn.S].sum() == 0 and Ya1[:, Wn.S].sum() == 0
        ways = ((Ya0[:, Wn.B] == 0).astype(np.int64) + (Ya1[:, Wn.B] == 0).astype(np.int64))
        cnt_per_beta = ways.prod(axis=1)
        total = int(cnt_per_beta.sum())
        formula = 32 ** n * (8 ** n + 2 * 6 ** n + 5 ** n)
        print(f"    patterns of the {nbot} bottoms and {8 * n} cells below that empty the band: {total}; "
              f"32^n (8^n + 2*6^n + 5^n) = {formula}; of 2^{12 * n}")
        assert total == formula
        okb = pat[cnt_per_beta > 0]
        rows_const = [bool((okb[:, [i + n * j for i in range(n)]].min(axis=1) == okb[:, [i + n * j for i in range(n)]].max(axis=1)).all())
                      for j in range(4)]
        print(f"    in every killing pattern the bottoms of row j are all equal, j = 0..3: {rows_const}")
        assert rows_const[0] and rows_const[2] and not rows_const[1] and not rows_const[3]
        # random full patterns with the true stepper against the per-cell prediction
        m = 300000
        rb = (rng.random((m, nbot)) < 0.5).astype(np.int8)
        # bias half of the samples towards killing patterns so that both outcomes are seen
        pick = rng.integers(0, len(okb), m // 2)
        rb[:m // 2] = okb[pick]
        rrand = (rng.random((m, len(Wn.rr))) < 0.5).astype(np.int8)
        Xr = np.tile(X0, (m, 1)); Xr[:, botn] = rb; Xr[:, Wn.rr] = rrand
        lowcells = [i for i, p in enumerate(Vn.cells) if p[2] < Z - 3]
        Xr[:, lowcells] = rng.random((m, len(lowcells))) < 0.5
        Yr = Vn.step(Xr)
        emp = Yr[:, bandn].sum(axis=1) == 0
        # prediction from the journal's sentence
        b_ = lambda i, j: rb[:, (i % n) + n * j]
        rpos = {c: t for t, c in enumerate(Wn.rr)}
        rh_ = lambda i, j: rrand[:, rpos[Wn.rh(i % n, j)]]
        rv_ = lambda i, j: rrand[:, rpos[Wn.rv(i % n, j)]]
        pred = np.ones(m, bool)
        for i in range(n):
            for j in (0, 2):
                pred &= (b_(i, j) == b_(i + 1, j)) & (rh_(i, j) == b_(i, j))
            pred &= (b_(i, 0) + b_(i, 1) + rv_(i, 0)) >= 1
            pred &= (b_(i, 1) + b_(i, 2) + rv_(i, 1)) >= 1
        print(f"    {m} random patterns (half drawn from killing bottoms), true rule: band empty in {int(emp.sum())}; "
              f"the journal's conditions predict the same set: {bool((emp == pred).all())}")
        assert (emp == pred).all() and emp.sum() > 100

    section("claim 23: the lone cell of the layer under an empty sheet (wall 3 x 3)")
    W3 = Wall(3, 3)
    V3 = W3.V
    p = W3.h(0, 0)
    inl = [q for q in V3.nlist[p] if q in set(W3.B)]
    seven = [p] + inl
    assert len(set(seven)) == 7
    relb = sorted({q for c in seven for q in V3.nlist[c] if V3.cells[q][2] == Z - 2})
    relr = sorted({q for c in seven for q in V3.nlist[c] if V3.cells[q][2] == Z - 3})
    print(f"  cells that matter: {len(relb)} bottoms, {len(relr)} below the layer")
    assert (len(relb), len(relr)) == (6, 7)
    pat = bits(13, 0, 1 << 13)
    X = np.zeros((1 << 13, V3.N), np.int8)
    X[:, relb + relr] = pat
    X[:, p] = 1
    emp = V3.step(X)[:, W3.band].sum(axis=1) == 0
    print(f"  of the 2^13 patterns, {int(emp.sum())} leave the band empty next (journal 3,793): {emp.sum() / 8192:.4f}")
    assert emp.sum() == 3793

    def poly(rb, rr_):
        a, ab, x = rb, 1 - rb, 1 - rr_
        return (ab ** 6 + 6 * a * ab ** 5 + a ** 2 * ab ** 4 * (8 + 7 * x) + a ** 3 * ab ** 3 * (2 + 8 * x + 10 * x ** 2)
                + a ** 4 * ab ** 2 * (5 * x ** 2 + 8 * x ** 3 + 2 * x ** 4) + a ** 5 * ab * (2 * x ** 4 + 4 * x ** 5) + a ** 6 * x ** 7)
    nb1 = pat[:, :6].sum(axis=1); nr1 = pat[:, 6:].sum(axis=1)
    for rb, rr_ in [(0.5, 0.5), (0.52, 0.52), (0.398, 0.398), (0.4155, 0.4155), (0.3, 0.8), (0.9, 0.1)]:
        en = float((rb ** nb1 * (1 - rb) ** (6 - nb1) * rr_ ** nr1 * (1 - rr_) ** (7 - nr1))[emp].sum())
        print(f"    rho_beta = {rb}, rho_r = {rr_}: enumeration {en:.6f}, ladder polynomial {poly(rb, rr_):.6f}")
        assert abs(en - poly(rb, rr_)) < 1e-12
    gump = lambda r: (1 - 3 * r ** 3 + 3 * r ** 5 - r ** 6) * (1 - r ** 3) ** 4
    print(f"    journal's numbers: 3793/8192 = {3793 / 8192:.4f}; at 0.52: face12e {poly(.52, .52):.4f} (0.4214), gump {gump(.52):.4f} (0.3668); "
          f"face12e at 0.398: {poly(.398, .398):.3f} (0.672), at 0.4155: {poly(.4155, .4155):.3f} (0.638); gump at 0.4155: {gump(.4155):.3f} (0.606); "
          f"(7/8)^7 = {0.875 ** 7:.3f}")
    # control: a wall too small for the six cubes to be distinct
    Wc = Wall(2, 2)
    Vc = Wc.V
    pc = Wc.h(0, 0)
    sev = [pc] + [q for q in Vc.nlist[pc] if q in set(Wc.B)]
    rel = sorted({q for c in sev for q in Vc.nlist[c] if Vc.cells[q][2] in (Z - 2, Z - 3)})
    X = np.zeros((1 << len(rel), Vc.N), np.int8)
    X[:, rel] = bits(len(rel), 0, 1 << len(rel)); X[:, pc] = 1
    e2 = Vc.step(X)[:, Wc.band].sum(axis=1) == 0
    print(f"    control, wall 2 x 2 (cubes coincide): {int(e2.sum())} of 2^{len(rel)} = {e2.mean():.4f}, not 0.4630")
    assert abs(e2.mean() - 3793 / 8192) > 1e-3

    section("claim 6 (face12e): a lone closed cube under the wall")
    cube = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    # a cell outside a cube sees at most two of its faces
    mx = 0
    for x, y, z in itertools.product(range(-4, 5), repeat=3):
        if (x % 2) + (y % 2) + (z % 2) == 1 and (x, y, z) not in cube:
            mx = max(mx, sum(1 for q in neighbours((x, y, z), "edge") if q in cube))
    ins = [sum(1 for q in neighbours(c, "edge") if q in cube) for c in cube]
    print(f"  each face of a cube sees {set(ins)} of the others; a cell outside sees at most {mx}")
    assert set(ins) == {4} and mx == 2
    for k in (1, 2):
        for half, label in ((2 * k + 2, 'journal'), (2 * k - 2, 'control: 2k - 2')):
            Dm = 4 * k + 4
            cells = [(x, y, z) for x in range(-Dm, Dm + 1) for y in range(-Dm, Dm + 1) for z in range(-Dm, 2)
                     if (x % 2) + (y % 2) + (z % 2) == 1]                 # wall at z = 1: the cube (0,0,0) is a top cube
            Vg = Vessel(cells, coplanar="edge")
            cf = [Vg.index[c] for c in cube]
            inbox = np.array([max(abs(c) for c in p_) <= half for p_ in Vg.cells])
            fails = 0
            for dens in (0.3, 0.5, 0.7):
                X = (rng.random((500, Vg.N)) < dens).astype(np.int8)
                X[:, inbox] = 0
                X[:, cf] = 1
                for _ in range(k):
                    X = Vg.step(X)
                fails += int((X[:, cf].sum(axis=1) < 6).sum())
            print(f"  k = {k}, box half-width {half} ({label}): cube not intact after {k} generations in {fails} of 1500 random outsides")
            if label == 'journal':
                assert fails == 0
    print(f"\nall assertions passed  [{time.time() - t00:.0f} s]")


if __name__ == "__main__":
    main()
