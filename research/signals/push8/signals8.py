#!/usr/bin/env python3
"""signals8 (push 8): what each small change of a standing background becomes (the sixth push's method, section 30).

    python3 signals8.py wire  [--bg 7|d] [--pairs] [--T 60]   one-cell flips (5 x 5 tube) of the uniform wire B (7) or B' (d;
                                                          inside a stretch of 60 units: use --T 40 so that pulses do not reach its walls);
                                                          --pairs: also every two-cell flip inside the 3 x 3 tube on
                                                          two adjacent units
    python3 signals8.py wall  [--mid ddf] [--pairs]       the same at the two boundaries of the stretch `mid` in wire B

Background: capL + 7^50 + mid + 7^50 + capR (exp8.line), a finite object, so every run is exact on the infinite
lattice.  An event is a set of cells flipped at generation g0 (0 or 1; the background has period 2 away from capR).
The run and the undisturbed run are compared at generations g0 + T and g0 + T + 4 (T = 60).  The difference is cut into
clusters (pieces separated by 4 or more units that do not differ).  Verdicts:
  vanish        no difference at g0 + 60
  stand:<k>     one cluster, same cells at both times (a standing defect; k = number of cells that differ)
  move          every cluster at g0 + 64 is a cluster of g0 + 60 moved by +2 or -2 units (rigid, 1 unit per 2
                generations), or stands; the verdict lists each cluster as name(direction)
  other         anything else (a front, a slower object, growth)
A cluster's name is its set of difference cells relative to its lowest unit, at generation parity (g0 + 60) mod 2;
names are assigned in order of first appearance and written with their cells to the JSON output.
"""
import sys, os, json, itertools, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X
from lab8 import tr, unit

E5 = [(x, y, z) for x in (0, 1) for y in range(-4, 5) for z in range(-6, 9)
      if lab8.is_cell((x, y, z)) and -1 <= x + y + z <= 7 and -1 <= x - y + z <= 7]
E3 = [c for c in E5 if 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5]


def clusters(cells, gap=4):
    us = sorted(set(unit(c) for c in cells)); out = []
    for u in us:
        if out and u - out[-1][-1] < gap:
            out[-1].append(u)
        else:
            out.append([u])
    return [(g[0], frozenset(tr(c, -g[0]) for c in cells if g[0] <= unit(c) <= g[-1])) for g in out]


class Census:
    def __init__(self, mid='', nL=50, nR=50, T=60):
        self.obj, self.N = X.line(mid, nL, nR)
        self.L = X.lab_for(self.N)
        self.T = T
        self.ref = {}
        for g0 in (0, 1):
            r = self.L.arr(self.obj); self.L.run(r, g0); r0 = r.copy()
            self.L.run(r, T); r1 = r.copy(); self.L.run(r, 4)
            self.ref[g0] = (r0, self.L.cells(r1), self.L.cells(r))
        self.names = {}

    def name(self, shape, par):
        k = (par, shape)
        if k not in self.names:
            self.names[k] = 's%d' % len(self.names)
        return self.names[k]

    def event(self, flips, g0):
        L = self.L; r0, c1, c2 = self.ref[g0]
        a = r0.copy(); L.flip(a, flips)
        L.run(a, self.T); d1 = L.cells(a) ^ c1
        if not d1:
            return 'vanish', []
        L.run(a, 4); d2 = L.cells(a) ^ c2
        k1 = clusters(d1); k2 = clusters(d2)
        par = (g0 + self.T) % 2
        if len(k1) == 1 and len(k2) == 1 and k1 == k2:
            return 'stand:%d' % len(d1), [(self.name(k1[0][1], par), 0, k1[0][0])]
        if len(k1) != len(k2):
            return 'other', []
        parts = []
        for (u1, s1), (u2, s2) in zip(k1, k2):
            if s1 != s2 or u2 - u1 not in (-2, 0, 2):
                return 'other', []
            parts.append((self.name(s1, par), (u2 - u1) // 2, u1))
        return 'move', parts


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('what', choices=['wire', 'wall'])
    ap.add_argument('--bg', default='7'); ap.add_argument('--mid', default='ddf'); ap.add_argument('--pairs', action='store_true')
    ap.add_argument('--out'); ap.add_argument('--T', type=int, default=60)
    a = ap.parse_args()
    if a.what == 'wire':
        if a.bg == '7':
            C = Census('', 50, 50, a.T); sites = [54]
        else:
            C = Census('d' * 60 + 'f', 20, 20, a.T); sites = [4 + 20 + 30]
        label = 'wire ' + a.bg
    else:
        C = Census(a.mid, 50, 50, a.T)
        w0 = 4 + 50; w1 = w0 + len(a.mid) - 1          # first unit of the stretch; the edge unit
        sites = sorted(set(range(w0 - 2, w0 + 2)) | set(range(w1 - 1, w1 + 3)))
        label = 'stretch ' + a.mid + f' (units {w0}..{w1}; flips on units {sites})'
    rows = []
    for u in sites:
        for g0 in (0, 1):
            for c in E5:
                v, parts = C.event([tr(c, u)], g0)
                rows.append(dict(flips=[c], u=u, g0=g0, verdict=v, parts=parts))
    if a.pairs:
        for u in sites:
            for g0 in (0, 1):
                two = [tr(c, u) for c in E3] + [tr(c, u + 1) for c in E3]
                base = set(tr(c, u) for c in E3)
                for c1, c2 in itertools.combinations(two, 2):
                    if c1 not in base and c2 not in base:
                        continue
                    v, parts = C.event([c1, c2], g0)
                    rows.append(dict(flips=[tr(c1, -u), tr(c2, -u)], u=u, g0=g0, verdict=v, parts=parts))
    # summary
    from collections import Counter
    def key(r):
        if r['verdict'] == 'move':
            return 'move: ' + ' + '.join(sorted(f"{n}({'>' if d > 0 else '<' if d < 0 else '.'})" for n, d, _ in r['parts']))
        if r['verdict'].startswith('stand'):
            return r['verdict'] + ' ' + r['parts'][0][0]
        return r['verdict']
    print(label, f': {len(rows)} events')
    for nflip in (1, 2):
        cnt = Counter(key(r) for r in rows if len(r['flips']) == nflip)
        if cnt:
            print(f'  {nflip}-cell events: {sum(cnt.values())}')
            for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
                print(f'    {v:5d}  {k}')
    names = {v: dict(parity=k[0], cells=sorted(k[1])) for k, v in C.names.items()}
    for n in sorted(names, key=lambda s: int(s[1:])):
        print(f"  {n}: parity {names[n]['parity']}, {len(names[n]['cells'])} cells {names[n]['cells'][:10]}{' ...' if len(names[n]['cells']) > 10 else ''}")
    if a.out:
        json.dump(dict(label=label, rows=rows, names=names), open(a.out, 'w'))


if __name__ == '__main__':
    main()
