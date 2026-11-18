#!/usr/bin/env python3
"""blast/ref-proofs: referee's own dense code for the one-layer dice surrogate S(G).

Written from docs/AUTOMATON.md (12 offsets, rule B45/S345) and the definition of S in the referee's brief only.
Geometry: the {111} layer x+y+z = 1 in doubled coordinates.  In-layer neighbours = the offsets with zero sum (6);
coins = the offsets with sum -2 (two, density rho1) and -4 (one, density rho2).
Naming conventions (needed to address the same shapes as rigour's table) are rigour's:
  torus H K D : period lattice <H*E1 + K*E2, D*E2>, E1 = (2,-2,0), E2 = (2,0,-2)
  hull R      : x,y,z >= 0, x+y+z = R; a coin exists only if the cell beneath has |x|+|y|+|z| <= R
  strip W D / patch W D : unit cells (a,b) = {X at (1,0,0), Y at (0,1,0), Z at (0,0,1)} + a*E1 + b*E2,
                0 <= a < W, b mod D (strip) or 0 <= b < D (patch); three coins everywhere

usage: ref.py <kind> <args...> [--rho 0.44 0.42] [--eig] [--tilt] [--bust] [--mc N] [--lemma0]
"""
import sys, itertools, math
import numpy as np

# ---------------------------------------------------------------- geometry
def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; out.append(tuple(v))
    assert len(set(out)) == 12
    return out

OFF = [offsets(a) for a in range(3)]
for a in range(3):   # T1: layer histogram 1,2,6,2,1
    hist = {}
    for o in OFF[a]:
        hist[sum(o)] = hist.get(sum(o), 0) + 1
    assert hist == {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1}, hist
BASE = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

def ori(p):
    par = [c % 2 for c in p]
    assert sum(par) == 1
    return par.index(1)

def to_oab(p):
    o = ori(p); bs = BASE[o]
    a = -(p[1] - bs[1]) // 2; b = -(p[2] - bs[2]) // 2
    assert (bs[0] + 2 * a + 2 * b, bs[1] - 2 * a, bs[2] - 2 * b) == tuple(p)
    return o, a, b

def from_oab(o, a, b):
    bs = BASE[o]
    return (bs[0] + 2 * a + 2 * b, bs[1] - 2 * a, bs[2] - 2 * b)

def add(p, q):
    return tuple(p[i] + q[i] for i in range(3))

def g_torus(H, K, D):
    def red(o, a, b):
        q, a2 = divmod(a, H)
        return (o, a2, (b - q * K) % D)
    cells = [(o, a, b) for a in range(H) for b in range(D) for o in range(3)]
    ix = {c: i for i, c in enumerate(cells)}
    nb = []
    for (o, a, b) in cells:
        p = from_oab(o, a, b)
        nb.append([ix[red(*to_oab(add(p, off)))] for off in OFF[o] if sum(off) == 0])
    return nb, [(2, 1)] * len(cells)

def g_hull(R):
    cells = [(x, y, R - x - y) for x in range(R + 1) for y in range(R + 1 - x)
             if (x % 2) + (y % 2) + ((R - x - y) % 2) == 1]
    ix = {c: i for i, c in enumerate(cells)}
    nb, m = [], []
    for p in cells:
        o = ori(p); l = []; m1 = m2 = 0
        for off in OFF[o]:
            q = add(p, off); s = sum(off)
            if s == 0 and q in ix: l.append(ix[q])
            if s == -2 and sum(abs(c) for c in q) <= R: m1 += 1
            if s == -4 and sum(abs(c) for c in q) <= R: m2 += 1
        nb.append(l); m.append((m1, m2))
    return nb, m

def g_strip(W, D, periodic=True):
    cells = [(o, a, b) for a in range(W) for b in range(D) for o in range(3)]
    ix = {c: i for i, c in enumerate(cells)}
    nb = []
    for (o, a, b) in cells:
        p = from_oab(o, a, b); l = []
        for off in OFF[o]:
            if sum(off) == 0:
                o2, a2, b2 = to_oab(add(p, off))
                if periodic: b2 %= D
                if (o2, a2, b2) in ix: l.append(ix[(o2, a2, b2)])
        nb.append(l)
    return nb, [(2, 1)] * len(cells)

def build(kind, args):
    if kind == 'torus': return g_torus(*args)
    if kind == 'hull': return g_hull(*args)
    if kind == 'strip': return g_strip(*args)
    if kind == 'patch': return g_strip(*args, periodic=False)
    raise SystemExit(__doc__)

# ---------------------------------------------------------------- the chain
def coin_law(m1, m2, r1, r2):
    """law of b = Bin(m1, r1) + Bin(m2, r2), by enumerating the coins"""
    pb = np.zeros(m1 + m2 + 1)
    for coins in itertools.product((0, 1), repeat=m1 + m2):
        w = 1.0
        for j, c in enumerate(coins):
            r = r1 if j < m1 else r2
            w *= r if c else 1 - r
        pb[sum(coins)] += w
    return pb

