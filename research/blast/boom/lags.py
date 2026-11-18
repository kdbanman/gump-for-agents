#!/usr/bin/env python3
"""Generations from the launch to the empty face, and the lowest point before the end: shape against shape.
    python3 lags.py NAME ...  -> out/lags.txt   (natural deaths; launch = last generation with P >= ceil(A/2))"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
out = ['run      A  deaths  mean lag  share of deaths with lag >=: 4      6      8     10     12     16     20   | mean P one, two, three generations after the launch (per cell) | share with a rise after the first fall']
for nm in sys.argv[1:]:
    rows = [[int(x) for x in l.split()[2:34]] for l in open(os.path.join(SCR, nm + '.deaths'))]
    A = int(open(os.path.join(SCR, nm + '.sum')).read().split()[5]); L = (A + 1) // 2
    lag = []; after = []; rise = 0
    for r in rows:
        P = np.array(r); j = np.nonzero(P >= L)[0]
        if len(j) == 0: continue
        k = j[0]; lag.append(k + 1); seq = P[:k][::-1]           # populations after the launch, forwards in time
        after.append([seq[i] if i < len(seq) else 0 for i in range(3)])
        if len(seq) > 1 and (np.diff(seq) > 0).any(): rise += 1
    lag = np.array(lag); after = np.array(after, float)
    out.append(f'{nm:8s} {A:3d} {len(lag):6d}  {lag.mean():6.2f}   ' + '                              ' + ' '.join(f'{(lag >= x).mean():6.3f}' for x in (4, 6, 8, 10, 12, 16, 20))
               + '   |  ' + ' '.join(f'{x / A:.3f}' for x in after.mean(0)) + f'   |  {rise / len(lag):.3f}  (+- {(.25 / len(lag)) ** .5:.3f})')
open(os.path.join(HERE, 'out', 'lags.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
