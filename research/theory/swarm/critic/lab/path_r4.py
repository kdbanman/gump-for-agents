"""Critic's lab: path, round 4 (entries 16-21). Exact computations and arithmetic on the curated tallies
(data/fluct_tables.npz: pooled one-step tables of the face population of gump hulls, A = 30, 45, 63, 84; no new runs).

  python3 path_r4.py props   Propositions T', T, the cases of 17.4, Lemma C: worked cases and random tables
  python3 path_r4.py lr9     LR9: per row and size, mean, variance, third cumulant of the step, against k/A; block minima of the
                             roots; where the roots start to decrease; what Theorem Q gives on each table and what it loses
  python3 path_r4.py lr10    LR10: (a) path's bellman.py on every row's root and variance; (b) the recursion with each row's own
                             rate (Cramer transform of the row), on a grid of 1/4 cell, rising steps allowed
  python3 path_r4.py lr11    LR11: the committor of the m-fold extensive chain built from one table, m = 1, 2, 4, 8, 16
  python3 path_r4.py lr12    LR12 and Lemma F: sealed sets of face12e slabs (integer programme), walls 3 x 3 and 4 x 4, 2-4 cubes deep
  python3 path_r4.py fits    arithmetic of entry 16.1 (ring minus anchored row against ln L and against L)
  python3 path_r4.py limit   path's check_limit.py redone with a cancellation-free solver (is 'exact linear algebra' exact at e^-286?)
  python3 path_r4.py all
"""
import sys, os, json, itertools, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import path_r2 as q2
import path_r3 as q3

