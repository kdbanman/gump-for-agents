"""Critic's lab, part 3: gump (B45/S345 on the faces of the cubic honeycomb) on small vessels, exactly.

Cells: doubled coordinates p in Z^3 with exactly one odd coordinate (docs/AUTOMATON.md section 1-2).
Vessels:
  hull(R, centre)      diagonal hull |d.(p - c)| <= R for the four body diagonals d;
                       centre 'c' (cube centre, c = 0, R odd) or 'v' (vertex, c = (1,1,1), R even)
  slab_patch(...)      not built yet; ask
Faces of a hull: for each signed diagonal d (8 of them) the cells with d.(p - c) = R.

  python3 gump_lab.py selftest      stepper vs research/theory/check_threshold.py (set stepper, open lattice) and
                                    vs reference/oracle.py (numpy, torus); T1; hull and face sizes
  python3 gump_lab.py sizes         cells and face areas of small hulls
  python3 gump_lab.py census R c|v  exhaustive fate of every state of a hull with <= 26 cells
"""
import os, sys, itertools, importlib.util
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact

B, S = (4, 5), (3, 4, 5)
DIAG = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
SDIAG = DIAG + [tuple(-v for v in d) for d in DIAG]


def axis(p):
    return 0 if p[0] & 1 else (1 if p[1] & 1 else 2)


def offsets(a):
    """12 neighbour offsets of a face with normal axis a, built from the text of AUTOMATON.md section 2."""
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):                 # coplanar, touching at a corner
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):             # perpendicular, sharing an edge
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


OFF = [offsets(a) for a in range(3)]


def is_cell(p):
    return sum(v & 1 for v in p) == 1


def hull(R, centre='c'):
    c = (0, 0, 0) if centre == 'c' else (1, 1, 1)
    assert (R % 2 == 1) == (centre == 'c'), "cube-centred hulls have odd R, vertex-centred even R"
    cells = []
    rng = range(-R - 2, R + 4)
    for p in itertools.product(rng, repeat=3):
        if is_cell(p) and all(abs(sum(d[i] * (p[i] - c[i]) for i in range(3))) <= R for d in DIAG):
            cells.append(p)
    return sorted(cells), c


def nbrs(cells):
    idx = {p: i for i, p in enumerate(cells)}
    nb = []
    for p in cells:
        v = []
        for o in OFF[axis(p)]:
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            if q in idx:
                v.append(idx[q])
        nb.append(v)
    return nb


def faces(cells, c, R):
    """dict signed diagonal -> list of cell indices in the outer layer d.(p - c) = R."""
    out = {}
    for d in SDIAG:
        out[d] = [i for i, p in enumerate(cells) if sum(d[k] * (p[k] - c[k]) for k in range(3)) == R]
    return out


def step_set(Sset):
    """Open-lattice set stepper (own code)."""
    cnt = {}
    for p in Sset:
        for o in OFF[axis(p)]:
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            cnt[q] = cnt.get(q, 0) + 1
    return frozenset(q for q, k in cnt.items() if k in (4, 5) or (k == 3 and q in Sset))


def _load(path, name, cut=None):
    src = open(path).read()
    if cut:
        src = src[:src.index(cut)]
    ns = {'__name__': name}
    exec(compile(src, path, 'exec'), ns)
    return ns


