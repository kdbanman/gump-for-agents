#!/usr/bin/env python3
"""verify_call9 (push 9): the call line on reference/oracle.py alone (numpy, json).

    python3 verify_call9.py [objects/call9.json] [--only NAME]

Each run of the object file starts from the state of its `start` letters, laid on the oracle's cubic torus of side H
(oracle.masks(H), oracle.step).  The object is finite and the run is that of the infinite lattice: (a) the start
cells and each of their images under a nonzero multiple of H are more than 12 sites apart in max-norm (computed);
(b) at every generation, and after every operation, every live cell is within 4 sites (max-norm) of a start cell
(checked).  A cell's neighbours are at most 2 sites from it, so by induction no cell ever has neighbours in two
images and no live cell leaves the 4-site region of its own image.
A state of letters (words joined by '|', one per store wire) = for each word j: capL + for each letter i the two
stators and the sites of hex digit w[i], moved to unit 4 + i + capR moved to unit 4 + N, all moved by offsets[j];
+ the run's extra cells (the call lines at rest: capped wires C across the store wires); unit u = move by
(2u, 0, -2u).
At each generation: first every check of that generation (the whole torus equals the state of the check's letters,
cell for cell: so every line is at rest and exactly as it was, and nothing else is alive), then that generation's
operations (cells removed, each of which must be live; cells made live, each of which must be dead), then one step.
Also checked for every run: the start state returns to itself after 2 generations when left alone; the lines alone
return to themselves after 2 generations; no cell of a line is a cell of a store wire; every cell removed is a
stator of a store wire at least 10 units from every unit d, f of that wire in the last checked state and from every
crossing; the cells made live are two, in one generation, at least 10 cubes (20 doubled units, max-norm) from every
cell of every store wire.
Prints PASS or FAIL per run and ALL PASS.
"""
import sys, os, json, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402

D = 4


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    if only in args:
        args.remove(only)
    d = json.load(open(args[0] if args else os.path.join(HERE, 'objects', 'call9.json')))
    tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
    stators = set(map(tuple, d['stators']))

    def one(word):
        cells = set(map(tuple, d['capL']))
        for i, ch in enumerate(word):
            h = int(ch, 16)
            cells |= {tr(c, 4 + i) for c in d['stators']} | {tr(d['sites'][j], 4 + i) for j in range(4) if h >> j & 1}
        return cells | {tr(c, 4 + len(word)) for c in d['capR']}

    ok_all = True
    for run in d['runs']:
        if only and run['name'] != only:
            continue
        H = run['H']; m = oracle.masks(H); t0 = time.time(); extra = set(map(tuple, run['extra']))
        offs = [tuple(o) for o in run['offsets']]

        def wires(word):
            cells = set()
            for w, o in zip(word.split('|'), offs):
                mv = {(c[0] + o[0], c[1] + o[1], c[2] + o[2]) for c in one(w)}
                assert not (cells & mv)
                cells |= mv
            return cells

        def state(word):
            w = wires(word)
            assert not (w & extra)
            return w | extra

        def arr(cells):
            h = np.zeros((H, H, H), np.int8)
            for c in cells:
                i = (c[0] % H, c[1] % H, c[2] % H); assert m[0][i] or m[1][i] or m[2][i], c
                assert h[i] == 0, 'two cells of the state fall on one site of the torus'
                h[i] = 1
            return h

        # the torus is large enough (see the docstring): images of the start cells more than 12 sites apart, and a guard
        # region of the torus = every site within D = 4 sites (max-norm) of a start cell
        cells0 = state(run['start'])
        S = np.array(sorted(cells0))
        assert all(S[:, i].max() - S[:, i].min() < H for i in range(3))
        dmin = min(int(np.abs(S[:, None, :] - S[None, :, :] - H * np.array(v)).max(axis=2).min())
                   for v in itertools.product((-1, 0, 1), repeat=3) if any(v))
        ok = dmin > 2 * D + 4
        why = '' if ok else f' the torus is too small: the start cells and their images are {dmin} sites apart;'
        guard = np.zeros((H, H, H), bool)
        guard[S[:, 0] % H, S[:, 1] % H, S[:, 2] % H] = True
        for _ in range(D):
            for ax in range(3):
                guard = guard | np.roll(guard, 1, ax) | np.roll(guard, -1, ax)
        start = arr(cells0)
        if not np.array_equal(oracle.step(oracle.step(start, m), m), start):
            ok = False; why += ' start state is not standing;'
        if extra:
            e = arr(extra)
            if not np.array_equal(oracle.step(oracle.step(e, m), m), e):
                ok = False; why += ' the lines alone are not standing;'
        ops = {g: (off, on) for g, off, on in run['ops']}
        h = start; G = max(g for g, _ in run['checks']); nchk = 0; last = run['start']; ncall = 0
        for g in range(G + 1):
            if (h.astype(bool) & ~guard).any():
                ok = False; why += f' a live cell more than {D} sites from the start cells at {g};'
            for cg, word in run['checks']:
                if cg == g:
                    nchk += 1; last = word
                    if not np.array_equal(h, arr(state(word))):
                        ok = False; why += f' state at {g} is not {word};'
            if g in ops:
                off, on = ops[g]
                if not any(cg == g for cg, _ in run['checks']):
                    ok = False; why += f' no whole-state check at the generation of the operation at {g};'
                for c in off:
                    i = (c[0] % H, c[1] % H, c[2] % H)
                    if h[i] != 1:
                        ok = False; why += f' operation at {g} removes a dead cell;'
                    h[i] = 0
                    found = False
                    for w, o in zip(last.split('|'), offs):
                        q = (c[0] - o[0], c[1] - o[1], c[2] - o[2]); u = q[0] // 2
                        if tuple(tr(q, -u)) in stators and 4 <= u < 4 + len(w):
                            found = True
                            near = [4 + j for j, ch in enumerate(w) if ch in 'df'] + [4 + x for x in run['crossings']]
                            if any(abs(u - v) < 10 for v in near):
                                ok = False; why += f' operation at {g} is nearer than 10 units to a store or to a crossing;'
                    if not found:
                        ok = False; why += f' operation at {g} removes a cell that is not a stator of a store wire;'
                if on:
                    ncall += 1
                    w = wires(last)
                    dist = min(max(abs(c[0] - q[0]), abs(c[1] - q[1]), abs(c[2] - q[2])) for c in on for q in w)
                    if len(on) != 2 or dist < 20:
                        ok = False; why += f' the call at {g} is not two cells at least 10 cubes from the store wires (distance {dist});'
                    for c in on:
                        i = (c[0] % H, c[1] % H, c[2] % H)
                        if h[i] != 0:
                            ok = False; why += f' operation at {g} makes a live cell live;'
                        h[i] = 1
                        if not guard[i]:
                            ok = False; why += f' operation at {g} makes a cell live more than {D} sites from the start cells;'
            if g < G:
                h = oracle.step(h, m)
        ok_all &= ok
        noff = sum(len(o[0]) for o in ops.values())
        print(('PASS ' if ok else 'FAIL ') + f"{run['name']}: {run['text']}  ({len(cells0)} cells at the start, {noff} cells removed and {ncall} calls "
              f"in all, {nchk} whole-state checks to generation {G}; torus {H}, images {dmin} sites apart)" + why + f'  [{time.time() - t0:.0f} s]', flush=True)
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
