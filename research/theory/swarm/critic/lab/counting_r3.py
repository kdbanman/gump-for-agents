"""Critic's lab: counting, round 3 (closing report). Exact; no sampling.

face12e = gump's cells (faces of the cubic honeycomb, doubled coordinates with one odd entry) and gump's rule
B45/S345, but the four coplanar neighbours of a face share an EDGE with it (+-2e_b, +-2e_c). It is not gump.
Vessel: slab 1 <= x <= 9 (four cubes deep), walls at x = 1 and x = 9, periodic N x M in y, z.
  sheet S        x-normal faces (1, 2i, 2j)                       'tops' sigma_(i,j) of the top cubes (2, 2i, 2j)
  layer B        (2, 2i+1, 2j) = h(i,j), between cubes (i,j), (i+1,j);  (2, 2i, 2j+1) = v(i,j), between (i,j), (i,j+1)
  bottoms        (3, 2i, 2j) = beta_(i,j);   private cells r_p = p + (2, 0, 0) at x = 4
The stepper is research/audit/class/lead_check.py (plain numpy on a cell graph; `validate` there checks it
against reference/oracle.py with gump's offsets); `structure` below re-derives the face12e offsets from the
definition "the twelve faces that share an edge" and compares.

  python3 counting_r3.py structure   Proposition F items 1-3, 5 and path's Lemma F (i), (ii) read off the graph; the lone closed cube
  python3 counting_r3.py lone        lab request 1: 3,793 of 2^13; the ladder polynomial coefficient by coefficient
  python3 counting_r3.py pi1         lab request 2: configuration Pi_1 on walls 3 x 4 and 4 x 4; the table of classes
  python3 counting_r3.py theta       lab request 2, second part: Theta on box walls n x n, n = 3..7; every sheet of the periodic walls 3 x 3, 4 x 4, 5 x 5 (1 min)
  python3 counting_r3.py oh          lab request 3: the O_h faces R = 3, 5, 7, 9 (cube-centred), 4, 6, 8, 10 (vertex-centred)
  python3 counting_r3.py lemma8      Lemma 8 on D2 rings: the Perron vector phi, the doom mass pi(1 - phi) of product rows,
                                     the inequality against exact P(T <= k)   (about 2 min)
  python3 counting_r3.py all
"""
import sys, os, itertools, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'audit', 'class')))
import lead_check as lc
import gump_lab as g3

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# --------------------------------------------------------------------------------------------- face12e geometry
def edge_sharing_offsets(axis):
    """The offsets to the faces that share an edge with a face of normal `axis`, from the geometry: a unit face
    centred at p (doubled coordinates) has four edges with midpoints p +- e_b, p +- e_c; the faces containing the
    edge with midpoint m (direction c, say) are m +- e_a and m +- e_b."""
    a = axis; b, c = [i for i in range(3) if i != a]
    out = set()
    for (t, u) in ((b, c), (c, b)):               # edge midpoint p +- e_t, edge runs along u
        for s in (1, -1):
            m = [0, 0, 0]; m[t] = s
            for w in (a, t):                      # the two axes perpendicular to the edge
                for s2 in (1, -1):
                    q = list(m); q[w] += s2
                    if any(q):
                        out.add(tuple(q))
    return out


def slab(N, M):
    cells, nbr = lc.graph((11, 2 * N, 2 * M), (False, True, True), "edge", xrange_=(1, 9))
    idx = {tuple(int(v) for v in p): i for i, p in enumerate(cells)}
    return cells, nbr, idx


def step1(state, nbr):
    """state: (R, n) uint8 -> next, via lead_check.step."""
    s = np.zeros((state.shape[0], state.shape[1] + 1), np.uint8); s[:, :-1] = state
    return lc.step(s, nbr)[:, :-1]


def names(N, M, idx):
    top = lambda i, j: idx[(1, 2 * (i % N), 2 * (j % M))]
    h = lambda i, j: idx[(2, (2 * i + 1) % (2 * N), 2 * (j % M))]
    v = lambda i, j: idx[(2, 2 * (i % N), (2 * j + 1) % (2 * M))]
    bot = lambda i, j: idx[(3, 2 * (i % N), 2 * (j % M))]
    rh = lambda i, j: idx[(4, (2 * i + 1) % (2 * N), 2 * (j % M))]
    rv = lambda i, j: idx[(4, 2 * (i % N), (2 * j + 1) % (2 * M))]
    return top, h, v, bot, rh, rv


