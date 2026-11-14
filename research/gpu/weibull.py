#!/usr/bin/env python3
"""Age dependence of the death rate from a run's raw lives: censored (and optionally left-truncated) Weibull fit.

  python3 research/gpu/weibull.py research/data/gpu_facelaw/symcR43_s501_A10G.json [more files]

Residence t = age - T0 for lives with age >= T0 (T0 = 1000 symmetric, 200 asymmetric); deaths are kind 1; settled
lives (kinds 2, 3) are censored at their settle age; lives open at the end are censored. Fit S(t) = exp(-(t/lam)^k)
by profile likelihood over k (lam closed-form for each k); with a start a (left truncation), lives that ended before
a are dropped and each contributes from a. Reports k, its 95% profile interval and the likelihood-ratio p for k = 1,
and the hazard by age in units of the exponential tau (= exposure / deaths), with the 95% Poisson range.
"""
import json, math, sys
import numpy as np
import facelaw


def fit(t, d, a=0.0):
    keep = t > a
    t, d = t[keep], d[keep]
    D = d.sum(); lt = np.log(t[d])
    if D < 2:
        return dict(n=int(keep.sum()), deaths=int(D), k=float('nan'), k95=(float('nan'), float('nan')), p_k1=float('nan'))
    def prof(k):
        s = (t ** k - a ** k).sum()
        lamk = s / D
        return D * math.log(k) - D * math.log(lamk) + (k - 1) * lt.sum() - D, lamk
    ks = np.linspace(0.6, 1.4, 801)
    ll = np.array([prof(k)[0] for k in ks])
    i = int(ll.argmax()); kbest = ks[i]
    ci = ks[ll >= ll[i] - 1.92]
    p = math.erfc(math.sqrt(max(2 * (ll[i] - prof(1.0)[0]), 0) / 2))
    return dict(n=int(keep.sum()), deaths=int(D), k=float(kbest), k95=(float(ci.min()), float(ci.max())), p_k1=p)


def main(paths):
    for path in paths:
        r = json.load(open(path))
        a, k, b = facelaw.unpack(r['raw'])
        T0 = 1000 if r.get('sym') else 200
        keep = a >= T0
        t = (a[keep] - T0).astype(float); kind = k[keep]
        d = kind == 1
        tau = t.sum() / d.sum()
        print(f'{path.split("/")[-1]}: {len(t)} lives, {d.sum()} deaths, {int((kind >= 2).sum())} settled '
              f'(kind 3: {int((kind == 3).sum())}), tau = {tau:.4g} (ln {math.log(tau):.3f} +- {1 / math.sqrt(d.sum()):.3f}), '
              f'oldest {t.max() / tau:.2f} tau')
        for lo in (0.0, 0.05 * tau):
            f = fit(np.maximum(t, 1.0), d, lo)
            print(f'  Weibull, ages >= {lo / tau:.2f} tau: {f["deaths"]} deaths, k = {f["k"]:.3f} '
                  f'(95% {f["k95"][0]:.3f}-{f["k95"][1]:.3f}), LR p(k = 1) = {f["p_k1"]:.3f}')
        edges = np.array([0, .01, .03, .1, .2, .3, .5, .75, 1, 1.5, 2, 3, 5]) * tau
        out = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            e = np.clip(np.minimum(t, hi) - lo, 0, None).sum()
            n = int((d & (t >= lo) & (t < hi)).sum())
            if e > 0:
                exp = e / tau
                out.append(f'[{lo / tau:.2g},{hi / tau:.2g}) {n}/{exp:.1f}={n / exp:.2f}')
        print('  hazard x tau by age/tau (deaths / expected):', '; '.join(out))


if __name__ == '__main__':
    main(sys.argv[1:])
