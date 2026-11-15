#!/usr/bin/env python3
"""geomcheck.py: own checks of the README's section-1 geometric statements. python3 geomcheck.py"""
import itertools, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo
print('hull faces: area, rim cells (on >= 2 faces), apex (on 4 faces); and rim removal')
for R in (7, 9, 11, 13, 15, 23, 37):
    S = geo.vessel(R, 'c'); f = S.faces[0]
    cnt = {i: sum(i in set(F) for F in S.faces) for i in f}
    rim = sum(1 for i in f if cnt[i] >= 2); apex = sum(1 for i in f if cnt[i] == 4)
    inner = sorted(tuple(np.array(S.cells[i])) for i in f if cnt[i] == 1)
    Sv = geo.vessel(R - 3, 'v') if R - 3 > 0 else None
    same = None
    if Sv:
        fv = sorted(tuple(np.array(Sv.cells[i])) for i in Sv.faces[0])
        # compare as sets up to a translation along (1,1,1) direction family: try all translations t with t in 2Z^3 or not
        a = np.array(inner); b = np.array(fv)
        t = a.min(0) - b.min(0)
        same = len(a) == len(b) and set(map(tuple, b + t)) == set(map(tuple, a)), tuple(t)
    print(f'  c R={R}: A={len(f)} (3(R+1)(R+3)/8={3*(R+1)*(R+3)//8}) rim={rim} (3(R-1)+3={3*(R-1)+3}) apex={apex}; '
          f'interior = v-face R-3 up to translation: {same}')
for R in (8, 12, 24):
    S = geo.vessel(R, 'v'); f = S.faces[0]
    cnt = {i: sum(i in set(F) for F in S.faces) for i in f}
    print(f'  v R={R}: A={len(f)} (3R(R+2)/8={3*R*(R+2)//8}) rim={sum(1 for i in f if cnt[i] >= 2)} (3R/2={3*R//2}) apex={sum(1 for i in f if cnt[i] == 4)}')
print('cells adjacent to their own image (a quotient self-loop) and fixed cells, R = 11 c and 12 v:')
for sysn in ('v11c', 'v12v'):
    for g in ('csz', 'ci', 'c2e', 'c2v', 'd2h'):
        S, nb, orb, gens = geo.build(sysn, g)
        N = len(S.cells)
        # all group elements: closure
        els = [np.arange(N)]; seen = {els[0].tobytes()}
        k = 0
        while k < len(els):
            for h in gens:
                e = h[els[k]]
                if e.tobytes() not in seen: seen.add(e.tobytes()); els.append(e)
            k += 1
        nontriv = els[1:]
        fixed = set(i for e in nontriv for i in range(N) if e[i] == i)
        loops = set(i for e in nontriv for i in range(N) if e[i] in set(nb[i].tolist()))
        far = [i for i in loops if not fixed or min(abs(np.array(S.cells[i]) - np.array(S.cells[j])).sum() for j in fixed) > 4]
        print(f'  {sysn} {g}: |G|={len(els)} fixed cells {len(fixed)}, cells adjacent to an image {len(loops)}, of which more than 4 (L1, doubled) from any fixed cell {len(far)}; example {S.cells[sorted(loops)[0]] if loops else None}')
