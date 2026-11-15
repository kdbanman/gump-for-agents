#!/usr/bin/env python3
"""Routes 3 and 4 of the thin line (empty windows on a ring of 64; front distance from a wall in a segment of 61), refit
with forms the line did not use, from its curated research/theory/thin/data/windows.json (review, claim 3).
ln W(x) and ln E(l) are fitted directly (unweighted on a range of x: the samples are correlated in time, so formal
errors would mean little; stability over ranges is the test).

    python3 research/audit/thin/refit_win.py
"""
import json, os
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
w = json.load(open(os.path.join(ROOT, 'research', 'theory', 'thin', 'data', 'windows.json')))

FORMS = {   # ln W(x) = c - g x + ...
    'pure exp': lambda x: [np.ones_like(x), -x],
    '- p ln x': lambda x: [np.ones_like(x), -x, -np.log(x)],
    '- p ln x + q/x': lambda x: [np.ones_like(x), -x, -np.log(x), 1 / x],
    '- a sqrt x': lambda x: [np.ones_like(x), -x, -np.sqrt(x)],
    '- a sqrt x - p ln x': lambda x: [np.ones_like(x), -x, -np.sqrt(x), -np.log(x)],
    '- p ln x + q ln x / x': lambda x: [np.ones_like(x), -x, -np.log(x), np.log(x) / x],
}


def fit(x, y, form):
    X = np.array(FORMS[form](x)).T
    p, *_ = np.linalg.lstsq(X, y, rcond=None)
    return p[1], float(np.sqrt(np.mean((y - X @ p) ** 2)))


def table(name, x, y, ranges):
    print(f'== {name}: gamma per site (rms residual of ln) by fit range')
    for form in FORMS:
        row = []
        for lo, hi in ranges:
            s = (x >= lo) & (x <= hi)
            if s.sum() <= len(FORMS[form](x[:1])) + 1:
                row.append('-'); continue
            g, r = fit(x[s], y[s], form)
            row.append(f'[{lo},{hi}] {g:.4f} ({r:.1e})')
        print(f'  {form:24s} ' + ' | '.join(row))


v = w['seg_det_n61']
h = np.array(v['hfl'], float) + np.array(v['hfr'], float)
W = np.cumsum(h[::-1])[::-1]          # W(x) = P(first x sites from the wall empty) * norm
xs = np.arange(len(W), dtype=float)
ok = W > 400                           # at least ~400 samples beyond x
table('route 4: ln W(x), segment of 61 (both walls pooled)', xs[ok & (xs >= 1)], np.log(W[ok & (xs >= 1)]),
      [(8, 32), (12, 32), (16, 36), (20, 36)])
v = w['win_det_b64']
lnE = np.array(v['lnE'], float); ls = np.arange(len(lnE), dtype=float)
okE = np.isfinite(lnE) & (ls >= 1) & (np.array(v['lnE_err'], float) < 0.05)
table('route 3: ln E(l), ring of 64', ls[okE], lnE[okE], [(8, 40), (12, 40), (16, 40), (20, 40)])
print('largest l with lnE_err < 0.05:', int(ls[okE].max()), '; largest x with W > 400:', int(xs[ok].max()))
