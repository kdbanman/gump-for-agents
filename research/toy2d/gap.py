"""Does a dead stretch of the edge row heal or spread?  (1D "front" along the edge: the 2D replacement for
the closed rim of a hole in a gump face.)

Interior cells of a dead stretch of edge row (width >= 2r+1, r = in-row reach) can never be reborn: they see only
the cells below them (Moore: 3, cross2: 2 -- fewer than bmin). So a dead stretch changes only at its two ends.
Test: periodic strip W x L, R replicas; equilibrate T0 generations from a soup, then kill the edge row (row 0) on
x in [0, G) and follow the longest dead run of row 0 that contains the killed stretch... measured simply as
D(t) = longest periodic run of dead cells in row 0, averaged over replicas, plus the fraction of replicas whose
row 0 is entirely dead (edge death) and whose longest dead run has fallen to <= 4 (healed).

python3 gap.py RULE LAT [G=32] [L=128] [W=16] [R=128] [T0=400] [T=4000] [DEPTH=1]
(DEPTH > 1: kill rows 0..DEPTH-1 on the stretch -- a notch)
"""
import sys
import numpy as np
import geom

rule, lat = sys.argv[1], sys.argv[2]
G, L, W, R, T0, T, DEPTH = [int(v) for v in (sys.argv[3:10] + ['32', '128', '16', '128', '400', '4000', '1'][len(sys.argv[3:10]):])]
B, S = geom.parse_rule(rule); offs = geom.OFFS[lat]


def step(x):
    p = np.zeros((x.shape[0], W + 4, L), np.int8); p[:, 2:-2] = x
    n = np.zeros(x.shape, np.int8)
    for dx, dy in offs:
        n += np.roll(p, -dx, 2)[:, 2 + dy:2 + dy + W]
    n = n.astype(np.int64)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1).astype(np.int8)


def longest_dead(row):
    # row: (R, L) 0/1; longest periodic run of zeros
    out = np.zeros(row.shape[0], int)
    for i, r in enumerate(row):
        if r.sum() == 0:
            out[i] = L; continue
        k = np.argmax(r)  # rotate so it starts with a live cell
        rr = np.roll(r, -k)
        z = np.flatnonzero(np.diff(np.concatenate([[1], rr, [1]])) != 0)
        runs = z[1::2] - z[0::2] if len(z) else [0]
        out[i] = max(runs) if len(runs) else 0
    return out


rng = np.random.default_rng(5)
x = (rng.random((R, W, L)) < 0.5).astype(np.int8)
for _ in range(T0):
    x = step(x)
alive = x[:, 0].sum(1) > 0
base = longest_dead(x[:, 0])
x[:, :DEPTH, :G] = 0
print('%s %s: strip %dx%d, %d replicas, kill row 0 on [0,%d) (depth %d) after %d gens; equilibrium longest dead run in row 0: mean %.1f, max %d'
      % (rule, lat, W, L, R, G, DEPTH, T0, base.mean(), base.max()))
ts = [0, 10, 30, 100, 300, 1000, 2000, 4000, 8000, 16000]
t = 0
for tt in ts:
    while t < tt:
        x = step(x); t += 1
    D = longest_dead(x[:, 0])
    print('  t=%5d  mean longest dead run %6.1f  median %5.0f  edge dead %.2f  healed(<=8) %.2f' % (
        t, D.mean(), np.median(D), (D == L).mean(), (D <= 8).mean()), flush=True)
    if t >= T:
        break
