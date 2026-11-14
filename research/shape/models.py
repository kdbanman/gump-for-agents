#!/usr/bin/env python3
"""Geometric invariants of the tori measured here, and what each hypothesis predicts (numbers in PREDICTIONS.md).

    python3 research/shape/models.py

Per torus (HNF a, k, b; index n = ab; area A = 3n):
  sys2   Euclidean systole^2, in units |u1|^2: min Q(x, y) = x^2 + xy + y^2 over nonzero lattice vectors
  hexsys systole in the hexagonal (graph) metric of the triangular cube lattice: min (|x| + |y| + |x + y|) / 2,
         the number of in-plane cube steps (+-u1, +-u2, +-(u1 - u2)) of the shortest non-contractible loop
  rows   closure lengths of the three kagome row directions u1, u2, u1 - u2 (the in-plane length of a transverse layer)
  cut    cells in the cheapest transverse firewall (three layers of a diagonal with >= 3 layers); None if no diagonal
"""
import itertools, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice import Q, reduced, row_closure  # noqa: E402
import tslab                                  # noqa: E402

TORI = [  # (label, a, k, b)
    ('3x8', 3, 0, 8), ('4x6', 4, 0, 6), ('4x6 k2', 4, 2, 6), ('4x6 k4', 4, 4, 6), ('2x12 k5', 2, 5, 12),
    ('4x6 k3', 4, 3, 6), ('4x6 k5', 4, 5, 6), ('3x8 k1', 3, 1, 8), ('6x4 k1', 6, 1, 4), ('6x4 k3', 6, 3, 4),
    ('2x12 k3', 2, 3, 12), ('4x6 k1', 4, 1, 6), ('8x3 k2', 8, 2, 3),
]


def lat_vectors(a, k, b, R=30):
    for p, q in itertools.product(range(-R, R + 1), repeat=2):
        v = (p * a, p * k + q * b)
        if v != (0, 0):
            yield v


def invariants(a, k, b, m=8):
    vs = list(lat_vectors(a, k, b))
    sys2 = min(Q(*v) for v in vs)
    hexs = min((abs(x) + abs(y) + abs(x + y)) // 2 for x, y in vs)
    rows = row_closure(a, k, b)
    P = tslab.periods(a, k, b)
    ncell = 3 * a * b * m
    cuts = [3 * ncell // (p // 2) for p in P if p // 2 >= 3]
    return dict(sys2=sys2, hexsys=hexs, rows=tuple(rows.values()), periods=P, cut=min(cuts) if cuts else None,
                gram=reduced(a, k, b)[0], nshort=sum(Q(*v) == sys2 for v in vs))


def interp(x, pts):
    """piecewise linear through pts, linear extrapolation with the last segment's ... slope capped (see text)"""
    pts = sorted(pts)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    return y1 + (y1 - y0) / (x1 - x0) * (x - x1)


def predictions(inv):
    s = math.sqrt(inv['sys2'])
    # H1: function of the Euclidean systole: through 3 -> 14.621 and 4 -> 14.970, then +0.07 per unit (s >= 4 offset)
    h1 = interp(s, [(3, 14.621), (4, 14.970), (5, 15.040)])
    # H0a: function of the hex systole, same anchors
    h0a = interp(inv['hexsys'], [(3, 14.621), (4, 14.970), (5, 15.040)])
    # H0b: function of the shortest row closure r (= firewall-proneness): 3 -> 14.621, 4 -> 14.970, +0.07 per unit
    r = min(inv['rows'])
    h0b = interp(r, [(3, 14.621), (4, 14.970), (5, 15.040)])
    return h1, h0a, h0b


if __name__ == '__main__':
    print(f'{"torus":9s} {"HNF":10s} {"Gram":14s} sys2 #short hexsys rows        cut   H1     H0a    H0b')
    for lab, a, k, b in TORI:
        inv = invariants(a, k, b)
        h1, h0a, h0b = predictions(inv)
        print(f'{lab:9s} {str((a, k, b)):10s} {str(inv["gram"]):14s} {inv["sys2"]:4d} {inv["nshort"]:5d} {inv["hexsys"]:6d} '
              f'{str(inv["rows"]):11s} {str(inv["cut"]):5s} {h1:.3f} {h0a:.3f} {h0b:.3f}')
