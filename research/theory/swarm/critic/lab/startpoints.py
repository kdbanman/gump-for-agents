"""Critic's lab, round 0b: checks of the three "Starting points" of swarm/PROBLEM.md (revision of 2026-11-13).
Exact computations only.

  python3 startpoints.py bijection   counting: mean time for a bijection to fall into a trapdoor H
  python3 startpoints.py monotone    probability: the capped rule against the uncapped (monotone) rule
  python3 startpoints.py triangles   how the cells beneath a gump face are shared; one-generation emptiability
  python3 startpoints.py game R      the face game on a hull face (R = 3, 5): generations needed to empty it
  python3 startpoints.py crossing    path: generations needed to cross a face, against the length of the plunge
  python3 startpoints.py slab        path: sealed bands (transverse firewalls) in periodic slabs, against the face
  python3 startpoints.py image       counting: how far from invertible (|F^t(X)| / |X|, small vessels)
  python3 startpoints.py all         everything except `game 5` and the slower integer programmes
"""
import sys, os, itertools, random
from fractions import Fraction
from collections import deque
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
import gump_lab as g3
import toy2d_lab as t2

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ------------------------------------------------------------------------------------------------ bijection
def bijection(nmax=7):
    """f a bijection of X (n points), H a nonempty subset, T(x) = min{t >= 0 : f^t(x) in H} (infinite if the
    cycle of x misses H).  Claims tested, every permutation and every H for n <= nmax:
      (a) if every cycle meets H:  mean T >= n/(2|H|) - 1/2            [the lemma of PROBLEM.md]
      (b) always:                  #{x : T(x) <= t} <= (t + 1)|H|       [union bound; implies (a)]
      (c) the mean over the points that do fall is >= n'/(2|H|) - 1/2 with n' = their number, and can be far
          below n/(2|H|) - 1/2."""
    print("bijection with a trapdoor: every permutation of n <= %d points, every nonempty H" % nmax)
    a_ok = b_ok = c_ok = True
    eq = 0; cases = 0; worst_cond = None
    for n in range(1, nmax + 1):
        for f in itertools.permutations(range(n)):
            # cycles
            seen = [False] * n; cyc = []
            for x in range(n):
                if not seen[x]:
                    c = []; y = x
                    while not seen[y]:
                        seen[y] = True; c.append(y); y = f[y]
                    cyc.append(c)
            for Hm in range(1, 1 << n):
                h = bin(Hm).count('1')
                tot = 0; nfall = 0; allhit = True
                cnt = {}
                for c in cyc:
                    pos = [i for i, y in enumerate(c) if (Hm >> y) & 1]
                    if not pos:
                        allhit = False; continue
                    l = len(c); nfall += l
                    for i in range(l):
                        t = min((p - i) % l for p in pos)
                        tot += t; cnt[t] = cnt.get(t, 0) + 1
                cases += 1
                run = 0
                for t in sorted(cnt):
                    run += cnt[t]
                    if run > (t + 1) * h:
                        b_ok = False
                bound_cond = Fraction(nfall, 2 * h) - Fraction(1, 2)
                if Fraction(tot, nfall) < bound_cond:
                    c_ok = False
                if allhit:
                    d = Fraction(tot, n) - (Fraction(n, 2 * h) - Fraction(1, 2))
                    if d < 0:
                        a_ok = False
                    if d == 0:
                        eq += 1
                else:
                    gap = Fraction(tot, nfall) - (Fraction(n, 2 * h) - Fraction(1, 2))
                    if worst_cond is None or gap < worst_cond[0]:
                        worst_cond = (gap, n, f, Hm, Fraction(tot, nfall))
    check(a_ok, f"(a) mean T >= n/(2|H|) - 1/2 whenever every cycle meets H ({cases} cases; equality in {eq}: equal gaps)")
    check(b_ok, "(b) #{T <= t} <= (t+1)|H| for every t (needs only that the uniform measure is invariant)")
    check(c_ok, "(c) mean over the points that fall >= n'/(2|H|) - 1/2, n' = number of points on cycles meeting H")
    g, n, f, Hm, m = worst_cond
    print(f"  the conditional mean can be far below n/(2|H|) - 1/2: n = {n}, f = {f}, H = {[i for i in range(n) if (Hm >> i) & 1]}: "
          f"mean over those that fall = {m}, n/(2|H|) - 1/2 = {Fraction(n, 2 * bin(Hm).count('1')) - Fraction(1, 2)}")


