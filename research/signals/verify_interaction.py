#!/usr/bin/env python3
"""Verify an interaction of two pulses (L3) with reference/oracle.py as the judge.

    python3 verify_interaction.py objects/interaction-B.json

The file gives the wire (`bg`, repeat vector v), a right-moving pulse `right` and a left-moving pulse `left` (cells
flipped relative to the wire at generation 0; each alone is checked by verify_pulse.py), and cases: the left pulse is
started `sep` cubes further along the ring than where it is given.  Stepping: oracle.masks / oracle.step on the cubic
array torus only.  For each case, at generation T (after the pulses have met, before they could meet again on the
far side of the ring):
  pass   the state is exactly the wire with the right pulse moved T/2 cubes forward and the left pulse moved T/2
         cubes back: each has gone through the other without delay or change;
  stop   the state is stationary (same 2 and 40 generations later), and differs from the bare wire in exactly
         `mark` cells, which lie where the pulses met: both pulses are gone and a small standing mark is left.
"""
import json, sys
import sg

ob = json.load(open(sys.argv[1]))
v = ob['v']; C = ob['cubes']; H = 2 * C; T = ob['T']
mod = lambda c: (c[0] % H, c[1] % H, c[2] % H)
tr = lambda cells, k: frozenset(mod((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)
bg0 = frozenset().union(*[tr([tuple(c) for c in ob['bg']], k) for k in range(C)])
R = frozenset(mod(tuple(c)) for c in ob['right']); L = frozenset(mod(tuple(c)) for c in ob['left'])
print(f"{ob['name']}: wire of {len(ob['bg'])} cells per cube, ring of {C} cubes on the cubic torus (H = {H}); pulses of {len(R)} and {len(L)} cells", flush=True)
ok = True
for case in ob['cases']:
    sep = case['sep']
    x0 = bg0 ^ R ^ tr(L, sep)
    states = {t: st for t, st in sg.oracle_run(x0, (H, H, H), T + 40) if t in (T // 2 - 4, T, T + 2, T + 40)}
    bgT = [st for t, st in sg.oracle_run(bg0, (H, H, H), T) if t == T][0]
    if case['expect'] == 'pass':
        good = states[T] == bgT ^ tr(R, T // 2) ^ tr(L, sep - T // 2)
        print('PASS' if good else 'FAIL', f"pass  left pulse started {sep} cubes along: at generation {T} the state is the wire with both pulses "
              f"where they would be had they never met (moved {T // 2} cubes each)", flush=True)
    else:
        d = states[T] ^ bgT
        good = states[T + 2] == states[T] and states[T + 40] == states[T] and len(d) == case['mark']
        xs = sorted(set((c[0] // 2) % C for c in d))
        print('PASS' if good else 'FAIL', f"stop  left pulse started {sep} cubes along: at generation {T} the state is stationary (same at {T + 2} and {T + 40}) "
              f"and differs from the bare wire in {len(d)} cells, in cubes {xs}: {sorted(d)}", flush=True)
    ok &= good
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
