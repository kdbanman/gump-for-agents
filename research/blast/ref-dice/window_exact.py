#!/usr/bin/env python3
"""ref-dice: the bust share as a share of actual deaths, exactly, without the QSD.

From the full face (or any start), propagate the joint law of (state, generations since the last fall of >= ceil(A/2)
live cells, capped at 6) and, at each generation t, split the death mass P(T = t) into deaths whose last 6
transitions (the death included) contain such a fall and the rest. For large t this is the quasi-stationary share
(the start is forgotten at rate |lambda_2/lambda_1|^t). Float64.

    python3 window_exact.py FACE [start]     (start default: the full face 2^A - 1; torus faces: 73)
"""
import sys
import numpy as np
import myface
from compare_kernel import KIND
from numerics import lean_cells


def main():
    name = sys.argv[1]
    kind, args = KIND[name]
    F = myface.build(kind, args, lean_cells(name))
    A = F['A']; n = 2 ** A
    at = myface.a_table(F)
    af = np.array([[float(a) for a in row] for row in at])
    P = np.ones((n, n))
    ys = np.arange(n)
    for i in range(A):
        bit = (ys >> i) & 1
        P *= np.where(bit[None, :] == 1, af[:, i:i + 1], 1 - af[:, i:i + 1])
    pop = np.array([bin(x).count('1') for x in range(n)])
    half = (A + 1) // 2
    big = (pop[:, None] - pop[None, :]) >= half            # transition x -> y is a fall
    start = int(sys.argv[2]) if len(sys.argv) > 2 else (73 if kind == 'torus' else n - 1)
    # J[c][x]: mass at state x (alive) with c = generations since the last fall (c = 6: none in the last 6)
    J = np.zeros((7, n)); J[6, start] = 1.0
    out = []
    for t in range(1, 121):
        NJ = np.zeros((7, n))
        dead_bust = dead_fade = 0.0
        for c in range(7):
            if not J[c].any():
                continue
            flow = J[c][:, None] * P                          # x -> y
            fb = (flow * big).sum(0); fn = (flow * ~big).sum(0)
            # death: y = 0
            dead_bust += fb[0] + (fn[0] if c < 5 else 0.0)     # c < 5: an earlier fall within the last 6 transitions
            dead_fade += fn[0] if c >= 5 else 0.0
            fb[0] = fn[0] = 0.0
            NJ[0] += fb
            NJ[min(c + 1, 6)] += fn
        J = NJ
        tot = dead_bust + dead_fade
        out.append((t, tot, dead_bust / tot if tot else float('nan')))
    allb = sum(tot * sh for t, tot, sh in out); allm = sum(tot for t, tot, sh in out)
    print('%s from %d: share of ALL deaths (t <= 120, mass %.8f): %.6f' % (name, start, allm, allb / allm))
    for t, tot, sh in out:
        if t in (6, 10, 20, 40, 60, 80, 100, 120):
            print('%s from %d: t = %3d  P(T = t) = %.3e  bust share of the deaths at t: %.10f' % (name, start, t, tot, sh))


if __name__ == '__main__':
    main()
