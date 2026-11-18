#!/usr/bin/env python3
"""island tables.   python3 ani.py i48 i63     (files written by `rbi island ...` in research/scratch/blast/ref-boom/)"""
import sys, os
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
CL = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 12), (13, 999)]
for name in sys.argv[1:]:
    n = np.zeros((3, 200)); f = np.zeros((3, 200)); u = np.zeros((3, 200)); ic = {}
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A': A = int(w[1])
        if w[0] == 'IC': ic[int(w[1])] = (int(w[3]), int(w[4]))
        if w[0] == 'I': b, z = int(w[1]), int(w[2]); n[b, z] = int(w[3]); f[b, z] = int(w[4]); u[b, z] = int(w[5])
    print(f"== {name}: A = {A}; parents (generation after a face of q cells) and the untouched state's own deaths, by q/A in "
          f"[0.62,0.70), [0.70,0.78), >=0.78: " + '; '.join(f'{ic[b][0]} / {ic[b][1]}' for b in range(3)) + f"; undecided after 400 generations: {int(u.sum())}")
    print('   cluster size alone:      ' + ' '.join(f'{a}' if a == b else (f'{a}-{b}' if b < 999 else f'>{a - 1}') for a, b in CL).replace(' ', '          '))
    for b in list(range(3)) + ['all']:
        nn = n.sum(0) if b == 'all' else n[b]; ff = f.sum(0) if b == 'all' else f[b]
        row = []
        for a, c in CL:
            N = nn[a:c + 1].sum(); F = ff[a:c + 1].sum()
            row.append(f'{F / N:.4f}+-{np.sqrt(max(F, 1) * (1 - F / N)) / N:.4f}' if N else '   -   ')
        print(f'   fails, q-bin {b}:  ' + '  '.join(row))
    nn = n.sum(0); ff = f.sum(0)
    print(f"   clusters of 7 or more: {int(ff[7:].sum())} fail of {int(nn[7:].sum())} = {ff[7:].sum() / nn[7:].sum():.5f} (regrow {1 - ff[7:].sum() / nn[7:].sum():.4f}); "
          f"of 7-12: {ff[7:13].sum() / nn[7:13].sum():.4f}; largest cluster that failed: {int(np.nonzero(ff)[0].max())}")
