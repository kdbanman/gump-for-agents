"""Critic's lab: lab requests of probability, round 2 (exact; no sampling).

One row of cells; given the row S every cell is alive next independently with probability a[x][k], x its own state
and k the number of live cells among its in-row neighbours (y-2, y-1, y+1, y+2, as far as the vessel has them).
  D2(rho) / E1(pi): a = prob_r1.a_table(pi)        (the 2D rule over dice)
  OP5(p):           a[x][k] = p if x + k >= 1 else 0   (five-parent oriented site percolation)
Vessels: 'ring'; 'dead' (interval, nothing outside); 'refl' (interval, reflecting ends); 'mixed' (left end dead,
right end reflecting). tau = 1/(1 - lambda), lambda the Perron eigenvalue of the kernel on non-empty rows.

  python3 prob_r2.py check        the general kernel (right and left multiplication) against dense kernels built cell
                                  by cell, against prob_r1.py, and OP5 against a direct dense construction
  python3 prob_r2.py claims       Proposition W (a), (d), Lemma 3, the domination behind Theorems A and A', Proposition F's root
  python3 prob_r2.py game [m]     the local game asserted in entry 7 (claim 13), arcs of 1..m cells (default 7: 2 min; 8: 10 min)
  python3 prob_r2.py op5scan      extra: OP5(p) for p = 0.30..0.50 on rings of 9..17 cells
  python3 prob_r2.py r5 [max]     R5: OP5(1/2) on rings and dead-ended intervals of 8..max cells (default 19: 4 min)
  python3 prob_r2.py r6           R6: Proposition W in D2(L, 0.472), L = 12, 15, 18 (2 min)
  python3 prob_r2.py r7           R7: how D2 dies: the row j generations before death, ring 14, 18 and interval 14
  python3 prob_r2.py r8 [max]     R8: D2(., 0.472) with one dead and one reflecting end, M = 12..max (default 19)
  python3 prob_r2.py r9 [max]     R9: the anchor (1/2, 0, 1/2) on dead-ended and reflecting intervals, M = 8..max
State index: cell 0 is the highest bit (as in prob_r1.py).
"""
import sys, os, itertools, string
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prob_r1 as pr

D2 = (0.278784, 0.498432, 0.222784)        # Bin(2, 0.472)
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def neighbours(M, kind):
    out = []
    for y in range(M):
        v = []
        for d in (-2, -1, 1, 2):
            z = y + d
            if kind == 'ring':
                v.append(z % M)
            elif kind == 'dead':
                if 0 <= z < M: v.append(z)
            elif kind == 'refl':
                if z < 0: z = -1 - z
                if z >= M: z = 2 * M - 1 - z
                v.append(z)
            elif kind == 'mixed':
                if z < 0: continue
                if z >= M: z = 2 * M - 1 - z
                v.append(z)
        out.append(v)
    return out


def op5_table(p):
    return np.array([[0.0 if x + k == 0 else p for k in range(7)] for x in (0, 1)])


def make_ops(M, kind, a):
    """(right, left): right(f) = Q f, left(mu) = mu Q, for the full kernel Q on all 2^M rows (the empty row included)."""
    nbs = neighbours(M, kind)
    letters = string.ascii_letters
    Sl = lambda i: letters[i]; Pl = lambda i: letters[26 + i]
    factors = []; last_use = {}
    for y in range(M):
        cells = sorted(set(nbs[y]) | {y})
        W = np.zeros((2,) + (2,) * len(cells))
        for bits in itertools.product((0, 1), repeat=len(cells)):
            val = dict(zip(cells, bits))
            k = sum(val[z] for z in nbs[y])
            p = a[val[y], k]
            W[(1,) + bits] = p; W[(0,) + bits] = 1 - p
        factors.append((cells, W))
        for z in cells: last_use[z] = y

    def right(f):
        A = f.reshape((2,) * M)
        axes = [Pl(i) for i in range(M)]
        for y in range(M):
            cells, W = factors[y]
            wl = Pl(y) + ''.join(Sl(z) for z in cells)
            out = [ax for ax in axes if ax != Pl(y)]
            for z in cells:
                if Sl(z) not in out: out.append(Sl(z))
            A = np.einsum(''.join(axes) + ',' + wl + '->' + ''.join(out), A, W)
            axes = out
        return np.einsum(''.join(axes) + '->' + ''.join(Sl(i) for i in range(M)), A).reshape(-1)

    def left(mu):
        A = mu.reshape((2,) * M)
        axes = [Sl(i) for i in range(M)]
        for y in range(M):
            cells, W = factors[y]
            wl = Pl(y) + ''.join(Sl(z) for z in cells)
            out = [ax for ax in axes if not (ax in [Sl(z) for z in cells if last_use[z] == y])] + [Pl(y)]
            A = np.einsum(''.join(axes) + ',' + wl + '->' + ''.join(out), A, W)
            axes = out
        return np.einsum(''.join(axes) + '->' + ''.join(Pl(i) for i in range(M)), A).reshape(-1)
    return right, left


