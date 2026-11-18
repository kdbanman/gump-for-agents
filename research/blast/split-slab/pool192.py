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


def ancestry(pattern):
    a = []
    for f in sorted(glob.glob(os.path.join(HERE, 'data', pattern))):
        for l in open(f):
            if l.startswith('REP') and ' anc ' in l:
                t = l.split(); a.append((float(t[t.index('lntau') + 1]), int(t[t.index('anc') + 1]), float(t[t.index('eff') + 1]), float(t[t.index('top') + 1])))
    return a


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
    sets.append(('16,384 chains (32 sweeps)', rates(f'sub16k_{tag}_s*.txt')))
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

print()
print('**Replications of 16,384 chains: value and ancestry of the dying chains of each** (distinct ancestors = fresh chains that have descendants among the dying chains of the final ensemble; effective number = inverse Simpson index of the family sizes; top = share of the largest family).')
print()
print('| torus | replication | ln tau | distinct ancestors | effective number | share of the largest family |')
print('|---|---:|---:|---:|---:|---:|')
for L in ((1, 30, 64), (8, 0, 8)):
    a = ancestry('sub16k_%d_%d_%d_s*.txt' % L)
    for i, (lt, anc, eff, top) in enumerate(a):
        print(f'| ({L[0]},{L[1]}),(0,{L[2]}) | {i} | {lt:.2f} | {anc} | {eff:.1f} | {top:.2f} |')
    if a:
        n = len(a)
        print(f'| ({L[0]},{L[1]}),(0,{L[2]}) | mean of {n} | | {sum(x[1] for x in a) / n:.1f} | {sum(x[2] for x in a) / n:.1f} | {sum(x[3] for x in a) / n:.2f} |')
t, w = res.get(((1, 30, 64), '16,384 chains (32 sweeps)')), res.get(((8, 0, 8), '16,384 chains (32 sweeps)'))
if t and w:
    print(f'\n16,384 chains: wide - tube = {w["lt"] - t["lt"]:.3f} ± {math.hypot(w["se"], t["se"]):.3f} (lognormal ± {math.hypot(w["lnse"], t["lnse"]):.3f}); wide - line 40.07 = {w["lt"] - 40.07:+.3f} ± {max(w["se"], w["lnse"]):.3f}')

print()
print('**Sensitivity to the largest replication, and the combination I would defend.** Per set: share of the summed rate carried by the largest replication; ln tau without it. Combination: the three sets weighted by 1/e^2, e = the larger of the scatter error and the lognormal error; error inflated by sqrt(chi2/dof) if that exceeds 1.')
print()
print('| torus | set | n | ln tau ± e | largest replication carries | ln tau without it | lognormal-model estimate: mean(ln tau_i) - s^2/2 |')
print('|---|---|---:|---|---:|---:|---|')
comb = {}
for L in ((1, 30, 64), (8, 0, 8)):
    tag = '%d_%d_%d' % L; vals = []
    for name, pat in (('4,096 chains, 32 sweeps', f'sub_{tag}_s*.txt'), ('4,096 chains, 64 sweeps', f'subx2_{tag}_s*.txt'), ('16,384 chains, 32 sweeps', f'sub16k_{tag}_s*.txt')):
        r = rates(pat)
        if len(r) < 3:
            continue
        st = stat(r); e = max(st['se'], st['lnse']); top = max(r) / sum(r); r2 = sorted(r)[:-1]
        ln = [-math.log(x) for x in r]; mu = sum(ln) / len(ln); s2 = sum((x - mu) ** 2 for x in ln) / (len(ln) - 1)
        print(f'| ({L[0]},{L[1]}),(0,{L[2]}) | {name} | {len(r)} | {st["lt"]:.3f} ± {e:.3f} | {top:.2f} | {-math.log(sum(r2) / len(r2)):.3f} | {mu - s2 / 2:.3f} ± {math.sqrt(s2 / len(r) + s2 * s2 / (2 * (len(r) - 1))):.3f} |')
        vals.append((st['lt'], e))
    w = [1 / e ** 2 for _, e in vals]; m = sum(wi * v for wi, (v, _) in zip(w, vals)) / sum(w); err = 1 / math.sqrt(sum(w))
    chi = sum(((v - m) / e) ** 2 for v, e in vals); dof = max(1, len(vals) - 1); infl = max(1.0, math.sqrt(chi / dof))
    comb[L] = (m, err * infl)
    print(f'| ({L[0]},{L[1]}),(0,{L[2]}) | **combined** | | **{m:.3f} ± {err * infl:.3f}** (chi2 {chi:.1f} on {dof}) | | | |')
if len(comb) == 2:
    t, w = comb[(1, 30, 64)], comb[(8, 0, 8)]; d, de = 0.041, 0.021
    print(f'\ncombined, dice chain: tube {t[0]:.3f} ± {t[1]:.3f}; wide {w[0]:.3f} ± {w[1]:.3f}; wide - tube = {w[0] - t[0]:.3f} ± {math.hypot(t[1], w[1]):.3f}')
    print(f'minus the calibrated offset of the chain and sampler against gump (+{d} ± {de}, anchors of 63 to 108 cells): tube {t[0] - d:.3f} ± {math.hypot(t[1], de):.3f}; wide {w[0] - d:.3f} ± {math.hypot(w[1], de):.3f} (wide line 40.07: {w[0] - d - 40.07:+.3f}); not included: a drift of the offset beyond 108 cells, bounded only to +0.17 ± 0.25 at 192 cells')
