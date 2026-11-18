#!/usr/bin/env python3
"""The report's living-state estimator, ln tau = -ln nu_A(face >= 0.74 A) + 0.1273 A - 1.37 (research/blast/ref-boom/
STATIC.md; nu log-interpolated between the two whole numbers of cells round 0.74 A, as its ah.py does), evaluated on
this directory's own histograms of the living face, beside this directory's own lifetime and the anchor on file.

    python3 research/audit/blast/estimator.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyse as an
ROWS = [('wide torus (1,4),(0,21)', 63, ['slab63_s11', 'slab63_s12', 'slab63_s13', 'slab63_s14'], 13.1622),
        ('wide torus (1,4),(0,28)', 84, ['wide84_s41', 'wide84_s42'], 17.5387),
        ('tube (1,12),(0,28)', 84, ['tube84_s31', 'tube84_s32'], 17.3175),
        ('hull face, radius 11', 63, ['hull63_s21', 'hull63_s22', 'hull63_s23', 'hull63_s24'], 13.633),
        ('hull face, radius 13', 84, ['hull84_s51'], 18.141),
        ('hull face, radius 15', 108, ['hull108_s52'], 23.3392)]
print('face                        A   ln nu(>= 0.74 A)   estimator   ln tau here (deaths)     anchor   -ln P(population = 0.762 A)')
for name, A, pre, anchor in ROWS:
    S, H, J, K, L, Q, QB, DB = an.load_sum(pre)
    pr = H / H.sum(); cum = pr[::-1].cumsum()[::-1]
    u = 0.74 * A; ln = (1 - (u - int(u))) * np.log(cum[int(u)]) + (u - int(u)) * np.log(cum[int(u) + 1])
    lt = np.log(S['nfaces'] * S['exposure'] / S['deaths'])
    print(f'{name:26s} {A:3d}   {ln:9.4f}        {-ln + 0.1273 * A - 1.37:7.3f}     {lt:7.4f} +- {1 / np.sqrt(S["deaths"]):.4f} ({S["deaths"]})   {anchor:8.4f}   {-np.log(pr[int(round(0.762 * A))]):.3f}')
