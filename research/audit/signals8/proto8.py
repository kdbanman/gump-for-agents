#!/usr/bin/env python3
"""proto8 (REVIEW-signals-8): the memory cell and its protocol rebuilt on reference/oracle.py alone.

    python3 proto8.py [--long 20000] [--only A,B,...]

Every step is oracle.step on a rectangular array in which nothing wraps (a8.Orc; its margin is asserted dead after
every generation).  States are compared as whole sets of live cells with states laid from letters (a8.cell_state):
capL + family units from unit 4 + the cell's right cap.  From the push: the cap cells, the stators and sites only.
Operations: R@u / L@u = remove the stator (0,1,2) / (0,1,4) of unit u (it must be live).  Places are wire places
(place p = unit 4 + p).  Prints PASS / FAIL / NOTE lines and a last line ALL PASS or SOME FAIL.

Sections:
  A  the empty cell stands: period exactly 2, 38 + 5N cells, N = 4..30; N = 7 followed for --long generations
  B  set: the push's operation on N = 7; every pair R@u, L@v in one generation on N = 9
  C  add one / bit read / count read on a cell written by signals only (set, three adds, read): N = 24
  D  count read, every k that fits (N = 24, k = 1..20): the state at every even generation, then the empty cell
  E  transfer
  F  every state reached above is exactly periodic with period 2 (so it stands for ever)
  G  what the push's table does not say (each found with st8 in tables8.py, here on the oracle):
       operations next to a cap, pairs closer than three units, pulses one unit apart, a pulse sent into a
       count read, the stretch against the caps, the fixed sender
"""
import sys, time
import numpy as np
import a8
from a8 import tr, SR, SL

T0 = time.time()
OK = [True]


def say(ok, text):
    if ok is None:
        print(f'NOTE {text}  [{time.time() - T0:.0f} s]', flush=True); return
    OK[0] &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - T0:.0f} s]', flush=True)


def R(u):
    return tr(SR, u)


def L(u):
    return tr(SL, u)


class Run:
    """one oracle run of a cell of N wire units; self.h is the state at generation self.g"""

    def __init__(self, word, rcap=None):
        self.N = len(word); self.rcap = rcap
        self.O = a8.Orc(-6, self.N + 16)
        self.h = self.O.arr(a8.cell_state(word, rcap)); self.g = 0

    def to(self, g):
        assert g >= self.g
        self.h = self.O.run(self.h, g - self.g); self.g = g
        return self

    def kill(self, *cells):
        for c in cells:
            self.O.kill(self.h, c)
        return self

    def add(self, *cells):
        for c in cells:
            assert self.h[self.O.idx(c)] == 0; self.O.flip(self.h, [c])
        return self

    def cells(self):
        return self.O.cells(self.h)

    def letters(self):
        return a8.letters_of(self.cells(), 4, 4 + self.N)

    def is_word(self, word):
        return self.cells() == a8.cell_state(word, self.rcap)

    def stands(self):
        """exactly periodic with period 2 (and not 1)"""
        h1 = self.O.run(self.h, 1); h2 = self.O.run(h1, 1)
        return np.array_equal(h2, self.h) and not np.array_equal(h1, self.h)

    def desc(self):
        w = self.letters()
        return w if ('?' not in w and '_' not in w and self.is_word(w)) else f'[{a8.rle(w)}: {len(self.cells())} cells]'


def first_time(run, word, gmax, step=2):
    """first generation (a multiple of `step` from now) at which the whole state is the cell with `word`"""
    while run.g <= gmax:
        if run.is_word(word):
            return run.g
        run.to(run.g + step)
    return None


