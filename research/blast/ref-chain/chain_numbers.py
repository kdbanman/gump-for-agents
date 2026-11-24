#!/usr/bin/env python3
"""ref-chain: the chain theorems' numbers on small wrapped faces of the surrogate, from my own code.

  OMP_NUM_THREADS=1 python3 research/blast/ref-chain/chain_numbers.py [H K D ...]     (about 1 min for the default list)

Geometry: kagome_check.py (cells of the layer x+y+z = 1 mod the period lattice, in-layer neighbours from
reference/oracle.py's offsets).  Kernel: every cell has two coins of density rho1 = 0.44 and one of rho2 = 0.42
(the oracle's layer histogram: 2 cells in the layer beneath, 1 two beneath); a cell is alive next iff
rule(x_i, k_i + b_i), rule = the oracle's BIRTH/SURVIVE.  Dense 2^A x 2^A product kernel, Q its block on the
non-empty states.  The QSD is the dominant left eigenvector (power iteration); tau = 1/h, h = sum mu d.

Printed per face, each line a claim of the Lean files tested numerically:
  ln tau (against rigour's exact.csv as reproduced by ref-proofs), the tilt identity (64-point Gauss-Legendre),
  monotonicity of <E>_s on 2001 points, <E>_1 <= ln tau <= <E>_0 = E_mu E <= eps_max A, prices per cell
  (one per orientation; one per cell iff rotation-invariant), Lemma 0's class structure (one class, the all-X
  state u reaches every living state in one step, Q u u > 0, the only other living state dies surely), the
  Riemann bracket, decay_bounds and lifetime_from_bounds, and the junk QSD (point mass on the all-alive state).
"""
import os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
from oracle import BIRTH, SURVIVE
from kagome_check import cells, oracle_nbrs, rotation_invariant

R1, R2 = 0.44, 0.42
EXACT = {(2, 0, 2): 3.981836588280, (1, 1, 4): 3.711833898815, (1, 0, 4): 4.133012406313,
         (1, 1, 3): 2.694626605944, (1, 0, 3): 3.393524719052}     # rigour exact.csv, ref-proofs A4


def coin_law(r1, r2):
    """Law of Bin(2, r1) + Bin(1, r2)."""
    p = np.zeros(4)
    for c1 in range(3):
        for c2 in range(2):
            p[c1 + c2] += [1, 2, 1][c1] * r1 ** c1 * (1 - r1) ** (2 - c1) * r2 ** c2 * (1 - r2) ** (1 - c2)
    return p


def alive_table(r1, r2):
    """a[s, k] = P(alive next | state s, k live in-layer neighbours), k = 0..6."""
    p = coin_law(r1, r2)
    a = np.zeros((2, 7))
    for s in (0, 1):
        for k in range(7):
            a[s, k] = sum(p[b] for b in range(4) if (k + b in (SURVIVE if s else BIRTH)))
    return a


def build(H, K, D, r1=R1, r2=R2):
    cs = cells(H, K, D)
    index = {c: i for i, c in enumerate(cs)}
    A = len(cs)
    N = np.zeros((A, A), int)                      # N[i, j] = multiplicity of j among i's in-layer neighbours
    for c in cs:
        for d in oracle_nbrs(c, H, K, D):
            N[index[c], index[d]] += 1
    n = 1 << A
    X = ((np.arange(n)[:, None] >> np.arange(A)[None, :]) & 1)          # X[x, i] = bit i of state x
    k = X @ N.T                                                         # k[x, i] = live neighbours of i
    a = alive_table(r1, r2)[X, k]                                       # a[x, i]
    P = np.ones((n, 1))
    for i in reversed(range(A)):                                        # index of y = sum y_i 2^i
        P = (P[:, :, None] * np.stack([1 - a[:, i], a[:, i]], axis=1)[:, None, :]).reshape(n, -1)
    return cs, N, X, a, P


def qsd(Q, tol=1e-15, maxit=20000):
    mu = np.full(Q.shape[0], 1.0 / Q.shape[0])
    for it in range(maxit):
        nu = mu @ Q
        lam = nu.sum()
        nu /= lam
        if np.abs(nu - mu).max() < tol:
            return nu, lam, it
        mu = nu
    raise RuntimeError("no convergence")


def tilt_stats(mu, E):
    """<E>_s and the log-partition function on a grid, stabilised."""
    def mean(s, f):
        w = mu * np.exp(-s * (E - E.min()))
        return (w * f).sum() / w.sum()
    return mean


