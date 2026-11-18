#!/usr/bin/env python3
"""probe_kymo (push 8): a second wire beside the first on a ring, with a pulse on the second wire: a kymograph.

    python3 probe_kymo.py SYM PHASE B C R|L [--k 3] [--n 64] [--at U] [--T 200] [--every 8] [--quiet]

First wire: a ring of n units of wire B with the stretch d^k f from unit 20 (k = 0: plain).  Second wire: wire B under
symmetry SYM of probe8.syms(), phase PHASE, moved by (0, B, C); its pulse (the image of wire B's right- or left-going
pulse) is put at source unit U.  Printed every `every` generations: the second wire, one character per unit of the
ring ('.' as at rest, 'p' 1 to 4 cells differ, '#' more, '_' empty), and the first wire's hex letters.
Returns/prints at the end whether the first wire is exactly as it was and whether the pair stands without the pulse.
"""
import sys
import numpy as np
import lab8, wire8 as W, exp8 as X, probe8 as P
from lab8 import Lab, tr, unit


def run(si, ph, b, c, sname, k=3, n=64, at=10, T=200, every=8, quiet=False):
    S = P.syms(); g = S[si][2]
    L0 = Lab(0, n, ring=True)
    a = L0.arr(W.wire('B', 0, n)); L0.flip(a, X.pulseR(at) if sname == 'R' else X.pulseL(at)); L0.run(a, ph)
    w2 = P.place(L0.cells(a), g, b, c, n)
    r = L0.arr(W.wire('B', 0, n)); L0.run(r, ph); w2n = P.place(L0.cells(r), g, b, c, n)
    w2n1 = None
    word = '7' * 20 + ('d' * k + 'f' if k else '') + '7' * (n - 20 - (k + 1 if k else 0))
    w1 = X.hexword(word, 0)
    tube = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5
    L = Lab(0, n, -28, 28, -28, 32, ring=True)
    ref = L.arr(w1 | w2n); r0 = ref.copy(); L.run(ref, 2 * n); stands = bool(np.array_equal(ref, r0))
    x = L.arr(w1 | w2); ref = r0.copy()
    rows = []
    for t in range(0, T + 1, every):
        cells = L.cells(x); rc = L.cells(ref)
        c1 = frozenset(q for q in cells if tube(q)); c2 = cells - c1; r2 = rc - frozenset(q for q in rc if tube(q))
        line = ''
        for u in range(n):
            mine = {q for q in c2 if unit(q) == u}; rest = {q for q in r2 if unit(q) == u}
            dd = len(mine ^ rest)
            line += '_' if not mine else ('.' if dd == 0 else ('p' if dd <= 4 else '#'))
        first = X.hexletters(L, L.arr(c1), 0, n)
        rows.append((t, line, first))
        if not quiet:
            print(f'{t:4d} 2: {line}\n     1: {first}')
        L.run(x, every); L.run(ref, every)
    cells = L.cells(x); c1 = frozenset(q for q in cells if tube(q))
    same1 = c1 == frozenset(w1)
    if not quiet:
        print(f'pair stands without the pulse (2 laps): {stands}; first wire exactly as it was at the end: {same1}')
    return stands, same1, rows


if __name__ == '__main__':
    A = sys.argv
    opt = lambda name, dflt: int(A[A.index(name) + 1]) if name in A else dflt
    run(int(A[1]), int(A[2]), int(A[3]), int(A[4]), A[5], opt('--k', 3), opt('--n', 64), opt('--at', 10), opt('--T', 200), opt('--every', 8), '--quiet' in A)
