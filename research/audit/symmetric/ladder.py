#!/usr/bin/env python3
"""ladder.py: the A = 63 (R = 11, cube-centred) group ladder and the slab case from this review's runs.
    python3 research/audit/symmetric/ladder.py"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ana
P = os.path.join(ana.SCR, 'lives_{}_{}_s{}.bin')
def one(s, g, seed, nf, low=False):
    a, t, fm, det = ana.load(P.format(s, g, seed))
    if low: a = np.where(t == 4, det if os.environ.get('LADDER_LOW') else a // 2, a)
    E, D, lt, se = ana.est(a, t, nf); return lt, se, E, D, a, t, fm
L = {}
for g, seed, nf in (('c1', 9101, 8), ('csz', 9102, 4), ('c2v', 9106, 2), ('d2h', 9103, 1), ('ci', 9104, 4), ('c2e', 9105, 4)):
    L[g] = one('v11c', g, seed, nf)
def d(x, y): return x[0] - y[0], math.hypot(x[1], y[1])
print('A = 63 ladder (ln tau_face, +- 1/sqrt(D))')
for g in L: print(f'  {g:4s} {L[g][0]:.4f} +- {L[g][1]:.4f}  (D = {L[g][3]})')
dl = one('v11c', 'd2h', 9103, 1, low=True)
print(f'  d2h with settled lives counted to half the snapshot age: {dl[0]:.4f}')
f16 = ana.SCR + '/lives_v11c_d2h_s9116.bin'
if os.path.exists(f16) and os.path.getsize(f16):
    a, t, fm, det = ana.load(f16); hi = ana.est(a, t, 1); lo = ana.est(np.where(t == 4, det, a), t, 1)
    print(f'  d2h, finer ladder (LADDER=16, seed 9116): {hi[2]:.4f} +- {hi[3]:.4f}, settled lives counted to the previous rung {lo[2]:.4f}')
for a_, b_ in (('csz', 'c1'), ('c2v', 'csz'), ('d2h', 'c2v'), ('ci', 'c1'), ('c2e', 'c1')):
    x, e = d(L[a_], L[b_]); print(f'  {a_} - {b_}: {x:+.4f} +- {e:.4f}')
# c2e split by face orbit: orbits 0 and 3 are edge-paired, 1 and 2 opposite-paired (geo.py order)
lt, se, E, D, a, t, fm = L['c2e']
late = (a > 512) & ((t == 1) | (t == 3))
edge = late & ((fm & (0b00000011 | 0b11000000)) != 0)   # faces 0,1 = (+++),(++-); 6,7 = (--+),(---)
opp = late & ((fm & 0b00111100) != 0)
for lab, m, k in (('edge-paired (2 orbits)', edge, 2), ('opposite-paired (2 orbits)', opp, 2)):
    Dk = int(m.sum()); l = math.log(k * E / Dk)
    print(f'  c2e {lab}: ln tau_face = {l:.4f} +- {1 / math.sqrt(Dk):.4f} (D = {Dk}); minus c1: {l - L["c1"][0]:+.4f} +- {math.hypot(1 / math.sqrt(Dk), L["c1"][1]):.4f}')
print('slab, 48 quotient cells')
s8 = one('s8x2', 'cs', 9108, 2); s4 = one('s4x2', 'c1', 9107, 2)
print(f'  s8x2 cs {s8[0]:.4f} +- {s8[1]:.4f}; s4x2 c1 {s4[0]:.4f} +- {s4[1]:.4f}; difference {s8[0] - s4[0]:+.4f} +- {math.hypot(s8[1], s4[1]):.4f}')
print('vertex-centred, R = 12 (A = 63)')
def split(sysn, seed):
    lt, se, E, D, a, t, fm = one(sysn, 'c2e', seed, 4)
    late = (a > 512) & ((t == 1) | (t == 3))
    out = []
    for m in (0b11000011, 0b00111100):
        Dk = int((late & ((fm & m) != 0)).sum()); out.append((math.log(2 * E / Dk), 1 / math.sqrt(Dk), Dk))
    return (lt, se), out
f12 = P.format('v12v', 'c1', 9115)
c12 = one('v12v', 'c1', 9115, 8) if os.path.exists(f12) and os.path.getsize(f12) else (14.3099, 0.0259)  # line's value if own run absent
cz = one('v12v', 'csz', 9118, 4); pooled, (ed, op) = split('v12v', 9117)
print(f'  c1 {c12[0]:.4f} +- {c12[1]:.4f}; csz {cz[0]:.4f} +- {cz[1]:.4f} (minus c1 {cz[0] - c12[0]:+.4f} +- {math.hypot(cz[1], c12[1]):.4f})')
print(f'  c2e pooled {pooled[0]:.4f} +- {pooled[1]:.4f}; edge-paired {ed[0]:.4f} +- {ed[1]:.4f} (D = {ed[2]}, minus c1 {ed[0] - c12[0]:+.4f} +- {math.hypot(ed[1], c12[1]):.4f}); '
      f'opposite-paired {op[0]:.4f} +- {op[1]:.4f} (D = {op[2]}, minus c1 {op[0] - c12[0]:+.4f} +- {math.hypot(op[1], c12[1]):.4f})')
print('asymmetric centring pairs, vertex minus cube at equal area')
for (sc, ss), (sv, sw), A in ((('v7c', 9111), ('v8v', 9112), 30), (('v9c', 9113), ('v10v', 9114), 45), (('v11c', 9101), ('v12v', 9115), 63)):
    fc, fv = P.format(sc, 'c1', ss), P.format(sv, 'c1', sw)
    if not (os.path.exists(fv) and os.path.getsize(fv)): print(f'  A = {A}: (vertex run absent)'); continue
    c, vv = one(sc, 'c1', ss, 8), one(sv, 'c1', sw, 8)
    print(f'  A = {A}: c {c[0]:.4f} +- {c[1]:.4f}, v {vv[0]:.4f} +- {vv[1]:.4f}, v - c {vv[0] - c[0]:+.4f} +- {math.hypot(c[1], vv[1]):.4f}')
