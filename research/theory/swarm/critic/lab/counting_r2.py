"""Critic's lab: checks and lab requests for counting, round 2 (exact; no sampling).

  python3 counting_r2.py lemma7        Lemma 7 (a live edge cell thins its own support) by enumeration (seconds)
  python3 counting_r2.py lemma6        Lemma 6 (gaps persist) on every state of two strips; the local fact behind claim 18
  python3 counting_r2.py ckcheck       validation of the fixed-age transfer matrices of D2 (2 min)
  python3 counting_r2.py ck [kmax]     request 1: fixed-age exponents c_k of the one-row dice model D2, k = 1..kmax
                                       (default 5: 1 min; 6: 25 min more; results are cached in data/counting_r2_ck.json)
  python3 counting_r2.py profile       request 1: density of the row generation by generation in the dying ensembles, k <= 4
  python3 counting_r2.py steady        request 1: exact ln tau of D2(M, 1/2) on dead-ended intervals, M = 12..19 (1 min)
  python3 counting_r2.py ages [Lmax]   request 1, the other order of limits: exact hazard by age on rings of L <= Lmax
                                       cells from a Bernoulli row (default 18: 3 min)
  python3 counting_r2.py ringint       fixed-age death probabilities on a ring against an interval, k = 2, 3
  python3 counting_r2.py gap2          request 2: the horizon-2 exponents V1, V2, V3 against the true rule's c_2
  python3 counting_r2.py tilt          request 3: the tilted (Perron) measures of M_1 and M_2 (1 min)
  python3 counting_r2.py tri           request 5: lone cell and lone triangle of a periodic gump face over dice
  python3 counting_r2.py small         every face configuration of one, two or three nearby cells: P(face empty next) over dice
  python3 counting_r2.py gump1         request 4: gump's one-generation exponent on a strip three top cubes wide,
                                       and on the whole 3 x 3 periodic face (4 min)

How each part is validated (every command prints its own checks and ends with ALL OK or SOMETHING FAILED):
  ck       The transfer matrix on windows of four cells of the rows S_0..S_{k-1} exists in two codes: `d2_matrix`
           (explicit, k <= 4) and `d2_step` (the same product contracted row by row, any k). `ckcheck` shows that
           tr(M^L) of the first equals P(row empty at generation k) computed from the kernel of prob_r1.py on rings of
           5..7 cells (k = 1..4, two parameter pairs), that the two codes agree on a random vector, and that power
           iteration agrees with a dense eigenvalue solver for k <= 3.
  gap2     the three models are summed directly over (S_0, S_1) on a ring of 6 and compared with tr(M^6).
  tilt     k = 1: the conditional density on rings from the matrix against every state of the strips 3 x 6..8;
           k = 2: the generation-0 and generation-1 densities on a ring of 5 against every state of the strip 5 x 5.
  tri      the true rule is stepped on the slab 4 x 4 x 4 for every pattern beneath each cube concerned.
  gump1    the per-cube weights are checked against every state of the slabs 1 x 1 x 3, 2 x 1 x 3 and 2 x 1 x 4 stepped
           by the true rule; the strip matrix is checked against the whole 3 x 3 torus (tr M^3 = sum over 2^27 faces).
"""
import sys, os, json, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prob_r1 as pr
import counting_r1 as c1m
import startpoints as sp
import gump_lab as g3
import exact
import toy2d_lab as t2

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'data', 'counting_r2_ck.json')
OK = True
binl = lambda r: ((1 - r) ** 2, 2 * r * (1 - r), r * r)
PAIRS = ((0.5, 0.5), (0.472, 0.472), (0.6455, 0.472))


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def rule(s, n):
    return ((n + s >= 3) & (n <= 4)).astype(np.int64)


# -------------------------------------------------------------------------------------------------- lemma 7
def lemma7():
    # cells: (x,0); (x,1) with its row neighbours x+-1, x+-2; (x,2) with its row neighbours; (x,3); (x,4)
    names = ['e0', 'c1', 'c2', 'c3', 'c4'] + ['a%d' % i for i in range(4)] + ['b%d' % i for i in range(4)]
    cnt = {}
    for bits in itertools.product((0, 1), repeat=len(names)):
        v = dict(zip(names, bits))
        n1 = v['e0'] + v['c2'] + v['c3'] + sum(v['a%d' % i] for i in range(4))
        n2 = v['e0'] + v['c1'] + v['c3'] + v['c4'] + sum(v['b%d' % i] for i in range(4))
        y1 = int(n1 + v['c1'] >= 3 and n1 <= 4); y2 = int(n2 + v['c2'] >= 3 and n2 <= 4)
        key = (v['e0'], y1, y2)
        cnt[key] = cnt.get(key, 0) + 1
    tot = 1 << (len(names) - 1)
    p1 = {s: sum(c for (e, a, b), c in cnt.items() if e == s and a) / tot for s in (0, 1)}
    p2 = {s: sum(c for (e, a, b), c in cnt.items() if e == s and b) / tot for s in (0, 1)}
    check(abs(p1[0] - 85 / 128) < 1e-12 and abs(p1[1] - 76 / 128) < 1e-12 and abs(p2[0] - 161 / 256) < 1e-12 and abs(p2[1] - 119 / 256) < 1e-12,
          f"Lemma 7: P((x,1) alive at 1 | s) = {p1[0]:.6f}, {p1[1]:.6f} (85/128, 76/128); P((x,2) alive at 1 | s) = {p2[0]:.6f}, {p2[1]:.6f} (161/256, 119/256)")
    pair = {s: [cnt.get((s, a, b), 0) / tot for a in (0, 1) for b in (0, 1)] for s in (0, 1)}
    print("       joint law of ((x,1), (x,2)) at generation 1 given s: (00, 01, 10, 11) =", [round(v, 5) for v in pair[0]], "for s = 0;",
          [round(v, 5) for v in pair[1]], "for s = 1")
    return cnt, tot


def lemma6():
    print("Lemma 6 (gaps persist) and claim 18, by enumeration")
    for (H, L) in ((3, 8), (4, 6)):
        F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
        s = np.arange(len(F), dtype=np.uint32)
        bad = 0
        for x in range(L):
            win = sum(1 << ((x + d) % L) for d in (-2, -1, 0, 1, 2))
            bad += int((((s & np.uint32(win)) == 0) & (((F >> np.uint32(x)) & 1) == 1)).sum())
        check(bad == 0, f"strip {H} x {L}, every state: an edge cell that is dead with its four in-row neighbours dead is dead next (violations: {bad})")
    # claim 18: a cell with four free neighbours and m in 0..4 fixed live ones cannot be held (live or dead) against every outside
    held = [(x, m) for x in (0, 1) for m in range(5) if all(int(n + x >= 3 and n <= 4) == x for n in range(m, m + 5))]
    check(held == [], "a cell with four neighbours outside the pattern keeps its state against every outside for no (state, count of live pattern neighbours)")


