#!/usr/bin/env python3
"""Is the face population a sufficient variable? d(p) of three Markov closures against the natural deaths.

    python3 closure.py NAME        (NAME run with the M3/M4 counts)  -> out/closure_NAME.txt
    python3 closure.py NAME against OTHER    the chains of NAME tested on the natural deaths of the independent run OTHER

chain 1: states P.   chain 2: states (P(t-1), P(t)).   chain PU: states (P, U), U = population of the layer beneath.
Each chain is built from the run's own transition counts; d(p) = chance that from a generation with population p the
face is empty before its population is >= L = ceil(A/2) again. All three reproduce the total rate by flux balance;
what is tested is where they put the launches and by how much they misjudge the bust from an over-full face.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
HL = 32

TEST = None
def main(nm):
    p = os.path.join(SCR, nm)
    M = np.fromfile(p + '.M'); A = int(round(len(M) ** .5)) - 1; NA = A + 1; M = M.reshape(NA, NA); L = (A + 1) // 2
    M3 = np.fromfile(p + '.M3').reshape(NA, NA, NA)
    M4 = np.fromfile(p + '.M4', np.uint32).reshape(NA, NA, NA, NA).astype(float)
    N = M.sum(1); nu = N / N.sum(); ps = np.arange(NA)
    H = np.array([[int(x) for x in l.split()[2:2 + HL]] for l in open(p + '.deaths')])
    nl = np.zeros(NA)
    for r in H:
        j = np.nonzero(r >= L)[0]
        if len(j): nl[r[j[0]]] += 1
    d_dir = nl / np.maximum(N, 1)
    if TEST:      # cross-validation: the natural deaths of an independent run of the same vessel (out/TEST.json from analyse.py)
        import json; r = json.load(open(os.path.join(HERE, 'out', TEST + '.json'))); nl = np.array(r['nl']); d_dir = nl / np.maximum(np.array(r['N']), 1)
    low = np.arange(1, L); nlw = len(low)
    # chain 1
    T = M / np.maximum(N, 1)[:, None]
    h1 = np.linalg.solve(np.eye(nlw) - T[np.ix_(low, low)], T[low, 0])
    d1 = T[:, 0] + T[:, low] @ h1
    # chain 2: state (prev, q), q < L
    N3 = M3.sum(2); T3 = M3 / np.maximum(N3, 1)[:, :, None]
    S = NA * nlw; B = np.zeros((S, S)); b = np.zeros(S)
    for prev in range(NA):
        for qi, q in enumerate(low):
            s = prev * nlw + qi
            if N3[prev, q] == 0: continue
            b[s] = T3[prev, q, 0]
            B[s, q * nlw:(q + 1) * nlw] = T3[prev, q, low]
    h2 = np.linalg.solve(np.eye(S) - B, b).reshape(NA, nlw)       # h2[prev, q]
    d2 = np.array([(M3[:, pp, 0].sum() + (M3[:, pp, :][:, low].sum(0) * h2[pp]).sum()) / max(N[pp], 1) for pp in range(NA)])
    # chain PU: state (q, u), q < L
    N4 = M4.sum((2, 3))
    S = nlw * NA; B = np.zeros((S, S)); b = np.zeros(S)
    for qi, q in enumerate(low):
        for u in range(NA):
            if N4[q, u] == 0: continue
            s = qi * NA + u
            b[s] = M4[q, u, 0].sum() / N4[q, u]
            B[s] = (M4[q, u][low] / N4[q, u]).reshape(-1)
    h4 = np.linalg.solve(np.eye(S) - B, b).reshape(nlw, NA)       # h4[q, u]
    d4 = np.array([(M4[pp, :, 0].sum() + (M4[pp][:, low, :].sum(0) * h4).sum()) / max(N[pp], 1) for pp in range(NA)])
    out = []; w = out.append
    w(f'{nm}: A {A} L {L}; {int(nl.sum())} natural deaths with a launch; total rate {nl.sum() / N.sum():.4g}')
    for lab, d in (('natural deaths', d_dir), ('chain 1 (P)', d1), ('chain 2 (P(t-1), P(t))', d2), ('chain PU (P, layer beneath)', d4)):
        r = nu * d; tot = r[L:].sum(); m = (r[L:] * ps[L:]).sum() / tot
        w(f'  {lab:28s} sum nu d = {tot:.4g}; mean launch theta {m / A:.4f}; share launched from >= 0.70 A: {r[int(np.ceil(.7 * A)):].sum() / tot:.3f}')
    w('    p  theta  launches   d natural   chain 1 / natural   chain 2 / natural   chain PU / natural')
    for pp in range(L, NA):
        if nl[pp] >= 20: w(f'  {pp:3d}  {pp / A:.3f}  {int(nl[pp]):6d}   {d_dir[pp]:.3e}     {d1[pp] / d_dir[pp]:6.3f}              {d2[pp] / d_dir[pp]:6.3f}              {d4[pp] / d_dir[pp]:6.3f}')
    hi = ps >= 0.70 * A
    for lab, d in (('chain 1', d1), ('chain 2', d2), ('chain PU', d4)):
        w(f'  {lab}: rate launched from >= 0.70 A, model / natural = {(nu * d)[hi].sum() / (nu * d_dir)[hi].sum():.3f}')
    open(os.path.join(HERE, 'out', 'closure_' + nm + ('_against_' + TEST if TEST else '') + '.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))

if __name__ == '__main__':
    if len(sys.argv) > 3 and sys.argv[2] == 'against': TEST = sys.argv[3]; main(sys.argv[1])
    else:
        for nm in sys.argv[1:]: main(nm)
