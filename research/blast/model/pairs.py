#!/usr/bin/env python3
"""pairs.py (blast/model): where along the dip does a tube part from a wide face of the same area?
Delta(n) = ln pi_tube(n) - ln pi_wide(n) from the population histograms (long runs where on file, else the short
ones), against the measured discount D = ln tau_wide - ln tau_tube of the pair. If Delta(n) has reached D at some
level and stays there, the discount is made above that level and the tails are parallel below it.

    python3 research/blast/model/pairs.py
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qsd


def ph_of(spec):
    best = None
    for d in (qsd.DAT, qsd.SCR):
        for pre in ('hist_', 'hist_s_'):
            p = os.path.join(d, pre + spec + '.txt')
            if os.path.exists(p):
                for ln in open(p):
                    u = ln.split()
                    if u and u[0] == 'phist':
                        ph = [int(x) for x in u[1:]]
                        if best is None or sum(ph) > sum(best):
                            best = ph
    return best


PAIRS = [('gen_1_5_22_c1', 'gen_1_4_22_c1', 66, 13.7710 - 13.6459), ('gen_1_12_28_c1', 'gen_1_4_28_c1', 84, 17.5387 - 17.3190),
         ('gen_1_16_36_c1', 'gen_6_0_6_c1', 108, 22.5414 - 22.1599)]
for t, w, A, D in PAIRS:
    a, b = ph_of(t), ph_of(w)
    if a is None or b is None:
        continue
    ta, tb = sum(a[1:]), sum(b[1:])
    ma = sum(n * c for n, c in enumerate(a) if n) / ta
    print(f'\n{t} against {w} (A = {A}); measured D = {D:.3f}; samples {ta:.2e}, {tb:.2e}')
    print('  n   n/Pbar  Delta(n) (se)   slope tube  slope wide')
    for n in range(1, int(ma) + 1):
        if a[n] < 200 or b[n] < 200 or a[n + 1] < 200 or b[n + 1] < 200:
            continue
        dl = math.log(a[n] / ta) - math.log(b[n] / tb); se = math.sqrt(1 / a[n] + 1 / b[n]) * 4   # x4: correlated samples
        print(f'  {n:3d} {n / ma:6.2f}  {dl:+7.3f} ({se:.3f})   {math.log(a[n + 1] / a[n]):6.3f}  {math.log(b[n + 1] / b[n]):6.3f}')
