"""Audit of push 8b: stores, readers and probes built from cells on file (the push's JSON objects and the first push's
definitions of wire B and its pulses in research/signals/README.md).  q.c stepper; nothing of the push's code.

Own frame of a wire: axis v = (1,0,-1), unit u = cells with x in {2u, 2u+1}, tube 1 <= x+y+z <= 5, 1 <= x-y+z <= 5.
Pieces, each read off a JSON object and checked here to stand (period 2) when assembled (`python3 rd.py`):
  CAPL, CAPR   the two caps of the push's 169-cell reader, mapped back to the own frame (wire on units -14..13)
  capped(ua, ub, word=None)   cap, units ua..ub-1 (hex digits of `word`, default all wire B = '7'), cap
A reader placement is (g, t, phase): own cell c at own generation `phase` sits at g(c) + t when the store is at an even
generation.  B13(U) is the push's reader b13 with its crossing at store unit U; B8(U) its mirror reader.
"""
import numpy as np
import qa
from qa import tr, unit, pk, up, run, xor, union, same

B = 0x7; BP = 0xd; C = 0xb; F = 0xf


def HT(c):
    """the half-turn that maps wire B to itself reversed."""
    return (-c[0] - 2, c[1], 8 - c[2])


# ---- the reader of the push, back in its own frame: placed = (82 - x, z, -84 - y)  <=>  own = (82 - X, -84 - Z, Y)
def _own_reader():
    ob = qa.obj('read-echo-B-line')
    placed = [tuple(c) for c in ob['cases'][0]['reader']]
    return sorted((82 - X, -84 - Z, Y) for (X, Y, Z) in placed)


_R = _own_reader()
CAPL = [tr(c, 14) for c in _R if unit(c) < -14]        # normalised: wire begins at unit 0
CAPR = [tr(c, -14) for c in _R if unit(c) >= 14]       # normalised: wire ends at unit -1
assert sorted(c for c in _R if -14 <= unit(c) < 14) == sorted(tr(c, u) for u in range(-14, 14) for c in qa.unit_cells(B))


def capped(ua, ub, word=None):
    word = word or '7' * (ub - ua)
    assert len(word) == ub - ua
    cells = [tr(c, ua) for c in CAPL] + [tr(c, ub) for c in CAPR]
    for i, ch in enumerate(word):
        cells += qa.unit_cells(int(ch, 16), ua + i)
    return sorted(set(cells))


def pR(u):
    """right-going pulse of wire B with its first cell in unit u (flip at an even own generation): 6f."""
    return [(1 + 2 * u, 0, -2 * u), (2 + 2 * u, 2, 1 - 2 * u)]


def pL(u):
    """left-going pulse at unit u (flip at an even own generation): the unit becomes b."""
    return [tr((1, 0, 4), u), tr((0, 2, 3), u)]


def stator(u, which):
    """(0,1,2) [which = 2: a right-going pulse is born] or (0,1,4) [4: a left-going one] of unit u."""
    return tr((0, 1, which), u)


class Placement:
    def __init__(self, g, t, phase=0):
        self.g = g if not isinstance(g, int) else qa.SYMS[g]
        self.t = tuple(t); self.phase = phase; self.gi = qa.inv(self.g)

    def __call__(self, cells):
        return [qa.app(self.g, c, self.t) for c in cells]

    def back(self, c):
        return qa.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2]))

    def moved(self, k):
        """the same placement k store units on."""
        return Placement(self.g, (self.t[0] + 2 * k, self.t[1], self.t[2] - 2 * k), self.phase)


G13 = ((0, 2, 1), (-1, 1, -1))      # (x,y,z) -> (-x, z, -y)
G8 = ((0, 2, 1), (1, 1, 1))         # (x,y,z) -> ( x, z,  y)
assert qa.SYMS[13] == G13 and qa.SYMS[8] == G8


def B13(U=0):
    """the push's reader b13: (x,y,z) -> (-2 - x, z, -y), crossing at store unit U (reader's own unit -1)."""
    return Placement(G13, (-2 + 2 * U, 0, -2 * U))


def B8(U=0):
    """the push's mirror reader b8: (x,y,z) -> (84 + x, 2 + z, y - 78) at unit 42; own crossing unit 0."""
    return Placement(G8, (2 * U, 2, 6 - 2 * U))


def period(k, pmax=8):
    x = k
    for p in range(1, pmax + 1):
        x = run(x, 1)
        if same(x, k):
            return p
    return None


def tube_part(k):
    return k[qa.tube_mask(k)]


