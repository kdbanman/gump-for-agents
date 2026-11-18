#!/usr/bin/env python3
"""check_st9 (review of signals push 9): this review's stepper st9.c and its oracle wrapper a9.Orc.

    python3 check_st9.py

1  st9.c = oracle.step (a9.Orc) = a pure-python set stepper, cell for cell at every generation, on six random soups
   (blobs of 10 to 14 cubes a side at three densities, 40 generations);
2  a wrong rule (B45/S34) is noticed on the same soups;
3  a9.Orc (rectangular torus, guard planes) = oracle.masks(H) / oracle.step on a cubic torus exactly as the oracle's
   own main uses them, on the store with the line and a CALL, k = 3, 70 generations;
4  st9.c ring mode = the oracle on a cubic torus of side 2R on which a wire closes on itself (R = 24, a ring of wire B
   with a stretch d^3 f and a right-going pulse, 120 generations).
The call line's own runs (st9 = oracle at every generation of every run) are in call_oracle.py, trig9.py, beyond9.py
--orc, coexist9.py --orc and extra9.py.
"""
import random
from a9 import *

OK = True


def say(ok, text):
    global OK
    OK &= bool(ok)
    print(('PASS  ' if ok else 'FAIL  ') + text, flush=True)


def soup(side, dens, seed):
    rnd = random.Random(seed); cells = set()
    for x in range(2 * side + 1):
        for y in range(2 * side + 1):
            for z in range(2 * side + 1):
                if (x & 1) + (y & 1) + (z & 1) == 1 and rnd.random() < dens:
                    cells.add((x, y, z))
    return frozenset(cells)


def step_wrong(cells):
    cnt = {}
    for q in cells:
        for n in nbrs(q):
            cnt[n] = cnt.get(n, 0) + 1
    return frozenset(q for q, n in cnt.items() if (n in (4, 5) and q not in cells) or (n in (3, 4) and q in cells))


def main():
    bad = 0; wrong_seen = 0; n = 0
    for i, (side, dens) in enumerate(((10, 0.2), (10, 0.38), (12, 0.5), (14, 0.3), (12, 0.38), (11, 0.6))):
        s = soup(side, dens, 100 + i)
        o = Orc(s, pad=90); a = s; b = s; wr = s; differs = False
        for t in range(40):
            o.step(); a = run(a, 1); b = step_set(b); wr = step_wrong(wr)
            x = o.cells()
            if not (x == a == b):
                bad += 1
            differs |= wr != x
            n += 1
        wrong_seen += differs
    say(bad == 0, f'1  st9.c = oracle = set stepper on six soups, {n} generations compared, {bad} differences')
    say(wrong_seen == 6, f'2  a wrong rule (B45/S34) differs from the oracle on {wrong_seen} of 6 soups')
    S = wire('7' * 32 + 'dddf' + '7' * 14) | LINE | set(CALL)
    say(cubic_check(S, 70), '3  a9.Orc = oracle.masks(H), oracle.step on a cubic torus: the store with the line and a CALL, k = 3, 70 generations')
    R = 24; H = 2 * R; m = oracle.masks(H)
    word = '7' * 10 + 'dddf' + '7' * 10
    cells = (wire(word, first=0, caps=False) - {RST(3)})
    h = np.zeros((H, H, H), np.int8)
    for q in cells:
        h[q[0] % H, q[1] % H, q[2] % H] = 1
    s = frozenset(cells); ok = True
    for t in range(120):
        h = oracle.step(h, m); s = run(s, 1, ring=R)
        k = frozenset((q[0] % H, q[1] % H, q[2] % H) for q in s)
        ok &= len(k) == len(s) and k == frozenset(zip(*[v.tolist() for v in np.nonzero(h)]))
    say(ok, '4  st9.c ring mode = the oracle on a cubic torus of side 48: a ring of 24 units with d^3 f and a pulse, 120 generations')
    print('ALL PASS' if OK else 'SOME FAIL')


if __name__ == '__main__':
    main()
