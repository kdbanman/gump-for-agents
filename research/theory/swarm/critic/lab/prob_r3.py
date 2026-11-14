"""Critic's lab: probability, round 3 (entries 11-15). Exact; no sampling.

  python3 prob_r3.py r10 [m]   R10: Lemma 5's three moves, arcs of m = 1..8 cells, every row on I + [-6, 6] (default 8: 1 min)
                               and the bound P_S(S_3 misses I) >= p^(3m+12) from the exact kernel on small rings
  python3 prob_r3.py r11 [M]   R11: Lemma 6, the graph S -> S' iff F(S) <= S' <= S + N(S) on non-empty subsets of an interval of
                               M = 5..14 cells, dead and reflecting ends: one strongly connected class?
  python3 prob_r3.py r12       R12: Lemma 4: tables (O1), (O2), the marks' implications (a), (b); the coupling (c) run on a periodic
                               face with every die drawn; what fails when the three counts of a cube come from real cells
  python3 prob_r3.py pe1       arithmetic: the two sizes of exam P-E1 that are in the examiner's log against the exact tables
  python3 prob_r3.py all
"""
import sys, os, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prob_r1 as pr
import prob_r2 as p2

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# alive-sets of the 2D edge cell: b in {0,1,2} live beneath, k live among the four in-row neighbours
def alive_set(x, k):
    return frozenset(b for b in (0, 1, 2) if (k + b) in ((2, 3, 4) if x else (3, 4)))


def cheap(want_alive, x, k):
    """is the outcome available with conditional probability >= min(pi0, pi2) (the set of b giving it contains 0 or 2), or forced?"""
    s = alive_set(x, k) if want_alive else frozenset((0, 1, 2)) - alive_set(x, k)
    return (0 in s) or (2 in s)


def r10(mmax=8):
    print("R10. Lemma 5: an arc I of m cells is emptied in three generations by dice on I+4, I+2, I, whatever the row beyond I+6")
    AL = np.array([[len(alive_set(x, k)) for k in range(5)] for x in (0, 1)])
    CH_alive = np.array([[cheap(True, x, k) for k in range(5)] for x in (0, 1)])
    CH_dead = np.array([[cheap(False, x, k) for k in range(5)] for x in (0, 1)])
    for m in range(1, mmax + 1):
        W = m + 12                                        # cells 0..W-1 = I + [-6, 6]; I = cells 6..6+m-1
        n = 1 << W
        S = ((np.arange(n)[:, None] >> np.arange(W)) & 1).astype(np.int8)
        def kcount(X, lo, hi):                            # in-row counts of cells lo..hi-1 (their neighbours lie inside the array)
            return X[:, lo - 2:hi - 2] + X[:, lo - 1:hi - 1] + X[:, lo + 1:hi + 1] + X[:, lo + 2:hi + 2]
        # D on I+4 = cells 2..W-3 (needs S on I+6)
        lo1, hi1 = 2, W - 2
        k0 = kcount(S, lo1, hi1); x0 = S[:, lo1:hi1]
        D = ((x0 + k0) > 0).astype(np.int8)
        # move 1: outcome D for every cell of I+4
        ok1 = np.where(D == 1, CH_alive[x0, k0], CH_dead[x0, k0]).all()
        forced_dead_ok = ((D == 1) | ((x0 == 0) & (k0 == 0))).all()
        S1 = np.zeros_like(S); S1[:, lo1:hi1] = D
        # move 2: cells of I+2 = 4..W-5
        lo2, hi2 = 4, W - 4
        k1 = kcount(S1, lo2, hi2); x1 = S1[:, lo2:hi2]
        no_small = (~((x1 == 1) & (k1 <= 1))).all()        # a live cell of S_1 inside I+2 has k >= 2
        E = ((x1 == 1) & (k1 == 2)).astype(np.int8)        # forced survivors
        ok2 = np.where(E == 1, True, CH_dead[x1, k1]).all()
        S2 = np.zeros_like(S); S2[:, lo2:hi2] = E
        # move 3: cells of I = 6..W-7: every one dead next
        lo3, hi3 = 6, W - 6
        k2 = kcount(S2, lo3, hi3); x2 = S2[:, lo3:hi3]
        not_forced = (~((x2 == 1) & (k2 == 2))).all()
        ok3 = CH_dead[x2, k2].all()
        # E has no two cells within distance 2 (inside I+2)
        sep = (((E[:, :-1] + E[:, 1:]) < 2).all() and ((E[:, :-2] + E[:, 2:]) < 2).all())
        check(bool(ok1 and forced_dead_ok and no_small and ok2 and sep and not_forced and ok3),
              f"m = {m}: all {n:,} rows on I+6: move 1 (S_1 = D on I+4), move 2 (kill k >= 3, no birth: S_2 = E on I+2), move 3 (I dead): every prescribed outcome is forced or allowed by b = 0 or b = 2; no two cells of E within distance 2")
    print("   the bound itself, from the exact kernel (ring; min over every non-empty row S of P_S(S_3 misses I) against p^(3m+12)):")
    for name, pi in (("anchor (1/2, 0, 1/2)", (0.5, 0.0, 0.5)), ("Bin(2, 0.472)", p2.D2)):
        a = pr.a_table(pi); p = min(pi[0], pi[2])
        for m, L in ((1, 13), (2, 14), (3, 15)):
            right, _ = p2.make_ops(L, 'ring', a)
            idx = np.arange(1 << L)
            f = np.ones(1 << L)
            for c in range(m): f *= 1 - ((idx >> (L - 1 - c)) & 1)          # arc = cells 0..m-1 dead
            g = right(right(right(f)))
            mn = float(g[1:].min())
            check(mn >= p ** (3 * m + 12) * (1 - 1e-9), f"   {name}, L = {L}, m = {m}: min_S P_S(S_3 misses I) = {mn:.3e} >= p^(3m+12) = {p ** (3 * m + 12):.3e}  (ratio {mn / p ** (3 * m + 12):.1f})")


