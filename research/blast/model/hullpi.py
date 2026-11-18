#!/usr/bin/env python3
"""hullpi.py (blast/model): the population distribution of the 63-cell hull face against the 63-cell wide torus
(ex5 files hist5_oct_11_c_c1.txt and hist5_gen_1_4_21_c1.txt + the long hist_gen_1_4_21_c1.txt), level by level.

    python3 research/blast/model/hullpi.py
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import boom as B, qsd
h = B.load5('oct_11_c_c1'); t = B.load5('gen_1_4_21_c1'); tl = qsd.load('gen_1_4_21_c1')
ph_h = h['ph']; ph_t = np.array(tl['ph'], float) + t['ph']
th, tt = ph_h[1:].sum(), ph_t[1:].sum()
print('63 cells, hull face against wide torus:  n   ln pi_hull   ln pi_torus   difference   slope hull   slope torus')
for n in list(range(1, 13)) + list(range(14, 52, 2)):
    if ph_h[n] < 30 or ph_t[n] < 30 or ph_h[n + 1] < 30 or ph_t[n + 1] < 30:
        continue
    a, b = math.log(ph_h[n] / th), math.log(ph_t[n] / tt)
    print(f'{n:3d} {a:9.3f} {b:9.3f} {a - b:+8.3f}   {math.log(ph_h[n + 1] / ph_h[n]):7.3f} {math.log(ph_t[n + 1] / ph_t[n]):7.3f}')
sl = lambda ph, a, b: (math.log(ph[b]) - math.log(ph[a])) / (b - a)
print(f'mean slope of ln pi over 4..12 cells: hull {sl(ph_h, 4, 12):.3f}, torus {sl(ph_t, 4, 12):.3f}')
print(f'deaths / pi(1): hull {h["fdeaths"] / ph_h[1]:.3f}, torus {(t["fdeaths"] + tl["fdeaths"]) / ph_t[1]:.3f}')
