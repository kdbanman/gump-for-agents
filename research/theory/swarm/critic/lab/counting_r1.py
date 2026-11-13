"""Critic's lab: checks and lab requests for counting, round 1 (exact; no sampling).

  python3 counting_r1.py c1      requests 1, 2: c_1, the 2507 states of the strip 3 x 5, classes of the 16-state graph
  python3 counting_r1.py c2      request 3: c_2 by a transfer matrix on 2^16 window states, rho^0_2, density 0.472,
                                 checked against every state of the strips 5 x 4 and 5 x 5
  python3 counting_r1.py lemma5  request 4: one-generation emptiability of a periodic gump face, SAT against the
                                 cube-by-cube criterion
  python3 counting_r1.py coll    request 6: collision probability of the top three rows at generations 1..8
  python3 counting_r1.py c4      claim 10 at k = 1: the C4 box 7 x 7, every symmetric state, against the band argument
  python3 counting_r1.py lift    claim 2: the second-order lift on a small vessel, every pair-state
  python3 counting_r1.py data    the data readings of entry 5 (committed toy2d files)
"""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
import toy2d_lab as t2
import gump_lab as g3
import startpoints as sp
import iid_flash

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def rule(s, n):
    """2D rule B34/S234, vectorised: alive next iff n + s >= 3 and n <= 4."""
    return ((n + s >= 3) & (n <= 4)).astype(np.int64)


# -------------------------------------------------------------------------------------------------- c1
def k1_matrix(p=0.5, pe=None):
    """16 x 16 matrix on windows (x-2, x-1, x, x+1) of the edge row: weight of cell x being dead next, the two cells
    beneath summed out (density p), times the weight of the edge bit (density pe, default p)."""
    pe = p if pe is None else pe
    pb = [(1 - p) ** 2, 2 * p * (1 - p), p ** 2]
    T = np.zeros((16, 16))
    for a, b, c, d in itertools.product((0, 1), repeat=4):
        for e in (0, 1):
            k = a + b + d + e
            dead = sum(pb[bb] for bb in range(3) if not (k + bb <= 4 and k + bb + c >= 3))
            T[a * 8 + b * 4 + c * 2 + d, b * 8 + c * 4 + d * 2 + e] = (pe if c else 1 - pe) * dead
    return T


def sccs(adj):
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    n, lab = connected_components(csr_matrix(adj), directed=True, connection='strong')
    return n, lab


