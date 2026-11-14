"""face12e.py -- tests of the edge-neighbour rule (NOT gump): faces of the cubic honeycomb, 8 perpendicular +
4 coplanar edge-sharing neighbours, B45/S345 unless another cap is given.  Stepper: aud.c (validate.py first).

    python3 face12e.py structure          exact: sealing by plane position, degrees, firewalls, sealed sets, armour
    python3 face12e.py confine            soups in free space: odd box never left, tight box and diagonal hull left
    python3 face12e.py bulk [c]           torus 10^3 cubes, 64 soups per density
    python3 face12e.py slab n gens [c] [depth] [watch]   periodic wall of n x n cubes; watch = two (default) | one
    python3 face12e.py life n cap [c] [p] boxes of n^3 cubes with odd walls, 64 soups: lifetimes and how they end
    python3 face12e.py layers n cap [seed] one box, 64 soups: the sequence of permanent layer deaths
    python3 face12e.py cuts n T [batches]  periodic slab: wall death or transverse firewall, which comes first
Same commands with "gump" as an extra last word run the control on gump's own neighbourhood where it makes sense.
"""
import itertools, json, sys
import numpy as np
import aud

B45, S345 = [4, 5], [3, 4, 5]


def rule(c, b=4):
    return aud.capped(b, c, 12)


# ------------------------------------------------------------------------------------------------ structure
def inside_counts(L, u, C, reach=6):
    """For the half-space {u.p <= C}: max over cells outside of the number of neighbours inside, per (type, height)."""
    out = {}
    R = 4
    for p in itertools.product(range(-R, R + 1), repeat=3):
        t = L.typ(p)
        if t is None:
            continue
        h = sum(a * b for a, b in zip(u, p))
        if h <= C:
            continue
        n = sum(1 for o in L.offsets[t] if sum(a * (b + c) for a, b, c in zip(u, p, o)) <= C)
        out[(t, h - C)] = max(out.get((t, h - C), 0), n)
    return out


