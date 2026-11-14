"""Critic's lab: path, closing round (journal entries 22-24; lab requests LR13, LR14). Exact arithmetic on small chains
written down by hand or drawn at random, on chains built from the curated tallies (data/fluct_tables.npz: pooled one-step
tables of the face population of gump hulls, A = 30, 45, 63, 84, rows k <= A/2), and on the tallies themselves. No runs.
Nothing here imports path's code (path/vminus_check.py is run separately for LR13).

  python3 path_r5.py hand     worked cases: Theorem V- (24.2), Theorem Q in its final form (23.2), and one hand-size chain
                              for each hypothesis of V- dropped in turn
  python3 path_r5.py random   Theorem V- and Corollary H on random tables with an ARBITRARY real W and its least slack;
                              two weaker forms of the hypotheses; three negative controls
  python3 path_r5.py family   Corollary V-(E) on exact m-fold families: the finite-m inequality from the threshold (S) on;
                              a family that keeps R with a margin and violates (E) only at large s (a one-step
                              catastrophe of probability e^{-cm}): the conclusion fails, Theorem Q's does not
  python3 path_r5.py tables   Theorem V- on each tallied table by itself (does any delta < 1 certify more than the block
                              bound?); V with its continuation, and with (E) asked only for 0 <= s <= s_max; the two
                              continuations against the tallies in kind; hypothesis (E) between every pair of tallied sizes
  python3 path_r5.py lr14     LR14: Phi, C+ at K = ceil(0.35 A) and ceil(0.45 A); condition B+ for W_J and W°; and the
                              entry term over ALL rows, those above A/2 included, from the histogram by the inflow identity
  python3 path_r5.py split    entry 24.7, point 3: convexity of k -> ln M_k(s) and the cost of an uneven split
  python3 path_r5.py all      (about three minutes on one core)
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import path_r2 as q2
import path_r4 as q4

AREA = {7: 30, 9: 45, 11: 63, 13: 84}
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ------------------------------------------------------------------------------------------------ tools
def committor(T):
    """T[n, n'] for n, n' in 0..n1 (row 0 unused; column 0 = death). Smallest non-negative solution of
    psi(n) = T[n, 0] + sum_{n' in 1..n1} T[n, n'] psi(n'), psi(0) = 1. Elimination without pivoting."""
    return np.concatenate([[1.0], q4.committor_pos(T[1:, 1:].copy(), T[1:, 0].copy())])


def lnM(row, n, s):
    nz = np.flatnonzero(row)
    e = np.log(row[nz]) - s * (nz - n)
    return float(e.max() + np.log(np.exp(e - e.max()).sum()))


def root(row, n):
    return q4.theta_of_row(row, n)


def legendre_row(row, n, ntgt):
    """J_n(n') = sup_{s real} [ s (n - n') - ln M_n(s) ] for n' = 0..ntgt-1, M_n the transform of the WHOLE row.
    Exact: +inf outside the hull of the support, -ln row[n'] at its two ends, and inside the unique s at which the
    tilted mean is n' (bisection, vectorised over the targets)."""
    nz = np.flatnonzero(row); lo, hi = int(nz.min()), int(nz.max())
    lw = np.log(row[nz]); st = (nz - n).astype(float)
    J = np.full(ntgt, np.inf)
    tg = np.arange(ntgt)
    if lo < ntgt: J[lo] = -np.log(row[lo])
    if hi < ntgt: J[hi] = -np.log(row[hi])
    inner = tg[(tg > lo) & (tg < hi)]
    if len(inner) == 0: return J
    a = np.full(len(inner), -80.0); b = np.full(len(inner), 80.0)

    def tilt(s):
        e = lw[None, :] - s[:, None] * st[None, :]
        mx = e.max(axis=1, keepdims=True)
        w = np.exp(e - mx)
        return (w * nz[None, :]).sum(1) / w.sum(1), mx[:, 0] + np.log(w.sum(1))
    for _ in range(70):
        mid = 0.5 * (a + b)
        mean, _ = tilt(mid)
        up = mean > inner                    # the tilted mean falls as s grows
        a = np.where(up, mid, a); b = np.where(up, b, mid)
    s = 0.5 * (a + b)
    _, lm = tilt(s)
    J[inner] = np.maximum(s * (n - inner) - lm, 0.0)
    return J


def shortest(cost):
    """largest W with W(0) = 0 and W(n) - W(n') <= cost[n, n'] for n >= 1: the cheapest path to 0 (Bellman-Ford)."""
    n1 = cost.shape[0] - 1
    c = cost.copy(); c[0, :] = np.inf
    W = np.full(n1 + 1, np.inf); W[0] = 0.0
    for _ in range(50 * n1 + 50):
        new = np.minimum(W, (c + W[None, :]).min(axis=1)); new[0] = 0.0
        if np.array_equal(new, W): break
        W = new
    return W


def w_path(T):
    with np.errstate(divide='ignore'):
        return shortest(-np.log(T))


def w_cramer(rows, n1):
    cost = np.full((n1 + 1, n1 + 1), np.inf)
    for n in range(1, n1 + 1):
        cost[n] = legendre_row(rows[n], n, n1 + 1)
    return shortest(cost)


def square(rows, n1):
    T = np.zeros((n1 + 1, n1 + 1))
    for n in range(1, n1 + 1):
        w = rows[n][:n1 + 1]; T[n, :len(w)] = w
    return T


def slack(T, W, k0, mode='full'):
    """least e >= 0 with W(n) - W(n') <= -ln T(n, n') + e on the rows k0 < n <= n1.
    mode 'full': all targets 0..n1 (the statement).  'weak': targets n' <= k0 are asked only against max_{j <= k0} W(j).
    'down': targets n' < n only (a negative control)."""
    n1 = T.shape[0] - 1
    wbar = W[:k0 + 1].max()
    e = 0.0
    for n in range(k0 + 1, n1 + 1):
        for t in np.flatnonzero(T[n]):
            if mode == 'down' and t >= n: continue
            ref = wbar if (mode == 'weak' and t <= k0) else W[t]
            e = max(e, W[n] - ref + np.log(T[n, t]))
    return e


def goodness(T, full, n, th0, delta, e, form='statement'):
    """ln of the left side of (G) at row n. 'statement': (e^e N_n)^(1-delta) M_n(th0)^delta, M over the whole row;
    'sharp': e^((1-delta) e) sum_{n' <= n1} [T e^{-th0 (n'-n)}]^delta; 'nocount': M_n(th0)^delta alone (negative control)."""
    nz = np.flatnonzero(T[n])
    if len(nz) == 0: return -np.inf
    if form == 'sharp':
        return (1 - delta) * e + np.log(np.exp(delta * (np.log(T[n, nz]) - th0 * (nz - n))).sum())
    lm = lnM(full[n], n, th0)
    if form == 'nocount': return delta * lm
    return (1 - delta) * (e + np.log(len(nz))) + delta * lm


def exponent(W, k0, th0, delta):
    """the certified exponent of Theorem V-: [(1 - delta)(W(n) - max_{j<=k0} W(j)) + delta th0 (n - k0)]^+."""
    n = np.arange(len(W))
    return np.maximum((1 - delta) * (W - W[:k0 + 1].max()) + delta * th0 * (n - k0), 0.0)


# ------------------------------------------------------------------------------------------------ hand
def hand():
    print("Worked cases")
    r3 = np.sqrt(3.0)
    # the walk on {0,1,2,3}, up 3/4, down 1/4; low set {1, 2}
    full = [None, np.array([.25, 0, .75, 0]), np.array([0, .25, 0, .75])]
    T = square(full, 2)
    psi = committor(T); W = w_path(T)
    check(abs(psi[1] - 4 / 13) < 1e-14 and abs(psi[2] - 1 / 13) < 1e-14 and abs(W[2] - 2 * np.log(4)) < 1e-14,
          "walk on {0..3}, up 3/4: psi*(1) = 4/13, psi*(2) = 1/13; W°(2) = 2 ln 4 = 2.773 >= -ln psi*(2) = 2.565")
    th0 = np.log(r3)
    dmin = np.log(2) / (np.log(2) - lnM(full[1], 1, th0))
    g = exponent(W, 0, th0, 0.9)[2]
    check(abs(np.exp(lnM(full[1], 1, th0)) - (r3 / 4 + .75 / r3)) < 1e-14 and abs(dmin - 0.828) < 5e-4 and abs(g - 1.266) < 5e-4 and g <= -np.log(psi[2]),
          f"   e^theta0 = sqrt 3: M = 0.866; row 1 (two targets) is good iff delta >= {dmin:.3f}; delta = 0.9, k0 = 0: certified {g:.3f} <= 2.565  [path's smallest case]")
    # (G) dropped, and the count N_n dropped from (G): same walk, delta = 0.05
    g = exponent(W, 0, th0, 0.05)[2]
    check(goodness(T, full, 1, th0, 0.05, 0.0) > 0 and goodness(T, full, 1, th0, 0.05, 0.0, 'nocount') <= 0 and g > -np.log(psi[2]),
          f"   (G) is needed, and so is the count of targets in it: delta = 0.05, row 1 has M = 0.866 <= 1 (R holds) and is not good; "
          f"the formula would give {g:.3f} > -ln psi*(2) = {-np.log(psi[2]):.3f}")
    # (B) on rising targets dropped
    eta, c = 1e-6, 0.01
    full = [None, np.array([eta, 0, 1 - eta, 0]), np.array([c, 0, 0, 1 - c])]
    T = square(full, 2); psi = committor(T)
    W = np.array([0.0, -np.log(eta), -np.log(c)])                 # the cost of the cheapest DECREASING path
    ok_down = slack(T, W, 0, 'down') == 0.0 and slack(T, W, 0, 'full') > 9
    good = all(goodness(T, full, n, 1.0, 0.5, 0.0) <= 0 for n in (1, 2))
    g = exponent(W, 0, 1.0, 0.5)[1]
    check(ok_down and good and g > -np.log(psi[1]) + 2,
          f"   (B) is needed at RISING targets: rows 1 -> 0 w.p. 1e-6, else 2; 2 -> 0 w.p. 0.01, else 3; low set {{1, 2}}; W = cost of the cheapest "
          f"decreasing path (13.82, 4.61) satisfies (B) at every target below the row and fails it at 1 -> 2; both rows are good at theta0 = 1, delta = 1/2; "
          f"the formula would give {g:.3f} at row 1, and -ln psi*(1) = {-np.log(psi[1]):.3f}")
    # W(0) = 0 is a normalisation: shift W
    # Theorem Q, final form: walk on {0..3}, up 3/4, held at 3; K = 3, k0 = 0, theta0 = ln 3
    P = np.array([[0, .75, 0], [.25, 0, .75], [0, .25, .75]])      # states 1, 2, 3 (death = missing mass of row 1)
    ev, vec = np.linalg.eig(P.T); i = int(np.argmax(ev.real)); p = np.abs(vec[:, i].real); p /= p.sum(); h = 1 - ev.real[i]
    th0 = np.log(3.0)
    Phi = p[2] * .25 * np.exp(th0 * (3 - 2)); Cp = .25 * 3 + .75
    w = p[0] * np.exp(-th0 * 1) + p[1] * np.exp(-th0 * 2)          # mean of the certificate over the living law (boundary term)
    bound = Phi * np.exp(-th0 * 3) / (1 - w)
    check(abs(Phi - 0.538) < 1e-3 and Cp == 1.5 and Phi <= Cp and abs(bound - 0.0208) < 1e-4 and abs(h - 0.0143) < 1e-4 and h <= bound,
          f"Theorem Q (23.2), smallest case: Phi = 3/4 p3 = {Phi:.3f} <= C+ = 1.5; bound (Phi/27)/(1 - w) = {bound:.4f} >= h = {h:.4f}")


# ------------------------------------------------------------------------------------------------ random
def random_table(rng, n1):
    """rows 1..n1 on targets 0..n1+10: a few targets each, most of the mass going up; long jumps and direct deaths allowed;
    censored mass in a third of the tables."""
    full = [None]
    cens = rng.random() < 1 / 3
    for n in range(1, n1 + 1):
        row = np.zeros(n1 + 11)
        for u in rng.integers(1, 8, size=int(rng.integers(1, 3))):
            row[n + u] += rng.random()
        row /= row.sum()
        down = 10.0 ** rng.uniform(-5, -0.7)
        row *= 1 - down
        tg = rng.integers(0, n, size=int(rng.integers(1, 3)))
        w = rng.random(len(tg))
        for t, x in zip(tg, w): row[t] += down * x / w.sum()
        if cens: row *= rng.uniform(0.6, 1.0)
        full.append(row)
    return full


def stationary(full, n1, top):
    """the chain on 1..top (rows above n1 drawn like the others), restarted at `top` at death and for mass thrown above top
    or censored; returns the law mu on 1..top and the full rows."""
    P = np.zeros((top, top))
    for z in range(1, top + 1):
        w = full[z][1:top + 1]; P[z - 1, :len(w)] = w
        P[z - 1, top - 1] += 1.0 - P[z - 1].sum()
    return q4.gth(P[::-1, ::-1].copy())[::-1]


def random_checks(trials=4000, seed=7):
    print("Theorem V- (24.2) and Corollary H (24.4) on random tables; W is any real function (not built from the table), e its least slack")
    rng = np.random.default_rng(seed)
    cnt = dict(stmt=0, sharp=0, weak=0, beat=0, H=0, Hbeat=0)
    worst = dict(stmt=np.inf, sharp=np.inf, weak=np.inf, H=np.inf, Hid=0.0)
    neg = dict(down=[0, 0], nocount=[0, 0], noG=[0, 0])
    for t in range(trials):
        n1 = int(rng.integers(4, 16)); top = n1 + 6
        full = random_table(rng, top)
        T = square(full, n1)
        psi = committor(T)
        if (psi[1:] <= 0).any(): continue
        lp = -np.log(psi)
        Wo = w_path(T)
        if not np.isfinite(Wo).all(): continue
        kind = t % 4
        if kind == 0: W = Wo.copy()
        elif kind == 1: W = rng.uniform(0.3, 1.1) * Wo + rng.normal(0, 0.3, n1 + 1)
        elif kind == 2: W = np.sort(rng.uniform(0, Wo.max(), n1 + 1)); W[0] = 0.0 if rng.random() < .5 else W[0]
        else:                                                   # the cheapest DECREASING path: admissible at lower targets only
            with np.errstate(divide='ignore'):
                W = shortest(np.where(np.arange(n1 + 1)[None, :] < np.arange(n1 + 1)[:, None], -np.log(T), np.inf))
            W = np.where(np.isfinite(W), W, Wo)
        if kind == 1 and rng.random() < .5: W = W + rng.normal(0, 2.0)     # W(0) != 0: a constant shift must not matter
        mu = stationary(full, n1, top)
        hz = float(sum(mu[z - 1] * full[z][0] for z in range(1, top + 1)))
        for delta in (0.3, 0.5, 0.7, 0.9, 1.0):
            for th0 in rng.uniform(0.05, 2.0, size=2):
                for k0 in sorted(set(int(x) for x in rng.integers(0, n1, size=2))):
                    e_full = slack(T, W, k0); e_weak = slack(T, W, k0, 'weak'); e_down = slack(T, W, k0, 'down')
                    g = exponent(W, k0, th0, delta)
                    block = range(k0 + 1, n1 + 1)
                    gap = float((lp[1:] - g[1:]).min())
                    for form, e in (('stmt', e_full), ('sharp', e_full)):
                        if all(goodness(T, full, n, th0, delta, e, 'statement' if form == 'stmt' else 'sharp') <= 0 for n in block):
                            cnt[form] += 1; worst[form] = min(worst[form], gap)
                            if form == 'stmt' and delta < 1 and g[n1] > th0 * (n1 - k0) + 1e-9: cnt['beat'] += 1
                    # weak form: (B) at targets <= k0 only against W-bar; (G), sharp, only at rows where the exponent is positive
                    if all(goodness(T, full, n, th0, delta, e_weak, 'sharp') <= 0 for n in block if g[n] > 0):
                        cnt['weak'] += 1; worst['weak'] = min(worst['weak'], gap)
                    # negative controls
                    if delta < 1:
                        if e_down < e_full - 1e-9 and all(goodness(T, full, n, th0, delta, e_down) <= 0 for n in block):
                            neg['down'][1] += 1; neg['down'][0] += int(gap < -1e-9)
                        if all(goodness(T, full, n, th0, delta, e_full, 'nocount') <= 0 for n in block):
                            neg['nocount'][1] += 1; neg['nocount'][0] += int(gap < -1e-9)
                        neg['noG'][1] += 1; neg['noG'][0] += int(gap < -1e-9)
                    # Corollary H on the restarted chain: h = sum_{z >= K} mu_z sum_{z' <= n1} T(z, z') psi*(z') exactly (restart outside the low set)
                    if all(goodness(T, full, n, th0, delta, e_full) <= 0 for n in block):
                        K = n1 + 1
                        zs = [z for z in range(K, top + 1) if mu[z - 1] > 0]
                        ident = sum(mu[z - 1] * float(full[z][:K] @ psi) for z in zs)
                        worst['Hid'] = max(worst['Hid'], abs(ident / hz - 1))
                        cert = np.exp(-g)
                        Phi = sum(mu[z - 1] * float(full[z][:K] @ cert) for z in zs)
                        Cp = max(np.exp(lnM(full[z], z, th0) - th0 * (z - K)) for z in zs)
                        eB = e_full
                        for z in zs:
                            for zp in np.flatnonzero(full[z][:K]):
                                eB = max(eB, W[n1] - W[zp] + np.log(full[z][zp]))
                        if not all(goodness(T, full, n, th0, delta, eB) <= 0 for n in block): continue
                        closed = (1 - delta) * (eB + np.log(K)) + delta * np.log(Cp) - ((1 - delta) * (W[n1] - W[:k0 + 1].max()) + delta * th0 * (K - k0))
                        cnt['H'] += 1
                        worst['H'] = min(worst['H'], min(np.log(Phi) - np.log(hz), closed - np.log(Phi)))
                        cnt['Hbeat'] += int(delta < 1)
    check(worst['stmt'] >= -1e-9 and worst['sharp'] >= -1e-9 and cnt['stmt'] > 5000,
          f"Theorem V-: {cnt['stmt']} cases with every block row good as stated ({cnt['beat']} of them with delta < 1 and a certificate above the block bound), "
          f"{cnt['sharp']} in the sharp form: -ln psi* >= the certified exponent at every row (smallest gap {worst['stmt']:.1e}, {worst['sharp']:.1e})")
    check(worst['weak'] >= -1e-9 and cnt['weak'] >= cnt['sharp'],
          f"   a weaker set of hypotheses is enough ({cnt['weak']} cases, smallest gap {worst['weak']:.1e}): W any real function (W(0) = 0 is a normalisation); "
          f"(B) at targets n' <= k0 asked only against max_(j<=k0) W(j); (G) asked only at rows where the certified exponent is positive")
    check(neg['down'][0] > 0 and neg['nocount'][0] > 0 and neg['noG'][0] > 0,
          f"   negative controls (delta < 1), violations / cases: (B) asked at lower targets only {neg['down'][0]}/{neg['down'][1]}; "
          f"(G) without the count of targets {neg['nocount'][0]}/{neg['nocount'][1]}; (G) dropped {neg['noG'][0]}/{neg['noG'][1]}")
    check(worst['H'] >= -1e-9 and worst['Hid'] < 1e-9 and cnt['H'] > 1000,
          f"Corollary H on the restarted chain with its own stationary law: {cnt['H']} cases ({cnt['Hbeat']} with delta < 1): hazard = entry flux x psi* "
          f"(largest relative error {worst['Hid']:.1e}); hazard <= Phi[psi] <= (e^e K)^(1-delta) (C+)^delta exp(-[...]) with the least C+ and e of R+, B+ (smallest margin {worst['H']:.1e} nats)")


# ------------------------------------------------------------------------------------------------ family
def binom_row(n, p, mult=2):
    """law of mult * Bin(n, p) on 0..mult n."""
    from math import lgamma
    k = np.arange(n + 1)
    lg = np.array([lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) for i in k])
    w = np.exp(lg + k * np.log(p) + (n - k) * np.log(1 - p))
    out = np.zeros(mult * n + 1); out[::mult] = w
    return out


def family():
    print("Corollary V-(E) on exact m-fold families")
    # (i) a base table whose cheapest route to death has many steps, with a margin large enough for the threshold (S) to be reached:
    #     rows k = 1..4; from k cells each cell leaves 2 cells, or none with probability c_k = 0.10, 0.15, 0.20, 0.25
    cs = [None, 0.10, 0.15, 0.20, 0.25]
    base = [np.array([1.0])] + [binom_row(k, 1 - cs[k]) for k in range(1, 5)]
    th = [root(base[k], k) for k in range(1, 5)]
    print("   (i) base rows k = 1..4: each of the k cells leaves 2 cells, or none with probability 0.10, 0.15, 0.20, 0.25; roots " + ', '.join(f"{t:.3f}" for t in th))
    allok = True; lines = []; seen = 0
    th0 = 0.5
    eps = min(-lnM(base[k], k, th0) for k in range(1, 5))        # margin per patch on the block (1, 4]: integer rows 1..4
    for m in (1, 2, 4, 8, 16, 32, 48):
        rows = q4.mfold(base, m); n1 = 4 * m
        T = square(rows, n1); psi = committor(T); lp = -np.log(psi)
        WJ = w_cramer(rows, n1); Wo = w_path(T)
        allok = allok and bool((lp <= Wo + 1e-9).all()) and bool((WJ <= Wo + 1e-9).all())
        line = f"      m = {m:2d}: -ln psi*(4m)/m = {lp[n1] / m:.4f}; W_J(4m)/m = {WJ[n1] / m:.4f}; W°(4m)/m = {Wo[n1] / m:.4f};"
        for delta in (0.5, 0.3):
            k0 = m                                                  # block (1, 4] in patch units
            S = delta * m * eps >= (1 - delta) * np.log(4 * m + 1)
            g = exponent(WJ, k0, th0, delta)
            good = all(goodness(T, rows, n, th0, delta, 0.0) <= 0 for n in range(k0 + 1, n1 + 1))
            holds = bool((lp[1:] >= g[1:] - 1e-9).all())
            if S: allok = allok and good and holds; seen += 1
            line += f" delta {delta}: (S) {'holds' if S else 'fails'}, rows {'good' if good else 'not all good'}, certified {g[n1] / m:.3f}{'' if holds else ' (VIOLATED)'};"
        lines.append(line)
    print('\n'.join(lines))
    check(allok and seen >= 4, f"   margin eps0 = {eps:.3f} nats per patch at theta0 = {th0}; wherever (S) holds every block row is good and -ln psi*_m(n) >= (1 - delta)(W_J(n) - W-bar) + delta theta0 (n - m) at every row "
                 "(W_J = m V on the chain's own lattice); psi* >= e^(-W°) and W_J <= W° always")
    # (ii) (E) violated at large s only. Base: Galton-Watson, each cell leaves 2 cells or none (1/4): V(x) = x ln 3 exactly.
    #      m-fold chain = the same branching process on n cells. Add a one-step catastrophe of probability e^{-c m} from every row.
    print("   (ii) each cell leaves 2 cells or none (probability 1/4): root ln 3 in every row, V(x) = x ln 3, low set {1..3m}; block (1, 3]; V(3) - V-bar = 2 ln 3 = 2.197.")
    th0, c = 0.3, 1.3
    percell = -lnM(binom_row(1, .75), 1, th0)
    out = {}
    for m in (12, 24, 48, 96):
        n1 = 3 * m
        res = {}
        for cat in (False, True):
            rows = [np.array([1.0])]
            for n in range(1, n1 + 1):
                r = binom_row(n, .75)
                if cat:
                    r = r * (1 - np.exp(-c * m)); r[0] += np.exp(-c * m)
                rows.append(r)
            T = square(rows, n1); psi = committor(T)
            marg = min(-lnM(rows[n], n, th0) for n in range(m + 1, n1 + 1)) / m
            # (E) against the base rates, at the largest s where it matters: direct death from the top row
            edef = np.log(rows[n1][0]) - n1 * np.log(.25)
            # the tilts at which (E) against the base rates (e_m = ln 2) fails at the top row: ln M_n(s) > n Lam_1(s) + ln 2
            sfail = next((sv for sv in np.arange(0.0, 3.0, 0.005) if lnM(rows[n1], n1, sv) > n1 * lnM(binom_row(1, .75), 1, sv) + np.log(2)), np.nan)
            res[cat] = (-np.log(psi[n1]) / m, marg, edef / m, sfail)
        delta = 0.5
        S = delta * m * res[True][1] >= (1 - delta) * np.log(3 * m + 1)
        bound = (1 - delta) * 2 * np.log(3) + delta * th0 * 2
        out[m] = (res, S, bound)
        print(f"      m = {m:2d}: without the catastrophe -ln psi*(3m)/m = {res[False][0]:.4f}; with it {res[True][0]:.4f} (margin of R at theta0 = {th0}: {res[True][1]:.4f} per patch; "
              f"(E) against the base rates, e_m = ln 2, holds at the top row for s < {res[True][3]:.3f} and fails beyond, by {res[True][2]:.3f} m nats as s -> inf); "
              f"delta = 1/2: (S) {'holds' if S else 'fails'}; the corollary's bound with the base V would be {bound:.3f}; Theorem Q's is {th0 * 2:.3f}")
    r96 = out[96]
    check(r96[1] and r96[0][True][0] < r96[2] - 0.09 and r96[0][False][0] >= r96[2] and r96[0][True][0] >= th0 * 2 and r96[0][True][1] > 0.1 and r96[0][True][3] > th0,
          f"   catastrophe of probability e^(-{c} m): R holds with a margin and (S) holds, yet -ln psi*/m <= {c} < {r96[2]:.3f}: the conclusion with the base table's V FAILS; "
          "(E) holds at theta0 and fails only at larger tilts: (E) beyond theta0 is what carries V (a bound on one-step events of probability e^(-cm), direct deaths included); Theorem Q's exponent survives")


# ------------------------------------------------------------------------------------------------ tables
def bellman(Tb, KM, sub, floor, sgrid, cap=None, inflate=0.0, top=None):
    """S on the grid x = j / sub, 0 <= x <= KM - 1, of the recursion S(x) = min_y [I(x -> y) + S(y)], S(0) = 0, with
    I(x -> y) = sup over the grid of s of s (x - y) - Lam_x(s); Lam_x = linear interpolation of the rows' ln M_k (below `floor`:
    (x / floor) Lam_floor, 'clusters'). cap = 'root': only 0 <= s <= the root of Lam_x. inflate = eta: Lam_x(s) multiplied by
    1 + eta wherever it is positive (the transform beyond the root made larger). top: the low set is [0, top] (default: the top tallied row);
    rising steps are allowed inside the low set and not beyond it."""
    Lam = q4.cramer_tables(Tb, KM, sgrid)
    G = (KM - 1 if top is None else top) * sub; xg = np.arange(G + 1) / sub
    cost = np.full((G + 1, G + 1), np.inf)
    for i in range(1, G + 1):
        x = xg[i]; k = int(np.floor(x)); f = x - k
        L = (x / floor) * Lam[floor] if (floor and x < floor) else (Lam[k] if f == 0 else (1 - f) * Lam[k] + f * Lam[min(k + 1, KM - 1)])
        sg = sgrid
        if inflate: L = np.where(L > 0, (1 + inflate) * L, L)
        if cap == 'root':
            keep = (sgrid >= 0) & (L <= 1e-12)
            L = L[keep]; sg = sgrid[keep]
        cost[i] = (-np.outer(xg - x, sg) - L[None, :]).max(axis=1)
    return shortest(np.maximum(cost, 0.0))


def tables():
    print("Theorem V- on each tallied table by itself (sharp form of (G); W = W_J and W°; delta from 0.30 to 0.995 and 1; theta0 from 0.01 to 0.70)")
    deltas = [0.3, 0.5, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.97, 0.98, 0.99, 0.995, 1.0]
    gains = []; dbest = []
    for R in (9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        rows = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KM)]
        for top in (0.35, 0.45, 0.5):
            n1 = min(int(np.ceil(top * A)) - 1, KM - 1)
            T = square(rows, n1); lp = -np.log(committor(T))
            best = {}
            for name, W in (("W_J", w_cramer(rows, n1)), ("W°", w_path(T))):
                for delta in deltas:
                    for th0 in np.arange(0.01, 0.705, 0.01):
                        bad = [n for n in range(1, n1 + 1) if goodness(T, rows, n, th0, delta, 0.0, 'sharp') > 0]
                        n0 = (max(bad) + 1) if bad else 1
                        if n0 > n1: continue
                        g = exponent(W, n0 - 1, th0, delta)
                        key = name if delta < 1 else 'block'
                        if key not in best or g[n1] > best[key][0]: best[key] = (g[n1], delta, th0, n0)
            blk = best['block'][0]
            sub = {k: v for k, v in best.items() if k != 'block'}
            gains.append(max(v[0] for v in sub.values()) - blk); dbest.append(min(v[1] for v in sub.values() if v[0] > blk) if gains[-1] > 0 else 1.0)
            print(f"   A = {A}, low set to {top} A (n1 = {n1}): -ln psi*(n1) = {lp[n1]:.2f}; block bound (delta = 1) {blk:.2f} at theta0 = {best['block'][2]:.2f}, rows from {best['block'][3]}; best with delta < 1: "
                  + '; '.join(f"{k}: {v[0]:.2f} (delta {v[1]}, theta0 {v[2]:.2f}, rows from {v[3]})" for k, v in sub.items()))
    check(max(gains) < 0.5 and min(dbest) >= 0.96,
          f"on the tallied tables a delta < 1 adds at most {max(gains):.2f} nats to the block bound, and only with delta >= {min(dbest)}: "
          "at the measured sizes Theorem V- says what Theorem Q says (path's 'no delta < 1 makes the rows good' is for delta <= 0.9)")

    print("V of the A = 84 table (value of the recursion, per cell of the face; grids of 1/4 and 1/8 cell, extrapolated) at the top tallied row | at row 29 = 0.35 A")
    Tr, N, Tb = q2.table(13); KM = Tr.shape[0]; A = 84
    pos = np.concatenate([[0.0], np.geomspace(1e-3, 60, 500)])
    full = np.concatenate([-pos[:0:-1], pos])
    th29 = root(Tb[29], 29)

    def V(floor, sg, **kw):
        a, b = bellman(Tb, KM, 4, floor, sg, **kw), bellman(Tb, KM, 8, floor, sg, **kw)
        return (2 * b[-1] - a[-1]) / A, (2 * b[29 * 8] - a[29 * 4]) / A
    vals = {}
    for label, floor in (("c0, rows 1-4 as tallied", 0), ("c1, clusters of 5 below row 5", 5)):
        line = f"   {label}:"
        for sname, sg, kw in (("all real s", full, {}), ("s >= 0", pos, {}), ("s <= 0.7", pos[pos <= 0.7], {}), ("s <= 0.6", pos[pos <= 0.6], {}), ("s <= 0.5", pos[pos <= 0.5], {}),
                              ("s <= 0.4", pos[pos <= 0.4], {}), ("s <= 0.3", pos[pos <= 0.3], {}), ("s <= the row's own root", pos, dict(cap='root')),
                              ("transform x 1.1 beyond the root", pos, dict(inflate=0.1)), ("x 1.2", pos, dict(inflate=0.2)), ("x 1.5", pos, dict(inflate=0.5))):
            if floor == 0 and sname not in ("all real s", "s >= 0"): continue
            vals[(floor, sname)] = V(floor, sg, **kw)
            line += f" {sname}: {vals[(floor, sname)][0]:.4f} | {vals[(floor, sname)][1]:.4f};"
        print(line)
    v = lambda f, n: vals[(f, n)][0]
    check(abs(v(0, "all real s") - 0.2054) < 6e-4 and abs(v(5, "all real s") - 0.2191) < 6e-4 and abs(v(0, "s >= 0") - v(0, "all real s")) < 1e-6
          and abs(v(5, "s >= 0") - v(5, "all real s")) < 1e-6 and abs(v(5, "s <= 0.7") - v(5, "all real s")) < 3e-4 and v(5, "s <= 0.5") < v(5, "all real s") - 0.01,
          "0.2054 (c0) and 0.2191 (c1) reproduced (0.2056 on these grids). Rates with s >= 0 only give the same V; with s <= 0.7 too; with s <= 0.5 V is lower by 0.018: "
          "(E) is needed, at EVERY row of the block, for 0 <= s <= the largest root of the table (0.6), not for all real s")
    capped = {}
    for nm, kw in (("all s >= 0", {}), ("s <= the row's own root", dict(cap='root'))):
        a, b = bellman(Tb, KM, 4, 5, pos, top=29, **kw), bellman(Tb, KM, 8, 5, pos, top=29, **kw)
        capped[nm] = 2 * b[-1] - a[-1]
    print(f"   low set [0, 0.35 A] (rows 1..29), c1: all s >= 0: {capped['all s >= 0']:.2f} nats = {capped['all s >= 0'] / A:.4f} per cell; "
          f"s <= the row's own root: {capped[chr(115) + ' <= the row' + chr(39) + 's own root']:.2f} nats; 29 x theta_29 = {th29 * 29:.2f}")
    check(abs(capped["s <= the row's own root"] - th29 * 29) < 0.15,
          "with (E) asked only up to each row's own root, the quasi-potential of the low set [0, 0.35 A] is x Theta(x) = Theorem Q's block bound (0.144 per cell): "
          "everything V adds to Q comes from (E) at tilts ABOVE the row's root. (In a larger low set it is smaller still: the path may rise for nothing to a row with a smaller root.)")

    print("The two continuations against the tallies in kind: roots of rows 1..8 of the 2-fold chain of a table (c0 | finite form of c1) against the measured rows of the table nearest in size")
    for Rs, Rb in ((7, 11), (9, 13)):
        As, Ab = AREA[Rs], AREA[Rb]
        Trs, Ns, Tbs = q2.table(Rs); KMs = Trs.shape[0]
        rows = [np.array([1.0])] + [Tbs[k].copy() for k in range(1, KMs)]
        Trb, Nb, Tbb = q2.table(Rb)
        meas = [root(Tbb[k], k) for k in range(1, 9)]
        c0 = [root(r, i) for i, r in enumerate(q4.mfold(rows, 2)[:9]) if i]
        c1 = [root(r, i) for i, r in enumerate(q4.mfold(rows, 2, floor=5)[:9]) if i]
        print(f"   2 x {As} = {2 * As} cells: c0 " + ' '.join(f"{t:.3f}" for t in c0) + "\n" + ' ' * 22 + "c1 " + ' '.join(f"{t:.3f}" for t in c1)
              + f"   (in the limit c1 has the root of row 5, {root(Tbs[5], 5):.3f}, at every sparse row)\n      measured, A = {Ab}:  " + ' '.join(f"{t:.3f}" for t in meas))
        if Rs == 9:
            check(all(meas[i] - c0[i] > 0.13 for i in (2, 3, 4, 5)) and abs(c1[3] - meas[3]) < 0.1,
                  f"   c0 puts the small roots of rows 1, 2 of the table at rows 2-4 of the doubled face and is contradicted by the measured face of {Ab} cells at rows 3-6 "
                  f"({', '.join(f'{c0[i]:.2f}' for i in (2, 3, 4, 5))} against {', '.join(f'{meas[i]:.2f}' for i in (2, 3, 4, 5))}); c1 is not contradicted and not established")

    print("Hypothesis (E) between tallied sizes: is ln M_n(s) of the larger table <= (A'/A) Lam_(n A/A')(s), Lam the interpolated rows of the smaller? (e = 0; m = A'/A need not be an integer)")
    print("   defect = ln M' - m Lam, nats (negative = sub-extensive); rows n of the larger table from x0 = 5 cells of the smaller up to the smaller table's top row")
    # the code on a pair that is exactly extensive: the 2-fold chain of the A = 45 table against that table
    Trs, Ns, Tbs = q2.table(9); KMs = Trs.shape[0]
    rows2 = q4.mfold([np.array([1.0])] + [Tbs[k].copy() for k in range(1, KMs)], 2)

    def defect(rowb, n, Tsm, KMsm, m, s):
        x = n / m; k = int(np.floor(x + 1e-12)); f = x - k
        if f < 1e-9: f = 0.0
        if x < 5 or k + (1 if f > 0 else 0) > KMsm - 1: return None
        lam = (1 - f) * lnM(Tsm[k], k, s) + (f * lnM(Tsm[k + 1], k + 1, s) if f > 0 else 0.0)
        return lnM(rowb, n, s) - m * lam
    zero = max(abs(defect(rows2[n], n, Tbs, KMs, 2.0, s)) for n in range(10, 2 * (KMs - 1) + 1) for s in (0.2, 0.6, 1.0))
    check(zero < 1e-9, f"   the test on an exactly extensive pair (the 2-fold chain of the A = 45 table against that table): largest |defect| {zero:.1e}")
    sgr = np.arange(0.02, 1.001, 0.02)
    stats_ = {}
    for Rs, Rb in ((7, 9), (7, 11), (7, 13), (9, 11), (9, 13), (11, 13)):
        As, Ab = AREA[Rs], AREA[Rb]; m = Ab / As
        Trs, Ns, Tbs = q2.table(Rs); KMs = Trs.shape[0]
        Trb, Nb, Tbb = q2.table(Rb); KMb = Trb.shape[0]
        rowsn = [n for n in range(1, KMb) if defect(Tbb[n], n, Tbs, KMs, m, 0.1) is not None]
        D = np.array([[defect(Tbb[n], n, Tbs, KMs, m, s) for s in sgr] for n in rowsn])
        th = np.array([root(Tbb[n], n) for n in rowsn])
        below = np.array([[s <= t for s in sgr] for t in th])                 # s up to the row's own root
        worst_below = D[below].max()
        frac_below = float((D[below] > 0).mean())
        above = ~below
        frac_above = float((D[above] > 0).mean())
        upper = np.array(rowsn) > 0.3 * Ab
        i6 = int(np.argmin(abs(sgr - 0.6))); i10 = len(sgr) - 1; i3 = int(np.argmin(abs(sgr - 0.3)))
        lm6 = np.array([lnM(Tbb[n], n, 0.6) for n in rowsn])
        stats_[(As, Ab)] = (worst_below, frac_below, frac_above, D[:, i3].max(), D[upper][:, i6].max(), float((D[upper][:, i6] / lm6[upper]).max()))
        print(f"   {As} -> {Ab} (m = {m:.3f}, rows {rowsn[0]}..{rowsn[-1]}): for s up to the row's root: largest defect {worst_below:+.3f}, positive in {100 * frac_below:.1f}% of (row, s); "
              f"beyond the root: positive in {100 * frac_above:.0f}%; at s = 0.3: max {D[:, i3].max():+.3f}; rows above 0.3 A', s = 0.6: max {D[upper][:, i6].max():+.3f} "
              f"({100 * stats_[(As, Ab)][5]:.0f}% of ln M'), {int((D[upper][:, i6] > 0).sum())}/{int(upper.sum())} rows positive; s = 1.0: max {D[upper][:, i10].max():+.3f}")
    check(all(v[0] < 0.02 and v[1] < 0.05 for v in stats_.values()) and all(v[4] > 0.05 for v in stats_.values()),
          "in all six pairs (E) with the smaller table's rates HOLDS for s up to each row's own root (the part that gives Theorem Q) and FAILS beyond it on the rows above 0.3 A' "
          "(part of what V needs): there the larger face's transform exceeds the m-fold of the smaller's, by more the further apart the sizes")

    print("Admissibility itself (the hypothesis of 24.2, weaker than (E)): W(n) = m V_small(n / m) on the larger table, least slack e over the rows n > 5 m and all targets (c1 below row 5)")
    adm = []
    for Rs, Rb in ((9, 13), (11, 13), (9, 11)):
        As, Ab = AREA[Rs], AREA[Rb]; m = Ab / As
        Trs, Ns, Tbs = q2.table(Rs); KMs = Trs.shape[0]
        Trb, Nb, Tbb = q2.table(Rb); KMb = Trb.shape[0]
        S = bellman(Tbs, KMs, 8, 5, pos)
        n1 = min(int(np.floor(m * (KMs - 1))), KMb - 1)
        W = m * np.interp(np.arange(n1 + 1) / m, np.arange(len(S)) / 8, S)
        T = square([np.array([1.0])] + [Tbb[k].copy() for k in range(1, KMb)], n1)
        k0 = int(np.ceil(5 * m))
        e = slack(T, W, k0)
        arg = max(((W[n] - W[t] + np.log(T[n, t]), n, int(t)) for n in range(k0 + 1, n1 + 1) for t in np.flatnonzero(T[n])))
        adm.append(arg[0])
        print(f"   {As} -> {Ab}: W(n1 = {n1}) = {W[n1]:.2f}; largest W(n) - W(n') + ln T'(n, n') = {arg[0]:+.3f} (at {arg[1]} -> {arg[2]}): least slack e = {e:.3f}")
    check(max(adm) <= 0, "the scaled quasi-potential of the smaller table is admissible for the larger one with e = 0 in the three pairs: at these sizes the hypothesis that 24.2 uses "
                          "holds although (E), which is how the corollary reaches it, does not (a point probability is well below its Chernoff bound at these sizes)")
    return stats_


