#!/usr/bin/env python3
"""Geometry of a rhombic patch of a {111} face layer: cells, boundary cells and cut in-layer bonds.

A patch a x b is the 3ab face cells of the cube columns (i, j), 0 <= i < a, 0 <= j < b, of one layer.  In-layer
neighbours (6 per cell) from docs/AUTOMATON.md section 2, restricted to one layer s = 2(i + j + k) + 1:
  X(i,j): X(i,j+1) X(i,j-1) Y(i,j) Y(i+1,j-1) Z(i,j) Z(i+1,j)
  Y(i,j): Y(i+1,j) Y(i-1,j) Z(i,j) Z(i,j+1)   X(i,j) X(i-1,j+1)
  Z(i,j): Z(i+1,j-1) Z(i-1,j+1) X(i,j) X(i-1,j) Y(i,j) Y(i,j-1)
(checked below against the cube-index table by brute force).  Used only to convert the forecast for sigma in
PREDICTIONS.md between the possible definitions of "perimeter".

    python3 research/constant/patch_geom.py
"""
NB = {
    'X': [('X', 0, 1), ('X', 0, -1), ('Y', 0, 0), ('Y', 1, -1), ('Z', 0, 0), ('Z', 1, 0)],
    'Y': [('Y', 1, 0), ('Y', -1, 0), ('Z', 0, 0), ('Z', 0, 1), ('X', 0, 0), ('X', -1, 1)],
    'Z': [('Z', 1, -1), ('Z', -1, 1), ('X', 0, 0), ('X', -1, 0), ('Y', 0, 0), ('Y', 0, -1)],
}


def check_table():
    """In-layer neighbours from the doubled-coordinate offsets of AUTOMATON.md, independent of the table above."""
    ax = {'X': 0, 'Y': 1, 'Z': 2}
    name = 'XYZ'
    ok = True
    for t, a in ax.items():
        b, c = (a + 1) % 3, (a + 2) % 3
        offs = []
        for sb in (2, -2):
            for sc in (2, -2):
                o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
        for sa in (1, -1):
            for other in (b, c):
                for so in (1, -1):
                    o = [0, 0, 0]; o[a] = sa; o[other] = so; offs.append(tuple(o))
        assert len(offs) == 12
        p = [0, 0, 0]; p[a] = 1                       # the face X[0,0,0] etc. in doubled coordinates
        mine = set()
        for o in offs:
            if sum(o) != 0:
                continue                              # another layer
            q = [p[i] + o[i] for i in range(3)]
            odd = [i for i in range(3) if q[i] % 2]
            assert len(odd) == 1
            cube = [(q[i] - (1 if i == odd[0] else 0)) // 2 for i in range(3)]
            mine.add((name[odd[0]], cube[0], cube[1]))
        ok = ok and mine == set(NB[t]) and len(mine) == 6
    return ok


def patch(a, b):
    cells = {(t, i, j) for t in 'XYZ' for i in range(a) for j in range(b)}
    boundary = 0; cut = 0
    for (t, i, j) in cells:
        out = sum((u, i + di, j + dj) not in cells for u, di, dj in NB[t])
        cut += out; boundary += out > 0
    return len(cells), boundary, cut


if __name__ == '__main__':
    print('in-layer neighbour table agrees with AUTOMATON.md offsets:', check_table())
    print(' a  b  cells  perimeter 2(a+b)  boundary cells  cut in-layer bonds')
    for a, b in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (1, 2), (1, 3), (1, 6), (2, 3), (3, 6)]:
        n, bd, cut = patch(a, b)
        print(f'{a:2d} {b:2d} {n:6d} {2*(a+b):10d} {bd:15d} {cut:15d}')
