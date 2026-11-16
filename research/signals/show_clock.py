#!/usr/bin/env python3
"""Draw a shuttle clock (objects/clock-C.json) as text: one character per unit of wire, one line per 2 generations.

    python3 show_clock.py [N] [GENS]

b = a unit of wire C as it stands; f = the rake going towards +v (one extra cell); 7 = a pulse going towards -v;
5f = the rake going towards -v; 9f = a pulse going towards +v; ? = cap cells.  (The characters are the hex mask of
which of the four sites (1,0,0), (1,0,2), (1,0,4), (0,2,3) of the unit are alive; family.py.)  Steps: sg.step_set.
"""
import json, sys
import sg, scat, family as F

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
gens = int(sys.argv[2]) if len(sys.argv) > 2 else 4 * N + 2 + 2 * N + 10
ob = json.load(open('objects/clock-C.json'))
x = {tuple(c) for c in ob['capL']} | {scat.tr(tuple(c), k) for c in ob['unit'] for k in range(N)} | {scat.tr(tuple(c), N) for c in ob['capR']}
x = frozenset(x | {scat.tr(tuple(ob['ignite']), N // 2)})
for t in range(gens + 1):
    if t % 2 == 0:
        by = {}
        for c in x:
            by.setdefault(scat.unit(c), set()).add(scat.tr(c, -scat.unit(c)))
        row = ''
        for u in range(-5, N + 5):
            s = by.get(u, set())
            if not s:
                row += '.'
            elif s - set(F.STATOR) - set(F.SITES) or not set(F.STATOR) <= s:
                row += '?'
            else:
                row += '%x' % sum(1 << i for i in range(4) if F.SITES[i] in s)
        print('%4d %s' % (t, row))
    x = sg.step_set(x)
