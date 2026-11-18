#!/usr/bin/env python3
"""What an over-full generation does to a hull face and to a wrapped face, cell class by cell class.

From fd.c's 'O' records (the face layer held >= THR cells 16 generations before the end of the record; no face of
the replica died in between).  Classes of a face-layer cell by its neighbours inside the vessel: 9 (interior),
7 (rim row), 4 (corner); a wrapped face has only the first.  Printed per class: cells, occupancy in the over-full
generation, the share of its live cells that are alive one generation later, the share of its live cells with
>= 6 live neighbours, births per dead cell.

    python3 research/audit/blast/rimtest.py hull_11 hull63_s21 [MINPOP]      (and slab_1_4_21 slab63_s11)
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyse as an

vessel, prefix = sys.argv[1], sys.argv[2]
minpop = int(sys.argv[3]) if len(sys.argv) > 3 else 48
V = np.load(os.path.join(an.SCR, vessel + '.npz'))
cells, NBR, faces = V['cells'], V['nb'], V['faces']
n = len(cells); nf = faces.shape[0]
sizes = [int((faces[0, l] >= 0).sum()) for l in range(faces.shape[1])]
R, nbytes = an.load_rec([prefix], sizes)
O = R['O']
off = np.cumsum([0] + nbytes)
lists = [[faces[f, l][faces[f, l] >= 0] for l in range(an.NLB)] for f in range(nf)]
deg = (NBR < n).sum(1)
print(f'# {vessel} {prefix}: neighbours inside the vessel, face-layer cells of face 0: '
      + ', '.join(f'{d}: {int((deg[lists[0][0]] == d).sum())} cells' for d in sorted(set(deg[lists[0][0]]))))
nbidx = []
for f in range(nf):
    loc = -np.ones(n + 1, int); base = 0
    for l in range(an.NLB):
        loc[lists[f][l]] = base + np.arange(sizes[l]); base += sizes[l]
    t = loc[NBR[lists[f][0]]]
    nbidx.append(np.where(t >= 0, t, base))
j = an.RING - 1 - 16
acc = {}
use = 0
for i in range(len(O['pops'])):
    if O['pops'][i, j, 0] < minpop: continue
    use += 1
    f = int(O['face'][i]); b = O['bits'][i]
    cb = [np.unpackbits(b[:, off[l]:off[l + 1]], axis=1, bitorder='little')[:, :sizes[l]] for l in range(an.NLB)]
    allb = np.concatenate(cb + [np.zeros((an.RING, 1), np.uint8)], axis=1)
    now, nxt = cb[0][j].astype(int), cb[0][j + 1].astype(int)
    cnt = allb[j][nbidx[f]].sum(1)
    for d in set(deg[lists[f][0]]):
        m = deg[lists[f][0]] == d
        a = acc.setdefault(d, np.zeros(7))
        a += [m.sum(), now[m].sum(), (now[m] & nxt[m]).sum(), (now[m] & (cnt[m] >= 6)).sum(), ((1 - now[m]) & nxt[m]).sum(), (1 - now[m]).sum(), 1]
tot = O['pops'][O['pops'][:, j, 0] >= minpop]
print(f'{use} non-fatal generations with >= {minpop} cells; mean population then {tot[:, j, 0].mean():.2f}, one generation later {tot[:, j + 1, 0].mean():.2f}, two later {tot[:, j + 2, 0].mean():.2f}')
for d in sorted(acc, reverse=True):
    a = acc[d]
    print(f'  cells with {d} neighbours inside ({a[0] / a[6]:.0f} a face): occupancy {a[1] / a[0]:.3f}; live cells that survive {a[2] / a[1]:.3f}; '
          f'live cells with >= 6 live neighbours {a[3] / a[1]:.3f}; births per dead cell {a[4] / a[5]:.3f}')
