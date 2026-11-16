# Review: signals, sixth push (README sections 30–35: the four signals, their meetings, the gun end, the reflector)

Adversarial review, 2026-11-15. Code in `research/audit/signals6/`; every command is run from there. Bulk output:
`research/scratch/audit/signals6/` (ignored by git). Times are single-core wall times on this machine.

**Steppers.** `st6.py` is written from the cube-index table of `docs/AUTOMATON.md` §2 (its offsets are also asserted
equal to the doubled-offset description), with no code from `research/signals/` or `research/audit/signals5/`: a sparse
stepper on the infinite lattice and a numpy batch stepper on a fixed cell set (the 3 × 3 tube, or a wider tube, on a
long unit range; cells outside are dead for ever by T2). `trains6.py` holds the train in the push's frame (base cells
read from `objects/echo-train.json`) and in review 5's frame (base cells copied from `st5.py`), both checked to be
orbits. `frame6.py` finds the map between the frames (the wire-C mirror, then −5 units and one generation) by search.
`python3 check6.py` (161 s): both steppers equal `reference/oracle.py` on the whole state, every generation, 1,050
generations over 15 runs (one-cell and two-cell events of each kind, a break, three flips outside the 3 × 3 tube on the
wider tube, four census ends with an event 16 units in front): ALL PASS. Taken from the push or the previous review
as initial data only: the train's base cells, the signal cells (`echo-train.json`), the gun list
(`p6/guns_5f_37.json`), the 741 ends (`scratch/audit/signals5/ends.json`), the reflector records (`end_echo.json`), the
line (`line-C.json`).

## Verdicts

| # | claim | verdict | in one line |
|---|---|---|---|
| 6 | correction to review 5 (`bare_classes` misses up-movers) | **confirmed, and closed** | 16 of the 338 'break' events become E (14) or U (2) alone; all 11,856 end rows are the undisturbed end for ever; nothing alive and changed |
| 1 | §30 four signals | **confirmed for one-cell flips; "the four signals of the train" refuted** | 112 events reproduced exactly; five more rigid signals exist (K3; N1 up; N2, N3 down; N4 down, partly outside the tube), all proved and on the oracle |
| 2 | §31 meetings | **confirmed, fronts now proved; one word claim refuted** | one meeting per pair at every offset 1..41; fronts proved for ever by a gluing script; s = 2 is not clean (a pulse rides down in the wire B); B′ standing proved for ever for s = 3..14 |
| 3 | §32 the gun end | **confirmed, and widened** | 67 distinct guns (not 68); own encoding that allows ANY return: E UNSAT at C = 31..37 (glucose4; C = 31 also maplechrono and T = 48) |
| 4 | §33 the reflector | **confirmed** | one-cell coupling at (2,0,−1), generations tg + 16, 18, 20, on the oracle; not reusable at s = 1..20; own encoding (any return up the stream) UNSAT for H at C = 31, 33, for K0 at C = 31 |
| 5 | §34 no loop, no listener | **confirmed within bounds** | see 3 and 4; the push's "no loop can be built from these parts" holds only for period-4 guns and ends in the 3 × 3 tube at the stated C and T |

## 1. Item 6 first: the events review 5 did not follow

`python3 scan6a.py bare` (4 s) rebuilds the 426 events of `scan5.py` (its description, my code) in review 5's frame
and runs each on the bare train (units −230..230, read at generation 102, rigid components checked at 106, 110 and
named by the push's shapes mapped with `frame6`). Per end: words 8 (H ×4, H H, H ×5, two in one cluster ×2);
removals 344 (vanish 16; H 30, K0 4, K3 2, two H 6; **E 10, U 2**; break 274); additions 70 (vanish 14; H 2, K0 2;
**E 4**; break 48); bare wire 4 (H). Review 5's classes are reproduced exactly (ride 42 + 4 + 4 + 8, vanish 16 + 14,
break 286 + 52 = 338), and the 338 are 16 up-makers (none with a second signal) and 322 events that break the bare
train by themselves (`python3 breaks6.py`, 12 s: all 322 still break at generation 202, none becomes a signal later).