def structure():
    for name in ("face12e", "gump"):
        L = aud.lattice(name)
        print(f"== {name}: most neighbours inside {{u.p <= C}} of a cell outside it, by plane position C")
        for u in ((1, 0, 0), (1, 1, 1), (1, 1, 0)):
            row = []
            for C in (0, 1, 2, 3):
                ic = inside_counts(L, u, C)
                row.append(f"C={C}: {max(ic.values())}")
            cu = max(sum(1 for o in offs if sum(a * b for a, b in zip(u, o)) < 0) for offs in L.offsets)
            print(f"   u={u}: c(u) = max a- = {cu};  " + "  ".join(row))
    L = aud.lattice("face12e")
    print("== face12e, box of n^3 cubes with odd walls: vessel degrees")
    for n in (2, 3, 4):
        V = aud.box(L, (1, 1, 1), (2 * n + 1,) * 3)
        deg = V.degrees()
        hist = {int(d): int((deg == d).sum()) for d in np.unique(deg)}
        print(f"   n={n}: {V.N} cells (3n^2(n+1) = {3 * n * n * (n + 1)}), degree histogram {hist}")
        for c in (6, 7, 8, 9, 10):
            # Theorem E armour: (b-1)-core of the subgraph on cells of vessel-degree <= c - 1
            W = set(int(i) for i in np.nonzero(deg <= c - 1)[0])
            ch = True
            while ch:
                ch = False
                for i in list(W):
                    if sum(1 for q in V.nbr[i] if int(q) in W) < 3:
                        W.discard(i); ch = True
            print(f"      cap c={c}: armoured core (3-core of the degree <= {c - 1} cells) has {len(W)} cells")
    print("== face12e: bands of consecutive x-layers that are sealed for b = 4 (dead forever whatever is outside)")
    V, xs = aud.slab100(L, 1, 21, 3)
    for lo in (8, 9):
        for w in (1, 2, 3, 4):
            W = np.nonzero((xs >= lo) & (xs < lo + w))[0]
            S = aud.largest_sealed_subset(V, W, 4)
            print(f"   layers x = {lo}..{lo + w - 1} ({'even' if lo % 2 == 0 else 'odd'} first): "
                  f"{'sealed' if len(S) == len(W) else 'not sealed'} (largest sealed subset {len(S)} of {len(W)})")
    for w in (1, 2, 3, 4):
        W = np.nonzero(xs > 21 - w)[0]
        S = aud.largest_sealed_subset(V, W, 4)
        print(f"   the top {w} layer(s) under an odd wall (x = {22 - w}..21): "
              f"{'sealed' if len(S) == len(W) else 'not sealed'} ({len(S)} of {len(W)})")
    print("== face12e: a filled closed cube (free space) after one generation")
    for n in (2, 3, 5):
        Vb = aud.box(L, (-3, -3, -3), (2 * n + 5,) * 3)
        Pb = np.array(Vb.cells)
        st = ((Pb >= 1) & (Pb <= 2 * n + 1)).all(1).astype(np.uint8)[None]
        x = aud.step(Vb, aud.pack(st), B45, S345)
        print(f"   {n}^3 cubes, {int(st.sum())} cells -> {int(aud.unpack(x, 1).sum())} alive")
    print("== face12e: finite sealed sets?  peel a finite patch inside a slab with odd walls (outside patch = alive)")
    for xlo, xhi, tag in ((1, 1, "one sheet of x-faces"), (1, 3, "one cube thick (odd, even, odd)"),
                          (1, 5, "two cubes thick"), (1, 2, "odd wall + even layer (upper side open)")):
        V, xs = aud.slab100(L, xlo, xhi, 12)
        ys = np.array([p[1] for p in V.cells]); zs = np.array([p[2] for p in V.cells])
        W = np.nonzero((ys >= 4) & (ys <= 19) & (zs >= 4) & (zs <= 19))[0]
        S = aud.largest_sealed_subset(V, W, 4)
        print(f"   slab x = {xlo}..{xhi} ({tag}): largest sealed subset of a 8x8-cube patch: {len(S)} of {len(W)} cells")
    print("== forward-count certificate (C1) for the same slabs: min over cells of #neighbours q in the vessel with v.q > v.p")
    rng = np.random.default_rng(5)
    for xlo, xhi in ((1, 1), (1, 3), (1, 5), (1, 9)):
        V, xs = aud.slab100(L, xlo, xhi, 4)
        best = 0
        for trial in range(200):
            v = np.array([0.0, *rng.normal(size=2)]) + np.array([rng.choice([-1, 1]) * 1e-3, 0, 0])
            worst = 99
            for p in V.cells:
                cnt = sum(1 for o in L.offsets[L.typ(p)] if xlo <= p[0] + o[0] <= xhi and np.dot(v, o) > 0)
                worst = min(worst, cnt)
            best = max(best, worst)
        print(f"   slab x = {xlo}..{xhi}: best worst-case forward count {best} (need >= 4 for 'no finite sealed set')")


# ------------------------------------------------------------------------------------------------ confinement
def confine(T=200, nsoup=64, names=("face12e", "gump"), rules=None):
    H = 40
    rules = rules or {}
    for name in names:
        L = aud.lattice(name)
        B45, S345 = rules.get(name, ([4, 5], [3, 4, 5]))
        V = aud.torus(L, H)
        P = np.array(V.cells)
        rng = np.random.default_rng(3)
        print(f"== {name}: {nsoup} soups (density 0.5) per seed cube, free space (torus H={H}), {T} generations")
        for lo, hi in ((15, 23), (14, 22), (14, 23), (16, 22), (17, 21)):
            seed = ((P >= lo) & (P <= hi)).all(1)
            st = np.zeros((nsoup, V.N), np.uint8)
            st[:, seed] = rng.random((nsoup, int(seed.sum()))) < 0.5
            olo = np.array([st[r][:, None] * 0 + 0 for r in range(1)])  # placeholder to keep numpy quiet
            # per-soup tight bounding box of the seed, its odd box, and its diagonal hull
            tlo = np.array([P[st[r] == 1].min(0) for r in range(nsoup)]); thi = np.array([P[st[r] == 1].max(0) for r in range(nsoup)])
            olo = tlo - (tlo % 2 == 0); ohi = thi + (thi % 2 == 0)
            signs = np.array(list(itertools.product((1, -1), repeat=3)))
            D = P @ signs.T                                           # d.p for the 8 diagonals
            dmax = np.array([D[st[r] == 1].max(0) for r in range(nsoup)])
            out_odd = 0; out_tight = 0; out_diag = 0; reach_wall = np.zeros((nsoup, 6), bool)
            x = aud.pack(st)
            alive_end = 0
            for t in range(T):
                x = aud.step(V, x, B45, S345)
                u = aud.unpack(x, nsoup)
                for r in range(nsoup):
                    live = P[u[r] == 1]
                    if len(live) == 0:
                        continue
                    mn, mx = live.min(0), live.max(0)
                    out_odd += int((mn < olo[r]).any() or (mx > ohi[r]).any())
                    out_tight += int((mn < tlo[r]).any() or (mx > thi[r]).any())
                    out_diag += int((D[u[r] == 1].max(0) > dmax[r]).any())
                    reach_wall[r] |= np.concatenate([mn == olo[r], mx == ohi[r]])
            u = aud.unpack(x, nsoup)
            print(f"   seed cube [{lo},{hi}]^3: soup-generations with a live cell outside the ODD box: {out_odd}; "
                  f"outside the tight bounding box: {out_tight}; outside the diagonal hull: {out_diag}; "
                  f"odd walls touched (of {6 * nsoup}): {int(reach_wall.sum())}; alive at the end: {int((u.sum(1) > 0).sum())}")


