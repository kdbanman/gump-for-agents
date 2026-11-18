#!/usr/bin/env python3
"""pair66.py (blast/model): tube against wide torus at 66 cells in the boom-and-bust decomposition (ex5 files).
Is the tube's shorter life in the boom (no: upper.py), in the fall, in the kill, or in deaths without a bust?

    python3 research/blast/model/pair66.py [TUBE WIDE]
"""
import math, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import boom as B
tb, wd = (sys.argv[1:3] if len(sys.argv) > 2 else ('gen_1_5_22_c1', 'gen_1_4_22_c1'))
T, W = B.load5(tb), B.load5(wd)
n = np.arange(128)
out = {}
for lab, o in (('tube', T), ('wide', W)):
    ph = o['ph']; tot = ph[1:].sum(); m = (n[1:] * ph[1:]).sum() / tot; sd = math.sqrt((((n[1:] - m) ** 2) * ph[1:]).sum() / tot)
    out[lab] = dict(m=m, sd=sd, tot=tot, lntau=math.log(o['expo'] / o['fdeaths']), F=o['fdeaths'])
hi = int(math.ceil(out['wide']['m'] + 2 * out['wide']['sd']))        # one threshold for both: the wide face's mean + 2 sd
print(f"tube {tb}: ln tau {out['tube']['lntau']:.3f} ({out['tube']['F']:.0f} deaths);  wide {wd}: ln tau {out['wide']['lntau']:.3f} ({out['wide']['F']:.0f} deaths);"
      f"  over-full = P >= {hi} on both")
print('lag   over-full share of dying faces: tube (se)   wide (se)   difference')
tot_t = tot_w = 0.0
st = {lab: (o['ph'][n >= hi].sum() / o['ph'][1:].sum()) for lab, o in (('tube', T), ('wide', W))}
for L in range(2, 10):
    a = T['dl'][L][n >= hi].sum() / T['dl'][L].sum(); b = W['dl'][L][n >= hi].sum() / W['dl'][L].sum()
    sa = math.sqrt(a * (1 - a) / T['dl'][L].sum()); sb = math.sqrt(b * (1 - b) / W['dl'][L].sum())
    tot_t += a - st['tube']; tot_w += b - st['wide']
    print(f'{L:3d}   {a:.3f} ({sa:.3f})   {b:.3f} ({sb:.3f})   {a - b:+.3f}')
print(f"stationary over-full share: tube {st['tube']:.4f}, wide {st['wide']:.4f};  excess summed over lags 2-9: tube {tot_t:.3f}, wide {tot_w:.3f}")
print('fall map and kill at equal population P:  P   E[next|P] tube, wide   P(next <= 16 | P) tube, wide   g_4(P) tube, wide (deaths)')
for P in range(hi, hi + 14, 2):
    rt, rw = T['J'][P], W['J'][P]
    if rt.sum() < 200 or rw.sum() < 200:
        continue
    print(f"  {P:3d}   {(n * rt).sum() / rt.sum():6.2f} {(n * rw).sum() / rw.sum():6.2f}    {rt[n <= 16].sum() / rt.sum():.4f} {rw[n <= 16].sum() / rw.sum():.4f}    "
          f"{T['dl'][4][P] / T['ph'][P]:.2e} {W['dl'][4][P] / W['ph'][P]:.2e} ({T['dl'][4][P]:.0f}, {W['dl'][4][P]:.0f})")
