#!/usr/bin/env python3
"""Spot recomputation of research/blast/rigour's exactly solved one-layer dice surrogate, with a dense code written
here (graphs from this directory's geom.py, i.e. from reference/oracle.py's offsets).

The chain: the cells of one face layer; each generation every cell counts its live in-layer neighbours k and draws
b = Bin(m1, r1) + Bin(m2, r2) (m1, m2 = its neighbours one and two layers beneath inside the vessel: 2 and 1 on a
wrapped face); B45/S345 on n = k + b, all cells at once; the empty face absorbs.  tau = 1 / (1 - lambda) from the
quasi-stationary law.  "Bust share" (their definition, rigour/qsd.c): the share of the quasi-stationary death flux
whose last 6 transitions, the death included, contain a fall of at least ceil(A/2) cells in one generation.

    python3 research/audit/blast/dice.py            # the rows below against rigour's printed values (2 min, 1 GB)
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom


def face_graph(kind, *a):
    if kind == 'torus':
        cells, nb, faces, _ = geom.slab(*a)
    else:
        cells, nb, faces, _ = geom.hull(*a)
    lay = [set(l) for l in faces[0][:3]]
    f0 = faces[0][0]; loc = {c: i for i, c in enumerate(f0)}
    N = [[loc[j] for j in nb[c] if j in lay[0]] for c in f0]            # with multiplicity
    m1 = [sum(j in lay[1] for j in nb[c]) for c in f0]
    m2 = [sum(j in lay[2] for j in nb[c]) for c in f0]
    return N, m1, m2


def solve(kind, a, r1=0.44, r2=0.42, K=6):
    N, m1, m2 = face_graph(kind, *a)
    A = len(N); S = 1 << A
    st = (np.arange(S)[:, None] >> np.arange(A)[None, :]) & 1                 # S x A
    pop = st.sum(1)
    alive = np.zeros((S, A))                                                  # P(cell alive next | state)
    for i in range(A):
        k = np.zeros(S, int)
        for j in N[i]:
            k += st[:, j]
        pb = np.zeros(4)                                                      # law of b
        for c1 in range(m1[i] + 1):
            for c2 in range(m2[i] + 1):
                w = (r1 ** c1 * (1 - r1) ** (m1[i] - c1) * (2 if (m1[i] == 2 and c1 == 1) else 1)
                     * r2 ** c2 * (1 - r2) ** (m2[i] - c2))
                pb[c1 + c2] += w
        assert abs(pb.sum() - 1) < 1e-12
        for b in range(4):
            n = k + b
            alive[:, i] += pb[b] * np.where(st[:, i] == 1, (n >= 3) & (n <= 5), (n >= 4) & (n <= 5))
    P = np.ones((S, 1))
    for i in range(A):                                                        # next-state bit i is the new high bit
        P = np.concatenate([P * (1 - alive[:, i:i + 1]), P * alive[:, i:i + 1]], axis=1)
    assert np.allclose(P.sum(1), 1)
    d = P[:, 0].copy()                                                        # to the empty face in one step
    Q = P[1:, 1:]
    mu = np.ones(S - 1) / (S - 1)
    for it in range(20000):
        v = mu @ Q; lam = v.sum(); v /= lam
        if np.abs(v - mu).max() < 1e-15: break
        mu = v
    h = 1 - lam
    full = np.r_[0.0, mu]
    assert abs((full * d).sum() - h) < 1e-12
    # the tilt identity and its two bounds
    E = -np.log(np.maximum(d, 1e-300))
    xs, ws = np.polynomial.legendre.leggauss(48); xs = (xs + 1) / 2; ws = ws / 2
    Es = []
    for s in xs:
        w = full * np.exp(-s * E); Es.append((w * E).sum() / w.sum())
    tilt = float((np.array(Es) * ws).sum())
    E0 = (full * E).sum(); w1 = full * d; E1 = (w1 * E).sum() / w1.sum()
    # bust share
    half = (A + 1) // 2
    ok = (pop[:, None] - pop[None, :]) < half                                 # transitions without a half-face fall
    Pn = P * ok
    v = full.copy()
    for j in range(1, K + 1):
        nv = v @ Pn
        Dnb = nv[0]; nv[0] = 0; v = nv
    bust = 1 - Dnb / (lam ** (K - 1) * h)
    return dict(A=A, lntau=-np.log(h), h=h, bust=bust, tilt=tilt, E0=E0, E1=E1, dens=(full * pop).sum() / A)


ROWS = [('hull', (3,), 2.4837157463, 0.0170), ('torus', (1, 1, 3), 2.6946266059, 0.9369), ('torus', (1, 0, 3), 3.3935247191, None),
        ('torus', (2, 0, 2), 3.9818365883, 0.5675), ('torus', (1, 1, 4), 3.7118338988, 0.7909), ('torus', (1, 0, 4), 4.1330124063, None)]

if __name__ == '__main__':
    print('face              A   ln tau (here)    ln tau (rigour)  bust share (here)  (rigour)   tilt integral   <E>_1 <= ln tau <= <E>_0')
    for kind, a, lt, bs in ROWS:
        r = solve(kind, a)
        print(f'{kind:5s} {str(a):10s} {r["A"]:3d}   {r["lntau"]:.10f}   {lt:.10f}     {r["bust"]:.4f}            '
              f'{"%.4f" % bs if bs is not None else "  -   "}     {r["tilt"]:.10f}   {r["E1"]:.3f} <= {r["lntau"]:.3f} <= {r["E0"]:.3f}', flush=True)