# ------------------------------------------------------------------------------------------------ bulk
def bulk(c=6, name="face12e"):
    L = aud.lattice(name)
    V = aud.torus(L, 20)
    B, S = rule(c)
    print(f"== {name} B{B}/S{S} torus of 10^3 cubes ({V.N} cells), 64 soups per density; "
          f"columns: running (not periodic), density, activity x(t)!=x(t-2)")
    for p in (0.15, 0.25, 0.35, 0.45, 0.55, 0.7):
        out = aud.bulk_run(V, B, S, p, [1024, 4096], seed=int(p * 100))
        print(f"   p0={p:.2f}: t=1024: {int(out[0, 0])}/64 rho={out[0, 1]:.4f} act={out[0, 2]:.4f} | "
              f"t=4096: {int(out[1, 0])}/64 rho={out[1, 1]:.4f} act={out[1, 2]:.4f} (all 64: rho={out[1, 3]:.4f})")


# ------------------------------------------------------------------------------------------------ slab
def slab(n, gens, c=6, depth=4, watch="two", name="face12e", p=0.45, seed=1, n2=None):
    L = aud.lattice(name)
    B, S = rule(c)
    n2 = n if n2 is None else n2
    if name == "face12e":
        xlo, xhi = 1, 2 * depth + 1
        V, xs = aud.slab100(L, xlo, xhi, n, n2)
        if watch == "two":
            groups = [np.nonzero(xs >= xhi - 1)[0], np.nonzero(xs <= xlo + 1)[0]]
        elif watch == "one":
            groups = [np.nonzero(xs == xhi)[0], np.nonzero(xs == xlo)[0]]
        elif watch == "second":
            groups = [np.nonzero(xs == xhi - 1)[0], np.nonzero(xs == xlo + 1)[0]]
        lab = np.where((xs == xlo) | (xs == xhi), 1, np.where((xs == xlo + 1) | (xs == xhi - 1), 2,
                       np.where((xs == xlo + 2) | (xs == xhi - 2), 3, 0)))
        A = n * n2
    else:
        V, layer = aud.slab111(L, 2 * depth, n, n2)
        m = 2 * depth
        groups = [np.nonzero(layer == m - 1)[0], np.nonzero(layer == 0)[0]]
        lab = np.where((layer == 0) | (layer == m - 1), 1, np.where((layer == 1) | (layer == m - 2), 2, 0))
        A = len(groups[0])
    r = aud.face_run(V, B, S, groups, lab, p, gens, seed=seed)
    ts = aud.tau_stats(r, 2)
    haz = [(k, int(r["bindeath"][k]), r["binexp"][k]) for k in range(len(r["binexp"])) if r["binexp"][k] > 0]
    rec = dict(lattice=name, rule=f"B{B}/S{S}", n=[n, n2], A=A, N=V.N, depth=depth, watch=watch, gens=gens,
               deaths=r["deaths"], early=r["early"], settle=r["settle"], early_settle=r["early_settle"],
               exposure=r["exposure"], by_group=r["by_group"], dens=[round(float(d), 4) for d in r["dens"]],
               lntau=None if ts is None else round(ts["lntau"], 3), err=None if ts is None else round(ts["err"], 3),
               cv=None if ts is None else round(ts["cv"], 3),
               hazard=[[k, d, round(2 * e / d, 1) if d else None] for k, d, e in haz])
    print(json.dumps(rec))
    return rec