# ------------------------------------------------------------------- D2 at a fixed age: two transfer codes
def d2_matrix(k, p, laws, cond_law=None):
    """Transfer matrix of P(row empty at generation k) for one row of the 2D rule over dice, row 0 started
    Bernoulli(p). laws[t] = law (pi0, pi1, pi2) of b at the step t -> t+1. cond_law (k = 2 only): a dict
    (s0, s1) -> law used for the step 1 -> 2 (s0, s1 = the cell's own states at generations 0, 1).
    States: windows (x-2, x-1, x, x+1) of the rows S_0..S_{k-1}, bit 4t+i = S_t(x-2+i); 2^k new bits per step.
    Returns W[state, new], nxt[state, new]."""
    A = [pr.a_table(l) for l in laws]
    Ac = {key: pr.a_table(l) for key, l in cond_law.items()} if cond_law is not None else None
    nst = 1 << (4 * k)
    S = np.arange(nst, dtype=np.int64)
    win = [[(S >> (4 * t + i)) & 1 for i in range(4)] for t in range(k)]
    W = np.zeros((nst, 1 << k)); nxt = np.zeros((nst, 1 << k), np.int64)
    for new in range(1 << k):
        nb = [(new >> t) & 1 for t in range(k)]                                    # S_t(x+2)
        w = np.where(win[0][2] == 1, p, 1 - p).astype(float)
        for t in range(k):
            kk = win[t][0] + win[t][1] + win[t][3] + nb[t]
            s = win[t][2]
            if Ac is not None and t == 1:
                pa = np.zeros(nst)
                for (s0, s1), tab in Ac.items():
                    m = (win[0][2] == s0) & (win[1][2] == s1)
                    pa[m] = tab[s[m], kk[m]]
            else:
                pa = A[t][s, kk]
            w = w * (np.where(win[t + 1][2] == 1, pa, 1 - pa) if t + 1 < k else 1 - pa)
        W[:, new] = w
        st = np.zeros(nst, np.int64)
        for t in range(k):
            st |= ((win[t][1]) | (win[t][2] << 1) | (win[t][3] << 2) | (nb[t] << 3)) << (4 * t)
        nxt[:, new] = st
    return W, nxt


def matrix_perron(W, nxt, iters=20000, tol=1e-14):
    nst = W.shape[0]
    v = np.ones(nst) / nst; lam = 0.0
    flat = nxt.ravel()
    for it in range(iters):
        u = np.bincount(flat, weights=(v[:, None] * W).ravel(), minlength=nst)
        l2 = u.sum(); u /= l2
        if it > 50 and abs(l2 - lam) < tol * l2:
            lam = l2; v = u; break
        v, lam = u, l2
    return lam, v


def matrix_trace(W, nxt, k, L):
    """tr(M^L) as a sum over L-periodic sequences of new-bit k-tuples."""
    seqs = np.indices(((1 << k),) * L).reshape(L, -1).T.astype(np.int64)
    st = np.zeros(len(seqs), np.int64)
    for t in range(k):
        for i in range(4):
            st |= ((seqs[:, (-4 + i) % L] >> t) & 1) << (4 * t + i)
    w = np.ones(len(seqs))
    for x in range(L):
        w *= W[st, seqs[:, x]]
        st = nxt[st, seqs[:, x]]
    return float(w.sum())


def d2_tables(k, laws):
    out = []
    for t in range(k):
        A = pr.a_table(laws[t])
        F = np.zeros((2,) * 6)
        for a, b, c, d, e in itertools.product((0, 1), repeat=5):
            pa = A[c, a + b + d + e]
            F[a, b, c, d, e, 1] = pa; F[a, b, c, d, e, 0] = 1 - pa
        out.append(F)
    return out


def d2_step(X, k, F, p):
    """the same matrix applied from the left, row by row. X has 4k binary axes, axis 4t+i <-> S_t(x-2+i)."""
    for t in range(k):
        src = [4 * t, 4 * t + 1, 4 * t + 2, 4 * t + 3]
        last = (t == k - 1)
        if not last:
            src.append(4 * t + 6)                           # S_{t+1}(x), not yet shifted
        Xm = np.moveaxis(X, src, list(range(len(src))))
        out = np.zeros(Xm.shape)
        rest = Xm.ndim - len(src)
        for a in (0, 1):
            for e in (0, 1):
                f = (F[t][a, :, :, :, e, 0].reshape((2, 2, 2) + (1,) * rest) if last
                     else F[t][a, :, :, :, e, :].reshape((2, 2, 2, 2) + (1,) * rest))
                if t == 0:
                    f = f * np.array([1 - p, p]).reshape((1, 2, 1) + (1,) * (f.ndim - 3))
                out[:, :, :, e] += Xm[a] * f
        X = np.moveaxis(out, list(range(len(src))), src)
    return X


def d2_exponent(k, p, laws, iters=20000, tol=1e-11):
    """c_k = -ln(Perron eigenvalue), by power iteration with d2_step."""
    F = d2_tables(k, laws)
    X = np.full((2,) * (4 * k), 1.0 / (1 << (4 * k)))
    lam = 0.0
    for it in range(iters):
        Y = d2_step(X, k, F, p)
        l2 = Y.sum(); Y /= l2
        if it > 30 and abs(l2 - lam) < tol * l2:
            lam = l2; break
        X, lam = Y, l2
    return float(-np.log(lam)), it


def dk_kernel(L, p, pi, kmax, kind='ring'):
    """P(row empty at generation k), k = 0..kmax, row started Bernoulli(p): by the kernel of prob_r1.py."""
    ap = pr.make_apply(L, kind, pi)
    S = np.arange(1 << L)
    pop = np.zeros(1 << L, np.int64)
    for i in range(L):
        pop += (S >> i) & 1
    nu = p ** pop * (1 - p) ** (L - pop)
    f = np.zeros(1 << L); f[0] = 1.0
    out = [float(nu @ f)]
    for _ in range(kmax):
        f = ap(f)
        out.append(float(nu @ f))
    return np.array(out)


