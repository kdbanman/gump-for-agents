#!/usr/bin/env python3
"""check_st8 (REVIEW-signals-8): st8.c against reference/oracle.py, whole state, every generation, on runs of every
kind the review uses st8 for.

    python3 check_st8.py [--seed 8] [--census 40]

Runs (each: the same start and the same operations in a8.Box and in a8.Orc, compared as sets of cells after every
generation; st8's `touch` must stay False):
  protocol     set, adds from both sides, count read, on N = 24 (520 generations)
  destroyed    R@4; L@4; L@5; R@last; pairs 2 apart and 1 apart: the cell burns or is wrecked (300 generations each)
  trains       6ef / bbb / 6f6f into a store; a pulse into a running count read
  census       a random sample of the 760 one-cell events of the 5 x 5 tube at d^3 f (both phases), 110 generations
  outside      (1,4,2) made live beside the unit before the stretch, k = 1, 4, 9 (4k + 60 generations)
  line caps    push 7's right cap: a right-going pulse at its bad phase (the line burns) and at its good phase
  soup         a block of random soup in a wide box against the pure-Python set stepper (40 generations)
"""
import sys, time, random
import numpy as np
import a8
from a8 import tr, SR, SL

T0 = time.time(); OK = [True]


def say(ok, text):
    OK[0] &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - T0:.0f} s]', flush=True)


def both(word, ops, G, rcap=None):
    """ops: {generation: [('kill' | 'flip', cell)]}; returns (first generation at which the two differ or None, touch, final cells)"""
    N = len(word)
    B = a8.Box(-6, N + 16); O = a8.Orc(-6, N + 16)
    a = B.arr(a8.cell_state(word, rcap)); h = O.arr(a8.cell_state(word, rcap))
    for g in range(G + 1):
        for kind, c in ops.get(g, []):
            if kind == 'kill':
                B.kill(a, c); O.kill(h, c)
            else:
                B.flip(a, [c]); O.flip(h, [c])
        if B.cells(a) != O.cells(h):
            return g, B.touch, None
        if g < G:
            B.run(a, 1); h = O.run(h, 1)
    return None, B.touch, B.cells(a)


def main():
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 8
    ncen = int(sys.argv[sys.argv.index('--census') + 1]) if '--census' in sys.argv else 30
    rng = random.Random(seed)
    R = lambda u: ('kill', tr(SR, u)); L = lambda u: ('kill', tr(SL, u))
    bad, t, fin = both('7' * 24, {0: [R(8), L(21)], 120: [L(24)], 200: [R(7)], 280: [L(24)], 360: [R(12)]}, 520)
    say(bad is None and not t and fin == a8.cell_state('7' * 24), 'protocol: set, three adds, count read on N = 24, generations 0..520 (ends as the empty cell)')
    res = []
    for name, ops in (('R@4', {0: [R(4)]}), ('L@4', {0: [L(4)]}), ('L@5', {0: [L(5)]}), ('R@15', {0: [R(15)]}), ('R@8 L@10', {0: [R(8), L(10)]}),
                      ('R@8 L@9', {0: [R(8), L(9)]}), ('R@9 L@8', {0: [R(9), L(8)]}), ('R@8 at 1', {1: [R(8)]}), ('L@4 at 1', {1: [L(4)]})):
        bad, t, fin = both('7' * 12, ops, 300)
        res.append((name, bad, t, len(fin) if fin is not None else None))
    say(all(b is None and not t for _, b, t, _ in res), f'destroyed / wrecked cells, 300 generations each (name, first difference, touch, cells left): {res}')
    res = []
    for word, ops in (('7' * 4 + '6ef' + '7' * 5 + 'df' + '7' * 10, {}), ('7' * 6 + 'df' + '7' * 4 + 'bbb' + '7' * 9, {}), ('7' * 4 + '6f6f' + '7' * 4 + 'df' + '7' * 10, {}),
                      ('7' * 10 + '6f' + '7' * 8 + 'dddf' + '7' * 6, {0: [R(23)]}), ('7' * 9 + '6f' + '7' * 9 + 'dddf' + '7' * 6, {0: [R(23)]})):
        bad, t, fin = both(word, ops, 300)
        res.append((a8.rle(word), bad, t, a8.rle(a8.letters_of(fin, 4, 4 + len(word))) if fin else None))
    say(all(b is None and not t for _, b, t, _ in res), f'trains and a pulse into a count read (start, first difference, touch, end): {res}')
    # census sample
    E5 = [(x, y, z) for x in (0, 1) for y in range(-4, 5) for z in range(-6, 9)
          if a8.is_cell((x, y, z)) and -1 <= x + y + z <= 7 and -1 <= x - y + z <= 7]
    assert len(E5) == 38
    word = '7' * 30 + 'dddf' + '7' * 30; w0 = 34
    events = [(g0, u, c) for g0 in (0, 1) for u in range(w0 - 3, w0 + 7) for c in E5]
    assert len(events) == 760
    sample = rng.sample(events, ncen); nbad = 0; touched = 0
    for g0, u, c in sample:
        bad, t, fin = both(word, {g0: [('flip', tr(c, u))]}, 110, rcap=a8.CAPR7)
        nbad += bad is not None; touched += t
    say(nbad == 0 and touched == 0, f'census: {ncen} of the 760 one-cell events at d^3 f (push 7\'s caps, 30 units of wire each side), 110 generations: {ncen - nbad} equal at every generation, touch {touched}')
    res = []
    for k in (1, 4, 9):
        word = '7' * (2 * k + 30) + 'd' * k + 'f' + '7' * 10; w = 4 + 2 * k + 30
        bad, t, fin = both(word, {0: [('flip', tr((1, 4, 2), w - 1))]}, 4 * k + 60)
        res.append((k, bad, t, a8.rle(a8.letters_of(fin, 4, 4 + len(word)).strip('7')) if fin else None))
    say(all(b is None and not t for _, b, t, _ in res), f'outside cell (1,4,2) made live beside the unit before the stretch (k, first difference, touch, train at 4k + 60): {res}')
    res = []
    for g0 in (0, 2):
        bad, t, fin = both('7' * 28, {g0: [R(14)]}, 300, rcap=a8.CAPR7)
        res.append((g0, bad, t, len(fin) if fin is not None else None))
    say(all(b is None and not t for _, b, t, _ in res), f"push 7's right cap, a right-going pulse born at unit 14 at generation 0 / 2 (generation, first difference, touch, cells at 300): {res}")
    # soup against the set stepper
    r2 = np.random.default_rng(seed); B = a8.Box(-14, 14, -28, 28, -28, 28)
    soup = [(x, y, z) for x in range(-8, 8) for y in range(-8, 8) for z in range(-8, 8) if a8.is_cell((x, y, z)) and r2.random() < 0.4]
    a = B.arr(soup); s = frozenset(soup); bad = None
    for g in range(40):
        s = a8.step_set(s); B.run(a, 1)
        if B.cells(a) != s:
            bad = g; break
    say(bad is None and not B.touch, f'soup of {len(soup)} cells: st8 == set stepper for 40 generations ({len(s)} cells left)')
    print('ALL PASS' if OK[0] else 'SOME FAIL')
    sys.exit(0 if OK[0] else 1)


if __name__ == '__main__':
    main()
