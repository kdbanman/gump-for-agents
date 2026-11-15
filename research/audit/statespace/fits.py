#!/usr/bin/env python3
"""Robustness of the study's scaling fits (claim 3), from research/statespace/data/vessels.jsonl
(rows independently reproduced for 6 vessels by this audit).  python3 fits.py"""
import json
import numpy as np
rows = [json.loads(l) for l in open('/home/user/gump-for-agents/research/statespace/data/vessels.jsonl')]
FAM = {'hull': ('hull', 'hullbig'), 'slab3': ('slab3all',), 'slab2': ('slab2',), 'kagome': ('slab1',), 'torus3d': ('torus',)}


def fit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    co, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ co
    return co, float(np.sqrt((r ** 2).mean()))


for fam, keys in FAM.items():
    fr = [r for r in rows if r['family'] in keys]
    for nmin in (9, 15, 21):
        g = [r for r in fr if r['N'] >= nmin]
        if len({r['N'] for r in g}) < 3:
            continue
        N = np.array([r['N'] for r in g], float)
        im = np.log2(np.array([r['N'] and (2 ** r['N'] - r['goe']) for r in g], float))
        cy = np.log2(np.array([r['cyclic_states'] for r in g], float))
        mt = np.array([r['mean_visited'] for r in g]); xt = np.array([r['max_visited'] for r in g], float)
        (a1, _), _ = fit(N, im); (a2, _), _ = fit(N, cy)
        # mean visited: linear vs exponential (log-linear), compare rms of residual in the same (linear) units
        (s, c), rl = fit(N, mt)
        (le, lc), _ = fit(N, np.log(mt)); re = float(np.sqrt(((mt - np.exp(lc + le * N)) ** 2).mean()))
        (sx, cx), rlx = fit(N, xt)
        (lex, lcx), _ = fit(N, np.log(xt)); rex = float(np.sqrt(((xt - np.exp(lcx + lex * N)) ** 2).mean()))
        sizes = sorted({int(x) for x in N})
        print(f'{fam:8s} N>={nmin:2d} ({len(g):3d} vessels, {len(sizes)} sizes {sizes[0]}..{sizes[-1]}): '
              f'log2|f(S)| {a1:.3f}N  log2 cyclic {a2:.3f}N | mean visited lin {s:.3f}N rms {rl:.2f} vs '
              f'exp e^({le:.3f}N) rms {re:.2f} | max visited lin {sx:.2f}N rms {rlx:.1f} vs exp e^({lex:.3f}N) rms {rex:.1f}')
# hulls: one value per N (the max over hulls of that N) to remove the shape mix
fr = [r for r in rows if r['family'] in FAM['hull']]
Ns = sorted({r['N'] for r in fr if r['N'] >= 9})
for stat in ('mean_visited', 'max_visited'):
    y = np.array([max(r[stat] for r in fr if r['N'] == n) for n in Ns], float); x = np.array(Ns, float)
    (s, c), rl = fit(x, y); (le, lc), _ = fit(x, np.log(y)); re = float(np.sqrt(((y - np.exp(lc + le * x)) ** 2).mean()))
    print(f'hull per-N max of {stat}: lin {s:.3f}N rms {rl:.2f}; exp e^({le:.3f}N) rms {re:.2f}')
