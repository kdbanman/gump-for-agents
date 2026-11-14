#!/usr/bin/env python3
"""The table statements of the path line, tested on random tables with exact (linear-algebra) committors.

  python3 p2_tables.py            (about two minutes, one core)

Each block prints the number of cases and the number of violations; a "control" line drops one hypothesis
and reports how often the conclusion then fails (so the hypothesis is seen to be used).

  T'   (journal 17.2)  block bound  psi*(k) <= exp(-theta0 (k-k0)^+)
  T    (17.3)          psi*(k) >= c0 (exp(-S(k)) - exp(-S(K)))
  X    (17.4)          skip-free rows; branching rows; the three numbers 1.695 < 1.863 < 2.234
  C    (entry 18)      comparison with a monotone kernel
  V-   (24.2)          the mixed certificate, with W = W°, W_J and slack; the lower bound exp(-W°)
  V'   (24.5)          the gain-or-rare form; control: W not admissible
  E1, V-(E) (24.3)     the m-fold family: transform identity; (S) => rows good => bound; "nothing subtracted"
"""
import sys, time, math
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp

TOL = 1e-9


# ---------------------------------------------------------------- tables, transforms, roots, committors
def rand_row(rng, k, nmax, drift, jump, death=0.0, cens=0.0):
    lo, hi = max(0, k - jump), min(nmax, k + jump)
    tg = rng.choice(np.arange(lo, hi + 1), size=min(hi - lo + 1, int(rng.integers(2, 7))), replace=False)
    w = rng.random(len(tg)) * np.exp(drift * (tg - k))
    row = np.zeros(nmax + 1)
    row[tg] = w / w.sum()
    if death:
        row *= (1 - death); row[0] += death
    return row * (1 - cens)


def rand_table(rng, nmax, drift=None, jump=None, death=None, cens=None):
    drift = rng.uniform(0.3, 1.6) if drift is None else drift
    jump = int(rng.integers(1, 6)) if jump is None else jump
    T = np.zeros((nmax + 1, nmax + 1)); T[0, 0] = 1
    for k in range(1, nmax + 1):
        dth = (rng.random() < 0.3) * rng.uniform(0, 0.05) if death is None else death
        cn = (rng.random() < 0.5) * rng.uniform(0, 0.2) if cens is None else cens
        T[k] = rand_row(rng, k, nmax, drift, jump, dth, cn)
    return T


def M(row, k, s):
    j = np.nonzero(row)[0]
    return float(np.sum(row[j] * np.exp(-s * (j - k))))


def root(row, k):
    """theta_k = sup{ s >= 0 : M_k(s) <= 1 } (inf if the row cannot go down)."""
    j = np.nonzero(row)[0]
    if len(j) == 0 or j.min() >= k:
        return math.inf
    hi = 1.0
    while M(row, k, hi) <= 1:
        hi *= 2
        if hi > 1e4:
            return math.inf
    lo = 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if M(row, k, mid) <= 1: lo = mid
        else: hi = mid
    return lo


def committor(T, K):
    """psi* for the low set {1..K-1}: psi(0)=1, psi(k>=K)=0."""
    L = np.arange(1, K)
    A = np.eye(K - 1) - T[np.ix_(L, L)]
    psi = np.zeros(T.shape[0]); psi[0] = 1
    psi[L] = np.linalg.solve(A, T[L, 0])
    return psi


def leq(a, b):
    return a <= b * (1 + 1e-7) + 1e-13


# ---------------------------------------------------------------- T', T
def test_Tprime_T(rng, ntab=1500):
    cases = viol = cT = vT = ctrl = ctrl_v = 0
    for _ in range(ntab):
        nmax = int(rng.integers(6, 15)); T = rand_table(rng, nmax)
        th = [math.inf] + [root(T[k], k) for k in range(1, nmax + 1)]
        for _ in range(6):
            K = int(rng.integers(3, nmax + 1)); k0 = int(rng.integers(0, K - 1))
            try:
                psi = committor(T, K)
            except np.linalg.LinAlgError:
                continue
            blk = [k for k in range(max(k0, 1), K)]
            t0 = min(min(th[k] for k in blk), 30.0)
            for theta0 in (t0, t0 * rng.random()):
                cases += 1
                viol += not all(leq(psi[k], math.exp(-theta0 * max(k - k0, 0))) for k in range(nmax + 1))
            if 0 < t0 < 30:                              # control: a theta0 above the block's least root
                ctrl += 1
                ctrl_v += not all(leq(psi[k], math.exp(-2.0 * t0 * max(k - k0, 0))) for k in range(nmax + 1))
            if k0 >= 1 and all(th[k] < math.inf for k in range(k0, K)):
                s = {k: max(th[j] for j in range(k, K)) for k in range(k0, K)}
                S = {k0: 0.0}
                for k in range(k0 + 1, K): S[k] = S[k - 1] + s[k]
                SK = S[K - 1] + s[K - 1]
                c0 = math.exp(-s[k0] * k0) * min(psi[j] for j in range(0, k0))
                for k in range(k0, K):
                    cT += 1
                    vT += not leq(c0 * (math.exp(-S[k]) - math.exp(-SK)), psi[k])
    print(f"T' : {cases} (table, block, theta0) cases, violations {viol};  control (theta0 doubled): "
          f"{ctrl_v} of {ctrl} fail")
    print(f"T  : {cT} (table, block, row) cases, violations {vT}")
    return viol == 0 and vT == 0


