#!/usr/bin/env python3
"""Theorem P-bar and Theorem Q on a sample of gump's own living state: the hull R = 7 (faces of 30 cells).

  python3 p5_hull30.py [replicas=40000] [seed=1]        (about three minutes, one core)

Sample: soups of density 0.35 in the diagonal hull R = 7 (264 cells), stepped with p0_lib.Vessel (bit-exact
against reference/oracle.py, `python3 p0_lib.py`). A replica is observed from age T0 = 200 while all eight
faces are alive and the state has not been seen to repeat with period 1 or 2; the first face to empty is a death
(of that face; the other seven are censored). The statistic is the population of a face, pooled over the
eight faces. The counts N(z), D(z), F(z, z') are integers, tallied for every row (also above A/2).

Printed:
  1. Theorem P-bar on the sample, in exact rational arithmetic (both sides of the identity, compared with ==).
  2. The local roots, hypothesis R on the block [5, K), K = ceil(0.35 A) = 11, and Phi, C+ of Theorem Q:
     over the rows K..A/2 (what path could compute from the tallies it had) and over all rows.
  3. The size of each term of Q's bound against the measured hazard.
"""
import sys, time, math
from fractions import Fraction as Fr
import numpy as np
from p0_lib import hull, DIAGS, committor
from p2_tables import M, root

R, T0, TMAX, DENS = 7, 200, 4000, 0.35


def sample(n_rep, seed):
    V = hull(R); N = V.N
    faces = [V.layer(d, R) for d in DIAGS]
    A = len(faces[0])
    FI = np.zeros((N, 8), np.int64)
    for f, cells in enumerate(faces):
        FI[cells, f] = 1
    rng = np.random.default_rng(seed)
    Nc = np.zeros(A + 1, np.int64); Dc = np.zeros(A + 1, np.int64); Fc = np.zeros((A + 1, A + 1), np.int64)
    start = np.zeros(A + 1, np.int64); end = np.zeros(A + 1, np.int64)
    born = settled = 0
    for chunk in range(0, n_rep, 10000):
        n = min(10000, n_rep - chunk)
        X = (rng.random((n, N)) < DENS).astype(np.int8)
        Xm1 = None; Xm2 = None
        Z = X.astype(np.int64) @ FI
        keep = (Z > 0).all(1); X, Z = X[keep], Z[keep]
        for t in range(0, TMAX + 1):
            if len(X) == 0:
                break
            if t == T0:
                born += len(X)
                np.add.at(start, Z.ravel(), 1)
            Y = V.step(X)
            Zn = Y.astype(np.int64) @ FI
            dead = (Zn == 0)
            anydead = dead.any(1)
            per = np.zeros(len(X), bool)
            if Xm1 is not None:
                per = (Y == X).all(1) | (Y == Xm1).all(1)          # period 1 or 2 detected at t+1
            per &= ~anydead
            if t >= T0:
                np.add.at(Nc, Z.ravel(), 1)
                np.add.at(Dc, Z[dead], 1)                          # the faces that are empty at t+1
                st = ~anydead & ~per
                np.add.at(Fc, (Z[st].ravel(), Zn[st].ravel()), 1)
                settled += int(per.sum())
            st = ~anydead & ~per
            Xm1 = X[st]; X = Y[st]; Z = Zn[st]
        np.add.at(end, Z.ravel(), 1)                               # still observed at TMAX + 1
    return A, Nc, Dc, Fc, start, end, born, settled


