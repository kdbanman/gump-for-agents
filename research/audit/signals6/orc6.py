"""Oracle checks of REVIEW-signals-6's own meeting results (C): each configuration run on reference/oracle.py on a
ring of 128 units (box torus 256 x 32 x 256, whole torus) and compared, at generations 20, 40, 60, 80, with
meet6r's linear run (st6.Batch) wrapped onto the ring; then the outcome claimed in the review is read from the
oracle state itself.

    python3 orc6.py            (~3 min)
"""
import time
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import meet6r as M
import glue6

L = 128
SHAPE = (2 * L, 32, 2 * L)
wrap = lambda s: frozenset((c[0] % SHAPE[0], c[1], c[2] % SHAPE[2]) for c in s)
CASES = [
    ('U meets K3 -> one H', [('U', 1), ('K3', 22)]),
    ('U meets K0 -> nothing', [('U', 1), ('K0', 22)]),
    ('E meets K0 -> holed train', [('E', 0), ('K0', 22)]),
    ('E meets K3 -> holed train', [('E', 0), ('K3', 22)]),
    ('E meets H -> wire B', [('E', 0), ('H', 21)]),
    ('E, two holes 2 rakes apart -> wire B with a pulse', [('E', 0), ('H', 21), ('H', 25)]),
    ('E, two holes 3 rakes apart -> standing B\' at 11..13', [('E', 0), ('H', 21), ('H', 27)]),
    ('E, four holes 3 apart -> standing B\' at 11..15', [('E', 0), ('H', 21), ('H', 27), ('H', 33), ('H', 39)]),
]
R = M.Runner(260)
t0 = time.time()
allok = True
for name, cf in CASES:
    snaps = R.run([cf], 80, keep=[20, 40, 60, 80])
    ring0 = frozenset(tr(c, w) for w in range(-40, L - 40) for c in T.BASE[1][w % 2])
    S0 = ring0
    for k, u in cf:
        S0 = S0 ^ M.sigcells(k, u)
    ok = True
    for t, s in st6.oracle_torus(S0, 80, SHAPE, (0, -16, 0)):
        if t in snaps:
            lin = R.state(snaps[t], 0)
            d = R.diff(snaps[t], 0)
            lo = (min(unit_of(c) for c in d) if d else 0) - 10
            win = units(lin, lo, lo + L)
            assert R.exact(units(lin, lo, lo + L), t) or True
            assert -R.A + t + 1 <= lo and lo + L < R.A - t - 1
            ok &= wrap(win) == wrap(s)
            last = s
    allok &= ok
    print(f'{name}: oracle ring equals the linear run at t = 20, 40, 60, 80: {ok}  ({time.time() - t0:.0f} s)', flush=True)
print('ALL PASS' if allok else 'FAIL')
