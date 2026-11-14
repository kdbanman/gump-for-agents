#!/usr/bin/env python3
"""Audit of the counting line, claim 24 (journal entry 15): the faces of cube-centred and vertex-centred O_h hulls.

  python3 c4_oh_faces.py            (a few seconds)

Everything is listed, nothing is taken from a formula: cells of the face d = (1,1,1) of the hull |x|+|y|+|z| <= R
about a cube centre (R = 2N + 1) or about a vertex (R = 2N + 2); in-layer adjacency from reference/oracle.py's
offsets; orbits under the six permutations of the coordinates about the centre.
"""
import itertools
from collections import Counter
from p0_lib import neighbours, axis_of

T = lambda j: j * (j + 1) // 2


def face(N, centre):
    """Absolute doubled coordinates (exactly one odd). Returns (cells, centre point c0, R)."""
    if centre == 'cube':
        R, c0 = 2 * N + 1, (0, 0, 0)
    else:
        R, c0 = 2 * N + 2, (1, 1, 1)
    cells = []
    for x in range(0, R + 1):
        for y in range(0, R + 1 - x):
            z = R - x - y
            p = (x + c0[0], y + c0[1], z + c0[2])
            if sum(c % 2 for c in p) == 1:
                cells.append(p)
    return cells, c0, R


def analyse(N, centre):
    cells, c0, R = face(N, centre)
    cs = set(cells)
    s = sum(cells[0])
    rel = lambda p: tuple(p[i] - c0[i] for i in range(3))
    # orbits under C3v = permutations of the relative coordinates
    seen, orbits, fixed_by_mirror, fixed_by_rot = set(), 0, 0, 0
    for p in cells:
        r = rel(p)
        if r not in seen:
            orbits += 1
            for perm in itertools.permutations(range(3)):
                seen.add(tuple(r[i] for i in perm))
        fixed_by_mirror += (r[0] == r[1])
        fixed_by_rot += (r[0] == r[1] == r[2])
    kag = hexp = 0
    deg = Counter()
    for p in cells:
        a = axis_of(p)
        d = 0
        for q in neighbours(p):
            if q in cs:
                d += 1
                if q[a] != p[a]:
                    kag += 1                       # perpendicular, shares an edge: kagome bond
                else:
                    hexp += 1                      # coplanar, across a hexagon
        deg[d] += 1
    kag //= 2; hexp //= 2
    e = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    add = lambda p, o, m=1: tuple(p[i] + m * o[i] for i in range(3))
    # top-cube triangles: cube centre q (all even), sum = s - 1, cells q + e_a
    top = Counter(add(p, e[axis_of(p)], -1) for p in cells)
    top_complete = sum(1 for q, c in top.items() if c == 3)
    alone = sum(1 for q, c in top.items() if c == 1)
    two = sum(1 for q, c in top.items() if c == 2)
    # triangles of the other orientation: cube centre u above the layer, cells u - e_a
    oth = Counter(add(p, e[axis_of(p)]) for p in cells)
    oth_complete = sum(1 for q, c in oth.items() if c == 3)
    # hexagons: lattice vertices v (all odd) in the layer plane, cells v + e_a - e_b
    hexc = Counter()
    for p in cells:
        a, b = [i for i in range(3) if i != axis_of(p)]            # the two even coordinates
        for sg in (1, -1):
            v = list(p); v[a] += sg; v[b] -= sg                    # p = v -+ (e_a - e_b)
            v = tuple(v)
            assert all(c % 2 == 1 for c in v) and sum(v) == s
            hexc[v] += 1
    hex_complete = sum(1 for v, c in hexc.items() if c == 6)
    shared = sum(1 for p in cells if rel(p)[2] == 0)
    return dict(R=R, A=len(cells), orbits=orbits, mirror_fixed=fixed_by_mirror, rot_fixed=fixed_by_rot, kagome=kag, hexpairs=hexp,
                top3=top_complete, top2=two, top1=alone, other3=oth_complete, hexagons=hex_complete, shared=shared,
                deg=dict(sorted(deg.items())))


def main():
    print("  N  centre   R    A  orbits  m  kagome  hexpairs  top-cube triangles (3/2/1 cells)  other triangles  hexagons  shared  degrees")
    ok = True
    for N in range(1, 10):
        rc, rv = analyse(N, 'cube'), analyse(N, 'vertex')
        for nm, r in (('cube', rc), ('vertex', rv)):
            print(f"  {N}  {nm:6s} {r['R']:3d} {r['A']:4d}  {r['orbits']:4d}  {r['mirror_fixed']:2d}  {r['kagome']:5d}  {r['hexpairs']:6d}"
                  f"      {r['top3']:3d}/{r['top2']}/{r['top1']:<3d}                    {r['other3']:4d}           {r['hexagons']:4d}"
                  f"     {r['shared']:3d}    {r['deg']}")
        m = N // 2 + 1
        A = 3 * T(N + 1)
        chk = [
            rc['A'] == rv['A'] == A,
            rc['rot_fixed'] == rv['rot_fixed'] == 0,
            rc['mirror_fixed'] == rv['mirror_fixed'] == m,
            rc['orbits'] == rv['orbits'] == (A + 3 * m) // 6 and (A + 3 * m) % 6 == 0,
            rc['kagome'] == rv['kagome'] == 3 * (N + 1) ** 2,
            rc['hexpairs'] == rv['hexpairs'] == 3 * T(N),
            (rc['top3'], rc['top2'], rc['top1']) == (T(N + 1), 0, 0),
            rc['other3'] == T(N - 1), rc['hexagons'] == T(N), rc['deg'].get(2, 0) == 3,
            rv['other3'] == T(N + 1), (rv['top3'], rv['top2'], rv['top1']) == (T(N), 0, 3 * (N + 1)), rv['hexagons'] == T(N - 1),
            rc['shared'] == 2 * (N + 1), rv['shared'] == N + 1,
        ]
        ok &= all(chk)
        if not all(chk):
            print("    MISMATCH with entry 15:", chk)
    print(f"\nentry 15 for N = 1..9: A = 3T(N+1) in both; no cell on the axis; m = floor(N/2)+1 cells on each mirror; (A+3m)/6 orbits;")
    print(f"3(N+1)^2 kagome bonds and 3T(N) pairs across hexagons in both; cube-centred: T(N+1) top-cube triangles, T(N-1) of the")
    print(f"other orientation, T(N) hexagons, 3 cells of degree 2; vertex-centred: T(N+1) of the other orientation, T(N) top-cube")
    print(f"triangles, T(N-1) hexagons, 3(N+1) cells alone in their top cube; shared with one neighbouring face 2(N+1) / N+1: {ok}")
    assert ok
    r35, r36 = analyse(17, 'cube'), analyse(17, 'vertex')
    print(f"R = 35: A = {r35['A']}, orbits {r35['orbits']};  R = 36: A = {r36['A']}, orbits {r36['orbits']}   (journal: 513, 90)")
    assert (r35['A'], r35['orbits'], r36['A'], r36['orbits']) == (513, 90, 513, 90)
    r1c, r1v = analyse(1, 'cube'), analyse(1, 'vertex')
    print(f"N = 1: degrees cube-centred {r1c['deg']} (journal 4^6 2^3), vertex-centred {r1v['deg']} (journal 4^3 3^6); "
          f"bonds {r1c['kagome']}, {r1v['kagome']}; hexagon pairs {r1c['hexpairs']}, {r1v['hexpairs']}")
    assert r1c['deg'] == {2: 3, 4: 6} and r1v['deg'] == {3: 6, 4: 3}
    print("all assertions passed")


if __name__ == "__main__":
    main()
