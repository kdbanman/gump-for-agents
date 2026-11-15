#!/usr/bin/env python3
"""Bounds on "zombie lives" from the committed logs only (no GPU, no new runs).

A zombie is a replica that has settled into a cycle the settle test does not catch (period > pw; > 2 for the runs that
predate kind 3 and for the patch runs, which step one generation per launch). It never dies and is never frozen, so
it keeps adding exposure to the end of the run (there is no age cap) and enters the estimate as a censored life.

  python3 research/gpu/zombies.py            # every table of README "Zombie lives"

Lifetime runs (gpu_facelaw/*.json, facelaw and fwslab files with age bins). Per-replica hazard h = deaths / exposure.
For each age threshold a = k/h (k = 1, 2, 3, 5; first bin edge at or above it) compare the deaths in the bins above a with
h x their exposure. A zombie adds exposure there and no deaths, so

  Z(>a) <= E(>a) - D95(>a) / h,      D95 = one-sided 95% lower Poisson bound on the deaths (Wilson-Hilferty),

and Z(>a) / E is printed. Zombies younger than a escape this test; if they are born at a constant rate through a
run of length G, the fraction of their exposure above age a is (1 - a/G)^2, so the whole-run bound is
Z(>a) / (1 - a/G)^2 ("all ages"), printed for the first threshold at or above 2 mean lives (h is fitted to the
same deaths, most of which lie below 2/h, so the test is weakest there), else for the lowest threshold with data.
"oldest bin" is the top edge of the oldest age bin with exposure, in mean lives (bins are a factor 1.78 wide). The bound is of the exposure fraction,
which is the bias in ln tau to first order. Runs shorter than about one mean life (G*h < 1) give no age bound: a
zombie looks like any other old replica; for those, each zombie adds about 1/R of the exposure.

Patch runs (gpu_patches/*.csv): a zombie whose cycle contains an empty patch adds hits at a fixed rate from its birth
on, in one seed; the per-seed and per-half counts of the largest well-sampled shapes are printed.
"""
import glob, json, math, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def lower95(n):
    """one-sided 95% lower confidence bound on a Poisson mean given n counts (Wilson-Hilferty)"""
    if n <= 0:
        return 0.0
    return n * (1 - 1 / (9 * n) - 1.645 / (3 * math.sqrt(n))) ** 3


def age_bound(edges, deaths, exposure, G):
    e = np.asarray(edges, float); d = np.asarray(deaths); x = np.asarray(exposure, float)
    n = min(len(e) - 1, len(d), len(x)); e, d, x = e[:n + 1], d[:n], x[:n]
    E = x.sum(); h = d.sum() / E
    rows = []
    seen = set()
    for k in (1, 2, 3, 5):
        sel = e[:-1] >= k / h
        if not sel.any() or x[sel].sum() == 0:
            continue
        a = e[:-1][sel][0]
        if a in seen:
            continue
        seen.add(a); Eb = x[sel].sum(); Db = int(d[sel].sum())
        Z = max(0.0, Eb - lower95(Db) / h) / E
        rows.append(dict(a_h=a * h, D=Db, expected=h * Eb, Z=Z, Z_all=Z / max(1e-12, 1 - a / G) ** 2))
    oldest = e[np.nonzero(x)[0].max() + 1] * h
    return h, rows, oldest


def lifetime_runs():
    out = []
    for p in sorted(glob.glob(os.path.join(DATA, 'gpu_facelaw', '*.json'))):
        r = json.load(open(p)); name = os.path.basename(p)[:-5].replace('_A10G', '')
        if 'agg' in r and 'bins' in r:                       # facelaw.py: replica lives, T0 = 200 aggregate
            a = r['agg']['200']
            edges, deaths, exposure = r['bins']['edges'], r['bins']['deaths'], r['bins']['exposure']
            settled = a.get('settled', 0); R = r['replicas']
        elif 'hist' in r and 'deaths' in r['hist']:                                    # fwslab.py: kinds 1 (face) and 4 (firewall) end a life
            hd = r['hist']['deaths']
            edges, exposure = r['hist']['edges'], r['hist']['exposure']
            deaths = np.add(hd['1'], hd['4'])
            settled = int(np.sum(hd['2']) + np.sum(hd['3'])); R = r['replicas']
        elif 'exposure' in r and 'face' in r:                # early fwslab files: totals only, no age bins
            h = (r['face'] + r['fw']) / r['exposure']
            out.append(dict(run=name, R=r['replicas'], Gh=r['gens'] * h, lives_ended=r['face'] + r['fw'], settled=None,
                            oldest=float('nan'), rows=[]))
            continue
        else:
            continue
        h, rows, oldest = age_bound(edges, deaths, exposure, r['gens'])
        out.append(dict(run=name, R=R, Gh=r['gens'] * h, lives_ended=int(np.sum(deaths)) + settled, settled=settled,
                        oldest=oldest, rows=rows))
    return out


def patch_runs():
    sys.path.insert(0, HERE)
    import patches
    paths = sorted(glob.glob(os.path.join(DATA, 'gpu_patches', 'patches_s81*_A10G.csv')))
    seeds, meta, H, H2, S = patches.load_csv(paths)
    names = [m['name'] for m in meta]
    nb = len(H) // len(seeds)
    res = []
    for s in ('rhombus 4x4', 'rhombus 4x5'):
        j = names.index(s); x = H[:, j].reshape(len(seeds), nb); x2 = H2[:, j].reshape(len(seeds), nb)
        res.append(dict(shape=s, per_seed=x.sum(1).tolist(), halves=[(int(r[:nb // 2].sum()), int(r[nb // 2:].sum())) for r in x],
                        persistence=(x2.sum(1) / np.maximum(1, x.sum(1))).round(3).tolist()))
    return seeds, res


def main():
    print('Lifetime runs (h = deaths / exposure over all ages): zombie exposure / total exposure, one-sided 95% upper bound (age test)')
    print(f'{"run":24s} {"G*h":>8s} {"lives ended":>11s} {"settled<=pw":>11s} {"oldest bin":>10s}  bounds above age a (a in mean lives)')
    for L in lifetime_runs():
        b = ' | '.join(f'>{r["a_h"]:.1f}: D {r["D"]} vs {r["expected"]:.0f}, Z <= {r["Z"]:.1e}' for r in L['rows'])
        pick = next((r for r in L['rows'] if r['a_h'] >= 2), L['rows'][0] if L['rows'] else None)
        allages = f'  [all ages (from >{pick["a_h"]:.1f}), uniform births: <= {pick["Z_all"]:.1e}]' if pick else \
            (f'  [no age bins in this file]' if L['settled'] is None else
             f'  [no age bound: G*h < 1 or no exposure past 2 mean lives; one zombie ~ 1/R = {1 / L["R"]:.1e}]')
        print(f'{L["run"]:24s} {L["Gh"]:8.2f} {L["lives_ended"]:11d} {L["settled"] if L["settled"] is not None else "-":>11} {L["oldest"]:10.1f}  {b}{allages}')
    print('\nPatch runs (12x12x8): hits per seed, per half-run, and persistence P(t,t+1)/P(t) per seed')
    seeds, res = patch_runs()
    for r in res:
        print(f'  {r["shape"]:12s} seeds {",".join(seeds)}: {r["per_seed"]}; halves {r["halves"]}; persistence {r["persistence"]}')


if __name__ == '__main__':
    main()
