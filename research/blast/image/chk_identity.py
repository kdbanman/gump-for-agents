#!/usr/bin/env python3
"""Brute-force check of the seam identity on a small deterministic CA (blast/image README, "The identity").

Ring of L cells (the "torus") and ring of K L cells (its cover), elementary CA `RULE`, soup of density p, T steps.
Seam slice s = the T+1-generation history of two adjacent cells (0, 1); its image on the cover: cells (L, L+1).
Claim: P_T(history of the strip 0..L-1) / P_c(history of the strip 0..L-1, and history of (L, L+1) = history of (0, 1))
depends on the strip history only through s.  (For K -> infinity the ratio is 1 / (pi(s) Z).)

    python3 research/blast/image/chk_identity.py        # prints the largest relative spread of the ratio within a seam class
"""
import itertools, sys
from collections import defaultdict


def run(x, rule, T):
    n = len(x); h = [tuple(x)]
    for _ in range(T):
        x = tuple((rule >> (4 * x[(i - 1) % n] + 2 * x[i] + x[(i + 1) % n])) & 1 for i in range(n))
        h.append(x)
    return h


def test(rule, L, K, T, p=0.4, SW=2):
    PT = defaultdict(float); PC = defaultdict(float)
    for x in itertools.product((0, 1), repeat=L):
        h = run(x, rule, T); w = p ** sum(x) * (1 - p) ** (L - sum(x))
        PT[tuple(r[:L] for r in h)] += w
    for x in itertools.product((0, 1), repeat=K * L):
        h = run(x, rule, T); w = p ** sum(x) * (1 - p) ** (K * L - sum(x))
        if all(r[L:L + SW] == r[0:SW] for r in h):
            PC[tuple(r[:L] for r in h)] += w
    cls = defaultdict(list); only = 0
    for s, w in PC.items():
        if s in PT:
            cls[tuple(r[:SW] for r in s)].append(PT[s] / w)
        else:
            only += 1
    miss = sum(1 for s in PT if s not in PC)
    spread = max((max(v) - min(v)) / max(v) for v in cls.values())
    multi = sum(1 for v in cls.values() if len(v) > 1)
    print(f'rule {rule} L={L} K={K} T={T}: {len(PT)} strip histories on the torus, {len(PC)} on the cover with the seam recurring; '
          f'in one and not the other: {miss}, {only}; seam classes {len(cls)} ({multi} with more than one strip history); '
          f'largest relative spread of P_T / P_c within a class: {spread:.2e}')
    return spread < 1e-9 and miss == 0


ok = all([test(110, 5, 2, 2), test(30, 6, 2, 3), test(22, 5, 3, 2), test(30, 4, 3, 3)])
print('negative control (a seam one cell thick is not a separator: the ratio must NOT be constant):')
ok = ok and not test(110, 5, 2, 2, SW=1)
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