def ckcheck():
    print("validation of the fixed-age transfer matrices of D2")
    for (p, rho) in ((0.5, 0.5), (0.6455, 0.472)):
        pi = binl(rho)
        for k in (1, 2, 3, 4):
            W, nxt = d2_matrix(k, p, [pi] * k)
            for L in ((5, 6, 7) if k <= 2 else (5, 6) if k == 3 else (5,)):
                D = dk_kernel(L, p, pi, k)[k]
                tr = matrix_trace(W, nxt, k, L)
                check(abs(tr - D) < 1e-12 * D, f"p = {p}, rho = {rho}, k = {k}, ring of {L}: P(empty at generation k) from the kernel {D:.12e}, tr(M^L) {tr:.12e}")
            x = np.random.default_rng(1).random(1 << (4 * k))
            u = np.bincount(nxt.ravel(), weights=(x[:, None] * W).ravel(), minlength=1 << (4 * k))
            rev = list(range(4 * k - 1, -1, -1))
            y = d2_step(x.reshape((2,) * (4 * k)).transpose(rev), k, d2_tables(k, [pi] * k), p).transpose(rev).reshape(-1)
            check(np.abs(y - u).max() < 1e-13, f"   k = {k}: the row-by-row contraction equals the explicit matrix on a random vector")
            if k <= 3:
                n = 1 << (4 * k)
                M = np.zeros((n, n)); np.add.at(M, (np.repeat(np.arange(n), 1 << k), nxt.ravel()), W.ravel())
                ev = np.linalg.eigvals(M); ev = ev[np.argsort(-np.abs(ev))]
                c, _ = d2_exponent(k, p, [pi] * k)
                check(abs(-np.log(abs(ev[0])) - c) < 1e-8, f"   k = {k}: dense eigenvalue c = {-np.log(abs(ev[0])):.9f}, power iteration {c:.9f}; "
                                                          f"second eigenvalue / first = {abs(ev[1]) / abs(ev[0]):.4f}")
    check(abs(d2_exponent(1, 0.5, [binl(0.5)])[0] - 0.551535) < 1e-6, "k = 1, p = rho = 1/2 is the true rule's c_1 = 0.551535")


def ck(kmax=5):
    print("request 1: c_k = -lim (1/L) ln P(row empty at generation k), D2 on a ring, row started Bernoulli(p), dice Bin(2, rho)")
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for p, rho in PAIRS:
        vals = []
        for k in range(1, kmax + 1):
            key = f"{p},{rho},{k}"
            if key not in cache:
                t0 = time.time()
                c, it = d2_exponent(k, p, [binl(rho)] * k)
                cache[key] = c
                json.dump(cache, open(CACHE, 'w'), indent=0)
            vals.append(cache[key])
        print(f"   p = {p}, rho = {rho}: c_1..c_{kmax} = " + ', '.join(f"{c:.6f}" for c in vals))
        d = [a - b for a, b in zip(vals, vals[1:])]
        print("        decrements c_k - c_k+1: " + ', '.join(f"{x:.5f}" for x in d) + ";  ratios: " + ', '.join(f"{b / a:.3f}" for a, b in zip(d, d[1:])))
        if len(d) >= 2:
            r = d[-1] / d[-2]
            geo = vals[-1] - d[-1] * r / (1 - r)
            kk = len(vals)
            pw = vals[-1] - d[-1] * (kk - 1) ** 2 * sum(1.0 / j ** 2 for j in range(kk, 200000))
            print(f"        two extrapolations of the limit (neither is a bound): geometric with the last ratio {geo:.4f}; decrements ~ 1/k^2: {pw:.4f}")
    print("   steady exponents of D2 to set beside them (steps of ln tau, exact; prob_r1.py):")
    print("     rho = 1/2:   ring L = 15..18: 0.543, 0.528, 0.528, 0.533;  interval with dead ends M = 13..19: 0.476, 0.470, 0.475, 0.480, 0.480, 0.479, 0.478")
    print("     rho = 0.472: ring L = 15..18: 0.536, 0.523, 0.522, 0.526;  interval with dead or reflecting ends M = 15..19: 0.460")
    full = -np.log(0.6455 * (1 - (1 - 0.472) ** 2))
    print(f"   note: at p = 0.6455 the completely live row dies at once with cost -ln(p (1 - pi_0)) = {full:.4f} per cell: c_1 = 0.7596 there is the overcrowding route")


def profile(kmax=4):
    """density of the row at generations 0..k-1 in the tilted (dying) ensemble of the fixed-age matrix, k <= 4."""
    print("request 1, what the dying ensembles look like: density of the row at generations 0..k-1 given that it is empty at generation k (L -> infinity)")
    for (p, rho) in PAIRS:
        for k in range(1, kmax + 1):
            W, nxt = d2_matrix(k, p, [binl(rho)] * k)
            lam, v = matrix_perron(W, nxt)
            u = np.ones(W.shape[0])
            for it in range(20000):
                u2 = (W * u[nxt]).sum(1); u2 /= u2.sum()
                done = it > 50 and np.abs(u2 - u).max() < 1e-15
                u = u2
                if done: break
            mu = v * u; mu /= mu.sum()
            S = np.arange(W.shape[0])
            dens = [float((mu * ((S >> (4 * t + 2)) & 1)).sum()) for t in range(k)]
            print(f"   p = {p}, rho = {rho}, k = {k} (c_k = {-np.log(lam):.4f}): " + ', '.join(f"{d:.3f}" for d in dens))
    # check of the k = 1 value at p = rho = 1/2 against `tilt` (0.0942, itself checked against every state of small strips)
    W, nxt = d2_matrix(1, 0.5, [binl(0.5)])
    lam, v = matrix_perron(W, nxt)
    u = np.ones(16)
    for it in range(2000):
        u = (W * u[nxt]).sum(1); u /= u.sum()
    mu = v * u; mu /= mu.sum()
    check(abs(float((mu * ((np.arange(16) >> 2) & 1)).sum()) - 0.094228) < 1e-5, "k = 1, p = rho = 1/2: 0.0942, the value of `tilt` (checked there against every state of the strips 3 x 6..8)")


def steady(Mmax=19):
    print("steady exponents of D2 at rho = 1/2 to set beside c_k: ln tau on an interval with dead ends (rho = 0.472: board L4.2)")
    prev = None
    for M in range(12, Mmax + 1):
        lt = pr.lntau(M, 'dead', binl(0.5))[0]
        print(f"   M = {M}: ln tau = {lt:.4f}" + ('' if prev is None else f"   step {lt - prev:.4f}"), flush=True)
        prev = lt


def ages(Lmax=18):
    print("request 1, the other order of limits: D2 on a ring of L cells from a Bernoulli(p) row; hazard at age j, P(T = j+1 | T > j), over the quasi-stationary hazard")
    for (p, rho) in PAIRS:
        for L in range(10, Lmax + 1, 2):
            pi = binl(rho)
            D = dk_kernel(L, p, pi, 26)
            haz = (D[1:] - D[:-1]) / (1 - D[:-1])
            lt, lam = pr.lntau(L, 'ring', pi)
            hq = np.exp(-lt)
            print(f"   p = {p}, rho = {rho}, L = {L}: ln tau = {lt:.4f}; P(dead by k = 1..5) = " + ' '.join(f"{d:.3e}" for d in D[1:6]) +
                  "; hazard(j)/h, j = 0..9: " + ' '.join(f"{haz[j] / hq:.3f}" for j in range(10)) + f"; j = 15, 25: {haz[15] / hq:.4f}, {haz[25] / hq:.4f}", flush=True)
            if L == 10:
                check(abs(haz[25] / hq - 1) < 1e-3, "      the hazard at age 25 equals the quasi-stationary hazard (L = 10)")


