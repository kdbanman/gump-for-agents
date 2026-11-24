#!/usr/bin/env python3
"""Wrapped-face rows (slab.c): ln tau of the watched face, p* by interpolation, and the way of dying against gump's.

    python3 research/blast/density/slabrec.py [DIR]       (files slab_*.txt; default data/slab)

Per size (A = 63: torus (1,4),(0,21); A = 45: (1,4),(0,15)): gump's face from the gump row (both faces: 2 E / deaths;
at 63 cells also the project's anchor 13.1622 +- 0.0007, research/blast/split-slab/README.md), the coin rows (L = 1:
the face the only real layer, every other cell a fresh coin every generation), Delta against the gump row, p* by a
weighted line through the two rows that bracket the zero (and any with |Delta| < 0.1), and the excursion split as in
skin.py: dips = descents from >= H to < H per hull-generation (H = round(A/4)), deadliness = their share that die
before the face is back at H, P1 = the share of descents to <= 1 cell that die. In gump's row a life also ends when
the other face dies, which censors a few descents (C in the REC line); the coin rows have no other face.
"""
import glob, math, os, re, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'slab')
rows = defaultdict(list)
for f in sorted(glob.glob(os.path.join(d, 'slab_*.txt'))):
    t = open(f).read(); h = t.splitlines()[0]
    A = int(re.search(r' A (\d+)', h).group(1)); L = int(re.search(r' L (\d+)', h).group(1)); p = float(re.search(r' p ([0-9.]+)', h).group(1))
    E = float(re.search(r'exposure ([0-9.e+]+)', h).group(1)); n0 = int(re.search(r' watched (\d+)', h).group(1)); n7 = int(re.search(r' other (\d+)', h).group(1))
    rec = [l for l in t.splitlines() if l.startswith('REC')][0].split(); H = int(rec[2]); R = {}
    for tok in rec[4:]:
        k, v = tok.split(':'); R[int(k)] = tuple(int(x) for x in v.split('/'))
    l1 = [l for l in t.splitlines() if l.startswith('LAYER1')][0]
    rows[A].append(dict(f=os.path.basename(f), L=L, p=p, E=E, n0=n0, n7=n7, H=H, R=R, l1=l1))
for A in sorted(rows):
    gs = [r for r in rows[A] if r['L'] == 8]
    if not gs: continue
    g = dict(E=sum(r['E'] for r in gs), n0=sum(r['n0'] for r in gs), n7=sum(r['n7'] for r in gs), H=gs[0]['H'], l1=gs[0]['l1'], f=', '.join(r['f'] for r in gs),
             R={k: tuple(sum(r['R'][k][i] for r in gs) for i in range(3)) for k in gs[0]['R']})
    gv = math.log(2 * g['E'] / (g['n0'] + g['n7'])); ge = 1 / math.sqrt(g['n0'] + g['n7'])
    k = g['H'] - 1; gd = g['R'][k][0] / g['E']; gP = g['R'][k][1] / g['R'][k][0]; g1 = g['R'][1][1] / g['R'][1][0]
    print(f'{A} cells: gump {gv:.4f} +- {ge:.4f} (both faces; {g["f"]}; watched face alone {math.log(g["E"] / g["n0"]):.4f})' + ('; anchor 13.1622 +- 0.0007' if A == 63 else ''))
    print(f'   gump: dips {gd:.3e}, deadliness {gP:.4f}, P1 {g1:.4f}; {g["l1"]}')
    pts = []
    for r in sorted((r for r in rows[A] if r['L'] < 8), key=lambda r: ('skin' in r['f'], r['L'], r['p'])):
        v = math.log(r['E'] / r['n0']) - gv; e = math.hypot(1 / math.sqrt(r['n0']), ge)
        N = r['R'][k][0]; D = r['R'][k][1]; N1, D1 = r['R'][1][0], r['R'][1][1]
        print(f'   p {r["p"]:.4f}: Delta {v:+.4f} +- {e:.4f} ({r["n0"]} deaths)  d ln dips {math.log(N / r["E"]) - math.log(gd):+.3f}  '
              f'd ln deadliness {math.log(D / N) - math.log(gP):+.3f}  P1 {D1 / N1:.4f} +- {math.sqrt(D1 / N1 * (1 - D1 / N1) / N1):.4f}  ({r["f"]})')
        if 'skin' not in r['f']: pts.append((r['p'], v, 1 / math.sqrt(r['n0'])))
        else: print(f'      ^ skin row: real layers 0..{r["L"] - 1}, coins at gump\'s layer means from layer {r["L"]}')
    br = [i for i in range(len(pts) - 1) if pts[i][1] < 0 <= pts[i + 1][1]]
    if br:
        sel = [x for x in pts if abs(x[1]) < 0.1]
        for x in (pts[br[0]], pts[br[0] + 1]):
            if x not in sel: sel.append(x)
        S = sum(1 / e ** 2 for p, D, e in sel); Sx = sum(p / e ** 2 for p, D, e in sel); Sy = sum(D / e ** 2 for p, D, e in sel)
        Sxx = sum(p * p / e ** 2 for p, D, e in sel); Sxy = sum(p * D / e ** 2 for p, D, e in sel)
        det = S * Sxx - Sx * Sx; b = (S * Sxy - Sx * Sy) / det; a = (Sy - b * Sx) / S
        va, vb, cab = Sxx / det, S / det, -Sx / det; ps = -a / b; dpa, dpb = -1 / b, a / b ** 2
        eps = math.sqrt(dpa ** 2 * va + dpb ** 2 * vb + 2 * dpa * dpb * cab + (ge / b) ** 2)
        print(f'   p* = {ps:.4f} +- {eps:.4f} (line through {len(sel)} rows, slope {b:.1f} per unit p)')
