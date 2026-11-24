#!/usr/bin/env python3
"""ref-dice: which faces satisfy `Face.regular` (6 neighbour slots per cell, each cell in 6 slots) and `coin = true`,
with myface.py's neighbour lists (equal to Lean's Face.nb on the five 9-cell faces, compare_kernel.py); and the local
certificate of DiceBound2 (`weighted_cell`, delta1 = 0.1462 at w = 152/125) recomputed in exact rationals, with the
best w; and max_x -ln P(x, empty) / A on the 9-cell tori (the notes' "1.52-1.82").
    python3 regular_check.py
"""
import math
from fractions import Fraction
import myface

base = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
grid = lambda W, D: [tuple(base[o][t] + a * (2, -2, 0)[t] + b * (2, 0, -2)[t] for t in range(3))
                     for a in range(W) for b in range(D) for o in range(3)]


def hull_cells(R):
    return [(x, y, R - x - y) for x in range(R + 1) for y in range(R + 1 - x) if myface.is_cell((x, y, R - x - y))]


def regular(F):
    A = F['A']
    outd = all(len(l) == 6 for l in F['nb'])
    ind = all(sum(l.count(j) for l in F['nb']) == 6 for j in range(A))
    return outd and ind


res = []
for H in range(1, 5):
    for D in range(1, 5):
        for K in range(0, D):
            F = myface.build('torus', (H, K, D), grid(H, D))
            res.append(('torus', (H, K, D), regular(F)))
bad = [r for r in res if not r[2]]
print('tori (H,K,D), 1<=H,D<=4, 0<=K<D: %d faces, regular: %d, not regular: %s' % (len(res), len(res) - len(bad), bad))
for W in range(1, 4):
    for D in range(1, 4):
        print('strip %dx%d regular: %s; patch %dx%d regular: %s' % (
            W, D, regular(myface.build('strip', (W, D), grid(W, D))), W, D,
            regular(myface.build('patch', (W, D), grid(W, D)))))
for R in (1, 3, 5, 7):
    F = myface.build('hull', (R,), hull_cells(R))
    print('hull %d (A=%d) regular: %s; all coins: %s' % (R, F['A'], regular(F),
          all((a, b) == (2, 1) for a, b in zip(F['m1'], F['m2']))))

# weighted_cell: delta1 * (s ? 1 : w^k) <= (1 - a(2,1,k,s)) * (s ? w^(6-k) : 1), k <= 6
def margin(w):
    best = None
    for k in range(7):
        for s in (0, 1):
            d = 1 - myface.alive_prob(2, 1, k, s)
            val = d * (w ** (6 - k) if s else 1) / (1 if s else w ** k)
            best = val if best is None or val < best else best
    return best
w = Fraction(152, 125)
print('weighted_cell at w = 152/125: min over (k,s) of the weighted factor = %.6f (claimed delta1 = 0.1462); '
      'holds: %s' % (float(margin(w)), margin(w) >= Fraction(1462, 10000)))
bw = max((margin(Fraction(i, 1000)), i) for i in range(1000, 1500))
print('best w on a 0.001 grid: w = %.3f gives %.6f -> ln tau < %.4f A' % (bw[1] / 1000, float(bw[0]), -math.log(bw[0])))
print('unweighted delta0 = %.6f -> %.5f A' % (float(margin(Fraction(1))), -math.log(margin(Fraction(1)))))
for args in ((1, 0, 3), (1, 1, 3), (2, 0, 2), (1, 0, 4), (1, 1, 4)):
    F = myface.build('torus', args, grid(args[0], args[2]))
    at = myface.a_table(F)
    A = F['A']
    E = max(-sum(math.log(1 - float(a)) for a in at[x]) for x in range(1, 2 ** A))
    print('torus %s (A=%d): max_x -ln P(x,empty)/A = %.4f' % (args, A, E / A))
