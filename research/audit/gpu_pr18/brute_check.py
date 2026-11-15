#!/usr/bin/env python3
"""PR 18 review: pc.c's patch counts against a brute-force numpy count from the cell sets (W = 1, 64 replicas, same
soup RNG reproduced in Python), burn B, then G counted generations; every group's samples / hits / hits2 compared.
  python3 research/audit/gpu_pr18/brute_check.py
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'pr18')
sys.path.insert(0, HERE)
import geom18

PC = os.path.join(OUT, 'pc')
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', PC, os.path.join(HERE, 'pc.c')])
prog = os.path.join(OUT, 'prog_o0.bin')
cells, groups, sets, inl = geom18.write(prog, 0)
_, layer, nb, inl, nodes, groups, _ = geom18.program(0)
n = len(cells)
seed, p, B, G = 5, 0.4, 40, 30
M64 = (1 << 64) - 1
sm = (seed * 0x2545F4914F6CDD1D + 777) & M64
thr = int(p * 2 ** 64)
X = np.zeros((n + 1, 64), bool)
for i in range(n):
    for k in range(64):
        sm = (sm + 0x9e3779b97f4a7c15) & M64; z = sm
        z = ((z ^ (z >> 30)) * 0xbf58476d1ce4e5b9) & M64; z = ((z ^ (z >> 27)) * 0x94d049bb133111eb) & M64; z ^= z >> 31
        X[i, k] = z < thr
# explicit cell sets per (group, translate), from the definitions (not from the DAG)
N, Mm = geom18.N, geom18.M
idx = {c: i for i, c in enumerate(cells)}
want = {}
for f, t in ((0, 0), (1, Mm - 1)):
    for kind in ('up', 'down'):
        T = lambda i, j: geom18.tri(idx, t, 0, i, j, kind)
        for b in geom18.STRIPS:
            want[f'f{f} {kind} strip 1x{b}'] = [sorted({c for y in range(b) for c in T(i, j + y)}) for i in range(N) for j in range(N)]
        for a, b in geom18.RHOMBI:
            want[f'f{f} {kind} rhombus {a}x{b}'] = [sorted({c for x in range(a) for y in range(b) for c in T(i + x, j + y)})
                                                    for i in range(N) for j in range(N)]
    face = [u for u in range(n) if layer[u] == t]
    for r in geom18.BALLS:
        L = []
        for c0 in face:
            seen = {c0}; fr = [c0]
            for _ in range(r):
                fr = [v for u in fr for v in inl[u] if v not in seen]; seen |= set(fr)
            L.append(sorted(seen))
        want[f'f{f} ball r={r}'] = L
assert set(want) == {g for g, _ in groups}
tot = {g: [0, 0, 0] for g in want}
prev = {}
for gen in range(B + G):
    c = X[nb].sum(1)                       # (n, 64) live neighbour counts (sentinel row n is dead)
    Y = np.zeros_like(X); Y[:n] = ((c[:n] == 4) | (c[:n] == 5)) | (X[:n] & (c[:n] == 3)); X = Y
    if gen + 1 <= B:
        continue
    for g, L in want.items():
        E = np.array([~X[s].any(0) for s in L])          # (translates, 64)
        tot[g][0] += E.size; tot[g][1] += int(E.sum())
        if g in prev:
            tot[g][2] += int((E & prev[g]).sum())
        prev[g] = E
fo = os.path.join(OUT, 'brute_pc.tsv')
subprocess.check_call([PC, prog, '1', str(p), str(seed), str(B), str(G), '1', fo], stderr=subprocess.DEVNULL)
got = {}
for line in open(fo):
    if line.startswith('#'):
        print(line.strip()); continue
    b, name, s, h, h2 = line.rstrip('\n').split('\t'); got[name] = [int(s), int(h), int(h2)]
bad = [g for g in want if got[g] != tot[g]]
nh = sum(v[1] for v in tot.values())
print(f'{len(want)} groups, {G} generations x 64 replicas, {nh} empty patches in all: '
      + ('identical' if not bad else f'DIFFER in {bad[:5]}'))
for g in ('f0 up rhombus 2x2', 'f0 down rhombus 2x2', 'f1 up rhombus 2x2', 'f0 ball r=2'):
    print(' ', g, tot[g], got[g])