`python3 scan6a.py ends` (15 s) runs the 16 up-making events against each of the 741 ends (3 × 3 tube, planes C ≤ 39,
units −100..15, each end checked to leave units < 6 as the plain train). Criterion: at generation 42 the whole-state
difference from the undisturbed run equals the bare-train difference (the departing signal) and lies at least 6 units
below the lowest unit at which the undisturbed run differs from the train. Then the end is equal to the undisturbed
end for ever: the state is (undisturbed run) xor (signal), the signal's neighbourhood is plain train, so by the
two-generation identity it rides on, away from the end, and the end never sees it.

| events | rows | equal to the undisturbed end (for ever) | dead | alive and different |
|---|---|---|---|---|
| 14 that make E | 10,374 | 10,374 | 0 | 0 |
| 2 that make U | 1,482 | 1,482 | 0 | 0 |

On the oracle: `python3 orcA6.py` (19 s): ends #0 (the C = 31 absorber), #10 (capA's end), #300, each with event #16
(→ E) and #221 (→ U), finite train on a box torus, whole torus: the difference at generation 42 is the bare signal,
6 or more units from the end: ALL PASS. **Nothing alive and different; no listener here.** Review 5's sentence "no
end is left alive and changed" now stands for all 426 events: the 58 riding ones (review 5), the 16 up-makers (here),
and the 322 that break the stream themselves, which leave no stream to speak of.

## 2. The signals (section 30)

`python3 kinds6.py one` (1 s): the 112 one-cell flips (tube cells of units 0, 1, phases 0..3), run to generation 101
(the push stopped at 41–44): vanish 24, break 66, E 6, U 2, H 8, K0 6, the same events as the push's table. The train
is invariant under two-unit translations and its 4-cycle, so these are all one-cell flips inside the tube.

`prove_echo.py`'s argument holds: its comparison is of the whole infinite state at generation 2 (on units −27..26 by
computation, elsewhere the train by locality), not of a window round the signal, so there is no distance it misses.
`python3 sig6.py` (5 s) repeats it for every signal below and runs each on the oracle on a ring of 48 units (box torus
96 × 32 × 96), every even generation 0..120, whole torus: all PASS.

Wider sets: `kinds6.py two` (15 s, every two-cell flip inside units 0, 1: 1,512 events), `two3` (30 s, one cell in units
0, 1 and one in units 2, 3: 3,136), `wide` (35 s, one-cell flips of the cells of the tube −3 ≤ x+y+z, x−y+z ≤ 9 outside
the 3 × 3 tube, units 0, 1: 480). Components are named by exact cover with the known signals; what cannot be covered:

| signal | dir | cells at phase 1 (relative to unit u, parity) | made by |
|---|---|---|---|
| K3 | down | (0,0,3) of u, (0,0,5) of u+2 (u even) | two-cell flips (9 in `two`, 15 in `two3`); review 5's K3 |
| **N1** | **up** | (0,0,1), (1,2,2) of u; (0,0,3) of u+1 (u even) | two-cell flips (4 + 2) |
| N2 | down | (0,0,3) of u; (0,0,1), (0,0,3) of u+1; (0,0,5) of u+2 (u even) | two-cell flips (2 + 5) |
| N3 | down | (0,0,3) of u; (0,0,1), (0,0,3) of u+1; (0,0,3) of u+2 (u even) | two-cell flips (7) |
| N4 | down | (0,0,3), (1,2,2), (1,2,4) of u (u odd); (1,2,4) is outside the 3 × 3 tube | one-cell flips outside the tube (8) |

So the push's four are complete for one-cell flips inside the tube, and **not** the train's signals: nine are known.
N1 is a third up-moving signal. Everything in sections 32–33 that names "E or U" or "H or K0" as the signals that
can be returned is narrower than the set that exists. Not tried: three-cell flips, flips further from the tube.

