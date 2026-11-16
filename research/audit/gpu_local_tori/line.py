#!/usr/bin/env python3
"""line.py: the card's five equilateral tori against a line and against forms with a decaying correction, and what
each form predicts for A = 81, 84, 108, 111.

    python3 line.py            # -> line_out.txt

Input: the five values recomputed from the card's csv rows at b843883 (ln(2E/F), error 1/sqrt(F)); A = 57 also with
its error scaled by sqrt(chi2) of its two seeds (6.9 on 1). Shortest loop l = sqrt(n) = sqrt(A/3) (checked below
from the lattices: every one has exactly 6 shortest vectors of Q(x, y) = x^2 + xy + y^2 = n).
Prediction errors: from the fit covariance (Jacobian), scaled by sqrt(chi2/dof) when that exceeds 1; for forms with
no degrees of freedom left the error is the covariance alone.
"""
import math
import numpy as np
from scipy.optimize import curve_fit

LAT = {48: (4, 0, 4), 57: (1, 7, 19), 63: (1, 4, 21), 75: (5, 0, 5), 93: (1, 5, 31),
       81: (3, 3, 9), 84: (2, 4, 14), 108: (6, 0, 6), 111: (1, 10, 37)}
VAL = {48: (9.9251, 0.0004), 57: (11.8756, 0.0006), 63: (13.1622, 0.0007), 75: (15.6630, 0.0023), 93: (19.4141, 0.0053)}
NEW = [81, 84, 108, 111]
CARD = {81: (16.913, 0.006), 84: (17.539, 0.007), 108: (22.540, 0.014), 111: (23.165, 0.015)}   # its block 3


def shortest(a, k, b):
    vs = [(x * a, x * k + y * b) for x in range(-12, 13) for y in range(-12, 13) if (x, y) != (0, 0)]
    q = sorted(u * u + u * v + v * v for u, v in vs)
    return q[0], sum(1 for z in q if z == q[0])


def fit(f, p0, A, y, e, names):
    p, C = curve_fit(f, A, y, p0=p0, sigma=e, absolute_sigma=True, maxfev=200000)
    chi2 = float((((f(A, *p) - y) / e) ** 2).sum()); dof = len(A) - len(p)
    s = math.sqrt(max(1.0, chi2 / dof)) if dof > 0 else 1.0
    pred = {}
    for a in NEW:
        g = np.zeros(len(p)); h = 1e-6
        for i in range(len(p)):
            dp = np.array(p, float); dp[i] += h * max(1, abs(p[i]))
            g[i] = (f(np.array([a]), *dp)[0] - f(np.array([a]), *p)[0]) / (h * max(1, abs(p[i])))
        pred[a] = (float(f(np.array([a]), *p)[0]), s * math.sqrt(max(0.0, g @ C @ g)))
    return p, np.sqrt(np.diag(C)), chi2, dof, pred


