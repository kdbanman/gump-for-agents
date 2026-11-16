#!/usr/bin/env python3
"""How the reflector makes the echo (README section 33): the line with the oscillator beside capA
(research/audit/signals5/end_echo.json, records 0 and 2), with and without the hole, compared with the line and the
oscillator stepped apart.     python3 stroke6.py     (10 s; sg.step_set)

For each run, at every generation: J = the joint state stepped once; S = (its line part stepped alone) | (its
oscillator part stepped alone), where the oscillator part is the cells within the support of the free oscillator's
orbit... printed: the generations and cells where J and S differ (the coupling), in the plain run and in the holed
run."""
import json
import echo6 as E, sg

recs = json.load(open(E.os.path.join(E.ROOT, 'research', 'audit', 'signals5', 'end_echo.json')))
for ri in (0, 1, 2, 3):
    r = recs[ri]
    osc0 = frozenset(map(tuple, r['oscillator'])); line0 = frozenset(map(tuple, r['line']))
    orb = [osc0]
    while True:
        n = sg.step_set(orb[-1])
        if n == osc0:
            break
        orb.append(n)
    sup = frozenset().union(*orb)
    P = len(orb)
    for holed in (False, True):
        X = line0 | osc0
        for t in range(r['tg']):
            X = sg.step_set(X)
        if holed:
            X = X - {tuple(r['hole'])}
        coup = []
        for t in range(r['tg'], r['tg'] + 60):
            J = sg.step_set(X)
            o = X & sup; l = X - sup
            S = sg.step_set(o) | sg.step_set(l)
            if J != S:
                coup.append((t + 1, sorted(J - S), sorted(S - J)))
            X = J
        print(f"{r['osc']} gap {r['gap_k']} {'holed' if holed else 'plain'}: oscillator period {P}; coupling events "
              f"(generation, born only jointly, dead only jointly): {coup[:6]}{' ...' if len(coup) > 6 else ''} ({len(coup)} in 60 generations)")