def c1():
    c = iid_flash.cost(0.5, 0.5)
    T = k1_matrix(0.5)
    lam = max(np.linalg.eigvals(T).real)
    check(abs(c + np.log(lam)) < 1e-12 and 0.273 <= c <= 0.562,
          f"c_1 = -ln(largest eigenvalue of the 16 x 16 matrix) = {c:.6f} (rho_1 = 8 e^(-c_1) = {8 * np.exp(-c):.6f}); "
          f"inside the hand bounds [0.273, 0.562]")
    # strip 3 x 5, every state
    H, L = 3, 5
    F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
    cnt = int(((F & np.uint32((1 << L) - 1)) == 0).sum())
    tr = np.trace(np.linalg.matrix_power(T, 5)) * 2 ** 15
    check(cnt == 2507 and abs(tr - 2507) < 1e-6, f"strip 3 x 5: states with row 0 empty one generation later: {cnt} (claimed 2507; "
                                                   f"8^5 tr(T^5) = {tr:.6f})")
    for LL in (6, 7, 8):
        F = exact.full_map(t2.nbrs(3, LL, True), t2.B, t2.S)
        cnt = int(((F & np.uint32((1 << LL) - 1)) == 0).sum())
        tr = np.trace(np.linalg.matrix_power(T, LL)) * 8 ** LL
        check(abs(tr - cnt) < 1e-4, f"strip 3 x {LL}: {cnt} states; 8^L tr(T^L) = {tr:.4f}; D_1 = {cnt / 8 ** LL:.6f}")
    # request 2: the graph of positive weights
    adj = (T > 0).astype(int)
    n, lab = sccs(adj)
    names = lambda idx: [format(i, '04b') for i in idx]
    print(f"       k = 1 graph: 16 window states, {int(adj.sum())} edges of positive weight (the 6 missing ones are the windows "
          f"'live cell with exactly two live in-row neighbours'); strongly connected components: {n}")
    for comp in range(n):
        idx = np.flatnonzero(lab == comp)
        sub = T[np.ix_(idx, idx)]
        r = max(abs(np.linalg.eigvals(sub))) if len(idx) > 1 or sub[0, 0] > 0 else 0.0
        print(f"         component {names(idx)}: spectral radius {r:.6f}" + ("  <- contains 0000" if 0 in idx else ""))
    idx0 = np.flatnonzero(lab == lab[0])
    r0 = max(abs(np.linalg.eigvals(T[np.ix_(idx0, idx0)])))
    check(True, f"rho^0_1 / rho_1 = {r0 / lam:.6f}: " + ("the class of the all-dead window is dominant, c^0_1 = c_1" if abs(r0 - lam) < 1e-12
                                                         else f"c^0_1 = {-np.log(r0):.6f} > c_1"))
    # box edge, exact: [T^(L+4)]_00 against every state of the box 3 x L
    for LL in (5, 6, 7):
        nb = t2.nbrs(3, LL, False)
        F = exact.full_map(nb, t2.B, t2.S)
        cnt = int(((F & np.uint32((1 << LL) - 1)) == 0).sum())
        # walks of L steps (one per box cell) from a window 00** to a window **00: the dead cells outside the box
        # carry no weight (they have nothing beneath them and are never born); this is [M_1^(L+4)]_00 of the claim
        # written for the reduced matrix
        val = np.linalg.matrix_power(T, LL)[np.ix_([0, 1, 2, 3], [0, 4, 8, 12])].sum() * 8 ** LL
        check(abs(val - cnt) < 1e-4, f"box 3 x {LL} (free ends): {cnt} states with row 0 empty next; closed-walk formula {val:.4f}; "
                                     f"ring of the same length: {np.trace(np.linalg.matrix_power(T, LL)) * 8 ** LL:.0f}")
    for p in (0.472,):
        Tp = k1_matrix(p)
        print(f"       at soup density {p}: c_1 = {-np.log(max(np.linalg.eigvals(Tp).real)):.6f}")


# -------------------------------------------------------------------------------------------------- c2
def k2_weights(p=0.5):
    """W[state, new] for the horizon-2 window. state bits: row 0 at columns x-4..x+3 (bits 0..7), row 1 at x-2..x+1
    (bits 8..11), row 2 at x-2..x+1 (bits 12..15). new = (a0, a1, a2): row 0 at x+4, rows 1, 2 at x+2.
    Weight = sum over (r3, r4) at column x of the product of the weights of the five new bits, when the edge cell
    (x, 0) is dead at generation 2; with p = 1/2 everything is multiplied by 2^5 so that W counts configurations."""
    S = np.arange(1 << 16, dtype=np.int64)
    r0 = [(S >> i) & 1 for i in range(8)]             # r0[i] = column x-4+i
    r1 = [(S >> (8 + i)) & 1 for i in range(4)]       # r1[i] = column x-2+i
    r2 = [(S >> (12 + i)) & 1 for i in range(4)]
    W = np.zeros((1 << 16, 8))
    for new in range(8):
        a0, a1, a2 = new & 1, (new >> 1) & 1, (new >> 2) & 1
        R0 = r0 + [np.full_like(S, a0)]               # columns x-4..x+4 -> index c+4
        R1 = r1 + [np.full_like(S, a1)]               # columns x-2..x+2 -> index c+2
        R2 = r2 + [np.full_like(S, a2)]
        # row 0 at generation 1, columns x-2..x+2
        g0 = []
        for c in range(-2, 3):
            n = R0[c + 2] + R0[c + 3] + R0[c + 5] + R0[c + 6] + R1[c + 2] + R2[c + 2]
            g0.append(rule(R0[c + 4], n))
        w_new = (p if a0 else 1 - p) * (p if a1 else 1 - p) * (p if a2 else 1 - p)
        for r3 in (0, 1):
            for r4 in (0, 1):
                n1 = R1[0] + R1[1] + R1[3] + R1[4] + R0[4] + R2[2] + r3
                y1 = rule(R1[2], n1)
                n2 = R2[0] + R2[1] + R2[3] + R2[4] + R1[2] + R0[4] + r3 + r4
                y2 = rule(R2[2], n2)
                G = rule(g0[2], g0[0] + g0[1] + g0[3] + g0[4] + y1 + y2)
                W[:, new] += (G == 0) * w_new * (p if r3 else 1 - p) * (p if r4 else 1 - p)
    nxt = np.zeros((1 << 16, 8), np.int64)
    for new in range(8):
        a0, a1, a2 = new & 1, (new >> 1) & 1, (new >> 2) & 1
        s0 = ((S & 0xFF) >> 1) | (a0 << 7)
        s1 = (((S >> 8) & 0xF) >> 1) | (a1 << 3)
        s2 = (((S >> 12) & 0xF) >> 1) | (a2 << 3)
        nxt[:, new] = s0 | (s1 << 8) | (s2 << 12)
    return W, nxt


