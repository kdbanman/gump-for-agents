#!/usr/bin/env python3
"""unzip8 (push 8): every one-cell change at a stretch of wire B' in wire B, and what releases its count.

    python3 unzip8.py census [--k 3]       every cell of the 5 x 5 tube on the units from 3 left of the stretch to 3 right
                                           of its edge, flipped at phase 0 and at phase 1; outcome 100 generations later
    python3 unzip8.py law [--K 40]         the products of the clean triggers as a function of the stretch length k
    python3 unzip8.py catch [--K 12]       a second stretch (d f) 20 units to the left catches the pulses of the count read

Background: capL + 7^60 + d^k f + 7^60 + capR (exp8.line), a finite object; nothing reaches a cap within the run.
Outcome classes of the census (the wire read as hex letters at generation 100 or 101, an even number later than the flip):
  healed          the background
  count +1        the stretch one unit longer, nothing else (a pulse was made and absorbed)
  count -1        the stretch one unit shorter, nothing else
  pulse away      the stretch as it was, one pulse leaving
  released <-     the stretch gone, a train of family units leaving to the left (the train is given)
  released ->     the same to the right
  standing        a standing change at the stretch (not a family word, or a different word), nothing leaving
  other           anything else (fronts, fire)
"""
import sys, os, re, argparse
from collections import Counter, defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X, signals8 as S
from lab8 import tr

NL = NR = 60


def outcome(k, flips, g0):
    """flip at generation g0, read at generation 100: (hex letters of the wire, whether the state has period dividing 4)"""
    mid = 'd' * k + 'f'
    obj, N = X.line(mid, NL, NR); L = X.lab_for(N); a = L.arr(obj); L.run(a, g0)
    L.flip(a, flips); L.run(a, 100 - g0)
    b = a.copy(); L.run(b, 4)
    return X.hexletters(L, a, 4, 4 + N), np.array_equal(a, b)


def classify(k, s, still):
    if s == '7' * NL + 'd' * k + 'f' + '7' * NR:
        return 'healed'
    if still:
        m = re.fullmatch(r'(7*)(d+)f(7*)', s)
        if m:
            return 'count %+d' % (len(m.group(2)) - k)
        core = s.strip('7')
        return 'standing' if len(core) <= k + 10 else 'other'
    left, mid, right = s[:NL - 3].strip('7'), s[NL - 3:NL + k + 4].strip('7'), s[NL + k + 4:].strip('7')
    if any(ch in left + mid + right for ch in '?_'):
        return 'other'
    if bool(left) == bool(right):
        return 'other'
    side, prod = ('<-', left) if left else ('->', right)
    if mid == '':
        return f'released {side} {X.hexrle(prod)}'
    m = re.fullmatch(r'(d+)f', mid)
    if m:
        dk = len(m.group(1)) - k
        return ('pulse away' if dk == 0 else 'count %+d and a train' % dk) + f' {side} {X.hexrle(prod)}'
    return 'other'


def census(k):
    w0 = 4 + NL; e = w0 + k
    rows = []
    for g0 in (0, 1):
        for u in range(w0 - 3, e + 4):
            for c in S.E5:
                s, still = outcome(k, [tr(c, u)], g0)
                rows.append((u - w0, c, g0, classify(k, s, still), s))
    cnt = Counter(r[3] for r in rows); ex = defaultdict(list)
    for r in rows:
        ex[r[3]].append(r[:3])
    print(f'stretch d^{k} f in wire B: {len(rows)} one-cell events (units -3..{k + 3} relative to its first unit, 38 cells, 2 phases)')
    for key, v in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f'  {v:4d}  {key:44s} e.g. unit {ex[key][0][0]:+d}, cell {ex[key][0][1]}, phase {ex[key][0][2]}')
    return rows


TRIGGERS = [  # (name, unit relative to the stretch's first unit, cell, phase)
    ('stator (0,1,2) of the unit before the stretch, phase 0', -1, (0, 1, 2), 0),
    ('site (1,0,2) of the unit before the stretch, phase 0', -1, (1, 0, 2), 0),
    ('stator (0,1,4) of the unit before the stretch, phase 1', -1, (0, 1, 4), 1),
    ('(0,2,3) added to the unit before the stretch, phase 0', -1, (0, 2, 3), 0),
    ('stator (0,1,4) of the unit before the stretch, phase 0', -1, (0, 1, 4), 0),
    ('site (1,0,4) of the unit before the stretch, phase 0', -1, (1, 0, 4), 0),
    ('(0,2,3) of the first unit of the stretch, phase 0', 0, (0, 2, 3), 0),
    ('(1,4,2) born beside the unit before the stretch (outside the 3 x 3 tube), phase 0', -1, (1, 4, 2), 0),
]


def law(K):
    w0 = 4 + NL
    for name, u, c, g0 in TRIGGERS:
        prods = []
        for k in range(1, K + 1):
            G = 4 * k + 100 + (g0 % 2)
            mid = 'd' * k + 'f'
            obj, N = X.line(mid, NL + 2 * K, NR); L = X.lab_for(N); a = L.arr(obj); L.run(a, g0)
            L.flip(a, [tr(c, 4 + NL + 2 * K + u)]); L.run(a, G)
            prods.append(X.hexletters(L, a, 4, 4 + N).strip('7'))
        forms = [('(b7)^k', lambda k: ('b7' * k)[:-1]), ('(b7)^(k-1)', lambda k: ('b7' * (k - 1))[:-1]), ('b5f(9f)^k', lambda k: 'b5f' + '9f' * k),
                 ('b5f(9f)^(k+1)', lambda k: 'b5f' + '9f' * (k + 1)), ('b^(2k+2)', lambda k: 'b' * (2 * k + 2)), ('b^(2k)', lambda k: 'b' * (2 * k))]
        hit = [fn for fn, f in forms if all(prods[k - 1] == f(k) for k in range(1, K + 1))]
        print(f"  {name}: k = 1..{K}: " + (f'exactly {hit[0]} leaving to the left, the wire plain behind it' if hit else 'no single form: ' + ', '.join(X.hexrle(p) for p in prods[:4])))


def catch(K):
    for k in range(1, K + 1):
        word = '7' * 10 + 'df' + '7' * 20 + 'd' * k + 'f' + '7' * 10
        obj, N = X.cell(word, 0, 0); L = X.lab_for(N); a = L.arr(obj)
        L.flip(a, [tr(X.RIGHT, 4 + 10 + 2 + 20 - 1)]); L.run(a, 200 + 4 * k)
        want, _ = X.cell('7' * 10 + 'd' * (k + 1) + 'f' + '7' * (N - 12 - k), 0, 0)
        print(f'  store {k}, receiver 1: after the count read the receiver holds {k + 1} and the store is gone: {L.cells(a) == want}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('what', choices=['census', 'law', 'catch'])
    ap.add_argument('--k', type=int, default=3); ap.add_argument('--K', type=int, default=40)
    a = ap.parse_args()
    if a.what == 'census':
        census(a.k)
    elif a.what == 'law':
        law(a.K)
    else:
        catch(min(a.K, 12))
