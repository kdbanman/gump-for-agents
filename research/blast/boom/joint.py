#!/usr/bin/env python3
"""The two-layer boom: joint over-fill of the face (P) and of the layer beneath (U), tube against torus.
    python3 joint.py TUBE TORUS  -> out/joint_TUBE_TORUS.txt
From the (P, U) counts of the plain runs (from-states): ln of the share of face-generations with P >= a A and U >= b A,
and the difference tube - torus with its counting error. Also Var(U)/A, Cov(P, U)/A."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
def load(nm):
    A = int(open(os.path.join(SCR, nm + '.sum')).read().split()[5]); G = np.fromfile(os.path.join(SCR, nm + '.GU')).reshape(A + 1, -1, 6)[:, :, 0]
    return A, G
a, b = sys.argv[1:3]; (A, Ga), (A2, Gb) = load(a), load(b); assert A == A2
out = []; w = out.append
for nm, G in ((a, Ga), (b, Gb)):
    ps = np.arange(G.shape[0])[:, None]; us = np.arange(G.shape[1])[None, :]; n = G.sum()
    mp = (G * ps).sum() / n; mu = (G * us).sum() / n
    w(f'{nm}: A {A}; mean P/A {mp / A:.5f}, U/A {mu / A:.5f}; Var P/A {((G * ps ** 2).sum() / n - mp ** 2) / A:.5f}; Var U/A {((G * us ** 2).sum() / n - mu ** 2) / A:.5f}; '
      f'Cov(P,U)/A {((G * ps * us).sum() / n - mp * mu) / A:.5f}; Var(P+U)/A {((G * (ps + us) ** 2).sum() / n - (mp + mu) ** 2) / A:.5f}')
w(f'ln share of face-generations with P >= a A and U >= b A: {a} / {b} / difference (+- counting error)')
w('  a \\ b ' + ''.join(f'{x:>34.2f}' for x in (0.0, 0.52, 0.56, 0.60, 0.64)))
for ta in (0.62, 0.66, 0.70, 0.72, 0.74, 0.76, 0.78):
    s = f'  {ta:.2f}  '
    for tb in (0.0, 0.52, 0.56, 0.60, 0.64):
        i = int(np.ceil(ta * A - 1e-9)); j = int(np.ceil(tb * A - 1e-9)); ca = Ga[i:, j:].sum(); cb = Gb[i:, j:].sum()
        s += f'   {np.log(ca / Ga.sum()):7.3f} /{np.log(cb / Gb.sum()):7.3f} / {np.log(ca / Ga.sum()) - np.log(cb / Gb.sum()):+.3f} ({(1 / ca + 1 / cb) ** .5:.3f})' if ca > 0 and cb > 0 else '                 -                '
    w(s)
w('the same for the sum: ln share with P + U >= s A')
for ts in (1.10, 1.20, 1.25, 1.30, 1.35, 1.40):
    k = int(np.ceil(ts * A - 1e-9)); idx = np.add.outer(np.arange(Ga.shape[0]), np.arange(Ga.shape[1])) >= k
    ca = Ga[idx].sum(); cb = Gb[idx].sum()
    if ca > 0 and cb > 0: w(f'  {ts:.2f}   {np.log(ca / Ga.sum()):7.3f} /{np.log(cb / Gb.sum()):7.3f} / {np.log(ca / Ga.sum()) - np.log(cb / Gb.sum()):+.3f} ({(1 / ca + 1 / cb) ** .5:.3f})')
open(os.path.join(HERE, 'out', f'joint_{a}_{b}.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
