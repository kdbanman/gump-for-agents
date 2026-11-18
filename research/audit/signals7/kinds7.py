#!/usr/bin/env python3
"""The signal kinds of the push's two files, and review 6's nine signals, in one frame (oracle only).

    python3 kinds7.py        (20 s)

(1) Every kind of signals7.json (absorber frame, train fb) and signals7_5f.json (gun frame, train 5f): the
    two-generation identity on a ring of 96 units, whole ring: train(1) xor D, two oracle steps on, equals train(3)
    xor D moved one unit in its direction (so it rides for ever), and its direction is the file's.
(2) Review 6's nine signals (gun frame; cells from research/audit/signals6/sig6.py, copied here) mapped into the
    absorber frame by the mirror M(x,y,z) = (z-4, y, x+4): the mirrored state is aligned with the fb train by search,
    stepped to train phase 1, and its difference from the train is looked up among the kinds of signals7.json.
    Printed: which of the nine the push's census of ends was sent, and which it was not.
"""
import numpy as np
import orc7 as O, census7a as CA
from lines import M

R6 = {  # review 6 (sig6.py): parity of the lowest unit, cells at phase 1 in the gun frame, direction (+1 = up, towards +v)
    'E': (0, [(1, 2, 2), (2, 0, 1), (2, 0, 3)], +1), 'U': (1, [(0, 0, 3)], +1),
    'H': (1, [(1, 2, 2)], -1), 'K0': (0, [(0, 0, 3)], -1),
    'K3': (0, [(0, 0, 3), (4, 0, 1)], -1), 'N1': (0, [(0, 0, 1), (1, 2, 2), (2, 0, 3)], +1),
    'N2': (0, [(0, 0, 3), (2, 0, 1), (2, 0, 3), (4, 0, 1)], -1), 'N3': (0, [(0, 0, 3), (2, 0, 1), (2, 0, 3), (4, 0, -1)], -1),
    'N4': (1, [(0, 0, 3), (1, 2, 2), (1, 2, 4)], -1)}
L = 96


def rides(frame, cells, u0):
    """Direction (+1: towards +v) in which train(1) xor cells (moved u0 units) rides rigidly, or None."""
    T = O.Tor.helix(L, 0)
    h = T.step(T.arr(O.train0(frame, 0, L)))
    t1 = T.units(h).copy()
    D = [O.tr(c, u0) for c in cells]
    T.flip(h, D)
    h2 = T.step(h, 2); t3 = T.units(T.step(T.arr(O.train0(frame, 0, L)), 3))
    d1 = T.units(h) ^ t1; d3 = T.units(h2) ^ t3
    assert T.outside(h2) == 0
    for d in (1, -1):
        if np.array_equal(np.roll(d1, d, axis=0), d3):
            return d
    return None


def main():
    ok = True
    for frame in ('fb', '5f'):
        K = CA.kinds(frame); tdir = 1 if frame == 'fb' else -1
        for n, k in K.items():
            d = rides(frame, k['cells'], 40)
            want = tdir if k['dir'] == 'down' else -tdir
            good = d == want; ok &= good
            print(('PASS' if good else 'FAIL'), f'{frame} {n:8s} {k["dir"]:4s} {len(k["cells"])} cells: rides {"towards +v" if d == 1 else ("towards -v" if d == -1 else "NOT RIGID")}')
    # review 6's signals in the gun frame, then mirrored
    K5 = CA.kinds('5f'); Kf = CA.kinds('fb')
    canon = lambda D: tuple(sorted(O.tr(c, -(min(O.unit(x) for x in D) - min(O.unit(x) for x in D) % 2)) for c in D))
    P = CA.patterns('fb')
    print('review 6 signal -> gun-frame kind of signals7_5f.json -> absorber-frame kind of signals7.json (sent to the ends?)')
    for name, (par, cells, d) in R6.items():
        g = rides('5f', cells, 40 + par)
        k5 = next((n for n, k in K5.items() if canon([O.tr(c, par) for c in cells]) == tuple(sorted(k['cells']))), None)
        # mirror: the 5f train xor signal at generation 1 on a finite piece, mirrored, aligned with the fb train
        T = O.Tor.helix(L, 0)
        h = T.step(T.arr(O.train0('5f', 0, L)))
        T.flip(h, [O.tr(c, 40 + par) for c in cells])
        S = T.cells(h)
        found = None
        for t in range(4):
            m = frozenset(M(c) for c in S)
            lo = min(O.unit(c) for c in m)
            for k in range(-8, 8):
                mm = frozenset(O.tr(c, k - lo) for c in m)       # now on units k .. k+L-1
                U = O.uarr([c for c in mm if 0 <= O.unit(c) < 20], 0, 20)
                for tt in range(4):
                    if np.array_equal(U, CA.train_arr('fb', tt, 0, 20)):
                        found = (mm, tt, k); break
                if found:
                    break
            if found:
                break
            S = None
        mm, tt, k = found
        # mm is an fb-frame state at fb-generation tt on units k..k+L-1 (a ring of L units): step to phase 1
        T2 = O.Tor.helix(L, k)
        h = T2.arr(mm); g2 = tt
        while g2 % 4 != 1:
            h = T2.step(h); g2 += 1
        Dm = [O.tr(O.BASE[i], int(u) + k) for u, i in zip(*np.nonzero(T2.units(h) ^ CA.train_arr('fb', 1, k, k + L)))]
        kf = next((n for n, kk in Kf.items() if canon(Dm) == tuple(sorted(kk['cells']))), None)
        sent = kf is not None and Kf[kf]['dir'] == 'down'
        updown = 'up' if d == 1 else 'down'
        print(f'  {name:3s} ({updown}, rides {g == d}): gun frame {k5}; absorber frame {kf}' + (f' = {sorted(canon(Dm))}' if kf is None else '') +
              ('' if updown == 'up' else ('; SENT to the ends' if sent else '; NOT among the census events')))
    print('ALL PASS' if ok else 'SOME FAIL')


if __name__ == '__main__':
    main()
