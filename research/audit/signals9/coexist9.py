#!/usr/bin/env python3
"""coexist9 (review of signals push 9): push 8b's reader b13 and push 9's call line on ONE store wire.

    python3 coexist9.py reader       the reader alone on this review's store (echo beside 7, nothing beside d)
    python3 coexist9.py stand        store d^k f armed at the call line + the reader crossing at unit w + j: which stand
    python3 coexist9.py seq          for every standing (k, j): read, CALL, read again
    python3 coexist9.py write        the reader and the line in place on an EMPTY wire: set, add, read, CALL, read
    python3 coexist9.py lineread     is the call line itself a reader?  words of the line beside 7, d, f and the walls
    [--orc]                          replay the rows marked * on reference/oracle.py

From push 8b's JSON (objects/read-echo-B-small.json) only cells: the 169 cells of the reader (its crossing at store
unit 0 of the standard frame) and the four cells of its probe (two pulses B in adjacent units).  Stepper st9.c.
w = CROSS + 1 is the unit of the first d of an armed stretch; the reader `at U` is the reader moved U units along the
store wire.  A read = the probe flipped at an even generation; 30 generations later the run differs from the
unprobed run in 2 cells (echo: the unit under the reader is wire B), in none (wire B'), or otherwise.
"""
import sys, json, time
from a9 import *

_d = json.load(open(os.path.join(ROOT, 'research', 'signals', 'push8b', 'objects', 'read-echo-B-small.json')))
READER0 = frozenset(map(tuple, _d['cases'][0]['reader']))
PROBE0 = [tuple(q) for q in _d['cases'][0]['probe']]
assert len(READER0) == 169 and len(PROBE0) == 4
ORC = '--orc' in sys.argv
N, FIRST = 70, 4
c = CROSS; w = c + 1
reader = lambda U: frozenset(tr(q, U) for q in READER0)
probe = lambda U: [tr(q, U) for q in PROBE0]


def W(k, o=0):
    wd = list('7' * N)
    for j in range(k):
        wd[w + o + j - FIRST] = 'd'
    if k:
        wd[w + o + k - FIRST] = 'f'
    return ''.join(wd)


def flip(s, cells):
    return frozenset(set(s) ^ set(cells))


def stands(S, gens=40):
    return run(S, gens) == S and run(S, 2) == S


def read(S, U):
    """(class, restored-from) of a read launched on the standing state S"""
    A, B = S, flip(S, probe(U))
    A, B = run(A, 30), run(B, 30)
    if A is None or B is None:
        return 'burn', None
    d30 = len(A ^ B); res = None
    for g in range(30, 161, 2):
        if A == B:
            res = g; break
        A, B = run(A, 2), run(B, 2)
        if B is None or len(B) > 3000:
            return 'burn', None
    cls = {2: 'echo', 0: 'nothing'}.get(d30, f'other({d30})')
    return cls, res


def describe(S, U, fixed):
    """store letters if the whole state is the wire of those letters + the fixed objects, else a summary"""
    if S is None:
        return 'burn'
    if fixed <= S:
        lw = letters(S - fixed, N, FIRST)
        if '?' not in lw and S == wire(lw, first=FIRST) | fixed:
            return rle(lw)
    return f'{len(S)} cells; line {"ok" if LINE <= S else "changed"}; reader {"ok" if reader(U) <= S else "changed"}'


def orc_equal(start, ops, T, st_final):
    o = play(start, ops, T, engine='orc', every=T)
    return o[T] == st_final


def cmd_reader():
    for k, U, want in ((0, w + 6, 'echo'), (6, w + 2, 'nothing'), (6, w + 3, 'nothing'), (6, w + 9, 'echo'), (6, w - 5, 'echo')):
        S = wire(W(k)) | reader(U)
        st = stands(S); cls, res = read(S, U) if st else ('-', None)
        print(f'{"PASS" if st and cls == want else "FAIL"}  store {rle(W(k))} + reader at w{U - w:+d} (no line): stands {st}; read: {cls}, '
              f'identical to the unprobed run from {res} generations after the probe')
    print('# which units the reader stands at, beside d^k f (first d at w), no line: j = U - w from -8 to 12')
    for k in (0, 1, 2, 3, 5):
        print(f'  k = {k}: ' + ''.join('.' if stands(wire(W(k)) | reader(w + j)) else 'x' for j in range(-8, 13)))


