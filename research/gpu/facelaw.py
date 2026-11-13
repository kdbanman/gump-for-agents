#!/usr/bin/env python3
"""Face law for asymmetric octahedral soups on the GPU: wait from age T0 to the first death of any face layer.

Same statistic as research/experiments/verify_face_law.py / engine/scripts/face_law.py (soup p = 0.35 in |p|_1 <= R,
open space, exact by T2): a replica is a fresh soup; its life ends when some face layer of the initial hull is extinct
(kind 1), when it settles into period 1 or 2 (kind 2), or when the run stops (kind 0, censored). Every life's end age
and kind are kept, so any T0 can be applied afterwards; lives that end before T0 are excluded (the engine scripts'
"full hull at T0"). Estimator: mean wait = total exposure after T0 / number of deaths (exponential waits).

  modal run research/gpu/modal_app.py::facelaw --r 15 --minutes 30 --seed 1 --gpu A10G
  python3 research/gpu/facelaw.py summary research/data/gpu_facelaw/R15_*.json
"""
import glob, json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

AREA = lambda R: 3 * ((R - 1) // 2 + 1) * ((R - 1) // 2 + 2) // 2
SLAB_LAW = lambda A: math.exp(-0.09 + 0.209 * A)          # tau_face, research/STATUS.md


def run(R, wall_s, seed, p=0.35, launch_s=1.0, log=print, **cfg):
    import cupy as cp
    import gsim
    from gsim import fl
    v = fl.Vessel(fl.octa_hull(R), 'c', sym=False)
    s = gsim.Sim(v, backend='gpu', seedable=gsim.seed_mask(v, R), **cfg)
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)       # soup_bit hashes seed and replica separately
    birth = np.zeros(s.R, np.int64)
    ages, kinds = [], []
    G, rnd, K = 0, 1, 1024
    t_start = time.time()
    last_log = t_start
    while time.time() - t_start < wall_s:
        t = time.time()
        reps, tt, kk = s.step(K)
        cp.cuda.Device().synchronize()
        dt = time.time() - t
        if len(reps):
            ages.append(G + tt - birth[reps]); kinds.append(kk)
        G += K
        if len(reps):
            s.reseed(reps, seed=(seed << 32) + rnd, p=p); rnd += 1
            birth[reps] = G
        if dt < launch_s / 2 and K < 1 << 24:
            K *= 2
        if time.time() - last_log > 120:
            a = np.concatenate(ages) if ages else np.zeros(0); k = np.concatenate(kinds) if kinds else np.zeros(0)
            log(json.dumps(dict(R=R, gen=G, launch=K, elapsed=round(time.time() - t_start), deaths_after_200=int(((k == 1) & (a >= 200)).sum()),
                                early=int((a < 200).sum()), settled=int((k == 2).sum()))))
            last_log = time.time()
    ages.append(G - birth); kinds.append(np.zeros(s.R, np.int64))
    ages, kinds = np.concatenate(ages), np.concatenate(kinds)
    return dict(R=R, A=v.A, seed=seed, p=p, gens=G, replicas=s.R, nodes=v.n, wall_s=time.time() - t_start,
                config=dict(WB=s.WB, J=s.J, T=s.T, blocks=s.blocks), **compact(ages, kinds))


T0S = (60, 200, 1000, 10000)
EDGES = [0, 60, 200, 1000] + [int(round(10 ** (3 + i / 4))) for i in range(1, 49)]   # to 1e15


def compact(ages, kinds):
    """small, mergeable summary of all lives (Modal results above a few MB go through a blob host this environment
    does not reach): exact per-T0 aggregates, deaths and exposure per age bin, raw death ages if there are few."""
    agg = {}
    for T0 in T0S:
        keep = ages >= T0
        agg[T0] = dict(deaths=int(((kinds == 1) & keep).sum()), settled=int(((kinds == 2) & keep).sum()),
                       censored=int(((kinds == 0) & keep).sum()), excluded=int((~keep).sum()),
                       exposure=int((ages[keep] - T0).sum()))
    E = np.array(EDGES, np.int64)
    bins = dict(edges=EDGES, deaths=np.histogram(ages[kinds == 1], E)[0].tolist(),
                exposure=[int(np.clip(np.minimum(ages, hi) - lo, 0, None).sum()) for lo, hi in zip(E[:-1], E[1:])])
    d = ages[kinds == 1]
    return dict(agg=agg, bins=bins, death_ages=(np.sort(d).tolist() if len(d) <= 50000 else None),
                settled_ages=np.sort(ages[kinds == 2]).tolist()[:10000], max_age=int(ages.max()))


