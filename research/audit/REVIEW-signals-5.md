# Review: signals, fifth push (README sections 26–29: a listener)

Adversarial review, 2026-11-15. Code in `research/audit/signals5/`; commands are run from there. Bulk output:
`research/scratch/audit/signals5/` (ignored by git). Run times are single-core wall times on this machine.

**Steppers.** `st5.py` is written from `docs/AUTOMATON.md` §2 (no code from `sg.py` or `scat.py`): a sparse stepper
on the infinite lattice and a numpy batch stepper on the 3 × 3 tube inside the planes, whose upstream boundary unit is
refilled with the plain rake train (exact while the two units above it hold the plain train, which every caller checks
at every generation). `python3 check_st5.py` (45 s): the train formula is an orbit on the oracle; the sparse stepper
equals `reference/oracle.py` on the whole state (2 ends × 3 events × 140 generations); the tube stepper equals the
oracle on every unit ≥ −20 at every generation (8 ends, half healing and half dying, × 3 events: a hole, a two-cell
removal at an odd generation, a one-cell addition; 1,620 generations compared, 20 runs stopped where the disturbance
reached the boundary): ALL PASS. The only thing taken from the push is initial data: the cells of the ends
(`sat_gun.py --all` lists), the train's base cells (copied into `st5.PAT`, then checked on the oracle) and the
records of `gapstream*.jsonl`.

## Verdicts

| # | claim | verdict | in one line |
|---|---|---|---|
| 1 | §26 SAT negative | **confirmed, narrowed** | one hole (4, 4) at C = 29..39, (8, 8) at C = 31, and the words [0,1], [0,2,4] at C = 33 reproduced by an independent encoding with glucose4 / kissat404; (8, 8) at C = 33 cut; C = 29 is vacuous (no end exists there) and C ≤ 37 is also answered by the census; "movers are excluded too" holds only for ends that fit at C − 4k |
| 2 | §27 census, 741 ends, 599 heal / 142 die | **confirmed for holes; the dichotomy refuted for other gaps** | 741 recounted with an independent key; all eight words re-run on the whole state: 599 / 142 exactly; but the stream carries a second one-cell signal, and 503 of the 741 ends treat it differently from the hole |
| 3 | §28 beside the stream | **confirmed (no listener), narrowed** | divgap 1,034 / 1,021 / 13 / 0 reproduced; the four `LISTENER?` are false (oracle); one of the "28" is a plain-run gun death; of the 46 gun deaths only 25 are fires: beside capA, 8 turn the stream into another wire and 4 are **echoes**, a three-cell signal sent back up the stream through the rakes (oracle) |

## 1. The SAT negative (section 26)

**Reading `sat_listen.py` against the soundness argument.** Region, ties and times are as the README says: ua = KS −
2 − M = 0; X's units 0, 1 are tied to the holed train H at every generation, units 2..5 free; A and B are tied to the
train on units < 6 with the rule imposed on those cells (so the end may not disturb the train in front of it); X(0) =
A(0) and X(T) = B(0) on the whole region; the "≠" compares B(0) and A(T mod TA) on units ≥ 6, the same train phase on
both sides; T = 62 for one hole (66, 70, 70, 78 for the words). The hole is in the train X sees (H(0) = plain ⊕ hole,
the hole at units −4, −6, … at generation 0, and the script asserts it reaches nothing before generation 4).
Points found:

- **H is a finite piece whose downstream end is at unit 46.** Its own end burns back at half a unit per generation
  (measured with `st5.step`): it reaches unit 9 at generation 75 and units 0, 1 at about generation 88. The largest T
  in the push is 78 ([0,2,4]), so every instance is clean, by a margin of about ten generations; an instance with T ≳
  88 (e.g. `--word 0,2,4,6` or S ≥ 50 with [0,2,4]) would silently tie X to a burning train. `mysat5.py` builds H on
  units −400..300 and checks it against a longer piece.
- **"B is A moved … all are allowed, so movers are excluded too" is true only within the region.** B must be the
  train on units < 6 and lie inside the planes. A move by k units (either way) is therefore representable only for an
  end that, with k spare train units, still fits: an end at its lowest position must fit inside the planes C − 4k (a
  unit is 4 in x + y − z). At C = 39 the instance excludes one-unit movers of ends that fit at C = 35, two-unit movers
  of ends at C = 31, and so on; it says nothing about movers of the ends that need the full C = 39. (The census of §27
  steps its ends on the open lattice and finds no mover among its 741, for its eight words.)