# ------------------------------------------------------------------------------------------------- monotone
def step_nb(nb, x, lo_b, lo_s, cap):
    n = np.array([sum(int(x[j]) for j in v) for v in nb])
    alive = np.where(x == 1, n >= lo_s, n >= lo_b)
    if cap is not None:
        alive &= n <= cap
    return alive.astype(np.uint8)


def monotone():
    print("capped rule G against the uncapped threshold rule F (gump: n + x >= 4, cap n <= 5; 2D: n + x >= 3, cap n <= 4)")
    # (i) local tables: G <= F, and F is monotone in (x, n)
    for name, K, th, cap in (('gump', 12, 4, 5), ('2D', 8, 3, 4)):
        G = lambda x, n: int(n + x >= th and n <= cap)
        F = lambda x, n: int(n + x >= th)
        check(all(G(x, n) <= F(x, n) for x in (0, 1) for n in range(K + 1)), f"{name}: G <= F at every (x, n)")
        check(all(F(x, n) <= F(x2, n2) for x in (0, 1) for n in range(K + 1) for x2 in (x, 1) for n2 in range(n, K + 1)),
              f"{name}: F is monotone")
    # (ii) what survives of the all-alive state: the only cells a monotone minorant H <= G can ever make alive,
    #      because H(S) <= H(all) <= G(all)
    for R, ce in ((5, 'c'), (7, 'c'), (6, 'v'), (9, 'c')):
        cells, c = g3.hull(R, ce); nb = g3.nbrs(cells)
        x = step_nb(nb, np.ones(len(cells), np.uint8), 4, 3, 5)
        deg = sorted(set(len(nb[i]) for i in np.flatnonzero(x)))
        x2 = step_nb(nb, x, 4, 3, 5)
        print(f"  gump hull R={R}{ce}: G(all alive) has {int(x.sum())} of {len(cells)} cells (in-vessel degrees {deg}); "
              f"G(G(all alive)) has {int(x2.sum())}")
    for (a, b, m) in ((3, 3, 3), (4, 4, 8)):
        cells, nb = make_slab(a, b, m)
        x = step_nb(nb, np.ones(len(cells), np.uint8), 4, 3, 5)
        print(f"  gump slab {a}x{b}, {m} layers: G(all alive) has {int(x.sum())} of {len(cells)} cells")
    for kind, H, L in (('strip', 6, 12), ('box', 6, 12)):
        nb = t2.nbrs(H, L, kind == 'strip')
        x = step_nb(nb, np.ones(H * L, np.uint8), 3, 2, 4)
        x2 = step_nb(nb, x, 3, 2, 4)
        print(f"  2D {kind} {H}x{L}: G(all alive) has {int(x.sum())} of {H * L} cells; G(G(all alive)) has {int(x2.sum())}")
    # (iii) orbit domination G^t(S) <= F^t(S) (two-line proof; here a sanity run)
    dom = True
    cells, c = g3.hull(7, 'c'); nb = g3.nbrs(cells)
    for seed in range(10):
        rng = np.random.default_rng(seed)
        x = (rng.random(len(cells)) < rng.choice([0.2, 0.3, 0.4])).astype(np.uint8); y = x.copy()
        for t in range(40):
            x = step_nb(nb, x, 4, 3, 5); y = step_nb(nb, y, 4, 3, None)
            dom &= bool((x <= y).all())
    check(dom, "gump hull R=7: capped orbit below uncapped orbit, 10 soups x 40 generations")
    # (iv) the driven face (face layer over arbitrary cells beneath): interior face cells of a full face die
    cells, c = g3.hull(13, 'c'); nb = g3.nbrs(cells)
    face = g3.faces(cells, c, 13)[(1, 1, 1)]; fs = set(face)
    kin = [sum(1 for j in nb[i] if j in fs) for i in face]
    print(f"  face of the R=13 hull: in-face degree of its cells: { {k: kin.count(k) for k in sorted(set(kin))} }; a cell with "
          f"in-face degree 6 is dead after a full face whatever lies beneath (n >= 6)")


# ------------------------------------------------------------------------------------------------ triangles
def face_setup(R, d=(1, 1, 1)):
    cells, c = g3.hull(R, 'c'); nb = g3.nbrs(cells)
    face = g3.faces(cells, c, R)[d]
    fs = set(face)
    s = lambda i: sum(d[k] * cells[i][k] for k in range(3))
    inl = {i: [j for j in nb[i] if j in fs] for i in face}
    ben1 = {i: [j for j in nb[i] if s(j) == R - 2] for i in face}
    ben2 = {i: [j for j in nb[i] if s(j) == R - 4] for i in face}
    return cells, nb, face, inl, ben1, ben2


