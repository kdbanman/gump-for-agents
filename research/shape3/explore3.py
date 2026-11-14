#!/usr/bin/env python3
"""Post hoc (after the runs): every measured pair difference next to the lattice invariants of its two classes.

    python3 research/shape3/explore3.py
Invariants: Gram (Q1, 2B, Q2), h = Im tau, x = Re tau, rows (closure along the three kagome row directions),
transverse layers per diagonal (period / 2), cheapest firewall cut, firewall share W/F and near-firewall rate
(checks with two adjacent dead transverse layers, per life-generation) measured in the same runs.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze3 import load, lnt, PAIRS  # noqa: E402
from predict3 import geo  # noqa: E402
import lattice2 as L2  # noqa: E402
import csv  # noqa: E402

if __name__ == '__main__':
    T, nj, B = load()
    near = {}
    for r in csv.DictReader(open(os.path.join(HERE, 'data', 'runs.csv'))):
        L = (int(r['a']), int(r['k']), int(r['b'])); near.setdefault(L, [0, 0.0])
        near[L][0] += int(r['near2']); near[L][1] += float(r['exposure'])
    print('| pair | A | d | class | Gram | x | rows | layers | cut | W/F | near2 per 10^6 life-gens |')
    print('|---|---:|---|---|---|---:|---|---|---:|---:|---:|')
    for lab, X, Y in PAIRS:
        if X not in T or Y not in T:
            continue
        (vx, ex), (vy, ey) = lnt(T[X]['exposure'], T[X]['F']), lnt(T[Y]['exposure'], T[Y]['F'])
        for i, c in enumerate((X, Y)):
            g = geo(c); inv = L2.invariants(*c)
            first = f'| {lab} | {3*c[0]*c[2]} | {vy - vx:+.4f} ± {math.hypot(ex, ey):.4f}' if i == 0 else '| | | '
            print(f'{first} | {c} | ({g["q1"]},{2*g["B"]:.0f},{g["q2"]}) | {g["x"]:.3f} | {inv["rows"]} | '
                  f'{tuple(p // 2 for p in inv["periods"])} | {inv["cut"]} | {T[c]["W"] / T[c]["F"]:.4f} | '
                  f'{1e6 * 8 * near[c][0] / near[c][1]:.2f} |')

    # post hoc: refit every candidate on all pairs (the three known values pooled with this experiment's
    # re-measurements, and every new pair); chi^2 of the best fit
    import numpy as np
    from scipy.optimize import least_squares
    from scipy.stats import chi2
    import predict3 as P
    meas = {}
    for lab, X, Y in PAIRS:
        if X in T and Y in T and lab != 'T02':
            (vx, ex), (vy, ey) = lnt(T[X]['exposure'], T[X]['F']), lnt(T[Y]['exposure'], T[Y]['F'])
            meas[lab] = (3 * X[0] * X[2], X, Y, vy - vx, math.hypot(ex, ey))
    for lab, A, X, Y, d, e in P.KNOWN:     # pool the published value with the re-measurement
        if lab in meas:
            d2, e2 = meas[lab][3], meas[lab][4]; w1, w2 = 1 / e ** 2, 1 / e2 ** 2
            meas[lab] = (A, X, Y, (d * w1 + d2 * w2) / (w1 + w2), (w1 + w2) ** -0.5)
        else:
            meas[lab] = (A, X, Y, d, e)
    for title, keep in (('all pairs', lambda k: True), ('shortest loop^2 >= 12 only (P, T, N)', lambda k: k[0] in 'PTN')):
        sub = {k: v for k, v in meas.items() if keep(k)}
        print(f'\nPost hoc refit of each candidate on {title} (' + ', '.join(sorted(sub)) + '):')
        for name, (f, p0) in P.CANDS.items():
            best = None
            starts = [p0] if len(p0) == 1 else [[lb, K] for lb in (-2, 1, 4, 7) for K in (0.2, 0.65, 1.4, 2.5)]
            for s0 in starts:
                r = least_squares(lambda p: np.array([(f(A, X, Y, p) - d) / e for A, X, Y, d, e in sub.values()]), s0)
                best = r if best is None or r.cost < best.cost else best
            dof = len(sub) - len(p0)
            print(f'  {name:11s} chi2 {2 * best.cost:8.1f} on {dof}  p {chi2.sf(2 * best.cost, dof):.2g}  params {np.round(best.x, 5).tolist()}')
    print('  pooled pair values: ' + '; '.join(f'{k} {v[3]:+.4f} ± {v[4]:.4f}' for k, v in sorted(meas.items())))
