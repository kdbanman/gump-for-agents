#!/usr/bin/env python3
"""Tests of "ln tau_face is a function of X alone" from research/shape/data/A<area>.csv.

    python3 research/shape/fits.py 72

For each candidate X (the shape itself, Euclidean systole^2, hex systole, shortest row closure, firewall cut) the tori
are grouped by X, each group gets its weighted mean, and chi^2 of the values about their group means is printed with
its degrees of freedom and p-value. "shape" (group by reduced Gram) is the control: presentations of one torus.
Also: a straight line in the Euclidean systole sigma = sqrt(systole^2) through the shapes with systole^2 >= 12.
"""
import csv, math, os, sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))


def load(A):
    return list(csv.DictReader(open(os.path.join(HERE, 'data', f'A{A}.csv'))))


def group_chi2(rows, key):
    g = {}
    for r in rows:
        g.setdefault(key(r), []).append((float(r['ln_tau_face']), float(r['err'])))
    chi, dof, means = 0.0, 0, {}
    for k, v in g.items():
        y = np.array([a for a, _ in v]); e = np.array([b for _, b in v]); w = 1 / e ** 2
        m = (w * y).sum() / w.sum(); means[k] = (m, 1 / math.sqrt(w.sum()), len(v))
        chi += (w * (y - m) ** 2).sum(); dof += len(v) - 1
    return chi, dof, (stats.chi2.sf(chi, dof) if dof else float('nan')), means


if __name__ == '__main__':
    A = int(sys.argv[1]); rows = load(A)
    keys = {
        'shape (control)': lambda r: r['gram'],
        'Euclidean systole^2': lambda r: int(r['systole2']),
        'hex systole': lambda r: int(r['hex_systole']),
        'shortest row closure': lambda r: min(map(int, r['rows'].split())),
        'area only': lambda r: 0,
    }
    for name, f in keys.items():
        chi, dof, p, means = group_chi2(rows, f)
        print(f'{name:22s} chi2 {chi:7.2f} / {dof:2d}  p = {p:.3g}')
        if name != 'area only':
            for k in sorted(means, key=lambda z: means[z][0]):
                m, e, n = means[k]
                print(f'      {str(k):12s} {m:.3f} ± {e:.3f}  ({n} tori)')
    # shapes pooled, then a line in sigma for systole^2 >= 12 and the residuals
    chi, dof, p, sh = group_chi2(rows, keys['shape (control)'])
    s2 = {r['gram']: int(r['systole2']) for r in rows}
    hx = {r['gram']: int(r['hex_systole']) for r in rows}
    X = np.array([math.sqrt(s2[k]) for k in sh]); Y = np.array([sh[k][0] for k in sh]); E = np.array([sh[k][1] for k in sh])
    sel = X >= math.sqrt(12) - 1e-9
    for lab, mask in [('sys2 >= 12', sel), ('all', np.ones_like(sel))]:
        w = 1 / E[mask] ** 2
        Am = np.vstack([np.ones(mask.sum()), X[mask]]).T
        cov = np.linalg.inv(Am.T @ (Am * w[:, None])); beta = cov @ (Am.T @ (w * Y[mask]))
        res = Y[mask] - Am @ beta
        print(f'line in sigma ({lab}): ln tau = {beta[0]:.3f} + {beta[1]:.4f} sigma  (slope ± {math.sqrt(cov[1, 1]):.4f}); '
              f'chi2 {np.sum(w * res ** 2):.2f} / {mask.sum() - 2}')
        for k, x, y, e, r_ in zip(np.array(list(sh))[mask], X[mask], Y[mask], E[mask], res):
            print(f'      {k:12s} sigma {x:.3f} hex {hx[k]}  {y:.3f} ± {e:.3f}  resid {r_ / e:+.2f} sd')
