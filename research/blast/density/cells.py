#!/usr/bin/env python3
"""Group densities in gump from per-cell densities (CELL lines of a layer run, nzd with NZD_LAYERS=1), and the bias
strings of the skin-depth rows.

    python3 research/blast/density/cells.py FILE            (a layer run of gump, e.g. data/layers/lay3_gump_R11_s9911.txt)

Columns: the cell's density over all counted hull-generations and given the watched face's population <= 20, 15, 10,
6, 4, 2. A group's density is the mean over its cells (each cell is counted in the same hull-generations).
Groups by depth k under the watched face (dep0) and the cell's least depth under the other seven faces (dmo):
  full k    every cell of layer k
  DO>=j k   the cells of layer k at depth >= j under every other face (DO >= 1: what full replacement with DO = 1
            replaces at depth k; DO >= 3: the core, what DO = 3 replaces)
Bias strings: column A (depth >= d under the watched face, >= 3 under the others): each depth at the mean density of its
DO >= 3 cells; column B (depth >= d under every face): each depth at the mean density of its DO >= d cells.
"""
import sys
from collections import defaultdict

f = sys.argv[1]
cells = []
for l in open(f):
    if l.startswith('CELL '):
        t = l.split()
        cells.append(dict(i=int(t[1]), dep=int(t[5]), dmo=int(t[6]), v=[float(x) for x in t[8:]]))
    if l.startswith('CELLN'):
        cn = [float(x) for x in l.split()[2:9]]
R = max(c['dep'] for c in cells)
TH = ['all', '<=20', '<=15', '<=10', '<=6', '<=4', '<=2']
print(f'{f}: {len(cells)} cells, R = {R}; hull-generations counted ' + ', '.join(f'{t} {n:.3g}' for t, n in zip(TH, cn)))

def grp(sel):
    cs = [c for c in cells if sel(c)]
    if not cs: return None, 0
    return [sum(c['v'][t] for c in cs) / len(cs) for t in range(7)], len(cs)

print(f'\n{"group":22s} {"cells":>5s} ' + ' '.join(f'{t:>7s}' for t in TH) + '   min over face<=20..2 (at)')
rows = []
for k in range(1, R):
    for name, sel in ((f'full {k}', lambda c, k=k: c['dep'] == k), (f'DO>=1 {k}', lambda c, k=k: c['dep'] == k and c['dmo'] >= 1),
                      (f'DO>=2 {k}', lambda c, k=k: c['dep'] == k and c['dmo'] >= 2), (f'DO>=3 {k}', lambda c, k=k: c['dep'] == k and c['dmo'] >= 3),
                      (f'DO>=4 {k}', lambda c, k=k: c['dep'] == k and c['dmo'] >= 4)):
        v, n = grp(sel)
        if v is None or (name.startswith('DO>=') and k > 6): continue
        m = min(range(1, 7), key=lambda t: v[t])
        print(f'{name:22s} {n:5d} ' + ' '.join(f'{x:7.4f}' for x in v) + f'   {v[m]:.4f} ({TH[m]})')
for name, sel in (('all DO>=1 (k >= 1)', lambda c: c['dep'] >= 1 and c['dmo'] >= 1), ('all DO>=3 (k >= 1)', lambda c: c['dep'] >= 1 and c['dmo'] >= 3)):
    v, n = grp(sel); m = min(range(1, 7), key=lambda t: v[t])
    print(f'{name:22s} {n:5d} ' + ' '.join(f'{x:7.4f}' for x in v) + f'   {v[m]:.4f} ({TH[m]})')

print('\nBias strings (mean density over all counted hull-generations, by depth):')
def bias(j, d):
    out = []
    for k in range(d, R):
        v, n = grp(lambda c, k=k: c['dep'] == k and c['dmo'] >= j)
        if v is not None: out.append(f'{k}:{v[0]:.4f}')
    return ','.join(out)
for d in (1, 2, 3, 4):
    print(f'  A d={d}: DW {d} DO 3  {bias(3, d)}')
for d in (1, 2, 3, 4):
    print(f'  B d={d}: DW {d} DO {d}  {bias(d, d)}')
