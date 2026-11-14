"""structure.py -- exact (no dynamics) facts behind PREDICTIONS.md: sealing of the strips and hulls used, layer
structure of the wall, forward counts (Theorem C, C1), finite sealed sets at a wall by peeling, armoured cores
(Theorem E) in strips, hulls and boxes.

    python3 structure.py 2d          kagome4 (b = 2), kagome8 and hex9 (b = 4)
    python3 structure.py bond10      bond10 at b = 3: box degrees, armoured cores of boxes and columns
"""
import itertools, sys
import numpy as np
import fu

# wall directions: (lattice, b, u, g, sealed residues of C (inside u.p <= C) mod m, m)
WALLS = {
    "kagome4": (2, [((1, 0), (0, 2))]),
    "kagome8": (4, [((1, 0), (0, 2)), ((2, 1), (2, -4))]),
    "hex9": (4, [((2, 1), (1, -2))]),
}
HULLDIRS = {
    "kagome4": ([(1, 0), (0, 1), (1, 1)], 2, {0}),
    "kagome8": ([(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)], 2, {0}),
    "hex9": ([(1, -1), (2, 1), (1, 2)], 3, {0, 2}),
}


def sealed_C(name, u, C):
    """is {u.p <= C} sealed, by direct count over the cells just outside."""
    L = fu.lattice(name)
    b = WALLS[name][0]
    C = C % HULLDIRS[name][1]          # sealing is periodic in C (lattice translations); keeps the plane in the window
    inside = lambda p: p[0] * u[0] + p[1] * u[1] <= C
    cand = [p for p in itertools.product(range(-12, 13), repeat=2)]
    return fu.outside_count(L, inside, cand) <= b - 1


def strip_for(name, u, g, depth, n):
    """strip whose two walls are sealed: lo..hi chosen at sealed positions for u and -u."""
    dirs, m, res = HULLDIRS[name]
    hi = next(C for C in range(depth, depth + 6) if sealed_C(name, u, C))
    mu = (-u[0], -u[1])
    lo = -next(C for C in range(0, 6) if sealed_C(name, mu, C))
    # the first layers inside that hold cells
    V = fu.strip2d(fu.lattice(name), u, lo, hi, g, n)
    return V


def hull_of(name, pts):
    dirs, m, res = HULLDIRS[name]
    allu = dirs + [(-a, -b) for a, b in dirs]
    bounds = []
    for u in allu:
        s = max(u[0] * p[0] + u[1] * p[1] for p in pts)
        C = s
        while not sealed_C(name, u, C):
            C += 1
        bounds.append((u, C))
    return bounds


def hull_vessel(name, R):
    """hull of the seed hexagon |p0|, |p1|, |p0 + p1| <= 2R (cells of the lattice in it)."""
    L = fu.lattice(name)
    seed = [p for p in itertools.product(range(-2 * R, 2 * R + 1), repeat=2)
            if L.typ(p) is not None and abs(p[0]) <= 2 * R and abs(p[1]) <= 2 * R and abs(p[0] + p[1]) <= 2 * R]
    bounds = hull_of(name, seed)
    pred = lambda p: all(u[0] * p[0] + u[1] * p[1] <= C for u, C in bounds)
    return fu.region(L, pred, 4 * R + 6), bounds


def forward_min(V, v, cells=None):
    """min over cells of #{in-vessel neighbours q with v.(q - p) > 0}, with q - p the lattice offset (no wrap)."""
    L = V.L
    best = 99
    idx = range(V.N) if cells is None else cells
    for i in idx:
        offs = L.offsets[L.typ(tuple(V.cells[i]))]
        k = sum(1 for j, q in enumerate(V.nbr[i]) if q < V.N and np.dot(v, offs[j]) > 1e-9)
        best = min(best, k)
    return best