## 3. Meetings (section 31)

**The parity argument** is right: with phase-1 positions of fixed parity, configurations of one ordered pair are
labelled by b − a, the dynamics lowers it by 2 every two generations, and 2-unit translations are symmetries. Test
(`python3 meet6r.py opp`, 20 s; units −320..320, exact window asserted): for every pair, every offset of the allowed
parity from 1 to 41 units, each run with offset d + 2 equals the run with offset d two generations earlier moved one
unit, every generation 0..198: no exception (also at the smallest offsets). Outcome at generation 200, every offset:
E–H and U–H wire B between two edges, E–K0 the holed train between two edges, U–K0 the plain train exactly (cancel),
as claimed. New: E–K3 the holed train (as E–K0); **U–K3 leaves one H** (oracle).

**The fronts, for ever.** `glue6.py` writes the gluing step as a lemma and a check (docstring): if the state is a
medium M with Φ(M) = M (Φ = four generations; wire B and the holed train both checked on an 80-unit piece) except on
pieces separated by at least 8 units of medium, the lowest moving −2 units and the highest +2 units per Φ (any in
between standing), and each piece satisfies Φ(S) = S moved on its units widened by 4, then the orbit is the glued one
for every later time (a unit within 4 of a piece sees, over Φ, only units within 8, where the state is the piece's
translate; any other unit sees medium). It passes at generation 196 → 200 for E–H, U–H, E–K0, E–K3 at every offset
1..41. So the four front outcomes are **proved for ever on the infinite train**, not by hand.

**Same direction** (`python3 meet6r.py same`, 3 s; spacing 1..12): every non-overlapping pair of E, U travels together,
and every pair of H, K0 except H with K0 one unit apart; each travelling pair passes the two-generation identity from
generation 0, so it travels for ever. "U one unit above E" is not a pair: E and U then share the cell (0,0,3) of
unit u + 1 (their xor is a two-cell change, not two signals). K3 fails at 1 or 3 below H, 2 below K0 or K3, 1 above H.

**Words** (`python3 meet6r.py words`, 13 s; units −420..420, generation 240): E against two holes s rakes apart:
s = 1 clean wire B; **s = 2 is not clean**: a pulse of one to three cells rides down inside the wire B at the speed of
the lower edge, a few units above it (non-wire-B units −23..−21 at generation 100, −93..−91 at 240); the push read the
medium only on 8 units round the middle. s = 3..14: a B′ stretch on units s + 8 .. s + 10, **standing for ever** (the
gluing check passes with a standing piece). 3, 4, 5, 6 holes at spacings 3 and 4, and the words (21, 27, 33, 41),
(21, 27, 35), (21, 29, 33): the stretch has 2 + (number of holes) units, so each further hole adds one unit, also one 2
rakes behind the previous (21, 29, 33). On the oracle (`python3 orc6.py`, 30 s; ring of 128 units, box torus
256 × 32 × 256): U–K3, U–K0, E–K0, E–K3, E–H, s = 2, s = 3 and four holes 3 apart equal the linear runs above, whole
torus, at generations 20, 40, 60, 80: ALL PASS.

## 4. The gun end (section 32)

`python3 guns6.py` (5 s): the 68 entries, each aligned to the train by search (period dividing 4, units < 6 the
train) and keyed by its orbit translated to its lowest differing unit and re-indexed to train phase: **67 distinct
guns** (entries 15 and 40 are one gun). Each hit by E, U, N1 at unit −30/−31 (3 × 3 tube, planes C ≤ 37, units
−300..15, 160 generations): E kills all 68; U is absorbed exactly by #0, 1, 2, 4, 8–14 (the push's eleven); N1 kills
all 68. No gun returns anything.

