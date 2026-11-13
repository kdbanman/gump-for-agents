"""gap.py -- does a hole in a living face heal, and does its drift/diffusion ratio give the face-law exponent?

A periodic strip (2D) is run to its quasi-stationary state in 64 replicas; then a stretch of g cells of one edge
row is killed in every replica (the cells behind it are untouched) and the number N(t) of live cells of that row is
followed.  If the hole closes from its two ends with front speed v and front diffusivity D,
      d<N>/dt = 2 v rho_f ,      (1/2) dVar(N)/dt = 2 D rho_f^2 + v chi
(rho_f = edge density, chi = equilibrium variance of N per cell), and a hole that must grow to length L against
this drift costs exp(-(v/D) L): the prediction is  slope of ln tau_edge per cell  =  v / D.

    python3 gap.py LATTICE b c L m g [reps] [p]
"""
import json, os, struct, subprocess, sys
import numpy as np
import lattices as LT, theory as TH, vessel as VS, run as RN

if __name__ == "__main__":
    lat, b, c, Ln, m, g = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    reps = int(sys.argv[7]) if len(sys.argv) > 7 else 8
    L = LT.get(lat)
    B, S = TH.capped(b, c, L.K)
    p = float(sys.argv[8]) if len(sys.argv) > 8 else RN.default_p(L.K, B, S)
    u = (0, 1) if lat.startswith(("cross", "moore", "vn", "star")) else tuple(TH.sealed_rays(L, b)[0])
    V = VS.slab(L, u, m, Ln)
    row = sorted(V.faces[0], key=lambda i: V.cells[i])
    kill = row[len(row) // 2 - g // 2: len(row) // 2 - g // 2 + g]
    gf = os.path.join(RN.SCR, f"gap_{os.getpid()}.bin")
    kf = gf + ".kill"
    V.write(gf)
    open(kf, "wb").write(struct.pack("<i", len(kill)) + np.array(kill, dtype="<i4").tobytes())
    Tr = 4 * g + 100
    acc = []
    eqm, eqv = [], []
    for s in range(reps):
        out = subprocess.run([os.path.join(RN.SCR, "gstep_gap"), "gap", gf, str(RN.mask(B)), str(RN.mask(S)), str(b), str(p),
                              str(1000 + s), "600", str(Tr), kf], capture_output=True, text=True, check=True).stdout
        r = json.loads(out)
        acc.append(np.array(r["rows"], dtype=float))
        eqm.append(r["eq_mean"]); eqv.append(r["eq_var"])
    os.remove(gf); os.remove(kf)
    A = np.mean(acc, axis=0)          # t, mean N, var N (within-run over 64 replicas), dead count
    Lrow = len(row)
    rho_f, chi = np.mean(eqm) / Lrow, np.mean(eqv) / Lrow
    N0, Neq = A[0, 1], np.mean(eqm)
    # closing window: from 10% to 60% of the deficit recovered
    deficit = Neq - A[:, 1]
    d0 = deficit[0]
    lo = next((i for i in range(len(A)) if deficit[i] <= 0.9 * d0), None)
    hi = next((i for i in range(len(A)) if deficit[i] <= 0.4 * d0), None)
    if lo is None or hi is None or hi - lo < 4:
        print(f"{lat} b={b} c={c}: the hole did not close (deficit {d0:.1f} -> {deficit[-1]:.1f} after {Tr} generations; "
              f"rho_f={rho_f:.3f}); replicas with a dead row at the end: {A[-1, 3]:.1f}/64")
        sys.exit(0)
    t = A[lo:hi + 1, 0]
    dN = np.polyfit(t, A[lo:hi + 1, 1], 1)[0]
    dV = np.polyfit(t, A[lo:hi + 1, 2], 1)[0]
    v = dN / (2 * rho_f)
    D = (0.5 * dV - v * chi) / (2 * rho_f ** 2)
    print(f"{lat} b={b} c={c} L={Lrow} m={m} hole={g}: rho_f={rho_f:.3f} chi={chi:.3f}; window t={int(t[0])}..{int(t[-1])}; "
          f"d<N>/dt={dN:.4f} dVar/dt={dV:.4f} -> v={v:.4f} cells/gen, D={D:.4f}; predicted slope v/D = {v / D if D > 0 else float('nan'):.3f} per cell")
