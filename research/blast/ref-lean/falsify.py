#!/usr/bin/env python3
"""Referee's falsification tests for the Lean statements of research/blast/lean (REVIEW.md, section 2).

    python3 research/blast/ref-lean/falsify.py [TEST ...]      (all tests if none named; about a minute)

Written from reference/oracle.py alone (offsets, masks, step), not from the Lean proofs. Where a Lean
*definition* might differ from the informal one, it is transcribed literally (functions named lean_*), and
both readings are tested. Every test prints PASS/FAIL lines and what it measured; the exit status is 1 if any
FAIL was printed.
"""
import itertools, json, math, os, random, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

FAILS = []


def report(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg, flush=True)
    if not ok:
        FAILS.append(msg)


# ------------------------------------------------------------------ the rule, from the oracle

OFFS = {a: [tuple(o) for o in oracle.offsets(a)] for a in range(3)}


def add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def dot(u, p):
    return u[0] * p[0] + u[1] * p[1] + u[2] * p[2]


def is_cell(p):                       # oracle.masks: coordinate a odd, the other two even
    return sum(c % 2 for c in p) == 1


def axis(p):
    return [i for i in range(3) if p[i] % 2][0]


def nbrs(p):
    return [add(p, o) for o in OFFS[axis(p)]]


DIAGS = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


# ------------------------------------------------------------------ literal transcriptions of Gump/Basic.lean

def lean_offsets():
    src = open(os.path.join(ROOT, 'research', 'blast', 'lean', 'Gump', 'Basic.lean'), encoding='utf-8').read()
    block = src[src.index('def offsets'):src.index('/-- The twelve neighbours of a cell')]
    parts = re.split(r'\|\s*\.(X|Y|Z)\s*=>', block)
    return {'XYZ'.index(n): [tuple(map(int, t)) for t in re.findall(r'⟨\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*⟩', b)]
            for n, b in zip(parts[1::2], parts[2::2])}


LOFFS = lean_offsets()


def lean_isCell(p):                   # Pt.isCell, with Int.emod (Python % agrees for the divisor 2)
    x, y, z = p
    return ((x % 2 != 0 and y % 2 == 0 and z % 2 == 0) or (x % 2 == 0 and y % 2 != 0 and z % 2 == 0)
            or (x % 2 == 0 and y % 2 == 0 and z % 2 != 0))


def lean_axis(p):                     # Pt.axis: X if x odd, else Y if y odd, else Z (also for non-cells)
    return 0 if p[0] % 2 != 0 else (1 if p[1] % 2 != 0 else 2)


def lean_nbrs(p):
    return [add(p, o) for o in LOFFS[lean_axis(p)]]


# ------------------------------------------------------------------ the oracle on a padded box

def to_array(cells, H, shift):
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[tuple(np.array(c) + shift)] = 1
    return h


def from_array(h, shift):
    return {tuple(int(v) for v in x) for x in np.argwhere(h == 1) - shift}