# ---------------------------------------------------------------- X
def test_X(rng):
    ok = True
    # (a) skip-free
    worst_lo, worst_hi = 9, 0
    for _ in range(500):
        K = int(rng.integers(3, 14)); nmax = K
        T = np.zeros((nmax + 1, nmax + 1)); T[0, 0] = 1
        r = []
        for k in range(1, nmax + 1):
            u = rng.uniform(0.3, 0.8); d = u * rng.uniform(0.02, 0.9); r.append(d / u)
            sc = rng.uniform(0.5, 1) / max(u + d, 1)
            u, d = u * sc, d * sc
            T[k, k - 1] = d; T[k, min(k + 1, nmax)] += u; T[k, k] += 1 - u - d
        psi = committor(T, K)
        pi = np.cumprod([1.0] + r[:K - 1])
        rbar = max(r[:K - 1])
        for k in range(1, K):
            exact = pi[k:K].sum() / pi[:K].sum()
            ok &= abs(exact - psi[k]) < 1e-9 * exact + 1e-15
            ok &= abs(-math.log(r[k - 1]) - root(T[k], k)) < 1e-8
            ratio = psi[k] / pi[k]
            worst_lo = min(worst_lo, ratio / (1 - rbar)); worst_hi = max(worst_hi, ratio * (1 - rbar))
    ok &= worst_lo >= 1 - 1e-9 and worst_hi <= 1 + 1e-9
    print(f"X(a): 500 skip-free tables: gambler's-ruin formula and r_k = d_k/u_k reproduced; "
          f"psi*(k)/pi_k within [(1-rbar), 1/(1-rbar)]: min ratio/(1-rbar) = {worst_lo:.4f}, max ratio*(1-rbar) = {worst_hi:.4f}")
    # (b) branching
    bad = 0; n = 0
    for _ in range(300):
        J = int(rng.integers(2, 5)); f = rng.random(J + 1); f[0] *= rng.uniform(0.05, 0.6); f /= f.sum()
        if np.dot(np.arange(J + 1), f) <= 1.05: continue
        q = 0.0
        for _ in range(5000): q = float(np.polyval(f[::-1], q))
        K = int(rng.integers(3, 9)); nmax = J * K
        T = np.zeros((nmax + 1, nmax + 1)); T[0, 0] = 1
        row = np.array([1.0])
        for k in range(1, K):
            row = np.convolve(row, f); T[k, :len(row)] = row
        psi = committor(T, K)
        ths = [root(T[k], k) for k in range(1, K)]
        for k in range(1, K):
            n += 1
            bad += not (leq(q ** k - q ** K, psi[k]) and leq(psi[k], q ** k))
            bad += abs(ths[k - 1] + math.log(q)) > 1e-6
    print(f"X(b): {n} branching rows: q^k - q^K <= psi* <= q^k and theta_k = -ln q, violations {bad}")
    ok &= bad == 0
    # (c) the three numbers
    T = np.zeros((5, 5)); T[0, 0] = 1; T[1, 0], T[1, 2] = .2, .8; T[2, 0], T[2, 2], T[2, 4] = .09, .42, .49
    psi = committor(T, 3); t1, t2 = root(T[1], 1), root(T[2], 2)
    print(f"X(c): theta1={t1:.3f} theta2={t2:.3f} block bound {2 * min(t1, t2):.3f} < -ln psi*(2) = {-math.log(psi[2]):.3f}"
          f" < root sum {t1 + t2:.3f}")
    ok &= abs(2 * min(t1, t2) - 1.695) < 1e-3 and abs(-math.log(psi[2]) - 1.863) < 1e-3 and abs(t1 + t2 - 2.234) < 1e-3
    return ok


