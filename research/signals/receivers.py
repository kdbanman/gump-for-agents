#!/usr/bin/env python3
"""Receivers: stationary defects of a wire that survive being hit by pulses, and what a train of pulses does to them.

    python3 receivers.py DEFECTS.json --pulse objects/pulse-B.json [--max 150] [--shots 8]

Each stationary defect (from sat_defects.py, S = 0) is placed at cube 60 of a ring of 96 (tube [-7,13]^2, exact in
free space) and hit from the left by one pulse after another (each launched at cube 20 once the ring is quiet again:
260 generations between shots).  After each shot: is the wire alight ('fire'); did a pulse come out on the right
('T', transmitted) or go back ('R', reflected); and the state of the target, named a, b, c, ... in order of first
appearance (the same letter = the same cells differing from the wire, in the same place, at an even generation).
A line such as  a -> b -> a  (no T, no R)  is a defect that absorbs every pulse and toggles.
"""
import argparse, json
from collections import Counter
import numpy as np
import plab, sg

N = 96; SITE = 60; WAIT = 260


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('defects'); ap.add_argument('--pulse', default='objects/pulse-B.json'); ap.add_argument('--max', type=int, default=150)
    ap.add_argument('--shots', type=int, default=8); ap.add_argument('--period', type=int, default=0); ap.add_argument('--show', type=int, default=40)
    a = ap.parse_args()
    ob = json.load(open(a.pulse)); D = json.load(open(a.defects))
    g = plab.geom(N); bg = plab.background(g, ob)       # WAIT is even, so the background is always in phase 0 at a shot
    bgG = g.as_grid(bg)
    summary = Counter(); lines = []
    for k, sol in enumerate(D['solutions'][:a.max]):
        per = sol['period'] or 2
        if a.period and per != a.period:
            continue
        x = plab.with_defect(g, bg, [tuple(c) for c in sol['cells']], SITE - sol['cubes'][0])
        if not (g.run(x, per, sparse=True) == x).all():
            continue
        names = {}; seq = []
        def name(x):
            d = g.as_grid(x) != bgG
            key = (d[SITE - 12:SITE + 16]).tobytes()
            return names.setdefault(key, 'abcdefghijklmnop'[len(names)] if len(names) < 16 else '?')
        seq.append(name(x)); ev = []
        for shot in range(a.shots):
            x = plab.with_defect(g, x, ob['defect'], 20)
            x = g.run(x, WAIT, sparse=True)
            d = (g.as_grid(x) != bgG).sum(1)
            if (d > 0).sum() > 40:
                ev.append('fire'); break
            # anything outside the site window?  the ring is 96 cubes and a pulse covers 130 cubes in 260 generations
            outside = [u for u in np.nonzero(d)[0] if not SITE - 12 <= u < SITE + 16]
            tag = ''
            if outside:
                # let it run on: classify by direction
                x2 = g.run(x, 8, sparse=True); d2 = (g.as_grid(x2) != bgG).sum(1)
                o2 = [u for u in np.nonzero(d2)[0] if not SITE - 12 <= u < SITE + 16]
                if o2 and outside:
                    sh = (o2[0] - outside[0]) % N
                    tag = 'T' if sh == 4 else ('R' if sh == N - 4 else '?')
                # remove what left, so that the next shot meets a clean ring: reset those cubes to the background
                M = g.as_grid(x).copy()
                for u in outside:
                    for w in (u - 1, u, u + 1):
                        if not SITE - 12 <= w % N < SITE + 16:
                            M[w % N] = bgG[w % N]
                x = g.from_grid(M)
                if not (g.run(x, 4, sparse=True) == x).all():
                    ev.append(tag + '!unclean'); break
            ev.append(tag or '-'); seq.append(name(x))
            if names and seq[-1] == '' :
                break
        s = ' -> '.join(seq) + '   out: ' + ' '.join(ev)
        kind = 'fire' if 'fire' in ev else ('eats, unchanged' if set(seq) == {'a'} and set(ev) == {'-'} else
                                           ('gone after first' if False else 'other'))
        summary[kind] += 1
        if 'fire' not in ev[:1]:
            lines.append((sol['ncells'], k + 1, 'P%d ' % per + s))
    print(dict(summary))
    for nc, k, s in sorted(lines)[:a.show]:
        print('  defect #%d (%d cells): %s' % (k, nc, s))


if __name__ == '__main__':
    main()