# ------------------------------------------------------------------------------------------------ R11
def r11(Mmax=14):
    print("R11. Lemma 6: E1(pi), pi0, pi2 > 0, on an interval of M cells: S -> S' has positive probability iff F(S) <= S' <= S + N(S)")
    # the characterisation of positive transitions, from the table a(x, k) at a law with pi0, pi1, pi2 > 0 and at the anchor (pi1 = 0)
    for pi in ((0.3, 0.4, 0.3), (0.5, 0.0, 0.5)):
        a = pr.a_table(pi)
        good = all((a[1, k] == 1.0) == (k == 2) and a[1, k] > 0 for k in range(5)) and all((a[0, k] == 0.0) == (k == 0) and a[0, k] < 1 for k in range(5))
        check(good, f"pi = {pi}: a live cell is forced to stay iff k = 2 and is never forced to die; a dead cell is forced to stay dead iff k = 0 and is never forced to be born")
    for kind in ('dead', 'refl'):
        res = []
        for M in range(5, Mmax + 1):
            nbs = p2.neighbours(M, kind)
            n = 1 << M
            idx = np.arange(n)
            bit = lambda y: (idx >> (M - 1 - y)) & 1
            k = np.zeros((M, n), np.int64)
            for y in range(M):
                for z in nbs[y]: k[y] += bit(z)
            F = np.zeros(n, np.int64); U = np.zeros(n, np.int64)
            for y in range(M):
                x = bit(y)
                F |= ((x == 1) & (k[y] == 2)).astype(np.int64) << (M - 1 - y)
                U |= ((x == 1) | (k[y] >= 1)).astype(np.int64) << (M - 1 - y)
            full = n - 1
            # (i) every non-empty S reaches the full interval (S -> S + N(S) repeatedly)
            cur = idx.copy(); steps = 0
            while not (cur[1:] == full).all() and steps < 3 * M:
                cur = U[cur]; steps += 1
            reach_full = bool((cur[1:] == full).all())
            # (ii) forward search from the full interval: successors of S are F(S) | sub, sub a submask of U(S) & ~F(S), non-empty
            seen = np.zeros(n, bool); seen[full] = True
            frontier = [full]; depth = 0
            while frontier and not seen[1:].all():
                nxt = []
                for s in frontier:
                    f, free = int(F[s]), int(U[s] & ~F[s])
                    if free == full and f == 0:
                        new = np.flatnonzero(~seen[1:]) + 1; seen[1:] = True; nxt.extend(new.tolist()); break
                    bits = [b for b in range(M) if (free >> b) & 1]
                    sub = np.zeros(1, np.int64)
                    for b in bits: sub = np.concatenate([sub, sub | (1 << b)])
                    t = f | sub; t = t[t != 0]
                    new = t[~seen[t]]
                    seen[new] = True; nxt.extend(new.tolist())
                frontier = nxt; depth += 1
            ok = reach_full and bool(seen[1:].all())
            res.append((M, ok, steps, depth))
            if not ok: check(False, f"{kind} ends, M = {M}: not strongly connected")
        check(all(r[1] for r in res), f"{kind} ends, M = 5..{Mmax}: every non-empty S reaches the full interval (at most {max(r[2] for r in res)} steps) and the full interval reaches every non-empty T "
              f"(search depth {[r[3] for r in res]}): one class; a state with a loop exists (the class contains S -> S), so the chain is aperiodic")
    # the steps of the proof, M = 5..14, dead ends
    good = True
    for M in range(5, Mmax + 1):
        nbs = p2.neighbours(M, 'dead')
        def FU(S):
            k = {y: sum(1 for z in nbs[y] if z in S) for y in range(M)}
            return {y for y in S if k[y] == 2}, set(S) | {y for y in range(M) if k[y] >= 1}
        def step_ok(S, T):
            f, u = FU(S); return f <= T <= u and len(T) > 0
        J = set(range(M))
        chain = [J, {0, M - 1}, {0}, {2}, {0, 3}]
        R = {0, 3}; r = 3
        while r + 3 <= M - 1:
            chain.append(R | {r + 2}); R = R | {r + 3}; r += 3; chain.append(set(R))
        good &= all(step_ok(a, b) for a, b in zip(chain, chain[1:]))
        f, u = FU(R)
        good &= (f == set() and u == J)
    check(good, f"the proof's chain, M = 5..{Mmax}: J -> {{1, M}} -> {{1}} -> {{3}} -> {{1, 4}} -> ... -> R = {{1, 4, 7, ...}}, each step allowed; R is loose and D(R) = J, so R -> every T")