def ringint():
    print("fixed age, ring against interval with dead ends (D2, exact transfer matrix): local slopes -ln D_k(L+1)/D_k(L)")
    for (p, rho) in ((0.5, 0.5), (0.6455, 0.472)):
        pi = binl(rho)
        for k in (2, 3):
            W, nxt = d2_matrix(k, p, [pi] * k)
            n = 1 << (4 * k)
            M = np.zeros((n, n)); np.add.at(M, (np.repeat(np.arange(n), 1 << k), nxt.ravel()), W.ravel())
            # ring: tr(M^L) = sum of the L-th powers of the eigenvalues. Interval of L cells with dead ends (cells 1..L;
            # the cells outside are dead for ever and carry no weight): the walk starts from any window (-1, 0, 1, 2) whose
            # cells -1, 0 are dead in every row, takes L steps (one per cell), and ends in a window (L-1, L, L+1, L+2)
            # whose cells L+1, L+2 are dead in every row.
            Ls = list(range(5, 61))
            ev = np.linalg.eigvals(M)
            c = -np.log(max(abs(ev)))
            ring = {L: float(np.sum(ev ** L).real) for L in Ls + [61]}
            start = np.array([all(((s >> (4 * t)) & 3) == 0 for t in range(k)) for s in range(n)])
            end = np.array([all(((s >> (4 * t + 2)) & 3) == 0 for t in range(k)) for s in range(n)])
            itv = {}
            vec = start.astype(float)
            for L in range(1, 62):
                vec = vec @ M
                itv[L] = float(vec[end].sum())
            if k == 2:
                tr = matrix_trace(W, nxt, k, 6)
                check(abs(ring[6] - tr) < 1e-12 * tr, f"ring of 6, k = {k}: sum of eigenvalue powers {ring[6]:.10e} = sum over periodic sequences {tr:.10e}")
            if k == 2:
                for Lc in (5, 6, 7):
                    D = dk_kernel(Lc, p, pi, k, kind='dead')[k]
                    check(abs(itv[Lc] - D) < 1e-12 * D, f"interval of {Lc} cells with dead ends, k = {k}: transfer walk {itv[Lc]:.10e} = kernel {D:.10e}")
            rs = lambda dct, L: -np.log(dct[L + 1] / dct[L])
            print(f"   p = {p}, rho = {rho}, k = {k} (c_k = {c:.4f}): ring, L = 10, 14, 18, 24, 32, 44, 58: " + ' '.join(f"{rs(ring, L):.4f}" for L in (10, 14, 18, 24, 32, 44, 58)) +
                  ";  interval: " + ' '.join(f"{rs(itv, L):.4f}" for L in (10, 14, 18, 24, 32, 44, 58)))
            print(f"        ln D_k(ring L) - ln D_k(interval L) at L = 10, 18, 32, 58: " + ' '.join(f"{np.log(ring[L] / itv[L]):+.3f}" for L in (10, 18, 32, 58)))


# ----------------------------------------------------------------------------------------------------- gap2
def pair_laws():
    """true rule, uniform soup, half-plane: law of b_1 = (x,1) + (x,2) at generation 1; and the same given (s0, s1),
    the states of (x,0) at generations 0 and 1; and given s0 alone (Lemma 7)."""
    names = ['e0', 'c1', 'c2', 'c3', 'c4'] + ['a%d' % i for i in range(4)] + ['b%d' % i for i in range(4)] + ['r%d' % i for i in range(4)]
    joint = {}
    for bits in itertools.product((0, 1), repeat=len(names)):
        v = dict(zip(names, bits))
        n1 = v['e0'] + v['c2'] + v['c3'] + sum(v['a%d' % i] for i in range(4))
        n2 = v['e0'] + v['c1'] + v['c3'] + v['c4'] + sum(v['b%d' % i] for i in range(4))
        y1 = int(n1 + v['c1'] >= 3 and n1 <= 4); y2 = int(n2 + v['c2'] >= 3 and n2 <= 4)
        n0 = sum(v['r%d' % i] for i in range(4)) + v['c1'] + v['c2']
        s1 = int(n0 + v['e0'] >= 3 and n0 <= 4)
        key = (v['e0'], s1, y1 + y2)
        joint[key] = joint.get(key, 0) + 1
    tot = float(1 << len(names))
    marg = tuple(sum(c for (s0, s1, b), c in joint.items() if b == bb) / tot for bb in range(3))
    cond = {}
    for s0 in (0, 1):
        for s1 in (0, 1):
            z = sum(c for (a, b_, bb), c in joint.items() if a == s0 and b_ == s1)
            cond[(s0, s1)] = tuple(joint.get((s0, s1, bb), 0) / z for bb in range(3))
    cond0 = {}
    for s0 in (0, 1):
        z = sum(c for (a, b_, bb), c in joint.items() if a == s0)
        cond0[s0] = tuple(sum(joint.get((s0, s1, bb), 0) for s1 in (0, 1)) / z for bb in range(3))
    return marg, cond, cond0


def gap2_direct(L, law1, cond=None):
    """P(row empty at generation 2) on a ring of L: fair row, fair dice at the step 0 -> 1, law1 (or cond) at 1 -> 2."""
    A0 = pr.a_table(binl(0.5))
    A1 = pr.a_table(law1)
    Ac = {key: pr.a_table(l) for key, l in cond.items()} if cond is not None else None
    tot = 0.0
    for S0 in range(1 << L):
        b0 = [(S0 >> i) & 1 for i in range(L)]
        k0 = [b0[(x - 2) % L] + b0[(x - 1) % L] + b0[(x + 1) % L] + b0[(x + 2) % L] for x in range(L)]
        for S1 in range(1 << L):
            b1 = [(S1 >> i) & 1 for i in range(L)]
            w = 0.5 ** L
            for x in range(L):
                pa = A0[b0[x], k0[x]]
                w *= pa if b1[x] else 1 - pa
            if w == 0:
                continue
            for x in range(L):
                k1 = b1[(x - 2) % L] + b1[(x - 1) % L] + b1[(x + 1) % L] + b1[(x + 2) % L]
                tab = A1 if Ac is None else Ac[(b0[x], b1[x])]
                w *= 1 - tab[b1[x], k1]
            tot += w
    return tot


