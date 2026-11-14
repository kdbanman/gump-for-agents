#!/usr/bin/env python3
"""Verdict 2 of research/theory/exponent.md (section 4): tau_edge(L) = 12.1 / E(L - 6.5).

  python3 verdict2.py fit           the two-constant fit on the filed E(l) (exponent/data/gap.json): profile in the
                                    shift, leave-out predictions, comparison with other curves
  python3 verdict2.py errors [FILE] errors of the window cost.  (a) filed counts: compound-Poisson error from the
                                    run-length structure (spatial overlap only; a lower bound).  (b) FILE = output of
                                    toygap.c (batches): batch-to-batch scatter, which includes the time correlation.
Lifetimes: this study's 16 x L strips L = 12-28 (scratch/exponent/runs_truth.json, as tabulated in section 2) and
toy2d's L = 32, 36 (research/toy2d/data/law_cross2_B34S234.json).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
GAP = json.load(open(os.path.join(ROOT, 'theory', 'exponent', 'data', 'gap.json')))
LT = [(12, 5.6444, 0.0134), (16, 7.4070, 0.0108), (20, 9.1423, 0.0108), (24, 10.7883, 0.0119), (28, 12.4337, 0.0179)]
T2 = {r['L']: (r['lntau'], r['err']) for r in json.load(open(os.path.join(ROOT, 'toy2d', 'data', 'law_cross2_B34S234.json')))['rows']}
LT += [(32,) + T2[32], (36,) + T2[36]]


def lnE_interp(E):
    lE = np.log(np.asarray(E))
    def f(x):
        i = int(np.floor(x)); t = x - i
        return (1 - t) * lE[i] + t * lE[i + 1]
    return f


def fit(pts, f, s):
    L, y, e = np.array(pts).T
    z = np.array([-f(l - s) for l in L])          # ln tau = c + z
    wts = 1 / e ** 2
    c = np.sum(wts * (y - z)) / np.sum(wts)
    r = y - z - c
    return c, r, float(np.sum(wts * r ** 2))


def best(pts, f, grid=np.arange(3.0, 10.01, 0.05)):
    out = [(fit(pts, f, s)[2], s) for s in grid]
    chi, s = min(out)
    return s, chi, out


def do_fit():
    f = lnE_interp(GAP['gap_H16_L128']['E'])
    s, chi, prof = best(LT, f)
    c, r, _ = fit(LT, f, s)
    print('all seven: best shift %.2f, prefactor exp(c) = %.2f, chi2 = %.1f / 5; residuals %s' %
          (s, np.exp(c), chi, ' '.join('%+.3f' % v for v in r)))
    c, r, chi65 = fit(LT, f, 6.5)
    print('shift 6.5 (the report): prefactor %.2f, chi2 %.1f / 5, residuals %s' % (np.exp(c), chi65, ' '.join('%+.3f' % v for v in r)))
    lo = [ss for ch, ss in prof if ch <= chi + max(1.0, chi / 5)]
    print('shift range with chi2 <= min + max(1, chi2/dof): %.2f - %.2f (scale-corrected 1 sigma)' % (min(lo), max(lo)))
    for ss in (3, 4, 5, 6, 6.5, 7, 8, 9, 10):
        print('   shift %4.1f: chi2 %.1f   prefactor %.1f' % (ss, fit(LT, f, ss)[2], np.exp(fit(LT, f, ss)[0])))
    # out of sample: fit on this study's five points (L = 12-28), predict toy2d's L = 32, 36
    s5, chi5, _ = best(LT[:5], f)
    c5, r5, _ = fit(LT[:5], f, s5)
    print('fit on L = 12-28 only: shift %.2f, prefactor %.2f, chi2 %.1f / 3' % (s5, np.exp(c5), chi5))
    for L, y, e in LT[5:]:
        pred = c5 - f(L - s5)
        print('   predict L = %d: %.3f, measured %.3f +- %.3f, residual %+.3f' % (L, pred, y, e, y - pred))
    c5b, _, _ = fit(LT[:5], f, 6.5)
    for L, y, e in LT[5:]:
        print('   (shift fixed at 6.5, prefactor from L = 12-28) predict L = %d: %.3f, residual %+.3f' % (L, c5b - f(L - 6.5), y - (c5b - f(L - 6.5))))
    # comparison curves on the same seven points
    L, y, e = np.array(LT).T; w = 1 / e ** 2
    for name, X in (('a + bL', np.c_[np.ones(7), L]), ('a + bL + c lnL', np.c_[np.ones(7), L, np.log(L)]),
                    ('a + bL + c/L', np.c_[np.ones(7), L, 1 / L])):
        beta = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
        res = y - X @ beta
        print('%-16s chi2 %.1f / %d  coeffs %s' % (name, np.sum(w * res ** 2), 7 - X.shape[1], ' '.join('%.4f' % b for b in beta)))
    # the same two-constant fit with the eight-row model's and the one-row model's windows
    for key in ('gap_w8_L128', 'gap_w1_L128'):
        g = lnE_interp(GAP[key]['E'])
        n = len(GAP[key]['E']) - 1
        pts = [p for p in LT if p[0] - 3 <= n - 1]
        sk, chik, _ = best(pts, g)
        ck, rk, _ = fit(pts, g, sk)
        print('%s windows: best shift %.2f prefactor %.2f chi2 %.1f on %d points, residuals %s' % (key, sk, np.exp(ck), chik, len(pts), ' '.join('%+.2f' % v for v in rk)))


def compound_poisson(counts, a, b):
    """counts[l] = windows of length l (filed).  Runs of exactly r empty cells: n_r = c_r - 2 c_{r+1} + c_{r+2}.
    Error of (ln c_a - ln c_b) / (b - a) if every maximal empty run were independent (Poisson in number)."""
    c = np.asarray(counts, float); top = len(c) - 3
    n = np.array([c[r] - 2 * c[r + 1] + c[r + 2] if r <= top else 0 for r in range(len(c))])
    n = np.clip(n, 0, None)
    var = 0.0
    for r in range(len(c)):
        if n[r] <= 0:
            continue
        ga = (r - a + 1) / c[a] if r >= a else 0.0
        gb = (r - b + 1) / c[b] if r >= b else 0.0
        var += n[r] * (ga - gb) ** 2
    return np.sqrt(var) / (b - a), (c[a] - c[a + 1]) if a + 1 < len(c) else float('nan')


def do_errors(fn=None):
    c = GAP['gap_H16_L128']['counts']
    print('filed counts (16 x 128 strips), spatial-overlap error only:')
    for a, b in ((10, 11), (20, 21), (30, 31), (34, 42), (42, 50), (34, 41)):
        if b < len(c):
            err, runs = compound_poisson(c, a, b)
            cost = (np.log(c[a]) - np.log(c[b])) / (b - a)
            print('   window cost %d -> %d: %.4f +- %.4f   (maximal empty runs of length >= %d: %.0f)' % (a, b, cost, err, a, runs))
    if not fn:
        return
    rows = []
    for line in open(fn):
        v = line.split('|')[0].split()
        rows.append([float(t) for t in v])
    A = np.array(rows); N = A[:, 1]; C = A[:, 2:]
    tot = C.sum(0); Ntot = N.sum()
    print('own run %s: %d batches of %.0f generations, %.3g window samples' % (fn, len(A), A[0, 0], Ntot))
    E = tot / Ntot
    print('   E(1) = %.4f (filed %.4f)' % (E[0], GAP['gap_H16_L128']['E'][1]))
    nb = len(A)
    for a, b in ((10, 11), (20, 21), (30, 31), (34, 42), (42, 50), (34, 41)):
        if tot[b - 1] < 30:
            print('   %d -> %d: too few windows' % (a, b)); continue
        cost = (np.log(tot[a - 1]) - np.log(tot[b - 1])) / (b - a)
        # jackknife over batches
        jk = []
        for k in range(nb):
            ta, tb = tot[a - 1] - C[k, a - 1], tot[b - 1] - C[k, b - 1]
            jk.append((np.log(ta) - np.log(tb)) / (b - a))
        jk = np.array(jk); se = np.sqrt((nb - 1) / nb * np.sum((jk - jk.mean()) ** 2))
        filed = (np.log(c[a]) - np.log(c[b])) / (b - a) if b < len(c) else float('nan')
        print('   window cost %d -> %d: %.4f +- %.4f (jackknife over batches)   filed %.4f   windows of length %d: %.0f' %
              (a, b, cost, se, filed, b, tot[b - 1]))
    # the formula with my own E
    f = lnE_interp(np.r_[1.0, E])
    usable = [p for p in LT if p[0] - 6.5 + 1 < len(E)]
    c0, r, chi = fit(usable, f, 6.5)
    print('   tau = %.2f / E(L - 6.5) with my E: chi2 %.1f, residuals %s' % (np.exp(c0), chi, ' '.join('%+.3f' % v for v in r)))


if __name__ == '__main__':
    if sys.argv[1] == 'fit':
        do_fit()
    elif sys.argv[1] == 'errors':
        do_errors(sys.argv[2] if len(sys.argv) > 2 else None)
