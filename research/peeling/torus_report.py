#!/usr/bin/env python3
"""torus.csv from scratch/peeling/torus.jsonl: whole-torus soups, lifetime (MLE, censored at cap) and death mode."""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import exp_fit
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for l in open(os.path.join(HERE, '..', 'scratch', 'peeling', 'torus.jsonl')):
    r = json.loads(l); st = np.array([x['settle'] for x in r['reps']]); pop = np.array([x['pop'] for x in r['reps']])
    obs = st >= 0; t = np.where(obs, st, r['gen_end'])
    fw = np.array([min([f for f in x['fw'] if f is not None], default=np.inf) for x in r['reps']])
    mean, (lo, hi), k = exp_fit(t, obs)
    rows.append(dict(N=r['N'], cells=3 * r['N'] ** 3, p=r['p'], replicas=len(t), died=int(k), extinct=int(np.sum(obs & (pop == 0))),
                     froze_ash=int(np.sum(obs & (pop > 0))), firewall_before_end=int(np.sum(obs & (fw < t - 16))),
                     mean_life=round(mean, 1), ci_lo=round(lo, 1), ci_hi=round(hi, 1), cap=r['cap'],
                     cv=round(t[obs].std() / t[obs].mean(), 2) if k > 1 else ''))
with open(os.path.join(HERE, 'torus.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
