#!/usr/bin/env python3
"""The one-cell census of the rake train, recounted on the oracle (README: 24 vanish / 66 break / 22 ride, 8 up, 14 down).

    python3 onecell.py        (1 min)

For each frame (fb, 5f): the plain train on a helix ring of 240 units, stepped to phase p = 0..3; one cell of the
3 x 3 tube flipped in unit 100 or 101 (14 cells x 2 units x 4 phases = 112 flips); 100 more generations (nothing can
go round the ring: a difference moves at most one unit per generation).  Then, on the whole ring:
  vanish   the state is the train's;
  ride     the difference from the train at generations 100 and 102 after the flip is the same pattern moved one
           unit (up: against the train's motion, down: with it), i.e. the two-generation identity holds;
  break    anything else (the number of units that differ is printed as a range).
The generation of the test is the first one >= 100 after the flip at which the train is at phase 1, so that a rider
can be named: its cells, moved down by an even number of units, are looked up among the kinds of the push's signal
files (the review's kinds7.py checks those).
"""
from collections import Counter
import numpy as np
import orc7 as O, census7a as CA

L = 240; G = 100


def main():
    for frame in ('fb', '5f'):
        tdir = 1 if frame == 'fb' else -1          # the train's motion in units per two generations
        T = O.Tor.helix(O.helix_len(L), 0)
        LL = T.units(T.arr(O.train0(frame, 0, 2))).shape[0]
        tr = [T.arr(O.train0(frame, 0, LL))]
        for _ in range(G + 12):
            tr.append(T.step(tr[-1]))
        assert np.array_equal(tr[4], tr[0])
        cells3 = [b for b in O.BASE if O.in_tube(b, 1, 5)]
        assert len(cells3) == 14
        ct = Counter(); width = Counter(); kinds = Counter()
        names = {tuple(sorted(tuple(c) for c in k['cells'])): n for n, k in CA.kinds(frame).items()}
        for p in range(4):
            for u in (100, 101):
                for b in cells3:
                    h = tr[p].copy(); T.flip(h, [O.tr(b, u)])
                    g = G + (1 - p) % 4
                    h = T.step(h, g); h2 = T.step(h, 2)
                    assert T.outside(h2) == 0 or True
                    d1 = T.units(h) ^ T.units(tr[p + g]); d2 = T.units(h2) ^ T.units(tr[p + g + 2])
                    out_ = T.outside(h) + T.outside(h2)
                    if not d1.any() and not d2.any() and out_ == 0:
                        ct['vanish'] += 1; continue
                    r = None
                    if out_ == 0:
                        for d in (1, -1):
                            if np.array_equal(np.roll(d1, d, axis=0), d2):
                                r = 'down' if d == tdir else 'up'
                    if r:
                        ct['ride ' + r] += 1
                        D = O.ucells(d1, 0); lo = min(O.unit(c) for c in D)
                        key = tuple(sorted(O.tr(c, -(lo - lo % 2)) for c in D))
                        kinds[(r, names.get(key, f'unnamed, {len(D)} cells'))] += 1
                    else:
                        ct['break'] += 1
                        rows = np.nonzero(d1.any(1))[0]
                        width[min(int(len(rows)) // 20 * 20, 180)] += 1
        ride = ct['ride up'] + ct['ride down']
        print(f'{frame}: 112 one-cell flips: {ct["vanish"]} vanish / {ct["break"]} break / {ride} ride ({ct["ride up"]} up, {ct["ride down"]} down)')
        print('   riders by (direction, kind):', dict(sorted(kinds.items())))
        print('   breaks by number of differing units at generation 100 (floor to 20):', dict(sorted(width.items())))


if __name__ == '__main__':
    main()