- **C = 29 is vacuous and C ≤ 37 is implied by §27.** No absorber exists at C = 29 (§21; `python3 mysat5.py 29
  --same` is UNSAT in 5 s), so "UNSAT at C = 29" says nothing. At C = 31 there is one end, at C = 33 twelve, and every
  end at C ≤ 37 of period dividing 4 is in the census lists (complete by their final UNSAT), so for C ≤ 37 the SAT rows
  and the census answer the same question by two methods. The rows that reach ends the census does not list are C = 39
  (period 4) and none of the period-8 ones: the period-8 lists at C = 31 and C = 33 (`p4/abs8_fb_31.json`,
  `p4/abs8_fb_33.json`, both complete) hold only period-4 ends (`census5.py`), so (8, 8) at C = 31, 33 adds only that
  a hole cannot take an end into a period-8 orbit, which the census of the period-8 lists also implies.
- Nothing else found: TA = 8 does cover both arrival phases, the periods and the time allowance are as stated.

**Independent encoding** (`mysat5.py`): own region, constants and holed train; constant cells are folded into the
clauses instead of being tied variables; a sequential counter with full equivalence instead of the totalizer; solvers
glucose4 and kissat404 (the push used CaDiCaL 1.5.3).

| instance | verdict | time |
|---|---|---|
| `python3 mysat5.py 29` (one hole, (4,4)) | UNSAT (vacuous: `--same` also UNSAT) | 5 s |
| `python3 mysat5.py 31` | UNSAT, glucose4 | 41 s |
| `python3 mysat5.py 31 --solver kissat404` | UNSAT | 39 s |
| `python3 mysat5.py 33` | UNSAT, glucose4 / kissat404 | 36 s / 161 s |
| `python3 mysat5.py 35` | UNSAT | 103 s |
| `python3 mysat5.py 37` | UNSAT | 748 s |
| `python3 mysat5.py 39 --solver kissat404` | **UNSAT** (the one row beyond the census) | 787 s |
| `python3 mysat5.py 33 --word 0,1` | UNSAT | 135 s |
| `python3 mysat5.py 33 --word 0,2,4` | UNSAT | 74 s |
| `python3 mysat5.py 31 --mult 2 --multB 2` ((8, 8)) | UNSAT | 1,000 s |
| `python3 mysat5.py 33 --mult 2 --multB 2` | CUT at 1,500 s (the push: UNSAT in 994 s with CaDiCaL) | — |

**Mutation tests** (`mysat5.py`, glucose4):

