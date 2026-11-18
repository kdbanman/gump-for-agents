#!/usr/bin/env python3
"""cell9 (push 9): the signal-triggered count read, written to objects/trigger9.json for verify_trigger9.py.

    python3 cell9.py            plays every run on lab8 (asserting each check), prints the letters at the checked
                                generations and writes objects/trigger9.json
    python3 cell9.py --law      the release for k = 1..40 and both parities of arrival (lab8)

The object: push 8's cell (capL + N units of wire B + capL turned round) and, beside the wire, the six-cell still
life S6b of the atlas (TRIG below, placed relative to a unit w): it lies at tube radius 6 to 10, has ONE cell,
(0,1,8) + unit w, that is a neighbour of a cell of the wire (the stator (0,1,4) of unit w - 1) and is never changed.
A stretch d^k f whose first unit is w stands beside it.  A right-going pulse that reaches the wall releases the whole
stretch as a block of 2k + 2 adjacent units of wire C moving left (b^(2k+2)); the wire is left plain and the still
life is as it was.  A stretch absorbs a block b^n as ceil(n/2) units, so a second store counts the release as k + 1.

States are written as push 8's letters (one hex digit per unit of wire) + the still life.  Operations remove ONE live
cell at an even generation: R@u = the stator (0,1,2) of unit u (a right-going pulse), L@u = the stator (0,1,4)
(a left-going pulse).  A check [generation, letters] says that the whole state is capL + those units + the right
cap + the still life, cell for cell.
"""
import os, sys, json
import numpy as np
import lab9 as Z
from lab9 import Lab, tr, unit, X, W

HERE = Z.HERE
TRIG = [(0, 0, 9), (0, 1, 8), (1, 0, 8), (1, 2, 10), (2, 1, 10), (2, 2, 9)]     # S6b beside the wall whose first unit is unit 0

R_ = lambda u: list(tr(X.RIGHT, u))
L_ = lambda u: list(tr(X.LEFT, u))


def trig(w):
    return [list(tr(c, w)) for c in TRIG]


def mk(name, text, start, ops, checks, w=None, H=None):
    """letters start at unit 4; w = the wire position (index into the letters) of the unit the still life is placed
    at, or None for no still life"""
    N = len(start)
    return dict(name=name, text=text, N=N, H=H or 2 * (N + 16 + (N % 2)), start=start,
                extra=trig(4 + w) if w is not None else [], ops=ops, checks=checks)


def runs():
    out = []
    # 1. the trigger alone: a store of 3, the pulse born 12 units before the wall
    s = '7' * 16 + 'dddf' + '7' * 6
    out.append(mk('trigger', 'a store holding 3 with the still life at its wall; ONE cell removed 12 units before the wall: the pulse '
                  'arrives and the store leaves as a block of 8 units of wire C; the left cap swallows it; the wire is plain',
                  s, [[0, [R_(4 + 4)]]], [[0, s], [16, None], [22, None], [30, None], [40, None], [200, '7' * 26], [202, '7' * 26]], w=16))
    # 2. control: the same without the still life
    out.append(mk('control', 'the same run without the still life: the pulse is absorbed and the store holds 4',
                  s, [[0, [R_(4 + 4)]]], [[0, s], [200, '7' * 15 + 'ddddf' + '7' * 6]], w=None))
    # 3. the loop: store, trigger, second store
    s = '7' * 5 + 'df' + '7' * 22 + 'dddf' + '7' * 6
    out.append(mk('loop', 'two stores holding 1 and 3, the still life at the wall of the right one; ONE cell removed between them, '
                  '11 units from the right store and 10 from the left one: the right store empties into the left one, which then holds 1 + 4',
                  s, [[0, [R_(4 + 17)]]], [[0, s], [40, None], [60, None], [200, '7' * 5 + 'dddddf' + '7' * 28], [202, '7' * 5 + 'dddddf' + '7' * 28]], w=29))
    # 4. the count is written by signals, then called out by a signal
    s = '7' * 5 + 'df' + '7' * 22 + 'df' + '7' * 16
    out.append(mk('write-then-call', 'the right store starts at 1; three left-going pulses made 12 units to its right add one each '
                  '(the still life does not notice); then ONE cell removed between the stores calls the count out: the left store holds 1 + 5',
                  s, [[0, [L_(4 + 43)]], [60, [L_(4 + 43)]], [120, [L_(4 + 43)]], [200, [R_(4 + 17)]]],
                  [[0, s], [60, None], [120, None], [200, '7' * 5 + 'df' + '7' * 22 + 'ddddf' + '7' * 13], [240, None],
                   [420, '7' * 5 + 'd' * 6 + 'f' + '7' * 35], [422, '7' * 5 + 'd' * 6 + 'f' + '7' * 35]], w=29))
    return out


