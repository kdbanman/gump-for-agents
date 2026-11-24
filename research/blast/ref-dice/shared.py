#!/usr/bin/env python3
"""ref-dice: the hull-3 face over SHARED coins, stepped by reference/oracle.py, against Face.P (private coins).

The face (9 cells of x+y+z = 3, x,y,z >= 0) is put on a real gump array; each of the 15 distinct cells of the
octahedron |x|+|y|+|z| <= 3 that lie one layer beneath (9 cells, density rho1) or two layers beneath (6 cells,
density rho2) some face cell is an independent coin; everything else is dead. For a start state x the exact law of
the face's next state is the sum over the 2^15 coin patterns of one `oracle.step`. Printed: total variation distance
to the surrogate's row P(x, .) (myface.py, equal to Lean's Face.P entry for entry by compare_kernel.py), and the
one-step death probabilities under both.

    python3 shared.py [x ...]        (default: 511 = full, 0b101010101 = 341, 0b000010110 = 22)
"""
import sys, itertools, time
from fractions import Fraction
import numpy as np
import myface, oracle

CELLS = [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
R = 3
HA, C0 = 12, 6


def main():
    xs = [int(a) for a in sys.argv[1:]] or [511, 341, 22]
    F = myface.build('hull', (R,), CELLS)
    at = myface.a_table(F)
    ex = lambda q: sum(map(abs, q)) <= R
    beneath = {}
    for p in CELLS:
        for q in myface.nbrs(p):
            d = myface.s(q) - R
            if d in (-2, -4) and ex(q):
                beneath[q] = myface.R1 if d == -2 else myface.R2
    bq = sorted(beneath)
    m = oracle.masks(HA)
    idx = lambda q: (q[0] + C0, q[1] + C0, q[2] + C0)
    for x in xs:
        t = time.time()
        law = {}
        h = np.zeros((HA, HA, HA), np.int8)
        for i, p in enumerate(CELLS):
            h[idx(p)] = (x >> i) & 1
        for pat in itertools.product((0, 1), repeat=len(bq)):
            w = Fraction(1)
            for q, b in zip(bq, pat):
                h[idx(q)] = b
                w *= beneath[q] if b else 1 - beneath[q]
            new = oracle.step(h, m)
            y = sum(int(new[idx(p)]) << i for i, p in enumerate(CELLS))
            law[y] = law.get(y, Fraction(0)) + w
        assert sum(law.values()) == 1
        row = myface.kernel_row(at[x], 9)
        tv = sum(abs(law.get(y, 0) - row[y]) for y in range(512)) / 2
        print('x = %3d (%d live): TV(shared, private) = %.4f; P(x, empty): shared %.5f, private %.5f; '
              'states reachable: shared %d, private %d  (%.0f s)'
              % (x, bin(x).count('1'), float(tv), float(law.get(0, 0)), float(row[0]),
                 sum(1 for v in law.values() if v > 0), sum(1 for v in row if v > 0), time.time() - t))


if __name__ == '__main__':
    main()
