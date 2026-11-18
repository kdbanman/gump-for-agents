#!/usr/bin/env python3
"""blast/ref-proofs: my own simulations of the tube (1,1),(0,D) (data/mc_tube11.txt) against rigour's rows, and the
branch rates from my points alone."""
import re, math
rig = {6: (5.1064, 0.0045, 0.8105, 0.0023), 8: (6.7278, 0.0045, 0.7131, 0.0026), 10: (8.2757, 0.0040, 0.5772, 0.0049), 12: (9.7304, 0.0054, 0.4165, 0.0102)}
mine = {}; D = None
for line in open('data/mc_tube11.txt'):
    m = re.match(r'== torus_1_1_(\d+)', line)
    if m: D = int(m.group(1))
    m = re.search(r'deaths (\d+)\s+halffall6 share ([\d.]+) \+- ([\d.]+)\s+lntau ([\d.]+) \+- ([\d.]+)', line)
    if m: mine[D] = (float(m.group(4)), float(m.group(5)), float(m.group(2)), float(m.group(3)), int(m.group(1)))
for D in sorted(mine):
    l, el, p, ep, n = mine[D]; rl, rel, rp, rep = rig[D]
    print('D=%2d deaths %6d  lntau %.4f+-%.4f (rigour %.4f+-%.4f: %+.1f sigma)   bust share %.4f+-%.4f (rigour %.4f+-%.4f: %+.1f sigma)' %
          (D, n, l, el, rl, rel, (l - rl) / math.hypot(el, rel), p, ep, rp, rep, (p - rp) / math.hypot(ep, rep)))
Ds = sorted(mine)
for a, b in zip(Ds, Ds[1:]):
    n = b - a; (la, ea, pa, epa, _), (lb, eb, pb, epb, _) = mine[a], mine[b]
    st = (lb - la) / n; est = math.hypot(ea, eb) / n
    cs = st - (math.log(1 - pb) - math.log(1 - pa)) / n; ecs = math.sqrt(est ** 2 + ((epa / (1 - pa)) ** 2 + (epb / (1 - pb)) ** 2) / n ** 2)
    cb = st - (math.log(pb) - math.log(pa)) / n; ecb = math.sqrt(est ** 2 + ((epa / pa) ** 2 + (epb / pb) ** 2) / n ** 2)
    print('%2d->%2d per unit: step %.3f+-%.3f   -d ln h_starve %.3f+-%.3f   -d ln h_bust %.3f+-%.3f' % (a, b, st, est, cs, ecs, cb, ecb))
