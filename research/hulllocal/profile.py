#!/usr/bin/env python3
"""The hull face cell by cell: density of each orbit of face cells (under the face's C3v), pooled over the 8 faces,
against a wrapped face's density measured by the same code; rim excess per unit of rim length.

  python3 research/hulllocal/profile.py RHO_W hull15_s1 [hull13_s2 ...]

Orbit label of a face-layer cell of face f: (e1, e2, e3 | v1, v2, v3), the sorted depths of the cell below the 3
faces sharing an edge with f (normals with dot product +1 with f's) and below the 3 sharing only a corner (-1).
r = min of all six (0 = the cell is also in a second face's layer). "Edge" cells: r_e = min(e) <= 2 and
min(e2, v1) >= 5 (far from the corners); "corner" region: the rest of r <= 4.
Rim excess  E = sum over the face's cells of (rho_cell - RHO_W), per face; per unit rim: E / (3 R) (the face has
3 R cells at r = 0, R cells on each edge).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hl  # noqa: E402

FN = np.array([hl.DIAGS[f // 2] * (1 if f % 2 == 0 else -1) for f in range(8)])


def orbits(v):
    lab = {}
    for f in range(8):
        dots = FN @ FN[f]
        E = [e for e in range(8) if dots[e] == 1]
        V = [e for e in range(8) if dots[e] == -1 and e != f ^ 1]
        assert len(E) == 3 and len(V) == 3
        for i in v.faces[f]:
            key = (tuple(sorted(v.depth[i, E])), tuple(sorted(v.depth[i, V])))
            lab.setdefault(key, []).append(i)
    return {k: np.array(c) for k, c in sorted(lab.items())}


def main(rho_w, tags):
    for tag in tags:
        z = np.load(os.path.join(hl.SCR, tag + '.npz'))
        v = hl.vessel(str(z['name']))
        R = v.R
        live = z['live'].sum(1); expo = z['expo'].sum(1)[:, 0]          # blocks
        rho = live / expo[:, None]                                          # (blocks, n)
        ob = orbits(v)
        print(f'== {tag}: hull R = {R}, A = {len(v.faces[0])}; wrapped reference {rho_w}')
        print(f'   {"edge depths | corner depths":<34}{"r":>3}{"cells/face":>11}{"rho":>11}{"± ":>9}{"rho - rho_w":>13}')
        tot = np.zeros(rho.shape[0]); edge = np.zeros(rho.shape[0]); corner = np.zeros(rho.shape[0]); inter = []
        nint = 0
        for k, c in ob.items():
            r = min(k[0][0], k[1][0])
            per = rho[:, c].mean(1)
            m, s = per.mean(), per.std(ddof=1) / np.sqrt(len(per))
            nf = len(c) // 8
            ex = (rho[:, c] - rho_w).sum(1) / 8                              # per face, per block
            tot += ex
            if r >= 3:
                inter.append(ex); nint += nf
            elif min(k[0][1], k[1][0]) >= 5:
                edge += ex
            else:
                corner += ex
            print(f'   {str(k):<34}{r:>3}{nf:>11}{m:>11.6f}{s:>9.6f}{m - rho_w:>+13.6f}')
        f = lambda a: f'{a.mean():+.4f} ± {a.std(ddof=1) / np.sqrt(len(a)):.4f}'
        ia = np.sum(inter, 0)
        print(f'   per face: total excess {f(tot)} cells; interior (r >= 3, {nint} cells) {f(ia)}; '
              f'edge region (r <= 2, away from corners) {f(edge)}; corner regions {f(corner)}')
        print(f'   per unit rim (3R = {3 * R}): total {f(tot / (3 * R))}; edge region {f(edge / (3 * R))}; '
              f'edge region per cell of edge row away from corners counted from the edge orbits')


if __name__ == '__main__':
    main(float(sys.argv[1]), sys.argv[2:])