def dense(M, kind, a):
    nbs = neighbours(M, kind)
    Q = np.zeros((1 << M, 1 << M))
    for S in range(1 << M):
        bits = [(S >> (M - 1 - i)) & 1 for i in range(M)]
        p = [a[bits[y], sum(bits[z] for z in nbs[y])] for y in range(M)]
        for T in range(1 << M):
            w = 1.0
            for y in range(M):
                w *= p[y] if (T >> (M - 1 - y)) & 1 else 1 - p[y]
            Q[S, T] = w
    return Q


def perron_right(M, kind, a, iters=3000, tol=1e-14):
    """lambda and the right eigenvector r on non-empty rows (r[0] = 0), normalised to max 1."""
    right, _ = make_ops(M, kind, a)
    f = np.ones(1 << M); f[0] = 0.0
    lam = 0.0
    for it in range(iters):
        g = right(f); g[0] = 0.0
        l2 = g.max(); g /= l2
        if it > 10 and abs(l2 - lam) < tol:
            f, lam = g, l2; break
        f, lam = g, l2
    g = right(f); g[0] = 0.0
    lam = float(g.sum() / f.sum())
    return lam, f


def perron_left(M, kind, a, iters=3000, tol=1e-15):
    """lambda and the quasi-stationary law mu (mu[0] = 0, sum 1)."""
    _, left = make_ops(M, kind, a)
    mu = np.ones(1 << M); mu[0] = 0.0; mu /= mu.sum()
    lam = 0.0
    for it in range(iters):
        nu = left(mu); nu[0] = 0.0
        l2 = nu.sum(); nu /= l2
        if it > 10 and abs(l2 - lam) < tol:
            mu, lam = nu, l2; break
        mu, lam = nu, l2
    return float(lam), mu


def lntau(M, kind, a):
    lam, _ = perron_right(M, kind, a)
    return float(-np.log(1 - lam))


def popcount(M):
    S = np.arange(1 << M)
    pop = np.zeros(1 << M, np.int64)
    for i in range(M): pop += (S >> i) & 1
    return pop


