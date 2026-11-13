"""Critic's lab: checks and lab requests for path, round 1.

  python3 path_r1.py psharp   the worked numbers of Theorem P / Corollary P1 (biased walk, K = 2 and K = 30)
  python3 path_r1.py data     the data readings of path's entry 3 and entry 5 (committed files only)
  python3 path_r1.py lr1      LR1: generating-function test of (*)(i) on the measured one-step table Tr[k, k']
  python3 path_r1.py lr3      LR3: the last generations before a face death
  python3 path_r1.py lr2      LR2: the certificate of Theorem P on the exact one-row dice model D2(L, 0.472)
  python3 path_r1.py seg      D2 on a segment (two dead ends) against D2 on a ring, exact (bears on guess G1)

lr1 and lr3 read tallies that are NOT in git (research/scratch/fluct/qsd_R*.npz, written by research/fluct/qsd.py
on 2026-11-13). They are checked here against the committed research/fluct/data/qsd_summary.json before use.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dice_w1 as dw

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))        # research/
AREA = {7: 30, 9: 45, 11: 63, 13: 84, 15: 108, 17: 135}


# ----------------------------------------------------------------------------------------------------- P
def walk_h(K, p):
    """exact quasi-stationary hazard of the walk on {1..K}: up p (held at K), down q, absorbed at 0."""
    q = 1 - p
    Q = np.zeros((K, K))
    for z in range(1, K + 1):
        if z < K: Q[z - 1, z] = p
        else: Q[z - 1, z - 1] = p
        if z > 1: Q[z - 1, z - 2] = q
    lam = max(np.linalg.eigvals(Q).real)
    return 1 - lam


def psharp():
    p, q = 0.75, 0.25
    K, r = 2, 0.5
    a = p * r + q / r; C = p * (1 - r)
    print(f"K=2, p=3/4, r=1/2: a = {a}, C = {C}, bound C r^K/(1-a) = {C * r ** K / (1 - a)}, exact h = {walk_h(2, p):.4f}")
    K = 30
    rs = np.linspace(q / p + 1e-4, 0.999, 20000)
    b = p * (1 - rs) * rs ** K / (1 - (p * rs + q / rs))
    i = int(np.argmin(b))
    print(f"K=30: best r = {rs[i]:.3f}, bound {b[i]:.2e}; exact h = {walk_h(30, p):.2e}; (q/p)^K = {(q / p) ** K:.2e}; "
          f"bound / exact = {b[i] / walk_h(30, p):.0f}")
    # direct check of the theorem's conclusion on a non-Markov-looking example: lumped population of D2
    return


# -------------------------------------------------------------------------------------------------- data
def local_slopes(rows, per=1.0):
    return [per * (b['lntau'] - a['lntau']) / (b['L'] - a['L']) for a, b in zip(rows, rows[1:])]


def data():
    d = os.path.join(RES, 'toy2d', 'data')
    print("5.2: local slopes of ln tau per orbit of edge cells (committed toy2d data)")
    for name, per in (('box_none', 1), ('box_diag', 1), ('mx', 2), ('box_d4', 2), (None, 1), ('box_c4', 1)):
        fn = 'law_cross2_B34S234' + ('_' + name if name else '') + '.json'
        rows = json.load(open(os.path.join(d, fn)))['rows']
        key = 'lntau'
        Ls = [r['L'] for r in rows]
        sl = local_slopes(rows, per)
        err = [per * np.hypot(a['err'], b['err']) / (b['L'] - a['L']) for a, b in zip(rows, rows[1:])]
        print(f"  {name or 'strip, no symmetry':20s} L = {Ls}: " + ', '.join(f"{s:.3f}+-{e:.3f}" for s, e in zip(sl, err)))
    g = json.load(open(os.path.join(RES, 'theory', 'exponent', 'data', 'gap.json')))['gap_H16_L128']
    E = np.array(g['E'], float); cnt = np.array(g['counts'], float)
    ok = cnt > 200
    lmax = int(np.flatnonzero(ok)[-1])
    dec = -np.log(E[1:lmax + 1] / E[:lmax])              # dec[l] = -ln E(l+1)/E(l)
    print(f"5.2: empty-window decrement -ln[E(l+1)/E(l)], ring L = 128 (windows with > 200 counts: l <= {lmax})")
    print("  l = 5, 10, ..., 35: " + ', '.join(f"{dec[l]:.3f}" for l in range(5, 40, 5)))
    for gg in (0.33, 0.34, 0.345, 0.355, 0.365):
        print(f"  (decrement - {gg})(l + 1/2) at l = 15..35: " + ', '.join(f"{(dec[l] - gg) * (l + 0.5):.2f}" for l in range(15, 40, 5)))
    # how well is g determined? weighted fits dec(l) = g + c/(l + delta), delta fixed, l in [l0, 38]
    w_all = 1.0 / np.sqrt(1.0 / cnt[1:lmax + 1] + 1.0 / np.maximum(cnt[:lmax], 1))     # 1 / se of the decrement
    print("  fits of the decrement on l = l0..38:  form                      g        second parameter   chi2/dof")
    for l0 in (10, 15, 20):
        ls = np.arange(l0, min(39, lmax))
        y = dec[ls]; w = w_all[ls]
        for form, col in (('g + c/(l+1/2)', 1.0 / (ls + 0.5)), ('g + c/(l+1/2)^2', 1.0 / (ls + 0.5) ** 2),
                          ('g + c exp(-l/10)', np.exp(-ls / 10.0)), ('g + c exp(-l/20)', np.exp(-ls / 20.0))):
            X = np.stack([np.ones(len(ls)), col], 1) * w[:, None]
            coef, res, *_ = np.linalg.lstsq(X, y * w, rcond=None)
            chi2 = float(((X @ coef - y * w) ** 2).sum())
            cov = np.linalg.inv(X.T @ X)
            print(f"    l0={l0:2d}  {form:22s}  g = {coef[0]:.4f} +- {np.sqrt(cov[0, 0]):.4f}   c = {coef[1]:7.3f}   {chi2:.1f}/{len(ls) - 2}")
    s = json.load(open(os.path.join(RES, 'fluct', 'data', 'qsd_summary.json')))['sizes']
    print("entry 3: slope of ln p_k against k for 4 <= k <= 20 (qsd_summary.json, field lnp)")
    for R in ('9', '11', '13', '15'):
        if R in s:
            lnp = s[R]['lnp']
            ks = [k for k in range(4, 21) if k < len(lnp) and lnp[k] is not None]
            sl = np.polyfit(ks, [lnp[k] for k in ks], 1)[0]
            first = lnp[5] - lnp[4]; last = lnp[20] - lnp[19] if len(lnp) > 20 and lnp[20] is not None else float('nan')
            print(f"  A = {s[R]['A']}: mean slope {sl:.3f} (ratio p_k/p_k+1 = {np.exp(-sl):.3f}); k=4->5: {first:.3f}; k=19->20: {last:.3f}; "
                  f"mean/A = {s[R]['mean']:.3f}; -ln h/A = {-s[R]['ln_h'] / s[R]['A'] if s[R].get('ln_h') else float('nan'):.4f}")


# --------------------------------------------------------------------------------------------------- lr1
def load_npz(R):
    fn = os.path.join(RES, 'scratch', 'fluct', f'qsd_R{R}.npz')
    return np.load(fn, allow_pickle=True)


def npz_against_summary():
    s = json.load(open(os.path.join(RES, 'fluct', 'data', 'qsd_summary.json')))['sizes']
    ok = True
    for R in (7, 9, 11, 13):
        z = load_npz(R)
        d, e = int(z['deaths'][0]), int(z['expo'][0])
        lnh = np.log(d / (8.0 * e))
        ok &= d == s[str(R)]['deaths'] and abs(lnh - s[str(R)]['ln_h']) < 1e-9
        print(f"  R={R}: npz deaths {d}, exposure {e} replica-generations, ln h = {lnh:.4f}; summary: {s[str(R)]['deaths']}, {s[str(R)]['ln_h']:.4f}")
    print("  tallies agree with the committed summary:", ok)
    return ok


def lr1():
    print("LR1. a_k(r) = sum_k' Tr[k,k'] r^(k'-k) / sum_k' Tr[k,k']   (k' = 0 is death, weight r^-k)")
    npz_against_summary()
    rs = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]
    for R in (7, 9, 11, 13):
        z = load_npz(R)
        Tr = z['Tr'].astype(float)
        A = AREA[R]; KM = Tr.shape[0]
        tot = Tr.sum(1)
        ks = np.arange(1, KM)
        kp = np.arange(Tr.shape[1])
        print(f"  A = {A} (R = {R}): rows k = 1..{KM - 1}; row totals: k=1: {tot[1]:.0f}, k=2: {tot[2]:.0f}, k=3: {tot[3]:.0f}, k=5: {tot[5]:.0f}, "
              f"k=10: {tot[10]:.0f}, k={KM - 1}: {tot[KM - 1]:.0f}")
        print("     r     max_k a_k   at k   | a_1    a_2    a_3    a_4    a_6    a_10   a_%d" % (KM - 1))
        for r in rs:
            a = np.array([(Tr[k] * r ** (kp - float(k))).sum() / tot[k] if tot[k] > 0 else np.nan for k in range(KM)])
            kk = int(np.nanargmax(a[1:])) + 1
            print(f"    {r:.2f}   {a[kk]:8.4f}   {kk:3d}   | " + '  '.join(f"{a[k]:.3f}" for k in (1, 2, 3, 4, 6, 10, KM - 1)))
        # the interval of r on which every row contracts, and per-row roots
        grid = np.linspace(0.30, 0.999, 700)
        amax = np.array([max((Tr[k] * r ** (kp - float(k))).sum() / tot[k] for k in range(1, KM) if tot[k] > 0) for r in grid])
        good = grid[amax < 1]
        print(f"     max_k a_k(r) < 1 for r in " + (f"[{good.min():.3f}, {good.max():.3f}]; smallest max_k a_k = {amax.min():.4f} at r = {grid[int(np.argmin(amax))]:.3f}"
                                                   if len(good) else f"no r; smallest max_k a_k = {amax.min():.4f} at r = {grid[int(np.argmin(amax))]:.3f}"))
        # one-step death probabilities and drift by row
        pd = Tr[:, 0] / np.maximum(tot, 1)
        mean_step = (Tr * (kp[None, :] - np.arange(KM)[:, None])).sum(1) / np.maximum(tot, 1)
        print("     P(death | k), k = 1..6: " + ', '.join(f"{pd[k]:.4f}" for k in range(1, 7)) +
              "   mean step E[k' - k], k = 1, 2, 3, 5, 10: " + ', '.join(f"{mean_step[k]:+.2f}" for k in (1, 2, 3, 5, 10)))


def lr3():
    print("LR3. face population n at lag s before the death (lag 0 = empty), from the `pre` arrays")
    s = json.load(open(os.path.join(RES, 'fluct', 'data', 'qsd_summary.json')))['sizes']
    for R in (7, 9, 11, 13):
        z = load_npz(R)
        pre = z['pre'][:, :, 0].astype(float)          # (deaths, 65): index 64 = the death
        A = AREA[R]; mean_live = s[str(R)]['mean'] * A
        lag = lambda j: pre[:, 64 - j]
        assert (lag(0) == 0).all()
        print(f"  A = {A}: {len(pre)} deaths; living mean {mean_live:.1f} cells")
        print("    lag:     " + ' '.join(f"{j:5d}" for j in (1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64)))
        print("    mean n:  " + ' '.join(f"{lag(j).mean():5.1f}" for j in (1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64)))
        for qq, nm in ((25, 'q25:     '), (50, 'median:  '), (75, 'q75:     ')):
            print("    " + nm + ' '.join(f"{np.percentile(lag(j), qq):5.1f}" for j in (1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64)))
        m = np.array([lag(j).mean() for j in range(0, 65)])
        half = next(j for j in range(1, 65) if m[j] >= mean_live / 2)
        # interpolate
        j0 = half - 1
        x = j0 + (mean_live / 2 - m[j0]) / (m[half] - m[j0])
        q90 = next((j for j in range(1, 65) if m[j] >= 0.9 * mean_live), None)
        # per-death: last lag at which the face still had at least half the living mean
        last_half = np.array([next((j for j in range(1, 65) if row[64 - j] >= mean_live / 2), 65) for row in pre])
        print(f"    mean crosses half the living mean at lag {x:.1f}; reaches 90% of it at lag {q90}; per death, the last time "
              f"n >= half the living mean: median lag {np.median(last_half):.0f}, quartiles {np.percentile(last_half, 25):.0f}-{np.percentile(last_half, 75):.0f}")


# --------------------------------------------------------------------------------------------------- lr2
def lumped(L, rho):
    reps, idx, M = dw.reduced_kernel(L, rho)
    Q = M[1:, 1:]
    lam, mu, v = dw.perron(Q)
    n = np.array([bin(int(S)).count('1') for S in reps])
    pn = np.bincount(n[1:], weights=mu, minlength=L + 1)
    T = np.zeros((L + 1, L + 1))
    for npr in range(L + 1):
        col = M[1:, n == npr].sum(1)                      # P(orbit -> population n')
        T[:, npr] = np.bincount(n[1:], weights=mu * col, minlength=L + 1)
    T[1:] /= pn[1:, None]
    return 1 - lam, pn, T


def certificate(T, h, L):
    """smallest eps(r, K, a) with  T(n,0) + sum_{n'>=1} T(n,n') r^min(n',K)  <=  a r^min(n,K) + eps  for all n >= 1."""
    best = {}
    ns = np.arange(L + 1)
    for a in (0.9, 0.95, 0.99):
        for K in range(1, L + 1):
            for r in np.linspace(0.05, 0.99, 189):
                phi = r ** np.minimum(ns, K)
                lhs = T[1:, 0] + T[1:, 1:] @ phi[1:]
                eps = max(0.0, float((lhs - a * phi[1:]).max()))
                b = eps / (1 - a)
                if (a, K) not in best or b < best[(a, K)][0]:
                    best[(a, K)] = (b, r, eps)
    return best


def lr2():
    print("LR2. D2(L, 0.472), exact. Lumped one-step table of the population under the quasi-stationary law; smallest")
    print("     eps for (*) with phi = r^min(n,K); bound eps/(1-a) (s = 0) against the true h. 'loss' = ln(bound/h).")
    for L in (8, 10, 12, 14):
        h, pn, T = lumped(L, 0.472)
        assert abs(T[1:].sum(1) - 1).max() < 1e-9
        best = certificate(T, h, L)
        print(f"  L = {L}: h = {h:.4e} (-ln h = {-np.log(h):.3f}); P_qs(n = 1..4) = " + ', '.join(f"{pn[k]:.2e}" for k in range(1, 5)) +
              f"; mode at n = {int(np.argmax(pn))}; T(1,0) = {T[1, 0]:.3f}, T(2,0) = {T[2, 0]:.3f}, T(3,0) = {T[3, 0]:.4f}")
        for a in (0.9, 0.95, 0.99):
            Kb = min(range(1, L + 1), key=lambda K: best[(a, K)][0])
            b, r, eps = best[(a, Kb)]
            line = '  '.join(f"K={K}: {np.log(best[(a, K)][0] / h):+.2f} (r={best[(a, K)][1]:.2f})" for K in sorted(set([2, 4, 6, 8, Kb, L])) if K <= L)
            print(f"    a = {a}: best K = {Kb}, r = {r:.3f}: bound {b:.3e}, loss {np.log(b / h):+.2f} nats, bound's exponent "
                  f"K ln(1/r) = {Kb * np.log(1 / r):.2f}.  loss by K: {line}")
        # is part (i) of (*) satisfiable at all: rows n < K contract for which r?
        ns = np.arange(L + 1)
        for r in (0.4, 0.5, 0.6, 0.7):
            a_n = (T[1:, 0] + T[1:, 1:] @ (r ** ns[1:])) / r ** ns[1:]
            print(f"    r = {r}: a_n(r) = [P(death) + E r^n'] / r^n for n = 1..{min(L, 8)}: " + ', '.join(f"{x:.2f}" for x in a_n[:8]))


# --------------------------------------------------------------------------------------------------- seg
def seg_kernel(L, rho, ring=False):
    """D2 on a segment of L cells (cells beyond both ends dead for ever), reduced by the reflection."""
    P = dw.p_alive(rho)
    s = np.arange(1 << L, dtype=np.int64)
    rev = np.zeros_like(s)
    for i in range(L):
        rev |= ((s >> i) & 1) << (L - 1 - i)
    can = np.minimum(s, rev)
    reps, idx = np.unique(can, return_inverse=True)
    M = np.empty((len(reps), len(reps)))
    for rr, S in enumerate(reps):
        S = int(S)
        bits = [(S >> i) & 1 for i in range(L)]
        g = lambda i: bits[i] if 0 <= i < L else 0
        v = np.ones(1)
        for x in range(L):
            p = P[bits[x], g(x - 1) + g(x - 2) + g(x + 1) + g(x + 2)]
            v = np.concatenate((v * (1 - p), v * p))
        M[rr] = np.bincount(idx, weights=v, minlength=len(reps))
    return reps, M


def seg():
    rho = 0.472
    print("D2 on a segment of L cells (dead beyond both ends) against D2 on a ring of L cells, rho = 0.472, exact")
    print("   L   ln tau(segment)  step    ln tau(ring)   step    ring - segment")
    ps = pr = None
    for L in range(5, 15):
        reps, M = seg_kernel(L, rho)
        lam, mu, v = dw.perron(M[1:, 1:])
        ls = -np.log(1 - lam)
        lr = dw.analyse(L, rho)['lntau']
        print(f"  {L:2d}   {ls:8.4f}       {'' if ps is None else f'{ls - ps:.4f}':>7s}   {lr:8.4f}     {'' if pr is None else f'{lr - pr:.4f}':>7s}   {lr - ls:+.4f}", flush=True)
        ps, pr = ls, lr


if __name__ == '__main__':
    what = sys.argv[1]
    dict(psharp=psharp, data=data, lr1=lr1, lr2=lr2, lr3=lr3, seg=seg)[what]()
