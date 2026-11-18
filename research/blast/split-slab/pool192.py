#!/usr/bin/env python3
"""The 192-cell tube and wide torus: default sweeps (data/sub_*), doubled sweeps (data/subx2_*), pooled; honest errors.

    python3 pool192.py

Per set: n replications, -ln(mean rate), standard error from the scatter, a bootstrap 16-84% interval of
-ln(mean rate) over replications, the sd of ln(rate) between replications and the standard error a lognormal of
that width would give (the sample scatter misses the upper tail when n is small).
"""
import glob, math, os, random, re
HERE = os.path.dirname(os.path.abspath(__file__))


def rates(pattern):
    r = []
    for f in sorted(glob.glob(os.path.join(HERE, 'data', pattern))):
        r += [float(l.split('rate')[1].split()[0]) for l in open(f) if l.startswith('REP') and 'rate' in l]
    return r


def stat(r, rng=random.Random(7)):
    n = len(r); m = sum(r) / n; sd = math.sqrt(sum((x - m) ** 2 for x in r) / (n - 1))
    ln = [-math.log(x) for x in r if x > 0]; mu = sum(ln) / len(ln); s2 = sum((x - mu) ** 2 for x in ln) / (len(ln) - 1)
    bs = sorted(-math.log(sum(rng.choice(r) for _ in range(n)) / n) for _ in range(4000))
    return dict(n=n, lt=-math.log(m), se=sd / m / math.sqrt(n), lo=bs[int(0.16 * 4000)], hi=bs[int(0.84 * 4000)], logsd=math.sqrt(s2),
                lnse=math.sqrt((math.exp(s2) - 1) / n), med=sorted(ln)[len(ln) // 2], ext=sum(x == 0 for x in r))


FORMS = {(1, 30, 64): 'tube forms: 39.17 (K = 1), 39.01 (K = 2), 38.92 (K = 3), 38.86 (power law)', (8, 0, 8): 'wide-face line: 40.07'}
print('| torus | sweeps | replications | ln tau (dice chain) | bootstrap 16-84% | sd of ln(rate) between replications | error for a lognormal of that width | median replication |')
print('|---|---|---:|---|---|---:|---:|---:|')
res = {}
for L in ((1, 30, 64), (8, 0, 8)):
    tag = '%d_%d_%d' % L
    sets = [('default (32)', rates(f'sub_{tag}_s*.txt')), ('doubled (64)', rates(f'subx2_{tag}_s*.txt'))]
    sets.append(('pooled', sets[0][1] + sets[1][1]))
    for name, r in sets:
        if len(r) < 2:
            continue
        s = stat(r); res[(L, name)] = s
        print(f'| ({L[0]},{L[1]}),(0,{L[2]}) | {name} | {s["n"]} | {s["lt"]:.3f} ± {s["se"]:.3f} | {s["lo"]:.2f} .. {s["hi"]:.2f} | {s["logsd"]:.2f} | {s["lnse"]:.3f} | {s["med"]:.2f} |')
print()
for L in ((1, 30, 64), (8, 0, 8)):
    a, b = res.get((L, 'default (32)')), res.get((L, 'doubled (64)'))
    if a and b:
        print(f'({L[0]},{L[1]}),(0,{L[2]}): doubled - default = {b["lt"] - a["lt"]:+.3f} ± {math.hypot(a["se"], b["se"]):.3f} (lognormal errors: ± {math.hypot(a["lnse"], b["lnse"]):.3f}); {FORMS[L]}')
t, w = res.get(((1, 30, 64), 'pooled')), res.get(((8, 0, 8), 'pooled'))
if t and w:
    print(f'pooled: wide - tube = {w["lt"] - t["lt"]:.3f} ± {math.hypot(w["se"], t["se"]):.3f} (lognormal ± {math.hypot(w["lnse"], t["lnse"]):.3f})')
for key in ('doubled (64)',):
    t, w = res.get(((1, 30, 64), key)), res.get(((8, 0, 8), key))
    if t and w:
        print(f'{key}: wide - tube = {w["lt"] - t["lt"]:.3f} ± {math.hypot(w["se"], t["se"]):.3f} (lognormal ± {math.hypot(w["lnse"], t["lnse"]):.3f})')