**Own encoding** (`mysat6.py`; own CNF: a totalizer with full equivalence, Tseitin gates, no code from `scat.py` or
`sat_gun*.py`; pysat glucose4 unless stated). Push frame; A a gun of period dividing 4 (train phase t at generation t),
B one at train phase T + 1; X(0) = A(1) xor the signal four units in front of the gun. Instead of enumerating return
histories it uses the light cone: a cell of unit u at generation k with u ≤ KS − 1 − k depends only on the train and
the signal and is a constant (the free run); every other cell of the region is free with the rule imposed. At T:
X(T) = B(0) on the gun and the 4 units in front. So a model is a gun that is a gun again at T **whatever it has sent
down the stream** (any signals, two of them, a front): a relaxation of the push's instance in returns, the same in
period, tube and planes; its time allowance is T = 36 after the signal is set 4 units in front (the push: 52 after it
is set 10 units in front; both leave about 30 generations after arrival).

| instance | expected | result | time |
|---|---|---|---|
| `mysat6.py 31 --kind none --T 12` | SAT | SAT, re-stepped: A, B periodic, run reaches B | 5 s |
| `37 --kind U --fixA 4` (a gun that absorbs U) | SAT | SAT, re-stepped | 2 s |
| `37 --kind E --fixA 4` | UNSAT | UNSAT | 2 s |
| `37 --kind U --fixA 3` (a gun U kills) | UNSAT | UNSAT | 2 s |
| `37 --kind U` | SAT | SAT, re-stepped | 30 s |
| `31 --kind E` | — | **UNSAT** (also `--solver mcb`, maplechrono: UNSAT 29 s) | 16 s |
| `31 --kind E --T 48` | — | **UNSAT** | 73 s |
| `33 --kind E` / `35` / `37` | — | **UNSAT** / UNSAT / UNSAT | 61 / 20 / 85 s |
| `39 --kind E` | — | CUT (external timeout 1,500 s) | — |
| `31 / 33 / 35 --kind N1` | — | UNSAT / UNSAT / UNSAT | 9 / 26 / 38 s |
| `37 --kind N1` | — | UNSAT | 68 s |
| `31 / 33 --kind U` | — | UNSAT / UNSAT (no U-absorber fits below C = 37) | 31 / 14 s |
| `35 --kind U --diffwin 28` (restored AND something sent down) | — | UNSAT | 47 s |
| `37 --kind U --diffwin 28` | — | **UNSAT** | 883 s |

So: no gun of period dividing 4 in the 3 × 3 tube at C ≤ 37 survives E by T = 36 whatever it answers; in particular
none answers with K3, N2, N3, two signals or a front, which the push's instance did not exclude.

