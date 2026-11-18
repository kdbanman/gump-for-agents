#!/usr/bin/env python3
"""How much of a tube's discount is the frequency of the four-layer over-fill?   (as joint2.py, with layers 2-4)
    python3 joint3.py TUBE WIDE  (equal area; runs with a LAYERS file, run_f.sh)  -> out/joint3_TUBE_WIDE.txt
Launch state = (P, S) at the launch, S = U + W3 + W4 (populations of layers 2, 3, 4). d pooled over both shapes.
ln R = ln [sum nu_tube(state) d(state) / sum nu_wide(state) d(state)]: the rate ratio that the frequencies of the
launch states alone would give, for state = P; (P, S); P + S. Errors: bootstrap over the deaths."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
def load(nm):
    s = open(os.path.join(SCR, nm + '.sum')).read().split(); A = int(s[5]); ex = float(s[s.index('expoF') + 1])
    G = np.fromfile(os.path.join(SCR, nm + '.GS')).reshape(A + 1, -1); L = []
    for l in open(os.path.join(SCR, nm + '.deaths')):
        r = [int(x) for x in l.split()[2:]]; P, U, W3, W4 = (np.array(r[i * 32:(i + 1) * 32]) for i in range(4)); j = np.nonzero(P >= (A + 1) // 2)[0]
        if len(j): L.append((P[j[0]], U[j[0]] + W3[j[0]] + W4[j[0]]))
    return A, G, np.array(L), ex
a, b = sys.argv[1:3]; A, Ga, La, ea = load(a); A2, Gb, Lb, eb = load(b); assert A == A2
tot = np.add.outer(np.arange(Ga.shape[0]), np.arange(Ga.shape[1]))
def fold(G): return np.bincount(tot.ravel(), weights=G.ravel(), minlength=tot.max() + 1)
def parts(La, Lb):
    Ha = np.zeros_like(Ga); Hb = np.zeros_like(Gb); np.add.at(Ha, (La[:, 0], La[:, 1]), 1); np.add.at(Hb, (Lb[:, 0], Lb[:, 1]), 1)
    out = []
    with np.errstate(all='ignore'):
        for f in (lambda X: X.sum(1), lambda X: X, fold):
            d = np.nan_to_num(f(Ha + Hb) / f(Ga + Gb)); out.append(np.log((f(Ga) / Ga.sum() * d).sum() / (f(Gb) / Gb.sum() * d).sum()))
    return out
r = parts(La, Lb); rng = np.random.default_rng(1)
bs = np.array([parts(La[rng.integers(0, len(La), len(La))], Lb[rng.integers(0, len(Lb), len(Lb))]) for i in range(200)]).std(0)
out = [f'{a} against {b} (A = {A}; {len(La)} and {len(Lb)} deaths): ln rate tube - wide = {np.log((len(La) / ea) / (len(Lb) / eb)):+.3f} +- {(1 / len(La) + 1 / len(Lb)) ** .5:.3f}',
       f'  frequency part with the launch state = P:            {r[0]:+.3f} +- {bs[0]:.3f}',
       f'  frequency part with the launch state = (P, S):       {r[1]:+.3f} +- {bs[1]:.3f}',
       f'  frequency part with the launch state = P + S:        {r[2]:+.3f} +- {bs[2]:.3f}',
       f'  mean launch (P, S)/A: tube ({La[:, 0].mean() / A:.3f}, {La[:, 1].mean() / A:.3f}), wide ({Lb[:, 0].mean() / A:.3f}, {Lb[:, 1].mean() / A:.3f})']
for nm, G in ((a, Ga), (b, Gb)):
    h = fold(G); x = np.arange(len(h)); m = (h * x).sum() / h.sum(); out.append(f'  {nm}: top four layers together: mean {m / A:.4f} A, variance per cell {((h * x * x).sum() / h.sum() - m * m) / A:.4f}')
open(os.path.join(HERE, 'out', f'joint3_{a}_{b}.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
