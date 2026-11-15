#!/usr/bin/env python3
"""The quantities each forecast of PREDICTIONS.md is scored on, from data/vessels.jsonl.

  python3 research/statespace/score.py
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as AN

rows = [AN.derived(r) for r in AN.load()]
fams = ['hull', 'slab3all', 'slab2', 'slab1', 'torus']
fam = lambda r: 'hull' if r['family'] in ('hull', 'hullbig') else r['family']


def fit(xs, ys):
    return np.polyfit(xs, ys, 1)


print('E1: share without predecessor, range over vessels with N >= 15:',
      f"{min(r['goe_share'] for r in rows if r['N'] >= 15):.3f}-{max(r['goe_share'] for r in rows if r['N'] >= 15):.3f}")
for f in fams:
    rs = [r for r in rows if fam(r) == f and r['N'] >= 9]
    co = fit([r['N'] for r in rs], [math.log2(r['image_t'][1]) for r in rs])
    big = max(rs, key=lambda r: r['N'])
    print(f'   {f}: slope of log2|f(S)| against N {co[0]:.3f} (N 9..{big["N"]}); at the largest N log2|f(S)|/N = {big["b_image1"]:.3f}')
print('E2: slope of log2(cyclic) against N, and share of cyclic states with period <= 2 (min over vessels N >= 15)')
for f in fams:
    rs = [r for r in rows if fam(r) == f and r['N'] >= 9]
    co = fit([r['N'] for r in rs], [math.log2(r['cyclic_states']) for r in rs])
    big = max(rs, key=lambda r: r['N'])
    print(f'   {f}: slope {co[0]:.3f}; at the largest N log2(cyclic)/N = {big["b_cyclic"]:.3f}; '
          f'p<=2 share of cyclic states min {min(r["p12_states_share"] for r in rs if r["N"] >= 15):.3f}')
print('E3: ratio max/mean transient, smallest and largest vessel (N >= 9) of each family')
for f in fams:
    rs = sorted([r for r in rows if fam(r) == f and r['N'] >= 9], key=lambda r: r['N'])
    if f == 'hull':
        rec = AN.record_rows(); rs = sorted([r for (ff, N), r in rec.items() if ff == 'hull' and N >= 9], key=lambda r: r['N'])
    a, b = rs[0], rs[-1]
    print(f"   {f}: N={a['N']} {a['max_transient'] / a['mean_transient']:.2f}  ->  N={b['N']} {b['max_transient'] / b['mean_transient']:.2f}")
print('E4/I2: mean transient: fit of ln(mean transient) against the cells of one layer (A = N/m for slabs)')
for f in fams:
    rs = [r for r in rows if fam(r) == f and r['N'] >= 9]
    m = {'slab3all': 3, 'slab2': 2, 'slab1': 1}.get(f, 1)
    co = fit([r['N'] / m for r in rs], [math.log(r['mean_transient']) for r in rs])
    print(f"   {f}: d ln(mean transient)/dA = {co[0]:.3f};  max mean transient {max(r['mean_transient'] for r in rs):.2f}")
print('E5: champions with a nontrivial stabiliser (among the first 64 listed) in vessels with N >= 19:',
      [r['name'] for r in rows if r['N'] >= 19 and max(r['champion_stabilisers']) > 1])
print('E6: share of the eventual loss in bits (N - log2 cyclic) reached by t = 3; min / median / max over N >= 15')
for f in fams:
    v = [r['loss_share_t3'] for r in rows if fam(r) == f and r['N'] >= 15]
    print(f'   {f}: {min(v):.2f} / {np.median(v):.2f} / {max(v):.2f} ({len(v)} vessels, {sum(x > 0.5 for x in v)} above 0.5)')
print('I1: vessels (N >= 9) whose largest basin is not the empty state:',
      [(r['name'], round(r['big_share'], 3), round(r['empty_share'], 3)) for r in rows if r['N'] >= 9 and r['top_basins'][0][2] != '0'])
print('    hulls (N >= 9) whose empty basin holds less than half the seeds:',
      sum(1 for r in rows if fam(r) == 'hull' and r['N'] >= 9 and r['empty_share'] < 0.5), 'of',
      sum(1 for r in rows if fam(r) == 'hull' and r['N'] >= 9))
print('I3: vessels with max transient >= 2N:', [(r['name'], r['max_transient']) for r in rows if r['max_transient'] >= 2 * r['N']])
print('I4: min share without predecessor over N >= 15:', f"{min(r['goe_share'] for r in rows if r['N'] >= 15):.3f}",
      [(r['name'], round(r['goe_share'], 3)) for r in rows if r['N'] >= 15 and r['goe_share'] <= 0.8][:12])
print('I5: vessels with N >= 20 whose cyclic states exceed sqrt(pi M/2):',
      [(r['name'], r['cyclic_states'], round(r['rm_rho'])) for r in rows if r['N'] >= 20 and r['cyclic_states'] > r['rm_rho']])
print('    of', sum(1 for r in rows if r['N'] >= 20))
print('I6: at the largest N of each family: champion log2(visited)/N, mean-seed log2(mean visited)/N, mean of log2 visited / N')
for f in fams:
    rs = [r for r in rows if fam(r) == f]
    Nm = max(r['N'] for r in rs)
    for r in [r for r in rs if r['N'] == Nm]:
        print(f"   {r['name']}: {r['b_champ']:.3f}, {r['b_mean_vis']:.3f}, {r['mean_log2_visited'] / r['N']:.3f}")
