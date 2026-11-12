"""Shared analysis: layer death times from rep.c output, firewalls, censored exponential fits."""
import numpy as np
from scipy import stats

INF = np.inf


def death_times(la, gen_end):
    """la: [R, nL] last-alive gens. Death time = la + 1 (resolution K) if the layer is dead at the end, else inf."""
    d = (la + 1).astype(float)
    d[la >= gen_end] = INF
    return d


def ring_firewall(D, ring):
    """D: [R, n] death times of the layers of one diagonal, in ring order (circular if ring) -> [R] first time
    three consecutive layers are all dead (T3), inf if never."""
    n = D.shape[1]
    idx = range(n) if ring else range(n - 2)
    best = np.full(D.shape[0], INF)
    for i in idx:
        t = np.max(D[:, [i, (i + 1) % n, (i + 2) % n]], axis=1)
        best = np.minimum(best, t)
    return best


def exp_fit(t, observed):
    """Censored exponential MLE. t: times (event or censoring), observed: bool.
    Returns mean, (lo, hi) 95% CI, number of events."""
    t = np.asarray(t, float); observed = np.asarray(observed, bool)
    k, T = observed.sum(), t.sum()
    if k == 0:
        return INF, (2 * T / stats.chi2.ppf(0.95, 2), INF), 0  # one-sided 95% lower bound T/3
    lo = 2 * T / stats.chi2.ppf(0.975, 2 * k + 2)
    hi = 2 * T / stats.chi2.ppf(0.025, 2 * k) if k > 0 else INF
    return T / k, (lo, hi), int(k)


def exp_tests(t):
    """Uncensored sample: CV, KS p-value against a shifted exponential (shift = min, fitted mean)."""
    t = np.sort(np.asarray(t, float))
    cv = t.std() / t.mean()
    t0 = t[0]
    p = stats.kstest(t - t0, 'expon', args=(0, (t - t0).mean())).pvalue
    return cv, p
