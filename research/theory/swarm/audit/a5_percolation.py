"""A5.  The percolation models under the lower bound, exactly, on small rings.

zeta = two-parent oriented site percolation of density p on the cylinder Z_K x N:
       zeta'(i) = V(i) * max(zeta(i), zeta(i+1)),  V i.i.d. Bernoulli(p).
OP5  = five-parent oriented site percolation of density p on Z_L.
Kernel of either: zeta' = p-thinning of the eligible set N(zeta); so (Qf)(zeta) = g(N(zeta)) with
g(M) = sum_{B<=M} p^|B| (1-p)^(|M|-|B|) f(B)  (one pass per site).

(1) Unconditional comparison of Perron eigenvalues (AUDIT section 2, Theorem U):
        lambda_anchor(L) >= lambda_OP5(1/2)(L) >= lambda_2dOP(3/4)(L/2),   L = 6..LA even.
    (anchor values: recomputed here with the generic contraction engine)
(2) 2dOP(p) on Z_K, K = 2..KMAX: tau = 1/(1-lambda), ln tau and steps, at p = 0.60 (subcritical),
    0.7055 (near critical), 0.75 (the density the theorem uses), 0.85, 0.95.
    This shows what fact F2 asserts and at which sizes it becomes visible.
(3) OP5(1/2) on Z_L, L = 5..LMAX5: ln tau and steps (prob. Proposition F: limsup step <= 0.4812).
(4) Submultiplicativity fill-in (AUDIT 2.6): for a monotone chain started from the top,
    E T >= M  implies  P(T >= M/2) >= 1/2.  Checked on 2dOP(3/4), K = 3..10, exactly.
(5) Survival from one site on Z (no wrap while n < K-1), p = 3/4: P(alive at n), n <= 21.  A consequence of
    Liggett's inequality as quoted by Rath-Valesin is that this stays >= 2/3 for all n (AUDIT 3.2).

Run:  python3 a5_percolation.py [KMAX=22] [LMAX5=22] [LA=16]
"""
import sys
import math
import numpy as np
from audit_lib import apply_kernel, local_kernel_E1, perron

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22
LMAX5 = int(sys.argv[2]) if len(sys.argv) > 2 else 22
LA = int(sys.argv[3]) if len(sys.argv) > 3 else 16
ok = True


def thin_transform(f, K, p):
    g = np.array(f, dtype=float).reshape((2,) * K)
    for ax in range(K):
        g0 = np.take(g, 0, axis=ax)
        g1 = np.take(g, 1, axis=ax)
        g = np.stack([g0, (1 - p) * g0 + p * g1], axis=ax)
    return g.reshape(-1)


def eligible(K, parents):
    N = 1 << K
    S = np.arange(N, dtype=np.int64)
    Nb = np.zeros(N, dtype=np.int64)
    for d in parents:
        dd = (-d) % K
        Nb |= (((S << dd) | (S >> (K - dd))) & (N - 1)) if dd else S
    return Nb


def op_perron(K, p, parents, tol=1e-13, maxit=200000):
    """Collatz-Wielandt bracket of the Perron eigenvalue on non-empty states (power iteration from 1)."""
    Nb = eligible(K, parents)
    N = 1 << K
    v = np.ones(N)
    v[0] = 0
    for it in range(1, maxit + 1):
        w = thin_transform(v, K, p)[Nb]
        w[0] = 0
        r = w[1:] / v[1:]
        lo, hi = r.min(), r.max()
        v = w / w[1:].max()
        if hi - lo < tol * hi:
            break
    return lo, hi, it


def op_survival_from(K, p, parents, start, tmax):
    Nb = eligible(K, parents)
    N = 1 << K
    v = np.ones(N)
    v[0] = 0
    out = [1.0]
    for _ in range(tmax):
        v = thin_transform(v, K, p)[Nb]
        v[0] = 0
        out.append(v[start])
    return np.array(out)


# (1)
print("(1)  L   1-lambda: anchor        OP5(1/2) on Z_L     2dOP(3/4) on Z_{L/2}    order holds")
qA = local_kernel_E1((0.5, 0.0, 0.5))
for L in range(6, LA + 1, 2):
    lo, hi, v, it = perron(L, qA, tol=1e-13)
    hA = 1 - 0.5 * (lo + hi)
    lo, hi, it = op_perron(L, 0.5, (-2, -1, 0, 1, 2))
    h5 = 1 - 0.5 * (lo + hi)
    lo, hi, it = op_perron(L // 2, 0.75, (0, 1))
    h2 = 1 - 0.5 * (lo + hi)
    good = hA <= h5 <= h2
    ok &= good
    print("     %2d   %.6e      %.6e        %.6e            %s     (ln tau: %.3f, %.3f, %.3f)"
          % (L, hA, h5, h2, good, -math.log(hA), -math.log(h5), -math.log(h2)), flush=True)

# (2)
for p in (0.60, 0.7055, 0.75, 0.85, 0.95):
    print("(2) 2dOP(p=%.4f) on Z_K:   K   ln tau    step" % p)
    prev = None
    for K in range(2, KMAX + 1):
        lo, hi, it = op_perron(K, p, (0, 1))
        h = 1 - 0.5 * (lo + hi)
        if h < 1e-11:
            print("       %2d   (1-lambda below 1e-11: beyond double precision; stopped)" % K)
            break
        lt = -math.log(h)
        print("       %2d  %8.4f  %s" % (K, lt, ("%7.4f" % (lt - prev)) if prev is not None else ""), flush=True)
        prev = lt

# (3)
print("(3) OP5(1/2) on Z_L:   L   ln tau    step      (Proposition F: limsup step <= ln((1+sqrt 5)/2) = %.4f)" % math.log((1 + 5 ** 0.5) / 2))
prev = None
for L in range(5, LMAX5 + 1):
    lo, hi, it = op_perron(L, 0.5, (-2, -1, 0, 1, 2))
    h = 1 - 0.5 * (lo + hi)
    lt = -math.log(h)
    print("       %2d  %8.4f  %s" % (L, lt, ("%7.4f" % (lt - prev)) if prev is not None else ""), flush=True)
    prev = lt

# (4)
for K in range(3, 11):
    N = 1 << K
    lo, hi, it = op_perron(K, 0.75, (0, 1))
    tau = 1 / (1 - 0.5 * (lo + hi))
    s = op_survival_from(K, 0.75, (0, 1), N - 1, int(40 * tau) + 50)
    ET = s.sum()                       # E T = sum_{t>=0} P(T > t)
    half = int(math.floor(ET / 2))
    # P(T >= M/2) with M = E T:  P(T >= x) = P(T > ceil(x) - 1)
    x = math.ceil(ET / 2)
    pr = s[x - 1] if x >= 1 else 1.0
    sub = bool(np.all(s[2:200:3] <= s[1] * s[1:199:3] + 1e-15))
    ok &= pr >= 0.5
    print("(4) K=%2d  E_full T = %10.3f  (tau = %10.3f)   P(T >= E T / 2) = %.4f >= 1/2: %s"
          % (K, ET, tau, pr, pr >= 0.5))

# (5)
K = 24
s = op_survival_from(K, 0.75, (0, 1), 1, K - 3)
print("(5) 2dOP(3/4) on Z from one occupied site: P(alive at n), n = 1..%d" % (K - 3))
print("    " + " ".join("%.4f" % z for z in s[1:]))
ok &= bool(np.all(s >= 2 / 3))
print("    all >= 2/3: %s" % bool(np.all(s >= 2 / 3)))

print("A5 ALL OK" if ok else "A5 FAILED")