# ------------------------------------------------------------------------------------------------ R12
def B(x, k):
    """alive-set of a gump face cell: b in {0..3} live beneath, k live in-face neighbours; alive next iff n = k + b in {4,5} (dead) or {3,4,5} (live)."""
    return frozenset(b for b in range(4) if (k + b) in ((3, 4, 5) if x else (4, 5)))


def kappa_gamma(x, k):
    Bs = B(x, k)
    kap = 0 if 0 not in Bs else 3
    if x + k >= 1 and k <= 5:
        gam = frozenset({0}) if 0 in Bs else (frozenset({3}) if 3 in Bs else frozenset({1, 2}))
    else:
        gam = frozenset({1, 2})
    return kap, gam


def r12():
    print("R12. Lemma 4: gump's face rule driven by counts b in {0, 1, 2, 3}")
    want_dead = {0: set(), 1: {3}, 2: {2, 3}, 3: {1, 2}, 4: {0, 1}, 5: {0}, 6: set()}
    want_live = {0: {3}, 1: {2, 3}, 2: {1, 2, 3}, 3: {0, 1, 2}, 4: {0, 1}, 5: {0}, 6: set()}
    check(all(B(0, k) == want_dead[k] and B(1, k) == want_live[k] for k in range(7)), "the table of alive-sets B(x, k), k = 0..6, as printed in entry 13")
    check(all(not ({0, 3} <= B(x, k)) for x in (0, 1) for k in range(7)), "(O1) no alive-set contains both 0 and 3: its complement contains 0 or 3")
    o2 = all((0 in B(x, k)) or (3 in B(x, k)) or B(x, k) == {1, 2} for x in (0, 1) for k in range(6) if x + k >= 1)
    only = [(x, k) for x in (0, 1) for k in range(6) if x + k >= 1 and B(x, k) == {1, 2}]
    check(o2 and only == [(0, 3)], "(O2) for x + k >= 1, k <= 5 the alive-set contains 0, or contains 3, or is {1, 2}; the last only for a dead cell with k = 3")
    good = True
    for x in (0, 1):
        for k in range(7):
            kap, gam = kappa_gamma(x, k)
            good &= kap not in B(x, k) and kap not in gam
            if x + k >= 1 and k <= 5: good &= gam <= B(x, k)
    check(good, "(a), (b): kappa(x, k) is outside B(x, k) and outside gamma(x, k); gamma(x, k) is inside B(x, k) whenever x + k >= 1 and k <= 5")
    check(abs((1 / 3) * (1 - (2 / 3) ** 6) - 665 / 2187) < 1e-15 and abs(1 - (2 / 3) ** 3 - 19 / 27) < 1e-15, "entry 14: sigma (1 - (1 - s)^6) = 665/2187 = 0.3041 at s = sigma = 1/3; 1 - (1 - sigma)^3 = 19/27 = 0.7037")
    # (c) on a periodic face 3 x 3 cubes (27 cells), dice i.i.d. with law (1/3, 1/6, 1/6, 1/3): the coupling, path by path
    import startpoints as sp
    cells, nb = sp.make_slab(3, 3, 1)
    n = len(cells)
    check(n == 27 and all(len(set(v)) == 6 for v in nb), "periodic face of 3 x 3 cubes: 27 cells, six distinct in-face neighbours each")
    nbr = np.array(nb)
    rng = np.random.default_rng(4)
    law = np.array([1 / 3, 1 / 6, 1 / 6, 1 / 3]); s_, sig = 1 / 3, 1 / 3
    KAP = np.array([[kappa_gamma(x, k)[0] for k in range(7)] for x in (0, 1)])
    GAM = np.zeros((2, 7, 4), bool)
    for x in (0, 1):
        for k in range(7):
            for b in kappa_gamma(x, k)[1]: GAM[x, k, b] = True
    ALIVE = np.zeros((2, 7, 4), bool)
    for x in (0, 1):
        for k in range(7):
            for b in B(x, k): ALIVE[x, k, b] = True
    Rr = 20000; T = 12
    S = (rng.random((Rr, n)) < 0.5)
    eta = S.copy(); Z = ~S
    bad = 0; marks = np.zeros(3); pairs = np.zeros((3, 3)); nontrivial = 0
    prevM = None
    for t in range(T):
        k = S[:, nbr].sum(2); x = S.astype(int)
        b = rng.choice(4, size=(Rr, n), p=law)
        kap = KAP[x, k]; ing = GAM[x, k, b]
        qK = law[kap]; qG = np.where(GAM[x, k], law[None, None, :], 0).sum(2)
        V = rng.random((Rr, n))
        M = np.full((Rr, n), 2)                                 # 0 = K, 1 = G, 2 = N
        M[(b == kap) & (V <= s_ / qK)] = 0
        M[ing & (V <= sig / qG)] = 1
        Snew = ALIVE[x, k, b]
        etanew = (M == 1) & (eta[:, nbr].any(2) | eta) & Z[:, nbr].any(2)
        bad += int((etanew & ~Snew).sum()) + int(((M == 0) & Snew).sum())
        for v in range(3): marks[v] += (M == v).sum()
        if prevM is not None:
            for u in range(3):
                for v in range(3): pairs[u, v] += ((prevM == u) & (M == v)).sum()
        S, eta, Z, prevM = Snew, etanew, (M == 0), M
        nontrivial += int(eta.sum())
    freq = marks / marks.sum(); joint = pairs / pairs.sum()
    check(bad == 0, f"(c): 20,000 faces x 12 generations with every die drawn: eta_t inside S_t and no cell marked K alive, without exception (the marks' frequencies K, G, N: {freq[0]:.4f}, {freq[1]:.4f}, {freq[2]:.4f};"
          f" largest |joint - product| of a cell's marks in successive generations {np.abs(joint - np.outer(joint.sum(1), joint.sum(0))).max():.1e}; the test is not vacuous: {nontrivial:,} cell-generations of eta alive)")
    # what real cells beneath do to the hypothesis: the cube lemma, b_a = u_b + u_c + v_a for the three faces of one top cube
    trip = set()
    for u in itertools.product((0, 1), repeat=3):
        for v in itertools.product((0, 1), repeat=3):
            trip.add((u[1] + u[2] + v[0], u[0] + u[2] + v[1], u[0] + u[1] + v[2]))
    check(len(trip) == 40 and not any(t[0] == 3 and t[1] == 0 for t in trip), "cube lemma: of the 64 triples of counts beneath one cube 40 occur, and (3, 0, .) does not: independent counts with pi0 pi3 > 0 are not counts of cells")
    # one-generation killability of a cube triple by real cells: is there, for every (x, k) of its three cells, a pattern beneath that kills all three?
    unk = []; npic = 0
    states = [(x, k) for x in (0, 1) for k in range(7)]
    for st in itertools.product(states, repeat=3):
        # the three cells of a cube are mutual in-face neighbours: k_i counts the two mates and four other cells
        if not all(st[(i + 1) % 3][0] + st[(i + 2) % 3][0] <= st[i][1] <= st[(i + 1) % 3][0] + st[(i + 2) % 3][0] + 4 for i in range(3)): continue
        npic += 1
        if not any(all(t[i] not in B(*st[i]) for i in range(3)) for t in trip): unk.append(st)
    ex = ((1, 3), (1, 2), (1, 2))
    check(len(unk) > 0 and ex in unk, f"with real cells beneath, {len(unk)} of the {npic} local pictures (x, k) of a cube triple cannot be killed together by any pattern of the six cells (example, board E10: three live cells with k = 3, 2, 2: the first needs b = 3, the others b = 0);"
          " so Lemma 4 (a) and the bound E T <= s^-A are statements about F(pi), not about a face over dice cells (D3)")
    # per-cell kill and per-cell grow under D3 with density rho: P(b = 0), P(b = 3) given the other two cells' counts can be 0
    zero = sum(1 for t in trip if t[0] == 3) and not any(t[0] == 0 and t[1] == 3 for t in trip)
    check(zero, "   in D3, P(b_a = 0 | b_b = 3) = 0: the conditional hypothesis of Lemma 4 fails inside a cube for every density")


