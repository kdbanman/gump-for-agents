#!/usr/bin/env python3
"""exp8 (push 8): building blocks for experiments on the standing line (wire B between push 7's two caps).

capL, capR: the two caps of push 7's standing line (gun 4 and mirrored end 70 after E and holes), cut from the
run of record line-N80-gun4-end70-n3 at generation 880 (units 0..3 and 80..84) and cached in objects/caps.json.
line(mid, nL, nR): capL on units 0..3, then the word 7^nL + mid + 7^nR (hex family letters) from unit 4, then capR.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W
from lab8 import tr, unit, Lab

CAPS = os.path.join(HERE, 'objects', 'caps.json')


def caps():
    if not os.path.exists(CAPS):
        L, a = W.run_push7(3, 880)
        cells = L.cells(a)
        capL = sorted(c for c in cells if unit(c) <= 3)
        capR = sorted(tr(c, -80) for c in cells if unit(c) >= 80)
        json.dump(dict(note="caps of push 7's standing line (record line-N80-gun4-end70-n3 at generation 880): capL on units 0..3 "
                            "(wire B at phase 0 from unit 4 on), capR on units 0..4 (wire B at phase 0 up to unit -1); doubled coordinates",
                       capL=capL, capR=capR), open(CAPS, 'w'))
    d = json.load(open(CAPS))
    return frozenset(tuple(c) for c in d['capL']), frozenset(tuple(c) for c in d['capR'])


CAPL, CAPR = caps()


def hexword(s, u0=0):
    out = set()
    for i, ch in enumerate(s):
        if ch != '_':
            out |= set(tr(c, u0 + i) for c in W.fam(int(ch, 16)))
    return frozenset(out)


def line(mid='', nL=10, nR=10):
    """(cells, N): capL + 7^nL mid 7^nR + capR; the wire occupies units 4..4+N-1, capR units 4+N..8+N"""
    s = '7' * nL + mid + '7' * nR
    N = len(s)
    return CAPL | hexword(s, 4) | frozenset(tr(c, 4 + N) for c in CAPR), N


def lab_for(N, wide=False):
    if wide:
        return Lab(-6, N + 16, -10, 14, -10, 18)
    return Lab(-6, N + 16)


def kymo(L, a, gens, every=2, t0=0, ref=None, u0=None, u1=None, out=None):
    """letters every `every` generations; if ref (an array run in lockstep) is given, units that differ are shown
    with the letter and a line of '^' below."""
    lines = []
    a = a.copy(); r = None if ref is None else ref.copy()
    for g in range(0, gens + 1, every):
        s = W.letters(L, a, t0 + g, u0, u1)
        if r is not None:
            lo = L.ua if u0 is None else u0; hi = L.ub if u1 is None else u1
            d = ''.join('^' if not np.array_equal(L.units(a, u, u + 1), L.units(r, u, u + 1)) else ' ' for u in range(lo, hi))
            lines.append(f'{t0 + g:5d} {s}')
            if d.strip():
                lines.append(f'      {d}')
        else:
            lines.append(f'{t0 + g:5d} {s}')
        L.run(a, every)
        if r is not None:
            L.run(r, every)
    txt = '\n'.join(lines)
    if out:
        open(out, 'w').write(txt + '\n')
    return txt


def diff_units(L, a, r):
    return [u for u in range(L.ua, L.ub) if not np.array_equal(L.units(a, u, u + 1), L.units(r, u, u + 1))]


def rle(s):
    """run-length form of a letter string: B12 P3 # B20 ..."""
    out = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i] + (str(j - i) if j - i > 1 else '')); i = j
    return ' '.join(out)


RIGHT, LEFT = (0, 1, 2), (0, 1, 4)     # stator cells: removing one at phase 0 emits a pulse towards +v / -v
PULSE_R = [(1, 0, 0), (2, 2, 1)]        # pulse B towards +v at phase 0: flips relative to wire B (unit u: site 0 off; unit u+1: site 3 on)


def pulseR(u):
    return [tr(c, u) for c in PULSE_R]


def pulseL(u):
    """the left-going pulse at phase 0: unit u of wire B becomes a unit of wire C ((1,0,4) off, (0,2,3) on)"""
    return [tr((1, 0, 4), u), tr((0, 2, 3), u)]
