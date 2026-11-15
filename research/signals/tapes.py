#!/usr/bin/env python3
"""Tapes: pairs of unit types of the four-site family (family.py; a unit = the two stators plus a subset of the
four sites, written as a hex digit) such that EVERY sequence of the two types moves rigidly along the wire.

    python3 tapes.py

For each of the 120 pairs {a, b} of the 16 unit types and each of the 32 windows of 5 units over {a, b}: the
window is stepped 2 generations on the infinite lattice (sg.step_set; units beyond the window are filled with a
copy of its end units, which cannot matter: 2 generations reach 2 units) and the middle unit is compared with the
unit that was to its right (the pattern moves towards -v), to its left (towards +v), or itself (stands still).
A pair for which all 32 windows agree on one of these is a tape: by the light cone every infinite sequence of the
two unit types then moves (or stands) exactly.  objects/tape-BC.json is the pair {7, b} = {B, C} on the oracle.
"""
import itertools
import sg, scat, family as F

tr = scat.tr; unit = scat.unit
cells = lambda m: F.unit_cells([i for i in range(4) if m >> i & 1])
found = []
for a, b in itertools.combinations(range(16), 2):
    verdict = {'towards -v': True, 'towards +v': True, 'stands': True}
    for w in itertools.product((a, b), repeat=5):
        seq = [w[0]] * 3 + list(w) + [w[4]] * 3                      # units -5 .. 5, the window at -2 .. 2
        x = frozenset(tr(c, u - 5) for u, m in enumerate(seq) for c in cells(m))
        y = sg.step_set(sg.step_set(x))
        mid = frozenset(c for c in y if unit(c) == 0)
        verdict['towards -v'] &= mid == cells(w[3]); verdict['towards +v'] &= mid == cells(w[1]); verdict['stands'] &= mid == cells(w[2])
        if not any(verdict.values()):
            break
    for k, v in verdict.items():
        if v:
            found.append((a, b, k))
print('pairs of unit types of which every sequence moves rigidly (2 generations per unit) or stands:')
for a, b, k in found:
    print('   {%x, %x}  %s   %s' % (a, b, k, ' '.join(F.NAMES.get(tuple(i for i in range(4) if m >> i & 1), '') for m in (a, b))))
