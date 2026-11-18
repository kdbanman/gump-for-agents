#!/usr/bin/env python3
"""Table of the subset sampler's results (data/sub_*.txt) against the gump anchors.   python3 table_sub.py"""
import glob, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ANCH = {(4, 0, 4): (9.9251, 0.0004), (1, 4, 21): (13.1622, 0.0007), (1, 12, 28): (17.3175, 0.0031), (1, 4, 28): (17.5387, 0.0031),
        (1, 17, 32): (19.7446, 0.0042), (1, 16, 36): (22.1599, 0.0086), (6, 0, 6): (22.5405, 0.0074)}
rows = []; pool = {}
for f in sorted(glob.glob(os.path.join(HERE, 'data', 'sub_*_s*.txt'))):
    m = re.match(r'sub_(\d+)_(\d+)_(\d+)_s(\d+).txt', os.path.basename(f)); H, K, D, seed = map(int, m.groups())
    rates = [float(l.split('rate')[1].split()[0]) for l in open(f) if l.startswith('REP') and 'rate' in l]
    if len(rates) < 2:
        continue
    n = len(rates); mean = sum(rates) / n; sd = math.sqrt(sum((r - mean) ** 2 for r in rates) / (n - 1))
    rows.append((3 * H * D, (H, K, D), seed, n, -math.log(mean), sd / mean / math.sqrt(n), sd / mean, sum(r == 0 for r in rates)))
    pool.setdefault((H, K, D), []).extend(rates)
print('| cells | torus | seed | replications | ln tau, dice chain (subset sampler) | rel. sd of one replication | extinct | gump anchor | sampler - anchor |')
print('|---:|---|---:|---:|---|---:|---:|---|---|')
for A, L, seed, n, lt, err, rsd, ext in sorted(rows):
    a = ANCH.get(L)
    print(f'| {A} | ({L[0]},{L[1]}),(0,{L[2]}) | {seed} | {n} | {lt:.3f} ± {err:.3f} | {rsd:.2f} | {ext} | ' +
          (f'{a[0]} ± {a[1]} | {lt - a[0]:+.3f} ± {math.hypot(err, a[1]):.3f} |' if a else '— | — |'))

print()
print('Pooled over seeds (all replications of version 2):')
print()
print('| cells | torus | replications | ln tau, dice chain | gump anchor | dice chain (sampler) - gump |')
print('|---:|---|---:|---|---|---|')
offs = []
res = {}
for L, rates in sorted(pool.items(), key=lambda kv: (3 * kv[0][0] * kv[0][2], kv[0])):
    n = len(rates); mean = sum(rates) / n; sd = math.sqrt(sum((r - mean) ** 2 for r in rates) / (n - 1)); lt = -math.log(mean); err = sd / mean / math.sqrt(n)
    a = ANCH.get(L); res[L] = (lt, err)
    print(f'| {3 * L[0] * L[2]} | ({L[0]},{L[1]}),(0,{L[2]}) | {n} | {lt:.3f} ± {err:.3f} | ' + (f'{a[0]} ± {a[1]} | {lt - a[0]:+.3f} ± {math.hypot(err, a[1]):.3f} |' if a else '— | — |'))
    if a and L in ((1, 12, 28), (1, 17, 32), (1, 16, 36)):
        offs.append((lt - a[0], math.hypot(err, a[1])))
if offs:
    w = [1 / e ** 2 for _, e in offs]; d = sum(wi * o for wi, (o, _) in zip(w, offs)) / sum(w); de = 1 / math.sqrt(sum(w))
    chi = sum(((o - d) / e) ** 2 for o, e in offs)
    print(f'\noffset d = dice chain - gump, weighted mean over the tubes of 84, 96, 108 cells: {d:+.3f} ± {de:.3f} (chi2 {chi:.1f} on {len(offs) - 1})')
    for L in sorted(res):
        if L not in ANCH:
            print(f'  ({L[0]},{L[1]}),(0,{L[2]}), {3 * L[0] * L[2]} cells: dice chain {res[L][0]:.3f} ± {res[L][1]:.3f}; minus d: {res[L][0] - d:.3f} ± {math.hypot(res[L][1], de):.3f}')