def gap2():
    print("request 2: horizon 2, uniform start (density 1/2); exponent per cell of P(row 0 empty at generation 2)")
    marg, cond, cond0 = pair_laws()
    mean = lambda l: l[1] + 2 * l[2]
    check(abs(mean(marg) - 602 / 512) < 1e-12 and abs(mean(cond0[0]) - 331 / 256) < 1e-12 and abs(mean(cond0[1]) - 271 / 256) < 1e-12,
          f"law of b at generation 1 (true rule from soup): {tuple(round(x, 5) for x in marg)}, mean {mean(marg):.4f} = 602/512; "
          f"given s0 = 0, 1 the means are 331/256, 271/256 (Lemma 7)")
    for key in sorted(cond):
        print(f"       given (s0, s1) = {key}: {tuple(round(x, 5) for x in cond[key])}, mean {mean(cond[key]):.4f}")
    out = {}
    for name, law1, cl in (('V1', binl(0.5), None), ('V2', marg, None), ('V3', marg, cond)):
        W, nxt = d2_matrix(2, 0.5, [binl(0.5), law1], cond_law=cl)
        lam, _ = matrix_perron(W, nxt)
        out[name] = -np.log(lam)
        direct = gap2_direct(6, law1, cl)
        tr = matrix_trace(W, nxt, 2, 6)
        check(abs(direct - tr) < 1e-13, f"{name}: ring of 6, direct sum over (S_0, S_1) {direct:.12f} = tr(M^6) {tr:.12f}")
    v0 = 0.467693
    print(f"   V0 (true rule) = {v0:.6f};  V1 (fresh fair dice at generation 1) = {out['V1']:.6f};  V2 (dice with the true law of b_1) = {out['V2']:.6f};  "
          f"V3 (law of b_1 given the cell's own two states) = {out['V3']:.6f}")
    print(f"   V1 - V2 = {out['V1'] - out['V2']:+.4f} (density);  V2 - V3 = {out['V2'] - out['V3']:+.4f} (own-column feedback);  "
          f"V3 - V0 = {out['V3'] - v0:+.4f} (everything spatial);  V1 - V0 = {out['V1'] - v0:+.4f}")


# ----------------------------------------------------------------------------------------------------- tilt
def tilt():
    print("request 3: the tilted (Perron) measures of the horizon-1 and horizon-2 matrices at density 1/2")
    T = c1m.k1_matrix(0.5)
    ev, R = np.linalg.eig(T); i = int(np.argmax(ev.real)); r = np.abs(R[:, i].real)
    ev2, Lv = np.linalg.eig(T.T); j = int(np.argmax(ev2.real)); l = np.abs(Lv[:, j].real)
    P5 = np.zeros(32)                                      # windows (a, b, c, d, e), a the highest bit
    for s in range(16):
        for e in (0, 1):
            t = ((s << 1) & 15) | e
            P5[(s << 1) | e] += l[s] * T[s, t] * r[t]
    P5 /= P5.sum()
    dens = sum(P5[w] for w in range(32) if (w >> 2) & 1)
    # validation: the conditional density on a ring of L from the matrix, against every state of the strip 3 x L
    T1 = T * np.array([(s >> 1) & 1 for s in range(16)])[:, None]          # centre cell c alive
    for L in (6, 7, 8):
        F = exact.full_map(t2.nbrs(3, L, True), t2.B, t2.S)
        dead = (F & np.uint32((1 << L) - 1)) == 0
        st = np.flatnonzero(dead)
        pop = np.zeros(len(st), np.int64)
        for b in range(L):
            pop += (st >> b) & 1
        brute = pop.sum() / (L * len(st))
        mat = np.trace(np.linalg.matrix_power(T, L - 1) @ T1) / np.trace(np.linalg.matrix_power(T, L))
        check(abs(brute - mat) < 1e-12, f"k = 1, strip 3 x {L}, every state: density of row 0 given that it is empty next: {brute:.6f}; from the matrix {mat:.6f}")
    big = [np.trace(np.linalg.matrix_power(T, L - 1) @ T1) / np.trace(np.linalg.matrix_power(T, L)) for L in (16, 32, 64)]
    check(abs(big[-1] - dens) < 1e-6, f"k = 1: ring of 16, 32, 64: {big[0]:.6f}, {big[1]:.6f}, {big[2]:.6f} -> Perron value {dens:.6f}")
    print(f"   k = 1: density of live edge cells at generation 0 in the dying ensemble: {dens:.4f} (soup 0.5); window 00000: {P5[0]:.4f} (soup 0.0312); "
          f"isolated live cell 00100: {P5[4]:.4f} (soup 0.0312); full window 11111: {P5[31]:.4f}; 01010 + 10101: {P5[10] + P5[21]:.4f}")
    top = np.argsort(-P5)[:6]
    print("          most frequent five-cell windows: " + ', '.join(f"{format(int(w), '05b')} {P5[w]:.4f}" for w in top))
    # k = 2
    W, nxt = c1m.k2_weights(0.5)
    nst = 1 << 16
    S64 = np.arange(nst, dtype=np.int64)
    r0 = [(S64 >> i) & 1 for i in range(8)]
    r1 = [(S64 >> (8 + i)) & 1 for i in range(4)]; r2 = [(S64 >> (12 + i)) & 1 for i in range(4)]
    W1 = np.zeros((nst, 8))                               # the part of W with the centre cell (x, 0) alive at generation 1
    for new in range(8):
        a0, a1, a2 = new & 1, (new >> 1) & 1, (new >> 2) & 1
        R0 = r0 + [np.full_like(S64, a0)]; R1 = r1 + [np.full_like(S64, a1)]; R2 = r2 + [np.full_like(S64, a2)]
        g0 = []
        for c in range(-2, 3):
            n = R0[c + 2] + R0[c + 3] + R0[c + 5] + R0[c + 6] + R1[c + 2] + R2[c + 2]
            g0.append(rule(R0[c + 4], n))
        for r3 in (0, 1):
            for r4 in (0, 1):
                n1 = R1[0] + R1[1] + R1[3] + R1[4] + R0[4] + R2[2] + r3
                y1 = rule(R1[2], n1)
                n2 = R2[0] + R2[1] + R2[3] + R2[4] + R1[2] + R0[4] + r3 + r4
                y2 = rule(R2[2], n2)
                G = rule(g0[2], g0[0] + g0[1] + g0[3] + g0[4] + y1 + y2)
                W1[:, new] += (G == 0) * g0[2] / 32.0
    W0 = W * r0[4][:, None]                               # centre cell alive at generation 0
    # validation on the strip 5 x 5, every state
    L = 5
    F = exact.full_map(t2.nbrs(5, L, True), t2.B, t2.S)
    mask = np.uint32((1 << L) - 1)
    st = np.flatnonzero((F[F] & mask) == 0)
    pop0 = np.zeros(len(st), np.int64); pop1 = np.zeros(len(st), np.int64)
    f1 = F[st]
    for b in range(L):
        pop0 += (st >> b) & 1; pop1 += (f1 >> np.uint32(b)) & 1
    b0 = pop0.sum() / (L * len(st)); b1 = pop1.sum() / (L * len(st))

    def ring(Wa):
        seqs = np.indices((8,) * L).reshape(L, -1).T.astype(np.int64)
        s = np.zeros(len(seqs), np.int64)
        for i in range(8):
            s |= (seqs[:, (-8 + i) % L] & 1) << i
        for i in range(4):
            s |= ((seqs[:, (-4 + i) % L] >> 1) & 1) << (8 + i)
            s |= ((seqs[:, (-4 + i) % L] >> 2) & 1) << (12 + i)
        w = np.ones(len(seqs))
        for x in range(L):
            w *= (Wa if x == 0 else W)[s, seqs[:, x]]
            s = nxt[s, seqs[:, x]]
        return w.sum()
    z = ring(W)
    check(abs(ring(W0) / z - b0) < 1e-12 and abs(ring(W1) / z - b1) < 1e-12,
          f"k = 2, strip 5 x 5, every state ({len(st)} with row 0 empty at generation 2): density of row 0 at generation 0: {b0:.6f}, at generation 1: {b1:.6f}; "
          f"from the transfer weights {ring(W0) / z:.6f}, {ring(W1) / z:.6f}")
    flat = nxt.ravel()
    v = np.ones(nst) / nst; u = np.ones(nst) / nst
    for it in range(3000):
        v2 = np.bincount(flat, weights=(v[:, None] * W).ravel(), minlength=nst); lam2 = v2.sum(); v2 /= lam2
        u2 = (W * u[nxt]).sum(1); u2 /= u2.sum()
        done = it > 50 and np.abs(v2 - v).max() < 1e-15 and np.abs(u2 - u).max() < 1e-15
        v, u = v2, u2
        if done:
            break
    den = float((v[:, None] * W * u[nxt]).sum())
    d0 = float((v[:, None] * W0 * u[nxt]).sum()) / den
    d1 = float((v[:, None] * W1 * u[nxt]).sum()) / den
    mu = v * u; mu /= mu.sum()
    w5 = sum(r0[i] << (i - 2) for i in range(2, 7))              # cells x-2..x+2, x the bit 2
    P5b = np.bincount(w5, weights=mu, minlength=32)
    check(abs(5 * np.log(2) - np.log(lam2 * 32) - 0.467693) < 1e-6 and abs(float((mu * r0[4]).sum()) - d0) < 1e-9,
          f"k = 2: Perron eigenvalue gives c_2 = {5 * np.log(2) - np.log(lam2 * 32):.6f}; the two ways of computing the generation-0 density agree")
    print(f"   k = 2: density of live edge cells at generation 0: {d0:.4f}; at generation 1: {d1:.4f}; window 00000 at generation 0: {P5b[0]:.4f}; "
          f"isolated live cell 00100: {P5b[4]:.4f}; full window 11111: {P5b[31]:.4f}")
    top = np.argsort(-P5b)[:6]
    print("          most frequent five-cell windows at generation 0 (bit order x+2..x-2): " + ', '.join(f"{format(int(w), '05b')} {P5b[w]:.4f}" for w in top))