def checks():
    a2 = pr.a_table(D2)
    for kind in ('ring', 'dead', 'refl', 'mixed'):
        M = 7
        Q = dense(M, kind, a2)
        right, left = make_ops(M, kind, a2)
        x = np.random.default_rng(0).random(1 << M)
        check(np.abs(right(x) - Q @ x).max() < 1e-13 and np.abs(left(x) - x @ Q).max() < 1e-13 and abs(Q.sum(1) - 1).max() < 1e-13,
              f"{kind}, {M} cells: right and left multiplication agree with the dense kernel built cell by cell")
        lam = max(np.linalg.eigvals(Q[1:, 1:]).real)
        check(abs(lntau(M, kind, a2) + np.log(1 - lam)) < 1e-9 and abs(perron_left(M, kind, a2)[0] - lam) < 1e-10,
              f"   ln tau = {-np.log(1 - lam):.6f} by the dense eigenvalue, by right and by left power iteration")
    for kind, M, want in (('ring', 12, 6.4169), ('dead', 10, 6.7641), ('refl', 10, 5.9342)):
        v = lntau(M, kind, a2)
        check(abs(v - want) < 6e-5 and abs(v - pr.lntau(M, kind, D2)[0]) < 1e-8, f"D2(0.472), {kind} of {M}: ln tau = {v:.4f} (board: {want}; prob_r1.py: the same)")
    # the mixed interval of M cells is the dead-ended interval of 2M cells with mirror-symmetric rows and mirrored dice
    M = 5; nb2 = neighbours(2 * M, 'dead')
    Qs = np.zeros((1 << M, 1 << M))
    for S in range(1 << M):
        bits = [(S >> (M - 1 - i)) & 1 for i in range(M)]
        full = bits + bits[::-1]
        p = [a2[full[y], sum(full[z] for z in nb2[y])] for y in range(M)]
        for T in range(1 << M):
            w = 1.0
            for y in range(M):
                w *= p[y] if (T >> (M - 1 - y)) & 1 else 1 - p[y]
            Qs[S, T] = w
    lam = max(np.linalg.eigvals(Qs[1:, 1:]).real)
    check(abs(lntau(M, 'mixed', a2) + np.log(1 - lam)) < 1e-9, f"mixed ends, {M} cells = mirror-symmetric rows of the dead-ended interval of {2 * M}: ln tau = {-np.log(1 - lam):.6f}")
    # OP5 directly: a cell is alive next with probability p iff some cell within distance 2 (itself included) is alive
    for kind in ('ring', 'dead'):
        M = 7; p = 0.5
        Q = np.zeros((1 << M, 1 << M))
        for S in range(1 << M):
            bits = [(S >> (M - 1 - i)) & 1 for i in range(M)]
            reach = []
            for y in range(M):
                zs = [(y + d) % M for d in range(-2, 3)] if kind == 'ring' else [y + d for d in range(-2, 3) if 0 <= y + d < M]
                reach.append(any(bits[z] for z in zs))
            for T in range(1 << M):
                tb = [(T >> (M - 1 - i)) & 1 for i in range(M)]
                if any(t and not r for t, r in zip(tb, reach)): continue
                Q[S, T] = p ** sum(reach)
        Qg = dense(M, kind, op5_table(p))
        check(np.abs(Q - Qg).max() < 1e-14, f"OP5(1/2), {kind} of {M}: the table a[x][k] = p*[x + k >= 1] reproduces the direct construction")


