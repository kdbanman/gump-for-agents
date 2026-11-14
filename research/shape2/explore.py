#!/usr/bin/env python3
"""Post-hoc (not forecast) descriptions of ln tau_face over all measured classes: loop sums with several decay
functions, fitted per area and jointly, on subsets by systole; and the cost per cell by systole between areas.

    python3 research/shape2/explore.py
"""
import math, os, sys
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as C2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze2 import points  # noqa: E402
from laws import all_lengths  # noqa: E402
from lattice2 import invariants  # noqa: E402

G = {'exp': lambda L, K: np.exp(-K * L), 'pow': lambda L, K: L ** -K, 'gauss': lambda L, K: np.exp(-(K * L) ** 2),
     'exp/L': lambda L, K: np.exp(-K * L) / L}


def fit(pts, g, scale, prim=True):
    keys = sorted(pts); y = np.array([pts[k][0] for k in keys]); e = np.array([pts[k][1] for k in keys])
    areas = sorted({k[0] for k in keys})
    Ls = [all_lengths(c)[1 if prim else 0] for _, c in keys]
    amp = np.array([(A / 72 if scale == 'area' else 1.0) for A, _ in keys])

    def model(p):
        f = -math.exp(p[0]) * amp * np.array([G[g](L, p[1]).sum() for L in Ls])
        out = np.empty_like(f)
        for A in areas:
            m = np.array([k[0] == A for k in keys]); w = 1 / e[m] ** 2
            out[m] = f[m] + (w * (y[m] - f[m])).sum() / w.sum()
        return out
    best = None
    for K0 in ((2.5, 4, 8) if g == 'pow' else (0.2, 0.5, 1, 2, 3)):
        for lB in (-4, 0, 3, 6):
            try:
                r = least_squares(lambda p: (model(p) - y) / e, [lB, K0],
                                  bounds=([-20, 2.01 if g == 'pow' else 0.01], [40, 40]))
            except Exception:
                continue
            if best is None or r.cost < best.cost:
                best = r
    dof = len(y) - 2 - len(areas)
    res = (y - model(best.x)) / e
    return 2 * best.cost, dof, best.x, dict(zip(keys, res))


if __name__ == '__main__':
    allp = points(min_l1=3)
    # review's independent A = 72 values could be pooled; not done here (research/shape's values as published)
    print('cost per cell between areas, by systole^2 (classes pooled within area by inverse variance):')
    by = {}
    for (A, c), (v, e) in allp.items():
        by.setdefault((invariants(*c)['l1'], A), []).append((v, e))
    for q in sorted({q for q, _ in by}):
        vals = {}
        for A in (48, 60, 72):
            if (q, A) in by:
                w = [1 / e ** 2 for _, e in by[(q, A)]]
                vals[A] = (sum(wi * v for wi, (v, _) in zip(w, by[(q, A)])) / sum(w), 1 / math.sqrt(sum(w)))
        s = '  '.join(f'A={A}: {v:.4f}±{e:.4f}' for A, (v, e) in vals.items())
        sl = []
        As = sorted(vals)
        for A0, A1 in zip(As, As[1:]):
            sl.append(f'b({A0}-{A1}) {(vals[A1][0] - vals[A0][0]) / (A1 - A0):.4f}±'
                      f'{math.hypot(vals[A1][1], vals[A0][1]) / (A1 - A0):.4f}')
        print(f'  sys2 {q:2d}: {s}   ' + ' '.join(sl))
    for lo in (12, 7, 3):
        for areas in ((48,), (60,), (72,), (48, 60, 72)):
            pts = {k: v for k, v in allp.items() if k[0] in areas and invariants(*k[1])['l1'] >= lo}
            if len(pts) - 2 - len(areas) < 1:
                continue
            out = []
            for g in G:
                for scale in (('const', 'area') if len(areas) > 1 else ('const',)):
                    x, d, p, res = fit(pts, g, scale)
                    out.append((x, f'{g}-{scale}: {x:.1f}/{d} (p {C2.sf(x, d):.2g}; K {p[1]:.2f})'))
            out.sort()
            print(f'\nsys2 >= {lo}, A in {areas}, {len(pts)} classes: ' + ';  '.join(s for _, s in out))
    # residuals of the best joint form for sys2 >= 7
    pts = {k: v for k, v in allp.items() if invariants(*k[1])['l1'] >= 7}
    x, d, p, res = fit(pts, 'exp', 'area')
    print(f'\nresiduals, exp-area loop sum, sys2 >= 7 (chi2 {x:.1f}/{d}):')
    for (A, c), r in sorted(res.items()):
        inv = invariants(*c)
        print(f'  A={A} {str(c):12s} loops {inv["loops"][:4]} angle {inv["angle"]:.0f}  {allp[(A, c)][0]:.4f}  resid {r:+.1f} sd')
