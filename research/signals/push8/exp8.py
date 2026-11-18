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


def hexletters(L, a, u0, u1):
    """hex family letters of units u0..u1-1 at an even phase ('?' if a unit is not stators + sites; '_' empty)"""
    out = []
    for u in range(u0, u1):
        uc = L.unit_cells(a, u)
        if not uc:
            out.append('_'); continue
        rest = uc - set(W.ST)
        if len(uc - rest) != 2 or not rest <= set(W.SITES):
            out.append('?'); continue
        out.append('%x' % sum(1 << i for i in range(4) if W.SITES[i] in rest))
    return ''.join(out)


def ring_test(word, n=40, gens=40, bg='7'):
    """does `word` (hex letters) in a ring of n units of wire bg move rigidly?  returns (shift per 2 generations or None, hex string after gens)"""
    L = Lab(0, n, ring=True)
    s = bg * 10 + word + bg * (n - 10 - len(word))
    a = L.arr(hexword(s, 0)); b = a.copy()
    L.run(b, 2)
    sh = None
    for d in (-1, 0, 1):
        if np.array_equal(b, L.arr(hexword(''.join(s[(i - d) % n] for i in range(n)), 0))):
            sh = d
    L.run(b, gens - 2)
    return sh, hexletters(L, b, 0, n)


def hexrle(s):
    out = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i] + ('^%d' % (j - i) if j - i > 2 else s[i] * (j - i - 1))); i = j
    return ''.join(out).replace('^', '{').replace('{', '^')


def shoot(mid, sig, side, dist=10, nL=40, nR=40, G=120, g0=0):
    """the word `sig` (hex) put in the wire B of line(mid, nL, nR) with its nearest unit `dist` units from the
    stretch (side 'L': to the left of it, 'R': to the right), at generation g0; returns the hex letters at g0 + G
    (units 4..4+N-1, run-length), the left and right cap states ('ok' if as undisturbed), and the period."""
    obj, N = line(mid, nL, nR)
    L = lab_for(N); a = L.arr(obj); L.run(a, g0); r = a.copy()
    w0 = 4 + nL; w1 = w0 + len(mid) - 1
    u = (w0 - dist - len(sig)) if side == 'L' else (w1 + 1 + dist)
    L.flip(a, hexword('7' * len(sig), u) ^ hexword(sig, u))
    L.run(a, G); L.run(r, G)
    capl = 'ok' if np.array_equal(L.units(a, -6, 4), L.units(r, -6, 4)) else 'CHANGED'
    capr = 'ok' if np.array_equal(L.units(a, 4 + N, N + 16), L.units(r, 4 + N, N + 16)) else 'CHANGED'
    return hexrle(hexletters(L, a, 4, 4 + N)), capl, capr
