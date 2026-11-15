#!/usr/bin/env python3
"""round3_persite.py: added after round-3 T1 (not forecast). The per-site cost of a dip with the size-independent
rate of shallow dips removed, [ln ν(0.9) − ln ν(p)]/A, and the unweighted tail slope (the lead's fit), by size.

    python3 research/dying/round3_persite.py     # reads research/dying/data/r3_excursions.csv
"""
import csv, os, numpy as np
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'r3_excursions.csv'))))
LT = {}
for spec in ['oct_9_c_c1', 'oct_11_c_c1', 'oct_13_c_c1', 'oct_15_c_c1', 'hex_4_1_c1']:
    r = [x for x in rows if x['spec'] == spec]; A = int(r[0]['A']); pb = float(r[0]['pbar'])
    d = {float(x['p']): (float(x['ln_nu']), int(x['n_reach']), float(x['ln_nu_se'])) for x in r}
    ps = [p for p in d if 0.1 - 1e-9 <= p <= 0.45 + 1e-9 and d[p][1] >= 20]
    X = np.array([p * pb for p in ps]); Y = np.array([d[p][0] for p in ps]); s = np.polyfit(X, Y, 1)
    cost = {p: (d[0.9][0] - d[p][0]) / A for p in (0.7, 0.5, 0.3, 0.1) if d[p][1] >= 20}
    print(f'{spec:12s} A {A:3d} P̄/A {pb / A:.3f}  unweighted slope 0.10-0.45 ({len(ps)} levels) {s[0]:.3f}, line at p=0 minus ln ν(0.9), per site '
          f'{(d[0.9][0] - s[1]) / A:.4f};  [ln ν(0.9) − ln ν(p)]/A: ' + ', '.join(f'p {p}: {v:.4f}' for p, v in cost.items()))
