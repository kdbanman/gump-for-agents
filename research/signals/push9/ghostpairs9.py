#!/usr/bin/env python3
"""ghostpairs9 (push 9): a trigger cell held live together with a second held cell: is any pair a trigger that
does not harm a pulse on plain wire?

    python3 ghostpairs9.py [--rmax 8]

First ghost: (0,1,8) (the still life's cell that biases the stator of the unit before the wall: release b^(2k+2)) or
(-2,1,10) (the same one unit to the left: b^(2k+5)).  Second ghost: every cell of ghost9.ghost_cells(rmax).
Printed: counts of (wall outcome, what the right-going pulse does on plain wire), and every pair that releases at
the wall and passes or eats the right-going pulse on plain wire.
"""
import sys, argparse, time
from collections import Counter
import ghost9 as G


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--rmax', type=int, default=8)
    a = ap.parse_args()
    gs = G.ghost_cells(a.rmax)
    for g1 in ((0, 1, 8), (-2, 1, 10)):
        t0 = time.time()
        sets = [[g1, g] for g in gs if g != g1]
        res = G.census(sets, 3)
        c = Counter(); good = []
        for s, r in zip(sets, res):
            if r is None:
                continue
            wall = 'release' if (r.get('wA', '').startswith('RELEASE') and r.get('wB', '').startswith('RELEASE')) else (
                'falls' if r['wall'].startswith('falls') else ('absorbed' if r.get('wA') == 'absorbed' else 'other'))
            pr = (r.get('pRA', '-').split(' ')[0], r.get('pRB', '-').split(' ')[0]) if r['plain'] == 'stands' else ('plain falls',)
            c[(wall, pr)] += 1
            if wall == 'release' and pr[0] in ('pass', 'eaten', 'to') and pr[-1] in ('pass', 'eaten', 'to'):
                good.append((s, r))
        print(f'first ghost {g1}: {len(sets)} pairs  [{time.time() - t0:.0f} s]')
        for k, v in c.most_common():
            print(f'  {v:5d}  wall: {k[0]:9s} plain wire, right-going pulse: {k[1]}')
        for s, r in good:
            print('   GOOD', s, r)


if __name__ == '__main__':
    main()
