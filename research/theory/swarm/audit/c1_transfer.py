#!/usr/bin/env python3
"""Audit of the counting line, 2D rule at a fixed horizon: claims 4, 5, 7, 8, 12, 13, 14.

  python3 c1_transfer.py            (about 3 minutes, one core)

Every "brute" number below is a count over all states of a vessel with the stepper of c0_lib.py; every "matrix"
number comes from a transfer matrix built here. The explicit window matrix M_1 (2^12 states: 4 columns x 3 rows)
is built from the stepper itself, not from the table w(s, k).
"""
import itertools, math, sys, time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from c0_lib import step2d, states, count_edge_dead, T1, T2, w1, spectral_radius, rule

t00 = time.time()
LN2 = math.log(2)


def section(s):
    print(f"\n=== {s}  [{time.time() - t00:.0f} s]")


def build_M1():
    """M_1 on windows of 4 columns of rows 0..2 (column j of the window = bits 3j..3j+2: rows 0, 1, 2)."""
    X = np.zeros((1 << 15, 3, 5), np.int8)
    idx = np.arange(1 << 15, dtype=np.int64)
    for j in range(5):
        for r in range(3):
            X[:, r, j] = (idx >> (3 * j + r)) & 1
    g = step2d(X, periodic=False)[:, 0, 2]                 # cell (2, 0) of a 3 x 5 window at generation 1
    u = idx & 0xFFF
    v = idx >> 3
    M = np.zeros((4096, 4096))
    np.add.at(M, (u[g == 0], v[g == 0]), 1.0)
    return M