def structure():
    print("face12e: the graph, and what counting's Proposition F and path's Lemma F read off it")
    lc.validate()
    for a in range(3):
        check(set(lc.offsets(a, "edge")) == edge_sharing_offsets(a) and len(edge_sharing_offsets(a)) == 12,
              f"axis {a}: lead_check's face12e offsets = the twelve faces sharing an edge (derived from the edge midpoints)")
    N = M = 4
    cells, nbr, idx = slab(N, M); n = len(cells)
    xs = cells[:, 0]
    S = np.flatnonzero(xs == 1); B = np.flatnonzero(xs == 2)
    def by_layer(i):
        out = {}
        for j in nbr[i]:
            key = 'outside' if j == n else int(xs[j])
            out[key] = out.get(key, 0) + 1
        return out
    check(all(by_layer(i) == {1: 4, 2: 4, 'outside': 4} for i in S), "every sheet cell: 4 neighbours in the sheet, 4 in the layer beneath, 4 outside, none elsewhere (F.1, F.3; Lemma F (i))")
    check(all(by_layer(i) == {2: 6, 1: 2, 3: 2, 4: 1, 'outside': 1} for i in B), "every cell of the layer: 6 in the layer, 2 in the sheet, 2 bottoms, 1 two layers in, 1 outside (F.1; Lemma F (ii))")
    top, h, v, bot, rh, rv = names(N, M, idx)
    good = True
    for i in range(N):
        for j in range(M):
            good &= sorted(int(t) for t in nbr[top(i, j)] if t != n) == sorted([top(i + 1, j), top(i - 1, j), top(i, j + 1), top(i, j - 1), h(i, j), h(i - 1, j), v(i, j), v(i, j - 1)])
            good &= sorted(int(t) for t in nbr[h(i, j)] if t != n) == sorted([h(i, j + 1), h(i, j - 1), v(i, j), v(i, j - 1), v(i + 1, j), v(i + 1, j - 1), top(i, j), top(i + 1, j), bot(i, j), bot(i + 1, j), rh(i, j)])
            good &= sorted(int(t) for t in nbr[v(i, j)] if t != n) == sorted([v(i + 1, j), v(i - 1, j), h(i, j), h(i - 1, j), h(i, j + 1), h(i - 1, j + 1), top(i, j), top(i, j + 1), bot(i, j), bot(i, j + 1), rv(i, j)])
            readers = sorted(t for t in range(n) if bot(i, j) in nbr[t] and xs[t] <= 2)
            good &= readers == sorted([h(i, j), h(i - 1, j), v(i, j), v(i, j - 1)])
            good &= [t for t in range(n) if rh(i, j) in nbr[t] and xs[t] <= 2] == [h(i, j)] and [t for t in range(n) if rv(i, j) in nbr[t] and xs[t] <= 2] == [v(i, j)]
    check(good, "names: sigma_q sees its 4 sheet neighbours and the 4 sides of q; h(i,j), v(i,j) see exactly the cells listed in entry 14; beta_q is read by the 4 sides of q only, r_p by p only")
    rng = np.random.default_rng(3)
    # F.2: H = {S = 0, B = 0} absorbing; neither half alone
    st = (rng.random((4096, n)) < 0.5).astype(np.uint8); st[:, S] = 0; st[:, B] = 0
    nx = step1(st, nbr)
    check(not nx[:, S].any() and not nx[:, B].any(), "F.2: band empty stays empty (4,096 random states of the rest; also by the counts: a band cell sees at most 3 cells outside the band)")
    st = np.zeros((1, n), np.uint8); st[0, [h(0, 0), h(-1, 0), v(0, 0), v(0, -1)]] = 1
    check(step1(st, nbr)[0, top(0, 0)] == 1, "F.2, F.5: sheet empty, the four sides of a cube alive: its top is born")
    cnt = [0, 0]
    for bits in itertools.product((0, 1), repeat=3):
        st = np.zeros((1, n), np.uint8); st[0, S] = 1
        st[0, [bot(0, 0), bot(1, 0), rh(0, 0)]] = bits
        born = int(step1(st, nbr)[0, h(0, 0)])
        cnt[born] += 1
        if born != (sum(bits) >= 2): cnt = None; break
    check(cnt == [4, 4], "F.2 as corrected in entry 17: under a full sheet a dead cell of the layer with k = 0 is born iff at least two of its three cells beneath are alive")
    # F.3: the sheet's next state is a function of the band
    st = (rng.random((2048, n)) < 0.5).astype(np.uint8)
    st2 = st.copy(); rest = np.flatnonzero(xs >= 3); st2[:, rest] = (rng.random((2048, len(rest))) < 0.5)
    check((step1(st, nbr)[:, S] == step1(st2, nbr)[:, S]).all(), "F.3: the sheet's next state does not change when everything below the band is redrawn (2,048 states)")
    # F.5: S = 0: sigma born iff four sides alive; p follows gump's rule on k_p + beta + beta' + r_p
    st = (rng.random((8192, n)) < 0.45).astype(np.uint8); st[:, S] = 0
    nx = step1(st, nbr); good = True
    for i in range(N):
        for j in range(M):
            four = st[:, [h(i, j), h(i - 1, j), v(i, j), v(i, j - 1)]].sum(1) == 4
            good &= (nx[:, top(i, j)] == four).all()
            for p, lay, ben in ((h(i, j), [h(i, j + 1), h(i, j - 1), v(i, j), v(i, j - 1), v(i + 1, j), v(i + 1, j - 1)], [bot(i, j), bot(i + 1, j), rh(i, j)]),
                                (v(i, j), [v(i + 1, j), v(i - 1, j), h(i, j), h(i - 1, j), h(i, j + 1), h(i - 1, j + 1)], [bot(i, j), bot(i, j + 1), rv(i, j)])):
                cntp = st[:, lay].sum(1) + st[:, ben].sum(1)
                good &= (nx[:, p] == ((cntp + st[:, p] >= 4) & (cntp < 6))).all()
    check(good, "F.5: over an empty sheet a top is born iff its cube's four sides are alive, and each cell of the layer follows gump's rule on (6 in the layer) + (2 bottoms) + (1 private) (8,192 states)")
    # lone closed cube in an otherwise empty slab, two cubes below the wall and right under it
    for x0, label in ((4, 'in the interior'), (2, 'under the wall (its top in the sheet)')):
        cube = [(x0 - 1, 0, 0), (x0 + 1, 0, 0), (x0, 1, 0), (x0, 2 * N - 1, 0), (x0, 0, 1), (x0, 0, 2 * M - 1)]
        st = np.zeros((1, n), np.uint8); st[0, [idx[c] for c in cube]] = 1
        check((step1(st, nbr) == st).all(), f"a lone closed cube {label} is a still life of face12e (each face sees the 4 others it shares an edge with; no outside cell sees more than 2)")
    print("   [not checked by enumeration: 'whatever is outside a dead box of half-width 2k + 2' for the guard of claim 6; that is the light-cone argument of entry 4]")


