"""Item 1: neighbours inside the vessel of the cells of an edge row, cross2, by enumeration on toy2d's cell graph.
Usage: python3 counts.py   (cap: a cell with n >= 5 dies)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'toy2d'))
import geom
for ves, dims, L in (('strip', (16, 20), 20), ('box', (20,), 20)):
    g = geom.build('cross2', ves, dims); idx = g['idx']
    deg = [int((g['nb'][idx[0, x]] >= 0).sum()) for x in range(L)]
    inrow = [sum(1 for j in g['nb'][idx[0, x]] if j >= 0 and j < L) for x in range(L)]
    print(ves, dims, 'edge row: neighbours inside the vessel by position', deg[:4], '...', deg[-3:], ' of which in the row', inrow[:4], '...')
    print('   can be overcrowded (>= 5 neighbours exist):', [int(d >= 5) for d in deg[:4]], '; needs ALL its neighbours alive:', [int(d == 5) for d in deg[:4]])