def main():
    section("claim 4, horizon 1: explicit M_1 (4096 states), rings, open words, the worked case")
    M1 = build_M1()
    rho1 = max(abs(np.linalg.eigvals(M1)))
    c1 = 3 * LN2 - math.log(rho1)
    print(f"rho(M_1) = {rho1:.6f} of 8   c_1 = 3 ln 2 - ln rho = {c1:.6f}   (journal: 4.608520, 0.551535)")
    P = np.eye(4096)
    pw = {}
    for n in range(1, 13):
        P = P @ M1
        pw[n] = (round(np.trace(P)), round(P[0, 0]), round(P.sum()))
    brute_ring = {}
    for L in range(1, 9):
        brute_ring[L] = count_edge_dead(3, L, 1, True)
        print(f"  ring 3 x {L}: brute {brute_ring[L]:>8d}   tr(M_1^{L}) {pw[L][0]:>8d}   "
              f"{'ok' if brute_ring[L] == pw[L][0] else 'DIFFERENT'}")
        assert brute_ring[L] == pw[L][0]
    print(f"  journal: 2507, 10846, 47383, 209825 at L = 5..8; ratios "
          + ", ".join(f"{brute_ring[L + 1] / brute_ring[L]:.3f}" for L in range(5, 8)))
    assert [brute_ring[L] for L in (5, 6, 7, 8)] == [2507, 10846, 47383, 209825]
    # deeper strip: rows below 2k are free
    b45 = count_edge_dead(4, 5, 1, True)
    print(f"  ring 4 x 5: brute {b45} = 2^5 * {b45 // 32} (rows below 2k cancel)")
    assert b45 == 32 * 2507
    # control: W = 2 < 2k + 1
    b25 = count_edge_dead(2, 5, 1, True)
    print(f"  control, strip 2 x 5 (W < 2k + 1): brute {b25} / 2^10 = {b25 / 1024:.5f} against tr/8^5 = {2507 / 32768:.5f}"
          f"  -> {'differs, as it should' if b25 * 32 != 2507 else 'EQUAL?'}")
    assert b25 * 32 != 2507
    # bound D <= m_k e^{-c L}
    for L in range(1, 9):
        assert brute_ring[L] <= 4096 * rho1 ** L * (1 + 1e-12)
    print("  D_1(L) <= m_1 e^{-c_1 L} holds at L = 1..8 (m_1 = 4096)")
    # open words: q_1(l)
    for l in (1, 2, 3):
        n = l + 4
        cnt = 0
        for X in states(3 * n):
            X = X.reshape(-1, 3, n)
            Y = step2d(X, periodic=False)                  # the middle cells never see the box's sides
            cnt += int((Y[:, 0, 2:n - 2].sum(axis=1) == 0).sum())
        print(f"  open word, l = {l}: brute {cnt}   1^T M_1^{l} 1 = {pw[l][2]}   {'ok' if cnt == pw[l][2] else 'DIFFERENT'}")
        assert cnt == pw[l][2]

    section("claim 4, the 16-state form, the hand bounds, the still triple")
    Tc = T1(0.5, count=True)
    r16 = max(abs(np.linalg.eigvals(Tc)))
    print(f"16-state matrix (weights 4w): rho = {r16:.6f}; c_1 = {3 * LN2 - math.log(r16):.6f}")
    assert abs(r16 - rho1) < 1e-9
    for L in range(1, 9):
        assert round(np.trace(np.linalg.matrix_power(Tc, L))) == brute_ring[L]
    print("  tr(T^L) = brute ring counts for L = 1..8")
    # closed form L = 5
    from fractions import Fraction as F
    wtab = {(s, k): F(w1(s, k)).limit_denominator(4) for s in (0, 1) for k in range(5)}
    tot = F(0)
    for S in itertools.product((0, 1), repeat=5):
        pr = F(1)
        for x in range(5):
            k = sum(S) - S[x]
            pr *= wtab[S[x], k]
        tot += pr
    print(f"  L = 5 by the table: sum = {tot} (journal 2507/1024)")
    assert tot == F(2507, 1024)
    # hand bound (i): lambda^5 = lambda^4 + (3/4)^5
    f = lambda x: x ** 5 - x ** 4 - 0.75 ** 5
    lo, hi = 1.0, 2.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    print(f"  bound (i): root {lo:.4f}, c_1 <= {LN2 - math.log(lo):.4f} (journal 1.1403, 0.562)")
    # verify (i) is a lower bound on the sum by brute force on a ring: isolated live cells, gaps >= 4
    # hand bound (ii)
    def g(x):
        y = 0.75 / x
        return 1 / x + 0.75 ** 5 * x ** -6 / (1 - y - y ** 2 - y ** 3 - y ** 4 - y ** 5) - 1
    lo, hi = 1.5, 2.0                                       # g decreasing here, pole below 1.5
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
    print(f"  bound (ii): root {lo:.4f}, c_1 >= {LN2 - math.log(lo):.4f} (journal 1.5213, 0.273)")
    assert LN2 - math.log(lo) <= c1 <= 0.5619
    # (ii) directly: growth of sum_S (3/4)^{|S u N(S)|} on rings
    prev = None
    for L in (10, 14, 18):
        tot = 0.0
        for X in states(L):
            S = X
            near = np.zeros_like(S)
            for d in (1, 2, -1, -2):
                near |= np.roll(S, d, axis=1)
            tot += float((0.75 ** (S | near).sum(axis=1)).sum())
        if prev:
            print(f"  sum_S (3/4)^|S u N(S)| on rings: growth per cell between L = {prev[0]} and {L}: "
                  f"{(tot / prev[1]) ** (1 / (L - prev[0])):.4f}")
        prev = (L, tot)
    # still triple
    x = np.zeros((1, 9, 15), np.int8)
    x[0, 0, 6:9] = 1
    y = x.copy()
    for _ in range(6):
        y = step2d(y, periodic=False)
    print(f"  lone triple 111 in row 0: unchanged after 6 generations: {bool((y == x).all())}")
    assert (y == x).all()

    section("claim 5: c_1(p), c_2(p)")
    for p in (0.5, 0.472):
        r = max(abs(np.linalg.eigvals(T1(p))))
        print(f"  p = {p}: c_1 = {-math.log(r):.6f}")
    T2c = T2(0.5, count=True)
    rho2, vec2 = spectral_radius(T2c)
    c2 = 5 * LN2 - math.log(rho2)
    print(f"  horizon 2, 2^16-state matrix: rho_2 = {rho2:.6f} of 32, c_2 = {c2:.6f}  (journal 20.046271, 0.467693)")
    r2p, _ = spectral_radius(T2(0.472))
    print(f"  p = 0.472: c_2 = {-math.log(r2p):.4f}  (journal 0.4671)")
    r2h, _ = spectral_radius(T2(0.5))
    assert abs(-math.log(r2h) - c2) < 1e-9
    # traces of T2^4, T2^5 against brute force on strips 5 x 4, 5 x 5
    A2 = (T2c @ T2c).tocsr()
    A3 = (A2 @ T2c).tocsr()
    tr4 = int(round(A2.multiply(A2.T).sum()))
    tr5 = int(round(A2.multiply(A3.T).sum()))
    tr3 = int(round(T2c.multiply(A2.T).sum()))
    b3 = count_edge_dead(5, 3, 2, True)
    b4 = count_edge_dead(5, 4, 2, True)
    print(f"  ring 5 x 3 at generation 2: brute {b3}, tr(T2^3) = {tr3}")
    print(f"  ring 5 x 4 at generation 2: brute {b4}, tr(T2^4) = {tr4}  (journal 224,471)")
    b5 = count_edge_dead(5, 5, 2, True, chunk=1 << 19)
    print(f"  ring 5 x 5 at generation 2: brute {b5}, tr(T2^5) = {tr5}  (journal 7,043,564)")
    assert (b3, b4, b5) == (tr3, tr4, tr5)
    assert c2 <= c1

    section("claim 7: box edges; classes of the all-dead window")
    for L in range(1, 8):
        b = count_edge_dead(3, L, 1, False)
        print(f"  box 3 x {L}: brute {b:>6d}   [M_1^{L + 4}]_00 = {pw[L + 4][1]:>6d}   {'ok' if b == pw[L + 4][1] else 'DIFFERENT'}")
        assert b == pw[L + 4][1]
    print("  journal: L = 1: 7; boxes 3 x 5..7: 2977, 13850, 64434")
    # k = 1 classes
    ncomp, lab = connected_components(sp.csr_matrix(Tc > 0), directed=True, connection='strong')
    print(f"  k = 1: 16-state graph has {ncomp} strongly connected class(es)")
    G1 = sp.csr_matrix(M1 > 0)
    ncomp, lab = connected_components(G1, directed=True, connection='strong')
    sizes = np.bincount(lab)
    cl0 = lab[0]
    sub = M1[np.ix_(lab == cl0, lab == cl0)]
    r0 = max(abs(np.linalg.eigvals(sub)))
    others = sorted(sizes[np.arange(ncomp) != cl0], reverse=True)[:3]
    print(f"  k = 1, M_1 itself: {ncomp} classes; class of 0 has {sizes[cl0]} of 4096 states, rho0 = {r0:.6f} "
          f"(rho = {rho1:.6f}); largest other classes: {others}")
    assert abs(r0 - rho1) < 1e-8
    # k = 2 classes (reduced matrix)
    ncomp, lab = connected_components(T2c > 0, directed=True, connection='strong')
    sizes = np.bincount(lab)
    cl0 = lab[0]
    mask = lab == cl0
    sub = T2c[mask][:, mask]
    r0, _ = spectral_radius(sub)
    other_sizes = sizes[np.arange(ncomp) != cl0]
    diag = T2c.diagonal()
    print(f"  k = 2: class of the all-dead state has {sizes[cl0]} of 65536 states (journal 54,591); "
          f"other classes: {len(other_sizes)}, largest {other_sizes.max()}; largest self-loop weight outside: "
          f"{diag[~mask].max():.0f}")
    print(f"  k = 2: rho of the class of 0 = {r0:.6f}, rho = {rho2:.6f}  -> c0_2 = c_2: {abs(r0 - rho2) < 1e-6}")
    assert abs(r0 - rho2) < 1e-6 and other_sizes.max() == 1
    # boxes at k = 2: brute against path sums of T2
    for L in (1, 2, 3, 4, 5):
        b = count_edge_dead(5, L, 2, False, chunk=1 << 19)
        # start states: negative columns dead; end: columns >= L dead. Path over centres 0..L-1.
        # state bits: row0 x-4..x+3 (0..7), row1 x-2..x+1 (8..11), row2 x-2..x+1 (12..15), x = centre about to be judged
        v = np.zeros(1 << 16)
        s = np.arange(1 << 16)
        start_ok = ((s & 0x0F) == 0) & (((s >> 8) & 0x3) == 0) & (((s >> 12) & 0x3) == 0)
        # columns present before centre 0: row0 cols 0..3 (bits 4..7), rows 1,2 cols 0..1 (bits 10,11 / 14,15);
        # columns >= L must be dead
        ok = start_ok.copy()
        for j in range(4):
            if j >= L:
                ok &= ((s >> (4 + j)) & 1) == 0
        for j in range(2):
            if j >= L:
                ok &= ((s >> (10 + j)) & 1) == 0
                ok &= ((s >> (14 + j)) & 1) == 0
        v[ok] = 1.0
        for x in range(L):
            v = T2c.T @ v
            # the new columns are row0[x+4], row1[x+2], row2[x+2]: must be dead if outside the box
            s_ok = np.ones(1 << 16, bool)
            if x + 4 >= L:
                s_ok &= ((s >> 7) & 1) == 0
            if x + 2 >= L:
                s_ok &= ((s >> 11) & 1) == 0
                s_ok &= ((s >> 15) & 1) == 0
            v[~s_ok] = 0.0
        t = int(round(v.sum()))
        print(f"  box 5 x {L} at generation 2: brute {b}, matrix path sum {t}   {'ok' if b == t else 'DIFFERENT'}")
        assert b == t

    section("claim 8: mirror ring (b), C4 and diagonal boxes (c), light cone (e); k = 1")
    wt = {(s, k): 4 * w1(s, k) for s in (0, 1) for k in range(5)}
    for L in (8, 10, 12, 14, 16, 18, 20, 22):
        n = L // 2 + 1
        # symmetric killable states of rows 0..2: sum over symmetric row 0 of prod over orbits of columns
        kill = 0
        for X in states(n):
            row = np.concatenate([X, X[:, 1:(L - n + 1)][:, ::-1]], axis=1)     # columns 0..n-1, then mirror images
            assert row.shape[1] == L
            k = sum(np.roll(row, d, axis=1) for d in (1, 2, -1, -2))
            w = np.ones(len(X))
            for x in range(n):
                tab = np.array([[wt[s, kk] for kk in range(5)] for s in (0, 1)])
                w *= tab[row[:, x], k[:, x]]
            kill += w.sum()
        kill = int(round(kill))
        bound = pw[n - 4][2] if n - 4 >= 1 else None
        if L == 8:
            # brute check of the reduction on the ring 3 x 8
            cnt = 0
            for X in states(3 * n):
                X = X.reshape(-1, 3, n)
                full = np.concatenate([X, X[:, :, 1:(L - n + 1)][:, :, ::-1]], axis=2)
                Y = step2d(full, periodic=True)
                cnt += int((Y[:, 0, :].sum(axis=1) == 0).sum())
            print(f"  mirror ring L = 8: brute over the 8^{n} symmetric states {cnt}, by weights {kill}")
            assert cnt == kill
        rate = -math.log(kill / 8.0 ** n) / L
        print(f"  mirror ring L = {L:2d}: killable symmetric {kill:>12d} of 8^{n};  bound 1^T M^(n-4) 1 = {bound};"
              f"  -(1/L) ln = {rate:.4f}  (c_1/2 = {c1 / 2:.4f})")
        if bound is not None:
            assert kill <= bound
    # C4 box 7 x 7: all 2^13 symmetric states
    def c4_count(L):
        orb = -np.ones((L, L), int)
        no = 0
        for r in range(L):
            for c in range(L):
                if orb[r, c] < 0:
                    rr, cc = r, c
                    for _ in range(4):
                        orb[rr, cc] = no
                        rr, cc = cc, L - 1 - rr
                    no += 1
        cnt = 0
        bands = set()
        for X in states(no, chunk=1 << 16):
            full = X[:, orb.ravel()].reshape(-1, L, L)
            Y = step2d(full, periodic=False)
            dead = Y[:, 0, :].sum(axis=1) == 0
            cnt += int(dead.sum())
            if L == 7:
                code = (full[:, :3, :].reshape(len(full), -1).astype(np.int64) << np.arange(3 * L)).sum(axis=1)
                bands.update(code.tolist())
        return no, cnt, len(bands)
    no, cnt, nb = c4_count(7)
    print(f"  C4 box 7 x 7: {cnt} of 2^{no} symmetric states have the top edge dead at generation 1 (journal 502 of 8192); "
          f"distinct bands {nb} (journal 4096)")
    assert (cnt, 1 << no, nb) == (502, 8192, 4096)
    print(f"    bounds of (c): [M^(L-2)]_00 = {pw[5][1]} <= {cnt // 2} <= [M^(L+4)]_00 = {pw[11][1]}")
    assert pw[5][1] <= cnt // 2 <= pw[11][1]

    # constrained bands, general L, k = 1: C4 (right corner = rotated left) and diagonal (left corner symmetric)
    def band_counts(L, kind):
        cells = [(r, c) for r in range(3) for c in range(L)]
        orb = {}
        for (r, c) in cells:
            if kind == 'C4':
                img = (c, L - 1 - r)                      # (row, column) -> rotated; lands in the band iff c <= 2
            else:
                img = (c, r)
            a, b = (r, c), img
            if b[0] <= 2 and 0 <= b[1] < L:
                orb.setdefault(min(a, b), set()).update([a, b])
            else:
                orb.setdefault(a, set()).add(a)
        # merge
        rep = {}
        for k_, v_ in orb.items():
            for cell in v_:
                rep.setdefault(cell, k_)
        # union-find for safety
        parent = {c: c for c in cells}
        def find(a):
            while parent[a] != a:
                a = parent[a]
            return a
        for (r, c) in cells:
            img = (c, L - 1 - r) if kind == 'C4' else (c, r)
            if img in parent:
                parent[find((r, c))] = find(img)
        roots = sorted({find(c) for c in cells})
        ridx = {rt: i for i, rt in enumerate(roots)}
        col = np.array([ridx[find(c)] for c in cells])
        kill = 0
        for X in states(len(roots)):
            band = X[:, col].reshape(-1, 3, L)
            Y = step2d(band, periodic=False)               # rows 0..2 only: row 0 at generation 1 is exact
            kill += int((Y[:, 0, :].sum(axis=1) == 0).sum())
        return len(roots), kill
    for kind in ('C4', 'diagonal'):
        for L in (7, 8):
            nfree, kill = band_counts(L, kind)
            lo_b, hi_b = pw[L - 2][1], pw[L + 4][1]
            expect = 3 * (L - 3) if kind == 'C4' else 3 * L - 3
            print(f"  {kind} box {L} x {L}: constrained bands 2^{nfree} (expected 2^{expect}), killable {kill}; "
                  f"[M^(L-2)]_00 = {lo_b} <= killable <= [M^(L+4)]_00 = {hi_b}: {lo_b <= kill <= hi_b}")
            assert nfree == expect and lo_b <= kill <= hi_b
    # (e) light cone, C4 box L = 11, k = 1: the cell x = 5 (distance >= 4k + 1 from both corners)
    L = 11
    orbmap = {}
    cells = [(r, c) for r in range(3) for c in range(L)]
    parent = {c: c for c in cells}
    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a
    for (r, c) in cells:
        img = (c, L - 1 - r)
        if img in parent:
            parent[find((r, c))] = find(img)
    roots = sorted({find(c) for c in cells})
    ridx = {rt: i for i, rt in enumerate(roots)}
    col = np.array([ridx[find(c)] for c in cells])
    cone = [(r, c) for r in range(3) for c in range(5 - 2, 5 + 3)]
    print(f"  (e) C4 box 11 x 11, k = 1: orbits met by the cone of the cell x = 5: {len({find(c) for c in cone})} "
          f"for {len(cone)} cells (no two in one orbit: {len({find(c) for c in cone}) == len(cone)})")
    hist_sym = np.zeros((2, 2), np.int64)
    alld_sym = 0
    for X in states(len(roots)):
        band = X[:, col].reshape(-1, 3, L)
        Y = step2d(band, periodic=False)
        np.add.at(hist_sym, (band[:, 0, 5], Y[:, 0, 5]), 1)
    hist_free = np.zeros((2, 2), np.int64)
    for X in states(15):                                    # the cell's cone, free soup
        w = X.reshape(-1, 3, 5)
        Y = step2d(w, periodic=False)
        np.add.at(hist_free, (w[:, 0, 2], Y[:, 0, 2]), 1)
    ps, pf = hist_sym / hist_sym.sum(), hist_free / hist_free.sum()
    print(f"      law of (state at 0, state at 1) of that cell: symmetric soup {ps.ravel()}, free soup {pf.ravel()}")
    assert np.allclose(ps, pf, atol=0, rtol=0)
    print(f"      control, the whole edge of the 7 x 7 box: P(dead at 1) = 251/4096 = {251 / 4096:.5f} under C4, "
          f"{pw[11][1]}/2^21 = {pw[11][1] / 2 ** 21:.5f} free")

    section("claim 12: gaps persist")
    # every state of the ring 3 x 9 would be 2^27; use ring 3 x 8, window at columns 0..l+3
    for l in (1, 2, 3, 4):
        viol = viol_ctrl = n_cond = n_ctrl = 0
        for X in states(24):
            X = X.reshape(-1, 3, 8)
            Y = step2d(X, periodic=True)
            cond = X[:, 0, :l + 4].sum(axis=1) == 0
            n_cond += int(cond.sum())
            viol += int((Y[cond][:, 0, 2:l + 2].sum(axis=1) > 0).sum())
            ctrl = X[:, 0, :l + 2].sum(axis=1) == 0        # control: only one dead cell of margin at each end
            n_ctrl += int(ctrl.sum())
            viol_ctrl += int((Y[ctrl][:, 0, 1:l + 1].sum(axis=1) > 0).sum())
        print(f"  ring 3 x 8, l = {l}, j = 1: {n_cond} states with the window of {l + 4} dead, middle {l} alive "
              f"somewhere next: {viol};  control (window {l + 2}): {viol_ctrl} of {n_ctrl}")
        assert viol == 0 and viol_ctrl > 0
    rng = np.random.default_rng(3)
    for j in (2, 3):
        W, L, l = 2 * j + 3, 4 * j + 9, 3
        X = (rng.random((200000, W, L)) < 0.5).astype(np.int8)
        X[:, 0, :l + 4 * j] = 0
        Y = X
        for _ in range(j):
            Y = step2d(Y, periodic=True)
        v = int((Y[:, 0, 2 * j:2 * j + l].sum(axis=1) > 0).sum())
        X2 = (rng.random((200000, W, L)) < 0.5).astype(np.int8)
        X2[:, 0, :l + 4 * j - 2] = 0
        Y2 = X2
        for _ in range(j):
            Y2 = step2d(Y2, periodic=True)
        v2 = int((Y2[:, 0, 2 * j - 1:2 * j - 1 + l].sum(axis=1) > 0).sum())
        print(f"  ring {W} x {L}, l = 3, j = {j}: 200000 random states with a dead window of {l + 4 * j}: violations {v}; "
              f"control (window {l + 4 * j - 2}): {v2}")
        assert v == 0 and v2 > 0

    section("claim 13: c_k(p) <= -ln(1 - p)")
    print("     p    -ln(1-p)    c_1(p)     c_2(p)")
    for p in (0.02, 0.05, 0.1, 0.2, 0.3, 0.472, 0.5, 0.6455, 0.8):
        c1p = -math.log(max(abs(np.linalg.eigvals(T1(p)))))
        c2p = -math.log(spectral_radius(T2(p))[0])
        print(f"  {p:6.4f}  {-math.log(1 - p):8.5f}  {c1p:9.6f}  {c2p:9.6f}")
        assert c2p <= c1p + 1e-9 <= -math.log(1 - p) + 2e-9

    section("claim 14: the dice hierarchy, exactly, on rings of L = 5 and L = 4")
    def d2_count(L, w, k):
        """Number of (start, dice history) of D2(L, 1/2; w) with row 0 empty at generation k; and the total."""
        ns = w * L
        cnt = np.ones(1 << ns, np.int64)                    # uniform start
        sh = np.arange(ns, dtype=np.int64)
        dice = ((np.arange(1 << (2 * L), dtype=np.int64)[:, None] >> np.arange(2 * L)) & 1).astype(np.int8)
        dice = dice.reshape(-1, 2, L)
        for t in range(k):
            new = np.zeros(1 << ns, np.int64)
            live = np.nonzero(cnt)[0]
            for lo in range(0, len(live), 1 << 10):
                idx = live[lo:lo + (1 << 10)]
                st = ((idx[:, None] >> sh) & 1).astype(np.int8).reshape(-1, 1, w, L)
                st = np.broadcast_to(st, (len(idx), dice.shape[0], w, L))
                dd = np.broadcast_to(dice[None], (len(idx), dice.shape[0], 2, L))
                full = np.concatenate([st, dd], axis=2).reshape(-1, w + 2, L)
                Y = step2d(full, periodic=True)[:, :w, :]   # rows 0..w-1 by the rule; rows w, w+1 were dice
                code = (Y.reshape(len(full), ns).astype(np.int64) << sh).sum(axis=1)
                np.add.at(new, code, np.repeat(cnt[idx], dice.shape[0]))
            cnt = new
        row0_mask = (1 << L) - 1
        dead = (np.arange(1 << ns) & row0_mask) == 0
        return int(cnt[dead].sum()), 1 << (ns + 2 * L * k)
    true = {(5, 1): 2507 / 8 ** 5, (5, 2): b5 / 32 ** 5, (4, 1): brute_ring[4] / 8 ** 4, (4, 2): b4 / 32 ** 4}
    for (L, w, k) in [(5, 1, 1), (5, 2, 1), (5, 3, 2), (4, 3, 2), (4, 4, 2), (5, 1, 2), (5, 2, 2), (4, 1, 2), (4, 2, 2)]:
        a, tot = d2_count(L, w, k)
        eq = a / tot == true[L, k]
        need = w >= 2 * k - 1
        print(f"  D2(L = {L}; w = {w}), k = {k}: P(row 0 empty) = {a}/{tot} = {a / tot:.8f}; true rule {true[L, k]:.8f}; "
              f"equal: {eq}  (w >= 2k - 1: {need})")
        assert eq == need
    print(f"\nall assertions passed  [{time.time() - t00:.0f} s]")


if __name__ == "__main__":
    main()
