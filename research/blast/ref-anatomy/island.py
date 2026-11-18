#!/usr/bin/env python3
"""One live cell left on a face (anatomy's claim 4, second half), with the referee's stepper.
   python3 island.py [BATCHES]  -> out/island.txt     (256 trials per batch; soup, 1000 generations, then the cut)"""
import sys, os, subprocess
import numpy as np, vessel
HERE = os.path.dirname(os.path.abspath(__file__))
B = sys.argv[1] if len(sys.argv) > 1 else '60'
out = open(os.path.join(HERE, 'out', 'island.txt'), 'w')
def run(name, lab, cand, seed):
    fn, v = vessel.write(name)
    r = subprocess.check_output([os.path.join(HERE, 'fd_island'), fn, 'island', str(seed), B, str(len(cand))] + [str(c) for c in cand]).decode().strip()
    s = f'{name:7s} {lab:28s} ({len(cand):2d} cells): {r}'; print(s); out.write(s + '\n')
for k, name in enumerate(('t63', 'tube60')):
    v = vessel.get(name); run(name, 'any cell', list(v['faces'][0]), 31 + k)
v = vessel.get('h63'); fc = v['faces'][0]; pts = np.abs(np.array(v['cells'])[fc])
nz = (pts == 0).sum(1); mn = pts.min(1); mx = pts.max(1)
run('h63', 'corner', list(fc[nz == 2]), 41)
run('h63', 'rim line next to a corner', list(fc[(nz == 1) & (mx >= 9)]), 42)
run('h63', 'rim line, the rest', list(fc[(nz == 1) & (mx < 9)]), 43)
run('h63', 'rim line, all but corners', list(fc[nz == 1]), 44)
run('h63', 'inside (no zero coordinate)', list(fc[nz == 0]), 45)
run('h63', 'centre (min coordinate 3)', list(fc[mn >= 3]), 46)
for d in (1, 2):
    run('h63', f'inside, min coordinate {d}', list(fc[(nz == 0) & (mn == d)]), 50 + d)
