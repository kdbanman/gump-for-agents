#!/usr/bin/env python3
"""Tables from data/runs.csv (research/blast/rim).   python3 research/blast/rim/table.py
Pools runs of the same vessel and face class (sum of exposure and first deaths), prints every class, then the
symmetric prisms (w,w,L,0) as a width x length table with the prices per cell of added length and added width."""
import csv, math, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'data', 'runs.csv'))))
P = collections.OrderedDict()
for r in rows:
    k = (r['vessel'], r['faces'], int(r['cells']), r['rows'])
    e, d = P.get(k, (0.0, 0))
    P[k] = (e + float(r['exposure']), d + int(r['first_deaths']))
T = {}
print('vessel            faces     cells rows                        ln tau_face      first deaths')
for (v, f, c, rw), (e, d) in P.items():
    m = len(f.split('+')); lt = math.log(m * e / d) if d else float('nan'); er = 1 / math.sqrt(d) if d else float('nan')
    T[(v, f)] = (lt, er, c)
    print(f'{v:17s} {f:9s} {c:5d} {rw:27s} {lt:8.4f} +- {er:.4f} {d:10d}')
S = {}
for (v, f), (lt, er, c) in T.items():
    p = v.split('_')
    if p[0] == 'prism' and p[1] == p[2] and p[4] == '0' and int(p[1]) % 2 == 0: S[(int(p[1]), int(p[3]))] = (lt, er, c)
ws = sorted({w for w, L in S}); Ls = sorted({L for w, L in S})
print('\nsymmetric prisms (w,w,L,0): ln tau_face (rows: w; columns: L)')
print('  w\\L ' + ''.join(f'{L:>18d}' for L in Ls))
for w in ws:
    print(f'  {w:3d} ' + ''.join((f'{S[(w, L)][0]:11.4f}+-{S[(w, L)][1]:.4f}' if (w, L) in S else ' ' * 18) for L in Ls))
print('\nprice per cell of added LENGTH at fixed width (ln tau(w,L+1) - ln tau(w,L)) / (1.5 w)')
for w in ws:
    for L in Ls:
        if (w, L) in S and (w, L + 1) in S:
            a, b = S[(w, L)], S[(w, L + 1)]
            print(f'  w = {w:2d}, L {L} -> {L + 1}: {(b[0] - a[0]) / (1.5 * w):.4f} +- {math.hypot(a[1], b[1]) / (1.5 * w):.4f}   (slope per unit length {b[0] - a[0]:.3f})')
print('\nprice per cell of added WIDTH at fixed length (ln tau(w+2,L) - ln tau(w,L)) / (3 L)')
for L in Ls:
    for w in ws:
        if (w, L) in S and (w + 2, L) in S:
            a, b = S[(w, L)], S[(w + 2, L)]
            print(f'  L = {L}, w {w:2d} -> {w + 2:2d}: {(b[0] - a[0]) / (3 * L):.4f} +- {math.hypot(a[1], b[1]) / (3 * L):.4f}')
print('\nmixed second difference per cell: [t(w+2,L+1) - t(w+2,L) - t(w,L+1) + t(w,L)] / 3')
for L in Ls:
    for w in ws:
        ks = [(w, L), (w, L + 1), (w + 2, L), (w + 2, L + 1)]
        if all(k in S for k in ks):
            v = S[ks[3]][0] - S[ks[2]][0] - S[ks[1]][0] + S[ks[0]][0]; e = math.sqrt(sum(S[k][1] ** 2 for k in ks))
            print(f'  w {w}->{w + 2}, L {L}->{L + 1}: {v / 3:.4f} +- {e / 3:.4f}')