def run(H, K, D, verbose=True):
    cs, N, X, a, P = build(H, K, D)
    A = len(cs); n = 1 << A
    assert np.allclose(P.sum(1), 1, atol=1e-12)
    Q = P[1:, 1:]                                   # living states 1..2^A-1 (state 0 = empty face)
    d = P[1:, 0]                                    # death probability = P(x, empty)
    dc = 1 - a[1:]                                  # local factors d_i(x)
    assert np.allclose(d, dc.prod(1), rtol=1e-12)
    eps = -np.log(dc); E = eps.sum(1)
    mu, lam, it = qsd(Q)
    h = mu @ d
    lntau = -np.log(h)
    out = {}
    out['lntau'] = lntau
    res = np.abs(mu @ Q - lam * mu).max()
    print(f"\n== torus ({H},{K}),(0,{D}): A = {A}, rho = ({R1}, {R2});  power iteration {it} steps, "
          f"|mu Q - lam mu| = {res:.1e}, lam = {lam:.15f}, 1 - lam - h = {1 - lam - h:.1e}")
    ex = EXACT.get((H, K, D))
    print(f"   ln tau = {lntau:.12f}" + (f"   (exact.csv {ex:.12f}, diff {lntau - ex:.1e})" if ex else ""))
    # --- tilt identity
    xg, wg = np.polynomial.legendre.leggauss(64); sg = (xg + 1) / 2; wg = wg / 2
    mean = tilt_stats(mu, E)
    integ = sum(w * mean(s, E) for s, w in zip(sg, wg))
    grid = np.linspace(0, 1, 2001)
    curve = np.array([mean(s, E) for s in grid])
    mono = np.diff(curve).max()
    E0, E1 = mean(0.0, E), mean(1.0, E)
    emax = -np.log(min(R1 ** 2 * R2, (1 - R1) ** 2 * (1 - R2)))
    print(f"   tilt identity: int_0^1 <E>_s ds - ln tau = {integ - lntau:.1e};  max increase of <E>_s on 2001 "
          f"points = {mono:.1e} (<= 0 means antitone)")
    print(f"   <E>_1 = {E1:.6f} <= ln tau = {lntau:.6f} <= <E>_0 = E_mu E = {E0:.6f} (= {E0 / A:.4f} per cell)"
          f" <= eps_max A = {emax * A:.4f};  max eps_i(x) = {eps.max():.6f}, eps_max = {emax:.6f}")
    # --- prices
    c = np.array([sum(w * mean(s, eps[:, i]) for s, w in zip(sg, wg)) for i in range(A)])
    byo = [c[[j for j, cc in enumerate(cs) if cc[0] == o]] for o in range(3)]
    spread = max(b.max() - b.min() for b in byo)
    co = [b.mean() for b in byo]
    print(f"   prices: sum c_i - ln tau = {c.sum() - lntau:.1e};  spread within an orientation = {spread:.1e};  "
          f"c_X, c_Y, c_Z = {co[0]:.10f}, {co[1]:.10f}, {co[2]:.10f};  ln tau / A = {lntau / A:.10f}; "
          f"rotation-invariant: {rotation_invariant(H, K, D)}")
    print(f"   |T| (c_X+c_Y+c_Z) - ln tau = {H * D * sum(co) - lntau:.1e};  all c_i in [0, eps_max]: "
          f"{bool((c >= 0).all() and (c <= emax).all())}")
    # --- Lemma 0: class structure
    S = Q > 0
    u = sum(1 << j for j, cc in enumerate(cs) if cc[0] == 0) - 1     # index in Q of the all-X state
    def reach(start, M):
        seen = np.zeros(M.shape[0], bool); seen[start] = True; front = seen.copy()
        while front.any():
            nxt = M[front].any(0) & ~seen
            seen |= nxt; front = nxt
        return seen
    fwd = reach(u, S); bwd = reach(u, S.T)
    cls = fwd & bwd
    canlive = S.any(1)
    others = np.nonzero(~canlive)[0]
    print(f"   Lemma 0: class of u = all-X has {cls.sum()} of {n - 1} living states; states that can survive = "
          f"{canlive.sum()}; class == can-survive: {bool((cls == canlive).all())};  Q u y > 0 for all y: "
          f"{bool(S[u].all())};  Q u u = {Q[u, u]:.3e};  surely-dying living states: "
          f"{[format(int(x) + 1, 'b') for x in others]}")
    # --- junk QSD: point mass on a surely-dying state
    for z in others:
        delta = np.zeros(n - 1); delta[z] = 1
        print(f"   junk QSD: point mass on state {int(z) + 1}: |delta Q - 0 delta| = {np.abs(delta @ Q).max():.1e}, "
              f"its tau = 1/d = {1 / d[z]:.3f}, ln tau = {np.log(1 / d[z]):.3f}")
    # --- QSD positivity / uniqueness
    print(f"   mu > 0 everywhere: {bool((mu > 0).all())}  (min {mu.min():.2e});  ")
    ev = None
    if n <= 512:
        ev = np.sort(np.abs(np.linalg.eigvals(Q)))[::-1]
        print(f"   |lam_2 / lam_1| = {ev[1] / ev[0]:.4f}")
    # --- Riemann bracket
    for m in (1, 2, 4, 8, 16):
        lo = np.mean([mean(j / m, E) for j in range(1, m + 1)])
        up = np.mean([mean(j / m, E) for j in range(0, m)])
        print(f"   Riemann n = {m:2d}: {lo:.6f} <= {lntau:.6f} <= {up:.6f}: {lo <= lntau <= up};  width {up - lo:.6f}"
              f" = (<E>_0-<E>_1)/n {(E0 - E1) / m:.6f} <= eps_max A/n {emax * A / m:.4f}")
    # --- decay bounds and lifetime from every start
    B = Q[np.ix_(cls, cls)]
    w = np.ones(B.shape[0])
    for _ in range(20000):
        w2 = B @ w; r = w2.max(); w2 /= r
        if np.abs(w2 - w).max() < 1e-15: break
        w = w2
    r = (B @ w)[0] / w[0]
    mlo, Mhi = w.min(), w.max()
    surv = np.ones(n - 1); ok = True; worst_lo = np.inf; worst_up = -np.inf
    for t in range(0, 400):
        lo = mlo / Mhi * r ** t
        worst_lo = min(worst_lo, (surv[cls] - lo).min())
        surv_next = Q @ surv
        up = Mhi / mlo * r ** t
        worst_up = max(worst_up, (surv_next - up).max())
        surv = surv_next
    print(f"   decay_bounds: Perron eigenvalue of the class block r = {r:.15f} (QSD lam - r = {lam - r:.1e}); "
          f"m/M = {mlo / Mhi:.4f};  min over t<400, x of P_x(T>t) - (m/M) r^t = {worst_lo:.2e} (>= 0);  "
          f"max of P_x(T>t+1) - (M/m) r^t = {worst_up:.2e} (<= 0)")
    ET = np.linalg.solve(np.eye(n - 1) - Q, np.ones(n - 1))
    lo_b = mlo / Mhi / (1 - r); up_b = 1 + Mhi / mlo / (1 - r)
    print(f"   lifetime_from_bounds: {lo_b:.3f} <= E_x T in [{ET[cls].min():.3f}, {ET[cls].max():.3f}] <= {up_b:.3f}: "
          f"{bool(lo_b <= ET[cls].min() and ET[cls].max() <= up_b)};  tau = 1/h = {1 / h:.3f}; "
          f"E_x T from the all-X state = {ET[u]:.3f}")
    out.update(dict(E0=E0, E1=E1, A=A, curve=curve, grid=grid, c=co, mean=mean, E=E, mu=mu))
    return out


