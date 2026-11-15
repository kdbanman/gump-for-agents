#!/usr/bin/env python3
"""Verify a transmission (L2) with reference/oracle.py as the judge.

    python3 verify_transmission.py objects/transmission-B.json

The file gives the wire (`bg`, one repeat at generation 0, repeat vector v), a receiver (`receiver`: cells flipped
relative to the wire at generation 0, a stationary defect), the cell `flip` at place A, the times of the shots and the
torus.  Everything is stepped with oracle.masks / oracle.step on the cubic array torus; the only intervention is that
at each shot time the one cell at A is flipped.  Two runs are made side by side: the *signalled* run and a *control*
run in which A is never touched.  Checks:
  A  before the first shot the wire with its receiver is stationary (period 2), and the receiver is at least
     `min_distance` cubes from A;
  B  in the control run nothing ever changes (same state every 2 generations to the end);
  C  after each shot k = 1, 2, ...: the signalled run is again stationary (period 2); it differs from the bare wire
     only inside the receiver's window (so the wire between A and B, and A itself, are exactly as they were); and the
     receiver has changed: its set of differing cells is the previous set plus `step_cells` new cells, the same new
     cells each time moved one repeat towards A;
  D  between shots, while the pulse is under way, the signalled run differs from the control run in a small moving
     set of cells (the pulse): half-way, between 1 and `pulse_cells_max` cells, strictly between A and the receiver,
     besides what earlier shots wrote at the receiver.
"""
import json, sys
import numpy as np
import sg
sys.path.insert(0, sg.ROOT + '/reference')
import oracle

ob = json.load(open(sys.argv[1]))
v = ob['v']; C = ob['cubes']; H = 2 * C
mod = lambda c: (c[0] % H, c[1] % H, c[2] % H)
tr = lambda cells, k: frozenset(mod((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)
bg0 = frozenset().union(*[tr([tuple(c) for c in ob['bg']], k) for k in range(C)])
recv = frozenset(mod(tuple(c)) for c in ob['receiver'])
flip = mod(tuple(ob['flip']))
shots = ob['shots']; gap = ob['gap']; t_first = ob['t_first']
m = oracle.masks(H)


def arr(cells):
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c] = 1
    return h


cells_of = lambda h: frozenset(map(tuple, np.argwhere(h).tolist()))
xcube = lambda c: (c[0] // 2) % C                  # cube index along the ring (x advances one cube per repeat)
ax, rx = xcube(flip), sorted(xcube(c) for c in recv)
dist = min((u - ax) % C for u in rx)
print(f"{ob['name']}: wire of {len(ob['bg'])} cells per cube, ring of {C} cubes on the cubic torus (H = {H}); A = cell {tuple(ob['flip'])} "
      f"(cube {ax}); receiver of {len(recv)} cells in cubes {rx[0]}..{rx[-1]}, {dist} cubes from A; {shots} shots, one every {gap} generations", flush=True)
ok = True
sig = arr(bg0 ^ recv); ctl = sig.copy(); bare = arr(bg0)
start = sig.copy()
t = 0


def advance(n):
    global sig, ctl, bare, t
    for _ in range(n):
        sig = oracle.step(sig, m); ctl = oracle.step(ctl, m); bare = oracle.step(bare, m); t += 1


advance(2); goodA = (sig == start).all() and dist >= ob['min_distance']
advance(t_first - 2)
goodA &= (sig == start).all()
print('PASS' if goodA else 'FAIL', f'A  wire + receiver is stationary (checked at generations 2 and {t_first}); receiver {dist} >= {ob["min_distance"]} cubes from A'); ok &= goodA
prev = cells_of(sig ^ bare); new_prev = None
window = lambda cells: all((xcube(c) - ax) % C >= ob['min_distance'] for c in cells)
for k in range(1, shots + 1):
    assert t % 2 == 0
    sig[flip] ^= 1                                 # the change made at A
    advance(gap // 2)
    d = cells_of(sig ^ ctl)
    record = prev - recv                           # what earlier shots wrote at the receiver (stationary)
    pulse_only = d - record
    goodD = record <= d and 1 <= len(pulse_only) <= ob['pulse_cells_max'] and all(0 < (xcube(c) - ax) % C < dist - k for c in pulse_only)
    advance(gap - gap // 2 - 2)
    a = sig.copy(); advance(2)
    stat = (sig == a).all()
    cur = cells_of(sig ^ bare)
    new = cur - prev
    grown = prev <= cur and len(new) == ob['step_cells'] and window(cur)
    moved = True if new_prev is None else new == tr(new_prev, -1)
    good = stat and grown and moved
    print('PASS' if good else 'FAIL', f'C  shot {k} (cell at A flipped at generation {t - gap}): at generation {t} stationary again; differs from the bare wire in '
          f'{len(cur)} cells, all at least {ob["min_distance"]} cubes from A; receiver = previous + {len(new)} new cells'
          + ('' if new_prev is None else ', the same as last time moved one cube towards A'), flush=True)
    print('PASS' if goodD else 'FAIL', f'D  shot {k}: half-way ({gap // 2} generations after the flip) the signalled and control runs differ in the '
          f'receiver\'s earlier record and in {len(pulse_only)} cells in transit, {min((xcube(c) - ax) % C for c in pulse_only) if pulse_only else "-"} cubes from A', flush=True)
    ok &= good and goodD
    prev, new_prev = cur, new
goodB = (ctl == start).all()
print('PASS' if goodB else 'FAIL', f'B  control run (A never touched): unchanged at generation {t}'); ok &= goodB
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
