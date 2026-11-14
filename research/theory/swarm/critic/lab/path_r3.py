"""Critic's lab: the lab work path asked for at the end of its interim round 3. Arithmetic on the curated tallies
(data/fluct_tables.npz; no new runs) and exact computations on the dice model D2.

  python3 path_r3.py th      15.2: local roots theta_k = -ln r_k of the pooled one-step table, their sums against
                             -ln psi*(K) (the table's own committor) and against -ln h; 2 mean / variance; collapse
                             in k/A; psi*_A(k) against A at fixed k
  python3 path_r3.py age [L] 15.3: D2(L, 0.472) on a ring (default 16; 18 takes 6 min): under the quasi-stationary
                             process, the law of the number of generations the central cell of an empty window of
                             l cells has been dead
  python3 path_r3.py mono    source's monotone comparison (board, lemma exchange) applied to the pooled table:
                             is the pooled one-step table stochastically monotone, and do the four sizes dominate
                             one another row by row?
The pre-death populations of D2 from the exact reversed chain are in prob_r2.py r7.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prob_r1 as pr
import prob_r2 as p2
import path_r2 as q2

AREA = q2.AREA
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def root(row, k):
    """r in (0, 1) with sum_k' row[k'] r^(k' - k) = 1, or None (it exists iff the mean step is positive and death is possible)."""
    step = (np.arange(len(row)) - k).astype(float)
    f = lambda r: float((row * r ** step).sum()) - 1
    if (row * step).sum() <= 0:
        return None
    lo, hi = 1e-3, 1 - 1e-10
    if not (f(lo) > 0 and f(hi) < 0):
        return None
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


def th():
    print("15.2. theta_k = -ln r_k, r_k the root of sum_k' T(k, k') r^(k'-k) = 1 for the pooled one-step table of the face population (rows k < A/2)")
    summ = {}
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        H = q2.CUR[f'H_{R}'].astype(float); mean = float((H * np.arange(len(H))).sum() / H.sum()); mode = int(np.argmax(H))
        lnh = float(q2.SUMM[str(R)]['ln_h'])
        theta = np.full(KM, np.nan); mv = np.full(KM, np.nan)
        for k in range(1, KM):
            r = root(Tb[k], k)
            step = np.arange(Tb.shape[1]) - k
            mu = float((Tb[k] * step).sum()); var = float((Tb[k] * step ** 2).sum() - mu ** 2)
            mv[k] = 2 * mu / var
            if r is not None: theta[k] = -np.log(r)
        first = int(np.flatnonzero(~np.isnan(theta))[0])
        last = int(np.flatnonzero(~np.isnan(theta))[-1])
        csum = np.nancumsum(theta)                      # sum_{j <= k} theta_j (undefined rows count 0)
        psi_full = q2.committor(Tb, KM)                 # psi*(1..KM-1) with K = KM
        sel = [k for k in (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40) if k < KM]
        print(f"  A = {A}: rows 1..{KM - 1} tallied; mean population {mean:.1f}, mode {mode}; -ln h = {-lnh:.3f}; theta defined for k = {first}..{last}")
        print("       k              " + ' '.join(f"{k:6d}" for k in sel))
        print("       theta_k        " + ' '.join(('    --' if np.isnan(theta[k]) else f"{theta[k]:6.3f}") for k in sel))
        print("       2 mean/var     " + ' '.join(f"{mv[k]:6.3f}" for k in sel))
        print("       k/A            " + ' '.join(f"{k / A:6.3f}" for k in sel))
        # WKB against the table's own committor: -ln psi*(k) + ln psi*(k0) against sum_{k0 <= j < k} theta_j
        k0 = max(first, 3)
        print(f"       -ln[psi*(k)/psi*({k0})] against sum of theta_j, {k0} <= j < k (psi* = committor of the same table, K = {KM}):")
        ks = [k for k in (5, 8, 10, 15, 20, 25, 30, 35, 40) if k0 < k < KM]
        print("           k:         " + ' '.join(f"{k:6d}" for k in ks))
        print("           committor: " + ' '.join(f"{-np.log(psi_full[k - 1] / psi_full[k0 - 1]):6.2f}" for k in ks))
        print("           sum theta: " + ' '.join(f"{csum[k - 1] - csum[k0 - 1]:6.2f}" for k in ks))
        tot = float(csum[min(last, int(round(mean)))])
        summ[A] = (tot, -lnh, mean, float(np.nansum(mv[1:int(round(mean)) + 1])) if int(round(mean)) < KM else float('nan'), last)
        print(f"       sum of theta_k up to the mean population (rows that have a root; the last tallied row is {KM - 1}): {tot:.2f};  -ln h = {-lnh:.2f};  "
              f"difference {-lnh - tot:+.2f};  per cell: {tot / A:.4f} against {-lnh / A:.4f}")
    As = sorted(summ)
    print("  slopes between successive sizes: of the sum of theta " + ', '.join(f"{(summ[b][0] - summ[a][0]) / (b - a):.4f}" for a, b in zip(As, As[1:])) +
          ";  of -ln h " + ', '.join(f"{(summ[b][1] - summ[a][1]) / (b - a):.4f}" for a, b in zip(As, As[1:])))
    print("  collapse in x = k/A: theta at x = 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45 (linear interpolation in k)")
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        th_ = np.array([np.nan] + [(-np.log(root(Tb[k], k)) if root(Tb[k], k) is not None else np.nan) for k in range(1, KM)])
        out = []
        for x in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45):
            k = x * A
            lo = int(np.floor(k))
            if lo + 1 >= KM or np.isnan(th_[lo]) or np.isnan(th_[lo + 1]): out.append('    --'); continue
            out.append(f"{th_[lo] + (k - lo) * (th_[lo + 1] - th_[lo]):6.3f}")
        print(f"       A = {A}: " + ' '.join(out))
    print("  psi*_A(k) at fixed k (K = ceil(0.4 A)): is it non-increasing in A?")
    psis = {AREA[R]: q2.committor(q2.table(R)[2], int(np.ceil(0.4 * AREA[R]))) for R in (7, 9, 11, 13)}
    viol = []
    for k in range(1, 13):
        vals = [psis[A][k - 1] if k - 1 < len(psis[A]) else np.nan for A in (30, 45, 63, 84)]
        if k in (1, 2, 3, 4, 5, 6, 8, 10, 12):
            print(f"       k = {k:2d}: " + ' '.join(f"{v:.4g}" for v in vals))
        for (a, va), (b, vb) in zip(zip((30, 45, 63, 84), vals), list(zip((30, 45, 63, 84), vals))[1:]):
            if vb > va: viol.append((k, a, b, vb / va))
    print("       pairs (k, A < A') with psi*_A'(k) > psi*_A(k): " + (', '.join(f"k = {k}: {a} -> {b} (x{r:.3f})" for k, a, b, r in viol) if viol else "none"))


