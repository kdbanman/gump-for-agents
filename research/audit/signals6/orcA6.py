"""A of REVIEW-signals-6 on the oracle: three ends of the census (#0 the C = 31 absorber, #10 capA's end, #300), each
with two of the scan's up-making events (#16 'rm g0 unit0 2/6' -> E, #221 'rm g2 unit0 1/6' -> U), stepped with
reference/oracle.py on a box torus (finite train of units -100..5, the end, whole torus), 60 generations: the
difference between the evented and the undisturbed run must be, at generation 42, exactly the bare-train difference
(the signal, computed here with st6 on a bare train) and lie at least 6 units below the end.

    python3 orcA6.py          (~3 min)
"""
import json, os, time
import numpy as np
import st6
from st6 import tr, unit_of, units
import trains6 as T
import scan6a as S6

ends = json.load(open(os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals5', 'ends.json')))['ends']
ev = S6.events()
t0 = time.time()
ok = True
for j in (16, 221):
    nm, g, _ = ev[j]
    fl = S6.flips_of(ev[j])
    # bare difference at 42 (st6, long piece)
    P = T.train5(0, -200, 120); Q = None
    for t in range(43):
        if t == g:
            Q = P ^ fl
        P = st6.step(P) if t < 42 else P
        if Q is not None and t < 42:
            Q = st6.step(Q)
    dbare = units(P ^ Q, -100, 100)
    for i in (0, 10, 300):
        cap = frozenset(tuple(c) for c in ends[i]['cap'])
        x0 = T.train5(0, -100, 6) | cap
        xs = list(st6.oracle_torus(x0, 42, (480, 40, 480), (-260, -20, -240)))
        y = xs[g][1] ^ fl
        ys = list(st6.oracle_torus(y, 42 - g, (480, 40, 480), (-260, -20, -240)))
        d = xs[42][1] ^ ys[-1][1]
        far = min(unit_of(c) for c in xs[42][1] ^ T.train5(42, -100, 30) if unit_of(c) > -50)
        good = d == dbare and max(unit_of(c) for c in d) <= far - 6
        ok &= good
        print(f'end #{i}, event #{j} ({nm}): oracle difference at 42 = the bare signal ({len(d)} cells, units '
              f'{min(unit_of(c) for c in d)}..{max(unit_of(c) for c in d)}), end from unit {far}: {good}  ({time.time() - t0:.0f} s)', flush=True)
print('ALL PASS' if ok else 'FAIL')
