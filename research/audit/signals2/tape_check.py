"""Tape theorem (README section 10), tested on the oracle with words and ring lengths the study did not use.

    python3 tape_check.py            (about 2 min)

A ring of L units of the 3x3 tube along v=(1,0,-1), each unit B or C (cells at an even generation, unit 0):
  B: (0,1,2) (0,1,4) (1,0,0) (1,0,2) (1,0,4)      C: (0,1,2) (0,1,4) (0,2,3) (1,0,0) (1,0,2)
is put on the oracle's box torus (2L, 16, 2L).  There the ring's copies differ by 2L >= 12 in x+z and by 16 in y,
while a neighbour changes x+z by at most 4 and y by at most 2, and it is checked at every generation that no live
cell lies outside the tube 1 <= x+y+z, x-y+z <= 5 (taken modulo the box): so the box run IS the ring.
Claim: after 2j generations the state is the start moved j units towards -v, for j = 1 .. L + 4 (a lap and more).
"""
import sys
import numpy as np
import gs
oracle = gs.oracle
B = [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]
C = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]


def cells(word):
    return [gs.tr(c, u) for u, ch in enumerate(word) for c in (B if ch == 'B' else C)]


def test(word, extra=4):
    L = len(word); shape = (2 * L, 16, 2 * L); m = gs.box_masks(shape)
    idx = np.indices(shape)
    # tube modulo the box: x + z taken in a representative window, y in [-2,2]
    y = np.where(idx[1] >= 8, idx[1] - 16, idx[1])
    xz = (idx[0] + idx[2]) % (2 * L)
    s1 = xz + y; s2 = xz - y
    tube = (s1 >= 1) & (s1 <= 5) & (s2 >= 1) & (s2 <= 5)
    h0 = gs.to_arr(cells(word), shape); h = h0.copy(); ok = True; inside = True
    for j in range(1, L + extra + 1):
        h = oracle.step(h, m); inside &= not (h.astype(bool) & ~tube).any()
        h = oracle.step(h, m); inside &= not (h.astype(bool) & ~tube).any()
        exp = gs.to_arr(cells(word[j % L:] + word[:j % L]), shape)
        if not (h == exp).all():
            ok = False; break
    return ok and inside, (ok, inside, j)


rng = np.random.default_rng(2026)
words = []
for L in (6, 7, 9, 11, 13, 16, 23, 32, 41):
    for _ in range(3):
        words.append(''.join(rng.choice(['B', 'C'], L)))
words += ['B' * 19 + 'C', 'C' * 19 + 'B', 'B' * 10 + 'C' * 10, 'BC' * 10, 'BBC' * 7, 'B' * 12, 'C' * 12,
          'B' * 7 + 'C' * 2 + 'B' * 6 + 'C' * 9, 'C' * 30 + 'B' * 3]
allok = True
for w in words:
    good, info = test(w)
    allok &= good
    print('PASS' if good else 'FAIL', f'L={len(w):2d} {w}', '' if good else info, flush=True)
print('ALL PASS' if allok else 'SOME FAILED')
sys.exit(0 if allok else 1)
