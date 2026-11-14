"""three_d.py -- items 3 and 4 of PREDICTIONS.md: bond10 at b = 3, face12e B45/S345 (face12e is not gump).

    python3 three_d.py slab LAT c n1 n2 depth gens [seed]
        slab x = 1 .. 2*depth+1 (walls at odd x), periodic in y, z with n1 x n2 cubes; wall deaths, cuts, pits,
        periodic replicas (fu_slab, a whole x-layer of depth <= 1 inside the dead sealed set = wall death)
    python3 three_d.py column LAT c n m gens [seed]
        walls at odd x and odd y (n x n cubes), periodic in z with m cubes: the four walls of a box, no end caps
    python3 three_d.py box LAT c n cap [seed] [P]
        box of n^3 cubes, 64 soups: lifetime, first permanent dead set, first dead wall sheet (fu_life)
    python3 three_d.py symbox c n cap [seed]      face12e box of n^3 cubes, 64 O_h-symmetric soups
    python3 three_d.py symcheck n                 symmetric soups stay symmetric (200 generations), and the orbit count
    python3 three_d.py bond10c6 n cap             bond10 B345/S2345 boxes: final state, armoured corners, dead walls
"""
import itertools, json, sys
import numpy as np
import fu

B_OF = {"bond10": 3, "face12e": 4}


def rule(name, c):
    return fu.capped(B_OF[name], c, 12 if name == "face12e" else 10)


def slab_vessel(L, xlo, xhi, n1, n2):
    P1, P2 = 2 * n1, 2 * n2
    canon = lambda p: None if (p[0] < xlo or p[0] > xhi) else (p[0], p[1] % P1, p[2] % P2)
    cells = [p for p in itertools.product(range(xlo, xhi + 1), range(P1), range(P2)) if L.typ(p) is not None]
    return fu.Vessel(L, cells, canon)


def column_vessel(L, n, m):
    hi = 2 * n + 1; Pz = 2 * m
    canon = lambda p: None if not (1 <= p[0] <= hi and 1 <= p[1] <= hi) else (p[0], p[1], p[2] % Pz)
    cells = [p for p in itertools.product(range(1, hi + 1), range(1, hi + 1), range(Pz)) if L.typ(p) is not None]
    return fu.Vessel(L, cells, canon)


def box_vessel(L, n):
    hi = 2 * n + 1
    return fu.region(L, lambda q: all(1 <= a <= hi for a in q), hi + 1)


def slab(name, c, n1, n2, depth, gens, seed=1):
    L = fu.lattice(name); b = B_OF[name]; B, S = rule(name, c)
    xlo, xhi = 1, 2 * depth + 1
    V = slab_vessel(L, xlo, xhi, n1, n2)
    x = V.P[:, 0]
    order = [xhi, xlo] + list(range(xlo + 1, xhi))
    layers = [np.nonzero(x == v)[0] for v in order]
    gdepth = [min(v - xlo, xhi - v) for v in order]
    lab = np.minimum(np.minimum(x - xlo, xhi - x), 3).astype(np.int32)
    r = fu.slab_run(V, B, S, b, layers, gdepth, 1, lab, 0.45, gens, P=8, seed=seed)
    ts = fu.tau_line(r)
    rec = dict(lattice=name, rule=f"B{B}/S{S}", vessel="slab", n=[n1, n2], A=n1 * n2, depth=depth, N=V.N, gens=gens,
               seed=seed, walls=r["walls"], walls_by_depth=[int((r["wdepth"] == k).sum()) for k in range(2)],
               deep=r["deep"], cuts=r["cuts"], pits=r["pits"], periodic=r["periodic"], early=r["early"],
               exposure=r["exposure"], max_age=r["max_age"], max_age_end=r["max_age_end"],
               alive_old_end=r["alive_old_end"], dens=[round(float(d), 4) for d in r["dens"]],
               lntau=None if ts is None else round(ts["lntau"], 4), err=None if ts is None else round(ts["err"], 4),
               cv=None if ts is None or ts["cv"] is None else round(ts["cv"], 3), hazard=fu.hazard(r),
               binexp=[int(v) for v in r["binexp"][:26]], binwall=[int(v) for v in r["binwall"][:26]])
    print(json.dumps(rec), flush=True)


