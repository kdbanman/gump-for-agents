#!/usr/bin/env python3
"""Every index-n period lattice of the {111} slab face, grouped into classes under the twelve symmetries of the
triangular lattice, with the invariants used by the candidate laws.

    python3 research/shape2/lattice2.py 20            # table
    python3 research/shape2/lattice2.py 20 --csv      # research/shape2/data/classes_A60.csv

Lattice: generators (a, k), (0, b) in the cube coordinates (i, j), ab = n, 0 <= k < b; |x u1 + y u2|^2 ∝ Q = x^2+xy+y^2.
Class canonical form: copied from research/audit/shape_lead_check.py (hnf, cls; the review checked these classes).
Per class:
  loops   Q of the first six primitive lattice vectors up to sign, increasing (ties in arbitrary order)
  l1, l2  successive minima (Q), angle between the reduced basis vectors (degrees, 60..90)
  rows    shortest closure n > 0 with n w in the lattice for w = u1, u2, u1 - u2 (research/shape/lattice.py)
  cut     cells in the cheapest transverse firewall: 3 x layer size over diagonals with >= 3 layers (as
          research/shape/models.py); 'none' if every diagonal has <= 2 layers
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'shape'))
from lattice import row_closure, transverse_periods  # noqa: E402

M = 8


def hnf(v, w):                      # canonical generators (a, k), (0, b), 0 <= k < b, of Z v + Z w
    (p, q), (r, s) = v, w
    while r:
        t = p // r; p, q, r, s = r, s, p - t * r, q - t * s
    if p < 0: p, q = -p, -q
    s = abs(s)
    return (p, q % s, s)


ROT = lambda v: (-v[1], v[0] + v[1])
REF = lambda v: (v[1], v[0])


def cls(a, k, b):
    out = set(); v, w = (a, k), (0, b)
    for _ in range(6):
        v, w = ROT(v), ROT(w); out.add(hnf(v, w)); out.add(hnf(REF(v), REF(w)))
    return min(out)


def Q(x, y):
    return x * x + x * y + y * y


def primitive_loops(a, k, b, R=None):
    """Q of primitive lattice vectors up to sign, sorted (all with Q <= bound that is surely complete)."""
    n = a * b
    R = R or 3 * n + 6
    out = []
    for p in range(0, R + 1):
        for q in range(-R, R + 1):
            if p == 0 and q <= 0:
                continue
            if math.gcd(p, abs(q)) != 1:
                continue
            x, y = p * a, p * k + q * b
            out.append((Q(x, y), (x, y)))
    out.sort()
    return out


def invariants(a, k, b):
    L = primitive_loops(a, k, b)
    q1, v1 = L[0]
    # second minimum: shortest vector independent of v1
    q2, v2 = next((q, v) for q, v in L if v[0] * v1[1] - v[1] * v1[0] != 0)
    Bv = v1[0] * v2[0] + (v1[0] * v2[1] + v1[1] * v2[0]) / 2 + v1[1] * v2[1]
    ang = math.degrees(math.acos(abs(Bv) / math.sqrt(q1 * q2)))
    rows = tuple(row_closure(a, k, b).values())
    P = transverse_periods(a, k, b)
    cuts = [3 * (3 * a * b * M) // (p // 2) for p in P if p // 2 >= 3]
    return dict(loops=[q for q, _ in L[:6]], allq=[q for q, _ in L], l1=q1, l2=q2, angle=ang, rows=rows,
                minrow=min(rows), cut=min(cuts) if cuts else None, periods=P)


def classes(n):
    out = {}
    for a in range(1, n + 1):
        if n % a:
            continue
        b = n // a
        for k in range(b):
            out.setdefault(cls(a, k, b), []).append((a, k, b))
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]); C = classes(n)
    rows = []
    for c in sorted(C, key=lambda c: (invariants(*c)['loops'], c)):
        inv = invariants(*c)
        rows.append((c, C[c], inv))
        if '--csv' not in sys.argv:
            print(f'{str(c):13s} x{len(C[c]):2d}  loops {inv["loops"]}  l1,l2 {inv["l1"]},{inv["l2"]} '
                  f'angle {inv["angle"]:.1f}  rows {inv["rows"]}  cut {inv["cut"]}')
    print(f'index {n}: {sum(len(v) for v in C.values())} lattices, {len(C)} classes', file=sys.stderr)
    if '--csv' in sys.argv:
        f = open(os.path.join(HERE, 'data', f'classes_A{3 * n}.csv'), 'w')
        f.write('cls_a,cls_k,cls_b,n_presentations,loops6,l1,l2,angle,rows,minrow,cut\n')
        for c, pres, inv in rows:
            f.write(f'{c[0]},{c[1]},{c[2]},{len(pres)},{" ".join(map(str, inv["loops"]))},{inv["l1"]},{inv["l2"]},'
                    f'{inv["angle"]:.2f},{" ".join(map(str, inv["rows"]))},{inv["minrow"]},{inv["cut"]}\n')
