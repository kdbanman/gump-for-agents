"""two_d.py -- items 1 and 2 of PREDICTIONS.md: kagome8 and hex9 at b = 4, kagome4 at b = 2.

    python3 two_d.py confine LAT c            soups in free space: escapes from the position-aware hull
    python3 two_d.py bulk LAT c               torus statistics (the review's aud_bulk), 4 soup densities
    python3 two_d.py slab LAT c ORBIT n depth gens [seed]
                                              strip between two sealed walls, n periods long, depth = number of
                                              values of u.p; wall deaths / cuts / pits / periodic (fu_slab)
    python3 two_d.py life LAT c R cap         hull of the hexagonal seed of radius R, 64 soups (fu_life)
LAT in kagome4 (b = 2), kagome8, hex9 (b = 4).  ORBIT: A (u = (1,0)) or B (u = (2,1)).  One JSON line per run.
"""
import json, sys, itertools
import numpy as np
import fu, structure as st

B_OF = {"kagome4": 2, "kagome8": 4, "hex9": 4}
ORB = {("kagome4", "A"): ((1, 0), (0, 2)), ("kagome8", "A"): ((1, 0), (0, 2)), ("kagome8", "B"): ((2, 1), (2, -4)),
       ("hex9", "B"): ((2, 1), (1, -2))}


def confine(name, c, H=96, T=300, seeds=(3, 4, 5)):
    L = fu.lattice(name); b = B_OF[name]
    B, S = fu.capped(b, c, L.K)
    V = fu.torus(L, H)
    P = V.P
    dirs, m, res = st.HULLDIRS[name]
    U = np.array(dirs + [(-a, -q) for a, q in dirs])
    gen = np.array([(3, 1), (1, 3), (-3, -1), (-1, -3), (3, -1), (-1, 3), (5, 2), (-2, -5)])
    rng = np.random.default_rng(c)
    sealed = {tuple(u): [C for C in range(m) if st.sealed_C(name, tuple(u), C)] for u in U}
    out = dict(lattice=name, rule=f"B{B}/S{S}", H=H, T=T, soups=0, outside_hull=0, outside_tight=0,
               outside_seed_support_unsealed_dirs=0, alive_end=0)
    for R in seeds:
        cen = H // 2 - (H // 2) % 6
        q = P - cen
        reg = (np.abs(q[:, 0]) <= 2 * R) & (np.abs(q[:, 1]) <= 2 * R) & (np.abs(q[:, 0] + q[:, 1]) <= 2 * R)
        stt = np.zeros((64, V.N), np.uint8)
        stt[:, reg] = rng.random((64, int(reg.sum()))) < 0.5
        hb, tb, gb = [], [], []
        for r in range(64):
            live = P[stt[r] == 1]
            s = (live @ U.T).max(0)
            push = []
            for j, u in enumerate(U):
                C = int(s[j])
                while C % m not in sealed[tuple(u)]:
                    C += 1
                push.append(C)
            hb.append(np.array(push)); tb.append(s); gb.append((live @ gen.T).max(0))
        x = fu.pack(stt)
        for t in range(T):
            x = fu.step(V, x, B, S)
            u = fu.unpack(x)
            for r in range(64):
                live = P[u[r] == 1]
                if len(live) == 0:
                    continue
                s = (live @ U.T).max(0)
                out["outside_hull"] += int((s > hb[r]).any())
                out["outside_tight"] += int((s > tb[r]).any())
                out["outside_seed_support_unsealed_dirs"] += int(((live @ gen.T).max(0) > gb[r]).any())
        out["soups"] += 64
        out["alive_end"] += int((fu.unpack(x).sum(1) > 0).sum())
    print(json.dumps(out))


def bulk(name, c):
    L = fu.lattice(name); b = B_OF[name]
    B, S = fu.capped(b, c, L.K)
    V = fu.torus(L, 126 if name == "hex9" else 128)
    rows = []
    for p in (0.2, 0.35, 0.5, 0.65):
        o = fu.bulk_run(V, B, S, p, [1024, 4096], seed=int(100 * p) + c)
        rows.append(dict(p0=p, running_1024=int(o[0, 0]), rho_1024=round(float(o[0, 1]), 4),
                         act_1024=round(float(o[0, 2]), 4), running_4096=int(o[1, 0]), rho_4096=round(float(o[1, 1]), 4),
                         act_4096=round(float(o[1, 2]), 4), rho_all_4096=round(float(o[1, 3]), 4)))
    print(json.dumps(dict(lattice=name, rule=f"B{B}/S{S}", N=V.N, rows=rows)))


