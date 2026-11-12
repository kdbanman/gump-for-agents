#!/usr/bin/env python3
"""Tables from octa_hazard.json (run octa_hazard.py first).

octa_first.csv   per batch (R, p, sym): first peel after t0 (MLE mean, CI), lifetime (median, censoring), initial face area
octa_hazard.csv  per batch and face-area bin: events, exposure, hazard per face (sym: per 8-face family)
"""
import csv, json, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import exp_fit
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', 'scratch', 'peeling')
H = json.load(open(os.path.join(S, 'octa_hazard.json')))
recs = [json.loads(l) for l in open(os.path.join(S, 'octa.jsonl'))]


def write(name, rows):
    with open(os.path.join(HERE, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


first_rows, haz_rows = [], []
pool = defaultdict(lambda: defaultdict(lambda: [0, 0.0]))
for h, r in zip(H, recs):
    f = np.array([x[0] for x in h['first']], float); obs = np.array([not x[2] for x in h['first']])
    mean, (lo, hi), k = exp_fit(f, obs)
    life = np.array([x['settle'] if x['settle'] >= 0 else np.inf for x in r['reps']])
    A0 = [x[1] for x in h['first'] if not x[2]]
    first_rows.append(dict(R=h['R'], p=h['p'], sym=int(h['sym']) + int(h.get('vertex', False)), replicas=len(r['reps']), established=len(f), first_peels=k, mean_first=round(mean, 1),
                           ci_lo=round(lo, 1), ci_hi=round(hi, 1), cv_first=round(f[obs].std() / f[obs].mean(), 3) if k else '',
                           median_area_first=float(np.median(A0)) if A0 else '',
                           life_median=float(np.median(life)), life_censored=int(np.sum(life == np.inf)), cap=r['cap']))
    key = (h['R'], h['p'], int(h['sym']) + int(h.get('vertex', False)))
    for A, (e, T) in h['hazard'].items():
        pool[key][int(A)][0] += e; pool[key][int(A)][1] += T
for key, d in sorted(pool.items()):
    R, p, sym = key
    bw = 6 if not sym else 18
    bins = defaultdict(lambda: [0, 0.0, 0.0])
    for A, (e, T) in d.items():
        b = A // bw
        bins[b][0] += e; bins[b][1] += T; bins[b][2] += A * T
    for b, (e, T, AT) in sorted(bins.items()):
        if T <= 0:
            continue
        lo = stats.chi2.ppf(0.025, 2 * e) / (2 * T) if e else 0.0
        hi = stats.chi2.ppf(0.975, 2 * e + 2) / (2 * T)
        haz_rows.append(dict(R=R, p=p, sym=sym, A_mean=round(AT / T, 1), events=e, exposure=round(T),
                             hazard=e / T, h_lo=lo, h_hi=hi))
write('octa_first.csv', first_rows)
write('octa_hazard.csv', haz_rows)
for d in first_rows:
    print(d)
