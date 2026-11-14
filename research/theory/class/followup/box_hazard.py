"""box_hazard.py -- rate of the first permanent wall death in bond10 B34/S234 boxes, with box settling as a competing
ending (censored).  python3 box_hazard.py n cap seeds"""
import sys, json
import numpy as np
import fu, three_d
n, cap, ns = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
L = fu.lattice("bond10"); B, S = three_d.rule("bond10", 5)
V = three_d.box_vessel(L, n)
ev = ex = 0; endset = 0
for s in range(ns):
    r = fu.life_run(V, B, S, 3, three_d.sheets(V, n), 0.45, cap, P=1, seed=100 + s)
    life = np.where(r["kind"] > 0, r["life"], cap)
    tG = r["tG"]
    died = (tG >= 0) & (tG <= life + 2)
    ev += int(died.sum()); ex += float(np.where(died, tG, life).sum())
    endset += int(((tG < 0) & (r["kind"] > 0)).sum())
print(json.dumps(dict(lattice="bond10", rule="B34/S234", n=n, boxes=64 * ns, first_wall_deaths=ev,
                      settled_before_any_wall_death=endset, exposure=ex,
                      tau_per_wall=6 * ex / ev if ev else None, ln_tau_per_wall=float(np.log(6 * ex / ev)) if ev else None,
                      err=1 / np.sqrt(ev) if ev else None)))
