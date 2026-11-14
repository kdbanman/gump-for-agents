"""others.py -- the two lattices whose table row changes under position-aware sealing (PREDICTION-repaired.md).

    python3 others.py kagome [c]         kagome (4 nearest), b = 2: confinement, torus, strips, hexagons
    python3 others.py bond10             bond10, b = 3: confinement, torus for c = 4..8
    python3 others.py bond10 slab C n gens     slab with odd walls, n x n cubes, cap C
    python3 others.py bond10 life C n cap      box of n^3 cubes with odd walls
    python3 others.py bond10-endings n T       bond10 at b = 4 in class.md's {111} slab: which dead sealed set comes first
"""
import itertools, json, sys
import numpy as np
import aud


def kag_typ(p):
    a, b = p[0] % 2, p[1] % 2
    return None if (a == 0 and b == 0) else {(1, 0): 0, (0, 1): 1, (1, 1): 2}[(a, b)]


KAG = aud.Lat("kagome4", 2, kag_typ, [[(0, 1), (0, -1), (1, -1), (-1, 1)],     # midpoint of an e1 edge
                                      [(1, 0), (-1, 0), (1, -1), (-1, 1)],     # e2 edge
                                      [(1, 0), (-1, 0), (0, 1), (0, -1)]])     # e1 - e2 edge


def kag_check():
    """offsets = the 4 nearest neighbours (squared length x^2 + xy + y^2 = 1 in units of half a lattice step)."""
    ok = True
    for rep in ((1, 0), (0, 1), (1, 1)):
        t = kag_typ(rep)
        near = {o for o in itertools.product(range(-2, 3), repeat=2)
                if o[0] ** 2 + o[0] * o[1] + o[1] ** 2 == 1 and kag_typ((rep[0] + o[0], rep[1] + o[1])) is not None}
        ok &= near == set(KAG.offsets[t])
    return ok


def kag_strip(m, n):
    """rows x = 0 .. 2m (both walls sparse rows at even x), periodic in y with period 2n."""
    cells = [(x, y) for x in range(0, 2 * m + 1) for y in range(2 * n) if kag_typ((x, y)) is not None]
    V = aud.Vessel(KAG, cells, lambda p: (p[0], p[1] % (2 * n)) if 0 <= p[0] <= 2 * m else None)
    return V, np.array([p[0] for p in cells])


def kag_hex(R):
    pred = lambda p: abs(p[0]) <= 2 * R and abs(p[1]) <= 2 * R and abs(p[0] + p[1]) <= 2 * R
    return aud.region(KAG, pred, 2 * R)


def kagome(c=3):
    B, S = aud.capped(2, c, 4)
    print(f"kagome4 offsets are the 4 nearest neighbours: {kag_check()};  rule B{B}/S{S}")
    # confinement in free space
    H = 64
    V = aud.torus(KAG, H)
    P = np.array(V.cells)
    rng = np.random.default_rng(1)
    dirs = np.array([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)])
    gen = np.array([(2, 1), (-2, -1), (1, 2), (-1, -2), (1, -1), (-1, 1), (3, 1), (1, 3)])
    for lo, hi in ((24, 40), (25, 39), (27, 37)):
        seed = ((P >= lo) & (P <= hi)).all(1)
        st = np.zeros((64, V.N), np.uint8)
        st[:, seed] = rng.random((64, int(seed.sum()))) < 0.5
        # sealed position: the plane u.p <= C with C even; push each support value up to the next even number
        sup = np.array([(P[st[r] == 1] @ dirs.T).max(0) for r in range(64)])
        sup_even = sup + (sup % 2 != 0)
        gsup = np.array([(P[st[r] == 1] @ gen.T).max(0) for r in range(64)])
        out_hex = out_tight = out_gen = 0
        x = aud.pack(st)
        for t in range(300):
            x = aud.step(V, x, B, S)
            u = aud.unpack(x)
            for r in range(64):
                live = P[u[r] == 1]
                if len(live) == 0:
                    continue
                s = (live @ dirs.T).max(0)
                out_hex += int((s > sup_even[r]).any()); out_tight += int((s > sup[r]).any())
                out_gen += int(((live @ gen.T).max(0) > gsup[r]).any())
        print(f"   free space, seed square [{lo},{hi}]^2, 64 soups x 300 generations: soup-generations outside the "
              f"hexagon at sealed positions: {out_hex}; outside the tight hexagon: {out_tight}; beyond the seed's "
              f"support in 8 other directions: {out_gen}; alive at the end {int((aud.unpack(x).sum(1) > 0).sum())}")
    # torus
    V = aud.torus(KAG, 128)
    print(f"   torus 64 x 64 periods ({V.N} cells): running / density / activity at t = 1024 and 4096")
    for p in (0.2, 0.35, 0.5, 0.65):
        o = aud.bulk_run(V, B, S, p, [1024, 4096], seed=int(100 * p))
        print(f"      p0={p}: {int(o[0, 0])}/64 rho={o[0, 1]:.4f} act={o[0, 2]:.4f} | {int(o[1, 0])}/64 rho={o[1, 1]:.4f} act={o[1, 2]:.4f}")


