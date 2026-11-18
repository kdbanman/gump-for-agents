#!/usr/bin/env python3
"""Marginal price of an empty band from `tube1d bandp` output: local slopes of -ln P(empty) per face cell.
    python3 bandfit.py FILE [FILE ...]"""
import sys, math
for fn in sys.argv[1:]:
    rows = [l.split() for l in open(fn) if l.strip() and l[0].isdigit()]
    hdr = open(fn).readline().strip()
    print(hdr[:150])
    w = [float(r[0]) for r in rows]; cells = [float(r[1]) for r in rows]; y = [float(r[4]) for r in rows]; e = [float(r[5]) for r in rows]
    print("  width  cells  -lnP      err    | marginal price per cell from the previous width (err) | from two widths back")
    for i in range(len(rows)):
        s1 = (y[i] - y[i-1]) / (cells[i] - cells[i-1]) if i >= 1 else float('nan')
        e1 = math.hypot(e[i], e[i-1]) / (cells[i] - cells[i-1]) if i >= 1 else float('nan')
        s2 = (y[i] - y[i-2]) / (cells[i] - cells[i-2]) if i >= 2 else float('nan')
        e2 = math.hypot(e[i], e[i-2]) / (cells[i] - cells[i-2]) if i >= 2 else float('nan')
        print(f"  {w[i]:4.1f}  {cells[i]:5.1f}  {y[i]:8.4f}  {e[i]:.4f} |  {s1:.4f} ({e1:.4f})  |  {s2:.4f} ({e2:.4f})")
