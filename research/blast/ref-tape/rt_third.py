#!/usr/bin/env python3
"""ref-tape, third review (2026-11-24): the lit clock from one cell, the two readers, the beam, the divider.

    python3 rt_third.py DUMP2 DUMP3     (outputs of RtDump2.lean and RtDump3.lean; about 3 minutes)

Objects from the JSON files (clock-C, call9, beam-5f, divider-C8), behaviour from reference/oracle.py only.
"""
import random, sys
from rt_lib import orc_run, trs, tr, unit_of, load, OBJ
import rt_objects as O
import rt_dyn
from rt_dyn import report

D = {}
for f in sys.argv[1:3]:
    for line in open(f):
        line = line.rstrip('\n')
        if line:
            name, pts = line.split('|', 1)
            D[name] = [tuple(map(int, p.split(','))) for p in pts.split()] if pts else []
S = lambda name: frozenset(D[name])
inbox = lambda c, a, b: 2 * a <= c[0] <= 2 * b + 1 and -8 <= c[1] <= 8 and -24 <= c[0] + c[2] <= 24

# ---------------------------------------------------------------- 1. the lit clock
for N in range(13, 31):
    report(len(D[f'litList.{N}']) == len(S(f'litList.{N}')) and S(f'litList.{N}') == O.clock_cells(N),
           f'litList {N} = capL + {N} units + capR moved {N} + (1,0,4) moved {N // 2} (clock-C.json)')
lit6 = orc_run(O.clock_cells(6), 41 + 26)
Xb = lambda s: lit6[41 + (s + 7) % 26]
for N in range(6, 31):
    P, mu = 4 * N + 2, N - 2
    o = orc_run(O.clock_cells(N), mu + 2 * P)
    exact = o[mu + P] == o[mu] and all(o[mu + k] != o[mu] for k in range(1, P))
    first = o[mu - 1 + P] != o[mu - 1]
    C = S(f'clockOf.{N}')
    boxed = all(inbox(c, -6, N + 5) for t in range(mu, mu + P) for c in o[t])
    on = [t for t in range(mu, mu + P) if o[t] == C]
    left = frozenset(c for c in o[N - 3] if unit_of(c) <= 2)
    match = [s for s in range(26) if frozenset(c for c in Xb(s) if unit_of(c) <= 2) == left]
    right = frozenset(tr(c, -(N - 6)) for c in o[N - 3] if unit_of(c) >= N - 3)
    rmatch = [s for s in range(26) if frozenset(c for c in Xb(s) if unit_of(c) >= 3) == right]
    report(exact and first and boxed and len(on) == 1,
           f'lit clock N={N}: periodic from N-2 = {mu} with exact period {P}: {exact}; generation {mu - 1} not on the cycle: '
           f'{first}; clockOf {N} = its state at generation {on}; at N-3 the units <= 2 equal the base at times {match}, '
           f'the units >= N-3 (moved back) the base\'s units >= 3 at times {rmatch}')

# ---------------------------------------------------------------- 2. the readers
wTest = lambda u: 'C' if (u % 3 == 0 or u == 1) else 'B'
CAPL = frozenset(O.T('capL', O.CLOCK))
ref = CAPL | O.tape_cells(wTest, 0, 12)
report(S('readerC') == frozenset(c for c in ref if inbox(c, -8, 12)) and all(inbox(c, -8, 12) for c in ref),
       f'readerC = clock-C capL on the units < 0 + the tape of the word on the units >= 0 ({len(ref)} cells)')
CAPL9 = frozenset(map(tuple, O.CALL9['capL']))
ref9 = CAPL9 | O.tape_cells(wTest, 4, 16)
report(S('readerCall') == frozenset(c for c in ref9 if inbox(c, -4, 16)) and all(inbox(c, -4, 16) for c in ref9)
       and all(0 <= unit_of(c) <= 3 for c in CAPL9),
       f'readerCall = call9.json capL (units 0..3) + the tape from unit 4 ({len(ref9)} cells)')
rnd = random.Random(1125)
for capname, cap, first in (('clock capL', CAPL, 0), ('call9 capL', CAPL9, 4)):
    for trial in range(4):
        Lw = 64
        dens = [0.1, 0.5, 0.9, 0.3][trial]
        word = [('C' if rnd.random() < dens else 'B') for _ in range(Lw)]
        if trial == 0:
            word = ['B'] * Lw
        w = lambda u: word[u - first]
        start = cap | O.tape_cells(w, first, first + Lw - 1)
        T = 40
        orb = orc_run(start, T, margin=16)
        good = True
        for n in range(T // 2 + 1):
            hi = first + Lw - 1 - 2 * n - 1                    # units the cut end of the finite word cannot reach
            want = cap | O.tape_cells(lambda u: word[u + n - first] if u + n - first < Lw else 'B', first, hi)
            got = frozenset(c for c in orb[2 * n] if unit_of(c) <= hi)
            good &= got == want
        report(good, f'{capname}: word of {Lw} letters (C density {dens}), every even generation 0..{T}: the cap and the '
               f'word moved on, cell for cell, on every unit the cut end cannot reach')

# ---------------------------------------------------------------- 3. the beam
BEAM = load(f'{OBJ}/beam-5f.json')
def beam_cells(N):
    cells = set(map(tuple, BEAM['left']))
    for k in range(N):
        cells |= trs(map(tuple, BEAM['b0' if k % 2 == 0 else 'b1']), k)
    cells |= trs(map(tuple, BEAM['R_even' if N % 2 == 0 else 'R_odd']), N)
    return frozenset(cells)
for N in range(1, 13):
    report(len(D[f'beamList.{N}']) == len(S(f'beamList.{N}')) and S(f'beamList.{N}') == beam_cells(N),
           f'beamList {N} = the note of beam-5f.json ({len(beam_cells(N))} cells)')
for N in list(range(1, 21)) + [30]:
    o = orc_run(beam_cells(N), 8)
    report(o[4] == o[0] and all(o[k] != o[0] for k in range(1, 4)), f'beam N={N}: exact period 4 from generation 0 (oracle)')

# ---------------------------------------------------------------- 4. the divider
DIV = load(f'{OBJ}/divider-C8.json')
def div_cells(N):
    cells = set(map(tuple, DIV['capA']))
    for k in range(N):
        cells |= trs(map(tuple, DIV['unit']), k)
    cells |= trs(map(tuple, DIV['gun']), N) | trs(map(tuple, DIV['osc']), N)
    return frozenset(cells)
for N in range(3, 21):
    report(len(D[f'divList.{N}']) == len(S(f'divList.{N}')) and S(f'divList.{N}') == div_cells(N),
           f'divList {N} = the note of divider-C8.json ({len(div_cells(N))} cells)')
for N in list(range(3, 21)) + [24, 30]:
    T = 2 * N + 140
    o = orc_run(div_cells(N), T)
    seen, mu, P = {}, None, None
    for t, s in enumerate(o):
        if s in seen:
            mu, P = seen[s], t - seen[s]
            break
        seen[s] = t
    claim = (mu == 2 * N - 3 and P == 8)
    if N >= 8:
        report(claim, f'divider N={N}: preperiod {mu}, period {P} (claimed 2N-3 = {2 * N - 3}, 8)')
    else:
        print(f'INFO divider N={N} (not claimed): preperiod {mu}, period {P}, '
              f'population at the start {len(o[0])}, at {T}: {len(o[-1])}', flush=True)

print('ALL PASS' if rt_dyn.ok else 'SOME CHECKS FAILED')
sys.exit(0 if rt_dyn.ok else 1)
