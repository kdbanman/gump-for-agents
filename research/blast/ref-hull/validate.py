#!/usr/bin/env python3
"""State-for-state check of rh.c's stepper against reference/oracle.py.
   validate.py R SEED GENS [NEG]   (NEG=1: negative control, must FAIL)"""
import sys, subprocess, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "reference"))
import oracle
R, seed, gens = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
neg = int(sys.argv[4]) if len(sys.argv) > 4 else 0
out = subprocess.run([os.path.join(here, "rh"), "val", str(R), str(seed), str(gens), str(neg)], capture_output=True, text=True).stdout.split("\n")
N, R2 = map(int, out[0].split()); assert R2 == R
xyz = np.array([list(map(int, out[1 + i].split())) for i in range(N)])
assert all(abs(xyz).sum(1) <= R) and all((abs(xyz) % 2).sum(1) == 1)
H = 2 * R + 10; o = R + 5; assert o % 2 == 0
m = oracle.masks(H)
ix = (xyz[:, 0] + o, xyz[:, 1] + o, xyz[:, 2] + o)
def dec(hx):
    bits = np.zeros(N, np.int8)
    for k in range(0, len(hx), 16):
        w = int(hx[k:k + 16], 16); base = (k // 16) * 64
        for b in range(64):
            if (w >> b) & 1: bits[base + b] = 1
    return bits
states = {}
for line in out[1 + N:]:
    if not line.strip(): continue
    g, lane, hx = line.split(); states[(int(g), int(lane))] = hx
lanes = sorted({k[1] for k in states})
bad = 0
for lane in lanes:
    h = np.zeros((H, H, H), np.int8); h[ix] = dec(states[(0, lane)])
    pops = []
    for g in range(1, gens + 1):
        h = oracle.step(h, m)
        mine = dec(states[(g, lane)])
        tot = int(h.sum()); inside = h[ix]
        if tot != int(inside.sum()) or not (inside == mine).all():
            print(f"R {R} lane {lane}: FIRST MISMATCH at generation {g} (oracle pop {tot}, rh pop {int(mine.sum())})"); bad += 1; break
        pops.append(tot)
    else:
        print(f"R {R} lane {lane}: {gens} generations identical to the oracle, state for state; N={N} pop first/min/last {pops[0]}/{min(pops)}/{pops[-1]}")
print("VALIDATION", "FAILED" if bad else "PASSED", f"(R={R}, seed={seed}, gens={gens}, neg={neg})")
sys.exit(1 if bad else 0)
