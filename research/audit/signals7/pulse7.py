#!/usr/bin/env python3
"""What a later pulse of wire B does to the standing line: at the stretch, at the gun cap, at the end cap (oracle).

    python3 pulse7.py        (4 min)

Lines: the push's (gun 4, end 70), the other four guns with end 70, and gun 4 with ends 3, 40, 729, 735 of
wireB_caps.json.  For each line two standing objects: the plain one (E and one hole) and the one with a stretch of
three units (E and three holes, 3 rakes apart), each taken at a generation = 0 mod 4.  Into each, one flip of a cell
that never changes in wire B, at phase 0..3:
    (0,1,2) of unit 20   (below the stretch)
    (0,1,4) of unit 60   (above the stretch)
and the same two cells at the other place.  Printed per (object, cell, unit): the outcome at each of the four phases
(the signature of line7b.Lab.sig: 'same', 'plain', 'unit:ddd..f', or OTHER with the population), and for the phase-0
run the first generation at which a difference from the unflipped object is seen at the end cap (units <= 5) and at
the gun cap (units >= 78): that says which way the flip sends something.
"""
import sys, json
import numpy as np
import orc7 as O, lines as Ln
from line7b import Lab


def trace(lab, base_h, cell, ph, Gmax=700):
    """Run base (a state at generation 0 mod 4) with one flip at generation ph; the first generations at which the
    difference from the unflipped run reaches the two caps."""
    T = lab.T
    a = base_h.copy(); b = base_h.copy(); lo = hi = None
    for t in range(Gmax):
        if t == ph:
            T.flip(b, [cell])
        if t >= ph:
            d = np.nonzero((T.units(a) != T.units(b)).any(1))[0]
            if len(d):
                if lo is None and d[0] + lab.ua <= 5:
                    lo = t
                if hi is None and d[-1] + lab.ua >= 78:
                    hi = t
            if lo is not None and hi is not None:
                break
        a = T.step(a); b = T.step(b)
    return lo, hi


def main():
    w = Ln.caps(); G = {g['i']: g['cap'] for g in w['guns']}; E = {e['i']: e['cap'] for e in w['receiving']}
    pairs = [(4, 70)] + [(g, 70) for g in (1, 3, 9, 10)] + [(4, e) for e in (3, 40, 729, 735)]
    for g, e in pairs:
        lab = Lab(80, gun=G[g], end=E[e])
        print(f'gun {g}, end {e}: {int(lab.alone.sum())} cells', flush=True)
        for n in (1, 3):
            holes = [48 + 6 * j for j in range(n)]
            g0, per, U, h, t = Ln.settle(lab.T, lab.y0, lab.flips(32, holes), lab.Gmax)
            assert g0 is not None and t % 4 == 0
            base = lab.T.cells(h)
            s0 = lab.sig(dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum())))
            for c, u in (((0, 1, 2), 20), ((0, 1, 4), 60), ((0, 1, 4), 20), ((0, 1, 2), 60)):
                cell = O.tr(c, u); outs = []
                for ph in range(4):
                    q0, per2, U2, h2, t2 = Ln.settle(lab.T, base, {ph: [cell]}, 900)
                    s = lab.sig(dict(g0=q0, per=per2, U=U2, t=t2, pop=int(U2.sum())))
                    outs.append('same' if s == s0 else s.replace(' period', ',').split(' units')[0])
                lo, hi = trace(lab, h, cell, 0)
                print(f'   object {s0:10s} flip {c} of unit {u}: ' + ' | '.join(outs) + f'   [phase 0: difference at the end cap from {lo}, at the gun cap from {hi}]', flush=True)


if __name__ == '__main__':
    main()
