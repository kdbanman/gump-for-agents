#!/usr/bin/env python3
"""One- and two-cell flips of every wire on file: what happens to each.

    python3 flips.py [--pairs] [--N 32] [WID ...]     # singles: ~10 min for all 21; with --pairs: hours

For each wire (ring of N repeats, images 16 cubes apart, 16 layers), each phase t and each candidate cell c of one
repeat (every cell that is live in some phase, and every neighbour of such a cell), flip c at phase t and run beside
the intact wire (sgc.c track).  With --pairs: flip c and one more candidate cell within 4 doubled units (max-norm) of
c, in the same or an adjacent repeat.  Fates:
  heals    the difference vanishes                      stays   settles into a cycle, never further than REACH repeats
  runs     the difference comes to span 12 repeats (a front, on one side or both; `sides` says which)
  pulse    the difference at some time lies wholly at least 3 repeats to one side of where it was made
  open     none of these within MAXGEN generations
Writes one JSON line per wire to research/scratch/signals/flips_<singles|pairs>.jsonl and prints a table.
"""
import argparse, json, os
from collections import Counter
import numpy as np
import sg
import wirelab as wl

ap = argparse.ArgumentParser()
ap.add_argument('ids', nargs='*'); ap.add_argument('--pairs', action='store_true'); ap.add_argument('--N', type=int, default=32)
ap.add_argument('--maxgen', type=int, default=1500)
a = ap.parse_args()
N = a.N; u0 = N // 2
out = open(os.path.join(sg.SCR, 'flips_%s.jsonl' % ('pairs' if a.pairs else 'singles')), 'a')
grand = Counter()
for rec in wl.all_wires():
    if a.ids and rec['id'] not in a.ids:
        continue
    P = rec['period']
    g = wl.ring(rec, N, 16, (-7, 23))
    orb = g.orbit(wl.wire_state(g, rec), P - 1)
    U = np.nonzero(np.array([o[:g.n] for o in orb]).any(0))[0]
    cand = set(U.tolist()) | set(g.nb[U].ravel().tolist()); cand.discard(g.n)
    c0 = sorted(i for i in cand if g.unit[i] == u0)
    near = sorted(i for i in cand if abs(int(g.unit[i]) - u0) <= 1)
    if a.pairs:
        # lifted coordinates near the origin repeat, to measure distances between candidates
        base = g.cells[c0[0]]
        def lifted(i):
            p = g.cells[i]; v = rec['v']; w = wl.transverse(v, 16); best = None
            for k in (-1, 0, 1):
                for m in (-1, 0, 1):
                    q = tuple(p[j] + 2 * k * N * v[j] + 2 * m * w[j] for j in range(3))
                    d = max(abs(q[j] - base[j]) for j in range(3))
                    if best is None or d < best[0]:
                        best = (d, q)
            return best[1]
        L = {i: lifted(i) for i in near}
        trials = [(i, j) for i in c0 for j in near if j != i and max(abs(L[i][k] - L[j][k]) for k in range(3)) <= 4
                  and (g.unit[j] != u0 or j > i)]
    else:
        trials = [(i,) for i in c0]
    fates = Counter(); notable = []
    for t in range(P):
        for tr in trials:
            x = orb[t].copy()
            for i in tr:
                x[i] ^= 1
            r = g.track(orb[t], x, u0, span=12, maxgen=a.maxgen)
            lo, hi = r['lo'], r['hi']
            reach = int(max(hi.max(), -lo.min()))
            away = bool(((lo >= 3) | (hi <= -3))[r['cnt'] > 0].any())
            if away:
                fate = 'pulse'
            elif r['ret'] == 0:
                fate = 'heals'
            elif r['ret'] == 1:
                fate = 'stays'
            elif r['ret'] == 2:
                fate = 'runs'
            else:
                fate = 'open'
            fates[fate] += 1
            if fate in ('pulse', 'open', 'runs') or (fate == 'stays' and reach >= 4):
                sides = ('+' if hi[-1] >= 5 else '') + ('-' if lo[-1] <= -5 else '')
                notable.append(dict(t=t, cells=[list(g.cells[i]) for i in tr], fate=fate, gens=int(r['gens']), per=int(r['per']),
                                    lo=int(lo.min()), hi=int(hi.max()), sides=sides))
    sides = Counter(x['sides'] for x in notable if x['fate'] == 'runs')
    line = dict(id=rec['id'], P=P, N=N, pairs=a.pairs, candidates=len(c0), trials=len(trials) * P, fates=dict(fates), run_sides=dict(sides),
                max_stay_reach=max([max(x['hi'], -x['lo']) for x in notable if x['fate'] == 'stays'] or [0]), notable=notable[:4000])
    out.write(json.dumps(line) + '\n'); out.flush()
    grand.update(fates)
    print('%s P%-2d %-11s cand %3d trials %6d: %s; runs by side %s; pulses %d' % (
        rec['id'], P, tuple(rec['v']), len(c0), len(trials) * P, dict(sorted(fates.items())), dict(sides), fates['pulse']), flush=True)
print('all wires:', dict(grand))
