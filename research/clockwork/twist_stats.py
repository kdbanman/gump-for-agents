#!/usr/bin/env python3
"""Twist statistics of the box census: for every object of period >= 3, twist m = |orbit symmetry| / |phase symmetry|
(the phase shift group image; period = m x quotient length).  Groups by period, and by whether the object's union is its whole diagonal hull.
  twist_stats.py   (reads scratch/clockwork/census_3_objects.json, written by box_census.py report 3)"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import SCR, orbit, sym_order, spacetime_sym, hull_cells, hull_ranges  # noqa: E402
objs = json.load(open(os.path.join(SCR, 'census_3_objects.json')))
rows = []
for k, d in objs.items():
    c0 = frozenset(tuple(map(int, t.split(','))) for t in k.split()); P = d['period']
    ph = orbit(c0, P - 1)
    m = spacetime_sym(ph) // sym_order(c0)
    U = frozenset().union(*ph)
    rows.append((P, m, len(U) == len(hull_cells(hull_ranges(U)))))   # fills its own diagonal hull
json.dump(rows, open(os.path.join(SCR, 'twist_rows.json'), 'w'))
for lab, sel in [('all objects', lambda r: True), ('fills own hull', lambda r: r[2]), ('does not', lambda r: not r[2])]:
    t = defaultdict(Counter)
    for P, m, f in rows:
        if sel((P, m, f)):
            band = 'P3-6' if P <= 6 else 'P7-16' if P <= 16 else 'P17+'
            t[band][m] += 1
    print(lab, {b: dict(sorted(t[b].items())) for b in ('P3-6', 'P7-16', 'P17+')})
ev = defaultdict(Counter)
for P, m, f in rows:
    if P % 2 == 0 and P >= 8:
        ev[P][m > 1] += 1
print('even P>=8: twisted / untwisted', {P: (c[True], c[False]) for P, c in sorted(ev.items())})
