#!/usr/bin/env python3
"""blast/strips: tables from the LIFE lines of strips.c.   python3 table.py [DIR ...]   (default: data/runs)
Pools runs of the same vessel (sums deaths and exposure). Two bookings: 'all' = every life ends at its first empty
face; 'nofw' = a life ends at the first firewall or empty face and only face deaths with no firewall before count."""
import sys, glob, os, math, re
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or [os.path.join(here, "data", "runs")]
NFACE = {"oct": 8, "prism": 4, "tet": 4, "slab": 2}
acc = defaultdict(lambda: [0, 0, 0, 0, 0])   # deaths, exposure, nofw deaths, nofw exposure, firewalls
for d in dirs:
    for fn in sorted(glob.glob(os.path.join(d, "*.txt"))):
        for line in open(fn):
            if not line.startswith("LIFE "): continue
            t = line.split(); key = (t[1], int(t[2]), int(t[3]))
            a = acc[key]; a[0] += int(t[t.index("deaths") + 1]); a[1] += int(t[t.index("exposure") + 1])
            if "nofw" in t:
                i = t.index("nofw"); a[2] += int(t[i + 2]); a[3] += int(t[i + 4]); a[4] += int(t[t.index("firewalls") + 1])
            else: a[2] += int(t[t.index("deaths") + 1]); a[3] += int(t[t.index("exposure") + 1])
def val(key, nofw=False):
    if key not in acc: return None
    a = acc[key]; d, x = (a[2], a[3]) if nofw else (a[0], a[1])
    if d == 0: return None
    return (math.log(NFACE[key[0]] * x / d), 1 / math.sqrt(d))
def fmt(v, nd=4): return "      --      " if v is None else f"{v[0]:.{nd}f} ± {v[1]:.{nd}f}"
def comb(terms, scale=1.0):
    """terms: list of (coefficient, value); returns (value, error) / scale or None"""
    if any(v is None for _, v in terms): return None
    return (sum(c * v[0] for c, v in terms) / scale, math.sqrt(sum((c * v[1]) ** 2 for c, v in terms)) / scale)

