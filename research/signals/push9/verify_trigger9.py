#!/usr/bin/env python3
"""verify_trigger9 (push 9): the signal-triggered count read on reference/oracle.py alone (numpy, json).

    python3 verify_trigger9.py [objects/trigger9.json] [--only NAME]

Each run of the object file starts from the state of its `start` letters, laid on the oracle's cubic torus of side H
(oracle.masks(H), oracle.step; the wire along (1,0,-1) closes into a ring of H/2 units, of which the object fills at
most N + 8, the rest is dead margin: a finite object, so the run is that of the infinite lattice by T2).
A state of letters w = capL + for each letter i the two stators and the sites of hex digit w[i], moved to unit 4 + i
+ capR moved to unit 4 + N + the run's extra cells (the still life beside the wire); unit u = move by (2u, 0, -2u).
At each generation: first every check of that generation (the whole torus equals the state of the check's letters,
cell for cell: so the still life is as it was and nothing else is alive), then that generation's operations (each
removes one cell, which must be live), then one step.
Also checked for every run: the start state returns to itself after 2 generations when left alone; the extra cells
form a still life on their own; every operation is at least 10 units from every unit d, f of the state it is applied
to and from the still life (the trigger is made far away and arrives as a pulse).
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
    d = json.load(open(args[0] if args else os.path.join(HERE, 'objects', 'trigger9.json')))
    tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)

    def state(word, extra):
        cells = set(map(tuple, d['capL']))
        for i, ch in enumerate(word):
            h = int(ch, 16)
            cells |= {tr(c, 4 + i) for c in d['stators']} | {tr(d['sites'][j], 4 + i) for j in range(4) if h >> j & 1}
        cells |= {tr(c, 4 + len(word)) for c in d['capR']}
        n = len(cells)
        cells |= set(map(tuple, extra))
        assert len(cells) == n + len(extra)
        return cells

    ok_all = True
    for run in d['runs']:
        if only and run['name'] != only:
            continue
        H = run['H']; m = oracle.masks(H); t0 = time.time(); extra = run['extra']
        assert H // 2 >= run['N'] + 8 + 6

        def arr(cells):
            h = np.zeros((H, H, H), np.int8)
            for c in cells:
                i = (c[0] % H, c[1] % H, c[2] % H); assert m[0][i] or m[1][i] or m[2][i], c
                h[i] = 1
            return h

        start = arr(state(run['start'], extra))
        ok = np.array_equal(oracle.step(oracle.step(start, m), m), start)
        why = '' if ok else ' start state is not standing;'
        if extra:
            e = arr(extra)
            if not np.array_equal(oracle.step(e, m), e):
                ok = False; why += ' the extra cells are not a still life;'
        ops = {g: cells for g, cells in run['ops']}
        h = start; G = max(g for g, _ in run['checks']); nchk = 0; last = run['start']
        for g in range(G + 1):
            for cg, word in run['checks']:
                if cg == g:
                    nchk += 1; last = word
                    if not np.array_equal(h, arr(state(word, extra))):
                        ok = False; why += f' state at {g} is not {word};'
            for c in ops.get(g, []):
                i = (c[0] % H, c[1] % H, c[2] % H)
                if h[i] != 1:
                    ok = False; why += f' operation at {g} removes a dead cell;'
                h[i] = 0
                u = c[0] // 2
                near = [4 + j for j, ch in enumerate(last) if ch in 'df'] + [q[0] // 2 for q in extra]
                if any(abs(u - v) < 10 for v in near):
                    ok = False; why += f' operation at {g} is nearer than 10 units to a store or to the still life;'
                if not any(cg == g for cg, _ in run['checks']):
                    ok = False; why += f' no whole-state check at the generation of the operation at {g};'
            if g < G:
                h = oracle.step(h, m)
        ok_all &= ok
        nops = sum(len(c) for c in ops.values())
        ncell = len(state(run['start'], extra))
        print(('PASS ' if ok else 'FAIL ') + f"{run['name']}: {run['text']}  ({ncell} cells at the start, {nops} cells removed in all, "
              f"{nchk} whole-state checks to generation {G})" + why + f'  [{time.time() - t0:.0f} s]', flush=True)
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
