#!/usr/bin/env python3
"""beyond9 (review of signals push 9): the call line outside the push's runs.  Stepper st9.c; `--orc` replays every
row whose class is marked * on reference/oracle.py (a9.Orc) and compares the whole state at every even generation.

    python3 beyond9.py dist            the pair launched 3..21 units before the crossing
    python3 beyond9.py offsets         the wall at CROSS + 1 + o, o = -8..10, k = 1..6: does it stand, what a CALL does
    python3 beyond9.py words           one pulse, the pair, three, four, spaced pairs, left-going pulses of the line
    python3 beyond9.py pulse           a CALL while a pulse of the store wire is near the crossing
    python3 beyond9.py write           a CALL while a set or an add is under way
    python3 beyond9.py twice           two CALLs d generations apart
    python3 beyond9.py left            pulses that reach an armed store from the left (they pass under the line)

Geometry: store wire on units 4..4+N-1 with the push's caps; the line fixed, crossing unit CROSS = 35; e1 (the one
cell a pair makes live beside the crossing unit) appears 29 generations after a CALL seeded at line unit 6.
An outcome is read at generation T and T + 2: `word` if the whole state is exactly store letters + the line at rest,
with the number of pulses that left through the left cap counted on the way (units b crossing unit 8).
"""
import sys, time
from a9 import *

N, FIRST = 64, 4
ORC = '--orc' in sys.argv
c = CROSS


def W(k, o=0, extra=''):
    w = list('7' * N)
    for j in range(k):
        w[c + 1 + o + j - FIRST] = 'd'
    if k:
        w[c + 1 + o + k - FIRST] = 'f'
    return ''.join(w)


def seed(u=6):
    return [q for q in lstep(CALL, u - 6)]


def outcome(start, ops, T=700, lines=LINE):
    """returns (class, text, passed) ; passed = number of units b seen at store unit 8 at even generations"""
    s = frozenset(start); passed = 0; hist = {}
    for g in range(T + 3):
        if g in ops:
            r, m = frozenset(ops[g][0]), frozenset(ops[g][1])
            if not (r <= s) or (m & s):
                return 'n/a', f'operation at {g} does not apply', 0, hist
            s = (s - r) | m
        if g % 2 == 0:
            hist[g] = s
            u8 = {tr(q, -8) for q in s if q[0] >> 1 == 8 and 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5}
            if u8 == unit_cells(0xb, 0):
                passed += 1
        if g == T:
            sT = s
        s = run(s, 1, cap=60000)
        if s is None or len(s) > 3000:
            return 'burn', 'more than 3000 cells', passed, hist
    line_ok = lines <= sT
    w = letters(sT - lines, N, FIRST) if line_ok else None
    if line_ok and sT == wire(w.replace('?', '7'), first=FIRST) | lines and '?' not in w:
        return ('store' if s == run(sT, 3) else 'moving'), rle(w), passed, hist
    per = s == run(sT, 3)
    return ('standing-other' if per else 'changing'), f'{len(sT)} cells, line {"as it was" if line_ok else "changed"}' + \
        (f', store letters {rle(letters(sT - lines, N, FIRST))}' if line_ok else ''), passed, hist


def orc_same(start, ops, hist, T):
    o = play(start, ops, T, engine='orc')
    return all(o[g] == hist[g] for g in range(0, T + 1, 2))


def row(name, start, ops, T=700, lines=LINE, mark=False):
    cls, text, passed, hist = outcome(start, ops, T, lines)
    extra = ''
    if ORC and mark and cls != 'n/a':
        To = min(T, 300)
        t0 = time.time()
        extra = f'   [oracle: whole state equal at every even generation 0..{To}: {orc_same(start, ops, hist, To)}; {time.time() - t0:.0f} s]'
    print(f'{name:<46} {cls:<15} out {passed}  {text}{extra}', flush=True)
    return cls, text, passed


def dist():
    print('# the pair seeded at line unit u (crossing unit 21): k = 3 armed')
    for u in range(0, 19):
        row(f'seed at line unit {u}', wire(W(3)) | LINE, {0: ([], seed(u))}, mark=u in (0, 18))
    print('# the pair laid as the word 9df with its 9 at line unit u')
    for u in range(0, 19):
        row(f'9df at line unit {u}', with_lword(wire(W(3)) | LINE, '9df', u), {})


def offsets():
    print('# stretch d^k f with its first unit at CROSS + 1 + o; "stands" = period 2 with the line; then a CALL')
    for o in range(-8, 11):
        for k in range(1, 7):
            S = wire(W(k, o)) | LINE
            st = run(S, 2) == S
            if not st:
                cls, text, p = row(f'o = {o:+d} k = {k}: does NOT stand; left alone', S, {}, mark=(k == 3))
            else:
                row(f'o = {o:+d} k = {k}: stands; CALL', S, {0: ([], seed())}, mark=(k == 3 and o in (-1, 1, 0)))


