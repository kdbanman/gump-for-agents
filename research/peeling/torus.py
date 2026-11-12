#!/usr/bin/env python3
"""Whole-torus soups (no faces): how and when do they die?

  torus.py N p cap [--W 8] [--seed S]
Per replica: first T3 firewall time on each of the 4 diagonals (ring of N layers, 3N^2 cells each),
settle time, final population. Appends to research/scratch/peeling/torus.jsonl.
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom
from analyze import death_times, ring_firewall, INF

ap = argparse.ArgumentParser()
ap.add_argument('N', type=int); ap.add_argument('p', type=float); ap.add_argument('cap', type=int)
ap.add_argument('--W', type=int, default=8); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--K', type=int, default=16)
a = ap.parse_args()
v = geom.torus(a.N)
seed = a.seed * 1000003 + a.N * 31 + int(a.p * 1000)
st, pop, la = v.run(a.W, a.p, seed, a.cap, a.K)
ge = v.gen_end
D = death_times(la, ge)
keys = [k for k, _ in v.layers]
fw = []
for d in range(4):
    cols = [i for i, k in enumerate(keys) if k[0] == d]
    fw.append(ring_firewall(D[:, cols], ring=True))
fw = np.array(fw).T
reps = [dict(fw=[None if x == INF else float(x) for x in fw[r]], settle=int(st[r]), pop=int(pop[r])) for r in range(len(st))]
rec = dict(N=a.N, p=a.p, cap=a.cap, gen_end=ge, seed=seed, K=a.K, reps=reps)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scratch', 'peeling', 'torus.jsonl'), 'a') as f:
    f.write(json.dumps(rec) + '\n')
first_fw = fw.min(1)
end = np.where(st >= 0, st, ge)
print(f"torus N={a.N} p={a.p} end={ge}: settled {np.sum(st>=0)}/{len(st)} (extinct {np.sum((st>=0)&(pop==0))}), "
      f"firewall first {np.sum(first_fw < end)}, mean end {end.mean():.4g}", flush=True)