def ring_sum(W, nxt, L):
    """sum over L-periodic sequences of new-bit triples of the product of weights = tr(M^L)."""
    tot = 0.0
    for seq in itertools.product(range(8), repeat=L):
        # the window state before step x is fixed by the periodic sequence: row 0 bit i = column x-4+i was introduced at
        # step (x-4+i) - 4; rows 1, 2 bit i = column x-2+i introduced at step (x-2+i) - 2
        st = 0
        for i in range(8):
            st |= (seq[(-8 + i) % L] & 1) << i
        for i in range(4):
            st |= ((seq[(-4 + i) % L] >> 1) & 1) << (8 + i)
            st |= ((seq[(-4 + i) % L] >> 2) & 1) << (12 + i)
        w = 1.0
        for x in range(L):
            w *= W[st, seq[x]]
            if w == 0:
                break
            st = nxt[st, seq[x]]
        tot += w
    return tot


def spectral(W, nxt, idx=None, iters=400):
    """spectral radius of the sparse matrix (restricted to the states idx), by power iteration with a shift."""
    n = W.shape[0]
    mask = np.ones(n, bool) if idx is None else np.zeros(n, bool)
    if idx is not None:
        mask[idx] = True
    Wm = W * mask[:, None] * mask[nxt]
    v = mask.astype(float); v /= v.sum()
    shift = 0.5 * Wm.sum(1).max()
    lam = 0.0
    for it in range(iters):
        u = np.zeros(n)
        np.add.at(u, nxt.ravel(), (v[:, None] * Wm).ravel())          # left multiplication: u = v M
        u += shift * v
        l2 = u.sum(); u /= l2
        if abs(l2 - lam) < 1e-13 * l2 and it > 30:
            lam = l2; break
        v, lam = u, l2
    return lam - shift


