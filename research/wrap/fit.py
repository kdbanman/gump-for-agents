#!/usr/bin/env python3
"""Independent refit of the wrapping law and its rivals (research/wrap).  Data from faces.py (primary files).

    python3 research/wrap/fit.py lead        # the lead's selection: reproduce the 32-face table and parameters
    python3 research/wrap/fit.py all         # + shape3 (and this study's runs, if any), every model, LOO tables
    python3 research/wrap/fit.py all --corr  # the same with the stamping-bias corrections of faces.py
    python3 research/wrap/fit.py forecast    # this study's forecast for the new faces (model M1 on 'all --corr' data)

Models (y = ln tau_face; N_q = number of loop directions with |v|^2 = q, q in QS; X_q = sum over those):
  LAW   a + c (A-63) - (A - A0) sum_q k_q N_q            (the lead's; A0 profiled on a grid)        7 parameters
  PC    a + c (A-63) - A sum_q k_q N_q                   (A0 = 0: discount per cell, no offset)       6
  OFF   a + c (A-63) - sum_q (u_q + k A) N_q             (an offset per loop length, one per-cell k)  7
  OFF2  a + c (A-63) - sum_q (u_q + w_q A) N_q           (free line per loop length)                  10
"""
import math, sys
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import faces  # noqa: E402

QS = [12, 13, 16, 19]


def select(mode, corr):
    recs = faces.raw(corr, wrap=(mode != 'lead'))
    if mode == 'lead':
        keep = []
        for r in recs:
            eq = r['g'][0] == r['g'][1] == r['g'][2]
            if r['src'] == 'shape3':
                continue
            if eq and r['src'] != 'card':
                continue
            keep.append(r)
        recs = keep
    else:
        recs = [r for r in recs if not (r['g'][0] == r['g'][1] == r['g'][2] and r['src'] not in ('card', 'wrap'))]
    return faces.pooled(recs)


def design(pts, model, A0=21.25, qs=QS):
    A = np.array([p['A'] for p in pts], float)
    N = np.array([[sum(1 for q in p['loops'] if q == Q) for Q in qs] for p in pts], float)
    one = np.ones(len(pts)); c = A - 63
    if model == 'LAW':
        cols = [one, c] + [-(A - A0) * N[:, j] for j in range(len(qs))]
    elif model == 'PC':
        cols = [one, c] + [-A * N[:, j] for j in range(len(qs))]
    elif model == 'OFF':
        cols = [one, c] + [-N[:, j] for j in range(len(qs))] + [-A * N.sum(1)]
    elif model == 'OFF2':
        cols = [one, c] + [-N[:, j] for j in range(len(qs))] + [-A * N[:, j] for j in range(len(qs))]
    return np.column_stack(cols)


def wls(X, y, se):
    W = 1 / se
    b, *_ = np.linalg.lstsq(X * W[:, None], y * W, rcond=None)
    cov = np.linalg.pinv((X * W[:, None]).T @ (X * W[:, None]))
    r = (y - X @ b) / se
    return b, cov, r


def fitmodel(pts, model, qs=QS, grid=np.arange(0, 45.01, 0.25)):
    y = np.array([p['y'] for p in pts]); se = np.array([p['se'] for p in pts])
    if model == 'LAW':
        best = None
        for a0 in grid:
            b, cov, r = wls(design(pts, model, a0, qs), y, se)
            if best is None or r @ r < best[0]:
                best = (float(r @ r), a0, b, cov, r)
        return best
    b, cov, r = wls(design(pts, model, qs=qs), y, se)
    return (float(r @ r), None, b, cov, r)


def predict(pts_fit, pts_new, model, A0=None, qs=QS):
    chi, a0, b, cov, r = fitmodel(pts_fit, model, qs)
    X = design(pts_new, model, a0 if a0 is not None else 21.25, qs)
    f = X @ b
    fe = np.sqrt(np.einsum('ij,jk,ik->i', X, cov, X))
    return f, fe, a0


def npar(model, qs=QS):
    return {'LAW': 3 + len(qs), 'PC': 2 + len(qs), 'OFF': 3 + len(qs), 'OFF2': 2 + 2 * len(qs)}[model]


