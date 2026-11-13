#!/usr/bin/env python3
"""Collect new objects (period >= 17, or twist >= 3 with period >= 7) from portrait_*.json files, skip those already
in the catalogue or in objects/*.cells, name them C<period>.<minpop><letter>, save objects/<id>.cells and
append to objects/portrait_objects.jsonl.   harvest_portraits.py FILE.json ..."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import (catalogue, orbit, components, canonical_orbit, sym_order, spacetime_sym, hull_cells, hull_ranges,
                thickness, write_cells, read_cells, fmt_key, step)  # noqa: E402
HERE = os.path.dirname(os.path.abspath(__file__))
cat = catalogue()
known = {fmt_key(tuple(map(tuple, o['cells']))): k for k, o in cat.items()}
names = set()
for fn in glob.glob(os.path.join(HERE, 'objects', '*.cells')):
    c = read_cells(fn); n = os.path.basename(fn)[:-6]; names.add(n)
    P = int(n[1:].split('.')[0]); known[fmt_key(canonical_orbit(orbit(c, P - 1))[0])] = n
out = open(os.path.join(HERE, 'objects', 'portrait_objects.jsonl'), 'a')
for fn in sys.argv[1:]:
    d = json.load(open(fn))
    for cy in d['cycles']:
        if cy['period'] < 7:
            continue
        S = frozenset(tuple(map(int, t.split(','))) for t in cy['phase0'].split())
        ph = orbit(S, cy['period'] - 1); U = frozenset().union(*ph)
        for comp in components(U, 2):
            q = [x & comp for x in ph]; L = len(q)
            P = next(p for p in range(1, L + 1) if L % p == 0 and all(q[(t + p) % L] == q[t] for t in range(L)))
            co = canonical_orbit(q[:P]); key = fmt_key(co[0])
            if key in known:
                continue
            c0 = frozenset(co[0]); ph2 = orbit(c0, P - 1)
            m = spacetime_sym(ph2) // sym_order(c0)
            if not (P >= 17 or (m >= 3 and P >= 7)):
                continue
            mp = min(map(len, ph2)); k = 0
            while 'C%d.%d%s' % (P, mp, 'abcdefghijklmnop'[k]) in names:
                k += 1
            name = 'C%d.%d%s' % (P, mp, 'abcdefghijklmnop'[k]); names.add(name); known[key] = name
            Uc = frozenset().union(*ph2)
            rec = dict(id=name, period=P, minpop=mp, maxpop=max(map(len, ph2)), union=len(Uc),
                       hull=len(hull_cells(hull_ranges(Uc))), layers=list(thickness(Uc)), sym=sym_order(c0),
                       spacetime_sym=spacetime_sym(ph2), twist=m, quotient_length=P // m, source=os.path.basename(fn),
                       cells=[list(c) for c in sorted(c0)])
            write_cells(os.path.join(HERE, 'objects', name + '.cells'), c0,
                        '%s: period %d, union %d, twist %d (quotient length %d); phase 0; from %s' % (name, P, len(Uc), m, P // m, os.path.basename(fn)))
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(name, P, 'union', len(Uc), 'hull', rec['hull'], 'twist', m, 'L', P // m, rec['layers'])
