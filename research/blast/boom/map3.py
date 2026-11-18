#!/usr/bin/env python3
"""The face population as a map with one generation of memory: state (P(t-1), P(t)), next P(t+1).

    python3 map3.py NAME [MINCOUNT]   (NAME run with the M3 counts)  -> out/map3_NAME.txt

closure.py shows this pair is a sufficient state to a few per cent (the one-variable map and the pair (P, layer
beneath) are not). Here: its minimum action to an empty face, per cell, from the run's own counts, nothing fitted.
  model G: Gaussian step, cost (c - f(a,b))^2 / (2 v(a,b) A)
  model E: empirical step, cost sup_l [l (c - f) - ln E e^{l (P' - f)}] / A  (Legendre transform of the measured law)
V(b, c) = min_a V(a, b) + cost(a, b -> c), from the most visited pair; price = min V(a, b) + cost(a, b -> 0).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
nm = sys.argv[1]; MINC = int(sys.argv[2]) if len(sys.argv) > 2 else 100
s = open(os.path.join(SCR, nm + '.sum')).read().split(); A = int(s[5]); NA = A + 1; ex = float(s[s.index('expoF') + 1]); dth = int(s[s.index('deaths') + 1])
M3 = np.fromfile(os.path.join(SCR, nm + '.M3')).reshape(NA, NA, NA); N3 = M3.sum(2); ps = np.arange(NA)
ok = (N3 >= MINC); ok[:, 0] = False
lam = np.linspace(-4, 4, 401)
CG = np.full((NA, NA, NA), np.inf, np.float32); CE = np.full((NA, NA, NA), np.inf, np.float32)
for a, b in np.argwhere(ok):
    w = M3[a, b] / N3[a, b]; f = (w * ps).sum(); v = (w * ps ** 2).sum() - f * f
    if v <= 0: continue
    CG[a, b] = (ps - f) ** 2 / (2 * v * A)
    nz = w > 0; e = lam[:, None] * (ps[nz] - f)[None, :]; mx = e.max(1); Lam = mx + np.log((w[nz][None, :] * np.exp(e - mx[:, None])).sum(1))
    CE[a, b] = np.max(lam[:, None] * (ps - f)[None, :] - Lam[:, None], axis=0) / A
out = [f'{nm}: A {A}; {dth} deaths; ln tau / A = {np.log(ex / dth) / A:.4f}; pairs used (>= {MINC} visits): {int(ok.sum())}']
st = np.unravel_index(np.argmax(N3), N3.shape)
for lab, C in (('G', CG), ('E', CE)):
    V = np.full((NA, NA), np.inf, np.float32); V[st] = 0; prev = np.full((NA, NA), -1)
    for it in range(300):
        cand = V[:, :, None] + C                      # [a, b, c]
        best = cand.min(0); arg = cand.argmin(0); upd = best < V - 1e-7
        if not upd.any(): break
        V[upd] = best[upd]; prev[upd] = arg[upd]
    last = V + C[:, :, 0]; k = np.unravel_index(np.argmin(last), last.shape); price = float(last[k])
    path = [k[1], k[0]]; a, b = k
    while prev[a, b] >= 0 and len(path) < 60: a, b = prev[a, b], a; path.append(a)
    path = path[::-1]; top = max(path); i = path.index(top)
    Vtop = float(V[path[i - 1], top]) if i > 0 else 0.0
    out.append(f'  model {lab}: minimum action {price:.4f} per cell (A V = {A * price:.2f}); path {" ".join(map(str, path))} 0; top {top} ({top / A:.3f} A) reached at V = {Vtop:.4f}; the rest {price - Vtop:.4f}')
open(os.path.join(HERE, 'out', 'map3_' + nm + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
