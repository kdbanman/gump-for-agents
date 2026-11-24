#!/usr/bin/env python3
"""Writes Gump/TapeMeetData.lean for the meetings of section 31 (Gump/TapeMeet.lean, Gump/TapeMeetFront.lean) and
checks on reference/oracle.py what the Lean files prove.

    python3 research/blast/lean/tape_meet.py > research/blast/lean/Gump/TapeMeetData.lean
    python3 research/blast/lean/tape_meet.py --fronts > research/blast/lean/Gump/TapeMeetFronts.lean

A meeting is `pair A B a b`: the plain train at phase 1 with the up-signal A flipped at unit a and the down-signal B
at unit b (tape_signals.py's cells). For each front meeting (U meets H, E meets H, E meets K0) at its base distance,
the differences sigma_t = S(t) xor train(1 + t) are computed with the oracle for the generations the Lean chain
needs (two-generation steps up to g, then single steps to g + 4) and written out; Lean re-checks every step with its
own stepper. Also checked here on the oracle (the Lean statements, for a test the proof does not need): from
generation g on, S(t + 4) is S(t) with its units <= m moved two units down and its units > m moved two units up, for
t = g .. g + 24, and the units m - 2 .. m + 3 hold the medium.
"""
import sys
from tape_lib import load, orbit_box, tr, unit, units, shift, lean_list

lc = load('research/signals/objects/line-C.json')
R5 = [tuple(c) for c in lc['rake5']]; RF = [tuple(c) for c in lc['rakef']]
SIGS = {'E': (0, [(1, 2, 2), (2, 0, 1), (2, 0, 3)], +1), 'U': (1, [(0, 0, 3)], +1),
        'H': (1, [(1, 2, 2)], -1), 'K0': (0, [(0, 0, 3)], -1)}
LO, HI = -60, 60
piece0 = frozenset(tr(c, u) for u in range(-60, 60) for c in (R5 if u % 2 == 0 else RF))
o0 = orbit_box(piece0, 6)
BASE = [[frozenset(tr(c, -par) for c in units(o0[t], par, par)) for par in (0, 1)] for t in range(4)]
train = lambda t, a, b: frozenset(tr(c, u) for u in range(a, b + 1) for c in BASE[t % 4][u % 2])
sig = lambda K, u: frozenset(tr(c, u) for c in SIGS[K][1])
BE = frozenset([(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)])
BO = frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)])
ok = True


def report(name, good):
    global ok
    ok &= bool(good)
    print(('PASS ' if good else 'FAIL ') + name, file=sys.stderr, flush=True)


def diffs(A, a, B, b, T):
    S = train(1, LO, HI) ^ sig(A, a) ^ sig(B, b)
    o = orbit_box(S, T)
    out = []
    for t in range(T + 1):
        ex = (LO + t + 2, HI - t - 2)
        out.append(units(o[t], *ex) ^ units(train(1 + t, LO, HI), *ex))
    return out


def front_ok(D, g, m, medium, T):
    """D[t + 4] == D[t] with units <= m moved -2 and units > m moved +2 (the train is unchanged by these moves at
    t and t + 4), and the medium on units m - 2 .. m + 3, for g <= t <= T - 4."""
    good = True
    for t in range(g, T - 3):
        lo_, hi_ = LO + t + 8, HI - t - 8
        want = frozenset(c for c in shift(D[t], -2) if unit(c) <= m) | frozenset(c for c in shift(D[t], 2) if unit(c) > m)
        good &= units(D[t + 4], lo_, hi_) == units(want, lo_, hi_)
        for u in range(m - 2, m + 4):
            cells = frozenset(tr(c, -u) for c in units(D[t], u, u) ^ units(train(1 + t, u, u), u, u))
            good &= cells == medium(t, u)
    return good


