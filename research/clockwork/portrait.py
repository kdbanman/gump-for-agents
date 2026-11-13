#!/usr/bin/env python3
"""Phase portrait of a closed box by uniform sampling: every distinct cycle reached, its basin fraction, and
what it contains.   portrait.py OID|RANGES NS [SEED]   (OID: use that catalogue object's own hull)"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import sym_order, spacetime_sym, catalogue, orbit, hull_ranges, hull_cells, cell_vessel, step, canon, components, fmt_key, SCR  # noqa
arg, ns = sys.argv[1], int(sys.argv[2])
if arg.startswith('S6:'):   # S6 box about d4 centred at the vertex (3,3,3): radius a along d4, b along the others
    a_, b_ = map(int, arg[3:].split(','))
    arg = '%d,%d,%d,%d,%d,%d,%d,%d' % (9 - b_, 9 + b_, 3 - b_, 3 + b_, 3 - b_, 3 + b_, 3 - a_, 3 + a_); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
cat = catalogue(); keyid = {fmt_key(tuple(map(tuple, o['cells']))): k for k, o in cat.items()}
if arg in cat:
    o = cat[arg]; orb = orbit(frozenset(map(tuple, o['cells'])), o['period']); rng = hull_ranges(frozenset().union(*orb))
else:
    v = list(map(int, arg.split(','))); rng = [(v[2 * k], v[2 * k + 1]) for k in range(4)]
cells = hull_cells(rng); v = cell_vessel(cells)
print('# box cells', len(cells), flush=True)
res = []
for chunk in range(0, ns, 200000):
    res += v.run(os.path.join(SCR, f'portrait_{os.getpid()}.bin'), min(200000, ns - chunk), 0.5, seed * 1000 + chunk // 200000, 10 ** 6)
cyc = Counter(); ph = {}
for r in res:
    S = frozenset(v.cells[i] for i in r['live']); P = r['period']
    if P >= 3:
        orb = [S]
        for _ in range(P - 1): orb.append(step(orb[-1]))
        k = min(tuple(sorted(q)) for q in orb); cyc[(P, k)] += 1; ph[(P, k)] = orb
pc = Counter(r['period'] for r in res)
print(f'box {rng} cells={len(cells)} samples={ns} periods={sorted(pc.items())}')
print('max transient', max(r['mu'] for r in res), 'median', sorted(r['mu'] for r in res)[ns // 2])
out = []
for (P, k), n in sorted(cyc.items(), key=lambda kv: (-kv[0][0], -kv[1])):
    orb = ph[(P, k)]; U = frozenset().union(*orb)
    objs = []
    for comp in components(U, 2):
        q = [x & comp for x in orb]
        per = next(d for d in range(1, P + 1) if P % d == 0 and all(q[(t + d) % P] == q[t] for t in range(P)))
        key = fmt_key(min(canon(x) for x in q[:per]))
        objs.append('%s(p%d,u%d)' % (keyid.get(key, 'NEW'), per, len(frozenset().union(*q))))
    m = spacetime_sym(orb) // sym_order(orb[0]) if P >= 7 else 0
    if P >= 7:
        print('P%-3d twist %d basin %.2e (%d)  union %d  %s' % (P, m, n / ns, n, len(U), ' + '.join(objs)))
    out.append(dict(period=P, twist=m, count=n, union=len(U), objects=objs, phase0=fmt_key(sorted(orb[0]))))
json.dump(dict(ranges=rng, ns=ns, periods=sorted(pc.items()), cycles=out), open(os.path.join(SCR, f'portrait_{arg}_{ns}.json'), 'w'))
