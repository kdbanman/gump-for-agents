#!/usr/bin/env python3
"""Tables of part A (and D) from data/vessels.jsonl.

  python3 research/statespace/analyze.py [tables|scaling|hullsizes]

Random map on M states (the comparison of part D): distinct states visited from a random start ~ sqrt(pi M / 2)
(mean rho length; 1.2533 sqrt M); states on cycles ~ sqrt(pi M / 2); share without a predecessor e^-1; number of
cycles ~ (ln M)/2 + 0.29 (gamma/2 + ln(2)/2); mean tail sqrt(pi M / 8).
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FAM_ORDER = ['hull', 'slab3all', 'slab2', 'slab1', 'torus', 'hullbig']
FAM_NAME = {'hull': 'diagonal hulls', 'hullbig': 'diagonal hulls', 'slab3all': '3-layer slab tori',
            'slab2': '2-layer slab tori', 'slab1': '1-layer (kagome) tori', 'torus': '3D tori'}


def load():
    rows, seen = [], set()
    for line in open(os.path.join(HERE, 'data', 'vessels.jsonl')):
        r = json.loads(line)
        if r['name'] in seen:
            continue
        seen.add(r['name']); rows.append(r)
    return rows


def lg(x):
    return math.log2(x) if x > 0 else float('-inf')


def derived(r):
    N = r['N']; M = 2 ** N
    d = dict(r)
    d['goe_share'] = r['goe'] / M
    d['b_image1'] = lg(r['image_t'][1]) / N
    d['b_cyclic'] = lg(r['cyclic_states']) / N
    d['b_champ'] = lg(r['max_transient'] + r['champion_cycle_period']) / N
    d['b_mean_vis'] = lg(r['mean_visited']) / N
    d['rm_rho'] = math.sqrt(math.pi * M / 2)
    d['rm_cycles'] = 0.5 * math.log(M) + 0.29
    d['big_share'] = r['largest_basin'] / M
    d['empty_share'] = r['empty_basin'] / M
    per = {p: (c, s, b) for p, c, s, b in r['by_period']}
    d['p12_states_share'] = (per.get(1, (0, 0, 0))[1] + per.get(2, (0, 0, 0))[1]) / r['cyclic_states']
    d['p12_basin_share'] = (per.get(1, (0, 0, 0))[2] + per.get(2, (0, 0, 0))[2]) / M
    d['periods'] = sorted(per)
    # bits lost by generation t, as a share of the eventual loss
    tot = N - lg(r['cyclic_states'])
    im = r['image_t']
    d['loss_share_t3'] = (N - lg(im[min(3, len(im) - 1)])) / tot if tot > 0 else float('nan')
    d['loss_share_t1'] = (N - lg(im[1])) / tot if tot > 0 else float('nan')
    return d


def tables():
    rows = [derived(r) for r in load()]
    for fam in FAM_ORDER:
        fr = sorted([r for r in rows if r['family'] == fam], key=lambda r: (r['N'], r['name']))
        if not fr:
            continue
        print(f'\n### {FAM_NAME[fam]} ({fam})\n')
        print('| vessel | N | born-capable | no predecessor | log2 image(1)/N | on cycles | cycles | periods | largest basin '
              '| mean / median / max transient | mean / max visited | champions (orbits, stabiliser) |')
        print('|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|---|')
        for r in fr:
            stab = sorted(set(r['champion_stabilisers']))
            print(f"| `{r['name']}` | {r['N']} | {r['cells_deg_ge4']} | {r['goe_share']:.4f} | {r['b_image1']:.3f} | "
                  f"{r['cyclic_states']:,} | {r['cycles']:,} | {','.join(map(str, r['periods']))} | "
                  f"{r['big_share']:.3f} (p{r['top_basins'][0][1]}{', empty' if r['top_basins'][0][2] == '0' else ''}) | "
                  f"{r['mean_transient']:.2f} / {r['median_transient']} / {r['max_transient']} | "
                  f"{r['mean_visited']:.2f} / {r['max_visited']} | {r['n_champions']} "
                  f"({r['champion_orbits']}, {'/'.join(map(str, stab))} of {r['sym_order']}) |")


def hull_census():
    """per N over all diagonal hulls of N cells: min / median / max of the main counts"""
    rows = [derived(r) for r in load() if r['family'] in ('hull', 'hullbig')]
    by = {}
    for r in rows:
        by.setdefault(r['N'], []).append(r)
    print('| N | hulls | no predecessor (min-max) | log2 image(1)/N (max) | on cycles (max) | mean transient (max) | '
          'max transient (max, its hull) |')
    print('|---:|---:|---|---:|---:|---:|---|')
    for N in sorted(by):
        rs = by[N]
        best = max(rs, key=lambda r: (r['max_transient'], r['mean_transient']))
        print(f"| {N} | {len(rs)} | {min(r['goe_share'] for r in rs):.3f}-{max(r['goe_share'] for r in rs):.3f} | "
              f"{max(r['b_image1'] for r in rs):.3f} | {max(r['cyclic_states'] for r in rs):,} | "
              f"{max(r['mean_transient'] for r in rs):.2f} | {best['max_transient']} (`{best['name']}`) |")
    return by


def record_rows():
    """per family, per N: the vessel with the longest champion (for the hulls), else the family's vessel"""
    rows = [derived(r) for r in load()]
    out = {}
    for r in rows:
        fam = 'hull' if r['family'] in ('hull', 'hullbig') else r['family']
        key = (fam, r['N'])
        if key not in out or (r['max_transient'], r['mean_transient']) > (out[key]['max_transient'], out[key]['mean_transient']):
            out[key] = r
    return out


def scaling():
    rows = [derived(r) for r in load()]
    for fam in ['hull', 'slab3all', 'slab2', 'slab1', 'torus']:
        fr = [r for r in rows if (r['family'] in ('hull', 'hullbig') if fam == 'hull' else r['family'] == fam) and r['N'] >= 9]
        if len(fr) < 3:
            continue
        N = np.array([r['N'] for r in fr], float)
        for key, lab in [('b_image1', 'log2|f(S)|'), ('b_cyclic', 'log2 cyclic')]:
            y = np.array([r[key] for r in fr]) * N
            A = np.vstack([N, np.ones_like(N)]).T
            co = np.linalg.lstsq(A, y, rcond=None)[0]
            print(f'{fam:9s} {lab:12s} = {co[0]:.3f} N + {co[1]:+.2f}   (N = {int(N.min())}..{int(N.max())}, {len(fr)} vessels)')
        mt = np.array([r['mean_transient'] for r in fr]); xt = np.array([r['max_transient'] for r in fr])
        co = np.polyfit(N, mt, 1); co2 = np.polyfit(N, xt, 1)
        print(f'{fam:9s} mean transient ~ {co[0]:.3f} N {co[1]:+.2f};  max transient ~ {co2[0]:.2f} N {co2[1]:+.1f}')


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'tables'
    if what == 'tables':
        tables()
    elif what == 'hullsizes':
        hull_census()
    elif what == 'scaling':
        scaling()
