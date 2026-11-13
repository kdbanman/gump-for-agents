#!/usr/bin/env python3
"""Twist and compound statistics of the clockwork box census, with a stepper written from the rule text
(independent of research/clockwork/*.py). For every object of research/scratch/clockwork/census_3_objects.json
(written by `research/clockwork/box_census.py report 3`): period P, quotient length L (first return to a symmetric
image of phase 0), twist m = P/L, and whether any cell has the full period (if none: a compound of sub-clocks).

  python3 research/experiments/census_twist.py
"""
import json, collections, itertools
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
def axis(c): return [i for i in range(3) if c[i] % 2][0]
def step(S):
    cnt = {}
    for c in S:
        for o in OFF[axis(c)]:
            n = (c[0] + o[0], c[1] + o[1], c[2] + o[2]); cnt[n] = cnt.get(n, 0) + 1
    return frozenset(c for c, k in cnt.items() if (k in (4, 5) and c not in S) or (k in (3, 4, 5) and c in S))
SYM = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def match(A, B):
    """is B a rotated/reflected and translated copy of A?"""
    mb = tuple(min(c[i] for c in B) for i in range(3))
    for p, s in SYM:
        X = [tuple(s[i] * c[p[i]] for i in range(3)) for c in A]; mx = tuple(min(c[i] for c in X) for i in range(3))
        if frozenset(tuple(c[i] + mb[i] - mx[i] for i in range(3)) for c in X) == B: return True
    return False
d = json.load(open('research/scratch/clockwork/census_3_objects.json'))
rows = []
for k, meta in d.items():
    x0 = frozenset(tuple(map(int, t.split(','))) for t in k.split())
    orb = [x0]
    while True:
        y = step(orb[-1])
        if y == x0: break
        orb.append(y)
        assert len(orb) < 300
    P = len(orb); assert P == meta['period']
    L = P
    for j in range(1, P):
        if P % j == 0 and len(orb[j]) == len(x0) and match(x0, orb[j]): L = j; break
    U = frozenset().union(*orb)
    full = False
    for c in U:
        seq = [c in s for s in orb]
        if not any(all(seq[i] == seq[(i + q) % P] for i in range(P)) for q in range(1, P) if P % q == 0): full = True; break
    rows.append((P, P // L, full, meta.get('id'), meta['hits']))
print(len(rows), "objects; non-trivial (some cell has the full period):", sum(r[2] for r in rows))
nt = [r for r in rows if r[2]]
print("m distribution (non-trivial):", collections.Counter(r[1] for r in nt))
for thr in (3, 5, 7, 9, 12, 16, 20, 24):
    u = sum(1 for P, m, f, i, h in nt if m == 1 and P >= thr); t = sum(1 for P, m, f, i, h in nt if m > 1 and P // m >= thr)
    print("L>=%d: untwisted %d twisted %d frac %.3f" % (thr, u, t, t / (u + t)))
byL = collections.defaultdict(lambda: [0, 0])
for P, m, f, i, h in nt: byL[P // m][m > 1] += 1
print("L: [untw, tw] for L>=14:", {L: v for L, v in sorted(byL.items()) if L >= 14})
byP = collections.defaultdict(lambda: [0, 0, 0])
for P, m, f, i, h in rows:
    byP[P][0 if not f else (2 if m > 1 else 1)] += 1
print("period: [trivial, untwisted, twisted]", {P: v for P, v in sorted(byP.items())})
