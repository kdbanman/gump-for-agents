#!/usr/bin/env python3
"""ref-dice: the alive probabilities a_i(x) of the dice surrogate obtained by STEPPING reference/oracle.py.

For every state x and cell i: put the face's layer on a real gump array (every layer point within max-distance 4
of cell i gets the state of the face cell it stands for, or 0 if it stands for none: the free rim; on a wrapped face
the periodic images), put cell i's own existing neighbours one and two layers beneath (its private coins) to each of
their 2^m patterns, everything else 0 (above the face: dead), run ONE `oracle.step`, read cell i, and sum the
pattern weights rho1^j (1-rho1)^(..) rho2^l (1-rho2)^(..) over the patterns where it is alive.
Used by compare_kernel.py --oracle; on its own:  python3 oracle_alive.py   (self-test on hull 3, prints timing)
"""
import itertools, time
from fractions import Fraction
import numpy as np
import myface
import oracle

HA = 24                 # array side (even: a proper torus; nothing populated comes near the seam)
C0 = (12, 12, 12)       # even shift keeps the parity of coordinates


def oracle_a_table(kind, args, cells, F, r1=myface.R1, r2=myface.R2):
    A = F['A']
    m = oracle.masks(HA)
    if kind == 'hull':
        R, = args
        exists = lambda q: abs(q[0]) + abs(q[1]) + abs(q[2]) <= R
        rep = lambda q: cells.index(q) if q in cells else None
    else:
        exists = lambda q: True
        gens = {'torus': lambda a: [(a[0], a[1]), (0, a[2])], 'strip': lambda a: [(0, a[1])],
                'patch': lambda a: []}[kind](args)

        def rep(q):
            for j, p in enumerate(cells):
                if myface.axis(p) == myface.axis(q) and myface.in_lattice(
                        myface.ab(tuple(q[t] - p[t] for t in range(3))), gens):
                    return j
            return None
    # per cell: the layer window (point -> face index or None), and the private coins
    win, coins = [], []
    for i, p in enumerate(cells):
        w = []
        for d in itertools.product(range(-4, 5), repeat=3):
            q = tuple(p[t] + d[t] for t in range(3))
            if myface.is_cell(q) and myface.s(q) == myface.s(p):
                w.append((q, rep(q)))
        win.append(w)
        cs = []
        for o in oracle.offsets(myface.axis(p)):
            q = tuple(p[t] + o[t] for t in range(3))
            ds = myface.s(q) - myface.s(p)
            if ds in (-2, -4) and exists(q):
                cs.append((q, r1 if ds == -2 else r2))
        coins.append(cs)
    out = []
    for x in range(2 ** A):
        row = []
        for i, p in enumerate(cells):
            h = np.zeros((HA, HA, HA), np.int8)
            for q, r in win[i]:
                if r is not None and (x >> r) & 1:
                    h[q[0] + C0[0], q[1] + C0[1], q[2] + C0[2]] = 1
            tot = Fraction(0)
            for pat in itertools.product((0, 1), repeat=len(coins[i])):
                wgt = Fraction(1)
                for (q, r), b in zip(coins[i], pat):
                    h[q[0] + C0[0], q[1] + C0[1], q[2] + C0[2]] = b
                    wgt *= r if b else 1 - r
                new = oracle.step(h, m)
                if new[p[0] + C0[0], p[1] + C0[1], p[2] + C0[2]]:
                    tot += wgt
            for q, r in coins[i]:
                h[q[0] + C0[0], q[1] + C0[1], q[2] + C0[2]] = 0
            row.append(tot)
        out.append(row)
    return out


if __name__ == '__main__':
    cells = [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
    F = myface.build('hull', (3,), cells)
    t = time.time()
    ao = oracle_a_table('hull', (3,), cells, F)
    at = myface.a_table(F)
    print('hull 3: oracle-stepped vs combinatorial a table: %d mismatching states; %.0f s'
          % (sum(ao[x] != at[x] for x in range(512)), time.time() - t))
