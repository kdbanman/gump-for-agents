#!/usr/bin/env python3
"""win.py DIR -- share of deaths (and of deep dips) that come within WIN generations of an over-full face (P >= 0.7 A),
for slab tori (DIR/win_t*.txt, rows of `sl nu H K D SEED GENS LAMA WIN`) and hulls (DIR/win_h*.txt, NUB rows of `rh nu R SEED GENS LAMA WIN`)."""
import sys, glob, os, math, collections
import numpy as np
agg = collections.OrderedDict()
for fn in sorted(glob.glob(os.path.join(sys.argv[1], "win_*.txt"))):
    for line in open(fn):
        t = line.split()
        if not t or t[0] not in ("NU", "NUB"): continue
        d = {t[i]: t[i + 1] for i in range(1, t.index("cross"), 2)}
        ic, ib = t.index("cross"), t.index("bust")
        c = np.array(list(map(float, t[ic + 1:ib]))); b = np.array(list(map(float, t[ib + 1:])))
        nf = 2 if t[0] == "NU" else 8
        name = ("torus " + d["T"]) if t[0] == "NU" else ("hull R " + d["R"])
        a = agg.setdefault((name, int(d["A"]), int(d["win"])), [0, 0, 0.0, 0.0, int(d["lamA"])])
        a[0] = a[0] + c; a[1] = a[1] + b; a[2] += nf * float(d["expo"]); a[3] += float(d["nover"])
for (name, A, W), (c, b, fg, nov, lamA) in sorted(agg.items()):
    r = nov / fg; chance = 1 - (1 - r) ** W
    pb = lamA - 0.5
    lv = lambda p: int(p * pb)
    s = f"{name} A {A} window {W:2d}: over-full rate {r:.2e}/face-gen, chance level {chance:.3f};  deaths: {b[0] / c[0]:.3f} ({int(b[0])}/{int(c[0])})"
    for p in (0.2, 0.4, 0.6):
        if c[lv(p)] >= 30: s += f";  dips to {p} P-bar: {b[lv(p)] / c[lv(p)]:.3f}"
    print(s)
