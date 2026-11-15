"""Lead's recomputation of the headline numbers of research/dying from its committed table, 2026-11-15.

Reads only research/dying/data/occupancy_by_cell.csv (mean occupancy of each of the 63 cells of the canonical
face, stationary ("null") and at lags before the face's death). Own code; nothing imported from research/dying.
Run: python3 research/audit/dying_lead_check.py
"""
import csv
from collections import defaultdict

rows = list(csv.DictReader(open('research/dying/data/occupancy_by_cell.csv')))
G = defaultdict(list)
for r in rows:
    G[r['group']].append(r)
lnT = {'c1': 13.634, 'csz': 11.456, 'c2v': 9.291, 'd2h': 7.168}      # the symmetric study's values, A = 63
tied = {'c1': '', 'csz': 'z', 'c2v': 'xy', 'd2h': 'xyz'}               # edges shared with a face in lockstep
print('group  cells  P_null   row-1 occupancy by edge (x, y, z; * = tied)   band/interior at lag 4, by edge')
P = {}
for g in ('c1', 'csz', 'c2v', 'd2h'):
    c = G[g]
    P[g] = sum(float(r['null']) for r in c)
    out = []
    ratio = []
    inter = [r for r in c if min(int(r['x']), int(r['y']), int(r['z'])) >= 2]
    for a in 'xyz':
        others = [b for b in 'xyz' if b != a]
        row1 = [r for r in c if int(r[a]) == 0 and all(int(r[b]) >= 2 for b in others)]
        band = [r for r in c if int(r[a]) <= 1 and all(int(r[b]) >= 2 for b in others)]
        out.append('%.3f%s (%d)' % (sum(float(r['null']) for r in row1) / len(row1), '*' if a in tied[g] else ' ', len(row1)))
        ratio.append('%.3f%s' % ((sum(float(r['lag4']) for r in band) / len(band)) / (sum(float(r['lag4']) for r in inter) / len(inter)), '*' if a in tied[g] else ' '))
    print(f'{g:5} {len(c):5d}  {P[g]:6.2f}   {"  ".join(out)}   {"  ".join(ratio)}   (band {len(band)} cells, interior {len(inter)})')
gs = ['c1', 'csz', 'c2v', 'd2h']
print('steps in stationary population per tied edge:', ' '.join('%.2f' % (P[gs[i + 1]] - P[gs[i]]) for i in range(3)))
print('steps in ln tau per tied edge:               ', ' '.join('%.3f' % (lnT[gs[i + 1]] - lnT[gs[i]]) for i in range(3)))
print('ln tau lost per stationary live cell lost:   ', ' '.join('%.3f' % ((lnT[gs[i + 1]] - lnT[gs[i]]) / (P[gs[i + 1]] - P[gs[i]])) for i in range(3)),
      '; whole ladder %.3f' % ((lnT['d2h'] - lnT['c1']) / (P['d2h'] - P['c1'])))
print('for comparison, ln tau per stationary live cell of the untied face: %.3f (ln tau / P_null); per site %.4f' % (lnT['c1'] / P['c1'], lnT['c1'] / 63))
# where the stationary cells are lost: tied rows against the same rows of c1
c1 = {(r['x'], r['y'], r['z']): float(r['null']) for r in G['c1']}
for g in ('csz', 'c2v', 'd2h'):
    d = defaultdict(float)
    for r in G[g]:
        rowdist = min(int(r[a]) for a in tied[g])            # rows from the nearest tied edge (0 = rim row)
        d[rowdist] += float(r['null']) - c1[(r['x'], r['y'], r['z'])]
    print(f'{g}: stationary cells lost against c1, by row from the nearest tied edge:', ' '.join('%d: %+.2f' % (k, d[k]) for k in sorted(d)))
