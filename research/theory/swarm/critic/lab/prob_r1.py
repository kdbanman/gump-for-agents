"""Critic's lab: checks and lab requests for probability, round 1 (exact; no sampling).

MODEL E1(pi) = D2 with a general law pi = (pi0, pi1, pi2) of b (live cells beneath an edge cell): a row of cells
follows B34/S234 with k = live cells among the four in-row neighbours; next state 1 iff k + b <= 4 and
k + b + x >= 3. Rows: 'ring' (Z_L), 'dead' (an interval with dead cells outside), 'refl' (an interval with
reflecting ends, x_{1-i} := x_i, x_{M+i} := x_{M+1-i}: the mirror-symmetric ring of 2M cells).

  python3 prob_r1.py tables        R1: the table a(x, k) and the minorant table, by enumeration; Lemma 2's numbers
  python3 prob_r1.py ring [Lmax]   R2: ln tau_L on the ring for the three laws, L = 5..Lmax (default 18)
  python3 prob_r1.py ends [Mmax]   R3: ln tau_M on an interval with dead and with reflecting ends, pi = Bin(2, 0.472)
  python3 prob_r1.py check         the fast kernel against dice_w1.py (orbit-reduced dense kernel) and path_r1.py seg

The kernel is applied without being stored: (Qf)(S) = sum_{S'} prod_y P(S'_y | S) f(S') is contracted one cell at a
time (probability's cost note), by einsum on arrays with at most M + 5 binary axes.
"""
import sys, os, itertools, string
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LAWS = {'(1/2, 0, 1/2)': (0.5, 0.0, 0.5), 'Bin(2, 1/2)': (0.25, 0.5, 0.25), 'Bin(2, 0.472)': (0.278784, 0.498432, 0.222784)}
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def a_table(pi):
    """a[x][k] = P(alive next | own state x, k live in-row neighbours), from the rule as birth/survival sets."""
    B, S = (3, 4), (2, 3, 4)
    return np.array([[sum(pi[b] for b in range(3) if (k + b) in (S if x else B)) for k in range(7)] for x in (0, 1)])


def neighbours(M, kind):
    """for each cell y: list of (cell index) of its four in-row neighbours, with multiplicity; dead ones omitted."""
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
        out.append(v)
    return out


def make_apply(M, kind, pi):
    a = a_table(pi)
    nbs = neighbours(M, kind)
    letters = string.ascii_letters
    Sl = lambda i: letters[i]                 # axis label of S_i
    Pl = lambda i: letters[26 + i]            # axis label of S'_i
    factors = []
    for y in range(M):
        cells = sorted(set(nbs[y]) | {y})
        W = np.zeros((2,) + (2,) * len(cells))
        for bits in itertools.product((0, 1), repeat=len(cells)):
            val = dict(zip(cells, bits))
            k = sum(val[z] for z in nbs[y])          # with multiplicity (reflecting ends, short rings)
            p = a[val[y], k]
            W[(1,) + bits] = p; W[(0,) + bits] = 1 - p
        factors.append((cells, W))

    def apply(f):
        A = f.reshape((2,) * M)
        axes = [Pl(i) for i in range(M)]
        for y in range(M):
            cells, W = factors[y]
            wl = Pl(y) + ''.join(Sl(z) for z in cells)
            out = [ax for ax in axes if ax != Pl(y)]
            for z in cells:
                if Sl(z) not in out:
                    out.append(Sl(z))
            A = np.einsum(''.join(axes) + ',' + wl + '->' + ''.join(out), A, W)
            axes = out
        # reorder to S_0 .. S_{M-1}
        A = np.einsum(''.join(axes) + '->' + ''.join(Sl(i) for i in range(M)), A)
        return A.reshape(-1)
    return apply


def lntau(M, kind, pi, iters=400, tol=1e-13):
    """-ln(1 - lambda), lambda the Perron eigenvalue of the kernel on non-empty rows. State index: S_0 is the highest bit."""
    ap = make_apply(M, kind, pi)
    f = np.ones(1 << M); f[0] = 0.0
    lam = 0.0
    for it in range(iters):
        g = ap(f); g[0] = 0.0
        l2 = g.max(); g /= l2
        if abs(l2 - lam) < tol and it > 10:
            lam = l2; break
        f, lam = g, l2
    # refine with a Rayleigh-type quotient
    g = ap(f); g[0] = 0.0
    lam = float(g.sum() / f.sum())
    return -np.log(1 - lam), lam