def report(pts, title):
    print(f'== {title}: {len(pts)} faces')
    for model in ('LAW', 'PC', 'OFF', 'OFF2'):
        chi, a0, b, cov, r = fitmodel(pts, model)
        e = np.sqrt(np.diag(cov)); dof = len(pts) - npar(model)
        s = ' '.join(f'{x:.5f}({ee:.5f})' for x, ee in zip(b, e))
        print(f'{model:5s} chi2 {chi:6.1f} on {dof}  ' + (f'A0={a0:.2f} ' if a0 is not None else '') + s)
    chi, a0, b, cov, r = fitmodel(pts, 'LAW')
    fit = np.array([p['y'] for p in pts]) - r * np.array([p['se'] for p in pts])
    print('   A  gram            loops<=20        lnτ       se     n  srcs                  LAW fit  r/se  LOO r/se  LOAO r/se')
    loo = []
    for i, p in enumerate(pts):
        others = [q for j, q in enumerate(pts) if j != i]
        f, fe, _ = predict(others, [p], 'LAW')
        lr = (p['y'] - f[0]) / math.hypot(p['se'], fe[0])
        same = [q for q in pts if q['A'] != p['A']]
        f2, fe2, _ = predict(same, [p], 'LAW')
        la = (p['y'] - f2[0]) / math.hypot(p['se'], fe2[0])
        loo.append((lr, la))
        print(f"{p['A']:4d}  {str(p['g']):15s} {str([q for q in p['loops'] if q <= 20]):16s} {p['y']:8.4f} {p['se']:.4f} "
              f"{p['n']:2d}  {','.join(p['srcs']):20s} {fit[i]:8.4f} {r[i]:+5.1f}  {lr:+5.1f}  {la:+5.1f}")
    L = np.array(loo)
    print(f'LOO: sum r^2 = {float((L[:, 0] ** 2).sum()):.1f}; leave-one-area-out: sum r^2 = {float((L[:, 1] ** 2).sum()):.1f} '
          f'(n = {len(pts)})')
    print()
    return L


if __name__ == '__main__':
    mode = sys.argv[1]; corr = '--corr' in sys.argv
    if mode in ('lead', 'all'):
        pts = select(mode, corr)
        report(pts, f'{mode} selection, corr={corr}')
        if mode == 'all':
            p48 = [p for p in pts if p['A'] >= 57]
            report(p48, 'A >= 57 only')


# ------------------------------------------------------------------------------------------------- forecasts
NEW = [(2, 2, 6), (1, 3, 13), (1, 3, 14), (1, 3, 15),                       # A = 36-45: below the fitted range
       (1, 3, 17), (1, 4, 18), (1, 3, 18), (1, 3, 19), (1, 3, 21), (1, 8, 21),
       (1, 5, 22), (1, 3, 22), (1, 4, 22), (1, 3, 23), (1, 4, 23),            # A = 51-69 (W1)
       (1, 3, 25), (1, 9, 25), (1, 4, 25), (1, 6, 26), (1, 3, 26), (1, 7, 26), (1, 4, 26),   # A = 75, 78
       (1, 8, 20), (2, 2, 10)]                                               # W6: the A = 60 loop^2 12 pair
FROZEN = dict(a=13.1629, c=0.20860, A0=21.25, k={12: 0.002918, 13: 0.002271, 16: 0.001353, 19: 0.000338})


def frozen(p):
    s = sum(FROZEN['k'].get(q, 0.0) for q in p['loops'] if q <= 20)
    return FROZEN['a'] + FROZEN['c'] * (p['A'] - 63) - (p['A'] - FROZEN['A0']) * s


def forecast():
    import lattices as L
    pts = select('all', True)
    pts = [p for p in pts if p.get('srcs') != ['wrap']]
    assert not any('wrap' in p['srcs'] for p in pts), 'forecasts must be made before this study\'s runs'
    new = []
    for h, k, d in NEW:
        new.append(dict(A=3 * h * d, g=L.gram(h, k, d), loops=L.loops(h, k, d, 30), hkd=(h, k, d)))
    fl, fle, a0 = predict(pts, new, 'LAW')
    fo, foe, _ = predict(pts, new, 'OFF2')
    print(f'fits on the {len(pts)} faces on file (shape3 included, stamping bias corrected); LAW refit A0 = {a0}')
    print('   A  HNF          gram            loops<=20      frozen LAW    LAW refit (+-)     OFF2 (+-)        mine')
    for p, a, ae, b, be in zip(new, fl, fle, fo, foe):
        print(f"{p['A']:4d}  {str(p['hkd']):11s}  {str(p['g']):15s} {str([q for q in p['loops'] if q <= 20]):14s} "
              f"{frozen(p):9.4f}    {a:8.4f} ({ae:.4f})   {b:8.4f} ({be:.4f})   {b:8.4f}")


if __name__ == '__main__' and sys.argv[1] == 'forecast':
    forecast()
