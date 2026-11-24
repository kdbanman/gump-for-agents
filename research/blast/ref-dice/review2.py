#!/usr/bin/env python3
"""ref-dice, second review (dice commits up to 6f70d2d). With myface.py (built from oracle.py alone):
  (a) hull faces R = 1..15: the (degree, m1, m2) types and the balance in-degree = out-degree of every cell;
  (b) the weighted local check on the three hull types: the best uniform w and its delta; w = 1341/1000, delta 0.109;
  (c) thin and skewed tori (H = 1, D = 1, 2; K != 0; K >= D): regularity (6 slots, in-degree 6);
  (d) ln tau / A of every torus with A <= 12 and of the hull faces R = 3 (and 5 by the README) against the
      bounds 1.9228 and 2.2165 (dense float power iteration on Q, 800 steps);
  (e) the death-flux share from mu, generation by generation (window propagation started FROM mu): flux_share says
      it equals bustShare at every generation m + 6.
    python3 review2.py [a b c d e]
"""
import sys, math
from fractions import Fraction
import numpy as np
import myface
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    from regular_check import grid, hull_cells, regular   # (its own printout suppressed)

parts = sys.argv[1:] or list('abcde')


def balanced(F):
    return all(sum(l.count(j) for l in F['nb']) == len(F['nb'][j]) for j in range(F['A']))


if 'a' in parts:
    for R in range(1, 16, 2):
        F = myface.build('hull', (R,), hull_cells(R))
        types = {}
        for i in range(F['A']):
            t = (len(F['nb'][i]), F['m1'][i], F['m2'][i])
            types[t] = types.get(t, 0) + 1
        sym = all(F['nb'][i].count(j) == F['nb'][j].count(i) for i in range(F['A']) for j in range(F['A']))
        nodup = all(len(set(l)) == len(l) for l in F['nb'])
        print('(a) hull %2d: A = %3d, types %s, balanced %s, symmetric %s, no repeated neighbour %s'
              % (R, F['A'], dict(sorted(types.items())), balanced(F), sym, nodup))

TYPES = [(6, 2, 1), (4, 2, 1), (2, 2, 0)]


def wmin(w, types=TYPES):
    best = None
    for d, m1, m2 in types:
        for k in range(d + 1):
            for s in (0, 1):
                v = (1 - myface.alive_prob(m1, m2, k, s)) * (w ** (d - k) if s else 1) / (1 if s else w ** k)
                best = v if best is None or v < best else best
    return best


if 'b' in parts:
    w = Fraction(1341, 1000)
    print('(b) w = 1341/1000: min weighted factor over the 3 hull types = %.6f >= 0.109: %s -> ln tau < %.4f A'
          % (float(wmin(w)), wmin(w) >= Fraction(109, 1000), -math.log(wmin(w))))
    best = max((wmin(Fraction(i, 1000)), i) for i in range(1000, 1700))
    print('    best uniform w on a 0.001 grid: %.3f, delta %.6f -> %.4f A; -ln 0.109 = %.5f'
          % (best[1] / 1000, float(best[0]), -math.log(best[0]), -math.log(0.109)))

if 'c' in parts:
    out = []
    for H, K, D in [(1, 1, 1), (1, 2, 1), (1, 5, 1), (2, 1, 1), (3, 2, 1), (1, 1, 2), (1, 3, 2), (1, 5, 2), (2, 1, 2),
                    (2, 3, 2), (5, 3, 2), (1, 4, 3), (1, 7, 3), (2, 5, 3), (4, 6, 5), (1, 2, 7)]:
        F = myface.build('torus', (H, K, D), grid(H, D))
        selfloops = sum(F['nb'][i].count(i) for i in range(F['A']))
        maxmult = max(l.count(j) for l in F['nb'] for j in set(l))
        out.append('(%d,%d,%d): A=%d regular=%s self-slots=%d max multiplicity=%d'
                   % (H, K, D, F['A'], regular(F), selfloops, maxmult))
    print('(c) tori:\n    ' + '\n    '.join(out))


