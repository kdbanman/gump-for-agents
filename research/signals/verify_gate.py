#!/usr/bin/env python3
"""Verify the collision gate of wire C with reference/oracle.py as the judge.

    python3 verify_gate.py objects/gate-C.json

The file gives the wire (`bg`, one repeat; repeat vector v), a right-moving object `right` and a left-moving object
`left` (cells flipped relative to the wire at generation 0), and cases: the left object is started `sep` units
further along the ring than where it is given.  Stepping: oracle.masks / oracle.step on the cubic array torus only.
For each case three runs of T generations are compared cell for cell over the whole torus: both objects together,
`right` alone, `left` alone (and the bare wire).  A case expects
  "left"   the run with both ends EXACTLY as the run with `left` alone: the right-mover has vanished without trace
           and the left-mover is not delayed or changed;
  "right"  the same with the roles exchanged.
In every case it is also checked that the two single runs differ from each other and from the bare wire (each
object alone is still on its way at generation T).  As a truth table, with R, L = "a pulse was sent from that side":
a case "left" computes (left output, right output) = (L, R and not L); a case "right" computes (L and not R, R).
"""
import json, sys
import sg

ob = json.load(open(sys.argv[1]))
v = ob['v']; C = ob['cubes']; H = 2 * C; T = ob['T']
mod = lambda c: (c[0] % H, c[1] % H, c[2] % H)
tr = lambda cells, k: frozenset(mod((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)
bg0 = frozenset().union(*[tr([tuple(c) for c in ob['bg']], k) for k in range(C)])
run = lambda x: [st for t, st in sg.oracle_run(x, (H, H, H), T) if t == T][0]
print(f"{ob['name']}: wire of {len(ob['bg'])} cells per unit, ring of {C} units on the cubic torus (H = {H}); T = {T}", flush=True)
bgT = run(bg0); ok = True
for case in ob['cases']:
    R = frozenset(mod(tuple(c)) for c in case.get('right', ob['right'])); L = tr([tuple(c) for c in case.get('left', ob['left'])], case['sep'])
    both = run(bg0 ^ R ^ L); onlyR = run(bg0 ^ R); onlyL = run(bg0 ^ L)
    sane = len({both, onlyR, onlyL, bgT} | {onlyR, onlyL, bgT}) >= 3 and onlyR != bgT and onlyL != bgT and onlyR != onlyL
    good = sane and both == (onlyL if case['expect'] == 'left' else onlyR)
    print('PASS' if good else 'FAIL', f"{case.get('what', 'pulse against pulse')}, left one started {case['sep']} units along: after {T} generations the state is "
          f"exactly the state of the run with the {case['expect']}-mover alone ({len(onlyR ^ bgT)} / {len(onlyL ^ bgT)} cells differ from the bare wire in the single runs)", flush=True)
    ok &= good
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