def lone():
    print("lab request 1: face12e, wall 3 x 3, slab four cubes deep, sheet empty, one live cell h(0,1) in the layer beneath;")
    print("   6 bottoms (cubes (0,0),(1,0),(0,1),(1,1),(0,2),(1,2)) and 7 private cells (below the cell and its 6 in-layer neighbours)")
    N = M = 3
    cells, nbr, idx = slab(N, M); n = len(cells); xs = cells[:, 0]
    top, h, v, bot, rh, rv = names(N, M, idx)
    band = np.flatnonzero(xs <= 2)
    p0 = h(0, 1)
    seven = [(h(0, 1), rh(0, 1)), (h(0, 0), rh(0, 0)), (h(0, 2), rh(0, 2)), (v(0, 0), rv(0, 0)), (v(0, 1), rv(0, 1)), (v(1, 0), rv(1, 0)), (v(1, 1), rv(1, 1))]
    check(sorted(t for t in nbr[p0] if t != n and xs[t] == 2) == sorted(c for c, _ in seven[1:]), "the six in-layer neighbours of h(0,1) are h(0,0), h(0,2), v(0,0), v(0,1), v(1,0), v(1,1)")
    bots = [bot(0, 0), bot(1, 0), bot(0, 1), bot(1, 1), bot(0, 2), bot(1, 2)]
    priv = [r for _, r in seven]
    free = bots + priv
    pat = ((np.arange(1 << 13)[:, None] >> np.arange(13)) & 1).astype(np.uint8)
    rng = np.random.default_rng(5)
    counts = []
    for bg in ('all dead', 'all alive', 'random', 'random'):
        st = np.zeros((1 << 13, n), np.uint8)
        others = np.array([i for i in range(n) if xs[i] >= 3 and i not in free])
        if bg == 'all alive': st[:, others] = 1
        if bg == 'random': st[:, others] = (rng.random((1 << 13, len(others))) < 0.5)
        st[:, p0] = 1
        st[:, free] = pat
        nx = step1(st, nbr)
        dead = ~nx[:, band].any(axis=1)
        counts.append(int(dead.sum()))
        if bg == 'all dead': dead0 = dead
    check(counts == [3793] * 4, f"patterns of the 13 cells that leave the band empty next: {counts[0]} of 8,192 (claimed 3,793 = 0.4630), whatever the other cells of the slab hold ({counts})")
    nb_ = pat[:, :6].sum(1); nr0 = 7 - pat[:, 6:].sum(1)
    # ladder polynomial: P = sum over bottom sets V of a^|V| (1-a)^(6-|V|) x^(e(V)), x = P(private cell dead)
    claimed = {0: {0: 1}, 1: {0: 6}, 2: {0: 8, 1: 7}, 3: {0: 2, 1: 8, 2: 10}, 4: {2: 5, 3: 8, 4: 2}, 5: {4: 2, 5: 4}, 6: {7: 1}}
    got = {}
    for V in range(64):
        sel = (pat[:, :6] @ (1 << np.arange(6))) == V
        c = int(dead0[sel].sum())               # = 2^(7 - e)
        e = 7 - int(round(math.log2(c)))
        check_pow = (1 << (7 - e)) == c
        if not check_pow: got = None; break
        s = bin(V).count('1')
        got.setdefault(s, {}); got[s][e] = got[s].get(e, 0) + 1
    check(got == claimed, f"by number of live bottoms and number of private cells that must be dead: {got} = the coefficients (1; 6; 8+7x; 2+8x+10x^2; 5x^2+8x^3+2x^4; 2x^4+4x^5; x^7)")
    def poly(a, x):
        return sum(c * a ** s * (1 - a) ** (6 - s) * x ** e for s, d in claimed.items() for e, c in d.items())
    def exact(a, r):
        w = a ** nb_ * (1 - a) ** (6 - nb_) * (1 - r) ** nr0 * r ** (7 - nr0)
        return float(w[dead0].sum())
    for rho, said in ((0.5, 0.4630), (0.52, 0.4214), (0.398, 0.672), (0.4155, 0.638)):
        e = exact(rho, rho)
        check(abs(e - poly(rho, 1 - rho)) < 1e-12 and abs(e - said) < 6e-4, f"rho_beta = rho_r = {rho}: enumeration {e:.4f} = polynomial; the journal says {said}")
    g = lambda r: (1 - 3 * r ** 3 + 3 * r ** 5 - r ** 6) * (1 - r ** 3) ** 4
    print(f"   gump's lone cell (board, lemma exchange): {g(0.5):.4f}, {g(0.52):.4f}, {g(0.4155):.4f} at 0.5, 0.52, 0.4155;  independent threats (7/8)^7 = {(7 / 8) ** 7:.4f}")


