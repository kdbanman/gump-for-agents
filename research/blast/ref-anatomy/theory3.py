#!/usr/bin/env python3
"""Two checks for THEORY.md.  (1) The populations of the first four layers (P, B, C, D4) round a fatal fall of half
the face, from the death windows of run.sh (t63): is the boom a two-layer event or deeper?  (2) The Gaussian action
of the *measured* mean route on the 63-cell torus map, against the minimum.   python3 theory3.py -> out/theory3.txt"""
import os
os.environ['THEORY_OUT'] = 'theory3.txt'
import numpy as np, vessel, theory as th
for name in ('t63', 'tube60', 'h63'):
    v = vessel.get(name); N = v['N']; nby = (N + 7) // 8; rec = 64 + 16 * nby
    raw = np.fromfile(os.path.join(vessel.SCR, name + '.win'), np.uint8)
    raw = raw[:len(raw) // rec * rec].reshape(-1, rec)
    age = raw[:, 4:8].copy().view(np.uint32)[:, 0]
    A = len(v['faces'][0]); HALF = (A + 1) // 2
    if v['kind'] == 'slab':
        lay = v['lay']; L = [[np.where(lay == s)[0] for s in (1, 3, 5, 7, 9)], [np.where(lay == s)[0] for s in (15, 13, 11, 9, 7)]]
    else:
        import itertools
        cells = np.array(v['cells']); L = []
        for d in itertools.product((1, -1), repeat=3):
            s = cells @ np.array(d); L.append([np.where(s == v['R'] - 2 * k)[0] for k in range(5)])
    for ch, lab in ((ord('D'), 'fatal falls of half the face'), (ord('C'), 'non-fatal falls of half the face'), (ord('O'), 'over-full living generations'), (ord('L'), 'living faces, any generation')):
        idx = np.where((raw[:, 0] == ch) & (age >= 1064))[0][:4000]
        rows = []
        for i in idx:
            PH = raw[i, 16:64].astype(int); f = raw[i, 1]
            st = np.unpackbits(raw[i, 64:].reshape(16, nby), axis=1, bitorder='little')[:, :N]
            if ch == ord('D'):
                d = PH[35:47] - PH[36:48]
                if d.max() < HALF: continue
                k = 36 + int(np.argmax(d)) - 32            # state index of the generation after the fall
            elif ch == ord('L'):
                k = 9
            else:
                k = 8
            if k < 2: continue
            rows.append([[st[k + o][c].sum() for c in L[f]] for o in (-2, -1, 0)])
        r = np.array(rows, float).mean(0)
        th.pr(f'{name}: {lab} ({len(rows)}): layers 1-5 two generations before / at the over-full generation / one after: '
              + ' | '.join(' '.join(f'{x:.1f}' for x in row) for row in r) + f'   (cells per layer: {[len(c) for c in L[0]]})')
D = th.load('t63')
M, C, ok = th.per_cell(D, 63, 200)
def cost(a, b):
    mu = M[a]; c = C[a]; det = c[0] * c[1] - c[2] ** 2
    d = np.array(b, float) - mu
    return 0.5 * (c[1] * d[0] ** 2 - 2 * c[2] * d[0] * d[1] + c[0] * d[1] ** 2) / det
for lab, path in (('measured mean route (anatomy / REVIEW: 33,25 -> 49,40 -> 11,10 -> 6,10 -> 3,12 -> 2,15 -> 1,19)', [(33, 25), (49, 40), (11, 10), (6, 10), (3, 12), (2, 15), (1, 19)]),
                  ('Gaussian optimum', [(33, 28), (35, 30), (33, 25), (46, 42), (16, 7), (11, 6), (6, 6), (4, 6), (3, 7), (2, 9), (1, 11)])):
    cs = [cost(path[i], path[i + 1]) for i in range(len(path) - 1)]
    last = 0.5 * max(M[path[-1]][0] - 0.5, 0) ** 2 / C[path[-1]][0]
    th.pr(f't63 map, {lab}: step costs ' + ' '.join(f'{x:.2f}' for x in cs) + f' + {last:.2f} = {sum(cs) + last:.2f}; populated: {[bool(ok[p]) for p in path]}')
    th.pr('   mean next at each state: ' + ' '.join(f'({M[p][0]:.1f},{M[p][1]:.1f})' for p in path))
th.out.close()