def secA(long_gens):
    ok = True
    for N in range(4, 31):
        r = Run('7' * N)
        ok &= len(r.cells()) == 38 + 5 * N and r.stands()
    say(ok, 'A  the empty cell (capL + 7^N + right cap) has 38 + 5N cells and period exactly 2 for N = 4..30 (so it stands for ever)')
    r = Run('7' * 7); h0 = r.h.copy(); ok = True
    for g in range(2, long_gens + 1, 2):
        r.to(g); ok &= np.array_equal(r.h, h0)
    say(ok, f'A  N = 7 (73 cells): equal to the start at every even generation up to {long_gens}')
    r = Run('777ddf7'); h0 = r.h.copy(); ok = True
    for g in range(2, long_gens + 1, 2):
        r.to(g); ok &= np.array_equal(r.h, h0)
    say(ok, f'A  N = 7 holding 2 (777ddf7): equal to the start at every even generation up to {long_gens}')


def secB():
    r = Run('7' * 7).kill(R(5), L(10))
    t = first_time(r, '777df77', 200)
    say(t is not None and r.stands(), f"B  set on N = 7: R@5 and L@10 at generation 0 give exactly 777df77 from generation {t} on (period 2)")
    N = 9; tab = {}
    for u in range(4, 4 + N):
        for v in range(4, 4 + N):
            if u == v:
                continue
            r = Run('7' * N).kill(R(u), L(v)).to(240)
            tab[(u - 4, v - 4)] = r.desc()
    setp = {k for k, d in tab.items() if d.count('d') == 1 and d.replace('7', '') == 'df'}
    emp = {k for k, d in tab.items() if d == '7' * N}
    want_set = {(p, q) for p in range(1, N - 1) for q in range(p + 3, N, 2)}
    say(setp == want_set, f'B  N = 9, every pair R@p, L@q (places 0..8) in one generation: exactly the pairs with 1 <= p, q - p odd and >= 3 '
        f'leave one df ({len(setp)} pairs), with d at place (p + q - 1)/2: {all(tab[k].index("d") == (k[0] + k[1] - 1) // 2 for k in setp)}')
    want_emp = {(p, q) for p in range(1, N - 1) for q in range(2, N) if (q - p >= 4 and (q - p) % 2 == 0) or q <= p - 2}
    say({k for k in emp if k[0] >= 1} == want_emp, f'B  ... the empty cell again, for 1 <= p <= {N - 2}, exactly when q >= 2 and (q - p even and >= 4: the pulses pass; or q <= p - 2: they part): {len(want_emp)} pairs')
    rest = {k: d for k, d in tab.items() if k not in setp and k not in emp}
    dead = sorted(k for k, d in rest.items() if d.endswith(': 12 cells]'))
    want_dead = {(p, q) for p in range(N) for q in range(N) if p != q and (p == N - 1 or q <= 1 or (q - p == 2 and p >= 1))}
    say(set(dead) == want_dead, f'B  CORRECTION to "u\' - u even: they pass": {len(dead)} pairs burn the whole cell down to 12 cells: every pair with q - p = 2 (p >= 1), with q <= 1, or with p = {N - 1}')
    other = {k: a8.rle(d) for k, d in rest.items() if k not in dead}
    say(all(abs(k[0] - k[1]) == 1 or k[0] == 0 for k in other) and all(k in other for k in tab if abs(k[0] - k[1]) == 1 and 1 <= k[0] <= N - 2 and k[1] >= 2),
        f'B  ... and {len(other)} pairs leave another object (every pair with |q - p| = 1 away from the caps, and pairs with p = 0): e.g. (3,4): {other.get((3, 4))}; (4,3): {other.get((4, 3))}; (0,4): {other.get((0, 4))}')
    for p in range(N):
        print('      p=%d: ' % p + ' '.join('%-12s' % ('--' if p == q else ('E' if tab[(p, q)] == '7' * N else a8.rle(tab[(p, q)]))[:12]) for q in range(N)))


