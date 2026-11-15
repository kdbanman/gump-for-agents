#!/usr/bin/env python3
"""The instance `sat_turn.py 16 47 --KS 10 --lo -1 --hi 7 --eat 16` (README section 18, left unanswered) settled by
direct test.  Its solutions are among the period-2 caps that turn a lone rake with class 2 at T = 16, C = 47 in the
5 x 5 tube; that list is complete at 8 (`k2caps.py 16 47`, CaDiCaL, 15 min; kept in scratch/signals/k2caps_16_47.json).
The extra condition: a lone p> (the cells `wl.pulse_cells('R', 0, 0)` of sat_turn.py, units 6 and 7, flipped at
generation 0, the cap's first unit being 10) is swallowed and the object is as it was 16 generations later.

    python3 eat_direct.py            # needs scratch/signals/k2caps_16_47.json (python3 k2caps.py 16 47)

For each of the 8 caps: unlit, is it of period 2; lit by the p>, at which generations t <= 120 does the state on
units >= -20 equal the unlit one of the same parity.  None, for all 8: the instance is UNSAT.
Stepping: sg.step_set (not the oracle)."""
import json
import sg, scat, turnclass as tc
from scat import unit

d = json.load(open(sg.os.path.join(sg.SCR, 'k2caps_16_47.json')))
obj = lambda f: json.load(open(sg.os.path.join(sg.HERE, 'objects', f)))
wl = scat.Wire(obj('pulse-C.json'), obj('pulse-C-left.json'))
pin = frozenset(wl.pulse_cells('R', 0, 0))
print('p> cells flipped at generation 0:', sorted(pin), 'units', sorted({unit(c) for c in pin}))
near = lambda s: frozenset(c for c in s if unit(c) >= -20)
bad = 0
for n, e in enumerate(d):
    cap = frozenset(tuple(c) for c in e['cap'])
    base = frozenset(c for u in range(-60, 10) for c in tc.uc(0xb, u)) | cap
    b1 = sg.step_set(base)
    stat = near(sg.step_set(b1)) == near(base)
    x = base ^ pin
    hits = []
    for t in range(1, 121):
        x = sg.step_set(x)
        if near(x) == near(base if t % 2 == 0 else b1):
            hits.append(t)
    bad += bool(hits) or not stat
    print(f'#{n} {len(cap)} cells; unlit period 2: {stat}; restored at generations: {hits or "never (t <= 120)"}; '
          f'after 120: units -20..9 = {tc.dec(x, -20, 10)}, live cells beyond unit 9: {len([c for c in x if unit(c) >= 10])}')
print('none of the 8 is restored: the --eat instance is UNSAT' if not bad else 'SOME CAP IS RESTORED OR NOT PERIOD 2: look')