def claims():
    """numerical checks of the statements probability tags as proved in round 2."""
    a2 = pr.a_table(D2)
    # Proposition W (a): Q_ring(S, S') = w(S) Q_dead(S, S') for S, S' inside A = ring minus four adjacent cells
    L = 10; M = L - 4
    Qr = dense(L, 'ring', a2); Qd = dense(M, 'dead', a2)
    u = {(0, 0): 1.0, (0, 1): 1 - D2[2], (1, 0): (1 - D2[2]) ** 2, (1, 1): D2[0] * (1 - D2[2])}
    worst = 0.0; wvals = set()
    for S in range(1, 1 << M):                           # ring cells 0..3 = G (dead), cells 4..L-1 = A = interval cells 0..M-1
        bits = [(S >> (M - 1 - i)) & 1 for i in range(M)]
        w = u[(bits[0], bits[1])] * u[(bits[M - 1], bits[M - 2])]
        wvals.add(round(w, 12))
        worst = max(worst, float(np.abs(Qr[S, : 1 << M] - w * Qd[S]).max()))
    check(worst < 1e-14 and abs(min(wvals) - (D2[0] * (1 - D2[2])) ** 2) < 1e-12,
          f"Proposition W(a), ring of {L} against the dead-ended interval of {M}: Q_ring(S, S') = w(S) Q_dead(S, S') for all 2^{M} - 1 rows S and all S' "
          f"(max error {worst:.1e}); smallest w = {min(wvals):.6f} = [pi_0 (1 - pi_2)]^2")
    # (d): the same for the reflecting interval of M + 4 cells with its two outer cells at each end dead
    Qf = dense(M + 4, 'refl', a2)
    worst = 0.0
    for S in range(1, 1 << M):
        bits = [(S >> (M - 1 - i)) & 1 for i in range(M)]
        w = u[(bits[0], bits[1])] * u[(bits[M - 1], bits[M - 2])]
        Sf = S << 2                                       # cells 0, 1 and M+2, M+3 dead
        idx = np.arange(1 << M) << 2
        worst = max(worst, float(np.abs(Qf[Sf, idx] - w * Qd[S]).max()))
    check(worst < 1e-14, f"Proposition W(d), reflecting interval of {M + 4}: the same identity with the same w (max error {worst:.1e})")
    # Lemma 3: d + Q g <= a g + eps at every living state implies 1 - lambda <= eps. Tried on D2 (ring of 9) with many g.
    L = 9
    Q = dense(L, 'ring', a2)
    lam = max(np.linalg.eigvals(Q[1:, 1:]).real)
    d = Q[1:, 0]; Qt = Q[1:, 1:]
    pop = popcount(L)[1:]
    rng = np.random.default_rng(0)
    n_ok = n_app = 0; best = 1.0
    for trial in range(400):
        if trial < 100:
            g = rng.uniform(0.2, 1.0) ** pop * rng.uniform(0.5, 1.0)
        elif trial < 200:
            g = rng.random(len(pop))
        else:
            g = np.clip(rng.uniform(0.3, 0.9) ** np.minimum(pop, rng.integers(1, L)) + 0.05 * rng.standard_normal(len(pop)), 0, 1)
        for a in (0.2, 0.5, 0.8, 0.95):
            eps = float(np.max(d + Qt @ g - a * g))
            if eps >= 0 and a + eps < 1:
                n_app += 1; n_ok += (1 - lam <= eps + 1e-12); best = min(best, eps)
    check(n_app > 0 and n_ok == n_app, f"Lemma 3 on D2(9, 0.472): in all {n_app} cases (random g, four values of a) where a + eps < 1, 1 - lambda = {1 - lam:.5f} <= eps "
                                       f"(smallest eps met: {best:.5f})")
    # Theorem A' / Lemma 1(d): the row dominates OP5(p), p = min(pi_0, pi_2): survival from the full row, exactly
    for pi, name in (((0.5, 0.0, 0.5), 'anchor'), (D2, 'Bin(2, 0.472)')):
        L = 10; p = min(pi[0], pi[2])
        r1, _ = make_ops(L, 'ring', pr.a_table(pi)); r2, _ = make_ops(L, 'ring', op5_table(p))
        f1 = np.zeros(1 << L); f1[0] = 1.0; f2 = f1.copy()
        okk = True; ex = []
        for t in range(1, 41):
            f1 = r1(f1); f2 = r2(f2)                      # P_S(T <= t)
            okk &= bool(np.all(f1[1:] <= f2[1:] + 1e-12))
            if t in (5, 20, 40): ex.append((t, 1 - f1[-1], 1 - f2[-1]))
        check(okk, f"domination by OP5({p:.4f}), ring of {L}, {name}: P_S(T > t) of the edge >= that of the percolation for every start S and t <= 40; from the full row: " +
              ', '.join(f"t = {t}: {x:.4f} >= {y:.4f}" for t, x, y in ex))
    b = (0.5 + np.sqrt(0.25 + 1.0)) / 1.0
    check(abs(np.log(b) - 0.481212) < 1e-6 and abs(0.5 * b * b - 0.5 * b - 0.5) < 1e-12, f"Proposition F: beta*(1/2) = {b:.6f} is the root of q b^2 - p b - p, ln = {np.log(b):.4f}")


