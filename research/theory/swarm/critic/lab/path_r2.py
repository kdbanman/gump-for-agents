"""Critic's lab: checks and lab requests for path, round 2. Arithmetic on the curated tallies
(data/fluct_tables.npz, see curate_fluct.py) and exact computations on the dice model D2; no new runs.

  python3 path_r2.py pbar    Theorem P-bar on the worked walk; Proposition R by enumeration on small graphs
  python3 path_r2.py lr4     LR4: the committor psi*_K of the pooled one-step table; the identity of Theorem P-bar
  python3 path_r2.py lr5     LR5: mean, variance and Lundberg root of the one-step change, row by row
  python3 path_r2.py lr6     LR6: the pre-death curve predicted by the pooled table (time-reversed chain)
  python3 path_r2.py lr7     LR7: tail slopes at A = 108, 135, 165; the histogram against its own parabola
  python3 path_r2.py lr8     LR8': empty-window probabilities under the quasi-stationary law of D2 (segment, ring)
  python3 path_r2.py deep    the 'd-deep' characterisation of path's Corollary 4a, on hulls
"""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prob_r1 as pr
import gump_lab as g3

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
AREA = {7: 30, 9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165}
CUR = np.load(os.path.join(HERE, 'data', 'fluct_tables.npz'))
SUMM = json.load(open(os.path.join(RES, 'fluct', 'data', 'qsd_summary.json')))['sizes']
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def table(R):
    Tr = CUR[f'Tr_{R}'].astype(float)
    N = Tr.sum(1)
    Tb = Tr / np.maximum(N, 1)[:, None]
    return Tr, N, Tb


# ---------------------------------------------------------------------------------------------------- pbar
def pbar():
    # the worked walk on {0, 1, 2}: up 3/4, down 1/4, held at 2
    Q = np.array([[0, .75], [.25, .75]])
    ev, vec = np.linalg.eig(Q.T)
    i = int(np.argmax(ev.real)); lam = ev.real[i]; p = np.abs(vec[:, i].real); p /= p.sum()
    h = 1 - lam
    entry = p[1] * .25; psi = .25; w = psi * p[0]
    check(abs(entry * psi / (1 - w) - h) < 1e-12, f"walk on {{0,1,2}}: p1 = {p[0]:.4f}, p2 = {p[1]:.4f}, h = {h:.4f}; entry flux x psi = {entry * psi:.4f}; "
                                                    f"/(1 - w) = {entry * psi / (1 - w):.4f} = h")
    # Proposition R: biased voter on small graphs, every start, by solving the absorption equations
    lam_ = 1.7
    graphs = {'path of 4': [(0, 1), (1, 2), (2, 3)], 'cycle of 5': [(i, (i + 1) % 5) for i in range(5)],
              'star of 5': [(0, i) for i in range(1, 5)], 'K4 minus an edge': [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]}
    worst = 0.0
    for name, edges in graphs.items():
        n = 1 + max(max(e) for e in edges)
        full = (1 << n) - 1
        A = np.zeros((1 << n, 1 << n)); b = np.zeros(1 << n)
        for S in range(1 << n):
            if S == 0:
                A[S, S] = 1; b[S] = 1; continue
            if S == full:
                A[S, S] = 1; continue
            tot = 0.0
            for x, y in edges:
                for (u, v) in ((x, y), (y, x)):
                    if (S >> u) & 1 and not (S >> v) & 1:
                        A[S, S | (1 << v)] -= lam_; A[S, S & ~(1 << u)] -= 1.0; tot += lam_ + 1.0
            A[S, S] += tot
        sol = np.linalg.solve(A, b)
        for S in range(1, full):
            k = bin(S).count('1')
            worst = max(worst, abs(sol[S] - (lam_ ** -k - lam_ ** -n) / (1 - lam_ ** -n)))
    check(worst < 1e-12, f"Proposition R (lambda = {lam_}), 4 graphs, every starting set: P(empty before full) = (lam^-n - lam^-N)/(1 - lam^-N), max error {worst:.1e}")


# ----------------------------------------------------------------------------------------------------- lr4
def committor(Tb, K):
    """psi*_K on rows 1..K-1: death before the population reaches K or more, for the chain of the pooled table."""
    T = Tb[1:K, 1:K]; d = Tb[1:K, 0]
    return np.linalg.solve(np.eye(K - 1) - T, d)


