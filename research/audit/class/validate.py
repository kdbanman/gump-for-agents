"""validate.py -- anchor the audit stepper (aud.c / aud.py) bit-exact to reference/oracle.py, then to naive numpy
rolls for the lattices the oracle does not cover.  Prints one line per check and "ALL OK" at the end.

    python3 validate.py
"""
import os, sys
import numpy as np
import aud

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "reference"))
import oracle  # the project's ground truth (gump only)

ok = True


def check(name, cond):
    global ok
    print(("PASS  " if cond else "FAIL  ") + name)
    ok &= bool(cond)


def roll_step(h, typemasks, offs, B, S):
    """Naive doubled-coordinate stepper: one np.roll per offset per type (the oracle's scheme, any offsets)."""
    new = np.zeros_like(h)
    for t, m in enumerate(typemasks):
        cnt = np.zeros(h.shape, np.int16)
        for o in offs[t]:
            cnt += np.roll(h, tuple(-d for d in o), axis=tuple(range(h.ndim)))
        new[m & (((h == 0) & np.isin(cnt, B)) | ((h == 1) & np.isin(cnt, S)))] = 1
    return new


def to_grid(V, H, states):
    g = np.zeros((states.shape[0],) + (H,) * V.L.dim, np.int8)
    idx = tuple(np.array([p[a] for p in V.cells]) for a in range(V.L.dim))
    for r in range(states.shape[0]):
        g[r][idx] = states[r]
    return g


# 1. offsets of my gump lattice = the oracle's
G = aud.lattice("gump")
check("gump offsets equal oracle.offsets (as sets, per type)",
      all(set(G.offsets[a]) == set(oracle.offsets(a)) for a in range(3)))

# 2. gump torus, 64 soups, bit-exact against oracle.step for 40 generations
rng = np.random.default_rng(11)
for H in (8, 12):
    V = aud.torus(G, H)
    m = oracle.masks(H)
    st = (rng.random((64, V.N)) < 0.42).astype(np.uint8)
    x = aud.pack(st)
    grids = to_grid(V, H, st)
    good = True
    for t in range(40):
        x = aud.step(V, x, [4, 5], [3, 4, 5])
        grids = np.array([oracle.step(g, m) for g in grids])
        good &= np.array_equal(to_grid(V, H, aud.unpack(x)), grids)
    check(f"gump torus H={H} ({V.N} cells): 64 soups x 40 generations bit-exact vs reference/oracle.py "
          f"(final populations {int(grids.sum())})", good and grids.sum() > 0)

# 3. golden side-8 cube log (legacy H = 40), 23 generations, final population 384
ref = [int(l.split()[1]) for l in open(os.path.join(HERE, "..", "..", "..", "reference", "golden",
                                                    "legacy_cube_side08_H40.txt")) if l.strip()]
H = 40
V = aud.torus(G, H)
lo, hi = oracle.legacy_seed_span(H)
h = oracle.fill_box(H, lo, hi, oracle.masks(H))
st = np.array([[h[p] for p in V.cells]], dtype=np.uint8)
x = aud.pack(st)
pops = [0]
for g in range(1, len(ref)):
    x = aud.step(V, x, [4, 5], [3, 4, 5])
    pops.append(int(aud.unpack(x, 1).sum()))
check(f"golden side-8 cube: {len(ref) - 1} generations of populations equal the 2012 log, final {pops[-1]}",
      pops[1:] == ref[1:] and pops[-1] == 384)

# 4. face12e against naive rolls (the oracle's scheme with the coplanar four replaced)
E = aud.lattice("face12e")
for a in range(3):
    b, c = [i for i in range(3) if i != a]
    perp = {o for o in E.offsets[a] if o[a] != 0}
    cop = {o for o in E.offsets[a] if o[a] == 0}
    want = set()
    for t in (b, c):
        for s in (2, -2):
            o = [0, 0, 0]; o[t] = s; want.add(tuple(o))
    good = cop == want and perp == {o for o in G.offsets[a] if o[a] != 0} and len(E.offsets[a]) == 12
    check(f"face12e type {a}: 8 perpendicular offsets as gump, coplanar four = +-2e_b, +-2e_c", good)
for H in (8, 12):
    V = aud.torus(E, H)
    m = oracle.masks(H)
    st = (rng.random((64, V.N)) < 0.42).astype(np.uint8)
    x = aud.pack(st)
    grids = to_grid(V, H, st)
    good = True
    for t in range(40):
        x = aud.step(V, x, [4, 5], [3, 4, 5])
        grids = np.array([roll_step(g, m, E.offsets, [4, 5], [3, 4, 5]) for g in grids])
        good &= np.array_equal(to_grid(V, H, aud.unpack(x)), grids)
    check(f"face12e torus H={H}: 64 soups x 40 generations bit-exact vs numpy rolls (final {int(grids.sum())})",
          good and grids.sum() > 0)
