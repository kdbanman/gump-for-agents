#!/usr/bin/env python3
"""Check st.c (the sparse stepper of push 8b) cell for cell against reference/oracle.py.

    python3 check_st.py            (about 4 min; the line is the slow part)
    python3 check_st.py --quick    (skips the push-7 line: 20 s)

A  random soups (three densities, a 14^3 block of doubled coordinates in a cubic torus H = 72, 40 generations);
B  a pulse on a capped wire: the second push's register (objects/register-BBp.json) with one write, 100 generations,
   cubic torus H = 96;
C  push 7's line (objects7.json, record line-N80-gun4-end70-n2: 419 cells, E and 2 holes flipped at generation 1),
   every generation 0..920 on the box torus 280 x 16 x 280 of push 7's own verifier;
D  the ring mode of st.c: pulse B on a ring of 40 units (objects/pulse-B.json) against the oracle on H = 80, 100
   generations.
The oracle run is oracle.step on the array torus; st.c runs on the infinite lattice (or its ring).  Compared: the
set of live cells at every generation (st's cells reduced mod the torus, which must be injective).
Prints PASS/FAIL per check and ALL PASS.
"""
import json, os, sys, time
import numpy as np
import lab
sys.path.insert(0, os.path.join(lab.ROOT, 'reference'))
import oracle


def box_masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def arr(cells, shape):
    h = np.zeros(shape, np.int8)
    for c in cells:
        assert lab.is_cell(c)
        h[c[0] % shape[0], c[1] % shape[1], c[2] % shape[2]] = 1
    assert int(h.sum()) == len(cells), 'cells collide on the torus'
    return h


def compare(cells, shape, gens, flips=None, L=0, label=''):
    """flips: {generation: [cells]} applied to both.  Returns True if equal at every generation 0..gens."""
    flips = flips or {}
    m = box_masks(shape)
    h = arr(cells, shape)
    k = lab.pk(cells)
    t0 = time.time()
    for t in range(gens + 1):
        if t in flips:
            for c in flips[t]:
                h[c[0] % shape[0], c[1] % shape[1], c[2] % shape[2]] ^= 1
            k = lab.xor(k, lab.pk(flips[t]))
        mine = arr(lab.up(k), shape)
        if not np.array_equal(mine, h):
            print(f'    {label}: differ at generation {t}')
            return False
        if t < gens:
            h = oracle.step(h, m)
            k = lab.run(k, 1, L)
    return True


def main():
    quick = '--quick' in sys.argv
    ok = True
    rng = np.random.default_rng(1)
    good = True
    for rho in (0.2, 0.4, 0.6):
        cells = [(x, y, z) for x in range(30, 44) for y in range(30, 44) for z in range(30, 44)
                 if lab.is_cell((x, y, z)) and rng.random() < rho]
        good &= compare(cells, (72, 72, 72), 40, label=f'soup {rho}')
    print('PASS' if good else 'FAIL', 'A  three soups, 40 generations, torus H = 72'); ok &= good

    ob = lab.load('register-BBp')
    frame = [tuple(c) for c in (json.loads(ob['frame']) if isinstance(ob['frame'], str) else ob['frame'])]
    cells = set(frame)
    for u in range(ob['ua'], ob['ub']):
        cells |= {lab.tr(tuple(c), u) for c in (ob['B'] if u < ob['w0'] else ob['Bp'])}
    good = compare(sorted(cells), (96, 96, 96), 100, flips={0: [tuple(ob['write'])]}, label='register')
    print('PASS' if good else 'FAIL', 'B  the register with one write (a pulse B on a capped wire), 100 generations, torus H = 96'); ok &= good

    ob = lab.load('pulse-B')
    cells = {lab.tr(tuple(c), u) for c in ob['bg'] for u in range(40)}
    cells ^= {((c[0] % 80), c[1], c[2] + (c[0] - c[0] % 80)) for c in map(tuple, ob['defect'])}
    good = compare(sorted(cells), (80, 80, 80), 100, L=40, label='ring')
    print('PASS' if good else 'FAIL', 'D  ring mode: pulse B on a ring of 40 units, 100 generations, torus H = 80'); ok &= good

    if not quick:
        d = json.load(open(os.path.join(lab.SIG, 'push7', 'objects7.json')))
        r = next(r for r in d['records'] if r['name'] == 'line-N80-gun4-end70-n2')
        assert 'train' not in r
        cells = [tuple(c) for c in r['y0']]
        flips = {f[0]: [tuple(c) for c in f[1]] for f in r['flips']}
        t0 = time.time()
        good = compare(cells, (2 * r['L'], 16, 2 * r['L']), 920, flips=flips, label='line')
        print('PASS' if good else 'FAIL', f'C  push 7 line N = 80 with E and 2 holes, generations 0..920, torus 280 x 16 x 280 ({time.time() - t0:.0f} s)'); ok &= good
    print('ALL PASS' if ok else 'SOME FAIL')


if __name__ == '__main__':
    main()