def column(name, c, n, m, gens, seed=1):
    """four walls; wall death = a whole wall sheet (x = 1, x = hi, y = 1 or y = hi) inside the dead sealed set.
    fu_slab's two 'boundary layers' are x = 1 and x = hi; the y-sheets are given as further layers of depth 0."""
    L = fu.lattice(name); b = B_OF[name]; B, S = rule(name, c)
    V = column_vessel(L, n, m)
    hi = 2 * n + 1
    P = V.P
    layers = [np.nonzero(P[:, 0] == hi)[0], np.nonzero(P[:, 0] == 1)[0], np.nonzero(P[:, 1] == hi)[0],
              np.nonzero(P[:, 1] == 1)[0], np.nonzero(P[:, 0] == hi - 1)[0], np.nonzero(P[:, 0] == 2)[0],
              np.nonzero(P[:, 1] == hi - 1)[0], np.nonzero(P[:, 1] == 2)[0]]
    gdepth = [0, 0, 0, 0, 1, 1, 1, 1]
    dist = np.minimum(np.minimum(P[:, 0] - 1, hi - P[:, 0]), np.minimum(P[:, 1] - 1, hi - P[:, 1]))
    lab = np.minimum(dist, 3).astype(np.int32)
    r = fu.slab_run(V, B, S, b, layers, gdepth, 1, lab, 0.45, gens, P=8, seed=seed)
    ts = fu.tau_line(r, nwalls=4)
    rec = dict(lattice=name, rule=f"B{B}/S{S}", vessel="column", n=n, m=m, A=n * m, N=V.N, gens=gens, seed=seed,
               walls=r["walls"], cuts=r["cuts"], pits=r["pits"], periodic=r["periodic"], deep=r["deep"],
               early=r["early"], exposure=r["exposure"], max_age=r["max_age"], max_age_end=r["max_age_end"],
               alive_old_end=r["alive_old_end"], dens=[round(float(d), 4) for d in r["dens"]],
               lntau_per_wall=None if ts is None else round(ts["lntau"], 4),
               err=None if ts is None else round(ts["err"], 4),
               cv=None if ts is None or ts["cv"] is None else round(ts["cv"], 3), hazard=fu.hazard(r, nwalls=4))
    print(json.dumps(rec), flush=True)


def sheets(V, n):
    hi = 2 * n + 1
    P = V.P
    return [np.nonzero(P[:, a] == v)[0] for a in range(3) for v in (1, hi)]


def summarize_life(r, cap, V, extra):
    k = r["kind"]
    Lf = np.where(k > 0, r["life"], cap + 1)
    tD = np.where(r["tD"] >= 0, r["tD"], cap + 1); tG = np.where(r["tG"] >= 0, r["tG"], cap + 1)
    rec = dict(extra, N=V.N, cap=cap, finished=int((k > 0).sum()), long_cycles=int((k == 2).sum()),
               median=float(np.median(Lf)), q25=float(np.percentile(Lf, 25)), q75=float(np.percentile(Lf, 75)),
               lifetimes_finished=sorted(int(v) for v in r["life"][k > 0]),
               final_density=round(float(r["pop"][k > 0].mean() / V.N), 4) if (k > 0).any() else None,
               empty=int(((r["pop"] == 0) & (k > 0)).sum()),
               with_permanent_dead_set=int((r["tD"] >= 0).sum()), first_permanent_median=float(np.median(tD)),
               with_dead_sheet=int((r["tG"] >= 0).sum()), first_dead_sheet_median=float(np.median(tG)),
               dead_set_size_at_end_mean=round(float(r["dsize"].mean()), 1))
    print(json.dumps(rec), flush=True)
    return rec


def box(name, c, n, cap, seed=1, P=16):
    L = fu.lattice(name); b = B_OF[name]; B, S = rule(name, c)
    V = box_vessel(L, n)
    r = fu.life_run(V, B, S, b, sheets(V, n), 0.45, cap, P=P, seed=seed)
    return summarize_life(r, cap, V, dict(lattice=name, rule=f"B{B}/S{S}", vessel="box", n=n, seed=seed, soups="random 0.45"))


def oh_orbits(V, n):
    """orbits of the cells of the box 1..2n+1 under O_h about its centre (n+1, n+1, n+1)."""
    cen = n + 1
    idx = V.index
    orb = -np.ones(V.N, np.int64); k = 0
    for i, p in enumerate(V.cells):
        if orb[i] >= 0:
            continue
        q = tuple(a - cen for a in p)
        for perm in itertools.permutations(range(3)):
            for sg in itertools.product((1, -1), repeat=3):
                im = tuple(sg[j] * q[perm[j]] + cen for j in range(3))
                orb[idx[im]] = k
        k += 1
    return orb, k


