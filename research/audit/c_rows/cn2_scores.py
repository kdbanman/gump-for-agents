#!/usr/bin/env python3
"""CN2 (CLAIMS.md): the scores of research/constant/PREDICTIONS.md parts A and B, recomputed.
    python3 research/audit/c_rows/cn2_scores.py
Part A: forecast -ln P (PREDICTIONS.md A.4) against GP10's measured ln P (CLAIMS.md GP10 row).
Part B: z = (measured - forecast) / sigma_measured on T01, T12, N72, Q63 with the forecasts of model (a), (b-exp),
(b-K0) on fitting set W (PREDICTIONS.md B table) and the measured d +- err printed by
research/audit/shape3_lead_check.py (copied below; re-run that script to check them); chi-square on 4."""
from scipy import stats
fA = {'2x2': 5.0, '3x3': 9.5, '4x4': 15.3}; mA = {'2x2': 6.254, '3x3': 12.128, '4x4': 19.423}
for k in fA: print(f'A {k}: forecast {fA[k]}, measured {mA[k]:.2f}, low by {mA[k] - fA[k]:.2f}; measured cost per cell {mA[k] / (3 * int(k[0]) ** 2):.3f}')
meas = {'T01': (-0.0062, 0.0041), 'T12': (0.0005, 0.0041), 'N72': (0.0018, 0.0061), 'Q63': (0.0017, 0.0020), 'Q36': (-0.0223, 0.0007)}
fc = {'a': {'T01': .0008, 'T12': .0008, 'N72': .0001, 'Q63': 0.0, 'Q36': .0029},
      'b-exp': {'T01': .0007, 'T12': .0007, 'N72': .0001, 'Q63': 0.0, 'Q36': .0025},
      'b-K0': {'T01': .0007, 'T12': .0007, 'N72': .0001, 'Q63': 0.0, 'Q36': .0026}}
for mname, f in fc.items():
    z = {k: (meas[k][0] - f[k]) / meas[k][1] for k in ('T01', 'T12', 'N72', 'Q63')}
    s = sum(v * v for v in z.values())
    print(f"B model ({mname}): z {', '.join(f'{k} {v:+.2f}' for k, v in z.items())}; sum z^2 = {s:.2f} on 4, p = {stats.chi2.sf(s, 4):.2f}; "
          f"Q36 forecast {f['Q36']:+.4f} vs measured {meas['Q36'][0]:+.4f}")
z0 = sum((meas[k][0] / meas[k][1]) ** 2 for k in ('T01', 'T12', 'N72', 'Q63'))
print(f'against zero: sum z^2 = {z0:.2f}, p = {stats.chi2.sf(z0, 4):.2f}')
