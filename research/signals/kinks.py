#!/usr/bin/env python3
"""Phase kinks: repeats 10..29 of a ring of 40 start at phase d, the rest at phase 0.  Does the boundary move?

    python3 kinks.py [WID ...]         # default all 21 wires; ~4 min

Per wire and per d = 1 .. P-1: run 40 P generations (or to a cycle) and label every repeat by the phase of the wire
it is in, relative to the phase-0 region ('.' = not a phase of the wire).  Reported per wire:
  static   both boundaries are where they started and every repeat away from them is still a wire phase
  moved    some repeat changed from one wire phase to another (a kink that travels: listed)
  burnt    a region that is no phase of the wire has grown by more than 3 repeats (a front)
"""
import sys
from collections import Counter
import numpy as np
import wirelab as wl

N = 40


def labels(g, x, rows, t, P):
    """Phase offset of every repeat relative to the intact wire at time t, or -1."""
    M = g.as_grid(x); out = []
    for u in range(N):
        lab = -1
        for j in range(P):
            if (M[u] == rows[(t + j) % P][u]).all():
                lab = j; break
        out.append(lab)
    return out


def main():
    ids = sys.argv[1:]
    for rec in wl.all_wires():
        if ids and rec['id'] not in ids:
            continue
        P = rec['period']
        g = wl.ring(rec, N, 16, (-7, 23))
        orb = g.orbit(wl.wire_state(g, rec), P - 1)
        rows = [g.as_grid(o) for o in orb]
        res = Counter(); moved = []
        for d in range(1, P):
            M = rows[0].copy(); M[10:30] = rows[d][10:30]
            x = g.from_grid(M)
            T = 40 * P
            x = g.run(x, T, sparse=True)
            lab = labels(g, x, rows, T, P)
            a = sum(1 for u in range(N) if lab[u] == 0); b = sum(1 for u in range(N) if lab[u] == d); bad = sum(1 for u in range(N) if lab[u] < 0)
            oth = N - a - b - bad
            if bad > 8:
                res['burnt'] += 1
            elif oth > 0 or abs(a - 20) > 2 or abs(b - 20) > 2:
                res['moved'] += 1; moved.append((d, ''.join('.' if v < 0 else '0123456789abcdefghijklmnopqrstuvwxyz'[v] for v in lab)))
            else:
                res['static'] += 1
        print(rec['id'], 'P%d' % P, dict(res), flush=True)
        for d, s in moved[:6]:
            print('    d = %d: %s' % (d, s))


if __name__ == '__main__':
    main()
