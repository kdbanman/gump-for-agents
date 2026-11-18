#!/usr/bin/env python3
"""fast7 (the review's C ring stepper) against the oracle on the helix torus, bit for bit at every generation.

    python3 fastcheck.py        (about 1 min)

(1) 12 random soups in the 5 x 5 tube on rings of 96, 120 and 160 units (densities 0.15..0.5), 60 generations each;
(2) the push's line N = 80 alone and with E and 0..3 holes, 300 generations;
(3) six ends of the C <= 37 list (own enumeration) on a finite train with each of three events (a hole word, a down
    signal, the wire-B edge), 260 generations, ring of 448 units.
"""
import json, os, random
import numpy as np
import orc7 as O, fast7, lines as Ln


def same(T, R, cells, flips, G):
    h = T.arr(cells); x = R.arr(cells)
    for t in range(G + 1):
        if t in flips:
            T.flip(h, flips[t]); R.flip(x, flips[t])
        if T.outside(h) != 0 or not np.array_equal(T.units(h), x):
            return False
        if t < G:
            h = T.step(h); x = R.step(x)
    return True


def main():
    ok = True; rnd = random.Random(3)
    for k in range(12):
        L = (96, 120, 160)[k % 3]; dens = rnd.uniform(0.15, 0.5)
        cells = [O.tr(c, u) for u in range(L) for c in O.BASE if rnd.random() < dens]
        r = same(O.Tor.helix(L, 0), fast7.Ring(L, 0), cells, {}, 60)
        ok &= r; print(('PASS' if r else 'FAIL'), f'soup {k}: ring of {L} units, density {dens:.2f}, {len(cells)} cells, 60 generations')
    y0, E, H = Ln.push_line()
    for n in (None, 0, 1, 2, 3):
        fl = {} if n is None else {1: [O.tr(c, 32) for c in E] + [O.tr(c, 48 + 6 * j) for j in range(n) for c in H]}
        r = same(O.Tor.helix(160, -34), fast7.Ring(160, -34), y0, fl, 300)
        ok &= r; print(('PASS' if r else 'FAIL'), f'line N=80 {"alone" if n is None else f"with E and {n} holes"}, 300 generations')
    import census7a as CA
    d = json.load(open(os.path.join(O.SCR, 'fb_37.json')))
    C = CA.Census('fb')
    for i in rnd.sample(range(len(d['list'])), 6):
        cap = [tuple(c) for c in d['list'][i]]
        cells = O.train0('fb', C.ulo, CA.KS) | frozenset(cap)
        for ev in (('word', (0, 2)), ('sig', 'K0'), ('wireB', None)):
            t0, fl = C.flips(ev)
            r = same(O.Tor.helix(448, C.ua), fast7.Ring(448, C.ua), cells, {t0: fl}, 260)
            ok &= r; print(('PASS' if r else 'FAIL'), f'end (list entry {i}) with event {ev}, ring 448, 260 generations')
    print('ALL PASS' if ok else 'SOME FAIL')


if __name__ == '__main__':
    main()
