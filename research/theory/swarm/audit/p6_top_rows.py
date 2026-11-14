#!/usr/bin/env python3
"""Hypothesis R+ of Theorem Q (journal 23.2) at the top rows: overcrowded faces collapse.

  python3 p6_top_rows.py            (about 20 s, one core)

R+ asks, for EVERY visited row z >= K, that  C_z := M_z(theta0) e^{-theta0 (z-K)} = E_z[ e^{-theta0 (Z'-K)} ]  be at
most a constant C+.  A face cell with all six in-face neighbours alive has n >= 6 and is dead next (the "doomed"
cell of journal 1.1), whatever lies beneath.  So:

 (i)  rim-free face (a {111} slab, periodic in the plane): a full face is empty one generation later, with
      certainty; from A - j live cells the next population is at most 7 j.  Checked here on a periodic slab
      (3 layers, 27 cells a layer) over random states beneath.  Hence C_A = e^{theta0 K}, and
      C_{A-j} >= e^{theta0 (K - 7j)} whenever that row is visited.
 (ii) hull face, R = 7 (A = 30): the next population from a full or nearly full face over random states of
      the rest of the hull, and the resulting C_z with theta0 = 0.41, K = 11.
 (iii) the exhaustive vessel of p1 (22 cells, face of 11): the full row is visited at every time t >= 1 of the
      exact pooled law, not only in the initial soup.
"""
import sys, math, time
import numpy as np
from p0_lib import DIAGS, Vessel, hull, hull_cells


def periodic_slab(n, layers):
    """Cells with s = x+y+z in `layers`, modulo the in-plane lattice spanned by (2n,-2n,0), (0,2n,-2n)."""
    def wrap(p):
        x, y, z = p
        a = x // (2 * n); x -= 2 * n * a; y += 2 * n * a
        b = y // (2 * n); y -= 2 * n * b; z += 2 * n * b
        return (x, y, z)
    cells = []
    for s in layers:
        for x in range(2 * n):
            for y in range(2 * n):
                z = s - x - y
                if (x % 2) + (y % 2) + (z % 2) == 1:
                    cells.append((x, y, z))
    return Vessel(cells, wrap=wrap)


def main():
    rng = np.random.default_rng(5)
    theta0, K = 0.41, 11
    # (i) rim-free
    V = periodic_slab(3, (1, 3, 5))
    top = [i for i, p in enumerate(V.cells) if sum(p) == 5]; A = len(top); ts = set(top)
    assert all(sum(q in ts for q in V.nlist[i]) == 6 and len(V.nlist[i]) == 9 for i in top)
    S = 20000
    print(f"(i) periodic slab, 3 layers of {A} cells; top face; {S} random states beneath for each j")
    for j in (0, 1, 2, 3):
        X = (rng.random((S, V.N)) < rng.choice([0.2, 0.5, 0.8], size=(S, 1))).astype(np.int8)
        X[:, top] = 1
        for r in range(S if j else 0):
            X[r, rng.choice(top, size=j, replace=False)] = 0
        zn = V.step(X)[:, top].sum(1)
        print(f"    from A - {j} = {A - j} live cells: next population max {int(zn.max())} (bound 7j = {7 * j}), mean {zn.mean():.2f}")
        assert zn.max() <= 7 * j
    # (ii) hull R = 7
    V = hull(7); F = V.layer((1, 1, 1), 7); A = len(F)
    print(f"(ii) hull R=7, face of {A} cells, rest of the hull at random (densities 0.2, 0.4, 0.6); theta0 = {theta0}, K = {K}")
    for j in (0, 1, 2, 4, 8):
        X = (rng.random((S, V.N)) < rng.choice([0.2, 0.4, 0.6], size=(S, 1))).astype(np.int8)
        X[:, F] = 1
        for r in range(S if j else 0):
            X[r, rng.choice(F, size=j, replace=False)] = 0
        zn = V.step(X)[:, F].sum(1)
        Cz = float(np.mean(np.exp(-theta0 * (zn - K))))
        print(f"    from {A - j} live cells: next population mean {zn.mean():.2f}, min {int(zn.min())}, max {int(zn.max())}; "
              f"P(next < K) = {(zn < K).mean():.3f}; C_z = E e^(-theta0 (Z'-K)) = {Cz:.2f}   (e^(theta0 K) = {math.exp(theta0 * K):.1f})")
    # (iii) the exhaustive vessel
    C = dict(zip(DIAGS, (1, 3, 3, 5, 5, 3, 3, 1)))
    V = Vessel(hull_cells(C)); N = V.N; Sx = 1 << N
    pw = (1 << np.arange(N)).astype(np.int64)
    succ = np.empty(Sx, np.int64)
    for a in range(0, Sx, 1 << 18):
        idx = np.arange(a, min(Sx, a + (1 << 18)), dtype=np.int64)
        X = ((idx[:, None] >> np.arange(N)) & 1).astype(np.int8)
        succ[a:a + len(idx)] = V.step(X).astype(np.int64) @ pw
    face = V.layer((1, 1, 1), 1); fm = sum(1 << i for i in face)
    idx = np.arange(Sx, dtype=np.int64)
    full = (idx & fm) == fm
    m = np.ones(Sx)
    print(f"(iii) exhaustive vessel ({N} cells, face of {len(face)}): number of the 2^{N} soups whose face is full at time t")
    out = []
    for t in range(0, 9):
        out.append(int(m[full].sum()))
        m = np.bincount(succ, weights=m, minlength=Sx)
    print("    t = 0..8:", out)
    nxt = np.zeros(Sx, np.int64)
    for i in face:
        nxt += (succ >> i) & 1
    print(f"    from a full face the next population is at most {int(nxt[full].max())}, and 0 in "
          f"{int((nxt[full] == 0).sum())} of {int(full.sum())} states")


if __name__ == "__main__":
    t = time.time(); main(); print(f"({time.time() - t:.0f} s)")
