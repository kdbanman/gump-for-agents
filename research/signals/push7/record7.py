#!/usr/bin/env python3
"""A count that lasts at the receiving end: E against a word of n holes in front of an end that caps wire B.

    python record7.py CENSUS.json [--n 0,1,2,3,4] [--s 3] [--which 0]

From the census rows whose wire-B outcome is 'wireB:cap', take the one with the fewest cells (or --which k in order
of cells).  Events (absorber frame, train (fb)^inf moving +v into the end; kinds of signals7.json at train phase 1,
generation 1): E at unit KS - 26 and n holes H at units KS - 40, KS - 40 - 2s, ... (s rakes apart).  E meets the first
hole, the stream between the two edges becomes wire B, the later holes meet the upper edge and leave a stretch of
wire B' standing in the wire B (README section 31), and the lower edge runs down into the end.
Stepped with step7 (window of 220 units below the end, the plain train below it; exact while the upper edge, which
leaves near unit KS - 30 at one unit per 2 generations, has not reached the window's lower boundary: some 380
generations).  Printed for each n: whether units >= KS - 60 have period dividing 8 on generations 150..166 and
250..266 and are equal at 166 and 266 (standing), and the units (from KS - 60) that differ from wire B, by letter:
'.' wire B, '#' other, at generation 266; and whether the final states for different n differ.
"""
import sys, os, json, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import census7 as C
from step7 import Window, INDEX
from scat import unit, tr

KS = C.KS


def run(cap, n, s, upto=266):
    W = Window('fb', KS - 220, KS + C.WR)
    y = W.array(C.G.train_cells(C.pat, 0, W.ua, KS, 1) | frozenset(tuple(c) for c in cap))
    W.run(y, 0, 1); x = y.copy()
    D = [tr(tuple(c), KS - 26) for c in C.SK[C.NAMES.index('E')]['cells']]
    for j in range(n):
        D += [tr(tuple(c), KS - 40 - 2 * s * j) for c in C.SK[C.NAMES.index('H')]['cells']]
    for c in D:
        u = unit(c); x[u - W.ua, INDEX[tr(c, -u)]] ^= 1
    t = 1; snaps = {}
    for T in (150, 250):
        W.run(x, t, T - t); t = T
        seq = []
        for j in range(17):
            seq.append(x[220 - 60:].copy()); W.run(x, t, 1); t += 1
        snaps[T] = seq
    per = all(np.array_equal(sq[j], sq[j + 8]) for sq in snaps.values() for j in range(9))
    stand = np.array_equal(snaps[150][8], snaps[250][8])          # generations 158 and 258 (equal mod 4... and 8)
    final = snaps[250][16]                                          # generation 266
    T = C.wireB_template()
    letters = ''.join('.' if np.array_equal(final[k], T[266 % 4, (KS - 60 + k) % 2]) else ('_' if not final[k].any() else '#')
                      for k in range(final.shape[0]))
    return per, stand, letters, final


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('census'); ap.add_argument('--n', default='0,1,2,3,4')
    ap.add_argument('--s', type=int, default=3); ap.add_argument('--which', type=int, default=0)
    ap.add_argument('--json', help='write verify7 records (n >= 1) to this file')
    a = ap.parse_args()
    rows = [r for r in json.load(open(a.census))['rows'] if r['outcomes'][-1]['out'] == 'wireB:cap']
    rows.sort(key=lambda r: (r['cells'], r['i']))
    r = rows[a.which]
    print(f"end {r['i']} of {r['src']} ({r['cells']} cells, C={r['C']}); {len(rows)} ends cap wire B in this census")
    finals = {}
    for n in map(int, a.n.split(',')):
        per, stand, letters, final = run(r['cap'], n, a.s)
        finals[n] = final
        print(f"  n={n} holes (s={a.s}): period | 8 on 150..166 and 250..266: {per}; generation 158 == 258: {stand}")
        print(f"      units {KS - 60}..{KS + C.WR - 1} at 266: {letters}")
    ns = sorted(finals)
    print('  final states pairwise different:', all(not np.array_equal(finals[i], finals[j]) for i in ns for j in ns if i < j))
    if a.json:
        import make7
        recs = []
        for n in ns:
            if n == 0:
                continue
            D = [list(tr(tuple(c), KS - 26)) for c in C.SK[C.NAMES.index('E')]['cells']]
            for j in range(n):
                D += [list(tr(tuple(c), KS - 40 - 2 * a.s * j)) for c in C.SK[C.NAMES.index('H')]['cells']]
            ulo, L = make7.ring_for(166, KS - 40 - 2 * a.s * (n - 1))
            y0 = sorted(set(C.G.train_cells(C.pat, 0, ulo, KS, 1)) | set(tuple(c) for c in r['cap']))
            recs.append(dict(name=f"record-end{r['i']}-n{n}", L=L, ulo=ulo, y0=[list(c) for c in y0], flips=[[1, D]],
                             claim=dict(type='periodic', gen=150, until=166, period=8, ua=KS - 60, ub=KS + 14, wa=KS - 58, wb=KS - 44),
                             text=f"count that lasts: the {r['cells']}-cell end {r['i']} with E and {n} holes {a.s} rakes apart: "
                                  f"units {KS - 60}.. of period 8 at 150..166 with wire (period 2) on units {KS - 58}..{KS - 45}"))
        json.dump(dict(records=recs), open(a.json, 'w'))
        print(f'  wrote {len(recs)} records to {a.json}')


if __name__ == '__main__':
    main()
