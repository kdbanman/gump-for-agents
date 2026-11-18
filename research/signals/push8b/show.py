#!/usr/bin/env python3
"""push 8b: kymograph of one placement of survey.py.

    python3 show.py READER g phi tx ty tz KIND [--T 80] [--delay 0] [--nopulse]

One line per 2 generations: the store read unit by unit in its own frame, then the reader read in its own frame
(letters of line.letters: b/B wire B phase 0/1, p/P wire B', c/C wire C, _ empty, # other).  Only cells inside each
wire's own 3 x 3 tube are read (the other wire's cells that lie inside it count)."""
import sys, argparse
import lab, wires, line, survey
from lab import unit


def in_tube(c):
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('g', type=int); ap.add_argument('phi', type=int)
    ap.add_argument('t', type=int, nargs=3); ap.add_argument('kind')
    ap.add_argument('--T', type=int, default=80); ap.add_argument('--delay', type=int, default=0); ap.add_argument('--nopulse', action='store_true')
    ap.add_argument('--settle', type=int, default=200); ap.add_argument('--pulses', default='0'); ap.add_argument('--every', type=int, default=2)
    a = ap.parse_args()
    L = survey.Lab(a.reader)
    g = lab.SYMS[a.g]; t = tuple(a.t); gi = survey.inv(g)
    HRg = [lab.app(g, c) for c in L.FRh]
    us, ur = survey.crossing(g, t, HRg, L.HS)
    S0 = L.stores[a.kind]; R0 = L.reader(g, a.phi, t)
    Y = lab.run(lab.union(S0, R0), a.settle + a.phi + a.delay)
    X = Y
    launches = [] if a.nopulse else [int(x) for x in a.pulses.split(',')]
    print(f'crossing at store unit {us}, reader unit {ur}; reader axis {lab.appv(g, lab.V)}')
    for tt in range(0, a.T + 1):
        if tt in launches:
            X = lab.xor(X, lab.pk([lab.app(g, c, t) for c in wires.pulse(L.pulse, ur - survey.U0)]))
        if tt % a.every == 0:
            cells = lab.up(X)
            st = lab.pk([c for c in cells if in_tube(c)])
            rd = [lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2])) for c in cells]
            rd = lab.pk([c for c in rd if in_tube(c)])
            _, s1 = line.letters(st, -survey.NS - 4, survey.NS + 4)
            _, s2 = line.letters(rd, -survey.NR - 5, survey.NR + 5)
            d = len(lab.xor(X, Y))
            print(f'{tt:4d} {s1}   {s2}   diff {d}')
        X = lab.run(X, 1); Y = lab.run(Y, 1)


if __name__ == '__main__':
    main()
