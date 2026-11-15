#!/usr/bin/env python3
"""Loop counts: the lead's shorts()/gram_of_hnf() against lattices.py, on every class with loop^2 >= 7 at A <= 126.
    python3 research/wrap/loopcheck.py"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lattices as L  # noqa: E402
src = open(os.path.join(HERE, '..', 'audit', 'wrap_law_lead.py')).read()
ns = {}
exec(src.split("FROZEN = dict")[0].replace("NOSLAB = '--noslab' in sys.argv", "NOSLAB = False"), ns)   # the two functions only
bad = n = 0
for A in range(36, 127, 3):
    for g, reps in L.classes(A).items():
        if g[0] < 7:
            continue
        mine = [q for q in L.loops(*reps[0], 20)]
        for h, k, d in reps:
            n += 1
            if ns['gram_of_hnf'](h, k, d) != mine or ns['shorts'](g) != mine:
                bad += 1; print('DIFFER', A, g, (h, k, d), mine, ns['gram_of_hnf'](h, k, d), ns['shorts'](g))
print(f'{n} lattices checked, {bad} differ')
