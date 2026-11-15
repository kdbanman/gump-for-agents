#!/usr/bin/env python3
"""What the L2 receiver is: the record each pulse adds is 2 cells per cube, (0,2,3) turned on and (1,0,2) turned off
(per-cube representatives).  Is wire B with that change in every cube ("wire B'") itself a wire (period 2 on a
ring of 24 cubes, own sparse ring stepper), i.e. is the receiver a wall between B and B' that each pulse moves?

    python3 receiver_wire.py
"""
import json, subprocess
from lat import sstep_ring, canon_ring, wire, ROOT
ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'bcd5844:research/signals/objects/transmission-B.json']))
bg = [tuple(c) for c in ob['bg']]
assert (1, 0, 2) in bg and (0, 2, 3) not in bg
bp = [c for c in bg if c != (1, 0, 2)] + [(0, 2, 3)]
N = 24
x = frozenset(canon_ring(c, N) for c in wire(bp, 0, N)); orb = [x]
for t in range(12):
    x = sstep_ring(x, N); orb.append(x)
per = next((q for q in range(1, 13) if orb[q] == orb[0]), None)
print("wire B' (B with (1,0,2) off and (0,2,3) on in every cube), ring of 24 cubes: period", per,
      '; cells per cube over 12 generations:', [len(s) // N for s in orb])
