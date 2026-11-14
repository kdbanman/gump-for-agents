#!/usr/bin/env python3
"""Independent brute force of theorems.md Theorem B (the toy's edge game).  Shares no code with game_check.py.

Game (from Lemma A, re-derived here from the rule): from live set S on the ring Z_L the next live set S' can be any set
with F(S) <= S' <= S | N(S), F = live cells with exactly two live among x+-1, x+-2, N = dead cells with at least one.
The rule table behind it is checked first: for every (state, k, b) the toy's next state, and which (state, k) are
forced.  Then min number of generations to empty every configuration, L = 5..13.
  python3 gamecheck.py 13
"""
import sys


def rule_table():
    forced = {}
    for x in (0, 1):
        for k in range(5):
            outs = {1 if ((x and 2 <= k + b <= 4) or (not x and 3 <= k + b <= 4)) else 0 for b in (0, 1, 2)}
            forced[(x, k)] = outs
    assert forced[(1, 2)] == {1} and forced[(0, 0)] == {0}
    assert all(len(v) == 2 for key, v in forced.items() if key not in ((1, 2), (0, 0)))
    return forced


def main(Lmax):
    rule_table()
    print('Lemma A table: live k=2 forced alive, dead k=0 forced dead, all other 8 cases free: OK')
    for L in range(5, Lmax + 1):
        full = (1 << L) - 1
        rot = lambda v, s: ((v << s) | (v >> (L - s))) & full if s > 0 else ((v >> -s) | (v << (L + s))) & full
        F = [0] * (1 << L); U = [0] * (1 << L)
        for S in range(1 << L):
            f = n = 0
            for x in range(L):
                k = sum((S >> ((x + d) % L)) & 1 for d in (1, -1, 2, -2))
                if (S >> x) & 1:
                    if k == 2:
                        f |= 1 << x
                elif k >= 1:
                    n |= 1 << x
            F[S] = f; U[S] = S | n
        INF = 99
        steps = [INF] * (1 << L); steps[0] = 0
        for level in range(1, 5):
            new = []
            for S in range(1, 1 << L):
                if steps[S] < INF:
                    continue
                f, free = F[S], U[S] & ~F[S]
                sub = free; ok = False
                while True:
                    if steps[f | sub] == level - 1:
                        ok = True; break
                    if sub == 0:
                        break
                    sub = (sub - 1) & free
                if ok:
                    new.append(S)
            for S in new:
                steps[S] = level
        cnt = {}
        for S in range(1, 1 << L):
            cnt[steps[S]] = cnt.get(steps[S], 0) + 1
        three = [S for S in range(1, 1 << L) if steps[S] == 3]
        triples = {((0b111 << i) | (0b111 >> (L - i))) & full for i in range(L)}
        print('L = %2d: emptied in 1/2/3/more generations: %s; needing 3 = rotations of the lone triple: %s' %
              (L, ' '.join('%d' % cnt.get(i, 0) for i in (1, 2, 3, INF)), set(three) == triples if L >= 9 else '-'))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
