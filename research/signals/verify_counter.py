#!/usr/bin/env python3
"""Verify with reference/oracle.py that the wall 8|C counts pulses p<: each pulse arriving from the C side moves
the wall one unit towards it, and nothing else changes.

    python3 verify_counter.py            (about 20 s)

A ring of N = 48 units of the 3 x 3 tube on the box torus (96, 20, 96) (oracle.step on a box, as in sg.oracle_run):
units 0..11 hold wire 8 (the stators (0,1,2), (0,1,4) and (0,2,3)), units 12..47 wire C; the wall C|8 at 47|0 is
stationary too.  Pulses p< (a unit of wire B in wire C) are put on units listed below, at spacings 2 to 5.  Claim:
after 2*(48) generations the state is exactly the ring with wire 8 on units 0..11+n and wire C on the rest, n the
number of pulses; and at every even generation in between nothing but the travelling pulses and the wall differs
from that description (checked: at the end, cell for cell)."""
import sg, scat, family as F
tr = scat.tr
def uc(m, u):
    return {tr(c, u) for c in F.STATOR} | {tr(F.SITES[i], u) for i in range(4) if m >> i & 1}
N = 48; shape = (2 * N, 20, 2 * N)
ok_all = True
for pulses in ([20], [20, 22], [20, 23, 26, 30, 34], [18, 20, 22, 24, 26, 28, 30], [14, 19, 25, 27, 33, 38, 41, 44]):
    def ring(w, P=()):
        cells = set()
        for u in range(N):
            cells |= uc(0x8 if u < w else (0x7 if u in P else 0xb), u)
        return frozenset(((c[0]) % shape[0], (c[1] + 10) % shape[1], c[2] % shape[2]) for c in cells)
    start = ring(12, pulses); want = ring(12 + len(pulses))
    last = None
    for t, st in sg.oracle_run(start, shape, 2 * N + 4, every=2):
        last = st
    ok = last == want
    ok_all &= ok
    print('PASS' if ok else 'FAIL', f'pulses at units {pulses}: after {2 * N + 4} generations the wall has moved {len(pulses)} units, the rest exactly as it was')
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED', '- counter 8|C')
