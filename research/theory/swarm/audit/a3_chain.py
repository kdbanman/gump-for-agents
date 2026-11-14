"""A3.  The dice chain E1(1/2,0,1/2) on the ring Z_L (the row 0 of A(L)): structure and lifetime.

(1) engine check: the cell-by-cell contraction apply_kernel equals the dense matrix (L = 5..9).
(2) at the anchor, S' is uniform on the interval [F(S), E(S)] of the subset lattice,
    F = live cells with k = 2, E = S + [-2,2]  (prob. entry 3, "what this model is").
(3) irreducible and aperiodic on non-empty states (L = 5..10): from the full ring every subset is a
    next state; the full ring is reached from every non-empty state in ceil(L/4) steps.
(4) the three-move game (theorems.md B(a)): for every S the proof's strategy empties the ring in <= 3
    moves, each move allowed (L = 5..16); and exactly, min_S P_S(T <= 3) >= 8^-L (L = 5..9).
(5) Perron eigenvalue lambda_L, tau_L = 1/(1-lambda_L), ln tau_L, steps, for L = 5..LMAX (default 16);
    Collatz-Wielandt bracket for lambda; the bound tau_L <= 3*8^L; exactly geometric from mu_L.
(6) "from one start to tau" (prob. entry 1): with t* = max{t : P_full(T > t) >= 1/2},
    tau_L >= (t*+m)/(L m ln 2 + ln 2), m = ceil(L/4)  (L = 5..12).

Run:  python3 a3_chain.py [LMAX]      (LMAX = 16: about 10 minutes; 18: about an hour)
"""
import sys
import math
import numpy as np
from audit_lib import (bit, kcount, dense_kernel, local_kernel_E1, apply_kernel, perron, survival_curve)

LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
q = local_kernel_E1((0.5, 0.0, 0.5))
ok = True


def F_set(S, L):
    return sum(1 << y for y in range(L) if bit(S, y, L) and kcount(S, y, L) == 2)


def E_set(S, L):
    out = 0
    for y in range(L):
        if any(bit(S, y + d, L) for d in (-2, -1, 0, 1, 2)):
            out |= 1 << y
    return out


# (1) engine
rng = np.random.default_rng(1)
for L in range(5, 10):
    Q = dense_kernel(L, q)
    f = rng.random(1 << L)
    err = np.abs(Q @ f - apply_kernel(f, L, q)).max()
    ok &= err < 1e-13
    print("(1) L=%d  max |dense Q f - contraction| = %.1e" % (L, err))

# (2) interval structure
for L in range(5, 11):
    Q = dense_kernel(L, q)
    good = True
    for S in range(1, 1 << L):
        F, E = F_set(S, L), E_set(S, L)
        free = bin(E & ~F).count("1")
        Sp = np.arange(1 << L)
        inside = ((Sp & F) == F) & ((Sp & ~E) == 0)
        good &= bool(np.all(Q[S][inside] == 0.5 ** free) and np.all(Q[S][~inside] == 0))
    ok &= good
    print("(2) L=%d  Q(S,.) uniform on [F(S),E(S)] for every S: %s" % (L, good))

# (3) irreducible, aperiodic
for L in range(5, 11):
    Q = dense_kernel(L, q)
    full = (1 << L) - 1
    a = bool(np.all(Q[full] == 0.5 ** L))
    m = math.ceil(L / 4)
    P = np.linalg.matrix_power(Q, m)
    b = bool(np.all(P[1:, full] >= 0.5 ** (L * m)))
    ok &= a and b
    print("(3) L=%d  full -> every subset w.p. 2^-L: %s;  min_S P_S(S_m = full), m=%d: %.3e >= 2^-(Lm) = %.3e: %s"
          % (L, a, m, P[1:, full].min(), 0.5 ** (L * m), b))

