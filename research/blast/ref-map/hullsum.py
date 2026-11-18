#!/usr/bin/env python3
"""The deciding test: the hull's Gaussian-chain action and chain ln tau at 45, 63, 84 cells, each from its own map,
under several extrapolation rules and both definitions of B; per-cell price from differences.
  hullsum.py 7,9,11|9,11,13 [modes...]   -> prints a table; gump: ln tau = 1.14 + 0.2308 A - 0.342 k  (9.819, 13.633, 18.141)"""
import sys, os, numpy as np
from dp import Map, build, chain
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-map')
confs = sys.argv[1:] or ['visited:200', 'visited:50', 'visited:1000', 'nearest:200', 'poly2:200', 'poly3:200', 'carry:200', 'carryabs:200', 'carry:2000']
TR = sys.argv[1]; confs = sys.argv[2:] or confs      # first argument: the triple of radii, e.g. 7,9,11 or 9,11,13
RS = [int(r) for r in TR.split(',')]; KS = [(r + 1) // 2 for r in RS]; AS = [3 * k * (k + 1) // 2 for k in KS]
FILES = {7: 'h7.tal', 9: 'h9.tal', 11: 'h11.tal', 13: 'h13.tal+h13b.tal'}
GUMP = {7: 6.804, 9: 9.819, 11: 13.633, 13: 18.141}
def fit3(v):   # v at three consecutive sides k: v = a + c*A + b*k
    c = (v[2] - 2 * v[1] + v[0]) / 3; b = (v[1] - v[0]) - (AS[1] - AS[0]) * c; a = v[0] - AS[0] * c - KS[0] * b
    return a, c, b
g = [GUMP[r] for r in RS]; D1 = AS[1] - AS[0]; D2 = AS[2] - AS[1]
print("cells", AS)
print("gump            ln tau %7.3f %7.3f %7.3f | d1 %.4f %.4f | a %.2f c %.4f b %+.3f" % (*g, (g[1]-g[0])/D1, (g[2]-g[1])/D2, *fit3(g)))
for d in (0, 1):
    maps = [Map('+'.join(os.path.join(SCR, f) for f in FILES[R].split('+')), d) for R in RS]
    if d == 0:
        for m in maps:
            lt, e = m.lntau(); i = np.unravel_index(m.n.argmax(), m.n.shape)
            print(f"  A={m.A} nB={m.nB}: expo {m.expo:.3g} deaths {m.deaths:.0f} ln tau {lt:.3f}+-{e:.3f} mode {tuple(int(x) for x in i)} "
                  f"cov/A {m.vPP[i]/m.A:.3f} {m.vBB[i]/m.A:.3f} {m.vPB[i]/m.A:.3f} cells n>=200 {(m.n>=200).sum()} n>=50 {(m.n>=50).sum()}")
    for cf in confs:
        mode, nmin = cf.split(':'); nmin = int(nmin); Sv = []; Tv = []; routes = []
        for k, m in enumerate(maps):
            src = maps[k - 1] if (mode.startswith('carry') and k > 0) else None
            r = chain(m, *build(m, mode if (not mode.startswith('carry') or k > 0) else 'nearest', nmin, src))
            Sv.append(r['S']); Tv.append(r['lntau']); routes.append(r)
        print(f"d={d} {cf:13s} S      %7.3f %7.3f %7.3f | S/A %.4f %.4f %.4f | d1 %.4f %.4f | a %.2f c %.4f b %+.3f" %
              (*Sv, Sv[0]/AS[0], Sv[1]/AS[1], Sv[2]/AS[2], (Sv[1]-Sv[0])/D1, (Sv[2]-Sv[1])/D2, *fit3(Sv)))
        print(f"d={d} {cf:13s} ln tau %7.3f %7.3f %7.3f | -gump %+.3f %+.3f %+.3f | d1 %.4f %.4f | a %.2f c %.4f b %+.3f" %
              (*Tv, Tv[0]-g[0], Tv[1]-g[1], Tv[2]-g[2], (Tv[1]-Tv[0])/D1, (Tv[2]-Tv[1])/D2, *fit3(Tv)), flush=True)
        for m, r in zip(maps, routes):
            print(f"     A={m.A} route ({len(r['route'])} steps, max P {max(p for p,b in r['route'])}): " + ' '.join(f"({p},{b})" for p, b in r['route']))
