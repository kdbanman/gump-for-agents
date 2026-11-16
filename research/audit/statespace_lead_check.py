"""Lead's own check of one row of research/statespace/data/vessels.jsonl (2026-11-15).

Uses only reference/oracle.py (masks, step) and the vessel's name; none of the study's code.  A diagonal hull
`hull_L0_H0_L1_H1_L2_H2_L3_H3` is the set of face cells p (doubled coordinates, exactly one odd) with
L_d <= d.p <= H_d on the four body diagonals d = (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), in that order (the
convention of research/statespace/vessels.py, read there; the cell set is rebuilt here and its size checked).  Every one of the 2^N states is then placed in empty space (an array torus with a margin of 6 doubled
units on every side), stepped ONCE by the oracle, and the image is checked to lie inside the hull (so the map is
closed) and recorded.  From the full table f: states with no predecessor, states on cycles, the number of cycles,
transient lengths (mean, maximum, how many states attain the maximum), and the size of the empty state's basin.
    python3 research/audit/statespace_lead_check.py hull_-1_1_-5_-1_-5_3_-3_5
"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

name = sys.argv[1]
row = next(r for r in map(json.loads, open('research/statespace/data/vessels.jsonl')) if r['name'] == name)
b = [int(x) for x in name.split('_')[1:]]; N = row['N']
R = 14
pts = [p for p in itertools.product(range(-R, R + 1), repeat=3) if sum(c % 2 for c in p) == 1]
# the study's convention (read from its definition, not imported): s_d = D[d].p with these four diagonals, in order
D = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
cells = [p for p in pts if all(b[2 * k] <= sum(D[k][i] * p[i] for i in range(3)) <= b[2 * k + 1] for k in range(4))]
diag = D
assert len(cells) == N and max(max(abs(x) for x in p) for p in cells) < R - 1, len(cells)
assert cells, 'no convention gives N cells'
lo = [min(p[i] for p in cells) for i in range(3)]; hi = [max(p[i] for p in cells) for i in range(3)]
H = max(hi[i] - lo[i] for i in range(3)) + 14; H += H % 2
off = [(6 - lo[i]) // 2 * 2 + 2 for i in range(3)]
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
idx = [tuple(p[i] + off[i] for i in range(3)) for p in cells]
assert all(valid[x] for x in idx)
inside = np.zeros((H, H, H), dtype=bool)
for x in idx: inside[x] = True
flat = np.array([np.ravel_multi_index(x, (H, H, H)) for x in idx])
S = 1 << N
f = np.zeros(S, dtype=np.int64)
w = (1 << np.arange(N)).astype(np.int64)
for s in range(S):
    h = np.zeros(H * H * H, dtype=bool)
    bits = (s >> np.arange(N)) & 1
    h[flat] = bits.astype(bool)
    g = oracle.step(h.reshape(H, H, H), m)
    assert not (g & ~inside).any(), ('a cell was born outside the hull', s)
    f[s] = int((g.ravel()[flat] * w).sum())
indeg = np.bincount(f, minlength=S)
goe = int((indeg == 0).sum())
# states on cycles: iterate f^(2^k) image until stable
on = np.ones(S, dtype=bool); cur = np.arange(S)
img = np.unique(f)
while True:
    nxt = np.unique(f[img])
    if len(nxt) == len(img): break
    img = nxt
cyc = set(img.tolist())
# transient length of every state
T = np.full(S, -1, dtype=np.int64)
for s in cyc: T[s] = 0
order = np.argsort(indeg)  # any order; resolve by walking
for s in range(S):
    path = []
    x = s
    while T[x] < 0: path.append(x); x = int(f[x])
    t = T[x]
    for y in reversed(path): t += 1; T[y] = t
seen = set(); ncyc = 0
for s in cyc:
    if s in seen: continue
    ncyc += 1; x = s
    while x not in seen: seen.add(x); x = int(f[x])
# basin of the empty state (a fixed point)
assert f[0] == 0
x = np.arange(S)
for _ in range(int(T.max()) + 1): x = f[x]
empty_basin = int((x == 0).sum())
mine = dict(N=N, goe=goe, cycles=ncyc, cyclic_states=len(cyc), max_transient=int(T.max()), n_champions=int((T == T.max()).sum()),
            mean_transient=float(T.mean()), empty_basin=empty_basin)
ok = True
for k, v in mine.items():
    same = abs(v - row[k]) < 1e-9
    ok &= same
    print(f'{k:16s} mine {v}   study {row[k]}   {"same" if same else "DIFFERENT"}')
print('diagonals used', diag, 'H', H)
print('PASS' if ok else 'FAIL')