def two_d():
    rng = np.random.default_rng(3)
    for name, (b, walls) in WALLS.items():
        L = fu.lattice(name)
        print(f"===== {name}, b = {b}, K = {L.K}, types {L.ntypes}")
        dirs, m, res = HULLDIRS[name]
        for u in dirs + [(-a, -c) for a, c in dirs]:
            sealedC = [C for C in range(m) if sealed_C(name, u, C)]
            print(f"   u = {u}: sealed positions C mod {m} = {sealedC} (direct count)")
        # generic forward count on a torus (C1 on the full lattice)
        T = fu.torus(L, 12 if name != "hex9" else 12)
        fw = max(forward_min(T, rng.normal(size=2)) for _ in range(20))
        print(f"   full lattice: best min forward count over 20 generic v = {fw} (b = {b}): "
              f"{'no finite sealed set (C1)' if fw >= b else 'C1 gives no certificate'}")
        for u, g in walls:
            V = strip_for(name, u, g, 24, 30)
            h = V.h
            lo, hi = int(h.min()), int(h.max())
            layers = sorted(set(h.tolist()))
            top = layers[-4:][::-1]
            desc = []
            for hv in top:
                idx = np.nonzero(h == hv)[0]
                types = sorted({L.typ(tuple(V.cells[i])) for i in idx})
                desc.append(f"h={hv}: {len(idx) // 30} cells/period, types {types}, degree {sorted(set(V.degrees()[idx].tolist()))}")
            print(f"   strip u = {u}, g = {g}: layers h = {lo}..{hi}; top layers: " + "; ".join(desc))
            # half-plane forward count (top wall only: cells in the upper half)
            up = [i for i in range(V.N) if h[i] >= (lo + hi) / 2]
            gv = np.array(g, float)
            # u as a vector in coordinate space dual: use the gradient direction of h, i.e. u itself
            uv = np.array(u, float)
            best = max(forward_min(V, s * gv - e * uv, up) for s in (1, -1) for e in (1e-3, -1e-3))
            print(f"      half-plane at the top wall: best min forward count (v = +-g +- eps u) = {best}: "
                  f"{'no finite sealed set at a wall (C1)' if best >= b else 'no certificate'}")
            # peeling search for finite sealed sets near the top wall and for a transverse cut
            wg = V.P @ np.array(g)
            per = 30 * (g[0] ** 2 + g[1] ** 2)
            win = (wg >= per // 4) & (wg <= 3 * per // 4)
            for d in (1, 2, 3, 4, 6, 8):
                W = np.nonzero(win & (h >= hi - d))[0]
                s = fu.sealed_subset(V, W, b)
                print(f"      finite window of the top {d + 1} layers, length {per // 2 // (g[0] ** 2 + g[1] ** 2)} periods: "
                      f"largest sealed subset {len(s)} cells")
                if s:
                    break
            gg = g[0] ** 2 + g[1] ** 2
            for wl in range(1, 16):
                W = np.nonzero((wg >= per // 4) & (wg < per // 4 + wl * gg))[0]
                if fu.sealed_subset(V, W, b):
                    print(f"      shortest full-width window containing a sealed set (a transverse cut): {wl} periods of g")
                    break
            W = np.nonzero(win)[0]
            s = fu.sealed_subset(V, W, b)
            ws = (V.P[list(s)] @ np.array(g)) if s else []
            print(f"      whole width ({hi - lo + 1} values of h) in the window: largest sealed subset {len(s)} cells"
                  + (f", spans h {int(h[list(s)].min())}..{int(h[list(s)].max())}, extent along g "
                     f"{(max(ws) - min(ws)) / (g[0] ** 2 + g[1] ** 2):.1f} periods" if s else ""))
            for c in range(b + 1, L.K + 2):
                core = fu.armoured_core(V, b, c)
                print(f"      strip cap c = {c}: armoured core {len(core)} cells" +
                      (f" (layers {sorted(set(h[list(core)].tolist()))[:6]})" if core else ""))
        for R in (3, 5):
            Hv, bounds = hull_vessel(name, R)
            deg = Hv.degrees()
            line = f"   hull of the seed hexagon R = {R}: {Hv.N} cells, {len(bounds)} sealed sides, degrees " \
                   f"{ {int(d): int((deg == d).sum()) for d in np.unique(deg)} }; armoured core by cap: "
            line += ", ".join(f"c={c}: {len(fu.armoured_core(Hv, b, c))}" for c in range(b + 1, L.K + 2))
            print(line)


def box(L, n):
    return fu.region(L, lambda q: all(1 <= a <= 2 * n + 1 for a in q), 2 * n + 2)


def bond10():
    L = fu.lattice("bond10")
    b = 3
    for n in (2, 3, 4, 5):
        V = box(L, n)
        deg = V.degrees()
        print(f"bond10 box {n}^3 cubes (walls at x = 1, {2 * n + 1}): {V.N} cells; degrees "
              f"{ {int(d): int((deg == d).sum()) for d in np.unique(deg)} }; armoured core: "
              + ", ".join(f"c={c}: {len(fu.armoured_core(V, b, c))}" for c in (4, 5, 6, 7)))
    # sealing of the box walls, direct count
    for C in (1, 2, 3):
        inside = lambda p: p[0] >= C
        cnt = fu.outside_count(L, inside, list(itertools.product(range(C - 4, C + 1), range(-4, 5), range(-4, 5))))
        print(f"   half-space x >= {C}: most neighbours inside of a cell outside = {cnt} (sealed for b = 3 iff <= 2)")
    V = box(L, 4)
    P = V.P
    for x in (1, 2, 3):
        idx = np.nonzero(P[:, 0] == x)[0]
        sub = [i for i in idx if all(3 <= P[i, a] <= 7 for a in (1, 2))]
        print(f"   box 4^3, layer x = {x}: {len(idx)} cells; interior-of-wall cells have degree "
              f"{sorted(set(V.degrees()[sub].tolist()))}, in-layer neighbours "
              f"{sorted(set(int(sum(1 for q in V.nbr[i] if q < V.N and P[q, 0] == x)) for i in sub))}")
    # finite dead sealed sets in a box: the walls (sheet + layer beneath), and smaller ones?
    for n in (3, 4):
        V = box(L, n); P = V.P
        for name, W in (("sheet x=1", P[:, 0] == 1), ("sheet+beneath x<=2", P[:, 0] <= 2),
                        ("x<=3", P[:, 0] <= 3), ("edge x<=2 and y<=2", (P[:, 0] <= 2) & (P[:, 1] <= 2)),
                        ("corner x,y,z<=2", (P[:, 0] <= 2) & (P[:, 1] <= 2) & (P[:, 2] <= 2)),
                        ("two sheets x<=2 or y<=2", (P[:, 0] <= 2) | (P[:, 1] <= 2))):
            s = fu.sealed_subset(V, np.nonzero(W)[0], b)
            print(f"   box {n}^3: largest sealed subset of [{name}] ({int(W.sum())} cells): {len(s)}")


if __name__ == "__main__":
    {"2d": two_d, "bond10": bond10}[sys.argv[1]]()
