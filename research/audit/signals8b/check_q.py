#!/usr/bin/env python3
"""check_q.py: q.c (the audit's sparse stepper) against reference/oracle.py, cell for cell, every generation.

    python3 check_q.py          (about 1 min)

A  six soups (densities 0.15 to 0.7, a 16^3 block of doubled coordinates) on a cubic torus H = 80, 12 generations
   (the speed limit keeps them 4 sites from the seam: asserted by Box.step), and the pure-python set stepper too
B  push 8b's line object: line0 of objects/read-echo-B-line.json with the E-and-2-holes write at generation 1,
   generations 0..400, box torus thin in y
C  the store-and-reader of case n = 1 of that object with its probe, 80 generations (cells taken at generation 0 from
   the JSON store of objects/read-echo-B-small.json: needs no line)
D  a wrong rule is noticed: the oracle with B45/S34 differs from q.c on a soup
"""
import time
import numpy as np
import qa
from qa import oracle


def compare(cells, box, gens, flips=None, label='', third=False):
    flips = flips or {}
    h = box.arr(cells); k = qa.pk(cells); s = frozenset(cells)
    for t in range(gens + 1):
        if t in flips:
            box.flip(h, flips[t]); k = qa.xor(k, qa.pk(flips[t])); s = s ^ frozenset(flips[t])
        if not qa.same(box.keys(h), k):
            print(f'    {label}: q.c differs from the oracle at generation {t}'); return False
        if third and qa.pk(s).tolist() != k.tolist():
            print(f'    {label}: step_py differs at generation {t}'); return False
        if t < gens:
            h = box.step(h); k = qa.run(k, 1)
            if third:
                s = qa.step_py(s)
    return True


def main():
    ok = True; t0 = time.time()
    rng = np.random.default_rng(20261118)
    good = True
    for rho in (0.15, 0.25, 0.35, 0.45, 0.55, 0.7):
        cells = [(x, y, z) for x in range(-8, 8) for y in range(-8, 8) for z in range(-8, 8) if qa.is_cell((x, y, z)) and rng.random() < rho]
        good &= compare(cells, qa.Box((80, 80, 80), (40, 40, 40)), 12, label=f'soup {rho}', third=True)
    print('PASS' if good else 'FAIL', f'A  six soups, 12 generations, oracle = q.c = step_py at every generation ({time.time() - t0:.0f} s)'); ok &= good

    t1 = time.time()
    ob = qa.obj('read-echo-B-line')
    line0 = [tuple(c) for c in ob['line0']]
    st = ob['cases'][1]['store']
    flips = {f[0]: [tuple(c) for c in f[1]] for f in st['flips']}
    box = qa.Box.around(line0, 12)
    good = compare(line0, box, 400, flips=flips, label='line')
    print('PASS' if good else 'FAIL', f'B  the line with E and 2 holes (flips at generation {sorted(flips)}), generations 0..400, box {box.shape} ({time.time() - t1:.0f} s)'); ok &= good

    t1 = time.time()
    ob = qa.obj('read-echo-B-small')
    good = True
    for case in ob['cases']:
        cells = [tuple(c) for c in case['store']['cells']] + [tuple(c) for c in case['reader']]
        box = qa.Box.around(cells, 14)
        good &= compare(cells, box, case['probe_gen'] + 80, flips={case['probe_gen']: [tuple(c) for c in case['probe']]}, label=case['label'])
    print('PASS' if good else 'FAIL', f'C  short store + reader + probe, both cases, 100 generations ({time.time() - t1:.0f} s)'); ok &= good

    cells = [(x, y, z) for x in range(-8, 8) for y in range(-8, 8) for z in range(-8, 8) if qa.is_cell((x, y, z)) and rng.random() < 0.4]
    box = qa.Box((80, 80, 80), (40, 40, 40))
    h = box.arr(cells); k = qa.pk(cells); differs = False
    for t in range(8):
        h = oracle.step(h, box.m, survive=(3, 4)); k = qa.run(k, 1)
        differs |= not qa.same(box.keys(h), k)
    print('PASS' if differs else 'FAIL', 'D  the oracle run with the wrong rule B45/S34 differs from q.c'); ok &= differs
    print(('ALL PASS' if ok else 'SOME FAIL') + f'  ({time.time() - t0:.0f} s)')


if __name__ == '__main__':
    main()
