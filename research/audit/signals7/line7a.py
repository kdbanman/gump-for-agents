#!/usr/bin/env python3
"""The push's finite line (gun 4, 80 units of train, mirrored end 70; 419 cells) on the oracle, in a box where nothing
wraps (margin asserted dead at every generation).

    python3 line7a.py box [--G 1200]       line alone; E alone; E and n = 1..6 holes 3 rakes apart  (about 3 min)
    python3 line7a.py long [--G 40000]     the same on the helix ring L = 160 (checked equal to the box by
                                           check_helix.py), far longer                             (about 10 min)

For each run: the first generation g with state(g + 4) == state(g) on the WHOLE array (then the object has period
dividing 4 for ever: the rule is deterministic), its least period, the population, and the per-unit letters of the
state at the last generation.  Final unit arrays are saved to scratch (line7a_box.npz) for `line7b.py`.
Initial cells from the push: the line (record line-N80-gun4-end70-alone), E and the hole H (the record n1's flips).
"""
import sys, argparse
import numpy as np
import orc7 as O
from check_helix import line_events


def settle(T, h, flips, G, box):
    """Run to generation G.  Returns (g0, period, U): g0 the first generation with h(g0 + 4) == h(g0) (None if
    none by G), the least period dividing 4 from then, the unit array at G."""
    hist = []; g0 = None
    for t in range(G + 1):
        if t in flips:
            T.flip(h, flips[t])
        if box:
            T.check_margin(h)
        if g0 is None:
            if len(hist) == 4 and np.array_equal(hist[0], h):
                g0 = t - 4
                per = next(p for p in (1, 2, 4) if np.array_equal(hist[4 - p], h))
            hist.append(h)
            if len(hist) > 4:
                hist.pop(0)
        if t < G:
            h = T.step(h)
    assert T.outside(h) == 0
    return g0, (per if g0 is not None else None), T.units(h), h


def letters(U, ua, G):
    """Per unit: '_' empty, else a letter per distinct unit content (most common first: a, b, c..)."""
    from collections import Counter
    keys = [bytes(u) if u.any() else None for u in U]
    ct = Counter(k for k in keys if k is not None)
    name = {k: (chr(97 + i) if i < 26 else '#') for i, (k, _) in enumerate(ct.most_common())}
    return ''.join('_' if k is None else name[k] for k in keys)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['box', 'long']); ap.add_argument('--G', type=int)
    ap.add_argument('--nmax', type=int, default=6)
    a = ap.parse_args()
    y0, E, H = line_events()
    ua, ub = -30, 120
    box = a.mode == 'box'
    G = a.G or (1200 if box else 40000)
    assert G % 4 == 0
    T = O.Tor.box(ua, ub) if box else O.Tor.helix(160, -34)
    off = 0 if box else ua - T.ua
    out = {}
    runs = [('alone', {})] + [(f'n{n}', {1: E + [O.tr(c, 6 * j) for j in range(n) for c in H]}) for n in range(0, a.nmax + 1)]
    for name, fl in runs:
        g0, per, U, h = settle(T, T.arr(y0), fl, G, box)
        U = U[off: off + ub - ua]
        out[name] = U
        print(f'{name:6s} torus {T.shape}: periodic from generation {g0}, least period {per}; {int(U.sum())} cells at generation {G}', flush=True)
        print(f'        units {ua}..{ub - 1}: {letters(U, ua, G)}', flush=True)
    if box:
        np.savez_compressed(O.os.path.join(O.SCR, 'line7a_box.npz'), **out)
    ns = [k for k in out if k.startswith('n')]
    print('final states pairwise different:', all(not np.array_equal(out[i], out[j]) for i in ns for j in ns if i < j))


if __name__ == '__main__':
    main()