def lr4():
    print("LR4. the committor psi*_K = (I - T_<K)^-1 d of the pooled one-step table of the face population")
    out = {}
    for frac in (0.3, 0.4):
        print(f"  K = ceil({frac} A):")
        for R in (7, 9, 11, 13):
            A = AREA[R]; Tr, N, Tb = table(R); KM = Tr.shape[0]
            K = int(np.ceil(frac * A))
            psi = committor(Tb, K)
            out[(frac, R)] = psi
            sl = -np.diff(np.log(psi))
            print(f"    A = {A}, K = {K}: psi*(1..10) = " + ' '.join(f"{x:.4g}" for x in psi[:10]))
            print(f"            -d ln psi*/dk, k = 1..{min(K - 2, 14)}: " + ' '.join(f"{x:.3f}" for x in sl[:14]))
        ref = out[(frac, 11)]
        for R in (7, 9, 13):
            m = min(10, len(out[(frac, R)]), len(ref))
            print(f"    ln[psi*(A = {AREA[R]}) / psi*(A = 63)], k = 1..{m}: " + ' '.join(f"{np.log(out[(frac, R)][k] / ref[k]):+.3f}" for k in range(m)))
    print("  the identity of Theorem P-bar (per face-generation of exposure; boundary and censoring terms not included):")
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = table(R); KM = Tr.shape[0]
        expo = 8.0 * float(CUR[f'expo_{R}'][0]); deaths_tab = Tr[:, 0].sum()
        h = float(np.exp(SUMM[str(R)]['ln_h']))
        for frac in (0.3, 0.4):
            K = int(np.ceil(frac * A)); psi = committor(Tb, K)
            direct = Tr[K:, 0].sum()                                   # deaths straight from n >= K (tallied rows)
            ent_tab = Tr[K:, 1:K]                                      # entries from tallied rows K..KM-1
            inflow_all = N[1:K]                                        # (I): all arrivals at z' < K  ~  exposure at z'
            ent_un = inflow_all - Tr[1:, 1:K].sum(0)                   # arrivals from rows >= KM
            flux = (ent_tab * psi[None, :]).sum() + (ent_un * psi).sum()
            byrow = (ent_tab * psi[None, :]).sum(1)
            top = np.argsort(byrow)[::-1][:3] + K
            bypoint = (ent_tab.sum(0) + ent_un) * psi
            tp = np.argsort(bypoint)[::-1][:3] + 1
            print(f"    A = {A}, K = {K}: deaths in the table {deaths_tab:.0f} (h = {deaths_tab / expo:.3e}; summary {h:.3e}); direct from n >= K: {direct:.0f}; "
                  f"sum over entries of psi* = {flux:.1f} (ratio to deaths from below K: {flux / (deaths_tab - direct):.4f}); "
                  f"arrivals from untallied rows: {ent_un.sum():.0f} of {ent_tab.sum() + ent_un.sum():.0f}")
            print(f"          entry rows carrying most: " + ', '.join(f"{z} ({byrow[z - K] / flux:.2f})" for z in top) +
                  f";  entry points carrying most: " + ', '.join(f"{z} ({bypoint[z - 1] / flux:.2f})" for z in tp) +
                  f";  mean entry point {((ent_tab.sum(0) + ent_un) * np.arange(1, K)).sum() / (ent_tab.sum() + ent_un.sum()):.2f}")


# ----------------------------------------------------------------------------------------------------- lr5
def lr5():
    print("LR5. one-step change of the face population from k (death = step to 0): mean, variance, root r_k of sum T(k,k') r^(k'-k) = 1")
    for R in (7, 9, 11, 13):
        A = AREA[R]; Tr, N, Tb = table(R); KM = Tr.shape[0]
        kp = np.arange(Tr.shape[1])
        rows = []
        for k in range(1, KM):
            step = kp - k
            mu = (Tb[k] * step).sum(); var = (Tb[k] * step ** 2).sum() - mu ** 2
            f = lambda r: (Tb[k] * r ** step.astype(float)).sum() - 1
            root = None
            if mu > 0:
                lo, hi = 0.05, 1 - 1e-9
                if f(lo) > 0 and f(hi) < 0:
                    for _ in range(80):
                        mid = (lo + hi) / 2
                        if f(mid) > 0: lo = mid
                        else: hi = mid
                    root = (lo + hi) / 2
            rows.append((k, mu, var, root, N[k]))
        sel = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40]
        print(f"  A = {A}:   k      " + ' '.join(f"{k:6d}" for k in sel if k < KM))
        print("         mean     " + ' '.join(f"{rows[k - 1][1]:+6.2f}" for k in sel if k < KM))
        print("         mean/sqrt k" + ' '.join(f"{rows[k - 1][1] / np.sqrt(k):6.2f}" for k in sel if k < KM)[1:])
        print("         variance " + ' '.join(f"{rows[k - 1][2]:6.2f}" for k in sel if k < KM))
        print("         root r_k " + ' '.join(('   -- ' if rows[k - 1][3] is None else f"{rows[k - 1][3]:6.3f}") for k in sel if k < KM))