AREA = q2.AREA
PATHDIR = os.path.normpath(os.path.join(HERE, '..', '..', 'path'))
SCRATCH = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'scratch', 'critic'))
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ------------------------------------------------------------------------------------------------ tools
def committor_pos(T, d, tol=1e-13, itmax=200000):
    """smallest non-negative solution of psi = d + T psi by elimination without pivoting (I - T is an M-matrix: the only
    subtraction is on the diagonal, which stays >= the exit probability), so that tiny entries keep their relative accuracy."""
    n = len(d)
    A = np.eye(n) - T; b = d.astype(float).copy()
    A = A.copy()
    for i in range(n):
        piv = A[i, i]
        f = A[i + 1:, i] / piv
        A[i + 1:, i:] -= f[:, None] * A[i, i:][None, :]
        b[i + 1:] -= f * b[i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


def theta_of_row(row, k, smax=40.0):
    """theta = max{s >= 0 : M(s) <= 1}, M(s) = sum_k' row[k'] exp(-s (k' - k)); 0 if the mean step is <= 0 (row sum 1)."""
    step = (np.arange(len(row)) - k).astype(float)
    M = lambda s: float((row * np.exp(-s * step)).sum())
    if not (row[:k] > 0).any():
        return np.inf
    if M(1e-9) > 1: return 0.0
    lo, hi = 0.0, 1.0
    while M(hi) <= 1 and hi < smax: hi *= 2
    if M(hi) <= 1: return np.inf
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if M(mid) <= 1: lo = mid
        else: hi = mid
    return lo


def roots(Tb, KM):
    return np.array([np.nan] + [theta_of_row(Tb[k], k) for k in range(1, KM)])


# ------------------------------------------------------------------------------------------------ props
def props():
    print("Proposition T' (block bound), Proposition T (root sum), 17.4 (a)-(c), Lemma C")
    # worked cases of the journal
    T = np.zeros((4, 4)); T[1, 0] = .25; T[1, 2] = .75; T[2, 1] = .25; T[2, 3] = .75
    psi = committor_pos(T[1:3, 1:3], T[1:3, 0])
    check(abs(psi[1] - 1 / 13) < 1e-14 and abs(theta_of_row(T[1], 1) - np.log(3)) < 1e-9, "walk on {0..3}, up 3/4: psi*(2) = 1/13, theta = ln 3; T' gives 1/9 >= 1/13; T gives 2/27 <= 1/13")
    T = np.zeros((3, 5)); T[1, 0] = .2; T[1, 2] = .8; T[2, 0] = .09; T[2, 2] = .42; T[2, 4] = .49
    psi = committor_pos(T[1:3, 1:3], T[1:3, 0])
    t1, t2 = theta_of_row(T[1], 1), theta_of_row(T[2], 2)
    check(abs(psi[1] - 0.09 / 0.58) < 1e-14 and abs(t1 - np.log(4)) < 1e-9 and abs(t2 - np.log(7 / 3)) < 1e-9 and 2 * t2 < -np.log(psi[1]) < t1 + t2,
          f"17.4 (c): theta = {t1:.3f}, {t2:.3f}; block bound {2 * t2:.3f} < -ln psi*(2) = {-np.log(psi[1]):.3f} < root sum {t1 + t2:.3f}")
    q = 1 / 3
    check(abs(1 / 16 + 6 / 16 * q ** 2 + 9 / 16 * q ** 4 - q ** 2) < 1e-15, "17.4 (b): offspring 0 or 2 with probabilities 1/4, 3/4: q = 1/3 and q^2 is harmonic from two cells")
    rng = np.random.default_rng(7)
    # random tables: rows k = 1..K-1 on {0..K+J}; with and without censoring
    nT = nTl = 0; worstT1 = -np.inf; worstT = -np.inf
    for trial in range(4000):
        K = int(rng.integers(3, 12)); J = int(rng.integers(1, 6)); W = K + J
        Tb = np.zeros((K, W + 1))
        for k in range(1, K):
            lo = max(0, k - int(rng.integers(1, 5))); hi = min(W, k + int(rng.integers(1, 6)))
            w = rng.random(hi - lo + 1) * (rng.random(hi - lo + 1) < 0.8) + 1e-3
            w[: k - lo] *= rng.random() * 0.7                        # bias upward so that roots exist
            Tb[k, lo:hi + 1] = w / w.sum() * (1 - 0.1 * rng.random() * (trial % 2))
        th = roots(Tb, K)
        psi = np.concatenate([[1.0], committor_pos(Tb[1:K, 1:K], Tb[1:K, 0])])     # psi[k], k = 0..K-1
        # T': any block
        k0 = int(rng.integers(0, K - 1))
        blk = [th[k] for k in range(max(k0, 1), K)]
        th0 = min(blk)
        if np.isfinite(th0):
            for k in range(1, K):
                worstT1 = max(worstT1, np.log(psi[k]) + th0 * max(k - k0, 0)); nT += 1
        # T: k0 >= 1, s_k = max_{k <= j < K} theta_j, needs finite roots
        k0 = int(rng.integers(1, K))
        s = np.array([np.nan] * K)
        run = 0.0
        for k in range(K - 1, k0 - 1, -1):
            run = max(run, th[k]); s[k] = run
        if np.isfinite(s[k0]) and trial % 2 == 0:                   # no censoring: every state leaves the block with probability one
            S = np.zeros(K + 1)
            for k in range(k0 + 1, K): S[k] = S[k - 1] + s[k]
            S[K] = S[K - 1] + s[K - 1]
            c0 = np.exp(-s[k0] * k0) * psi[:k0].min()
            for k in range(k0, K):
                lower = c0 * (np.exp(-S[k]) - np.exp(-S[K]))
                worstT = max(worstT, lower / psi[k]); nTl += 1
    check(worstT1 <= 1e-9, f"T': psi*(k) <= exp(-theta0 (k - k0)^+) in {nT:,} cases on 4,000 random tables (half of them with censored mass); largest ln(psi*/bound) = {worstT1:.2e}")
    check(worstT <= 1 + 1e-9, f"T: psi*(k) >= c0 (e^-S(k) - e^-S(K)) in {nTl:,} cases on 2,000 random tables; largest bound/psi* = {worstT:.6f}")
    # 17.4 (a): skip-free rows
    worst_lo = np.inf; worst_hi = 0
    for trial in range(2000):
        K = int(rng.integers(3, 30))
        dn = rng.random(K) * 0.3 + 0.01; up = dn / (rng.random(K) * 0.9 + 0.05); tot = np.maximum(dn + up, 1.0); dn, up = dn / tot, up / tot
        Tb = np.zeros((K, K + 1))
        for k in range(1, K): Tb[k, k - 1] = dn[k]; Tb[k, k + 1] = up[k]; Tb[k, k] = 1 - dn[k] - up[k]
        psi = committor_pos(Tb[1:K, 1:K], Tb[1:K, 0])
        r = dn[1:K] / up[1:K]; rbar = r.max(); pi_ = np.cumprod(r)
        if rbar >= 1: continue
        ratio = psi / pi_
        worst_lo = min(worst_lo, (ratio / (1 - rbar)).min()); worst_hi = max(worst_hi, (ratio * (1 - rbar)).max())
        thk = np.array([theta_of_row(Tb[k], k) for k in range(1, K)])
        if np.abs(np.exp(-thk) - r).max() > 1e-7: check(False, "skip-free row: exp(-theta_k) != d_k/u_k")
    check(worst_lo >= 1 - 1e-9 and worst_hi <= 1 + 1e-9, f"17.4 (a), 2,000 random skip-free chains: (1 - rbar) pi_k <= psi*(k) <= pi_k / (1 - rbar)  (extremes {worst_lo:.4f}, {worst_hi:.4f} of the allowed range)")
    # Lemma C: q monotone, pooled rows dominate q's rows (censored mass at infinity)
    worst = -np.inf; n = 0; nonmono_fail = 0
    for trial in range(3000):
        K = int(rng.integers(3, 12)); W = K + 4
        # monotone kernel: rows as sorted quantile functions of increasing laws
        base = np.sort(rng.random((K, 6)) * (W + 1), axis=1)
        shift = np.cumsum(rng.random(K) * 1.5)
        q = np.zeros((K, W + 2))                                     # last column: 'K or more / infinity'
        for k in range(1, K):
            pts = np.clip(np.floor(base[0] * 0.5 + shift[k] - 1.0), 0, W + 1).astype(int)
            for pnt in pts: q[k, pnt] += 1 / 6
        cdfq = np.cumsum(q, axis=1)
        mono = all((cdfq[k + 1] <= cdfq[k] + 1e-12).all() for k in range(1, K - 1))
        if not mono: nonmono_fail += 1; continue
        # pooled table dominating q: move each atom up by a random amount (possibly to infinity = censored)
        Tp = np.zeros_like(q)
        for k in range(1, K):
            for j in np.flatnonzero(q[k]):
                parts = rng.dirichlet(np.ones(3)) * q[k, j]
                for part in parts:
                    Tp[k, min(W + 1, j + int(rng.integers(0, 4)))] += part
        psi_q = committor_pos(q[1:K, 1:K], q[1:K, 0]); psi_p = committor_pos(Tp[1:K, 1:K], Tp[1:K, 0])
        sup = Tp[1:K, 0] + Tp[1:K, 1:K] @ psi_q - psi_q
        worst = max(worst, sup.max(), (psi_p - psi_q).max()); n += 1
        if (np.diff(psi_q) > 1e-12).any(): check(False, "psi_q not non-increasing")
    check(worst <= 1e-12 and n > 1000, f"Lemma C on {n:,} random monotone kernels q with a dominating pooled table (censoring included): psi_q is non-increasing, a supersolution, and psi* <= psi_q (largest excess {worst:.1e})")
    # the hypothesis 'monotone' is needed: a two-row example
    # the hypothesis 'rows of q non-decreasing' is needed: K = 3, q(1, .) = 0.99 d_1 + 0.01 d_3, q(2, .) = 0.9 d_0 + 0.1 d_3
    q = np.zeros((3, 4)); q[1] = [0.0, 0.99, 0.0, 0.01]; q[2] = [0.9, 0.0, 0.0, 0.1]
    Tp = np.zeros((3, 4)); Tp[1] = [0.0, 0.0, 0.99, 0.01]; Tp[2] = [0.9, 0.0, 0.0, 0.1]      # row 1 moved up: dominates q's row 1
    pq = committor_pos(q[1:3, 1:3], q[1:3, 0]); pp = committor_pos(Tp[1:3, 1:3], Tp[1:3, 0])
    check(pq[0] < 1e-12 and abs(pp[0] - 0.891) < 1e-12, f"Lemma C needs the monotone rows: q(1,.) = 0.99 d_1 + 0.01 d_3, q(2,.) = 0.9 d_0 + 0.1 d_3 (row 2 below row 1); the table with row 1 moved to 2 dominates q row by row and has psi*(1) = {pp[0]:.3f} > psi_q(1) = {pq[0]:.3f}")


# ------------------------------------------------------------------------------------------------ LR9
def stats(Tb, KM):
    out = np.full((KM, 4), np.nan)
    for k in range(1, KM):
        step = np.arange(Tb.shape[1]) - k
        m = float((Tb[k] * step).sum()); c2 = float((Tb[k] * (step - m) ** 2).sum()); c3 = float((Tb[k] * (step - m) ** 3).sum())
        out[k] = (m, c2, c3, Tb[k, 0])
    return out


def lr9():
    print("LR9. Pooled one-step table of the face population (rows k < A/2): step statistics per cell against x = k/A; the roots")
    data = {}
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        data[A] = (Tr, N, Tb, KM, stats(Tb, KM), roots(Tb, KM))
    xs = (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45)
    def at(arr, A, x):
        k = x * A; lo = int(np.floor(k))
        if lo < 1 or lo + 1 >= len(arr) or np.isnan(arr[lo]) or np.isnan(arr[lo + 1]): return np.nan
        return arr[lo] + (k - lo) * (arr[lo + 1] - arr[lo])
    for name, col, scale in (("mean step / A", 0, 1), ("variance of the step / A", 1, 1), ("third cumulant / A", 2, 1)):
        print(f"   {name} at x = " + ', '.join(f"{x:.2f}" for x in xs))
        for A in (30, 45, 63, 84):
            st = data[A][4]
            print(f"      A = {A}: " + ' '.join(f"{at(st[:, col], A, x) / A:8.4f}" for x in xs))
    print("   variance / mean population k (variance per live cell) at the same x")
    for A in (30, 45, 63, 84):
        st = data[A][4]
        print(f"      A = {A}: " + ' '.join(f"{at(st[:, 1], A, x) / (x * A):8.4f}" for x in xs))
    print("   root theta at the same x (lab L9.1 gave x >= 0.10)")
    for A in (30, 45, 63, 84):
        print(f"      A = {A}: " + ' '.join(f"{at(data[A][5], A, x):8.4f}" for x in xs))
    print("   rows: k, exposure N_k, theta_k for A = 84 (k = 1..12)")
    Tr, N, Tb, KM, st, th = data[84]
    print("      " + ' '.join(f"{k}:{int(N[k])}:{th[k]:.3f}" for k in range(1, 13)))
    print("   block minima min_{k0 <= k < 0.35 A} theta_k, the row where it is attained, and the first row from which theta is non-increasing up to the last tallied row")
    for A in (30, 45, 63, 84):
        Tr, N, Tb, KM, st, th = data[A]
        K = int(np.ceil(0.35 * A))
        outs = []
        for k0 in (1, 2, 3, 4, 5):
            seg = th[k0:K]; j = int(np.nanargmin(seg)) + k0
            outs.append(f"k0 = {k0}: {np.nanmin(seg):.4f} (row {j})")
        dec = next(k for k in range(1, KM) if all(th[j + 1] <= th[j] + 1e-12 for j in range(k, KM - 1)))
        dec_tol = next(k for k in range(1, KM) if all(th[j + 1] <= th[j] + 0.01 for j in range(k, KM - 1)))
        kmax = int(np.nanargmax(th[1:])) + 1
        print(f"      A = {A} (K = {K}): " + '; '.join(outs) + f"; largest root {np.nanmax(th[1:]):.3f} at row {kmax}; non-increasing from row {dec} (from row {dec_tol} if rises of < 0.01 are allowed)")
    print("   Theorem Q on each table: the best block bound sup over (kappa, k0) of theta0 (kappa A - k0), theta0 = min of the roots on the block")
    summ = q2.SUMM
    for A, R in ((30, 7), (45, 9), (63, 11), (84, 13)):
        Tr, N, Tb, KM, st, th = data[A]
        best = (0, 0, 0, 0)
        for k0 in range(0, 8):
            for K in range(k0 + 2, KM + 1):
                t0 = np.nanmin(th[max(k0, 1):K])
                val = t0 * (K - 1 - k0)
                if val > best[0]: best = (val, k0, K, t0)
        psi = committor_pos(Tb[1:KM, 1:KM], Tb[1:KM, 0])
        lnh = -float(summ[str(R)]['ln_h'])
        # Q with (0.35, 0.40, 5) and with the best block: bound on the committor at the top of the block and the flux form
        K35 = int(np.ceil(0.35 * A)); t35 = np.nanmin(th[5:K35])
        # crossing term of Theorem P-bar for the block certificate psi = exp(-theta0 (k - k0)^+), low set {1..K-1}: entries z >= K -> z' < K from tallied rows
        def crossing(K, t0, k0):
            ent = 0.0; ent_star = 0.0; nent = 0.0; mom = 0.0; drop = np.zeros(200)
            psi_K = np.concatenate([[1.0], committor_pos(Tb[1:K, 1:K], Tb[1:K, 0])])
            for z in range(K, KM):
                for z2 in range(1, K):
                    ent += Tr[z, z2] * np.exp(-t0 * max(z2 - k0, 0)); ent_star += Tr[z, z2] * psi_K[z2]
                    nent += Tr[z, z2]; mom += Tr[z, z2] * np.exp(t0 * (K - z2)); drop[K - z2] += Tr[z, z2] * psi_K[z2]
            return ent, ent_star, float(Tr[1:K, 0].sum()), float(Tr[K:KM, 0].sum()), nent, mom / nent, drop / drop.sum()
        e35, e35s, dlow, dhigh, nent, C, drop = crossing(K35, t35, 5)
        expo = 8.0 * float(q2.CUR[f'expo_{R}'][0])
        print(f"      A = {A}: -ln h = {lnh:.2f}; -ln psi*(top row {KM - 1}) = {-np.log(psi[-1]):.2f}; best block k0 = {best[1]}, rows < {best[2]}, theta0 = {best[3]:.4f}: bound {best[0]:.2f} = {best[0] / A:.4f} A;"
              f"  R(0.35, theta0, 5): theta0 = {t35:.4f}, theta0 (K - 1 - 5) = {t35 * (K35 - 1 - 5):.2f} = {t35 * (K35 - 1 - 5) / A:.4f} A")
        print(f"             P-bar with low set {{1..{K35 - 1}}}: deaths from the low set {dlow:.0f}, from rows {K35}..{KM - 1}: {dhigh:.0f}; sum over tallied entries of psi*: {e35s:.1f}; of the block certificate: {e35:.1f}"
              f"  -> Q's bound on the hazard through tallied entries: -ln = {-np.log((e35 + dhigh) / expo):.2f} (the identity with psi* gives {-np.log((e35s + dhigh) / expo):.2f}; entries from rows >= {KM} are not tallied)")
        print(f"             tallied downward crossings of K = {K35}: {nent:.3g} ({nent / expo:.3e} per face-generation); C = E_cross[exp(theta0 (K - z'))] = {C:.2f} (ln C = {np.log(C):.2f});"
              f" share of the psi*-weighted entry flux by depth of landing K - z' = 1, 2, 3, 4-6, 7+: {drop[1]:.2f}, {drop[2]:.2f}, {drop[3]:.2f}, {drop[4:7].sum():.2f}, {drop[7:].sum():.2f};"
              f" share of the deaths from the low set not accounted for by tallied entries: {1 - e35s / dlow:.3f}")
    return data


# ------------------------------------------------------------------------------------------------ LR10
def cramer_tables(Tb, KM, sgrid):
    """Lam[k, s] = ln sum_k' T(k,k') exp(-s (k'-k)) for rows 1..KM-1 (row 0: point mass at 0, Lam = 0)."""
    Lam = np.zeros((KM, len(sgrid)))
    for k in range(1, KM):
        nz = np.flatnonzero(Tb[k]); step = (nz - k).astype(float)
        e = -np.outer(sgrid, step) + np.log(Tb[k, nz])[None, :]
        mx = e.max(axis=1)
        Lam[k] = mx + np.log(np.exp(e - mx[:, None]).sum(axis=1))
    return Lam


def bellman_exact(Tb, KM, sub=4, rising=True, top=None, floor=0, gauss=False):
    """S(x) on the grid x = j/sub, 0 <= x <= top (default KM - 1): S(0) = 0, S(x) = min_y [ I_x(y - x) + S(y) ], I_x the Legendre
    transform of Lam_x(s) = linear interpolation in x of the rows' ln M_k(s) (the limit of the m-fold chain of LR11)."""
    top = KM - 1 if top is None else top
    sgrid = np.concatenate([-np.geomspace(60, 1e-3, 500), [0.0], np.geomspace(1e-3, 60, 500)])
    Lam = cramer_tables(Tb, KM, sgrid)
    if gauss:                                            # same mean and variance, Gaussian: ln M(s) = -s mu + s^2 var / 2
        st = stats(Tb, KM)
        for k in range(1, KM): Lam[k] = -sgrid * st[k, 0] + sgrid ** 2 * st[k, 1] / 2
    G = top * sub
    xg = np.arange(G + 1) / sub
    cost = np.full((G + 1, G + 1), np.inf)
    for i in range(1, G + 1):
        x = xg[i]; k = int(np.floor(x)); f = x - k
        if floor and x < floor:
            L = (x / floor) * Lam[floor]                 # a sparse face as independent clusters of `floor` cells
        else:
            L = Lam[k] if f == 0 else (1 - f) * Lam[k] + f * Lam[min(k + 1, KM - 1)]
        # support: the mixture row can reach y in [lowest, highest]; the Legendre transform is +inf outside (large on the s-grid)
        dy = xg - x
        cost[i] = (-np.outer(dy, sgrid) - L[None, :]).max(axis=1)
    cost = np.maximum(cost, 0.0)
    S = np.full(G + 1, np.inf); S[0] = 0.0
    arg = np.zeros(G + 1, int)
    for i in range(1, G + 1):                                    # decreasing paths first
        c = cost[i, :i] + S[:i]; arg[i] = int(c.argmin()); S[i] = c[arg[i]]
    Sdec = S.copy()
    if rising:
        for sweep in range(200):
            new = np.minimum(S, (cost + S[None, :]).min(axis=1)); new[0] = 0.0
            if np.abs(new - S).max() < 1e-12: break
            S = new
    return xg, S, Sdec, arg


def lr10():
    print("LR10. The recursion V(x) = min_y [ I(x -> y) + V(y) ] on the tables themselves")
    os.makedirs(SCRATCH, exist_ok=True)
    print("   (a) path's own bellman.py (Gaussian closure, decreasing paths, Theta -> 0 at the mean) fed with every row's root and variance, rows k >= 5")
    for R in (9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        H = q2.CUR[f'H_{R}'].astype(float); mean = float((H * np.arange(len(H))).sum() / H.sum())
        st = stats(Tb, KM); th = roots(Tb, KM)
        ks = [k for k in range(5, KM) if k < mean]
        fn = os.path.join(SCRATCH, f'path_r4_table_A{A}.json')
        json.dump({"A": A, "mean": mean, "k": ks, "theta": [float(th[k]) for k in ks], "var": [float(st[k, 1]) for k in ks]}, open(fn, 'w'))
        out = subprocess.run([sys.executable, os.path.join(PATHDIR, 'bellman.py'), fn], capture_output=True, text=True).stdout.strip().split('\n')
        print(f"      A = {A} (mean {mean:.2f}, rows 5..{ks[-1]}): " + ' | '.join(l.strip() for l in out[1:5]))
    print("      default data of bellman.py (eleven roots, five standard deviations typed in): " + ' | '.join(
        l.strip() for l in subprocess.run([sys.executable, os.path.join(PATHDIR, 'bellman.py')], capture_output=True, text=True).stdout.strip().split('\n')[1:5]))
    print("   (b) each row's own rate (Legendre transform of the row's ln M_k; between rows, ln M interpolated linearly: the limit of the m-fold chain of LR11);")
    print("       S = value at the top tallied row, decreasing paths; grid of 1/2, 1/4, 1/8, 1/16 cell and Richardson's value from the last two")
    res = {}
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        th = roots(Tb, KM)
        psi = committor_pos(Tb[1:KM, 1:KM], Tb[1:KM, 0])
        row = {}
        for label, kw in (("rows as tallied", dict()), ("rows below 5 replaced by clusters of 5 (root of row 5 down to 0)", dict(floor=5)),
                          ("the same, Gaussian rates with each row's mean and variance", dict(floor=5, gauss=True))):
            if A == 30 and kw: continue
            vals = []
            for sub in (2, 4, 8, 16):
                xg, S, Sdec, arg = bellman_exact(Tb, KM, sub=sub, rising=(sub == 4), **kw)
                vals.append(Sdec[-1])
                if sub == 4: rise = S[-1]; path = [len(xg) - 1]; xg4 = xg; arg4 = arg
            while path[-1] > 0: path.append(arg4[path[-1]])
            lim = 2 * vals[-1] - vals[-2]
            row[label] = lim
            print(f"      A = {A}, {label}: S = " + ', '.join(f"{v:.3f}" for v in vals) + f" -> {lim:.3f} = {lim / A:.4f} A  (rising steps allowed, grid 1/4: {rise:.3f})")
            if not kw: print(f"              the table's own -ln psi*(top row {KM - 1}) = {-np.log(psi[-1]):.3f}; sum of roots = {np.nansum(th[1:KM]):.3f}; minimising path at grid 1/4: " + ' '.join(f"{xg4[i]:.1f}" for i in path[:14]))
        res[A] = row
    return res


# ------------------------------------------------------------------------------------------------ LR11
def conv(a, b):
    return np.convolve(a, b)


def mfold(rows, m, floor=0):
    """rows[k] = law of the next population from k (k = 0..KT), rows[0] = delta_0. Returns the rows n = 0..m*KT of the chain of m
    independent patches with the population split as evenly as possible: row(m k + r) = rows[k]^{*(m - r)} * rows[k+1]^{*r}."""
    KT = len(rows) - 1
    pw = {}
    def power(k, e):
        if e == 0: return np.array([1.0])
        if (k, e) not in pw:
            pw[(k, e)] = conv(power(k, e - 1), rows[k]) if e > 1 else rows[k].copy()
        return pw[(k, e)]
    out = []
    for n in range(m * KT + 1):
        if floor and n < floor * m:                      # a patches of `floor` cells and one patch with the remainder
            a, c = divmod(n, floor)
            out.append(conv(power(floor, a), rows[c]))
            continue
        k, r = divmod(n, m)
        out.append(conv(power(k, m - r), power(k + 1, r)) if r else power(k, m))
    return out


def lr11(R=13, ms=(1, 2, 4, 8, 16)):
    A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]; KT = KM - 1
    print(f"LR11. The extensive chain built from the table of A = {A}: m independent patches, row(m k + r) = T_k^(*(m-r)) * T_(k+1)^(*r); low set {{1..m*{KT}}}")
    rows = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KM)]
    allv = {}
    for label, floor in (("as requested (rows 1, 2, ... of the table at the bottom)", 0), ("variant: below 5 m cells the face is clusters of 5 cells (rows T_5^(*a) * T_c)", 5)):
        print(f"   {label}")
        vals = {}
        for m in ms:
            q = mfold(rows, m, floor=floor); n = m * KT
            T = np.zeros((n, n)); d = np.zeros(n)
            for i in range(1, n + 1):
                row = q[i]; d[i - 1] = row[0]
                w = row[1:n + 1]; T[i - 1, :len(w)] = w
            psi = committor_pos(T, d)
            agree = float(np.abs(np.log(np.maximum(np.linalg.solve(np.eye(n) - T, d), 1e-300)) - np.log(psi)).max()) if m <= 4 else float('nan')
            th = np.array([np.nan] + [theta_of_row(q[i], i) for i in range(1, n + 1)])
            vals[m] = dict(top=-np.log(psi[-1]), at45=-np.log(psi[int(round(0.45 * A * m)) - 1]), sumth=float(np.nansum(th[1:])),
                           block=max(np.nanmin(th[max(k0, 1):K]) * (K - 1 - k0) for k0 in range(0, 6 * m, max(m // 2, 1)) for K in range(k0 + 2, n + 2, max(m // 2, 1))))
            print(f"      m = {m:2d} (A = {m * A}): -ln psi*(top row {n}) = {vals[m]['top']:.3f}; at 0.45 A: {vals[m]['at45']:.3f}; sum of roots {vals[m]['sumth']:.3f}; best block bound {vals[m]['block']:.3f}"
                  + (f"; elimination without pivoting against numpy's solve: largest difference of ln psi* {agree:.1e}" if m <= 4 else ''), flush=True)
        print("      increments per cell of the face between successive m:")
        for a_, b_ in zip(ms, ms[1:]):
            dA = (b_ - a_) * A
            print(f"         m {a_} -> {b_}: top row {(vals[b_]['top'] - vals[a_]['top']) / dA:.4f} (total {vals[b_]['top'] - vals[a_]['top']:.2f}); at 0.45 A {(vals[b_]['at45'] - vals[a_]['at45']) / dA:.4f}; "
                  f"sum of roots {(vals[b_]['sumth'] - vals[a_]['sumth']) / dA:.4f}; block bound {(vals[b_]['block'] - vals[a_]['block']) / dA:.4f}")
        lims = []
        for sub in (8, 16):
            xg, S, Sdec, arg = bellman_exact(Tb, KM, sub=sub, rising=False, floor=floor)
            lims.append((Sdec[-1], Sdec[int(round(0.45 * A)) * sub]))
        lt, l45 = 2 * lims[1][0] - lims[0][0], 2 * lims[1][1] - lims[0][1]
        print(f"      the recursion with the same rows' own rates (LR10 b, grids 1/8 and 1/16 extrapolated): {lt / A:.4f} per cell at the top row, {l45 / A:.4f} at 0.45 A")
        allv[floor] = vals
    d2 = allv[0][4]['top'] - allv[0][2]['top']
    check(abs(d2 - 36.6) <= 1.2, f"path's prediction for the request as written: the second doubling adds 36.6 +- 1.2 to -ln psi* at the top row; exact: {d2:.2f}")
    print("      path's Gaussian closure on typed-in numbers (bellman.py): 0.218 to the mean density, 0.2135 to 0.45")
    return allv


# ------------------------------------------------------------------------------------------------ LR12
def min_sealed2(nb, q, forbid=(), allowed=None, time_limit=60):
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    N = len(nb)
    A = lil_matrix((N + 1 + len(forbid), N))
    lo = np.zeros(N + 1 + len(forbid)); hi = np.full(N + 1 + len(forbid), np.inf)
    for i, v in enumerate(nb):
        if len(v) > q:
            for j in v: A[i, j] += 1
            A[i, i] -= (len(v) - q)
    A[N, :] = 1; lo[N] = 1
    for k, cells in enumerate(forbid):
        for c in cells: A[N + 1 + k, c] = 1
        lo[N + 1 + k] = -np.inf; hi[N + 1 + k] = len(cells) - 1
    ub = np.ones(N)
    if allowed is not None:
        ub[:] = 0; ub[list(allowed)] = 1
    res = milp(c=np.ones(N), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(N), bounds=Bounds(0, ub), options=dict(time_limit=time_limit))
    if res.x is None: return None, res
    W = [i for i in range(N) if res.x[i] > 0.5]
    Ws = set(W)
    assert all(sum(1 for j in nb[i] if j not in Ws) <= q for i in W), "not sealed"
    return W, res


def lr12():
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'audit', 'class')))
    import lead_check as lc
    print("LR12 and Lemma F. face12e slab, walls at x = 1 and x = 2D + 1, periodic N x M: sealed sets (every cell has at most 3 neighbours in the vessel outside the set)")
    for (N, M, D) in ((3, 3, 2), (3, 3, 3), (3, 3, 4), (4, 4, 2), (4, 4, 3), (4, 4, 4), (3, 5, 2), (5, 5, 4)):
        cells, nbr = lc.graph((2 * D + 3, 2 * N, 2 * M), (False, True, True), "edge", xrange_=(1, 2 * D + 1))
        n = len(cells); nb = [[int(j) for j in row if j != n] for row in nbr]
        xs = cells[:, 0]
        W1 = [i for i in range(n) if xs[i] <= 2]; W2 = [i for i in range(n) if xs[i] >= 2 * D]
        sealed = all(sum(1 for j in nb[i] if xs[j] > 2) <= 3 for i in W1)
        sub, res = min_sealed2(nb, 3, forbid=[W1], allowed=W1)
        check(sealed and sub is None and res.status == 2, f"wall {N} x {M}, {D} cubes deep ({n} cells): sheet + layer beneath ({len(W1)} = 3A cells) is sealed and has no non-empty sealed proper subset (programme infeasible): Lemma F (iii)")
        found = []; forbid = []
        budget = 12 if n <= 130 else 8
        while len(found) < budget:
            W, res = min_sealed2(nb, 3, forbid=forbid, time_limit=20)
            if W is None: break
            optimal = (res.status == 0)
            lay = {}
            for i in W:
                lay.setdefault(tuple(int(v) for v in cells[i]), 1)
            def kind(W):
                Ws = set(W)
                if Ws == set(W1) or Ws == set(W2): return 'wall band (sheet + layer beneath)'
                for ax, per in ((1, 2 * N), (2, 2 * M)):
                    vals = sorted({int(cells[i][ax]) for i in W})
                    full = all(sum(1 for i in range(n) if int(cells[i][ax]) == v) == sum(1 for i in W if int(cells[i][ax]) == v) for v in vals)
                    if full and len(vals) == 3: return f"transverse band: the three layers {'yz'[ax - 1]} = {vals} (mod {per}), whole"
                xv = sorted({int(cells[i][0]) for i in W})
                return f"other: x-layers {xv}, y-values {sorted({int(cells[i][1]) for i in W})}, z-values {sorted({int(cells[i][2]) for i in W})}"
            found.append((len(W), kind(W), optimal)); forbid.append(W)
        from collections import Counter
        cnt = Counter((s, k.split(':')[0] if k.startswith('transverse') else k, o) for s, k, o in found)
        print(f"      inclusion-minimal sealed sets in order of size (each new one contains none found before; first {len(found)}):")
        for (s, k, o), c in sorted(cnt.items()):
            print(f"         {c} x  {s} cells  {k}{'' if o else '  [time limit: size not proved minimal]'}")
        smallest = found[0]
        check(smallest[0] == min(3 * N * M, (5 * D + 2) * min(N, M)), f"      smallest sealed set: {smallest[0]} cells = min(3A = {3 * N * M}, transverse band (5D + 2) min(N, M) = {(5 * D + 2) * min(N, M)})")


# ------------------------------------------------------------------------------------------------ fits, limit
def fits():
    print("entry 16.1: intact row minus notched row of the same strips (exam E1), L = 20, 24, 28, 32")
    L = np.array([20, 24, 28, 32.0]); y = np.array([0.556, 0.857, 1.087, 1.348]); e = np.array([0.055, 0.053, 0.056, 0.062])
    for name, X in (("a ln L + c", np.log(L)), ("a L + c", L)):
        Wt = 1 / e ** 2
        Sx, Sy, S1, Sxx, Sxy = (Wt * X).sum(), (Wt * y).sum(), Wt.sum(), (Wt * X * X).sum(), (Wt * X * y).sum()
        a = (S1 * Sxy - Sx * Sy) / (S1 * Sxx - Sx ** 2); c = (Sy - a * Sx) / S1
        chi = float((Wt * (y - a * X - c) ** 2).sum()); ea = np.sqrt(S1 / (S1 * Sxx - Sx ** 2))
        print(f"      {name}: a = {a:.3f} +- {ea:.3f}, c = {c:.2f}, chi^2 = {chi:.2f} on 2")
    print("      journal: 1.66(16) ln L - 4.41 (chi^2 0.25) and 0.065(6) L - 0.73 (chi^2 0.32)")


def limit():
    print("entry 21: path's check_limit.py (committor of a formula-defined chain with Gaussian rows) with a cancellation-free solver")
    sys.path.insert(0, PATHDIR)
    import importlib
    cl = importlib.import_module('check_limit')
    said = {84: 17.137, 168: 34.829, 336: 70.472, 672: 142.215}
    for A in (84, 168, 336, 672):
        K = int(np.floor(cl.rho * A)); ks = np.arange(1, K)
        Th = np.interp(ks / A, cl.tx, cl.th); v = np.interp(ks / A, cl.vx, cl.vv); b = Th * v / 2
        T = np.zeros((K - 1, K - 1)); d = np.zeros(K - 1)
        for i, k in enumerate(ks):
            mu, sd = k + A * b[i], np.sqrt(A * v[i])
            j = np.arange(-int(8 * sd) - k - 2, int(mu + 10 * sd) + 3)
            w = np.exp(-(j - mu) ** 2 / (2 * sd * sd)); w /= w.sum()
            d[i] = w[j <= 0].sum(); m = (j >= 1) & (j <= K - 1); T[i, j[m] - 1] = w[m]
        mine = -np.log(committor_pos(T, d)[int(round(cl.X * A)) - 1])
        check(abs(mine - said[A]) < 2e-3, f"A = {A}: -ln psi*(0.45 A) = {mine:.3f} by elimination without pivoting; the journal's table says {said[A]}")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('props', 'all'): props()
    if cmd in ('lr9', 'all'): lr9()
    if cmd in ('lr10', 'all'): lr10()
    if cmd in ('lr11', 'all'): lr11()
    if cmd in ('lr12', 'all'): lr12()
    if cmd in ('fits', 'all'): fits()
    if cmd in ('limit', 'all'): limit()
    print('ALL OK' if OK else 'SOMETHING FAILED')
