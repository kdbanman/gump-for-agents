#!/usr/bin/env python3
"""The measured parts of claims Q and V-(E), recomputed from the lab's tallies with the audit's own code.

  python3 p7_tallies.py            (a second)

Reads `critic/lab/data/fluct_tables.npz` (hull faces A = 30, 45, 63, 84; Tr[k, k'] = one-step transitions from
rows k <= A/2, column 0 = death; H[z] = face-generations at population z, all rows). Rows are normalised by
their own sums (the tallies hold no censored transitions). Uses only p2_tables.root and p2_tables.M.

  - least local root on the block [5, K), K = ceil(0.35 A)                (claims.md, Q: 0.4034, 0.4261, 0.4117, 0.4172)
  - Phi and C+ over the tallied rows K..A/2, with theta0 = that minimum   (0.136, 0.103, 0.085, 0.046; <= 1.07)
  - for A = 84: the margin eps0 of the block 5..29 at its best theta0, and the thresholds m0(delta) of (S)
    (claims.md, V-(E): 41, 197, 489)
  - the smallest case of claim Q (walk on {0..3}, up 3/4, held at 3)
"""
import os, math
import numpy as np
from p2_tables import M, root

HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(HERE, "..", "critic", "lab", "data", "fluct_tables.npz"))

for R in (7, 9, 11, 13):
    Tr = d[f"Tr_{R}"].astype(float); H = d[f"H_{R}"].astype(float)
    A = len(H) - 1; half = Tr.shape[0] - 1
    T = np.zeros((half + 1, A + 1))
    for k in range(1, half + 1):
        T[k] = Tr[k] / Tr[k].sum()
    K = math.ceil(0.35 * A); k0 = 5
    th = {k: root(T[k], k) for k in range(1, half + 1)}
    theta0 = min(th[k] for k in range(k0, K)); kmin = min(range(k0, K), key=lambda k: th[k])
    p = H / H.sum()
    Phi = sum(p[z] * sum(T[z, z2] * math.exp(theta0 * (K - z2)) for z2 in range(0, K)) for z in range(K, half + 1))
    chi = sum(p[z] * T[z, :K].sum() for z in range(K, half + 1))
    Cp, zarg = max((M(T[z], z, theta0) * math.exp(-theta0 * (z - K)), z) for z in range(K, half + 1))
    h = float(d[f"deaths_{R}"][0]) / H.sum()
    print(f"A={A}: K={K}; roots of rows 1..5: {' '.join(f'{th[k]:.3f}' for k in range(1, 6))}; least root on [5,{K}) = "
          f"{theta0:.4f} (row {kmin}); chi = {chi:.4f}; Phi = {Phi:.4f}; C+ = {Cp:.3f} (row {zarg}); "
          f"theta0(K-5) - ln Phi = {theta0 * (K - 5) - math.log(Phi):.2f}; -ln h = {-math.log(h):.2f}; "
          f"exposure above A/2: {p[half + 1:].sum():.2f}")
    if A == 84:
        for (lo, hi) in ((5, 29), (5, 37), (5, 42), (1, 42)):
            best = max(((-max(math.log(M(T[k], k, s)) for k in range(lo, hi + 1)), s) for s in np.arange(0.002, 0.7, 0.002)))
            eps0, s = best
            m0 = {}
            for delta in (0.5, 0.2, 0.1):
                ok = lambda m: delta * m * eps0 >= (1 - delta) * math.log(m * hi + 1)
                b = 1
                while not ok(b): b *= 2
                a = b // 2                       # least m with (S): the difference of the two sides is convex in m
                while b - a > 1:
                    c = (a + b) // 2
                    a, b = (a, c) if ok(c) else (c, b)
                m0[delta] = b
            print(f"      block {lo}..{hi}: best theta0 = {s:.3f}, margin eps0 = {eps0:.4f}; m0(0.5, 0.2, 0.1) = "
                  f"{m0[0.5]}, {m0[0.2]}, {m0[0.1]}")

# the smallest case of claim Q
P = np.array([[0, .75, 0], [.25, 0, .75], [0, .25, .75]])
w, v = np.linalg.eig(P.T); i = int(np.argmax(w.real)); p = np.abs(v[:, i].real); p /= p.sum()
h = 1 - w[i].real
theta0 = math.log(3); K, k0 = 3, 0
Phi = p[2] * 0.25 * math.exp(theta0 * (K - 2)); Cp = 0.75 + 0.25 * math.exp(theta0)
wq = p[0] * math.exp(-theta0) + p[1] * math.exp(-2 * theta0)
print(f"smallest case of Q: Phi = {Phi:.3f} (= 3/4 p3), C+ = {Cp:.2f}, (Phi/27)/(1-w) = {Phi / 27 / (1 - wq):.4f}, exact h = {h:.4f}")
