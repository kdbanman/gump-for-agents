#!/usr/bin/env python3
"""samelevel.py -- hull face against wide torus of the same area at the same ABSOLUTE level L = x A (not a fraction of each P-bar).
Reads out/nu (hull rows) and out/w (torus rows); prints -ln nu, -ln q = ln tau + ln nu, and hull minus torus."""
import math, glob, os, numpy as np
here = os.path.dirname(os.path.abspath(__file__))
def load(fn, nf):
    c = None; e = 0.0
    for line in open(fn):
        t = line.split()
        if not t or t[0] != "NU": continue
        ic = t.index("cross"); ib = t.index("bust") if "bust" in t else len(t)
        v = np.array(list(map(float, t[ic + 1:ib]))); c = v if c is None else c + v
        e += nf * float(t[t.index("expo") + 1])
    return c / e
def at(nu, L):
    lo = int(math.floor(L)); f = L - lo
    return (1 - f) * math.log(nu[lo]) + f * math.log(nu[lo + 1])
H = {63: (13.633, load(os.path.join(here, "out/nu/nu11.txt"), 8)), 84: (18.141, load(os.path.join(here, "out/nu/nu13.txt"), 8)), 108: (23.3392, load(os.path.join(here, "out/nu/nu15.txt"), 8))}
T = {63: (13.1622, load(os.path.join(here, "out/w/w_1_4_21.txt"), 2)), 84: (17.5387, load(os.path.join(here, "out/w/w_1_4_28.txt"), 2)), 108: (22.5405, load(os.path.join(here, "out/w/w_6_0_6.txt"), 2))}
for x in (0.36, 0.31, 0.26, 0.21):
    row = []
    for A in (63, 84, 108):
        hn, tn = -at(H[A][1], x * A), -at(T[A][1], x * A)
        row.append(f"A {A}: -ln nu hull {hn:.3f} torus {tn:.3f} (hull - torus {hn - tn:+.3f}); -ln q hull {H[A][0] - hn:.3f} torus {T[A][0] - tn:.3f} ({(H[A][0] - hn) - (T[A][0] - tn):+.3f})")
    print(f"level {x} A: " + ";  ".join(row))
    hq = [H[A][0] + at(H[A][1], x * A) for A in (63, 84, 108)]; tq = [T[A][0] + at(T[A][1], x * A) for A in (63, 84, 108)]
    print(f"      slopes of -ln q per cell (63-84, 84-108): hull {(hq[1] - hq[0]) / 21:.4f} {(hq[2] - hq[1]) / 24:.4f}; torus {(tq[1] - tq[0]) / 21:.4f} {(tq[2] - tq[1]) / 24:.4f}")
