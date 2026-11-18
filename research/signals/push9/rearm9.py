#!/usr/bin/env python3
"""rearm9 (push 9): can a signal put a stretch back beside the still life?

    python3 rearm9.py [--K 3] [--j 0]

Plain wire B on a ring of 60 units with the still life placed for unit 30 + j... i.e. the trigger's place when a
stretch's first unit is 30.  Every word of up to K family units is put in the wire 10 units to the left of unit 30
(its last unit at 19) and, in a second run, 10 units to the right (its first unit at 42), and the ring is read 120
generations later.  Reported: the outcomes that are standing (period 2), keep the still life, and hold a unit d.
"""
import sys, itertools, argparse, time
from collections import Counter
import numpy as np
import lab9 as Z, cell9 as C
from lab9 import Lab, tr, unit, X, W

R = 60; W0 = 30


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--K', type=int, default=3); ap.add_argument('--j', type=int, default=0)
    a = ap.parse_args()
    S = [tuple(c) for c in C.trig(W0 + a.j)]
    L = Lab(0, R, -8, 12, -8, 20, ring=True)
    base = L.arr(X.hexword('7' * R, 0)); L.flip(base, S)
    out = Counter(); hits = []
    t0 = time.time(); n = 0
    for K in range(1, a.K + 1):
        for w in itertools.product('0123456789abcdef', repeat=K):
            w = ''.join(w)
            if w[0] == '7' or w[-1] == '7':
                continue
            for side, u in (('L', W0 - 10 - K), ('R', W0 + 12)):
                x = base.copy(); L.flip(x, X.hexword('7' * K, u) ^ X.hexword(w, u)); L.run(x, 120)
                n += 1
                y = x.copy(); L.run(y, 2)
                s = Z.hexring(L, x)
                if not np.array_equal(x, y) or Z.outside(L, x) != frozenset(S) or 'd' not in s or '?' in s:
                    out['standing with a d' if np.array_equal(x, y) and 'd' in s else ('plain' if s == '7' * R and np.array_equal(x, y) else 'other')] += 1
                    continue
                i = s.index('d')
                hits.append((side, w, i - W0, X.hexrle(s)))
                out['stretch'] += 1
    print(f'{n} runs, {time.time() - t0:.0f} s: {dict(out)}')
    c = Counter((h[0], h[2], h[3]) for h in hits)
    for (side, off, s), v in sorted(c.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        ex = [h[1] for h in hits if (h[0], h[2], h[3]) == (side, off, s)][:6]
        print(f'  from the {"left" if side == "L" else "right"}: first d at unit {off:+d} relative to the trigger place: {s}   ({v} words, e.g. {ex})')


if __name__ == '__main__':
    main()
