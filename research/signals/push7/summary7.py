#!/usr/bin/env python3
"""Tables of a census7 run: ends by size (cells at generation 0 of the list entry) and period, outcomes per event,
outcome vectors, and the candidates (any outcome but healed / dead / wireB:dead / wireB:wall / periodic-no-wire).

    python summary7.py CENSUS.json [CENSUS.json ...] [--guns] [--out ENDS.json]

--out writes the ends compactly (cap cells, period, size, plane bound C at which the list entry was found, outcome
vector) for the record.
"""
import sys, os, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import census7 as C

files = [a for a in sys.argv[1:] if a.endswith('.json') and not a.startswith('--')]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
files = [f for f in files if f != out]
rows = []
for fn in files:
    rows += json.load(open(fn))['rows']
print(f'{len(rows)} distinct ends')
evs = [tuple(o['ev']) for o in rows[0]['outcomes']]


def evname(ev):
    typ, arg, dt = ev
    if typ == 'word':
        return 'holes' + ','.join(map(str, arg))
    if typ == 'sig':
        return C.NAMES[arg] + ('' if dt == 0 else f'+{dt}')
    return 'wireB-edge'


size = Counter((r['cells'], r['period']) for r in rows)
print('ends by size (cells of the list entry at generation 0) and period:')
for p in sorted({k[1] for k in size}, key=lambda x: (x is None, x)):
    line = ', '.join(f'{c}: {size[(c, p)]}' for c in sorted({k[0] for k in size}) if size[(c, p)])
    print(f'  period {p}: {sum(v for k, v in size.items() if k[1] == p)} ends; by cells {line}')
tab = defaultdict(Counter)
for r in rows:
    for o in r['outcomes']:
        tab[evname(tuple(o['ev']))][o['out']] += 1
print('outcomes per event:')
for e in tab:
    print(f'  {e:16s} ' + ', '.join(f'{k} {v}' for k, v in sorted(tab[e].items())))
vec = Counter(tuple(o['out'] for o in r['outcomes']) for r in rows)
print(f'{len(vec)} distinct outcome vectors over {len(evs)} events; the most common:')
for v, n in vec.most_common(12):
    print(f'  {n:6d} ' + ' '.join(x.replace('healed', 'h').replace('dead', 'd').replace('wireB:', 'B:') for x in v))
ordinary = {'healed', 'dead', 'wireB:dead', 'wireB:wall', 'wireB:periodic-no-wire', 'wireB:cap'}
cand = [(r, o) for r in rows for o in r['outcomes'] if o['out'] not in ordinary]
print(f'candidates (an outcome other than {sorted(ordinary)}): {len(cand)}')
for r, o in cand[:40]:
    print(f"  end {r['i']} of {r['src']} ({r['cells']} cells, period {r['period']}): {evname(tuple(o['ev']))}: {o['out']} at {o['t']}")
if out:
    json.dump(dict(events=[evname(e) for e in evs], ends=[dict(src=r['src'], i=r['i'], C=r['C'], lo=r['lo'], hi=r['hi'],
                                                              cells=r['cells'], period=r['period'], cap=r['cap'],
                                                              out=[o['out'] for o in r['outcomes']]) for r in rows]),
              open(out, 'w'), separators=(',', ':'))
    print(f'wrote {out} ({os.path.getsize(out) // 1024} KB)')
