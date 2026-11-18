#!/usr/bin/env python3
"""What else is special about a launch that ends in death? The layer beneath (U) at and around the launch.
    python3 hidden.py NAME   -> out/hidden_NAME.txt
For the natural deaths: U at the launch, one generation before and after, against the stationary E[U | P = p]
(from the run's (P, U) counts), by launch population p; and P one generation before the launch.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
HL = 32
def main(nm):
    p = os.path.join(SCR, nm); M = np.fromfile(p + '.M'); A = int(round(len(M) ** .5)) - 1; NA = A + 1; M = M.reshape(NA, NA); L = (A + 1) // 2
    GU = np.fromfile(p + '.GU').reshape(NA, -1, 6); NU = GU.shape[1]; us = np.arange(NU)
    cnt = GU[:, :, 0]; EU = (cnt * us).sum(1) / np.maximum(cnt.sum(1), 1); SU = ((cnt * us ** 2).sum(1) / np.maximum(cnt.sum(1), 1) - EU ** 2) ** .5
    ps = np.arange(NA); N = M.sum(0); T = M / np.maximum(M.sum(1), 1)[:, None]
    # stationary E[P(t-1) | P(t) = p]
    Eprev = (M * ps[:, None]).sum(0) / np.maximum(N, 1); Sprev = ((M * ps[:, None] ** 2).sum(0) / np.maximum(N, 1) - Eprev ** 2) ** .5
    rows = [[int(x) for x in l.split()[2:]] for l in open(p + '.deaths')]
    acc = {}
    for r in rows:
        P = np.array(r[:HL]); U = np.array(r[HL:2 * HL]); j = np.nonzero(P >= L)[0]
        if len(j) == 0 or j[0] == 0 or j[0] >= HL - 1: continue
        k = j[0]          # the arrays run backwards in time: index k - 1 is the generation AFTER the launch, k + 1 the one BEFORE
        acc.setdefault(P[k], []).append((U[k], U[k - 1], U[k + 1], P[k + 1], P[k - 1], U[k - 2] if k >= 2 else np.nan))
    out = []; w = out.append
    w(f'{nm}: A {A}; stationary mean of U {(cnt.sum(0) * us).sum() / cnt.sum():.2f}, of P {(cnt.sum(1) * ps).sum() / cnt.sum():.2f}')
    w('  p  theta  deaths | U at launch: deaths, all states with that p (s.d.), z | one generation before the launch (deaths): P, U; all states with that p: P (s.d.) | one generation after (deaths): P, U | two after: U')
    tz = []; 
    for pp in sorted(acc):
        a = np.array(acc[pp], float)
        if len(a) < 30: continue
        zU = (a[:, 0].mean() - EU[pp]) / SU[pp]; zP = (a[:, 3].mean() - Eprev[pp]) / Sprev[pp]
        w(f' {pp:3d} {pp / A:.3f} {len(a):6d} | {a[:, 0].mean():6.2f} {EU[pp]:6.2f} ({SU[pp]:.2f}) {zU:+.2f} | {a[:, 3].mean():6.2f} {a[:, 2].mean():6.2f}; {Eprev[pp]:6.2f} ({Sprev[pp]:.2f}) | {a[:, 4].mean():6.2f} {a[:, 1].mean():6.2f} | {np.nanmean(a[:, 5]):6.2f}')
        tz.append((len(a), zU, zP))
    tz = np.array(tz); w(f'  weighted over launches: U at launch is {np.average(tz[:, 1], weights=tz[:, 0]):+.2f} s.d. from the stationary mean given p; P one generation before the launch {np.average(tz[:, 2], weights=tz[:, 0]):+.2f} s.d. from the stationary mean given p')
    open(os.path.join(HERE, 'out', 'hidden_' + nm + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
for nm in sys.argv[1:]: main(nm)