def secC():
    N = 24
    r = Run('7' * N).kill(R(8), L(21))
    t = first_time(r, '7' * 10 + 'df' + '7' * 12, 200); states = [('set', r.g, r.letters())]
    say(t is not None, f'C  set (R@8, L@21): df with d at place 10 from generation {t}')
    # bit read of the set cell from the left: absorbed, and nothing ever differs to the right of the edge
    g0 = r.g; r.kill(R(6)); quiet = True
    ref = a8.cell_state('7' * 10 + 'df' + '7' * 12)
    for g in range(g0, g0 + 120):
        r.to(g + 1)
        cur = r.cells()
        quiet &= {c for c in cur ^ ref if a8.unit(c) >= 4 + 13} == set() or (r.g % 2 == 1)
    say(r.is_word('7' * 9 + 'ddf' + '7' * 12) and quiet, 'C  add one / bit read "full" (R@6): the pulse is absorbed, count 2, and at no even generation does any unit right of the edge differ from the standing cell')
    r.kill(L(27)); r.to(r.g + 120)
    say(r.is_word('7' * 9 + 'dddf' + '7' * 11), 'C  add one from the right (L@27): count 3, the edge one unit to the right')
    r.kill(R(5)); r.to(r.g + 120)
    say(r.is_word('7' * 8 + 'ddddf' + '7' * 11), 'C  add one from the left (R@5): count 4, the wall one unit to the left')
    stands = r.stands()
    # count read
    g0 = r.g; r.kill(R(4 + 7)); seen = []
    for g in range(g0 + 2, g0 + 200, 2):
        r.to(g); w = r.letters()
        if r.is_word(w) and set(w) <= set('7b'):
            seen.append((g - g0, w))
    trains = sorted({w.strip('7') for _, w in seen if 'b' in w}, key=len)
    full = [(g, w) for g, w in seen if w.count('b') == 4]
    say(bool(full) and all(w.strip('7') == 'b7b7b7b' for g, w in full) and stands,
        f"C  count read (R@11, the unit before the wall at place 8): from generation +{full[0][0] if full else None} the whole state is the empty cell with exactly 4 units b, two apart "
        f"({len(full)} even generations); as capL swallows them the trains seen are {trains}")
    t = next((g for g, w in seen if set(w) == {'7'}), None)
    say(t is not None and r.stands(), f'C  ... and the cell is exactly the empty cell from generation +{t} after the read')
    # bit read, empty
    r2 = Run('7' * N).kill(R(6)); far = None
    for g in range(2, 140, 2):
        r2.to(g); w = r2.letters()
        if '6f' in w and far is None and w.index('6') >= 18 and r2.is_word(w):
            far = (g, w.index('6'))
    say(far is not None and r2.is_word('7' * N), f'C  bit read "empty" (R@6 on the empty cell): the pulse 6f is at place {far[1] if far else None} at generation {far[0] if far else None}, whole state exact; then the right cap swallows it: the empty cell')


def secD():
    ok = True; times = []; K = 20
    for k in range(1, K + 1):
        N = 3 * k + 12; p = N - k - 2          # the stretch at the right end, one unit of wire after its edge; 2k + 10 units before it
        word = '7' * p + 'd' * k + 'f' + '7'
        r = Run(word)
        if not r.stands():
            ok = False; continue
        r.kill(R(4 + p - 1)); good = 0
        for g in range(2, 4 * k + 22, 2):
            r.to(g)
            lead = p + 2 - g // 2               # place of the leading pulse
            want = ['7'] * N
            for j in range(k):
                if lead + 2 * j < N:
                    want[lead + 2 * j] = 'b'
            hit = lead + 2 * (k - 1) < N and r.is_word(''.join(want))
            if g >= 2 * k + 6:
                good += hit; ok &= hit
            else:
                ok &= not hit
        r.to(8 * k + 160)
        ok &= r.is_word('7' * N) and r.stands()
        times.append(good)
    say(ok, f'D  count read for k = 1..{K} (N = 3k + 12, 2k + 10 units of wire before the wall): at every even generation t from 2k + 6 to 4k + 20 the whole state is the '
        f'empty cell with exactly k units b two apart, the leading one at place (wall + 2 - t/2), and at no even generation before 2k + 6; at 8k + 160 exactly the empty cell, period 2 '
        f'(whole-state checks per k: {min(times)}..{max(times)})')


