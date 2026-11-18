#!/usr/bin/env python3
"""Exact live-neighbour budgets of face cells near rims and corners (pure geometry, T1's layer histogram applied
to two or more diagonals at once).   python3 research/blast/rim/budget.py
For each class of face cell: neighbours inside the vessel (the most that can ever be alive), of which in the
cell's own face layer / one layer beneath / two beneath, and how many of the inside neighbours lie in the
NEIGHBOURING face's layer (cells that belong to the other face)."""
import numpy as np, vessel, collections


def table(V, f, label, rowkey):
    h, idx = V.faces[f]; d, C = V.hs[h]
    other = [(hh, dd, CC) for hh, (dd, CC) in enumerate(V.hs) if hh != h]
    out = collections.OrderedDict()
    for i in idx:
        p = V.cells[i]; nbs = [j for j in V.nb[i] if j >= 0]
        dep = [int((C - V.cells[j] @ d) // 2) for j in nbs]
        inother = sum(1 for j in nbs if any(V.cells[j] @ dd == CC for _, dd, CC in other))
        k = (rowkey(p), len(nbs), dep.count(0), dep.count(1), dep.count(2), inother)
        out[k] = out.get(k, 0) + 1
    print(label)
    print('   row/class            inside  in-layer  1 beneath  2 beneath  in another face layer   cells')
    for k, c in sorted(out.items(), key=lambda kv: str(kv[0][0])):
        print(f'   {str(k[0]):20s} {k[1]:5d} {k[2]:8d} {k[3]:9d} {k[4]:9d} {k[5]:12d} {c:15d}')


if __name__ == '__main__':
    V = vessel.prism(8, 8, 6, 0); h, idx = V.faces[0]
    D2 = np.array(vessel.D2)
    def rk(p):
        s2 = int(p @ D2); r_obt = (15 - s2) // 2; r_sharp = (s2 - 1) // 2
        kind = 'dense' if (p[2] % 2 == 0) else 'sparse'
        return f'obt{r_obt}' + kind if r_obt <= 3 else f'sharp{r_sharp}' + kind
    table(V, 0, 'prism(8,8,6,0), face d1+ (obtuse rim row dense, sharp rim row sparse); row index from the nearer rim', rk)
    V = vessel.prism(8, 8, 6, 1)
    def rk1(p):
        s2 = int(p @ D2); r_obt = (17 - s2) // 2; r_sharp = (s2 - 3) // 2
        kind = 'dense' if (p[2] % 2 == 0) else 'sparse'
        return f'obt{r_obt}' + kind if r_obt <= 3 else f'sharp{r_sharp}' + kind
    table(V, 0, 'prism(8,8,6,1), face d1+ (obtuse rim row sparse, sharp rim row dense)', rk1)
    R = 11; V = vessel.hull(R)
    def rkh(p):
        q = np.sort(np.abs(p))  # face (1,1,1): x,y,z >= 0; depth below the 3 edge-adjacent faces = the coordinates
        return 'r=' + str(tuple(int(v) for v in np.sort(p)[:2]))
    hh = [k for k, (d, C) in enumerate(V.hs) if tuple(d) == (1, 1, 1)][0]
    f = [k for k, (h_, _) in enumerate(V.faces) if h_ == hh][0]
    table(V, f, 'hull R = 11, face (1,1,1): class = the two smallest coordinates (0 = on an edge; (0,0) = the corner cell)', rkh)
