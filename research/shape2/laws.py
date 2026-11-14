#!/usr/bin/env python3
"""Candidate laws for ln tau_face at fixed area as a function of the period lattice; fitted on the PUBLISHED values
only (research/shape/data/A72.csv, A60.csv, presentations pooled per class), then evaluated on every class at
A = 48, 60, 72.

    python3 research/shape2/laws.py              # fits on published data + prediction table (PREDICTIONS.md)
    python3 research/shape2/laws.py --json F     # also write predictions to F

Lengths |v| in units of |u1| (|v|^2 = Q). Within each area the constant c(A) is free (one per area); the laws differ
in the shape term f, ln tau = c(A) + f(lattice; A):
  L1  f = -B * exp(-K s1)                                         s1 = shortest loop length
  L2  f = -B * (exp(-K s1) + exp(-K s2))                          s1, s2 successive minima
  L3  f = -B * sum over primitive v (mod sign) exp(-K |v|)
  L4  f = -B * (A/72) * sum over all v != 0 (mod sign) exp(-K |v|) / |v|     (finite-size term of a gapped field
      on a torus: extensive in A, one term per winding vector; prefactor 1/|v| chosen before fitting)
For L1-L3 two scalings across areas are fitted: amplitude B the same at every area ('const'), or B ∝ A ('area').
"""
import csv, json, math, os, sys
import numpy as np
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice2 import cls, classes, invariants, Q  # noqa: E402


def published():
    out = {}
    for A in (72, 60):
        rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'shape', 'data', f'A{A}.csv'))))
        g = {}
        for r in rows:
            c = cls(int(r['a']), int(r['k']), int(r['b']))
            g.setdefault(c, [0.0, 0])
            g[c][0] += float(r['exposure']); g[c][1] += int(r['face_deaths'])
        for c, (E, F) in g.items():
            out[(A, c)] = (math.log(2 * E / F), 1 / math.sqrt(F))
    return out


def all_lengths(c, Lmax=12.0):
    """lengths of all nonzero lattice vectors mod sign with |v| <= Lmax, and the primitive ones"""
    a, k, b = c
    R = int(Lmax * 2) + 2
    allv, prim = [], []
    for p in range(0, R + 1):
        for q in range(-3 * R, 3 * R + 1):
            if p == 0 and q <= 0:
                continue
            x, y = p * a, p * k + q * b
            L = math.sqrt(Q(x, y))
            if L <= Lmax:
                allv.append(L)
                if math.gcd(p, abs(q)) == 1:
                    prim.append(L)
    return np.array(sorted(allv)), np.array(sorted(prim))


def shape_term(law, c, A, B, K, scale):
    inv = invariants(*c)
    s1, s2 = math.sqrt(inv['l1']), math.sqrt(inv['l2'])
    amp = B * (A / 72 if scale == 'area' else 1.0)
    if law == 'L1':
        return -amp * math.exp(-K * s1)
    if law == 'L2':
        return -amp * (math.exp(-K * s1) + math.exp(-K * s2))
    allv, prim = all_lengths(c)
    if law == 'L3':
        return -amp * np.exp(-K * prim).sum()
    if law == 'L4':
        return -B * (A / 72) * (np.exp(-K * allv) / allv).sum()


LAWS = [('L1', 'const'), ('L1', 'area'), ('L2', 'const'), ('L2', 'area'), ('L3', 'const'), ('L3', 'area'), ('L4', 'area')]


def fit(law, scale, data):
    keys = sorted(data)
    y = np.array([data[k][0] for k in keys]); e = np.array([data[k][1] for k in keys])
    areas = sorted({A for A, _ in keys})

    def model(p):
        B, K = math.exp(p[0]), p[1]
        f = np.array([shape_term(law, c, A, B, K, scale) for A, c in keys])
        # c(A) profiled out: weighted mean residual per area
        out = np.empty_like(f)
        for A in areas:
            m = np.array([k[0] == A for k in keys])
            w = 1 / e[m] ** 2
            out[m] = f[m] + (w * (y[m] - f[m])).sum() / w.sum()
        return out
    best = None
    for K0 in (0.5, 1.0, 1.5, 2.0, 3.0):
        for lB in (0.0, 2.0, 4.0, 6.0):
            try:
                r = least_squares(lambda p: (model(p) - y) / e, [lB, K0], bounds=([-10, 0.05], [30, 8]))
            except Exception:
                continue
            if best is None or r.cost < best.cost:
                best = r
    p = best.x; mod = model(p)
    cA = {A: float(np.mean((y - mod + mod)[[k[0] == A for k in keys]])) for A in areas}
    # c(A) values
    cvals = {}
    for A in areas:
        m = np.array([k[0] == A for k in keys]); w = 1 / e[m] ** 2
        f = np.array([shape_term(law, c, AA, math.exp(p[0]), p[1], scale) for AA, c in np.array(keys, dtype=object)[m]])
        cvals[A] = float((w * (y[m] - f)).sum() / w.sum())
    return dict(B=math.exp(p[0]), K=p[1], chi2=2 * best.cost, dof=len(y) - 2 - len(areas), c=cvals,
                resid={f'{A} {c}': float((y[i] - mod[i]) / e[i]) for i, (A, c) in enumerate(keys)})


if __name__ == '__main__':
    data = published()
    print('published classes (presentations pooled):')
    for (A, c), (v, e) in sorted(data.items()):
        inv = invariants(*c)
        print(f'  A={A} {str(c):12s} loops {inv["loops"]}  {v:.4f} +- {e:.4f}')
    res = {}
    for law, scale in LAWS:
        r = fit(law, scale, data); res[f'{law}-{scale}'] = r
        print(f'{law}-{scale}: B {r["B"]:.4g} K {r["K"]:.3f} chi2 {r["chi2"]:.1f} / {r["dof"]}  c {r["c"]}')
        print('   resid (sd): ' + ' '.join(f'{k.split()[0]}:{v:+.1f}' for k, v in r['resid'].items()))
    # predictions for every class, as differences from the area's reference class (largest l1, then l2):
    pred = {}
    for n in (16, 20, 24):
        A = 3 * n; C = classes(n)
        cl = sorted(C, key=lambda c: (invariants(*c)['loops'], c))
        for key, r in res.items():
            law, scale = key.split('-')
            f = {c: shape_term(law, c, A, r['B'], r['K'], scale) for c in cl}
            pred.setdefault(A, {})[key] = {str(c): float(f[c]) for c in cl}
    if '--json' in sys.argv:
        json.dump(dict(fits=res, shape_terms=pred), open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
    for A in (48, 60, 72):
        print(f'\nA = {A}: shape term f (ln tau = c(A) + f); '
              + ('c(A) from the fit' if A in (60, 72) else 'c(48) not fitted'))
        keys = list(res)
        print(f'{"class":13s} {"loops":28s} ' + ' '.join(f'{k:>9s}' for k in keys))
        for c in pred[A][keys[0]]:
            cc = tuple(int(x) for x in c.strip('()').split(','))
            print(f'{c:13s} {str(invariants(*cc)["loops"]):28s} '
                  + ' '.join(f'{pred[A][k][c] + (res[k]["c"].get(A, 0)):9.3f}' for k in keys))
