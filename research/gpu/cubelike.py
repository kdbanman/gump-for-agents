#!/usr/bin/env python3
"""Plateaus of cube-like seeds at vertex-centred R = 40 (the lead's experiment c).

Seeds (deterministic, O_h-symmetric, research/lineage/seeds.py's `sc` family one size up): the closed cube of side 14
plus the hollow shell of side 16, minus one (`sc:14:K`), two (`sc2:14:A:B`) or three (`sc3`, the same construction
with three shell orbits) of the shell's 36 O_h orbits. 7,807 seeds in all.

  python3 research/gpu/cubelike.py prepare OUT.npz     # local, fl.c: burst of 1000 generations, keep distinct states
                                                       # whose hull is exactly R = 40 (vertex-centred) at generation 1000
  modal run research/gpu/modal_app.py::cubelike        # GPU: residence at 40, then (kept state) at 38, then at 36
  python3 research/gpu/cubelike.py analyse research/data/gpu_facelaw/cubelike_v40.json

Plateau at R: from generation 1000 (for R = 40; the study in research/lineage/ starts it at the last burst death, at
most 1000 generations earlier, ~1e-5 tau) or from the peel that ended the previous plateau, to the generation the outer
layer of the R hull is extinct. Censored: settled first (kinds 2, 3: period <= 128) — excluded from the statistics
and counted — or still alive at the cap (12 stationary tau). Stationary tau from fresh O_h soups (this directory).
"""
import itertools, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TAU = {40: 8.630e7, 38: 1.254e7, 36: 2.247e6}          # fresh O_h vertex soups, research/data/gpu_facelaw/symvR{40,38,36}*


def specs_and_bits(v):
    sys.path.insert(0, os.path.join(HERE, '..', 'lineage'))
    import seeds
    from gsim import fl
    c = (1, 1, 1)
    cube, sh = seeds.box_cells(c, 14), seeds.shell_cells(c, 16)
    orbs = seeds.orbits_of(sh, c)[::-1]                    # outermost first, as seeds.py's sc / sc2
    base = fl.bits_from_cells(v, list(cube | sh))
    index = {tuple(p): i for i, p in enumerate(v.cells)}
    onode = [int(v.orbit_of[index[next(iter(o))]]) for o in orbs]
    specs, rows = [], []
    for r in (1, 2, 3):
        for ks in itertools.combinations(range(len(orbs)), r):
            b = base.copy(); b[[onode[k] for k in ks]] = False
            specs.append(('sc', 'sc2', 'sc3')[r - 1] + ':14:' + ':'.join(map(str, ks))); rows.append(b)
    specs.insert(0, 'sc:14:-1'); rows.insert(0, base)
    # cross-check two seeds against seeds.py itself
    for sp in ('sc:14:3', 'sc2:14:2:7'):
        assert np.array_equal(rows[specs.index(sp)], fl.bits_from_cells(v, list(seeds.make(sp))))
    return specs, np.array(rows)


