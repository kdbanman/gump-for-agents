#!/usr/bin/env python3
"""Face hazard in the first generations of a life, exact per generation (numpy stepper of fwcheck.py).

    python3 research/audit/shape2/earlycheck.py a k b R GENS SEED

R lives from p = 0.4 soups; counts first face deaths (before any firewall) and exposure in age bins of 32
generations; prints ln(2E/F) per bin. Used to decide between ts.c and research/shape2 (rep.c) where their hazard
in ages [0, 64) disagrees.
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwcheck import setup  # noqa


def main(L, R, gens, seed):
    n, NB, layers, f0, f1 = setup(L)
    rng = np.random.default_rng(seed)
    x = np.zeros((n + 1, R), bool); x[:n] = rng.random((n, R)) < 0.4
    alive = np.ones(R, bool)          # no event yet
    end = np.full(R, gens); isF = np.zeros(R, bool)
    for g in range(1, gens + 1):
        c = x[NB].sum(1)
        x[:n] = (c == 4) | (c == 5) | (x[:n] & (c == 3))
        xi = x[:n].astype(np.int32)
        fd = (f0 @ xi == 0) | (f1 @ xi == 0)
        fwh = np.zeros(R, bool)
        for M in layers:
            if M.shape[0] < 3:
                continue
            dead = (M.astype(np.int32) @ xi) == 0
            fwh |= (dead & np.roll(dead, -1, 0) & np.roll(dead, -2, 0)).any(0)
        newF = alive & fd & ~fwh; newW = alive & fwh
        end[newF | newW] = g; isF[newF] = True; alive &= ~(newF | newW)
    out = []
    for lo in range(0, gens, 32):
        hi = lo + 32
        ex = (np.clip(end, lo, hi) - lo).sum(); nf = int((isF & (end > lo) & (end <= hi)).sum())
        out.append(f'[{lo},{hi}):{math.log(2 * ex / nf) if nf else float("nan"):.3f}({nf})')
    ex = end.sum(); nf = int(isF.sum())
    print(f'{L} R {R} gens {gens}: ' + ' '.join(out) + f'; all ages < {gens}: {math.log(2 * ex / nf):.3f} +- {1 / math.sqrt(nf):.3f} ({nf})')


if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    main(tuple(a[:3]), a[3], a[4], a[5])
