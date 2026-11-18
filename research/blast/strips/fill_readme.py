#!/usr/bin/env python3
"""Fill the numbers that depend on the last runs into README.md (placeholders @KEY@ and bare keys), from data/runs."""
import glob, math, os, re
here = os.path.dirname(os.path.abspath(__file__))
acc = {}
for fn in glob.glob(os.path.join(here, "data", "runs", "*.txt")):
    for line in open(fn):
        if not line.startswith("LIFE "): continue
        t = line.split(); key = (t[1], int(t[2]), int(t[3])); a = acc.setdefault(key, [0, 0, 0, 0])
        a[0] += int(t[t.index("deaths") + 1]); a[1] += int(t[t.index("exposure") + 1])
        if "nofw" in t: i = t.index("nofw"); a[2] += int(t[i + 2]); a[3] += int(t[i + 4])
        else: a[2] += int(t[t.index("deaths") + 1]); a[3] += int(t[t.index("exposure") + 1])
def S(w, L): a = acc[("prism", 2 * w - 1, L)]; return (math.log(4 * a[3] / a[2]), a[2] ** -0.5)
def comb(terms, scale=1.0): return (sum(c * v[0] for c, v in terms) / scale, math.sqrt(sum((c * v[1]) ** 2 for c, v in terms)) / scale)
f4 = lambda v: f"{v[0]:.4f} ± {v[1]:.4f}"; f3 = lambda v: f"{v[0]:.3f} ± {v[1]:.3f}"
wp6 = comb([(1, S(5, 6)), (-1, S(4, 6))], 18); wp5 = comb([(1, S(5, 5)), (-1, S(4, 5))], 15)
m56 = comb([(1, S(5, 6)), (-1, S(5, 5)), (-1, S(4, 6)), (1, S(4, 5))], 3)
m45 = comb([(1, S(5, 5)), (-1, S(5, 4)), (-1, S(4, 5)), (1, S(4, 4))], 3)
g6 = comb([(1, S(5, 6)), (-1, S(4, 6))]); a6 = comb([(5, S(4, 6)), (-4, S(5, 6))])
tube6 = (0.2101, 0.0024); closed56 = (0.2134, 0.0040)
R = {"T96": f4(S(5, 6)), "N96": f"{acc[('prism', 9, 6)][0]:,}", "FWN96": f"{acc[('prism', 9, 6)][0]:,}",
     "WP6": f4(wp6), "WP6S": f"{wp6[0]:.4f}", "STEP6": f"{wp6[0] - wp5[0]:+.4f}",
     "LP56": f4(comb([(1, S(5, 6)), (-1, S(5, 5))], 15)), "L56": f3(comb([(1, S(5, 6)), (-1, S(5, 5))])),
     "DIFF6": f"{wp6[0] - tube6[0]:+.4f} ± {math.hypot(wp6[1], tube6[1]):.4f}",
     "M56": f4(m56), "M56S": f"{m56[0]:.3f}", "MSTEP": f"{m56[0] - m45[0]:+.3f}", "INC56": f3((3 * m56[0], 3 * m56[1])),
     "DM56": f"{m56[0] - closed56[0]:.3f} ± {math.hypot(m56[1], closed56[1]):.3f}",
     "G6": f3(g6), "A6": f3(a6), "A6S": f"{a6[0]:.2f}"}
if ("prism", 11, 5) in acc:
    R["T65"] = f3(S(6, 5)); R["WP56"] = f4(comb([(1, S(6, 5)), (-1, S(5, 5))], 15))
    R["M65"] = f3(comb([(1, S(6, 5)), (-1, S(6, 4)), (-1, S(5, 5)), (1, S(5, 4))], 3))
    d = comb([(1, S(4, 5)), (-2, S(5, 5)), (1, S(6, 5))]); R["DEF45"] = f"{-d[0]:.2f} ± {d[1]:.2f}"
    w56 = comb([(1, S(6, 5)), (-1, S(5, 5))], 15); R["WP56S"] = f"{w56[0]:.4f}"; R["STEP56"] = f"{w56[0] - 0.1947:+.4f}"
    R["M65S"] = "{:.3f}".format(comb([(1, S(6, 5)), (-1, S(6, 4)), (-1, S(5, 5)), (1, S(5, 4))], 3)[0])
s = open(os.path.join(here, "README.md")).read()
if os.path.exists(os.path.join(here, "scores.txt")): s = s.replace("SCORES\n", open(os.path.join(here, "scores.txt")).read())
for k, v in R.items(): s = s.replace("@" + k + "@", v)
for k in sorted(R, key=len, reverse=True): s = re.sub(r"(?<![A-Za-z0-9@])" + k + r"(?![A-Za-z0-9@])", R[k], s)
open(os.path.join(here, "README.md"), "w").write(s)
for k, v in sorted(R.items()): print(k, "=", v)
left = re.findall(r"@[A-Z0-9]+@", s); print("left:", left)
