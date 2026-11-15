#!/usr/bin/env python3
"""oh_data.py: the O_h face measurements made before this study (research/fluct/data/sym_residence.csv, CPU;
research/data/gpu_facelaw/sym*.json, GPU), the geometry of the faces, and what the data say about the three fitted
ingredients of ln tau = 0.698 + (0.209/6) A - 0.196 sqrt(A).

    python3 research/theory/symmetric/oh_data.py

Prints: (1) exact counts for the faces actually measured: cells on diagonal mirrors, rim cells, corner cells, kind
of the centre; (2) the pooled table of ln tau by area and centring; (3) cube-centred fits a + sA + b sqrt(A) with
the slope pinned to c/6 for several c, and free; (4) the vertex/cube difference against a constant and against
k sqrt(A); (5) residuals by kind of centre.
"""
import csv, glob, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def face_cells(R, centre):
    """cells of the (111) face of the octahedron of radius R, as offsets from the centre (all >= 0, sum R)."""
    out = []
    odd = 1 if centre == 'c' else 2
    for x in range(R + 1):
        for y in range(R + 1 - x):
            z = R - x - y
            if (x % 2) + (y % 2) + (z % 2) == odd:
                out.append((x, y, z))
    return np.array(out)


def geometry(R, centre):
    f = face_cells(R, centre); A = len(f)
    onmirror = (f[:, 0] == f[:, 1]) | (f[:, 1] == f[:, 2]) | (f[:, 0] == f[:, 2])
    nzero = (f == 0).sum(1)
    rim = nzero == 1; corner = nzero == 2
    s = R if centre == 'c' else R + 3            # layer index along the axis through a cube centre
    kind = {1: 'triangle', 3: 'hexagon', 5: 'triangle*'}[s % 6]
    return dict(R=R, centre=centre, A=A, mirror=int((onmirror & ~corner).sum()), rim=int(rim.sum()), corner=int(corner.sum()),
                mirror_and_rim=int((onmirror & rim).sum()), kind=kind)


def load():
    """-> {(A, centre): (deaths, exposure)} pooled; CPU fresh soups and GPU runs (no copies of the cube16 snapshots)."""
    pool = {}
    with open(os.path.join(ROOT, 'research', 'fluct', 'data', 'sym_residence.csv')) as fh:
        for r in csv.DictReader(fh):
            if r['tag'].startswith('snap') or int(r['deaths']) == 0:
                continue
            p = pool.setdefault((int(r['A']), r['centre']), [0, 0.0]); p[0] += int(r['deaths']); p[1] += float(r['exposure'])
    for f in sorted(glob.glob(os.path.join(ROOT, 'research', 'data', 'gpu_facelaw', 'sym*.json'))):
        d = json.load(open(f)); e = d['agg']['1000']
        p = pool.setdefault((int(d['A']), d['centre']), [0, 0.0]); p[0] += e['deaths']; p[1] += e['exposure']
    return pool


def wls(X, y, s):
    W = 1 / s ** 2
    cov = np.linalg.inv(X.T @ (X * W[:, None])); b = cov @ (X.T @ (W * y))
    chi2 = float((((X @ b) - y) ** 2 * W).sum())
    return b, np.sqrt(np.diag(cov)), chi2


