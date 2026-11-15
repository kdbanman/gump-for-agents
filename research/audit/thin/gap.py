#!/usr/bin/env python3
"""Do the layers beneath a gap of the face thin out? (review of research/theory/thin/, claim 6). tt.c traces of single
lanes of the deterministic ring b = 48; for each generation >= 256 while face 0 lives, each maximal run of >= L empty
face sites; density of layers 1..4 (three cells per site) at the middle site of the run, against the mean density of
the layer.

    python3 research/audit/thin/gap.py [nseeds] [G]
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tt  # noqa: E402

b = 48
ns = int(sys.argv[1]) if len(sys.argv) > 1 else 4
G = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
tt.build()
cells, idx, nb, face, wallc, coin, inter = tt.vessel('det', b, 0, 0)
path = tt.write_vessel('det', b, 0, 0)
sc = lambda s, t: [idx[c] for c in tt.site_cells(s, t, b)]
S = np.array([[sc(s, t) for s in range(b)] for t in range(8)])      # [t, s, 3]
acc = {}; mean = np.zeros(8); nmean = 0
for seed in range(ns):
    tr = os.path.join(tt.OUT, f'gap_{os.getpid()}.txt')
    subprocess.run([tt.BIN, path, str(7000 + seed), '1', '0', '/dev/null', '-t', tr, str(G)], check=True)
    X = np.array([[int(ch) for ch in l.split()[2]] for l in open(tr)], dtype=np.int8)
    os.remove(tr)
    occ = X[:, S].sum(3)                                               # [g, t, s] live cells per site
    for g in range(256, len(X)):
        if occ[g, 0].sum() == 0:
            break
        mean += occ[g].mean(1) / 3; nmean += 1
        o = occ[g, 0] > 0
        if o.all():
            continue
        s0 = int(np.argmax(o))
        run = 0
        for k in range(1, b + 1):
            s = (s0 + k) % b
            if not o[s]:
                run += 1
            else:
                if run >= 2:
                    mid = (s - 1 - (run - 1) // 2) % b
                    key = min(run, 10)
                    a = acc.setdefault(key, [np.zeros(8), 0]); a[0] += occ[g, :, mid] / 3; a[1] += 1
                run = 0
mean /= nmean
print(f'{ns} lanes, {nmean} living generations; mean density by layer 0..4: ' + ' '.join(f'{x:.3f}' for x in mean[:5]))
for k in sorted(acc):
    v, n = acc[k]
    print(f'gap {k:2d}{"+" if k == 10 else " "} sites ({n:7d}): density at its middle, layers 1..4: ' +
          ' '.join(f'{x:.3f}' for x in (v / n)[1:5]))
