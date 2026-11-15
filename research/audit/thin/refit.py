#!/usr/bin/env python3
"""Refits of the thin line's lifetime laws with correction forms it did not use (review of research/theory/thin/).
Reads the line's curated research/theory/thin/data/lifetimes.json, and the review's own runs if present
(tt.py load). Weighted least squares; gamma per site and per cell, with the fit's own error and chi^2/dof.

    python3 research/audit/thin/refit.py
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
D = json.load(open(os.path.join(ROOT, 'research', 'theory', 'thin', 'data', 'lifetimes.json')))

FORMS = {
    'a+gL': lambda L: [np.ones_like(L), L],
    'a+gL+c/L': lambda L: [np.ones_like(L), L, 1 / L],
    'a+gL+c lnL': lambda L: [np.ones_like(L), L, np.log(L)],
    'a+gL+c sqrtL': lambda L: [np.ones_like(L), L, np.sqrt(L)],
    'a+gL+c/L+d/L^2': lambda L: [np.ones_like(L), L, 1 / L, 1 / L ** 2],
    'a+gL+c lnL+d/L': lambda L: [np.ones_like(L), L, np.log(L), 1 / L],
}


def fit(L, y, e, form):
    X = np.array(FORMS[form](L)).T
    Wt = 1 / e ** 2
    A = X.T @ (X * Wt[:, None]); cov = np.linalg.inv(A); p = cov @ (X.T @ (Wt * y))
    r = (y - X @ p) / e
    dof = len(L) - X.shape[1]
    return p[1], math.sqrt(cov[1, 1]), float(r @ r), dof


def expfit(L, y, e, xis=(3, 5, 8, 12, 20)):
    """a + g L + c exp(-L/xi): profile over xi"""
    best = None
    for xi in xis:
        X = np.array([np.ones_like(L), L, np.exp(-L / xi)]).T; Wt = 1 / e ** 2
        A = X.T @ (X * Wt[:, None]); cov = np.linalg.inv(A); p = cov @ (X.T @ (Wt * y)); r = (y - X @ p) / e
        out = (float(r @ r), p[1], math.sqrt(cov[1, 1]), xi)
        best = out if best is None or out[0] < best[0] else best
    return best


def series(prefix, own=None):
    pts = []
    for k, v in D.items():
        if k.startswith(prefix) and k[len(prefix):].isdigit():
            n = v['b'] - v['wall']
            pts.append((n, v['lntau'], v['err'], 'line'))
    if own:
        pts += own
    pts.sort()
    return pts


def report(name, pts, mins, forms):
    print(f'== {name}: ' + ', '.join(f'{n}:{y:.4f}({e * 1e4:.0f}){"*" if s != "line" else ""}' for n, y, e, s in pts))
    for form in forms:
        row = []
        for m in mins:
            sel = [p for p in pts if p[0] >= m]
            L = np.array([p[0] for p in sel], float); y = np.array([p[1] for p in sel]); e = np.array([p[2] for p in sel])
            k = len(FORMS[form](L))
            if len(L) <= k:
                row.append(f'>= {m}: -'); continue
            g, ge, chi, dof = fit(L, y, e, form)
            row.append(f'>={m}: {g:.4f}({ge * 1e4:.0f}) [{g / 3:.4f}] chi2 {chi:.1f}/{dof}')
        print(f'  {form:16s} ' + ' | '.join(row))
    row = []
    for m in mins:
        sel = [p for p in pts if p[0] >= m]
        L = np.array([p[0] for p in sel], float); y = np.array([p[1] for p in sel]); e = np.array([p[2] for p in sel])
        if len(L) > 4:
            chi, g, ge, xi = expfit(L, y, e)
            row.append(f'>={m}: {g:.4f}({ge * 1e4:.0f}) [{g / 3:.4f}] xi {xi} chi2 {chi:.1f}')
    print(f'  {"a+gL+c e^-L/xi":16s} ' + ' | '.join(row))


def own(prefix_ring, wall):
    try:
        import tt
    except Exception:
        return []
    out = []
    import glob
    for d in glob.glob(os.path.join(tt.OUT, prefix_ring + '*')):
        tag = os.path.basename(d)
        if not tag[len(prefix_ring):].isdigit():
            continue
        acc = tt.load(tag)
        if acc['n'] and acc['F'] > 100:
            lt, er = tt.lntau(acc)
            n = int(tag[len(prefix_ring):])
            out.append((n, lt, er, 'own'))
    return out


if __name__ == '__main__':
    forms = ['a+gL', 'a+gL+c/L', 'a+gL+c lnL', 'a+gL+c sqrtL', 'a+gL+c/L+d/L^2', 'a+gL+c lnL+d/L']
    seg = series('seg_det_n')
    report('segments (line data)', [p for p in seg if p[0] >= 9], [13, 17, 21, 25], forms)
    ring = series('det_b')
    report('rings (line data)', ring, [16, 20, 24], forms[:4])
    so, ro = own('s', 3), own('r', 0)
    if ro:
        report('rings (review runs only)', ro, [16, 24], forms[:4])
        report('rings (line + review)', sorted(ring + [p for p in ro if p[0] not in {q[0] for q in ring}]), [16, 20, 24], forms[:4])
    if so:
        print('review segments:', so)
