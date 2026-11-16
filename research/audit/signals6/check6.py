"""Check st6.step (sparse) and st6.Batch (tube batch) against reference/oracle.py on the whole state.

    python3 check6.py          (~2 min)

Cases (finite pieces on an even torus large enough that nothing wraps; whole state compared every generation):
  (a) the push-frame train, units -30..30, with 10 events: one-cell flips making E, U, H, K0, a 'break', a
      'vanish', a two-cell flip, a flip outside the 3x3 tube (Batch on the wide tube -3..9), 70 generations;
  (b) review-5-frame train with four ends of the census and an event 16 units in front of each, 70 generations.
"""
import json, os, time
import numpy as np
import st6
from st6 import tr, unit_of
import trains6 as T

T.check()


def compare(cells0, gens, lo=1, hi=9 ** 9, ua=-200, ub=200, label=''):
    xs = [c[0] for c in cells0]; zs = [c[2] for c in cells0]
    # box: x in [min-2g-8, max+2g+8], z likewise, y in [-20, 20)
    ox = (min(xs) - 2 * gens - 8) & ~1; oz = (min(zs) - 2 * gens - 8) & ~1
    sx = ((max(xs) + 2 * gens + 8 - ox) // 2 + 1) * 2; sz = ((max(zs) + 2 * gens + 8 - oz) // 2 + 1) * 2
    orc = st6.oracle_torus(cells0, gens, (sx, 40, sz), (ox, -20, oz))
    s = frozenset(cells0)
    import kinds6
    cells = [c for u in range(ua, ub) for c in kinds6._tube_unit(u, lo, hi)]
    B = st6.Batch(cells); v = B.vec(s)[None, :]
    for t, o in orc:
        assert o == s, (label, 'sparse', t)
        assert B.set_of(v[0]) == o, (label, 'batch', t)
        s = st6.step(s); v = B.step(v)
    return gens


t0 = time.time()
n = 0
ev = [(0, [(1, 0, 0)]), (3, [(0, 0, 3)]), (1, [(0, 0, 5)]), (1, [(0, 1, 4)]), (0, [(0, 1, 2)]), (2, [(1, 0, 4)]),
      (1, [(0, 0, 1), (2, 1, 2)]), (2, [(3, 0, 2), (2, -1, 0)])]
for f, cl in ev:
    s = T.train(f, -30, 30) ^ frozenset(cl)
    n += compare(s, 70, 1, 5, -110, 110, label=(f, cl))
for f, c in [(0, (1, 4, 0)), (1, (0, -3, 0)), (2, (3, 4, 0))]:
    assert st6.is_cell(c) and not st6.in_tube(c)
    s = T.train(f, -30, 30) ^ frozenset([c])
    n += compare(s, 70, -3, 9, -110, 110, label=(f, c))
ends = json.load(open(os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals5', 'ends.json')))['ends']
for i, (g, c) in zip([0, 9, 10, 300], [(0, (1, 0, 4)), (1, (0, 1, 2)), (2, (1, 0, 0)), (3, (0, 0, 5))]):
    cap = frozenset(tuple(q) for q in ends[i]['cap'])
    s = T.train5(0, -40, 6) | cap
    for _ in range(g):
        s = st6.step(s)
    cell = tr(c, -10 + g // 2)
    s = s ^ frozenset([cell])
    n += compare(s, 70, 1, 5, -120, 40, label=('end', i))
print(f'ALL PASS: {n} generations compared on the whole state, sparse and batch, {time.time() - t0:.0f} s')
