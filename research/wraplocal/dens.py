#!/usr/bin/env python3
"""The image-sum model of a local statistic and its relation to the price (research/wraplocal).

Model (IMG): on a face torus with period lattice Lambda, a statistic s (default: face-layer density) is
    s(torus) = s_inf - sum over v in Lambda \\ 0, one per +-v, of f(|v|^2)
with f free for each |v|^2 <= QF and zero beyond (linear least squares, weights from the block errors).
Inputs: every torus with live.py runs (ana.summary).

    python3 research/wraplocal/dens.py [STAT]          # STAT one of ana.py's keys (default rho_face)
    python3 research/wraplocal/dens.py rho_face --price  # also the relation to the tube prices (CLAIMS WL3)
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ana  # noqa: E402
import lattices as L  # noqa: E402  (research/wrap, via ana's path)

QS = [9, 12, 13, 16, 19, 21, 25, 27, 28, 31, 36, 37, 39]
SIGN = {}     # statistics that rise with the deficit get sign -1 in the printout only


def counts(h, k, d):
    lp = L.loops(h, k, d, cap=max(QS))
    return np.array([lp.count(q) for q in QS], float)


def data(stat):
    rows = []
    for t in ana.tori_with_runs():
        r = ana.summary(*t)
        m, e = r[stat]
        rows.append((t, 3 * t[0] * t[2], counts(*t), m, e, r['_nb']))
    return rows


def fit(rows, qs_free):
    idx = [QS.index(q) for q in qs_free]
    X = np.array([[1.0] + [-r[2][i] for i in idx] for r in rows])
    y = np.array([r[3] for r in rows]); se = np.array([r[4] for r in rows])
    se = np.maximum(se, 1e-6)
    Wt = 1 / se
    b, *_ = np.linalg.lstsq(X * Wt[:, None], y * Wt, rcond=None)
    cov = np.linalg.inv((X * Wt[:, None]).T @ (X * Wt[:, None]))
    res = (y - X @ b) / se
    return b, np.sqrt(np.diag(cov)), res, cov


# tube prices per cell (CLAIMS WL3; python3 research/audit/wrap_haz_lead.py --tube)
PRICE = {None: (0.20864, 0.00009), 12: (0.20437, 0.00016), 13: (0.20602, 0.00033), 16: (0.20717, 0.00011),
         19: (0.20898, 0.00120)}


if __name__ == '__main__':
    stat = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else 'rho_face'
    rows = data(stat)
    present = [q for i, q in enumerate(QS) if any(r[2][i] for r in rows)]
    b, e, res, cov = fit(rows, present)
    print(f'statistic {stat}: IMG fit on {len(rows)} tori, free f(q) for q in {present}; chi2 {res @ res:.1f} on '
          f'{len(rows) - len(present) - 1}')
    print(f'   s_inf = {b[0]:.6f} ± {e[0]:.6f}')
    for q, bi, ei in zip(present, b[1:], e[1:]):
        print(f'   f({q:2d}) = {bi:+.6f} ± {ei:.6f}   ln|f| = {np.log(abs(bi)) if bi else float("nan"):+.3f}   |v| = {q ** 0.5:.3f}')
    print('   torus         A   loops<=39                       measured            IMG       z')
    for r, z in zip(rows, res):
        lp = L.loops(*r[0], cap=39)
        print(f'   {str(r[0]):12s} {r[1]:3d}  {str(lp):30s} {r[3]:.6f} ± {r[4]:.6f}  {r[3] - z * max(r[4], 1e-6):.6f}  {z:+5.1f}')
    if '--price' in sys.argv:
        fq = dict(zip(present, b[1:])); eq = dict(zip(present, e[1:]))
        print('\nprice relation  c_q = c_open - kappa f(q), kappa fixed on loop^2 12 and 16 (weighted), forecast 13 and 19')
        dc = {q: (PRICE[None][0] - PRICE[q][0], np.hypot(PRICE[None][1], PRICE[q][1])) for q in (12, 13, 16, 19)}
        num = sum(dc[q][0] * fq[q] / dc[q][1] ** 2 for q in (12, 16)); den = sum(fq[q] ** 2 / dc[q][1] ** 2 for q in (12, 16))
        kap = num / den
        kerr = den ** -0.5
        print(f'   kappa = {kap:.3f} ± {kerr:.3f} (price errors only)')
        for q in (12, 13, 16, 19):
            fc = kap * fq[q]
            ferr = np.hypot(kap * eq[q], kerr * fq[q])
            print(f'   loop^2 {q}: discount measured {dc[q][0]:.5f} ± {dc[q][1]:.5f}, kappa f = {fc:.5f} ± {ferr:.5f}, '
                  f'(m - f)/sigma = {(dc[q][0] - fc) / np.hypot(dc[q][1], ferr):+.1f}')
        for q in present:
            if q not in (12, 13, 16, 19):
                print(f'   forecast loop^2 {q}: discount {kap * fq[q]:+.5f} ± {np.hypot(kap * eq[q], kerr * fq[q]):.5f} per cell '
                      f'-> price {PRICE[None][0] - kap * fq[q]:.5f}')
        print(f'   open price from the same relation through zero would need s_inf * kappa = {b[0] * kap:.4f} '
              f'(measured {PRICE[None][0]})')