# ----------------------------------------------------------------------------------------------------- lr6
def lr6():
    print("LR6. pre-death mean population from the pooled table alone (time-reversed chain), against the recorded histories")
    for R in (9, 11, 13):
        A = AREA[R]; Tr, N, Tb = table(R); KM = Tr.shape[0]
        ph = CUR[f'prehist_{R}'].astype(float)
        meas = (ph * np.arange(A + 1)).sum(1) / ph[0].sum()
        # reversed kernel on tallied rows: P(prev = k | now = k') = Tr[k, k'] / inflow(k'), inflow(k') ~ N(k') (untallied -> lost)
        w = Tr[:, 0].copy(); w[0] = 0                 # lag 1: distribution of the population one generation before death
        w /= w.sum()
        pred = []; lost = []
        mass_out = 0.0
        for lag in range(1, 9):
            pred.append((w * np.arange(KM)).sum() / max(w.sum(), 1e-300)); lost.append(mass_out)
            new = np.zeros(KM)
            for kprime in range(1, KM):
                if w[kprime] == 0: continue
                col = Tr[1:KM, kprime]
                tot = N[kprime]                       # all arrivals at k' (identity (I)); the part from rows >= KM is lost
                new[1:KM] += w[kprime] * col / tot
                mass_out += w[kprime] * max(tot - col.sum(), 0.0) / tot
            w = new
        print(f"  A = {A}: lag            " + ' '.join(f"{j:6d}" for j in range(1, 9)))
        print("        recorded       " + ' '.join(f"{meas[j]:6.2f}" for j in range(1, 9)))
        print("        reversed chain " + ' '.join(f"{x:6.2f}" for x in pred) + "   (mean over the mass still inside the tallied rows)")
        print("        mass that has left the tallied rows: " + ' '.join(f"{x:6.3f}" for x in lost))


# ----------------------------------------------------------------------------------------------------- lr7
def lr7():
    print("LR7. slope of ln p_k over 8 <= k <= 20 (face-population histogram H, 8 faces pooled)")
    for R in (9, 11, 13, 15, 17, 19):
        H = CUR[f'H_{R}'].astype(float); A = AREA[R]
        ks = np.arange(8, 21)
        ok = H[ks] > 0
        cnt = H[ks]
        if ok.sum() >= 5:
            w = np.sqrt(cnt[ok])                       # weights 1/se of ln count
            Xm = np.stack([np.ones(ok.sum()), ks[ok]], 1) * w[:, None]
            coef, *_ = np.linalg.lstsq(Xm, np.log(cnt[ok]) * w, rcond=None)
            cov = np.linalg.inv(Xm.T @ Xm)
            loc = [np.log(H[k + 1] / H[k]) if H[k] > 0 and H[k + 1] > 0 else np.nan for k in (8, 12, 16, 19)]
            print(f"  A = {A}: counts at k = 8, 12, 20: {H[8]:.0f}, {H[12]:.0f}, {H[20]:.0f}; weighted slope {coef[1]:.3f} +- {np.sqrt(cov[1, 1]):.3f}; "
                  f"local at k = 8, 12, 16, 19: " + ', '.join(f"{x:.3f}" for x in loc) + f"; smallest k with a count: {int(np.flatnonzero(H[1:] > 0)[0]) + 1}")
    print("     the histogram against the parabola of its own mean and variance (assumption M3):")
    for R in (11, 13):
        H = CUR[f'H_{R}'].astype(float); A = AREA[R]
        p = H / H.sum(); n = np.arange(A + 1)
        mean = (p * n).sum(); var = (p * n ** 2).sum() - mean ** 2
        gauss = -(n - mean) ** 2 / (2 * var) - 0.5 * np.log(2 * np.pi * var)
        lp = np.log(np.maximum(p, 1e-300))
        slope = np.gradient(lp)
        theta = {11: 0.46, 13: 0.485}[R]
        xstar = mean - theta * var
        # where does the measured local slope equal theta, and where does the parabola's
        print(f"  A = {A}: mean {mean:.2f}, variance {var:.2f}; x* A = mean - theta var = {xstar:.1f} (theta = {theta})")
        print("       n:                 " + ' '.join(f"{int(k):6d}" for k in np.round(np.linspace(4, mean, 9))))
        print("       ln p - parabola:   " + ' '.join(f"{lp[int(k)] - gauss[int(k)]:+6.2f}" for k in np.round(np.linspace(4, mean, 9))))
        print("       local slope:       " + ' '.join(f"{slope[int(k)]:6.3f}" for k in np.round(np.linspace(4, mean, 9))))
        print("       parabola's slope:  " + ' '.join(f"{-(int(k) - mean) / var:6.3f}" for k in np.round(np.linspace(4, mean, 9))))