def forced(n_out):
    """for every row c on n_out + 4 cells: for its inner n_out cells (two cells dropped at each end), the mask of
    cells whose next state does not depend on b ((live, k = 2): alive; (dead, k = 0): dead) and their forced values."""
    n = n_out + 4
    C = np.arange(1 << n, dtype=np.int64)
    bit = lambda i: (C >> i) & 1
    F = np.zeros(1 << n, np.int64); V = np.zeros(1 << n, np.int64)
    for j in range(n_out):
        i = j + 2
        k = bit(i - 2) + bit(i - 1) + bit(i + 1) + bit(i + 2)
        fa = (bit(i) == 1) & (k == 2); fd = (bit(i) == 0) & (k == 0)
        F |= (fa | fd).astype(np.int64) << j
        V |= fa.astype(np.int64) << j
    return F, V


def exists(G, F, V, chunk=2048):
    """for every row c: is there x with G[x] and (x & F[c]) == V[c]?"""
    X = np.flatnonzero(G).astype(np.int64)
    out = np.zeros(len(F), bool)
    for lo in range(0, len(F), chunk):
        f = F[lo:lo + chunk, None]; v = V[lo:lo + chunk, None]
        out[lo:lo + chunk] = ((X[None, :] & f) == v).any(1)
    return out


def game(mmax=7):
    print("the local three-move game behind claim 13: an arc of m cells inside any row. We choose b on the arc and the cells that can reach it (4, 2, 0 cells on")
    print("each side at the three steps); the row beyond six cells from the arc is arbitrary and cannot reach the arc in three generations.")
    for m in range(1, mmax + 1):
        F2, V2 = forced(m)                               # rows on m + 4 cells: which arc cells are forced
        G2 = (F2 & V2) == 0                              # no arc cell is live with exactly two live neighbours: the arc can be emptied next
        F1, V1 = forced(m + 4)                           # rows on m + 8 cells
        G1 = exists(G2, F1, V1)                          # ... from which the arc can be emptied in two generations
        F0, V0 = forced(m + 8)                           # rows on m + 12 cells
        G0 = exists(G1, F0, V0)                          # ... in three
        bad = int((~G0).sum()); two = int((~G1).sum())
        ex = ''
        if two:
            c = int(np.flatnonzero(~G1)[0])
            ex = "; e.g. " + format(c, f'0{m + 8}b')[::-1] + " (arc = the middle " + str(m) + " cells)"
        check(bad == 0, f"m = {m}: every one of the 2^{m + 12} rows on the arc and six cells each side can be steered so that the arc is empty three generations later "
                        f"(failures: {bad}); two generations do not suffice for {two} of the 2^{m + 8} rows on the arc and four cells each side{ex}", )
    print("   so an arc of m cells (m as checked) is empty three generations later with probability >= p^(3m+12), p = min(pi_0, pi_2), whatever the row")


def op5scan(mx=17):
    print("extra (not requested): OP5(p) on the ring, steps of ln tau, for a rough location of its critical density (lower bound proved by probability: 1/3)")
    for p in (0.30, 0.34, 0.38, 0.42, 0.46, 0.50):
        a = op5_table(p)
        vals = [lntau(M, 'ring', a) for M in range(9, mx + 1)]
        print(f"   p = {p:.2f}: ln tau at L = {mx}: {vals[-1]:.4f}; steps L = 10..{mx}: " + ' '.join(f"{y - x:.4f}" for x, y in zip(vals, vals[1:])) +
              f";  step x L at the last three: " + ' '.join(f"{(vals[i] - vals[i - 1]) * (9 + i):.2f}" for i in (-3, -2, -1)).replace('  ', ' '), flush=True)


def r5(mx=19):
    print("R5. OP5(1/2): every cell within distance 2 of a live cell is alive next with probability 1/2; ln tau and steps")
    a = op5_table(0.5)
    print("    cells   ring     step     interval  step     ring - interval")
    pr_, pd = None, None
    for M in range(8, mx + 1):
        g = lntau(M, 'ring', a); d = lntau(M, 'dead', a)
        st = lambda v, q: '       ' if q is None else f"{v - q:7.4f}"
        print(f"    {M:3d}   {g:8.4f} {st(g, pr_)}   {d:8.4f} {st(d, pd)}   {g - d:+.4f}", flush=True)
        pr_, pd = g, d
    print("    Proposition F: the steps must end at or below ln((1 + sqrt 5)/2) = 0.4812; attractiveness: ring >= interval")


