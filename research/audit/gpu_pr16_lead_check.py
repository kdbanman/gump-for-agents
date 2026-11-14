#!/usr/bin/env python3
"""Lead's own re-derivation of pull request 16's headline numbers (GPU session: the width of a periodic slab face)
from the summary fields of its JSON files (exposure, face deaths). Shares no code with research/gpu/.

  python3 research/audit/gpu_pr16_lead_check.py DIR      DIR holds fwslab*.json

ln tau_face = ln(2 * exposure / face deaths) per slab s x M x 8 (s = short side, A = 3 s M), runs of one slab pooled.
Family slope b(s): weighted least squares of ln tau on A within one short side (weights = face deaths).

Results, 2026-11-14, on the files at branch head 0f14c27 (17 files, 14 slabs):
  s = 3: 11.082, 14.621, 18.046 at A = 54, 72, 90 (12.6%, 86.6%, 99.6% of lives ended by a firewall);
         b = 0.1959, chi2 80.3/1; local slopes 0.1966, 0.1902
  s = 4: 12.486, 14.971, 17.465, 19.943, 22.373 at A = 60..108 (0.5% .. 99.2%); b = 0.2072 +- 0.0001, chi2 4.2/3;
         local slopes 0.2071, 0.2078, 0.2065, 0.2025
  s = 5: 15.661, 18.786, 21.890, 25.046 at A = 75..120 (0.3% .. 92.1%); b = 0.2082 +- 0.0006, chi2 0.3/2
  s = 6: 22.568 +- 0.041, 26.405 +- 0.104 at A = 108, 126; b = 0.2131 +- 0.0062
  4x9 - 6x6 (A = 108): -0.196 +- 0.059;  3x8 - 4x6 (A = 72): -0.350 +- 0.003;  3x10 - 5x6 (A = 90): -0.740 +- 0.016
Every number in the pull request's table and outcome block is reproduced. What this check adds: (i) the family
s = 3 is not a straight line (chi2 80 on 1), and in both narrow families the local slope is lowest where firewalls
end over 99% of lives, which is where a bias from the competing channel would show; (ii) the headline pair at
A = 108 compares a slab with 99.2% firewall endings against one with 2.1%. Extrapolating the s = 4 family from its
three points with under 42% firewalls (slope 0.2075 from A = 84) gives 22.445 at A = 108, so the width difference
there is between -0.12 and -0.20 according to how much the last point is trusted: the sign stands either way;
(iii) b(4) and b(5) differ by 0.0010 +- 0.0006, so "the cost per cell rises with width" rests on s = 3 against the
rest and on the two s = 6 points (b(6) - b(5) = 0.005 +- 0.006), not on a monotone sequence.
Not checked here: the per-life rows, the code, the independence of the two channels (the adversarial review's job).
"""
import glob, json, math, sys
from collections import defaultdict

tot = defaultdict(lambda: [0, 0, 0])
for f in sorted(glob.glob(sys.argv[1] + "/fwslab*.json")):
    d = json.load(open(f)); n, m = sorted(d["slab"][:2])
    t = tot[(n, m)]; t[0] += d["exposure"]; t[1] += d["face"]; t[2] += d["fw"]
pts = {}
for (s, M), (E, nf, nw) in sorted(tot.items()):
    pts[(s, M)] = (3 * s * M, math.log(2 * E / nf), 1 / math.sqrt(nf), nf, nw)
fam = defaultdict(list)
for (s, M), v in pts.items(): fam[s].append(v)
for s in sorted(fam):
    v = sorted(fam[s])
    print(f"s = {s}: " + "; ".join(f"A={a}: {y:.3f}+-{e:.3f} ({nf} face, {100 * nw / (nf + nw):.1f}% fw)" for a, y, e, nf, nw in v))
    if len(v) >= 2:
        w = [1 / e ** 2 for _, _, e, _, _ in v]; W = sum(w)
        ma = sum(wi * a for wi, (a, *_) in zip(w, v)) / W; my = sum(wi * y for wi, (_, y, *_) in zip(w, v)) / W
        sxx = sum(wi * (a - ma) ** 2 for wi, (a, *_) in zip(w, v))
        b = sum(wi * (a - ma) * (y - my) for wi, (a, y, *_) in zip(w, v)) / sxx
        chi = sum(wi * (y - my - b * (a - ma)) ** 2 for wi, (a, y, *_) in zip(w, v))
        print(f"       slope b({s}) = {b:.4f} +- {1 / math.sqrt(sxx):.4f}, chi2 {chi:.1f}/{len(v) - 2}; "
              f"local: " + ", ".join(f"{(v[i + 1][1] - v[i][1]) / (v[i + 1][0] - v[i][0]):.4f}" for i in range(len(v) - 1)))
def diff(p, q):
    a, b = pts[p], pts[q]
    return f"{p[0]}x{p[1]} - {q[0]}x{q[1]} (A = {a[0]}): {a[1] - b[1]:+.3f} +- {math.hypot(a[2], b[2]):.3f}"
for p, q in (((4, 9), (6, 6)), ((3, 8), (4, 6)), ((3, 10), (5, 6))):
    if p in pts and q in pts: print(diff(p, q))
