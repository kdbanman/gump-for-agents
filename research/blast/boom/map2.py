#!/usr/bin/env python3
"""Two-variable return map (P, U): face population and the population of the layer beneath (the PI's request, 04:20 UTC).

    python3 map2.py NAME[+NAME2] [MINCOUNT]   -> out/map2_NAME.txt

From the plain run's moments by (P, U) at t (boom.c .GU): drift (E P', E U') and covariance of (P', U'), per state.
Gaussian model: (P', U') = drift(P, U) + noise with that covariance. Action per cell of a path = sum over steps of
delta^T Sigma^-1 delta / (2 A). Quasi-potential V from the most visited state by value iteration over the integer
grid; the price is min over states of V(state) + (drift_P)^2 / (2 Var_P A)  (one more step to an empty face).
Nothing is fitted; states with fewer than MINCOUNT visits (default 100) are not used as starting points of a step.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
names = sys.argv[1].split('+'); MINC = int(sys.argv[2]) if len(sys.argv) > 2 else 100
G = None; ex = 0; dth = 0
for nm in names:
    s = open(os.path.join(SCR, nm + '.sum')).read().split(); A = int(s[5]); ex += float(s[s.index('expoF') + 1]); dth += int(s[s.index('deaths') + 1])
    g = np.fromfile(os.path.join(SCR, nm + '.GU')).reshape(A + 1, -1, 6); G = g if G is None else G + g
NA, NU = G.shape[:2]; n = G[:, :, 0]
with np.errstate(all="ignore"):
    mP = G[:, :, 1] / n; mU = G[:, :, 2] / n; vP = G[:, :, 3] / n - mP ** 2; vU = G[:, :, 4] / n - mU ** 2; cv = G[:, :, 5] / n - mP * mU
    det = vP * vU - cv ** 2
ok = (n >= MINC) & (np.nan_to_num(det) > 1e-6) & (np.arange(NA)[:, None] > 0)
fi = np.argwhere(ok); nF = len(fi)
with np.errstate(all="ignore"):
    a = (vU / det)[ok]; b = (-cv / det)[ok]; c = (vP / det)[ok]; fP = mP[ok]; fU = mU[ok]; fvP = vP[ok]
pp, uu = np.meshgrid(np.arange(NA), np.arange(NU), indexing='ij'); pp = pp.ravel().astype(np.float32); uu = uu.ravel().astype(np.float32)
C = np.empty((nF, NA * NU), np.float32)
for i in range(nF):
    dP = pp - fP[i]; dU = uu - fU[i]; C[i] = (a[i] * dP * dP + 2 * b[i] * dP * dU + c[i] * dU * dU) / (2 * A)
fidx = fi[:, 0] * NU + fi[:, 1]
start = int(np.argmax(n)); V = np.full(NA * NU, np.inf, np.float32); V[start] = 0; prev = np.full(NA * NU, -1)
for it in range(200):
    cand = V[fidx][:, None] + C; best = cand.min(0); arg = cand.argmin(0); upd = best < V - 1e-7
    if not upd.any(): break
    V[upd] = best[upd]; prev[upd] = fidx[arg[upd]]
last = V[fidx] + fP ** 2 / (2 * fvP * A); k = int(np.argmin(last)); price = float(last[k])
path = [int(fidx[k])]
while prev[path[-1]] >= 0 and len(path) < 80: path.append(int(prev[path[-1]]))
path = path[::-1]
out = []; w = out.append
w(f'{"+".join(names)}: A {A}; {ex:.3g} face-generations, {dth} deaths, ln tau / A = {np.log(ex / dth) / A:.4f}; states used as starting points (>= {MINC} visits): {nF}')
w(f'  two-variable Gaussian map: minimum action to an empty face = {price:.4f} per cell (A V = {A * price:.2f})')
w('  path (P, U) and V per cell: ' + '  '.join(f'({q // NU},{q % NU}) {V[q]:.4f}' for q in path) + f'  -> empty {price:.4f}')
top = max(path, key=lambda q: q // NU); w(f'  top of the path: P = {top // NU} ({top // NU / A:.3f} A), U = {top % NU} ({top % NU / A:.3f} A), V = {V[top]:.4f}; the rest {price - V[top]:.4f}')
# the marginal quasi-potential of P in this model against the measured one
Vm = V.reshape(NA, NU).min(1); nuP = n.sum(1) / n.sum()
w('  V_min over U at P = theta A against measured -ln(nu sqrt(2 pi A 0.4))/A: ' + '; '.join(f'{th:.2f}: {Vm[int(round(th * A))]:.4f} / {-np.log(nuP[int(round(th * A))] * (2 * np.pi * A * 0.4) ** .5) / A:.4f}' for th in (0.66, 0.70, 0.74, 0.78, 0.82) if nuP[int(round(th * A))] > 0))
# drift in over-full states: regression of P' on (P, U) for P >= 0.68 A, weights n
sel = ok & (np.arange(NA)[:, None] >= 0.68 * A)
X = np.stack([np.ones(sel.sum()), np.argwhere(sel)[:, 0], np.argwhere(sel)[:, 1]], 1); wt = n[sel]
for lab, y in (("P'", mP[sel]), ("U'", mU[sel])):
    cf = np.linalg.lstsq(X * wt[:, None] ** .5, y * wt ** .5, rcond=None)[0]
    w(f"  over-full states (P >= 0.68 A): E[{lab}] = {cf[0]:.1f} + {cf[1]:.3f} P + {cf[2]:.3f} U")
open(os.path.join(HERE, 'out', 'map2_' + names[0] + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
