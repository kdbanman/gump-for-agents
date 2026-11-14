#!/usr/bin/env python3
"""Candidate second variables and their forecasts for research/shape3 (written before any production run).

    python3 research/shape3/predict3.py            # table of forecasts; writes research/shape3/data/predictions.json

Every candidate is a formula in the period lattice. Free parameters are fitted by weighted least squares on the
three pair differences known before this experiment (in-sample; research/audit/REVIEW-shape2.md, claim 4):
  P1  A=48 l1=12  (2,2,8) -> (1,6,16)   +0.0151 +- 0.0017
  P2  A=60 l1=16  (1,5,20) -> (1,4,20)  +0.0142 +- 0.0019
  P3  A=60 l1=12  (1,8,20) -> (2,2,10)  +0.0063 +- 0.0035
A difference d(X -> Y) is ln tau_face(Y) - ln tau_face(X); in every group Y has the longer second loop.
Reduced Gram (Q1, 2B, Q2) (Q = x^2 + xy + y^2, research/shape/lattice.py reduced()); D = Q1 Q2 - B^2 (fixed by A);
modulus tau = (B + i sqrt D) / Q1, so h = Im tau = sqrt(D)/Q1, x = Re tau = B/Q1 in [0, 1/2].
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'shape2'))
import lattice2 as L2  # noqa: E402
from lattice import reduced, Q  # noqa: E402

KNOWN = [('P1', 48, (2, 2, 8), (1, 6, 16), 0.0151, 0.0017),
         ('P2', 60, (1, 5, 20), (1, 4, 20), 0.0142, 0.0019),
         ('P3', 60, (1, 8, 20), (2, 2, 10), 0.0063, 0.0035)]
# new differences (groups from enum3.py: every equal-area equal-loop group with loop^2 >= 12 at A <= 72, and the
# loop^2 9 groups at A = 36..63, which are below saturation)
NEW = [('T01', 72, (1, 6, 24), (2, 4, 12)), ('T12', 72, (2, 4, 12), (1, 5, 24)), ('T02', 72, (1, 6, 24), (1, 5, 24)),
       ('N72', 72, (2, 2, 12), (1, 10, 24)),
       ('Q36', 36, (1, 4, 12), (1, 3, 12)), ('Q45', 45, (1, 5, 15), (1, 4, 15)),
       ('Q54', 54, (3, 0, 6), (1, 5, 18)), ('Q63', 63, (1, 6, 21), (1, 7, 21))]


def geo(c):
    (q1, b2, q2), _, _ = reduced(*c)
    B = b2 / 2; D = q1 * q2 - B * B
    inv = L2.invariants(*c)
    return dict(q1=q1, q2=q2, B=B, h=math.sqrt(D) / q1, x=B / q1, theta=math.degrees(math.acos(B / math.sqrt(q1 * q2))),
                l3=inv['loops'][2], cut=inv['cut'], rows=inv['rows'])


def primsum(c, K, Lmax=40.0):
    a, k, b = c; R = int(Lmax) + 2; s = 0.0
    for p in range(0, R + 1):
        for q in range(-4 * R, 4 * R + 1):
            if (p == 0 and q <= 0) or math.gcd(p, abs(q)) != 1:
                continue
            L = math.sqrt(Q(p * a, p * k + q * b))
            if L <= Lmax:
                s += math.exp(-K * L)
    return s


# --- candidates: each maps (A, X, Y, params) -> forecast difference -----------------------------------------
def f_l2(A, X, Y, p):      # K1: linear in the second loop
    return p[0] * (geo(Y)['q2'] - geo(X)['q2'])


def f_theta(A, X, Y, p):   # K1a: linear in the angle between the reduced basis vectors (degrees)
    return p[0] * (geo(X)['theta'] - geo(Y)['theta'])


def f_mod(A, X, Y, p):     # K3: leading Re tau dependence of any modular (scale-free) function
    gx, gy = geo(X), geo(Y)
    return p[0] * (math.exp(-2 * math.pi * gx['h']) * math.cos(2 * math.pi * gx['x'])
                   - math.exp(-2 * math.pi * gy['h']) * math.cos(2 * math.pi * gy['x']))


def f_cosx(A, X, Y, p):    # K3b: cos 2 pi Re tau without the e^{-2 pi h} factor
    return p[0] * (math.cos(2 * math.pi * geo(X)['x']) - math.cos(2 * math.pi * geo(Y)['x']))


def f_loop(A, X, Y, p):    # K2: ln tau = c(A) - Bamp (A/72) sum_prim e^{-K|v|}
    return -math.exp(p[0]) * (A / 72) * (primsum(Y, p[1]) - primsum(X, p[1]))


CANDS = {'K1_l2': (f_l2, [0.005]), 'K1a_angle': (f_theta, [0.0007]), 'K2_loopsum': (f_loop, [3.0, 0.65]),
         'K3_modular': (f_mod, [10.0]), 'K3b_cosx': (f_cosx, [0.005])}


def fit(f, p0):
    from scipy.optimize import least_squares
    res = lambda p: np.array([(f(A, X, Y, p) - d) / e for _, A, X, Y, d, e in KNOWN])
    best = None
    starts = [p0] if len(p0) == 1 else [[lb, K] for lb in (-2, 1, 4, 7) for K in (0.2, 0.4, 0.65, 1.0, 1.5)]
    for s in starts:
        try:
            r = least_squares(res, s)
        except Exception:
            continue
        if best is None or r.cost < best.cost:
            best = r
    J = best.jac; cov = np.linalg.pinv(J.T @ J)
    return best.x, cov, 2 * best.cost


def forecast(f, p, cov, A, X, Y):
    v = f(A, X, Y, p); g = []
    for i in range(len(p)):
        dp = np.array(p, float); h = 1e-6 * max(1, abs(p[i])); dp[i] += h
        g.append((f(A, X, Y, dp) - v) / h)
    g = np.array(g)
    return v, math.sqrt(max(0.0, g @ cov @ g))


if __name__ == '__main__':
    print('geometry:')
    for lab, A, X, Y, *_ in KNOWN + [tuple(t) + (None, None) for t in NEW]:
        for c in (X, Y):
            g = geo(c)
            print(f'  {lab:4s} A={A} {str(c):12s} gram ({g["q1"]},{2*g["B"]:.0f},{g["q2"]}) h={g["h"]:.3f} x={g["x"]:.3f} '
                  f'theta={g["theta"]:.1f} l3={g["l3"]} cut={g["cut"]} rows={g["rows"]}')
    out = {'known': KNOWN, 'new': NEW, 'cands': {}}
    for name, (f, p0) in CANDS.items():
        p, cov, chi = fit(f, p0)
        fc = {lab: forecast(f, p, cov, A, X, Y) for lab, A, X, Y in NEW}
        ins = {lab: forecast(f, p, cov, A, X, Y) for lab, A, X, Y, _, _ in KNOWN}
        out['cands'][name] = dict(params=list(map(float, p)), cov=cov.tolist(), chi2_in=chi, dof_in=3 - len(p),
                                  forecast={k: list(v) for k, v in fc.items()}, insample={k: list(v) for k, v in ins.items()})
        print(f'{name:11s} params {np.round(p, 5).tolist()} in-sample chi2 {chi:.2f} on {3 - len(p)}  ' +
              ' '.join(f'{k}:{v:+.4f}' for k, (v, _) in ins.items()))
        print('            ' + '  '.join(f'{k} {v:+.4f}+-{e:.4f}' for k, (v, e) in fc.items()))
    if '--write' in sys.argv:
        json.dump(out, open(os.path.join(HERE, 'data', 'predictions.json'), 'w'), indent=1)