def mono():
    print("the pooled one-step table of the face population as a kernel on {0, .., A}: stochastic monotonicity and order between sizes")
    tabs = {}
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = q2.table(R); KM = Tr.shape[0]
        tabs[A] = Tb
        cdf = np.cumsum(Tb, axis=1)                     # P(n' <= j | n = k)
        # monotone iff cdf[k+1, j] <= cdf[k, j] for all j
        worst = 0.0; where = None
        for k in range(1, KM - 1):
            d = cdf[k + 1] - cdf[k]
            if d.max() > worst: worst = float(d.max()); where = (k, int(np.argmax(d)))
        se = np.sqrt(0.25 / np.minimum(N[1:KM - 1], N[2:KM])).max()
        print(f"   A = {A}: largest violation of 'row k+1 dominates row k' (rows 1..{KM - 1}): {worst:.4f}" + (f" at k = {where[0]}, n' <= {where[1]}" if where else "") +
              f"  (largest sampling error of a row's distribution function: {se:.4f})")
    for (a, b) in ((30, 45), (45, 63), (63, 84)):
        Ta, Tb_ = tabs[a], tabs[b]
        K = min(Ta.shape[0], Tb_.shape[0])
        ca = np.cumsum(Ta, axis=1); cb = np.cumsum(Tb_, axis=1)
        m = min(ca.shape[1], cb.shape[1])
        d = cb[1:K, :m] - ca[1:K, :m]                   # > 0: the larger face is stochastically lower somewhere
        k, j = np.unravel_index(np.argmax(d), d.shape)
        k2, j2 = np.unravel_index(np.argmin(d), d.shape)
        print(f"   rows of A = {b} against rows of A = {a} (k = 1..{K - 1}): max of F_{b} - F_{a} = {d.max():+.4f} (k = {k + 1}, n' <= {j}); min = {d.min():+.4f} (k = {k2 + 1}, n' <= {j2});  "
              f"death column: " + ', '.join(f"k = {kk}: {Tb_[kk, 0]:.4f} / {Ta[kk, 0]:.4f}" for kk in (1, 2, 3, 4)))