# ------------------------------------------------------------------------------------------------ hull lifetimes
def life(n, cap, c=6, p=0.45, name="face12e", seed=1):
    L = aud.lattice(name)
    B, S = rule(c)
    if name == "face12e":
        V = aud.box(L, (1, 1, 1), (2 * n + 1,) * 3)
    else:   # gump: octahedron of n layers about a cube centre (control)
        V = aud.region(L, lambda q: all(abs(sx * q[0] + sy * q[1] + sz * q[2]) <= 2 * n - 1
                                        for sx in (1,) for sy in (1, -1) for sz in (1, -1)), 2 * n + 1)
    lf, pop, kind = aud.life_run(V, B, S, p, cap, seed=seed)
    fin = lf[kind > 0]
    med = float(np.median(np.where(kind > 0, lf, cap + 1)))
    rec = dict(lattice=name, rule=f"B{B}/S{S}", n=n, N=V.N, p=p, cap=cap, finished=int((kind > 0).sum()),
               median=med if med <= cap else f">{cap}", q25=float(np.percentile(np.where(kind > 0, lf, cap + 1), 25)),
               q75=float(np.percentile(np.where(kind > 0, lf, cap + 1), 75)),
               mean_final_density=round(float(pop[kind > 0].mean() / V.N), 4) if len(fin) else None,
               empty_endings=int(((pop == 0) & (kind > 0)).sum()), long_cycles=int((kind == 2).sum()))
    print(json.dumps(rec))
    return rec


def layers(n, cap, seed=1, c=6, p=0.45):
    """One box of n^3 cubes, 64 soups, stepped from python: record every permanent layer death (wall sheet and
    the layer beneath simultaneously empty, measured against the current sealed box) until each soup is periodic."""
    L = aud.lattice("face12e")
    B, S = rule(c)
    V = aud.box(L, (1, 1, 1), (2 * n + 1,) * 3)
    P = np.array(V.cells)
    rng = np.random.default_rng(seed)
    st = (rng.random((64, V.N)) < p).astype(np.uint8)
    x = aud.pack(st)
    lo = np.ones((64, 3), int); hi = np.full((64, 3), 2 * n + 1)
    events = [[] for _ in range(64)]
    prev2 = None; prev1 = aud.unpack(x)
    done = np.zeros(64, bool); endt = np.zeros(64, int); temp_empty = np.zeros(64, int)
    for t in range(1, cap + 1):
        x = aud.step(V, x, B, S)
        u = aud.unpack(x)
        for r in range(64):
            if done[r]:
                continue
            live = P[u[r] == 1]
            if prev2 is not None and np.array_equal(u[r], prev2[r]):
                done[r] = True; endt[r] = t - 2
                continue
            ch = True
            while ch and (hi[r] > lo[r]).all():
                ch = False
                for a in range(3):
                    if hi[r, a] - lo[r, a] >= 2 and not (live[:, a] >= hi[r, a] - 1).any():
                        hi[r, a] -= 2; events[r].append((t, a, +1)); ch = True
                    if hi[r, a] - lo[r, a] >= 2 and not (live[:, a] <= lo[r, a] + 1).any():
                        lo[r, a] += 2; events[r].append((t, a, -1)); ch = True
            # wall sheet alone empty while the layer beneath is not: a temporary (non-sealed) emptiness
            for a in range(3):
                temp_empty[r] += int(not (live[:, a] == hi[r, a]).any()) + int(not (live[:, a] == lo[r, a]).any())
        prev2, prev1 = prev1, u
        if done.all():
            break
    u = aud.unpack(x)
    nev = [len(e) for e in events]
    side = (hi - lo) // 2
    print(f"box n={n} ({V.N} cells), 64 soups, p={p}: finished {int(done.sum())}/64 within {cap}; median end "
          f"{np.median(endt[done]) if done.any() else None}")
    print(f"   permanent two-layer deaths per soup before settling: mean {np.mean(nev):.2f}, min {min(nev)}, max {max(nev)}")
    vol = np.array([int(np.prod(s)) for s in side])
    print(f"   sealed box left at the end, in cubes (n^3 = {n ** 3} at the start): median volume {int(np.median(vol))}, "
          f"max {int(vol.max())}; largest side still alive: "
          f"{ {int(k): int((side.max(1) == k).sum()) for k in np.unique(side.max(1))} } (side: soups)")
    waits = [e[0][0] for e in events if e]
    last = [e[-1][0] for e in events if e]
    print(f"   first permanent layer death at generation: median {np.median(waits):.0f}; last one: median {np.median(last):.0f}")
    print(f"   final population: mean {u.sum(1).mean():.1f}, empty {int((u.sum(1) == 0).sum())}/64; "
          f"soup-wall-generations with the wall sheet empty (any, incl. temporary): {int(temp_empty.sum())}")
    # is the live set at the end inside the sealed box, and is the region outside it dead (it must be)
    return events, endt, side


