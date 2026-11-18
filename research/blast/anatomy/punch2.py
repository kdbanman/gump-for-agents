#!/usr/bin/env python3
"""Islands on a hull face against islands on the wrapped face of the same area (research/blast/anatomy).

    python3 punch2.py       # about half a minute; out/punch2.json

Hull of radius 11 (63-cell faces) and torus (1,4),(0,21) (63 cells). After 800 generations all cells of face 0 are
killed except the n nearest to a chosen cell (hull: the centre, the middle of a rim line, the rim line next to a
corner, a corner); 4 trials x 512 replicas. Reported: share of faces alive at generation 150, by the number of
island cells that were alive at the start.
"""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geom, deaths as D
AN = os.path.join(geom.SCR, 'an'); T0, TMAX, NT = 800, 150, 4


def run(kind, args, name, clear, seed):
    path, (vname, cells, nb, faces, groups, meta) = geom.build(kind, *args)
    fc, uc = faces[0]
    cl = os.path.join(geom.SCR, f'punch_{name}.txt'); open(cl, 'w').write(' '.join(str(fc[i]) for i in clear))
    out = os.path.join(geom.SCR, f'punch_{name}.bin')
    subprocess.check_call([AN, path, 'punch', str(seed), '0.4', str(T0), str(TMAX), str(NT), cl, out])
    raw = np.fromfile(out, np.uint8).reshape(NT, TMAX + 1, len(fc) + len(uc), 64)
    bits = np.unpackbits(raw, axis=3, bitorder='little'); os.remove(out)
    return bits[:, :, :len(fc), :].transpose(1, 2, 0, 3).reshape(TMAX + 1, len(fc), NT * 512), meta


res = {}; seed = 500
path, v = geom.build('hull', 11); meta = v[5]; mp = [tuple(sorted(m)) for m in meta['mapped'][0]]
Gh = D.Geo(meta['facepos'][0], None)
path, v = geom.build('slab', 1, 4, 21); Gt = D.Geo(v[5]['facepos'][0], v[5]['period'])
sites = [('hull', (11,), 'centre (3,4,4)', mp.index((3, 4, 4)), Gh), ('hull', (11,), 'rim middle (0,5,6)', mp.index((0, 5, 6)), Gh),
         ('hull', (11,), 'rim near corner (0,2,9)', mp.index((0, 2, 9)), Gh), ('hull', (11,), 'corner (0,0,11)', mp.index((0, 0, 11)), Gh),
         ('slab', (1, 4, 21), 'torus 63', 0, Gt)]
for kind, args, nm, c, G in sites:
    for n in (3, 5, 8):
        seed += 1
        isl = np.argsort(G.r[c])[:n]; clear = np.setdiff1d(np.arange(G.A), isl)
        S, _ = run(kind, args, 'p2', list(clear), seed)
        P = S.sum(1); n0 = S[0][isl].sum(0); alive = P[TMAX] >= 8
        by = {int(k): (float(alive[n0 == k].mean()), int((n0 == k).sum())) for k in np.unique(n0)}
        res[f'{nm} n={n}'] = dict(regrow=float(alive.mean()), mean_alive0=float(n0.mean()), by=by)
        print(f'{nm:26s} island of {n}: {n0.mean():.2f} alive at start; regrows {alive.mean():.3f}; by number alive at start: '
              + ' '.join(f'{k}:{a:.3f}+-{np.sqrt(a * (1 - a) / m):.3f}({m})' for k, (a, m) in by.items()))
json.dump(res, open(os.path.join(HERE, 'out', 'punch2.json'), 'w'), indent=1)
