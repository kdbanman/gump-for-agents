#!/usr/bin/env python3
"""push 8b: kymograph of a reader beside push 7's standing line.

    python3 show3.py READER g phi tx ty tz n [--T 80] [--settle 200] [--nopulse] [--launch -9] [--every 2]

Per line: generation; the store units 30..56 read in the store's tube; the reader's units read in the reader's own
frame and tube; the number of cells in which the run differs from the same run without the pulse."""
import argparse
import lab, wires, line, survey2
from survey import inv
from survey2 import in_tube
from lab import unit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('g', type=int); ap.add_argument('phi', type=int)
    ap.add_argument('t', type=int, nargs=3); ap.add_argument('n', type=int)
    ap.add_argument('--T', type=int, default=80); ap.add_argument('--settle', type=int, default=200)
    ap.add_argument('--nopulse', action='store_true'); ap.add_argument('--launch', type=int, default=-9)
    ap.add_argument('--every', type=int, default=2); ap.add_argument('--delay', type=int, default=0)
    a = ap.parse_args()
    P = survey2.Probe(a.reader, a.n)
    g = lab.SYMS[a.g]; t = tuple(a.t); gi = inv(g)
    S0 = P.store; R0 = P.reader(g, a.phi, t)
    U = lab.union(S0, R0)
    print('overlap', len(S0) + len(R0) - len(U))

    def show(X, Y, tt):
        cells = lab.up(X)
        st = lab.pk([c for c in cells if in_tube(c)])
        rd = [lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2])) for c in cells]
        rd = lab.pk([c for c in rd if in_tube(c)])
        _, s1 = line.letters(st, 30, 57)
        _, s2 = line.letters(rd, -survey2.NR - 3, survey2.NR + 3)
        print(f'{tt:5d} {s1}   {s2}   diff {len(lab.xor(X, Y))}')

    Y = U
    if a.settle:
        print('settling (no pulse):')
        for tt in range(0, a.settle + 1):
            if tt % 20 == 0 or tt < 12:
                show(Y, Y, tt)
            if tt < a.settle:
                Y = lab.run(Y, 1)
        print('period', next((p for p in (1, 2, 4, 8) if lab.same(lab.run(Y, p), Y)), None), ' differs from the union in', len(lab.xor(Y, lab.run(U, a.settle % 4))), 'cells')
    Y = lab.run(Y, a.phi + a.delay)
    X = Y if a.nopulse else lab.xor(Y, lab.pk([lab.app(g, c, t) for c in wires.pulse(P.pulse, a.launch)]))
    print('pulse:')
    for tt in range(0, a.T + 1):
        if tt % a.every == 0:
            show(X, Y, tt)
        X = lab.run(X, 1); Y = lab.run(Y, 1)


if __name__ == '__main__':
    main()
