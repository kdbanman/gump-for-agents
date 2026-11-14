#!/usr/bin/env python3
"""Calculator for journal entries 23 and 24 (path line, closing round). No simulation: exact arithmetic on the curated
tallies ../critic/lab/data/fluct_tables.npz (pooled one-step tables of the face population of gump hulls, A = 30, 45,
63, 84, rows k <= A/2) and on chains built from them, plus a test of Theorem V- on random tables.

  python3 vminus_check.py random   Theorem V- (entry 24.2) on random tables, censored mass and slack e > 0 included:
                                   whenever the hypotheses hold the committor must be below the certificate
  python3 vminus_check.py q        entry 23: Theorem Q's undershoot moment per crossing (C) and per unit of exposure
                                   (Phi = chi C), and the one-step constant C+ of condition R+, on the tallies and on
                                   the m-fold chain of the A = 84 table
  python3 vminus_check.py m0       entry 24.3: margins eps0 of the base tables and the proof's threshold m0(delta)
  python3 vminus_check.py example  entry 24.5: a three-row family in which exp(-(1 - delta) m V) alone is not a
                                   supersolution at small m
  python3 vminus_check.py v [M]    entry 24.8: Theorem V- on the m-fold chains of the A = 84 table, m = 1 ... M
                                   (default 16, one minute; 32 takes three more): exact committor, the certified
                                   exponent, the admissible functions W_J (Chernoff rates) and W° (most probable path)
  python3 vminus_check.py all

Everything is independent of the critic's lab code (only its data file is read), so the numbers that both compute
(committors of the m-fold chains, the constant C) are computed twice.  One core: set OMP_NUM_THREADS=1.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', 'critic', 'lab', 'data', 'fluct_tables.npz'))
AREA = {7: 30, 9: 45, 11: 63, 13: 84}
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ----------------------------------------------------------------------------------------------- tools
def table(R):
    """counts Tr[k, k'] (k' = 0: death), row exposures N, normalised rows Tb, total exposure in face-generations."""
    cur = np.load(DATA)
    Tr = cur[f'Tr_{R}'].astype(float)
    N = Tr.sum(1)
    return Tr, N, Tr / np.maximum(N, 1)[:, None], 8.0 * float(cur[f'expo_{R}'][0])


def mfold(rows, m, floor=0):
    """rows[k] = law of the next population from k (rows[0] = [1.0]).  Chain of m independent patches, population split
    as evenly as possible: row(m k + r) = rows[k]^{*(m-r)} * rows[k+1]^{*r}.  With floor = c: below c m cells the face
    is a clusters of c cells and one patch with the remainder, row(c a + b) = rows[c]^{*a} * rows[b]."""
    KT = len(rows) - 1
    cache = {}

    def power(k, e):
        if e == 0:
            return np.array([1.0])
        if (k, e) not in cache:
            cache[(k, e)] = rows[k].copy() if e == 1 else np.convolve(power(k, e - 1), rows[k])
        return cache[(k, e)]

    out = []
    for n in range(m * KT + 1):
        if floor and n < floor * m:
            a, b = divmod(n, floor)
            out.append(np.convolve(power(floor, a), rows[b]))
        else:
            k, r = divmod(n, m)
            out.append(np.convolve(power(k, m - r), power(k + 1, r)) if r else power(k, m))
    return out


def square(q, n1):
    """T[n, n'] for n, n' in 0..n1 (row 0 is not used): the rows cut at the top of the low set {1..n1}."""
    T = np.zeros((n1 + 1, n1 + 1))
    for n in range(1, n1 + 1):
        w = q[n][:n1 + 1]
        T[n, :len(w)] = w
    return T


def committor(T):
    """smallest non-negative solution of psi(n) = T[n, 0] + sum_{n' in 1..n1} T[n, n'] psi(n'); psi(0) = 1.
    Elimination without pivoting on the M-matrix I - T (no subtraction of nearly equal numbers)."""
    n1 = T.shape[0] - 1
    A = np.eye(n1) - T[1:, 1:]
    b = T[1:, 0].copy()
    for i in range(n1):
        f = A[i + 1:, i] / A[i, i]
        A[i + 1:, i:] -= f[:, None] * A[i, i:][None, :]
        b[i + 1:] -= f * b[i]
    x = np.zeros(n1)
    for i in range(n1 - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return np.concatenate([[1.0], x])


def shortest(cost):
    """largest W with W(0) = 0 and W(n) - W(n') <= cost[n, n'] (n >= 1): cost of the cheapest path to 0."""
    n1 = cost.shape[0] - 1
    c = cost.copy()
    c[0, :] = np.inf
    W = np.full(n1 + 1, np.inf)
    W[0] = 0.0
    for _ in range(20 * n1 + 20):
        new = np.minimum(W, (c + W[None, :]).min(axis=1))
        new[0] = 0.0
        if np.array_equal(new, W):
            break
        W = new
    return W


def w_path(T):
    """W°: cost -ln T of the most probable path to 0 inside the low set."""
    with np.errstate(divide='ignore'):
        return shortest(-np.log(T))


SGRID = np.concatenate([-np.geomspace(60, 1e-3, 300), [0.0], np.geomspace(1e-3, 60, 300)])


def w_legendre(q, n1):
    """W_J: the same with the Chernoff cost J_n(n') = sup_s [ s (n - n') - ln M_n(s) ] of the full row (sup over a grid
    of s, so J is under-estimated: W_J stays admissible).  For the m-fold chain J_n(n') = m I(n/m -> n'/m)."""
    cost = np.full((n1 + 1, n1 + 1), np.inf)
    tgt = np.arange(n1 + 1)
    for n in range(1, n1 + 1):
        nz = np.flatnonzero(q[n])
        e = -np.outer(SGRID, nz - n) + np.log(q[n][nz])[None, :]
        mx = e.max(axis=1)
        lnM = mx + np.log(np.exp(e - mx[:, None]).sum(axis=1))
        cost[n] = np.maximum((np.outer(n - tgt, SGRID) - lnM[None, :]).max(axis=1), 0.0)
    return shortest(cost)


def ln_M(row, n, s):
    nz = np.flatnonzero(row)
    e = np.log(row[nz]) - s * (nz - n)
    return float(e.max() + np.log(np.exp(e - e.max()).sum()))


def root(row, n):
    """theta = max{s >= 0 : M(s) <= 1}; 0 if the mean step is not positive."""
    if ln_M(row, n, 1e-9) > 0:
        return 0.0
    lo, hi = 0.0, 1.0
    while ln_M(row, n, hi) <= 0 and hi < 64:
        hi *= 2
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if ln_M(row, n, mid) <= 0 else (lo, mid)
    return lo


def certificate(T, W, th0, delta, e=0.0, full_rows=None):
    """Theorem V-.  Row n is good if  e^{(1-delta) e} sum_{n' <= n1} [T(n, n') e^{-th0 (n' - n)}]^delta <= 1  (the sharp
    form), or, when full_rows is given, if (e^e N_n)^{1-delta} M_n(th0)^delta <= 1 (the form of the statement).
    Returns n0 = k0 + 1 (least row with all of n0..n1 good; None if the top row is bad) and the exponent
    g(n) = [(1 - delta)(W(n) - max_{j <= k0} W(j)) + delta th0 (n - k0)]^+ , so that psi* <= exp(-g)."""
    n1 = T.shape[0] - 1
    good = np.zeros(n1 + 1, bool)
    for n in range(1, n1 + 1):
        nz = np.flatnonzero(T[n])
        if full_rows is None:
            val = (1 - delta) * e + np.log(np.exp(delta * (np.log(T[n, nz]) - th0 * (nz - n))).sum())
        else:
            val = (1 - delta) * (e + np.log(len(nz))) + delta * ln_M(full_rows[n], n, th0)
        good[n] = val <= 0
    bad = np.flatnonzero(~good[1:]) + 1
    n0 = int(bad.max()) + 1 if len(bad) else 1
    if n0 > n1:
        return None, None
    g = np.maximum((1 - delta) * (W - W[:n0].max()) + delta * th0 * (np.arange(n1 + 1) - n0 + 1), 0.0)
    return n0, g


# ----------------------------------------------------------------------------------------------- random tables
def random_tables(trials=3000, seed=1):
    print("Theorem V- on random tables (rows with an upward drift, a few long jumps, censored mass in half of them)")
    rng = np.random.default_rng(seed)
    used = cases = strict = teeth = teeth_cases = 0
    worst = np.inf
    for t in range(trials):
        n1 = int(rng.integers(6, 30))
        T = np.zeros((n1 + 1, n1 + 1))
        full = [None] * (n1 + 1)
        for n in range(1, n1 + 1):
            row = np.zeros(n1 + 12)
            ups = rng.integers(1, 9, size=int(rng.integers(1, 4)))
            for u in ups:
                row[n + u] += rng.random()
            row /= row.sum()
            row *= 1 - 10.0 ** rng.uniform(-6, -0.5)                 # mass that goes down
            downs = rng.integers(0, n, size=int(rng.integers(1, 4)))  # targets below n, 0 included
            wts = rng.random(len(downs))
            rest = 1 - row.sum()
            for d, wt in zip(downs, wts):
                row[d] += rest * wt / wts.sum()
            if t % 2:
                row *= rng.uniform(0.7, 1.0)                          # censored mass
            full[n] = row
            T[n] = row[:n1 + 1]
        psi = committor(T)
        W = w_path(T)
        if not np.isfinite(W[1:]).all() or (psi[1:] <= 0).any():
            continue
        e = float(rng.choice([0.0, 0.0, rng.uniform(0, 1)]))
        Wp = W + (rng.uniform(-e / 2, e / 2, size=n1 + 1) if e else 0.0)       # admissible with slack e
        Wp[0] = 0.0
        used += 1
        for delta in (0.3, 0.5, 0.7, 0.9, 1.0):
            for th0 in rng.uniform(0.05, 1.5, size=3):
                if delta < 1 and not e:                               # the same formula with the hypothesis dropped (k0 = 0)
                    g = np.maximum((1 - delta) * W + delta * th0 * np.arange(n1 + 1), 0.0)
                    teeth_cases += 1
                    teeth += int((-np.log(psi[1:]) - g[1:]).min() < -1e-9)
                for fr in (None, full):
                    n0, g = certificate(T, Wp, th0, delta, e=e, full_rows=fr)
                    if n0 is None:
                        continue
                    cases += 1
                    gap = (-np.log(psi[1:]) - g[1:]).min()
                    worst = min(worst, gap)
                    strict += int(delta < 1 and g[n1] > th0 * (n1 - n0 + 1) + 1e-9)
    check(worst >= -1e-9, f"{cases} cases on {used} tables: -ln psi* >= the certified exponent at every row (smallest gap {worst:.2e}); "
                          f"in {strict} cases with delta < 1 the certificate at the top row beats the block bound theta0 (n1 - k0)")
    check(teeth > 0, f"the test can fail: with the good-row hypothesis dropped (k0 = 0) the same formula is violated in {teeth} of {teeth_cases} cases")


# ----------------------------------------------------------------------------------------------- entry 23
def gth(P):
    """stationary law of an irreducible stochastic matrix, Grassmann-Taksar-Heyman elimination (no subtractions)."""
    P = P.copy()
    n = P.shape[0]
    for k in range(n - 1, 0, -1):
        P[:k, k] /= P[k, :k].sum()
        P[:k, :k] += np.outer(P[:k, k], P[k, :k])
    pi = np.zeros(n)
    pi[0] = 1.0
    for k in range(1, n):
        pi[k] = pi[:k] @ P[:k, k]
    return pi / pi.sum()


def undershoot(ms=(1, 2, 4, 8, 16)):
    print("Entry 23. Theorem Q's entry term: K = ceil(0.35 A), theta0 = least root on [5, K) (per patch)")
    print("  chi = downward crossings of K per unit of exposure; C = E[e^{theta0 (K - z')} | crossing] (the old side condition);")
    print("  Phi = chi C = the same moment per unit of exposure (what the proof uses); C+ = max_{z >= K} M_z(theta0) e^{-theta0 (z - K)} (one-step)")
    print("  (a) the tallies; rows above A/2 are not tallied, so chi, Phi and C+ are over the rows K <= z <= A/2 only")
    res = {}
    for R in (7, 9, 11, 13):
        A = AREA[R]
        Tr, N, Tb, H = table(R)
        KM = Tr.shape[0]
        K = int(np.ceil(0.35 * A))
        th = [np.nan] + [root(Tb[k], k) for k in range(1, KM)]
        th0 = min(th[5:K])
        expo = H
        cr = Tr[K:KM, 1:K]
        u = K - np.arange(1, K)
        chi = cr.sum() / expo
        C = (cr * np.exp(th0 * u)[None, :]).sum() / cr.sum()
        direct = Tr[K:KM, 0].sum()
        phit = chi * C + direct * np.exp(th0 * K) / expo
        cplus = max(np.exp(ln_M(Tb[z], z, th0) - th0 * (z - K)) for z in range(K, KM))
        h = Tr[:, 0].sum() / expo
        res[A] = (chi, C, phit, cplus)
        print(f"      A = {A}: K = {K}, theta0 = {th0:.4f}; chi = {chi:.4f}; C = {C:.2f}; direct deaths from K..A/2: {direct:.0f}; "
              f"Phi (direct deaths counted as undershoots to 0) = {phit:.4f}; C+ = {cplus:.3f}; "
              f"-ln[Phi e^(-theta0 (K - 5))] = {-np.log(phit) + th0 * (K - 5):.2f} against -ln h = {-np.log(h):.2f}")
    print("  (b) the m-fold chain of the A = 84 table (clusters of 5 at the bottom), restarted at its top row at death; stationary law by GTH")
    Tr, N, Tb, H = table(13)
    KT = Tr.shape[0] - 1
    rows = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KT + 1)]
    out = {}
    for m in ms:
        q = mfold(rows, m, floor=5)
        n = m * KT
        P = np.zeros((n, n))
        d = np.zeros(n)
        for i in range(1, n + 1):
            w = q[i][1:n + 1]
            P[i - 1, :len(w)] = w
            d[i - 1] = q[i][0]
            P[i - 1, n - 1] += 1.0 - P[i - 1].sum()
        mu = gth(P[::-1, ::-1].copy())[::-1]
        K = int(np.ceil(0.35 * 84 * m))
        th0 = min(root(q[i], i) for i in range(5 * m, K))
        z = np.arange(K, n + 1)
        zp = np.arange(1, K)
        F = mu[z - 1][:, None] * P[np.ix_(z - 1, zp - 1)]
        chi = F.sum()
        C = (F * np.exp(th0 * (K - zp))[None, :]).sum() / chi
        direct = float((mu[z - 1] * d[z - 1]).sum()) * np.exp(th0 * K)
        cplus = max(np.exp(ln_M(q[i], i, th0) - th0 * (i - K)) for i in z)
        h = float((mu * d).sum())
        out[m] = (chi, C, chi * C + direct, cplus)
        print(f"      m = {m:2d} ({84 * m} cells): K = {K}, theta0 = {th0:.4f}; ln chi = {np.log(chi):.2f}; C = {C:.2f}; Phi = {chi * C + direct:.3e}; "
              f"C+ = {cplus:.3f}; -ln[Phi e^(-theta0 (K - 5 m))] = {-np.log(chi * C + direct) + th0 * (K - 5 * m):.2f} against -ln h = {-np.log(h):.2f}", flush=True)
    print("  (c) entry 24.4, condition B+ on the tallied rows above the low set {1..K-1}: the largest W(K-1) - W(z') + ln T(z, z'), K <= z <= A/2, z' < K")
    bplus = []
    for R in (9, 11, 13):
        A = AREA[R]
        Tr, N, Tb, expo = table(R)
        KM = Tr.shape[0]
        rws = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KM)]
        n1 = int(np.ceil(0.35 * A)) - 1
        line = f"      A = {A}:"
        for name, W in (("W_J", w_legendre(rws, n1)), ("W°", w_path(square(rws, n1)))):
            worst = max(W[n1] - W[zp] + np.log(Tb[z, zp]) for z in range(n1 + 1, KM) for zp in range(n1 + 1) if Tb[z, zp] > 0)
            bplus.append(worst)
            line += f" {name}: {worst:+.3f};"
        print(line)
    check(max(bplus) <= 0, "B+ holds with e = 0 on every tallied row above K, for W_J and for W°")
    check(all(out[b][1] > out[a][1] for a, b in zip(ms, ms[1:])) and all(out[b][2] < out[a][2] for a, b in zip(ms, ms[1:]))
          and all(v[2] <= v[3] + 1e-12 for v in out.values()) and all(v[3] < 1.1 for v in out.values())
          and all(v[2] <= v[3] + 1e-12 and v[3] < 1.1 for v in res.values()),
          "per crossing the moment C grows with the size; per unit of exposure Phi falls and is below the one-step constant C+, "
          "which is below 1.1 on every tallied row and at every m")


# ----------------------------------------------------------------------------------------------- entry 24.3
def thresholds():
    print("Entry 24.3. Margin eps0 = min over the block rows of -ln M_k(theta0) (nats per patch), best theta0, and the proof's threshold")
    print("            m0(delta) = least m with delta m eps0 >= (1 - delta) ln(m k1 + 1)   (a face of m A cells)")
    for R in (9, 11, 13):
        A = AREA[R]
        Tr, N, Tb, H = table(R)
        KM = Tr.shape[0]
        th = [np.nan] + [root(Tb[k], k) for k in range(1, KM)]
        print(f"   A = {A}: roots of rows 1..5: " + ', '.join(f"{t:.3f}" for t in th[1:6]) + f"; of the top rows {KM - 3}..{KM - 1}: " + ', '.join(f"{t:.3f}" for t in th[KM - 3:])
              + f"; largest k' charged by rows 1, 2, 3: {[int(np.flatnonzero(Tb[k]).max()) for k in (1, 2, 3)]} (rim lemma: at most 7 k)")
        for k0, k1 in ((5, int(np.ceil(0.35 * A)) - 1), (5, int(np.ceil(0.45 * A)) - 1), (5, KM - 1), (1, KM - 1)):
            best = (0.0, None)
            for th0 in np.arange(0.002, 0.7, 0.002):
                eps = min(-ln_M(Tb[k], k, th0) for k in range(k0, k1 + 1))
                if eps > best[0]:
                    best = (eps, th0)
            if best[1] is None:
                print(f"      rows {k0}..{k1}: no theta0 with a positive margin")
                continue
            line = f"      rows {k0}..{k1}: eps0 = {best[0]:.4f} at theta0 = {best[1]:.3f}; m0: "
            for delta in (0.5, 0.2, 0.1):
                m = 1
                while delta * m * best[0] < (1 - delta) * np.log(m * k1 + 1):
                    m = max(m + 1, int(m * 1.002))
                line += f"delta {delta}: {m}; "
            print(line)


# ----------------------------------------------------------------------------------------------- entry 24.5
def vminus(mmax=16):
    print("Entry 24.8. Theorem V- on the m-fold chains of the A = 84 table. Low set {1..n1}, n1 = ceil(top 84 m) - 1 (or the top tallied row).")
    print("  Admissible W: W_J (Chernoff cost of each row; for rows as tallied this is m I(n/m -> n'/m)) and W° (most probable path).")
    print("  Certified = the largest exponent at n1 over delta in {0.3, ..., 1.0} and theta0 in {0.02, ..., 0.60} for which every row n0..n1 is good (sharp form); k0 = n0 - 1.")
    Tr, N, Tb, H = table(13)
    KT = Tr.shape[0] - 1
    rows = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KT + 1)]
    ms = [m for m in (1, 2, 4, 8, 16, 32) if m <= mmax]
    allok = True
    summary = {}
    for floor, label in ((0, "rows as tallied"), (5, "clusters of 5 below 5 m cells")):
        print(f"  {label}")
        for m in ms:
            q = mfold(rows, m, floor=floor)
            for top in (0.35, 0.45, 0.5):
                n1 = min(int(np.ceil(top * 84 * m)) - 1, m * KT)
                T = square(q, n1)
                psi = committor(T)
                WJ = w_legendre(q, n1)
                Wp = w_path(T)
                lp = -np.log(psi)
                best = {}
                for name, W in (("W_J", WJ), ("W°", Wp)):
                    for delta in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
                        for th0 in np.arange(0.02, 0.62, 0.02):
                            n0, g = certificate(T, W, th0, delta)
                            if n0 is None:
                                continue
                            allok = allok and bool((lp[1:] >= g[1:] - 1e-9).all())
                            if name not in best or g[n1] > best[name][0]:
                                best[name] = (g[n1], delta, th0, n0)
                            if delta == 1.0 and ("block" not in best or g[n1] > best["block"][0]):
                                best["block"] = (g[n1], delta, th0, n0)
                cells = 84 * m
                summary[(floor, m, top)] = (lp[n1], best["W_J"][0], best["block"][0], WJ[n1], Wp[n1])
                print(f"      m = {m:2d} ({cells} cells), top {top}: n1 = {n1}; -ln psi*(n1) = {lp[n1]:.2f} ({lp[n1] / cells:.4f} per cell); W_J(n1) = {WJ[n1]:.2f}; W°(n1) = {Wp[n1]:.2f}; "
                      f"certified with W_J: {best['W_J'][0]:.2f} ({best['W_J'][0] / cells:.4f}) at delta = {best['W_J'][1]:.1f}, theta0 = {best['W_J'][2]:.2f}, n0 = {best['W_J'][3]}; "
                      f"with W°: {best['W°'][0]:.2f} at delta = {best['W°'][1]:.1f}; block bound (delta = 1): {best['block'][0]:.2f} ({best['block'][0] / cells:.4f})", flush=True)
    check(allok, "no violation: wherever the rows n0..n1 are good, -ln psi* is at least the certified exponent at every row, for both W")
    check(all(v[0] <= v[4] + 1e-9 for v in summary.values()), "-ln psi*(n1) <= W°(n1) in every case (one path is a lower bound for the committor)")
    big = ms[-1]
    check(all(summary[(f, big, t)][1] > summary[(f, big, t)][2] for f in (0, 5) for t in (0.35, 0.45)),
          f"at m = {big} the certificate with delta < 1 beats the block bound at tops 0.35 and 0.45")


# ----------------------------------------------------------------------------------------------- entry 24.5
def example(c=0.01):
    print(f"Entry 24.5. A family where V alone has almost no slack: rows k = 1, 2, 3 go to 0 with probability {c}, to k + 1 otherwise; m-fold chains, low set {{1..3m}}")
    rows = [np.array([1.0])]
    for k in (1, 2, 3):
        r = np.zeros(k + 2)
        r[0], r[k + 1] = c, 1 - c
        rows.append(r)
    print("   roots of rows 1, 2, 3: " + ', '.join(f"{root(rows[k], k):.3f}" for k in (1, 2, 3))
          + "; margins -ln M_k(1.0): " + ', '.join(f"{-ln_M(rows[k], k, 1.0):.3f}" for k in (1, 2, 3)))
    fails = {}
    for m in (5, 10, 20, 40):
        q = mfold(rows, m)
        n1 = 3 * m
        T = square(q, n1)
        WJ = w_legendre(q, n1)
        line = f"   m = {m:2d}: W_J/m at x = 1, 2, 3: {WJ[m] / m:.4f}, {WJ[2 * m] / m:.4f}, {WJ[3 * m] / m:.4f};"
        for delta in (0.2, 0.5):
            for name, th0 in (("V alone", 0.0), ("with the linear term, theta0 = 1", 1.0)):
                G = (1 - delta) * WJ + delta * th0 * np.maximum(np.arange(n1 + 1) - m, 0)
                g = np.maximum(G - (1 - delta) * WJ[:m].max(), 0.0)
                ratio = np.array([(T[n] * np.exp(np.minimum(g[n] - g, 700))).sum() for n in range(1, n1 + 1)])
                bad = int(((ratio > 1 + 1e-12) & (g[1:] > 0)).sum())
                fails[(m, delta, th0)] = bad
                line += f" delta {delta}, {name}: {bad} rows fail;"
        print(line)
    check(all(fails[(m, d, 0.0)] > 0 for m in (5, 10) for d in (0.2, 0.5)) and all(fails[(m, d, 0.0)] == 0 for m in (20, 40) for d in (0.2, 0.5))
          and all(v == 0 for (m, d, t), v in fails.items() if t),
          "exp(-(1 - delta) m V) is not a supersolution at m = 5 and 10 and is one from m = 20; with the linear term it is one at every m tried")


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('example', 'all'):
        example()
    if cmd in ('random', 'all'):
        random_tables()
    if cmd in ('q', 'all'):
        undershoot()
    if cmd in ('m0', 'all'):
        thresholds()
    if cmd in ('v', 'all'):
        vminus(int(sys.argv[2]) if len(sys.argv) > 2 else 16)
    print('ALL OK' if OK else 'SOMETHING FAILED')
