#!/usr/bin/env python3
"""Post-hoc model (not forecast): the face death rate as a bulk term plus a sum over closed loops,
    1/tau = alpha_A + beta_A * sum over primitive lattice vectors v (mod sign) of exp(-kappa |v|),
|v| in units of |u1|, kappa shared by both areas. Fitted to the shape means of data/A72.csv and data/A60.csv.
Also: "systole only" with exp(-kappa * systole) for comparison (same parameter count).

    python3 research/shape/loopsum.py
"""
import csv, math, os, sys
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fits import group_chi2  # noqa: E402

shapes = []
for A in (72, 60):
    rows = list(csv.DictReader(open(os.path.join(HERE, 'data', f'A{A}.csv'))))
    _, _, _, means = group_chi2(rows, lambda r: r['gram'])
    for g, (m, e, n) in means.items():
        r = next(r for r in rows if r['gram'] == g)
        a, k, b = int(r['a']), int(r['k']), int(r['b'])
        L = []
        for p in range(-40, 41):
            for q in range(-40, 41):
                if math.gcd(p, q) != 1 or (p, q) <= (0, 0) and not (p == 0 and q > 0):
                    continue
                if p < 0 or (p == 0 and q < 0):
                    continue
                x, y = p * a, p * k + q * b
                L.append(math.sqrt(x * x + x * y + y * y))
        shapes.append((A, g, m, e, np.array(sorted(L))[:400], int(r['systole2'])))


def model(par, loops=True):
    k = par[4]
    out = []
    for A, g, m, e, L, s2 in shapes:
        al, be = (par[0], par[1]) if A == 72 else (par[2], par[3])
        S = np.exp(-k * L).sum() if loops else math.exp(-k * math.sqrt(s2))
        out.append(-math.log(math.exp(al) + math.exp(be) * S))
    return np.array(out)


for loops in (True, False):
    y = np.array([s[2] for s in shapes]); e = np.array([s[3] for s in shapes])
    best = None
    for k0 in (0.5, 1, 2, 3, 5):
        r = least_squares(lambda p: (model(p, loops) - y) / e, [-15.2, -12, -12.7, -10, k0])
        if best is None or r.cost < best.cost:
            best = r
    chi = 2 * best.cost
    print(f'{"loop sum" if loops else "systole only"}: chi2 {chi:.2f} / {len(y) - 5}; kappa {best.x[4]:.3f}')
    for s, mod in zip(shapes, model(best.x, loops)):
        print(f'   A={s[0]} {s[1]:10s} sys2 {s[5]:2d}  {s[2]:.3f} ± {s[3]:.3f}  model {mod:.3f}  ({(s[2] - mod) / s[3]:+.1f} sd)')
