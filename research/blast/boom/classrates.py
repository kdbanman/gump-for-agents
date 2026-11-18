#!/usr/bin/env python3
"""Absolute rates of deaths by class, wide faces against loop-12 tubes, as functions of area (the PI's test, 04:15 UTC).

    python3 classrates.py   -> out/classrates.txt

Classes of a death (natural deaths, 32-generation histories):
  bust     the largest one-generation fall of the face population in the 32 generations before the end is >= A/2
  no-bust  the rest;        also: by launch (last generation with P >= A/2): launch theta < 0.70, 0.70-0.78, >= 0.78.
Rates per face-generation. Wide faces: ln rate = a + b A fitted by weighted least squares; a tube is compared with
that line at its own area (difference of logarithms, + = the tube dies more often in that class).
"""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
WIDE = [('t57',), ('t63', 't63b'), ('w72',), ('t75',), ('t84',)]; TUBE = [('tube54',), ('tube60', 'tube60b'), ('tube72',), ('tube84',)]
CL = ['all', 'bust', 'no-bust', 'launch < 0.70', 'launch 0.70-0.78', 'launch >= 0.78']
def load(names):
    ex = 0; H = []
    for nm in names:
        p = os.path.join(SCR, nm)
        if not os.path.exists(p + '.sum'): continue
        s = open(p + '.sum').read().split(); A = int(s[5]); ex += float(s[s.index('expoF') + 1])
        H += [[int(x) for x in l.split()[2:34]] for l in open(p + '.deaths')]
    if not H: return None
    H = np.array(H); L = (A + 1) // 2; c = np.zeros(6)
    for r in H:
        seq = r[::-1]; fall = (seq[:-1] - seq[1:]).max(); fall = max(fall, seq[-1])       # the last step to 0 counts too
        j = np.nonzero(r >= L)[0]; th = r[j[0]] / A if len(j) else 0
        c[0] += 1; c[1 if fall >= A / 2 else 2] += 1; c[3 if th < 0.70 else 4 if th < 0.78 else 5] += 1
    return A, ex, c
out = []; w = out.append
w('run(s)             A   face-gen.   deaths | ln rate: ' + '  '.join(f'{c:>18s}' for c in CL) + ' | bust share')
W = [load(x) for x in WIDE]; T = [load(x) for x in TUBE]
for names, d in list(zip(WIDE, W)) + list(zip(TUBE, T)):
    if d is None: continue
    A, ex, c = d
    w(f'{"+".join(names):16s} {A:3d}  {ex:.3e}  {int(c[0]):6d} |          ' + '  '.join(f'{np.log(c[k] / ex):8.3f} +- {c[k] ** -.5:.3f}' if c[k] > 0 else '        -         ' for k in range(6)) + f' |  {c[1] / c[0]:.3f} +- {(c[1] * c[2] / c[0] ** 3) ** .5:.3f}')
Wd = [d for d in W if d is not None]
w('\nwide faces, ln rate = a + b (A - 66):   class: a, -b (+-)')
fit = {}
for k in range(6):
    A = np.array([d[0] for d in Wd if d[2][k] > 0], float); y = np.array([np.log(d[2][k] / d[1]) for d in Wd if d[2][k] > 0]); e = np.array([d[2][k] ** -.5 for d in Wd if d[2][k] > 0])
    cf, cov = np.polyfit(A - 66, y, 1, w=1 / e, cov='unscaled'); fit[k] = (cf, cov)
    chi = (((y - np.polyval(cf, A - 66)) / e) ** 2).sum()
    w(f'  {CL[k]:18s} a = {cf[1]:.3f} +- {cov[1, 1] ** .5:.3f}   price per cell {-cf[0]:.4f} +- {cov[0, 0] ** .5:.4f}   chi2 {chi:.1f} on {len(A) - 2}')
# second baseline: slope fixed at the anchors' wide-face price 0.20866 for every class, intercept from the faces with no loop^2 < 21
SL = 0.20866; Wd2 = [d for nms, d in zip(WIDE, W) if d is not None and nms[0] != 't57']
w(f'\nbaseline 2: every class with the anchors\' slope {SL}, intercept from t63(+b), w72, t75, t84 (t57 has loops^2 19 and is left out); tube (and t57) minus that line:')
w('run       A   ' + '  '.join(f'{c:>18s}' for c in CL[:3]) + '     chi2 of the wide runs about the line (3 d.o.f.): all, bust, no-bust')
ic = {}; chis = []
for k in range(3):
    y = np.array([np.log(d[2][k] / d[1]) + SL * (d[0] - 66) for d in Wd2]); e = np.array([d[2][k] ** -.5 for d in Wd2])
    a = (y / e ** 2).sum() / (1 / e ** 2).sum(); ic[k] = (a, (1 / e ** 2).sum() ** -.5); chis.append((((y - a) / e) ** 2).sum())
for names, d in [(WIDE[0], W[0])] + list(zip(TUBE, T)):
    if d is None: continue
    A, ex, c = d
    w(f'{names[0]:8s} {A:3d}  ' + ''.join(f'  {np.log(c[k] / ex) - (ic[k][0] - SL * (A - 66)):+8.3f} +- {(1 / c[k] + ic[k][1] ** 2) ** .5:.3f}' for k in range(3)) + ('      ' + ' '.join(f'{x:.1f}' for x in chis) if names[0] == 't57' else ''))
w('\ntube minus the wide line at the same area (ln rate; + = more deaths of that class on the tube):')
w('tube      A   ' + '  '.join(f'{c:>18s}' for c in CL))
for names, d in zip(TUBE, T):
    if d is None: continue
    A, ex, c = d; s = f'{names[0]:8s} {A:3d}  '
    for k in range(6):
        cf, cov = fit[k]; x = A - 66; pred = np.polyval(cf, x); ep = (cov[0, 0] * x * x + 2 * cov[0, 1] * x + cov[1, 1]) ** .5
        s += f'  {np.log(c[k] / ex) - pred:+8.3f} +- {(1 / c[k] + ep ** 2) ** .5:.3f}' if c[k] > 0 else '          -        '
    w(s)
open(os.path.join(HERE, 'out', 'classrates.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