def c2():
    print("request 3: horizon 2 (2D rule, half-plane, soup of density p)")
    for p in (0.5, 0.472):
        W, nxt = k2_weights(p)
        scale = 32.0 if p == 0.5 else 1.0
        Wc = W * scale
        if p == 0.5:
            for H, L in ((5, 4), (5, 5)):
                F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
                cnt = int(((F[F] & np.uint32((1 << L) - 1)) == 0).sum())
                val = ring_sum(Wc, nxt, L)
                check(abs(val - cnt) < 1e-6 * max(cnt, 1), f"strip {H} x {L}, every state: {cnt} have row 0 empty at generation 2 "
                                                             f"(D_2 = {cnt / 2 ** (H * L):.6f}); transfer weights give {val:.1f}")
        rho = spectral(Wc, nxt)
        # class of the all-dead window
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import connected_components
        rows = np.repeat(np.arange(1 << 16), 8); cols = nxt.ravel(); pos = Wc.ravel() > 0
        Gr = csr_matrix((np.ones(int(pos.sum())), (rows[pos], cols[pos])), shape=(1 << 16, 1 << 16))
        ncomp, lab = connected_components(Gr, directed=True, connection='strong')
        idx0 = np.flatnonzero(lab == lab[0])
        rho0 = spectral(Wc, nxt, idx0)
        sizes = np.bincount(lab)
        big = np.argsort(sizes)[::-1][:3]
        if p == 0.5:
            c = 5 * np.log(2) - np.log(rho); c0 = 5 * np.log(2) - np.log(rho0)
        else:
            c = -np.log(rho); c0 = -np.log(rho0)
        print(f"  p = {p}: rho_2 = {rho:.6f}" + (" (count per column, of 32)" if p == 0.5 else "") + f": c_2 = {c:.6f};  class of the all-dead "
              f"window: {len(idx0)} of 65536 states, c^0_2 = {c0:.6f};  {ncomp} strong components, largest {sizes[big].tolist()}")
        check(c > 0 and c <= iid_flash.cost(p, p) + 1e-9, f"0 < c_2 <= c_1 = {iid_flash.cost(p, p):.6f}")


# ----------------------------------------------------------------------------------------------- lemma5
def lemma5():
    from pysat.solvers import Cadical153
    print("request 4: periodic gump face, one-generation emptiability: SAT over all cells beneath against the criterion")
    for (a, b) in ((2, 2), (3, 2)):
        m = 4
        cells, nb = sp.make_slab(a, b, m)
        face = [i for i, cc in enumerate(cells) if cc[2] == -1]
        fs = set(face); A = len(face)
        inl = {i: [j for j in nb[i] if j in fs] for i in face}            # with multiplicity on small tori
        ben = {i: [j for j in nb[i] if j not in fs] for i in face}
        dup = any(len(set(nb[i])) < len(nb[i]) for i in face)
        under = sorted(set(j for i in face for j in ben[i]))
        var = {j: n + 1 for n, j in enumerate(under)}
        comps, _ = sp.components(face, ben)
        pos = {i: t for t, i in enumerate(face)}

        def crit(mask):
            for cp in comps:
                und = sorted(set(j for i in cp for j in ben[i]))
                good = False
                for bits in itertools.product((0, 1), repeat=len(und)):
                    val = dict(zip(und, bits))
                    ok = True
                    for i in cp:
                        k = sum((mask >> pos[j]) & 1 for j in inl[i])
                        bb = sum(val[j] for j in ben[i])
                        x = (mask >> pos[i]) & 1
                        if (3 if x else 4) <= k + bb <= 5:
                            ok = False; break
                    if ok:
                        good = True; break
                if not good:
                    return False
            return True

        def sat(mask):
            clauses = []
            for i in face:
                k = sum((mask >> pos[j]) & 1 for j in inl[i])
                x = (mask >> pos[i]) & 1
                und = sorted(set(ben[i])); mult = [ben[i].count(j) for j in und]
                for bits in itertools.product((0, 1), repeat=len(und)):
                    bb = sum(bt * mu for bt, mu in zip(bits, mult))
                    if (3 if x else 4) <= k + bb <= 5:
                        clauses.append([(-var[j] if bt else var[j]) for j, bt in zip(und, bits)])
            with Cadical153(bootstrap_with=clauses) as s:
                return s.solve()

        memo = {}
        nc = ns = dis = 0
        for mask in range(1 << A):
            c = crit(mask) if A <= 12 else None
            s_ = sat(mask)
            if c is None:
                c = crit(mask)
            nc += c; ns += s_; dis += (c != s_)
        check(dis == 0, f"slab face {a} x {b} ({A} cells, {len(comps)} cubes of sizes {sorted(set(len(c) for c in comps))}"
                        + (", doubled neighbours on this torus" if dup else "") +
                        f"): emptiable in one generation: {ns} of {1 << A} by SAT, {nc} by the cube criterion; disagreements {dis}")


