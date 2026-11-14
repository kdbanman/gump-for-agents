"""confine.py -- brute-force check of Theorem A on a torus: a soup inside the confinement polytope of the sealed
rays never leaves it, and (converse) for the cheapest unsealed ray a half-space pattern does put a live cell outside.

    python3 confine.py        ->  ALL OK
"""
import numpy as np
import lattices as LT, theory as TH, vessel as VS

ok_all = True
for lat, b, c, n, R in (("vn", 2, 3, 40, 8), ("cross2", 3, 5, 40, 8), ("cross3", 4, 9, 48, 8), ("moore", 4, 7, 40, 8),
                        ("gump", 4, 7, 12, 4), ("fcc", 4, 6, 22, 3), ("bcc8", 3, 5, 14, 4), ("sc6", 2, 3, 14, 4),
                        ("cross3d2", 3, 5, 16, 4), ("bond10", 4, 7, 12, 4), ("sc18", 6, 10, 14, 4)):
    L = LT.get(lat)
    B, S = TH.capped(b, c, L.K)
    V = VS.torus(L, n)
    U = TH.sealed_rays(L, b)
    gs = {u: TH.layer_info(L, u)["g"] for u in U}
    cells = np.array(V.cells)
    centre = cells.mean(axis=0).round().astype(int)
    rel = cells - centre
    inside = np.ones(V.N, bool)
    for u in U:
        inside &= (rel @ np.array(u)) <= R * gs[u]
    # the polytope must not touch itself around the torus (an FCC torus is a skew cell): every neighbour of an inside
    # cell must sit at its true offset
    for i in np.nonzero(inside)[0]:
        for o, q in zip(L.offsets[L.typ(V.cells[i])], V.nbr[i]):
            assert tuple(cells[q]) == tuple(cells[i] + np.array(o)), (lat, "hull wraps around the torus: enlarge n")
    rng = np.random.default_rng(1)
    x = ((rng.random(V.N) < 0.5) & inside).astype(np.int8)
    leaked = 0
    for t in range(200):
        x = VS.numpy_step(V, x, B, S)
        leaked += int(x[~inside].sum())
    # converse: an unsealed ray with the smallest count, half-space fully alive below, check a birth above
    R_all = TH.rays(L)
    bad = sorted((TH.cmax(L, u), u) for u in R_all if TH.cmax(L, u) >= b)
    conv = "n/a"
    if bad:
        cm, u = bad[0]
        h = rel @ np.array(u)
        best = False
        for dens in (1.0, 0.7, 0.5):
            for s in range(20):
                y = ((h <= 0) & (h > -40 * max(1, abs(np.array(u)).max())) & (rng.random(V.N) < dens)).astype(np.int8)
                z = VS.numpy_step(V, y, B, S)
                if z[(h > 0) & (h < 20)].sum() > 0:
                    best = True
                    break
            if best:
                break
        conv = f"unsealed ray {u} (count {cm}): birth outside {'found' if best else 'NOT found'}"
        ok_all &= best
    ok = leaked == 0 and inside.sum() < V.N and x.sum() >= 0
    ok_all &= ok
    print(f"{'OK ' if ok else 'FAIL'} {lat:9s} {TH.rule_name(B, S):16s} hull of {len(U)} rays, {int(inside.sum())} cells in a torus of {V.N}: "
          f"live cells outside over 200 generations: {leaked}; {conv}")
print("ALL OK" if ok_all else "SOME FAILED")
