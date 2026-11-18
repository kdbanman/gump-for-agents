#!/usr/bin/env python3
"""tables8 (REVIEW-signals-8): what the cell does beyond the push's five runs.  st8 only (check_st8.py compares st8
with the oracle on runs of each kind; proto8.py section G repeats one case of each law on the oracle).

    python3 tables8.py [singles pairs blocks both during capacity places gap]      (default: all)

Places are wire places (unit 4 + p).  Outcomes at the end of a run, from the whole state (lab.settle / lab.short):
E = exactly the empty cell; k@p = exactly the cell with one stretch d^k f, first d at place p; DEAD12 = 12 cells
left (two still lifes where the caps were); X:... = something else (letters / cells; m = still changing).

singles   one stator removed at generation 0 or 1 at every unit of a cell holding 0..4
pairs     R@p at generation 0 and L@q at generation dt = 0, 2, 4, 6 on the empty N = 20 cell
blocks    a formed block of m adjacent pulses (and trains with gaps) into a store from either side
both      a formed pulse from each side at every pair of distances 1..12
during    a formed pulse on its way when a count read starts: from the left (towards the wall) and from the right
capacity  the largest count signals can write on N wire units, and what the next operation does
places    every placement of d^k f on N = 12
gap       the transfer with the receiver's edge g units from the store's wall
"""
import sys, re, time
from collections import Counter, defaultdict
import a8, lab
from lab import R, L, settle, short

T0 = time.time(); OK = [True]


def say(ok, text):
    if ok is None:
        print(f'NOTE {text}  [{time.time() - T0:.0f} s]', flush=True); return
    OK[0] &= bool(ok)
    print(('PASS ' if ok else 'FAIL ') + text + f'  [{time.time() - T0:.0f} s]', flush=True)


def out(word, ops=None, G=400):
    return short(settle(word, ops or {}, G)[0])


def singles():
    a = b = 8
    for k in range(0, 5):
        word = '7' * a + ('d' * k + 'f' if k else '') + '7' * b; N = len(word)
        print(f'  cell {a8.rle(word)} (wall at place {a}, edge at place {a + k}); columns = places 0..{N - 1}')
        rows = {}
        for nm, f in (('R', R), ('L', L)):
            for g0 in (0, 1):
                row = []
                for u in range(4, 4 + N):
                    try:
                        row.append(out(word, {g0: [f(u)]}))
                    except AssertionError:
                        row.append('n/a')
                rows[(nm, g0)] = row
                print(f'    {nm} at generation {g0}: ' + ' '.join(row))
        if k == 0:
            say(rows[('R', 0)][1:N - 1] == ['E'] * (N - 2) and rows[('L', 0)][2:] == ['E'] * (N - 2) and rows[('R', 0)][0] != 'E' and rows[('R', 0)][-1] == 'DEAD12'
                and rows[('L', 0)][:2] == ['DEAD12'] * 2, 'singles, empty cell: R@p is harmless exactly for 1 <= p <= N - 2 and L@p for p >= 2; R at place 0 wrecks the wire, R at the last place and L at places 0, 1 burn the cell down')
        else:
            r0, l0 = rows[('R', 0)], rows[('L', 0)]
            plus_l = '%d@%d' % (k + 1, a - 1); plus_r = '%d@%d' % (k + 1, a); same = '%d@%d' % (k, a)
            ok = r0[1:a - 1] == [plus_l] * (a - 2) and r0[a - 1] == 'E' and l0[a + k + 2:] == [plus_r] * (N - a - k - 2) and l0[a + k + 1] == 'E'
            ok &= l0[2:a - 1] == [same] * (a - 3) and r0[a + k + 2:N - 1] == [same] * (N - a - k - 3)
            say(ok, f'singles, count {k}: R@p adds one for 1 <= p <= wall - 2 and empties the cell at p = wall - 1 (the count read); L@q adds one for q >= edge + 2 (to the last place) and empties '
                f'the cell at q = edge + 1 (the mirror read); L left of the store (p >= 2) and R right of it (to N - 2) change nothing')
            say(None, f'singles, count {k}: R at generation 0 on the stretch and one unit after (places {a}..{a + k + 1}): {r0[a:a + k + 2]}; L on the unit before and the stretch (places {a - 1}..{a + k}): {l0[a - 1:a + k + 1]}')
            say(None, f'singles, count {k}, generation 1: R: {rows[("R", 1)][a - 3:a + k + 3]} ; L: {rows[("L", 1)][a - 3:a + k + 3]} (places {a - 3}..{a + k + 2})')


