#!/usr/bin/env python3
"""call_oracle (review of signals push 9): the call line rebuilt on reference/oracle.py (a9.Orc), nothing of the push
imported; from its JSON only the caps, the family cells, the 162 cells of the line and the two cells of the CALL.

    python3 call_oracle.py stand            A  store + line: period, union, nearest torus image
    python3 call_oracle.py call 1,2,3       B  a CALL for each k: three oracle runs (X: store + line + CALL; V: the
                                               store alone with ONE cell made live at generation 29; Lf: the line
                                               alone with the CALL) compared at every generation, and the law
    python3 call_oracle.py proto            C  set / add / CALL / again; a move between stores; chain; bus

The line is fixed in space; a store wire is `first`.. units of letters with the push's caps.  CROSS = 35 is the store
unit the line crosses; a stretch is armed when its first unit is CROSS + 1.
Every oracle state is also compared with this review's stepper st9.c at every generation (that is a check of st9).
"""
import sys, time
from a9 import *

E1 = add(tr((1, 2, 0), CROSS), (0, 0, 0))      # (71, 2, -70): the one cell the pair makes live at generation 29
T_E1 = 29
OK = True


def say(ok, text):
    global OK
    OK &= bool(ok)
    print(('PASS  ' if ok else 'FAIL  ') + text, flush=True)


def store(nL, k, nR, o=0, off=(0, 0, 0)):
    """a wire with nL plain units, d^k f, nR plain units, the first d at unit CROSS + 1 + o"""
    word = '7' * nL + ('d' * k + 'f' if k else '') + '7' * nR
    first = CROSS + 1 + o - nL
    return wire(word, first=first, off=off), word, first


def stand():
    for k in range(0, 9):
        W, word, first = store(32, k, 14)
        S = W | LINE
        o = Orc(S); d = o.image_distance()
        o.step(); s1 = o.cells(); o.step(); s2 = o.cells()
        a = Orc(W).step().cells(); b = Orc(LINE).step().cells()
        say(s2 == S and s1 != S and s1 == a | b and not (a & b) and s1 == run(S, 1),
            f'k = {k}: store ({len(W)} cells) + line (162) has period exactly 2 and at the odd generation is the union '
            f'of the two alone; torus {o.shape}, nearest image of a live cell {d} sites away')


def call(ks):
    for k in ks:
        t0 = time.time()
        nL = max(32, 2 * k + 12); nR = 8
        W, word, first = store(nL, k, nR); N = len(word)
        T = 28 + 2 * k + 6 + 2 * (nL + 4) + 60
        X = Orc(W | LINE, reach=CALL + [E1]); V = Orc(W, reach=[E1]); L = Orc(LINE, reach=CALL)
        for c in CALL:
            X.make(c); L.make(c)
        sx = X.cells(); dist = X.image_distance()
        union_bad = []; st_bad = []; line_rest_from = None; final_from = None; train_at = []; lead_bad = []
        empty = wire('7' * N, first=first)
        for t in range(T + 1):
            if t == T_E1:
                V.make(E1)
            x = X.cells(); v = V.cells(); l = L.cells()
            if x != sx:
                st_bad.append(t)
            if x != v | l or (v & l):
                union_bad.append(t)
            if l == LINE:
                line_rest_from = t if line_rest_from is None else line_rest_from
            elif t % 2 == 0:
                line_rest_from = None
            if t % 2 == 0:
                w = letters(v, N, first)
                bs = [i for i, ch in enumerate(w) if ch == 'b']
                if v == wire(w.replace('?', '7'), first=first) and set(w) <= set('7b') and len(bs) == k and \
                        all(q - p == 2 for p, q in zip(bs, bs[1:])):
                    train_at.append(t)
                    if first + bs[0] != CROSS + 3 - (t - 28) // 2:
                        lead_bad.append(t)
                if v == empty:
                    final_from = t if final_from is None else final_from
                else:
                    final_from = None
            if t < T:
                X.step(); V.step(); L.step(); sx = run(sx, 1)
        t_last = 28 + 2 * (CROSS + 3 - first)       # the last even generation with the leading pulse on the wire
        want = list(range(2 * k + 34, t_last + 1, 2))
        say(not union_bad and not st_bad and train_at == want and not lead_bad and final_from is not None
            and line_rest_from == 42,
            f'k = {k}: X(t) = V(t) + Lf(t) at every generation 0..{T} (differences: {union_bad[:6]}); st9 = oracle '
            f'(differences: {st_bad[:6]}); the store is exactly plain wire with {k} units b two apart, the leading one at '
            f'unit {CROSS + 3} - (t - 28)/2, at every even generation {want[0]}..{want[-1]} (2k + 34 until the lead '
            f'reaches the cap) and at no earlier one: {train_at == want and not lead_bad}; the line is at rest from '
            f'{line_rest_from}; the whole state is the empty cell + the line at rest from {final_from}; N = {N}, '
            f'torus {X.shape}, nearest image {dist}; {time.time() - t0:.0f} s')


