#!/usr/bin/env python3
"""Audit of the counting line, the abstract lemmas and the small exact facts: claims 1, 2, 3, 15, 17, 18, 19, 20.

  python3 c5_measure.py            (about 2 minutes, one core)

Gump vessels and stepper: p0_lib (checked against reference/oracle.py). 2D rule: c0_lib.
"""
import itertools, math, sys, time
from fractions import Fraction as F
import numpy as np
from p0_lib import Vessel, hull_cells, DIAGS
from c0_lib import step2d, states, rule, w1

t00 = time.time()
rng = np.random.default_rng(2026)


def section(s):
    print(f"\n=== {s}  [{time.time() - t00:.0f} s]")


def table_of(step, N):
    """f as a table on state indices (bit i = cell i)."""
    idx = np.arange(1 << N, dtype=np.int64)
    X = ((idx[:, None] >> np.arange(N)) & 1).astype(np.int8)
    Y = step(X)
    return (Y.astype(np.int64) << np.arange(N)).sum(axis=1)


def random_invariant(n):
    """A map g on {0..n-1} and a probability mu (Fractions) with mu(g^-1 B) = mu(B): a permutation of the support
    with mu constant on its cycles, and g arbitrary on the null set."""
    ns = int(rng.integers(1, n + 1))
    supp = rng.permutation(n)[:ns]
    perm = rng.permutation(ns)
    g = rng.integers(0, n, n)
    g[supp] = supp[perm]
    mu = [F(0)] * n
    seen = np.zeros(ns, bool)
    for i in range(ns):
        if not seen[i]:
            w = F(int(rng.integers(1, 10)))
            j = i
            while not seen[j]:
                seen[j] = True
                mu[supp[j]] = w
                j = perm[j]
    tot = sum(mu)
    return g, [m / tot for m in mu]


def hit_times(g, H, kmax):
    n = len(g)
    T = np.full(n, 10 ** 9)
    cur = np.arange(n)
    inH = np.zeros(n, bool); inH[list(H)] = True
    for t in range(kmax + 1):
        new = inH[cur] & (T == 10 ** 9)
        T[new] = t
        cur = g[cur]
    return T