# ------------------------------------------------------------------------------- gump faces over dice
def face_data(a, b, m=4):
    cells, nb = sp.make_slab(a, b, m)
    face = [i for i, cc in enumerate(cells) if cc[2] == -1]
    fs = set(face)
    inl = {i: [j for j in nb[i] if j in fs] for i in face}
    ben = {i: [j for j in nb[i] if j not in fs] for i in face}
    comps, _ = sp.components(face, ben)
    return cells, nb, face, inl, ben, comps


def unit_table(cp, ben, rho):
    """for one component cp of 'shares a cell beneath' (a cube triple): tab[(x_1, k_1), ..] = probability over product
    dice of density rho beneath that every cell of cp is dead next, given each cell's state x and in-face count k.
    Key = sum over the cells of (7 x + k) * 14^position (first cell most significant)."""
    und = sorted(set(j for i in cp for j in ben[i]))
    mult = {}
    for bits in itertools.product((0, 1), repeat=len(und)):
        val = dict(zip(und, bits))
        t = tuple(sum(val[j] for j in ben[i]) for i in cp)
        mult[t] = mult.get(t, 0.0) + rho ** sum(bits) * (1 - rho) ** (len(und) - sum(bits))
    tab = np.zeros(14 ** len(cp))
    for combo in itertools.product(range(14), repeat=len(cp)):
        idx = 0
        for c in combo:
            idx = idx * 14 + c
        tab[idx] = sum(mu for t, mu in mult.items() if all(not ((3 if c // 7 else 4) <= (c % 7) + bb <= 5) for c, bb in zip(combo, t)))
    return tab


def face_death_prob(face, inl, ben, comps, mask_bits, rho, p=None):
    """P(face empty next | face configuration), product over the units; mask_bits: dict cell -> 0/1."""
    w = 1.0
    for cp in comps:
        tab = unit_table(cp, ben, rho)
        idx = 0
        for i in cp:
            idx = idx * 14 + 7 * mask_bits[i] + sum(mask_bits[j] for j in inl[i])
        w *= tab[idx]
    return w


def tri():
    print("request 5: periodic gump face 4 x 4 (48 cells, no doubled neighbours), slab 4 x 4 x 4, the true rule stepped once")
    cells, nb, face, inl, ben, comps = face_data(4, 4)
    N = len(cells)
    c0 = face[0]
    cube = [cp for cp in comps if c0 in cp][0]
    nbrs_tri = sorted(set(j for i in cube for j in inl[i]) - set(cube))
    ks = [sum(1 for j in inl[i] if j in cube) for i in nbrs_tri]
    cubes_n = [cp for cp in comps if any(i in nbrs_tri for i in cp)]
    check(len(nbrs_tri) == 12 and set(ks) == {1} and sorted(len([i for i in cp if i in nbrs_tri]) for cp in cubes_n) == [2] * 6,
          f"the triangle has {len(nbrs_tri)} dead in-face neighbours, each next to exactly one of its cells, two to a cube in {len(cubes_n)} cubes")
    und_all = [sorted(set(j for i in cp for j in ben[i])) for cp in comps]
    check(all(len(u) == 6 for u in und_all) and len(set(j for u in und_all for j in u)) == 6 * len(comps),
          "beneath each cube lie six cells, and no cell lies beneath two cubes (so the patterns beneath different cubes can be counted separately)")

    def count_unit(live, cp, others_alive=()):
        """number of the 64 patterns beneath the unit cp for which every cell of cp is dead after one generation of the
        true rule on the whole slab (all other cells beneath dead)."""
        und = sorted(set(j for i in cp for j in ben[i]))
        n = 0
        for bits in itertools.product((0, 1), repeat=len(und)):
            x = np.zeros(N, np.uint8)
            for i in live: x[i] = 1
            for j, bt in zip(und, bits): x[j] = bt
            y = sp.step_nb(nb, x, 4, 3, 5)
            n += all(y[i] == 0 for i in cp)
        return n
    for name, live, formula in (('lone cell', [c0], lambda r: (1 - 3 * r ** 3 + 3 * r ** 5 - r ** 6) * (1 - r ** 3) ** 4),
                                ('lone triangle', cube, lambda r: (1 - r) ** 6 * (1 - 2 * r ** 3 + r ** 5) ** 6)):
        act = set(live) | set(j for i in live for j in inl[i])
        units = [cp for cp in comps if any(i in act for i in cp)]
        counts = [count_unit(live, cp) for cp in units]
        num = 1
        for c in counts: num *= c
        tot = 64 ** len(units)
        check(abs(num / tot - formula(0.5)) < 1e-15, f"{name}: {len(units)} cubes concerned, patterns beneath each that leave its face cells dead: {sorted(counts)} of 64; "
                                                    f"product {num} of 2^{6 * len(units)} = {num / tot:.6f}; formula at rho = 1/2: {formula(0.5):.6f}")
        for rho in (0.4155, 0.52):
            val = face_death_prob(face, inl, ben, comps, {i: int(i in live) for i in face}, rho)
            check(abs(val - formula(rho)) < 1e-13, f"   rho = {rho}: product of the per-cube probabilities {val:.6f}; formula {formula(rho):.6f}")
    # the triangle's own cube: it dies iff all six beneath are dead
    und = sorted(set(j for i in cube for j in ben[i]))
    only = []
    for bits in itertools.product((0, 1), repeat=6):
        x = np.zeros(N, np.uint8)
        for i in cube: x[i] = 1
        for j, bt in zip(und, bits): x[j] = bt
        y = sp.step_nb(nb, x, 4, 3, 5)
        if all(y[i] == 0 for i in cube): only.append(bits)
    check(only == [(0,) * 6], "the triangle dies in one generation iff all six cells beneath its cube are dead")


def small(rhos=(0.5, 0.4155, 0.52)):
    """one-generation death probability of every face configuration of two or three cells lying within in-face distance 2
    of one another, on a 6 x 6 periodic face (108 cells; nothing wraps), over product dice."""
    print("gump face over product dice: P(face empty next) for the configurations of 1, 2, 3 cells (6 x 6 periodic face)")
    cells, nb, face, inl, ben, comps = face_data(6, 6)
    comp_of = {i: n for n, cp in enumerate(comps) for i in cp}
    c0 = face[0]
    d1 = set(inl[c0]); ball = {c0} | d1 | set(j for i in d1 for j in inl[i])
    tabs = {rho: [unit_table(cp, ben, rho) for cp in comps] for rho in rhos}

    def pdeath(live, rho):
        live = set(live)
        act = live | set(j for i in live for j in inl[i])
        w = 1.0
        for n in sorted(set(comp_of[i] for i in act)):
            idx = 0
            for i in comps[n]:
                idx = idx * 14 + 7 * int(i in live) + sum(1 for j in inl[i] if j in live)
            w *= tabs[rho][n][idx]
        return w

    def describe(live):
        live = list(live)
        pairs = [(a, b) for ia, a in enumerate(live) for b in live[ia + 1:]]
        same = sum(1 for a, b in pairs if comp_of[a] == comp_of[b])
        adj = sum(1 for a, b in pairs if b in inl[a])
        ax = lambda i: g3.axis((cells[i][0], cells[i][1], cells[i][2] - cells[i][0] - cells[i][1]))
        diag = sum(1 for a, b in pairs if b in inl[a] and ax(a) == ax(b))
        return (len(set(comp_of[i] for i in live)), adj, same, diag)
    one = {rho: pdeath([c0], rho) for rho in rhos}
    print("   n = 1: " + ', '.join(f"rho = {rho}: {one[rho]:.4f}" for rho in rhos))
    for n in (2, 3):
        groups = {}
        others = sorted(ball - {c0})
        for combo in itertools.combinations(others, n - 1):
            live = (c0,) + combo
            if n == 3 and not all(any(b in ball_of[a] for b in live if b != a) for a in live for ball_of in [ {x: set(inl[x]) | set(j for i in inl[x] for j in inl[i]) for x in live} ]):
                continue
            key = describe(live)
            val = tuple(round(pdeath(live, rho), 6) for rho in rhos)
            groups.setdefault((key, val), 0)
            groups[(key, val)] += 1
        print(f"   n = {n} (cells within in-face distance 2 of the first): cubes occupied, adjacent pairs, of them in one cube, of them coplanar-diagonal -> P(death) at rho = "
              + ', '.join(str(r) for r in rhos) + "   [number of such placements]")
        items = sorted(groups.items(), key=lambda kv: -kv[0][1][0])
        if n == 3:
            loose = [kv for kv in items if kv[0][0][1] < 2]
            print(f"        fewer than two adjacent pairs ({sum(c for _, c in loose)} placements): between "
                  + ', '.join(f"{min(kv[0][1][r] for kv in loose):.4f}" for r in range(len(rhos))) + " and "
                  + ', '.join(f"{max(kv[0][1][r] for kv in loose):.4f}" for r in range(len(rhos))))
            items = [kv for kv in items if kv[0][0][1] >= 2]
        for (key, val), cnt in items:
            print(f"        {key}: " + ', '.join(f"{v:.4f}" for v in val) + f"   [{cnt}]")
    tri_cube = comps[comp_of[c0]]
    check(abs(pdeath(tri_cube, 0.5) - (0.5 ** 6) * (1 - 2 * 0.125 + 1 / 32) ** 6) < 1e-12, "the triangle of one cube at rho = 1/2: 0.003553 (as in `tri`)")
    print("   measured on hull faces (board L1.1): P(death | n = 1, 2, 3) = 0.37-0.41, 0.10, 0.019")


def strip_tables(rho, a=3):
    """geometry of a strip a top cubes wide (periodic), read off the slab face a x 5: for the cubes (i, 2) of the
    middle column, the key of the per-cube table as KA[i][prev column] + KB[i][own column] + KC[i][next column]
    (column configurations are 3a-bit numbers, bit 3 i + axis)."""
    cells, nb, face, inl, ben, comps = face_data(a, 5)

    def cube_of(i):
        x, y, s = cells[i]; p = [x, y, s - x - y]; ax = g3.axis(tuple(p)); p[ax] -= 1
        return (p[0] // 2 % a, p[1] // 2 % 5, ax)
    lab = {i: cube_of(i) for i in face}
    by = {v: i for i, v in lab.items()}
    ncol = 1 << (3 * a)
    cfg = np.arange(ncol)
    bit = lambda ii, ax: (cfg >> (3 * ii + ax)) & 1
    KA, KB, KC, tabs = [], [], [], []
    for ii in range(a):
        cp = [by[(ii, 2, ax)] for ax in range(3)]
        assert sorted(cp) == sorted([c for c in comps if cp[0] in c][0])
        tabs.append(unit_table(cp, ben, rho))
        ka = np.zeros(ncol, np.int64); kb = np.zeros(ncol, np.int64); kc = np.zeros(ncol, np.int64)
        for pos, i in enumerate(cp):
            mul = 14 ** (2 - pos)
            kb += mul * 7 * bit(ii, lab[i][2])
            for j in inl[i]:
                (i2, j2, ax2) = lab[j]
                assert j2 in (1, 2, 3)
                if j2 == 1: ka += mul * bit(i2, ax2)
                elif j2 == 2: kb += mul * bit(i2, ax2)
                else: kc += mul * bit(i2, ax2)
        KA.append(ka); KB.append(kb); KC.append(kc)
    return KA, KB, KC, tabs


def strip_kernel(p, rho, a=3):
    """K[c, prev, next] = weight of the middle column c given its two neighbours: P(soup puts c) * prod of the per-cube
    probabilities that the column is dead next."""
    KA, KB, KC, tabs = strip_tables(rho, a)
    ncol = 1 << (3 * a)
    pop = np.zeros(ncol, np.int64)
    for b in range(3 * a):
        pop += (np.arange(ncol) >> b) & 1
    wsoup = p ** pop * (1 - p) ** (3 * a - pop)
    K = np.empty((ncol, ncol, ncol), np.float64)
    for c in range(ncol):
        w = np.full((ncol, ncol), wsoup[c])
        for ii in range(a):
            w *= tabs[ii][KA[ii][:, None] + KB[ii][c] + KC[ii][None, :]]
        K[c] = w
    return K


def torus_sum(a, b, p, rho, chunk_bits=22):
    """sum over every configuration of the a x b periodic face of P(soup) * prod over cubes of the per-cube weight."""
    cells, nb, face, inl, ben, comps = face_data(a, b)
    A = len(face)
    pos = {i: t for t, i in enumerate(face)}
    tabs = [unit_table(cp, ben, rho) for cp in comps]
    tot = 0.0; nposs = 0; dens_num = 0.0
    for lo in range(0, 1 << A, 1 << chunk_bits):
        S = np.arange(lo, min(lo + (1 << chunk_bits), 1 << A), dtype=np.int64)
        bits = [((S >> t) & 1) for t in range(A)]
        popc = np.zeros(len(S), np.int64)
        for t in range(A): popc += bits[t]
        w = p ** popc * (1 - p) ** (A - popc)
        for cp, tab in zip(comps, tabs):
            key = np.zeros(len(S), np.int64)
            for i in cp:
                k = np.zeros(len(S), np.int64)
                for j in inl[i]: k += bits[pos[j]]
                key = key * 14 + 7 * bits[pos[i]] + k
            w = w * tab[key]
        tot += float(w.sum()); nposs += int((w > 0).sum()); dens_num += float((w * popc).sum())
    return tot, nposs, dens_num / (tot * A)


def gump1():
    print("request 4: gump, one generation from a soup of density p (face and cells beneath): P(face empty next) = sum_S P(S) prod_cubes W_q(S)")
    # (i) the per-cube weights against the true rule on small slabs, every state
    for (a, b, m) in ((1, 1, 3), (2, 1, 3), (2, 1, 4)):
        cells, nb, face, inl, ben, comps = face_data(a, b, m)
        N = len(cells)
        F = exact.full_map(nb, g3.B, g3.S)
        fmask = sum(1 << i for i in face)
        cnt = int(((F & np.uint32(fmask)) == 0).sum())
        A = len(face)
        tot = 0.0
        for mask in range(1 << A):
            tot += face_death_prob(face, inl, ben, comps, {i: (mask >> t) & 1 for t, i in enumerate(face)}, 0.5)
        tot /= 1 << A
        check(abs(tot - cnt / 2 ** N) < 1e-13, f"slab {a} x {b} x {m} ({N} cells, doubled neighbours), true rule on every state: face empty next in {cnt} of 2^{N} "
                                              f"= {cnt / 2 ** N:.8f}; per-cube weights give {tot:.8f}")
    # (ii) the strip matrix against the whole 3 x 3 torus
    res = {}
    for p in (0.5, 0.4155):
        t0 = time.time()
        K = strip_kernel(p, p)
        ncol = K.shape[0]
        tr3 = 0.0
        for c0 in range(ncol):
            # sum over c1, c2 of K[c0][c2, c1] K[c1][c0, c2] K[c2][c1, c0]
            tr3 += float(np.einsum('ba,ab,ba->', K[c0], K[:, c0, :], K[:, :, c0]))
        tsum, nposs, dens = torus_sum(3, 3, p, p)
        check(abs(tr3 - tsum) < 1e-10 * tsum, f"p = {p}: whole 3 x 3 periodic face (27 cells, no doubled neighbours), every configuration: P(empty next) = {tsum:.6e}; "
                                             f"tr(M^3) of the strip matrix = {tr3:.6e}")
        # Perron eigenvalue: v[prev, c] -> u[c, next] = sum_prev v[prev, c] K[c, prev, next]
        v = np.full((ncol, ncol), 1.0 / ncol ** 2); lam = 0.0
        for it in range(5000):
            u = np.einsum('pc,cpn->cn', v, K)
            l2 = u.sum(); u /= l2
            if it > 20 and abs(l2 - lam) < 1e-13 * l2:
                lam = l2; break
            v, lam = u, l2
        # density of the face in the dying ensemble of the strip: right vector too
        r = np.full((ncol, ncol), 1.0)
        for it2 in range(it + 50):
            r2 = np.einsum('cpn,cn->pc', K, r); r2 /= r2.sum(); r = r2
        popc = np.zeros(ncol, np.int64)
        for b in range(9): popc += (np.arange(ncol) >> b) & 1
        mu = np.einsum('pc,cpn,cn->c', v, K, r); mu /= mu.sum()
        dstrip = float((mu * popc).sum()) / 9
        res[p] = (-np.log(lam) / 9, -np.log(tsum) / 27, nposs, dens, dstrip)
        print(f"   p = {p}: strip three cubes wide: Perron eigenvalue {lam:.6e} per column of 9 cells ({it} iterations): c_1 = {-np.log(lam) / 9:.5f} per face cell; "
              f"density of the face in the dying ensemble {dstrip:.4f}", flush=True)
        print(f"            whole 3 x 3 face: -ln P / 27 = {-np.log(tsum) / 27:.5f}; configurations that can be emptied: {nposs} of 2^27; density in the dying ensemble {dens:.4f}"
              f"   [{time.time() - t0:.0f} s]", flush=True)
        del K
    print(f"   for comparison: counting's hand estimate 0.54; the measured steady exponent 0.21-0.22 per face cell; ln 2 = 0.6931; "
          f"ratio c_1 / 0.21 = {res[0.5][0] / 0.21:.2f} (2D rule: 0.5515 / 0.36..0.42 = 1.3..1.5)")


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'lemma7': lemma7()
    elif what == 'lemma6': lemma6()
    elif what == 'ckcheck': ckcheck()
    elif what == 'ck': ck(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    elif what == 'profile': profile()
    elif what == 'steady': steady(int(sys.argv[2]) if len(sys.argv) > 2 else 19)
    elif what == 'ages': ages(int(sys.argv[2]) if len(sys.argv) > 2 else 18)
    elif what == 'ringint': ringint()
    elif what == 'gap2': gap2()
    elif what == 'tilt': tilt()
    elif what == 'tri': tri()
    elif what == 'small': small()
    elif what == 'gump1': gump1()
    print('ALL OK' if OK else 'SOMETHING FAILED')