# (4) three-move game: strategy S1 = E(S0), S2 = F(S1), S3 = F(S2) must be empty; moves allowed means
#     F(S) <= S' <= E(S) at each move
for L in range(5, 17):
    good = True
    for S0 in range(1, 1 << L):
        S1 = E_set(S0, L)
        S2 = F_set(S1, L)
        S3 = F_set(S2, L)
        good &= (S3 == 0) and (F_set(S0, L) & ~S1) == 0 and (S2 & ~E_set(S1, L)) == 0
        if not good:
            print("   counterexample", L, bin(S0))
            break
    ok &= good
    print("(4) L=%d  strategy of Theorem B(a) empties every non-empty row in <= 3 moves: %s" % (L, good))
for L in range(5, 10):
    Q = dense_kernel(L, q)
    P3 = np.linalg.matrix_power(Q, 3)
    mn = P3[1:, 0].min()
    arg = 1 + int(P3[1:, 0].argmin())
    ok &= mn >= 8.0 ** (-L)
    print("(4) L=%d  min_S P_S(T<=3) = %.6e (at S=%s) >= 8^-L = %.6e: %s; ratio %.1f"
          % (L, mn, format(arg, "0%db" % L), 8.0 ** (-L), mn >= 8.0 ** (-L), mn * 8.0 ** L))

# (5) Perron eigenvalue
print("(5)  L   1-lambda (lower, upper)            tau_L          ln tau_L   step    ln(3*8^L)  iterations")
prev = None
res = {}
for L in range(5, LMAX + 1):
    lo, hi, v, it = perron(L, q, tol=1e-13)
    h_lo, h_hi = 1 - hi, 1 - lo
    h = 0.5 * (h_lo + h_hi)
    lt = -math.log(h)
    res[L] = lt
    ok &= (1 / h) <= 3 * 8.0 ** L
    print("     %2d  %.10e  %.10e  %14.4f  %9.4f  %s  %8.3f   %d"
          % (L, h_lo, h_hi, 1 / h, lt, ("%6.4f" % (lt - prev)) if prev else "   -  ", math.log(3) + L * math.log(8), it), flush=True)
    prev = lt
quoted = {8: 6.5319, 12: 9.4733, 16: 12.2492, 18: 13.5946}
for L, val in quoted.items():
    if L in res:
        print("     L=%d: mine %.4f, quoted in source S14 (iii): %.4f, difference %.1e" % (L, res[L], val, res[L] - val))
        ok &= abs(res[L] - val) < 6e-5

# geometric law from mu (left eigenvector), dense, L = 8
L = 8
Q = dense_kernel(L, q)[1:, 1:]
w, V = np.linalg.eig(Q.T)
i = int(np.argmax(w.real))
mu = np.abs(V[:, i].real)
mu /= mu.sum()
lam = w[i].real
surv = [1.0]
cur = mu.copy()
for t in range(1, 6):
    cur = cur @ Q
    surv.append(cur.sum())
dev = max(abs(surv[t] - lam ** t) for t in range(6))
ok &= dev < 1e-13
print("(5) L=8: from mu_L, P(T>t) - lambda^t for t<=5: max %.1e;  mu Q / lambda = mu: %.1e"
      % (dev, np.abs(mu @ Q / lam - mu).max()))

# (6) from one start to tau
for L in range(5, 13):
    lo, hi, v, it = perron(L, q, tol=1e-13)
    tau = 1 / (1 - 0.5 * (lo + hi))
    full = (1 << L) - 1
    tmax = int(3 * tau) + 10
    s = survival_curve(L, q, full, tmax)
    tstar = int(np.max(np.nonzero(s >= 0.5)[0]))
    m = math.ceil(L / 4)
    bound = (tstar + m) / (L * m * math.log(2) + math.log(2))
    ok &= tau >= bound
    print("(6) L=%2d  t* = %6d   bound (t*+m)/(Lm ln2 + ln2) = %10.3f   tau_L = %12.3f   holds: %s"
          % (L, tstar, bound, tau, tau >= bound))

print("A3 ALL OK" if ok else "A3 FAILED")
