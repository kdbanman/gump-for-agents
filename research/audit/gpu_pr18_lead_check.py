#!/usr/bin/env python3
"""Lead's own recomputation of the headline table of the GPU session's pull request 18 (empty patches on a large
living face, 12 x 12 x 8 slab), from the committed raw counts. Shares no code with research/gpu/patches.py.

  python3 research/audit/gpu_pr18_lead_check.py research/data/gpu_patches/patches_s81*_A10G.csv

Prints, per shape: cells, perimeter, hits, ln P (hits / samples, pooled over seeds and time batches), an error from
the scatter of the 96 batch values (batch means), and the persistence P(empty at t and t+1) / P(empty at t). Then
for the rhombi: the incremental cost per cell between consecutive sizes, the two-parameter fit
ln P = k - c*cells - sigma*perimeter over 2x2..4x5, and (POST HOC, the lead's reading after seeing the data, not a
forecast) the incremental cost against 1/sqrt(cells at the midpoint), whose intercept is what a form
ln P = k - c*n - s*sqrt(n) would give for c.
"""
import csv, math, sys, collections
import numpy as np

rows = []
for f in sys.argv[1:]:
    rows += list(csv.DictReader(open(f)))
by = collections.defaultdict(list)
meta = {}
for r in rows:
    by[r["shape"]].append((int(r["samples"]), int(r["hits"]), int(r["hits_t_and_t1"])))
    meta[r["shape"]] = (int(r["cells"]), int(r["perimeter"]))
out = {}
print(f"{'shape':14s} {'cells':>5s} {'perim':>5s} {'hits':>14s} {'ln P':>9s} {'+-':>6s} {'persist':>7s}  batches")
for sh, v in by.items():
    S = sum(a for a, _, _ in v); H = sum(b for _, b, _ in v); H2 = sum(c for _, _, c in v)
    if H == 0:
        print(f"{sh:14s} {meta[sh][0]:5d} {meta[sh][1]:5d} {H:14d}      -inf"); continue
    p = np.array([b / a for a, b, _ in v]); se = p.std(ddof=1) / math.sqrt(len(p)) / p.mean()
    out[sh] = (meta[sh][0], meta[sh][1], math.log(H / S), max(se, 1 / math.sqrt(H)))
    print(f"{sh:14s} {meta[sh][0]:5d} {meta[sh][1]:5d} {H:14d} {math.log(H / S):9.4f} {out[sh][3]:6.4f} {H2 / H:7.3f}  {len(v)}")
rh = [(k, *out[k]) for k in out if k.startswith("rhombus")]
rh.sort(key=lambda t: t[1])
print("\nrhombi: incremental cost per cell, and 1/sqrt(mid cells)")
xs, ys, es = [], [], []
for (a, b) in zip(rh[:-1], rh[1:]):
    d = -(b[3] - a[3]) / (b[1] - a[1]); e = math.hypot(a[4], b[4]) / (b[1] - a[1]); mid = 0.5 * (a[1] + b[1])
    print(f"  {a[0]:12s} -> {b[0]:12s}: {d:.4f} +- {e:.4f}   1/sqrt(n) = {1 / math.sqrt(mid):.4f}")
    if a[1] >= 12 and b[4] < 0.1: xs.append(1 / math.sqrt(mid)); ys.append(d); es.append(max(e, 1e-4))
sel = [t for t in rh if t[1] >= 12 and t[4] < 0.1]
A = np.array([[1, -t[1], -t[2]] for t in sel]); y = np.array([t[3] for t in sel]); w = 1 / np.array([t[4] for t in sel])
sol, *_ = np.linalg.lstsq(A * w[:, None], y * w, rcond=None)
chi = float((((A @ sol) - y) * w) @ (((A @ sol) - y) * w))
print(f"\nfit ln P = k - c n - sigma p over {sel[0][0]}..{sel[-1][0]}: c = {sol[1]:.4f}, sigma = {sol[2]:.4f}, chi2 = {chi:.0f} / {len(sel) - 3}")
X = np.array([[1, x] for x in xs]); sol2, *_ = np.linalg.lstsq(X, np.array(ys), rcond=None)
print(f"POST HOC: incremental cost = {sol2[0]:.4f} + {sol2[1]:.3f}/sqrt(n) (unweighted, {len(xs)} points); residuals "
      + ", ".join(f"{yy - (sol2[0] + sol2[1] * xx):+.4f}" for xx, yy in zip(xs, ys)))

# POST HOC (the lead's analysis after seeing the data; not a forecast). Along a sequence of similar shapes
# (a x a, or a x (a+1)) the perimeter grows by the same 16 pairs per step, so the SECOND difference of ln P removes
# both the constant and a perimeter term of any coefficient: c = -(second difference) / (second difference of cells).
d = {t[0]: t for t in rh}
def sec(names):
    v = [d[n] for n in names if n in d]
    for a, b, c3 in zip(v[:-2], v[1:], v[2:]):
        dn = (c3[1] - b[1]) - (b[1] - a[1]); dp = (c3[2] - b[2]) - (b[2] - a[2])
        cc = -((c3[3] - b[3]) - (b[3] - a[3])) / dn
        ee = math.sqrt(c3[4] ** 2 + 4 * b[4] ** 2 + a[4] ** 2) / dn
        print(f"  {a[0]} -> {b[0]} -> {c3[0]}: perimeter second difference {dp}, c = {cc:.4f} +- {ee:.4f}")
print("\nPOST HOC second differences (constant and perimeter term removed):")
sec([f"rhombus {a}x{a}" for a in range(1, 7)])
sec([f"rhombus {a}x{a + 1}" for a in range(1, 6)])