def state(word, extra=()):
    N = len(word)
    return X.CAPL | X.hexword(word, 4) | frozenset(tr(c, 4 + N) for c in X.CAPR2) | frozenset(tuple(c) for c in extra)


def lab_for(N):
    return Lab(-6, N + 16, -8, 12, -8, 20)


def letters(Lb, a, N):
    """letters of the wire units, reading only the 3 x 3 tube"""
    return Z.hexring(Lb, a, 4, 4 + N)


def play(run, show=True):
    N = run['N']; Lb = lab_for(N); extra = run['extra']
    a = Lb.arr(state(run['start'], extra))
    b = a.copy(); Lb.run(b, 2); assert np.array_equal(a, b), 'start state is not standing'
    ops = {g: cells for g, cells in run['ops']}
    G = max(g for g, _ in run['checks'])
    for g in range(G + 1):
        for chk in run['checks']:
            if chk[0] == g:
                got = letters(Lb, a, N)
                if chk[1] is None:
                    chk[1] = got
                assert Lb.cells(a) == state(chk[1], extra), (run['name'], g, got, chk[1])
                if show:
                    print(f"  {run['name']:16s} generation {g:4d}: {got}")
        if g in ops:
            for c in ops[g]:
                assert a[Lb.idx(tuple(c))] == 1, (run['name'], g, c)
            Lb.flip(a, [tuple(c) for c in ops[g]])
        Lb.run(a, 1)
    assert not Lb.touch


def write():
    rs = runs()
    for run in rs:
        play(run)
    d = dict(note="signal-triggered count read of push 9. Doubled coordinates; unit u = cells with x in {2u, 2u+1}; tr(c, k) = (x + 2k, y, z - 2k). "
                  "A state 'letters' = capL + for each letter i (hex digit h) the stators and the sites of h moved to unit 4 + i + capR moved "
                  "to unit 4 + N + the run's extra cells (the still life S6b; never changed). runs[].ops = [generation, cells removed (each must "
                  "be live)]; runs[].checks = [generation, letters]: the whole state equals the state of those letters. H = side of the oracle's "
                  "cubic torus. trig = the still life placed for a stretch whose first unit is unit 0.",
             capL=sorted(map(list, X.CAPL)), capR=sorted(map(list, X.CAPR2)), stators=W.ST, sites=W.SITES, trig=TRIG, runs=rs)
    json.dump(d, open(os.path.join(HERE, 'objects', 'trigger9.json'), 'w'))
    print('wrote objects/trigger9.json')


def law(kmax=40):
    ok = True
    for k in range(1, kmax + 1):
        row = []
        for du in (11, 12):
            nL = 2 * k + 20; s = '7' * nL + 'd' * k + 'f' + '7' * 6; N = len(s)
            Lb = lab_for(N); a = Lb.arr(state(s, trig(4 + nL)))
            Lb.flip(a, [tr(X.RIGHT, 4 + nL - du)])
            Lb.run(a, 2 * du + 2 * k + 10)
            got = letters(Lb, a, N)
            good = Lb.cells(a) == state(got, trig(4 + nL)) and got.strip('7') == 'b' * (2 * k + 2)
            Lb.run(a, 4 * N + 100)
            good &= Lb.cells(a) == state('7' * N, trig(4 + nL))
            row.append(good); ok &= good
        print(f'  k = {k:2d}: block b^{2 * k + 2} and then the empty cell with the still life: {row}')
    print('law holds for k = 1..%d, both parities' % kmax if ok else 'LAW FAILS')


if __name__ == '__main__':
    if '--law' in sys.argv:
        law()
    else:
        write()
