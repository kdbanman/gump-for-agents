"""Lone-rake turn class of every cap state of scratch/signals/table_28_C.json (our own stepping, turn_check.py).
    python3 lone_census.py 29 31        (a few minutes)"""
import json, os, sys
from collections import Counter
import r3, turn_check as T
for C in sys.argv[1:]:
    D = json.load(open(os.path.join(T.SCR, f'table_28_{C}.json'))); tally = Counter(); cR = Counter()
    for sid, st in D['states'].items():
        cap0 = [tuple(c) for c in st]
        if not cap0:
            continue
        u0 = min(r3.unit(c) for c in cap0)
        K = 40; o, _ = T.lone_right({r3.tr(c, K - u0) for c in cap0}, K)
        if 'k' in o:
            tally['k=%d' % o['k']] += 1; cR[o['cR'] + 4 * u0] += 1
        else:
            tally['no turn'] += 1
    print(f'C = {C}: {dict(tally)}; exact constant c_R (cap frame of the table): {dict(cR)}', flush=True)