def cmd_stand():
    print('# store d^k f armed (first d at w = CROSS + 1) + call line + reader at w + j.  "." stands (40 generations, period 2), "x" not,')
    print('# "L" the line and the reader alone (no store) do not stand together.   j = -12 .. 16')
    pair = {j: stands(LINE | reader(w + j)) for j in range(-12, 17)}
    for k in range(0, 8):
        row = ''
        for j in range(-12, 17):
            S = wire(W(k)) | LINE | reader(w + j)
            row += 'L' if not pair[j] else '.' if len(S) == len(wire(W(k))) + 162 + 169 and stands(S) else 'x'
        print(f'  k = {k}: {row}')


def cmd_seq():
    print('# for every standing arrangement: read; CALL; 400 generations; read again')
    for k in range(0, 8):
        for j in range(-12, 17):
            U = w + j
            fixed = LINE | reader(U)
            S = wire(W(k)) | fixed
            if len(S) != len(wire(W(k))) + 331 or not stands(S):
                continue
            r1, res1 = read(S, U)
            S2 = run(flip(S, []) | set(CALL), 400, cap=80000)
            d = describe(S2, U, fixed)
            r2 = read(S2, U) if S2 is not None and fixed <= S2 and stands(S2) else ('-', None)
            mark = ''
            if ORC and k in (0, 2, 4) and j in (-6, 2, 3, 8):
                t0 = time.time()
                mark = f'   [oracle, whole state after CALL + 400: {orc_equal(S, {0: ([], CALL)}, 400, S2)}; {time.time() - t0:.0f} s]'
            print(f"k = {k} reader at w{j:+d}: read {r1} (restored +{res1}); CALL -> {d}; read {r2[0]}{mark}", flush=True)


def cmd_write():
    print('# empty wire + line + reader at w + j, everything in place; then by signals only:')
    print('#   t=0 set (R@c-10, L@c+13)   t=120 read   t=300 add (L@c+12)   t=420 add (L@c+12)   t=540 read   t=720 CALL   t=1100 read')
    for j in range(-12, 31):
        U = w + j
        fixed = LINE | reader(U)
        S = wire(W(0)) | fixed
        if len(S) != len(wire(W(0))) + 331 or not stands(S):
            print(f'reader at w{j:+d}: does not stand with the empty wire and the line'); continue
        log = []; ops = {}

        def do(S, rem=(), mk=(), gens=120):
            for q in rem:
                if q not in S: return None
            S = frozenset((set(S) - set(rem)) | set(mk))
            return run(S, gens, cap=80000)
        S1 = do(S, rem=[RST(c - 10), LST(c + 13)]); log.append('set -> ' + describe(S1, U, fixed))
        ok = S1 is not None and fixed <= S1 and stands(S1)
        if ok:
            log.append('read ' + read(S1, U)[0])
            S2 = do(run(S1, 60), rem=[LST(c + 12)]); log.append('add -> ' + describe(S2, U, fixed))
            ok = S2 is not None and fixed <= S2 and stands(S2)
        if ok:
            S3 = do(S2, rem=[LST(c + 12)]); log.append('add -> ' + describe(S3, U, fixed))
            ok = S3 is not None and fixed <= S3 and stands(S3)
        if ok:
            log.append('read ' + read(S3, U)[0])
            S4 = do(S3, mk=CALL, gens=400); log.append('CALL -> ' + describe(S4, U, fixed))
            ok = S4 is not None and fixed <= S4 and stands(S4)
        if ok:
            log.append('read ' + read(S4, U)[0])
        print(f'reader at w{j:+d}: ' + '; '.join(log), flush=True)


def cmd_lineread():
    print('# the call line as a reader: a word of the line, the stretch d^k f with its first unit at CROSS + 1 + o.')
    print('# kept: rows where store and line are exactly restored 300 generations on; sig = cells in which the line differs from the')
    print('# free line with the same word, 34 and 44 generations after a launch at line unit 6 (the crossing is passed at about 30)')
    rg = ['9f', '9df', '9ddf', '9dddf', '9f9f', '9fb9f', '9fbb9f', '9fbbb9f', '9df9f', '9f9df', '9df9df']
    lg = ['7', '77', '777', '7b7', '7bb7', '7bbb7']
    table = {}
    for wd, first in [(x, 6) for x in rg] + [(x, 25 - len(x)) for x in lg]:
        free = with_lword(LINE, wd, first)
        f34, f44 = run(free, 34), run(free, 44)
        for k in (0, 3):
            for o in (range(-8, 9) if k else (0,)):
                S0 = wire(W(k, o)) | LINE
                S = with_lword(S0, wd, first)
                a34 = run(S, 34); a44 = run(a34, 10); fin = run(a44, 256, cap=80000)
                restored = fin == S0
                sig = (len((a34 - wire(W(k, o))) ^ f34), len((a44 - wire(W(k, o))) ^ f44)) if restored else None
                table[(wd, k, o)] = sig
    for wd in rg + lg:
        row = []
        for k in (0, 3):
            for o in (range(-8, 9) if k else (0,)):
                s = table[(wd, k, o)]
                row.append(('k0' if not k else f'{o:+d}') + ':' + ('x' if s is None else f'{s[0]}/{s[1]}'))
        print(f'{wd:>10}  ' + ' '.join(row))