class Box:
    """A finite seed run by oracle.step in an even-H array big enough that the torus never matters (T2:
    the seed's diagonal hull, L1 radius R about an even centre, bounds every generation)."""

    def __init__(self, cells, margin=6):
        c = np.array(sorted(cells))
        lo, hi = c.min(0), c.max(0)
        self.centre = tuple(int(v) for v in ((lo + hi) // 2) & ~1)
        R = int(np.abs(c - self.centre).sum(1).max())
        H = 2 * R + 2 * margin
        H += H % 2
        self.H, self.R = H, R
        self.shift = np.array([((H // 2) & ~1) - v for v in self.centre])   # even: keeps every parity, so oracle.masks applies
        self.m = oracle.masks(H)
        self.h = to_array(cells, H, self.shift)

    def step(self):
        self.h = oracle.step(self.h, self.m)
        live = np.argwhere(self.h == 1)
        if len(live):
            assert live.min() >= 2 and live.max() <= self.H - 3, 'pattern reached the array edge'
        return self.cells()

    def cells(self):
        return from_array(self.h, self.shift)


def soup(rng, half, dens, centre=(0, 0, 0), shape=None):
    hx, hy, hz = shape or (half, half, half)
    out = set()
    for x in range(-hx, hx + 1):
        for y in range(-hy, hy + 1):
            for z in range(-hz, hz + 1):
                p = add(centre, (x, y, z))
                if is_cell(p) and rng.random() < dens:
                    out.add(p)
    return out


def catalogue():
    return [json.loads(l) for l in open(os.path.join(ROOT, 'research', 'atlas', 'catalogue.jsonl'))]


# ================================================================== tests

def test_nbrs():
    """nbrs_isCell, nbrs_symm, nbrs_not_symm_off_cells, offsets equal, mem_offsets_iff, layer_histogram, and
    the oracle's np.roll direction (cnt[p] = h[p + o])."""
    report(all(sorted(LOFFS[a]) == sorted(OFFS[a]) for a in range(3)), 'Basic.lean offsets = oracle.offsets as sets')
    pts = list(itertools.product(range(-7, 8), repeat=3))
    cells = [p for p in pts if is_cell(p)]
    report(all(lean_isCell(p) == is_cell(p) for p in pts), f'Pt.isCell = oracle mask on {len(pts)} points of [-7,7]^3')
    report(all(lean_axis(p) == axis(p) for p in cells), 'Pt.axis = the odd coordinate on every cell of [-7,7]^3')
    report(all(is_cell(q) for p in cells for q in nbrs(p)), f'nbrs_isCell on {len(cells)} cells of [-7,7]^3')
    report(all(len(set(nbrs(p))) == 12 for p in cells), 'twelve distinct neighbours')
    report(all((q in nbrs(p)) == (p in nbrs(q)) for p in cells for q in cells
               if max(abs(p[i] - q[i]) for i in range(3)) <= 2), 'nbrs_symm on all cell pairs within max-norm 2 in [-7,7]^3')
    report((2, 2, 0) in lean_nbrs((1, 1, 0)) and (1, 1, 0) not in lean_nbrs((2, 2, 0)),
           'nbrs_not_symm_off_cells holds for the literal Lean nbrs')
    # mem_offsets_iff, transcribed, on [-3,3]^3
    def char(a, o):
        b, c = [i for i in range(3) if i != a]
        return ((o[a] == 0 and abs(o[b]) == 2 and abs(o[c]) == 2) or
                (abs(o[a]) == 1 and ((abs(o[b]) == 1 and o[c] == 0) or (o[b] == 0 and abs(o[c]) == 1))))
    report(all((o in OFFS[a]) == char(a, o) for a in range(3) for o in itertools.product(range(-3, 4), repeat=3)),
           'mem_offsets_iff characterisation on [-3,3]^3, three axes')
    hist = all([sum(1 for o in OFFS[a] if dot(d, o) == v) for v in (-4, -2, 0, 2, 4)] == [1, 2, 6, 2, 1]
               for a in range(3) for d in DIAGS)
    report(hist, 'T1 layer histogram 1,2,6,2,1 for 3 axes x 8 diagonals')
    # np.roll direction: one live cell q; the cells p whose count is 1 are exactly {p : q in nbrs(p)}
    H = 12; m = oracle.masks(H); ok = True
    for q in [(5, 6, 6), (6, 5, 6), (6, 6, 5)]:
        h = np.zeros((H, H, H), np.int8); h[q] = 1
        for a in range(3):
            cnt = sum(np.roll(h, tuple(-d for d in o), axis=(0, 1, 2)) for o in oracle.offsets(a))
            got = {tuple(int(v) for v in x) for x in np.argwhere((cnt == 1) & m[a])}
            want = {p for p in itertools.product(range(H), repeat=3) if is_cell(p) and axis(p) == a and q in nbrs(p)}
            ok &= got == want
    report(ok, 'oracle.step counts h[p + o] over offsets(axis(p)) (np.roll direction), so nbrs(p) = p + offsets')


def kag_nbrs(d, p):                   # ThickHex.kagNbrs: same layer, other orientation
    return [q for q in nbrs(p) if dot(d, q) == dot(d, p) and axis(q) != axis(p)]


def layer_nbrs(d, p):
    return [q for q in nbrs(p) if dot(d, q) == dot(d, p)]


def sealed_in_layer(S, d):
    s = dot(d, next(iter(S)))
    return all(dot(d, p) == s for p in S) and \
        all(sum(1 for q in layer_nbrs(d, p) if q not in S) <= 3 for p in S)


def minimal_layer_sealed(d, start, kmax):
    """Every set sealed in the layer of `start` that contains `start` and has at most kmax cells contains one of
    the sets returned (complete branching on a violating cell)."""
    found = set()

    def rec(S):
        bad = None
        for p in sorted(S):
            inside = sum(1 for q in layer_nbrs(d, p) if q in S)
            if inside < 3:
                bad = p; break
        if bad is None:
            found.add(frozenset(S)); return
        if len(S) >= kmax:
            return
        for q in layer_nbrs(d, bad):
            if q not in S:
                rec(S | {q})
    rec({start})
    return found


def closed_kag_walks(d, start):
    out = set()

    def rec(path):
        if len(path) == 6:
            if start in kag_nbrs(d, path[-1]):
                out.add(frozenset(path))
            return
        for q in kag_nbrs(d, path[-1]):
            if q not in path:
                rec(path + [q])
    rec([start])
    return out


def test_layer():
    """layer_sealed_six, layer_no_sealed_le_five, hexagon_sealed, halfPlane_sealed; Theorem 4 (ii) by the oracle."""
    ok_min = ok_hex = ok_walk = True; n6 = 0; nwalk = 0; sizes = set()
    for d in [(1, 1, 1), (1, -1, 1), (-1, -1, 1)]:
        for s in (1, -1, 3, -5):
            for a in range(3):
                # a cell of axis a in layer s
                start = next(p for p in itertools.product(range(-6, 7), repeat=3)
                             if is_cell(p) and axis(p) == a and dot(d, p) == s)
                sets = minimal_layer_sealed(d, start, 7)
                sizes |= {len(S) for S in sets}
                ok_min &= all(len(S) >= 6 for S in sets)
                six = {S for S in sets if len(S) == 6}
                walks = closed_kag_walks(d, start)
                nwalk += len(walks); n6 += len(six)
                ok_hex &= all(sealed_in_layer(W, d) for W in walks)
                ok_walk &= six == walks and len(walks) == 2
    report(ok_min, f'no set sealed in one layer with <= 5 cells (complete search to 7 cells; 3 diagonals x 4 layers x '
           f'3 axes; sizes of the minimal sets found: {sorted(sizes)})')
    report(ok_hex, f'every closed kagome walk of 6 distinct cells is sealed in its layer ({nwalk} walks)')
    report(ok_walk, f'the sealed 6-sets through a cell are exactly its closed kagome 6-walks, two per cell '
           f'(the two hexagons at a kagome vertex): {n6} = {nwalk}')
    # halfPlane_sealed, transcribed: cells of layer s with C < v.p, each with <= 3 layer neighbours outside
    rng = random.Random(1); ok = True; tried = 0
    d = (1, 1, 1)
    layer_cells = [p for p in itertools.product(range(-9, 10), repeat=3) if is_cell(p) and dot(d, p) == 1]
    for _ in range(300):
        v = tuple(rng.randint(-5, 5) for _ in range(3)); C = rng.randint(-6, 6)
        for p in layer_cells:
            if dot(v, p) > C and max(map(abs, p)) <= 7:
                tried += 1
                ok &= sum(1 for q in layer_nbrs(d, p) if dot(v, q) <= C) <= 3
    report(ok, f'halfPlane_sealed: 300 random (v, C), {tried} cells checked')
    # Theorem 4 (ii) as the source states it, by the oracle: a one-layer pattern never leaves the convex hull
    ok = True; gens = 0
    layer_patch = [p for p in itertools.product(range(-10, 11), repeat=3) if is_cell(p) and dot(d, p) == 1]
    for seed in range(120):
        r = random.Random(seed)
        dens = (0.3, 0.45, 0.6)[seed % 3]
        cells = {p for p in layer_patch if r.random() < dens}
        if not cells:
            continue
        box = Box(cells)
        prev = cells
        for t in range(30):
            cur = box.step(); gens += 1
            if not cur:
                break
            ok &= all(in_hull_2d(prev, p) for p in cur)
            prev = cur
    report(ok, f'one layer (oracle): every live cell lies in the convex hull of the previous generation\'s live cells '
           f'(120 soups, {gens} generations)')


def proj2(p):                          # coordinates in the plane x + y + z = const
    return (p[0] - p[1], p[0] + p[1] - 2 * p[2])


def in_hull_2d(S, p):
    pts = sorted(set(proj2(q) for q in S)); x = proj2(p)
    if len(pts) == 1:
        return x == pts[0]
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0: lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0: upper.pop()
        upper.append(q)
    hull = lower[:-1] + upper[:-1]
    if len(hull) == 2:                 # collinear: on the segment
        a, b = hull
        return cross(a, b, x) == 0 and min(a[0], b[0]) <= x[0] <= max(a[0], b[0]) and \
            min(a[1], b[1]) <= x[1] <= max(a[1], b[1])
    return all(cross(hull[i], hull[(i + 1) % len(hull)], x) >= 0 for i in range(len(hull)))


SET36 = None


def lean_set36():
    src = open(os.path.join(ROOT, 'research', 'blast', 'lean', 'Gump', 'ThickSmall.lean'), encoding='utf-8').read()
    block = src[src.index('def set36'):src.index('/-- 36 distinct cells')]
    return [tuple(map(int, t)) for t in re.findall(r'⟨\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*⟩', block)]


def test_set36():
    """set36 against sealed.py's is_sealed and against "one closed 18-cell kagome loop in each layer"."""
    S = lean_set36(); W = set(S); d = (1, 1, 1)
    report(len(S) == 36 and len(W) == 36 and all(is_cell(p) for p in S), 'set36: 36 distinct cells')
    report(sorted(sum(1 for p in S if dot(d, p) == s) for s in (1, 3)) == [18, 18], 'set36: 18 in layer s=1, 18 in s=3')
    slab = lambda q: dot(d, q) in (1, 3)
    report(all(sum(1 for q in nbrs(p) if slab(q) and q not in W) <= 3 for p in W),
           'set36 sealed in the slab 1 <= s <= 3 (own transcription of SealedIn)')
    sys.path.insert(0, os.path.join(ROOT, 'research', 'theory'))
    try:
        import sealed as sealed_py
        same_off = all(sorted(map(tuple, sealed_py.OFF[a])) == sorted(OFFS[a]) for a in range(3))
        report(same_off, 'sealed.py OFF = oracle.offsets')
        report(sealed_py.layer((1, 0, 0)) == 0 and sealed_py.layer((1, 2, 0)) == 1, 'sealed.py layer 0,1 = s 1,3')
        report(sealed_py.is_sealed(W, 2), 'set36 sealed by research/theory/sealed.py is_sealed(W, m=2)')
    except Exception as e:           # noqa: BLE001
        report(False, f'sealed.py could not be loaded: {e}')
    for s in (1, 3):
        L = sorted(p for p in W if dot(d, p) == s)
        adj = {p: [q for q in kag_nbrs(d, p) if q in L] for p in L}
        degs = sorted(len(v) for v in adj.values())
        res = []

        def rec(path, seen):
            if res:
                return
            if len(path) == len(L):
                if L[0] in adj[path[-1]]:
                    res.append(list(path))
                return
            for q in adj[path[-1]]:
                if q not in seen:
                    seen.add(q); path.append(q); rec(path, seen); path.pop(); seen.discard(q)
        rec([L[0]], {L[0]})
        report(bool(res), f'set36 layer s={s}: its 18 cells are one closed kagome walk (a Hamiltonian kagome cycle '
               f'exists; the induced kagome graph is that cycle plus {sum(degs) // 2 - 18} chords, degrees {degs})')


def test_beyond():
    """beyond_sealed_iff for every primitive u with |u_i| <= 6 and C in [-8, 8]; also non-primitive u."""
    R = 16
    cells = [p for p in itertools.product(range(-R, R + 1), repeat=3) if is_cell(p)]
    cells_by_axis = {a: np.array([p for p in cells if axis(p) == a]) for a in range(3)}
    offs = {a: np.array(OFFS[a]) for a in range(3)}
    n = bad = 0; nonprim_bad = 0; nonprim = 0
    for u in itertools.product(range(-6, 7), repeat=3):
        if u == (0, 0, 0):
            continue
        g = math.gcd(math.gcd(abs(u[0]), abs(u[1])), abs(u[2]))
        ua = np.array(u)
        diag = abs(u[0]) == abs(u[1]) == abs(u[2])
        for C in range(-8, 9):
            sealed = True
            for a in range(3):
                P = cells_by_axis[a]
                up = P @ ua
                sel = (up > C) & (up <= C + 30)
                if not sel.any():
                    continue
                vals = np.unique(up[sel])
                ov = offs[a] @ ua
                for v in vals:          # outside count depends only on u.p
                    if np.sum(v + ov <= C) > 3:
                        sealed = False; break
                if not sealed:
                    break
            if g == 1:
                n += 1; bad += sealed != diag
            else:
                nonprim += 1; nonprim_bad += sealed != diag
    report(bad == 0, f'beyond_sealed_iff: {n} (primitive u, C) pairs, |u_i| <= 6, C in [-8,8]: sealed iff |ux|=|uy|=|uz| '
           f'({bad} disagreements)')
    report(nonprim_bad == 0, f'the same for {nonprim} non-primitive (u, C) (not claimed in Lean): {nonprim_bad} disagreements')


# ------------------------------------------------------------------ T5, transcribed from Threshold.lean

def hull_cells(seed):
    C = {d: max(dot(d, p) for p in seed) for d in DIAGS}
    R = max(C.values()) + 2
    out = []
    for p in itertools.product(range(-R, R + 1), repeat=3):
        if is_cell(p) and all(dot(d, p) <= C[d] for d in DIAGS):
            out.append(p)
    return out


def run_states(seed, gens):
    box = Box(seed)
    st = [set(seed)]
    for _ in range(gens):
        st.append(box.step())
    return st


def count(c, p):
    return sum(1 for q in nbrs(p) if q in c)


class T5:
    """F, drive, diss, o1, mism of mathlib/GumpMath/Threshold.lean, transcribed, over a vessel V (a list of
    points holding every live point of the run st[0], st[1], ...)."""

    def __init__(self, V, st):
        self.V, self.st = V, st
        self.cnt = [{p: sum(1 for q in nbrs(p) if q in s) for p in V} for s in st]

    def x(self, u, p):
        return 1 if p in self.st[u] else 0

    def hs(self, u, p):
        return self.cnt[u][p] + self.x(u, p)

    def pair(self, a, b):                         # x(a)^T (A + I) x(b), summed over V
        return sum(self.x(a, p) * (self.cnt[b][p] + self.x(b, p)) for p in self.V)

    def F(self, t):
        return -2 * self.pair(t + 1, t) + 7 * (len(self.st[t + 1]) + len(self.st[t]))

    def drive(self, t):
        return sum(2 * self.hs(t + 1, p) - 7 for p in self.V if self.cnt[t + 1][p] >= 6 and self.x(t, p))

    def diss(self, t):
        return sum(abs(2 * self.hs(t + 1, p) - 7) for p in self.V
                   if self.cnt[t + 1][p] <= 5 and self.x(t + 2, p) != self.x(t, p))

    def o1(self, t):
        return sum(1 for p in self.V if self.cnt[t + 1][p] >= 6 and self.x(t, p))

    def mism(self, t):
        return sum(1 for p in self.V if self.x(t + 2, p) != self.x(t, p))


def t5_quantities(V, st, t, q=None):
    q = q or T5(V, st)
    return q.F(t), q.F(t + 1), q.drive(t), q.diss(t), q.o1(t), q.mism(t), q.pair(t + 1, t) - q.pair(t, t + 1)


def test_t5():
    """energy_identity, energy_bounds, pair_comm, budget, period_two_of_no_O1's bound, oscillator_period_two's
    contrapositive (period >= 3 has O1 events), on random hull runs and catalogue oscillators."""
    rng = random.Random(5)
    ok_id = ok_b = ok_sym = ok_budget = ok_p2 = True; steps = 0; runs = 0; worst_t0 = 0; nontriv = 0; livecg = 0
    for k in range(24):
        half = rng.choice([1, 2, 2, 3]); dens = rng.choice([0.3, 0.45, 0.6, 0.8])
        seed = soup(rng, half, dens)
        if not seed:
            continue
        V = hull_cells(seed); N = len(V); Vset = set(V)
        G = 80
        st = run_states(seed, G + 2)
        assert all(s <= Vset for s in st[1:]) and seed <= Vset, 'hull (T2) violated by the oracle'
        runs += 1; livecg += sum(len(s) for s in st[:G])
        Fs, dr, di, o1s, ms = [], [], [], [], []
        q5 = T5(V, st)
        for t in range(G):
            F0, F1, D, Q, o1, mi, asym = t5_quantities(V, st, t, q5)
            ok_id &= (F1 - F0 == D - Q); ok_b &= (-12 * N <= F0 <= 14 * N); ok_sym &= asym == 0
            Fs.append(F0); dr.append(D); di.append(Q); o1s.append(o1); ms.append(mi); steps += 1
        for _ in range(20):
            T = rng.randrange(G); K = rng.randrange(G - T + 1)
            ok_budget &= sum(ms[T:T + K]) <= 20 * sum(o1s[T:T + K]) + 26 * N
        # period_two_of_no_O1: T = one after the last O1 event (Lean's index: o1 at t counts events at t+1)
        last = max([t for t in range(G) if o1s[t] > 0], default=-1)
        T = last + 1
        p2 = [t for t in range(T, G) if all(st[u + 2] == st[u] for u in range(t, G))]
        if p2:
            t0 = p2[0]; worst_t0 = max(worst_t0, t0 - T); nontriv += last >= 0
            ok_p2 &= t0 <= T + 26 * N
    report(ok_id, f'energy_identity F(t+1)-F(t) = drive - diss at every step ({steps} steps, {runs} hull runs, '
           f'{livecg} live cell-generations)')
    report(ok_b, 'energy_bounds -12N <= F <= 14N at every step')
    report(ok_sym, 'pair_comm: x(t+1)^T W x(t) = x(t)^T W x(t+1)')
    report(ok_budget, 'budget: sum mism <= 20 sum o1 + 26N over 20 random windows per run')
    report(ok_p2, f'period_two_of_no_O1: period <= 2 within 26N of the last O1 event ({nontriv} runs with events; '
           f'largest t0 - T seen {worst_t0})')
    # catalogue oscillators of period >= 3: every one has O1 events in its cycle; drive = diss over a period
    ok_o1 = ok_bal = True; n = 0
    for r in catalogue():
        if r['period'] < 3 or len(r['cells']) > 60 or n >= 40:
            continue
        P = r['period']; seed = {tuple(c) for c in r['cells']}
        st = run_states(seed, 2 * P + 2)
        if st[P] != st[0]:
            report(False, f'catalogue {r["id"]} does not return after {P} (oracle)'); continue
        V = sorted(set().union(*st)); n += 1
        q5 = T5(V, st)
        q = [t5_quantities(V, st, t, q5) for t in range(P)]
        ok_o1 &= sum(x[4] for x in q) > 0
        ok_bal &= sum(x[2] for x in q) == sum(x[3] for x in q)
    report(ok_o1, f'{n} catalogue oscillators of period >= 3: each has an O1 event in its cycle')
    report(ok_bal, 'and over one period, total drive = total dissipation')


def test_spaceship_lightcone():
    rng = random.Random(9)
    ok = True; nseed = 0
    for k in range(30):
        seed = soup(rng, rng.choice([1, 2, 3]), rng.choice([0.3, 0.5, 0.7]))
        if not seed:
            continue
        nseed += 1
        st = run_states(seed, 40)
        for T in range(41):
            S = st[T]
            if not S:
                break
            p0 = min(seed)
            for q in S:                 # candidate v maps p0 into S
                v = sub(q, p0)
                if v != (0, 0, 0) and all(add(p, v) in S for p in seed):
                    ok = False
    report(ok, f'no_spaceship (stronger form): no generation <= 40 of {nseed} random seeds contains a nonzero translate of the seed')
    # light cone: two configurations differing at one cell
    worst = {'max': 0.0, 'l1': 0.0}; ok = True; trials = 0; reach2n = 0; nmax2n = 0
    for k in range(24):
        seed = soup(rng, 4, rng.choice([0.3, 0.45, 0.6]))
        cand = [p for p in itertools.product(range(-2, 3), repeat=3) if is_cell(p)]
        p0 = rng.choice(cand)
        seed2 = set(seed) ^ {p0}
        A = Box(seed | {(9, 0, 0), (-9, 0, 0), (0, 9, 0), (0, -9, 0), (0, 0, 9), (0, 0, -9)}, margin=8)
        B = Box(seed2 | {(9, 0, 0), (-9, 0, 0), (0, 9, 0), (0, -9, 0), (0, 0, 9), (0, 0, -9)}, margin=8)
        for n in range(1, 13):
            a, b = A.step(), B.step(); trials += 1
            diff = a ^ b
            if not diff:
                break
            mx = max(max(abs(c) for c in sub(q, p0)) for q in diff)
            l1 = max(sum(abs(c) for c in sub(q, p0)) for q in diff)
            ok &= mx <= 2 * n
            reach2n += mx == 2 * n
            if mx == 2 * n:
                nmax2n = max(nmax2n, n)
            worst['max'] = max(worst['max'], mx / n); worst['l1'] = max(worst['l1'], l1 / n)
    report(ok, f'light_cone: a one-cell difference stays within max-norm 2n of the flipped cell ({trials} generations); '
           f'largest max-norm spread per generation {worst["max"]:.2f}, L1 {worst["l1"]:.2f}; '
           f'max-norm spread exactly 2n in {reach2n} of them, up to n = {nmax2n}')


def test_torus():
    """Torus.tstep, transcribed entry by entry, against oracle.step for odd and even H; lift_tstep for each H."""
    rng = np.random.default_rng(3)
    for H in (2, 3, 4, 5, 6, 7, 8, 9, 10):
        m = oracle.masks(H)
        ok_t = True; ok_lift = True
        for trial in range(4):
            h = (rng.random((H, H, H)) < 0.4).astype(np.int8)
            if trial % 2 == 0:
                h &= (m[0] | m[1] | m[2])           # the oracle's states; odd trials also have non-cell bits set
            new = oracle.step(h, m)
            # literal transcription of tstep
            t = np.zeros_like(h)
            for i, j, k in itertools.product(range(H), repeat=3):
                p = (i, j, k)
                if not lean_isCell(p):
                    continue
                cnt = sum(int(h[(i + o[0]) % H, (j + o[1]) % H, (k + o[2]) % H]) for o in LOFFS[lean_axis(p)])
                alive = h[p] == 1
                t[p] = 1 if (3 <= cnt <= 5 if alive else cnt in (4, 5)) else 0
            ok_t &= (t == new).all()
            # lift_tstep: lift(tstep h)(p) = step(lift h)(p) for every point p of a box
            lift = lambda arr, p: int(arr[p[0] % H, p[1] % H, p[2] % H])
            for p in itertools.product(range(-H - 2, H + 3), repeat=3):
                lhs = lift(t, p)
                if lean_isCell(p):
                    cnt = sum(lift(h, q) for q in lean_nbrs(p))
                    rhs = 1 if (3 <= cnt <= 5 if lift(h, p) else cnt in (4, 5)) else 0
                else:
                    rhs = 0
                if lhs != rhs:
                    ok_lift = False; break
        report(ok_t, f'H={H}: transcribed Torus.tstep = oracle.step entry by entry (4 states, two with non-cell bits)')
        report(ok_lift == (H % 2 == 0), f'H={H}: lift_tstep {"holds" if ok_lift else "fails"} '
               f'(the Lean theorem claims it for even H; its header says it is false for odd H)')


def test_hull_firewall():
    rng = random.Random(11)
    ok_h = True; gens = 0; live = 0
    for k in range(30):
        seed = soup(rng, rng.choice([1, 2, 3]), rng.choice([0.3, 0.6, 0.9]))
        if not seed:
            continue
        C = {d: max(dot(d, p) for p in seed) for d in DIAGS}
        st = run_states(seed, 30)
        for s in st:
            gens += 1; live += len(s)
            ok_h &= all(dot(d, p) <= C[d] for p in s for d in DIAGS)
    report(ok_h, f'hull (T2): {gens} generations of 30 seeds ({live} live cell-generations) stay in the seed\'s '
           f'diagonal hull (oracle)')
    # firewall: three dead layers C < s <= C+6 along (1,1,1) stay dead; two dead layers can fill
    d = (1, 1, 1); ok3 = True; fill2 = 0
    for k in range(40):
        seed = soup(rng, 5, 0.45)
        C = rng.choice([-1, 0, 1, 2])
        three = {p for p in seed if not (C < dot(d, p) <= C + 6)}
        st = run_states(three, 25)
        ok3 &= all(not (C < dot(d, p) <= C + 6) for s in st for p in s)
        two = {p for p in seed if not (C < dot(d, p) <= C + 4)}
        st2 = run_states(two, 1)
        fill2 += any(C < dot(d, p) <= C + 4 for p in st2[1])
    report(ok3, 'firewall (T3): 40 soups with three dead layers keep them dead for 25 generations (oracle)')
    report(fill2 > 0, f'two dead layers are not a firewall: born in the band in {fill2}/40 soups after one generation')


TESTS = {'nbrs': test_nbrs, 'layer': test_layer, 'set36': test_set36, 'beyond': test_beyond, 't5': test_t5,
         'spaceship': test_spaceship_lightcone, 'torus': test_torus, 'hull': test_hull_firewall}

if __name__ == '__main__':
    names = sys.argv[1:] or list(TESTS)
    for nme in names:
        print(f'--- {nme}', flush=True)
        TESTS[nme]()
    print(f'{len(FAILS)} FAIL lines')
    sys.exit(1 if FAILS else 0)