# ----------------------------------------------------------------------------------------------------- lr8
def make_apply_left(M, kind, pi):
    """mu -> mu Q for one row over dice, contracted one cell at a time (the transpose of prob_r1.make_apply)."""
    import string
    a = pr.a_table(pi); nbs = pr.neighbours(M, kind)
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

    def apply(mu):
        A = mu.reshape((2,) * M)
        axes = [Sl(i) for i in range(M)]
        for y in range(M):
            cells, W = factors[y]
            wl = Pl(y) + ''.join(Sl(z) for z in cells)
            out = [ax for ax in axes if not (ax in [Sl(z) for z in cells if last_use[z] == y])] + [Pl(y)]
            A = np.einsum(''.join(axes) + ',' + wl + '->' + ''.join(out), A, W)
            axes = out
        A = np.einsum(''.join(axes) + '->' + ''.join(Pl(i) for i in range(M)), A)
        return A.reshape(-1)
    return apply


def qsd(M, kind, pi, iters=300):
    ap = make_apply_left(M, kind, pi)
    mu = np.ones(1 << M); mu[0] = 0; mu /= mu.sum()
    lam = 0.0
    for it in range(iters):
        nu = ap(mu); nu[0] = 0.0
        l2 = nu.sum(); nu /= l2
        if abs(l2 - lam) < 1e-14 and it > 10:
            mu, lam = nu, l2; break
        mu, lam = nu, l2
    return mu, lam


def lr8():
    pi = pr.LAWS['Bin(2, 0.472)']
    print("LR8'. D2(0.472), quasi-stationary law mu. Decrement = -ln[E(l+1)/E(l)], E(l) = mu(a window of l cells is dead)")
    for M in (12, 14, 16, 18):
        mu, lam = qsd(M, 'dead', pi)
        chk = -np.log(1 - lam)
        S = np.arange(1 << M)
        E = []
        for l in range(0, M):
            mask = 0
            for i in range(l):                      # cells 0..l-1 from the left end; cell 0 is the highest bit
                mask |= 1 << (M - 1 - i)
            E.append(mu[(S & mask) == 0].sum())
        dec = [-np.log(E[l + 1] / E[l]) for l in range(0, M - 1)]
        print(f"  segment of {M} cells (dead ends), ln tau = {chk:.4f}; corner window, l = 0..{M - 2}:")
        print("      " + ' '.join(f"{x:.3f}" for x in dec))
        # an interior window, centred
        Ei = []
        for l in range(0, M - 1):
            start = (M - l) // 2
            mask = 0
            for i in range(start, start + l):
                mask |= 1 << (M - 1 - i)
            Ei.append(mu[(S & mask) == 0].sum())
        deci = [-np.log(Ei[l + 1] / Ei[l]) for l in range(0, M - 2)]
        print(f"      centred window, l = 0..{M - 3}: " + ' '.join(f"{x:.3f}" for x in deci))
    for L in (16, 18):
        mu, lam = qsd(L, 'ring', pi)
        S = np.arange(1 << L)
        E = []
        for l in range(0, L):
            mask = 0
            for i in range(l):
                mask |= 1 << (L - 1 - i)
            E.append(mu[(S & mask) == 0].sum())
        dec = [-np.log(E[l + 1] / E[l]) for l in range(0, L - 1)]
        print(f"  ring of {L} cells, ln tau = {-np.log(1 - lam):.4f}; window, l = 0..{L - 2}:")
        print("      " + ' '.join(f"{x:.3f}" for x in dec))


# ---------------------------------------------------------------------------------------------------- deep
def deep():
    print("path's Corollary 4a: 'd-deep' cells (all three d-upward neighbours in the hull), d = (1,1,1)")
    for R in (7, 9, 11):
        cells, c = g3.hull(R, 'c'); cs = set(cells)
        d = (1, 1, 1)
        bad = 0; n = 0
        for p in cells:
            a = g3.axis(p)
            up = [o for o in g3.OFF[a] if sum(o) > 0]
            deep_true = all((p[0] + o[0], p[1] + o[1], p[2] + o[2]) in cs for o in up)
            t = sum(p)
            cond = t <= R - 4
            for i in range(3):
                dp = list(d); dp[i] = -1
                v = sum(dp[j] * p[j] for j in range(3))
                cond &= v <= (R - 4 if i == a else R - 2)
            bad += (cond != deep_true); n += 1
        check(bad == 0, f"hull R = {R}: the stated inequalities characterise the d-deep cells ({n} cells, {bad} disagreements)")


if __name__ == '__main__':
    dict(pbar=pbar, lr4=lr4, lr5=lr5, lr6=lr6, lr7=lr7, lr8=lr8, deep=deep)[sys.argv[1]]()
    print('ALL OK' if OK else 'SOMETHING FAILED')
