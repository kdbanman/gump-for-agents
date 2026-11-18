#!/usr/bin/env python3
"""verify_osc9 (review of signals push 9): a call on the store's own wire by ONE pulse, with the period-3 oscillator
P3.15f beside the wire at the wall.  reference/oracle.py alone (numpy, json); reads only the object file.

    python3 verify_osc9.py [objects/osc-call-P3.15f.json] [--only NAME]

A state of `letters` at generation t = capL moved to unit first - 4 + for each letter i the two stators and the sites
of hex digit letters[i] moved to unit first + i + capR moved to unit first + N + osc_even[(t/2) mod 3], t even
(unit u = move by (2u, 0, -2u)).  osc_even = the oscillator's part of the standing pair (plain wire + oscillator) at
generations 0, 2, 4; osc_free = the free oscillator's three phases.  Each run starts from the state of its `start` letters at generation 0 on a rectangular array torus
(masks by oracle.masks' formula for the array's shape, even origin; stepping by oracle.step).
The run is the run of the infinite lattice: after every generation the four outermost index planes on every side of
the array are checked to be dead, and a cell's neighbours are at most 2 sites from it, so no neighbour count ever
includes a wrapped cell.  The exact distance from the start cells to their nearest torus image is printed.
At each generation: first every check of that generation (the whole torus equals the state of the check's letters,
cell for cell: the wire is exactly those letters, the oscillator is exactly its free orbit, nothing else is alive),
then that generation's operations (cells removed; each must be live and must be a stator (0,1,2) or (0,1,4) of a unit
at least 10 units from every unit d or f of the last checked state and from the wall), then one step.
Also checked: osc_free is one orbit of period exactly 3 when alone; osc_even[0] and osc_even[2] are its phases 0 and 1
and osc_even[1] is its phase 2 less the cells printed (the pair is a junction); plain wire + osc_even[0] stepped by the
oracle is plain wire + osc_even[1], osc_even[2] two and four generations on; the start state returns to itself after
6 generations and not before; every right-going pulse (stator (0,1,2) of unit u removed at generation g)
obeys the timing rule (g + u) mod 3 = (wall + 2) mod 3 and g is even.
Prints PASS or FAIL per run and ALL PASS.
"""
import sys, os, json, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle  # noqa: E402

PAD = 12


