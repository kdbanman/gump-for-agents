#!/usr/bin/env python3
"""reduce9 (push 9): what the CALL does to the store, in terms of push 8's hand release.

    python3 reduce9.py [--kmax 40]

Push 8 proved (prove_unzip8.py): on wire B with a stretch d^k f whose first unit is w, removing the stator (0,1,2) of
unit w - 1 at an even generation releases the stretch as exactly k left-going pulses two units apart, for every k.
Here, for k = 1..kmax, on push 8b's stepper (checked against the oracle on these objects by check9.py, part D):
  1  the store with the call line across unit w - 1 and a CALL launched at generation 0, 15 line units before the
     crossing, is at generation 90 + 4k EXACTLY (whole state) what the same store and line are at that generation
     when, instead of the CALL, the stator (0,1,2) of unit w - 1 is removed at generation s; the s that fits is
     printed (one s for every k).  At generation 90 the two are equal for k <= 29 only: the CALL also sends a
     difference along the stretch, one unit per two generations, which ends at the stretch's edge;
  2  the hand release with the line across unit w - 1 is at every generation 0..4k+60 the union of the hand release
     without the line and the line at rest (the line takes no part in the release).
"""
import sys
import call9 as C
from call9 import lab, state, line_cells, call_cells, R_, LAUNCH


def main():
    kmax = int(sys.argv[sys.argv.index('--kmax') + 1]) if '--kmax' in sys.argv else 40
    fits = {}; ok2 = True
    for k in range(1, kmax + 1):
        G = 2 * LAUNCH + 60 + 4 * k
        nL = 2 * k + 34; s = '7' * nL + 'd' * k + 'f' + '7' * 8; c = nL - 1
        ex = line_cells(c)
        U = lab.pk(state(s, ex)); hand = lab.pk([tuple(R_(c))])
        Bg = lab.run(lab.xor(U, lab.pk([tuple(q) for q in call_cells(c)])), G)
        fits[k] = [sh for sh in range(0, G, 2) if lab.same(lab.run(lab.xor(U, hand), G - sh), Bg)]
        A = lab.xor(U, hand); A0 = lab.xor(lab.pk(state(s, [])), hand); Ln = lab.pk([tuple(q) for q in ex])
        for t in range(4 * k + 61):
            if not lab.same(A, lab.union(A0, Ln)):
                ok2 = False; print(f'  k = {k}: the hand release with the line differs from the union at generation {t}'); break
            A = lab.run(A, 1); A0 = lab.run(A0, 1); Ln = lab.run(Ln, 1)
    vals = sorted({tuple(v) for v in fits.values()})
    print(f'1  k = 1..{kmax}: the CALL launched at generation 0 = the stator (0,1,2) of the crossing unit removed at generation s; s that fit: {vals}')
    print(f'2  k = 1..{kmax}: the hand release with the line = (the hand release) + (the line at rest) at every generation: {ok2}')
    odd = [k for k, v in fits.items() if v != [28]]
    print(f'   k with a fit other than s = 28 alone: {odd}')
    good = ok2 and not odd
    print('PASS' if good else 'FAIL')


if __name__ == '__main__':
    main()