def secE():
    N = 24
    r = Run('7' * 4 + 'df' + '7' * 8 + 'dddf' + '7' * 6)
    st = r.stands(); r.kill(R(17)); r.to(160)
    say(st and r.is_word('7' * 4 + 'ddddf' + '7' * 15) and r.stands(), 'E  transfer: stores 1 (place 4) and 3 (place 14); count read of the right one; the left one holds 4 and the right one is gone')
    ok = True
    for k in range(1, 9):
        w = '7' * 3 + 'df' + '7' * 4 + 'd' * k + 'f' + '7' * 2
        w += '7' * (N - len(w))
        r = Run(w); r.kill(R(4 + 8)); r.to(4 * k + 160)
        ok &= r.is_word('7' * 3 + 'd' * (k + 1) + 'f' + '7' * (N - 5 - k)) and r.stands()
    say(ok, 'E  ... k = 1..8 into a receiver df four units of wire away: the receiver holds k + 1 (it grows on the side the pulses come from, into the place the store has left)')
    out = []
    for gap in (1, 2, 3):
        for k in (1, 2, 5):
            w = '7' * 3 + 'df' + '7' * gap + 'd' * k + 'f'
            w += '7' * (N - len(w))
            r = Run(w); r.kill(R(4 + 5 + gap - 1)); r.to(4 * k + 200)
            out.append((gap, k, a8.rle(r.desc())))
    say(None, f'E  receiver and store closer together (gap of wire between the receiver\'s edge and the store\'s wall, k): {out}')