if __name__ == '__main__':
    k = pk(capped(-10, 10))
    print('capped wire B, 20 units:', len(k), 'cells, period', period(k), ' CAPL', len(CAPL), 'CAPR', len(CAPR))
    for name, cells, dirn in (('pR', pR(-6), 1), ('pL', pL(6), -1)):
        x = xor(k, pk(cells))
        rigid = all(same(xor(run(x, 2 * j), k), pk(pR(-6 + j) if dirn > 0 else pL(6 - j))) for j in range(1, 9))
        print(f'  {name}: rigid for 8 units {rigid}; swallowed, restored at generation 80: {same(run(x, 80), k)}')
    for word in ('7777777ddf7777777777', '7777777df77777777777', '77777dddddf777777777'):
        k = pk(capped(-10, 10, word))
        print('  word', word, 'period', period(k), 'letters', qa.letters(k, -10, 10))
    # the push's two readers reproduced from these pieces
    ob = qa.obj('read-echo-B-line')
    placed = pk([tuple(c) for c in ob['cases'][0]['reader']])
    print('  B13(42) reproduces the JSON reader:', same(placed, pk(B13(42)(capped(-14, 14)))))
    ob = qa.obj('cell-small')
    print('  cell-small reader = B13(0) of capped(-4, 2):', same(pk([tuple(c) for c in ob['cases'][0]['reader']]), pk(B13(0)(capped(-4, 2)))))
    print('  cell-small store0 = capped(-4, 4):', same(pk([tuple(c) for c in ob['store0']]), pk(capped(-4, 4))))
    ob = qa.obj('read-echo-B-small')
    for case in ob['cases']:
        S = pk([tuple(c) for c in case['store']['cells']])
        lo = min(unit(c) for c in up(S)); hi = max(unit(c) for c in up(S))
        print('  small store', case['label'], len(S), 'units', lo, hi, qa.letters(S, lo, hi + 1))


# ---------------------------------------------------------------- experiments (q.c)
def install(S, P, own, settle=40):
    """S: store keys at a generation divisible by 4.  own: the reader's own cells at own generation 0.
    Returns (verdict, J, R): J the joint state `settle` generations on (settle divisible by 4), R the placed reader.
    verdict: 'overlap' | 'union' (joint = union of the two alone at every generation 0..settle) | 'junction' (joint
    state of period <= 4, differs from the union, the store's tube as alone at every generation) | 'store' (stands,
    the tube differs from the store alone) | 'burn' (not of period <= 4 at `settle`)."""
    R = pk(P(up(run(pk(own), P.phase))))
    U = union(S, R)
    if len(U) != len(S) + len(R):
        return 'overlap', None, R
    s, r, u = S, R, U
    isunion = True; tube_ok = True
    for t in range(settle):
        s, r, u = run(s, 1), run(r, 1), run(u, 1)
        if isunion and not same(u, union(s, r)):
            isunion = False
        if not isunion and tube_ok and not same(tube_part(u), tube_part(s)):
            tube_ok = False
    if isunion:
        return 'union', u, R
    if not same(run(u, 4), u):
        return 'burn', None, R
    return ('junction' if tube_ok else 'store'), u, R


def lock(J, flips, T, stop_when_same=True):
    """Run J (no probe) and J with `flips` ({generation: keys}) side by side for T generations.
    Returns dict: diffs {t: keys of the difference} for every t, first (first generation after the last flip from
    which the two are equal, None if never within T), tube (number of generations with a difference in the tube),
    X, Y (final states), t (generation reached)."""
    X = Y = J
    last = max(flips)
    diffs = {}; tube = 0; first = None
    for t in range(T + 1):
        if t in flips:
            X = xor(X, flips[t])
        d = xor(X, Y)
        diffs[t] = d
        if len(d) and qa.tube_mask(d).any():
            tube += 1
        if t > last:
            if len(d) == 0:
                if first is None:
                    first = t
                if stop_when_same:
                    break
            else:
                first = None
        if t < T:
            X = run(X, 1); Y = run(Y, 1)
    return dict(diffs=diffs, first=first, tube=tube, X=X, Y=Y, t=t)


def describe(P, d):
    """the difference d (keys) in the reader's own frame: decomposed into right-going pulses R@u and left-going L@u
    when it is exactly a set of free pulses at an even own generation; otherwise the own units it occupies."""
    cells = set(P.back(c) for c in up(d))
    if not cells:
        return '-'
    rest = set(cells); found = []
    for u in sorted({unit(c) for c in cells}):
        if set(pR(u)) <= rest:
            rest -= set(pR(u)); found.append(f'R@{u}')
        if set(pL(u)) <= rest:
            rest -= set(pL(u)); found.append(f'L@{u}')
    if not rest:
        return ' '.join(found)
    us = sorted(unit(c) for c in cells)
    return f'{len(cells)} cells, own units {us[0]}..{us[-1]}'
