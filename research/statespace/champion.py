#!/usr/bin/env python3
"""Verify a champion file on reference/oracle.py alone (no enumerator involved).

  python3 research/statespace/champion.py research/statespace/data/champions/NAME.txt

The file names the vessel (vessels.py), the claimed transient and period, and the live cells (doubled coords).
The seed is lifted into the oracle's array torus (vessels.embed: a padded box for a hull, a periodic tiling for a
slab or torus), stepped with oracle.step, and read back on the vessel's cells; the first repeated state gives the
transient (generation at which the final cycle is entered) and the period. Also checks that no cell outside the
vessel is ever alive. Prints OK or FAIL.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import vessels as V
import oracle


def main(fn):
    lines = [l.split() for l in open(fn) if l.strip() and not l.startswith('#')]
    kind = lines[0][1]; args = [int(x) for x in lines[0][2:]]
    T = int(lines[1][1]); P = int(lines[2][1])
    v = V.make(kind, args)
    live = [v.canon(tuple(int(x) for x in l)) for l in lines[3:]]
    H, place, others = V.embed(v)
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    for k in live:
        for q in place[k]:
            h[q] = 1
    oth = tuple(np.array(others).T) if others else None
    first = {}
    g = 0
    while True:
        key = tuple(int(h[place[i][0]]) for i in range(v.n))
        if key in first:
            t0 = first[key]; per = g - t0
            break
        first[key] = g
        h = oracle.step(h, m); g += 1
        if oth is not None and h[oth].any():
            print('FAIL: a cell outside the vessel came alive at generation', g); sys.exit(1)
    ok = (t0, per) == (T, P)
    print(('OK' if ok else 'FAIL'), f'{v.name()}: oracle transient {t0}, period {per}; file says {T}, {P}')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main(sys.argv[1])