def sizes():
    for R, ce in [(1, 'c'), (2, 'v'), (3, 'c'), (4, 'v'), (5, 'c'), (6, 'v'), (7, 'c'), (9, 'c'), (11, 'c'), (13, 'c'), (15, 'c'), (17, 'c')]:
        cells, c = hull(R, ce)
        f = faces(cells, c, R)
        areas = sorted(set(len(v) for v in f.values()))
        nb = nbrs(cells)
        # in-vessel neighbour counts of a face cell
        fc = f[(1, 1, 1)]
        deg = sorted(set(len(nb[i]) for i in fc))
        print(f"hull R={R}{ce}: {len(cells)} cells, face area(s) {areas}, in-vessel degree of face cells {deg}")


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(here, '..', '..', '..', '..', '..'))
    ok = True
    # 0. T1: layer histogram 1,2,6,2,1 for every orientation and signed diagonal
    for a in range(3):
        for d in SDIAG:
            h = {}
            for o in OFF[a]:
                s = sum(d[i] * o[i] for i in range(3)); h[s] = h.get(s, 0) + 1
            if h != {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1}:
                ok = False; print('T1 FAILS', a, d, h)
    print('T1 layer histogram 1,2,6,2,1 for 3 orientations x 8 diagonals:', 'ok' if ok else 'FAILED')
    # 1. vs check_threshold.py's set stepper (open lattice), soups inside hulls: must stay inside (T2) and agree
    ct = _load(os.path.join(root, 'research', 'theory', 'check_threshold.py'), 'ct', cut="if __name__")
    import random
    ok1 = True
    for R, ce in [(5, 'c'), (7, 'c'), (6, 'v')]:
        cells, c = hull(R, ce)
        cs = set(cells)
        nb = nbrs(cells)
        for seed in range(6):
            rng = random.Random(100 * R + seed)
            rho = rng.choice((0.3, 0.4, 0.5))
            Sx = frozenset(p for p in cells if rng.random() < rho)
            Sy = Sx
            x = np.array([1 if p in Sx else 0 for p in cells], np.uint8)
            for t in range(120):
                Sx = step_set(Sx)
                Sy, _ = ct['step'](Sy)
                # vessel stepper by neighbour lists
                n = np.array([sum(int(x[j]) for j in v) for v in nb])
                x = np.where(x == 1, (n >= 3) & (n <= 5), (n >= 4) & (n <= 5)).astype(np.uint8)
                Sz = frozenset(p for p, b in zip(cells, x) if b)
                if not (Sx == Sy == Sz) or not Sx <= cs:
                    ok1 = False; print('MISMATCH', R, ce, seed, t); break
    print('vessel stepper = own set stepper = check_threshold.py stepper, 18 soups x 120 generations in hulls R=5c,7c,6v '
          '(and nothing leaves the hull):', 'identical' if ok1 else 'FAILED')
    # 2. vs reference/oracle.py on a torus large enough not to wrap (H even)
    orc = _load(os.path.join(root, 'reference', 'oracle.py'), 'orc', cut="def fill_box")
    ok2 = True
    H = 24; m = orc['masks'](H)
    cells, c = hull(7, 'c')
    for seed in range(3):
        rng = random.Random(seed)
        Sx = frozenset(p for p in cells if rng.random() < 0.45)
        h = np.zeros((H, H, H), np.int8)
        for p in Sx:
            h[p[0] + 12, p[1] + 12, p[2] + 12] = 1
        for t in range(60):
            Sx = step_set(Sx)
            h = orc['step'](h, m)
            got = frozenset((int(a) - 12, int(b) - 12, int(cc) - 12) for a, b, cc in zip(*np.nonzero(h)))
            if got != Sx:
                ok2 = False; print('MISMATCH oracle', seed, t); break
    print('own set stepper vs reference/oracle.py step (torus H=24, hull R=7 soups), 3 soups x 60 generations:',
          'identical' if ok2 else 'FAILED')
    # 3. full_map vs step_state vs the set stepper on the smallest hulls (random sample of states)
    ok3 = True
    for R, ce in [(1, 'c'), (2, 'v'), (3, 'c')]:
        cells, c = hull(R, ce)
        N = len(cells)
        if N > 24:
            continue
        nb = nbrs(cells)
        F = exact.full_map(nb, B, S)
        rng = random.Random(7)
        sample = range(1 << N) if N <= 12 else [rng.randrange(1 << N) for _ in range(3000)]
        for s in sample:
            Sx = frozenset(cells[i] for i in range(N) if (s >> i) & 1)
            Sn = step_set(Sx)
            t = sum(1 << i for i, p in enumerate(cells) if p in Sn)
            if t != int(F[s]) or exact.step_state(nb, B, S, s) != t or not Sn <= set(cells):
                ok3 = False; print('MISMATCH full_map', R, ce, s); break
        print(f'  full_map on hull R={R}{ce} ({N} cells) vs set stepper:', 'identical' if ok3 else 'FAILED')
    # 4. sizes used in the problem statement
    want = {7: 30, 9: 45, 11: 63, 13: 84}
    ok4 = True
    for R, A in want.items():
        cells, c = hull(R, 'c')
        f = faces(cells, c, R)
        if set(len(v) for v in f.values()) != {A}:
            ok4 = False
    cells9, _ = hull(9, 'c')
    print('face areas of cube-centred hulls R=7,9,11,13 are 30,45,63,84:', 'ok' if ok4 else 'FAILED',
          f'; hull R=9 has {len(cells9)} cells')
    allok = ok and ok1 and ok2 and ok3 and ok4
    print('ALL OK' if allok else 'FAILED')
    return allok


def census(R, ce):
    cells, c = hull(R, ce)
    N = len(cells)
    nb = nbrs(cells)
    F = exact.full_map(nb, B, S)
    f = faces(cells, c, R)
    living = np.ones(1 << N, bool)
    for d, v in f.items():
        living &= exact.any_alive(N, v)
    T = exact.death_times(F, living)
    cyc = exact.cyclic(F)
    imm = T < 0
    mort = T[T > 0]
    print(f"hull R={R}{ce}: N={N}, face areas {sorted(set(len(v) for v in f.values()))}")
    print(f"  some face empty at t=0: {int((T == 0).sum())}; mortal: {len(mort)}, max death time "
          f"{mort.max() if len(mort) else 0}; immortal basin {int(imm.sum())}")
    print(f"  cyclic states {int(cyc.sum())} by period {exact.periods(F, cyc)}")
    print(f"  death-time histogram: {np.bincount(T[T >= 0]).tolist()}")


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'selftest':
        sys.exit(0 if selftest() else 1)
    elif len(sys.argv) >= 2 and sys.argv[1] == 'sizes':
        sizes()
    elif len(sys.argv) == 4 and sys.argv[1] == 'census':
        census(int(sys.argv[2]), sys.argv[3])
    else:
        print(__doc__)
