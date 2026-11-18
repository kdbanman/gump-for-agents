#!/usr/bin/env python3
"""probe_look (push 8): one placement of probe8's finite test in detail.

    python3 probe_look.py SYM PHASE B C R|L [--T 260]

Prints, for the first wire plain and with the stretch d^3 f: whether the pair stands without the pulse, the first
wire's letters after the pulse, and in how many cells the second wire then differs from the run without the pulse.
"""
import sys
import numpy as np
import lab8, wire8 as W, exp8 as X, probe8 as P
from lab8 import tr, Lab


def look(si, ph, b, c, sname, T=260, quiet=False):
    S = P.syms(); g = S[si][2]
    N1 = 52; N2 = 70
    o_st, _ = X.cell('7' * 24 + 'dddf' + '7' * 24, 0, 0); o_pl, _ = X.cell('7' * N1, 0, 0)
    w2obj, _ = X.cell('7' * N2, 0, 0)
    tube = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5
    L2 = Lab(-8, N2 + 16)
    mid = g(tr((0, 0, 0), 4 + N2 // 2)); shift = (4 + N1 // 2) - (mid[0] >> 1)
    u2 = 4 + N2 // 2 + (-14 if sname == 'R' else 14)
    a2 = L2.arr(w2obj); L2.flip(a2, X.pulseR(u2) if sname == 'R' else X.pulseL(u2)); L2.run(a2, ph)
    mv = lambda cells: frozenset(tr((q[0], q[1] + b, q[2] + c), shift) for q in (g(x) for x in cells))
    w2 = mv(L2.cells(a2))
    b2 = L2.arr(w2obj); L2.run(b2, ph); w2ref = mv(L2.cells(b2))
    out = {}
    for nm, o1 in (('plain', o_pl), ('stretch', o_st)):
        Lb = Lab(-24, N1 + 34, -22, 22, -18, 24)
        r0 = Lb.arr(o1 | w2ref); rr = r0.copy(); Lb.run(rr, T)
        stands = bool(np.array_equal(rr, r0))
        a = Lb.arr(o1 | w2); Lb.run(a, T)
        cells = Lb.cells(a); rc = Lb.cells(rr)
        c1 = frozenset(q for q in cells if tube(q)); r1 = frozenset(q for q in rc if tube(q))
        A1 = Lb.arr(c1)
        out[nm] = dict(stands=stands, first=X.hexrle(X.hexletters(Lb, A1, 4, 4 + N1)), first_same=c1 == r1, second_diff=len((cells - c1) ^ (rc - r1)))
        if not quiet:
            print(f"  {nm:8s}: pair stands without the pulse: {stands}; first wire after the pulse: {out[nm]['first']} ({'as without' if c1 == r1 else 'CHANGED'}); second wire differs in {out[nm]['second_diff']} cells")
    return out


if __name__ == '__main__':
    T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 260
    look(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], T)
