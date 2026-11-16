#!/usr/bin/env python3
"""The class of a rake turn, mod 4: why every shuttle clock so far has period 4N + 2, and how to get 4N.

    python3 turnclass.py TABLE.json [--max M]

A rake f (towards +v) at unit u at an even generation t keeps a = t - 2u constant; the mirror rake 5f (towards -v,
'5' at unit u) keeps b = t + 2u constant.  A cap does not see a (the rake looks the same at every even generation,
the cap is the same at every even generation), so a cap that turns f into 5f has a turn constant
k = b - a  (mod 4)  that is a property of the cap alone, and translating the cap by one unit changes b - a by 4.
Same for a left cap turning 5f into f: k' = a - b (mod 4).  Going round a clock, a advances by its period P, so
P = k + k' (mod 4): a clock of period 0 mod 4 needs a pair of caps whose turn constants differ from clock-C's pair.
This script measures k for every cap state of TABLE.json (scatter_table.py, wire C) used as a right end: a lone
rake f is sent from 24 units away along a clean wire, and the first 5f seen moving away is located; the cap must
be exactly as it was (on its own units) 40 generations after the 5f left.  It also measures k' for capL of the
clock (mirror set-up).  Stepping: sg.step_set (the infinite lattice).
"""
import argparse, json
from collections import Counter
import sg, scat, family as F
tr = scat.tr; unit = scat.unit


def uc(m, u):
    return {tr(c, u) for c in F.STATOR} | {tr(F.SITES[i], u) for i in range(4) if m >> i & 1}


def dec(x, a, b):
    live = {}
    for c in x:
        live.setdefault(unit(c), set()).add(tr(c, -unit(c)))
    o = ''
    for u in range(a, b):
        s = live.get(u, set())
        if s - set(F.STATOR) - set(F.SITES) or not set(F.STATOR) <= s:
            o += '?' if s else '.'
        else:
            o += '%x' % sum(1 << i for i in range(4) if F.SITES[i] in s)
    return o


def right_turn(cap, K=24, far=-90):
    """cap: cells, its first unit at K.  Rake f at unit 0, generation 0.  Returns (k mod 4, restored) or None."""
    base = frozenset(c for u in range(far, K) for c in uc(0xb, u)) | cap
    near = lambda s: frozenset(c for c in s if unit(c) >= K - 2)
    if near(sg.step_set(sg.step_set(base))) != near(base):
        return 'not stationary'
    x = base ^ uc(0xb, 0) ^ uc(0xf, 0)
    a = 0
    for t in range(2, 4 * K + 60, 2):
        x = sg.step_set(sg.step_set(x))
        d = dec(x, -40, K)
        i = d.rfind('5f')
        if i >= 0 and i + (-40) < K - 6:
            u = i - 40
            # confirm it moves: two generations later one unit nearer -v
            y = sg.step_set(sg.step_set(x))
            if dec(y, -40, K)[i - 1:i + 1] != '5f':
                continue
            z = y
            for _ in range(20):
                z = sg.step_set(sg.step_set(z))
            restored = near(z) == near(base)
            return ((t + 2 * u - a) % 4, restored, t)
    return 'no turn'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table', nargs='*'); ap.add_argument('--max', type=int, default=10 ** 9)
    a = ap.parse_args()
    ck = json.load(open('objects/clock-C.json'))
    capR = frozenset(map(tuple, ck['capR']))
    print('clock-C capR:', right_turn(frozenset(tr(c, 24) for c in capR)))
    for tab in a.table:
        D = json.load(open(tab)); tally = Counter(); ex = {}
        for sid, st in list(D['states'].items())[:a.max]:
            cap = frozenset(map(tuple, st))
            if not cap:
                continue
            u0 = min(unit(c) for c in cap)
            r = right_turn(frozenset(tr(c, 24 - u0) for c in cap))
            key = r if isinstance(r, str) else ('k=%d' % r[0], 'restored' if r[1] else 'changed')
            tally[key] += 1; ex.setdefault(key, sid)
        print(tab, dict(tally)); print('   first example of each:', ex)


if __name__ == '__main__':
    main()
