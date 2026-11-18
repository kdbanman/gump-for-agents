#!/usr/bin/env python3
"""The jump's tail on the 63-cell torus: one-step histogram of (P',B') from the launch box |P-33|<=1, |B-25|<=2
against the Gaussian with the histogram's own mean and covariance.  box.py t63.tal [P B]"""
import sys, numpy as np
h = np.zeros((128, 128))
for line in open(sys.argv[1]):
    w = line.split()
    if w[0] == 'H': h[int(w[1]), int(w[2])] = float(w[3])
tp, tb = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (46, 42)
n = h.sum(); P, B = np.meshgrid(np.arange(128), np.arange(128), indexing='ij')
mp = (h * P).sum() / n; mb = (h * B).sum() / n
vpp = (h * (P - mp) ** 2).sum() / n; vbb = (h * (B - mb) ** 2).sum() / n; vpb = (h * (P - mp) * (B - mb)).sum() / n
det = vpp * vbb - vpb ** 2
g = np.exp(-0.5 * (vbb * (P - mp) ** 2 - 2 * vpb * (P - mp) * (B - mb) + vpp * (B - mb) ** 2) / det) / (2 * np.pi * np.sqrt(det))
print(f"steps from the box {n:.4g}; mean ({mp:.2f},{mb:.2f}); var {vpp:.2f} {vbb:.2f} cov {vpb:.2f}")
for name, sel in (('point', (P == tp) & (B == tb)), ('3x3', (abs(P - tp) <= 1) & (abs(B - tb) <= 1)),
                  ('5x5', (abs(P - tp) <= 2) & (abs(B - tb) <= 2)), ('quadrant beyond', (P >= tp) & (B >= tb))):
    c = h[sel].sum(); gg = g[sel].sum()
    print(f"  ({tp},{tb}) {name:16s}: count {c:.0f}  -ln measured {-np.log(max(c,1e-300)/n):.3f}  -ln Gaussian {-np.log(gg):.3f}  excess {-np.log(max(c,1e-300)/n)+np.log(gg):+.3f} +- {1/np.sqrt(max(c,1)):.3f}")
