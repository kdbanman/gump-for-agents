#!/usr/bin/env python3
"""Check every stepper of research/signals against reference/oracle.py.

    python3 check_stepper.py          # ~1 min; prints one line per test and ALL OK at the end

 1. Geom (C kernels, dense and sparse) on box tori, cubic and not, against oracle.step on the same box: random soups
    at three densities, 40 generations, every generation, cell for cell.
 2. step_set (python sets, infinite lattice) against the oracle on a padded cubic torus: random blobs, 25 generations.
 3. Geom on twisted tori with slab and tube bounds, and on rank-1 rings, against step_set on a lifted patch of the
    infinite lattice (hence, by 2, against the oracle): the centre of the patch, inside the light cone.
 4. A negative control: the same comparison with the rule changed (B45/S34) must fail.
"""
import itertools, random, sys
import numpy as np
import sg

ok = True


def report(name, good):
    global ok
    ok &= bool(good)
    print(('ok   ' if good else 'FAIL ') + name, flush=True)


def test_box(shape, rho, seed, gens=40):
    rng = random.Random(seed)
    N = [s // 2 for s in shape]
    g = sg.Geom([(N[0], 0, 0), (0, N[1], 0), (0, 0, N[2])], box=max(shape))
    assert g.n == 3 * N[0] * N[1] * N[2], (g.n, shape)
    cells = [p for p in g.cells if rng.random() < rho]
    std = g.state(cells); sts = std.copy()
    good = True
    for t, ref in sg.oracle_run(cells, shape, gens):
        good &= g.cells_of(std) == ref and g.cells_of(sts) == ref
        std = g.run(std, 1); sts = g.run(sts, 1, sparse=True)
    # also multi-generation calls
    good &= g.cells_of(g.run(g.state(cells), gens)) == ref and g.cells_of(g.run(g.state(cells), gens, sparse=True)) == ref
    return good, len(ref)


for shape in [(12, 12, 12), (16, 16, 16), (8, 12, 20), (6, 22, 10), (24, 8, 8)]:
    for rho in (0.2, 0.38, 0.6):
        good, pop = test_box(shape, rho, hash((shape, rho)) & 0xffff)
        report(f'1 box torus {shape} rho {rho}: Geom dense+sparse == oracle for 40 gens (final pop {pop})', good)


def test_set(seed, gens=25):
    rng = random.Random(seed)
    cells = [p for p in itertools.product(range(-5, 6), repeat=3) if sg.is_cell(p) and rng.random() < 0.4]
    H = 80; sh = 40
    cur = frozenset(cells); good = True
    for t, ref in sg.oracle_run([(p[0] + sh, p[1] + sh, p[2] + sh) for p in cells], (H, H, H), gens):
        good &= frozenset((p[0] + sh, p[1] + sh, p[2] + sh) for p in cur) == ref
        cur = sg.step_set(cur)
    return good, len(ref)


for seed in range(3):
    good, pop = test_set(seed)
    report(f'2 step_set == oracle on a random blob, 25 gens (seed {seed}, final pop {pop})', good)


def test_quotient(periods, bounds, rho, seed, T=8, R=4, unitvec=None, rule=None):
    """Random state of the quotient; its periodic lift restricted to the max-norm ball of R + T + 1 cubes about the
    origin is stepped T times with step_set; inside the ball of R cubes (the light cone: one cube per generation) the
    result must equal the quotient's evolution."""
    rng = random.Random(seed)
    g = sg.Geom(periods, bounds, unitvec=unitvec)
    cells = [p for p in g.cells if rng.random() < rho]
    st = g.state(cells)
    ball = lambda r: [p for p in itertools.product(range(-r, r + 1), repeat=3) if sg.is_cell(p) and g.inside(p)]
    live = g.cells_of(st)
    L = frozenset(p for p in ball(2 * (R + T + 1)) if g.canon(p) in live)
    for _ in range(T):
        L = sg.step_set(L)
    st = g.run(st, T, sparse=True) if rule is None else rule(g, st, T)
    live = g.cells_of(st)
    inner = ball(2 * R)
    return all((g.canon(p) in live) == (p in L) for p in inner), g.n, sum(p in L for p in inner)


S = (1, 1, 1); S2 = (1, -1, 1)
cases = [
    ('twisted torus (1,3,12), 8-layer slab', [(1, 3, -4), (0, 12, -12)], [(S, 1, 15)]),
    ('twisted torus (2,2,8), 5-layer slab', [(2, 2, -4), (0, 8, -8)], [(S, 1, 9)]),
    ('ring 5 x (3,0,-3) in a 4 x 5 diamond tube', [(15, 0, -15)], [(S, 1, 7), (S2, 1, 9)]),
    ('strip 4 x (1,3,-4) by (0,10,-10), 6-layer slab', [(4, 12, -16), (0, 10, -10)], [(S, 1, 11)]),
    ('3D twisted torus', [(3, 1, 0), (0, 4, 1), (1, 0, 5)], []),
]
for name, periods, bounds in cases:
    good, n, pop = test_quotient(periods, bounds, 0.38, 7)
    report(f'3 {name}: Geom == step_set on the lifted patch after 8 gens ({n} cells in the quotient, {pop} live in the compared ball)', good)


def wrong_rule(g, st, T):          # B45/S34: negative control
    for _ in range(T):
        cnt = st[g.nb].sum(1)
        new = np.zeros_like(st)
        new[:g.n] = np.where(st[:g.n] == 1, (cnt >= 3) & (cnt <= 4), (cnt == 4) | (cnt == 5))
        st = new
    return st


name, periods, bounds = cases[0]
good, n, pop = test_quotient(periods, bounds, 0.38, 7, rule=wrong_rule)
report('4 negative control: B45/S34 on the same case is detected as different', not good)

# unit positions along a ring
g = sg.Geom([(15, 0, -15)], [(S, 1, 7), (S2, 1, 9)], unitvec=(3, 0, -3))
report(f'5 ring units: N = {g.N}, every unit holds the same number of cells', g.N == 5 and len(set(np.bincount(g.unit))) == 1)
print('ALL OK' if ok else 'SOME TESTS FAILED')
sys.exit(0 if ok else 1)
