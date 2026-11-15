#!/usr/bin/env python3
"""Claim 5 of the review of research/shape3: the loop^2 >= 12 scores, (i) as in the README (T01, T12, N72 treated as
independent), (ii) with the covariance that T01 and T12 share through (2,4,12) (corr = -0.5), and (iii) for the null
"d = 0 at A = 72".  Measured values from the README table (recomputed from data/runs.csv by the lead's check), forecasts
from research/shape3/data/predictions.json (committed in 46baf66).

    python3 research/audit/shape3/score_check.py
"""
import json, math, os
import numpy as np
from scipy.stats import chi2
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
P = json.load(open(os.path.join(ROOT, 'research', 'shape3', 'data', 'predictions.json')))
F = {(1, 6, 24): 120229, (2, 4, 12): 120971, (1, 5, 24): 120906, (2, 2, 12): 53269, (1, 10, 24): 53171}
E = {(1, 6, 24): 1.920e11, (2, 4, 12): 1.920e11, (1, 5, 24): 1.920e11, (2, 2, 12): 7.680e10, (1, 10, 24): 7.680e10}
import csv
E = {}
for r in csv.DictReader(open(os.path.join(ROOT, 'research', 'shape3', 'data', 'runs.csv'))):
    L = (int(r['a']), int(r['k']), int(r['b']))
    if L in F:
        E[L] = E.get(L, 0) + float(r['exposure'])
lt = {L: math.log(2 * E[L] / F[L]) for L in F}
pairs = [('T01', (1, 6, 24), (2, 4, 12)), ('T12', (2, 4, 12), (1, 5, 24)), ('N72', (2, 2, 12), (1, 10, 24))]
d = np.array([lt[Y] - lt[X] for _, X, Y in pairs])
C = np.zeros((3, 3))
for i, (_, X, Y) in enumerate(pairs):
    for j, (_, X2, Y2) in enumerate(pairs):
        for La, sa in ((X, -1), (Y, 1)):
            for Lb, sb in ((X2, -1), (Y2, 1)):
                if La == Lb:
                    C[i, j] += sa * sb / F[La]
print('measured', ', '.join(f'{t} {x:+.4f} +- {math.sqrt(C[i, i]):.4f}' for i, ((t, _, _), x) in enumerate(zip(pairs, d))),
      f'; corr(T01, T12) = {C[0, 1] / math.sqrt(C[0, 0] * C[1, 1]):+.2f}')
for name, c in list(P['cands'].items()) + [('zero', None)]:
    f = np.array([c['forecast'][t][0] for t, _, _ in pairs]) if c else np.zeros(3)
    sf = np.array([c['forecast'][t][1] for t, _, _ in pairs]) if c else np.zeros(3)
    r = d - f
    diag = float(np.sum(r ** 2 / (np.diag(C) + sf ** 2)))
    full = float(r @ np.linalg.solve(C + np.diag(sf ** 2), r))
    print(f'{name:11s} independent chi2 {diag:5.1f} / 3 (p {chi2.sf(diag, 3):.2g});  with covariance {full:5.1f} / 3 (p {chi2.sf(full, 3):.2g})')
