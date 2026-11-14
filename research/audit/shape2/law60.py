#!/usr/bin/env python3
"""Forecast laws at A = 60 with this review's independent values, and with every run pooled.

    python3 research/audit/shape2/law60.py
"""
import json, math, os, sys
from scipy.stats import chi2 as C2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import recompute as rc  # noqa
import drv  # noqa
from drv import ts  # noqa

fc = json.load(open(os.path.join(rc.ROOT, 'research/shape2/data/predictions.json')))['fits']
mine = {}
for L in [(1, 2, 20), (1, 8, 20), (2, 2, 10), (1, 3, 20), (1, 5, 20), (1, 4, 20)]:
    try:
        r = ts.stats(L, quiet=True); mine[rc.canon(L)] = (r['lnF'], r['eF'])
    except Exception:
        pass
fresh = {}
for L in [(1, 2, 20), (1, 8, 20), (2, 2, 10), (1, 3, 20), (1, 5, 20), (1, 4, 20)]:
    s = rc.raw_stats(L); fresh[rc.canon(L)] = (s['ln'], s['e'])
p60 = rc.published(60)
rev = {rc.canon((4, 0, 5)): (12.4883, 0.0030), rc.canon((5, 1, 4)): (12.4707, 0.0030)}


def pool(*ds):
    out = {}
    for c in fresh:
        vals = [d[c] for d in ds if c in d]
        w = sum(1 / e ** 2 for _, e in vals); out[c] = (sum(v / e ** 2 for v, e in vals) / w, 1 / math.sqrt(w))
    return out


for lab, pts in [('this review only (systole^2 13 class not run: fresh value used)', {**fresh, **mine}),
                 ('all runs pooled (fresh, research/shape, both reviews)', pool(fresh, p60, rev, mine))]:
    print(lab)
    for key in ('L1-area', 'L2-area', 'L3-const', 'L3-area', 'L4-area'):
        law, scale = key.split('-'); par = fc[key]
        x, d = rc.chi2_c_free({(60, c): v for c, v in pts.items()}, law, scale, par['B'], par['K'], par['E'])
        x2, d2 = rc.chi2_c_free({(60, c): v for c, v in pts.items() if rc.gc.systole2(c) >= 12}, law, scale, par['B'], par['K'], par['E'])
        print(f'  {key}: chi2 {x:.1f} / {d} (p {C2.sf(x, d):.2g}); systole^2 >= 12 only {x2:.1f} / {d2} (p {C2.sf(x2, d2):.2g})')