def cmd_orc():
    """three scenarios on reference/oracle.py, compared with st9 at every even generation"""
    def both(name, start, ops, T):
        t0 = time.time()
        st = play(start, ops, T, engine='st')
        try:
            o = play(start, ops, T, engine='orc')
            same = all(o[g] == st[g] for g in range(0, T + 1, 2)); extra = f'nearest image {o["image_distance"]}, torus {o["shape"]}'
        except AssertionError as ex:
            same = None; extra = 'the oracle run left its guarded box: ' + str(ex)[:60]
        print(f'{name}: oracle = st9 at every even generation 0..{T}: {same}; {extra}; {time.time() - t0:.0f} s', flush=True)
        return st
    # (a) everything in place on an empty wire, the reader at w + 14: set, read, add, add, read, CALL, read
    U = w + 14; fixed = LINE | reader(U)
    S = wire(W(0)) | fixed
    ops = {0: ([RST(c - 10), LST(c + 13)], []), 180: ([LST(c + 12)], []), 300: ([LST(c + 12)], []),
           420: ([], CALL)}
    st = both('(a) reader at w+14, line, empty wire: set at 0, add at 180 and 300, CALL at 420', S, ops, 620)
    for t, want in ((120, W(1)), (298, W(2)), (418, W(3)), (620, W(0))):
        print(f'      t = {t}: whole state = {rle(want)} + line + reader: {st[t] == wire(want) | fixed}')
    # the reads, on the oracle: probe at 120 (store d f), at 420 - 60 = 360 (d d d f) and after the CALL
    for t in (120, 360, 620):
        base = st[t]
        oa = Orc(base, reach=probe(U)); ob = Orc(base, reach=probe(U))
        for q in probe(U): ob.flip(q)
        oa.step(30); ob.step(30); d30 = len(oa.cells() ^ ob.cells())
        oa.step(30); ob.step(30)
        print(f'      read launched at t = {t} (oracle): the probed run differs from the unprobed one in {d30} cells 30 generations on '
              f'and in {len(oa.cells() ^ ob.cells())} cells 60 generations on')
    # (b) the reader inside the stretch (placed with the store standing): read, then CALL
    U = w + 3; fixed = LINE | reader(U); S = wire(W(5)) | fixed
    oa = Orc(S, reach=probe(U)); ob = Orc(S, reach=probe(U))
    for q in probe(U): ob.flip(q)
    oa.step(30); ob.step(30); d30 = len(oa.cells() ^ ob.cells()); oa.step(30); ob.step(30)
    print(f'(b) d^5 f armed, reader at w+3 (inside the stretch): stands {Orc(S).step(2).cells() == S}; read (oracle): {d30} cells differ 30 '
          f'generations on, {len(oa.cells() ^ ob.cells())} 60 generations on')
    st = both('(b) then a CALL', S, {0: ([], CALL)}, 90)
    print(f'      t = 90: {len(st[90])} cells (start {len(S)}); line {"ok" if LINE <= st[90] else "changed"}; reader {"ok" if reader(U) <= st[90] else "changed"}')
    # (c) the reader left of the line: the released pulses reach it
    U = w - 6; fixed = LINE | reader(U); S = wire(W(4)) | fixed
    st = both('(c) d^4 f armed, reader at w-6 (left of the line): a CALL', S, {0: ([], CALL)}, 120)
    print(f'      t = 120: {len(st[120])} cells (start {len(S)}); line {"ok" if LINE <= st[120] else "changed"}; reader {"ok" if reader(U) <= st[120] else "changed"}')


if __name__ == '__main__':
    t0 = time.time()
    globals()['cmd_' + sys.argv[1]]()
    print(f'# {time.time() - t0:.0f} s')
