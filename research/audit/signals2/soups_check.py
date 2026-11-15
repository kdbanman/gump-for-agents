"""README section 12 (soup-born carriers) re-run with an independent stepper and other seeds.

    python3 soups_check.py NSOUP [seed]       (NSOUP per ring length; L = 1, 2, 3, 4, 6)

Ring of L units of the closed 3x3 tube (1 <= x+y+z, x-y+z <= 5; T2 closes it), as the periodic lift: cell c and
c + L(2,0,-2) identified, a cell may be its own neighbour (L = 1) which is right for the lift.  The ring stepper is
first checked against the oracle: a ring of 12 units on the box torus (24,16,24) (see tape_check.py), and rings of
L | 12 against the ring of 12 carrying the soup repeated.
Soup: each tube cell alive with probability 0.4.  3000 generations, then kept if S(T+2) == S(T) (period <= 2),
non-empty and the same in every unit.  Distinct wires: the unit-0 cells (relative), minimised over the two phases.
Pulse test (as the README describes it): on a ring of 24 units, every pair of cells of units 10..11 (at least one
in unit 10) flipped, at each phase; 2 generations later the difference must be exactly the pair moved one unit,
either way.
"""
import itertools, sys
from collections import Counter
import numpy as np
import gs
oracle = gs.oracle
inside = lambda p: 1 <= p[0] + p[1] + p[2] <= 5 and 1 <= p[0] - p[1] + p[2] <= 5


def ring(L):
    cells = [c for c in gs.closure([(1, 0, 2), (0, 1, 2), (0, 0, 3)], lambda p: inside(p) and 0 <= gs.unit(p) < L)]
    can = lambda p: gs.tr(p, -(gs.unit(p) // L) * L)
    D = gs.Dom(cells, can)
    assert all(inside(c) for c in D.cells)
    D.L = L; D.u = np.array([gs.unit(c) for c in D.cells])
    # local index: cell relative to its unit
    D.rel = [gs.tr(c, -gs.unit(c)) for c in D.cells]
    return D


def check_ring():
    rng = np.random.default_rng(5)
    R12 = ring(12); shape = (24, 16, 24); m = gs.box_masks(shape)
    ok = True
    for _ in range(5):
        s = (rng.random(R12.n + 1) < 0.4).astype(np.uint8); s[-1] = 0
        h = gs.to_arr(R12.cells_of(s), shape); x = s
        for t in range(40):
            h = oracle.step(h, m); x = R12.step(x)
            got = {(c[0] % 24, c[1] % 16, c[2] % 24) for c in R12.cells_of(x)}
            ok &= got == set(gs.from_arr(h))
    for L in (1, 2, 3, 4, 6):
        R = ring(L)
        for _ in range(5):
            s = (rng.random(R.n + 1) < 0.4).astype(np.uint8); s[-1] = 0
            big = R12.state([gs.tr(c, k * L) for c in R.cells_of(s) for k in range(12 // L)])
            a, b = R.run(s, 40), R12.run(big, 40)
            ok &= R12.cells_of(b) == frozenset(gs.tr(c, k * L) for c in R.cells_of(a) for k in range(12 // L))
    print('ring stepper vs oracle (L=12) and lifts (L=1,2,3,4,6):', 'OK' if ok else 'FAILED', flush=True)
    return ok


def pulses(unit_cells_phase0):
    R = ring(24)
    z0 = R.state([gs.tr(c, k) for c in unit_cells_phase0 for k in range(24)])
    assert (R.run(z0, 2) == z0).all()
    found = set()
    for ph in range(2):
        z = R.run(z0, ph); z2 = R.run(z, 2)
        cand = [i for i in range(R.n) if R.u[i] in (10, 11)]
        pairs = [pr for pr in itertools.combinations(cand, 2) if min(R.u[i] for i in pr) == 10]
        X = np.repeat(z[None], len(pairs), 0)
        for k, pr in enumerate(pairs):
            X[k, list(pr)] ^= 1
        Y = R.run(X, 2)
        for k, pr in enumerate(pairs):
            d = set(np.nonzero(Y[k, :R.n] != z2[:R.n])[0].tolist())
            for s in (1, -1):
                if d == {R.index[R.canon(gs.tr(R.cells[i], s))] for i in pr}:
                    found.add(s)
    return found


def main():
    nsoup = int(sys.argv[1]); seed = int(sys.argv[2]) if len(sys.argv) > 2 else 99
    assert check_ring()
    rng = np.random.default_rng(seed)
    wires = Counter(); per_L = {}
    for L in (1, 2, 3, 4, 6):
        R = ring(L)
        S = (rng.random((nsoup, R.n + 1)) < 0.4).astype(np.uint8); S[:, -1] = 0
        S = R.run(S, 3000); S2 = R.run(S, 2)
        keep = (S == S2).all(1) & (S[:, :R.n].sum(1) > 0)
        S1 = R.step(S)
        nk = 0
        for k in np.nonzero(keep)[0]:
            keys = []
            for st in (S[k], S1[k]):
                cells = [R.rel[i] for i in np.nonzero(st[:R.n])[0]]
                byu = Counter(R.u[i] for i in np.nonzero(st[:R.n])[0])
                rel = Counter(cells)
                uniform = len(byu) == L and all(v == L for v in rel.values())
                keys.append(frozenset(cells))
            if not uniform:
                continue
            nk += 1
            wires[min(keys, key=lambda f: sorted(f))] += 1
        per_L[L] = (int(keep.sum()), nk)
        print(f'L={L}: {nsoup} soups, period <= 2 and non-empty {int(keep.sum())}, of which uniform wires {nk}', flush=True)
    tot = sum(wires.values())
    print(f'uniform wires of period <= 2: {tot} soups of {5 * nsoup}, {len(wires)} distinct (up to phase)', flush=True)
    carriers = []
    for w, cnt in wires.most_common():
        # phase-0 representative: step the ring of 24 from w; pulses() tests both phases anyway
        f = pulses(sorted(w))
        if f:
            carriers.append((cnt, len(w), sorted(f)))
    print(f'carriers of a 2-cell pulse: {len(carriers)} distinct, born in {sum(c[0] for c in carriers)} soups')
    for c in carriers:
        print('   born', c[0], 'times;', c[1], 'cells per unit; directions', c[2])


if __name__ == '__main__':
    main()
