#!/usr/bin/env python3
"""wire8 (push 8): the four-site family of wires along (1,0,-1), letters for kymographs, push 7's standing lines.

Units: unit u holds the cells with x in {2u, 2u+1}; tr(c, k) moves a cell k units towards +v.
Family unit (README section 9): stators (0,1,2), (0,1,4) and a subset of sites 0 = (1,0,0), 1 = (1,0,2),
2 = (1,0,4), 3 = (0,2,3).  B = 7, C = b, B' = d, C' = e.  All four have period 2.
Letters: one character per unit.  'B' 'C' 'P' 'Q' = a unit of wire B, C, B', C' in the phase expected at that
generation (phase = generation mod 2 when the object was laid at phase 0 at generation 0); lower case = the other
phase; '8' / 'o' wire 8 (stators and (0,2,3)); '_' empty; '#' anything else.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8
from lab8 import tr, unit, Lab

ST = [(0, 1, 2), (0, 1, 4)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
HEX = {'B': 7, 'C': 0xb, 'P': 0xd, 'Q': 0xe, '8': 8}


def fam(h):
    return frozenset(ST + [SITES[i] for i in range(4) if h >> i & 1])


def _templates():
    T = {}; PH = {}
    for name, h in HEX.items():
        L = Lab(0, 8, ring=True); a = L.arr([tr(c, u) for u in range(8) for c in fam(h)])
        for ph in range(2):
            uc = L.unit_cells(a, 3); T[uc] = (name, ph); PH[(name, ph)] = uc
            L.run(a, 1)
        assert L.unit_cells(a, 3) == PH[(name, 0)]
    return T, PH


TEMPL, PHASE = _templates()


def wire(name, ua, ub, ph=0):
    """cells of units ua..ub-1 of wire `name` ('B', 'C', 'P', 'Q', '8') at phase ph"""
    return frozenset(tr(c, u) for u in range(ua, ub) for c in PHASE[(name, ph)])


def word(s, u0=0, ph=0):
    """cells of a word of unit letters laid from unit u0 (each letter a wire unit at phase ph; '_' empty)"""
    out = set()
    for i, ch in enumerate(s):
        if ch != '_':
            out |= wire(ch, u0 + i, u0 + i + 1, ph)
    return frozenset(out)


def letter(uc, t=0):
    if not uc:
        return '_'
    k = TEMPL.get(uc)
    if k is None:
        return '#'
    name, ph = k
    if name == '8':
        return '8' if ph == t % 2 else 'o'
    return name if ph == t % 2 else name.lower()


def letters(L, a, t=0, u0=None, u1=None):
    u0 = L.ua if u0 is None else u0; u1 = L.ub if u1 is None else u1
    return ''.join(letter(L.unit_cells(a, u), t) for u in range(u0, u1))


def push7_line(n):
    """(y0, flips) of push 7's line record with E and n holes (n = 1..4); flips = {generation: cells}"""
    d = json.load(open(os.path.join(HERE, '..', 'push7', 'objects7.json')))
    r = next(r for r in d['records'] if r['name'] == 'line-N80-gun4-end70-n%d' % n)
    return [tuple(c) for c in r['y0']], {f[0]: [tuple(c) for c in f[1]] for f in r['flips']}


def run_push7(n, gens, L=None):
    """the push-7 line with E and n holes (n = 0: the line alone) after `gens` generations: (Lab, array)"""
    y0, flips = push7_line(max(n, 1))
    if n == 0:
        flips = {}
    L = L or Lab(-8, 92)
    a = L.arr(y0)
    for g in range(gens):
        if g in flips:
            L.flip(a, flips[g])
        L.run(a, 1)
    return L, a
