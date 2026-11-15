#!/usr/bin/env python3
"""Corollary 2 check: O1 events (T5's drive: a cell with n(t) >= 6 live neighbours that was live at t-1) on the bare
wires and with each pulse, counted on a ring of 24 cubes (own sparse stepper modulo the ring only), 48 generations.

    python3 drive.py
"""
import json, subprocess
from collections import Counter
from lat import sstep_ring, canon_ring, nbrs, wire, ROOT

N = 24
for name, rev in (('pulse-A', 'bcd5844'), ('pulse-B', 'bcd5844'), ('pulse-B-left', '896f44b'), ('pulse-S', 'bcd5844')):
    ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'{rev}:research/signals/objects/{name}.json']))
    cr = lambda cells: frozenset(canon_ring(c, N) for c in cells)
    for label, x in (('bare', cr(wire(ob['bg'], 0, N))), ('pulse', cr(wire(ob['bg'], 0, N)) ^ cr(map(tuple, ob['defect'])))):
        prev = None; per = []; live_at_t = 0
        for t in range(48):
            cnt = Counter()
            for c in x:
                for q in nbrs(c):
                    cnt[canon_ring(q, N)] += 1
            if prev is not None:
                ev = [c for c, k in cnt.items() if k >= 6 and c in prev]
                per.append(len(ev)); live_at_t += sum(c in x for c in ev)
            prev, x = x, sstep_ring(x, N)
        print(f'{name:13s} {label:5s}: O1 events per generation over gens 1..47: {sorted(Counter(per).items())}; '
              f'of them live at t: {live_at_t} of {sum(per)}')
