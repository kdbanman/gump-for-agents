#!/usr/bin/env python3
"""In-plane period lattices of a {111} slab, in cube coordinates (i, j) (k = t - i - j).

A lattice is given in Hermite normal form by generators (a, k), (0, b), 0 <= k < b; index n = a*b, face area A = 3n.
Translation (x, y) in (i, j) is the cube vector x*u1 + y*u2, u1 = (1,0,-1), u2 = (0,1,-1) (60 degrees apart);
|x u1 + y u2|^2 = 2 Q(x, y), Q = x^2 + xy + y^2.  "Systole^2" below is Q of the shortest nonzero lattice vector.

    python3 research/shape/lattice.py 24      # every index-24 lattice, grouped into shapes (isometry classes)
"""
import itertools, math, sys


def Q(x, y):
    return x * x + x * y + y * y


def B(u, v):
    return u[0] * v[0] + (u[0] * v[1] + u[1] * v[0]) / 2 + u[1] * v[1]


def vectors(a, k, b, R=4):
    for p, q in itertools.product(range(-R * 6, R * 6 + 1), repeat=2):
        v = (p * a, p * k + q * b)
        if v != (0, 0):
            yield v


def reduced(a, k, b):
    """Gauss-reduced Gram (Q(u), |2B(u,v)|, Q(v)) with Q(u) <= Q(v); an isometry invariant (up to orientation;
    the hexagonal point group, order 12, includes reflections, so orientation does not matter)."""
    u, v = (a, k), (0, b)
    while True:
        if Q(*u) > Q(*v):
            u, v = v, u
        m = round(B(u, v) / Q(*u))
        if m == 0:
            break
        v = (v[0] - m * u[0], v[1] - m * u[1])
    return (Q(*u), abs(int(round(2 * B(u, v)))), Q(*v)), u, v


def systole2(a, k, b):
    return reduced(a, k, b)[0][0]


def row_closure(a, k, b):
    """Smallest n > 0 with n*w in the lattice, for the three kagome row directions w = u1, u2, u1 - u2, i.e. the
    in-plane length of a transverse diagonal layer (diags 2, 1, 3 of geom.DIAGS) in units of |u1|."""
    def first(w):
        n = 1
        while True:
            x, y = n * w[0], n * w[1]
            if x % a == 0 and (y - (x // a) * k) % b == 0:
                return n
            n += 1
    return {'u1 (diag 2)': first((1, 0)), 'u2 (diag 1)': first((0, 1)), 'u1-u2 (diag 3)': first((1, -1))}


def transverse_periods(a, k, b):
    """Period of s = d.p (doubled coords) on the lattice for diags 1..3 of geom.DIAGS: gcd of s over the generators.
    Generator (x, y) is the doubled vector 2(x, y, -x-y)."""
    out = []
    for d in [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
        g = 0
        for (x, y) in [(a, k), (0, b)]:
            g = math.gcd(g, 2 * (d[0] * x + d[1] * y - d[2] * (x + y)))
        out.append(g)
    return out


def hnf(n):
    for a in range(1, n + 1):
        if n % a == 0:
            b = n // a
            for k in range(b):
                yield a, k, b


if __name__ == '__main__':
    n = int(sys.argv[1])
    cls = {}
    for a, k, b in hnf(n):
        g, u, v = reduced(a, k, b)
        brute = min(Q(*w) for w in vectors(a, k, b))
        assert brute == g[0], (a, k, b, brute, g)
        cls.setdefault(g, []).append((a, k, b))
    for g in sorted(cls):
        reps = cls[g]
        a, k, b = reps[0]
        print(f'systole^2 {g[0]:3d}  reduced Gram (Q(u), |2B|, Q(v)) = {g}  row closures {row_closure(a, k, b)}  '
              f'periods {transverse_periods(a, k, b)}  HNFs {reps}')