# ------------------------------------------------------------------------------------------------- coll
def coll():
    c1v = iid_flash.cost(0.5, 0.5)
    print("request 6: collision probability of the top three rows at generation j from the uniform soup")
    print(f"   excess = (1/L) ln(2^(3L) * sum_u mu_j(u)^2), to compare with c_1 = {c1v:.4f}: the hypothesis of claim 15 needs excess < c_1")
    for H, L in ((4, 5), (4, 6), (5, 5)):
        N = H * L
        F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
        cur = np.arange(1 << N, dtype=np.uint32)
        top = np.uint32((1 << (3 * L)) - 1); row0 = np.uint32((1 << L) - 1)
        line_all = []; line_alive = []; frac = []; death = []
        for j in range(1, 9):
            cur = F[cur]
            u = (cur & top).astype(np.int64)
            cnt = np.bincount(u, minlength=1 << (3 * L)).astype(float)
            mu = cnt / cnt.sum()
            line_all.append(np.log(8.0 ** L * (mu ** 2).sum()) / L)
            alive = (cur & row0) != 0
            ca = np.bincount(u[alive], minlength=1 << (3 * L)).astype(float)
            ma = ca / ca.sum()
            line_alive.append(np.log(8.0 ** L * (ma ** 2).sum()) / L)
            frac.append(alive.mean())
            nxt = F[cur]
            death.append(float((((nxt & row0) == 0) & alive).sum()) / (1 << N))
        print(f"  strip {H} x {L}:  j =        " + ' '.join(f"{j:7d}" for j in range(1, 9)))
        print("     excess, all states:      " + ' '.join(f"{v:7.4f}" for v in line_all))
        print("     excess, row 0 alive:     " + ' '.join(f"{v:7.4f}" for v in line_alive))
        print("     fraction with row 0 alive:" + ' '.join(f"{v:7.4f}" for v in frac))
        print("     lambda(T = j+1):          " + ' '.join(f"{v:7.5f}" for v in death))


# ------------------------------------------------------------------------------------------------- lift
def lift():
    print("claim 2: second-order lift Phi(u, v) = (v, f(v) xor u), every pair-state")
    for name, nb, B, S, facebits in (('2D strip 2 x 5', t2.nbrs(2, 5, True), t2.B, t2.S, list(range(5))),
                                     ('gump hull R = 1c', g3.nbrs(g3.hull(1, 'c')[0]), g3.B, g3.S, None)):
        N = len(nb)
        if facebits is None:
            cells, c = g3.hull(1, 'c'); facebits = g3.faces(cells, c, 1)[(1, 1, 1)]
        F = exact.full_map(nb, B, S).astype(np.int64)
        u = np.repeat(np.arange(1 << N, dtype=np.int64), 1 << N); v = np.tile(np.arange(1 << N, dtype=np.int64), 1 << N)
        img = v * (1 << N) + (F[v] ^ u)
        bij = len(np.unique(img)) == 1 << (2 * N)
        fm = sum(1 << i for i in facebits)
        Hset = (v & fm) == 0
        H2 = Hset & ((u & fm) == 0)
        iu, iv = img // (1 << N), img % (1 << N)
        H2img = ((iv & fm) == 0) & ((iu & fm) == 0)
        enters = int((H2img & ~H2).sum())
        check(bij and enters == 0 and abs(Hset.mean() - 2.0 ** (-len(facebits))) < 1e-15,
              f"{name} ({N} cells, face of {len(facebits)}): Phi is a bijection of the {1 << (2 * N)} pair-states; 'face empty now' has "
              f"frequency {Hset.mean():.6f} = 2^-{len(facebits)}; states entering 'face empty twice running' from outside: {enters}")