def words():
    print('# words of the line, their first letter at line unit 6 (right-going) or their last at unit 24 (left-going)')
    rg = ['9f', '9df', '9ddf', '9dddf', '9ddddf', '9f9f', '9fb9f', '9fbb9f', '9fbbb9f', '9df9f', '9f9df', '9dfb9f', '9fb9df',
          '9df9df', '9dfb9df', '9dfbb9df', '9dfbbb9df']
    lg = ['7', '77', '777', '7b7', '7bb7', '7bbb7']
    for k in (0, 1, 2, 3, 5):
        for w in rg:
            S = with_lword(wire(W(k)) | LINE, w, 6)
            row(f'k = {k} right-going {w}', S, {}, mark=(k in (0, 3) and w in ('9f', '9ddf', '9f9f', '9fb9f')))
        for w in lg:
            S = with_lword(wire(W(k)) | LINE, w, 25 - len(w))
            row(f'k = {k} left-going {w}', S, {}, mark=(k in (0, 3) and w in ('7', '77')))


def pulse():
    print('# CALL at generation 0 (e1 at 29) and one pulse of the store wire born at generation 0 at unit CROSS + a')
    for k in (0, 1, 3):
        for a in list(range(-28, -1)):
            row(f'k = {k} R@CROSS{a:+d}', wire(W(k)) | LINE, {0: ([RST(c + a)], seed())}, mark=(k == 3 and a in (-14, -13, -5)) or (k == 0 and a in (-15, -14, -13)))
        for a in range(k + 4, 27):
            row(f'k = {k} L@CROSS{a:+d}', wire(W(k)) | LINE, {0: ([LST(c + a)], seed())}, mark=(k == 3 and a in (8, 9, 14)) or (k == 0 and a in (14, 15, 16)))
    print('# controls: the same pulses and no CALL')
    for k in (0, 1, 3):
        for a in (-20, -9, -2):
            row(f'k = {k} R@CROSS{a:+d}, no CALL', wire(W(k)) | LINE, {0: ([RST(c + a)], [])})
        for a in (k + 4, k + 9):
            row(f'k = {k} L@CROSS{a:+d}, no CALL', wire(W(k)) | LINE, {0: ([LST(c + a)], [])})


def write():
    print('# a set under way: R@CROSS-a and L@CROSS+a+3 at generation 0 (they stop each other at CROSS + 1, CROSS + 2); CALL at 0')
    for a in range(2, 27):
        row(f'set a = {a}', wire(W(0)) | LINE, {0: ([RST(c - a), LST(c + a + 3)], seed())}, mark=a in (11, 12, 13, 14, 15))
    print('# an add under way: armed d^k f, L@(edge + a) at generation 0; CALL at 0')
    for k in (1, 2, 3, 5):
        for a in range(2, 27):
            row(f'add k = {k} a = {a}', wire(W(k)) | LINE, {0: ([LST(c + 1 + k + a)], seed())}, mark=(k == 2 and a in (12, 13, 14, 15, 16)))


def twice():
    print('# two CALLs: seeds at line unit 6 at generations 0 and d')
    for k in (0, 1, 2, 3, 5, 8):
        for d in list(range(6, 64, 2)):
            row(f'k = {k} second CALL {d} generations later', wire(W(k)) | LINE, {0: ([], seed()), d: ([], seed())},
                mark=(k == 3 and d in (6, 8, 10, 12, 14, 20)))
    print('# two pairs laid as words: 9df at line unit 12 and another s units behind it')
    for k in (0, 3):
        for s in range(3, 12):
            S = with_lword(with_lword(wire(W(k)) | LINE, '9df', 12), '9df', 12 - s)
            row(f'k = {k} pairs {s} units apart', S, {})


def left():
    print('# an armed store hit from the left: R@CROSS-a at generation 0, no CALL; then a CALL at generation 200')
    for k in (1, 2, 3):
        for a in (4, 5, 9, 16):
            row(f'k = {k} R@CROSS-{a}', wire(W(k)) | LINE, {0: ([RST(c - a)], [])}, mark=(k == 3 and a == 9))
            row(f'k = {k} R@CROSS-{a}, CALL at 200', wire(W(k)) | LINE, {0: ([RST(c - a)], []), 200: ([], seed())}, mark=(k == 3 and a == 9))


if __name__ == '__main__':
    t0 = time.time()
    {'dist': dist, 'offsets': offsets, 'words': words, 'pulse': pulse, 'write': write, 'twice': twice, 'left': left}[sys.argv[1]]()
    print(f'# {time.time() - t0:.0f} s')
