#!/usr/bin/env python3
"""Merge record files (make7.py, record7.py, line7.py) into objects7.json, storing each record's finite train
compactly: if y0 contains the plain train of the absorber frame (fb) or the gun frame (5f) at generation 0 on units
ulo .. KS-1, those cells are replaced by "train": [frame, ua, ub] and the file carries the two base patterns
(generation 0, cells of an even and an odd unit relative to the unit), which verify7.py expands.

    python merge7.py OUT.json IN.json [IN.json ...]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sat_gun as G
from scat import unit, tr

KS = 6
BASES = {}
for fr, d in (('fb', 1), ('5f', -1)):
    pat, _ = G.train([int(ch, 16) for ch in fr], True, d)
    BASES[fr] = [sorted(tr(c, -p) for c in G.train_cells(pat, 0, p, p + 1, d)) for p in (0, 1)]


def expand(fr, ua, ub):
    return {tr(tuple(c), u) for u in range(ua, ub) for c in BASES[fr][u % 2]}


out = []
for fn in sys.argv[2:]:
    for r in json.load(open(fn))['records']:
        y0 = {tuple(c) for c in r['y0']}
        for fr in ('fb', '5f'):
            tc = expand(fr, r['ulo'], KS)
            if tc <= y0 and len(tc) > 50:
                r['train'] = [fr, r['ulo'], KS]
                r['y0'] = [list(c) for c in sorted(y0 - tc)]
                break
        out.append(r)
names = [r['name'] for r in out]
assert len(names) == len(set(names)), 'duplicate record names'
json.dump(dict(note='push 7: objects for verify7.py (reference/oracle.py only). A record\'s initial state is y0 plus, '
                    'if "train" = [frame, ua, ub] is given, the plain train of that frame at generation 0 on units '
                    'ua .. ub-1 (unit u holds bases[frame][u % 2] moved by u units, i.e. by (2u, 0, -2u)).',
               bases=BASES, records=out), open(sys.argv[1], 'w'), separators=(',', ':'))
print(f'{sys.argv[1]}: {len(out)} records, {os.path.getsize(sys.argv[1]) // 1024} KB')