def tables():
    print("R1. the table a(x, k) from the rule B34/S234, n = k + b")
    for name, pi in LAWS.items():
        a = a_table(pi)
        p0, p1, p2 = pi
        want_live = [p2, p1 + p2, 1.0, p0 + p1, p0]; want_dead = [0.0, p2, p1 + p2, p0 + p1, p0]
        check(np.allclose(a[1][:5], want_live) and np.allclose(a[0][:5], want_dead),
              f"{name}: live {np.round(a[1][:5], 4).tolist()}, dead {np.round(a[0][:5], 4).tolist()} = (pi2, pi1+pi2, 1, pi0+pi1, pi0) / (0, pi2, pi1+pi2, pi0+pi1, pi0)")
    print("    the minorant q(y; eta) = min over rows S' containing eta, by enumeration of the four neighbours and of y")
    rng = np.random.default_rng(1)
    allok = True
    laws = list(LAWS.values()) + [tuple(v / v.sum()) for v in rng.random((200, 3))]
    for pi in laws:
        a = a_table(pi); p0, p1, p2 = pi
        s = min(p0, p2); m = min(p0, 1 - p0)
        want = {(1, 0): s, (1, 1): m, (1, 2): p0, (1, 3): p0, (1, 4): p0, (0, 0): 0.0, (0, 1): s, (0, 2): m, (0, 3): p0, (0, 4): p0}
        for in_eta in (0, 1):
            for j in range(5):
                q = min(a[x][k] for x in ((1,) if in_eta else (0, 1)) for k in range(j, 5))
                allok &= abs(q - want[(in_eta, j)]) < 1e-12
    check(allok, f"minorant table (y in eta: s, m, pi0, pi0, pi0; y not in eta: 0, s, m, pi0, pi0) for the three laws and 200 random laws")
    # Lemma 2(b): kappa from the formula, and the exact worst ratio E Phi(eta') / Phi(eta) of the minorant on a ring
    for rho in (0.46, 0.472, 0.5):
        pi = ((1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2)
        p0, p1, p2 = pi; s = min(p0, p2); m = min(p0, 1 - p0); pbar = max(s, m, p0)
        g = [1 - (1 - s) * (1 - pbar) ** (i - 1) for i in (1, 2, 3, 4)]; c5 = 1 - (1 - pbar) ** 5
        kappa = (2 * sum(g) + c5) / 5
        L = 14
        worst = 0.0; arg = None
        qtab = {(1, 0): s, (1, 1): m, (0, 0): 0.0, (0, 1): s, (0, 2): m}
        for eta in range(1, 1 << L):
            bits = [(eta >> i) & 1 for i in range(L)]
            q = []
            for y in range(L):
                j = bits[(y - 2) % L] + bits[(y - 1) % L] + bits[(y + 1) % L] + bits[(y + 2) % L]
                q.append(qtab.get((bits[y], j), p0))
            N = [any(bits[(z + d) % L] for d in (-2, -1, 0, 1, 2)) for z in range(L)]
            phi = sum(N)
            e = 0.0
            for z in range(L):
                pr = 1.0
                for d in (-2, -1, 0, 1, 2):
                    pr *= 1 - q[(z + d) % L]
                e += 1 - pr
            if e / phi > worst:
                worst = e / phi; arg = eta
        one = 9 - (1 - s) ** 5 - 2 * sum((1 - s) ** i for i in (1, 2, 3, 4))
        check(worst <= kappa + 1e-12 and kappa < 1,
              f"rho = {rho}: kappa (formula) = {kappa:.4f}; exact sup over all eta on a ring of {L} of E Phi(eta')/Phi(eta) = {worst:.4f} "
              f"(at eta = {format(arg, '0%db' % L)}); single cell: E Phi' = {one:.3f} of 5")


def ring(Lmax=18):
    print("R2. ln tau_L = -ln(1 - lambda_L) on the ring Z_L")
    for name, pi in LAWS.items():
        print(f"  pi = {name}")
        prev = None; rows = []
        for L in range(5, Lmax + 1):
            lt, lam = lntau(L, 'ring', pi)
            rows.append((L, lt, None if prev is None else lt - prev)); prev = lt
            print(f"    L = {L:2d}: ln tau = {lt:9.5f}" + ('' if rows[-1][2] is None else f"   step {rows[-1][2]:.4f}"), flush=True)


def ends(Mmax=18):
    pi = LAWS['Bin(2, 0.472)']
    print("R3. pi = Bin(2, 0.472): interval of M cells with dead cells outside, and with reflecting ends; ring for comparison")
    print("     M   ln tau dead   step    ln tau refl   step    ln tau ring(M)  step    ring(2M) - refl(M)")
    pd = pr = pg = None
    for M in range(5, Mmax + 1):
        d, _ = lntau(M, 'dead', pi); r, _ = lntau(M, 'refl', pi); g, _ = lntau(M, 'ring', pi)
        g2 = lntau(2 * M, 'ring', pi)[0] if 2 * M <= 18 else None
        st = lambda v, p: '       ' if p is None else f"{v - p:7.4f}"
        print(f"    {M:2d}   {d:9.5f}  {st(d, pd)}   {r:9.5f}  {st(r, pr)}   {g:9.5f}     {st(g, pg)}" +
              ('' if g2 is None else f"    {g2 - r:+.4f}"), flush=True)
        pd, pr, pg = d, r, g


def check_fast():
    import dice_w1 as dw
    import path_r1 as pr
    okk = True
    for L in (6, 9, 12):
        a = lntau(L, 'ring', LAWS['Bin(2, 0.472)'])[0]; b = dw.analyse(L, 0.472)['lntau']
        okk &= abs(a - b) < 1e-8
        print(f"  ring L = {L}: fast kernel {a:.8f}, orbit-reduced dense kernel {b:.8f}")
    for M in (6, 10):
        reps, Mx = pr.seg_kernel(M, 0.472)
        lam, mu, v = dw.perron(Mx[1:, 1:])
        a = lntau(M, 'dead', LAWS['Bin(2, 0.472)'])[0]
        okk &= abs(a + np.log(1 - lam)) < 1e-8
        print(f"  dead ends M = {M}: fast kernel {a:.8f}, dense kernel {-np.log(1 - lam):.8f}")
    # reflecting interval of M cells against the mirror-symmetric states of the ring of 2M cells (dense, tiny)
    M = 5; pi = LAWS['Bin(2, 0.472)']; a = a_table(pi)
    L = 2 * M
    sym = []
    for S in range(1 << M):
        bits = [(S >> i) & 1 for i in range(M)]
        full = bits[::-1] + bits                       # cells -M..-1 mirror cells 0..M-1 (mirror between -1 and 0)
        sym.append(full)
    Q = np.zeros((1 << M, 1 << M))
    for i, full in enumerate(sym):
        p = []
        for y in range(M, 2 * M):                      # the right half; its image gets the same die
            k = sum(full[(y + d) % L] for d in (-2, -1, 1, 2))
            p.append(a[full[y], k])
        for T in range(1 << M):
            w = 1.0
            for t in range(M):
                w *= p[t] if (T >> t) & 1 else 1 - p[t]
            Q[i, T] = w
    lam = max(np.linalg.eigvals(Q[1:, 1:]).real)
    b = lntau(M, 'refl', pi)[0]
    okk &= abs(b + np.log(1 - lam)) < 1e-8
    print(f"  reflecting ends M = {M}: fast kernel {b:.8f}; mirror-symmetric ring of {L} with shared dice, dense: {-np.log(1 - lam):.8f}")
    check(okk, "fast kernel agrees with the dense kernels")


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'tables': tables()
    elif what == 'ring': ring(int(sys.argv[2]) if len(sys.argv) > 2 else 18)
    elif what == 'ends': ends(int(sys.argv[2]) if len(sys.argv) > 2 else 18)
    elif what == 'check': check_fast()
    print('ALL OK' if OK else 'SOMETHING FAILED')
