"""Kymograph of the edge row(s) of a periodic strip until an edge dies (numpy; for looking).
python3 kymo.py RULE LAT W L [seed] [maxgens] [rows]  -> prints the last `rows` generations of edge row 0 and row 1"""
import sys
import numpy as np
import geom
rule, lat, W, L = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
maxg = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 6
rows = int(sys.argv[7]) if len(sys.argv) > 7 else 60
B, S = geom.parse_rule(rule); offs = geom.OFFS[lat]


def step(x):
    p = np.zeros((W + 4, L), np.int64); p[2:-2] = x
    n = sum(np.roll(p, -dx, 1)[2 + dy:2 + dy + W] for dx, dy in offs)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1)


rng = np.random.default_rng(seed)
x = (rng.random((W, L)) < 0.5).astype(np.int64)
hist = []
for t in range(maxg):
    x = step(x); hist.append(x.copy())
    if len(hist) > rows: hist.pop(0)
    if t > 300 and (x[0].sum() == 0 or x[-1].sum() == 0):
        r = 0 if x[0].sum() == 0 else W - 1
        r2 = 1 if r == 0 else W - 2
        print('edge row %d died at t = %d; last %d generations (row %d | row %d), newest last' % (r, t, rows, r, r2))
        for h in hist:
            print(''.join('#' if c else '.' for c in h[r]), ' ', ''.join('#' if c else '.' for c in h[r2]), h[r].sum())
        break
