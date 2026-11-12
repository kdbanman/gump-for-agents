#!/usr/bin/env python3
"""Random soups in octahedral vessels (exact by T2): lifetimes and ash census.

  harvest.py CENTRE R NSOUPS RHO SEED [--maxgen G]     -> research/scratch/atlas/harvest_CENTRE_R_RHO_SEED.json
Each ash object = an R-component (distance <= 2) of the union of the final cycle's phases, keyed by
(period, min over phases of the canonical form).
"""
import argparse, json, os, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vessel import octa, classify_final  # noqa: E402
from lattice import fmt  # noqa: E402

OUT = os.path.join(HERE, '..', 'scratch', 'atlas')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('centre'); ap.add_argument('R', type=int); ap.add_argument('n', type=int)
    ap.add_argument('rho', type=float); ap.add_argument('seed', type=int)
    ap.add_argument('--maxgen', type=int, default=2_000_000)
    a = ap.parse_args()
    v = octa(a.centre, a.R)
    t0 = time.time()
    res = v.run(os.path.join(OUT, f'v_{a.centre}_{a.R}_{a.seed}.bin'), a.n, a.rho, a.seed, a.maxgen)
    objs = Counter(); soups = []
    for r in res:
        o = classify_final(v, r['live'], r['period']) if r['period'] else []
        for per, key in o:
            objs[(per, fmt(key))] += 1
        soups.append(dict(mu=r['mu'], period=r['period'], pop=r['pop'], nobj=len(o),
                          objs=[[per, len(key)] for per, key in o]))
    out = dict(centre=a.centre, R=a.R, cells=len(v.cells), rho=a.rho, seed=a.seed, n=a.n, maxgen=a.maxgen,
               time=time.time() - t0, soups=soups,
               objects=[[per, key, c] for (per, key), c in objs.most_common()])
    fn = os.path.join(OUT, f'harvest_{a.centre}_{a.R}_{a.rho}_{a.seed}.json')
    json.dump(out, open(fn, 'w'))
    mus = sorted(s['mu'] for s in soups)
    print(f'{a.centre} R={a.R} cells={len(v.cells)} rho={a.rho} n={a.n} time={time.time()-t0:.0f}s '
          f'mu median={mus[len(mus)//2]} max={mus[-1]} dead={sum(1 for s in soups if s["pop"]==0)} '
          f'periods={dict(Counter(s["period"] for s in soups))} distinct objects={len(objs)} -> {fn}')


if __name__ == '__main__':
    main()
