#!/usr/bin/env python3
"""ref-chain: ChainSeam.lean's identities by brute force over ring products of a random F >= 0.

  python3 research/blast/ref-chain/seam_check.py          (a few seconds)

Torus: m = M+1 bands (a, xs), weight F[a,x0] F[x0,x1] ... F[x_{M-1},a].  Cover: N = m + L bands cut at the seam
and at its image c one loop along, weight F[a,x0]...F[x_{M-1},c] * F[c,y0]...F[y_{L'-1},a], L = L'+1.
seam_identity:  P_T(a,xs) = sum_ys P_C(a,xs,a,ys) * Tr F^N / (Tr F^m * (F^L)[a,a]),  claimed for L = k*m.
Also: the same for L not a multiple of m (holds whenever (F^L)[a,a] > 0, fails where it vanishes and the torus
weight does not); seam_sharp under Tr F^m = Tr F^2m = 1 (a rank-one F = v w^T with w.v = 1).
"""
import itertools
import numpy as np

rng = np.random.default_rng(7)


def path(F, a, xs, b):
    w = 1.0; prev = a
    for x in list(xs) + [b]:
        w *= F[prev, x]; prev = x
    return w


def check(F, M, Lp, verbose=False):
    """max relative error of the seam identity over all (a, xs); also reports zero-denominator cases."""
    B = F.shape[0]; m = M + 1; L = Lp + 1; N = m + L
    trm = np.trace(np.linalg.matrix_power(F, m)); trN = np.trace(np.linalg.matrix_power(F, N))
    FL = np.linalg.matrix_power(F, L)
    worst = 0.0; fails = 0; zero_den = 0
    for a in range(B):
        for xs in itertools.product(range(B), repeat=M):
            PT = path(F, a, xs, a) / trm
            PC = sum(path(F, a, xs, a) * path(F, a, ys, a) for ys in itertools.product(range(B), repeat=Lp)) / trN
            den = trm * FL[a, a]
            rhs = PC * trN / den if den != 0 else 0.0          # Lean: x / 0 = 0
            if den == 0: zero_den += 1
            err = abs(PT - rhs) / max(abs(PT), 1e-300)
            if abs(PT - rhs) > 1e-12 * max(1, abs(PT)): fails += 1
            worst = max(worst, err if PT != 0 else abs(rhs))
    return worst, fails, zero_den


print("seam_identity on random F >= 0 (3x3, entries U(0,1) with 30% zeros):")
for M in (0, 1, 2, 3):
    for k in (1, 2):
        F = rng.random((3, 3)) * (rng.random((3, 3)) > 0.3)
        Lp = k * (M + 1) - 1
        w, f, z = check(F, M, Lp)
        print(f"  m = {M+1}, L = {k}*m = {Lp+1}: worst relative error {w:.1e}, failures {f}, zero denominators {z}")

print("L not a multiple of m, random dense F > 0 (identity holds whenever (F^L)[a,a] > 0):")
for M, Lp in ((1, 0), (2, 0), (2, 2), (3, 1)):
    F = rng.random((3, 3)) + 0.05
    w, f, z = check(F, M, Lp)
    print(f"  m = {M+1}, L = {Lp+1}: worst relative error {w:.1e}, failures {f}, zero denominators {z}")

print("L not a multiple of m, F = the 2-cycle [[0,1],[1,0]] (period 2), m = 2, L = 1 and L = 3:")
F = np.array([[0.0, 1.0], [1.0, 0.0]])
for Lp in (0, 2):
    w, f, z = check(F, 1, Lp)
    print(f"  m = 2, L = {Lp+1}: failures {f} of 4 torus configurations, zero denominators {z}  (P_T = 1/2 on "
          f"(a, other), right-hand side 0)")
w, f, z = check(F, 1, 1)
print(f"  m = 2, L = 2 (a multiple): failures {f}, zero denominators {z}")
F = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]) * 0.7 + 0.0
for M, Lp in ((2, 0), (2, 1), (2, 2), (2, 5)):
    w, f, z = check(F, M, Lp)
    print(f"  3-cycle, m = 3, L = {Lp+1}: failures {f}, zero denominators {z}")

print("seam_sharp, F = v w^T with w.v = 1 (Tr F^n = 1 for all n):")
for M in (0, 1, 2):
    v = rng.random(3); w = rng.random(3); w /= w @ v
    F = np.outer(v, w)
    m = M + 1
    tr1 = np.trace(np.linalg.matrix_power(F, m)); tr2 = np.trace(np.linalg.matrix_power(F, 2 * m))
    worst = 0.0
    for a in range(3):
        PTa = sum(path(F, a, ys, a) for ys in itertools.product(range(3), repeat=M)) / tr1
        for xs in itertools.product(range(3), repeat=M):
            lhs = sum(path(F, a, xs, a) * path(F, a, ys, a) for ys in itertools.product(range(3), repeat=M)) / tr2
            rhs = path(F, a, xs, a) / tr1 * PTa
            worst = max(worst, abs(lhs - rhs))
    print(f"  m = {m}: Tr F^m = {tr1:.15f}, Tr F^2m = {tr2:.15f}, worst |lhs - rhs| = {worst:.1e}")
F = rng.random((3, 3))
F /= np.abs(np.linalg.eigvals(F)).max()
M = 1; m = 2
tr1 = np.trace(np.linalg.matrix_power(F, m)); tr2 = np.trace(np.linalg.matrix_power(F, 2 * m))
worst = 0.0
for a in range(3):
    PTa = sum(path(F, a, ys, a) for ys in itertools.product(range(3), repeat=M)) / tr1
    for xs in itertools.product(range(3), repeat=M):
        lhs = sum(path(F, a, xs, a) * path(F, a, ys, a) for ys in itertools.product(range(3), repeat=M)) / tr2
        rhs = path(F, a, xs, a) / tr1 * PTa
        worst = max(worst, abs(lhs - rhs) / rhs)
print(f"  control, a generic F (traces {tr1:.3f}, {tr2:.3f}, not 1): worst relative |lhs - rhs| = {worst:.2f} "
      f"(the hypothesis is needed)")
