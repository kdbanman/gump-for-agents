#!/usr/bin/env python3
"""Which of the C = 35 guns are the C = 31 gun in disguise.  Needs the two lists written by (in research/signals/)
    python3 sat_gun.py 5f 31 --all --out ../scratch/signals4/gun31.json
    python3 sat_gun.py 5f 35 --all --out ../scratch/signals4/gun35.json
The C = 31 gun with its train is stepped (st.step) 0..3 generations, moved 0..2 units towards +v, and its units >= 6
compared with each C = 35 solution.     python3 census_translate.py"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
sys.path.insert(0, os.path.join(st.ROOT, 'research', 'signals'))
import sat_gun as G
S = os.path.join(st.ROOT, 'research', 'scratch', 'signals4')
g35 = [frozenset(map(tuple, d['cap'])) for d in json.load(open(os.path.join(S, 'gun35.json')))['list']]
g31 = frozenset(map(tuple, json.load(open(os.path.join(S, 'gun31.json')))['list'][0]['cap']))
pat, _ = G.train([5, 15])
xs = st.run(G.train_cells(pat, 0, -60, 6) | g31, 4)
for ph in range(4):
    for k in range(3):
        y = frozenset(st.tr(c, k) for c in xs[ph] if st.U(c) + k >= 6)
        for i, g in enumerate(g35):
            if y == g:
                print(f'C = 35 solution #{i} ({len(g)} cells) = the C = 31 gun at generation {ph} moved {k} units towards +v')
