#!/usr/bin/env python3
"""How deep is the boom? Layers 1-4 (face P, U, W3, W4) around the launch of the natural deaths.
    python3 deep.py NAME   (NAME run with a LAYERS file, see run_e.sh)  -> out/deep_NAME.txt
'given P': the mean (s.d.) over all face-generations with the same face population as the launch (from NAME.W, NAME.GU)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
for nm in sys.argv[1:]:
    p = os.path.join(SCR, nm); s = open(p + '.sum').read().split(); A = int(s[5]); NA = A + 1; L = (A + 1) // 2
    W = np.fromfile(p + '.W').reshape(NA, 5); G = np.fromfile(p + '.GU').reshape(NA, -1, 6)[:, :, 0]; us = np.arange(G.shape[1])
    n = W[:, 0]; tot = n.sum()
    with np.errstate(all='ignore'):
        m3 = W[:, 1] / n; s3 = (W[:, 2] / n - m3 ** 2) ** .5; m4 = W[:, 3] / n; s4 = (W[:, 4] / n - m4 ** 2) ** .5
        mU = (G * us).sum(1) / G.sum(1); sU = ((G * us ** 2).sum(1) / G.sum(1) - mU ** 2) ** .5
    M3 = W[:, 1].sum() / tot; M4 = W[:, 3].sum() / tot; MU = (G.sum(0) * us).sum() / G.sum(); MP = (n * np.arange(NA)).sum() / tot
    rows = [[int(x) for x in l.split()[2:]] for l in open(p + '.deaths')]
    acc = {k: [] for k in (-2, -1, 0, 1, 2, 3)}; z = []
    for r in rows:
        P, U, A3, A4 = (np.array(r[i * 32:(i + 1) * 32]) for i in range(4)); j = np.nonzero(P >= L)[0]
        if len(j) == 0 or j[0] < 3 or j[0] > 28: continue
        k = j[0]
        for dt in acc: acc[dt].append((P[k - dt], U[k - dt], A3[k - dt], A4[k - dt]))      # arrays run backwards in time
        z.append(((U[k] - mU[P[k]]) / sU[P[k]], (A3[k] - m3[P[k]]) / s3[P[k]], (A4[k] - m4[P[k]]) / s4[P[k]]))
    z = np.array(z)
    out = [f'{nm}: A {A}; {len(z)} deaths (those empty at least 4 generations after the launch); stationary means / A: P {MP / A:.3f}, U {MU / A:.3f}, layer 3 {M3 / A:.3f}, layer 4 {M4 / A:.3f}',
           '  generation relative to the launch:  P/A    U/A   layer 3 / A   layer 4 / A']
    for dt in sorted(acc):
        a = np.array(acc[dt], float).mean(0) / A; out.append(f'   {dt:+d}                                {a[0]:.3f}  {a[1]:.3f}    {a[2]:.3f}        {a[3]:.3f}')
    out.append(f'  at the launch, in s.d. of all face-generations with the same P: U {z[:, 0].mean():+.2f}, layer 3 {z[:, 1].mean():+.2f}, layer 4 {z[:, 2].mean():+.2f}')
    open(os.path.join(HERE, 'out', 'deep_' + nm + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
