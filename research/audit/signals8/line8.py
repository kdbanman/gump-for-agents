#!/usr/bin/env python3
"""line8 (REVIEW-signals-8): the reads of push 7's line, rebuilt on the oracle, and the phases the push did not run.

    python3 line8.py

From the push: objects/line7-read.json (y0 = the 419 cells of push 7's line, writes[n] = the cells flipped at
generation 1 for E and n holes).  Stepping: a8.Orc (oracle.step, nothing wrapping).  A_n(g) = the line written with n
holes and left alone.  The standing line has period 4 (push 7's right cap), so a read is tried at T0 = 882 and at
T0 + 2 = 884 (the two phases at which a stator removal makes a pulse).

  A   A_n(882) = A_n(886), n = 1..5; the wire (units 4..79) reads 7^76 for n = 1 and 7^37 d^n f 7^(38-n) for n >= 2
  B   count read (stator (0,1,2) of unit 40 removed) at 882 and at 884, n = 1..4: the state 40 generations later
      (letters) and 221 generations later (whole state against A_1)
  C   bit read from the right (stator (0,1,4) of unit 70) at 882 and 884, n = 1..4; and from the left (stator (0,1,2)
      of unit 20) at 882 and 884, n = 1..3
"""
import sys, json, time
import numpy as np
import a8
from a8 import tr, SR, SL

T0g = time.time(); OK = [True]


def say(ok, text):
    if ok is None:
        print(f'NOTE {text}  [{time.time() - T0g:.0f} s]', flush=True); return
    OK[0] &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - T0g:.0f} s]', flush=True)


def main():
    d = json.load(open(a8.os.path.join(a8.PUSH, 'objects', 'line7-read.json')))
    O = a8.Orc(-8, 98)
    T0 = 882
    A = {}
    for n in range(1, 6):
        h = O.arr(map(tuple, d['y0']))
        (g, cells), = d['writes'][str(n)]
        h = O.run(h, g); O.flip(h, [tuple(c) for c in cells]); h = O.run(h, T0 - g)
        seq = [h]
        for _ in range(7):
            seq.append(O.run(seq[-1], 1))
        A[n] = seq                                           # A[n][i] = A_n(882 + i), i = 0..7
    lets = {n: a8.letters_of(O.cells(A[n][0]), 4, 80) for n in A}
    say(all(np.array_equal(A[n][4], A[n][0]) for n in A) and lets[1] == '7' * 76 and all(lets[n] == '7' * 37 + 'd' * n + 'f' + '7' * (38 - n) for n in range(2, 6)),
        f'A  the five written lines are periodic (period dividing 4) at 882; wire units 4..79: n = 1: 7^76; n = 2..5: 7^37 d^n f 7^(38-n); cells {[int(A[n][0].sum()) for n in A]}')
    per2 = {n: np.array_equal(A[n][2], A[n][0]) for n in A}
    say(None, f'A  period 2 exactly? {per2} (the right cap has period 4)')

    def A1(g):
        return A[1][(g - T0) % 4]

    def desc(h, g):
        c = O.cells(h)
        if np.array_equal(h, A1(g)):
            return 'the n = 1 line exactly'
        for m in range(2, 6):
            if np.array_equal(h, A[m][(g - T0) % 4]):
                return f'the n = {m} line exactly'
        w = a8.letters_of(c, 4, 80)
        capsok = {x for x in c if a8.unit(x) < 4 or a8.unit(x) >= 80} == {x for x in O.cells(A1(g)) if a8.unit(x) < 4 or a8.unit(x) >= 80}
        return f"[{a8.rle(w)}; {len(c)} cells; caps {'as in the n = 1 line' if capsok else 'CHANGED'}]"

    # B: count read at both phases
    for dt in (0, 2):
        res = {}
        for n in range(1, 5):
            h = A[n][dt].copy(); O.kill(h, tr(SR, 40)); g = T0 + dt
            h = O.run(h, 40); mid = a8.rle(a8.letters_of(O.cells(h), 4, 80).strip('7'))
            h = O.run(h, 181); res[n] = (mid, desc(h, g + 221))
        good = all(res[n][0] == ('b7' * n)[:-1] and res[n][1] == 'the n = 1 line exactly' for n in range(2, 5))
        say(good, f'B  count read at {T0 + dt}, n = 2, 3, 4: 40 generations later the wire carries exactly (b7)^n; 221 generations later the whole state is the n = 1 line')
        say(None, f'B  count read at {T0 + dt}, n = 1 (nothing stored): train after 40: {res[1][0]}; 221 later: {res[1][1]}')
    # C: bit read from the right and from the left
    for dt in (0, 2):
        res = {}
        for n in range(1, 5):
            h = A[n][dt].copy(); O.kill(h, tr(SL, 70)); h = O.run(h, 200); res[n] = desc(h, T0 + dt + 200)
        say(res[1] == 'the n = 1 line exactly' and all(res[n] == f'the n = {n + 1} line exactly' for n in (2, 3, 4)),
            f'C  bit read from the right (stator (0,1,4) of unit 70) at {T0 + dt}: n = 1: crosses, capL swallows, the n = 1 line; n = 2, 3, 4: absorbed, the line of n + 1 holes exactly')
        res = {}
        for n in range(1, 4):
            h = A[n][dt].copy(); O.kill(h, tr(SR, 20)); h = O.run(h, 300); res[n] = desc(h, T0 + dt + 300)
        say(None, f'C  bit read from the left (stator (0,1,2) of unit 20) at {T0 + dt}, 300 generations later: {res}')
    print('ALL PASS' if OK[0] else 'SOME FAIL')
    sys.exit(0 if OK[0] else 1)


if __name__ == '__main__':
    main()
