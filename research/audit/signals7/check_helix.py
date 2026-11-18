#!/usr/bin/env python3
"""The helix torus against the box (nothing wraps), on the oracle, cell for cell at every generation.

    python3 check_helix.py          (about 1 min)

Runs: (1) the two trains of the push's `bases` on a helix ring are orbits: period 4, and two generations move them
one unit (fb towards +v, 5f towards -v); (2) the push's line N = 80 (gun 4, end 70; 419 cells) alone and with E and
0..3 holes, 400 generations, box (units -30..120, margin asserted dead) against helix L = 160 and helix L = 240;
(3) a finite piece of the fb train with a 5 x 5 event (N4-like: one cell outside the 3 x 3 tube flipped), box against
helix, 120 generations.  Prints PASS/FAIL per run.
"""
import sys
import numpy as np
import orc7 as O


def line_events():
    r0 = O.record('line-N80-gun4-end70-alone')
    y0 = [tuple(c) for c in r0['y0']]
    f1 = [tuple(c) for c in O.record('line-N80-gun4-end70-n1')['flips'][0][1]]
    H = [c for c in f1 if O.unit(c) >= 48]
    E = [c for c in f1 if O.unit(c) < 48]
    assert len(H) == 1 and len(E) == 3
    return y0, E, H


def compare(cells0, flips, G, ua, ub, helixL, ulo):
    """flips: {generation: cells}.  Box and helix in lockstep; unit arrays compared on the common unit range."""
    B = O.Tor.box(ua, ub)
    hb = B.arr(cells0)
    res = []
    for L in helixL:
        Hx = O.Tor.helix(L, ulo)
        res.append((Hx, Hx.arr(cells0)))
    hb0 = hb
    ok = True
    for t in range(G + 1):
        if t in flips:
            B.flip(hb, flips[t])
            for Hx, hh in res:
                Hx.flip(hh, flips[t])
        B.check_margin(hb)
        assert B.outside(hb) == 0
        ub_ = B.units(hb)
        for Hx, hh in res:
            assert Hx.outside(hh) == 0
            uh = Hx.units(hh)
            # helix units ulo..ulo+L-1 ; box units ua..ub-1 (inside the helix range)
            a = uh[ua - ulo: ub - ulo]
            if not np.array_equal(a, ub_) or uh.sum() != ub_.sum():
                ok = False
        if t < G:
            hb = B.step(hb)
            res = [(Hx, Hx.step(hh)) for Hx, hh in res]
    return ok


def main():
    allok = True
    # (1) trains
    for fr, d in (('fb', 1), ('5f', -1)):
        T = O.Tor.helix(96, -48)
        h0 = T.arr(O.train0(fr, -48, 48)); h = h0
        u0 = T.units(h0)
        h = T.step(h, 2); u2 = T.units(h)
        moved = np.array_equal(np.roll(u0, d, axis=0), u2)
        h = T.step(h, 2)
        per = np.array_equal(h, h0)
        print(('PASS' if moved and per else 'FAIL'), f'train {fr}: two generations = one unit towards {d:+d}v: {moved}; period 4 on the ring: {per}; outside {T.outside(h)}')
        allok &= moved and per and T.outside(h) == 0
    # (2) the line
    y0, E, H = line_events()
    for n in (None, 0, 1, 2, 3):
        fl = {}
        if n is not None:
            fl = {1: E + [O.tr(c, 6 * j) for j in range(n) for c in H]}
        ok = compare(y0, fl, 400, -30, 120, (160, 240), -34)
        print(('PASS' if ok else 'FAIL'), f'line N=80, {"alone" if n is None else f"E and {n} holes"}: box == helix 160 == helix 240 at every generation 0..400')
        allok &= ok
    # (3) a 5 x 5 event on a finite piece of the fb train
    cells = O.train0('fb', -40, 40)
    out5 = [c for c in O.BASE if not O.in_tube(c, 1, 5)]
    for c in out5[:6]:
        ok = compare(cells, {1: [O.tr(c, 2)]}, 120, -60, 60, (160,), -80)
        print(('PASS' if ok else 'FAIL'), f'fb train piece, cell {c} of unit 2 (outside the 3 x 3 tube) flipped at generation 1: box == helix 160, generations 0..120')
        allok &= ok
    print('ALL PASS' if allok else 'SOME FAIL')


if __name__ == '__main__':
    main()
