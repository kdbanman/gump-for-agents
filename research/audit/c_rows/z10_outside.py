#!/usr/bin/env python3
"""Z10 (CLAIMS.md): from the trial records of research/clockwork/perturb.py P66.27a, the fate of the trials that add
a lone cell outside P66.27a's box (the hull box of its orbit, as portrait.py uses), split by the number of in-box
neighbours of the added cell.
    python3 research/audit/c_rows/z10_outside.py PERTURB_JSON
(perturb.py writes research/scratch/clockwork/perturb_P66.27a.json.)"""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'clockwork'))
from cw import catalogue, orbit, hull_ranges, hull_cells, nbrs
o = catalogue()['P66.27a']
orb = orbit(frozenset(map(tuple, o['cells'])), o['period'])
box = set(map(tuple, hull_cells(hull_ranges(frozenset().union(*orb)))))
print('box cells', len(box))
recs = json.load(open(sys.argv[1]))
by = {}
for r in recs:
    c = tuple(r['cell'])
    if r['was_live'] or c in box: continue
    k = sum(1 for q in nbrs(c) if tuple(q) in box)
    by.setdefault(k, Counter())[r['fate']] += 1
for k in sorted(by):
    n = sum(by[k].values()); print(f'outside the box, {k} in-box neighbours: n = {n}, {dict(by[k])}, breaks {by[k]["breaks"] / n:.1%}')
