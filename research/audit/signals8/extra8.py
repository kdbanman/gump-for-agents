#!/usr/bin/env python3
"""extra8 (REVIEW-signals-8): smaller checks.

    python3 extra8.py sym        the half-turn maps d^k f onto itself (README section 1); B' is B under the two symmetries
    python3 extra8.py movers     R+, L+ and their trains: rigid, and what a store gains from each (st8; two on the oracle)
    python3 extra8.py twocell    every two-cell flip of wire B inside the 3 x 3 tube on two adjacent units: which movers appear
    python3 extra8.py first      the first push's receiver (objects/transmission-B.json) in letters, and its 36th shot
    python3 extra8.py beside     the place the push did not look: push 9's six-cell still life beside the wall (oracle)
    python3 extra8.py capr7      a stretch against push 7's right cap
    python3 extra8.py small6     the protocol on N = 6 and the set on N = 5, on the oracle
"""
import sys, re, json, time, itertools
from collections import Counter
import numpy as np
import a8, lab
from a8 import tr, SR, SL
from lab import R, L, settle, short

T0 = time.time()


def say(ok, text):
    tag = 'NOTE ' if ok is None else ('PASS ' if ok else 'FAIL ')
    print(tag + text + f'  [{time.time() - T0:.0f} s]', flush=True)


def sym():
    half = lambda c: (-c[0] - 2, c[1], 8 - c[2])
    res = []
    for k in (1, 2, 5):
        w = '7' * 10 + 'd' * k + 'f' + '7' * 10
        img = {half(c) for c in a8.word_cells(w, 0)}
        us = sorted({a8.unit(c) for c in img})
        lw = a8.letters_of(img, us[0], us[-1] + 1)
        res.append((k, a8.rle(lw)))
    say(all(re.fullmatch(r'7\^?\d*d*\^?\d*f7\^?\d*', r) or ('d' * k + 'f') in lw for (k, r) in res), f'sym: the half-turn (x,y,z) -> (-x-2, y, 8-z) of 7^10 d^k f 7^10, read in letters: {res}')
    # B' = B under (z-4, y, x+4) and (-z-4, y, 10-x), each with one generation
    B0 = a8.word_cells('7' * 12, 0); D0 = a8.word_cells('d' * 12, 0)
    B1 = a8.step_set(a8.word_cells('7' * 16, -2)); D1 = a8.step_set(a8.word_cells('d' * 16, -2))
    mid = lambda s: {c for c in s if 4 <= a8.unit(c) <= 7}
    out = []
    for name, g in (('(z-4, y, x+4)', lambda c: (c[2] - 4, c[1], c[0] + 4)), ('(-z-4, y, 10-x)', lambda c: (-c[2] - 4, c[1], 10 - c[0]))):
        imgs = {g(c) for c in B1}
        out.append((name, any(mid({tr(c, s) for c in imgs}) == mid(D0) for s in range(-12, 13)),
                    any(mid({tr(c, s) for c in {g(c) for c in B0}}) == mid(D1) for s in range(-12, 13))))
    say(all(a and b for _, a, b in out), f"sym: wire B at generation 1 mapped by each symmetry is wire B' at generation 0, and B at 0 is B' at 1 (up to a move along the wire): {out}")