def components(face, ben):
    """connected components of 'shares a cell beneath' among face cells; ben: dict face cell -> list of cells beneath."""
    owner = {}
    for i in face:
        for j in ben[i]:
            owner.setdefault(j, []).append(i)
    adj = {i: set() for i in face}
    for j, v in owner.items():
        for a in v:
            for b in v:
                if a != b:
                    adj[a].add(b)
    seen = set(); comps = []
    for i in face:
        if i not in seen:
            comp = []; dq = deque([i]); seen.add(i)
            while dq:
                a = dq.popleft(); comp.append(a)
                for b in adj[a]:
                    if b not in seen:
                        seen.add(b); dq.append(b)
            comps.append(sorted(comp))
    return comps, owner


def achievable(comp, ben):
    """set of tuples (b_c for c in comp) over all 0/1 assignments of the cells beneath the component."""
    under = sorted(set(j for i in comp for j in ben[i]))
    out = set()
    for bits in itertools.product((0, 1), repeat=len(under)):
        val = dict(zip(under, bits))
        out.add(tuple(sum(val[j] for j in ben[i]) for i in comp))
    return out


def triangles():
    print("the cells beneath a gump face (face of the R = 13 hull, 84 cells; d = (1,1,1))")
    cells, nb, face, inl, ben1, ben2 = face_setup(13)
    full = [i for i in face if len(nb[i]) == 9]
    ben = {i: ben1[i] + ben2[i] for i in face}
    comps, owner = components(face, ben)
    inner = [cp for cp in comps if all(i in full for i in cp)]
    check(all(len(ben1[i]) == 2 and len(ben2[i]) == 1 for i in full), "a face cell with all 9 neighbours has 2 one layer in, 1 two layers in")
    own2 = {}
    for i in face:
        for j in ben2[i]:
            own2.setdefault(j, []).append(i)
    check(all(len(v) == 1 for v in own2.values()), "every cell two layers in lies beneath exactly one face cell (private)")
    own1 = {}
    for i in face:
        for j in ben1[i]:
            own1.setdefault(j, []).append(i)
    print(f"  cells one layer in beneath the face: {len(own1)}; number of face cells above each: "
          f"{ {k: [len(v) for v in own1.values()].count(k) for k in (1, 2, 3)} }")
    check(all(len(cp) == 3 for cp in inner), f"components of 'share a cell beneath' made of 9-neighbour cells are triples ({len(inner)} of them)")
    tri_ok = all(all(b in inl[a] for a in cp for b in cp if a != b) for cp in inner)
    check(tri_ok, "each such triple is a triangle of in-face neighbours (a kagome triangle)")
    # each triangle: three shared cells, each beneath exactly two of the three; orientation
    sh_ok = True; orient = set()
    for cp in inner:
        shared = sorted(set(j for i in cp for j in ben1[i]))
        sh_ok &= len(shared) == 3 and all(sum(1 for i in cp if j in ben1[i]) == 2 for j in shared)
        orient.add(tuple(sorted(g3.axis(cells[i]) for i in cp)))
        cen = np.mean([cells[i] for i in cp], axis=0)
    check(sh_ok, "beneath a triangle: three cells one layer in, each beneath exactly two of its three cells")
    print(f"  normal axes of the three cells of a triangle: {orient}")
    sizes = sorted(len(cp) for cp in comps)
    print(f"  all components on this face (rim included), by size: { {k: sizes.count(k) for k in sorted(set(sizes))} }")
    # which kagome triangles: the face cells form up- and down-triangles; only one kind is a component
    tris = set()
    for a in full:
        for b in inl[a]:
            for cc in inl[b]:
                if cc in inl[a] and a < b < cc:
                    tris.add((a, b, cc))
    comp_set = set(tuple(cp) for cp in comps if len(cp) == 3)
    n_in = sum(1 for t in tris if t in comp_set)
    print(f"  in-face neighbour triangles through 9-neighbour cells: {len(tris)}; of these, components: {n_in} "
          f"(a cell lies in several neighbour triangles and in exactly one component)")
    cp = inner[0]
    ach = achievable(cp, ben)
    print(f"  achievable (b1, b2, b3) for one triangle: {len(ach)} of 64")
    print(f"    not achievable: {sorted(set(itertools.product(range(4), repeat=3)) - ach)}")
    check(not any(t[0] == 3 and t[1] == 0 for t in ach), "(3, 0, .) is not achievable: the frustration of board E10")
    # distribution of (b1,b2,b3) is a function of six independent cells; marginal b ~ Binomial(3, rho)
    # one-generation emptiability, recomputed by components, against the SAT counts of face_one_step.py
    for R, want_bad, want_all in ((3, 187, 512), (5, 180615, 262144)):
        bad = emptiable_count(R)
        check(bad == want_bad, f"R={R} face: configurations that cannot be emptied in one generation: {bad} of {want_all} "
                               f"(SAT, face_one_step.py: {want_bad})")


