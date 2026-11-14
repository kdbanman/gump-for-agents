#!/usr/bin/env python3
"""Groups of torus classes with equal area A = 3n and equal shortest loop (Q >= 12), with the invariants that
the candidate second variables of PREDICTIONS.md are computed from.

    python3 research/shape3/enum3.py 14 22          # print groups for n = 14..22
Class enumeration: research/shape2/lattice2.py (classes, invariants). Gram: research/shape/lattice.py reduced().
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'shape2'))
import lattice2 as L2  # noqa: E402
from lattice import reduced  # noqa: E402  (research/shape, put on the path by lattice2)


def groups(n, qmin=12):
    C = L2.classes(n)
    by = {}
    for c in C:
        inv = L2.invariants(*c)
        if inv['l1'] >= qmin:
            by.setdefault(inv['l1'], []).append(c)
    return {q: sorted(v, key=lambda c: L2.invariants(*c)['l2']) for q, v in by.items() if len(v) >= 2}, C


if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for n in range(lo, hi + 1):
        G, C = groups(n)
        for q, cl in sorted(G.items()):
            print(f'A={3*n} l1={q}:')
            for c in cl:
                inv = L2.invariants(*c); g = reduced(*c)[0]
                print(f'   {str(c):12s} x{len(C[c]):2d} gram {g} loops {inv["loops"]} angle {inv["angle"]:.1f} '
                      f'rows {inv["rows"]} cut {inv["cut"]} periods {inv["periods"]}')