# ---------------------------------------------------------------- C
def test_C(rng, ntab=3000):
    def run(monotone):
        n = bad = 0
        for _ in range(ntab):
            nmax = int(rng.integers(5, 11)); K = int(rng.integers(3, nmax + 1))
            q = np.zeros((nmax + 1, nmax + 1)); q[0, 0] = 1
            for k in range(1, nmax + 1):
                q[k] = rng.dirichlet(np.ones(nmax + 1) * 0.5)
            if monotone:                                     # cdf_k <= cdf_{k-1} pointwise
                cdf = np.cumsum(q, axis=1)
                for k in range(1, nmax + 1):
                    cdf[k] = np.minimum(cdf[k], cdf[k - 1])
                cdf[:, -1] = 1
                q = np.diff(np.concatenate([np.zeros((nmax + 1, 1)), cdf], axis=1), axis=1)
            T = np.zeros_like(q); T[0, 0] = 1                 # a table dominating q row by row
            for k in range(1, nmax + 1):
                for j in range(nmax + 1):
                    mass = q[k, j]
                    if mass == 0: continue
                    mv = rng.random() * mass * (rng.random() < 0.7)
                    T[k, j] += mass - mv
                    if j < nmax and rng.random() < 0.8:
                        T[k, int(rng.integers(j + 1, nmax + 1))] += mv      # moved up; otherwise censored
                cT = np.cumsum(T[k]); cq = np.cumsum(q[k])
                assert (cT <= cq + 1e-12).all()
            psiT, psiq = committor(T, K), committor(q, K)
            n += 1
            bad += not all(leq(psiT[k], psiq[k]) for k in range(1, K))
        return n, bad
    n, bad = run(True); n2, bad2 = run(False)
    print(f"C  : {n} (monotone q, dominating table) pairs, violations of psi*_T <= psi_q: {bad};  "
          f"control (q not monotone): {bad2} of {n2} fail")
    return bad == 0


# ---------------------------------------------------------------- V-, V'
def path_cost(cost, n1):
    """Bellman: W(n) = min over paths n -> ... -> 0 inside {1..n1} of the summed one-step cost. cost[n][n']."""
    W = np.full(n1 + 1, math.inf); W[0] = 0
    for _ in range(n1 + 2):
        for n in range(1, n1 + 1):
            W[n] = min(W[n], min(cost[n][m] + W[m] for m in range(n1 + 1)))
    return W


def J_cost(row, n, m):
    """sup_s [ s (n - m) - ln M_n(s) ]."""
    j = np.nonzero(row)[0]
    if m < j.min() or m > j.max():
        return math.inf
    f = lambda s: -(s * (n - m) - float(logsumexp(-s * (j - n), b=row[j])))
    r = minimize_scalar(f, bounds=(-60, 60), method="bounded", options={"xatol": 1e-10})
    return -r.fun


