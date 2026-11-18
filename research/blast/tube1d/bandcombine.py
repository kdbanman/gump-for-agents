#!/usr/bin/env python3
"""Independent replications of `tube1d bandp` (same vessel, different seeds): mean and standard error over runs of
-ln P(band empty) and of the marginal price per cell between consecutive widths; also the pooled estimate.
    python3 bandcombine.py FILE1 FILE2 ...      (prints a table; pooled rows are written to stdout in bandp format with '#POOL')"""
import sys, math
import numpy as np
runs = []
for fn in [a for a in sys.argv[1:] if not a.startswith('--')]:
    hdr = open(fn).readline(); samples = float(hdr.split('samples=')[1])
    rows = {float(l.split()[0]): l.split() for l in open(fn) if l.strip() and l[0].isdigit()}
    runs.append((samples, rows))
widths = sorted(set.intersection(*[set(r[1]) for r in runs]))
n = len(runs)
print(f"# {n} independent runs; samples per run: " + ' '.join(f"{r[0]:.3g}" for r in runs))
print("# width cells | -lnP pooled | mean over runs +- s.e. over runs | naive err 1/sqrt(appearances) | price per cell from the previous width: pooled, mean over runs +- s.e. | boom share pooled")
prev = None; slopes = []
for w in widths:
    cnt = sum(float(r[1][w][2]) for r in runs); smp = sum(r[0] for r in runs); app = sum(float(r[1][w][6]) for r in runs)
    y = np.array([float(r[1][w][4]) for r in runs]); cells = float(runs[0][1][w][1])
    pooled = -math.log(cnt / smp)
    line = f"{w:4.1f} {cells:5.1f} | {pooled:8.4f} | {y.mean():8.4f} +- {y.std(ddof=1)/math.sqrt(n) if n > 1 else float('nan'):.4f} | {1/math.sqrt(app):.4f} |"
    if prev is not None:
        pw, pc, ppool, py = prev
        sl = (y - py) / (cells - pc)
        line += f" {(pooled - ppool)/(cells - pc):.4f}, {sl.mean():.4f} +- {sl.std(ddof=1)/math.sqrt(n) if n > 1 else float('nan'):.4f}"
    if prev is not None and n > 1: slopes.append((prev[0], w, (pooled - prev[2]) / (cells - prev[1]), sl.std(ddof=1) / math.sqrt(n)))
    print(line); prev = (w, cells, pooled, y)
    print(f"#POOL {w} {cells} {cnt:.0f} {cnt/smp:.6g} {pooled:.4f} {(y.std(ddof=1)/math.sqrt(n)) if n > 1 else 1/math.sqrt(app):.4f} {app:.0f} {cnt/app:.3f}")

# slopes file for margfit.py: l1 l2 pooled price per cell, standard error over the independent runs
out = [a for a in sys.argv[1:] if a.startswith('--out=')]
if out:
    with open(out[0][6:], 'w') as f:
        f.write(f"# marginal price of an empty band, pooled over {n} independent runs; columns: width1 width2 price_per_cell se_over_runs\n")
        for a, b, p, e in slopes: f.write(f"{a} {b} {p:.5f} {e:.5f}\n")