def emptiable_count(R):
    cells, nb, face, inl, ben1, ben2 = face_setup(R)
    fs = set(face)
    ben = {i: [j for j in nb[i] if j not in fs] for i in face}        # as face_one_step.py: every neighbour off the face
    comps, _ = components(face, ben)
    pos = {i: t for t, i in enumerate(face)}
    A = len(face)
    inmask = [sum(1 << pos[j] for j in inl[i]) for i in face]
    ach = [achievable(cp, ben) for cp in comps]
    memo = {}
    bad = 0
    for m in range(1 << A):
        ok = True
        for ci, cp in enumerate(comps):
            key = (ci,) + tuple(((m >> pos[i]) & 1, bin(m & inmask[pos[i]]).count('1')) for i in cp)
            r = memo.get(key)
            if r is None:
                r = any(all(not ((3 if x else 4) <= k + b <= 5) for (x, k), b in zip(key[1:], bt)) for bt in ach[ci])
                memo[key] = r
            if not r:
                ok = False; break
        bad += not ok
    return bad


def game(R):
    """Face game: each generation the cells beneath are chosen freely. depth[S] = fewest generations to empty S."""
    cells, nb, face, inl, ben1, ben2 = face_setup(R)
    fs = set(face)
    ben = {i: [j for j in nb[i] if j not in fs] for i in face}
    comps, _ = components(face, ben)
    order = [i for cp in comps for i in cp]                 # component bits contiguous, first component = high bits
    A = len(order)
    pos = {i: A - 1 - t for t, i in enumerate(order)}      # bit position in the state integer
    inmask = {i: sum(1 << pos[j] for j in inl[i]) for i in face}
    ach = [achievable(cp, ben) for cp in comps]
    shape = tuple(1 << len(cp) for cp in comps)
    memo = {}

    def outcomes(m):
        res = []
        for ci, cp in enumerate(comps):
            key = (ci,) + tuple(((m >> pos[i]) & 1, bin(m & inmask[i]).count('1')) for i in cp)
            r = memo.get(key)
            if r is None:
                s = set()
                for bt in ach[ci]:
                    v = 0
                    for (x, k), b in zip(key[1:], bt):
                        v = (v << 1) | int((3 if x else 4) <= k + b <= 5)
                    s.add(v)
                r = np.array(sorted(s))
                memo[key] = r
            res.append(r)
        return res

    print(f"face game on the face of the R={R} hull: {A} cells, {len(comps)} components beneath, {1 << A} configurations")
    outs = [outcomes(m) for m in range(1 << A)]
    depth = np.full(1 << A, -1, np.int32); depth[0] = 0
    W = np.zeros(1 << A, bool); W[0] = True
    d = 0
    while True:
        d += 1
        Wv = W.reshape(shape)
        new = []
        for m in np.flatnonzero(depth < 0):
            if Wv[np.ix_(*outs[m])].any():
                new.append(m)
        if not new:
            break
        depth[new] = d; W[new] = True
        print(f"  emptied in exactly {d} generation(s): {len(new)}")
    never = int((depth < 0).sum())
    print(f"  never emptiable whatever lies beneath: {never}")
    if never:
        m = int(np.flatnonzero(depth < 0)[0])
        print("   example:", sorted(cells[i] for i in face if (m >> pos[i]) & 1))
    return depth


# ------------------------------------------------------------------------------------------------- crossing
def bfs(nb, src, allowed=None):
    dist = {src: 0}; dq = deque([src])
    while dq:
        a = dq.popleft()
        for b in nb[a]:
            if b not in dist and (allowed is None or b in allowed):
                dist[b] = dist[a] + 1; dq.append(b)
    return dist


