#!/usr/bin/env python3
"""The case research/signals/sat_div.py leaves out: the out-train (left of the object) one generation out of step
with the in-train (right), i.e. the wire C on the two sides of the object in opposite phases.  Uses sat_div.build
and sat_div.check unchanged; only the left pattern is advanced by one generation:
    pat'[0][j] = pat[1][j],  pat'[1][j] = pat[0][(j+1) mod L]     (two generations on, unit j holds unit j+1).
Controls: OUT = IN = 5f with the advance must be UNSAT for W = 1 unless a phase-slip object exists, and without the
advance (--noadv) must be SAT (the train itself).
    python3 sat_div_parity.py OUT IN W [--lo 1 --hi 5] [--noadv] [--timeout 1200]"""
import sys, os, math, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'signals'))
import sat_div as SD, sat_gun as G

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('inp'); ap.add_argument('W', type=int)
ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=1200)
ap.add_argument('--noadv', action='store_true')
a = ap.parse_args()
patL, sL = G.train([int(ch, 16) for ch in a.out]); patR, sR = G.train([int(ch, 16) for ch in a.inp])
LL, LR = len(patL[0]), len(patR[0])
if not a.noadv:
    patL = [list(patL[1]), [patL[0][(j + 1) % LL] for j in range(LL)]]
T = 2 * LL * LR // math.gcd(LL, LR)
for s in range(LL):
    t0 = time.time()
    R, pb, X = SD.build(patL, patR, T, a.W, s, a.lo, a.hi, a.KS)
    st, m = pb.solve('cadical153', a.timeout)
    tag = f'{sR} in, {sL} out {"in step" if a.noadv else "ONE GENERATION OUT OF STEP"} (shift {s}), T={T}, W={a.W}, tube [{a.lo},{a.hi}]'
    if st != 'SAT':
        print(f'{st:7s} {tag} {time.time() - t0:.0f}s', flush=True); continue
    obj = sorted(R.cells[i] for i in range(R.n) if a.KS <= R.units[i] < a.KS + a.W and X[0][i] in m)
    ok, info = SD.check(patL, patR, obj, T, a.W, s, a.KS)
    print(f'SAT     {tag} {time.time() - t0:.0f}s; object of {len(obj)} cells; re-stepped {"OK" if ok else "FAIL"} ({info})', flush=True)
    print('   object:', obj)
