#!/usr/bin/env python3
"""Checks with reference/oracle.py the word VW k n of Gump/CallProof.lean: push 9's V_k (the store wire alone, d^k f
on units 1 .. k + 1 with the crossing at unit 0, e1 = (1,2,0) of unit 0 made live at generation 29) at generation
28 + 2n, for k = 1 .. 8 and n = 2 .. k + 6 (whole state on the units a finite piece's ends cannot reach). The crossing
is moved to unit 0; Gump/Call.lean has it at 35 (a translation along the wire).

    python3 research/blast/lean/tape_call_front.py
"""
import sys
from tape_lib import orbit_box, tr, units

ST = [(0, 1, 2), (0, 1, 4)]
SI = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
hexc = lambda h: set(ST) | {SI[j] for j in range(4) if h >> j & 1}


def hcfg(word, lo, hi):
    return frozenset(tr(q, u) for u in range(lo, hi + 1) for q in hexc(word(u)))


def VW(k, n, u):
    if n <= k:
        if u <= n - 3: return 11 if (3 - n <= u and (u - (3 - n)) % 2 == 0) else 7
        if u == n - 2: return 15
        if u == n - 1: return 11
        if u == n: return 9
        if u <= k: return 13
        return 15 if u == k + 1 else 7
    if n == k + 1:
        if u <= k - 2: return 11 if (2 - k <= u and (u - (2 - k)) % 2 == 0) else 7
        if u == k - 1: return 15
        return 11 if u == k else 7
    if n == k + 2:
        if u <= k - 1: return 11 if (1 - k <= u and (u - (1 - k)) % 2 == 0) else 7
        return 15 if u == k else 7
    return 11 if (3 - n <= u < 3 - n + 2 * k and (u - (3 - n)) % 2 == 0) else 7


ok = True
for k in range(1, 9):
    T = 2 * k + 12
    lo, hi = -T - 2 * k - 16, k + T + 10
    store = hcfg(lambda u: 13 if 0 <= u - 1 < k else (15 if u - 1 == k else 7), lo, hi)
    S1 = orbit_box(store, 1)[1]
    V = orbit_box(S1 | {tr((1, 2, 0), 0)}, T)          # V[t] is generation 29 + t
    a, b = lo + T + 2, hi - T - 2
    good = all(units(V[2 * n - 1], a, b) == hcfg(lambda u: VW(k, n, u), a, b) for n in range(2, (T + 1) // 2 + 1))
    ok &= good
    print(('PASS' if good else 'FAIL'), f'k = {k}: generation 28 + 2n is VW k n for n = 2 .. {(T + 1) // 2}', flush=True)
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
