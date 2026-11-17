#!/usr/bin/env python3
"""Verify push 7's saved objects with reference/oracle.py alone (numpy and json; nothing else from this repository).

    python verify7.py [objects7.json] [--only NAME]

Each record holds initial cells (doubled coordinates) of a disturbed run `x0` and, where needed, of the undisturbed
run `y0` (the same end and finite train without the event), a ring length L (the oracle runs on the box torus
2L x 16 x 2L, on which the tube along v = (1,0,-1) closes into a ring of L units), and a claim:
  equal      x(t) == y(t) on the whole torus for every t in [gen, until]        (the end healed; nothing left anywhere)
  differ     x(until) != y(until) on units [ua, ub)                              (the end was not restored)
  periodic   x restricted to units [ua, ub) has period `period` on [gen, until], and units [wa, wb) of x are non-empty
             and of period 2 on [gen, until]                                     (an end standing with a wire in front)
  orbit      x0 alone: x(t + T) == x(t) on units [ua, ub) for t in [gen, until] (an end of period dividing T)
Units: unit(p) = floor(p.x / 2) with p in the record's own coordinates (before reduction mod the torus); a cell's
unit on the torus is taken as floor(x / 2) of its representative with x in [xlo, xlo + 2L), xlo = 2 * record['ulo'].
Prints PASS or FAIL per record and ALL PASS at the end.
"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402

HY = 16


def masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


class Ring:
    def __init__(self, L, ulo):
        self.L, self.ulo = L, ulo
        self.shape = (2 * L, HY, 2 * L)
        self.m = masks(self.shape)
        xs = np.arange(2 * L)
        # unit of each x index, for representatives with x in [2 ulo, 2 ulo + 2L)
        xr = ((xs - 2 * ulo) % (2 * L)) + 2 * ulo
        self.unit_of_x = xr // 2

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            i = (c[0] % self.shape[0], c[1] % self.shape[1], c[2] % self.shape[2])
            assert self.m[0][i] or self.m[1][i] or self.m[2][i], c
            h[i] = 1
        return h

    def step(self, h):
        return oracle.step(h, self.m)

    def units(self, h, ua, ub):
        sel = (self.unit_of_x >= ua) & (self.unit_of_x < ub)
        return h[sel, :, :]


def check(r):
    R = Ring(r['L'], r['ulo'])
    c = r['claim']; typ = c['type']
    x = R.arr(r['x0']); y = R.arr(r['y0']) if 'y0' in r else None
    G = c['until']
    if typ == 'equal':
        ok = True
        for t in range(G + 1):
            if t >= c['gen'] and not np.array_equal(x, y):
                ok = False; break
            if t < G:
                x = R.step(x); y = R.step(y)
        return ok
    if typ == 'differ':
        for t in range(G):
            x = R.step(x); y = R.step(y)
        return not np.array_equal(R.units(x, c['ua'], c['ub']), R.units(y, c['ua'], c['ub']))
    if typ in ('periodic', 'orbit'):
        P = c['period']; hist = []
        for t in range(G + 1):
            if t >= c['gen']:
                hist.append(x.copy())
            if t < G:
                x = R.step(x)
        ok = True
        for j in range(len(hist) - P):
            if not np.array_equal(R.units(hist[j], c['ua'], c['ub']), R.units(hist[j + P], c['ua'], c['ub'])):
                ok = False
        if typ == 'periodic':
            for j in range(len(hist)):
                w = R.units(hist[j], c['wa'], c['wb'])
                if not w.any():
                    ok = False
                if j + 2 < len(hist) and not np.array_equal(w, R.units(hist[j + 2], c['wa'], c['wb'])):
                    ok = False
        return ok
    raise ValueError(typ)


def main():
    fn = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(HERE, 'objects7.json')
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    recs = json.load(open(fn))['records']
    allok = True
    for r in recs:
        if only and r['name'] != only:
            continue
        ok = check(r)
        allok &= ok
        print(('PASS ' if ok else 'FAIL ') + r['name'] + ': ' + r['text'], flush=True)
    print('ALL PASS' if allok else 'SOME FAIL')


if __name__ == '__main__':
    main()
