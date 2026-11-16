#!/usr/bin/env python3
"""Additivity: mean residual of faces with one short direction (loop^2 <= 20) against faces with two or more, for the
law (frozen; and refitted) and HAZ, on A >= 48 (on file + new).   python3 research/wrap/additivity.py"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fit as Fm, models as Mm  # noqa: E402
pts = [p for p in Fm.select('all', True) if p['A'] >= 48]
y = np.array([p['y'] for p in pts]); se = np.array([p['se'] for p in pts])
ns = np.array([len([q for q in p['loops'] if q <= 20]) for p in pts])
A, N, _, _ = Mm.arrays(pts)
preds = {'frozen law': np.array([Fm.frozen(p) for p in pts])}
for m in ('LAW', 'HAZ'):
    th, cov, chi, r = Mm.fitm(m, pts); preds[m + ' refit'] = Mm.f(m, th, A, N)
for lab, f in preds.items():
    out = []
    for name, sel in (('one', ns == 1), ('two+', ns >= 2)):
        w = 1 / se[sel] ** 2; d = y[sel] - f[sel]
        out.append((name, int(sel.sum()), float((w * d).sum() / w.sum()), float(w.sum() ** -0.5)))
    diff = out[1][2] - out[0][2]; de = math.hypot(out[0][3], out[1][3])
    print(f'{lab:12s} ' + '  '.join(f'{n} short ({k} faces): {m:+.4f} ± {e:.4f}' for n, k, m, e in out) +
          f'   two+ minus one: {diff:+.4f} ± {de:.4f} ({diff / de:+.1f} se)')
