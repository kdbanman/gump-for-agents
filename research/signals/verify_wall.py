#!/usr/bin/env python3
"""Verify the moving walls between wire B and wire C (the left-going pulses of both wires are the shortest cases)
with reference/oracle.py as the judge.

    python3 verify_wall.py

Finite objects in empty space, units numbered along (1,0,-1).  Left end: the eater cap of wire B (seglab.py) for
objects that begin with B, capL of objects/clock-C.json for those that begin with C; right end likewise (capR).
Claims, each checked cell for cell over the whole torus at every even generation 2j, j = 1 .. J:
  1  B on units < w, C on units >= w: the wall is at w - j (wire C grows into wire B, one unit per 2 generations);
  2  C on units < w, B on units >= w: the wall is at w - j (wire B grows into wire C);
  3  C everywhere but B on units a .. b-1: the stretch of B is at a-j .. b-1-j (length 1: the pulse p< of wire C);
  4  B everywhere but C on units a .. b-1: the stretch of C is at a-j .. b-1-j (length 1: the left pulse of wire B).
"""
import json, sys
import numpy as np
import sg, scat, seglab, family as F
oracle = sg.oracle
tr = scat.tr; unit = scat.unit
ob = json.load(open('objects/clock-C.json'))
UB = F.unit_cells((0, 1, 2)); UC = F.unit_cells((0, 1, 3))
n = 24
o = seglab.Obj(left=([('B', n)], 'eater'), right=([('B', n)], 'eater'))
BL = frozenset(c for c in o.cells if unit(c) < -n); BR = frozenset(c for c in o.cells if unit(c) >= n)      # eater caps of B at -n and n
CL = frozenset(tr(tuple(c), -n) for c in ob['capL']); CR = frozenset(tr(tuple(c), n) for c in ob['capR'])


def obj(kind):
    """kind(u) in 'B', 'C' for units -n .. n-1; caps to match the two ends."""
    cells = set()
    for u in range(-n, n):
        cells |= {tr(c, u) for c in (UB if kind(u) == 'B' else UC)}
    return frozenset(cells | (BL if kind(-n) == 'B' else CL) | (BR if kind(n - 1) == 'B' else CR))


def run(cells, J):
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    mk = oracle.masks(H); out = []
    for t in range(2 * J + 1):
        if t % 2 == 0:
            out.append(frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in zip(*np.nonzero(h))))
        h = oracle.step(h, mk)
    return out


ok = True
J = 12
cases = [('1  B|C: the wall moves towards -v, C grows', lambda j: (lambda u: 'B' if u < 6 - j else 'C')),
         ('2  C|B: the wall moves towards -v, B grows', lambda j: (lambda u: 'C' if u < 6 - j else 'B'))]
for L in (1, 2, 3, 7):
    cases.append((f'3  a stretch of {L} units of B in wire C moves towards -v', lambda j, L=L: (lambda u: 'B' if 6 - j <= u < 6 - j + L else 'C')))
    cases.append((f'4  a stretch of {L} units of C in wire B moves towards -v', lambda j, L=L: (lambda u: 'C' if 6 - j <= u < 6 - j + L else 'B')))
for title, k in cases:
    states = run(obj(k(0)), J)
    good = all(states[j] == obj(k(j)) for j in range(1, J + 1)) and states[1] != states[0]
    ok &= good
    print('PASS' if good else 'FAIL', title, f'one unit per 2 generations, exactly, for {J} units (oracle)')
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '- walls between wire B and wire C')
sys.exit(0 if ok else 1)
