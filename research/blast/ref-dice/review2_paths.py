#!/usr/bin/env python3
"""ref-dice: exact path enumeration of P_x(T = n) and P_x(T = n, a fall >= ceil(A/2) among the last K transitions)
against Lean's `pathE` (Review2.lean output). Also nb/regular of the thin tori via nb_compare.py.
    python3 review2_paths.py review2.out"""
import sys, itertools
from fractions import Fraction
import myface
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    from regular_check import grid, hull_cells
faces = {'hull1': myface.build('hull', (1,), hull_cells(1)), 'torus111': myface.build('torus', (1, 1, 1), grid(1, 1))}
lean = {}
for line in open(sys.argv[1]):
    if line.startswith('PATH '):
        _, name, n, K, x, d, b = line.split()
        lean[(name, int(n), int(K), int(x))] = (Fraction(d), Fraction(b))
bad = 0
for (name, n, K, x), (d, b) in sorted(lean.items()):
    F = faces[name]; A = F['A']
    at = myface.a_table(F)
    P = [myface.kernel_row(at[u], A) for u in range(2 ** A)]
    half = (A + 1) // 2
    pop = lambda s: bin(s).count('1')
    md = mb = Fraction(0)
    for path in itertools.product(range(2 ** A), repeat=n):
        seq = (x,) + path
        if not (seq[-1] == 0 and all(s != 0 for s in seq[:-1])):
            continue
        w = Fraction(1)
        for u, v in zip(seq, seq[1:]):
            w *= P[u][v]
        md += w
        tr = list(zip(seq, seq[1:]))[-K:]
        if any(pop(u) - pop(v) >= half for u, v in tr):
            mb += w
    ok = (md == d and mb == b)
    bad += not ok
print('pathE checks: %d (face, n, K, start) cases, %d mismatches' % (len(lean), bad))
print('PASS' if bad == 0 else 'FAIL')
