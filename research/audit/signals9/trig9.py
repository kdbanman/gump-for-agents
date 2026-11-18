#!/usr/bin/env python3
"""trig9 (review of signals push 9): the still life at the wall, on reference/oracle.py (a9.Orc) with this review's
own states, places and checks.  From objects/trigger9.json only cells: `trig` (the six cells, for a stretch whose
first unit is unit 0) and the `extra` cells of the runs clear, one and sum.

    python3 trig9.py [A B C D E F]
  A  d^k f with the still life at its wall, k = 1..8, the pulse born 12 and 13 units before the wall: what leaves
  B  the same without the still life
  C  a second store 12 units to the left: what it holds afterwards (the block is worth k + 1)
  D  the still life one unit further from the stretch: block and worth
  E  the hazard: no stretch; a right-going and a left-going pulse at the bare still life
  F  the cube (clear), S6b elsewhere (one), two still lifes (sum): the push's start states, this review's checks
"""
import sys, json, time
from a9 import *

_T = json.load(open(os.path.join(P9, 'trigger9.json')))
TRIG = [tuple(q) for q in _T['trig']]
RUNS = {r['name']: r for r in _T['runs']}
N, FIRST = 46, 4
WALL = 30
OK = True


def say(ok, text):
    global OK
    OK &= bool(ok)
    print(('PASS  ' if ok else 'FAIL  ') + text, flush=True)


def word(stores, n=N):
    """stores: list of (first unit, k)"""
    w = list('7' * n)
    for u, k in stores:
        for j in range(k):
            w[u + j - FIRST] = 'd'
        w[u + k - FIRST] = 'f'
    return ''.join(w)


def trig(wall, shift=0):
    return frozenset(tr(q, wall + shift) for q in TRIG)


def follow(start, rem, fixed, T, n=N):
    """oracle run; returns (first exact state with b and no d/f: its letters, final letters or None, st9 equal)"""
    o = Orc(start); s = frozenset(start)
    for q in rem:
        o.remove(q)
    s = s - set(rem)
    seen = None; same = True
    for t in range(T + 1):
        x = o.cells()
        same &= x == s
        if t % 2 == 0 and seen is None and fixed <= x:
            lw = letters(x - fixed, n, FIRST)
            if '?' not in lw and x == wire(lw, first=FIRST) | fixed and 'b' in lw and 'd' not in lw and 'f' not in lw:
                seen = lw
        if t < T:
            o.step(); s = run(s, 1)
    x = o.cells()
    lw = letters(x - fixed, n, FIRST) if fixed <= x else None
    fin = lw if lw and '?' not in lw and x == wire(lw, first=FIRST) | fixed else None
    o.step(2)
    return seen, (fin if o.cells() == x else None), same, o


def part_A():
    for k in range(1, 9):
        for p in (0, 1):
            t0 = time.time()
            S = wire(word([(WALL, k)])) | trig(WALL)
            st = Orc(S).step(2).cells() == S
            seen, fin, same, o = follow(S, [RST(WALL - 12 - p)], trig(WALL), 220)
            blk = seen.strip('7') if seen else None
            say(st and blk == 'b' * (2 * k + 2) and fin == '7' * N and same,
                f'A  k = {k}, pulse born {12 + p} units before the wall: the stretch stands beside the still life; what leaves: '
                f'{rle(blk) if blk else None} (b^(2k+2) = b^{2 * k + 2}); 220 generations on: plain wire and the still life; '
                f'st9 = oracle at every generation: {same}; nearest image {o.image_distance()}; {time.time() - t0:.0f} s')


def part_B():
    for k in (1, 3, 6):
        S = wire(word([(WALL, k)]))
        seen, fin, same, o = follow(S, [RST(WALL - 12)], frozenset(), 120)
        say(fin == word([(WALL - 1, k + 1)]) and same, f'B  k = {k} without the still life: the pulse is absorbed: {rle(fin) if fin else None}')


