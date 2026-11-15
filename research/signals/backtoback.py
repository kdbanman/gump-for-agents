#!/usr/bin/env python3
"""Guns from two caps back to back: a clock (capL, N units of wire C, capR, a rake) whose left cap faces the right
end R1 of a long tape across a narrow gap.  Each time the rake turns at capL, does R1 write a letter B into its
tape and return to itself?  That would be a periodic emitter: one or more pulses p< per period, for ever.

    python3 backtoback.py TABLE.json [--N 5] [--max M] [--gaps -6 -5 -4]

TABLE.json: scatter_table.py output for wire C (its `states` are cap states, cells relative to their first unit);
every state that is a stationary right cap of wire C (checked here) is tried as R1.  R1 is placed with its first
unit at units g - span(R1) for each gap g, the tape running to its left; capL of the clock on units -4..-1, wire C
on 0..N-1, capR at N (objects/clock-C.json).  The unlit object must be stationary (period 2) on the units from R1's
tape to capR; then the rake is lit and, for 12 periods of the clock, the tape left of R1 is read at every even
generation.  Reported: every (R1, g) for which some unit of the tape becomes a B unit while the rest stays pure
tape, with what is written and whether the caps return to themselves.  Stepping: sg.Geom (family.Piece, the closed
3 x 3 tube) only.
"""
import argparse, json
from collections import Counter
import sg, scat, family as F

tr = scat.tr; unit = scat.unit


def uc(m, u):
    return {tr(c, u) for c in F.STATOR} | {tr(F.SITES[i], u) for i in range(4) if m >> i & 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table'); ap.add_argument('--N', type=int, default=5); ap.add_argument('--max', type=int, default=10 ** 9)
    ap.add_argument('--gaps', type=int, nargs='+', default=[-7, -6, -5, -4, -3])
    a = ap.parse_args(); N = a.N
    ck = json.load(open('objects/clock-C.json'))
    capL = frozenset(map(tuple, ck['capL'])); capR = frozenset(tr(tuple(c), N) for c in ck['capR'])
    ign = tr(tuple(ck['ignite']), N // 2)
    pc = F.Piece(170); g = pc.g
    D = json.load(open(a.table))
    tally = Counter(); hits = []
    p = 4 * N + 2; T = 12 * p + 60
    for sid, st in list(D['states'].items())[:a.max]:
        R1 = frozenset(map(tuple, st))
        if not R1:
            continue
        u0 = min(unit(c) for c in R1); span = max(unit(c) for c in R1) - u0
        for gap in a.gaps:
            sh = gap - span - u0
            R = frozenset(tr(c, sh) for c in R1)
            first = min(unit(c) for c in R)
            tape = set()
            for u in range(-160, first):
                tape |= uc(0xb, u)
            # R1's own cells overwrite: cells of units >= first are R1's
            cells = frozenset(c for c in tape if unit(c) < first) | R
            if cells & capL:
                tally['overlap'] += 1; continue
            cells = cells | capL | {c for u in range(N) for c in uc(0xb, u)} | capR
            try:
                x = g.state(cells)
            except KeyError:
                tally['outside tube'] += 1; continue
            win = lambda s: frozenset(c for c in g.cells_of(s) if first - 12 <= unit(c) <= N + 6)
            if win(g.run(x, 2, sparse=True)) != win(x):
                tally['unlit not stationary'] += 1; continue
            y = g.run(x, 0, sparse=True) if False else x.copy(); y[g.index[ign]] = 1
            seen = Counter(); clean = True; wrote = []
            for t in range(2, T + 1, 2):
                y = g.run(y, 2, sparse=True)
                d = pc.decode(y, first - 60, first - 2)
                if set(d) - set('7b'):
                    clean = False; break
                if '7' in d:
                    wrote.append(t)
            if not clean:
                tally['tape disturbed'] += 1; continue
            if not wrote:
                tally['nothing written'] += 1; continue
            tally['WRITES'] += 1
            z = g.run(y, p, sparse=True)
            back = win(z) == win(y)
            hits.append(dict(state=sid, gap=gap, ncells=len(R1), first_write=wrote[0], nwrites=len(wrote), caps_periodic=back))
            print('WRITES', hits[-1], pc.decode(y, first - 40, N + 3), flush=True)
    print(dict(tally))
    json.dump(hits, open(sg.os.path.join(sg.SCR, 'backtoback.json'), 'w'))


if __name__ == '__main__':
    main()
