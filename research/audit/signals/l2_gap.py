#!/usr/bin/env python3
"""L2 audit, rate: how close together can two shots at A be?  Same set-up as l2_transmission.py (ring of 48 cubes,
oracle.step); A flipped at generation 4 and again at 4 + g; after 200 generations: stationary?, how many record cells
(2 per pulse received), and the whole state compared with the single-shot record moved one more cube.

    nice -n 10 python3 l2_gap.py
"""
import json, subprocess
from lat import ring_torus, wire, ROOT

ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'bcd5844:research/signals/objects/transmission-B.json']))
N = 48; T = ring_torus(N)
bare0 = wire([tuple(c) for c in ob['bg']], 0, N)
recv = frozenset(tuple(c) for c in ob['receiver']); A = T.mod(tuple(ob['flip']))


def run(shots, T_end=220):
    x = T.arr(bare0 ^ recv); b = T.arr(bare0)
    for t in range(T_end):
        if t in shots:
            x[A] ^= 1
        x = T.step(x); b = T.step(b)
    x2 = T.step(T.step(x))
    d = T.cells(x) ^ T.cells(b)
    return (x2 == x).all(), len(d), sorted(set((c[0] // 2) % N for c in d))


base = run([4])
print('one shot: stationary %s, %d cells differ, cubes %s' % base)
for g in list(range(1, 21)) + [30, 40]:
    st, n, cubes = run([4, 4 + g])
    verdict = 'two pulses received' if st and n == base[1] + 2 and cubes[0] == base[2][0] - 1 else 'NOT two clean receptions'
    print(f'gap {g:2d}: stationary {st}, {n} cells differ, cubes {cubes[0]}..{cubes[-1]}: {verdict}', flush=True)
