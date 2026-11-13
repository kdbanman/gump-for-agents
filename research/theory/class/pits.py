"""pits.py -- finite sealed sets attached to a face ("pits"), and in thin slabs, by explicit search.

A set W is sealed (for minimum birth count b) if each of its cells has <= b-1 neighbours in the vessel outside W.
The largest sealed subset of a finite patch P is found by peeling (remove cells with >= b neighbours outside the
current set until none is left).  If it is nonempty it is an explicit finite sealed set; if it is empty there is
no sealed set inside that patch (not a proof for all patches -- the certificate of theory.slab_certificate is).

    python3 pits.py LATTICE [b]      half-space vessel (a thick slab, patch away from the far side)
    python3 pits.py LATTICE b M      slab of M layers (patch spans the slab)
"""
import sys
import numpy as np
import lattices as LT, theory as TH, vessel as VS


def patch_search(lat, b, m, n, depth, u=None, margin=None):
    L = LT.get(lat)
    if u is None:
        u = TH.sealed_rays(L, b)[0]
    V = VS.slab(L, tuple(u), m, n)
    g, lo = V.info["g"], V.info["lo"]
    hs = np.array([(TH.dot(u, p) - lo) // g for p in V.cells])
    # in-plane window: keep cells whose graph distance from a central boundary cell is small enough not to wrap
    start = [i for i in range(V.N) if hs[i] == 0][0]
    dist = np.full(V.N, -1)
    dist[start] = 0
    frontier = [start]
    while frontier:
        nxt = []
        for i in frontier:
            for q in V.nbr[i]:
                if q >= 0 and dist[q] < 0:
                    dist[q] = dist[i] + 1
                    nxt.append(q)
        frontier = nxt
    rad = margin if margin is not None else int(dist.max() * 0.45)
    patch = (dist <= rad) & (hs < depth)
    K = VS.max_sealed(V, patch, b)
    return V, patch, K, hs


if __name__ == "__main__":
    lat = sys.argv[1]
    L = LT.get(lat)
    b = int(sys.argv[2]) if len(sys.argv) > 2 else TH.confinement(L)["b_min"]
    u = TH.sealed_rays(L, b)[0]
    if len(sys.argv) > 3:
        m = int(sys.argv[3])
        n = 14 if L.dim == 3 else 40
        V, patch, K, hs = patch_search(lat, b, m, n, depth=m)
        what = f"slab of {m} layers"
    else:
        m = 10
        n = 12 if L.dim == 3 else 40
        V, patch, K, hs = patch_search(lat, b, m, n, depth=m - 4)
        what = "half-space (10-layer slab, patch confined to the 6 layers nearest one face)"
    cert = TH.slab_certificate(L, u, b, 12 if len(sys.argv) <= 3 else int(sys.argv[3]))
    print(f"{lat} b={b} u={u} {what}: patch {int(patch.sum())} cells -> largest sealed subset {int(K.sum())} cells"
          f" (layers used: {sorted(set(hs[K].tolist()))}); certificate count {cert} (>= b means provably none)")