# ------------------------------------------------------------------------------------------------ LR14
def lr14():
    print("LR14. Theorem Q's entry term on the tallies, recomputed; theta0 = least root on [5, K); k0 = 5")
    print("   Phi = sum_{K <= z <= A/2} p_z sum_{z' < K} T(z, z') e^{theta0 (K - z')}, a direct death counted as z' = 0; C+ = max_{K <= z <= A/2} M_z(theta0) e^{-theta0 (z - K)}")
    res = {}
    for frac in (0.35, 0.45):
        for R in (7, 9, 11, 13):
            A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
            H = q2.CUR[f'H_{R}'].astype(float); expo = H.sum()
            K = int(np.ceil(frac * A))
            th = q4.roots(Tb, KM); th0 = float(np.nanmin(th[5:K]))
            zp = np.arange(0, K)
            wgt = np.exp(th0 * (K - zp))
            tall = float((Tr[K:KM, :K] * wgt[None, :]).sum())
            chi = Tr[K:KM, 1:K].sum() / expo
            C = float((Tr[K:KM, 1:K] * wgt[None, 1:]).sum() / Tr[K:KM, 1:K].sum())
            direct = Tr[K:KM, 0].sum()
            Phi = tall / expo
            Cp = max(np.exp(lnM(Tb[z], z, th0) - th0 * (z - K)) for z in range(K, KM))
            zarg = max(range(K, KM), key=lambda z: lnM(Tb[z], z, th0) - th0 * (z - K))
            # the rows above A/2, by the inflow identity: every measured state at z' was entered from some row, so
            # (entries into z' from rows above A/2) = H(z') - sum_{z <= A/2} Tr[z, z'] + (landings counted in Tr at the moment another
            # face of the replica died) - (first measured states of a soup at z'). The last two are of relative order deaths / exposure.
            inflow = Tr[1:KM, :].sum(0)
            resid = H[:K] - inflow[:K]; resid[0] = 0.0
            above = float((np.maximum(resid, 0) * wgt).sum()) / expo
            contam = float((np.minimum(resid, 0) * wgt).sum()) / expo
            # direct deaths from rows above A/2: at most (face deaths in total) - (deaths from tallied rows); only replica deaths are recorded
            h = Tr[:, 0].sum() / expo
            res[(frac, A)] = dict(K=K, th0=th0, chi=chi, C=C, Phi=Phi, Cp=Cp, direct=direct, above=above, contam=contam, h=h, resid=resid)
            first = next((int(i) for i in range(1, K) if resid[i] > 0), None)
            print(f"   K = ceil({frac} A), A = {A}: K = {K}, theta0 = {th0:.4f}; chi = {chi:.4f}; C = {C:.2f}; direct deaths from rows K..A/2: {direct:.0f}; Phi = {Phi:.4f}; "
                  f"C+ = {Cp:.3f} (at row {zarg}); theta0 (K - 5) - ln Phi = {th0 * (K - 5) - np.log(Phi):.2f}; -ln h = {-np.log(h):.2f}\n"
                  f"        rows above A/2 (inflow identity): they add {above:.4f} to Phi ({100 * above / Phi:.1f}%); lowest row they enter: {first}; "
                  f"negative residuals (contamination, see the code) weigh {contam:.4f}; with them Phi = {Phi + above:.4f}, theta0 (K - 5) - ln Phi = {th0 * (K - 5) - np.log(Phi + above):.2f}")
    p = [res[(0.35, A)] for A in (30, 45, 63, 84)]
    check(np.allclose([x['Phi'] for x in p], [0.136, 0.103, 0.085, 0.046], atol=6e-4) and np.allclose([x['Cp'] for x in p], [1.043, 1.054, 1.068, 1.068], atol=6e-4)
          and np.allclose([x['C'] for x in p], [2.42, 3.08, 3.70, 4.45], atol=6e-3) and [x['direct'] for x in p] == [1, 0, 0, 0],
          "path's table of 23.3 at K = ceil(0.35 A) reproduced: Phi = 0.136, 0.103, 0.085, 0.046; C+ = 1.043, 1.054, 1.068, 1.068; C = 2.42, 3.08, 3.70, 4.45; direct deaths 1, 0, 0, 0")
    r84 = res[(0.35, 84)]['resid']
    check(all(r84[1:10] == 0) and (r84[1:] >= 0).all(),
          f"A = 84: no state with 9 cells or fewer was ever entered from a row above A/2 (residuals of rows 1..12: {', '.join(f'{v:.0f}' for v in r84[1:13])}); no residual is negative")

    print("   Condition B+ (24.4): the largest W(n1) - W(z') + ln T(z, z') over K <= z <= A/2, z' <= n1 = K - 1 (<= 0 means B+ holds with e = 0)")
    worst = []
    for frac in (0.35, 0.45):
        for R in (9, 11, 13):
            A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
            rows = [np.array([1.0])] + [Tb[k].copy() for k in range(1, KM)]
            n1 = int(np.ceil(frac * A)) - 1
            T = square(rows, n1)
            line = f"   K = ceil({frac} A), A = {A}:"
            for name, W in (("W_J", w_cramer(rows, n1)), ("W°", w_path(T))):
                w, arg = max(((W[n1] - W[zp] + np.log(Tb[z, zp]), (z, zp)) for z in range(n1 + 1, KM) for zp in range(n1 + 1) if Tb[z, zp] > 0))
                worst.append((frac, w))
                line += f" {name}: {w:+.3f} (at z = {arg[0]}, z' = {arg[1]});"
            print(line)
    w35 = [w for f, w in worst if f == 0.35]
    check(np.allclose(w35, [-2.439, -0.721, -2.637, -0.638, -2.792, -0.606], atol=0.02) and max(w for f, w in worst) <= 0,
          "B+ holds with e = 0 on the tallied rows at both K; at 0.35 A path's numbers (-2.44, -2.64, -2.79 for W_J; -0.72, -0.64, -0.61 for W°) are reproduced")
    return res