def merge(recs):
    agg = {T0: {k: sum(r['agg'][str(T0)][k] for r in recs) for k in recs[0]['agg'][str(T0)]} for T0 in T0S}
    nb = len(EDGES) - 1
    deaths = np.sum([r['bins']['deaths'] for r in recs], 0); expo = np.sum([r['bins']['exposure'] for r in recs], 0)
    da = None if any(r['death_ages'] is None for r in recs) else np.sort(np.concatenate([r['death_ages'] for r in recs]))
    return agg, deaths[:nb], expo[:nb], da


def summary(paths):
    by_R = {}
    for p in paths:
        r = json.load(open(p))
        by_R.setdefault(r['R'], []).append(r)
    rows = []
    for R, recs in sorted(by_R.items()):
        seen = {}
        for r in recs:      # independent runs share no death age (the seed-collision bug of 2026-11-13 showed up this way)
            for a in set(r['death_ages'] or []):
                if a > 10 ** 4:
                    seen.setdefault(a, set()).add(r['seed'])
        dup = {a: sd for a, sd in seen.items() if len(sd) > 1}
        if dup:
            print(f'WARNING R={R}: runs share {len(dup)} death ages (not independent?):', list(dup.items())[:5])
        agg, deaths, expo, da = merge(recs)
        A = AREA(R)
        pred = SLAB_LAW(A) / 8
        rg = sum(r['gens'] * r['replicas'] for r in recs)
        print(f'R={R} A={A} nodes={recs[0]["nodes"]}: {len(recs)} runs, {rg:.3g} replica-generations, '
              f'{sum(r["wall_s"] for r in recs) / 3600:.2f} GPU-h, oldest replica {max(r["max_age"] for r in recs):.3g}')
        for T0 in T0S:
            a = agg[T0]
            if a['deaths'] == 0:
                print(f'  T0={T0:5d}: no deaths; exposure {a["exposure"]:.3g}'); continue
            mean = a['exposure'] / a['deaths']
            print(f'  T0={T0:5d}: deaths {a["deaths"]:7d} settled {a["settled"]} censored {a["censored"]} excluded {a["excluded"]}: '
                  f'mean first-peel wait {mean:.4g} +- {mean / math.sqrt(a["deaths"]):.2g} (ln {math.log(mean):.3f} +- '
                  f'{1 / math.sqrt(a["deaths"]):.3f}); slab law / 8 = {pred:.3g}, ratio {mean / pred:.2f}')
            rows.append(dict(R=R, A=A, T0=T0, deaths=a['deaths'], exposure=a['exposure'], mean=mean))
        if da is not None and len(da) > 2:
            w = da[da >= 200] - 200
            print(f'  CV of uncensored waits (T0=200): {w.std() / w.mean():.2f} (biased low by censoring when lives are cut short)')
        hz = [(EDGES[i], EDGES[i + 1], int(deaths[i]), int(expo[i])) for i in range(len(deaths)) if expo[i] > 0 and EDGES[i] >= 200]
        print('  hazard by age (deaths / exposure):', '; '.join(f'[{lo:.0e},{hi:.0e}) {d}/{e:.2e}={d / e:.3g}' for lo, hi, d, e in hz if d or e > 0))
    # the face law: ln tau_face = ln(8 x first-peel mean), against the straight line of research/fluct (I(0) = 0.2077 + 0.55/A)
    t = [r for r in rows if r['T0'] == 200]
    if t:
        print('\n   A   deaths   ln tau_face      fluct line 0.2077A+0.55   excess   per site   local slope')
        prev = None
        for r in t:
            lt = math.log(8 * r['mean']); se = 1 / math.sqrt(r['deaths']); line = 0.2077 * r['A'] + 0.55
            sl = f'{(lt - prev[1]) / (r["A"] - prev[0]):.4f}' if prev else ''
            print(f'{r["A"]:4d} {r["deaths"]:8d}   {lt:7.3f} +- {se:.3f}   {line:7.3f}                  {lt - line:+.2f}    {lt / r["A"]:.4f}     {sl}')
            prev = (r['A'], lt)
    return rows


if __name__ == '__main__':
    if sys.argv[1] == 'summary':
        summary(sorted(sum((glob.glob(a) for a in sys.argv[2:]), [])))
