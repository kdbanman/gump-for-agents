#!/usr/bin/env python3
"""Verify a front with reference/oracle.py as the judge.

    python3 verify_front.py objects/<name>.json

The file gives: the wire (wires/Wnn.json), the cubic torus side `cubes` (the oracle box is H = 2*cubes; the wire,
whose direction has x-component 1 per cube step, closes on itself after `cubes` steps), the repeat that is removed,
the time t0 at which the comparison starts, the claimed space-time period (p, s) and `side` (+1: the front moves
towards +v), the window (doubled x, relative to the removed repeat) and the number of periods.

What is checked, all with oracle.step on the cubic array-index torus (oracle.masks, oracle.step, nothing else):
  A. the intact ring of the wire returns to itself after P generations and not before (the background is a wire);
  B. for j = 1 .. periods:  the live cells with x in [a + j*s*dx, b + j*s*dx] at time t0 + j*p are exactly the live
     cells with x in [a, b] at time t0, translated by j*s repeats (dx = doubled x-step of one repeat);
  C. at time t0 + j*p the part of the window ahead of the front (the last `ahead` doubled x-units of it) is the
     intact wire of the same time (so the front is running into untouched wire), and the part behind differs from it.
Prints PASS or FAIL for each and a final line.
"""
import json, os, sys
import numpy as np
import sg
import wirelab as wl

fr = json.load(open(sys.argv[1]))
rec = wl.load(fr['wire']); v = rec['v']; P = rec['period']
C = fr['cubes']; H = 2 * C
assert abs(v[0]) >= 1 and C % abs(v[0]) == 0 and all((C // abs(v[0]) * t) % C == 0 for t in v)
R = C // abs(v[0])                       # repeats on the ring
dx = 2 * v[0]
unit = [tuple(c) for c in rec['cells']]
wire = sg.lift_periodic(unit, [v], [range(R)])
wire = frozenset((p[0] % H, p[1] % H, p[2] % H) for p in wire)
assert len(wire) == R * len(unit), 'the ring overlaps itself on this torus'
cut = fr['cut']
gone = frozenset(((p[0] + 2 * cut * v[0]) % H, (p[1] + 2 * cut * v[1]) % H, (p[2] + 2 * cut * v[2]) % H) for p in unit)
x0c = min(p[0] + 2 * cut * v[0] for p in unit) % H          # doubled x of the removed repeat
p_, s_, t0, per, side = fr['p'], fr['s'], fr['t0'], fr['periods'], fr['side']
a, b, ahead = fr['window'][0], fr['window'][1], fr['ahead']
T = t0 + per * p_
print(f"{fr['name']}: wire {fr['wire']} (period {P}, v = {tuple(v)}), {R} repeats on the cubic torus of side {C} cubes (H = {H}); "
      f"repeat {cut} removed at generation 0; claim: after t0 = {t0}, every p = {p_} generations the front has moved s = {s_} "
      f"repeat(s) towards {'+' if side > 0 else '-'}v; {per} periods, {T} generations in all", flush=True)

ok = True
# A: the background
orb = [st for _, st in sg.oracle_run(wire, (H, H, H), P)]
goodA = orb[P] == orb[0] and all(orb[t] != orb[0] for t in range(1, P))
print(('PASS' if goodA else 'FAIL'), f'A  the intact ring has period exactly {P} under the oracle'); ok &= goodA


def window(st, lo, hi):
    return frozenset(p for p in st if (p[0] - x0c - lo) % H <= hi - lo)


def shifted(st, k):
    return frozenset(((p[0] + 2 * k * v[0]) % H, (p[1] + 2 * k * v[1]) % H, (p[2] + 2 * k * v[2]) % H) for p in st)


ref = None
bgi = sg.oracle_run(wire, (H, H, H), T)
for (t, st), (_, bg) in zip(sg.oracle_run(wire - gone, (H, H, H), T), bgi):
    if t < t0 or (t - t0) % p_:
        continue
    j = (t - t0) // p_
    k = side * j * s_
    lo, hi = a + k * dx, b + k * dx
    w = window(st, lo, hi)
    if j == 0:
        ref = w
        print(f'     t = {t}: reference window x - x_cut in [{lo}, {hi}] holds {len(w)} live cells')
    else:
        good = w == shifted(ref, k)
        print(('PASS' if good else 'FAIL'), f'B  t = {t} (period {j}): window [{lo}, {hi}] equals the reference window shifted by {k} repeats ({len(w)} live cells)', flush=True)
        ok &= good
    fl, fh = (hi - ahead, hi) if side > 0 else (lo, lo + ahead)
    bl, bh = (lo, hi - ahead - 1) if side > 0 else (lo + ahead + 1, hi)
    goodC = window(st, fl, fh) == window(bg, fl, fh) and window(st, bl, bh) != window(bg, bl, bh)
    print(('PASS' if goodC else 'FAIL'), f'C  t = {t}: ahead of the front ({ahead} x-units) the wire is intact; behind it the state differs from the wire', flush=True)
    ok &= goodC
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', fr['name'])
sys.exit(0 if ok else 1)
