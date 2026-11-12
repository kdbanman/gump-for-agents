#!/usr/bin/env python3
"""Slab experiments (skewed in-plane torus, two flat faces, no edges).

  slabs.py N1 N2 m cap [--W 8] [--seed S] [--p 0.4]
Appends one JSON line per run to research/scratch/peeling/slabs.jsonl with, per replica:
  peels: death times of the d0 layers in order of the hull shrinking (outermost first), as [time, side];
  fw: first transverse T3 firewall time (min over the 3 other diagonals); lfw: first interior d0 firewall;
  settle: generation by which the replica was periodic (-1: not by cap).
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom
from analyze import death_times, ring_firewall, INF

ap = argparse.ArgumentParser()
ap.add_argument('N1', type=int); ap.add_argument('N2', type=int); ap.add_argument('m', type=int); ap.add_argument('cap', type=int)
ap.add_argument('--W', type=int, default=8); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--p', type=float, default=0.4)
ap.add_argument('--K', type=int, default=16)
a = ap.parse_args()
v = geom.slab(a.N1, a.m, a.N2)
seed = a.seed * 1000003 + a.N1 * 1009 + a.N2 * 101 + a.m
st, pop, la = v.run(a.W, a.p, seed, a.cap, a.K)
ge = v.gen_end
D = death_times(la, ge)
keys = [k for k, _ in v.layers]
d0 = D[:, [keys.index((0, 2 * t + 1)) for t in range(a.m)]]
fw = np.full(len(st), INF)
for d in (1, 2, 3):
    cols = [i for i, k in enumerate(keys) if k[0] == d]
    fw = np.minimum(fw, ring_firewall(D[:, cols], ring=True))
lfw = ring_firewall(d0, ring=False)
reps = []
for r in range(len(st)):
    lo, hi, peels = 0, a.m - 1, []
    while lo <= hi:   # hull shrinking from both sides: the next peel is the earlier of the two outer layers' deaths
        tl, th = d0[r, lo], d0[r, hi]
        if min(tl, th) == INF:
            break
        if tl <= th:
            peels.append([tl, 0]); lo += 1
        else:
            peels.append([th, 1]); hi -= 1
    reps.append(dict(peels=[[float(t), s] for t, s in peels], fw=float(fw[r]) if fw[r] < INF else None,
                     lfw=float(lfw[r]) if lfw[r] < INF else None, settle=int(st[r]), pop=int(pop[r])))
rec = dict(N1=a.N1, N2=a.N2, m=a.m, A=3 * a.N1 * a.N2, p=a.p, cap=a.cap, gen_end=ge, seed=seed, K=a.K, reps=reps)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scratch', 'peeling', 'slabs.jsonl')
with open(out, 'a') as f:
    f.write(json.dumps(rec) + '\n')
first = np.array([r['peels'][0][0] if r['peels'] else INF for r in reps])
stop = np.where(st >= 0, st, ge).astype(float)      # settled without peeling: exits the risk set
expo = np.minimum(first, stop)
print(f"slab {a.N1}x{a.N2} m={a.m} A={3*a.N1*a.N2} end={ge}: first peel in {np.sum(first<INF)}/{len(reps)}, "
      f"froze first {np.sum((first==INF)&(st>=0))}, exposure-MLE mean first peel {expo.sum()/max(1,np.sum(first<INF)):.4g}; "
      f"fw-before-peel {sum(1 for r,f in zip(reps, first) if r['fw'] is not None and r['fw'] < f)}", flush=True)