def movers():
    res = []
    for sig, side, add in (('d6f', 'L', 2), ('d6ef', 'L', 2), ('cfd6f', 'L', 3), ('d6fd6f', 'L', 4), ('b5f', 'R', 2), ('bb5f', 'R', 2), ('b5f9f', 'R', 3), ('b5f5f9f', 'R', 4), ('b5fb5f', 'R', 4)):
        # rigid on plain wire?
        N = 40; w = '7' * 16 + sig + '7' * (N - 16 - len(sig))
        c, t = lab.play(w, {}, 8); l8 = lab.lett(c, N)
        sh = 4 if side == 'L' else -4
        rigid = l8 == ('7' * sh + w)[:N] if sh > 0 else l8 == (w[-sh:] + '7' * (-sh))
        rigid &= lab.is_state(c, l8)
        outs = []
        for d in (4, 5):
            ww = ('7' * (24 - d - len(sig)) + sig + '7' * d + 'ddf' + '7' * 12) if side == 'L' else ('7' * 12 + 'ddf' + '7' * d + sig + '7' * (24 - d - len(sig)))
            outs.append(short(settle(ww, {}, 400)[0]))
        want = '%d@%d' % (2 + add, 24 - add) if side == 'L' else '%d@12' % (2 + add)
        res.append((sig, 'rigid' if rigid else 'NOT rigid', outs, all(o == want for o in outs)))
    say(all((r[1] == 'rigid' or r[0] in ('d6fd6f', 'b5fb5f')) and r[3] for r in res), f'movers: each word (the two adjacent pairs d6fd6f, b5fb5f excepted) moves 4 units in 8 generations as an exact state, and a store ddf gains (d6f 2, d6ef 2, cfd6f 3, d6fd6f 4, b5f 2, bb5f 2, b5f9f 3, b5f5f9f 4, b5fb5f 4) '
        f'at two distances: {[(r[0], r[1], r[3]) for r in res]}')
    ok = True
    for ww, want in (('7' * 15 + 'd6f' + '7' * 4 + 'ddf' + '7' * 12, '7' * 20 + 'ddddf' + '7' * 12), ('7' * 12 + 'ddf' + '7' * 4 + 'b5f9f' + '7' * 15, '7' * 12 + 'dddddf' + '7' * 21)):
        O = a8.Orc(-6, len(ww) + 16); h = O.arr(a8.cell_state(ww)); h = O.run(h, 300)
        ok &= O.cells(h) == a8.cell_state(want)
    say(ok, 'movers: d6f into ddf from the left (+2) and b5f9f from the right (+3) on the oracle, whole state')


def twocell():
    E3 = [(x, y, z) for x in (0, 1) for y in range(-4, 5) for z in range(-6, 9)
          if a8.is_cell((x, y, z)) and 1 <= x + y + z <= 5 and 1 <= x - y + z <= 5]
    N = 100; base = '7' * N; u = 4 + 50
    S = a8.Box(-6, N + 16)
    ref = {}
    for g0 in (0, 1):
        h = S.arr(a8.cell_state(base)); S.run(h, g0); ref[g0] = h.copy()
    cnt = Counter(); n = 0
    cells = [tr(c, u) for c in E3] + [tr(c, u + 1) for c in E3]
    first = set(tr(c, u) for c in E3)
    for g0 in (0, 1):
        for c1, c2 in itertools.combinations(cells, 2):
            if c1 not in first and c2 not in first:
                continue
            h = ref[g0].copy(); S.flip(h, [c1, c2]); S.run(h, 60 - g0); n += 1
            c = S.cells(h); w = a8.letters_of(c, 4, 4 + N)
            exact = '?' not in w and '_' not in w and c == a8.cell_state(w)
            core = w.strip('7')
            if not exact:
                cnt['not a family word (fronts, defects)'] += 1
            else:
                cnt[a8.rle(re.sub(r'7+', '.', core)) or 'healed'] += 1
    say(None, f'twocell: {n} two-cell flips of plain wire B (3 x 3 tube, two adjacent units, both phases), letters at generation 60 (runs of 7 shown as .): {dict(cnt.most_common())}')
    has = [k for k in cnt if 'd6' in k or '5f' in k]
    say(None, f'twocell: outcomes containing R+ (d6f) or L+ (b5f): {has}')


def first():
    d = json.load(open(a8.os.path.join(a8.ROOT, 'research', 'signals', 'objects', 'transmission-B.json')))
    flips = [tuple(c) for c in d['receiver']]
    wire = a8.word_cells('7' * 48, 0)
    rec = wire ^ set(flips)
    say(None, f"first: the first push's receiver (8 flipped cells) in letters, units 38..45: {a8.letters_of(rec, 38, 46)}; cells of units 42, 43 moved to unit 0: "
        f"{sorted(tr(c, -42) for c in rec if a8.unit(c) == 42)}, {sorted(tr(c, -43) for c in rec if a8.unit(c) == 43)}")
    # the same object in a long capped cell: wire units 4..4+N-1; receiver at units 50..53, sender A = stator (0,1,2) of unit 14
    N = 70; S = a8.Box(-6, N + 16)
    h = S.arr(a8.cell_state('7' * N)); S.flip(h, [tr(c, 10) for c in flips])
    b = h.copy(); S.run(b, 2)
    stands = np.array_equal(b, h)
    log = []
    for shot in range(1, 39):
        c = tr(SR, 14)
        if not S.live(h, c):
            log.append((shot, 'stator dead')); break
        S.kill(h, c); S.run(h, 200)
        w = a8.letters_of(S.cells(h), 4, 4 + N)
        log.append((shot, a8.rle(w)))
    say(None, f'first: laid in a capped cell (receiver 36 units from the sender; stands: {stands}); shots 1, 2, 34..38: {log[:2] + log[33:]}')


