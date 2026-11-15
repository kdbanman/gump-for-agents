"""Which entries of the census lists does the push's key (census_ends.key_of) merge that census5.key keeps apart, and
are they translates (tau^k E(t - 2k) for some k, any time shift) of each other?  python3 pairs5.py (about 30 s)"""
import json, os
from census5 import LISTS, orbit_D, key
from st5 import train, unit, tr, step


def pushkey(p, D, t0=0):
    # census_ends.key_of: each d(t) moved to lowest unit 0, with the parity of t; as a set
    return frozenset(tuple(sorted(tr(c, -min(unit(q) for q in s)) for c in s)) + (('par', (t0 + j) % 2),) for j, s in enumerate(D))


rows = []
for fn in LISTS:
    d = json.load(open(fn))
    for i, e in enumerate(d['list']):
        cap = [tuple(c) for c in e['cap']]
        p, D = orbit_D(cap, d['KS'], d['T'])
        rows.append((os.path.basename(fn), i, p, D, key(p, D), pushkey(p, D)))
from collections import defaultdict
bypk = defaultdict(list)
for r in rows:
    bypk[r[5]].append(r)
print('push key classes', len(bypk), '; my key classes', len({r[4] for r in rows}))
n = 0
for pk, rs in bypk.items():
    mk = {r[4] for r in rs}
    if len(mk) > 1:
        n += 1
        a, b = rs[0], [r for r in rs if r[4] != rs[0][4]][0]
        # exact test: is b's orbit some tau^k a(t + s)?
        rel = [(k, s) for k in range(-6, 7) for s in range(a[2]) if all(frozenset(tr(c, k) for c in a[3][(t + s) % a[2]]) == b[3][t] for t in range(a[2]))]
        if n <= 14:
            print(f'merged by the push key, distinct here: {a[0]}#{a[1]} and {b[0]}#{b[1]}; sizes by phase {[len(s) for s in a[3]]} vs {[len(s) for s in b[3]]}; (k, time shift) with b = tau^k a(t+s): {rel}')
print(n, 'push-key classes hold more than one end')
