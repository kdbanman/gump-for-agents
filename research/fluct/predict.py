#!/usr/bin/env python3
"""Residence time at the current hull (memoryless) from a qsd_*.npz ensemble, and the predictive distribution of
the remaining wait of a single state now alive. D deaths in exposure E, prior flat in ln(rate): rate ~ Gamma(D, E),
so the remaining wait T has P(T > t) = (1 + t/E)^-D (Lomax).
  python3 research/fluct/predict.py TAG [TAG ...] [--now G]   (several TAGs: exposures and deaths pooled)
"""
import os, sys, math
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl
a = sys.argv[1:]; now = None
if '--now' in a: i = a.index('--now'); now = float(a[i + 1]); a = a[:i] + a[i + 2:]
D = E = 0
for tag in a:
    z = np.load(os.path.join(fl.SCR, f'qsd_{tag}.npz')); D += int(z['deaths'][0]); E += int(z['expo'][0])
    print(f'  {tag}: {int(z["deaths"][0])} deaths in {z["expo"][0]:.4g} generations')
lo, hi = stats.chi2.ppf([0.05, 0.95], 2 * D) / 2
print(f'mean residence tau = {E / D:.3g}  (90% CI {E / hi:.3g} .. {E / lo:.3g}; ln tau = {math.log(E / D):.2f} +- {1 / math.sqrt(D):.2f})')
q = lambda p: E * ((1 - p) ** (-1 / D) - 1)
print(f'remaining wait of one living state: median {q(0.5):.3g}, 50% interval {q(0.25):.3g} .. {q(0.75):.3g}, 90% interval {q(0.05):.3g} .. {q(0.95):.3g}')
if now:
    print(f'  -> death generation, given alive at {now:.4g}: median {now + q(0.5):.4g}, 90% interval {now + q(0.05):.4g} .. {now + q(0.95):.4g}')