def test_Vminus(rng, ntab=1200):
    n = bad = beat = ctrl = ctrl_bad = nl = bl = adm_bad = 0
    for it in range(ntab):
        n1 = int(rng.integers(4, 10)); nmax = n1 + int(rng.integers(1, 5))
        T = rand_table(rng, nmax, drift=rng.uniform(1.0, 3.0), jump=int(rng.integers(1, 4)))
        K = n1 + 1
        try:
            psi = committor(T, K)
        except np.linalg.LinAlgError:
            continue
        c0 = [[(-math.log(T[a, b]) if T[a, b] > 0 else math.inf) for b in range(n1 + 1)] for a in range(n1 + 1)]
        W0 = path_cost(c0, n1)
        if not np.isfinite(W0).all(): continue
        nl += n1; bl += sum(not leq(math.exp(-W0[k]), psi[k]) for k in range(1, K))
        Ws = [("W°", W0, 0.0)]
        if it % 4 == 0:
            cJ = [[(J_cost(T[a], a, b) if a >= 1 else math.inf) for b in range(n1 + 1)] for a in range(n1 + 1)]
            WJ = path_cost(cJ, n1)
            adm_bad += not all(WJ[a] - WJ[b] <= c0[a][b] + 1e-7 for a in range(1, K) for b in range(K))
            adm_bad += not all(WJ[a] <= W0[a] + 1e-7 for a in range(K))
            Ws.append(("W_J", WJ, 0.0))
        e = rng.uniform(0.05, 0.5); u = rng.random(n1 + 1) * 0.5; u[0] = 0
        Ws.append(("slack", W0 + e * u, e))
        Ws.append(("scaled", W0 * rng.random(), 0.0))
        Nn = [int((T[a, :n1 + 1] > 0).sum()) for a in range(n1 + 1)]
        for name, W, e in Ws:
            for delta in (0.5, 0.7, 0.85, 0.95, 1.0):
                for theta0 in (0.3, 0.7, 1.2, 2.0):
                    for k0 in (0, 1, 2):
                        good = all((math.exp(e) * Nn[a]) ** (1 - delta) * M(T[a], a, theta0) ** delta <= 1
                                   for a in range(k0 + 1, K))
                        W0bar = max(W[:k0 + 1])
                        cert = [max((1 - delta) * (W[a] - W0bar) + delta * theta0 * (a - k0), 0.0) for a in range(K)]
                        fails = not all(leq(psi[a], math.exp(-cert[a])) for a in range(1, K))
                        if good:
                            n += 1; bad += fails
                            beat += cert[n1] > theta0 * (n1 - k0) + 1e-9 and delta < 1
                        elif delta < 1:
                            ctrl += 1; ctrl_bad += fails
    print(f"V- : {n} cases with every block row good (W = W°, W_J, with slack, scaled), violations {bad}; "
          f"in {beat} the certificate at the top row exceeds theta0 (n1-k0)")
    print(f"     control (some row not good, delta < 1): the formula fails in {ctrl_bad} of {ctrl}")
    print(f"     psi* >= exp(-W°): {nl} rows, violations {bl};  W_J <= W° and W_J admissible: violations {adm_bad}")
    return bad == 0 and bl == 0 and adm_bad == 0


def test_Vprime(rng, ntab=3000):
    n = bad = ctrl = ctrl_bad = 0
    for _ in range(ntab):
        n1 = int(rng.integers(3, 9)); nmax = n1 + 2; K = n1 + 1
        eps = 10 ** rng.uniform(-5, -1.5)
        T = np.zeros((nmax + 1, nmax + 1)); T[0, 0] = 1
        for k in range(1, nmax + 1):
            for b in rng.choice(np.arange(0, k), size=min(k, int(rng.integers(1, 3))), replace=False):
                T[k, b] = eps * rng.uniform(0.2, 1)
            cand = np.arange(k + 1, nmax + 2)
            ups = rng.choice(cand, size=min(len(cand), int(rng.integers(1, 3))), replace=False)
            w = rng.random(len(ups)); w *= (1 - T[k].sum()) / w.sum()
            for b, x in zip(ups, w):
                T[k, min(b, nmax)] += x
        psi = committor(T, K)
        c0 = [[(-math.log(T[a, b]) if T[a, b] > 0 else math.inf) for b in range(K)] for a in range(K)]
        W = path_cost(c0, n1)
        if not np.isfinite(W).all(): continue
        for k0 in (0, 1):
            for delta in (0.3, 0.5, 0.7):
                for Wt, admissible in ((W, True), (3 * W, False)):
                    gains = [(Wt[b] - Wt[a], T[a, b]) for a in range(k0 + 1, K) for b in range(K) if T[a, b] > 0]
                    for c1 in sorted({round(g, 6) for g, _ in gains if g > 0})[:6]:
                        rare = [t for g, t in gains if g < c1 - 1e-12]
                        a_ = -math.log(max(rare)) if rare else 50.0
                        if a_ <= 0 or math.exp(-(1 - delta) * c1) + (n1 + 1) * math.exp(-delta * a_) > 1: continue
                        W0bar = max(Wt[:k0 + 1])
                        fails = not all(leq(psi[m], math.exp(-(1 - delta) * max(Wt[m] - W0bar, 0))) for m in range(1, K))
                        if admissible: n += 1; bad += fails
                        else: ctrl += 1; ctrl_bad += fails
    print(f"V' : {n} cases satisfying the hypothesis with W = W° (admissible, e = 0), violations {bad};  control "
          f"(W = 3 W°, not admissible, the two numerical conditions still met): {ctrl_bad} of {ctrl} fail")
    return bad == 0 and n > 0


# ---------------------------------------------------------------- E1, V-(E)
def mfold(base, m, k1):
    """Rows q_m(mk + r, .) = T_k^{*(m-r)} * T_{k+1}^{*r} for 1 <= n <= m k1. base[k] = law on {0,1,...}, base[0] = delta_0."""
    rows = {}
    for n in range(1, m * k1 + 1):
        k, r = divmod(n, m)
        row = np.array([1.0])
        for _ in range(m - r): row = np.convolve(row, base[k])
        for _ in range(r): row = np.convolve(row, base[k + 1])
        rows[n] = row
    return rows


