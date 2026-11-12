#!/usr/bin/env python3
"""Octahedral soups in open space (vessel = the octahedron |p|_1 <= R, exact by T2): full peel histories.

  octa.py R p cap [--sym] [--W 8] [--seed S] [--K 16] [--tag T]
Appends one JSON line per batch to research/scratch/peeling/octa.jsonl. Per replica:
  hist: [[t, f, C], ...] the hull's 8 face offsets over time: face f = 2*d + (0: +d, 1: -d) moves to
        distance C (outermost live layer at s = +C for +d, s = -C for -d; None: nothing left on that side) at time t
        (resolution K; t = first sample at which the old outer layer was dead);
  settle: generation by which periodic (-1: still active at cap), pop: final population.
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

ap = argparse.ArgumentParser()
ap.add_argument('R', type=int); ap.add_argument('p', type=float); ap.add_argument('cap', type=int)
ap.add_argument('--sym', action='store_true'); ap.add_argument('--W', type=int, default=8)
ap.add_argument('--seed', type=int, default=1); ap.add_argument('--K', type=int, default=16)
ap.add_argument('--tag', default='')
a = ap.parse_args()
v = geom.octa(a.R, a.sym)
seed = a.seed * 1000003 + a.R * 101 + int(a.p * 1000) * 7 + 5 * a.sym
st, pop, la = v.run(a.W, a.p, seed, a.cap, a.K)
ge = v.gen_end
keys = [k for k, _ in v.layers]
reps = []
for r in range(len(st)):
    hist = []
    for d in range(4):
        ss = sorted(s for (dd, s) in keys if dd == d)
        L = {s: la[r, keys.index((d, s))] for s in ss}
        for sign, f in ((1, 2 * d), (-1, 2 * d + 1)):
            order = ss[::-1] if sign == 1 else ss          # outermost first
            for i, s in enumerate(order):
                if L[s] >= ge:                              # alive at the end: hull stops here
                    break
                # layer s is dead from L[s]+1 on; it is the outer layer only once all outer ones are dead too
                t = int(max(L[x] for x in order[:i + 1]) + 1)
                nxt = next((x for x in order[i + 1:] if L[x] >= t), None)
                hist.append([t, f, None if nxt is None else sign * nxt])
    dd = {}
    for t, f, c in hist:            # several layers can be found dead at the same sample: keep the innermost
        dd[(t, f)] = c
    hist = sorted([t, f, c] for (t, f), c in dd.items())
    reps.append(dict(hist=hist, settle=int(st[r]), pop=int(pop[r])))
rec = dict(R=a.R, p=a.p, sym=a.sym, cap=a.cap, gen_end=ge, seed=seed, K=a.K, tag=a.tag, reps=reps)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scratch', 'peeling', 'octa.jsonl')
with open(out, 'a') as f:
    f.write(json.dumps(rec) + '\n')
life = np.array([r['settle'] if r['settle'] >= 0 else np.inf for r in reps])
print(f"octa R={a.R} p={a.p} sym={a.sym} end={ge}: settled {np.sum(life < np.inf)}/{len(reps)}, "
      f"median life {np.median(life):.4g}", flush=True)
