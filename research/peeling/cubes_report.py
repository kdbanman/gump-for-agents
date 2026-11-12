#!/usr/bin/env python3
"""Closed-cube lifetimes from the symmetric-soup face law.

Residence times per hull radius from the cube layer-death files (n = 11..13 regenerated in scratch/peeling,
n >= 14 from the lead's scratch/cubes runs), the O_h-symmetric face law fitted to symmetric soups
(octa_hazard.csv, sym = 1, per-state hazard, A >= 198), and the predicted mean lifetime
sum_R tau_sym(A(R)) from the established hull R0 downwards.  Writes cube_residence.csv, cube_lifetime.csv.
"""
import csv, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cubeface import face_area

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', 'scratch')
FILES = {n: f'{S}/peeling/cube_ev{n}.jsonl' for n in (11, 12, 13)}
FILES.update({n: f'{S}/cubes/ev{n}.jsonl' for n in (14, 15, 16)})
LIFE = {11: 4218, 12: 24286, 13: 169049, 14: 4460298, 15: 37367092}

# symmetric face law: weighted fit of ln(1/h) = a + b A over per-state bins with A >= 198
rows = [r for r in csv.DictReader(open(os.path.join(HERE, 'octa_hazard.csv'))) if r['sym'] == '1' and float(r['A_mean']) >= 198
        and int(r['events']) >= 5]
A = np.array([float(r['A_mean']) for r in rows]); y = -np.log([float(r['hazard']) for r in rows])
w = np.array([int(r['events']) for r in rows], float)
X = np.vstack([np.ones_like(A), A]).T
cov = np.linalg.inv(X.T @ (w[:, None] * X)); a, b = cov @ X.T @ (w * y)
res = y - X @ np.array([a, b]); s2 = np.sum(w * res ** 2) / (len(y) - 2); cov *= max(1.0, s2)
print(f'sym law: ln tau = {a:.3f} + {b:.5f} A  (se {math.sqrt(cov[0,0]):.3f}, {math.sqrt(cov[1,1]):.5f}); '
      f'slab c = 0.2088 -> A_eff = A / {0.2088 / b:.2f}')


VF = 1.5   # vertex-centred symmetric soups outlive cube-centred ones of equal face area by 1.47x (R=28 vs 27) and 1.54x (32 vs 31)


def tau(Rv, vertex):
    return math.exp(a + b * face_area(Rv, vertex)) * (VF if vertex else 1.0)


res_rows, life_rows = [], []
for n, f in FILES.items():
    if not os.path.exists(f) or os.path.getsize(f) == 0:
        continue
    vertex = n % 2 == 0
    off = 3 if vertex else 0
    ev = [json.loads(l) for l in open(f)]
    e = sorted([x for x in ev if x['axis'] == 0 and x['s'] > 0 and x['cause'] == 'hull'], key=lambda x: x['gen'])
    deaths = {}
    for x in e:
        deaths[x['s'] - off] = x['gen']
    Rs = sorted(deaths, reverse=True)
    R0 = 3 * n - 6
    t = deaths.get(R0 + 2, 0)
    for Rv in Rs:
        if Rv > R0:
            continue
        res_rows.append(dict(n=n, R=Rv, area=face_area(Rv, vertex), start=t, end=deaths[Rv], residence=deaths[Rv] - t,
                             predicted_mean=round(tau(Rv, vertex))))
        t = deaths[Rv]
    pred = sum(tau(Rv, vertex) for Rv in range(R0, 20, -2))
    lead = tau(R0, vertex)
    life_rows.append(dict(n=n, R0=R0, area0=face_area(R0, vertex), observed=LIFE.get(n, ''), predicted_mean=round(pred),
                          first_plateau_share=round(lead / pred, 3),
                          ratio=round(LIFE[n] / pred, 3) if n in LIFE else ''))
for n in (16, 17):   # predictions only
    if n in [r['n'] for r in life_rows]:
        continue
    vertex = n % 2 == 0; R0 = 3 * n - 6
    pred = sum(tau(Rv, vertex) for Rv in range(R0, 20, -2))
    life_rows.append(dict(n=n, R0=R0, area0=face_area(R0, vertex), observed='', predicted_mean=round(pred),
                          first_plateau_share=round(tau(R0, vertex) / pred, 3), ratio=''))
rng = np.random.default_rng(1)
for r in life_rows:
    n = r['n']; v = n % 2 == 0
    L = sum(rng.exponential(tau(Rv, v), 200000) for Rv in range(r['R0'], 20, -2))
    r['pred_5pct'], r['pred_95pct'] = [round(x) for x in np.quantile(L, [0.05, 0.95])]
    r['obs_quantile'] = round(float((L < r['observed']).mean()), 3) if r['observed'] != '' else ''
for name, rr in (('cube_residence.csv', res_rows), ('cube_lifetime.csv', life_rows)):
    with open(os.path.join(HERE, name), 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rr[0])); wr.writeheader(); wr.writerows(rr)
for r in life_rows:
    print(r)