def prepare(out, burst=1000):
    from gsim import fl
    from postpeel import node_map
    v46 = fl.Vessel(fl.octa_hull(46, 'v'), 'v', True)
    v40 = fl.Vessel(fl.octa_hull(40, 'v'), 'v', True)
    specs, B = specs_and_bits(v46)
    S = fl.Sim(v46, W=(len(B) + 63) // 64)
    X = np.zeros((S.R, v46.n), bool); X[:len(B)] = B; S.set_all(X)
    S.run(burst, record=False)
    st = S.get_all()[:len(B)]
    L1 = np.abs(v46.cells[v46.rep] - 1).sum(1)
    rad = np.array([L1[r].max() if r.any() else -1 for r in st])
    keep, seen = [], set()
    for i in np.nonzero(rad == 40)[0]:
        key = st[i].tobytes()
        if key not in seen:
            seen.add(key); keep.append(i)
    mp = node_map(v46, v40)
    S40 = np.zeros((len(keep), v40.n), bool)
    for j, i in enumerate(keep):
        assert not st[i][mp < 0].any()
        S40[j, mp[mp >= 0]] = st[i][mp >= 0]
    hist = {int(k): int(n) for k, n in zip(*np.unique(rad, return_counts=True))}
    np.savez_compressed(out, specs=np.array([specs[i] for i in keep]), states=np.packbits(S40, axis=1), n=v40.n,
                        hist=json.dumps(hist), nseeds=len(specs), burst=burst)
    print(f'{len(specs)} seeds; radius at generation {burst}: {hist}; {len(keep)} distinct lineages at R = 40 -> {out}')


def run(states, cap_tau=12.0, log=print, pw=128):
    """chain R = 40 -> 38 -> 36 on the GPU; states: (k, n40) bool at generation 1000. Returns per lineage and radius:
    wait, kind (1 died, 2/3 settled, 0 censored at the cap)."""
    import gsim
    from gsim import fl
    from postpeel import node_map, shrink
    out = {}
    cur = states
    alive_idx = np.arange(len(states))
    t_start = time.time()
    for R in (40, 38, 36):
        v = fl.Vessel(fl.octa_hull(R, 'v'), 'v', True)
        s = gsim.Sim(v, backend='gpu', keep=True, pw=pw)
        assert len(cur) <= s.R
        bits = np.zeros((s.R, v.n), bool); bits[:len(cur)] = cur
        s.set_all(bits)
        k = len(cur)
        w = np.full(s.R, -1, np.int64); kind = np.zeros(s.R, np.int64)
        cap = int(cap_tau * TAU[R]); g, K = 0, 1024
        while g < cap and (w[:k] < 0).any():
            reps, tt, kk = s.step(K)
            for r, t, kd in zip(reps, tt, kk):
                w[r] = g + t; kind[r] = kd
            g += K
            K = min(K * 2, 1 << 18)
        cen = w[:k] < 0
        w[:k][cen] = g
        died = (kind[:k] == 1) & ~cen
        out[R] = dict(lineage=alive_idx.tolist(), wait=w[:k].tolist(), kind=np.where(cen, 0, kind[:k]).tolist())
        log(json.dumps(dict(R=R, lineages=int(k), died=int(died.sum()), settled=int(((kind[:k] >= 2) & ~cen).sum()),
                            censored=int(cen.sum()), gens=g, wall=round(time.time() - t_start))))
        if R == 36:
            break
        nxt = s.get_lanes(np.nonzero(died)[0])           # states kept at the peel
        vn = fl.Vessel(shrink(v.hull), 'v', True)
        mp = node_map(v, vn)
        assert not nxt[:, mp < 0].any()
        cur = np.zeros((len(nxt), vn.n), bool); cur[:, mp[mp >= 0]] = nxt[:, mp >= 0]
        alive_idx = alive_idx[np.nonzero(died)[0]]
    return out


def analyse(path):
    d = json.load(open(path))
    res = d['result']
    print(f'{d["lineages"]} distinct cube-like lineages at R = 40 (of {d["nseeds"]} seeds; radius at generation 1000: '
          f'{d["hist"]})')
    for R in ('40', '38', '36'):
        r = res[R]
        w, k = np.array(r['wait'], float), np.array(r['kind'])
        ok = k < 2                                        # settled lives excluded
        x = w[ok] / TAU[int(R)]; died = k[ok] == 1
        n = len(x); nd = int(died.sum())
        mean = x.sum() / max(nd, 1)                       # exposure / deaths in units of tau, censoring at the cap
        xs = np.sort(x[died])
        ks = float(np.max(np.abs(np.arange(1, nd + 1) / n - (1 - np.exp(-xs))))) if nd else float('nan')
        lab = 'first plateau' if R == '40' else 'after a peel'
        print(f'  R = {R} ({lab}): {n} lineages ({int((k >= 2).sum())} settled, excluded; {int((k == 0).sum())} censored at '
              f'{12} tau): mean T/tau {mean:.3f} +- {mean / math.sqrt(max(nd, 1)):.3f}, CV {x[died].std() / x[died].mean():.3f} '
              f'(uncensored), > 4 tau {(x >= 4).mean():.4f} ({(x >= 4).sum()}; exponential {math.exp(-4) * n:.1f}), '
              f'< 0.05 tau {(x < 0.05).mean():.4f} ({(x < 0.05).sum()}; {(1 - math.exp(-0.05)) * n:.1f}), KS {ks:.4f} '
              f'(5% critical {1.36 / math.sqrt(n):.4f})')


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare(sys.argv[2])
    elif sys.argv[1] == 'analyse':
        analyse(sys.argv[2])