| instance | expected | got | time |
|---|---|---|---|
| `31 --same` (no "≠") | SAT, the C = 31 absorber | SAT; A(0) is the 16-cell absorber of `p4/abs8_fb_31.json` cell for cell; re-stepped: periodic, the run reaches B, B = A | 33 s |
| `33 --fixA ../../scratch/signals/p4/abs4_fb_33.json:0 --onlyX` (a healing end, X alone) | SAT | SAT; re-stepped, the run equals the model and heals | 6 s |
| `33 --fixA …:0` (the same end, full instance) | UNSAT | UNSAT | 6 s |
| `33 --fixA …:5 --onlyX` (an end the census says dies) | UNSAT, because the end disturbs units 0, 1 | UNSAT | 6 s |
| `33 --fixA …:5 --freeB --S 0` (B's rule and period dropped, T = 22) | SAT, X(T) ≠ A(T) | SAT; re-stepped: the run equals the model's X(T) and differs from the undisturbed end | 3 s |
| `31 --freeB --S 0` and `31 --freeB --S 40` | (no expectation) | UNSAT both: the C = 31 absorber has healed by generation 22 | 37 s, 23 s |

So a dying end is excluded by the X-tie (it burns back into units 0, 1), not by the "≠" clause: the instance excludes
"an end that is changed and stops the stream" by its bound M = 4, which the README states. The push's wire-B control
(`sat_listen.py C --pattern 77 --event …`) was not re-run and not re-encoded.

## 2. The census (section 27)

**(i) Count.** `python3 census5.py` (10 s) keys each end by its minimal period and the sequence of its differences
from the train over one period, canonical under the train's symmetry (k units with 2k generations), computed with
`st5.step`: **856 entries, 741 distinct ends.** `python3 pairs5.py` (30 s): the push's key and this one make the same
partition. The 12 extra entries of the C = 37 list (and 12 of the C = 35 list) are exact translates by one unit of the
twelve C = 33 ends, stored with one unit of plain train in front (7 more cells). (A first version of my key counted
the train cells beyond the end as differences and found 753: that key was not translation-covariant; fixed.)

**(ii) Completeness.** `sat_gun.py --all` blocks each model by its generation-0 state on the free cells, which
determines the orbit (the left input is fixed), and the four lists end in "UNSAT: list complete"; every model was
re-stepped. Known ends are present: the C = 31 absorber and the twelve C = 33 ends are in the C = 37 list (as are all
90 of C = 35); the period-8 list at C = 33 equals the period-4 one as a set of ends; and **the line's receiving cap
capA, in its absorbing cycle and mirrored to a +v end, is one of the 741** (`census5.py`). So §27's "not covered: the
line's own receiving cap" is wrong in the push's favour, and "ends of period 8 at C ≥ 33" should read C ≥ 35.

**(iii) Echoes.** `python3 scan5.py --out ../../scratch/audit/signals5/scan5.json` (5.5 min) steps every end with each
word on the whole region (units −60 up to the planes, the train refilled at unit −61, any disturbance of units −60,
−59 recorded as "upstream"). All eight words: **4,792 = 599 × 8 healed (the whole state equal to the plain run, so no
echo can have left), 1,136 = 142 × 8 upstream**; the longest heal takes 39 generations. This covers the five words the
lead's oracle check does not, and the three it does. An echo would have shown as a row that never heals and never
reaches the boundary, or reaches the boundary with the end restored; neither occurs for the words.

**(iv) Every one-unit change of one arriving rake.** The same scan sends each end, at each generation g = 0..3 (the
two parities and the two arrival phases mod 4 of a period-4 end), the rake pair at units −10, −9 (followed): every
non-empty subset of the live cells of either unit removed (94 subsets at even g, 78 at odd g), every dead tube cell of
the two units made live (17 at even g, 18 at odd g), and the pair replaced by bare wire (the rake missing); with the
eight words, 426 events per end, 315,666 runs. Each event was first run on the bare train (`bare_classes`: 'vanishes',
'rides' as a bounded difference moving with the train, or 'breaks' the wire). Outcome table (summed over g):

| events (per end) | on the bare train | healed | upstream |
|---|---|---|---|
| subsets removed, 344 | vanish 16 | 11,856 | 0 |
| | ride 42 | 22,310 | 8,812 |
| | break 286 | 0 | 211,926 (8,892 with the end untouched at that moment) |
| one cell added, 70 | vanish 14 | 10,374 | 0 |
| | ride 4 | 1,458 | 1,506 |
| | break 52 | 0 | 38,532 (of them 2,964 with the end untouched at that moment: the break runs up the stream first) |
| bare wire, 4 | ride 4 | 2,396 | 568 |
| the eight words | ride 8 | 4,792 | 1,136 |

**No run ends in any third state**: every run either becomes equal to the undisturbed run on the whole region within
39 generations or sends a difference 66 units up the stream. `python3 echo5.py --U0 -250 --G 300 --which heal` (4 min)
re-ran every upstream row of a riding event on an end that heals the hole (3,888 rows) with the boundary 256 units up:
**all 3,888 are burns** (the train 20–40 units in front of the end is broken at generation 300): no echo, no end left
alive and changed. `python3 echo5.py --U0 -250 --G 300 --which die` (2 min) does the same for the 8,134 upstream rows
of riding events on the 142 ends that die on holes: **all 8,134 are burns**. (The 286 + 52 events that break the bare
train break the stream by themselves; their rows say nothing about the end and were not followed.)

**But the dichotomy is not a property of the end alone.** `python3 kinds5.py` (1 min) sorts the 58 riding events by
the signal they become on the bare train. Besides the hole (kind K1, 40 events: one cell (0,2,3) missing at even
generations, the hole of §21) there is a **second one-cell signal, K0** (6 events: e.g. the wire cell (0,1,4) of the
rake unit removed at an even generation, or (0,−1,2) added at an odd one; it rides as the wire cell (1,0,2) missing),
and a two-cell one, K3 (2 events). The ends fall into four classes:

| ends | K1 (hole) and the words | K0 | K3 |
|---|---|---|---|
| 113 | heal | heal | heal |
| 486 | heal | **die** | die |
| 17 | **die** | **heal** | die |
| 125 | die | die | die |

So 503 of the 741 ends tell the hole from K0, and 17 of them die on the hole and survive K0. The gap is still forgotten
or fatal (no listener), but which of the two depends on the end and on the kind of gap. These ends are detectors of the
fatal kind: a K0 signal arriving at one of the 486 destroys it and burns back up the stream, a hole does not.
Among them is the C = 31 absorber, the receiver of the beam (§21): it heals every hole but is destroyed by K0 and K3.
The line's capA is among the 113 that heal everything.

**On the oracle** (`python3 oracle5.py`, 3 min; initial cells and events in `research/audit/signals5/two_kinds.json`):
seven ends, each at the end of a finite train of units −100..5 on an even torus, stepped by `reference/oracle.py`,
with the hole of word [0] and two K0 events (the cell (0,1,4) of unit −10 removed at generation 0; the cell (0,−1,2)
of unit −10 added at generation 1). Ends #0 (the C = 31 absorber), #1, #2: the hole heals (whole torus equal to the
plain run from generation 5), both K0 events kill (at generation 100 the difference has run up to unit −28 while the
plain run's train at units −40..−20 is intact). Ends #9, #26, #28: the hole kills (difference up to unit −40 or −41),
both K0 events heal (whole torus equal from generation 34). End #10 (capA's end): all three heal. All seven as the
scan predicted.

## 3. Beside the stream (section 28)

**(i) `divgap.py 16`** (the push's script, re-run from `research/signals/`: 42 s): 71 standing placements (the same
list of (shift, phase) as §28 describes), 1,034 gap runs, **1,021 healed (471 beside or below the oscillator, 550
upstream), 13 destroy the oscillator (all beside or below), 0 `LISTENER?`**: the three headline numbers reproduced.
This re-runs the push's code (`sg.step_set`); it was not re-implemented.

**(ii) The four `LISTENER?` runs** (`python3 lis4.py`, 85 s, oracle only, from the line's generation 0). In all four
plain runs the wire units 2..11 are empty from generation 84 on, as the push says; both runs end in period 20 with the
oscillator in its free orbit; the final cycles differ. The gapped runs keep an 18-cell block on units 4..7 that the
plain runs lose (seen with `st5.step` on C20.29a gap 0), and neither final cycle is the working line (checked against line-C's own period-4 cycle at every
generation): debris in both. So "not listeners" is right: the placement without the gap is not standing (it burns the
line), and the gap changes only the debris.

**(iii) All 46 runs in which a gap kills the gun and the oscillator is kept** (`python3 c46.py`, 2 min; `st5.step`,
checked against the oracle on the first record of each file for 150 generations inside the script). Classification
of the difference between the gapped and the plain run on the wire (outside the oscillator's orbit): *fire*, every
wire unit between the oscillator and the gun holds less than half its plain cells 10 generations after the difference
reaches the gun; *compact signal*, for 12 generations or more the difference is at most 3 units wide and 6 cells and
moves towards the gun; *wall*, 2 generations before the gun is reached the wire between the oscillator and the front
is a uniform wire of repeat one unit different from the plain run's; *other*, none of these.

| zone | runs | fire | wall | compact signal | other |
|---|---|---|---|---|---|
| beside units 4..7 (`gapstream.jsonl`) | 28 | 23 (one of them C9.28a, whose gun also dies in the plain run) | 0 | 0 | 5: C18.25b ×2 (the oscillator beside the gun, no wire between), C18.30a ×2, one C20.29a |
| beside capA (`gapstream_end.jsonl`) | 18 | 2 (C9.28a) | 8: C13.24a, C22.23b, C26.37a, C32.33b, both gaps each | 4: C18.23a, C20.33c, both gaps each | 4: C17.31a, C30.32a |

So the push's "a fuse, not a signal" holds for the mid-wire sample (23 of 28 plainly; the other 5 spread without a
compact carrier), and **not for the receiving end**:

- *Wall* (C13.24a, on the oracle: `python3 orc46.py`): the hole reaches the end, and from the end a front moves up the
  wire at one unit per 2 generations; behind it the wire is uniform, of repeat one unit and period 2, with base cells
  {(0,0,1),(0,0,3),(0,0,5),(0,1,2),(0,1,4)} and {(0,1,2),(0,1,4),(0,2,3),(1,0,0),(1,0,4)} at the two parities (not
  wire C: (1,0,4) in place of (1,0,2)). The stream is converted, not burnt.
- *Echo* (all four runs on the oracle: `python3 orc46.py`, 10 s; initial states in `end_echo.json`). C18.23a gap 0:
  the hole reaches
  capA with the oscillator beside it at generation 18; from generation 24 to 38 the **whole-state** difference between
  the gapped and the plain run is exactly three cells, (1,2,2) of unit u and (0,0,3), (0,0,5) of unit u + 1, moving
  rigidly one unit towards the gun every two generations, through the oncoming rakes; capA, the oscillator and every
  rake are as in the plain run. It reaches the gun at generation 40 and the gun dies. The other three runs (C18.23a gap
  1, C20.33c gaps 0 and 1) give the same three-cell signal, rigid over the 14 generations checked. The end is restored, so this is
  not a listener; it is a reflector that turns a gap into a counter-propagating signal, the "rake turned against the
  stream" that section 29 asked for.

## 4. Corrections

Applied to `research/signals/README.md` (sections 26–29 and the fifth-push introduction), each marked *Review*:

1. Introduction: the SAT negative stated with its bounds (period dividing 4 / 8, holes and four words, settling 42
   generations, disturbance of at most 4 units in front), C = 29 vacuous, C ≤ 37 also answered by the census; the
   census words are words of one-cell holes.
2. §26 "movers are excluded too": only for ends that fit at C − 4|k| (B must be the train on units < 6 and inside the
   planes). Added to "what this does not exclude".
3. §26 after the table: C = 29 vacuous; C ≤ 37 rows are a second method for the census's question; which rows were
   reproduced independently (one hole (4, 4) at C = 29..39; (8, 8) at C = 31; [0,1] and [0,2,4] at C = 33); the finite holed train H limits T to about 88.
4. §27 "which of the two is a property of the end alone": true for holes, false for gaps in general (the second
   one-cell signal K0; four classes of ends; oracle-checked on seven ends).
5. §27 "Not covered": period 8 not covered from C = 35 (not 33); capA is in the census (it was listed as not covered).
6. §28: one of the 28 mid-wire gun deaths (C9.28a) is a plain-run gun death; all 46 were looked at; beside the
   receiving end 16 of 18 are not fires (8 walls, 4 echoes, 4 other).
7. §29: "Not checked" updated with what this review checked; "perfect sink for gaps" narrowed to holes; the "where to
   go next (1)" question answered (echoes exist; nothing upstream survives them yet).

Not applied (outside sections 26–29 or not mine to change): `gapstream.py --summary` tests `gap_gun` before
`plain_gun`, which mislabels a run in which both guns die (C9.28a); `sat_listen.py` builds H on units −400..KS + 40,
which is too short for T ≳ 88; `PREDICTIONS.md` scoring: the scores and the Brier mean (0.06) recompute correctly
from the stated probabilities; P1 "failed" is right but its C = 29 part is vacuous.

## 5. Not checked

- Of the push's SAT rows, these rest on `sat_listen.py` alone: (8, 8) at C = 33 (my encoding was cut at 1,500 s), the
  words at C = 31, 35, 37, the words [0,2] and [0,1,2] at C = 33; no proof certificate
  was produced for any UNSAT (pysat's glucose4 / kissat404 verdicts only). The wire-B pulse control was not re-run.
  The 5 × 5 tube was not attempted.
- The census's 1,500-generation transients: the review's scan stops at 400 generations, which no row reached (every
  row healed within 39 generations or reached the boundary).
- The events that break the bare train by themselves (338 per end) were not followed: the end then receives a broken
  stream, not a gap.
- Events larger than one unit of the train (other than the eight words), events at other distances from the end, and
  additions of cells outside the 3 × 3 tube were not tried.
- §28's catalogue samples were not re-run (only their not-healed records were re-examined); the 5 "other" mid-wire
  and 4 "other" end runs were not characterised further; the wall's wire was not matched to the family of section 9.
- Which of the 46 behaviours depend on the placement only through the hole's arrival phase was not studied; the echo
  was put to the oracle for its four runs and the wall for one (C13.24a, gap 0); the other walls, the "other" runs
  and the fires rest on `st5.step` (checked against the oracle inside `c46.py` on one record per file). Whether the
  echo signal survives anything upstream other than the gun, or what it is on bare wire, was not looked at.
