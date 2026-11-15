#!/usr/bin/env python3
"""Shoot pulses at stationary defects of a wire and say what comes out.

    python3 collide.py DEFECTS.json [--pulse objects/pulse-A.json] [--max 60]

DEFECTS.json: output of sat_defects.py with S = 0 (stationary defects of the wire, as cells differing from the
background at generation 0).  Each is placed on a ring of 96 cubes (tube [-7,13]^2: exact in free space), checked to
be stationary alone, and hit by the pulse from the left at two distances (d and d+1; they differ only for defects of
period > 2).  The outcome is read off the cubes that differ from the background, 300 and 340 generations later:
  target      what is left where the defect was: 'same', 'gone', or 'changed' (with its period)
  out         what left: 'R' (a cluster moving right), 'L' (moving left), 'fire' (the differing region keeps growing)
"""
import argparse, json
from collections import Counter
import numpy as np
import plab, sg

N = 96


def clusters(d):
    """Maximal runs of differing cubes (gaps of up to 2 clean cubes are bridged)."""
    us = np.nonzero(d)[0]; out = []
    for u in us:
        if out and u - out[-1][1] <= 3:
            out[-1][1] = int(u)
        else:
            out.append([int(u), int(u)])
    return out


def outcome(g, x, bg, site, T=300):
    x = g.run(x, T, sparse=True); b = g.run(bg, T, sparse=True)
    d1 = (g.as_grid(x) != g.as_grid(b)).sum(1)
    x2 = g.run(x, 40, sparse=True); b2 = g.run(b, 40, sparse=True)
    d2 = (g.as_grid(x2) != g.as_grid(b2)).sum(1)
    c1, c2 = clusters(d1), clusters(d2)
    out = []
    if (d2 > 0).sum() >= (d1 > 0).sum() + 12 or (d1 > 0).sum() > 40:
        out.append('fire')
    else:
        for a, b_ in c1:
            if any(abs(a + 20 - a2) <= 1 and abs(b_ + 20 - b2) <= 1 for a2, b2 in c2):
                out.append('R')
            elif any(abs(a - 20 - a2) <= 1 and abs(b_ - 20 - b2) <= 1 for a2, b2 in c2):
                out.append('L')
    here = [c for c in c2 if c[1] >= site - 6 and c[0] <= site + 10]
    return out, here, x2, b2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('defects'); ap.add_argument('--pulse', default='objects/pulse-A.json'); ap.add_argument('--max', type=int, default=60)
    a = ap.parse_args()
    ob = json.load(open(a.pulse)); D = json.load(open(a.defects))
    g = plab.geom(N); bg = plab.background(g, ob)
    site = 60
    res = Counter(); notable = []
    for k, sol in enumerate(D['solutions'][:a.max]):
        cells = [tuple(c) for c in sol['cells']]
        shift = site - sol['cubes'][0]
        x0 = plab.with_defect(g, bg, cells, shift)
        P = sol['period'] or 2
        alone = g.run(x0, 2 * P, sparse=True)
        if not (alone == x0).all():
            res['(not stationary alone)'] += 1; continue
        ref = [g.run(x0, t, sparse=True) for t in range(P)]
        for d in (0, 1):
            x = plab.with_defect(g, x0, ob['defect'], 20 + d)
            out, here, x2, b2 = outcome(g, x, bg, site)
            if 'fire' in out:
                tgt = '-'
            elif not here:
                tgt = 'gone'
            else:
                # same as the original defect (any phase)?  compare the cubes around the site
                Mx = g.as_grid(x2)[site - 8:site + 14]
                tgt = 'same' if any((Mx == g.as_grid(r)[site - 8:site + 14]).all() for r in ref) else 'changed'
            key = (tgt, ''.join(sorted(out)))
            res[key] += 1
            if key not in (('-', 'fire'),):
                notable.append((k, sol['ncells'], P, d, key, here))
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]):
        print(v, k)
    for x in notable[:40]:
        print('  defect #%d (%d cells, period %d) distance parity %d -> %s, clusters near site %s' % x)


if __name__ == '__main__':
    main()
