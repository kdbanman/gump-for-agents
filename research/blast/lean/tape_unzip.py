#!/usr/bin/env python3
"""Checks with reference/oracle.py that the word W k n of Gump/UnzipProof.lean is the store wire after push 8's count
read at generation 2n, for k = 1 .. 10 and every n from 1 to k + 5 (whole state, on the units of a finite piece that
its ends cannot reach). The Lean proof does not need this (its base runs are kernel-checked); it is the tie of the
formula to the ground truth, and what suggested the proof.

    python3 research/blast/lean/tape_unzip.py        (a few minutes)
"""
import sys
from tape_lib import orbit_box, tr, units

ST = [(0, 1, 2), (0, 1, 4)]
SI = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
hexc = lambda h: set(ST) | {SI[j] for j in range(4) if h >> j & 1}


def hcfg(word, lo, hi):
    return frozenset(tr(c, u) for u in range(lo, hi + 1) for c in hexc(word(u)))


def W(k, n, u):                      # Gump.Unzip.W, branch by branch
    if n == 1:
        return 5 if u == -1 else (13 if 0 <= u < k else (15 if u == k else 7))
    if n <= k + 1:
        if u <= n - 4:
            return 11 if (2 - n <= u and (u - (2 - n)) % 2 == 0) else 7
        if u == n - 3: return 15
        if u == n - 2: return 9
        if u < k: return 13
        return 15 if u == k else 7
    if n == k + 2:
        if u <= k - 2:
            return 11 if (-k <= u and (u + k) % 2 == 0) else 7
        return 15 if u == k - 1 else 7
    return 11 if (2 - n <= u < 2 - n + 2 * k and (u - (2 - n)) % 2 == 0) else 7


ok = True
for k in range(1, 11):
    T = 2 * (k + 5)
    lo, hi = -T - k - 12, k + T + 8
    s0 = hcfg(lambda u: 13 if 0 <= u < k else (15 if u == k else 7), lo, hi) - {(-2, 1, 4)}
    o = orbit_box(s0, T)
    a, b = lo + T, hi - T
    good = all(units(o[2 * n], a, b) == hcfg(lambda u: W(k, n, u), a, b) for n in range(1, T // 2 + 1))
    ok &= good
    print(('PASS' if good else 'FAIL'), f'k = {k}: generation 2n is the word W k n for n = 1 .. {T // 2} (units {a} .. {b})', flush=True)
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