def expect(o, t, words, lines, firsts, offs, what):
    cells = set(lines)
    for w, f, off in zip(words, firsts, offs):
        cells |= wire(w, first=f, off=off)
    say(o.cells() == cells, f't = {t}: {what}: ' + ' | '.join(rle(w) for w in words))


def proto():
    # C1  set, add, add, CALL, again (the push's `cycle`, with this review's own places and times)
    t0 = time.time(); N = 50; first = 4; c = CROSS
    idx = lambda u: u - first
    w0 = '7' * N

    def W(k, pulses=()):
        w = list(w0)
        for j in range(k):
            w[idx(c + 1 + j)] = 'd'
        if k:
            w[idx(c + 1 + k)] = 'f'
        for u in pulses:
            w[idx(u)] = 'b'
        return ''.join(w)
    ops = {0: ([RST(c - 10), LST(c + 13)], []), 100: ([LST(c + 12)], []), 170: ([LST(c + 16)], []), 240: ([LST(c + 11)], []),
           330: ([], CALL)}
    # second round: another set at other places, one add, CALL
    ops.update({600: ([RST(c - 6), LST(c + 9)], []), 700: ([LST(c + 14)], []), 780: ([], CALL)})
    o = Orc(wire(w0) | LINE, reach=CALL + [E1]); st = o.cells(); bad = []
    checks = {0: (0, ()), 100: (1, ()), 170: (2, ()), 240: (3, ()), 330: (4, ()), 600: (0, ()), 700: (1, ()), 780: (2, ()),
              1000: (0, ()), 1002: (0, ())}
    # after a CALL at s the train is exact from s + 2k + 34, the lead at CROSS + 3 - (t - s - 28)/2; the line rests from s + 42
    for s, k in ((330, 4), (780, 2)):
        for t in (s + 42, s + 48):
            lead = c + 3 - (t - s - 28) // 2
            checks[t] = (0, tuple(lead + 2 * j for j in range(k)))
    for t in range(1003):
        if t in checks:
            k, pulses = checks[t]
            expect(o, t, [W(k, pulses)], LINE, [first], [(0, 0, 0)], 'whole state = these letters + the line at rest')
        if t in ops:
            for q in ops[t][0]: o.remove(q)
            for q in ops[t][1]: o.make(q)
            st = (st - set(ops[t][0])) | set(ops[t][1])
        if o.cells() != st:
            bad.append(t)
        o.step(); st = run(st, 1)
    say(not bad, f'C1 cycle: st9 = oracle at every generation 0..1002 ({bad[:5]}); torus {o.shape}, nearest image '
        f'{o.image_distance()}; {time.time() - t0:.0f} s')

    # C2  move: stores 1 and 3; CALL at the right one; the left one holds 4
    t0 = time.time()
    for kl, kr, gap in ((1, 3, 25), (2, 5, 20), (1, 1, 12), (4, 2, 3)):
        # the left store's edge f is `gap` units before the crossing unit
        w = list(w0)
        e = c - gap
        for j in range(kl):
            w[idx(e - 1 - j)] = 'd'
        w[idx(e)] = 'f'
        for j in range(kr):
            w[idx(c + 1 + j)] = 'd'
        w[idx(c + 1 + kr)] = 'f'
        w = ''.join(w)
        o = Orc(wire(w) | LINE, reach=CALL + [E1])
        for q in CALL: o.make(q)
        o.step(2 * gap + 4 * kr + 120)
        w2 = list(w0)
        for j in range(kl):
            w2[idx(e - 1 - j)] = 'd'
        for j in range(kr):
            w2[idx(e + j)] = 'd'
        w2[idx(e + kr)] = 'f'
        ok = o.cells() == wire(''.join(w2)) | LINE
        o.step(2)
        say(ok and o.cells() == wire(''.join(w2)) | LINE,
            f'C2 move: {rle(w)} + line, CALL -> {rle("".join(w2))} + line at rest (left store {kl} + {kr} = {kl + kr}; '
            f'its edge was {gap} units before the crossing)')
    print(f'      {time.time() - t0:.0f} s', flush=True)

    # C3  chain: two stores and two lines on one wire
    t0 = time.time(); N2 = 64; first2 = 4
    sep = 24                                    # the second line is the first moved 24 units back along the store wire
    LINE2 = frozenset(tr(q, -sep) for q in LINE); CALL2 = [tr(q, -sep) for q in CALL]
    c2 = c - sep
    w = list('7' * N2)
    for j in range(2): w[c2 + 1 + j - first2] = 'd'
    w[c2 + 3 - first2] = 'f'
    for j in range(3): w[c + 1 + j - first2] = 'd'
    w[c + 4 - first2] = 'f'
    w = ''.join(w)
    S0 = wire(w, first=first2) | LINE | LINE2
    assert len(S0) == len(wire(w, first=first2)) + 324
    o = Orc(S0, reach=CALL + CALL2)
    o.step(2); say(o.cells() == S0, f'C3 chain: {rle(w)} with two lines ({len(S0)} cells) has period 2; torus {o.shape}, '
                   f'nearest image {o.image_distance()}')
    for q in CALL: o.make(q)
    o.step(198)
    w2 = list('7' * N2)
    for j in range(5): w2[c2 + 1 + j - first2] = 'd'
    w2[c2 + 6 - first2] = 'f'
    w2 = ''.join(w2)
    say(o.cells() == wire(w2, first=first2) | LINE | LINE2, f'C3 chain: CALL on the right line -> {rle(w2)}, both lines at rest '
        '(the left store holds 2 + 3; its wall is still one unit after its crossing)')
    for q in CALL2: o.make(q)
    o.step(44)
    x = o.cells(); lw = letters(x - LINE - LINE2, N2, first2)
    bs = [i for i, ch in enumerate(lw) if ch == 'b']
    say(x == wire(lw, first=first2) | LINE | LINE2 and set(lw) <= set('7b') and len(bs) == 5 and all(q - p == 2 for p, q in zip(bs, bs[1:])),
        f'C3 chain: CALL on the left line, 44 generations on: {rle(lw)}: five pulses, both lines at rest')
    o.step(220)
    say(o.cells() == wire('7' * N2, first=first2) | LINE | LINE2, 'C3 chain: 220 generations later: the empty wire and both lines')
    print(f'      {time.time() - t0:.0f} s', flush=True)

    # C4  bus: one line across two parallel store wires
    t0 = time.time()
    for n in (5,):
        off2 = (2 * n, 2 * n, 0)
        wa = '7' * 5 + 'df' + '7' * 25 + 'dddf' + '7' * 14
        wb = '7' * 5 + 'df' + '7' * 25 + 'ddf' + '7' * 15
        A = wire(wa); B = wire(wb, off=off2)
        LL = long_line(n)                      # the line with n more units of wire C after the first crossing
        S0 = A | B | LL
        assert len(S0) == len(A) + len(B) + 162 + 5 * n
        o = Orc(S0, reach=CALL)
        o.step(2); ok = o.cells() == S0
        for q in CALL: o.make(q)
        o.step(300)
        ea = '7' * 5 + 'ddddf' + '7' * 40; eb = '7' * 5 + 'dddf' + '7' * 41
        say(ok and o.cells() == wire(ea) | wire(eb, off=off2) | LL,
            f'C4 bus: two store wires {n} line units apart ({rle(wa)} | {rle(wb)}) and ONE line of {26 + n} units ({len(S0)} cells): period 2; '
            f'one CALL -> {rle(ea)} | {rle(eb)}, the line at rest; torus {o.shape}, nearest image {o.image_distance()}')
    print(f'      {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'stand':
        stand()
    elif what == 'call':
        call([int(v) for v in sys.argv[2].split(',')])
    elif what == 'proto':
        proto()
    print('ALL PASS' if OK else 'SOME FAIL')
