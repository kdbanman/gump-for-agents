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
