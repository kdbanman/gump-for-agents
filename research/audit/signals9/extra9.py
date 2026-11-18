#!/usr/bin/env python3
"""extra9 (review of signals push 9): smaller checks.

    python3 extra9.py twice     the shortest safe interval between two CALLs, k = 1..14 (st9; k = 12 on the oracle)
    python3 extra9.py near      a right-going store pulse that meets a CALL at an armed store: the three odd cases on the oracle
    python3 extra9.py held      one cell held live at the wall (the push's ghost9): the two cells it names, a sample of the rest
    python3 extra9.py line      shorter lines; the pair from the far end; the bus at other distances (st9)
"""
import sys, time
from a9 import *
import beyond9 as B
from beyond9 import W, seed, outcome, c, N, FIRST


def twice():
    print('# second CALL d generations after the first (both seeded at line unit 6), store d^k f armed: the smallest d from')
    print('# which every tried d (step 2, up to 4k + 12) ends as the empty wire with the line as it was, and what the last bad d gives')
    for k in range(1, 15):
        rows = {}
        for d in range(6, 4 * k + 14, 2):
            cls, text, out, hist = outcome(wire(W(k)) | LINE, {0: ([], seed()), d: ([], seed())}, T=500 + 4 * k)
            rows[d] = (cls == 'store' and text == rle('7' * N) and out == k, text)
        bad = [d for d, (ok, t) in rows.items() if not ok]
        print(f'k = {k}: not clean for d in {bad[0] if bad else None}..{bad[-1] if bad else None} ({len(bad)} values, 4k = {4 * k}); '
              f'clean for every d from {max(bad) + 2 if bad else 6} to {4 * k + 12}' + (f'; at d = {bad[-1]}: {rows[bad[-1]][1]}' if bad else ''))
    t0 = time.time()
    for d in (44, 48, 50):
        ops = {0: ([], seed()), d: ([], seed())}
        cls, text, out, hist = outcome(wire(W(12)) | LINE, ops, T=300)
        o = play(wire(W(12)) | LINE, ops, 300, engine='orc')
        same = all(o[g] == hist[g] for g in range(0, 301, 2))
        print(f'k = 12, second CALL {d} generations later: at generation 300 {len(hist[300])} cells, the line '
              f'{"as it was" if LINE <= hist[300] else "changed"}, store letters {rle(letters(hist[300] - LINE, N, FIRST))}; '
              f'oracle = st9 at every even generation 0..300: {same}; {time.time() - t0:.0f} s', flush=True)


def near():
    for k, a in ((3, -17), (3, -16), (3, -15), (1, -15), (1, -17)):
        t0 = time.time()
        ops = {0: ([RST(c + a)], seed())}
        cls, text, out, hist = outcome(wire(W(k)) | LINE, ops, T=400)
        o = play(wire(W(k)) | LINE, ops, 300, engine='orc')
        same = all(o[g] == hist[g] for g in range(0, 301, 2))
        print(f'k = {k}, R@CROSS{a:+d} and a CALL at generation 0: {cls}, {out} pulses out, {text}; oracle = st9 at every even '
              f'generation 0..300: {same}; {time.time() - t0:.0f} s', flush=True)


def held():
    # a cell forced live after every generation (the push's "one cell held live")
    def go(start, cell, rem, T):
        s = frozenset(start) - set(rem)
        for t in range(T):
            s = run(s, 1, cap=60000)
            if s is None or len(s) > 3000:
                return None
            s = s | {cell}
        return s
    wl = c + 1
    for rel in ((0, 1, 8), (-2, 1, 10)):
        cell = tr(rel, wl)
        for k in (1, 3, 5):
            S = wire(W(k)) | {cell}
            st = go(S, cell, [], 40) == S
            f = go(S, cell, [RST(wl - 12)], 400)
            print(f'cell {rel} of the stretch\'s first unit held live, d^{k} f: stands {st}; a right-going pulse: '
                  + ('burn' if f is None else rle(letters(f, N, FIRST)) + f' ({len(f)} cells; plain wire + the cell: {f == wire("7" * N) | {cell}})'))
        S = wire(W(0)) | {cell}
        f = go(S, cell, [RST(wl - 12)], 400)
        print(f'cell {rel} held live beside PLAIN wire: a right-going pulse: ' + ('burn' if f is None else
              f'{len(f)} cells, restored: {f == S}, letters {rle(letters(f, N, FIRST))}'))


def line():
    print('# the line cut short: units removed before / after the crossing (the caps kept); k = 3, CALL seeded 4 units before the crossing')
    for nb, na in ((21, 4), (12, 4), (8, 4), (6, 4), (5, 4), (21, 3), (21, 2), (21, 1), (8, 2), (6, 2)):
        cells = set()
        for q in LINE:
            u = (q[0] - LT[0]) >> 1
            if u < 0: cells.add(lstep([q], 21 - nb).__iter__().__next__())
            elif u <= 25 and (21 - nb <= u <= 21 + na): cells.add(q)
            elif u > 25: cells.add(lstep([q], -(4 - na)).__iter__().__next__())
        L2 = frozenset(cells)
        st = run(L2, 2) == L2
        S = wire(W(3)) | L2
        st2 = st and run(S, 2) == S and len(S) == len(wire(W(3))) + len(L2)
        res = '-'
        if st2:
            sd = [q for q in lstep(CALL, 17 - 6)]
            if not (set(sd) & S):
                f = run(S | set(sd), 400, cap=60000)
                res = 'burn' if f is None else (rle(letters(f - L2, N, FIRST)) if L2 <= f and f - L2 == wire(letters(f - L2, N, FIRST)) else f'{len(f)} cells, line changed' if not L2 <= f else 'other')
        print(f'{nb} units before, {na} after ({len(L2)} cells): line alone stands {st}; with d^3 f stands {st2}; CALL -> {res}')
    print('# the bus: a second store wire n line units further on (both hold stores 1 and 3 / 1 and 2), one CALL')
    for n in range(2, 13):
        off2 = (2 * n, 2 * n, 0)
        wa = '7' * 5 + 'df' + '7' * 25 + 'dddf' + '7' * 28; wb = '7' * 5 + 'df' + '7' * 25 + 'ddf' + '7' * 29
        LL = long_line(n)
        A = wire(wa); Bw = wire(wb, off=off2)
        S = A | Bw | LL
        if len(S) != len(A) + len(Bw) + len(LL) or run(S, 2) != S:
            print(f'n = {n}: does not stand'); continue
        f = run(S | set(CALL), 400, cap=80000)
        ea = '7' * 5 + 'ddddf' + '7' * 54; eb = '7' * 5 + 'dddf' + '7' * 55
        print(f'n = {n}: stands; one CALL -> ' + ('both counts moved exactly (4 and 3), line at rest' if f == wire(ea) | wire(eb, off=off2) | LL else
              'burn' if f is None else f'{len(f)} cells (start {len(S)}); line {"ok" if LL <= f else "changed"}'))


if __name__ == '__main__':
    {'twice': twice, 'near': near, 'held': held, 'line': line}[sys.argv[1]]()