# ------------------------------------------------------------------------------------------------ split
def split():
    print("Entry 24.7, point 3, on the A = 84 table: k -> ln M_k(s) and the cost of an uneven split of two halves")
    Tr, N, Tb = q2.table(13); KM = Tr.shape[0]
    for s in (0.3,):
        L = np.array([np.nan] + [lnM(Tb[k], k, s) for k in range(1, KM)])
        d2 = L[4:KM - 2] + L[6:KM] - 2 * L[5:KM - 1]              # second differences centred at rows 5..KM-2
        cost = {k: L[k - 3] + L[k + 3] - 2 * L[k] for k in (10, 20, 30)}
        marg = {k: -L[k] for k in (10, 20, 30)}
        print(f"   s = {s}: second differences centred at rows 5..{KM - 2}: {int((d2 > 0).sum())} of {len(d2)} positive; "
              + '; '.join(f"k = {k}: ln M_(k-3) + ln M_(k+3) - 2 ln M_k = {cost[k]:+.3f} (margin -ln M_k = {marg[k]:.3f})" for k in cost))
    check(int((d2 > 0).sum()) >= 28 and all(v > 0 for v in cost.values()),
          "ln M_k(0.3) is convex in k on most of the block, so the pooled row of two independent halves (a mixture over the split) has a larger transform than the even split")
    return cost


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('hand', 'all'): hand()
    if cmd in ('random', 'all'): random_checks()
    if cmd in ('family', 'all'): family()
    if cmd in ('tables', 'all'): tables()
    if cmd in ('lr14', 'all'): lr14()
    if cmd in ('split', 'all'): split()
    print('ALL OK' if OK else 'SOMETHING FAILED')