def classes():
    """the table of entry 14: with r_p free, which m = beta_q + beta_q' leave p dead next, by (state, a)."""
    names_ = {(0, 1, 2): 'free', (0, 1): 'not both', (0, 2): 'equal', (1, 2): 'at least one', (0,): 'both dead', (2,): 'both alive', (): 'impossible'}
    tab = {}
    for s in (0, 1):
        for a in range(9):
            ok = tuple(m for m in (0, 1, 2) if any(not (((a + m + r) + s >= 4) and (a + m + r) < 6) for r in (0, 1)))
            tab[(s, a)] = names_[ok]
    return tab


def pi1():
    print("lab request 2: the table of classes, then configuration Pi_1 (row 1 of top cubes with tops and sides alive) on walls n x 4")
    tab = classes()
    want = {}
    for a in range(9):
        want[(0, a)] = 'free' if a in (0, 1, 5) or a >= 6 else {2: 'not both', 3: 'equal', 4: 'at least one'}[a]
        want[(1, a)] = 'free' if a in (0, 5) or a >= 6 else {1: 'not both', 2: 'both dead', 3: 'both alive', 4: 'at least one'}[a]
    check(tab == want, "entry 14's table of classes (dead: a = 2 not both, 3 equal, 4 at least one; live: 1 not both, 2 both dead, 3 both alive, 4 at least one; otherwise free) follows from the rule")
    for N in (3, 4):
        M = 4
        cells, nbr, idx = slab(N, M); n = len(cells); xs = cells[:, 0]
        top, h, v, bot, rh, rv = names(N, M, idx)
        band = np.flatnonzero(xs <= 2)
        base = np.zeros(n, np.uint8)
        for i in range(N):
            base[[h(i, 1), v(i, 0), v(i, 1), top(i, 1)]] = 1
        bots = [bot(i, j) for j in range(M) for i in range(N)]          # index j * N + i
        P = [(h(i, j), rh(i, j)) for i in range(N) for j in range(M)] + [(v(i, j), rv(i, j)) for i in range(N) for j in range(M)]
        pcell = np.array([p for p, _ in P]); rcell = np.array([r for _, r in P])
        nb_ = len(bots)
        tot = 0; unequal = 0; sheet_ok = True
        chunk = 1 << 12
        for lo in range(0, 1 << nb_, chunk):
            pat = ((np.arange(lo, lo + chunk)[:, None] >> np.arange(nb_)) & 1).astype(np.uint8)
            c = np.zeros((chunk, len(P)), np.int64)
            for r in (0, 1):
                st = np.tile(base, (chunk, 1)); st[:, bots] = pat; st[:, rcell] = r
                nx = step1(st, nbr)
                sheet_ok &= not nx[:, xs == 1].any()
                c += (nx[:, pcell] == 0)
            ways = c.prod(axis=1)
            tot += int(ways.sum())
            row0 = pat[:, 0:N]
            unequal += int(ways[(row0.min(1) != row0.max(1))].sum())
        claim = 32 ** N * (8 ** N + 2 * 6 ** N + 5 ** N)
        check(sheet_ok and tot == claim, f"wall {N} x 4: {tot:,} of 2^{12 * N} patterns of the {4 * N} bottoms and {8 * N} private cells empty the band; claimed 32^n (8^n + 2*6^n + 5^n) = {claim:,}")
        check(unequal == 0, f"wall {N} x 4: none of them has two unequal bottoms in row 0 (so 'bottoms (0,0) and (1,0) differ' is unsatisfiable)")
        if N == 3:
            # the privacy of r_p used above: p's next state depends on the private cells through r_p alone
            rng = np.random.default_rng(11)
            st = np.tile(base, (4096, 1)); st[:, bots] = (rng.random((4096, nb_)) < 0.5); st[:, rcell] = (rng.random((4096, len(P))) < 0.5)
            nx = step1(st, nbr); good = True
            for t, (p, r) in enumerate(P):
                st2 = st.copy(); others = np.delete(rcell, t); st2[:, others] = (rng.random((4096, len(others))) < 0.5)
                good &= (step1(st2, nbr)[:, p] == nx[:, p]).all()
            check(good, "   (the product over cells used for the count: redrawing every private cell but r_p never changes p's next state; 4,096 states)")
            # a direct count without the product, on a sub-cube that is small enough to step state by state:
            # bottoms of rows 1..3 alive (so every 'at least one' holds), the 8 patterns of row 0, all 2^12 patterns of the
            # private cells below the h-cells, the private cells below the v-cells dead
            rpat = ((np.arange(1 << 12)[:, None] >> np.arange(12)) & 1).astype(np.uint8)
            hs = [rh(i, j) for i in range(N) for j in range(M)]; vs = [rv(i, j) for i in range(N) for j in range(M)]
            direct = 0; prod_ = 0
            for b0 in range(8):
                pat0 = np.ones(nb_, np.uint8); pat0[:3] = [(b0 >> t) & 1 for t in range(3)]
                st = np.tile(base, (4096, 1)); st[:, bots] = pat0; st[:, hs] = rpat; st[:, vs] = 0
                direct += int((~step1(st, nbr)[:, band].any(axis=1)).sum())
                c = np.zeros(len(P), np.int64)
                for r in (0, 1):
                    st1 = base.copy()[None, :].copy(); st1[0, bots] = pat0; st1[0, rcell] = r
                    dead_r = (step1(st1, nbr)[0, pcell] == 0)
                    for t, (p, rr) in enumerate(P):
                        if rr in hs or r == 0: c[t] += dead_r[t]
                prod_ += int(c.prod())
            check(direct == prod_ and direct > 0, f"   direct stepping, state by state, of 8 x 2^12 states (row-0 bottoms free, other bottoms alive, private cells below the h-cells free): {direct:,} empty the band = the product formula on the same sub-cube")


