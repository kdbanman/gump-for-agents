#!/usr/bin/env python3
"""How much of a tube's discount is the frequency of the two-layer over-fill?
    python3 joint2.py TUBE WIDE   (equal area)  -> out/joint2_TUBE_WIDE.txt
Launch state = (P, U) at the launch. d(p, u) = launches at (p, u) / face-generations at (p, u), pooled over both
shapes. If d(p, u) did not depend on the shape, the ratio of the rates would be
    R2 = sum nu_tube(p, u) d(p, u) / sum nu_wide(p, u) d(p, u)        (the '(P, U)-frequency part' of the discount)
and with d pooled over u as well, R1 = sum nu_tube(p) d(p) / sum nu_wide(p) d(p)  (the 'P-frequency part').
Errors: bootstrap over the pooled deaths (the counts of face-generations are large)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
def load(names):
    G = None; L = []; ex = 0
    for nm in names.split('+'):
        s = open(os.path.join(SCR, nm + '.sum')).read().split(); A = int(s[5]); ex += float(s[s.index('expoF') + 1])
        g = np.fromfile(os.path.join(SCR, nm + '.GU')).reshape(A + 1, -1, 6)[:, :, 0]; G = g if G is None else G + g
        for l in open(os.path.join(SCR, nm + '.deaths')):
            r = [int(x) for x in l.split()[2:]]; P = np.array(r[:32]); U = np.array(r[32:64]); j = np.nonzero(P >= (A + 1) // 2)[0]
            if len(j): L.append((P[j[0]], U[j[0]]))
    return A, G, np.array(L), ex
a, b = sys.argv[1:3]; A, Ga, La, ea = load(a); A2, Gb, Lb, eb = load(b); assert A == A2
def parts(La, Lb):
    Ha = np.zeros_like(Ga); Hb = np.zeros_like(Gb)
    np.add.at(Ha, (La[:, 0], La[:, 1]), 1); np.add.at(Hb, (Lb[:, 0], Lb[:, 1]), 1)
    with np.errstate(all='ignore'):
        d2 = np.nan_to_num((Ha + Hb) / (Ga + Gb)); d1 = np.nan_to_num((Ha + Hb).sum(1) / (Ga + Gb).sum(1))
    R2 = ((Ga / Ga.sum()) * d2).sum() / ((Gb / Gb.sum()) * d2).sum()
    R1 = ((Ga.sum(1) / Ga.sum()) * d1).sum() / ((Gb.sum(1) / Gb.sum()) * d1).sum()
    return np.log(R1), np.log(R2), np.log((len(La) / ea) / (len(Lb) / eb))
r1, r2, r0 = parts(La, Lb); rng = np.random.default_rng(1); bs = []
for i in range(300):
    bs.append(parts(La[rng.integers(0, len(La), len(La))], Lb[rng.integers(0, len(Lb), len(Lb))]))
bs = np.array(bs).std(0)
out = [f'{a} against {b} (A = {A}; {len(La)} and {len(Lb)} deaths): ln rate tube - wide = {r0:+.3f} +- {(1 / len(La) + 1 / len(Lb)) ** .5:.3f}',
       f'  P-frequency part       ln R1 = {r1:+.3f} +- {bs[0]:.3f}',
       f'  (P, U)-frequency part  ln R2 = {r2:+.3f} +- {bs[1]:.3f}',
       f'  mean launch (P, U)/A: tube ({La[:, 0].mean() / A:.3f}, {La[:, 1].mean() / A:.3f}), wide ({Lb[:, 0].mean() / A:.3f}, {Lb[:, 1].mean() / A:.3f})']
open(os.path.join(HERE, 'out', f'joint2_{a.split("+")[0]}_{b.split("+")[0]}.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
