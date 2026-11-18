#!/usr/bin/env python3
"""check8 (push 8): lab8's stepper against reference/oracle.py, bit for bit, on push 7's line.

    python3 check8.py [--gens 900] [--n 0,1,2,3,4]

For each record line-N80-gun4-end70-n{1..4} of ../push7/objects7.json (the 419-cell line; E and n holes flipped in
at generation 1; n = 0 here means the line alone, no flips) the run is made twice: with oracle.step on the box torus
2L x 16 x 2L (L = 100 units; the tube along (1,0,-1) closes into a ring; masks by oracle.masks' own formula for a
non-cubic box) and with lab8 (dead outside the box).  The two whole states are compared as sets of cells at every
generation 0..gens.  Also: lab8's ring mode against the oracle on a ring of wire B with one pulse (cubic torus
H = 64, 200 generations), and lab8 against the pure-Python set stepper on a random soup in a box (40 generations).
Prints PASS/FAIL lines and ALL PASS.
"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle, lab8


def box_masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


class Torus:
    """oracle.step on a box torus (2L, HY, 2L); cells are taken mod the box"""
    def __init__(self, L, HY=16):
        self.shape = (2 * L, HY, 2 * L); self.m = box_masks(self.shape)

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            i = tuple(c[k] % self.shape[k] for k in range(3)); assert any(m[i] for m in self.m), c
            h[i] = 1
        return h

    def flip(self, h, cells):
        for c in cells:
            i = tuple(c[k] % self.shape[k] for k in range(3)); h[i] ^= 1

    def step(self, h):
        return oracle.step(h, self.m)

    def key(self, h):
        return frozenset(zip(*[v.tolist() for v in np.nonzero(h)]))

    def keyof(self, cells):
        return frozenset(tuple(c[k] % self.shape[k] for k in range(3)) for c in cells)


def main():
    gens = int(sys.argv[sys.argv.index('--gens') + 1]) if '--gens' in sys.argv else 900
    ns = [int(v) for v in sys.argv[sys.argv.index('--n') + 1].split(',')] if '--n' in sys.argv else [0, 1, 2, 3, 4]
    d = json.load(open(os.path.join(HERE, '..', 'push7', 'objects7.json')))
    R = {r['name']: r for r in d['records']}
    ok_all = True
    for n in ns:
        r = R['line-N80-gun4-end70-n%d' % max(n, 1)]
        y0 = [tuple(c) for c in r['y0']]
        flips = {f[0]: [tuple(c) for c in f[1]] for f in r['flips']} if n else {}
        T = Torus(100); h = T.arr(y0)
        L = lab8.Lab(-8, 92); a = L.arr(y0)
        t0 = time.time(); bad = None
        for g in range(gens + 1):
            if g in flips:
                T.flip(h, flips[g]); L.flip(a, flips[g])
            if T.key(h) != T.keyof(L.cells(a)):
                bad = g; break
            if g < gens:
                h = T.step(h); L.run(a, 1)
        ok = bad is None and not L.touch
        ok_all &= ok
        print(('PASS' if ok else 'FAIL') + f' push-7 line, n = {n}: lab8 == oracle on the whole state at every generation 0..{gens}'
              + ('' if ok else f' (first difference at generation {bad}, touch {L.touch})') + f'  [{time.time() - t0:.0f} s; {int(h.sum())} cells at the end]', flush=True)
    # ring mode: wire B with one pulse on a cubic torus H = 64 (a ring of 32 units)
    WB = [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]
    H = 64; m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
    cells = set(lab8.tr(c, u) for u in range(32) for c in WB) ^ {(13, 0, -12), (14, 2, -11)}
    for c in cells:
        h[c[0] % H, c[1] % H, c[2] % H] = 1
    L = lab8.Lab(0, 32, ring=True); a = L.arr(cells); bad = None
    for g in range(201):
        k1 = frozenset(zip(*[v.tolist() for v in np.nonzero(h)])); k2 = frozenset((c[0] % H, c[1] % H, c[2] % H) for c in L.cells(a))
        if k1 != k2:
            bad = g; break
        h = oracle.step(h, m); L.run(a, 1)
    ok = bad is None; ok_all &= ok
    print(('PASS' if ok else f'FAIL at {bad}') + ' ring mode: wire B with pulse B on a ring of 32 units, lab8 == oracle (H = 64) for 200 generations')
    # dead mode against the pure-Python set stepper on soup
    rng = np.random.default_rng(8); L = lab8.Lab(-12, 12, -24, 24, -24, 24)
    soup = [(x, y, z) for x in range(-8, 8) for y in range(-8, 8) for z in range(-8, 8) if lab8.is_cell((x, y, z)) and rng.random() < 0.4]
    a = L.arr(soup); s = frozenset(soup); bad = None
    for g in range(40):
        s = lab8.step_set(s); L.run(a, 1)
        if L.cells(a) != s:
            bad = g; break
    ok = bad is None and not L.touch; ok_all &= ok
    print(('PASS' if ok else f'FAIL at {bad}') + f' dead mode: soup of {len(soup)} cells, lab8 == set stepper for 40 generations ({len(s)} cells left)')
    print('ALL PASS' if ok_all else 'SOME FAIL')


if __name__ == '__main__':
    main()