**The push's instance.** Read for what it excludes: the signal arrives at one phase only, which is enough (all
period-4 guns see an up-mover arrive at one phase: its trajectories differ by 4-generation shifts); B may be any gun,
so a gun that turns into a different gun is excluded; returns are one H or one K0 only: not K3, N2, N3, N4 (N4 cannot
exist in the tube anyway), not two signals, not a front, not a return later than T − 8; nothing at period 8 or
outside the tube. Mutation (`python3 pushsat6.py U37`, 55 s, the push's script imported unchanged, CaDiCaL): the U
instance at C = 37 is SAT (history "none", a 26-cell gun), and that gun, re-stepped with st6 with U 37 units away,
equals the undisturbed run from generation 74 on. A planted "no signal" instance cannot be built with the push's code
(its history builder needs a non-empty signal); not done. The push's E instance was not re-run.

## 5. The reflector (section 33)

`python3 refl6.py couple` (49 s, every step on the oracle, records 0 and 2 of `end_echo.json`): C18.23a plain: no
coupling in 60 generations; holed: exactly three coupled generations, tg + 16 (the cell (2,0,−1) dies only in the
separate steps), tg + 18 and tg + 20 (it is born only jointly). C20.33c: coupled at every generation through
(1,0,−2), plain and holed. As the push says. Not checked: that the plain C18.23a run is periodic within 60
generations (so "only when a hole arrives" is shown for 60 generations).

`python3 refl6.py words` (18 s; line N = 70, st6): one hole returns one E (both oscillators); K0 is not returned as a
signal (C18.23a: 12 cells, not signals; C20.33c: the end destroyed); **two holes at every spacing s = 1..20 rakes:
never one E**: from s = 2 on, wire B on the stream (4 units at s = 2, 2s − 1 units at s = 3..20, read at generation
2(21 + 2s) + 40 after the word), and at s = 1 a 13-cell difference that is not a set of signals. Consistent with the meeting result, which is proved at every offset.

**Own encoding of the reflector negative** (`mysat6.py --frame5`: review 5's frame, the train moving into an end at
units ≥ 6, the signal mapped by `frame6`; the same light cone; at T = 36: X(T) = B(0) on the end and the 4 units in
front, and `--diffwin 28`: at least one cell of the 28 units above that differs from the train, i.e. the end is
restored and has sent something, anything, up the stream):

| instance | expected | result | time |
|---|---|---|---|
| `31 --frame5 --kind H --T 24` (no "sent") | SAT (the 16-cell absorber heals H) | SAT, re-stepped | 8 s |
| `31 --frame5 --kind H --diffwin 28 --plusE 12` (an E also on the stream) | SAT | SAT, re-stepped (the E is the difference) | 12 s |
| `31 --frame5 --kind H --diffwin 28` | — | **UNSAT** | 14 s |
| `33 --frame5 --kind H --diffwin 28` | — | **UNSAT** | 21 s |
| `35 --frame5 --kind H --diffwin 28` | — | **UNSAT** | 79 s |
| `37 --frame5 --kind H --diffwin 28` | — | CUT (external timeout 1,200 s) | — |
| `31 --frame5 --kind K0 --diffwin 28` | — | **UNSAT** | 20 s |

This is wider than the push's (any answer up the stream, not one E or U).

## 6. Corrections applied to README sections 30–35 (each marked *Review (REVIEW-signals-6 …)*)

1. §30, after the proof: the census reproduced; complete for one-cell flips inside the tube; five more signals.
2. §30, the correction to review 5: counted and followed (16 up-makers, every end unchanged for ever).
3. §31, the parity paragraph: tested at every offset 1..41; K3 meetings.
4. §31, the fronts: proved for ever by `glue6.py`, no longer by hand.
5. §31, same direction: to spacing 12, proved; "U one unit above E" is an overlap.
6. §31, words: s = 2 not clean (a pulse); B′ standing proved for ever; the count checked for longer words.
7. §32: 67 distinct guns; the own SAT encoding and what the push's instance does not exclude.
8. §33: coupling on the oracle; two holes at s = 1..20; own reflector encoding.
9. §35: "not checked" updated; the "four signals" and "one H or K0" wording narrowed.

Not applied (outside 30–35 or not mine): `PREDICTIONS.md`: the investigator's Brier scores recompute correctly
(mean 0.103); Q14 / S32 "failed" is defensible but the B′ stretch is now proved to be a lasting state of the infinite
train (written by holes, erased in the finite line by the gun's fire): the lead may want to say so. `meet6.py` reads the
medium on 8 units round the middle, which is how it missed the s = 2 pulse.

## 7. Not checked

- Signals: three-cell flips; flips further outside the tube; the meetings of N1, N2, N3, N4 with anything; the
  divider's stream (§30 "Other media") was not run.
- Meetings: offsets beyond 41 (covered by the orbit argument, not by runs); words other than those listed; mixed
  words with K0 (`meet6.py`'s five) were not re-run.
- Guns: E at C = 39 in my encoding (cut at 1,500 s); SAT negatives at period 8, in the 5 × 5 tube, with a settling time longer than T = 36 (48 at C = 31); no UNSAT
  certificate (pysat verdicts only); the push's E instance and its C = 39 row were not re-run by me with its code.
  The oscillator samples beside the gun (`oscecho.py`) were not re-run.
- Reflector: SAT negatives at C ≥ 37 (C = 37 cut at 1,200 s), K0 at C ≥ 33, and for U-returning answers beyond the window of 28 units;
  catalogue placements other than the two known.