def age(L=16):
    print(f"15.3. D2({L}, 0.472) on a ring, quasi-stationary process: for an empty window of l cells centred on cell x, the law of the number of generations x has been dead")
    a2 = pr.a_table(p2.D2)
    lam, mu = p2.perron_left(L, 'ring', a2)
    _, left = p2.make_ops(L, 'ring', a2)
    S = np.arange(1 << L, dtype=np.int64)
    x = L // 2
    bit = lambda i: (S >> (L - 1 - (i % L))) & 1
    dead_x = bit(x) == 0
    ells = [l for l in (1, 3, 5, 7, 9, 11, 13) if l < L - 3]
    masks = {}
    for l in ells:
        m = np.ones(1 << L, bool)
        for d in range(-(l // 2), l // 2 + 1): m &= bit(x + d) == 0
        m[0] = False                                      # the row is alive
        masks[l] = m
    m_j = mu * dead_x
    a = {l: [float(m_j[masks[l]].sum())] for l in ells}
    J = 120
    for j in range(2, J + 1):
        nxt = left(m_j); nxt[0] = 0.0
        m_j = nxt * dead_x / lam
        for l in ells: a[l].append(float(m_j[masks[l]].sum()))
        if a[ells[0]][-1] < 1e-7 * a[ells[0]][0] and all(a[l][-1] < 1e-6 * a[l][0] for l in ells):
            break
    print(f"   ln tau = {-np.log(1 - lam):.4f}; generations followed back: {len(a[ells[0]])}")
    print("     l    -ln P(window empty)   decrement   mean age   P(age = 1)  P(age >= 3)  P(age >= 6)  P(age >= 12)   last ratio a_j+1/a_j")
    prev = None
    for l in ells:
        v = np.array(a[l]); surv = v / v[0]
        meanage = float(surv.sum())
        dec = '' if prev is None else f"{(-np.log(v[0]) - prev) / 2:9.4f}"
        prev = -np.log(v[0])
        g = lambda j: surv[j - 1] if j - 1 < len(surv) else 0.0
        print(f"    {l:2d}    {-np.log(v[0]):10.4f}        {dec:>9s}   {meanage:8.3f}   {1 - g(2):8.3f}   {g(3):9.3f}   {g(6):9.3f}   {g(12):10.4f}        {v[-1] / v[-2]:.4f}")
    check(abs(a[1][0] - float((mu * dead_x).sum())) < 1e-12 and all(a[l][-1] < 1e-4 * a[l][0] for l in ells),
          "the sums have converged (the tail left out is below 1e-4 of the first term for every l)")


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'th': th()
    elif what == 'mono': mono()
    elif what == 'age': age(int(sys.argv[2]) if len(sys.argv) > 2 else 16)
    print('ALL OK' if OK else 'SOMETHING FAILED')