# --------------------------------------------------------------------------------------------------- c4
def c4():
    """claim 10 at k = 1 on the smallest admissible box (L = 7 = 4k + 3): under the C4-symmetric soup the top band
    (rows 0..2) is uniform on the configurations whose right corner square is the rotated left one."""
    L = 7; N = L * L
    nb = t2.nbrs(L, L, False)
    rot = lambda x, y: (L - 1 - y, x)                       # (column, row) -> (column, row), a quarter turn
    orb = {}; reps = []
    for y in range(L):
        for x in range(L):
            if (x, y) in orb: continue
            o = [(x, y)]
            while True:
                nx = rot(*o[-1])
                if nx == o[0]: break
                o.append(nx)
            for c_ in o: orb[c_] = len(reps)
            reps.append(o)
    no = len(reps)
    S = np.arange(1 << no, dtype=np.int64)
    X = np.zeros((1 << no, N), np.int64)
    for (x, y), k in orb.items():
        X[:, y * L + x] = (S >> k) & 1
    top = np.zeros(1 << no, np.int64)
    for x in range(L):
        i = x
        n = X[:, nb[i]].sum(1)
        top += rule(X[:, i], n)
    full_cnt = int((top == 0).sum())
    # the band alone
    free = [(r, x) for r in range(3) for x in range(L) if not (r <= 2 and x >= L - 3)]      # everything but the right square
    cnt = 0
    for bits in itertools.product((0, 1), repeat=len(free)):
        band = {c_: b for c_, b in zip(free, bits)}
        for r in range(3):
            for x in range(3):
                band[(x, L - 1 - r)] = band[(r, x)]            # (row x, column L-1-r) := (row r, column x)
        dead = True
        for x in range(L):
            g = lambda rr, xx: band.get((rr, xx), 0) if 0 <= xx < L else 0
            n = g(0, x - 2) + g(0, x - 1) + g(0, x + 1) + g(0, x + 2) + g(1, x) + g(2, x)
            sx = g(0, x)
            if (n + sx >= 3) and (n <= 4):
                dead = False; break
        cnt += dead
    T = k1_matrix(0.5)
    free_box = np.linalg.matrix_power(T, L)[np.ix_([0, 1, 2, 3], [0, 4, 8, 12])].sum()      # probability, box without symmetry
    check(full_cnt * (1 << len(free)) == cnt * (1 << no),
          f"box 7 x 7, C4-symmetric soup ({no} orbits): top edge empty after one generation in {full_cnt} of {1 << no} states "
          f"= {full_cnt / (1 << no):.6f}; constrained band alone: {cnt} of {1 << len(free)} = {cnt / (1 << len(free)):.6f}; "
          f"box without symmetry: {free_box:.6f}")


# ------------------------------------------------------------------------------------------------- data
def data():
    d = os.path.join(RES, 'toy2d', 'data')
    ld = lambda n: {r['L']: r for r in json.load(open(os.path.join(d, 'law_cross2_B34S234' + n + '.json')))['rows']}
    mx, box, c4, ring = ld('_mx'), ld('_box_none'), ld('_box_c4'), ld('')
    print("entry 5: ln tau(mirror ring, 2m) - ln tau(box, m): " + ', '.join(f"m={m}: {mx[2 * m]['lntau'] - box[m]['lntau']:+.2f}"
                                                                         for m in sorted(box) if 2 * m in mx))
    for L in sorted(c4):
        r = c4[L]; b = box.get(L)
        print(f"  C4 box L={L}: deaths {r['deaths']:.0f}, settles {r['settles']:.0f} ({r['settles'] / (r['settles'] + r['deaths']):.2f} of exits), "
              f"h/p1 = {r['h_over_p1']:.3f}, bulk activity {r['act_bulk']:.3f}" +
              (f";  box without symmetry: h/p1 = {b['h_over_p1']:.3f}, settles {b['settles']:.0f} of {b['settles'] + b['deaths']:.0f}, bulk activity {b['act_bulk']:.3f}" if b else ''))


if __name__ == '__main__':
    dict(c1=c1, c2=c2, c4=c4, lemma5=lemma5, coll=coll, lift=lift, data=data)[sys.argv[1]]()
    print('ALL OK' if OK else 'SOMETHING FAILED')
