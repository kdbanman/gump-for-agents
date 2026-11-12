#!/usr/bin/env python3
"""Decompose the final (static) states of the legacy closed-cube runs (sides 8-11) into objects.
Runs reference/oracle.py's legacy-cube seed to stillness, then splits the live set into neighbour
components and R-components (distance <= 2), giving canonical keys for lookup in the catalogue.
  legacy_ash.py  -> research/scratch/atlas/legacy_ash.json
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice import oracle, components, canon, fmt, step, sym_order, thickness, is_strict_still  # noqa: E402

RUNS = {8: 40, 9: 50, 10: 55, 11: 60}
out = {}
for n, H in RUNS.items():
    lo, hi = oracle.legacy_seed_span(H)
    m = oracle.masks(H)
    h = oracle.fill_box(H, lo, hi, m)
    g = 0
    while True:
        h2 = oracle.step(h, m); g += 1
        if (h2 == h).all():
            break
        h = h2
    c = (lo + hi) // 2; c -= c % 2      # even shift keeps cell parity (centroids are then offset by <=1)
    cells = frozenset(tuple(int(v) - c for v in p) for p in np.argwhere(h))
    assert step(cells) == cells
    objs = []
    for comp in components(cells, 2):
        sub = components(comp, 1)
        objs.append(dict(size=len(comp), key=fmt(canon(comp)), centroid=[round(float(np.mean([p[k] for p in comp])), 2) for k in range(3)],
                         nbr_components=sorted(len(s) for s in sub), strict=is_strict_still(comp),
                         sub_keys=[fmt(canon(s)) for s in sub], sym=sym_order(comp), thickness=thickness(comp)))
    out[n] = dict(H=H, gens_to_static=g - 1, pop=len(cells), sym=sym_order(cells), objects=objs)
    print(f'side {n}: static after {g-1} gens, pop {len(cells)}, whole-state symmetry {sym_order(cells)}, '
          f'{len(objs)} R-components sizes {sorted(o["size"] for o in objs)}')
json.dump(out, open(os.path.join(HERE, '..', 'scratch', 'atlas', 'legacy_ash.json'), 'w'), indent=1)