def secG():
    N = 12
    # 1. operations next to a cap
    res = {}
    for nm, f in (('R', R), ('L', L)):
        for p in (0, 1, N - 2, N - 1):
            r = Run('7' * N).kill(f(4 + p)).to(400)
            res[(nm, p)] = r.desc()
    bad = {k: v for k, v in res.items() if v != '7' * N}
    say(set(bad) == {('R', 0), ('R', N - 1), ('L', 0), ('L', 1)},
        f'G1 CORRECTION: on the empty N = 12 cell one stator removed at generation 0 next to a cap does not make a pulse the far cap swallows: {bad}; '
        f'so R@u needs 5 <= u <= N + 2 and L@u needs 6 <= u <= N + 3')
    # 2. adjacent pulses are counted once
    w = '7' * 12 + 'df' + '7' * 10
    r = Run(w).kill(R(8)).to(2).kill(R(8)).to(12)
    mid = r.letters()
    r.to(200)
    say('6ef' in mid and r.is_word('7' * 11 + 'ddf' + '7' * 10),
        f'G2 CORRECTION: R@8 at generations 0 and 2 puts two pulses one unit apart on the wire (letters 6ef at generation 12: {a8.rle(mid)}) and the store goes from 1 to 2, not 3')
    r = Run(w).kill(R(8)).to(4).kill(R(8)).to(200)
    say(r.is_word('7' * 10 + 'dddf' + '7' * 10), 'G2 ... the same stator at generations 0 and 4 (pulses two units apart): 1 to 3')
    out = []
    for train, add in (('6ef', 1), ('6eef', 2), ('6eeef', 2), ('6eeeef', 3), ('6f6f', 2), ('6f6f6f', 3)):
        ww = '7' * (12 - 4 - len(train)) + train + '7' * 4 + 'df' + '7' * 10
        r = Run(ww).to(200)
        out.append((train, r.is_word('7' * (12 - add) + 'd' * (1 + add) + 'f' + '7' * 10)))
    for train, add in (('bb', 1), ('bbb', 2), ('bbbb', 2), ('bbbbb', 3), ('b7b', 2), ('b7b7b', 3)):
        ww = '7' * 6 + 'df' + '7' * 4 + train
        ww += '7' * (24 - len(ww))
        r = Run(ww).to(200)
        out.append((train, r.is_word('7' * 6 + 'd' * (1 + add) + 'f' + '7' * (24 - 8 - add))))
    say(all(v for _, v in out), f'G2 ... formed trains into df: a block of m pulses one unit apart (6e^(m-1)f from the left, b^m from the right) adds ceil(m/2): {out}')
    # 3. a pulse sent into a count read
    out = []
    for D in (4, 5, 8, 9):
        ww = '7' * (20 - D - 2) + '6f' + '7' * D + 'ddd' + 'f' + '7' * 6
        r = Run(ww).kill(R(4 + 19)).to(400)
        out.append((D, r.desc()))
    exp = {4: '7' * 18 + 'dddf' + '7' * 8, 8: '7' * 16 + 'dddf' + '7' * 10, 5: '7' * 30, 9: '7' * 30}
    say(all(d == exp[D] for D, d in out), 'G3 a right-going pulse D units before the wall of d^3 f when the count read starts: D = 5, 9: it passes the three pulses and the cell ends empty; '
        'D = 4, 8: it stops the first, the mark absorbs the other two, and the store stands again with count 3, D/2 units to the left')
    # 4. the stretch against the caps, and the fixed sender
    out = []
    for k in (1, 3):
        r = Run('d' * k + 'f' + '7' * (N - k - 1)); t = first_time(r, '7' * N, 200)
        r2 = Run('7' + 'd' * k + 'f' + '7' * (N - k - 2)); r3 = Run('7' * (N - k - 1) + 'd' * k + 'f')
        out.append((k, t, r2.stands(), r3.stands()))
    say(all(t == 4 * k + 4 and a and b for k, t, a, b in out), f'G4 a stretch laid with its first unit next to capL is erased (the empty cell from generation 4k + 4); one unit away it stands; with its edge '
        f'unit as the last wire unit (against the right cap) it stands: {out}')
    r = Run('7' * 6 + 'df' + '7' * 4); log = []
    for shot in range(1, 7):
        r.kill(R(6)); r.to(r.g + 120); log.append(r.desc().strip('7') or 'empty')
    say(log == ['ddf', 'dddf', 'ddddf', 'empty', 'empty', 'empty'],
        f'G5 the fixed sender: the same operation R@6 six times, 120 generations apart, on a store df at place 6: {log} (three adds; the fourth is the count read, as the wall '
        f'has come next to the sender; then the cell is empty and the pulses cross it)')
    r = Run('7' * 2 + 'df' + '7' * 8); log = []
    for shot in range(1, 5):
        try:
            r.kill(R(5)); r.to(r.g + 160); log.append(r.desc())
        except AssertionError:
            log.append('stator not live'); break
    say(None, f'G5 a sender at place 1 (R@5) with df at place 2: {[a8.rle(x) for x in log]}')


def secF():
    ok = True
    for w in ['777df77', '777ddf7', '7' * 10 + 'df' + '7' * 12, '7' * 9 + 'ddf' + '7' * 12, '7' * 9 + 'dddf' + '7' * 11, '7' * 8 + 'ddddf' + '7' * 11,
              '7' * 4 + 'df' + '7' * 8 + 'dddf' + '7' * 6, '7' * 4 + 'ddddf' + '7' * 15] + ['7' + 'd' * k + 'f' + '7' * (22 - k) for k in range(1, 22)]:
        ok &= Run(w).stands()
    say(ok, 'F  every stored state used above, and 7 d^k f 7^(22-k) for k = 1..21 on N = 24, is exactly periodic with period 2: each stands for ever')


def main():
    long_gens = int(sys.argv[sys.argv.index('--long') + 1]) if '--long' in sys.argv else 20000
    only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else list('ABCDEFG')
    for s, f in (('A', lambda: secA(long_gens)), ('B', secB), ('C', secC), ('D', secD), ('E', secE), ('F', secF), ('G', secG)):
        if s in only:
            f()
    print('ALL PASS' if OK[0] else 'SOME FAIL')
    sys.exit(0 if OK[0] else 1)


if __name__ == '__main__':
    main()
