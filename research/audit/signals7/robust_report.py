#!/usr/bin/env python3
"""Summary of `line7c.py robust` (files line7c_robust_*.json in scratch): per spacing s and number of holes n, how many
of the gun x end pairs give the object the rule predicts, and which ends are the exceptions."""
import json, glob, os
from collections import Counter, defaultdict
import orc7 as O

rows = []
for fn in sorted(glob.glob(os.path.join(O.SCR, 'line7c_robust_*.json'))):
    rows += json.load(open(fn))
pairs = {(r['gun'], r['end']) for r in rows}
print(f'{len(pairs)} pairs (guns {sorted({r["gun"] for r in rows})}, {len({r["end"] for r in rows})} ends)')
tab = defaultdict(Counter); exc = defaultdict(set)
for r in rows:
    for k, sg in r['sig'].items():
        s, n = map(int, k.split(','))
        exp = 'plain' if (n == 1 or s < 3) else f'{38 + s}:' + 'd' * n + 'f'
        tab[s][(n, sg == exp)] += 1
        if sg != exp:
            exc[s].add(r['end'])
for s in sorted(tab):
    ok = sum(v for (n, good), v in tab[s].items() if good); bad = sum(v for (n, good), v in tab[s].items() if not good)
    print(f'  spacing {s}: {ok} runs as the rule (plain for n = 1{" and for every n" if s < 3 else "; n units of B-prime at unit " + str(38 + s)}), {bad} not'
          + (f'; the exceptions are all with ends {sorted(exc[s])}' if bad else ''))
