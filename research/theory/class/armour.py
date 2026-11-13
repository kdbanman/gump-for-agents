"""armour.py -- armoured live sets (immortal walls) of a vessel, by exact peeling.

Armour lemma (class.md 1.6): in a vessel V (outside dead forever), let W be a set of cells each of which has
>= s neighbours inside W and <= c-1 neighbours in V (s = least survival count, b-1 for the capped threshold;
c = cap).  If W is all alive at some time, it is alive forever: n >= s always, n <= c-1 always.
The largest such W is the s-core of the subgraph induced on {cells of V-degree <= c-1}.

    python3 armour.py LATTICE [b] [R]     hull vessel of "radius" R layers: least cap c with a nonempty armoured set
"""
import sys
import numpy as np
import lattices as LT, theory as TH, vessel as VS


def core(V, s, c):
    deg = np.array([sum(1 for q in lst if q >= 0) for lst in V.nbr])
    inW = deg <= c - 1
    nb = [np.array([q for q in lst if q >= 0], dtype=np.int64) for lst in V.nbr]
    changed = True
    while changed:
        changed = False
        for i in np.nonzero(inW)[0]:
            if inW[nb[i]].sum() < s:
                inW[i] = False
                changed = True
    return inW, deg


if __name__ == "__main__":
    lat = sys.argv[1]
    L = LT.get(lat)
    b = int(sys.argv[2]) if len(sys.argv) > 2 else TH.confinement(L)["b_min"]
    R = int(sys.argv[3]) if len(sys.argv) > 3 else (8 if L.dim == 3 else 12)
    V = VS.hull(L, b, R)
    u = TH.sealed_rays(L, b)[0]
    cs = TH.counts(L, u)
    Kf = max(c[0] + c[1] for c in cs)
    out = []
    for c in range(b + 1, L.K + 2):
        W, deg = core(V, b - 1, c)
        out.append((c, int(W.sum())))
    first = next((c for c, n in out if n > 0), None)
    print(f"{lat:9s} b={b} hull R={R} N={V.N} K_f={Kf}: least cap with armour c_arm={first}; "
          f"sizes {[(c, n) for c, n in out if n > 0][:4]}; min V-degree {int(deg.min())}")
