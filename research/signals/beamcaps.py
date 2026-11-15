#!/usr/bin/env python3
"""What the rake stream of the gun does at every right cap on file: looking for an end that modulates the beam.

    python3 beamcaps.py TABLE.json [--max M] [--gens 800] [--out FILE]

TABLE.json: output of scatter_table.py for wire C (its `states` are right caps of wire C, cells relative to their
first unit, at an even generation).  Object: the left end of objects/beam-5f.json with 6 units of its rake train (one
generation after the stored phase, so the train reads bfbfbf), then m units of bare wire C, then the cap; m = 4 and 5
(both parities of arrival).  Stepped with sg.step_set until the state repeats or `gens` generations pass.
Reported: counts by (final period, whether the left end is still emitting: the cells of units < 0 change with
period 4), and every case with a final period above 4.  Period 4 with the gun alive = the cap has become a standing
absorber: another beam oscillator.  Nothing here is a verdict of the oracle."""
import argparse, json, sys
from collections import Counter
import sg, scat
from clocks import period
tr = scat.tr; unit = scat.unit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table'); ap.add_argument('--max', type=int, default=10 ** 9); ap.add_argument('--gens', type=int, default=800)
    ap.add_argument('--out')
    a = ap.parse_args()
    ob = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'beam-5f.json')))
    T = lambda k: [tuple(c) for c in ob[k]]
    left, b = T('left'), [T('b0'), T('b1')]
    UNIT = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]
    s = set(left)
    for k in range(40):
        s |= {tr(c, k) for c in b[k % 2]}
    s1 = sg.step_set(frozenset(s))
    head = frozenset(c for c in s1 if unit(c) < 6)              # left end + 6 units of train, even generation
    D = json.load(open(a.table)); tally = Counter(); out = []
    for sid, st in list(D['states'].items())[:a.max]:
        cap = [tuple(c) for c in st]
        if not cap:
            continue
        for m in (4, 5):
            cells = head | frozenset(tr(c, k) for c in UNIT for k in range(6, 6 + m)) | frozenset(tr(c, 6 + m) for c in cap)
            p, t0 = period(cells, a.gens)
            x = frozenset(cells)
            for _ in range(t0):
                x = sg.step_set(x)
            g0 = frozenset(c for c in x if unit(c) < 0); y = x; alive = False
            if p:
                for _ in range(2):
                    y = sg.step_set(y)
                alive = p % 4 == 0 and frozenset(c for c in y if unit(c) < 0) != g0
            key = (p if p <= 4 else '>4', 'gun alive' if alive else 'gun dead')
            tally[key] += 1
            if p > 4 or (p == 4 and alive) or p == 0:
                out.append(dict(state=sid, m=m, period=p, from_=t0, alive=alive, ncells=len(x)))
                print(f'state {sid} m={m}: period {p} from generation {t0}, {len(x)} cells, gun {"alive" if alive else "dead"}', flush=True)
    print(a.table, {str(k): v for k, v in sorted(tally.items(), key=str)})
    if a.out:
        json.dump(out, open(a.out, 'w'))


if __name__ == '__main__':
    main()
