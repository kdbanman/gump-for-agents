#!/usr/bin/env python3
"""The rimmed hull face's vessel for hd.c: the exact hull of the soup region |p|_1 <= R (cube-centred), as in
research/gpu/facelaw.py / research/gpu-local/hullface.py `vessel(R)` (fl.Vessel(fl.octa_hull(R, 'c'), 'c', False),
seed mask gsim.seed_mask = |p|_1 <= R). Built with numpy only (no cupy, no GPU).

  python research/dying2/hull/hullvessel.py R        # writes research/scratch/dying2-hull/hv_R.bin and hv_R.npz

Vessel file (int32 LE): magic 0x48563031, n, nf (= 8), nfn, nb[n*12] (-1 = outside), seed[n] (0/1),
fn[nfn] (node of each face-layer cell, sorted), per face: A_f, then A_f positions into fn.
Geometry npz: cells, fn, face_pos (8 x A, positions into fn), and per face cell: row (layers to the nearest edge
plane, 0 = the shared rim row), dcorner (distance to the nearest corner, cube units), and the face adjacency
(edge neighbours, vertex neighbours, opposite).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'fluct'))
import fl  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'dying2-hull')


def build(R):
    v = fl.Vessel(fl.octa_hull(R, 'c'), 'c', False)
    seed = np.abs(v.cells - v.c).sum(1) <= R
    faces = [v.groups[g][0].astype(np.int64) for g in v.face_groups]      # order (d, sgn): (0,+),(0,-),(1,+),...
    names = [v.gnames[g] for g in v.face_groups]
    fn = np.unique(np.concatenate(faces))
    pos = {int(x): i for i, x in enumerate(fn)}
    face_pos = [np.array([pos[int(x)] for x in f], np.int64) for f in faces]
    s = v.cells @ fl.DIAGS.T
    hull = v.hull
    # adjacency by shared cells
    share = np.array([[len(np.intersect1d(a, b)) for b in faces] for a in faces])
    edge_nb, vert_nb, opp = [], [], []
    for f, (d, sg, _) in enumerate(names):
        e = [g for g in range(8) if g != f and share[f, g] > 2]
        o = [g for g, (d2, sg2, _) in enumerate(names) if d2 == d and sg2 != sg]
        vv = [g for g in range(8) if g != f and g not in e and g not in o]
        edge_nb.append(e); vert_nb.append(vv); opp.append(o[0])
        assert len(e) == 3 and len(vv) == 3, (f, e, vv, share[f])
    # rows: layers from each edge neighbour's plane
    row, dcorner, nface = [], [], np.zeros(len(fn), int)
    for f in range(8):
        nface[face_pos[f]] += 1
    for f in range(8):
        cf = faces[f]
        dist = []
        for g in edge_nb[f]:
            d2, sg2, _ = names[g]
            b = hull[d2][1] if sg2 > 0 else hull[d2][0]
            dist.append(np.abs(b - s[cf, d2]) // 2)
        dist = np.array(dist)                      # 3 x A
        row.append(dist.min(0))
        # corners: cells at distance 0 from two edge planes; cluster by which pair
        P = v.cells[cf] / 2.0
        cs = []
        for i in range(3):
            for j in range(i + 1, 3):
                m = (dist[i] == 0) & (dist[j] == 0)
                if not m.any():                    # corners cut: take the cells minimising the sum
                    t = dist[i] + dist[j]; m = t == t.min()
                cs.append(P[m].mean(0))
        cs = np.array(cs)
        dcorner.append(np.sqrt(((P[:, None, :] - cs[None]) ** 2).sum(-1)).min(1))
    return dict(v=v, seed=seed, faces=faces, names=names, fn=fn, face_pos=face_pos, edge_nb=edge_nb, vert_nb=vert_nb,
                opp=opp, row=row, dcorner=dcorner, nface=nface, share=share)


def write(R):
    os.makedirs(SCR, exist_ok=True)
    b = build(R); v = b['v']
    arr = [0x48563031, v.n, 8, len(b['fn'])]
    buf = np.array(arr, '<i4').tobytes() + v.nb.astype('<i4').tobytes() + b['seed'].astype('<i4').tobytes()
    buf += b['fn'].astype('<i4').tobytes()
    for fp in b['face_pos']:
        buf += np.array([len(fp)], '<i4').tobytes() + fp.astype('<i4').tobytes()
    p = os.path.join(SCR, f'hv_{R}.bin'); open(p, 'wb').write(buf)
    np.savez(os.path.join(SCR, f'hv_{R}.npz'), cells=v.cells, fn=b['fn'], face_pos=np.array(b['face_pos']),
             row=np.array(b['row']), dcorner=np.array(b['dcorner']), edge_nb=np.array(b['edge_nb']),
             vert_nb=np.array(b['vert_nb']), opp=np.array(b['opp']), nface=b['nface'], seed=b['seed'], nb=v.nb,
             names=np.array(b['names']), hull=np.array(v.hull))
    A = [len(f) for f in b['faces']]
    print(f'R = {R}: nodes {v.n}, seedable {int(b["seed"].sum())}, face cells {A}, face-layer union {len(b["fn"])}, '
          f'cells in 2 / >=3 faces {int((b["nface"] == 2).sum())} / {int((b["nface"] >= 3).sum())}; rows {np.bincount(b["row"][0])}; '
          f'edge nb of face 0 {b["edge_nb"][0]}, vertex {b["vert_nb"][0]}, opposite {b["opp"][0]} -> {p}')
    return p


if __name__ == '__main__':
    write(int(sys.argv[1]))