def theta():
    print("lab request 2 (second part), Proposition F.4: the sheet over an empty layer follows Theta (alive next iff live sheet neighbours + own state >= 4)")
    # (a) Theta is what the true rule does to the sheet when the layer beneath is empty: slab check
    N = M = 4
    cells, nbr, idx = slab(N, M); n = len(cells); xs = cells[:, 0]
    S = np.flatnonzero(xs == 1)
    rng = np.random.default_rng(2)
    st = (rng.random((4096, n)) < 0.5).astype(np.uint8); st[:, xs == 2] = 0
    nx = step1(st, nbr)
    sheetn = np.array([[j for j in nbr[i] if j != n and xs[j] == 1] for i in S])
    good = (nx[:, S] == ((st[:, sheetn].sum(2) + st[:, S]) >= 4)).all()
    check(good, "with the layer beneath empty the true rule gives the sheet Theta(S), whatever lies deeper (periodic wall 4 x 4, 4,096 states)")
    # (b) box walls n x n: sheet cells (i, j), neighbours (i +- 1, j), (i, j +- 1) inside the box
    for nn in (3, 4, 5, 6, 7):
        s = np.ones((nn, nn), np.int64); t = 0; hist = []
        d = np.array([[min(i + j, i + nn - 1 - j, nn - 1 - i + j, 2 * nn - 2 - i - j) for j in range(nn)] for i in range(nn)])
        good = True
        while s.any():
            p = np.pad(s, 1)
            cnt = p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]
            s = ((cnt + s) >= 4).astype(np.int64); t += 1
            good &= (s == (d >= t)).all()
            hist.append(int(s.sum()))
        check(good and t <= nn, f"box wall {nn} x {nn}: Theta^j(full) = {{d >= j}} (d = l1 distance to the nearest corner) for every j; empty after {t} steps and not after {t - 1} (populations {hist}); bound n = {nn}")
    # (b') periodic walls n x n (the vessel of the measured wall law): every sheet, Theta iterated
    for nn in (3, 4, 5):
        nbits = nn * nn
        S = np.arange(1 << nbits, dtype=np.uint32)
        full = np.uint32((1 << nbits) - 1)
        col0 = np.uint32(sum(1 << (nn * i) for i in range(nn))); colL = np.uint32(sum(1 << (nn * i + nn - 1) for i in range(nn)))
        def th(s):
            up = ((s << np.uint32(nn)) | (s >> np.uint32(nbits - nn))) & full
            dn = ((s >> np.uint32(nn)) | (s << np.uint32(nbits - nn))) & full
            lf = ((s << np.uint32(1)) & ~col0 & full) | ((s >> np.uint32(nn - 1)) & col0)
            rt = ((s >> np.uint32(1)) & ~colL) | ((s << np.uint32(nn - 1)) & colL & full)
            all4 = up & dn & lf & rt
            three = (up & dn & lf) | (up & dn & rt) | (up & lf & rt) | (dn & lf & rt)
            return all4 | (s & three)
        cur = S.copy(); alive = np.ones(len(S), bool); steps_to_die = np.zeros(len(S), np.int16)
        t = 0
        while t < 4 * nn:
            cur = th(cur); t += 1
            newly = alive & (cur == 0); steps_to_die[newly] = t; alive &= ~newly
        lim = cur[alive]
        per2 = bool((th(th(lim)) == lim).all()); nfix = int((th(lim) == lim).sum())
        rows = [np.uint32(sum(1 << (nn * i + j) for j in range(nn))) for i in range(nn)]
        cols = [np.uint32(sum(1 << (nn * i + j) for i in range(nn))) for j in range(nn)]
        pairs = [rows[i] | rows[(i + 1) % nn] for i in range(nn)] + [cols[j] | cols[(j + 1) % nn] for j in range(nn)]
        contains = np.zeros(len(S), bool)
        for pm in pairs: contains |= (S & pm) == pm
        check(per2 and bool(alive[contains].all()) and int((~alive).sum()) > 0,
              f"periodic wall {nn} x {nn}: of the {len(S):,} sheets {int(alive.sum()):,} ({alive.mean():.3%}) are never emptied by Theta: all {int(contains.sum()):,} that contain two adjacent full rows or columns, and "
              f"{int((alive & ~contains).sum()):,} others; they end in {len(np.unique(lim)):,} distinct sets, fixed or of period 2 ({nfix:,} of the sheets end fixed); every other sheet is empty within {int(steps_to_die.max())} steps")
    # (c) a box of face12e itself: the sheet of a wall of a 5^3 box with the layer beneath held empty
    nn = 5
    cells, nbr = lc.graph((2 * nn + 3, 2 * nn + 3, 2 * nn + 3), (False, False, False), "edge")
    keep = np.array([all(1 <= c <= 2 * nn + 1 for c in p) for p in cells])
    cells2 = cells[keep]; idx2 = {tuple(int(v) for v in p): i for i, p in enumerate(cells2)}
    n2 = len(cells2); nbr2 = np.full((n2, 12), n2, np.int64)
    for i, p in enumerate(cells2):
        a = [k for k in range(3) if p[k] % 2 == 1][0]
        for j, o in enumerate(lc.offsets(a, "edge")):
            nbr2[i, j] = idx2.get((int(p[0] + o[0]), int(p[1] + o[1]), int(p[2] + o[2])), n2)
    check(n2 == 3 * nn * nn * (nn + 1), f"box of {nn}^3 cubes: {n2} cells = 3 n^2 (n + 1)")
    xs2 = cells2[:, 0]; Sb = np.flatnonzero(xs2 == 1); Bb = np.flatnonzero(xs2 == 2)
    st = np.zeros((1, n2), np.uint8); st[0, Sb] = 1; t = 0; pops = []
    while st[0, Sb].any() and t < 20:
        st[0, Bb] = 0
        st = step1(st, nbr2); st[0, xs2 >= 2] = 0; t += 1; pops.append(int(st[0, Sb].sum()))
    check(t == 5 and pops[3] > 0, f"box of 5^3 cubes, true rule, wall sheet x = 1 full, everything else held empty: sheet populations {pops}; empty after 5 generations and not after 4")


