#!/usr/bin/env python3
"""ghost9 (push 9): what ONE cell held live beside the wall of a stretch does (a census of static biases).

    python3 ghost9.py [--k 3] [--rmax 8] [--out F.json]

A ghost is a cell held live for ever (lab9.run_bias: it adds one to the count of each of its 12 neighbours and never
changes).  It stands for one cell of an object that is not changed by what happens on the wire.  Ghost positions:
every cell with tube radius |y| + |x+z-3| between 3 and rmax in the units -4..+4 relative to the first unit of
the stretch d^k f (ring of 36 units, wall 17|18).  For each ghost, eight runs of 76 generations:
  wall:   rest; a right-going pulse born 11 and 12 units before the wall (A, B)
  plain:  rest; a right-going pulse born at unit 6 and 7; a left-going pulse born at unit 30 and 29
Printed: counts of outcome vectors, and every ghost with a release.
"""
import sys, json, argparse, time
from collections import Counter, defaultdict
import numpy as np
import lab9 as Z
from lab9 import Lab, tr, unit, X, W

R = 36; W0 = 18; T = 76


def read_wall(L, a, k, grown):
    s = Z.hexring(L, a)
    if s == '7' * (W0 - grown) + 'd' * (k + grown) + 'f' + '7' * (R - W0 - k - 1):
        return 'absorbed' if grown else 'stands'
    if not (set(s) - set('7b6f')) and Z.outside(L, a) == frozenset():
        nb = s.count('b'); n6 = s.count('6')
        return f'RELEASE {X.hexrle(Z.canon_ring(s))}' if nb + n6 else 'ERASED'
    return 'other ' + X.hexrle(s)


def read_plain(L, a, exp):
    if np.array_equal(a, exp):
        return 'pass'
    s = Z.hexring(L, a)
    if s == '7' * R and Z.outside(L, a) == frozenset():
        return 'eaten'
    if not (set(s) - set('7b6f')) and Z.outside(L, a) == frozenset():
        return 'to ' + X.hexrle(Z.canon_ring(s))
    return 'other ' + X.hexrle(s)


def census(ghost_sets, k=3, box=(-14, 14, -12, 18)):
    """ghost_sets: list of lists of cells (relative to the wall unit = unit 0).  Returns a list of outcome dicts."""
    L = Lab(0, R, *box, ring=True)
    wallw = '7' * W0 + 'd' * k + 'f' + '7' * (R - W0 - k - 1)
    wall0 = L.arr(X.hexword(wallw, 0)); plain0 = L.arr(X.hexword('7' * R, 0))
    out = []
    for gs in ghost_sets:
        g = [tr(c, W0) for c in gs]
        try:
            bias = Z.bias_of(L, g)
        except ValueError:
            out.append(None); continue
        res = {}
        if any(wall0[L.idx(c)] for c in g):
            res['wall'] = 'overlap'
        else:
            a = wall0.copy(); Z.run_bias(L, a, bias, 16)
            res['wall'] = 'stands' if np.array_equal(a, wall0) else None
            if res['wall'] is None:
                Z.run_bias(L, a, bias, T - 16); res['wall'] = 'falls: ' + read_wall(L, a, k, 0)
            else:
                for nm, u in (('wA', W0 - 11), ('wB', W0 - 12)):
                    a = wall0.copy(); L.flip(a, X.pulseR(u)); Z.run_bias(L, a, bias, T)
                    res[nm] = read_wall(L, a, k, 1)
        if any(plain0[L.idx(c)] for c in g):
            res['plain'] = 'overlap'
        else:
            a = plain0.copy(); Z.run_bias(L, a, bias, 16)
            res['plain'] = 'stands' if np.array_equal(a, plain0) else 'falls'
            if res['plain'] == 'stands':
                for nm, fl in (('pRA', X.pulseR(6)), ('pRB', X.pulseR(7)), ('pLA', X.pulseL(30)), ('pLB', X.pulseL(29))):
                    a = plain0.copy(); L.flip(a, fl); Z.run_bias(L, a, bias, 2 * R)
                    exp = plain0.copy(); L.flip(exp, fl)
                    res[nm] = read_plain(L, a, exp)
        out.append(res)
    return out


def ghost_cells(rmax, rmin=3, units=range(-4, 5)):
    out = []
    for u in units:
        for x in (2 * u, 2 * u + 1):
            for y in range(-rmax, rmax + 1):
                for wv in range(3 - rmax, 3 + rmax + 1):
                    c = (x, y, wv - x)
                    if Z.is_cell(c) and rmin <= abs(y) + abs(wv - 3) <= rmax:
                        out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--k', type=int, default=3); ap.add_argument('--rmax', type=int, default=8)
    ap.add_argument('--rmin', type=int, default=3); ap.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    gs = ghost_cells(a.rmax, a.rmin)
    res = census([[g] for g in gs], a.k)
    print(f'{len(gs)} ghost cells (tube radius {a.rmin}..{a.rmax}, units -4..4), k = {a.k}   [{time.time() - t0:.0f} s]')
    c = Counter()
    for g, r in zip(gs, res):
        wall = (r['wall'].split(' ')[0] + ' ' + ' '.join(r['wall'].split(' ')[1:2]), r.get('wA', '-').split(' ')[0], r.get('wB', '-').split(' ')[0])
        plain = (r['plain'],) + tuple(r.get(n, '-').split(' ')[0] for n in ('pRA', 'pRB', 'pLA', 'pLB'))
        c[(wall, plain)] += 1
    for kk, v in c.most_common():
        print(f'{v:5d}  wall {kk[0]}   plain {kk[1]}')
    print('ghosts with a release:')
    for g, r in zip(gs, res):
        if any(isinstance(v, str) and 'RELEASE' in v for v in r.values()):
            print(' ', g, 'radius', abs(g[1]) + abs(g[0] + g[2] - 3), r)
    if a.out:
        json.dump([dict(ghost=g, res=r) for g, r in zip(gs, res)], open(a.out, 'w'))


if __name__ == '__main__':
    main()