def crossing():
    print("generations for influence to cross a face (graph distance; one step per generation), hull faces")
    print("  measured plunge: 10-12 generations at A = 30-84 (fluct README, 'the last generations'); ordinary until -16")
    for R in (7, 9, 11, 13, 15, 17):
        cells, c = g3.hull(R, 'c'); nb = g3.nbrs(cells)
        face = g3.faces(cells, c, R)[(1, 1, 1)]; fs = set(face)
        dv = 0; df = 0; ecc = []
        for i in face:
            d1 = bfs(nb, i); d2 = bfs(nb, i, fs)
            e = max(d1[j] for j in face); ecc.append(e)
            dv = max(dv, e); df = max(df, max(d2[j] for j in face))
        print(f"  R={R:2d}, A={len(face):3d}: farthest pair of face cells: {dv} generations through the vessel "
              f"({df} staying in the face layer); from the best-placed cell every face cell is within {min(ecc)}")


# ----------------------------------------------------------------------------------------------------- slab
def make_slab(a, b, m):
    """m consecutive {111} layers s = x+y+z = -1, -3, ..., -(2m-1), modulo the in-plane translations
    (2a, 0, -2a) and (0, 2b, -2b): 3ab cells per layer (the geometry of exponent/xp.py and of research/peeling).
    Returns (cells as (x mod 2a, y mod 2b, s), neighbour lists)."""
    layers = [-(2 * j + 1) for j in range(m)]
    cells = []
    for s in layers:
        for x in range(2 * a):
            for y in range(2 * b):
                z = s - x - y
                if (x & 1) + (y & 1) + (z & 1) == 1:
                    cells.append((x, y, s))
    ix = {cc: i for i, cc in enumerate(cells)}
    nb = []
    for (x, y, s) in cells:
        p = (x, y, s - x - y)
        v = []
        for o in g3.OFF[g3.axis(p)]:
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            cc = (q[0] % (2 * a), q[1] % (2 * b), sum(q))
            if cc in ix:
                v.append(ix[cc])
        nb.append(v)
    return cells, nb


def slab_selftest(a, b, m, gens=3, reps=3):
    """my slab stepper against the open-lattice set stepper applied to the unrolled pattern (copies over a block of
    periods wide enough that the edge of the block cannot reach the central copy in `gens` generations)."""
    cells, nb = make_slab(a, b, m)
    good = len(cells) == 3 * a * b * m and all(len(set(v)) == len(v) for v in nb)
    good &= all((i in nb[j]) for i, v in enumerate(nb) for j in v)
    for seed in range(reps):
        rng = np.random.default_rng(seed)
        x = (rng.random(len(cells)) < 0.45).astype(np.uint8)
        k = gens + 2                                    # periods on each side
        live = set()
        for i, (cx, cy, s) in enumerate(cells):
            if x[i]:
                for u in range(-k, k + 1):
                    for v in range(-k, k + 1):
                        X = cx + 2 * a * u; Y = cy + 2 * b * v
                        live.add((X, Y, s - X - Y))
        y = x.copy()
        for t in range(gens):
            live = g3.step_set(live)
            y = step_nb(nb, y, 4, 3, 5)
        # T4: nothing outside the slab's layers near the centre
        for i, (cx, cy, s) in enumerate(cells):
            good &= ((cx, cy, s - cx - cy) in live) == bool(y[i])
        good &= not any(abs(p[0]) < 2 * a and abs(p[1]) < 2 * b and not (-(2 * m - 1) <= sum(p) <= -1) for p in live)
    return good