# --------------------------------------------------------------------------------------------- O_h faces
def oh():
    print("lab request 3: the face d = (1,1,1) of cube-centred (R = 2N+1) and vertex-centred (R = 2N+2) hulls, by listing")
    T = lambda j: j * (j + 1) // 2
    for N in (1, 2, 3, 4):
        row = {}
        for centre, R in (('c', 2 * N + 1), ('v', 2 * N + 2)):
            cells, c = g3.hull(R, centre)
            rel = [tuple(p[k] - c[k] for k in range(3)) for p in cells]
            cs = set(rel)
            face = [p for p in rel if sum(p) == R]
            fs = set(face)
            par = 1 if centre == 'c' else 0                       # parity of the normal coordinate in relative coordinates
            ax = lambda p: [k for k in range(3) if (p[k] & 1) == par][0]
            def inface(p):
                a = ax(p); b, cc = [k for k in range(3) if k != a]
                out = []
                for t in (b, cc):
                    for s in (1, -1):
                        o = [0, 0, 0]; o[a] = s; o[t] = -s; out.append((tuple(p[k] + o[k] for k in range(3)), 'kagome'))
                for s in (2, -2):
                    o = [0, 0, 0]; o[b] = s; o[cc] = -s; out.append((tuple(p[k] + o[k] for k in range(3)), 'hex'))
                return out
            # consistency with gump_lab's neighbour lists
            nb = g3.nbrs(cells); idx = {p: i for i, p in enumerate(rel)}
            good = all(sorted(idx[q] for q, _ in inface(p) if q in fs) == sorted(j for j in nb[idx[p]] if rel[j] in fs) for p in face)
            kag = sum(1 for p in face for q, kind in inface(p) if kind == 'kagome' and q in fs) // 2
            hexp = sum(1 for p in face for q, kind in inface(p) if kind == 'hex' and q in fs) // 2
            # orbits under the permutations of the coordinates
            seen = set(); orbits = 0; fixed_by_mirror = 0; fixed_by_rot = 0
            for p in face:
                if p in seen: continue
                orb = {tuple(p[i] for i in perm) for perm in itertools.permutations(range(3))}
                seen |= orb; orbits += 1
            fixed_by_mirror = sum(1 for p in face if p[0] == p[1])
            fixed_by_rot = sum(1 for p in face if p[0] == p[1] == p[2])
            # triangles: top cube q = p - e_a (sum R - 1) with its three top faces q + e_k; cube above u = p + e_a with its three bottom faces u - e_k
            unit = lambda k: tuple(1 if i == k else 0 for i in range(3))
            topc = {}; upc = {}
            for p in face:
                a = ax(p)
                q = tuple(p[k] - unit(a)[k] for k in range(3)); u = tuple(p[k] + unit(a)[k] for k in range(3))
                topc.setdefault(q, []).append(p); upc.setdefault(u, []).append(p)
            tri_top = sum(1 for q, v in topc.items() if len(v) == 3)
            tri_up = sum(1 for u, v in upc.items() if len(v) == 3)
            alone = sum(1 for q, v in topc.items() if len(v) == 1)
            two = sum(1 for q, v in topc.items() if len(v) == 2)
            # hexagons: the six cells w +- (e_a - e_b) round a lattice vertex w of the layer
            hexes = 0; cand = set()
            for p in face:
                a = ax(p); b, cc = [k for k in range(3) if k != a]
                for s in (1, -1):
                    o = [0, 0, 0]; o[b] = s; o[cc] = -s; cand.add(tuple(p[k] + o[k] for k in range(3)))
            for w in cand:
                six = [tuple(w[k] + s * (unit(i)[k] - unit(j)[k]) for k in range(3)) for i, j in ((0, 1), (0, 2), (1, 2)) for s in (1, -1)]
                if all(q in fs for q in six): hexes += 1
            shared = sum(1 for p in face if p[2] == 0)
            # cells beneath (neighbours in the two layers inward) of the cells that are alone in their top cube: shared with another face cell?
            ben = {p: {rel[j] for j in nb[idx[p]] if sum(rel[j]) < R} for p in face}
            lonely = [v[0] for q, v in topc.items() if len(v) == 1]
            sharing = sum(1 for p in lonely if any(ben[p] & ben[p2] for p2 in face if p2 != p))
            nben = sorted({len(ben[p]) for p in lonely})
            deg = {}
            for p in face:
                dgr = sum(1 for q, _ in inface(p) if q in fs); deg[dgr] = deg.get(dgr, 0) + 1
            row[centre] = dict(R=R, A=len(face), orbits=orbits, mirror_fixed=fixed_by_mirror, rot_fixed=fixed_by_rot, kagome=kag, hexpairs=hexp, tri_top=tri_top, tri_other=tri_up,
                               hexagons=hexes, alone=alone, two=two, shared=shared, deg=dict(sorted(deg.items())), ok=good, alone_sharing=sharing, alone_beneath=nben)
        c_, v_ = row['c'], row['v']
        m = N // 2 + 1
        print(f"   N = {N}:  cube-centred R = {c_['R']}: {c_}")
        print(f"           vertex-centred R = {v_['R']}: {v_}")
        check(c_['ok'] and v_['ok'], "      in-face neighbours as used here = gump_lab's neighbour lists restricted to the face")
        check(c_['A'] == v_['A'] == 3 * T(N + 1), f"      both have A = 3 T_(N+1) = {3 * T(N + 1)} cells")
        check(c_['rot_fixed'] == v_['rot_fixed'] == 0 and c_['mirror_fixed'] == v_['mirror_fixed'] == m and c_['orbits'] == v_['orbits'] == (3 * T(N + 1) + 3 * m) // 6,
              f"      no cell fixed by the rotation, {m} = floor(N/2) + 1 fixed by each mirror, (A + 3m)/6 = {(3 * T(N + 1) + 3 * m) // 6} orbits, in both")
        check(c_['kagome'] == v_['kagome'] == 3 * (N + 1) ** 2 and c_['hexpairs'] == v_['hexpairs'] == 3 * T(N), f"      {3 * (N + 1) ** 2} kagome bonds and {3 * T(N)} pairs across hexagons in both")
        check(c_['tri_top'] == T(N + 1) and c_['tri_other'] == T(N - 1) and c_['hexagons'] == T(N) and c_['alone'] == 0 and c_['two'] == 0,
              f"      cube-centred: T_(N+1) = {T(N + 1)} complete top-cube triangles (every cell in one), T_(N-1) = {T(N - 1)} of the other orientation, T_N = {T(N)} complete hexagons")
        check(v_['tri_other'] == T(N + 1) and v_['tri_top'] == T(N) and v_['hexagons'] == T(N - 1) and v_['alone'] == 3 * (N + 1) and v_['two'] == 0,
              f"      vertex-centred: T_(N+1) = {T(N + 1)} complete triangles of the other orientation, T_N = {T(N)} top-cube triangles, T_(N-1) = {T(N - 1)} hexagons, 3(N+1) = {3 * (N + 1)} cells alone in their top cube")
        check(v_['alone_sharing'] == 0, f"      vertex-centred: none of the {v_['alone']} lone rim cells shares a cell beneath with another face cell; cells beneath each: {v_['alone_beneath']}")
        check(c_['shared'] == 2 * (N + 1) and v_['shared'] == N + 1, f"      cells with third coordinate 0 (shared with the face (1,1,-1)): {c_['shared']} cube-centred, {v_['shared']} vertex-centred (claimed 2(N+1) against N+1)")
    print("   [the three 'tip cells' of the cube-centred face: the cells of in-face degree 2 in the lists above]")


