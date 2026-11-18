#!/usr/bin/env python3
"""lab: one experiment form for both steppers of a8 (REVIEW-signals-8).

    play(word, ops, G, sim='box' | 'orc', rcap=None, every=None)

Start: a8.cell_state(word) (capL, the word from unit 4, the right cap).  ops: {generation: [(kind, cell), ...]} with
kind 'kill' (the cell must be live), 'add' (must be dead) or 'flip'.  Returns the set of live cells at generation G
(and, with `every`, a list of (generation, cells) every `every` generations).  With sim='box' the box's `touch` flag
is returned as well: (cells, touch).
"""
import a8
from a8 import tr, SR, SL


def R(u):
    return ('kill', tr(SR, u))


def L(u):
    return ('kill', tr(SL, u))


def play(word, ops, G, sim='box', rcap=None, every=None, wide=False, pad_units=6):
    N = len(word)
    kw = dict(ylo=-12, yhi=14, wlo=-12, whi=20) if wide else {}
    S = (a8.Orc if sim == 'orc' else a8.Box)(-pad_units, N + 10 + pad_units, **kw)
    h = S.arr(a8.cell_state(word, rcap))
    hist = []
    for g in range(G + 1):
        if every and g % every == 0:
            hist.append((g, S.cells(h)))
        for kind, c in ops.get(g, []):
            if kind == 'kill':
                S.kill(h, c)
            elif kind == 'add':
                assert c not in S.cells(h), ('already live', c); S.flip(h, [c])
            else:
                S.flip(h, [c])
        if g < G:
            h = S.run(h, 1)
    out = S.cells(h)
    touch = getattr(S, 'touch', False)
    return (out, touch, hist) if every else (out, touch)


def lett(cells, N):
    return a8.letters_of(cells, 4, 4 + N)


def is_state(cells, word, rcap=None):
    if '?' in word or '_' in word:
        return False
    return cells == a8.cell_state(word, rcap)


def settle(word, ops, G, sim='box', rcap=None, wide=False):
    """run to G and to G + 2; returns (description, cells at G).  Description: the hex letters if the whole state is
    exactly the cell with those letters and is unchanged 2 generations later; otherwise '[letters pop n flags]' with
    flags m = still changing, T = a live cell reached the box's outer layer (st8 run not exact)."""
    N = len(word)
    kw = dict(ylo=-12, yhi=14, wlo=-12, whi=20) if wide else {}
    S = (a8.Orc if sim == 'orc' else a8.Box)(-6, N + 16, **kw)
    h = S.arr(a8.cell_state(word, rcap))
    for g in range(G):
        for kind, c in ops.get(g, []):
            if kind == 'kill':
                S.kill(h, c)
            elif kind == 'add':
                assert c not in S.cells(h), ('already live', c); S.flip(h, [c])
            else:
                S.flip(h, [c])
        h = S.run(h, 1)
    c0 = S.cells(h)
    h = S.run(h, 2) if sim == 'orc' else S.run(h.copy(), 2)
    still = S.cells(h) == c0
    w = lett(c0, N)
    touch = getattr(S, 'touch', False)
    if still and is_state(c0, w, rcap):
        return w, c0
    return f"[{w} pop {len(c0)}{'' if still else ' m'}{' T' if touch else ''}]", c0


def short(desc):
    """a compact outcome name: E = the empty cell; k@p = one stretch of k units of d with its first unit at wire
    place p (0 = unit 4); other exact states by run-length letters; inexact states as given"""
    import re
    if desc.startswith('['):
        m = re.match(r'\[(\S+) pop (\d+)(.*)\]', desc)
        return ('DEAD%s' % m.group(2) if set(m.group(1)) <= set('_') else 'X:' + a8.rle(m.group(1)) + '/' + m.group(2)) + m.group(3).replace(' ', '')
    if set(desc) == {'7'}:
        return 'E'
    m = re.fullmatch(r'(7*)(d+)f(7*)', desc)
    if m:
        return '%d@%d' % (len(m.group(2)), len(m.group(1)))
    return a8.rle(desc)