def slab_report(ip=True):
    from math import gcd
    import sealed_min as sm
    print("periodic slabs: m {111} layers on an a x b torus (two faces of A = 3ab cells)")
    check(all(slab_selftest(a, b, m) for (a, b, m) in ((3, 3, 3), (4, 3, 4), (4, 4, 3))),
          "slab stepper = open-lattice stepper on the unrolled pattern (3 slabs x 3 soups x 3 generations); 3abm cells; "
          "12 distinct neighbours, symmetric")
    print("  bands = three consecutive layers of one of the other three diagonals (T3 firewall); they close up on the torus")
    rows = []
    for (a, b, m) in ((3, 3, 3), (4, 4, 3), (5, 5, 3), (6, 6, 3), (3, 3, 8), (4, 4, 8), (5, 5, 8), (5, 6, 8), (8, 8, 8),
                      (12, 12, 8), (13, 13, 8), (4, 4, 12), (5, 5, 12)):
        cells, nb = make_slab(a, b, m)
        A = 3 * a * b
        face = [i for i, cc in enumerate(cells) if cc[2] == -1]
        assert len(face) == A and sm.is_sealed(nb, face, 3)
        best = None
        for name, f, per in (("x+y-z", lambda x, y, s: (2 * x + 2 * y - s) % (4 * gcd(a, b)), 4 * gcd(a, b)),
                             ("x-y+z", lambda x, y, s: (s - 2 * y) % (4 * b), 4 * b),
                             ("-x+y+z", lambda x, y, s: (s - 2 * x) % (4 * a), 4 * a)):
            vals = sorted(set(f(*cc) for cc in cells))
            if len(vals) < 4:
                continue
            for v0 in vals[:1]:
                band = [i for i, cc in enumerate(cells) if f(*cc) in (v0, (v0 + 2) % per, (v0 + 4) % per)]
                sealed = sm.is_sealed(nb, band, 3)
                two = [i for i, cc in enumerate(cells) if f(*cc) in (v0, (v0 + 2) % per)]
                if best is None or len(band) < best[1]:
                    best = (name, len(band), sealed, sm.is_sealed(nb, two, 3))
        rows.append((a, b, m, A, best))
        print(f"  {a}x{b}, m={m}: face {A} cells (sealed); smallest band: {best[1]} cells along {best[0]}, "
              f"sealed: {best[2]} (two layers only: sealed {best[3]}); band/face = {best[1] / A:.2f}")
    print("  band = 4.5 m min(a,b) cells for a = b; smaller than the face (3ab) iff a > 1.5 m")
    if ip:
        print("  smallest nonempty sealed set (integer programme, proved optimal unless said):")
        for (a, b, m) in ((3, 3, 3), (4, 4, 3), (5, 5, 3), (6, 6, 3), (4, 4, 4), (3, 3, 8)):
            cells, nb = make_slab(a, b, m)
            W, res = sm.min_sealed(nb, 3, time_limit=150)
            lay = {}
            for i in W:
                lay[cells[i][2]] = lay.get(cells[i][2], 0) + 1
            kind = 'one whole face' if (len(lay) == 1 and len(W) == 3 * a * b) else f'cells per layer {dict(sorted(lay.items(), reverse=True))}'
            print(f"    {a}x{b}, m={m} ({len(cells)} cells): {len(W)} cells ({kind})",
                  '| optimal' if res.status == 0 else f'| NOT proved optimal (status {res.status})')


# ---------------------------------------------------------------------------------------------------- image
def image():
    print("how far from invertible: |F^t(X)| / |X| (every state; F^t(X) decreases to the set of cyclic states)")
    cases = [('2D strip 3x6', t2.nbrs(3, 6, True), t2.B, t2.S), ('2D box 4x5', t2.nbrs(4, 5, False), t2.B, t2.S),
             ('2D strip 4x6', t2.nbrs(4, 6, True), t2.B, t2.S)]
    cells, c = g3.hull(2, 'v')
    cases.append(('gump hull R=2v', g3.nbrs(cells), g3.B, g3.S))
    for name, nb, B, S in cases:
        N = len(nb)
        F = exact.full_map(nb, B, S)
        img = np.ones(1 << N, bool); sizes = []
        for t in range(1, 60):
            nxt = np.zeros(1 << N, bool); nxt[F[img]] = True
            sizes.append(int(nxt.sum()))
            if (nxt == img).all():
                break
            img = nxt
        fr = [f"{s / (1 << N):.4f}" for s in sizes[:6]]
        print(f"  {name} ({N} cells): |F^t(X)|/|X| at t = 1..6: {', '.join(fr)}; eventual image {sizes[-1]} states "
              f"= {sizes[-1] / (1 << N):.5f}; entropy lost in one step {N - np.log2(sizes[0]):.2f} of {N} bits")


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('bijection', 'all'):
        bijection()
    if what in ('monotone', 'all'):
        monotone()
    if what in ('triangles', 'all'):
        triangles()
    if what == 'game':
        game(int(sys.argv[2]))
    if what in ('crossing', 'all'):
        crossing()
    if what in ('slab', 'all'):
        slab_report(ip=(what == 'slab'))
    if what in ('image', 'all'):
        image()
    print('ALL OK' if OK else 'SOMETHING FAILED')