def main():
    out = []
    pr = out.append
    for A, (a, k, b) in sorted(LAT.items()):
        q, m = shortest(a, k, b)
        assert q == A // 3 and m == 6, (A, q, m)
    pr('lattices: every one has 6 shortest vectors of norm^2 n = A/3 (equilateral), loop l = sqrt(A/3)')
    for tag, e57 in (('errors as recomputed', 0.0006), ('A = 57 error scaled by sqrt(6.9)', 0.0006 * math.sqrt(6.9))):
        V = dict(VAL); V[57] = (VAL[57][0], e57)
        pr(f'\n=== {tag} ===')
        A3 = np.array([63, 75, 93.]); y3 = np.array([V[a][0] for a in A3]); e3 = np.array([V[a][1] for a in A3])
        lin = lambda A, a0, c: a0 + c * A
        p, pe, chi2, dof, pred = fit(lin, [0, 0.2], A3, y3, e3, 'a c')
        pr(f'line through 63, 75, 93: c = {p[1]:.5f} +- {pe[1]:.5f}, a = {p[0]:.4f}; chi2 = {chi2:.4f} on {dof} '
           f'(p = {1 - math.erf(math.sqrt(chi2 / 2)):.3f} upper; P(chi2 <= this) = {math.erf(math.sqrt(chi2 / 2)):.3f})')
        for a in (48, 57):
            m = lin(a, *p); pr(f'  deficit at {a}: {V[a][0] - m:+.4f} (line {m:.4f})')
        s1 = (V[75][0] - V[63][0]) / 12; s2 = (V[93][0] - V[75][0]) / 18
        es = math.hypot(math.hypot(V[75][1], V[63][1]) / 12, 0); e2 = math.hypot(V[93][1], V[75][1]) / 18
        cov = -V[75][1] ** 2 / (12 * 18)
        ed = math.sqrt(es ** 2 + e2 ** 2 - 2 * cov)
        pr(f'  slopes 63->75 {s1:.5f} +- {es:.5f}, 75->93 {s2:.5f} +- {e2:.5f}; difference {s2 - s1:+.5f} +- {ed:.5f} '
           f'(2 sigma bound on a change of slope above 63: {2 * ed:.5f})')
        pr('  predictions of this line: ' + ', '.join(f'{a}: {pred[a][0]:.3f} +- {pred[a][1]:.3f}' for a in NEW))
        quad = lambda A, a0, c, kap: a0 + c * A + kap * (A - 63) * (A - 93)
        p, pe, chi2, dof, pred = fit(quad, [0, 0.2, 0], A3, y3, e3, '')
        pr(f'C: quadratic through 63, 75, 93 (curvature free, 0 dof): kappa = {p[2]:.2e} +- {pe[2]:.2e}; predictions: '
           + ', '.join(f'{a}: {pred[a][0]:.3f} +- {pred[a][1]:.3f}' for a in NEW))
        A5 = np.array(sorted(V), float); y5 = np.array([V[a][0] for a in A5]); e5 = np.array([V[a][1] for a in A5])
        L = lambda A: np.sqrt(A / 3.0)
        NOCUT = lambda A: np.isin(np.round(A), [57, 63, 93, 111]).astype(float)
        forms = [   # name, f(A, linear..., theta), number of linear params, theta grid (profiled), or None
            ('E: a + cA - g exp(-(l - 4)/lam)', lambda A, a0, c, g, lam: a0 + c * A - g * np.exp(-(L(A) - 4) / lam),
             np.geomspace(0.02, 20, 400)),
            ('P: a + cA - g (48/A)^q', lambda A, a0, c, g, q: a0 + c * A - g * (48.0 / A) ** q, np.geomspace(0.1, 200, 400)),
            ('M: a + A [c - g exp(-l/xi)] (per-cell price, massive-like, xi free)',
             lambda A, a0, c, g, xi: a0 + A * (c - g * np.exp(-L(A) / xi)), np.geomspace(0.02, 20, 400)),
            ('Q: a + cA + g1/A + g2/A^2', lambda A, a0, c, g1, g2: a0 + c * A + g1 / A + g2 / A ** 2, None),
            ('S: a + cA - g exp(-(A/A0)^6) (stretched; decays far faster than exponential)',
             lambda A, a0, c, g, A0: a0 + c * A - g * np.exp(-(A / A0) ** 6), np.linspace(20, 120, 1001)),
            ('H: a + cA - g max(0, A0 - A)^2 (quadratic hinge: straight above A0)',
             lambda A, a0, c, g, A0: a0 + c * A - g * np.maximum(0, A0 - A) ** 2, np.linspace(57.5, 80, 451)),
            ('B: a + cA - g max(0, A0 - A) (broken line, kink at A0: the card\'s reading)',
             lambda A, a0, c, g, A0: a0 + c * A - g * np.maximum(0, A0 - A), np.linspace(57.05, 62.95, 591)),
            ('K: a + cA + d [no cut] - g exp(-(l - 4)/lam) (two kinds; 0 dof)',
             lambda A, a0, c, d, g, lam: a0 + c * A + d * NOCUT(A) - g * np.exp(-(L(A) - 4) / lam), np.geomspace(0.02, 20, 400)),
        ]
        for name, f, grid in forms:
            npar = f.__code__.co_argcount - 1
            if grid is not None:                       # profile the last (nonlinear) parameter on a grid, linear LS inside
                best = None
                for th in grid:
                    X = np.stack([(f(A5, *np.eye(npar - 1)[i], th) - f(A5, *np.zeros(npar - 1), th)) for i in range(npar - 1)], 1)
                    y0 = f(A5, *np.zeros(npar - 1), th)
                    beta, *_ = np.linalg.lstsq(X / e5[:, None], (y5 - y0) / e5, rcond=None)
                    c2 = float((((X @ beta + y0) - y5) / e5) ** 2 @ np.ones(len(y5)))
                    if best is None or c2 < best[0]:
                        best = (c2, list(beta) + [th])
                p0 = best[1]
            else:
                p0 = [0, 0.21, 0, 0]
            try:
                p, pe, chi2, dof, pred = fit(f, p0, A5, y5, e5, '')
            except Exception as ex:                                    # noqa: BLE001
                pr(f'{name}: fit failed ({ex})'); continue
            res = ' '.join(f'{(y - f(np.array([a]), *p)[0]) / e:+.1f}' for a, y, e in zip(A5, y5, e5))
            sl = [(f(np.array([b]), *p)[0] - f(np.array([a]), *p)[0]) / (b - a) for a, b in ((63, 75), (75, 93), (93, 111))]
            pr(f'{name}\n  params {np.array2string(p, precision=5)} +- {np.array2string(pe, precision=5)}; chi2 {chi2:.3f} on {dof}; '
               f'residuals/sigma {res}\n  model slopes 63->75 {sl[0]:.5f}, 75->93 {sl[1]:.5f}, 93->111 {sl[2]:.5f}\n  predictions: '
               + ', '.join(f'{a}: {pred[a][0]:.3f} +- {pred[a][1]:.3f}' for a in NEW))
    pr('\ncard block 3: ' + ', '.join(f'{a}: {v:.3f} +- {e:.3f}' for a, (v, e) in CARD.items()))
    txt = '\n'.join(out); print(txt)
    return txt


if __name__ == '__main__':
    import os
    t = main()
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'line_out.txt'), 'w').write(t + '\n')
