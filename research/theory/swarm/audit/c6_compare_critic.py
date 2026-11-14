#!/usr/bin/env python3
"""Audit of the counting line: numbers set beside the critic's AFTER the verdicts were written.

  OMP_NUM_THREADS=1 python3 c6_compare_critic.py      (about 3 minutes, one core)

Part A is the only place where the audit touches the critic's lab code (critic/lab/counting_r1.py): it calls the
critic's own matrix and power iteration with more iterations, to show where "c_2 = 0.4671 at density 0.472" comes
from. It is a comparison, not a test of any claim; the audit's value (0.466846) is computed in c1_transfer.py from
the audit's own matrix. Parts B-D use only the audit's code.
"""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def part_a():
    print("=== A. c_2 at density 0.472: the critic's matrix and power iteration, more iterations")
    lab = os.path.join(HERE, "..", "critic", "lab")
    cwd = os.getcwd()
    os.chdir(lab)
    sys.path.insert(0, lab)
    try:
        import counting_r1 as cr
        W, nxt = cr.k2_weights(0.472)
        for it in (400, 1000, 3000, 10000):
            rho = cr.spectral(W, nxt, iters=it)
            print(f"  critic's spectral(), iters = {it:5d}: rho = {rho:.9f}, c_2 = {-math.log(rho):.6f}"
                  + ("   <- the lab's default; the reply and the board print 0.4671" if it == 400 else ""))
    finally:
        os.chdir(cwd)
        sys.path.remove(lab)


def part_b():
    print("\n=== B. the audit's matrix at density 0.472: two leading eigenvalues; c_2(p) near 1/2")
    import scipy.sparse.linalg as sla
    from c0_lib import T2, spectral_radius
    ev = sla.eigs(T2(0.472), k=2, which='LM', return_eigenvectors=False)
    ev = sorted(abs(ev), reverse=True)
    print(f"  leading eigenvalues {ev[0]:.6f}, {ev[1]:.6f} (ratio {ev[1] / ev[0]:.4f}); c_2 = {-math.log(ev[0]):.6f}")
    for p in (0.47, 0.472, 0.475, 0.48, 0.49, 0.5):
        print(f"  c_2({p}) = {-math.log(spectral_radius(T2(p))[0]):.6f}")


def part_c():
    print("\n=== C. exact slopes of -ln D_k(L) on rings between L = 20 and 32 (entry 13 quotes samples 0.542, 0.479)")
    import scipy.sparse.linalg as sla
    from c0_lib import T1, T2
    ev = np.linalg.eigvals(T1(0.5, count=True))
    Ls = [20, 24, 28, 32]
    v = [-math.log((np.sum(ev ** L)).real / 8.0 ** L) for L in Ls]
    print(f"  k = 1 (all 16 eigenvalues): -ln D_1 = {[round(x, 4) for x in v]}, slope {np.polyfit(Ls, v, 1)[0]:.5f}; limit 0.551535")
    ev2 = sla.eigs(T2(0.5, count=True), k=40, which='LM', return_eigenvectors=False, tol=1e-12)
    v = [-math.log((np.sum(ev2 ** L)).real / 32.0 ** L) for L in Ls]
    e = sorted(abs(ev2), reverse=True)
    print(f"  k = 2 (leading 40 eigenvalues; first two {e[0]:.4f}, {e[1]:.4f}): -ln D_2 = {[round(x, 4) for x in v]}, "
          f"slope {np.polyfit(Ls, v, 1)[0]:.5f}; limit 0.467693")


def part_d():
    print("\n=== D. numbers of the critic's replies recomputed with the audit's code")
    from c2_gump_face import slab, face_structure, predicted_counts
    for (m, n), quoted in (((1, 1), "185 of 2^9 states"), ((2, 2), "2,662 of 4,096 faces"), ((3, 2), "112,744 of 262,144 faces")):
        V, wrap = slab(m, n)
        face, beneath, cube = face_structure(V, wrap, 5)
        relevant = sorted({j for i in face for j in beneath[i]})
        _, pred, _, _ = predicted_counts(V, wrap, 5, relevant)
        print(f"  gump slab {m} x {n}: face configurations that can be emptied in one generation {sum(1 for x in pred if int(x) > 0)} "
              f"of {1 << len(face)}; states that empty the face {int(sum(pred))} of 2^{V.N}   (critic: {quoted})")
    from c0_lib import w1
    print("  Lemma 8 on the one-row dice chain D2(L, 1/2), ring (critic, reply to round 3, section 2):")
    for L in (10, 12):
        n = 1 << L
        S = ((np.arange(n)[:, None] >> np.arange(L)) & 1).astype(np.int8)
        k = sum(np.roll(S, d, axis=1) for d in (1, 2, -1, -2))
        wt = np.array([[w1(s, kk) for kk in range(5)] for s in (0, 1)])
        pd = wt[S, k]
        Q = np.ones((n, n))
        for i in range(L):
            Q *= np.where(S[None, :, i] == 0, pd[:, i][:, None], 1 - pd[:, i][:, None])
        Q = Q[1:, 1:]
        phi = np.ones(n - 1); mu = np.ones(n - 1) / (n - 1)
        for _ in range(3000):
            phi = Q @ phi; lam = phi.max(); phi /= lam
            mu = mu @ Q; mu /= mu.sum()
        h = 1 - lam
        pi = np.full(n - 1, 1 / (n - 1))
        print(f"    L = {L}: h = {h:.3e}; min phi = {phi.min():.2f}; mu(1 - phi)/h = {float(mu @ (1 - phi)) / h:.2f}; "
              f"fair product row on living rows: pi(1 - phi)/h = {float(pi @ (1 - phi)) / h:.2f}, "
              f"e(pi)/h = {(1 - float(pi @ phi) / float(mu @ phi)) / h:+.2f}")
    print("    critic: h = 4.50e-3, 1.62e-3; min phi 0.59; 3.7, 4.7; 3.35, 4.43; -0.34, -0.29")
    X = np.indices((4, 4)).sum(0) % 2
    m_ = sum(np.roll(X, s, a) for s in (1, -1) for a in (0, 1))
    print(f"  face12e sheet map Theta on a 4 x 4 torus: checkerboard -> its complement: {bool((((m_ + X) >= 4) == (1 - X)).all())} "
          f"(the period-2 orbits of the critic's E19)")


if __name__ == "__main__":
    part_a(); part_b(); part_c(); part_d()
