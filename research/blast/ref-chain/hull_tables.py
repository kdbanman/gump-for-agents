#!/usr/bin/env python3
"""ref-chain (fourth review): the hull faces' tables from my oracle-built geometry, in the format of the
`#eval dump R` that research/blast/lean/link_hull_cert.py reads (cell, Face.nb, m1, m2 per cell).
  python3 research/blast/ref-chain/hull_tables.py R... > TABLES
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_numbers import face, tables
for R in map(int, sys.argv[1:]):
    cells, red, coin = face('hull', R)
    nb, m1, m2 = tables(cells, red, coin)
    rows = [([*cells[i]], (nb[i], (m1[i], m2[i]))) for i in range(len(cells))]   # Lean prints (a, b, c, d) as nested pairs
    print(R, str(rows).replace(' ', ''))
