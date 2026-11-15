#!/usr/bin/env python3
"""Cut experiment: does a wire burn from a cut end?

    python3 cut_wires.py [N] [GAP ...]     # default N = 48 repeats, gaps 1 2 3 24; ~1 min

Each wire is laid N repeats long on a ring; `gap` consecutive repeats are removed, in each phase of the wire, and the
result is run beside the intact wire.  The difference between the two is tracked per repeat (sgc.c track): `lo`, `hi`
are how far (in repeats, from the middle of the gap) the damage reaches.  Outcomes: `capped` (the cut wire settles
into a cycle; reach = furthest repeat ever touched on each side), `burns` (the damage spans the ring), `open` (no cycle
by MAXGEN).  A fuse shows as `burns`.
"""
import sys
import numpy as np
import wirelab as wl

N = int(sys.argv[1]) if len(sys.argv) > 1 else 48
GAPS = list(map(int, sys.argv[2:])) or [1, 2, 3, 24]
MAXGEN = 20000
tot = {}
for rec in wl.all_wires():
    g = wl.ring(rec, N)
    P = rec['period']
    orb = g.orbit(wl.wire_state(g, rec), P - 1)
    line = []
    for gap in GAPS:
        u0 = N // 2
        keep = np.ones(g.n + 1, np.uint8)
        lo_u, hi_u = u0 - gap // 2, u0 - gap // 2 + gap - 1          # removed repeats
        keep[:g.n] = (g.unit < lo_u) | (g.unit > hi_u)
        res = []
        for t in range(P):
            r = g.track(orb[t], orb[t] & keep, u0, span=N - 1, maxgen=MAXGEN)
            left = lo_u - (u0 + int(r['lo'].min())); right = (u0 + int(r['hi'].max())) - hi_u
            kind = {0: 'heals', 1: 'capped', 2: 'burns', 3: 'open'}[r['ret']]
            res.append((kind, r['gens'], r['per'], left, right))
        kinds = sorted(set(k for k, *_ in res))
        mx = (max(x[3] for x in res), max(x[4] for x in res))
        line.append('gap %d: %s reach -%d/+%d gens<=%d per %s' % (gap, '/'.join('%s %d' % (k, sum(1 for x in res if x[0] == k)) for k in kinds),
                                                                 mx[0], mx[1], max(x[1] for x in res), sorted(set(x[2] for x in res))))
        for x in res:
            tot[x[0]] = tot.get(x[0], 0) + 1
    print(rec['id'], 'P%d' % P, tuple(rec['v']), ' | '.join(line), flush=True)
print('totals over wires, gaps and phases:', tot)
