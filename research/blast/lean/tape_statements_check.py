#!/usr/bin/env python3
"""Checks that the Lean statements of the unzip law and the call law (Gump/Unzip.lean `UnzipLaw`, `UnzipLawSharp`,
`stretch_stands`; Gump/Call.lean `CallLaw`, `LineRest`), transcribed here definition by definition, hold on
reference/oracle.py for small k. The infinite wire is a finite piece whose ends are more than t units from every
unit compared at generation t (one unit per generation is the light cone), so on those units the piece is the
infinite wire. This tests the transcription (cells, units, the removed stator, the pulse positions, e1, the
generation 29); it is not a proof of either law.

    python3 research/blast/lean/tape_statements_check.py      (a few minutes)
"""
import sys
from tape_lib import orbit_box as orbit, tr, unit, units, load

ST = [(0, 1, 2), (0, 1, 4)]
SI = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
hexc = lambda h: set(ST) | {SI[j] for j in range(4) if h >> j & 1}
ok = True


def report(name, good):
    global ok
    ok &= bool(good)
    print(('PASS ' if good else 'FAIL ') + name, flush=True)


def hcfg(word, lo, hi):
    """Units lo .. hi of the Lean hcfg of word (a function of the unit)."""
    return frozenset(tr(c, u) for u in range(lo, hi + 1) for c in hexc(word(u)))


def storeWord(k, u):
    return 13 if 0 <= u < k else (15 if u == k else 7)


def tape_pulses(k, lead, lo, hi):
    return hcfg(lambda u: 11 if (lead <= u < lead + 2 * k and (u - lead) % 2 == 0) else 7, lo, hi)


# Unzip: countRead k = store k minus shiftPt (-1) (0,1,2) = (-2, 1, 4)
for k in (1, 2, 3):
    T = 2 * (2 * k + 5)
    lo, hi = -T - 2 * k - 8, k + T + 4
    s0 = hcfg(lambda u: storeWord(k, u), lo, hi)
    rm = (-2, 1, 4)
    assert rm in s0
    o = orbit(s0 - {rm}, T)
    a, b = lo + T, hi - T
    good = all(units(o[2 * n], a, b) == tape_pulses(k, 2 - n, a, b) for n in range(2 * k + 4, T // 2 + 1))
    report(f'UnzipLaw k = {k}: run (countRead k) (2n) = tape (pulses k (2 - n)) for n = {2 * k + 4} .. {T // 2}, units {a} .. {b}', good)
    sharp = all(units(o[2 * n], a, b) == tape_pulses(k, 2 - n, a, b) for n in range(k + 3, T // 2 + 1)) and \
        units(o[2 * (k + 2)], a, b) != tape_pulses(k, 2 - (k + 2), a, b)
    report(f'UnzipLawSharp k = {k}: from n = k + 3 = {k + 3}, and not at n = k + 2', sharp)
    so = orbit(s0, 8)
    report(f'stretch_stands k = {k}: store k at generations 2, 4, 6, 8 equals generation 0 on units {lo + 8} .. {hi - 8}',
           all(units(so[t], lo + 8, hi - 8) == units(s0, lo + 8, hi - 8) for t in (2, 4, 6, 8)))

# Call: store wire with d^k f on units c+1 .. c+k+1, the line, the CALL
D9 = load('research/signals/push9/objects/call9.json')
LINE = frozenset(tuple(c) for c in D9['runs'][0]['extra'])
CALL = frozenset(tuple(c) for c in D9['runs'][0]['ops'][3][2])
c = 4 + D9['runs'][0]['crossings'][0]
E1 = tr((1, 2, 0), c)
for k in (1,):
    T = 42
    lo, hi = 26 - T, 42 + T
    store = hcfg(lambda u: storeWord(k, u - (c + 1)), lo, hi)
    X = orbit(store | LINE | CALL, T)
    Lf = orbit(LINE | CALL, T)
    S = orbit(store, 29)
    V = S[:29] + orbit(S[29] | {E1}, T - 29)
    a, b = lo + T, hi - T
    win = lambda s: units(s, a, b)
    good_a = all(win(X[t]) == win(V[t] | Lf[t]) and not (win(V[t]) & win(Lf[t])) for t in range(T + 1))
    report(f'CallLaw (a) k = {k}: run (callStart k) t = V k t ∪ Lf t, disjoint, t = 0 .. {T}, units {a} .. {b}', good_a)
    good_b = all(units(V[2 * n], a, b) == tape_pulses(k, c + 3 - (n - 14), a, b) for n in range(k + 17, T // 2 + 1))
    report(f'CallLaw (b) k = {k}: V k (2n) = tape (pulses k (c + 3 - (n - 14))) for n = {k + 17} .. {T // 2}', good_b)
    report('LineRest: Lf (42) = line', Lf[42] == LINE)
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
