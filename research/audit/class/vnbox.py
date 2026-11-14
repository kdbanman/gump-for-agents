"""vnbox.py -- von Neumann B2/S12 in square boxes, larger than class.md ran (its data stop at side 33).

    python3 vnbox.py [cap]

Prints the median lifetime of 64 soups (density 0.47) per side, and the local rates d ln T / d side and
d ln T / d ln side.  An exponential law has a constant first rate; a power law a constant second one."""
import sys, json
import numpy as np
import aud

cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
L = aud.lattice("vn")
prev = None
for side in (9, 13, 17, 21, 25, 29, 33, 41, 49, 65, 81):
    V = aud.box(L, (0, 0), (side - 1, side - 1))
    lf, pop, kind = aud.life_run(V, [2], [1, 2], 0.47, cap, seed=side)
    T = np.where(kind > 0, lf, cap + 1)
    med = float(np.median(T))
    rec = dict(side=side, N=V.N, finished=int((kind > 0).sum()), median=med, q25=float(np.percentile(T, 25)),
               q75=float(np.percentile(T, 75)), by_snapshot=int((kind == 2).sum()),
               final_density=round(float(pop[kind > 0].mean() / V.N), 4))
    if prev:
        rec["rate_per_side"] = round(float(np.log(med / prev[1]) / (side - prev[0])), 4)
        rec["local_power"] = round(float(np.log(med / prev[1]) / np.log(side / prev[0])), 2)
    prev = (side, med)
    print(json.dumps(rec), flush=True)