def lam_float(F, iters=800):
    A = F['A']; n = 2 ** A
    at = np.array([[float(a) for a in row] for row in myface.a_table(F)])
    ys = np.arange(n)
    P = np.ones((n, n))
    for i in range(A):
        bit = (ys >> i) & 1
        P *= np.where(bit[None, :] == 1, at[:, i:i + 1], 1 - at[:, i:i + 1])
    Q = P[1:, 1:]
    v = np.ones(n - 1)
    lam = 0
    for _ in range(iters):
        w = Q @ v; lam = w.max(); v = w / lam
    return lam, P


if 'd' in parts:
    rows = []
    for H, K, D in [(1, 0, 1), (1, 0, 2), (1, 1, 2), (2, 0, 1), (2, 1, 1), (1, 0, 3), (1, 1, 3), (1, 2, 3), (3, 0, 1),
                    (3, 1, 1), (1, 0, 4), (1, 1, 4), (1, 2, 4), (1, 3, 4), (2, 0, 2), (2, 1, 2), (4, 0, 1)]:
        F = myface.build('torus', (H, K, D), grid(H, D))
        lam, _ = lam_float(F)
        lt = -math.log(1 - lam)
        rows.append('(%d,%d,%d) A=%2d ln tau=%.6f  ln tau/A=%.4f  1.9228/(ln tau/A)=%.2f'
                    % (H, K, D, F['A'], lt, lt / F['A'], 1.9228 / (lt / F['A'])))
    print('(d) tori:\n    ' + '\n    '.join(rows))
    for R in (1, 3):
        F = myface.build('hull', (R,), hull_cells(R))
        lam, P = lam_float(F)
        lt = -math.log(1 - lam)
        E = max(-math.log(P[x, 0]) for x in range(1, 2 ** F['A']))
        print('(d) hull %d: A=%d ln tau=%.6f, ln tau/A=%.4f; bounds 2.2165 A = %.3f, 2.5095 A = %.3f; '
              'max_x -ln P(x,empty)/A = %.4f' % (R, F['A'], lt, lt / F['A'], 2.2165 * F['A'], 2.5095 * F['A'], E / F['A']))
    print('(d) hull 5 (README claim 3, exact qsd.c): ln tau = 4.2316548327, ln tau/A = %.4f against 2.2165' % (4.2316548327 / 18))

if 'e' in parts:
    from numerics import lean_cells
    from compare_kernel import KIND
    for name in ('hull3', 'torus113'):
        kind, args = KIND[name]
        F = myface.build(kind, args, lean_cells(name))
        A = F['A']; n = 2 ** A
        lam, P = lam_float(F)
        Q = P[1:, 1:]
        u = np.ones(n - 1)
        for _ in range(3000):
            u = u @ Q; u /= u.sum()
        mu = np.concatenate([[0.0], u])
        pop = np.array([bin(x).count('1') for x in range(n)])
        half = (A + 1) // 2
        big = (pop[:, None] - pop[None, :]) >= half
        J = np.zeros((7, n)); J[6] = mu
        shares = []
        for t in range(1, 13):
            NJ = np.zeros((7, n)); db = df = 0.0
            for c in range(7):
                flow = J[c][:, None] * P
                fb = (flow * big).sum(0); fn = (flow * ~big).sum(0)
                db += fb[0] + (fn[0] if c < 5 else 0.0); df += fn[0] if c >= 5 else 0.0
                fb[0] = fn[0] = 0.0
                NJ[0] += fb; NJ[min(c + 1, 6)] += fn
            J = NJ
            shares.append((t, db + df, db / (db + df), (db + df) / (lam ** (t - 1) * (1 - lam))))
        print('(e) %s from mu: ' % name + '; '.join('t=%d share %.10f, P(T=t)/(lam^(t-1)(1-lam)) %.12f' % s[0:1] + s[2:]
                                                    if False else 't=%d: %.10f (flux ratio %.12f)' % (s[0], s[2], s[3])
                                                    for s in shares))
