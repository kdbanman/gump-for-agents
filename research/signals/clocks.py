#!/usr/bin/env python3
"""Shuttle clocks with other caps: which caps of wire C turn the rake round, and what periods result.

    python3 clocks.py TABLE.json [--N 10] [--out FILE]

TABLE.json: output of scatter_table.py for wire C (survey wire 28): its `states` are caps of wire C (cells relative
to their first unit).  Each cap is put at the +v end of N units of wire C whose -v end carries capL of
objects/clock-C.json; one cell (the rake) is added in the middle; the state is stepped (sg.step_set, the infinite
lattice) until it repeats or 40N + 600 generations pass.  Reported: the caps for which the lit object is periodic
with period > 2 and the rake still shuttles (period grows by 4 per unit: checked at N and N + 1), by period.
"""
import argparse, json, sys
from collections import Counter
import sg, scat

tr = scat.tr


def period(cells, maxgen):
    seen = {}; y = frozenset(cells); t = 0
    while y not in seen and t < maxgen:
        seen[y] = t; y = sg.step_set(y); t += 1
    return (t - seen[y], seen[y]) if y in seen else (0, t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table'); ap.add_argument('--N', type=int, default=10); ap.add_argument('--out'); ap.add_argument('--max', type=int, default=10 ** 9)
    a = ap.parse_args()
    D = json.load(open(a.table)); ck = json.load(open('objects/clock-C.json'))
    capL = [tuple(c) for c in ck['capL']]; unit = [tuple(c) for c in ck['unit']]
    res = Counter(); good = []
    for sid, cap in sorted(D['states'].items(), key=lambda kv: int(kv[0]))[:a.max]:
        cap = [tuple(c) for c in cap]
        if not cap or max(scat.unit(c) for c in cap) > 8:
            continue
        ps = []
        for N in (a.N, a.N + 1):
            cells = set(capL) | {tr(c, k) for c in unit for k in range(N)} | {tr(c, N) for c in cap}
            if sg.step_set(sg.step_set(frozenset(cells))) != frozenset(cells):
                ps = None; break
            p, t0 = period(cells | {tr((1, 0, 4), N // 2)}, 40 * N + 600)
            ps.append(p)
        if ps is None:
            res['unlit object not stationary'] += 1
        elif ps[0] > 2 and ps[1] == ps[0] + 4:
            res['clock'] += 1; good.append((int(sid), ps[0] - 4 * a.N, cap))
        elif ps[0] in (1, 2):
            res['settles'] += 1
        elif ps[0] == 0:
            res['no repeat'] += 1
        else:
            res['periodic, not a shuttle (%d, %d)' % tuple(ps)] += 1
    print(dict(res))
    by = Counter(c for _, c, _ in good)
    print('clocks: period = 4N + c, with c:', dict(sorted(by.items())))
    for c in sorted(by):
        sid, _, cap = min((g for g in good if g[1] == c), key=lambda g: len(g[2]))
        print(f'   c = {c}: {by[c]} caps; smallest: state {sid}, {len(cap)} cells: {sorted(cap)}')
    if a.out:
        json.dump([dict(state=s, c=c, cap=[list(x) for x in cap]) for s, c, cap in good], open(a.out, 'w'))


if __name__ == '__main__':
    main()