def beside():
    TRIG = [(0, 0, 9), (0, 1, 8), (1, 0, 8), (1, 2, 10), (2, 1, 10), (2, 2, 9)]     # push 9's still life, relative to the stretch's first unit
    res = []
    for k in (1, 3, 6):
        word = '7' * (2 * k + 20) + 'd' * k + 'f' + '7' * 6; N = len(word); wu = 4 + 2 * k + 20
        O = a8.Orc(-6, N + 16, whi=20)
        sl = {tr(c, wu) for c in TRIG}
        h = O.arr(a8.cell_state(word) | sl)
        st = np.array_equal(O.run(h, 2), h)
        O.kill(h, tr(SR, wu - 12)); seen = None
        for g in range(2, 4 * k + 60, 2):
            h = O.run(h, 2)
            c = O.cells(h); w = a8.letters_of(c - sl, 4, 4 + N)
            if seen is None and 'b' in w and 'd' not in w and 'f' not in w and c == a8.cell_state(w) | sl:
                seen = (g, a8.rle(w.strip('7')))
        h = O.run(h, 200)
        res.append((k, st, seen, O.cells(h) == a8.cell_state('7' * N) | sl))
    say(all(st and seen and seen[1] == a8.rle('b' * (2 * k + 2)) and end for k, st, seen, end in res),
        f'beside: capL + 7^(2k+20) d^k f 7^6 + right cap + six cells beside the wall (outside the 5 x 5 tube): stands; ONE stator removed 12 units before the wall: '
        f'(k, stands, first exact state without d or f: (generation, train), ends as the empty cell + the six cells): {res}')


def capr7():
    res = []
    for k in (1, 2, 3):
        for gap in (0, 1, 2):
            w = '7' * 20 + 'd' * k + 'f' + '7' * gap
            S = a8.Box(-6, len(w) + 16); h = S.arr(a8.cell_state(w, a8.CAPR7)); S.run(h, 400)
            c = S.cells(h); b = h.copy(); S.run(b, 4)
            res.append((k, gap, len(c), 'periodic' if np.array_equal(b, h) else 'moving', a8.rle(a8.letters_of(c, 4, 4 + len(w)))))
    say(None, f"capr7: d^k f with `gap` units of wire between its edge and push 7's right cap, 400 generations (k, gap, cells, state, letters): {res}")


def small6():
    """the protocol on N = 6 (68 cells) and the set on N = 5 (63 cells), on the oracle"""
    O = a8.Orc(-6, 6 + 16); h = O.arr(a8.cell_state('777777')); n0 = int(h.sum()); log = []
    for ops in ([tr(SR, 5), tr(SL, 8)], [tr(SL, 9)], [tr(SR, 5)]):
        for c in ops:
            O.kill(h, c)
        h = O.run(h, 200); c = O.cells(h); w = a8.letters_of(c, 4, 10)
        log.append(w if c == a8.cell_state(w) else '?')
    O5 = a8.Orc(-6, 5 + 16); h5 = O5.arr(a8.cell_state('77777')); n5 = int(h5.sum())
    O5.kill(h5, tr(SR, 5)); O5.kill(h5, tr(SL, 8)); h5 = O5.run(h5, 200); w5 = a8.letters_of(O5.cells(h5), 4, 9)
    say(log == ['77df77', '77ddf7', '777777'] and n0 == 68 and w5 == '77df7' and O5.cells(h5) == a8.cell_state(w5) and n5 == 63,
        f'small6: N = 6 ({n0} cells), oracle: R@5 + L@8 -> {log[0]}; L@9 -> {log[1]}; R@5 -> {log[2]} (whole states); N = 5 ({n5} cells): R@5 + L@8 -> {w5}')


if __name__ == '__main__':
    for name in sys.argv[1:]:
        globals()[name]()
