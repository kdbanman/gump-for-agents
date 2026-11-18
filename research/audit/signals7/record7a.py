#!/usr/bin/env python3
""""A count that lasts, on the infinite train" (the push's record7.py) on the oracle.

    python3 record7a.py [--end 70]        (1 min)

The 20-cell end #70 of the push (cells from wireB_caps.json) at the end of a FINITE (fb) train on the helix ring
L = 448 (train on units -408..5).  At generation 1: E at unit KS - 26 and n holes H at KS - 40, KS - 46, .. (3 rakes
apart), n = 0..6.  The cut tail can influence unit u at generation t only if u <= -405 + t, so units >= KS - 60 are
exact for the semi-infinite train up to generation 300.  Printed per n: the least period of units >= KS - 60 on
generations 150..166 and 250..266, whether generations 158 and 258 are equal there, and the units (from KS - 60) in
the four-site code after subtracting nothing: '7' B, 'd' B', 'f' the edge unit, '#' the end.
"""
import sys, json, os
import numpy as np
import orc7 as O, census7a as CA, lines as Ln

KS = 6


def main():
    which = int(sys.argv[sys.argv.index('--end') + 1]) if '--end' in sys.argv else 70
    cap = next([tuple(c) for c in e['cap']] for e in Ln.caps()['receiving'] if e['i'] == which)
    K = CA.kinds('fb')
    L = 448; ulo = KS + 24 - L + 10; ua = ulo - 10
    T = O.Tor.helix(L, ua)
    assert ulo + 266 + 3 <= KS - 60
    finals = {}
    for n in range(0, 7):
        h = T.step(T.arr(O.train0('fb', ulo, KS) | frozenset(cap)))
        T.flip(h, [O.tr(c, KS - 26) for c in K['E']['cells']] + [O.tr(c, KS - 40 - 6 * j) for j in range(n) for c in K['H']['cells']])
        t = 1; snaps = {}
        for G in (150, 250):
            h = T.step(h, G - t); t = G; seq = []
            for j in range(17):
                seq.append(T.units(h)[KS - 60 - ua:].copy()); h = T.step(h); t += 1
            snaps[G] = seq
        assert T.outside(h) == 0
        per = [next((p for p in (1, 2, 4, 8) if all(np.array_equal(sq[j], sq[j + p]) for j in range(17 - p))), None) for sq in snaps.values()]
        stand = np.array_equal(snaps[150][8], snaps[250][8])
        fin = snaps[250][14]                                  # generation 264 (even: family codes readable)
        finals[n] = fin
        c = Ln.code(fin)
        nb = c.count('d'); nf = c.count('f')
        print(f'n={n}: least period on 150..166 / 250..266: {per[0]} / {per[1]}; generation 158 == 258: {stand}; '
              f"{nb} units of B', {nf} edge units; units {KS - 60}.. at 264: {c}", flush=True)
    ns = sorted(finals)
    print('final states (units >= KS - 60, generation 264) pairwise different for n = 1..6:',
          all(not np.array_equal(finals[i], finals[j]) for i in ns for j in ns if 0 < i < j))


if __name__ == '__main__':
    main()
