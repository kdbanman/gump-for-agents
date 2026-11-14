#!/usr/bin/env python3
"""Claim c: the cube-like plateau table re-derived from research/data/gpu_facelaw/cubelike_v40.json with own code,
the tau used per plateau re-derived from the fresh-soup files, and checks of the selection.

  python3 research/audit/gpu_pr12/cubelike_own.py PR12_WORKTREE
"""
import json, math, os, sys, itertools
import numpy as np
from scipy import stats
PR = sys.argv[1]
D = os.path.join(PR, 'research', 'data', 'gpu_facelaw')
d = json.load(open(os.path.join(D, 'cubelike_v40.json')))
TAU = {}
for R, f in ((40, 'symvR40_s103_A10G.json'), (38, 'symvR38_s102_A10G.json'), (36, 'symvR36_s101_A10G.json')):
    r = json.load(open(os.path.join(D, f)))
    assert r['sym'] and r['centre'] == 'v' and r['R'] == R
    a = r['agg']['1000']; TAU[R] = a['exposure'] / a['deaths']
    print(f'tau({R}) from {f}: exposure / deaths after T0 = 1000 = {TAU[R]:.4g} (ln {math.log(TAU[R]):.3f} +- '
          f'{1 / math.sqrt(a["deaths"]):.4f}); {a["deaths"]} deaths')
specs = d['specs']; hist = {int(k): v for k, v in d['hist'].items()}
n1 = 1 + 36 + 36 * 35 // 2 + 36 * 35 * 34 // 6
print(f'\nseeds {d["nseeds"]} (1 + C(36,1) + C(36,2) + C(36,3) = {n1}); radius at generation {d["burst"]}: {dict(sorted(hist.items()))}')
print(f'  at R = 40: {hist[40]} ({hist[40] / d["nseeds"]:.1%}); below 40: {sum(v for k, v in hist.items() if k < 40)}; '
      f'above 40 (still at 42-46): {sum(v for k, v in hist.items() if k > 40)}; kept distinct {len(specs)}')
print(f'  the side-16 cube itself (sc:14:-1) kept: {"sc:14:-1" in specs}; kinds of seed kept: '
      f'{ {p: sum(s.startswith(p + ":") for s in specs) for p in ("sc", "sc2", "sc3")} }')