def main():
    n_rep = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    t = time.time()
    A, Nc, Dc, Fc, start, end, born, settled = sample(n_rep, seed)
    Expo, Deaths = int(Nc.sum()), int(Dc.sum())
    print(f"hull R={R}: faces of A={A} cells; {n_rep} soups, {born} replicas reached age {T0} with eight living faces; "
          f"{settled} settled; exposure {Expo} face-generations, {Deaths} deaths ({time.time() - t:.0f} s)")
    h = Deaths / Expo
    print(f"hazard = {h:.4e}, -ln h = {-math.log(h):.3f} +- {1 / math.sqrt(Deaths):.3f}   (board: ln tau = 6.804 at A = 30)")
    # the two exact identities of entry 8
    assert all(Fc[z].sum() + Dc[z] <= Nc[z] for z in range(A + 1))
    assert all(Fc[:, z].sum() == Nc[z] - start[z] + end[z] for z in range(1, A + 1)), "identity (I)"
    K = math.ceil(0.35 * A); k0 = 5
    # 1. P-bar, exactly
    Ncnt = {z: int(Nc[z]) for z in range(1, A + 1) if Nc[z]}
    T = {(z, z2): Fr(int(Fc[z, z2]), int(Nc[z])) for z in Ncnt for z2 in range(1, A + 1) if Fc[z, z2]}
    d = {z: Fr(int(Dc[z]), int(Nc[z])) for z in Ncnt}
    for Kc in (K, A // 2 + 1):
        low = [z for z in range(1, Kc) if z in Ncnt]
        psi = committor(T, d, low)
        D_out = sum(int(Dc[z]) for z in range(Kc, A + 1))
        entry = sum(Fr(int(Fc[z, z2])) * psi[z2] for z in range(Kc, A + 1) for z2 in low if Fc[z, z2])
        bs = sum(Fr(int(start[z])) * psi[z] for z in low); be = sum(Fr(int(end[z])) * psi[z] for z in low)
        print(f"1. P-bar, low set 1..{Kc - 1}: Deaths = {Deaths};  direct deaths from above = {D_out}, "
              f"sum over entries of psi* = {float(entry):.4f}, start = {float(bs):.4f}, end = {float(be):.4f};  "
              f"identity exact: {Fr(Deaths) == D_out + entry + bs - be}")
        if Kc == K:
            psiK = psi
            n_entries = int(sum(Fc[z, z2] for z in range(K, A + 1) for z2 in range(1, K)))
            print(f"   crossings into the low set per unit exposure chi = {n_entries / Expo:.4f}; "
                  f"psi*(1..6) = {[round(float(psi[z]), 4) for z in range(1, 7)]}; psi*({K - 1}) = {float(psi[K - 1]):.3e}")
    # 2. roots, R, Phi, C+
    Tm = np.zeros((A + 1, A + 1)); Tm[0, 0] = 1
    for z in range(1, A + 1):
        if Nc[z]:
            Tm[z] = Fc[z] / Nc[z]; Tm[z, 0] = Dc[z] / Nc[z]
    th = {z: root(Tm[z], z) for z in range(1, A + 1) if Nc[z]}
    print("2. local roots theta_k, k = 1..15:", " ".join(f"{th[z]:.3f}" for z in range(1, 16)))
    print("   visits N(k), k = 1..10:", " ".join(str(int(Nc[z])) for z in range(1, 11)))
    theta0 = min(th[z] for z in range(k0, K))
    print(f"   least root on the block [{k0}, {K}) = {theta0:.4f}   (path, 23.3: 0.4034);  hypothesis R(0.35, 0.40, 5): {theta0 >= 0.40}")
    p = Nc / Expo
    def Phi_C(zmax):
        Phi = sum(p[z] * sum(Tm[z, z2] * math.exp(theta0 * (K - z2)) for z2 in range(0, K)) for z in range(K, zmax + 1))
        Cp, zarg = max((M(Tm[z], z, theta0) * math.exp(-theta0 * (z - K)), z) for z in range(K, zmax + 1) if Nc[z])
        dd = int(Dc[K:zmax + 1].sum())
        return Phi, Cp, zarg, dd
    for label, zmax in (("rows K..A/2", A // 2), ("all rows K..A", A)):
        Phi, Cp, zarg, dd = Phi_C(zmax)
        print(f"   {label}: Phi = {Phi:.4f}, C+ = {Cp:.4f} (at row {zarg}), direct deaths {dd}, "
              f"share of the exposure {float(p[K:zmax + 1].sum()):.3f}   (path, K..A/2: Phi 0.136, C+ 1.043, 1 direct death)")
    Phi, Cp, _, _ = Phi_C(A)
    # 3. Theorem Q on the sample
    psi = np.array([math.exp(-theta0 * max(z - k0, 0)) if z < K else 0.0 for z in range(A + 1)])
    bstart = float(np.dot(start[1:K], psi[1:K])); bend = float(np.dot(end[1:K], psi[1:K]))
    main_term = math.exp(-theta0 * (K - k0)) * Phi
    print(f"3. Theorem Q with theta0 = {theta0:.4f}, K = {K}, k0 = {k0}:")
    print(f"   Deaths/Expo = {h:.4e}  <=  e^(-theta0(K-k0)) Phi = {main_term:.4e}  +  (start - end)/Expo = "
          f"{(bstart - bend) / Expo:.3e}   holds: {h <= main_term + (bstart - bend) / Expo}")
    print(f"   theta0 (K-k0) - ln Phi = {theta0 * (K - k0) - math.log(Phi):.3f};  with C+ in place of Phi: "
          f"{theta0 * (K - k0) - math.log(Cp):.3f};  -ln h = {-math.log(h):.3f}")
    w = float(np.dot(p[1:K], psi[1:K])); cens = (Expo - Deaths - int(Fc.sum())) / Expo
    print(f"   pooled mass below K: {float(p[1:K].sum()):.4f}; w = sum p_z psi(z) = {w:.4e}; censoring per unit exposure "
          f"sbar = {cens:.4e} = {cens / h:.2f} h;  w sbar = {w * cens:.3e} (the quasi-stationary window term)")
    print(f"   start term per unit exposure {bstart / Expo:.3e}, end term {bend / Expo:.3e}")


if __name__ == "__main__":
    main()