def sym_seeds(V, n, seed, p=0.45):
    orb, k = oh_orbits(V, n)
    rng = np.random.default_rng(seed)
    vals = (rng.random((64, k)) < p).astype(np.uint8)
    return fu.pack(vals[:, orb]), orb, k


def symbox(c, n, cap, seed=1):
    L = fu.lattice("face12e"); b = 4; B, S = rule("face12e", c)
    V = box_vessel(L, n)
    x0, orb, k = sym_seeds(V, n, seed)
    r = fu.life_run(V, B, S, b, sheets(V, n), 0.45, cap, P=4, seed=seed, x0=x0[:V.N].copy())
    return summarize_life(r, cap, V, dict(lattice="face12e", rule=f"B{B}/S{S}", vessel="box", n=n, seed=seed,
                                          soups="O_h-symmetric 0.45", orbits=int(k)))


def symcheck(n):
    L = fu.lattice("face12e"); B, S = rule("face12e", 6)
    V = box_vessel(L, n)
    x, orb, k = sym_seeds(V, n, 99)
    ok = True
    for t in range(200):
        x = fu.step(V, x, B, S)
        u = fu.unpack(x)
        for o in range(k):
            m = orb == o
            col = u[:, m]
            ok &= bool((col.min(1) == col.max(1)).all())
    print(json.dumps(dict(check="O_h symmetry preserved 200 generations, 64 soups", n=n, cells=V.N, orbits=int(k),
                          ok=ok, alive_end=int(u.sum()))))


def bond10c6(n, cap, seed=1):
    """B345/S2345 boxes: run 64 soups to a periodic state (period <= 2 or a power-of-two snapshot), then report
    whether the 24-cell armoured core is alive, how many wall sheets are dead, final density."""
    L = fu.lattice("bond10"); b = 3; B, S = rule("bond10", 6)
    V = box_vessel(L, n)
    core = np.array(sorted(fu.armoured_core(V, b, 6)))
    rng = np.random.default_rng(seed)
    x = fu.pack((rng.random((64, V.N)) < 0.45).astype(np.uint8))
    prev2 = fu.unpack(x) * 0 + 2; prev1 = fu.unpack(x); snap = prev1 * 0 + 2
    done = np.zeros(64, bool); endt = -np.ones(64, int)
    final = np.zeros((64, V.N), np.uint8)
    for t in range(1, cap + 1):
        x = fu.step(V, x, B, S)
        u = fu.unpack(x)
        per = ((u == prev2).all(1) | (u == snap).all(1)) & ~done
        final[per] = u[per]; endt[per] = t; done |= per
        if (t & (t - 1)) == 0 and t >= 4:
            snap = u.copy()
        prev2, prev1 = prev1, u
        if done.all():
            break
    final[~done] = u[~done]
    sh = sheets(V, n)
    core_alive = (final[:, core] == 1).all(1)
    dead_sheets = np.array([[int(not final[r, s].any()) for s in sh] for r in range(64)]).sum(1)
    print(json.dumps(dict(lattice="bond10", rule=f"B{B}/S{S}", n=n, N=V.N, cap=cap, settled=int(done.sum()),
                          median_end=float(np.median(np.where(done, endt, cap + 1))),
                          core_fully_alive=int(core_alive.sum()), soups_with_a_dead_sheet=int((dead_sheets > 0).sum()),
                          dead_sheets_hist={int(v): int((dead_sheets == v).sum()) for v in np.unique(dead_sheets)},
                          final_density=round(float(final.mean()), 4),
                          core_cells=core.tolist()[:6])), flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "slab":
        slab(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), int(a[7]) if len(a) > 7 else 1)
    elif a[0] == "column":
        column(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]) if len(a) > 6 else 1)
    elif a[0] == "box":
        box(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]) if len(a) > 5 else 1, int(a[6]) if len(a) > 6 else 16)
    elif a[0] == "symbox":
        symbox(int(a[1]), int(a[2]), int(a[3]), int(a[4]) if len(a) > 4 else 1)
    elif a[0] == "symcheck":
        symcheck(int(a[1]))
    elif a[0] == "bond10c6":
        bond10c6(int(a[1]), int(a[2]))
