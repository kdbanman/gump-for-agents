#!/usr/bin/env python3
"""Verify the two-way wall (a register: a memory that is written from one side and erased from the other) with
reference/oracle.py as the judge.

    python3 verify_register.py objects/register-BBp.json

The object is finite and stands in empty space: a cap, a stretch of wire B, a stretch of wire B', a cap.  The file
gives `frame` (the cells of the two caps and of the wire units that never change), the two unit cells `B` and
`Bp`, and the range [ua, ub) of units in between: with the wall at w, units ua..w-1 are B and units w..ub-1 are B'
(unit u = unit cell moved by u*(2,0,-2)).  Operations, each a ONE-cell flip of a live cell:
  W  at an even generation flip `write` (a cell of wire B that never changes): a pulse B runs towards the wall;
  E  at an odd generation flip `erase` (a cell of wire B' that never changes): a pulse B' runs towards the wall.
Checks, all with oracle.masks and oracle.step on the cubic array torus (the object is far smaller than the torus):
  A  the object alone, wall at w0, is the same every 2 generations for the whole length of the run;
  B  after each operation of `sequence`, `gap` generations later, the WHOLE state is exactly the object with the
     wall one unit nearer the side the pulse came from: W: w -> w-1, E: w -> w+1.  So the state after any sequence
     depends only on (#E - #W), and E undoes W exactly.
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
C = ob['cubes']; H = 2 * C
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
frame = [tuple(c) for c in ob['frame']]; B = [tuple(c) for c in ob['B']]; Bp = [tuple(c) for c in ob['Bp']]
ua, ub, w0, gap = ob['ua'], ob['ub'], ob['w0'], ob['gap']


def cells(w):
    s = set(frame)
    for u in range(ua, ub):
        s |= {tr(c, u) for c in (B if u < w else Bp)}
    return s


def arr(cs):
    h = np.zeros((H, H, H), np.int8)
    for c in cs:
        assert sg.is_cell(c)
        h[c[0] % H, c[1] % H, c[2] % H] = 1
    assert int(h.sum()) == len(cs)
    return h


m = oracle.masks(H)
seq = ob['sequence']
print(f"{ob['name']}: {len(cells(w0))} cells, units {ua}..{ub - 1} between the caps, wall at {w0}; torus of side {C} cubes; "
      f"sequence {seq}, {gap} generations per operation", flush=True)
ok = True
h0 = arr(cells(w0)); h = h0.copy(); T = gap * len(seq)
good = True
for t in range(T):
    h = oracle.step(h, m)
    if t % 2 == 1 and not (h == h0).all():
        good = False; break
print('PASS' if good else 'FAIL', f'A  the object alone is the same every 2 generations for {T} generations'); ok &= good
h = h0.copy(); w = w0; nb = 0
for k, op in enumerate(seq):
    if op == 'W':
        c = tuple(ob['write'])
    else:
        h = oracle.step(h, m); c = tuple(ob['erase'])
    assert h[c[0] % H, c[1] % H, c[2] % H] == 1, 'the flipped cell must be live'
    h[c[0] % H, c[1] % H, c[2] % H] = 0
    for _ in range(gap - (op == 'E')):
        h = oracle.step(h, m)
    w += -1 if op == 'W' else 1
    good = bool((h == arr(cells(w))).all())
    nb += good
    print('PASS' if good else 'FAIL', f'B  operation {k + 1} ({op}): {gap} generations later the whole state is the object with the wall at {w}', flush=True)
    ok &= good
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
