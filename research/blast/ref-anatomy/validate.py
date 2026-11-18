#!/usr/bin/env python3
"""State-for-state check of fd.c + vessel.py against reference/oracle.py.

  python3 validate.py NAME [swap] [REPLICA] [GENS]     NAME in t63, tube60, h63

A slab with period lattice L of index n is put on the oracle's cubic torus of side 2n (n*(hex lattice) is inside L,
and s = x+y+z is defined modulo 2n >= 40, so the 8 live layers are separated from their images by >= 12 dead layers,
which stay dead by T2).  A hull of radius R sits in the middle of a torus of side 28.  The oracle is started from
fd's generation 0 and both run GENS generations; every generation the whole oracle array must equal the image
of fd's state.  `swap` uses a graph with one wrong neighbour and must FAIL.
"""
import sys, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle, vessel

name = sys.argv[1]
swap = 'swap' in sys.argv[2:]
nums = [int(a) for a in sys.argv[2:] if a.isdigit()]
rep = nums[0] if nums else 0
G = nums[1] if len(nums) > 1 else 1100
fn, v = vessel.write(name, swap)
out = os.path.join(vessel.SCR, f'trace_{name}{"_swap" if swap else ""}.bin')
subprocess.check_call([os.path.join(HERE, os.environ.get('FD', 'fd')), fn, 'trace', '7', str(rep), str(G), out])
tr = np.fromfile(out, np.uint8).reshape(G + 1, v['N'])
if v['kind'] == 'slab':
    H = 2 * v['HKD'][0] * v['HKD'][2]
else:
    H = 28
idm = np.full((H, H, H), -1, int)
m = oracle.masks(H)
valid = m[0] | m[1] | m[2]
for x, y, z in zip(*np.where(valid)):
    if v['kind'] == 'slab':
        s = (x + y + z) % H
        if s % 2 == 1 and 1 <= s <= 15:
            idm[x, y, z] = v['idx'][v['canon']((int(x) - (int(x + y + z) - int(s)), int(y), int(z)))]
    else:
        idm[x, y, z] = v['idx'].get((int(x) - 14, int(y) - 14, int(z) - 14), -1)
inside = idm >= 0
cnt = np.bincount(idm[inside], minlength=v['N'])
assert cnt.min() == cnt.max() >= 1, (cnt.min(), cnt.max())
def image(st):
    a = np.zeros((H, H, H), np.int8); a[inside] = st[idm[inside]]; return a
h = image(tr[0])
bad = None
for t in range(1, G + 1):
    h = oracle.step(h, m)
    if not (h == image(tr[t])).all():
        bad = t; break
pops = [int(tr[t].sum()) for t in (0, 10, 100, G // 2, G)]
print(f'{name}{" SWAP" if swap else ""} replica {rep}: oracle torus side {H}, {cnt.max()} images per cell, {v["N"]} cells; '
      f'populations at t=0,10,100,{G//2},{G}: {pops}; ' + (f'FIRST MISMATCH at generation {bad}' if bad else f'identical for {G} generations'))
sys.exit(1 if bad else 0)