def kag_slab(n, gens, c=3, m=8, watch="two", p=0.45):
    B, S = aud.capped(2, c, 4)
    V, xs = kag_strip(m, n)
    top = 2 * m
    if watch == "two":
        groups = [np.nonzero(xs >= top - 1)[0], np.nonzero(xs <= 1)[0]]
    else:
        groups = [np.nonzero(xs == top)[0], np.nonzero(xs == 0)[0]]
    lab = np.where((xs == 0) | (xs == top), 1, np.where((xs == 1) | (xs == top - 1), 2, 0))
    r = aud.face_run(V, B, S, groups, lab, p, gens)
    ts = aud.tau_stats(r, 2)
    print(json.dumps(dict(lattice="kagome4", rule=f"B{B}/S{S}", n=n, N=V.N, rows=2 * m + 1, watch=watch, gens=gens,
                          deaths=r["deaths"], early=r["early"], settle=r["settle"], early_settle=r["early_settle"],
                          dens=[round(float(d), 4) for d in r["dens"]],
                          lntau=None if ts is None else round(ts["lntau"], 3),
                          err=None if ts is None else round(ts["err"], 3), cv=None if ts is None else round(ts["cv"], 3))))


def kag_life(R, cap, c=3, p=0.45):
    B, S = aud.capped(2, c, 4)
    V = kag_hex(R)
    lf, pop, kind = aud.life_run(V, B, S, p, cap)
    L = np.where(kind > 0, lf, cap + 1)
    print(json.dumps(dict(lattice="kagome4", rule=f"B{B}/S{S}", R=R, N=V.N, finished=int((kind > 0).sum()),
                          median=float(np.median(L)), q25=float(np.percentile(L, 25)), q75=float(np.percentile(L, 75)),
                          final_density=round(float(pop[kind > 0].mean() / V.N), 4) if (kind > 0).any() else None,
                          empty=int(((pop == 0) & (kind > 0)).sum()))))


def bond10(args):
    L = aud.lattice("bond10")
    if not args:
        import face12e
        face12e.confine(names=("bond10",), rules={"bond10": ([3, 4], [2, 3, 4])})
        V = aud.torus(L, 20)
        for c in (4, 5, 6, 7, 8):
            B, S = aud.capped(3, c, 10)
            for p in (0.3, 0.5):
                o = aud.bulk_run(V, B, S, p, [1024, 4096], seed=c)
                print(f"bond10 b=3 c={c} B{B}/S{S} torus 10^3 cubes p0={p}: {int(o[0, 0])}/64 rho={o[0, 1]:.4f} "
                      f"act={o[0, 2]:.4f} | {int(o[1, 0])}/64 rho={o[1, 1]:.4f} act={o[1, 2]:.4f} (all: {o[1, 3]:.4f})")
        return
    c, n = int(args[1]), int(args[2])
    B, S = aud.capped(3, c, 10)
    if args[0] == "slab":
        V, xs = aud.slab100(L, 1, 9, n)
        groups = [np.nonzero(xs >= 8)[0], np.nonzero(xs <= 2)[0]]
        lab = np.where((xs == 1) | (xs == 9), 1, np.where((xs == 2) | (xs == 8), 2, 0))
        r = aud.face_run(V, B, S, groups, lab, 0.45, int(args[3]))
        ts = aud.tau_stats(r, 2)
        print(json.dumps(dict(lattice="bond10", rule=f"B{B}/S{S}", n=n, N=V.N, deaths=r["deaths"], early=r["early"],
                              settle=r["settle"], dens=[round(float(d), 4) for d in r["dens"]],
                              lntau=None if ts is None else round(ts["lntau"], 3),
                              err=None if ts is None else round(ts["err"], 3),
                              cv=None if ts is None else round(ts["cv"], 3))))
    else:
        V = aud.box(L, (1, 1, 1), (2 * n + 1,) * 3)
        cap = int(args[3])
        lf, pop, kind = aud.life_run(V, B, S, 0.45, cap)
        Lf = np.where(kind > 0, lf, cap + 1)
        print(json.dumps(dict(lattice="bond10", rule=f"B{B}/S{S}", n=n, N=V.N, finished=int((kind > 0).sum()),
                              median=float(np.median(Lf)), q25=float(np.percentile(Lf, 25)),
                              q75=float(np.percentile(Lf, 75)),
                              final_density=round(float(pop[kind > 0].mean() / V.N), 4) if (kind > 0).any() else None)))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "kagome":
        if len(a) > 1 and a[1] == "slab":
            kag_slab(int(a[2]), int(a[3]), int(a[4]) if len(a) > 4 else 3, watch=a[5] if len(a) > 5 else "two")
        elif len(a) > 1 and a[1] == "life":
            kag_life(int(a[2]), int(a[3]), int(a[4]) if len(a) > 4 else 3)
        else:
            kagome(int(a[1]) if len(a) > 1 else 3)
    elif a[0] == "bond10-endings":
        pass
    else:
        bond10(a[1:])