def cuts(n, T, batches=8, c=6, depth=4, p=0.45):
    """Competing endings in the periodic slab: for each soup, which permanent event comes first -- a wall death
    (wall sheet + layer beneath empty) or a transverse firewall (three consecutive y- or z-layers, even-odd-even,
    empty: sealed, wraps the periodic face).  Checked every 64 generations; both are permanent once present."""
    L = aud.lattice("face12e")
    B, S = rule(c)
    xlo, xhi = 1, 2 * depth + 1
    V, xs = aud.slab100(L, xlo, xhi, n)
    P = np.array(V.cells)
    rng = np.random.default_rng(n)
    walls = [np.nonzero(xs >= xhi - 1)[0], np.nonzero(xs <= xlo + 1)[0]]
    bands = []
    for a in (1, 2):
        for k in range(n):
            ys = [(2 * k) % (2 * n), (2 * k + 1) % (2 * n), (2 * k + 2) % (2 * n)]
            bands.append(np.nonzero(np.isin(P[:, a], ys))[0])
    first = {"wall": 0, "cut": 0, "both": 0, "none": 0, "settled": 0}
    tw, tc = [], []
    for bt in range(batches):
        st = (rng.random((64, V.N)) < p).astype(np.uint8)
        x = aud.pack(st)
        done = np.zeros(64, bool)
        for t in range(64, T + 1, 64):
            for _ in range(64):
                x = aud.step(V, x, B, S)
            u = aud.unpack(x)
            for r in np.nonzero(~done)[0]:
                w = any(not u[r, g].any() for g in walls)
                k = any(not u[r, g].any() for g in bands)
                if w or k:
                    done[r] = True
                    first["both" if (w and k) else ("wall" if w else "cut")] += 1
                    (tw if w else tc).append(t)
            if done.all():
                break
        first["none"] += int((~done).sum())
    tot = sum(first.values())
    print(f"face12e slab {n}x{n} cubes, {depth} deep, {tot} soups, up to {T} generations: first permanent event: "
          f"wall death {first['wall']}, transverse firewall {first['cut']}, both within 64 generations {first['both']}, "
          f"neither {first['none']};  median time wall {np.median(tw) if tw else None}, cut {np.median(tc) if tc else None}")


if __name__ == "__main__":
    a = sys.argv[1:]
    name = "face12e"
    if a and a[-1] in ("gump", "fcc"):     # controls / part 3: {111} slabs of 2*depth layers, octahedra
        name = a[-1]; a = a[:-1]
    cmd = a[0]
    if cmd == "structure":
        structure()
    elif cmd == "confine":
        confine()
    elif cmd == "confine-others":      # bond10 B45/S345 and face8 B34/S234: the table says "octahedron" for both
        confine(names=("bond10", "face8"), rules={"bond10": ([4, 5], [3, 4, 5]), "face8": ([3, 4], [2, 3, 4])})
    elif cmd == "bulk":
        bulk(int(a[1]) if len(a) > 1 else 6, name)
    elif cmd == "slab":
        n = a[1].split("x")
        slab(int(n[0]), int(a[2]), int(a[3]) if len(a) > 3 else 6, int(a[4]) if len(a) > 4 else 4,
             a[5] if len(a) > 5 else "two", name, n2=int(n[1]) if len(n) > 1 else None)
    elif cmd == "life":
        life(int(a[1]), int(a[2]), int(a[3]) if len(a) > 3 else 6, float(a[4]) if len(a) > 4 else 0.45, name)
    elif cmd == "cuts":
        cuts(int(a[1]), int(a[2]), int(a[3]) if len(a) > 3 else 8)
    elif cmd == "layers":
        layers(int(a[1]), int(a[2]), int(a[3]) if len(a) > 3 else 1)
