#!/usr/bin/env python3
"""Boom and bust in dying faces: populations of the dying face in its last 24 generations (`PATHFILE.pop` written
by `tube1d brute ... PATHFILE`; columns: age face pop(lag 0) ... pop(lag 23), lag 0 = the first empty generation).
    python3 pops.py A FILE.pop [FILE.pop ...]"""
import sys
import numpy as np
A = int(sys.argv[1])
for fn in sys.argv[2:]:
    P = np.array([[int(v) for v in l.split()[2:]] for l in open(fn) if l.strip()])
    n = len(P)
    fall = (P[:, 1:] - P[:, :-1]).max(axis=1)            # largest one-generation fall
    kf = (P[:, 1:] - P[:, :-1]).argmax(axis=1)           # lag (after the fall) at which it happened
    boom = P[:, :16].max(axis=1)
    s1 = (fall >= A / 2).mean(); s2 = (boom >= 0.70 * A).mean()
    e = lambda p: (p * (1 - p) / n) ** 0.5
    print(f"{fn.split('/')[-1]}: {n} deaths, A={A}; share with a one-generation fall of at least half the face {s1:.3f} +- {e(s1):.3f}; "
          f"share with population >= 0.70 A in the last 16 generations {s2:.3f} +- {e(s2):.3f}")
    print("   mean population at lags 0..11:", ' '.join(f"{v:.1f}" for v in P[:, :12].mean(axis=0)), f"  (stationary about {0.512*A:.1f})")
    b = fall >= A / 2
    if b.any(): print("   boom-and-bust deaths: mean population around the fall (2 before, before, after, 1 later, 2 later):",
          ' '.join(f"{np.mean([P[i, min(23, kf[i] + 1 + d)] for i in np.where(b)[0]]):.1f}" for d in (1, 0, -1, -2, -3)), f"; median lag of the fall {np.median(kf[b]):.0f}")
    if (~b).any(): print("   other deaths: mean population at lags 0..11:", ' '.join(f"{v:.1f}" for v in P[~b][:, :12].mean(axis=0)))
