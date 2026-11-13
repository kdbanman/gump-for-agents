#!/usr/bin/env python3
"""Checks for the threshold lemma (research/theory/PROGRAM.md, node S5), from the rule text alone:
1. every catalogued object of period >= 3 has, at some phase, a cell with >= 6 live neighbours;
2. the uncapped rule B4+/S3+ on random soups in octahedral hulls always reaches period <= 2, and how fast.
   python3 research/theory/check_threshold.py   (about a minute)"""
import json, random, itertools, collections
def offs(a):
    b, c = [i for i in range(3) if i != a]; o = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; o.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; o.append(tuple(v))
    return o
OFF = [offs(a) for a in range(3)]
def axis(c): return 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
def counts(S):
    cnt = {}
    for c in S:
        for o in OFF[axis(c)]:
            n = (c[0] + o[0], c[1] + o[1], c[2] + o[2]); cnt[n] = cnt.get(n, 0) + 1
    return cnt
def step(S, cap=True):
    cnt = counts(S)
    if cap: return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in S)), cnt
    return frozenset(c for c, k in cnt.items() if k >= 4 or (k == 3 and c in S)), cnt
def main():
    # 1. catalogue: does every period>=3 object have an overcrowded cell (>=6 live neighbours) at some phase?
    cat = [json.loads(l) for l in open('research/atlas/catalogue.jsonl')]
    res = collections.Counter()
    for o in cat:
        S = frozenset(tuple(c) for c in o['cells']); P = o['period']; over = False
        for t in range(P):
            S2, cnt = step(S)
            if any(k >= 6 for k in cnt.values()): over = True
            S = S2
        res[('period>=3' if P >= 3 else f'period {P}', 'overcrowded' if over else 'never overcrowded')] += 1
    for k, v in sorted(res.items()): print(k, v)
    # 2. uncapped rule B4+/S3+ on soups in an octahedral hull: period <= 2 always? transient?
    D = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
    for R in (7, 11):
        hull = [c for c in itertools.product(range(-R - 1, R + 2), repeat=3)
                if sum(x & 1 for x in c) == 1 and all(abs(sum(d[i] * c[i] for i in range(3))) <= R for d in D)]
        per = collections.Counter(); tr = []
        for s in range(40):
            rng = random.Random(s); S = frozenset(c for c in hull if rng.random() < rng.choice((0.2, 0.35, 0.5, 0.7)))
            hist = [S]
            for t in range(1, 400):
                S, _ = step(S, cap=False); hist.append(S)
                if t >= 2 and hist[t] == hist[t - 2]:
                    per[1 if hist[t] == hist[t - 1] else 2] += 1; tr.append(t - 2); break
            else: per['>2 or no convergence in 400'] += 1
        print(f"uncapped, R={R} ({len(hull)} cells): final periods {dict(per)}, transient max {max(tr)}, mean {sum(tr)/len(tr):.1f}")

if __name__ == '__main__':
    main()