# --------------------------------------------------------------------------------------------- Lemma 8
def lemma8(Ls=(10, 12, 14, 16, 18)):
    import prob_r1 as pr
    import prob_r2 as p2
    import counting_r2 as c2
    print("Lemma 8 on D2 rings: Q phi = lambda phi, max phi = 1; P_pi(T <= k) <= (1 - lambda^k) pi(phi) + pi(1 - phi) <= k h + pi(1 - phi)")
    # smallest case and a random check of the inequality
    rng = np.random.default_rng(1); worst = 0.0
    for trial in range(2000):
        m = int(rng.integers(2, 7))
        Q = rng.random((m, m)) * (rng.random((m, m)) < 0.6); Q /= np.maximum(Q.sum(1, keepdims=True), 1e-12) / rng.random((m, 1))
        w, V = np.linalg.eig(Q); i = int(np.argmax(w.real)); lam = float(w[i].real); phi = np.abs(V[:, i].real)
        if lam <= 1e-9 or np.abs(Q @ phi - lam * phi).max() > 1e-9: continue
        phi /= phi.max(); pi = rng.random(m); pi /= pi.sum()
        for k in (1, 2, 5, 20):
            lhs = 1 - pi @ np.linalg.matrix_power(Q, k) @ np.ones(m)
            worst = max(worst, lhs - ((1 - lam ** k) * (pi @ phi) + pi @ (1 - phi)))
    check(worst < 1e-9, f"the inequality on 2,000 random substochastic matrices (reducible ones included), k = 1, 2, 5, 20: largest violation {worst:.1e}")
    res = {}
    for (p, rho) in c2.PAIRS:
        pi_law = c2.binl(rho); a = pr.a_table(pi_law)
        for L in Ls:
            lam, phi = p2.perron_right(L, 'ring', a)
            h = 1 - lam
            pop = p2.popcount(L)
            nu = p ** pop * (1 - p) ** (L - pop)
            nu0 = float(nu[0]); nul = nu.copy(); nul[0] = 0.0
            doom = float(nul @ (1 - phi))                  # living starts only; the empty row has mass (1-p)^L and is T = 0
            D = c2.dk_kernel(L, p, pi_law, 8)              # P(row empty at generation k), the empty start included
            _, mu = p2.perron_left(L, 'ring', a)
            row = dict(h=h, doom=doom, piphi=float(nul @ phi), D=D, nu0=nu0, muphi=float(mu @ phi), phimin=float(phi[1:].min()),
                       phi_full=float(phi[-1]), q10=float(np.sort(phi[1:])[len(phi) // 10]))
            res[(p, rho, L)] = row
            viol = max((D[k] - nu0) - ((1 - lam ** k) * row['piphi'] + doom) for k in range(1, 9))
            print(f"   p = {p}, rho = {rho}, L = {L}: h = {h:.3e}; mu(phi) = {row['muphi']:.4f}; phi(full row) = {row['phi_full']:.4f}; min phi = {row['phimin']:.2e}; "
                  f"pi(1 - phi) = {doom:.3e} (-ln: {-np.log(doom):.3f}); P(0 < T <= k), k = 1..6: " + ' '.join(f"{D[k] - nu0:.2e}" for k in range(1, 7)) +
                  f"; bound at k = 6: {(1 - lam ** 6) * row['piphi'] + doom:.2e}", flush=True)
            if viol > 1e-12: check(False, f"      Lemma 8 violated by {viol:.2e}")
    check(True, "Lemma 8 holds at every (soup, L, k <= 8) above")
    print("   local slopes per cell between successive L of: -ln h | -ln pi(1 - phi) | -ln P(0 < T <= 4) | -ln P(0 < T <= 6)")
    for (p, rho) in c2.PAIRS:
        out = []
        for La, Lb in zip(Ls, Ls[1:]):
            A, Bq = res[(p, rho, La)], res[(p, rho, Lb)]
            f = lambda x, y: (np.log(x) - np.log(y)) / (Lb - La)
            out.append(f"L {La}-{Lb}: {f(A['h'], Bq['h']):.3f} | {f(A['doom'], Bq['doom']):.3f} | {f(A['D'][4] - A['nu0'], Bq['D'][4] - Bq['nu0']):.3f} | {f(A['D'][6] - A['nu0'], Bq['D'][6] - Bq['nu0']):.3f}")
        print(f"   p = {p}, rho = {rho}:  " + ';  '.join(out))
    print("   ratio pi(1 - phi) / h (how many generations of steady hazard the doomed starts of the soup are worth):")
    for (p, rho) in c2.PAIRS:
        print(f"   p = {p}, rho = {rho}:  " + ', '.join(f"L = {L}: {res[(p, rho, L)]['doom'] / res[(p, rho, L)]['h']:.2f}" for L in Ls))
    print("   the same ratio for the steady state itself, mu(1 - phi) / h (mu the quasi-stationary law; P_mu(T <= k) = 1 - lambda^k exactly):")
    for rho in sorted({r for (_, r) in c2.PAIRS}):
        p = [q for (q, r) in c2.PAIRS if r == rho][0]
        print(f"   rho = {rho}:  " + ', '.join(f"L = {L}: {(1 - res[(p, rho, L)]['muphi']) / res[(p, rho, L)]['h']:.2f}" for L in Ls))
    print("   excess of the soup over the steady state, e(pi) = 1 - pi(phi) / mu(phi) over living starts (= lim_k [P_pi(T <= k) - (1 - lambda^k)] / lambda^k), in units of h:")
    sign = {}
    for (p, rho) in c2.PAIRS:
        ex = [(1 - res[(p, rho, L)]['piphi'] / (1 - res[(p, rho, L)]['nu0']) / res[(p, rho, L)]['muphi']) / res[(p, rho, L)]['h'] for L in Ls]
        sign[(p, rho)] = ex
        print(f"   p = {p}, rho = {rho}:  " + ', '.join(f"L = {L}: {e:+.2f}" for L, e in zip(Ls, ex)))
    check(all(1 - res[key]['muphi'] > 2 * res[key]['h'] for key in res),
          "with max phi = 1 the steady state's own doom mass mu(1 - phi) exceeds 2 h at every size: the term pi(1 - phi) of Lemma 8 is not small against h even for pi = mu")
    return res, sign


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('structure', 'all'): structure()
    if cmd in ('lone', 'all'): lone()
    if cmd in ('pi1', 'all'): pi1()
    if cmd in ('theta', 'all'): theta()
    if cmd in ('oh', 'all'): oh()
    if cmd in ('lemma8', 'all'): lemma8()
    print('ALL OK' if OK else 'SOMETHING FAILED')
