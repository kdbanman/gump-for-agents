#!/usr/bin/env python3
"""Claim b: censored, left-truncated Weibull fits and the hazard-by-age table, re-derived with own code
(own unpacking; joint 2-parameter MLE by scipy, profile-likelihood intervals; no code from research/gpu/).

  python3 research/audit/gpu_pr12/weibull_own.py PR12_WORKTREE

Residence t = age - T0 (T0 = 1000, symmetric runs) for lives with age >= T0; kind 1 = death; kinds 2, 3 (settled)
and kind 0 (open at the end) censored. Left truncation at a: lives with t <= a dropped, each contributes
S(t)/S(a). Also: the falling-hazard alternative the earlier runs suggested (k = 0.94, 0.84), tested on this run.
"""
import base64, json, math, os, sys, zlib
import numpy as np
from scipy import optimize, stats

PR = sys.argv[1]
D = os.path.join(PR, 'research', 'data', 'gpu_facelaw')


def lives(name):
    r = json.load(open(os.path.join(D, name)))
    q = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), '<i8').reshape(r['raw']['shape'])
    a, k, b = q
    assert sorted(a[k == 1].tolist()) == r['death_ages']
    s = r['agg']['1000']; keep = a >= 1000
    assert s['deaths'] == int(((k == 1) & keep).sum()) and s['exposure'] == int((a[keep] - 1000).sum())
    t = (a[keep] - 1000).astype(float); d = k[keep] == 1
    return r, np.maximum(t, 1.0), d, k[keep]


def nll(params, t, d, a):
    lk, ll = params; kk = math.exp(lk); lam = math.exp(ll)
    z = (t / lam) ** kk - (a / lam) ** kk
    return -(d.sum() * math.log(kk) + (kk - 1) * np.log(t[d]).sum() - d.sum() * kk * math.log(lam) - z.sum())


def fitw(t, d, a=0.0):
    m = t > a; t, d = t[m], d[m]
    tau = (t - a).sum() / d.sum()
    res = optimize.minimize(nll, [0.0, math.log(tau)], args=(t, d, a), method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-7))
    k = math.exp(res.x[0]); best = res.fun
    def prof(kk):   # profile over lam
        r = optimize.minimize_scalar(lambda ll: nll([math.log(kk), ll], t, d, a), bracket=(res.x[1] - 1, res.x[1] + 1))
        return r.fun
    lo = optimize.brentq(lambda kk: prof(kk) - best - 1.92, 0.3, k)
    hi = optimize.brentq(lambda kk: prof(kk) - best - 1.92, k, 3.0)
    p1 = stats.chi2.sf(2 * (prof(1.0) - best), 1)
    return dict(k=k, lo=lo, hi=hi, p1=p1, n=int(m.sum()), deaths=int(d.sum()), tau=tau, prof=prof, best=best)


for name in ('symcR43_s501_A10G.json', 'symcR43_s201_A10G.json', 'symcR45_s202_A10G.json'):
    r, t, d, k = lives(name)
    tau = t.sum() / d.sum()
    print(f'{name}: R={r["R"]} A={r["A"]} replicas {r["replicas"]} gens {r["gens"]:.4g} seed {r["seed"]}: {len(t)} lives from T0, '
          f'{d.sum()} deaths, settled {int((k >= 2).sum())}, tau = {tau:.4g} (ln {math.log(tau):.3f} +- {1 / math.sqrt(d.sum()):.3f}), '
          f'oldest {t.max() / tau:.2f} tau')
    for a in (0.0, 0.05 * tau):
        if (d & (t > a)).sum() < 2:
            print(f'  Weibull from {a / tau:.2f} tau: no deaths'); continue
        f = fitw(t, d, a)
        extra = ''
        if name.startswith('symcR43_s501'):
            # likelihood-ratio p for the shapes the earlier runs suggested
            extra = '; LR p at k = 0.94: %.2g, at k = 0.84: %.2g, at k = 0.95: %.2g, at k = 1.05: %.2g' % tuple(
                stats.chi2.sf(2 * (f['prof'](q) - f['best']), 1) for q in (0.94, 0.84, 0.95, 1.05))
        print(f'  Weibull from {a / tau:.2f} tau: n {f["n"]}, deaths {f["deaths"]}: k = {f["k"]:.3f} (95% {f["lo"]:.3f}-{f["hi"]:.3f}), '
              f'p(k=1) = {f["p1"]:.3f}{extra}')
    if name.startswith('symcR43_s501'):
        edges = np.array([0, .01, .03, .1, .2, .3, .5, .75, 1, 1.5, 2, 3]) * tau
        rows = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            e = np.clip(np.minimum(t, hi) - lo, 0, None).sum(); n = int((d & (t >= lo) & (t < hi)).sum())
            ex = e / tau
            q = stats.poisson
            rows.append(f'[{lo / tau:.2g},{hi / tau:.2g}) {n}/{ex:.1f}={n / ex:.2f} (95% {q.ppf(.025, ex) / ex:.2f}-{q.ppf(.975, ex) / ex:.2f})')
        print('  hazard x tau by age, deaths/expected:\n    ' + '\n    '.join(rows))
        # the same age window as the short runs: censor this run at 0.23 tau (s201's oldest) and 0.04 tau (s202's)
        for w in (0.23, 0.04):
            L = w * tau; tw = np.minimum(t, L); dw = d & (t <= L)
            f = fitw(tw, dw)
            print(f'  this run censored at {w} tau (window of the shorter runs): deaths {f["deaths"]}, k = {f["k"]:.3f} '
                  f'(95% {f["lo"]:.3f}-{f["hi"]:.3f})')
# pooled R = 43 (two seeds, independent soups)
r1, t1, d1, _ = lives('symcR43_s501_A10G.json'); r2, t2, d2, _ = lives('symcR43_s201_A10G.json')
t = np.r_[t1, t2]; d = np.r_[d1, d2]
f = fitw(t, d); tau = t.sum() / d.sum()
print(f'pooled R=43 (seeds 501, 201): deaths {d.sum()}, ln tau {math.log(tau):.3f} +- {1 / math.sqrt(d.sum()):.3f}; '
      f'Weibull k = {f["k"]:.3f} ({f["lo"]:.3f}-{f["hi"]:.3f})')
