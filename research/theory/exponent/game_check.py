"""Brute-force check of the three-step lemma (exponent.md, Theorem B).

The toy's edge row with the two rows beneath chosen freely ("adversary"): from the live set S the next live set may be
any S' with F(S) <= S' <= S u N(S), where F(S) = live cells with exactly two live in-row neighbours (they survive
whatever lies below) and N(S) = dead cells with at least one live in-row neighbour (in-row neighbours: x+-1, x+-2).
Claim: on every ring of length L >= 5 every S can be emptied in <= 3 steps, and some S need 3.
Also checks the one-cell transition table against the rule itself.     python3 game_check.py [Lmax]"""
import sys
from itertools import product
Lmax = int(sys.argv[1]) if len(sys.argv) > 1 else 13
# 1. the table: outcomes reachable by choosing b in {0,1,2}
for x in (0, 1):
    for k in range(5):
        outs = {int((n := k + b) <= 4 and n + x >= 3) for b in range(3)}
        forced = (x == 1 and k == 2) or (x == 0 and k == 0)
        assert (len(outs) == 1) == forced, (x, k, outs)
        if forced: assert outs == {x}
print('table ok: forced outcomes are exactly (live, k=2) -> live and (dead, k=0) -> dead')
for L in range(5, Lmax + 1):
    full = (1 << L) - 1
    def kcount(S, x):
        return sum((S >> ((x + d) % L)) & 1 for d in (1, 2, -1, -2))
    FS = [0] * (1 << L); UP = [0] * (1 << L)
    for S in range(1 << L):
        f = 0; u = S
        for x in range(L):
            k = kcount(S, x)
            if (S >> x) & 1:
                if k == 2: f |= 1 << x
            elif k >= 1: u |= 1 << x
        FS[S] = f; UP[S] = u
    d = [None] * (1 << L); d[0] = 0
    one = [S for S in range(1, 1 << L) if FS[S] == 0]
    for S in one: d[S] = 1
    ok1 = set(one) | {0}
    # two steps: exists S' in [F(S), UP(S)] with F(S') = 0  (enumerate supersets of F within UP)
    two = set()
    for S in range(1, 1 << L):
        if d[S] is not None: continue
        free = UP[S] & ~FS[S]; sub = free
        while True:
            if FS[FS[S] | sub] == 0: d[S] = 2; two.add(S); break
            if sub == 0: break
            sub = (sub - 1) & free
    worst = 0; bad = 0
    for S in range(1, 1 << L):
        if d[S] is not None: worst = max(worst, d[S]); continue
        # three steps via the explicit strategy of the proof: S' = UP(S) (everything within distance 2 alive)
        Sp = UP[S]
        S2 = FS[Sp]
        if FS[S2] == 0: d[S] = 3; worst = 3
        else: bad += 1
    n3 = sum(1 for v in d if v == 3)
    print('L=%2d: states needing 1/2/3 steps: %d / %d / %d   strategy failures: %d   max = %d' % (L, len(one), len(two), n3, bad, worst))