def pairs():
    N = 20; bad = []; cnt = Counter()
    for dt in (0, 2, 4, 6):
        for p in range(2, N - 2):
            for q in range(2, N - 2):
                if p == q and dt == 0:
                    continue
                try:
                    o = out('7' * N, {0: [R(4 + p)], dt: [L(4 + q)]} if dt else {0: [R(4 + p), L(4 + q)]}, 300)
                except AssertionError:
                    cnt['second stator not live'] += 1; continue
                s = q - p - dt // 2                      # separation when the second pulse is born
                if s >= 3:
                    want = ('1@%d' % ((p + dt // 2 + q - 1) // 2 )) if s % 2 == 1 else 'E'
                elif s <= -2:
                    want = 'E'
                else:
                    want = None
                if want is None:
                    cnt[f's={s}: ' + ('E' if o == 'E' else 'DEAD' if o.startswith('DEAD') else 'set' if '@' in o and not o.startswith('X') else 'other')] += 1
                elif o != want:
                    bad.append((dt, p, q, o, want))
                else:
                    cnt['as the rule'] += 1
    say(not bad, f'pairs: R@p at 0 and L@q at dt (places 2..{N - 3}, dt = 0, 2, 4, 6), s = q - p - dt/2: s odd >= 3: one df with d at place (p + dt/2 + q - 1)/2; s even >= 4: empty; s <= -2: empty. exceptions: {bad[:6]}')
    say(None, f'pairs: counts {dict(cnt)}')


def blocks():
    bad = []; n = 0
    trains_l = [('6' + 'e' * (m - 1) + 'f', -(-m // 2)) for m in range(1, 9)] + [('6f6f', 2), ('6f76f', 2), ('6f6f6f', 3), ('6ef6f', 2), ('6f6ef', 2), ('6ef6ef', 2), ('6eef6f', 3), ('6ef76eef', 3)]
    trains_r = [('b' * m, -(-m // 2)) for m in range(1, 9)] + [('b7b', 2), ('b77b', 2), ('b7b7b', 3), ('bb7b', 2), ('b7bb', 2), ('bb7bb', 2), ('bbb7b', 3), ('bb77bbb', 3)]
    for k in (1, 2, 3, 4):
        for d in range(2, 10):
            for t, add in trains_l:
                w = '7' * (24 - d - len(t)) + t + '7' * d + 'd' * k + 'f' + '7' * 12
                n += 1
                if out(w) != '%d@%d' % (k + add, 24 - add):
                    bad.append((k, d, t, out(w)))
            for t, add in trains_r:
                w = '7' * 12 + 'd' * k + 'f' + '7' * d + t + '7' * (24 - d - len(t))
                n += 1
                if out(w) != '%d@%d' % (k + add, 12):
                    bad.append((k, d, t, out(w)))
    say(not bad, f'blocks: {n} runs (k = 1..4, distance 2..9, blocks of m = 1..8 adjacent pulses and 8 trains with gaps, each side): a block of m adds ceil(m/2), '
        f'blocks separated by one or more plain units add up, the stretch grows on the side hit; exceptions: {bad[:5]}')
    for d in (0, 1):
        res = [(t, out('7' * (24 - d - len(t)) + t + '7' * d + 'ddf' + '7' * 12)) for t, _ in trains_l[:3]] + [(t, out('7' * 12 + 'ddf' + '7' * d + t + '7' * (24 - d - len(t)))) for t, _ in trains_r[:3]]
        say(None, f'blocks: laid {d} units from the store ddf (wall at 24 / first d at 12): {res}')


def both():
    bad = []
    for k in (1, 2, 3, 4):
        for dL in range(1, 13):
            for dR in range(1, 13):
                w = '7' * (14 - dL) + '6f' + '7' * dL + 'd' * k + 'f' + '7' * dR + 'b' + '7' * (14 - dR)
                if out(w, G=300) != '%d@%d' % (k + 2, 15):
                    bad.append((k, dL, dR))
    say(not bad, f'both: a formed pulse from each side, 1..12 units from the wall and from the edge (144 pairs, k = 1..4): always count + 2, one unit gained on each side; exceptions: {bad[:5]}')


def during():
    bad = []; res = defaultdict(list)
    for k in range(1, 7):
        for D in range(2, 46):
            w = '7' * (50 - D - 2) + '6f' + '7' * D + 'd' * k + 'f' + '7' * 14
            o = out(w, {0: [R(4 + 49)]}, 600)
            want = 'E' if (D % 2 == 1 or D == 2) else '%d@%d' % (k, 50 - D // 2)
            if o != want:
                bad.append((k, D, o))
    say(not bad, f'during, from the left: a formed right-going pulse D units before the wall when the count read starts (D = 2..45, k = 1..6): D odd (and D = 2): the cell ends empty; '
        f'D even >= 4: a store with the same count k stands again, its first d at wall - D/2; exceptions: {bad[:5]}')
    bad = []
    for k in range(1, 6):
        for D in range(1, 25):
            w = '7' * 8 + 'df' + '7' * 16 + 'd' * k + 'f' + '7' * D + 'b' + '7' * (30 - D)
            o = out(w, {0: [R(4 + 25)]}, 700)
            if o != '%d@8' % (k + 2):
                bad.append((k, D, o))
    say(not bad, f'during, from the right: a formed left-going pulse D units after the edge when the count read starts (D = 1..24, k = 1..5), with a receiver df to the left: the receiver '
        f'ends with k + 2 (the k released pulses and the late one); exceptions: {bad[:5]}')


def capacity():
    for N in (7, 12, 16):
        mid = (N - 1) // 2
        p, q = 1, 1 + 2 * ((N - 2 - 1) // 2 // 1 // 2) + 3
        # set with the pair (1, q), q - 1 odd >= 3
        q = next(q for q in range(N - 1, 3, -1) if (q - 1) % 2 == 1)
        word = '7' * N
        S = a8.Box(-6, N + 16); h = S.arr(a8.cell_state(word)); log = []

        def state():
            c = S.cells(h); w = a8.letters_of(c, 4, 4 + N)
            return short(w if lab.is_state(c, w) else f'[{w} pop {len(c)}]')
        S.kill(h, R(4 + 1)[1]); S.kill(h, L(4 + q)[1]); S.run(h, 200); log.append(state())
        side = 0; stuck = 0
        while stuck < 2 and len(log) < 3 * N:
            before = state()
            m = re.fullmatch(r'(\d+)@(\d+)', before)
            if not m:
                break
            k, a = int(m.group(1)), int(m.group(2))
            if side == 0 and a - 2 >= 1:
                S.kill(h, R(4 + 1)[1]); S.run(h, 200); stuck = 0; log.append('R@1:' + state())
            elif side == 1 and a + k + 2 <= N - 1:
                S.kill(h, L(4 + N - 1)[1]); S.run(h, 200); stuck = 0; log.append(f'L@{N - 1}:' + state())
            else:
                stuck += 1
            side ^= 1
        final = state(); m = re.fullmatch(r'(\d+)@(\d+)', final)
        over_l = out(a8.letters_of(S.cells(h), 4, 4 + N), {0: [R(4 + 1)]}); over_r = out(a8.letters_of(S.cells(h), 4, 4 + N), {0: [L(4 + N - 1)]})
        say(m is not None and int(m.group(1)) == N - 4 and over_l == 'E' and over_r == 'E',
            f'capacity, N = {N}: senders at place 1 (R) and at the last place (L): {log}; full at count {m.group(1) if m else None} = N - 4 (wall at place 2, edge at place N - 2); '
            f'one more R@1 -> {over_l}, one more L@{N - 1} -> {over_r} (each is then the count read: the count leaves into the cap)')


def places():
    N = 12; bad = []
    for k in range(1, N):
        for p in range(0, N - k):
            w = '7' * p + 'd' * k + 'f' + '7' * (N - p - k - 1)
            o = out(w)
            if o != ('E' if p == 0 else '%d@%d' % (k, p)):
                bad.append((k, p, o))
    say(not bad, f'places: on N = 12 every d^k f laid with its first d at place p stands (period 2) for p >= 1, to the edge on the last place (k up to N - 2 = 10); '
        f'at p = 0 (against capL) it is erased and the cell is empty; exceptions: {bad[:5]}')


def gap():
    res = {}
    for g in range(1, 7):
        for k in range(1, 7):
            w = '7' * 6 + 'df' + '7' * g + 'd' * k + 'f' + '7' * 6
            res[(g, k)] = out(w, {0: [R(4 + 8 + g - 1)]}, 500)
    say(all(res[(g, k)] == '%d@6' % (k + 1) for g in range(2, 7) for k in range(1, 7)) and all(res[(1, k)] == 'E' for k in range(1, 7)),
        'gap: transfer into a receiver df whose edge is g units of wire from the store\'s wall: g = 2..6, k = 1..6: the receiver holds k + 1; g = 1 (the removed stator touches both): '
        'both stores are lost and the cell is empty')


if __name__ == '__main__':
    todo = sys.argv[1:] or ['singles', 'pairs', 'blocks', 'both', 'during', 'capacity', 'places', 'gap']
    for name in todo:
        globals()[name]()
    print('ALL PASS' if OK[0] else 'SOME FAIL')