def lean_steps(name, D, g):
    steps = [(t, 2) for t in range(0, g, 2)] + [(t, 1) for t in range(g, g + 4)]
    out = []
    for (t, k) in steps:
        s, s2 = D[t], D[t + k]
        us = [unit(c) for c in s]; us2 = [unit(c) for c in s2]
        lo = min(min(us) - k, min(us2) if us2 else 10 ** 9); hi = max(max(us) + k, max(us2) if us2 else -10 ** 9)
        assert hi - lo <= 31 - 2 * k, (name, t, lo, hi)
        c = (-8 - lo) + ((31 - (hi - lo)) // 2)
        cells = set(s) | train(1 + t, lo - k, hi + k)
        zs = [q[2] for q in cells]
        vz = ((-12 + 43) - (min(zs) + max(zs))) // 2 // 2 * 2
        assert -10 <= min(zs) + vz and max(zs) + vz <= 41, (name, t, min(zs), max(zs), vz)
        out.append((t, k, lo, hi, (2 * c, 8, vz)))
    return out


WB = lambda t, u: BO if t % 2 == 0 else BE
MEETS = [('UH', 'U', 1, 'H', 5, 12, 4, WB), ('EH', 'E', 0, 'H', 5, 22, 1, WB), ('EK', 'E', 0, 'K0', 4, 12, 1, None)]
# the holed train: train(1) with H at every odd unit, its unit at each phase and parity (oracle)
HT0 = train(1, LO, HI)
for u in range(LO, HI + 1):
    if u % 2 == 1:
        HT0 = HT0 ^ sig('H', u)
oht = orbit_box(HT0, 4)
HTU = {(s % 4, par): frozenset(tr(c, -u) for c in units(oht[s], u, u)) for s in range(4) for par in (0, 1)
       for u in [par + 10]}
report('the holed train (train(1) with H at every odd unit) has period 4 and repeats every two units',
       all(units(oht[4], -20, 20) == units(oht[0], -20, 20) for _ in [0]) and
       all(frozenset(tr(c, -u) for c in units(oht[s], u, u)) == HTU[(s % 4, u % 2)] for s in range(4) for u in range(-20, 20)))
HTmed = lambda t, u: HTU[((t - 12) % 4, u % 2)]
data = {}
for (name, A, a, B, b, g, m, med) in MEETS:
    if med is None:
        med = HTmed
    D = diffs(A, a, B, b, g + 28)
    report(f'{name}: from generation {g}, S(t+4) is S(t) moved down below unit {m} and up above it; the units '
           f'{m - 2} .. {m + 3} hold the medium (t = {g} .. {g + 24})', front_ok(D, g, m, med, g + 28))
    data[name] = (D, g, m, lean_steps(name, D, g))


def picture(S, t, lo, hi):
    """One character per unit: '.' the plain train, 'o'/'b' wire B (odd / even phase), 'h' the train with H, 'X' else."""
    out = ''
    for u in range(lo, hi + 1):
        c = frozenset(tr(q, -u) for q in units(S, u, u) ^ units(train(1 + t, u, u), u, u))
        tu = BASE[(1 + t) % 4][u % 2]
        out += ('.' if c == tu else 'o' if c == BO else 'b' if c == BE else
                'h' if c == tu ^ frozenset([(1, 2, 2)]) else 'X')
    return out


for name in ('UH', 'EH'):
    D, g, m, steps = data[name]
    for t in (g + 4, g + 5):
        print(f'{name} at generation {t}, units -12 .. 20: {picture(D[t], t, -12, 20)}', file=sys.stderr)
print('(E-H: the upper edge carries X.X below its four topmost units of wire B; U-H: none)', file=sys.stderr)
if not ok:
    sys.exit(1)
KIND = {'U': 'U', 'E': 'E', 'H': 'H', 'K0': 'K0'}


def fronts():
    print('''/-
Generated by tape_meet.py --fronts (do not edit): for each front meeting of section 31 at its base distance, the
kernel's chain from the meeting to generation g + 4 (`chain*_ok`), the front facts (`facts*_ok`), and the meeting for
every distance (`meet_*`), from `rigid_front` and `pair_run`.
-/
import Gump.TapeMeetFront

namespace Gump.Tape.Signals
open Gump Gump.Tape Gump.Bits
''')
    for (name, A, a, B, b, g, m, med) in MEETS:
        D, g, m, steps = data[name]
        P = f'pair .{A} .{B} {a} {b}'
        calls = [f'stepCheck {1 + t} {k} (d{name} {t}) (d{name} {t + k}) ({lo}) ({hi}) ⟨{V[0]}, {V[1]}, {V[2]}⟩'
                 for (t, k, lo, hi, V) in steps]
        print(f'def chain{name} : Bool :=\n  ' + ' &&\n  '.join(calls))
        print(f'\ntheorem chain{name}_ok : chain{name} = true := by decide +kernel\n')
        print(f'def facts{name} : Bool := sameL (d{name} {g + 4}) (frontList {m} (d{name} {g})) &&')
        print(f'  (List.range 4).all (fun r => (List.range 6).all (fun i => unitIs (1 + ({g} + r)) (d{name} ({g} + r))')
        if name == 'EK':
            print(f'    ({m} - 2 + (i : Int)) (medEK (({g} + r) % 4) ((({m} : Int) - 2 + (i : Int)) % 2).toNat)))')
        else:
            print(f'    ({m} - 2 + (i : Int)) (if ({g} + r) % 2 = 0 then BOc else BEc)))')
        print(f'\ntheorem facts{name}_ok : facts{name} = true := by decide +kernel\n')
        pat = 'c0'
        for i in range(1, len(steps)):
            pat = f'⟨{pat}, c{i}⟩'
        print(f'theorem run{name} : ∀ r, r ≤ 4 → run ({P}) ({g} + r) = xorC (train (1 + ({g} + r))) (lcfg (d{name} ({g} + r))) := by')
        print(f'  have hc := chain{name}_ok')
        print(f'  simp only [chain{name}, Bool.and_eq_true] at hc')
        print(f'  obtain {pat} := hc')
        print(f'  have e0 : run ({P}) 0 = xorC (train (1 + 0)) (lcfg (d{name} 0)) := by')
        print(f'    show {P} = _')
        print(f'    rw [pair, (sameL_iff _ _).mp (by decide : sameL (sig .{A} {a} ++ sig .{B} {b}) (d{name} 0) = true)]')
        prev = 'e0'; names = {0: 'e0'}
        for i, (t, k, lo, hi, V) in enumerate(steps):
            nm = f'e{t + k}'
            print(f'  have {nm} := chain_next {prev} c{i}')
            names[t + k] = nm; prev = nm
        print('  intro r hr')
        print('  rcases (show r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 ∨ r = 4 by omega) with rfl | rfl | rfl | rfl | rfl')
        for r in range(5):
            print(f'  · exact {names[g + r]}')
        MED = (lambda tt: f'medC medEK ({tt})') if name == 'EK' else (lambda tt: f'wireB ({tt})')
        FOF = f'front_of_facts_med _ (d{name}) medEK' if name == 'EK' else f'front_of_facts _ (d{name})'
        MEDN = (lambda tt: f'shiftC n (medC medEK ({tt}))') if name == 'EK' else (lambda tt: f'wireB ({tt})')
        b2 = f'{b} + 2 * n'
        PN = f'pair .{A} .{B} {a} ({b2})'
        medproof = '''    have := congrFun (medC_shift2 medEK t) q
    rfl''' if name == 'EK' else '''    have := congrFun (wireB_shift t n) q
    simp only [shiftC] at this
    exact this'''
        print(f'''
/-- The front law at the base distance, for ever from generation {g}. -/
theorem front{name} : ∀ s, run ({P}) ({g} + s + 4) = front {m} (run ({P}) ({g} + s)) ∧
    ∀ q, {m} - 2 ≤ unitOf q → unitOf q ≤ {m} + 3 → run ({P}) ({g} + s) q = {MED(f'{g} + s')} q := by
  have hf := facts{name}_ok
  simp only [facts{name}, Bool.and_eq_true, List.all_eq_true, List.mem_range] at hf
  exact {FOF} {m} {g} run{name} hf.1 hf.2

/-- The meeting from distance {b - a} + 2n, for every n: at generation 2n + {g} + r (r ≤ 4) the configuration is the
kernel's state, moved n units. -/
theorem state{name} (n r : Nat) (hr : r ≤ 4) :
    run ({PN}) (2 * n + ({g} + r)) = shiftC n (xorC (train (1 + ({g} + r))) (lcfg (d{name} ({g} + r)))) := by
  rw [run_add, pair_run .{A} .{B} rfl rfl {a} {b} (by decide) (by decide) (by decide) n, run_shiftC, run{name} r hr]

/-- **The meeting from every distance {b - a} + 2n, for ever**: from generation 2n + {g} on, four generations move
the configuration two units down at and below unit {m} + n and two units up above it, and the units {m} + n − 2 ..
{m} + n + 3 hold the medium. -/
theorem meet_{name} (n t : Nat) (ht : {g} ≤ t) :
    run ({PN}) (2 * n + t + 4) = front ({m} + n) (run ({PN}) (2 * n + t)) ∧
    ∀ q, {m} + n - 2 ≤ unitOf q → unitOf q ≤ {m} + n + 3 → run ({PN}) (2 * n + t) q = {MEDN('t')} q := by
  have red : ∀ s, run ({PN}) (2 * n + s) = shiftC n (run ({P}) s) := by
    intro s; rw [run_add, pair_run .{A} .{B} rfl rfl {a} {b} (by decide) (by decide) (by decide) n, run_shiftC]
  obtain ⟨hf, hm⟩ := front{name} (t - {g})
  rw [show {g} + (t - {g}) = t by omega] at hf hm
  refine ⟨?_, fun q h1 h2 => ?_⟩
  · rw [show 2 * n + t + 4 = 2 * n + (t + 4) by omega, red, red, hf, front_shift]
  · rw [red]
    show run ({P}) t (shiftPt (-(n : Int)) q) = _
    rw [hm _ (by simp only [unitOf_shiftPt]; omega) (by simp only [unitOf_shiftPt]; omega)]
{medproof}
''')
    print('end Gump.Tape.Signals')


if '--fronts' in sys.argv:
    fronts()
    sys.exit(0)
print('''/-
Generated by tape_meet.py (do not edit): the differences from the plain train of the front meetings of section 31
at their base distance, for the Lean chain of Gump/TapeMeetFront.lean, and the box translation of each step.
-/
import Gump.TapeBase

namespace Gump.Tape.Signals
open Gump
''')
for name, (D, g, m, steps) in data.items():
    ts = sorted({t for (t, k, *_ ) in steps} | {t + k for (t, k, *_ ) in steps})
    for t in ts:
        print(f'def d{name}{t} : List Pt := {lean_list(sorted(D[t]))}')
    print()
    print(f'def d{name} : Nat → List Pt')
    for t in ts:
        print(f'  | {t} => d{name}{t}')
    print('  | _ => []')
    print()
    if name == 'EK':
        print('/-- The holed train (train(1) with H at every odd unit, tape_meet.py), its unit at phase t % 4 and parity. -/')
        print('def medEK : Nat → Nat → List Pt')
        for ph in range(4):
            for par in (0, 1):
                print(f'  | {ph}, {par} => {lean_list(sorted(HTU[(ph, par)]))}')
        print('  | _, _ => []')
        print()
    print(f'/-- The steps of the chain: (generation, length, lo, hi, box translation). -/')
    print(f'def steps{name} : List (Nat × Nat × Int × Int × Pt) := [' + ', '.join(
        f'({t}, {k}, {lo}, {hi}, ⟨{V[0]}, {V[1]}, {V[2]}⟩)' for (t, k, lo, hi, V) in steps) + ']')
    print()
print('end Gump.Tape.Signals')
