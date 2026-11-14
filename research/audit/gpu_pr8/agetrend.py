#!/usr/bin/env python3
"""Audit of PR 8: does the hazard depend on age (since T0) in runs with raw lives stored?
  python3 research/audit/gpu_pr8/agetrend.py PR8_WORKTREE
Weibull fit with right censoring (shape k; k = 1 is exponential), profile likelihood ratio test against k = 1, and
a split of deaths / expected deaths at half the run length. Also: the same test on bin data (deaths, exposure per
age bin), fitting a hazard ~ age^(k-1), for runs without raw lives."""
import base64, glob, json, math, os, sys, zlib
import numpy as np
root = sys.argv[1]


def wll(x, d, k):
    D = d.sum(); lam = np.sum(x ** k) / D
    return D * math.log(k) - D * math.log(lam) + (k - 1) * np.sum(np.log(x[d])) - D


for p in sorted(glob.glob(os.path.join(root, 'research/data/gpu_facelaw/*A10G.json'))):
    r = json.load(open(p)); name = os.path.basename(p)
    T0 = 1000 if r.get('sym') else 200
    if 'raw' in r:
        a, k, b = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), np.int64).reshape(r['raw']['shape'])
        keep = (a > T0) & (k <= 1)        # settled lives (kind >= 2) dropped as censored-at-settle would need their age; few
        x = (a[keep] - T0).astype(float); d = k[keep] == 1
        ks = np.linspace(0.6, 1.4, 801)
        ll = np.array([wll(x, d, kk) for kk in ks]); i = ll.argmax()
        inside = ks[ll >= ll[i] - 0.5]
        lr = 2 * (ll[i] - wll(x, d, 1.0))
        print(f'{name:26s} raw: deaths {d.sum():6d}  Weibull k = {ks[i]:.3f} ({inside[0]:.3f}-{inside[-1]:.3f}, 68%)  '
              f'LR vs k=1: {lr:.1f} (p = {math.erfc(math.sqrt(lr / 2)):.2g})  oldest {x.max():.3g}')
    else:
        E = np.array(r['bins']['edges'], float); dd = np.array(r['bins']['deaths'], float); ee = np.array(r['bins']['exposure'], float)
        m = (E[:-1] >= T0) & (ee > 0)
        mid = np.sqrt(np.maximum(E[:-1], 1) * E[1:])[m]; dd = dd[m]; ee = ee[m]
        # Poisson fit of hazard c * mid^(k-1) on bins
        best = None
        for kk in np.linspace(0.6, 1.4, 801):
            w = ee * mid ** (kk - 1); c = dd.sum() / w.sum(); L = np.sum(dd * np.log(c * w + 1e-300) - c * w)
            if best is None or L > best[1]: best = (kk, L)
        w = ee; c = dd.sum() / w.sum(); L1 = np.sum(dd * np.log(c * w + 1e-300) - c * w)
        lr = 2 * (best[1] - L1)
        print(f'{name:26s} bins: deaths {int(dd.sum()):6d}  power k = {best[0]:.3f}  LR vs flat: {lr:.1f} (p = {math.erfc(math.sqrt(max(lr, 0) / 2)):.2g})')
