#!/usr/bin/env python3
"""Weighted least squares for research/constant/: linear and nonlinear models, chi-square, residuals, forecasts.

A model is a function f(theta, point) -> predicted ln tau.  fit() minimises sum(((y - f)/se)^2) and returns the
parameters, their covariance (from the Jacobian at the minimum, NOT inflated), chi2 and dof.  forecast() gives the
prediction for unseen points with the parameter error propagated; `inflate=True` multiplies the parameter covariance
by max(1, chi2/dof), the usual allowance for a model that does not fit its own data.
"""
import math
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2dist


class Fit:
    def __init__(self, name, f, theta, cov, chi2, dof, pts, names):
        self.name, self.f, self.theta, self.cov, self.chi2, self.dof, self.pts, self.names = \
            name, f, theta, cov, chi2, dof, pts, names

    @property
    def p(self):
        return float(chi2dist.sf(self.chi2, self.dof)) if self.dof > 0 else float('nan')

    def err(self, i, inflate=False):
        s = math.sqrt(max(self.cov[i, i], 0.0))
        return s * (math.sqrt(max(1.0, self.chi2 / self.dof)) if inflate and self.dof > 0 else 1.0)

    def par(self, name):
        i = self.names.index(name)
        return self.theta[i], self.err(i), self.err(i, True)

    def resid(self):
        return [(p, p['y'] - self.f(self.theta, p), (p['y'] - self.f(self.theta, p)) / p['se']) for p in self.pts]

    def predict(self, p, inflate=True):
        """prediction and its 1-sigma parameter error at point p (numerical gradient)."""
        y0 = self.f(self.theta, p)
        g = np.zeros(len(self.theta))
        for i in range(len(self.theta)):
            h = 1e-6 * max(1.0, abs(self.theta[i]))
            t = np.array(self.theta, float); t[i] += h
            g[i] = (self.f(t, p) - y0) / h
        var = float(g @ self.cov @ g)
        if inflate and self.dof > 0:
            var *= max(1.0, self.chi2 / self.dof)
        return y0, math.sqrt(max(var, 0.0))

    def summary(self, inflate_note=True):
        ps = ', '.join(f'{n} = {v:.5g} +- {self.err(i):.2g}' for i, (n, v) in enumerate(zip(self.names, self.theta)))
        verdict = 'fits' if (self.dof > 0 and self.p >= 0.01) else ('FAILS (p < 0.01)' if self.dof > 0 else 'no dof')
        return (f'{self.name}: chi2 = {self.chi2:.1f} / {self.dof} (p = {self.p:.2g}) {verdict}; {ps}')


def fit(name, f, theta0, pts, names, bounds=None):
    y = np.array([p['y'] for p in pts]); se = np.array([p['se'] for p in pts])

    def res(t):
        return np.array([(yy - f(t, p)) / s for yy, p, s in zip(y, pts, se)])
    kw = dict(x_scale='jac', xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=20000)
    if bounds is not None:
        kw['bounds'] = bounds
    r = least_squares(res, np.array(theta0, float), **kw)
    J = r.jac
    try:
        cov = np.linalg.inv(J.T @ J)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(J.T @ J)
    chi2 = float((r.fun ** 2).sum())
    return Fit(name, f, r.x, cov, chi2, len(pts) - len(theta0), pts, names)


def score(fitobj, pts, inflate=True, floor=0.0):
    """Out-of-sample score: for each unseen point z = (y - forecast)/sqrt(se^2 + forecast error^2 + floor^2).
    Returns (list of (point, forecast, ferr, resid, z), sum z^2, rms residual, mean residual)."""
    rows = []
    for p in pts:
        yf, ef = fitobj.predict(p, inflate)
        r = p['y'] - yf
        z = r / math.sqrt(p['se'] ** 2 + ef ** 2 + floor ** 2)
        rows.append((p, yf, ef, r, z))
    n = max(len(rows), 1)
    return rows, sum(z * z for *_, z in rows), math.sqrt(sum(r * r for *_, r, _ in rows) / n), \
        sum(r for *_, r, _ in rows) / n
