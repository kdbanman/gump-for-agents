#!/usr/bin/env python3
"""Face law for asymmetric octahedral soups on the GPU: wait from age T0 to the first death of any face layer.

Same statistic as research/experiments/verify_face_law.py / engine/scripts/face_law.py (soup p = 0.35 in |p|_1 <= R,
open space, exact by T2): a replica is a fresh soup; its life ends when some face layer of the initial hull is extinct
(kind 1), when it settles into period 1 or 2 (kind 2) or 3..128 (kind 3, kernel_shared's launch-snapshot test), or when the
run stops (kind 0, censored). Every life's end age
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


def run(R, wall_s, seed, p=0.35, launch_s=1.0, log=print, centre='c', sym=False, raw_cap=60000, **cfg):
    """asymmetric (sym=False: soup in |p - c|_1 <= R, 8 faces) or O_h-symmetric (sym=True: orbit soup over the whole
    vessel, one representative face) octahedral soups in their exact hull."""
    import cupy as cp
    import gsim
    from gsim import fl
    v = fl.Vessel(fl.octa_hull(R, centre), centre, sym)
    s = gsim.Sim(v, backend='gpu', seedable=None if sym else gsim.seed_mask(v, R), **cfg)
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)       # soup_bit hashes seed and replica separately
    birth = np.zeros(s.R, np.int64)
    ages, kinds, births = [], [], []
    G, rnd, K = 0, 1, 1024
    t_start = time.time()
    last_log = t_start
    while time.time() - t_start < wall_s:
        t = time.time()
        reps, tt, kk = s.step(K)
        cp.cuda.Device().synchronize()
        dt = time.time() - t
        if len(reps):
            ages.append(G + tt - birth[reps]); kinds.append(kk); births.append(birth[reps].copy())
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
    ages.append(G - birth); kinds.append(np.zeros(s.R, np.int64)); births.append(birth.copy())
    ages, kinds, births = np.concatenate(ages), np.concatenate(kinds), np.concatenate(births)
    T0 = 1000 if sym else 200
    out = dict(R=R, A=v.A, sym=sym, centre=centre, seed=seed, p=p, gens=G, replicas=s.R, nodes=v.n,
               wall_s=time.time() - t_start, config=dict(WB=s.WB, J=s.J, T=s.T, blocks=s.blocks), **compact(ages, kinds))
    out['lineage'] = lineage_stats(ages, kinds, births, G, T0)
    if len(ages) <= raw_cap:       # raw lives (age, kind, birth) for re-analysis; zlib + base64 to stay small
        out['raw'] = pack(np.stack([ages, kinds, births]))
    return out


def pack(a):
    import base64, zlib
    return dict(shape=list(a.shape), b64=base64.b64encode(zlib.compress(np.ascontiguousarray(a, np.int64).tobytes(), 9)).decode())


def unpack(d):
    import base64, zlib
    return np.frombuffer(zlib.decompress(base64.b64decode(d['b64'])), np.int64).reshape(d['shape'])


def trunc_exp_cv(L):
    """CV of min(X, L) for X exponential with mean 1"""
    m1 = 1 - math.exp(-L); m2 = 2 * (1 - math.exp(-L) * (1 + L))
    return math.sqrt(m2 / m1 ** 2 - 1)


def lineage_stats(ages, kinds, births, G, T0, L_mult=10):
    """memorylessness of single lineages. tau = exposure after T0 / deaths (all lives). Complete-life sample: lives born
    at least T0 + L_mult*tau before the end, so each either died (residence = age - T0) or is known to exceed
    L_mult*tau; lives that ended before T0 are excluded (as in the estimator). Kind 2 (settled) ends are reported."""
    keep = ages >= T0
    deaths = int(((kinds == 1) & keep).sum())
    if deaths == 0:
        return None
    tau = float((ages[keep] - T0).sum()) / deaths
    L = L_mult * tau
    sel = keep & (births <= G - T0 - L) & (kinds < 2)     # settled lives (kind 2: period 1-2, kind 3: 3..128) excluded
    r = (ages[sel] - T0).astype(float)
    died = (kinds[sel] == 1) & (r < L)
    x = np.where(died, r, L)
    n = int(sel.sum())
    if n < 10:
        return dict(tau=tau, deaths=deaths, complete_lives=n)
    fr = lambda m: dict(frac=float(m.mean()), se=float(math.sqrt(max(m.mean() * (1 - m.mean()), 1e-12) / n)))
    edges = np.array([0, .01, .05, .1, .25, .5, 1, 1.5, 2, 3, 4, 6, 10]) * tau
    hz = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        e = np.clip(np.minimum(x, hi) - lo, 0, None).sum()
        d = int((died & (r >= lo) & (r < hi)).sum())
        hz.append(dict(lo_tau=float(lo / tau), hi_tau=float(hi / tau), deaths=d, rate_x_tau=float(d / e * tau) if e > 0 else None))
    xs = np.sort(x[died])
    ks = float(np.max(np.abs(np.arange(1, len(xs) + 1) / n - (1 - np.exp(-xs / tau))))) if len(xs) else None
    return dict(tau=tau, deaths=deaths, settled_after_T0=int(((kinds >= 2) & keep).sum()), settled_long_after_T0=int(((kinds == 3) & keep).sum()),
                L_tau=L_mult, complete_lives=n,
                died_within_L=int(died.sum()), cv=float(x.std() / x.mean()), cv_expected=trunc_exp_cv(L_mult),
                beyond_4tau=fr(r >= 4 * tau), below_005tau=fr(r < 0.05 * tau), ks_vs_exponential=ks,
                ks_5pct_critical=float(1.36 / math.sqrt(n)), hazard_by_age=hz)


T0S = (60, 200, 1000, 10000)
EDGES = [0, 60, 200, 1000] + [int(round(10 ** (3 + i / 4))) for i in range(1, 49)]   # to 1e15


def compact(ages, kinds):
    """small, mergeable summary of all lives (Modal results above a few MB go through a blob host this environment
    does not reach): exact per-T0 aggregates, deaths and exposure per age bin, raw death ages if there are few."""
    agg = {}
    for T0 in T0S:
        keep = ages >= T0
        agg[T0] = dict(deaths=int(((kinds == 1) & keep).sum()), settled=int(((kinds >= 2) & keep).sum()),
                       settled_long=int(((kinds == 3) & keep).sum()),
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
        by_R.setdefault((r.get('sym', False), r.get('centre', 'c'), r['R']), []).append(r)
    rows = []
    for (sym, centre, R), recs in sorted(by_R.items()):
        seen = {}
        for r in recs:      # independent runs share no death age (the seed-collision bug of 2026-11-13 showed up this way)
            for a in set(r['death_ages'] or []):
                if a > 10 ** 4:
                    seen.setdefault(a, set()).add(r['seed'])
        dup = {a: sd for a, sd in seen.items() if len(sd) > 1}
        if dup:
            print(f'WARNING R={R}: runs share {len(dup)} death ages (not independent?):', list(dup.items())[:5])
        agg, deaths, expo, da = merge(recs)
        A = recs[0]['A']
        nf = 1 if sym else 8                     # symmetric: the eight faces die together, tau is the mean residence
        pred = SLAB_LAW(A) / nf
        rg = sum(r['gens'] * r['replicas'] for r in recs)
        print(f'{"O_h " + centre if sym else "asym"} R={R} A={A} nodes={recs[0]["nodes"]}: {len(recs)} runs, {rg:.3g} replica-generations, '
              f'{sum(r["wall_s"] for r in recs) / 3600:.2f} GPU-h, oldest replica {max(r["max_age"] for r in recs):.3g}')
        for T0 in T0S:
            a = agg[T0]
            if a['deaths'] == 0:
                print(f'  T0={T0:5d}: no deaths; exposure {a["exposure"]:.3g}'); continue
            mean = a['exposure'] / a['deaths']
            print(f'  T0={T0:5d}: deaths {a["deaths"]:7d} settled {a["settled"]} (period > 2: {a.get("settled_long", "n/a")}) censored {a["censored"]} excluded {a["excluded"]}: '
                  f'mean first-peel wait {mean:.4g} +- {mean / math.sqrt(a["deaths"]):.2g} (ln {math.log(mean):.3f} +- '
                  f'{1 / math.sqrt(a["deaths"]):.3f}); slab law / 8 = {pred:.3g}, ratio {mean / pred:.2f}')
            rows.append(dict(R=R, A=A, sym=sym, centre=centre, T0=T0, deaths=a['deaths'], exposure=a['exposure'], mean=mean))
        if da is not None and len(da) > 2:
            w = da[da >= 200] - 200
            print(f'  CV of uncensored waits (T0=200): {w.std() / w.mean():.2f} (biased low by censoring when lives are cut short)')
        for r in recs:
            L = r.get('lineage')
            if L and L.get('cv') is not None:
                print(f'  lineage (seed {r["seed"]}): tau {L["tau"]:.4g}, {L["complete_lives"]} complete lives ({L["died_within_L"]} died within '
                      f'{L["L_tau"]} tau): CV {L["cv"]:.4f} (exponential {L["cv_expected"]:.4f}); beyond 4 tau {L["beyond_4tau"]["frac"]:.4f} '
                      f'+- {L["beyond_4tau"]["se"]:.4f} (0.0183); below 0.05 tau {L["below_005tau"]["frac"]:.4f} +- {L["below_005tau"]["se"]:.4f} '
                      f'(0.0488); KS {L["ks_vs_exponential"]:.4f} (5% critical {L["ks_5pct_critical"]:.4f})')
                print('    hazard x tau by age/tau:', ', '.join(f'[{h["lo_tau"]:.2g},{h["hi_tau"]:.2g}) {h["rate_x_tau"]:.3f} ({h["deaths"]})'
                                                        for h in L['hazard_by_age'] if h['rate_x_tau'] is not None))
        hz = [(EDGES[i], EDGES[i + 1], int(deaths[i]), int(expo[i])) for i in range(len(deaths)) if expo[i] > 0 and EDGES[i] >= 200]
        print('  hazard by age (deaths / exposure):', '; '.join(f'[{lo:.0e},{hi:.0e}) {d}/{e:.2e}={d / e:.3g}' for lo, hi, d, e in hz if d or e > 0))
    # the face law: ln tau_face = ln(8 x first-peel mean), against the straight line of research/fluct (I(0) = 0.2077 + 0.55/A)
    t = [r for r in rows if r['T0'] == 200 and not r['sym']]
    if t:
        print('\n   A   deaths   ln tau_face      fluct line 0.2077A+0.55   excess   per site   local slope')
        prev = None
        for r in t:
            lt = math.log(8 * r['mean']); se = 1 / math.sqrt(r['deaths']); line = 0.2077 * r['A'] + 0.55
            sl = f'{(lt - prev[1]) / (r["A"] - prev[0]):.4f}' if prev else ''
            print(f'{r["A"]:4d} {r["deaths"]:8d}   {lt:7.3f} +- {se:.3f}   {line:7.3f}                  {lt - line:+.2f}    {lt / r["A"]:.4f}     {sl}')
            prev = (r['A'], lt)
    ts = [r for r in rows if r['T0'] == 1000 and r['sym']]
    if ts:
        print('\n O_h   R    A   deaths   ln tau (T0 = 1000)')
        for r in ts:
            print(f'  {r["centre"]}  {r["R"]:3d}  {r["A"]:4d} {r["deaths"]:7d}   {math.log(r["mean"]):.3f} +- {1 / math.sqrt(r["deaths"]):.3f}')
    return rows


if __name__ == '__main__':
    if sys.argv[1] == 'summary':
        summary(sorted(sum((glob.glob(a) for a in sys.argv[2:]), [])))
