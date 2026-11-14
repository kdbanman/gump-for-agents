#!/usr/bin/env python3
"""The thinnest face: gump on the twisted torus (1,1),(0,b), as a one-dimensional system.

Cubes (i, j, k), {111} layer t = i + j + k, in-plane periods (1, 1, -2) and (0, b, -b) (research/shape2: the
class (1,1),(0,b), shortest loop squared 3, face area A = 3b). Every cube of layer t has a unique representative
(0, c, t - c), c = (j - i) mod b: the *site*. A layer is a ring of b sites with three cells each, X_c, Y_c, Z_c
(the +x, +y, +z faces of the cube at site c).

    python3 thin.py table            # the helical neighbour table, derived from docs/AUTOMATON.md's offsets
    python3 thin.py oracle b m G     # reference stepper against reference/oracle.py, every cell, G generations
    python3 thin.py header           # write nbr.h for ring.c / cyl.c from the derived table

The table is *derived* here from the doubled-coordinate offsets (the same construction as reference/oracle.py),
not typed in: `helical()` builds the graph on the quotient and reads off (dt, orientation, dc) for each of the
12 neighbours, checking that the answer does not depend on b, c or t.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def offsets(axis):
    """12 neighbour offsets in doubled coordinates of a face with normal `axis` (docs/AUTOMATON.md section 2)."""
    a = axis
    b, c = [i for i in range(3) if i != a]
    offs = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs


def doubled(t, o, c):
    """Doubled coordinates of the cell (layer t, orientation o, site c): cube (0, c, t - c), face +o."""
    p = [0, 2 * c, 2 * (t - c)]
    p[o] += 1
    return tuple(p)


def site_of(p, b):
    """(t, o, c) of the doubled coordinate p on the quotient by (1,1,-2), (0,b,-b)."""
    o = next(x for x in range(3) if p[x] % 2)
    cube = [(p[x] - (1 if x == o else 0)) // 2 for x in range(3)]
    return sum(cube), o, (cube[1] - cube[0]) % b


def helical(bs=(7, 11, 16)):
    """For each orientation the 12 neighbours as (dt, o2, dc); asserts independence of b, c, t."""
    tab = None
    for b in bs:
        for t in (0, 3):
            for c in range(b):
                cur = []
                for o in range(3):
                    p = doubled(t, o, c)
                    lst = []
                    for off in offsets(o):
                        t2, o2, c2 = site_of(tuple(p[x] + off[x] for x in range(3)), b)
                        dc = (c2 - c) % b
                        if dc > b // 2:
                            dc -= b
                        lst.append((t2 - t, o2, dc))
                    cur.append(sorted(lst))
                if tab is None:
                    tab = cur
                assert cur == tab, (b, t, c)
    return tab


TAB = helical()


def graph(b, m):
    """Cell index (t, o, c) -> t*3*b + o*b + c; neighbour array [n, 12] with -1 outside layers 0..m-1."""
    n = m * 3 * b
    nb = np.full((n, 12), -1, np.int64)
    for t in range(m):
        for o in range(3):
            for c in range(b):
                i = (t * 3 + o) * b + c
                for k, (dt, o2, dc) in enumerate(TAB[o]):
                    if 0 <= t + dt < m:
                        nb[i, k] = ((t + dt) * 3 + o2) * b + (c + dc) % b
    return nb


def step_ref(x, nb):
    """One generation of B45/S345 on a neighbour array; x is a 0/1 vector, cells with index -1 read 0."""
    xx = np.append(x, 0)
    cnt = xx[nb].sum(1)
    return (((x == 0) & ((cnt == 4) | (cnt == 5))) | ((x == 1) & (cnt >= 3) & (cnt <= 5))).astype(np.int8)


def check_simple(b, m=8):
    """True if no cell has a repeated neighbour or itself as neighbour (the torus is a simple graph)."""
    nb = graph(b, m)
    for i, row in enumerate(nb):
        r = [v for v in row if v >= 0]
        if len(set(r)) != len(r) or i in r:
            return False
    return True


def oracle_check(b, m, G, seed=1, p=0.4):
    """Reference stepper against reference/oracle.py on the cubic torus of b^3 cubes, every cell, G generations."""
    sys.path.insert(0, os.path.join(ROOT, 'reference'))
    import oracle
    assert b >= m + 3, 'need three dead layers between the slab and its image'
    H = 2 * b
    rng = np.random.default_rng(seed)
    nb = graph(b, m)
    x = (rng.random(m * 3 * b) < p).astype(np.int8)
    # embedding: cell (t, o, c) and its b copies under (x, x, -2x)
    coords = np.zeros((m * 3 * b, b, 3), np.int64)
    for t in range(m):
        for o in range(3):
            for c in range(b):
                i = (t * 3 + o) * b + c
                p0 = doubled(t, o, c)
                for s in range(b):
                    coords[i, s] = [(p0[0] + 2 * s) % H, (p0[1] + 2 * s) % H, (p0[2] - 4 * s) % H]
    flat = coords.reshape(-1, 3)
    assert len({tuple(q) for q in flat}) == len(flat), 'copies overlap'
    h = np.zeros((H, H, H), np.int8)
    msk = oracle.masks(H)

    def put(x):
        h[:] = 0
        v = np.repeat(x, b)
        h[flat[:, 0], flat[:, 1], flat[:, 2]] = v
    put(x)
    tot = int(h.sum())
    assert tot == b * int(x.sum())
    pops = []
    for g in range(G):
        h = oracle.step(h, msk)
        x = step_ref(x, nb)
        got = h[coords[:, :, 0], coords[:, :, 1], coords[:, :, 2]]
        if not (got == x[:, None]).all() or int(h.sum()) != b * int(x.sum()):
            print(f'oracle_check b={b} m={m}: MISMATCH at generation {g + 1}')
            return False
        pops.append(int(x.sum()))
    print(f'oracle_check b={b} m={m}: {G} generations, every cell of every copy equal, nothing live outside; '
          f'populations {pops[:3]} .. {pops[-1]}, {len(set(pops))} distinct')
    return True


def write_header():
    names = 'XYZ'
    with open(os.path.join(HERE, 'nbr.h'), 'w') as f:
        f.write('/* generated by thin.py header from docs/AUTOMATON.md offsets: for orientation o, the 12 neighbours\n'
                '   (dt, o2, dc): layer t + dt, orientation o2, site c + dc. Do not edit. */\n')
        f.write('static const int NBR[3][12][3] = {\n')
        for o in range(3):
            f.write('  { ' + ', '.join('{%d,%d,%d}' % e for e in TAB[o]) + ' },\n')
        f.write('};\n')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if cmd == 'table':
        for o in range(3):
            print('XYZ'[o], ' '.join(f'{"XYZ"[o2]}(t{dt:+d},c{dc:+d})' for dt, o2, dc in TAB[o]))
        print('simple graph for b = 3..8:', [check_simple(b) for b in range(3, 9)])
    elif cmd == 'oracle':
        b, m, G = map(int, sys.argv[2:5])
        ok = oracle_check(b, m, G)
        sys.exit(0 if ok else 1)
    elif cmd == 'header':
        write_header()
        print('wrote nbr.h')