def p_alive(x, k, m1, m2, r1, r2):
    pb = coin_law(m1, m2, r1, r2)
    tot = 0.0
    for b, w in enumerate(pb):
        n = k + b
        if (x == 0 and n in (4, 5)) or (x == 1 and n in (3, 4, 5)):
            tot += w
    return tot

def kernel(nb, m, r1, r2):
    A = len(nb); N = 1 << A
    idx = np.arange(N)
    bits = ((idx[:, None] >> np.arange(A)[None, :]) & 1).astype(np.int64)      # bits[x, i]
    al = np.zeros((N, A))
    for i in range(A):
        k = np.zeros(N, dtype=np.int64)
        for j in nb[i]: k += bits[:, j]
        tab = np.array([[p_alive(x, kk, m[i][0], m[i][1], r1, r2) for kk in range(7)] for x in (0, 1)])
        al[:, i] = tab[bits[:, i], k]
    P = np.ones((N, 1))
    for i in range(A):                      # new cell i becomes bit i of the column index
        P = np.concatenate([P * (1 - al[:, i])[:, None], P * al[:, i][:, None]], axis=1)
    return P, al, bits

def qsd(P, tol=1e-15, maxit=20000):
    N = P.shape[0]
    Q = P[1:, 1:]
    v = np.full(N - 1, 1.0 / (N - 1))
    lam = 0
    for it in range(maxit):
        w = v @ Q
        l2 = w.sum(); w /= l2
        if abs(l2 - lam) < tol and np.abs(w - v).max() < tol: 
            v = w; lam = l2; break
        v = w; lam = l2
    mu = np.zeros(N); mu[1:] = v
    return lam, mu, it

