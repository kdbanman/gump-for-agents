#!/usr/bin/env python3
"""Random soups in the 1-layer kagome automaton on an N x N in-plane torus (3N^2 cells).
  kagome_soup.py N NSOUPS SEED [--rhos 0.05,0.1,...] [--census]
Per density: lifetime mu (first gen of final cycle), final density, final period; with --census
the ash is split into R-components, unwrapped and identified (period, canonical phase).
Appends JSON lines to research/scratch/atlas/kagome_soup.jsonl.
"""
import argparse, json, os, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vessel import slab, classify_final  # noqa: E402
from lattice import fmt  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('N', type=int); ap.add_argument('n', type=int); ap.add_argument('seed', type=int)
ap.add_argument('--rhos', default=','.join(f'{r/20:.2f}' for r in range(1, 20)))
ap.add_argument('--census', action='store_true')
a = ap.parse_args()
v = slab(a.N, 1)
for rho in map(float, a.rhos.split(',')):
    t0 = time.time()
    res = v.run(os.path.join(HERE, '..', 'scratch', 'atlas', f'kag_{a.N}_{a.seed}.bin'), a.n, rho, a.seed, 100000, cells=a.census)
    mus = sorted(r['mu'] for r in res)
    objs = Counter()
    if a.census:
        for r in res:
            if r['period']:
                for per, key in classify_final(v, r['live'], r['period'], torus=True):
                    objs[(per, fmt(key))] += 1
    rec = dict(N=a.N, cells=len(v.cells), rho=rho, n=a.n, seed=a.seed, mu=[r['mu'] for r in res], pop=[r['pop'] for r in res],
               period=[r['period'] for r in res], objects=[[p, k, c] for (p, k), c in objs.most_common()])
    with open(os.path.join(HERE, '..', 'scratch', 'atlas', 'kagome_soup.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(f'N={a.N} rho={rho:.2f}: mu median={mus[len(mus)//2]} mean={sum(mus)/len(mus):.1f} max={mus[-1]} '
          f'ash density={sum(r["pop"] for r in res)/len(res)/len(v.cells):.4f} '
          f'periods={dict(Counter(r["period"] for r in res))} objects={sum(objs.values())} distinct={len(objs)} '
          f'nonstill={[(p, len(k.split()), c) for (p, k), c in objs.items() if p != 1]} ({time.time()-t0:.0f}s)', flush=True)
