#!/usr/bin/env python3
"""The reflector (capA with C18.23a or C20.33c beside it, from research/audit/signals5/end_echo.json) sent words of
down-moving signals (README section 33).

    python3 reflect6.py        (about 2 min)

Object: the line of N = 40 units with the oscillator beside capA (echo6.reflector).  After 60 generations, at the
first generation at which the train on units 10..30 is at phase 1, the word is xored in (echo6.sig at units 21, 23,
...).  The run is compared with the undisturbed one (sg.step_set).  Printed: when the near end (units <= 4 and the
oscillator) is equal again to the undisturbed run, and the difference on units 3..30 at generation tw + 44 read as
signals (echo6.decompose), e.g. [('E', 7), ('E', 9)] = two echoes.
"""
import random
import echo6 as E, sg

N = 40


def trial(ri, word, G=44, extra=0):
    X, name = E.reflector(ri, N)
    for _ in range(60):
        X = sg.step_set(X)
    while E.phase_at(X, 10, 30) != 1:
        X = sg.step_set(X)
    Y = X
    for K, u in word:
        Y = Y ^ E.sig(K, u)
    near_ok = None
    for t in range(1, G + extra + 1):
        X = sg.step_set(X); Y = sg.step_set(Y)
    D = X ^ Y
    f = E.phase_at(X, 10, 30)
    mid = E.units(D, 3, 34)
    near = frozenset(c for c in D if E.unit_of(c) < 3)
    return name, f, (E.read_at(mid, f) if f in (1, 3) else 'phase %s' % f), len(near), len(mid)


if __name__ == '__main__':
    words = [[('H', 21)], [('H', 21), ('H', 23)], [('H', 21), ('H', 25)], [('H', 21), ('H', 27)],
             [('H', 21), ('H', 23), ('H', 25), ('H', 27)], [('K0', 20)], [('K0', 20), ('K0', 22)],
             [('H', 21), ('K0', 24)], [('K0', 20), ('H', 23)]]
    rnd = random.Random(1)
    for _ in range(4):
        words.append([('H', 21 + 2 * k) for k in range(6) if rnd.random() < 0.5] or [('H', 21)])
    for ri in (0, 2):
        for w in words:
            G = 2 * max(u for _, u in w) + 36
            name, f, r, nn, nm = trial(ri, w, G=G)
            print(f'{name}: word {w}: at +{G}: {nm} cells differ on units 3..33, {nn} below unit 3; read as {r}', flush=True)
