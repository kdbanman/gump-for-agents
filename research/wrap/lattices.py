#!/usr/bin/env python3
"""Face tori of index n (A = 3n cells per layer): every period lattice (h, k), (0, d) in Hermite normal form,
h d = n, 0 <= k < d, in the hexagonal basis |x e1 + y e2|^2 = x^2 + xy + y^2.  Written for research/wrap from the
definitions (shares no code with research/shape*/ or the lead's script).

Class = reduced Gram triple (Q1, 2B, Q2) with Q1 <= Q2, 0 <= 2B <= Q1 (B taken >= 0: classes up to isometry
including reflections, as the slab's in-plane point group with the face flip is the full hexagonal group).

    python3 research/wrap/lattices.py 51 54 57 63      # classes, a representative HNF, loops^2 <= 30
"""
import sys
from math import gcd


def Q(x, y):
    return x * x + x * y + y * y


def vectors(h, k, d, R=14):
    """all nonzero lattice vectors m (h, k) + j (0, d), one per +-v, as (q, x, y)"""
    out = []
    for m in range(0, R + 1):
        for j in range(-R, R + 1):
            if m == 0 and j <= 0:
                continue
            x, y = m * h, m * k + j * d
            out.append((Q(x, y), x, y))
    out.sort()
    return out


def bil(u, v):
    return (Q(u[0] + v[0], u[1] + v[1]) - Q(*u) - Q(*v)) / 2


def gram(h, k, d):
    vs = vectors(h, k, d)
    q1, *v1 = vs[0]
    n = h * d
    for q2, *v2 in vs[1:]:
        if v1[0] * v2[1] - v1[1] * v2[0] != 0:   # first non-parallel vector: with v1 a basis (2D successive minima)
            det = abs(v1[0] * v2[1] - v1[1] * v2[0])
            assert det == n, (h, k, d, v1, v2)
            B = abs(bil(v1, v2))
            assert 4 * (q1 * q2 - B * B) == 3 * n * n
            return (q1, int(round(2 * B)), q2)


def loops(h, k, d, cap=30):
    """squared lengths of the closed-loop directions (one per +-v, primitive or not) up to cap"""
    return [q for q, x, y in vectors(h, k, d) if q <= cap]


def classes(A):
    n = A // 3
    cl = {}
    for h in range(1, n + 1):
        if n % h:
            continue
        d = n // h
        for k in range(d):
            g = gram(h, k, d)
            cl.setdefault(g, []).append((h, k, d))
    return cl


if __name__ == '__main__':
    for A in map(int, sys.argv[1:]):
        for g, reps in sorted(classes(A).items()):
            h, k, d = reps[0]
            print(A, g, (h, k, d), len(reps), loops(h, k, d))
