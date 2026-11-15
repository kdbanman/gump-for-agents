#!/usr/bin/env python3
"""What lies beneath the wall of a segment (review of research/theory/thin/, claim 2). tt.c traces of single lanes
(det, b = 32, wall 3 = segment of 29 sites), generations 256..G while both faces live; density of live cells by
layer and site distance from the wall, for faces 0 and 7 folded together (layer depth = distance from the face).

    python3 research/audit/thin/beneath.py [nseeds] [G]
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tt  # noqa: E402

b, wall = 32, 3
ns = int(sys.argv[1]) if len(sys.argv) > 1 else 6
G = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
tt.build()
cells, idx, nb, face, wallc, coin, inter = tt.vessel('det', b, 0, wall)
path = tt.write_vessel('det', b, 0, wall)
site = np.array([(c[2] if c[0] in (1, 2) else (c[2] - 1)) % b for c in cells])
lay = np.array([c[3] for c in cells])
acc = np.zeros((8, b)); cnt = 0
for s in range(ns):
    tr = os.path.join(tt.OUT, f'bn_{os.getpid()}.txt')
    subprocess.run([tt.BIN, path, str(5000 + s), '1', '0', '/dev/null', '-t', tr, str(G)], check=True)
    X = np.array([[int(ch) for ch in l.split()[2]] for l in open(tr)], dtype=np.int8)
    os.remove(tr)
    f0 = X[:, face[0]].sum(1); f1 = X[:, face[1]].sum(1)
    alive = np.nonzero((f0 == 0) | (f1 == 0))[0]
    end = alive[0] if len(alive) else len(X)
    if end <= 256:
        continue
    Y = X[256:end].astype(float).mean(0) * (end - 256)
    for i in range(len(cells)):
        acc[lay[i], site[i]] += Y[i]
    cnt += end - 256
den = acc / (3 * cnt)
print(f'{ns} lanes, {cnt} generations with both faces alive; density by depth from the face (faces folded), by site')
print('site:      ' + ' '.join(f'{s:5d}' for s in range(b)))
for d in range(4):
    row = (den[d] + den[7 - d]) / 2
    print(f'depth {d}:   ' + ' '.join(f'{x:5.3f}' for x in row))
far = [s for s in range(b) if 10 <= s <= 25]
for d in range(4):
    row = (den[d] + den[7 - d]) / 2
    print(f'depth {d}: beneath wall sites 0-2 {row[:3].mean():.3f}; sites 3-4 {row[3:5].mean():.3f}; middle (10-25) {row[far].mean():.3f}')
