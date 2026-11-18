#!/usr/bin/env python3
"""As nuq.py, but ln q is continued by the parabola through the three anchor sizes (computed after the linear
procedure was scored; not a frozen forecast).  Same arguments as nuq.py."""
import math, sys
from nuq import load
tgt = load(sys.argv[1]); anc = []
for s in sys.argv[2:]:
    f, lt, er = s.split(':'); anc.append((load(f), float(lt), float(er)))
A0, E0, c0, d0 = tgt; xs = [a[0][0] for a in anc]
w = []
for i in range(3):
    num = den = 1.0
    for j in range(3):
        if j != i:
            num *= (A0 - xs[j]); den *= (xs[i] - xs[j])
    w.append(num / den)
print('weights', [round(x, 3) for x in w])
for p in range(1, 40):
    if p not in c0 or c0[p] < 100 or any(p not in a[0][2] or a[0][2][p] < 100 for a in anc):
        continue
    lq = [-lt - math.log(c[p] / E) for (A, E, c, d), lt, er in anc]
    sq = [math.sqrt(er ** 2 + 1 / c[p]) for (A, E, c, d), lt, er in anc]
    lt0 = -math.log(c0[p] / E0) - sum(wi * y for wi, y in zip(w, lq))
    err = math.sqrt(sum((wi * s) ** 2 for wi, s in zip(w, sq)) + 1 / c0[p])
    print(f'p {p:3d} count {c0[p]:7d}  ln tau (parabola) = {lt0:.4f} +- {err:.4f}')
