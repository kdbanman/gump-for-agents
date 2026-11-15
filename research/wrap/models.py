#!/usr/bin/env python3
"""Post-hoc rivals to the wrapping law (research/wrap), fitted by nonlinear least squares, with leave-one-out and
leave-one-area-out forecasts.  These forms were tried AFTER the new faces were measured: post hoc, not forecasts.

    python3 research/wrap/models.py [--onfile]      # --onfile: only the faces on file before this study

y = ln tau_face, x = A - 63, n_q = number of loop directions (one per +-v) with |v|^2 = q, q in 12, 13, 16, 19.
  LAW    a + c x - (A - A0) sum_q k_q n_q                                 7 parameters (the lead's)
  EXPA   a + c x - sum_q n_q r_q exp(g_q x)       log-discounts add       10
  EXPA1  a + c x - exp(g x) sum_q n_q r_q         one growth rate          7
  HAZ    a + c x - ln(1 + sum_q n_q r_q exp(g_q x))   hazards add          10
  HAZ1   a + c x - ln(1 + exp(g x) sum_q n_q r_q)                          7
In HAZ a short loop opens a second way to die whose rate per cell is c - g_q instead of c; r_q its share at 63 cells.
"""
import math, os, sys
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit as Fm  # noqa: E402

QS = [12, 13, 16, 19]


def arrays(pts):
    A = np.array([p['A'] for p in pts], float)
    N = np.array([[sum(1 for q in p['loops'] if q == Q) for Q in QS] for p in pts], float)
    y = np.array([p['y'] for p in pts]); se = np.array([p['se'] for p in pts])
    return A, N, y, se


def f(model, th, A, N):
    x = A - 63
    a, c = th[0], th[1]
    if model == 'LAW':
        A0, k = th[2], th[3:7]
        return a + c * x - (A - A0) * (N @ k)
    if model == 'EXPA':
        r, g = th[2:6], th[6:10]
        return a + c * x - (N * r * np.exp(np.outer(x, g))).sum(1)
    if model == 'EXPA1':
        r, g = th[2:6], th[6]
        return a + c * x - np.exp(g * x) * (N @ r)
    if model == 'HAZ':
        r, g = th[2:6], th[6:10]
        return a + c * x - np.log1p((N * r * np.exp(np.outer(x, g))).sum(1))
    if model == 'HAZ1':
        r, g = th[2:6], th[6]
        return a + c * x - np.log1p(np.exp(g * x) * (N @ r))


START = {'LAW': [13.16, 0.2086, 21.0, 0.003, 0.0023, 0.0013, 0.0003],
         'EXPA': [13.16, 0.2086, 0.12, 0.09, 0.05, 0.012, 0.03, 0.03, 0.02, 0.0],
         'EXPA1': [13.16, 0.2086, 0.12, 0.09, 0.05, 0.012, 0.03],
         'HAZ': [13.16, 0.2086, 0.12, 0.09, 0.05, 0.012, 0.03, 0.03, 0.02, 0.0],
         'HAZ1': [13.16, 0.2086, 0.12, 0.09, 0.05, 0.012, 0.03]}
NAMES = {'LAW': 'a c A0 k12 k13 k16 k19', 'EXPA': 'a c r12 r13 r16 r19 g12 g13 g16 g19',
         'EXPA1': 'a c r12 r13 r16 r19 g', 'HAZ': 'a c r12 r13 r16 r19 g12 g13 g16 g19', 'HAZ1': 'a c r12 r13 r16 r19 g'}


def fitm(model, pts, th0=None):
    A, N, y, se = arrays(pts)
    res = least_squares(lambda th: (y - f(model, th, A, N)) / se, th0 if th0 is not None else START[model],
                        method='lm', max_nfev=20000)
    J = res.jac
    try:
        cov = np.linalg.inv(J.T @ J)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(J.T @ J)
    return res.x, cov, float(res.fun @ res.fun), res.fun


def forecast(model, train, test, th0):
    th, cov, _, _ = fitm(model, train, th0)
    A, N, y, se = arrays(test)
    eps = 1e-6
    v = f(model, th, A, N)
    G = np.array([(f(model, th + eps * np.eye(len(th))[i], A, N) - v) / eps for i in range(len(th))]).T
    fe = np.sqrt(np.maximum(np.einsum('ij,jk,ik->i', G, cov, G), 0))
    return v, fe


if __name__ == '__main__':
    pts = Fm.select('all', True)
    if '--onfile' in sys.argv:
        pts = [p for p in pts if 'wrap' not in p['srcs']]
    print(f'{len(pts)} faces (loop^2 >= 12), stamping bias corrected; areas {sorted({p["A"] for p in pts})}')
    for model in ('LAW', 'EXPA', 'EXPA1', 'HAZ', 'HAZ1'):
        th, cov, chi, r = fitm(model, pts)
        e = np.sqrt(np.diag(cov)); dof = len(pts) - len(th)
        loo = []; loa = []
        for i, p in enumerate(pts):
            v, fe = forecast(model, [q for j, q in enumerate(pts) if j != i], [p], th)
            loo.append((p['y'] - v[0]) / math.hypot(p['se'], fe[0]))
        areas = sorted({p['A'] for p in pts})
        for a in areas:
            tr = [q for q in pts if q['A'] != a]; te = [q for q in pts if q['A'] == a]
            v, fe = forecast(model, tr, te, th)
            loa += [(q['y'] - vv) / math.hypot(q['se'], ee) for q, vv, ee in zip(te, v, fe)]
        print(f'{model:6s} chi2 {chi:7.1f} on {dof:2d}   LOO sum z^2 {sum(z * z for z in loo):8.1f}   '
              f'leave-one-area-out sum z^2 {sum(z * z for z in loa):9.1f}   worst LOAO {max(loa, key=abs):+.1f}')
        print('        ' + '  '.join(f'{n}={x:.5g}±{ee:.2g}' for n, x, ee in zip(NAMES[model].split(), th, e)))
        if '-v' in sys.argv:
            for p, ri in zip(pts, r):
                print(f"          {p['A']:4d} {str([q for q in p['loops'] if q <= 20]):16s} {p['y']:.4f} {ri:+.1f}")
