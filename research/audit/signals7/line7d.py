#!/usr/bin/env python3
"""Variants of the push's line experiment (oracle, helix ring; conventions of line7b.py).

    python3 line7d.py        (1 min)

(1) other lengths: N = 82, 84, 86, 122 (the push used multiples of 4);
(2) another up-signal in place of E at unit 32: U, N1, the pair EE; alone and with 1, 2, 3 holes from 48, 3 rakes apart;
(3) another down-signal in front of E: K0, K3 (D2), N2 (D5), N4, HH (D3) at unit 48 (+ its parity), alone and followed
    by holes at 54, 60.
Kinds from signals7_5f.json (checked to ride by kinds7.py).
"""
import numpy as np
import orc7 as O, lines as Ln, census7a as CA
from line7b import Lab, rle


def main():
    K = CA.kinds('5f')
    for N in (82, 84, 86, 122):
        lab = Lab(N)
        row = []
        for w in ([48], [48, 54], [48, 54, 60], [48, 52, 60], [48, 60, 62, 64]):
            r = lab.run(32, w); row.append(f'{w}: {lab.sig(r)} (from {r["g0"]})')
        print(f'N={N} ({int(lab.alone.sum())} cells), E at 32: ' + '; '.join(row), flush=True)
    lab = Lab()
    for up in ('U', 'N1', 'EE'):
        for w in ([], [48], [48, 54], [48, 54, 60]):
            fl = {1: [O.tr(c, 32) for c in K[up]['cells']] + [O.tr(c, p) for p in w for c in lab.H]}
            g0, per, U, h, t = Ln.settle(lab.T, lab.y0, fl, lab.Gmax)
            r = dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum()))
            same = g0 is not None and t % 4 == 0 and np.array_equal(U, lab.alone)
            print(f'{up} at 32, holes {w}: {"the line as it was (running)" if same else lab.sig(r)} (period {per} from {g0}; {r["pop"]} cells)', flush=True)
    for dn in ('K0', 'D2', 'D5', 'N4', 'D3'):
        for w in ([], [54], [54, 60]):
            fl = {1: [O.tr(c, 32) for c in lab.E] + [O.tr(c, 48) for c in K[dn]['cells']] + [O.tr(c, p) for p in w for c in lab.H]}
            g0, per, U, h, t = Ln.settle(lab.T, lab.y0, fl, lab.Gmax)
            r = dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum()))
            print(f'E at 32, {dn} at 48, holes {w}: {lab.sig(r)} (period {per} from {g0}; {r["pop"]} cells)', flush=True)
    # (4) E meets N2 (D5) on the bare train (ring of 240 units): what is left
    T = O.Tor.helix(240, 0)
    canon = lambda D: sorted(O.tr(c, -(min(O.unit(x) for x in D) - min(O.unit(x) for x in D) % 2)) for c in D)
    res = []
    for off in range(6, 42, 2):
        h = T.step(T.arr(O.train0('5f', 0, 240)))
        T.flip(h, [O.tr(c, 100) for c in lab.E] + [O.tr(c, 100 + off) for c in K['D5']['cells']])
        G = 4 * ((off + 40) // 4) + 1                       # a generation = 1 mod 4 well after they have met
        h = T.step(h, G - 1)
        tr = T.units(T.step(T.arr(O.train0('5f', 0, 240)), G))
        D = sorted(O.ucells(T.units(h) ^ tr, 0))
        res.append((off, [n for n, k in K.items() if sorted(k['cells']) == canon(D)] if D else ['nothing']))
    print('E at unit 100, N2 (the four-cell down signal D5) at unit 100 + off, ring of 240 units: what the difference from the train is afterwards:')
    print('   ' + ', '.join(f'off {o}: {"/".join(k) if k else "?"}' for o, k in res))


if __name__ == '__main__':
    main()