def part_C():
    for k in range(1, 7):
        for kl in (1, 2):
            left = WALL - 14 - kl
            S = wire(word([(left, kl), (WALL, k)])) | trig(WALL)
            seen, fin, same, o = follow(S, [RST(WALL - 10)], trig(WALL), 260)
            say(fin == word([(left, kl + k + 1)]) and same,
                f'C  stores {kl} and {k} (the still life at the wall of the right one), one cell removed between them: '
                f'{rle(fin) if fin else None}: the left store holds {kl} + {k} + 1')


def part_D():
    for k in (1, 2, 3, 5):
        left = WALL - 16
        S = wire(word([(left, 1), (WALL, k)])) | trig(WALL, -1)
        st = Orc(S).step(2).cells() == S
        seen, fin, same, o = follow(S, [RST(WALL - 11)], trig(WALL, -1), 280)
        say(st and fin == word([(left, 1 + k + 3)]) and same,
            f'D  the still life one unit further from the stretch, k = {k}: stands {st}; the left store (1) ends as '
            f'{rle(fin) if fin else None}: 1 + k + 3')
    for sh, name in ((1, 'one unit nearer'), (2, 'two units nearer'), (-2, 'two units further')):
        S = wire(word([(WALL, 3)])) | trig(WALL, sh)
        s2 = run(S, 2); s200 = run(S, 200)
        print(f'      [st9] the still life {name}: d^3 f stands with it: {s2 == S}; left alone 200 generations: '
              f'{"unchanged" if s200 == S else str(len(s200)) + " cells, letters " + rle(letters(s200 - trig(WALL, sh), N, FIRST))}')


def part_E():
    S = wire('7' * N) | trig(WALL)
    st = Orc(S).step(2).cells() == S
    for name, rem in (('right-going', [RST(WALL - 12)]), ('right-going, born one unit earlier', [RST(WALL - 13)]),
                      ('left-going', [LST(WALL + 8)]), ('left-going, born one unit later', [LST(WALL + 9)])):
        o = Orc(S, pad=40); s = S - set(rem)
        for q in rem: o.remove(q)
        same = True
        for t in range(70):
            o.step(); s = run(s, 1); same &= o.cells() == s
        s = run(s, 330)
        fin = s == S
        print(f'      E  plain wire + the still life (stands: {st}), a {name} pulse: st9 = oracle for 70 generations: {same}; '
              f'400 generations on [st9]: {"everything restored" if fin else str(len(s)) + " cells (start " + str(len(S)) + "), still life " + ("there" if trig(WALL) <= s else "gone") + ", letters " + rle(letters(s, N, FIRST))}')


def part_F():
    for name, T in (('clear', 240), ('one', 240), ('sum', 320), ('loop', 240), ('call-far', 240), ('smallest-loop', 320)):
        r = RUNS[name]; n = r['N']; fixed = frozenset(map(tuple, r['extra']))
        S = wire(r['start'], first=FIRST) | fixed
        o = Orc(S); st = Orc(S).step(2).cells() == S
        for g, rem in r['ops']:
            assert g == 0
            for q in rem: o.remove(tuple(q))
        o.step(T); x = o.cells()
        lw = letters(x - fixed, n, FIRST) if fixed <= x else None
        exact = bool(lw) and x == wire(lw, first=FIRST) | fixed
        o.step(2)
        say(st and exact and o.cells() == x, f'F  {name}: {rle(r["start"])} + {len(fixed)} cells beside the wire stands; '
            f'{len(r["ops"][0][1])} cell(s) removed; {T} generations on the whole state is exactly {rle(lw) if lw else None} + the same cells')


if __name__ == '__main__':
    for p in ([a for a in sys.argv[1:] if a in 'ABCDEF'] or list('ABCDEF')):
        globals()['part_' + p]()
    print('ALL PASS' if OK else 'SOME FAIL')
