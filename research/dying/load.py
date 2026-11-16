#!/usr/bin/env python3
"""load.py: read the death histories and null samples written by sd.c into canonical-face arrays.

    python3 research/dying/load.py            # all four groups -> research/scratch/dying/canon_G.npz

Canonical face (PREDICTIONS.md): the face with sign vector s (cells with s.p = 11) is mapped to the +++ face by
p -> s*p. CANON is the sorted list of the 63 canonical cells; for each face, FIDX[s] maps canonical index -> full
cell index. A death record holds H states of the replica at lags j = 0..H-1 generations before the check; the death
generation t_d is the first generation at which some face orbit is empty, found as the largest j_d such that some
face orbit is empty at every j <= j_d (checked: j_d < CHK and no face empty at j_d + 1).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying')
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory', 'symmetric'))
import geom

GROUPS = ['c1', 'csz', 'c2v', 'd2h']
TIED = {'c1': (), 'csz': (2,), 'c2v': (0, 1), 'd2h': (0, 1, 2)}
R_HULL = 11; H = 512; CHK = 4
SIGNS = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


def geometry(group):
    q = geom.build(f'oct_{R_HULL}_c_{group}'); f = q.f
    canon = None; fidx = {}
    for s in SIGNS:
        sel = np.nonzero(f.cells @ np.array(s) == R_HULL)[0]
        c = f.cells[sel] * np.array(s)
        assert (c >= 0).all() and len(sel) == 63
        order = np.lexsort((c[:, 2], c[:, 1], c[:, 0]))
        c = c[order]; sel = sel[order]
        if canon is None:
            canon = c
        assert (canon == c).all()
        fidx[s] = sel
    # face orbits: faces whose node sets coincide
    nodesets = {s: tuple(np.unique(q.orb[fidx[s]])) for s in SIGNS}
    orbit_of = {}; reps = []
    for s in SIGNS:
        k = nodesets[s]
        if k not in orbit_of:
            orbit_of[k] = len(reps); reps.append(s)
    face_orbit = {s: orbit_of[nodesets[s]] for s in SIGNS}
    return q, canon, fidx, reps, face_orbit


def regions(canon):
    """edge bands B_a (rows 1-2 along edge a, apexes excluded), interior, apex mask"""
    apex = (canon == R_HULL).any(1)
    band = [(canon[:, a] <= 1) & ~apex for a in range(3)]
    interior = canon.min(1) >= 2
    assert [b.sum() for b in band] == [16, 16, 16] and interior.sum() == 18 and apex.sum() == 3
    return band, interior, apex


def read_dump(path, n):
    nb = (n + 7) // 8; rec = 20 + H * nb
    raw = np.fromfile(path, dtype=np.uint8)
    assert raw.size % rec == 0
    raw = raw.reshape(-1, rec)
    hdr = raw[:, :20].copy().view(np.int32)
    bits = np.unpackbits(raw[:, 20:].reshape(len(raw), H, nb), axis=2, bitorder='little')[:, :, :n].astype(bool)
    return hdr, bits                                        # bits[d, j, node]


def read_null(path, n):
    nb = (n + 7) // 8; rec = 8 + nb
    raw = np.fromfile(path, dtype=np.uint8).reshape(-1, rec)
    hdr = raw[:, :8].copy().view(np.int32)
    bits = np.unpackbits(raw[:, 8:], axis=1, bitorder='little')[:, :n].astype(bool)
    return hdr, bits


def process(group):
    q, canon, fidx, reps, face_orbit = geometry(group)
    n = q.n
    hdr, hist = read_dump(os.path.join(SCR, f'dump_{group}.bin'), n)
    # face-orbit emptiness at every j: nodes of each orbit representative
    nodes = [np.unique(q.orb[fidx[s]]) for s in reps]
    empty = np.stack([~hist[:, :, nd].any(2) for nd in nodes], 2)       # [d, j, orbit]
    anyempty = empty.any(2)
    assert anyempty[:, 0].all(), 'a dumped death without an empty face at the check'
    jd = np.argmin(anyempty, axis=1) - 1                                 # last j with a face empty, contiguous from 0
    assert (jd >= 0).all() and (jd < CHK).all(), 'death not within the last check interval'
    D = len(hdr); L = H - CHK                                            # lags 0..L-1 available for every death
    dying = []; X = np.zeros((D, L, 63), bool); NBR = np.zeros((D, 3, L, 63), bool) if group == 'c1' else None
    wts = np.zeros(D); multi = 0; samples = []
    for d in range(D):
        orbs = np.nonzero(empty[d, jd[d]])[0]
        assert not empty[d, jd[d] + 1].any()
        if len(orbs) > 1:
            multi += 1
        for o in orbs:
            samples.append((d, o, 1.0 / len(orbs)))
    # one row per (death, orbit) sample
    S = len(samples)
    X = np.zeros((S, L, 63), bool); W = np.zeros(S); DID = np.zeros(S, int); FS = np.zeros((S, 3), int)
    if group == 'c1':
        NBR = np.zeros((S, 3, L, 63), bool)
    for k, (d, o, w) in enumerate(samples):
        s = reps[o]; j0 = jd[d]
        h = hist[d, j0:j0 + L]                                           # lag l = j - j_d
        X[k] = h[:, q.orb[fidx[s]]]; W[k] = w; DID[k] = d; FS[k] = s
        if group == 'c1':
            for a in range(3):
                s2 = list(s); s2[a] = -s2[a]
                NBR[k, a] = h[:, q.orb[fidx[tuple(s2)]]]
    nh, nbits = read_null(os.path.join(SCR, f'null_{group}.bin'), n)
    NUL = np.concatenate([nbits[:, q.orb[fidx[s]]] for s in reps], 0)    # every face orbit of every kept record
    out = dict(X=X, W=W, DID=DID, FS=FS, NUL=NUL, canon=canon, jd=jd, hdr=hdr, multi=multi, ndeaths=D)
    if group == 'c1':
        out['NBR'] = NBR
    np.savez_compressed(os.path.join(SCR, f'canon_{group}.npz'), **out)
    print(f'{group}: deaths {D}, samples {S} ({multi} deaths with more than one face orbit empty at t_d), '
          f'j_d histogram {np.bincount(jd, minlength=CHK).tolist()}, null records {len(nh)}, null faces {len(NUL)}', flush=True)


if __name__ == '__main__':
    for g in (sys.argv[1:] or GROUPS):
        process(g)