class Box:
    def __init__(self, cells):
        pts = np.array(sorted(cells), dtype=np.int64)
        lo = pts.min(0) - PAD; lo -= lo % 2
        shape = pts.max(0) + PAD - lo + 1; shape += shape % 2
        self.org = tuple(int(v) for v in lo); self.shape = tuple(int(v) for v in shape)
        par = np.indices(self.shape) % 2
        self.m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]
        self.valid = self.m[0] | self.m[1] | self.m[2]
        self.h = np.zeros(self.shape, np.int8)
        for c in cells:
            i = self.ix(c); assert self.valid[i] and self.h[i] == 0
            self.h[i] = 1
        self.guard()

    def ix(self, c):
        return (c[0] - self.org[0], c[1] - self.org[1], c[2] - self.org[2])

    def guard(self):
        h = self.h
        assert not (h[:4].any() or h[-4:].any() or h[:, :4].any() or h[:, -4:].any() or h[:, :, :4].any() or h[:, :, -4:].any())

    def step(self):
        self.h = oracle.step(self.h, self.m); self.guard()

    def cells(self):
        o = self.org
        return frozenset((int(a) + o[0], int(b) + o[1], int(c) + o[2]) for a, b, c in zip(*np.nonzero(self.h)))

    def image_distance(self):
        p = np.argwhere(self.h).astype(np.int64); best = None
        for T in itertools.product((-1, 0, 1), repeat=3):
            if T <= (0, 0, 0):
                continue
            q = p + np.array(T) * np.array(self.shape)
            d = int(np.abs(p[:, None, :] - q[None, :, :]).max(2).min())
            best = d if best is None else min(best, d)
        return best


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
    if only in args:
        args.remove(only)
    d = json.load(open(args[0] if args else os.path.join(HERE, 'objects', 'osc-call-P3.15f.json')))
    tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
    N, first, wall = d['N'], d['first'], d['wall']
    osc = [frozenset(map(tuple, x)) for x in d['osc_even']]
    free = [frozenset(map(tuple, x)) for x in d['osc_free']]
    stators = [tuple(c) for c in d['stators']]

    def wire(word):
        assert len(word) == N
        cells = {tr(tuple(c), first - 4) for c in d['capL']} | {tr(tuple(c), first + N) for c in d['capR']}
        for i, ch in enumerate(word):
            h = int(ch, 16)
            cells |= {tr(c, first + i) for c in stators} | {tr(tuple(d['sites'][j]), first + i) for j in range(4) if h >> j & 1}
        return cells

    def state(word, t):
        assert t % 2 == 0
        w = wire(word); ob = osc[(t // 2) % 3]
        assert not (w & ob)
        return frozenset(w | ob)

    ok_all = True
    # the oscillator alone: one orbit of period exactly 3; beside the wire: a junction
    b = Box(free[0]); o1 = []
    for _ in range(3):
        b.step(); o1.append(b.cells())
    osc_ok = o1[0] == free[1] and o1[1] == free[2] and o1[2] == free[0] and len(set(free)) == 3
    osc_ok &= osc[0] == free[0] and osc[2] == free[1] and osc[1] <= free[2]
    plain = '7' * N
    b = Box(state(plain, 0)); pair_ok = True
    for t in range(1, 7):
        b.step()
        if t % 2 == 0:
            pair_ok &= b.cells() == state(plain, t)
    print(('PASS' if osc_ok and pair_ok else 'FAIL') + f'  the oscillator alone has period exactly 3 ({[len(x) for x in free]} cells); beside plain '
          f'wire the pair is plain wire + osc_even at generations 2, 4, 6; absent from the free oscillator at generations = 2 mod 6: '
          f'{sorted(free[2] - osc[1])}')
    ok_all &= osc_ok and pair_ok
    for run in d['runs']:
        if only and run['name'] != only:
            continue
        t0 = time.time(); ok = True; msgs = []
        start = state(run['start'], 0)
        box = Box(start); dist = box.image_distance()
        ops = {g: [tuple(c) for c in cells] for g, cells in run['ops']}
        checks = {}
        for g, wd in run['checks']:
            checks.setdefault(g, []).append(wd)
        # the start state alone has period exactly 6
        b2 = Box(start); per = []
        for t in range(1, 7):
            b2.step(); per.append(b2.cells() == start)
        if per != [False] * 5 + [True]:
            ok = False; msgs.append('start state is not of period exactly 6')
        last = run['start']; nchecks = 0
        for t in range(run['T'] + 1):
            for wd in checks.get(t, []):
                nchecks += 1
                if box.cells() != state(wd, t):
                    ok = False; msgs.append(f'check at generation {t} fails')
                last = wd
            for c in ops.get(t, []):
                u = c[0] >> 1
                st = [tr(s, u) for s in stators]
                far = all(abs(u - (first + i)) >= 10 for i, ch in enumerate(last) if ch in 'df') and abs(u - wall) >= 10
                rule = c != st[0] or (t % 2 == 0 and (t + u) % 3 == (wall + 2) % 3)
                if c not in st or not far or not rule or t % 2 or box.h[box.ix(c)] != 1:
                    ok = False; msgs.append(f'operation at generation {t} is not allowed: {c}')
                box.h[box.ix(c)] = 0
            if t < run['T']:
                box.step()
        ok_all &= ok
        print(('PASS' if ok else 'FAIL') + f'  {run["name"]}: {nchecks} checks, {sum(len(v) for v in ops.values())} cells removed, '
              f'{run["T"]} generations; torus {box.shape}, nearest image of a start cell {dist} sites; {time.time() - t0:.0f} s'
              + ('; ' + '; '.join(msgs[:3]) if msgs else ''), flush=True)
    print('ALL PASS' if ok_all else 'SOME FAIL')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