print("== every vessel: ln tau_face, both bookings")
print(f"{'vessel':16s} {'cells':>5s} {'all first deaths':>18s} {'deaths':>8s} {'no firewall before':>18s} {'deaths':>8s} {'fw%':>6s}")
cells = lambda k: {"oct": lambda p: 3 * ((p[0] + 1) // 2) * ((p[0] + 1) // 2 + 1) // 2, "prism": lambda p: 3 * (p[0] + 1) // 2 * p[1],
                   "tet": lambda p: 3 * p[0] * (p[0] + 1) // 2, "slab": lambda p: 3 * p[0] * p[1]}[k[0]](k[1:])
for key in sorted(acc):
    a = acc[key]; fw = 100.0 * a[4] / (a[4] + a[2]) if a[2] else float("nan")
    print(f"{key[0]+' '+str(key[1])+' '+str(key[2]):16s} {cells(key):5d} {fmt(val(key)):>18s} {a[0]:8d} {fmt(val(key, True)):>18s} {a[2]:8d} {fw:6.1f}")

RIM = {(4, 3): (8.1447, 0.0015), (4, 4): (11.0912, 0.0032), (4, 5): (13.8608, 0.0082), (4, 6): (16.4735, 0.0264),
       (5, 3): (9.6694, 0.0026), (5, 4): (13.4383, 0.0076), (5, 5): (16.8863, 0.0203), (6, 3): (11.2277, 0.0037), (6, 4): (15.7736, 0.0247)}
print("\n== referee's part: strips (w unit rows, L) against agent rim's table (all first deaths)")
for (w, L), r in sorted(RIM.items()):
    v = val(("prism", 2 * w - 1, L))
    if v is None: continue
    e = math.hypot(v[1], r[1])
    print(f"  ({2*w},{2*w},{L}) = strip w={w} L={L}: mine {fmt(v)}   rim {r[0]:.4f} ± {r[1]:.4f}   difference {v[0]-r[0]:+.4f} = {(v[0]-r[0])/e:+.1f} sigma")

for nofw in (False, True):
    S = lambda w, L: val(("prism", 2 * w - 1, L), nofw)
    print(f"\n== strips, booking: {'no firewall before the death (the lead\'s)' if nofw else 'all first deaths (rim\'s)'}")
    print("  ln tau(w, L):")
    for w in range(2, 7):
        row = [fmt(S(w, L)) for L in range(3, 9)]
        if any(S(w, L) for L in range(3, 9)): print(f"   w={w}: " + "  ".join(row))
    print("  width price per cell [ln tau(w+1,L) - ln tau(w,L)] / 3L:")
    for w in range(2, 6):
        row = [fmt(comb([(1, S(w + 1, L)), (-1, S(w, L))], 3 * L)) for L in range(3, 9)]
        if any("--" not in r for r in row): print(f"   w={w}->{w+1}: " + "  ".join(row))
    print("  length price per cell [ln tau(w,L+1) - ln tau(w,L)] / 3w:")
    for w in range(2, 7):
        row = [fmt(comb([(1, S(w, L + 1)), (-1, S(w, L))], 3 * w)) for L in range(3, 8)]
        if any("--" not in r for r in row): print(f"   w={w}, L->L+1 from 3: " + "  ".join(row))
    print("  mixed second difference per cell M(w+1/2, L+1/2):")
    for w in range(2, 6):
        row = [fmt(comb([(1, S(w + 1, L + 1)), (-1, S(w + 1, L)), (-1, S(w, L + 1)), (1, S(w, L))], 3)) for L in range(3, 8)]
        if any("--" not in r for r in row): print(f"   w={w}->{w+1}, L->L+1 from 3: " + "  ".join(row))

# closed tubes: mine, and the lead's table (research/constant/out/points.txt, firewall channel resolved)
LEAD = {(3, 6): (11.0824, 0.0004), (3, 8): (14.6209, 0.0029), (3, 10): (18.0457, 0.0114), (4, 4): (9.9324, 0.0020), (4, 5): (12.4865, 0.0009),
        (4, 6): (14.9710, 0.0016), (4, 7): (17.4645, 0.0047), (4, 8): (19.9430, 0.0184), (4, 9): (22.3727, 0.0423), (5, 5): (15.6614, 0.0026),
        (5, 6): (18.7862, 0.0112), (5, 7): (21.8897, 0.0402), (5, 8): (25.0456, 0.0727), (6, 6): (22.5684, 0.0411), (6, 7): (26.4045, 0.1043)}
print("\n== closed wrapped faces a x L (8-layer slab): mine, both bookings, against the lead's table (no firewall before)")
for key in sorted(k for k in acc if k[0] == "slab"):
    a, L = sorted(key[1:]); lead = LEAD.get((a, L))
    print(f"  {a}x{L}: all {fmt(val(key))}  nofw {fmt(val(key, True))}  lead {('%.4f ± %.4f' % lead) if lead else '--'}")
def T(g, a):   # closed tube of girth g and length a, nofw: the lead's value where it exists, else mine
    k = tuple(sorted((g, a)))
    if k in LEAD: return LEAD[k]
    for key in (("slab", a, g), ("slab", g, a)):
        if val(key, True): return val(key, True)
    return None
print("  width price of a closed tube of girth g, per cell, [ln tau(g x (a+1)) - ln tau(g x a)] / 3g  (lead's values where they exist, else mine):")
for g in (3, 4, 5, 6):
    out = []
    for a in range(3, 10):
        v = comb([(1, T(g, a + 1)), (-1, T(g, a))], 3 * g)
        if v: out.append(f"{a}->{a+1}: {fmt(v)}")
    v2 = [(a, comb([(1, T(g, a + 2)), (-1, T(g, a))], 6 * g)) for a in range(3, 9)]
    out += [f"{a}->{a+2}: {fmt(v)}" for a, v in v2 if v and not (T(g, a + 1))]
    print(f"   girth {g}: " + ";  ".join(out))

print("\n== tetrahedra and octahedra: ln tau_face by side, first and second differences per cell")
for ves, name in (("oct", "octahedron (anchors where not run)"), ("tet", "tetrahedron")):
    ANCH = {3: (4.855, 0.015), 4: (6.804, 0.003), 5: (9.819, 0.003), 6: (13.633, 0.008), 7: (18.141, 0.005), 8: (23.3392, 0.0099)}
    def G(s):
        v = val((ves, 2 * s - 1 if ves == "oct" else s, 0))
        return v if v else (ANCH.get(s) if ves == "oct" else None)
    print(f"  {name}")
    for s in range(2, 14):
        if not G(s): continue
        d1 = comb([(1, G(s)), (-1, G(s - 1))], 3 * s) if G(s - 1) else None
        d2 = comb([(1, G(s + 1)), (-2, G(s)), (1, G(s - 1))], 3) if G(s - 1) and G(s + 1) else None
        print(f"   side {s:2d} cells {3*s*(s+1)//2:3d}: ln tau {fmt(G(s))}   per added cell from side-1: {fmt(d1)}   second difference/3: {fmt(d2)}")