def r6():
    print("R6. Proposition W in D2(L, 0.472): nu = the ring's quasi-stationary law restricted to rows whose cells 1-4 are dead")
    a2 = pr.a_table(D2)
    wmin = (D2[0] * (1 - D2[2])) ** 2
    for L in (12, 15, 18):
        lam_r, mu = perron_left(L, 'ring', a2)
        M = L - 4
        nu = mu[: 1 << M].copy()                       # cells 0..3 (the four highest bits) dead; the rest is the interval
        mG = float(nu.sum())
        lam_d, _ = perron_right(M, 'dead', a2)
        hd = 1 - lam_d; hr = 1 - lam_r
        _, left = make_ops(M, 'dead', a2)
        cur = nu.copy(); cur[0] = 0.0
        N = [float(cur.sum())]; dth = []
        for n in range(0, 16):
            nxt = left(cur)
            dth.append(float(nxt[0])); nxt[0] = 0.0
            cur = nxt; N.append(float(cur.sum()))
        rho = [dth[n] / (hd * N[n]) for n in range(16)]
        # the proposition's inequality (b): h_r >= wmin^(n+1) P_nu(T_d = n + 1)
        okb = all(hr >= wmin ** (n + 1) * dth[n] * (1 - 1e-9) for n in range(16))
        check(okb, f"L = {L}: inequality (b) h_ring >= w_min^(n+1) P_nu(T_d = n+1) holds for n = 0..15 (w_min = {wmin:.4f})")
        print(f"   L = {L}: m_G = {mG:.4e} (-ln m_G / 4 = {-np.log(mG) / 4:.3f} per cell); h_ring = {hr:.4e}; h_dead(L-4) = {hd:.4e}; ln(h_ring/h_dead) = {np.log(hr / hd):+.3f}")
        print("        N_n / m_G, n = 0..10: " + ' '.join(f"{N[n] / mG:.4f}" for n in range(11)))
        print("        rho_n,      n = 0..15: " + ' '.join(f"{r:.3g}" for r in rho))
        first = next((n for n in range(16) if rho[n] >= 0.5), None)
        best = max(range(16), key=lambda n: wmin ** (n + 1) * dth[n])
        print(f"        rho_n >= 1/2 first at n = {first}; the best lower bound of (b) is at n = {best}: ln[w_min^(n+1) P(T_d = n+1) / h_ring] = "
              f"{np.log(wmin ** (best + 1) * dth[best] / hr):+.2f}", flush=True)


def longest_dead_arc(L):
    """for every row of a ring of L cells (index: cell 0 = highest bit): length of the longest run of dead cells (cyclic)."""
    S = np.arange(1 << L, dtype=np.int64)
    dead = ((~S) & ((1 << L) - 1))
    best = np.zeros(1 << L, np.int64)
    cur = dead.copy()
    for n in range(1, L + 1):
        best[cur != 0] = n
        rot = ((dead << n) | (dead >> (L - n))) & ((1 << L) - 1)
        cur = cur & rot
    return best


def wall_gaps(M):
    """for every row of an interval of M cells: dead cells before the first live cell and after the last one."""
    S = np.arange(1 << M, dtype=np.int64)
    lead = np.full(1 << M, M, np.int64); trail = np.full(1 << M, M, np.int64)
    for i in range(M - 1, -1, -1):                     # cell i = bit M-1-i
        lead[(S >> (M - 1 - i)) & 1 == 1] = i
    for i in range(M):
        trail[(S >> (M - 1 - i)) & 1 == 1] = M - 1 - i
    return lead, trail