def test_E(rng, ntab=40):
    e1 = 0.0; n = bad = good_fail = n2 = bad2 = 0
    for _ in range(ntab):
        k1 = int(rng.integers(2, 5)); Jmax = k1 + 3
        base = [np.array([1.0])]
        for k in range(1, k1 + 1):
            row = rand_row(rng, k, Jmax, rng.uniform(1.2, 2.5), 2, death=rng.uniform(0.005, 0.05))
            base.append(row / row.sum())
        th = [root(base[k], k) for k in range(1, k1 + 1)]
        if min(th) <= 0.05: continue
        lam = lambda k, s: math.log(M(base[k], k, s)) if k else 0.0
        for m in (2, 3, 5):
            rows = mfold(base, m, k1)
            n1 = m * k1; K = n1 + 1; nmax = max(len(r) for r in rows.values()) - 1
            T = np.zeros((nmax + 1, nmax + 1)); T[0, 0] = 1
            for a, r in rows.items(): T[a, :len(r)] = r
            for a in rows:                                   # Lemma E1
                k, r = divmod(a, m)
                for s in (-0.7, -0.2, 0.3, 1.1):
                    lhs = math.log(M(T[a], a, s))
                    rhs = (m - r) * lam(k, s) + (r * lam(k + 1, s) if r else 0.0)
                    e1 = max(e1, abs(lhs - rhs))
            psi = committor(T, K)
            cJ = [[(J_cost(T[a], a, b) if a >= 1 else math.inf) for b in range(K)] for a in range(K)]
            WJ = path_cost(cJ, n1)
            Nn = [int((T[a, :K] > 0).sum()) for a in range(K)]
            for k0b in (1, 2):
                if k0b >= k1: continue
                for theta0 in (0.25 * min(th), 0.5 * min(th), 0.8 * min(th)):
                    eps0 = -max(lam(k, theta0) for k in range(k0b, k1 + 1))
                    if eps0 <= 0: continue
                    for delta in (0.4, 0.6, 0.8, 0.95, 1.0):
                        if delta * m * eps0 < (1 - delta) * math.log(m * k1 + 1): continue      # (S)
                        k0 = m * k0b
                        good_fail += not all(Nn[a] ** (1 - delta) * M(T[a], a, theta0) ** delta <= 1 + 1e-12
                                             for a in range(k0 + 1, K))
                        W0bar = max(WJ[:k0 + 1])
                        n += 1
                        bad += not all(leq(psi[a], math.exp(-max((1 - delta) * (WJ[a] - W0bar) + delta * theta0 * (a - k0), 0)))
                                       for a in range(1, K))
            # "nothing subtracted": theta0 below every root, k0 = n0(delta) - 1, m >= max(m0, n0)
            theta0 = 0.5 * min(th)
            eps0 = -max(lam(k, theta0) for k in range(1, k1 + 1))
            J1 = int(np.nonzero(base[1])[0].max()); w1 = -math.log(base[1][0])
            for delta in (0.6, 0.8, 0.95):
                n0 = next(a for a in range(1, 10 ** 6) if delta * a * eps0 >= (1 - delta) * math.log(J1 * a + 1))
                if m < n0 or delta * m * eps0 < (1 - delta) * math.log(m * k1 + 1): continue
                n2 += 1
                bad2 += not all(leq(psi[a], math.exp(-((1 - delta) * (WJ[a] - n0 * w1) + delta * theta0 * (a - n0))))
                                for a in range(1, K))
    print(f"E1 : largest |ln M^(m)_n(s) - m Lambda_(n/m)(s)| over all rows, m = 2, 3, 5, four real s: {e1:.2e}")
    print(f"V-(E): {n} (base table, m, block, theta0, delta) cases satisfying (S): rows not good {good_fail}, "
          f"violations of the bound {bad}")
    print(f"       'nothing subtracted' form (k0 = n0(delta)-1): {n2} cases, violations {bad2}")
    return e1 < 1e-9 and bad == 0 and good_fail == 0 and bad2 == 0


if __name__ == "__main__":
    t = time.time()
    rng = np.random.default_rng(20261114)
    ok = True
    for f in (test_Tprime_T, test_X, test_C, test_Vminus, test_Vprime, test_E):
        ok &= bool(f(rng)); sys.stdout.flush()
    print(f"ALL OK: {ok}   ({time.time() - t:.0f} s)")
    sys.exit(0 if ok else 1)
