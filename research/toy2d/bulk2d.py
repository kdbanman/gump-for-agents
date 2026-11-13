"""Bulk phase on a torus: density, non-period-2 activity, drive (exception) events per cell-generation.
python3 bulk2d.py RULE LATTICE THETA_INT [L=128] [gens=3000] [p=0.4]"""
import sys
import numpy as np
import geom
rule, lat, t = sys.argv[1], sys.argv[2], int(sys.argv[3])
L = int(sys.argv[4]) if len(sys.argv) > 4 else 128
gens = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
p = float(sys.argv[6]) if len(sys.argv) > 6 else 0.4
B, S = geom.parse_rule(rule); offs = geom.OFFS[lat]; theta = t - 0.5
rng = np.random.default_rng(1); x = (rng.random((L, L)) < p).astype(np.int64)
cnt = lambda x: sum(np.roll(np.roll(x, dy, 0), dx, 1) for dx, dy in offs)
f = lambda x, n: np.where(x == 1, (S >> n) & 1, (B >> n) & 1)
xp = x; x = f(x, cnt(x)); dens = []; act = []; drive = []; nhist = np.zeros(len(offs) + 1)
for g in range(gens):
    n = cnt(x); xn = f(x, n)
    thr = (n + x >= t).astype(np.int64)
    exc = xn != thr
    d = exc & (((xn == 0) & (xp == 1)) | ((xn == 1) & (xp == 0)))   # exception cells that inject energy (term > 0)
    if g > gens // 3:
        dens.append(x.mean()); act.append((xn != xp).mean()); drive.append(d.mean())
        nhist += np.bincount(n.ravel(), minlength=len(offs) + 1)
    xp, x = x, xn
print('%s on %s torus %d^2: density %.4f, mismatch (x(t+1) != x(t-1)) %.4f, drive events %.4f per cell-gen; P(n) %s' % (
    rule, lat, L, np.mean(dens), np.mean(act), np.mean(drive), np.round(nhist / nhist.sum(), 3).tolist()))