def main():
    section("claim 1 (a): mu(T_H <= k) <= (k + 1) mu(H) for maps preserving mu (exact fractions)")
    viol = tests = 0
    for trial in range(3000):
        n = int(rng.integers(2, 30))
        g, mu = random_invariant(n)
        # invariance, checked
        for y in range(n):
            assert sum(mu[x] for x in range(n) if g[x] == y) == mu[y]
        H = set(rng.permutation(n)[:int(rng.integers(1, n))].tolist())
        T = hit_times(g, H, 40)
        mH = sum(mu[x] for x in H)
        for k in range(0, 41, 3):
            tests += 1
            viol += sum(mu[x] for x in range(n) if T[x] <= k) > (k + 1) * mH
    print(f"  {tests} tests on 3000 random (g, mu, H): violations {viol}")
    assert viol == 0
    viol = tests = 0
    for trial in range(3000):
        n = int(rng.integers(2, 30))
        g = rng.integers(0, n, n)
        w = rng.integers(1, 10, n); mu = [F(int(a), int(w.sum())) for a in w]
        H = set(rng.permutation(n)[:int(rng.integers(1, max(2, n // 4)))].tolist())
        T = hit_times(g, H, 40)
        mH = sum(mu[x] for x in H)
        tests += 1
        viol += any(sum(mu[x] for x in range(n) if T[x] <= k) > (k + 1) * mH for k in range(0, 41, 3))
    print(f"  control, mu not invariant: the bound fails for {viol} of {tests} random (g, mu, H)")
    assert viol > 0

    section("claim 1 (b): bijections")
    bad = ctrl = ctrl_n = 0
    for trial in range(5000):
        n = int(rng.integers(1, 40))
        g = rng.permutation(n)
        H = rng.permutation(n)[:int(rng.integers(1, n + 1))]
        inH = np.zeros(n, bool); inH[H] = True
        # cycles
        seen = np.zeros(n, bool); Xp = []
        for i in range(n):
            if not seen[i]:
                cyc = [i]; seen[i] = True; j = g[i]
                while j != i:
                    cyc.append(j); seen[j] = True; j = g[j]
                if inH[cyc].any():
                    Xp += cyc
        Xp = np.array(Xp)
        T = hit_times(g, set(H.tolist()), n + 1)
        R = []
        for x in H:
            r = 1; y = g[x]
            while not inH[y]:
                y = g[y]; r += 1
            R.append(r)
        R = np.array(R)
        bad += R.sum() != len(Xp)
        bad += T[Xp].sum() != (R * (R - 1) // 2).sum()
        mean = F(int(T[Xp].sum()), len(Xp))
        bad += mean < F(len(Xp), 2 * len(H)) - F(1, 2)
        if len(Xp) < n:
            ctrl_n += 1
            ctrl += mean < F(n, 2 * len(H)) - F(1, 2)
    print(f"  5000 random permutations and sets H: failures of (sum R = |X'|, sum T = sum R(R-1)/2, mean >= |X'|/2|H| - 1/2): {bad}")
    print(f"  control: when a cycle misses H ({ctrl_n} cases) the form with |X| fails for the states that do fall in {ctrl} cases")
    assert bad == 0 and ctrl > 0
    for n in (1, 2, 7, 30):
        T = hit_times(np.roll(np.arange(n), -1), {0}, n + 1)
        assert F(int(T.sum()), n) == F(n - 1, 2)
    print("  rotation of Z_n, H = {0}: mean (n - 1)/2, equality (n = 1, 2, 7, 30)")

    section("claims 2, 3: the second-order lift on small vessels, every pair-state")
    vessels = []
    V = Vessel(hull_cells(1))
    vessels.append(("gump, one cube (hull R = 1)", V.N, lambda X, V=V: V.step(X), V.layer((1, 1, 1), 1)))
    C = {d: 1 for d in DIAGS}; C[(1, 1, 1)] = 3; C[(1, 1, -1)] = 3
    V = Vessel(hull_cells(C, bound=3))
    vessels.append(("gump, hull C = 3 on (1,1,1), (1,1,-1), 1 elsewhere", V.N, lambda X, V=V: V.step(X), V.layer((1, 1, 1), 3)))
    C = {d: 1 for d in DIAGS}; C[(1, 1, 1)] = 3; C[(1, 1, -1)] = 3; C[(1, -1, 1)] = 3
    V = Vessel(hull_cells(C, bound=3))
    vessels.append(("gump, hull C = 3 on (1,1,1), (1,1,-1), (1,-1,1)", V.N, lambda X, V=V: V.step(X), V.layer((1, 1, 1), 3)))
    vessels.append(("2D rule, strip 2 x 4", 8, lambda X: step2d(X.reshape(-1, 2, 4), True).reshape(-1, 8), [0, 1, 2, 3]))
    vessels.append(("2D rule, box 3 x 3", 9, lambda X: step2d(X.reshape(-1, 3, 3), False).reshape(-1, 9), [0, 1, 2]))
    for name, N, step, face in vessels:
        if N > 11:
            print(f"  {name}: {N} cells, skipped (too many pair-states)")
            continue
        f = table_of(step, N)
        A = len(face)
        fm = sum(1 << i for i in face)
        n1 = 1 << N
        # claim 3: H absorbing; {T <= k} = f^-k(H)
        Hs = (np.arange(n1) & fm) == 0
        absorbing = bool(Hs[f[Hs]].all())
        cur = np.arange(n1); frac = []
        for k in range(0, 9):
            frac.append(int(Hs[cur].sum())); cur = f[cur]
        u = np.arange(n1 * n1, dtype=np.int64) & (n1 - 1)
        v = np.arange(n1 * n1, dtype=np.int64) >> N
        phi = v | ((f[v] ^ u) << N)
        bij = len(np.unique(phi)) == n1 * n1
        inv = (f[u] ^ v) | (u << N)                                  # claimed inverse (v, w) -> (f(v) xor w, v)
        inv_ok = bool((inv[phi] == np.arange(n1 * n1)).all())
        H = (v & fm) == 0
        H2 = H & ((u & fm) == 0)
        fracH = F(int(H.sum()), n1 * n1)
        h2_in = bool(H2[phi[H2]].all())
        enters = int((H2[phi] & ~H2).sum())                           # states outside H2 mapped into H2
        cur = np.arange(n1 * n1); ever = H.copy(); okk = True; pre = []
        for k in range(1, 13):
            cur = phi[cur]
            pre.append(int(H[cur].sum()))
            ever |= H[cur]
            okk &= F(int(ever.sum()), n1 * n1) <= (k + 1) * F(1, 1 << A)
        print(f"  {name}: {N} cells, face {A}")
        print(f"    f(H) in H: {absorbing};  |f^-k(H)| for k = 0..8: {frac} of {n1}")
        print(f"    lift: bijection {bij}, inverse as stated {inv_ok}; |H|/|X^2| = {fracH} (2^-A = {F(1, 1 << A)}); "
              f"#(Phi^t x in H) for t = 1..12 all equal |H|: {all(p == int(H.sum()) for p in pre)}")
        print(f"    Phi(H2) in H2: {h2_in}; states outside H2 mapped into H2: {enters}; "
              f"'face empty at some generation <= k' <= (k+1) 2^-A for k = 1..12: {okk}")
        assert absorbing and bij and inv_ok and fracH == F(1, 1 << A) and h2_in and enters == 0 and okk
        assert all(p == int(H.sum()) for p in pre)
    # confinement of the lift: a hull inside a larger vessel
    C = {d: 1 for d in DIAGS}; C[(1, 1, 1)] = 3; C[(1, 1, -1)] = 3
    small = Vessel(hull_cells(C, bound=3)); big = Vessel(hull_cells(5))
    pos = [big.index[p] for p in small.cells]
    n1 = 1 << small.N
    allst = ((np.arange(n1)[:, None] >> np.arange(small.N)) & 1).astype(np.int8)
    Xb = np.zeros((n1, big.N), np.int8); Xb[:, pos] = allst
    Yb = big.step(Xb)
    outside = np.ones(big.N, bool); outside[pos] = False
    print(f"  confinement: every state of the 8-cell hull, stepped inside the hull R = 5 ({big.N} cells): cells born outside "
          f"{int(Yb[:, outside].sum())}; agrees with the hull's own step: {bool((Yb[:, pos] == small.step(allst)).all())}"
          f"  (so f(v) xor u stays in the hull when u and v do)")
    assert Yb[:, outside].sum() == 0 and (Yb[:, pos] == small.step(allst)).all()
    # claim 3 on a real face: hull R = 3
    V3 = Vessel(hull_cells(3)); f3 = V3.layer((1, 1, 1), 3)
    X = (rng.random((200000, V3.N)) < 0.5).astype(np.int8); X[:, f3] = 0
    print(f"  hull R = 3, 200000 random states with the face (1,1,1) empty: face cells alive next: {int(V3.step(X)[:, f3].sum())}")
    assert V3.step(X)[:, f3].sum() == 0

    section("claim 20 (Lemma 2'): invariant measure and absorbing set")
    bad = tests = 0
    for trial in range(3000):
        n = int(rng.integers(2, 30))
        g, mu = random_invariant(n)
        H = set(rng.permutation(n)[:int(rng.integers(1, n))].tolist())
        while True:                                                   # close H forwards: g(H) in H
            new = {int(g[x]) for x in H} - H
            if not new:
                break
            H |= new
        T = hit_times(g, H, n + 1)
        tests += 1
        bad += sum(mu[x] for x in range(n) if x not in H and T[x] < 10 ** 9) != 0
    print(f"  {tests} random (g, mu, absorbing H): mu(points outside H that enter H) != 0 in {bad} cases")
    assert bad == 0
    V = Vessel(hull_cells(1)); f = table_of(V.step, V.N); face = V.layer((1, 1, 1), 1)
    fm = sum(1 << i for i in face)
    full = (1 << V.N) - 1
    living = [x for x in range(1 << V.N) if x & fm]
    T = hit_times(f, {x for x in range(1 << V.N) if not (x & fm)}, 70)
    dying = sum(1 for x in living if T[x] < 10 ** 9)
    print(f"  wording: gump on one cube (6 cells): the full cube is a fixed point (f(full) = full: {f[full] == full}) with a live face, "
          f"so the point mass on it is an invariant measure carried by a living state; yet {dying} of the {len(living)} living states die")
    assert f[full] == full and dying > 0

    section("claim 15 (Lemma 7): every state of a 5 x 5 patch of the half-plane")
    cnt = np.zeros((2, 2, 2), np.int64)                               # [s, alive (x,1), alive (x,2)]
    for X in states(25, chunk=1 << 19):
        X = X.reshape(-1, 5, 5)
        Y = step2d(X, periodic=False)
        np.add.at(cnt, (X[:, 0, 2], Y[:, 1, 2], Y[:, 2, 2]), 1)
    for s in (0, 1):
        tot = int(cnt[s].sum())
        p1 = F(int(cnt[s, 1].sum()), tot); p2 = F(int(cnt[s, :, 1].sum()), tot)
        print(f"  s = {s}: P((x,1) alive at 1) = {p1} = {F(p1.numerator * (128 // p1.denominator), 128) if 128 % p1.denominator == 0 else p1}"
              f" ({p1.numerator * 128 // p1.denominator}/128), P((x,2) alive at 1) = {p2} ({p2.numerator * 256 // p2.denominator}/256), "
              f"E b_1 = {p1 + p2} ({(p1 + p2).numerator * 256 // (p1 + p2).denominator}/256)")
    assert F(int(cnt[0, 1].sum()), int(cnt[0].sum())) == F(85, 128) and F(int(cnt[0, :, 1].sum()), int(cnt[0].sum())) == F(161, 256)
    assert F(int(cnt[1, 1].sum()), int(cnt[1].sum())) == F(76, 128) and F(int(cnt[1, :, 1].sum()), int(cnt[1].sum())) == F(119, 256)
    print("  journal: 85/128, 161/256 (s = 0); 76/128, 119/256 (s = 1); 331/256, 271/256")

    section("claim 17: the Cauchy-Schwarz bound; the collision sum of the top three rows (strips, uniform soup)")
    c1 = 0.551535
    for (W, L, jmax) in [(4, 5, 8), (4, 6, 2), (5, 5, 2)]:
        n3 = 3 * L
        hist = [np.zeros(1 << n3, np.int64) for _ in range(jmax + 1)]
        hist_alive = [np.zeros(1 << n3, np.int64) for _ in range(jmax + 1)]
        sh = np.arange(n3, dtype=np.int64)
        for X in states(W * L, chunk=1 << 19):
            X = X.reshape(-1, W, L)
            for j in range(jmax + 1):
                code = (X[:, :3, :].reshape(len(X), n3).astype(np.int64) << sh).sum(axis=1)
                np.add.at(hist[j], code, 1)
                alive = X[:, 0, :].sum(axis=1) > 0
                np.add.at(hist_alive[j], code[alive], 1)
                if j < jmax:
                    X = step2d(X, True)
        # Y_1: top-three-row configurations whose row 0 is empty one generation later
        Y1 = np.zeros(1 << n3, bool)
        for U in states(n3):
            U3 = U.reshape(-1, 3, L)
            idx = (U.astype(np.int64) << sh).sum(axis=1)
            Y1[idx] = step2d(U3, True)[:, 0, :].sum(axis=1) == 0     # rows 3.. are not read by row 0
        out = []
        for j in range(1, jmax + 1):
            mu = hist[j] / hist[j].sum()
            col = float((mu ** 2).sum())
            lhs = float(mu[Y1].sum()); rhs = math.sqrt(Y1.sum() * col)
            assert lhs <= rhs + 1e-15
            mua = hist_alive[j] / hist_alive[j].sum()
            ex = math.log(8.0 ** L * col) / L
            exa = math.log(8.0 ** L * float((mua ** 2).sum())) / L
            atom = float(mu.max())
            out.append((j, ex, exa, lhs, rhs, atom))
        print(f"  strip {W} x {L}: |Y_1| = {int(Y1.sum())}")
        for j, ex, exa, lhs, rhs, atom in out:
            print(f"    j = {j}: (1/L) ln(8^L sum mu_j^2) = {ex:.3f} (living rows only: {exa:.3f}); must stay below c_1 = {c1:.3f} "
                  f"for the hypothesis; mu_j(Y_1) = {lhs:.4f} <= sqrt(|Y_1| sum mu^2) = {rhs:.4f}; heaviest atom {atom:.4f}")
    print("  journal (lab L3.5): excess 0.92-1.03 at generation 2, 1.7 at generation 8; living rows 0.64-0.73 at j = 2")

    section("claim 18: no finite pattern of the half-plane holds its cells against the outside")
    # every non-empty set P inside a 3 x 3 patch and every pattern on it; the patch at depth r0 = 0, 1, 2, 3
    done = fails = 0
    for r0 in (0, 1, 2, 3):
        Wd, Ld = r0 + 7, 11
        patch = [(r0 + i, 4 + j) for i in range(3) for j in range(3)]
        for mask in range(1, 512):
            P = [patch[t] for t in range(9) if (mask >> t) & 1]
            cmax = max(c for r, c in P)
            cell = max((r, c) for r, c in P if c == cmax)             # lowest cell of the right-most column
            nb = [(cell[0] + dr, cell[1] + dc) for dr, dc in ((0, 1), (0, -1), (0, 2), (0, -2), (1, 0), (-1, 0), (2, 0), (-2, 0))]
            nb = [q for q in nb if q[0] >= 0]
            free = [q for q in nb if q not in P]
            fixed = [q for q in nb if q in P]
            four = [(cell[0], cell[1] + 1), (cell[0], cell[1] + 2), (cell[0] + 1, cell[1]), (cell[0] + 2, cell[1])]
            assert all(q in free for q in four)
            for pat in range(1 << len(P)):
                st = {P[t]: (pat >> t) & 1 for t in range(len(P))}
                m = sum(st[q] for q in fixed)
                s = st[cell]
                # the proof's recipe
                if s == 1:
                    j = 0 if m <= 1 else 4
                else:
                    j = 3 - m if m <= 3 else 0
                x = np.zeros((1, Wd, Ld), np.int8)
                for q, val in st.items():
                    x[0, q[0], q[1]] = val
                for q in four[:j]:
                    x[0, q[0], q[1]] = 1
                y = step2d(x, periodic=False)
                done += 1
                fails += int(y[0, cell[0], cell[1]] == s)
    print(f"  {done} (set, pattern, depth) cases in a 3 x 3 patch: the cell named in the proof keeps its state in {fails} cases")
    assert fails == 0
    # control: a single row (no cells beneath): three dead cells hold against everything
    held = True
    for out in itertools.product((0, 1), repeat=4):
        x = np.zeros((1, 1, 7), np.int8)
        x[0, 0, [0, 1, 5, 6]] = out
        held &= step2d(x, periodic=False)[0, 0, 2:5].sum() == 0
    print(f"  control, a one-row vessel (no cells beneath): three dead cells stay dead against all 16 outsides: {held}")
    assert held

    section("claim 19 (Lemma 8): P_pi(T <= k) <= (1 - lam^k) pi(phi) + pi(1 - phi) <= k h + pi(1 - phi)")
    bad1 = bad2 = tests = skipped = ctrl = 0
    for trial in range(4000):
        n = int(rng.integers(1, 9))
        kind = trial % 3
        Q = rng.random((n, n)) * (rng.random((n, n)) < 0.6)
        if kind == 1:
            Q = np.triu(Q)                                            # reducible
        if kind == 2 and n > 1:
            Q[int(rng.integers(0, n))] = 0                            # a state that dies at once
        rs = Q.sum(axis=1)
        scale = np.where(rs > 0, rng.uniform(0.2, 1.0, n) / np.where(rs > 0, rs, 1), 0)
        Q = Q * scale[:, None]
        ev, vec = np.linalg.eig(Q)
        i = int(np.argmax(ev.real))
        lam = float(ev[i].real)
        phi = vec[:, i].real
        if phi.sum() < 0:
            phi = -phi
        if abs(ev[i].imag) > 1e-12 or phi.min() < -1e-9 or phi.max() <= 0 or np.abs(Q @ phi - lam * phi).max() > 1e-9:
            skipped += 1
            continue
        phi = np.clip(phi, 0, None) / phi.max()
        lam = max(lam, 0.0)
        h = 1 - lam
        pi = rng.dirichlet(np.ones(n))
        surv = np.ones(n)
        for k in range(1, 40):
            surv = Q @ surv
            p = 1 - float(pi @ surv)
            b1 = (1 - lam ** k) * float(pi @ phi) + float(pi @ (1 - phi))
            b2 = k * h + float(pi @ (1 - phi))
            tests += 1
            bad1 += p > b1 + 1e-9
            bad2 += b1 > b2 + 1e-9
            ctrl += p > k * h + 1e-9                                  # control: the doom term dropped
    print(f"  {tests} tests (irreducible, triangular, with a state that dies at once; {skipped} matrices skipped: no clean Perron vector): "
          f"first inequality fails {bad1}, second {bad2}; control without pi(1 - phi): fails {ctrl}")
    assert bad1 == 0 and bad2 == 0 and ctrl > 0
    hh, eps = F(1, 10), F(1, 7)
    for k in (1, 2, 5):
        exact = (1 - eps) * (1 - (1 - hh) ** k) + eps
        bound = (1 - (1 - hh) ** k) * (1 - eps) + eps
        assert exact == bound
    print("  smallest case (g stays with 1 - h, d dies at once): equality in the first inequality")
    # the one-row dice chain D2(L, 1/2) on a ring, from the fair product law
    print("  D2(L, 1/2) on rings (one row over fair dice), start = fair product row:")
    for L in (5, 6, 7, 8, 9, 10):
        n = 1 << L
        S = ((np.arange(n)[:, None] >> np.arange(L)) & 1).astype(np.int8)
        k = sum(np.roll(S, d, axis=1) for d in (1, 2, -1, -2))
        wt = np.array([[w1(s, kk) for kk in range(5)] for s in (0, 1)])
        pd = wt[S, k]                                                 # P(cell dead next)
        # Q[x, y] = prod_i (pd if y_i = 0 else 1 - pd)
        Q = np.ones((n, n))
        for i in range(L):
            Q *= np.where(S[None, :, i] == 0, pd[:, i][:, None], 1 - pd[:, i][:, None])
        Q = Q[1:, 1:]                                                 # living states: row 0 not empty
        ev, vec = np.linalg.eig(Q)
        i = int(np.argmax(ev.real)); lam = float(ev[i].real)
        phi = np.abs(vec[:, i].real); phi /= phi.max()
        pi = np.full(n, 1 / n)                                        # includes the dead row: phi = 0 there
        doom = float(pi[1:] @ (1 - phi)) + pi[0]
        surv = np.ones(n - 1); line = []
        for kk in range(1, 7):
            surv = Q @ surv
            p = 1 - float(pi[1:] @ surv)
            b = kk * (1 - lam) + doom
            assert p <= (1 - lam ** kk) * float(pi[1:] @ phi) + doom + 1e-12 <= b + 2e-12
            line.append(f"{p:.5f}")
        print(f"    L = {L:2d}: h = {1 - lam:.6f} (-ln h / L = {-math.log(1 - lam) / L:.3f}), pi(1 - phi) = {doom:.5f} "
              f"(-ln / L = {-math.log(doom) / L:.3f}); P(T <= k), k = 1..6: {', '.join(line)}")
    print(f"\nall assertions passed  [{time.time() - t00:.0f} s]")


if __name__ == "__main__":
    main()
