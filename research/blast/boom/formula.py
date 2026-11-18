#!/usr/bin/env python3
"""A formula for the price per cell from local measured quantities (step 5, the closed form).

    c = min_theta [ I_up(theta) + lam f(theta) - lam^2 s2(theta) / 2 ],     lam = 2 (g - 1) / kappa

I_up(theta): cost per cell of a face generation over-filled to theta (slope in A of ln(sqrt(A) nu(theta A))).
f, s2: mean and variance per cell of the next generation's population given theta now (the bust).
lam: price per surviving cell of starving, the extinction exponent of a branching process whose mean and variance
per parent cell are g and kappa: read from the bottom branch of the same return map, E[P'|q] = g q + a,
Var[P'|q] = kappa q + b at small q.   python3 formula.py  -> out/formula.txt
"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
R = {n: json.load(open(os.path.join(OUT, n + '.json'))) for n in ('t48', 't63', 't75', 't84') if os.path.exists(os.path.join(OUT, n + '.json'))}

def li(arr, x, log=False):
    i = int(np.floor(x)); t = x - i; a, b = arr[i], arr[i + 1]
    return (1 - t) * np.log(a) + t * np.log(b) if log else (1 - t) * a + t * b

L = []; w = L.append
th = np.arange(0.60, 0.861, 0.01)
def Iup(a, b):
    ra, rb = R[a], R[b]
    return np.array([-(li(rb['nu'], t * rb['A'], True) + .5 * np.log(rb['A']) - li(ra['nu'], t * ra['A'], True) - .5 * np.log(ra['A'])) / (rb['A'] - ra['A']) for t in th])
pairs = [p for p in (('t63', 't84'), ('t48', 't63'), ('t63', 't75'), ('t75', 't84')) if p[0] in R and p[1] in R]
I = {p: Iup(*p) for p in pairs}
big = 't84' if 't84' in R else 't63'
f = np.array([li(R[big]['f'], t * R[big]['A']) / R[big]['A'] for t in th]); s2 = np.array([li(R[big]['v'], t * R[big]['A']) / R[big]['A'] for t in th])
w('theta   ' + '  '.join(f'I_up {a}->{b}' for a, b in pairs) + f'    f(theta)  s2(theta)  [{big}]')
for i, t in enumerate(th):
    if i % 2 == 0: w(f'{t:.2f}    ' + '       '.join(f'{I[p][i]:.4f}' for p in pairs) + f'        {f[i]:.4f}   {s2[i]:.4f}')
# bottom branch: natural rows and rows of clones 1..5 generations after an over-full parent
lams = {}
for n in ('t48', 't63'):
    if n not in R: continue
    A = R[n]['A']; M = np.fromfile(os.path.join(SCR, n + '.M')).reshape(A + 1, A + 1); ps = np.arange(A + 1)
    Mc = np.fromfile(os.path.join(SCR, n + '.clone.Mc')).reshape(12, A + 1, A + 1)[1:6].sum(0)
    for lab, K in (('natural', M), ('after a launch', Mc)):
        q = np.array([x for x in range(4, 13) if x != 6]); Nq = K[q].sum(1)
        fq = (K[q] * ps).sum(1) / Nq; vq = (K[q] * ps ** 2).sum(1) / Nq - fq ** 2
        g, a = np.polyfit(q, fq, 1); kap, b = np.polyfit(q, vq, 1)
        # the chain's own ratio h(q+1)/h(q): P(empty before >= L)
        Lv = (A + 1) // 2; low = np.arange(1, Lv); T = K / np.maximum(K.sum(1), 1)[:, None]
        h = np.linalg.solve(np.eye(len(low)) - T[np.ix_(low, low)], T[low, 0])
        rat = np.exp(np.polyfit(np.arange(5, 13), np.log(h[4:12]), 1)[0])
        lams[(n, lab)] = (2 * (g - 1) / kap, -np.log(rat))
        w(f'{n}, bottom branch ({lab}), q = 4..12 without 6: E[P\'|q] = {g:.3f} q + {a:.2f}; Var = {kap:.3f} q + {b:.2f}; lam = 2(g-1)/kappa = {2 * (g - 1) / kap:.3f}; '
          f'the chain\'s own h(q+1)/h(q) = {rat:.3f} (lam = {-np.log(rat):.3f})')
def price(lam, Iv):
    J = np.where(f - lam * s2 > 0, lam * f - lam ** 2 * s2 / 2, f ** 2 / (2 * s2))
    k = int(np.argmin(Iv + J)); return (Iv + J)[k], th[k], Iv[k], J[k]
for p in pairs[:2]:
    w(f'with I_up from {p[0]} -> {p[1]}:')
    for lab, lam in [(f'{k[0]} {k[1]} (map)', v[0]) for k, v in lams.items()] + [(f'{k[0]} {k[1]} (chain ratio)', v[1]) for k, v in lams.items()]:
        c, t, a, b = price(lam, I[p]); w(f'   lam = {lam:.3f} [{lab}]: c = {c:.4f} at theta = {t:.2f} (I_up {a:.4f} + J {b:.4f})')
    ls = np.arange(0.30, 0.60, 0.001); cs = np.array([price(l, I[p])[0] for l in ls]); l0 = ls[np.argmin(abs(cs - 0.2087))]
    c, t, a, b = price(l0, I[p]); w(f'   lam fitted to c = 0.2087: {l0:.3f} (theta {t:.2f}, I_up {a:.4f}, J {b:.4f})')
open(os.path.join(OUT, 'formula.txt'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