def price_compare_check(F1, F2, n=4):
    """ChainTiltLimit.price_compare: |lnT/A - lnT'/A'| <= delta + w/n."""
    A1, A2 = F1['A'], F2['A']
    delta = max(abs(F1['mean'](k / n, F1['E']) / A1 - F2['mean'](k / n, F2['E']) / A2) for k in range(n + 1))
    w = max((F1['E0'] - F1['E1']) / A1, (F2['E0'] - F2['E1']) / A2)
    lhs = abs(F1['lntau'] / A1 - F2['lntau'] / A2)
    print(f"   price_compare n={n}: |ln tau/A - ln tau'/A'| = {lhs:.5f} <= delta + w/n = {delta:.5f} + {w:.5f}/{n} "
          f"= {delta + w / n:.5f}: {lhs <= delta + w / n}")


if __name__ == '__main__':
    args = [int(v) for v in sys.argv[1:]]
    tori = [tuple(args[i:i + 3]) for i in range(0, len(args), 3)] or [(1, 1, 3), (1, 0, 3), (2, 0, 2), (1, 1, 4), (1, 0, 4)]
    res = {t: run(*t) for t in tori}
    print()
    if (2, 0, 2) in res and (1, 1, 4) in res:
        for nn in (2, 4, 8):
            price_compare_check(res[(2, 0, 2)], res[(1, 1, 4)], nn)
