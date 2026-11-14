#!/usr/bin/env python3
"""Lead's own check of research/shape2/ (every torus of one area): the tables recomputed from the counts, the
shortest and second loops recomputed from the lattice, and the cost per cell by shortest loop.

  python3 research/audit/shape2_lead_check.py

ln tau_face = ln(2 * exposure / face deaths). A class is given by its canonical generators (a, k), (0, b); loops
have squared length x^2 + xy + y^2. Shares no code with research/shape2/.

Result, 2026-11-14: all 24 rows reproduce (shortest loop and ln tau from the counts). Cost per cell by shortest
loop^2, A = 48 -> 60 and 60 -> 72: 3: 0.1148, 0.1107; 4: 0.1414, 0.1353; 7: 0.1918, 0.1872; 12: 0.2073; 13: 0.2090;
16: 0.2125 (with research/shape's A = 72 values the second intervals are 0.2048, 0.2061, 0.2076 for 12, 13, 16).
At A = 48 the four classes with loop^2 12, 12, 13, 16 give 9.9243, 9.9384, 9.9390, 9.9324 (+- 0.0020). Not checked
here: the runs, the stepper on the thin tori, the law fits (the adversarial review, research/audit/REVIEW-shape2.md).
"""
import csv, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "shape2", "data")

def loops(a, k, b, R=40):
    q = sorted({X * X + X * Y + Y * Y for x in range(-R, R + 1) for y in range(-R, R + 1) if (x, y) != (0, 0)
                and math.gcd(x, y) == 1 for X, Y in [(a * x, k * x + b * y)]})
    return q[0], q[1]

tab = {}
for f in ("A48.csv", "A60.csv", "A72x.csv"):
    for r in csv.DictReader(open(os.path.join(D, f))):
        a, k, b = map(int, r["cls"].split()); A = int(r["A"]); assert 3 * a * b == A
        l1, l2 = loops(a, k, b); F = int(r["F"])
        lt = math.log(2 * float(r["exposure"]) / F); e = 1 / math.sqrt(F)
        ok = l1 == int(r["l1"]) and abs(lt - float(r["ln_tau_face"])) < 6e-4
        tab[(A, a, k, b)] = (l1, l2, lt, e, float(r["fw_share"]), r["thin"], ok)
for A in (48, 60, 72):
    print(f"A = {A}")
    for (AA, a, k, b), (l1, l2, lt, e, fw, thin, ok) in sorted(tab.items(), key=lambda t: (t[0][0], t[1][0], t[1][1])):
        if AA == A:
            print(f"  ({a},{k}),(0,{b})  loops^2 {l1:>3} {l2:>3}  ln tau {lt:8.4f} +- {e:.4f}  fw {fw:.3f}  {thin:5} {'ok' if ok else 'MISMATCH'}")
print("cost per cell by shortest loop (mean over classes of that loop at each area, then differences):")
for l1 in (3, 4, 7, 12, 13, 16):
    m = {}
    for A in (48, 60, 72):
        v = [(t[2], t[3]) for kk, t in tab.items() if kk[0] == A and t[0] == l1 and t[5] != "thin"]
        if v:
            w = [1 / e ** 2 for _, e in v]; m[A] = (sum(wi * y for wi, (y, _) in zip(w, v)) / sum(w), 1 / math.sqrt(sum(w)), len(v))
    s = "  ".join(f"A={A}: {m[A][0]:.3f} ({m[A][2]})" for A in m)
    d = "  ".join(f"{A1}->{A2}: {(m[A2][0] - m[A1][0]) / (A2 - A1):.4f}" for A1, A2 in ((48, 60), (60, 72)) if A1 in m and A2 in m)
    print(f"  loop^2 {l1:>2}: {s}   slope {d}")