res = d['result']
prev = None
print('\nplateau  n  settled(excl)  censored  mean T/tau (exposure/deaths)  CV  >4tau (exp)  <0.05tau (exp)  KS (crit)  KS p')
for R in (40, 38, 36):
    r = res[str(R)]
    lin = np.array(r['lineage']); w = np.array(r['wait'], float); k = np.array(r['kind'])
    if prev is not None:
        assert set(lin.tolist()) == prev, 'lineages at R are exactly those that died at the previous R'
    prev = set(lin[k == 1].tolist())
    ok = k < 2; x = w[ok] / TAU[R]; died = k[ok] == 1; n = len(x); nd = int(died.sum())
    mean = x.sum() / nd
    cv = x[died].std() / x[died].mean()
    b4 = int((x >= 4).sum()); s05 = int((x < 0.05).sum())
    ks = stats.kstest(x[died], 'expon') if nd == n else None
    # the same with settled lives censored at their settle generation instead of excluded
    xs = w / TAU[R]; dd = k == 1
    mean_c = xs.sum() / dd.sum()
    # binomial z of the tails
    z4 = (b4 - n * math.exp(-4)) / math.sqrt(n * math.exp(-4) * (1 - math.exp(-4)))
    p5 = 1 - math.exp(-0.05); z5 = (s05 - n * p5) / math.sqrt(n * p5 * (1 - p5))
    print(f'R={R}  {n}  {int((k >= 2).sum())}  {int((k == 0).sum())}  {mean:.3f} +- {mean / math.sqrt(nd):.3f} '
          f'(settled censored instead: {mean_c:.3f})  {cv:.3f}  {b4} ({n * math.exp(-4):.1f}, z {z4:+.1f})  '
          f'{s05} ({n * p5:.1f}, z {z5:+.1f})  {ks.statistic:.4f} ({1.36 / math.sqrt(n):.4f})  {ks.pvalue:.2f}')
    sw = w[k >= 2] / TAU[R]
    print(f'     settled lineages at T/tau: {np.round(np.sort(sw), 3).tolist()}')
    # near-duplicate lineages: identical waits. Waits < 1000 are double peels (the next layer within a few
    # generations), which coincide by construction; above that, compare with the chance level
    ww = w[(k == 1) & (w >= 1000)]
    vals, cnt = np.unique(ww, return_counts=True); pairs = int((cnt * (cnt - 1) // 2).sum())
    dens = np.histogram(ww, bins=200)[0]; width = (ww.max() - ww.min()) / 200
    exp_pairs = float((dens * (dens - 1) / 2).sum() / width)
    print(f'     waits < 1000 generations (double peels): {int(((k == 1) & (w < 1000)).sum())}; equal waits >= 1000: '
          f'{pairs} pairs, chance expectation {exp_pairs:.2f}')
# correlation of successive plateaus within a lineage (memory between plateaus)
w40 = dict(zip(res['40']['lineage'], res['40']['wait'])); w38 = dict(zip(res['38']['lineage'], res['38']['wait']))
w36 = dict(zip(res['36']['lineage'], res['36']['wait']))
k38 = dict(zip(res['38']['lineage'], res['38']['kind'])); k36 = dict(zip(res['36']['lineage'], res['36']['kind']))
c1 = [l for l in w38 if k38[l] == 1]; c2 = [l for l in w36 if k36[l] == 1 and l in w38]
r1 = stats.spearmanr([w40[l] for l in c1], [w38[l] for l in c1]); r2 = stats.spearmanr([w38[l] for l in c2], [w36[l] for l in c2])
print(f'\nSpearman rho between successive plateaus of a lineage: 40-38 {r1.statistic:+.3f} (p {r1.pvalue:.4f}, n {len(c1)}), '
      f'38-36 {r2.statistic:+.3f} (p {r2.pvalue:.2f}, n {len(c2)})')
a40 = np.array([w40[l] for l in c1]) / TAU[40]; b38 = np.array([w38[l] for l in c1]) / TAU[38]
for lo in (0.05, 0.3):
    m = a40 > lo; rr = stats.spearmanr(a40[m], b38[m])
    print(f'  40-38 restricted to R = 40 waits > {lo} tau: rho {rr.statistic:+.3f} (p {rr.pvalue:.3f}, n {m.sum()})')
q = np.quantile(a40, [0, .25, .5, .75, 1])
print('  mean R = 38 wait / tau(38) by quartile of the R = 40 wait: ' + ', '.join(
    f'[{lo:.2f},{hi:.2f}] tau: {b38[(a40 >= lo) & (a40 <= hi)].mean():.3f} +- {b38[(a40 >= lo) & (a40 <= hi)].mean() / math.sqrt(((a40 >= lo) & (a40 <= hi)).sum()):.3f}'
    for lo, hi in zip(q[:-1], q[1:])))
# what probability does this ensemble assign to a 6.1 tau plateau at R = 40
x40 = np.array(res['40']['wait'], float) / TAU[40]
print(f'fraction of cube-like R = 40 waits >= 6.1 tau: {(x40 >= 6.1).sum()} of {len(x40)} (exponential: {math.exp(-6.1) * len(x40):.1f}); '
      f'max {x40.max():.2f} tau')
# how far the experiment's power reaches: the largest admixture of a long-lived subpopulation consistent with the tail
for mult in (3, 6):
    # mixture (1-f) Exp(1) + f Exp(mult): 95% upper limit on f from the > 4 tau count (Poisson)
    n = len(x40); obs = int((x40 >= 4).sum()); up = stats.poisson.ppf(0.975, obs) if obs else 3
    p0, p1 = math.exp(-4), math.exp(-4 / mult)
    print(f'  95% upper bound on a fraction f of lineages with mean {mult} tau at R = 40 (from the > 4 tau count {obs}): '
          f'f < {(up / n - p0) / (p1 - p0):.3f}')