def r7():
    print("R7. how D2(0.472) dies: the row j generations before its death, law P(S) ~ mu(S) P_S(T = j)")
    a2 = pr.a_table(D2)
    for kind, M in (('ring', 14), ('ring', 18), ('dead', 14), ('dead', 18)):
        lam, mu = perron_left(M, kind, a2)
        right, _ = make_ops(M, kind, a2)
        pop = popcount(M)
        f = np.zeros(1 << M); f[0] = 1.0
        prev = f.copy()
        stats = {}
        if kind == 'ring':
            arc = longest_dead_arc(M)
        else:
            lead, trail = wall_gaps(M)
        for j in range(1, 13):
            f = right(f)                               # P_S(T <= j)
            g = (f - prev); g[0] = 0.0; prev = f.copy()   # P_S(T = j) for S non-empty
            w = mu * g; z = w.sum(); w /= z
            row = [float((w * pop).sum())]
            if kind == 'ring':
                row.append(float((w * arc).sum()))
            else:
                row += [float((w * (lead + trail)).sum()), float((w * np.maximum(lead, trail)).sum()), float((w * np.minimum(lead, trail)).sum())]
            stats[j] = row
        base = [float((mu * pop).sum())] + ([float((mu * arc).sum())] if kind == 'ring' else
                                            [float((mu * (lead + trail)).sum()), float((mu * np.maximum(lead, trail)).sum()), float((mu * np.minimum(lead, trail)).sum())])
        js = (1, 2, 3, 4, 6, 8, 12)
        name = f"ring of {M}" if kind == 'ring' else f"dead-ended interval of {M}"
        print(f"   {name} (ln tau = {-np.log(1 - lam):.4f}); j = " + ', '.join(str(j) for j in js) + "; then the quasi-stationary mean")
        print("        mean population:               " + ' '.join(f"{stats[j][0]:6.2f}" for j in js) + f"   | {base[0]:6.2f}")
        if kind == 'ring':
            print("        mean longest dead arc:         " + ' '.join(f"{stats[j][1]:6.2f}" for j in js) + f"   | {base[1]:6.2f}")
        else:
            print("        dead cells at the two walls:   " + ' '.join(f"{stats[j][1]:6.2f}" for j in js) + f"   | {base[1]:6.2f}   (sum of the two gaps)")
            print("        the larger of the two gaps:    " + ' '.join(f"{stats[j][2]:6.2f}" for j in js) + f"   | {base[2]:6.2f}")
            print("        the smaller of the two gaps:   " + ' '.join(f"{stats[j][3]:6.2f}" for j in js) + f"   | {base[3]:6.2f}", flush=True)


def r8(mx=19):
    print("R8. D2(., 0.472) on an interval with one dead and one reflecting end; exam entry P-E2 says: the mean of the two pure cases")
    a2 = pr.a_table(D2)
    for M in range(12, mx + 1):
        m = lntau(M, 'mixed', a2); d = lntau(M, 'dead', a2); r = lntau(M, 'refl', a2)
        print(f"    M = {M}: mixed {m:.4f}; dead {d:.4f}; reflecting {r:.4f}; mean of the two {0.5 * (d + r):.4f}; mixed - mean = {m - 0.5 * (d + r):+.4f}", flush=True)


def r9(mx=19):
    print("R9. the anchor (1/2, 0, 1/2) on dead-ended and reflecting intervals (ring for comparison, board L4.1: steps 0.685..0.671 at L = 15..18)")
    a = pr.a_table((0.5, 0.0, 0.5))
    pd = prf = None
    for M in range(8, mx + 1):
        d = lntau(M, 'dead', a); r = lntau(M, 'refl', a)
        st = lambda v, q: '       ' if q is None else f"{v - q:7.4f}"
        print(f"    M = {M}: dead {d:8.4f} {st(d, pd)}   reflecting {r:8.4f} {st(r, prf)}   dead - reflecting {d - r:+.4f}", flush=True)
        pd, prf = d, r


if __name__ == '__main__':
    what = sys.argv[1]
    arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
    if what == 'check': checks()
    elif what == 'claims': claims()
    elif what == 'game': game(arg or 7)
    elif what == 'op5scan': op5scan(arg or 17)
    elif what == 'r5': r5(arg or 19)
    elif what == 'r6': r6()
    elif what == 'r7': r7()
    elif what == 'r8': r8(arg or 19)
    elif what == 'r9': r9(arg or 19)
    print('ALL OK' if OK else 'SOMETHING FAILED')
