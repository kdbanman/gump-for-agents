#!/usr/bin/env python3
"""verify_call9 (push 9): the call line on reference/oracle.py alone (numpy, json).

    python3 verify_call9.py [objects/call9.json] [--only NAME]

Each run of the object file starts from the state of its `start` letters, laid on the oracle's cubic torus of side H
(oracle.masks(H), oracle.step): a finite object with a dead margin, so the run is that of the infinite lattice by T2
(asserted: no live cell ever comes within 4 sites of the planes x + z = 3 +- H/2 and y = H/2, where the torus would
close the store wire's tube and the line onto themselves).
A state of letters w = capL + for each letter i the two stators and the sites of hex digit w[i], moved to unit 4 + i
+ capR moved to unit 4 + N + the run's extra cells (the call line at rest: a capped wire C across the store wire);
unit u = move by (2u, 0, -2u).
At each generation: first every check of that generation (the whole torus equals the state of the check's letters,
cell for cell: so the line is at rest and exactly as it was, and nothing else is alive), then that generation's
operations (cells removed, each of which must be live; cells made live, each of which must be dead), then one step.
Also checked for every run: the start state returns to itself after 2 generations when left alone; the store wire
and the line together are exactly the two alone (no cell of one is a cell of the other, and the start state is the
union); every cell removed is a stator of the store wire at least 10 units from every unit d, f of the last checked
state and from the crossing; the cells made live are two, in one generation, at least 10 cubes (20 doubled units,
max-norm) from every cell of the store wire.
Prints PASS or FAIL per run and ALL PASS.
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    if only in args:
        args.remove(only)
    d = json.load(open(args[0] if args else os.path.join(HERE, 'objects', 'call9.json')))
    tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)

    def wire(word):
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
        assert H // 2 >= run['N'] + 8 + 6

        def arr(cells):
            h = np.zeros((H, H, H), np.int8)
            for c in cells:
                i = (c[0] % H, c[1] % H, c[2] % H); assert m[0][i] or m[1][i] or m[2][i], c
                h[i] = 1
            return h

        def state(word):
            w = wire(word)
            assert not (w & extra)
            return w | extra

        # where the torus would wrap the object onto itself
        idx = np.indices((H, H, H))
        seam = (np.abs(((idx[0] + idx[2] - 3 + H // 2) % H) - 0) < 4) | (np.abs(((idx[0] + idx[2] - 3 + H // 2) % H) - H) < 4) \
            | (np.abs(idx[1] - H // 2) < 4)
        start = arr(state(run['start']))
        ok = np.array_equal(oracle.step(oracle.step(start, m), m), start)
        why = '' if ok else ' start state is not standing;'
        if extra:
            e = arr(extra)
            if not np.array_equal(oracle.step(oracle.step(e, m), m), e):
                ok = False; why += ' the line alone is not standing;'
        ops = {g: (off, on) for g, off, on in run['ops']}
        h = start; G = max(g for g, _ in run['checks']); nchk = 0; last = run['start']; ncall = 0
        for g in range(G + 1):
            if (h & seam).any():
                ok = False; why += f' a live cell near the seam at {g};'
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
                    u = c[0] // 2
                    if tuple(tr(c, -u)) not in set(map(tuple, d['stators'])):
                        ok = False; why += f' operation at {g} removes a cell that is not a stator;'
                    near = [4 + j for j, ch in enumerate(last) if ch in 'df'] + ([4 + run['crossing']] if run.get('crossing') is not None else [])
                    if any(abs(u - v) < 10 for v in near):
                        ok = False; why += f' operation at {g} is nearer than 10 units to a store or to the crossing;'
                if on:
                    ncall += 1
                    w = wire(last)
                    dist = min(max(abs(c[0] - q[0]), abs(c[1] - q[1]), abs(c[2] - q[2])) for c in on for q in w)
                    if len(on) != 2 or dist < 20:
                        ok = False; why += f' the call at {g} is not two cells at least 10 cubes from the store wire (distance {dist});'
                    for c in on:
                        i = (c[0] % H, c[1] % H, c[2] % H)
                        if h[i] != 0:
                            ok = False; why += f' operation at {g} makes a live cell live;'
                        h[i] = 1
            if g < G:
                h = oracle.step(h, m)
        ok_all &= ok
        noff = sum(len(o[0]) for o in ops.values())
        print(('PASS ' if ok else 'FAIL ') + f"{run['name']}: {run['text']}  ({len(state(run['start']))} cells at the start, {noff} cells removed and {ncall} calls "
              f"in all, {nchk} whole-state checks to generation {G})" + why + f'  [{time.time() - t0:.0f} s]', flush=True)
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