def main():
    av = sys.argv[1:]
    r1, r2 = 0.44, 0.42
    if '--rho' in av:
        j = av.index('--rho'); r1, r2 = float(av[j + 1]), float(av[j + 2]); del av[j:j + 3]
    flags = [a for a in av if a.startswith('--')]
    mcN = 0
    if '--mc' in av:
        j = av.index('--mc'); mcN = int(float(av[j + 1])); del av[j:j + 2]
    pos = [a for a in av if not a.startswith('--')]
    kind = pos[0]; args = [int(x) for x in pos[1:]]
    nb, m = build(kind, args)
    A = len(nb); N = 1 << A
    name = kind + '_' + '_'.join(map(str, args))
    P, al, bits = kernel(nb, m, r1, r2)
    assert np.allclose(P.sum(1), 1, atol=1e-12)
    assert P[0, 0] == 1.0
    pop = bits.sum(1)
    lam, mu, it = qsd(P)
    d = P[:, 0].copy()
    h = float(mu @ d)
    print('== %s A %d rho %.2f %.2f  power iterations %d' % (name, A, r1, r2, it))
    print('h %.13e  1-lambda %.13e  lntau %.12f' % (h, 1 - lam, -math.log(h)))
    dens = float(mu @ pop) / A
    flux = mu * d / h
    print('density %.12f  death_from_1,2,3 %.6e %.6e %.6e' % (dens, flux[pop == 1].sum(), flux[pop == 2].sum(), flux[pop == 3].sum()))
    print('p1..p4 %.6e %.6e %.6e %.6e' % tuple(mu[pop == n].sum() for n in (1, 2, 3, 4)))
    if '--eig' in flags:
        ev = np.linalg.eigvals(P[1:, 1:])
        ev = ev[np.argsort(-np.abs(ev))]
        print('numpy eigvals: lambda1 %.15f  h_eig %.13e  lntau_eig %.12f  |lambda2/lambda1| %.4f' %
              (ev[0].real, 1 - ev[0].real, -math.log(1 - ev[0].real), abs(ev[1]) / abs(ev[0])))
    if '--tilt' in flags:
        # eps_i(x) = -ln P(cell i dead next | x)
        dead = 1 - al
        print('min over (cell,state) of P(dead next) %.6f -> eps_max on this graph %.6f ; (K) holds: %s' %
              (dead.min(), -math.log(dead.min()), dead.min() > 0))
        eps = -np.log(dead)
        E = eps.sum(1)
        assert np.allclose(np.exp(-E), d, rtol=1e-10)
        xs, ws = np.polynomial.legendre.leggauss(48)
        xs = (xs + 1) / 2; ws = ws / 2
        tot = 0; ci = np.zeros(A); path = []
        for s, w in zip(xs, ws):
            ms = mu * np.exp(-s * E); ms /= ms.sum()
            ci += w * (ms @ eps); tot += w * float(ms @ E)
        E0 = float(mu @ E); m1 = mu * np.exp(-E); m1 /= m1.sum(); E1 = float(m1 @ E)
        print('tilt: integral_0^1 <E>_s ds = %.12f   ln tau = %.12f   diff %.2e' % (tot, -math.log(h), tot + math.log(h)))
        print('<E>_1 = %.6f <= ln tau = %.6f <= <E>_0 = %.6f <= 2.509*A = %.3f' % (E1, -math.log(h), E0, 2.5094 * A))
        print('c_i (tilt path):', ' '.join('%.4f' % c for c in ci))
        # a second, equally exact, "sum of local costs": the chain rule in cell order (and in reverse order)
        for order, lab in ((range(A), 'order 0..A-1'), (range(A - 1, -1, -1), 'reverse order')):
            w = mu.copy(); prev = 1.0; cc = np.zeros(A)
            for i in order:
                w = w * dead[:, i]; cur = w.sum(); cc[i] = -math.log(cur / prev); prev = cur
            print('c_i (chain rule, %s): %s  sum %.12f' % (lab, ' '.join('%.4f' % c for c in cc), cc.sum()))
        # population law along the tilt (is mu_s ever a mixture of two kinds of face?)
        for s in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0):
            ms = mu * np.exp(-s * E); ms /= ms.sum()
            pl = np.array([ms[pop == n].sum() for n in range(A + 1)])
            Es = float(ms @ E); Vs = float(ms @ (E - Es) ** 2)
            print('  s %.1f <E>/A %.4f Var(E)/A %.4f density %.4f  P(pop=n): %s' % (s, Es / A, Vs / A, float(ms @ pop) / A, ' '.join('%.3f' % x for x in pl)))
    if '--bust' in flags:
        half = (A + 1) // 2
        # exact law of the last K transitions before death under the quasi-stationary start:
        # P_mu(T = K, no transition among the K falls by >= half) / P_mu(T = K)
        fall = pop[:, None] - pop[None, :]
        Pn = np.where(fall < half, P, 0.0)
        Qn = Pn[1:, 1:]; dn = Pn[1:, 0]
        v = mu[1:].copy(); out = []
        for K in range(1, 11):
            nodeath = float(v @ dn)                      # T = K, unmarked
            out.append((K, 1 - nodeath / (lam ** (K - 1) * h)))
            v = v @ Qn
        print('halffall_share (fall >= %d): ' % half + '  '.join('K=%d: %.6f' % o for o in out))
        # the marked share, split by where the fall happens (the death step itself, or earlier)
        print('  share with the DEATH step itself a half-fall (pop(T-1) >= %d): %.6f' % (half, (mu * d)[pop >= half].sum() / h))
    if mcN:
        rng = np.random.default_rng(12345)
        half = (A + 1) // 2
        tabs = [np.array([[p_alive(x, kk, m[i][0], m[i][1], r1, r2) for kk in range(7)] for x in (0, 1)]) for i in range(A)]
        R = 200000
        X = (rng.random((R, A)) < 0.5).astype(np.int8)
        age = np.zeros(R, dtype=np.int64)
        since = np.full(R, 10 ** 6, dtype=np.int64)       # transitions since the last half-fall
        deaths = marked = 0; burn = 40; steps = 0; expo = 0
        nbarr = [np.array(l, dtype=np.int64) for l in nb]
        while deaths < mcN:
            k = np.stack([X[:, nbarr[i]].sum(1) for i in range(A)], axis=1)
            pa = np.stack([tabs[i][X[:, i], k[:, i]] for i in range(A)], axis=1)
            Y = (rng.random((R, A)) < pa).astype(np.int8)
            fl = X.sum(1) - Y.sum(1) >= half
            since = np.where(fl, 0, since + 1); age += 1
            dead_now = Y.sum(1) == 0
            ok = dead_now & (age >= burn)
            deaths += int(ok.sum()); marked += int((ok & (since <= 5)).sum())
            expo += int((age >= burn).sum())
            nd = int(dead_now.sum())
            Y[dead_now] = (rng.random((nd, A)) < 0.5).astype(np.int8)
            age[dead_now] = 0; since[dead_now] = 10 ** 6
            X = Y
        p = marked / deaths
        print('MC (independent simulation, deaths after %d generations from a fair start): deaths %d  halffall6 share %.4f +- %.4f  lntau %.4f +- %.4f' %
              (burn, deaths, p, math.sqrt(p * (1 - p) / deaths), math.log(expo / deaths), 1 / math.sqrt(deaths)))
    if '--lemma0' in flags:
        S = (P[1:, 1:] > 0)
        Sf = S.astype(np.float32)
        def closure(start, M):
            seen = np.zeros(N - 1, dtype=bool); seen[start] = True; fr = seen.copy()
            while fr.any():
                nxt = (fr.astype(np.float32) @ M) > 0
                fr = nxt & ~seen; seen |= fr
            return seen
        # u = all cells of orientation X alive (cells are listed X, Y, Z per unit cell: index % 3 == 0)
        u = sum(1 << i for i in range(0, A, 3)) - 1
        fwd = closure(u, Sf); bwd = closure(u, Sf.T.copy())
        cls = fwd & bwd
        outside = ~cls
        surely = bool(np.all(P[1:, 0][outside] == 1.0)) if outside.any() else True
        print('lemma0: non-empty states %d; class of u (all X alive): %d; states outside: %d; all of those go to empty surely: %s; '
              'all reachable from u: %s; u -> u possible (aperiodic): %s; M(u) = V (every state a successor of u): %s' %
              (N - 1, int(cls.sum()), int(outside.sum()), surely, bool(fwd.all()), bool(S[u, u]), bool(S[u].all() and P[u + 1, 0] > 0)))

if __name__ == '__main__':
    main()
