#!/usr/bin/env python3
"""site9 (push 9): two pulses that meet at a wall-sensitive site.

    python3 site9.py G.jsonl [G2.jsonl ...]        (output files of wall9.py)

A wall-sensitive site: a (placement, e) of wall9.py's files beside which plain wire stands and passes both pulses
(beside9.py: R pass, L pass) and beside which the stretch d^3 f does not stand (wall9: released without a pulse).
On plain wire a right-going pulse born at unit 29 and a left-going one born at unit 52 stop each other and leave the
mark d f on units 40, 41 (asserted here): a stretch whose wall is where the scan had it.  Here the two pulses are
sent at the site (ring of 60 units, lab8, read after 76 generations; the same classes as wall9.py):
  unchanged     the mark d f stands beside the object
  RELEASE ...   the wire is plain, the object is as it would have been, and pulses leave: the letters are given
  ERASED        the same with no pulse
  other         anything else
Printed: the count of each outcome, the number of distinct objects, and one example per outcome.
"""
import sys, json
from collections import Counter, defaultdict
import numpy as np
import lab9 as Z
from lab9 import tr, X
import wall9
from wall9 import R, W0, T


def meet(orb, m, ua=29, ub=52):
    S0 = [tr(c, m) for c in orb[0]]
    L = Z.box_for([tr(c, m) for o in orb for c in o], R)
    a = L.arr(X.hexword('7' * R, 0)); L.flip(a, S0)
    L.flip(a, X.pulseR(ua)); L.flip(a, X.pulseL(ub))
    L.run(a, T)
    free = L.arr([tr(c, m) for c in orb[T % len(orb)]])
    s = Z.hexring(L, a); same = Z.outside(L, a) == Z.outside(L, free)
    if same and s == '7' * W0 + 'df' + '7' * (R - W0 - 2):
        return 'unchanged'
    if same and not (set(s) - set('7b6f')):
        nb = s.count('b'); n6 = s.count('6')
        return f'RELEASE {X.hexrle(Z.canon_ring(s))}' if nb + n6 else 'ERASED'
    return 'other' + ('' if same else ', object changed') + (' touch' if L.touch else '')


def main():
    L0 = Z.Lab(0, R, -6, 10, -6, 14, ring=True)
    a = L0.arr(X.hexword('7' * R, 0)); L0.flip(a, X.pulseR(29)); L0.flip(a, X.pulseL(52)); L0.run(a, T)
    assert Z.hexring(L0, a) == '7' * W0 + 'df' + '7' * (R - W0 - 2), Z.hexring(L0, a)
    rows = []
    for f in sys.argv[1:]:
        for l in open(f):
            try:
                r = json.loads(l)
            except Exception:
                continue
            rest = r['res'].get('rest', '')
            if (rest.startswith('RELEASE') or rest == 'ERASED') and r['R'] == 'pass' and r['L'] == 'pass':
                rows.append(r)
    c = Counter(); objs = defaultdict(set); ex = {}
    for r in rows:
        orb = Z.orbit([tuple(q) for q in r['cells']], r['P'])
        ob = wall9.Obj(orb)
        try:
            out = meet(orb, W0 - 1 + r['e'] - ob.umax)
        except ValueError:
            out = 'outside box'
        key = (r['res']['rest'].split('  ')[-1], out)
        c[key] += 1; objs[key].add(r['id']); ex.setdefault(key, (r['id'], r['gi'], r['ph'], r['t'], r['e']))
    print(f'{len(rows)} wall-sensitive sites that pass both pulses on plain wire; {len(set(r["id"] for r in rows))} objects')
    for key, n in c.most_common(30):
        print(f'  {n:5d}  d^3 f beside it: {key[0]:12s} two pulses meeting there: {key[1]:28s} {len(objs[key])} objects, e.g. {ex[key]}')


if __name__ == '__main__':
    main()
