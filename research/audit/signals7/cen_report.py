#!/usr/bin/env python3
"""Tables from census7a.py output, and the comparison of oracle rows with fast7 rows.

    python3 cen_report.py FILE.json [FILE.json ...] [--oracle ORC.json [ORC.json ..]]

Prints: outcomes per event, outcome vectors, and for the 'dead' rows the two diagnostics of census7a (how many of the 70
units between the far region and the end differ from the undisturbed run when the difference arrives far upstream;
how many cells are left on units >= KS).  With --oracle: every row of the oracle files is compared with the row of the
same end in FILEs (outcome, generation and diagnostics of every event).
"""
import sys, json
from collections import Counter

args = sys.argv[1:]
orc = []
if '--oracle' in args:
    k = args.index('--oracle'); orc = args[k + 1:]; args = args[:k]
rows = {}
for fn in args:
    d = json.load(open(fn))
    for r in d['rows']:
        rows[r['i']] = r
print(f'{len(rows)} ends (of {d["nends"]} distinct in the list)')
rs = [rows[i] for i in sorted(rows)]
print('all orbits of period dividing 4:', all(r['orbit'] for r in rs))
sz = Counter(r['cells'] for r in rs)
print(f'cells of the list entry (units >= 6, generation 0; depends on which translate was listed first): {min(sz)}..{max(sz)}, mode {sz.most_common(1)[0][0]}')
if 'sizes' in rs[0]:
    s0 = Counter(min(r['sizes']) for r in rs)
    print(f'cells on the end\'s own units, least over its four generations: {min(s0)}..{max(s0)}, mode {s0.most_common(1)[0][0]}')
    print('periods (of the units >= KS):', dict(Counter(r.get('period') for r in rs)))
evs = [tuple(map(str, o['ev'])) for o in rs[0]['outcomes']]
for k, ev in enumerate(evs):
    ct = Counter(r['outcomes'][k]['out'] for r in rs)
    print(f'  {ev[0]:6s} {ev[1]:22s} ' + ', '.join(f'{o} {v}' for o, v in sorted(ct.items())))
vec = Counter(tuple(o['out'] for o in r['outcomes']) for r in rs)
print(f'{len(vec)} outcome vectors:')
for v, n in vec.most_common():
    print(f'  {n:5d} ' + ' '.join(x.replace('healed', 'h').replace('dead', 'd').replace('wireB:', 'B:') for x in v))
dead = [(r, o) for r in rs for o in r['outcomes'] if o['out'] == 'dead']
if dead:
    mid = Counter(o['mid'] for r, o in dead); ec = Counter(min(o['endcells'], 1) for r, o in dead)
    print(f'{len(dead)} dead rows: units (of 70) between the far region and the end that differ at that generation: ' +
          ', '.join(f'{m}: {n}' for m, n in sorted(mid.items())))
    print(f'   end (units >= KS) empty at that generation: {ec[0]}; not empty: {ec[1]}')
    print(f'   generation of arrival far upstream: {min(o["t"] for r, o in dead)}..{max(o["t"] for r, o in dead)}')
    if 'rakes' in dead[0][1]:
        rk = Counter(o['rakes'] for r, o in dead)
        print('   rake units left on those 70 units (the plain train has 35): ' + ', '.join(f'{m}: {n}' for m, n in sorted(rk.items())))
    low = [(r['i'], o['ev'], o['mid'], o['t']) for r, o in dead if o['mid'] < 60]
    print(f'   rows with fewer than 60 of the 70 units differing (a candidate for "changed, with the stream left"): {len(low)}', low[:10])
heal = [o['t'] for r in rs for o in r['outcomes'] if o['out'] == 'healed']
if heal:
    print(f'{len(heal)} healed rows: whole ring equal from generation {min(heal)}..{max(heal)} at the latest')
other = Counter(o['out'] for r in rs for o in r['outcomes'] if o['out'] in ('sent', 'alive', 'horizon'))
print('rows sent / alive / horizon:', dict(other))
if orc:
    n = bad = 0
    for fn in orc:
        for r in json.load(open(fn))['rows']:
            n += 1
            f = rows.get(r['i'])
            if f is None or f['cap'] != r['cap'] or f['outcomes'] != r['outcomes'] or f['orbit'] != r['orbit']:
                bad += 1; print('  DIFFERENT: end', r['i'])
    print(f'oracle rows: {n}; equal to the fast7 row of the same end in every field: {n - bad}; different: {bad}')
