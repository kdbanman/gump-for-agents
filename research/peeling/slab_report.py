#!/usr/bin/env python3
"""Curated tables from research/scratch/peeling/slabs.jsonl.

slab_area.csv       first-peel statistics per (N1, N2, m) batch: events, censoring, MLE mean with 95% CI, CV, KS p
slab_thickness.csv  per area A and current thickness m': peel hazard pooled over all histories (exposure, events)
slab_fw.csv         competing first events per batch: transverse T3 firewall vs face peel vs freeze, with
                    the transverse cut size (3 x smallest transverse layer) and the face area
slab_end.csv        how slab histories end, per batch: thickness when chaos stopped, fraction frozen vs extinct, transverse firewall first
"""
import csv, json, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import exp_fit, exp_tests
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', 'scratch', 'peeling')
recs = [json.loads(l) for l in open(os.path.join(S, 'slabs.jsonl'))]

area_rows, thick, end_rows, fw_rows = [], defaultdict(lambda: [0, 0.0]), [], []
import geom
for r in recs:
    ge = r['gen_end']
    first = np.array([x['peels'][0][0] if x['peels'] else np.inf for x in r['reps']])
    st = np.array([x['settle'] for x in r['reps']])
    stop = np.where(st >= 0, st, ge).astype(float)
    obs = first < stop + 1e-9
    t = np.where(obs, first, stop)
    fwb = np.array([x['fw'] is not None and x['fw'] < f for x, f in zip(r['reps'], first)])
    mean, (lo, hi), k = exp_fit(t, obs)
    cv, p = exp_tests(t[obs]) if obs.mean() > 0.98 else (np.nan, np.nan)
    area_rows.append(dict(N1=r['N1'], N2=r['N2'], A=r['A'], m=r['m'], seed=r['seed'], replicas=len(t), peels=int(k),
                          frozen=int(np.sum(~obs & (st >= 0))), censored=int(np.sum(~obs & (st < 0))),
                          fw_before_peel=int(fwb.sum()), mean_first=round(mean, 1), ci_lo=round(lo, 1), ci_hi=round(hi, 1),
                          cv=round(cv, 3), ks_p=round(p, 3), cap=r['cap']))
    # competing first events: transverse firewall / peel / freeze / censored
    fwt = np.array([x['fw'] if x['fw'] is not None else np.inf for x in r['reps']])
    tend = np.minimum.reduce([fwt, first, stop])
    is_fw = (fwt <= first) & (fwt <= stop) & (fwt < np.inf)
    is_pe = (first < fwt) & (first <= stop)
    v = geom.slab(r['N1'], r['m'], r['N2'])
    lay = min(len(i) for k, i in v.layers if k[0] > 0)
    T = tend.sum()
    fw_rows.append(dict(N1=r['N1'], N2=r['N2'], m=r['m'], A=r['A'], cut=3 * lay, replicas=len(t), fw_first=int(is_fw.sum()),
                        peel_first=int(is_pe.sum()), freeze_first=int(np.sum(~is_fw & ~is_pe & (st >= 0))),
                        exposure=round(T), mean_fw=round(T / is_fw.sum(), 1) if is_fw.sum() else '',
                        mean_peel=round(T / is_pe.sum(), 1) if is_pe.sum() else '',
                        life_mean=round(float(np.mean(np.where(st >= 0, st, ge))), 1), life_censored=int(np.sum(st < 0))))
    # histories: thickness m' from m down; exposure at each m' until the next peel or the end of activity
    ends = defaultdict(int)
    for x, s_ in zip(r['reps'], stop):
        mm, t0 = r['m'], 0.0
        for tp, side in x['peels']:
            if tp > s_:
                break
            thick[(r['A'], r['N1'], r['N2'], mm)][1] += tp - t0
            thick[(r['A'], r['N1'], r['N2'], mm)][0] += 1
            mm, t0 = mm - 1, tp
        if mm > 0 and s_ > t0:
            thick[(r['A'], r['N1'], r['N2'], mm)][1] += s_ - t0
        ends[mm if x['settle'] >= 0 else 'running'] += 1
    end_rows.append(dict(N1=r['N1'], N2=r['N2'], A=r['A'], m=r['m'], seed=r['seed'],
                         ends=' '.join(f'{k}:{v}' for k, v in sorted(ends.items(), key=lambda kv: str(kv[0]))),
                         extinct=int(sum(1 for x in r['reps'] if x['settle'] >= 0 and x['pop'] == 0)),
                         fw_ever=int(sum(1 for x in r['reps'] if x['fw'] is not None))))


def write(name, rows):
    with open(os.path.join(HERE, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


write('slab_area.csv', sorted(area_rows, key=lambda d: (d['m'], d['A'], d['N1'])))
trows = []
for (A, N1, N2, mm), (k, T) in sorted(thick.items()):
    trows.append(dict(A=A, N1=N1, N2=N2, m_now=mm, peels=k, exposure=round(T), mean_wait=round(T / k, 1) if k else '',
                      ci_lo=round(2 * T / stats.chi2.ppf(0.975, 2 * k), 1) if k else round(T / 3, 1),
                      ci_hi=round(2 * T / stats.chi2.ppf(0.025, 2 * k), 1) if k else ''))
write('slab_thickness.csv', trows)
write('slab_end.csv', end_rows)
write('slab_fw.csv', sorted(fw_rows, key=lambda d: (d['m'], d['A'])))
for d in sorted(area_rows, key=lambda d: (d['m'], d['A'])):
    print(d)