if __name__ == '__main__':
    print('1. geometry of the faces (cells of the face on a diagonal mirror, rim cells = on a coordinate plane, corners)')
    print('   R  c/v    A  mirror  rim  corner  centre      mirror/sqrt(A/6)  rim-periods/sqrt(A/6) [periods: rim/2 (c), rim (v)], per wedge = /6')
    for R, cen in [(27, 'c'), (28, 'v'), (31, 'c'), (32, 'v'), (33, 'c'), (34, 'v'), (35, 'c'), (36, 'v'), (37, 'c'), (38, 'v'),
                   (39, 'c'), (40, 'v'), (41, 'c'), (42, 'v'), (43, 'c'), (44, 'v'), (45, 'c')]:
        g = geometry(R, cen); q = math.sqrt(g['A'] / 6)
        per = g['rim'] / 2 if cen == 'c' else g['rim']
        print(f'  {R:3d}  {cen}  {g["A"]:5d}  {g["mirror"]:5d} {g["rim"]:5d} {g["corner"]:5d}   {g["kind"]:10s} {g["mirror"] / 3 / q:10.3f} {per / 6 / q:16.3f}')
    pool = load()
    print('\n2. pooled ln tau (deaths)')
    C = sorted((A, math.log(e / d), 1 / math.sqrt(d), d) for (A, c), (d, e) in pool.items() if c == 'c' and d >= 10)
    V = sorted((A, math.log(e / d), 1 / math.sqrt(d), d) for (A, c), (d, e) in pool.items() if c == 'v' and d >= 10)
    for name, T in (('cube-centred', C), ('vertex-centred', V)):
        print('  ' + name + ': ' + '; '.join(f'A={a}: {l:.3f}+-{s:.3f} ({d})' for a, l, s, d in T))
    A_, y, s = (np.array(v, float) for v in zip(*[(a, l, e) for a, l, e, d in C]))
    print('\n3. cube-centred fits (A = %d..%d)' % (A_[0], A_[-1]))
    for c in (0.2011, 0.2072, 0.209, 0.2117, 0.2179):
        X = np.stack([np.ones_like(A_), np.sqrt(A_)], 1)
        b, eb, chi2 = wls(X, y - c / 6 * A_, s)
        print(f'  slope pinned c/6, c = {c:.4f}: a = {b[0]:6.3f}, coefficient of sqrt(A) = {b[1]:7.4f} +- {eb[1]:.4f}  chi2 {chi2:.1f}/{len(y) - 2}')
    X = np.stack([np.ones_like(A_), A_], 1); b, eb, chi2 = wls(X, y, s)
    print(f'  a + sA: s = {b[1]:.5f} +- {eb[1]:.5f} (x6 = {6 * b[1]:.4f})  chi2 {chi2:.1f}/{len(y) - 2}')
    X = np.stack([np.ones_like(A_), A_, np.sqrt(A_)], 1); b, eb, chi2 = wls(X, y, s)
    print(f'  a + sA + b sqrt(A): s = {b[1]:.5f} +- {eb[1]:.5f} (x6 = {6 * b[1]:.3f} +- {6 * eb[1]:.3f}), b = {b[2]:.3f} +- {eb[2]:.3f}  chi2 {chi2:.1f}/{len(y) - 3}')
    print('  local slopes x6 (per quotient cell): ' + ', '.join(f'{6 * (y[i + 1] - y[i]) / (A_[i + 1] - A_[i]):.3f}' for i in range(len(y) - 1)))
    print('\n4. vertex minus cube at equal area')
    cd = {a: (l, e) for a, l, e, d in C}; D = [(a, l - cd[a][0], math.hypot(e, cd[a][1])) for a, l, e, d in V if a in cd]
    for a, d, e in D:
        print(f'  A = {a}: {d:+.3f} +- {e:.3f}   per sqrt(A): {d / math.sqrt(a):.4f}')
    a_, d_, e_ = (np.array(v, float) for v in zip(*D))
    for name, X in (('constant', np.ones((len(a_), 1))), ('k sqrt(A)', np.sqrt(a_)[:, None]), ('d0 + k sqrt(A)', np.stack([np.ones_like(a_), np.sqrt(a_)], 1))):
        b, eb, chi2 = wls(X, d_, e_)
        print(f'  {name:16s}: ' + ', '.join(f'{x:.4f} +- {ex:.4f}' for x, ex in zip(b, eb)) + f'  chi2 {chi2:.1f}/{len(a_) - X.shape[1]}')
    print('\n5. residuals of the cube-centred points from a + (0.209/6)A + b sqrt(A), by kind of centre')
    X = np.stack([np.ones_like(A_), np.sqrt(A_)], 1); b, eb, chi2 = wls(X, y - 0.209 / 6 * A_, s)
    for a, l, e in zip(A_, y, s):
        R = int(round((-4 + math.sqrt(16 - 4 * (3 - 8 * a / 3))) / 2))
        print(f'  A = {int(a)} R = {R} {geometry(R, "c")["kind"]:10s} {l - (b[0] + 0.209 / 6 * a + b[1] * math.sqrt(a)):+.3f} +- {e:.3f}')