def bond10_endings(n=4, T=4096, batches=8, c=6, m=8, p=0.45, every=16):
    """bond10 at class.md's b = 4 (B45/S345 for c = 6) in class.md's vessel: {111} slab of m layers, periodic face
    of n x n periods.  For each soup: which permanent dead set appears first -- a face (a boundary {111} layer empty),
    an axis firewall (three consecutive x-, y- or z-layers, even-odd-even, empty) or a firewall of another diagonal
    (two consecutive layers empty).  Checked every `every` generations."""
    L = aud.lattice("bond10")
    B, S = aud.capped(4, c, 10)
    V, layer = aud.slab111(L, m, n, n)
    P = np.array(V.cells)
    P8 = 2 * n
    faces = [np.nonzero(layer == 0)[0], np.nonzero(layer == m - 1)[0]]
    axis = []
    for a in range(3):
        co = P[:, a] % P8
        for k in range(n):
            axis.append(np.nonzero(np.isin(co, [(2 * k) % P8, (2 * k + 1) % P8, (2 * k + 2) % P8]))[0])
    diag = []
    for d in ((1, 1, -1), (1, -1, 1), (-1, 1, 1)):
        h = (P @ np.array(d)) % (4 * n)
        for k in range(1, 4 * n, 2):
            diag.append(np.nonzero(np.isin(h, [k, (k + 2) % (4 * n)]))[0])
    # every such set must be sealed for b = 4 in this vessel, or the test is meaningless
    ok_axis = all(len(aud.largest_sealed_subset(V, W, 4)) == len(W) for W in axis[:3])
    ok_diag = all(len(aud.largest_sealed_subset(V, W, 4)) == len(W) for W in diag[:3])
    rng = np.random.default_rng(n)
    cnt = {"face": 0, "axis firewall": 0, "diagonal firewall": 0, "several at once": 0, "none": 0}
    for bt in range(batches):
        x = aud.pack((rng.random((64, V.N)) < p).astype(np.uint8))
        done = np.zeros(64, bool)
        for t in range(every, T + 1, every):
            for _ in range(every):
                x = aud.step(V, x, B, S)
            u = aud.unpack(x)
            for r in np.nonzero(~done)[0]:
                ev = [name for name, sets in (("face", faces), ("axis firewall", axis), ("diagonal firewall", diag))
                      if any(not u[r, g].any() for g in sets)]
                if ev:
                    done[r] = True
                    cnt[ev[0] if len(ev) == 1 else "several at once"] += 1
            if done.all():
                break
        cnt["none"] += int((~done).sum())
    print(f"bond10 B{B}/S{S}, {{111}} slab {m} layers, face {n}x{n} periods ({len(faces[0])} cells): axis bands sealed: "
          f"{ok_axis}, diagonal bands sealed: {ok_diag}; first permanent dead set in {64 * batches} soups: {cnt}")


if __name__ == "__main__" and sys.argv[1] == "bond10-endings":
    bond10_endings(int(sys.argv[2]), int(sys.argv[3]))