# the roll stepper itself reproduces the oracle when given gump's offsets
H = 8
m = oracle.masks(H)
g0 = ((rng.random((H, H, H)) < 0.42) & (m[0] | m[1] | m[2])).astype(np.int8)
a1, a2 = g0.copy(), g0.copy()
good = True
for t in range(30):
    a1 = oracle.step(a1, m); a2 = roll_step(a2, m, G.offsets, [4, 5], [3, 4, 5])
    good &= np.array_equal(a1, a2)
check("numpy roll stepper with gump offsets = oracle.step (30 generations)", good)

# 5. fcc and cross2 against naive rolls, two rules each
for name, H, rules in (("fcc", 10, [([4, 5], [3, 4, 5]), ([4, 5, 6], [3, 4, 5, 6])]),
                       ("cross2", 12, [([3, 4], [2, 3, 4]), ([3, 4, 5, 6], [2, 3, 4, 5, 6])]),
                       ("vn", 12, [([2], [1, 2])])):
    L = aud.lattice(name)
    V = aud.torus(L, H)
    full = np.zeros((H,) * L.dim, bool)
    full[tuple(np.array([p[a] for p in V.cells]) for a in range(L.dim))] = True
    for B, S in rules:
        st = (rng.random((64, V.N)) < 0.45).astype(np.uint8)
        x = aud.pack(st)
        grids = to_grid(V, H, st)
        good = True
        for t in range(30):
            x = aud.step(V, x, B, S)
            grids = np.array([roll_step(g, [full], L.offsets, B, S) for g in grids])
            good &= np.array_equal(to_grid(V, H, aud.unpack(x)), grids)
        check(f"{name} torus H={H} B{B}/S{S}: 64 soups x 30 generations bit-exact vs numpy rolls "
              f"(final {int(grids.sum())})", good)

# 6. vessels with a dead outside: gump {111} slab against a padded oracle run with the outside forced dead
V, layer = aud.slab111(G, 5, 2, 2)
# embed one period-image set into a big oracle torus is not possible for a periodic slab; instead check the slab
# graph against direct neighbour arithmetic
good = True
for i, p in enumerate(V.cells):
    for j, o in enumerate(G.offsets[G.typ(p)]):
        q = tuple(a + b for a, b in zip(p, o))
        s = sum(q)
        inside = 1 <= s <= 9
        good &= (V.nbr[i, j] < V.N) == inside
        if inside:
            r = V.cells[V.nbr[i, j]]
            d = tuple(a - b for a, b in zip(q, r))
            # q - r must be an integer combination of 2*g1 = (4,-4,0) and 2*g2 = (0,4,-4)
            good &= sum(d) == 0 and d[0] % 4 == 0 and d[2] % 4 == 0
check(f"gump {{111}} slab graph (5 layers, 2x2 periods, {V.N} cells): every neighbour is the right cell modulo "
      f"the period lattice", good and V.N == 5 * 12)
# box vessel against the oracle on a large torus with the outside dead by construction (octahedral hull, T2)
H = 24
m = oracle.masks(H)
c0 = 12
pred = lambda p: all(abs(sx * (p[0]) + sy * (p[1]) + sz * (p[2])) <= 9 for sx in (1,) for sy in (1, -1) for sz in (1, -1))
V = aud.region(G, pred, 10)
st = (rng.random((8, V.N)) < 0.45).astype(np.uint8)
x = aud.pack(st)
grids = np.zeros((8, H, H, H), np.int8)
idx = tuple(np.array([p[a] + c0 for p in V.cells]) for a in range(3))
for r in range(8):
    grids[r][idx] = st[r]
good = True
for t in range(60):
    x = aud.step(V, x, [4, 5], [3, 4, 5])
    grids = np.array([oracle.step(g, m) for g in grids])
    mine = np.zeros_like(grids)
    u = aud.unpack(x, 8)
    for r in range(8):
        mine[r][idx] = u[r]
    good &= np.array_equal(mine, grids)
check(f"gump octahedral hull vessel (radius 9, {V.N} cells): 8 soups x 60 generations equal the oracle on a free "
      f"torus (T2: nothing leaves the hull), final {int(grids.sum())}", good)

print("ALL OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
