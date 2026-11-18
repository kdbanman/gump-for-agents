#!/usr/bin/env python3
"""cell8 (push 8): the memory cell and its protocol, written to objects/cell8.json for verify_cell8.py.

    python3 cell8.py            prints each run (letters at the checked generations) and writes objects/cell8.json

The cell: capL (18 cells, units 0..3) + N units of wire B (units 4..N+3) + capL turned round (20 cells): a standing
object of period 2 with 38 + 5N cells.  Its state is written as the N hex letters of the wire (7 = wire B; d = wire
B'; f = the stretch's edge unit; b = a unit of wire C = a left-going pulse; 6f = a right-going pulse).
Every operation removes ONE live cell at an even generation: the stator (0,1,2) of a unit (written R@u) or the stator
(0,1,4) of a unit (L@u).
  set        R@u and L@u' in the same generation, u' - u odd: the two pulses stop each other and leave  d f  (count 1)
  add one    R@u at least two units left of the stretch, or L@u at least two units right of its edge: count + 1
  bit read   the same pulse: it crosses an empty cell and the far cap swallows it; a stretch absorbs it
  count read R@u with u the unit of wire B next to the stretch's first unit: the stretch dissolves into as many
             left-going pulses as it had units of wire B', two units apart; the wire is left plain
A run is a list of operations [generation, cells removed] and checks [generation, letters]; a check says that the
whole state at that generation is exactly capL + the family units of those letters + the right cap.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X
from lab8 import tr

R = lambda u: list(tr(X.RIGHT, u))
L_ = lambda u: list(tr(X.LEFT, u))

RUNS = [
    dict(name='smallest', N=7, H=48, start='7777777',
         text='the smallest cell found (73 cells): set, add one, count read (two pulses out), empty again',
         ops=[[0, [R(5), L_(10)]], [120, [L_(10)]], [240, [R(6)]]],
         checks=[[0, '7777777'], [118, '777df77'], [120, '777df77'], [238, '777ddf7'], [240, '777ddf7'], [250, 'b7b7777'], [360, '7777777']]),
    dict(name='count', N=24, H=80, start='7' * 24,
         text='set; three pulses add one each (right, left, right); count read: four pulses leave, the cell is empty again',
         ops=[[0, [R(8), L_(21)]], [120, [L_(24)]], [200, [R(7)]], [280, [L_(24)]], [360, [R(12)]]],
         checks=[[120, '7' * 10 + 'df' + '7' * 12], [200, '7' * 10 + 'ddf' + '7' * 11], [280, '7' * 9 + 'dddf' + '7' * 11],
                 [360, '7' * 9 + 'ddddf' + '7' * 10], [382, None], [520, '7' * 24]]),
    dict(name='transfer', N=24, H=80, start='7' * 4 + 'df' + '7' * 8 + 'dddf' + '7' * 6,
         text='two stores: the count read of the right one (3) sends three pulses to the left one (1), which then holds 4',
         ops=[[0, [R(17)]]],
         checks=[[0, '7' * 4 + 'df' + '7' * 8 + 'dddf' + '7' * 6], [14, None], [120, '7' * 4 + 'ddddf' + '7' * 15]]),
    dict(name='bit-empty', N=24, H=80, start='7' * 24,
         text='bit read of an empty cell: the pulse crosses the wire and the right cap swallows it',
         ops=[[0, [R(6)]]], checks=[[20, None], [120, '7' * 24]]),
    dict(name='bit-set', N=24, H=80, start='7' * 10 + 'df' + '7' * 12,
         text='bit read of a cell that holds a stretch: the pulse is absorbed (count 1 becomes 2), nothing reaches the far side',
         ops=[[0, [R(6)]]], checks=[[120, '7' * 9 + 'ddf' + '7' * 12], [122, '7' * 9 + 'ddf' + '7' * 12]]),
]


def state(word):
    N = len(word)
    return X.CAPL | X.hexword(word, 4) | frozenset(tr(c, 4 + N) for c in X.CAPR2)


def play(run, show=True):
    N = run['N']; Lb = X.lab_for(N); a = Lb.arr(state(run['start']))
    ops = {g: cells for g, cells in run['ops']}
    G = max(g for g, _ in run['checks'])
    for g in range(G + 1):
        for chk in run['checks']:                                 # checks come before the operations of the same generation
            if chk[0] == g:
                got = X.hexletters(Lb, a, 4, 4 + N)
                if chk[1] is None:
                    chk[1] = got                                  # a probe: read from the run, then checked as a state
                assert Lb.cells(a) == state(chk[1]), (run['name'], g, got, chk[1])
                if show:
                    print(f"  {run['name']:10s} generation {g:4d}: {X.hexrle(got)}")
        if g in ops:
            for c in ops[g]:
                assert a[Lb.idx(tuple(c))] == 1, (run['name'], g, c)
            Lb.flip(a, [tuple(c) for c in ops[g]])
        Lb.run(a, 1)
    assert not Lb.touch


def write():
    for run in RUNS:
        play(run)
    d = dict(note="memory cell of push 8. Doubled coordinates; unit u = cells with x in {2u, 2u+1}; tr(c, k) = (x + 2k, y, z - 2k). "
                  "A state 'letters' = capL + for each letter i (hex digit h) the stators and the sites of h moved to unit 4 + i + capR moved "
                  "to unit 4 + N. runs[].ops = [generation, cells removed (each must be live)]; runs[].checks = [generation, letters]: "
                  "the whole state equals the state of those letters. H = side of the oracle's cubic torus.",
             capL=sorted(map(list, X.CAPL)), capR=sorted(map(list, X.CAPR2)), stators=W.ST, sites=W.SITES, runs=RUNS)
    json.dump(d, open(os.path.join(HERE, 'objects', 'cell8.json'), 'w'))
    print('wrote objects/cell8.json')


if __name__ == '__main__':
    write()
