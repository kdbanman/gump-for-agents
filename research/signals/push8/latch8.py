#!/usr/bin/env python3
"""latch8 (push 8): standing structures beside the stretch, and what an arriving pulse does to each.

    python3 latch8.py [--k 3] [--words 3] [--pairs] [--out F.json]

Background: capL + 7^40 + d^k f + 7^40 + capR.  Candidates: every one-cell flip (5 x 5 tube, both phases) on the 5
units left of the stretch and its first unit; with --pairs every two-cell flip (3 x 3 tube) on the 3 units left of it
and its first unit; with --words K every family word of up to K units ending at the unit before the stretch.  A candidate is
kept if 200 generations later the state is periodic with period dividing 4, differs from the plain background, the
caps are as they were, and the difference from the background lies within 12 units of the stretch's left wall
(a standing structure).  Distinct structures (by state) are then each sent the pulse B from the left, born 20 and 21
units left of the wall, and the state 140 generations later is read as hex letters.
Printed: for each structure, its letters and the outcome for the two pulses; outcomes other than "absorbed, stretch
one unit longer" are flagged.
"""
import sys, os, json, itertools, argparse
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X, signals8 as S
from lab8 import tr


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--k', type=int, default=3); ap.add_argument('--words', type=int, default=0)
    ap.add_argument('--pairs', action='store_true'); ap.add_argument('--out'); ap.add_argument('--side', default='L')
    a = ap.parse_args()
    k = a.k; nL = nR = 40; mid = 'd' * k + 'f'
    obj, N = X.line(mid, nL, nR); L = X.lab_for(N)
    w0 = 4 + nL
    ref = {}
    for g0 in (0, 1):
        r = L.arr(obj); L.run(r, g0); ref[g0] = r.copy()
    r200 = L.arr(obj); L.run(r200, 200)
    events = []
    for g0 in (0, 1):
        for u in range(w0 - 5, w0 + 1):
            for c in S.E5:
                events.append((g0, [tr(c, u)], f'1cell u{u - w0} {c} g{g0}'))
    if a.pairs:
        for g0 in (0, 1):
            cs = [tr(c, u) for u in range(w0 - 3, w0 + 1) for c in S.E3]
            for c1, c2 in itertools.combinations(cs, 2):
                if abs(lab8.unit(c1) - lab8.unit(c2)) <= 2:
                    events.append((g0, [c1, c2], f'2cell {tr(c1, -w0)} {tr(c2, -w0)} g{g0}'))
    if a.words:
        base = '7' * nL
        for K in range(1, a.words + 1):
            for w in itertools.product('0123456789abcdef', repeat=K):
                w = ''.join(w)
                if w[0] == '7':
                    continue
                fl = X.hexword('7' * K, w0 - K) ^ X.hexword(w, w0 - K)
                events.append((0, sorted(fl), f'word {w}'))
    found = {}
    for g0, fl, tag in events:
        s = ref[g0].copy(); L.flip(s, fl); L.run(s, 200 - g0)
        if np.array_equal(s, r200):
            continue
        t = s.copy(); L.run(t, 4)
        if not np.array_equal(s, t):
            continue
        du = X.diff_units(L, s, r200)
        if not du or min(du) < w0 - 12 or max(du) > w0 + k + 12:
            continue
        key = s.tobytes()
        if key not in found:
            found[key] = (s, [tag])
        else:
            found[key][1].append(tag)
    print(f'k = {k}: {len(events)} candidates, {len(found)} distinct standing structures')
    rows = []
    for key, (s, tags) in found.items():
        letters = X.hexletters(L, s, w0 - 8, w0 + k + 5)
        outs = []
        for d in (20, 21):
            x = s.copy(); L.flip(x, X.pulseR(w0 - d)); L.run(x, 140)
            y = x.copy(); L.run(y, 4)
            outs.append((X.hexrle(X.hexletters(L, x, 4, 4 + N)), 'p4' if np.array_equal(x, y) else 'moving'))
        rows.append(dict(letters=letters, tags=tags[:3], ntags=len(tags), outs=outs, cells=int(s.sum())))
    rows.sort(key=lambda r: r['letters'])
    for r in rows:
        print(f"  {r['letters']}  ({r['ntags']} events, e.g. {r['tags'][0]}; {r['cells']} cells)")
        for o in r['outs']:
            print(f'      R pulse -> {o[0]} [{o[1]}]')
    if a.out:
        json.dump(rows, open(a.out, 'w'))


if __name__ == '__main__':
    main()
