#!/usr/bin/env python3
"""Claim a: re-derive the slab table from the committed JSON with independent unpacking and sums.

  python3 research/audit/gpu_pr12/slab_rederive.py PR12_WORKTREE

Own base64/zlib unpacking of `raw` (ages, kinds, births per life); estimator: tau_face = nf * exposure / deaths with
exposure = sum over lives of max(0, age - T0), deaths = kind-1 lives with age >= T0 (lives ending before T0 excluded),
nf = 2 faces. Cross-checks raw against the stored aggregates, then hazard vs age inside the observed window, and the
comparisons the PR makes.
"""
import base64, json, math, sys, zlib, glob, os
import numpy as np

PR = sys.argv[1]
D = os.path.join(PR, 'research', 'data', 'gpu_facelaw')


def raw(r):
    a = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), '<i8').reshape(r['raw']['shape'])
    return a[0], a[1], a[2]


def est(ages, kinds, T0, nf):
    keep = ages >= T0
    d = int(((kinds == 1) & keep).sum()); e = float((ages[keep] - T0).sum())
    return d, e, math.log(nf * e / d), 1 / math.sqrt(d)


line = lambda A: -0.091 + 0.2088 * A
res = {}
for geo in ('6x6x8', '6x7x8'):
    recs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(D, f'slab{geo}_*.json')))]
    seeds = [r['seed'] for r in recs]; assert len(set(seeds)) == len(seeds)
    A = recs[0]['A']; N1, N2, m = recs[0]['slab']; assert A == 3 * N1 * N2
    ages = []; kinds = []; births = []; G = []
    for r in recs:
        a, k, b = raw(r)
        # consistency: every replica's lives tile [0, gens]: sum of ages = replicas * gens
        # lives tile [0, gens] except the frozen rest of the launch after each death (reseed at launch end)
        gap = r['replicas'] * r['gens'] - a.sum(); assert gap >= 0
        print(f"  run seed {r['seed']}: replicas x gens - sum(ages) = {gap:.3g} = {gap / max(1, (k == 1).sum()):.3g} per death "
              f"(frozen remainder of the launch); births are launch ends: {np.unique(b).size} distinct")
        assert ((b + a) <= r['gens']).all()
        for T0 in (60, 200, 1000):
            s = r['agg'][str(T0)]; keep = a >= T0
            assert s['deaths'] == int(((k == 1) & keep).sum()) and s['exposure'] == int((a[keep] - T0).sum())
            assert s['settled'] == int(((k >= 2) & keep).sum())
        assert sorted(a[k == 1].tolist()) == r['death_ages']
        ages.append(a); kinds.append(k); births.append(b); G.append(r['gens'])
    a, k, b = np.concatenate(ages), np.concatenate(kinds), np.concatenate(births)
    print(f'slab {geo} A={A}: {len(recs)} runs, {len(a)} lives, deaths {int((k==1).sum())}, settled {int((k>=2).sum())}, '
          f'max age {a.max():.3g}, gens {G}')
    for T0 in (0, 60, 200, 1000):
        d, e, lt, se = est(a, k, T0, 2)
        print(f'  T0={T0:5d}: deaths {d}  ln(2 x mean) = {lt:.3f} +- {se:.3f}  line {line(A):.3f}  diff {lt - line(A):+.3f}  per cell {lt / A:.4f}')
    d, e, lt, se = est(a, k, 60, 2)
    res[A] = (lt, se)
    tau1 = e / d     # mean first peel
    # hazard vs age inside the window: deaths / exposure in age bins, relative to the overall rate
    mx = a.max()
    edges = np.unique(np.r_[0, 60, mx * np.array([.01, .03, .1, .2, .35, .5, .7, 1.0001])]).astype(np.int64)
    print(f'  window = {mx / tau1:.4f} of the mean first peel {tau1:.3g}; hazard / overall rate by age bin:')
    rate = d / e
    for lo, hi in zip(edges[:-1], edges[1:]):
        ex = np.clip(np.minimum(a, hi) - lo, 0, None).sum(); dd = int(((k == 1) & (a >= lo) & (a < hi)).sum())
        print(f'    age {lo:11.4g}-{hi:11.4g}: deaths {dd:4d} expected {rate * ex:7.1f}  ratio {dd / max(rate * ex, 1e-9):.2f}')
    # censored Weibull shape over the window (lives from age 60): MLE on a grid
    keep = a >= 60; x = (a[keep] - 60).astype(float); dd = (k[keep] == 1)
    x = np.maximum(x, 0.5)
    def ll(kk):
        lam = (np.sum(x ** kk) / dd.sum()) ** (1 / kk)
        return dd.sum() * math.log(kk) - dd.sum() * kk * math.log(lam) + (kk - 1) * np.log(x[dd]).sum() - np.sum((x / lam) ** kk)
    ks = np.linspace(0.6, 1.6, 1001); L = np.array([ll(q) for q in ks]); kh = ks[L.argmax()]
    ci = ks[L > L.max() - 1.92]
    print(f'  censored Weibull shape over the window: {kh:.3f} (95% {ci.min():.3f}-{ci.max():.3f})')
(l1, s1), (l2, s2) = res[108], res[126]
print(f'local slope 108 -> 126: {(l2 - l1) / 18:.4f} +- {math.hypot(s1, s2) / 18:.4f}')
print(f'slope of the CPU line through A=90 point to the GPU points: see claim text')
oct108 = 23.376
print(f'octahedral A=108 (23.376 +- 0.031) minus slab A=108: {oct108 - l1:.3f} +- {math.hypot(0.031, s1):.3f}')
