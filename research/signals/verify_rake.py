#!/usr/bin/env python3
"""Verify the rake of wire C (one cell that travels and emits a pulse every 2 generations) and what stops it, with
reference/oracle.py as the judge.

    python3 verify_rake.py objects/rake-C.json

Wire C is closed into a ring of `cubes` units on the cubic array torus; everything is stepped with oracle.masks /
oracle.step.  `rake` is ONE cell, dead in the wire; `pulse_left` the two cells of the left-moving pulse of wire C
(verify_pulse.py objects/pulse-C-left.json); all given for unit 0, unit u = moved by u*(2,0,-2).
  A  rake alone, switched on at unit u0 at generation 0: for m = 1 .. M, at generation 2m the state is EXACTLY
     the wire + the rake cell at unit u0+m + one left-moving pulse at each of the units u0+m-2, u0+m-4, ..., u0-m.
     So the rake moves one unit per 2 generations and leaves the wire behind it as it was except for a train of
     pulses two units apart, one more every 2 generations.
  B  `eaten`: a left-moving pulse started at unit u0+sep meets the rake head-on: at generation T the state is exactly
     that of the run with the rake alone (the pulse is gone, the rake undisturbed).
  C  `stops`: the same with sep one more: at generation T there is no rake: the state is the wire + left-moving
     pulses only, at the units listed (the train already emitted, and one more), and 2 generations later it is the
     same state moved one unit towards -v.
"""
import json, sys
import sg

ob = json.load(open(sys.argv[1]))
v = ob['v']; C = ob['cubes']; H = 2 * C
mod = lambda c: (c[0] % H, c[1] % H, c[2] % H)
tr = lambda cells, k: frozenset(mod((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)
bg0 = frozenset().union(*[tr([tuple(c) for c in ob['bg']], k) for k in range(C)])
rake = [tuple(ob['rake'])]; pl = [tuple(c) for c in ob['pulse_left']]
u0 = ob['u0']; M = ob['M']
assert mod(rake[0]) not in bg0
print(f"{ob['name']}: wire C, ring of {C} units on the cubic torus (H = {H})", flush=True)
ok = True
bad = []
for t, st in sg.oracle_run(bg0 ^ tr(rake, u0), (H, H, H), 2 * M):
    if t and t % 2 == 0:
        m = t // 2
        exp = bg0 ^ tr(rake, u0 + m)
        for k in range(1, m + 1):
            exp = exp ^ tr(pl, u0 + m - 2 * k)
        if st != exp:
            bad.append(t)
good = not bad
print('PASS' if good else 'FAIL', f'A  rake alone: at generation 2m the state is the wire, the rake cell m units on and m left-moving pulses two units apart, m = 1 .. {M}' + ('' if good else f' (fails at {bad[:5]})')); ok &= good
for case in ob['cases']:
    T = case['T']; x0 = bg0 ^ tr(rake, u0) ^ tr(pl, u0 + case['sep'])
    states = {t: st for t, st in sg.oracle_run(x0, (H, H, H), T + 2) if t >= T}
    if case['expect'] == 'eaten':
        alone = [st for t, st in sg.oracle_run(bg0 ^ tr(rake, u0), (H, H, H), T) if t == T][0]
        good = states[T] == alone
        print('PASS' if good else 'FAIL', f"B  a left-moving pulse started {case['sep']} units ahead of the rake: at generation {T} the state is exactly that of the rake alone", flush=True)
    else:
        exp = bg0
        for u in case['pulses_at']:
            exp = exp ^ tr(pl, u)
        good = states[T] == exp and states[T + 2] == frozenset(mod((c[0] - 2 * v[0], c[1] - 2 * v[1], c[2] - 2 * v[2])) for c in states[T])
        print('PASS' if good else 'FAIL', f"C  a left-moving pulse started {case['sep']} units ahead of the rake: at generation {T} no rake; the wire and {len(case['pulses_at'])} left-moving "
              f"pulses at units {case['pulses_at']}, all moving on unchanged", flush=True)
    ok &= good
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
