#!/usr/bin/env python3
"""Lifetime of random soups confined to m consecutive {111} layers on an N x N in-plane torus (T4: closed).
  thickness.py N m NSOUPS RHO SEED [--maxgen G]   prints one summary line and appends JSON to
  research/scratch/atlas/thickness.jsonl  (mu = first generation of the final cycle)
"""
import argparse, json, os, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vessel import slab  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('N', type=int); ap.add_argument('m', type=int); ap.add_argument('n', type=int)
ap.add_argument('rho', type=float); ap.add_argument('seed', type=int)
ap.add_argument('--maxgen', type=int, default=100000)
a = ap.parse_args()
v = slab(a.N, a.m)
t0 = time.time()
res = v.run(os.path.join(HERE, '..', 'scratch', 'atlas', f'slab_{a.N}_{a.m}_{a.seed}.bin'), a.n, a.rho, a.seed, a.maxgen, cells=False)
mus = sorted(r['mu'] for r in res)
rec = dict(N=a.N, m=a.m, cells=len(v.cells), rho=a.rho, seed=a.seed, n=a.n, maxgen=a.maxgen, mu=[r['mu'] for r in res],
           period=[r['period'] for r in res], pop=[r['pop'] for r in res], time=time.time() - t0)
with open(os.path.join(HERE, '..', 'scratch', 'atlas', 'thickness.jsonl'), 'a') as f:
    f.write(json.dumps(rec) + '\n')
print(f'N={a.N} m={a.m} cells={len(v.cells)} rho={a.rho} n={a.n}: mu median={mus[len(mus)//2]} mean={sum(mus)/len(mus):.1f} '
      f'max={mus[-1]} unsettled={sum(1 for r in res if r["period"]==0)} final density={sum(r["pop"] for r in res)/len(res)/len(v.cells):.3f} '
      f'periods={dict(Counter(r["period"] for r in res).most_common(6))} ({time.time()-t0:.0f}s)', flush=True)