def pe1():
    print("exam P-E1 (scored 'not decidable': slope 30 -> 38 = 0.512 +- 0.012): the examiner's three sizes against the exact tables of D2(., 0.472) (board L4.1, L4.2)")
    ring = {16: 9.1536, 17: 9.6834 - 0.0, 18: 9.6834, 19: 10.2118}
    dead19, step_d = 10.9538, 0.4595
    meas = {30: (15.843, 0.025), 34: (17.900, 0.042), 38: (19.941, 0.089)}
    print("      ring minus dead-ended interval of equal length, exact, L = 5, 10, 14, 19: -2.07, -1.38, -1.08, -0.74; fitted on L = 11..19 by -4.30 + 1.21 ln L (rms 0.016) or by -2.27 + 0.082 L (rms 0.028)")
    for L, (v, e) in meas.items():
        d = dead19 + step_d * (L - 19)
        a = d - 4.30 + 1.21 * np.log(L); b = d - 2.27 + 0.082 * L
        print(f"      L = {L}: interval extrapolated at its converged step 0.4595: {d:.3f}; ring predicted by the power form {a:.3f}, by the two-exponent form {b:.3f}; measured {v:.3f} +- {e:.3f}"
              f"  ({(v - a) / e:+.1f} and {(v - b) / e:+.1f} standard errors)")
    prev = (19, ring[19], 0.0)
    print("      ring's mean step between successive sizes, and the same minus the interval's 0.4595:")
    for L in (30, 34, 38):
        v, e = meas[L]
        st = (v - prev[1]) / (L - prev[0]); er = np.hypot(e, prev[2]) / (L - prev[0])
        mid = 0.5 * (L + prev[0])
        print(f"         {prev[0]} -> {L}: {st:.4f} +- {er:.4f}  (excess {st - step_d:+.4f}; the power form gives {1.21 * np.log(L / prev[0]) / (L - prev[0]):+.4f}, the two-exponent form +0.0820; exact at L = 16..19: +0.062 to +0.068)")
        prev = (L, v, e)
    # ring minus interval at L = 19 (exact), 30, 34, 38: a ln L + c and a L + c through the exact point, least squares on the three sampled ones
    Ls = np.array([30., 34., 38.]); y = np.array([meas[int(L)][0] - (dead19 + step_d * (L - 19)) for L in Ls]); e = np.array([meas[int(L)][1] for L in Ls])
    y19 = ring[19] - dead19
    for name, f in (("power form, y = y19 + a ln(L/19)", lambda L: np.log(L / 19)), ("two exponents, y = y19 + a (L - 19)", lambda L: L - 19.0)):
        X = f(Ls); a = float((X * (y - y19) / e ** 2).sum() / (X * X / e ** 2).sum()); chi = float((((y - y19 - a * X) / e) ** 2).sum())
        print(f"      {name}: a = {a:.3f}, chi^2 = {chi:.2f} on 2 (ring minus interval: exact {y19:.3f} at 19; sampled " + ', '.join(f"{v:+.3f} +- {s_:.3f}" for v, s_ in zip(y, e)) + ")")
    print("      (the interval's ln tau beyond M = 19 is its exact value at 19 plus 0.4595 per cell, the step it has held to 0.001 from M = 15 to 19; an error of 0.0005 in that step moves the differences by 0.006, 0.008, 0.010)")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if cmd in ('r10', 'all'): r10(arg or 8)
    if cmd in ('r11', 'all'): r11(arg or 14)
    if cmd in ('r12', 'all'): r12()
    if cmd in ('pe1', 'all'): pe1()
    print('ALL OK' if OK else 'SOMETHING FAILED')