def strip(name, orbit, n, depth):
    """strip between two sealed walls; returns the vessel, its layers (boundary layers first), their depths from the
    nearer wall (0 = boundary layer, counting only layers that hold cells) and a label per cell (depth, capped at 3)."""
    u, g = ORB[(name, orbit)]
    V = st.strip_for(name, u, g, depth, n)
    h = V.h
    hs = sorted(set(h.tolist()))
    order = [hs[-1], hs[0]] + hs[1:-1]
    layers = [np.nonzero(h == hv)[0] for hv in order]
    gdepth = [min(hs.index(hv), len(hs) - 1 - hs.index(hv)) for hv in order]
    lab = np.zeros(V.N, np.int32)
    for hv, d in zip(order, gdepth):
        lab[h == hv] = min(d, 3)
    return V, layers, gdepth, lab


def slab(name, c, orbit, n, depth, gens, seed=1, P=8, dmax=3, F=0):
    L = fu.lattice(name); b = B_OF[name]
    B, S = fu.capped(b, c, L.K)
    V, layers, gdepth, lab = strip(name, orbit, n, depth)
    h = V.h
    fz = \
        np.where(np.isin(np.arange(V.N), np.concatenate([layers[i] for i, d in enumerate(gdepth) if d <= 1 and
                                                          V.h[layers[i][0]] > V.h.mean()])), 1,
                 np.where(np.isin(np.arange(V.N), np.concatenate([layers[i] for i, d in enumerate(gdepth) if d <= 1 and
                                                                   V.h[layers[i][0]] < V.h.mean()])), 2, 0))
    r = fu.slab_run(V, B, S, b, layers, gdepth, dmax, lab, 0.45, gens, P=P, seed=seed, fz=fz, F=F)
    ts = fu.tau_line(r)
    wd = r["wdepth"]
    rec = dict(lattice=name, rule=f"B{B}/S{S}", orbit=orbit, n=n, wall_cells=len(layers[0]), depth=depth,
               layers=len(layers), N=V.N, gens=gens, seed=seed, P=P, dmax=dmax, F=F, frozen=r["frozen"], walls=r["walls"],
               walls_by_depth=[int((wd == k).sum()) for k in range(dmax + 1)], deep=r["deep"], cuts=r["cuts"],
               pits=r["pits"], periodic=r["periodic"], early=r["early"], exposure=r["exposure"], max_age=r["max_age"],
               max_age_end=r["max_age_end"], alive_old_end=r["alive_old_end"],
               dens=[round(float(d), 4) for d in r["dens"]],
               lntau=None if ts is None else round(ts["lntau"], 4), err=None if ts is None else round(ts["err"], 4),
               cv=None if ts is None or ts["cv"] is None else round(ts["cv"], 3), hazard=fu.hazard(r),
               binexp=[int(v) for v in r["binexp"][:26]], binwall=[int(v) for v in r["binwall"][:26]])
    print(json.dumps(rec), flush=True)


def life(name, c, R, cap, seed=1):
    L = fu.lattice(name); b = B_OF[name]
    B, S = fu.capped(b, c, L.K)
    V, bounds = st.hull_vessel(name, R)
    P = V.P
    groups = []
    for u, C in bounds:
        hv = P @ np.array(u)
        g = np.nonzero(hv == hv.max())[0]
        groups.append(g)
    r = fu.life_run(V, B, S, b, groups, 0.45, cap, P=16, seed=seed)
    k = r["kind"]
    Lf = np.where(k > 0, r["life"], cap + 1)
    print(json.dumps(dict(lattice=name, rule=f"B{B}/S{S}", R=R, N=V.N, cap=cap, finished=int((k > 0).sum()),
                          long_cycles=int((k == 2).sum()), median=float(np.median(Lf)),
                          q25=float(np.percentile(Lf, 25)), q75=float(np.percentile(Lf, 75)),
                          final_density=round(float(r["pop"][k > 0].mean() / V.N), 4) if (k > 0).any() else None,
                          empty=int(((r["pop"] == 0) & (k > 0)).sum()),
                          first_permanent_median=float(np.median(np.where(r["tD"] >= 0, r["tD"], cap + 1))),
                          first_side_death_median=float(np.median(np.where(r["tG"] >= 0, r["tG"], cap + 1))))),
          flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "confine":
        confine(a[1], int(a[2]))
    elif a[0] == "bulk":
        bulk(a[1], int(a[2]))
    elif a[0] == "slab":
        slab(a[1], int(a[2]), a[3], int(a[4]), int(a[5]), int(a[6]), int(a[7]) if len(a) > 7 else 1,
             F=int(a[8]) if len(a) > 8 else 0)
    elif a[0] == "life":
        life(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]) if len(a) > 5 else 1)
