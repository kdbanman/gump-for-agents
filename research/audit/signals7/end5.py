#!/usr/bin/env python3
"""The one 5 x 5 end the push has on file (objects7.json, records 27_5-end0-*; the README's row "5 x 5, C <= 27" is
"pending"), checked on the oracle and against this review's own instance.

    python3 end5.py        (2 min)

(1) its cells: how many lie outside the 3 x 3 tube, and the largest x+y-z and x-y-z over its four generations;
(2) it is an end: enum7.restep (oracle, the end on a finite train, units >= -6 equal after 4 generations);
(3) it is a model of the review's CNF for the 5 x 5 tube at C = 27 (enum7.build, the cap given as assumptions) and
    not of the one at C = 25;
(4) the 16 events of the census on the oracle (census7a.Census.row), against the text of the push's records.
"""
import json, time
import numpy as np
import orc7 as O, enum7, census7a as CA


def main():
    t0 = time.time()
    recs = [r for r in O.objects()['records'] if r['name'].startswith('27_5-end0-')]
    cap = sorted(tuple(c) for c in next(r for r in recs if r['name'].endswith('-orbit'))['y0'])
    out3 = [c for c in cap if not O.in_tube(c, 1, 5)]
    print(f'(1) {len(cap)} cells, units {min(map(O.unit, cap))}..{max(map(O.unit, cap))}; outside the 3 x 3 tube: {len(out3)} {out3}; outside the 5 x 5 tube: {sum(1 for c in cap if not O.in_tube(c))}')
    T = O.Tor.helix(O.helix_len(120), -90)
    h = T.arr(O.train0('fb', -60, enum7.KS) | frozenset(cap)); m = []; sizes = []; o3 = []
    for t in range(4):
        cs = [c for c in T.cells(h) if O.unit(c) >= enum7.KS]
        m.append(max(max(c[0] + c[1] - c[2], c[0] - c[1] - c[2]) for c in cs)); sizes.append(len(cs))
        o3.append(sum(1 for c in cs if not O.in_tube(c, 1, 5)))
        h = T.step(h)
    print(f'    over its four generations: cells on units >= 6: {sizes}; of them outside the 3 x 3 tube: {o3}; largest of x+y-z, x-y-z: {m} (the bound C = 27)')
    print(f'(2) restep on the oracle: {enum7.restep("fb", cap)}')
    from pysat.solvers import Solver
    for C in (27, 25):
        cells, X, f, P = enum7.build('fb', C, -1, 7)
        idx = {c: i for i, c in enumerate(cells)}
        if not all(c in idx for c in cap):
            print(f'(3) C = {C}: {sum(1 for c in cap if c not in idx)} of its cells lie outside the region: not a model'); continue
        on = {idx[c] for c in cap}
        with Solver(name='cadical153', bootstrap_with=f.cl) as sv:
            ok = sv.solve(assumptions=[X[0][i] if i in on else -X[0][i] for i in range(len(cells))])
        print(f'(3) C = {C}: {len(cells)} region cells; the cap as assumptions: {"SAT, a model" if ok else "UNSAT"}')
    Cn = CA.Census('fb'); row = Cn.row(cap)
    names = {('word', w): 'holes' + ''.join(map(str, w)) for w in map(tuple, CA.WORDS)}
    bad = 0
    for o in row['outcomes']:
        ev = (o['ev'][0], tuple(o['ev'][1]) if o['ev'][0] == 'word' else o['ev'][1])
        if ev[0] == 'wireB':
            print(f'    lower edge of wire B (no record of the push): {o["out"]}'); continue
        nm = names.get(ev, ev[1])
        r = next((r for r in recs if r['name'].endswith('-' + nm)), None)
        theirs = None if r is None else ('healed' if 'heals' in r['text'] else ('dead' if 'not healed' in r['text'] else '?'))
        same = theirs == o['out']; bad += not same
        print(f'    {nm:12s} here: {o["out"]:7s} push: {theirs}  {"" if same else "<-- DIFFERENT"}')
    print(f'(4) 16 events on the oracle: {16 - bad} as the push\'s records say; orbit of period dividing 4: {row["orbit"]}, period {row.get("period")}; {time.time() - t0:.0f} s')


if __name__ == '__main__':
    main()
