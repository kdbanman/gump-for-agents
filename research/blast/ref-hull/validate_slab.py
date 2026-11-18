#!/usr/bin/env python3
"""State-for-state check of sl.c (8-layer slab torus, period lattice (H,K),(0,D)) against reference/oracle.py.
The oracle only knows cubic array tori; a cubic torus of side 2n holds the slab torus (n,0),(0,n) (layers are
x+y+z mod 2n: 8 live layers, n-8 >= 3 dead ones, a firewall). A lattice (H,K),(0,D) that contains (n,0),(0,n) is
checked on that cover: the oracle starts from the periodic copies of sl's soup and must stay equal to sl on every copy.
   validate_slab.py H K D SEED GENS [NEG] [NLANES]      (NEG=1: negative control, must FAIL)"""
import sys, subprocess, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "reference"))
import oracle
H, K, D, seed, gens = map(int, sys.argv[1:6])
neg = int(sys.argv[6]) if len(sys.argv) > 6 else 0
nl = int(sys.argv[7]) if len(sys.argv) > 7 else 3
n = next(n for n in range(11, 400) if n % D == 0 and n % H == 0 and ((n // H) * K) % D == 0)
out = subprocess.run([os.path.join(here, "sl"), "val", str(H), str(K), str(D), str(seed), str(gens), str(neg)], capture_output=True, text=True).stdout.split("\n")
N = int(out[0].split()[0])
xyz = np.array([list(map(int, out[1 + i].split())) for i in range(N)])
assert all((abs(xyz) % 2).sum(1) == 1) and all(abs(xyz.sum(1)) <= 7)
HC = 2 * n; m = oracle.masks(HC)
v1 = np.array([2 * H + 2 * K, -2 * H, -2 * K]); v2 = np.array([2 * D, 0, -2 * D])
copies = n * n // (H * D)
sites = []
for c in range(N):
    st = set()
    for a in range(0, 2 * n // H + 1):
        for b in range(0, 2 * n // D + 1):
            st.add(tuple((xyz[c] + a * v1 + b * v2) % HC))
    assert len(st) == copies, (len(st), copies)
    sites.append(sorted(st))
flat = np.array([s for ss in sites for s in ss]); ix = (flat[:, 0], flat[:, 1], flat[:, 2])
assert len(set(map(tuple, flat))) == N * copies
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
bad = 0
for lane in sorted({k[1] for k in states})[:nl]:
    h = np.zeros((HC, HC, HC), np.int8); h[ix] = np.repeat(dec(states[(0, lane)]), copies)
    pops = []
    for g in range(1, gens + 1):
        h = oracle.step(h, m)
        mine = np.repeat(dec(states[(g, lane)]), copies)
        if int(h.sum()) != int(mine.sum()) or not (h[ix] == mine).all():
            print(f"torus ({H},{K}),(0,{D}) lane {lane}: FIRST MISMATCH at generation {g}"); bad += 1; break
        pops.append(int(mine.sum()) // copies)
    else:
        print(f"torus ({H},{K}),(0,{D}) lane {lane}: {gens} generations identical to the oracle (cubic torus of side {HC}, {copies} copies), state for state; N={N}, population min/last {min(pops)}/{pops[-1]}")
print("VALIDATION", "FAILED" if bad else "PASSED", f"(torus ({H},{K}),(0,{D}), seed={seed}, gens={gens}, neg={neg})")
sys.exit(1 if bad else 0)
