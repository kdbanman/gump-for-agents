# Review of signals push 9 (the call line, the still life at the wall, P3.15f)

2026-11-18. Reviewed: `research/signals/push9/` (README.md, PREDICTIONS.md, its scripts, `objects/call9.json`,
`objects/trigger9.json`). Code and outputs of this review: `research/audit/signals9/` (commands below are run from
there; outputs are in `out/`). Run times are for one process on the shared 4-core machine.

Tags: **[oracle]** = `reference/oracle.py`'s `step` on a torus in which nothing wraps (section 1);
**[st9]** = this review's stepper, itself checked against the oracle (section 1); **[proved]** = an argument written
out here whose base facts are oracle runs; *measured* = runs only.

## 0 Verdicts

| # | claim of the push | verdict | check |
|---|---|---|---|
| 1 | store wire and line stand together as the two alone | **confirmed** [oracle, k = 0..8] | `python3 call_oracle.py stand` (2 s) |
| 2 | the CALL passes the crossing and goes on unchanged; the line is afterwards cell for cell what it was | **confirmed**, and sharper: at *every* generation the line with its pair is exactly the line it would be with no store wire (section 2.2) [oracle, k = 1..12, 16, 20, 25, 30, 40] | `python3 call_oracle.py call 1,2,3,4,5,6,7,8,9,10,11,12` (130 s), `call 16,20,25,30` (165 s), `call 40` (126 s) |
| 3 | `d^k f` leaves as exactly k left-going pulses two units apart, the wire plain behind | **confirmed** [oracle, same k]; exact from generation 2k + 34 after a CALL seeded 15 line units before the crossing; **proved for every k** on the infinite wire (section 3) | same commands; `python3 proof9.py` (125 s) |
| 4 | it calls again: set, add, call, set, add, call | **confirmed** [oracle], with other places and times than the push's | `python3 call_oracle.py proto` (107 s), part C1 |
| 5 | move: a second store on the wire then holds the sum | **confirmed** [oracle]: 1+3, 2+5, 1+1, 4+2, the receiver's edge 25, 20, 12 and 3 units before the crossing | `proto`, C2 |
| 6 | chain: two stores, a line at each | **confirmed** [oracle] | `proto`, C3 |
| 7 | bus: one line across two store wires calls both | **confirmed** [oracle, 5 line units apart]; distances 3..12 work, 2 does not stand [st9] | `proto`, C4; `python3 extra9.py line` (20 s) |
| 8 | "A CALL does nothing to an empty wire" | **corrected**: true only while no pulse of the store wire is near the crossing. With one store pulse under way, 4 of 50 birth places end in a destroyed or converted store wire, two of them with a changed line [oracle] (section 2.3) | `python3 beyond9.py pulse --orc` (239 s) |
| 9 | "... or to a stretch that begins anywhere else" | **confirmed**: first unit at c + 1 + o, o = −8..10, k = 1..6: stands at every o, released only at o = 0 [st9; oracle at o = −1, 0, +1, k = 3] | `python3 beyond9.py offsets --orc` (83 s) |
| 10 | "Pulses of the store wire pass under the line in both directions" | **corrected**: on an empty wire, yes. A pulse that reaches an *armed* store from the left passes under the line, is absorbed, and moves the wall onto the crossing unit; the store (k + 1) then stands and is no longer released by a CALL [oracle, k = 3] | `python3 beyond9.py left --orc` (41 s) |
| 11 | "The CALL is push 8's hand release": equal at generation 90 + 4k, k = 1..40 | **corrected** (sharpened): the CALL's whole effect on the store wire is ONE cell made live at generation 29; the store's run equals the hand release cell for cell from generation 2k + 32 exactly, k = 1..40 [oracle for the first statement, st9 for the second] | `call_oracle.py call …`; `python3 extra9.py hand` (3 s) |
| 12 | "What destroys it": one pulse, three adjacent, two with a gap, at an armed crossing; all pass on an empty wire | **confirmed** [oracle at k = 0 and k = 3; st9 k = 0, 1, 2, 3, 5]; extended to 23 words (section 2.3) | `python3 beyond9.py words --orc` (212 s) |
| 13 | a left-going pair from the far side also calls | **confirmed** [oracle, k = 3] | same |
| 14 | the law for every k: "conjectured; route" | **proved** for the infinite store wire, given the base runs, T2 and the tape theorem (section 3) | `python3 proof9.py` |
| 15 | still life at the wall: block `b^(2k+2)`, worth k + 1, the still life never changes, single use | **confirmed** [oracle, k = 1..8, both arrival parities; worth k + 1 for k = 1..6] | `python3 trig9.py` (111 s) |
| 16 | P3.15f: "passes both pulses on plain wire with everything restored" (one timing tried), releases `d^3 f` as three pulses; "not yet a reusable same-wire trigger" | **corrected and completed**: a right-going pulse passes at ONE arrival timing in three (the other two change the wire or the oscillator); at that timing it releases exactly k pulses for k = 1..10 and the oscillator is as it would have been. It IS a reusable call on the store's own wire by one pulse, for pulses clocked to that timing; object and oracle verifier written (section 5.2) | `python3 verify_osc9.py` (65 s); `python3 osc9.py scan` (157 s), `osc9.py wall --push` (14 s), `--part 0/2`, `--part 1/2` (327 s, 319 s) |
| 17 | the 13 still lifes of at most 8 cells: 3,780 standing placements, 147 triggers (59 `b^11`, 59 `b^8`, 21 erased, 8 `bb`), 59 falls as `b^6` | **confirmed** by an independent enumeration [st9] | `python3 osc9.py still` (471 s), `osc9.py falls` (62 s) |
| 18 | the push's steppers equal the oracle (`check9.py`), `call9.py --law`, `reduce9.py`, `cell9.py --law` | **confirmed**: they pass as stated when run from the push's directory | outputs in `out/push_*.txt`; check9 parts A 66 s, C 3 s, D 142 s, E 62 s |
| 19 | forecasts: Brier 0.295 / 0.234 | arithmetic **confirmed**; two outcomes depend on a reading (section 7) | by hand |
| 20 | still lifes of 9 to 11 cells, the 37 oscillators other than P3.15f, the crossing scan (`cross9.py`), `ghost9.py` beyond two cells, `ghostpairs9.py`, `rearm9.py`, the block-meeting table, the fuse, the other release lines | **not checked** | |

Nothing in the push's account is refuted outright. Three statements are false as worded once a second signal is
present (rows 8 and 10, and two CALLs in quick succession, section 2.3).

Found here and not in the push:

- **A subtraction of one with a zero exit** [oracle, k = 0..5; st9 to k = 10] (section 2.4): a CALL and one
  right-going store pulse born 17 units before the crossing at the same generation. For k ≥ 1 exactly k − 1 pulses
  leave to the left and nothing leaves to the right; for k = 0 the pulse goes on to the right. A store on the left
  then holds its count plus k − 1.
- **Two CALLs need 4k + 2 generations between them** (section 2.3).
- **Write, read and call do not coexist usefully** (section 4): where push 8b's reader can tell the stretch it is
  destroyed by a write or by a CALL; where it survives it reads the same answer whatever the count.

## 1 Instruments

- `a9.py`. From the push only initial cells are read, in Python: the caps, stators and sites of the wire family,
  the 162 cells of the line and the two cells of the CALL (`objects/call9.json`), the six cells of the still life
  and the extra cells of six start states (`objects/trigger9.json`). No module of `research/signals/` is imported.
- **Oracle runs** (`a9.Orc`, and the same construction inside `verify_osc9.py`): `oracle.step` unchanged on a
  rectangular array torus whose masks are `oracle.masks`' formula for the array's shape. After every generation the
  four outermost index planes on every side are asserted dead. A cell's neighbours are at most 2 sites away, so no
  neighbour count ever includes a wrapped cell and the run is the run of the infinite lattice whatever the size.
  The exact max-norm distance from the live cells to their nearest torus image is computed and printed (26 to 44
  sites in the runs below).
- **st9.c**, a sparse stepper written for this review (neighbour offsets from `docs/AUTOMATON.md`).
  `python3 check_st9.py` (77 s, ALL PASS): st9 = oracle = a pure-Python set stepper at every generation on six
  random soups; a wrong rule (B45/S34) is noticed on all six; `a9.Orc` equals a cubic-torus run made with
  `oracle.masks(H)` as the oracle's own main does; st9's ring mode equals the oracle on a cubic torus. Beyond that,
  st9 is compared with the oracle at every generation of every run marked [oracle] in sections 2 to 5.
- The push's `verify_call9.py` computes that every live cell stays near a start cell; its `verify_trigger9.py`
  relies on the size of its torus. The runs of both objects were redone here with the guard planes.

Geometry used below (derived from the cells): the store wire is wire B along (1,0,−1), unit u = cells with x in
{2u, 2u + 1}; the line is wire C in the frame (x, y, z) → (x, −z, −y) + (28, −34, −72); it crosses the store wire at
store unit c = 35 (line unit 21 of 26) without touching it (closest cells 3 apart in max-norm). The CALL of
`call9.json` is two cells of line unit 6, 15 line units before the crossing; laid as the word `9df` it moves one
line unit per two generations. R@u / L@u = the stator (0,1,2) / (0,1,4) of store unit u removed at an even
generation (a right-going / left-going pulse).

## 2 The call

### 2.1 The push's claims

Rows 1 to 7 of the table. The cycle on the oracle (`proto` C1): set by R@c−10 and L@c+13, adds by L@c+12, L@c+16,
L@c+11, CALL: four pulses leave; set by R@c−6 and L@c+9, add, CALL: two leave; 14 whole-state checks (letters of the
store wire + the line at rest), st9 = oracle at every generation 0..1002; torus (140, 90, 140), nearest image 28.
Chain: stores 2 and 3 with a line at each (684 cells); CALL at the right line gives 5 in the left store with its wall
still one unit after its own crossing; CALL at the left line: five pulses, both lines at rest. Bus: two store wires
5 line units apart under one line of 31 units (767 cells): one CALL moves 3 and 2 exactly.

Only one arrival phase exists: store and line both have period 2 and pulses are born at even generations. The pair
seeded at line units 1..18 (or laid as `9df` at units 0..18) gives the same release; seeded at line unit 0 it changes
the line (378 cells remain) [oracle] (`python3 beyond9.py dist --orc`, 44 s).

The line can be much shorter [st9, `extra9.py line`]: with 5 to 21 units before the crossing and 1 to 4 after it
(the caps kept) it stands with `d^3 f` and calls; the smallest tried is 6 before + 2 after = 77 cells.

### 2.2 What the CALL is, exactly

For k = 1..12, 16, 20, 25, 30, 40 [oracle; three runs compared cell for cell at every generation]:

**X_k(t) = V_k(t) ⊔ Lf(t) for every t**, where X_k is the store `d^k f` with the line and the CALL made at
generation 0, Lf is the line alone with the CALL, and V_k is the store wire ALONE in which the single cell
e1 = (1,2,0) of the crossing unit (the cell (71, 2, −70) in the coordinates of `call9.json`) is made live at
generation 29. So:

- the line never feels the store wire: with its pair it is at every generation the free line, at rest from
  generation 42;
- the pair's whole effect on the store wire is the birth of that one cell at generation 29;
- the store wire is exactly plain wire carrying k units `b` two apart, the leading one at unit
  c + 3 − (t − 28)/2, at every even generation from **2k + 34** on and at none before;
- V_k equals push 8's hand release (the stator (0,1,2) of the crossing unit removed at generation 28) cell for cell
  from generation **2k + 32** and not before (k = 1..40, [st9] `extra9.py hand`). The push's "equal at 90 + 4k,
  at 90 only for k ≤ 29" is this statement at two sample times.

The finite cell: the left cap swallows the whole train; the state is the empty cell + the line from then on (e.g.
generation 106 for k = 3 with 32 units to the cap, 374 for k = 40) [oracle].

### 2.3 Beyond the push's runs: what is safe

All [st9], with the rows named replayed on the oracle (whole state equal at every even generation 0..300). An
outcome "destroyed" means the store wire burns down to about 12 cells or is converted to another wire for its whole
length; none of these states recovers.

| situation | result | oracle rows |
|---|---|---|
| **words of the line at an empty crossing** (23 words: one to five pulses, pairs 2 to 6 units apart, left-going 1 to 5) | all pass, everything restored | `9f`, `9ddf`, `9f9f`, `9fb9f`, left-going one and two |
| **words at an armed crossing** (k = 1, 2, 3, 5) | at every k only the adjacent pair, right-going (`9df`) or left-going, releases cleanly. One pulse, three, four or five adjacent pulses, a pulse beside a pair, two single pulses 2 to 5 units apart: the store wire is destroyed and in most cases the line is changed (typically 174 cells remain; 355 after one pulse at k = 3). Two exceptions, both at k = 1 (`9fb9f`, `9fb9df`), end with everything restored. Two pairs follow the next row | k = 3: `9f`, `9ddf`, `9f9f`, `9fb9f`, left-going one (destroyed), left-going pair (clean) |
| **two CALLs d generations apart** | not clean for 6 ≤ d ≤ 4k, clean from d = 4k + 2 (k = 2..14; k = 1 clean at every d). In the bad range the store wire is destroyed or converted; the line survives at most d | k = 3: d = 6, 8, 10, 12 destroyed, 14 and 20 clean; k = 12: d = 44 converted, 48 destroyed, 50 clean |
| **a CALL across an EMPTY wire while a store pulse is under way** (pulse born at c + a at the generation of the CALL) | harmless except R@c−14 (518 cells, line changed), R@c−13 (wire converted, line intact), L@c+15 (wire burnt, line intact), L@c+16 (wire burnt, line changed) | a = −15, −14, −13, +14, +15, +16 |
| **armed store, a right-going pulse under way** (R@c+a) | a ≤ −18 even: the pulse and the leading released pulse stop each other and the count k is re-stored further left; a ≤ −19 odd: they pass through each other, k pulses leave; **a = −17: k − 1 pulses leave** (section 2.4); a = −16: `d^k f` with its wall moved onto the crossing unit; **a = −15: store wire destroyed** (line intact); a ≥ −14: the pulse is absorbed first (`d^(k+1) f`, wall on the crossing unit) and the CALL does nothing | (k, a) = (3, −17), (3, −16), (3, −15), (1, −15), (1, −17), (3, −14), (3, −13), (3, −5) |
| **armed store, an add under way** (left-going pulse born 2..26 units right of the edge) | k + 1 pulses leave, clean, at every timing (k = 1, 2, 3, 5) | k = 2, a = 12..16; k = 3, L@c+8, +9, +14 |
| **a set under way** (R@c−a and L@c+a+3 with the CALL) | a ≤ 13: the mark forms first and is released (1 pulse); a ≥ 15: the CALL passes first and `d f` stands; **a = 14: destroyed** | a = 11..15 |
| **the stretch elsewhere** (first unit c + 1 + o) | stands at every o = −8..10; a CALL changes nothing unless o = 0 | o = −1, 0, +1, k = 3 |

Commands: `python3 beyond9.py words|twice|pulse|write|left|offsets --orc` (212, 144, 239, 189, 41, 83 s),
`python3 extra9.py twice` (95 s), `extra9.py near` (80 s).

Rules a user of the call line needs, none of them in the push: no store pulse within about 3 units of the
crossing when the pair reaches it (29 generations after a seed 15 line units before); no second CALL within
4k + 2 generations (the push's untested "closer than 44 generations" is unsafe for k ≥ 11); never one pulse on the
line of an armed store; counts are added from the right only (a pulse from the left disarms the store, row 10).

Two cells of the push's "one cell held live" list were checked [st9, `extra9.py held`]: (0,1,8) and (−2,1,10) of
the stretch's first unit held live release `d^k f` on a pulse (k = 1, 3, 5), and beside plain wire a right-going
pulse loses the wire. The other 970 are not checked.

### 2.4 One less, with a zero exit

A CALL (seeded as in `call9.json`) and R@c−17 at the same generation [oracle for k = 0, 1, 2, 3, 5 alone and for
k = 0..5 with a second store on the left; st9 for k = 0..10]:

| store at the line | leaves to the left | leaves to the right | end |
|---|---|---|---|
| empty (k = 0) | nothing | the pulse | empty wire, line at rest |
| k ≥ 1 | exactly k − 1 pulses | nothing | empty wire, line at rest |

With a store holding 2 at units 6..8: it ends holding 2 + (k − 1) for k = 1..5 and 2 for k = 0 (when the pulse
leaves to the right). `python3 extra9.py minus` (55 s), `extra9.py minus2` (90 s, oracle, nearest image 28).

This is one relative timing only: at R@c−19 and R@c−21 the pulse and the train pass through each other (k left,
one right), at even distances the count is re-stored. Both signals are made by hand at the same generation.

## 3 A proof of the call law for every k

**Theorem.** Let the store wire be an infinite wire B with the stretch `d^k f` on units c + 1 .. c + k + 1, the
call line (the finite object of `call9.json`) across unit c, and the two cells of the CALL made live at
generation 0. Then for every k ≥ 1, with V_k and Lf as in section 2.2:
(a) X_k(t) = V_k(t) ⊔ Lf(t) at every generation t;
(b) at every even t ≥ 2k + 34, V_k(t) is plain wire B carrying exactly k units `b`, at units
c + 3 − (t − 28)/2 + 2j, j = 0..k − 1.
So the whole state is from then on the free line (at rest from 42) and k pulses two units apart moving left.

Used without re-proof: T2 (`docs/AUTOMATON.md`: the wire's octahedral hull is never left) and the speed limit (a
change moves at most one unit of the wire per generation). The tape theorem (`research/signals/README.md`, section 10) is re-derived
from its base: part A below. Base facts, all [oracle], `python3 proof9.py [A B C D E F]` (A, B < 1 s; D + E 47 s; C 29 s;
F 48 s; ALL PASS). Notation: w = c + 1, τ = the move by one unit along the wire, lead(t) = c + 3 − (t − 28)/2.

**A (tape).** On a ring of 32 units holding all 32 runs of five letters over {7, b}, every word moves one unit
towards −v every 2 generations (40 moves). With the speed limit this gives: every word over {7, b} on wire B moves
one unit left per 2 generations, for ever.

**P1: V_k obeys (b) for every k.**

- *Direct* (part D), k = 1..13: (b) holds at every even t from 2k + 34 to 124 and at no earlier one; and
  W(k): on all units ≤ c + 5, V_k(t) is a word over {7, b} at every even t ≥ 44. By A both continue for ever.
- *Seam* (part E), K0 = 12: there is a path m(t), t = 31..124, with |m(t+1) − m(t)| ≤ 1, m(t) ≤ m(t−2) + 1,
  w + 3 ≤ m(31) ≤ w + K0 − 5, m(44) ≥ w + 3, lead + 2 ≤ m ≤ lead + 2K0 − 2 at even t ≥ 2K0 + 36, m(124) = lead + 3,
  such that V_12(t) and τV_12(t − 2) agree on the units m(t) − 1 .. m(t) + 1. (Found: m − w = 3 3 2 1 1 0 0 0 0 1 1
  2 2 3 2 1 0 −1 …; then it follows the train.) After 124 both sides are trains (A) and m(t) = lead(t) + 3 at
  even t, kept at the following odd t, continues the path for ever. Call this statement H(12); H(k) is the same
  with V_k and the same path.
- *Gluing.* Assume H(k), k ≥ 12. Let Y(t) = V_k(t) on units ≤ m(t) + 1 and τV_k(t − 2) on units ≥ m(t). The two
  agree on the overlap, a cell's neighbours lie within one unit, and the seam moves at most one unit per generation,
  so Y(t) steps to Y(t + 1). Y(31) = V_{k+1}(31): at generation 28 the standing stores `d^k f` and `d^{k+1} f`
  differ only on units ≥ w + k, so at 31 only on units ≥ w + k − 3 > m(31) + 1; and the event of generation 29
  has reached only units ≤ w + 1 < m(31), beyond which V_{k+1}(31) and τV_k(29) are both the standing store
  `d^{k+1} f` (its letters from unit w + 1 on are those of the shifted `d^k f`). Hence Y = V_{k+1} from 31 on.
- H(k + 1) follows with the same path: on units m − 1 .. m + 1, V_{k+1}(t) = V_k(t), and
  τV_{k+1}(t − 2) = τV_k(t − 2) because m(t) ≤ m(t − 2) + 1 (for t = 31, 32 by the light cone as above).
- (b) for k + 1: at even t ≥ 2(k+1) + 34 both pieces are trains, V_k(t) with units b at lead + 2j and τV_k(t − 2)
  at lead + 2 + 2j, j < k; the seam lies between lead + 2 and lead + 2K0 − 2, inside both; glued they are k + 1
  units b at lead + 2j. W(k + 1): at t = 44 every unit ≤ c + 5 is on the V_k side because m(44) ≥ w + 3; at even
  t ≥ 46 the other side is τV_k(t − 2) with t − 2 ≥ 44.
- A test of the gluing itself: V_12 glued along the path is the oracle's own V_13 at every generation 31..124.

**P2: (a) for every k.** A union of two disjoint sets steps to the union of their steps unless some cell has a
closed neighbour in both. Let Λ be the set of cells ever live in Lf (287 cells; Lf is at rest from generation 42:
part B) and let the tube be the wire's hull with e1 (1 ≤ x + y + z ≤ 5, −1 ≤ x − y + z ≤ 5), which V_k never leaves
(T2). No cell of Λ is in the tube, so the two parts are always disjoint. The cells with a closed neighbour in Λ and
one in the tube number 29, and their closed neighbourhoods meet the
tube only on the units c − 1 .. c + 3 (part B). So whether the union steps to the union at time t is decided by Lf(t)
and V_k(t) on those five units, and the one exception, the birth of e1 at generation 29, is decided there too.

- t < 44, k ≤ 18: X_k(t) = V_k(t) ⊔ Lf(t) at every generation 0..46 (part F, direct).
- t < 44, k > 18: at generation 28 V_k and V_18 are the standing stores and differ only on units ≥ w + 18, so up to
  generation 43 they differ only on units ≥ w + 3 = c + 4. On c − 1 .. c + 3 they are equal, so every step up to
  43 → 44 is decided as for k = 18.
- t ≥ 44: the line is at rest and, by W(k), V_k(t) is a word over {7, b} on all units ≤ c + 5 at every even t.
  **Lemma T** (part C): for each of the 512 words over {7, b} on the nine units c − 3 .. c + 5 the wire with the
  line at rest is, after one and after two generations, the union of the wire alone and the line alone. So every
  tape word passes under the line at rest and (a) continues for ever.

**Finite runs.** Each base run uses a finite capped wire; at every generation its four end units on each side are
those of the undisturbed standing object (checked in D, E, F), so the run glued to plain wire there is the run of the
infinite wire.

**What is proved.** (a) and (b) for every k ≥ 1, for the infinite store wire, the line and seed place of
`call9.json`, given the oracle runs A to F, T2 and the speed limit.

**What is left.** (i) A second reader of the argument and of `proof9.py`; nobody has tried to break it. (ii) The
finite cell: that the left cap takes a train of any length is measured (k ≤ 40), not proved; whether the third
push's reader theorem covers this cap was not checked. (iii) Other seed places and the shortened lines are direct
runs only. (iv) The exactness "at no earlier generation" is measured (k ≤ 40), not part of the theorem.

**Where the difficulty was.** The push looked for a gluing step for "the difference the CALL sends along the
stretch", comparing the CALL with the hand release. That comparison is not needed: the CALL acts on the wire as one
cell at one generation, V_k is an orbit of the wire alone, and push 8's seam argument applies to V_k directly. The
line enters only through lemma T, a finite check.

## 4 Write, read and call on one store

Reader: push 8b's capped wire B (169 cells, `push8b/objects/read-echo-B-small.json`; a probe of 4 cells; "echo"
beside wire B, nothing beside B′). `python3 coexist9.py reader|stand|seq|write|lineread` [st9] (1, 1, 13, 3, 5 s) and
`coexist9.py orc` [oracle, 91 s: three scenarios, st9 = oracle at every even generation].

- Line and reader do not stand together when the reader is within 2 units of the first unit of the stretch; the
  reader does not stand at the stretch's edge (8b's dead units, reproduced).
- **Reader left of the line** (4 or more units before the wall; at 3 units the read itself does not restore):
  reads echo (plain wire), whatever the count. A CALL sends the released pulses into it: the reader is destroyed,
  the line intact [oracle: `d^4 f`, reader 6 units before the wall: 406 cells at generation 120].
- **Reader inside the stretch** (3 or more units after the wall, before the edge): reads "nothing", i.e. it does
  tell the stretch. A CALL then destroys reader, line and wire [oracle: `d^5 f`, reader 3 units after the wall:
  1,213 cells at generation 90].
- **Reader right of the edge**: echo before, CALL clean, echo after.
- **Everything in place on an empty wire, signals only** (set, read, add, add, read, CALL, read): works with the
  reader 13 to 30 units right of the wall, and each read answers echo, for the counts 1, 3 and 0 alike [oracle,
  reader 14 units right: whole state exact after each step, the three reads on the oracle]. At every nearer place
  the set itself destroys the reader (8b's finding that the reader cannot be written under).
- The call line is not a reader: for 17 words of the line and the stretch at offsets −8..8, whenever store and line
  are restored the line differs from the free line in zero cells.

**Verdict.** A write, a read and a call in sequence survive only where the read carries no information. Not tried:
8b's other 22 reading placements, its reader b8, readers of wire C.

The emptiness of a store is nevertheless visible to a signal without any reader: a right-going pulse passes an empty
place and is absorbed by a store (push 8), and at the timing of section 2.4 a right-going pulse leaves to the right
exactly when the called store was empty.

## 5 The still life and the oscillator

### 5.1 The six-cell still life at the wall

`python3 trig9.py` [oracle, st9 = oracle at every generation, nearest image 26; 111 s; ALL PASS], states, places
and checks of this review:

- k = 1..8, the pulse born 12 and 13 units before the wall: the stretch stands beside the still life; what leaves is
  `b^(2k+2)`; 220 generations on: plain wire and the still life.
- Without the still life the pulse is absorbed (`d^(k+1) f`).
- A store 12 units to the left ends holding kl + k + 1 (k = 1..6, kl = 1, 2): the block is worth k + 1.
- The still life one unit further from the stretch: worth k + 3 (k = 1, 2, 3, 5). One unit nearer: the stretch
  falls by itself [st9].
- The hazard the push names: with no stretch, a right-going pulse at the bare still life loses the wire
  (`b^24 a 8 …`), left-going pulses pass.
- The push's start states `clear`, `one`, `sum`, `loop`, `call-far`, `smallest-loop` end as it says.

Single use, as the push says: after the release the still life stands beside plain wire, where the next
right-going pulse loses the wire.

### 5.2 P3.15f: a clocked call on the store's own wire

Own enumeration of the placements of the catalogue object beside wire B (`osc9.py`, [st9]): 2,656 placements, 1,576
stand beside plain wire, 1,408 pass a right-going and a left-going pulse at all three arrival timings each. Beside
`d^3 f` (wall offsets e = −5..5): 17,047 standing (placement, e), 55 with a release at some timing, 30 released at
every timing and every k = 1..8; **none of the 55 is a placement that passes all six plain-wire tests**.

The push's eight placements (gi 12, 14, 20, 22, 25, 27, 33, 35), three timings each:

- on plain wire a left-going pulse passes at all three timings; a right-going pulse passes at ONE timing in three,
  and at the other two the wire or the oscillator is changed;
- at the wall, at that same timing, `d^k f` leaves as **exactly k separate pulses** (k = 1..8), the oscillator as
  it would have been; the other two timings give `b 7 b^(2k+4)` and `b^(2k+5)` or do not settle;
- these are the only 8 (placement, e) of the scan with this property (8 more give the block `b^(2k+2)` at the
  passing timing);
- wire and oscillator are a junction, not two objects side by side: one cell of the free oscillator is absent at
  generations ≡ 2 mod 3.

**Object and verifier**: `objects/osc-call-P3.15f.json` (placement gi 14, translation (0, 2, 10), wall at unit 30
of a 64-unit cell) and `python3 verify_osc9.py` (numpy, json and `reference/oracle.py` only; 65 s; ALL PASS; torus
(168, 30, 168), nearest image 26). Timing rule: the stator (0,1,2) of unit u is removed at an even generation g with
(g + u) ≡ wall + 2 (mod 3), the oscillator being in its phase 0 at generation 0. Runs, every check a whole-state
equality:

- `pass`: the empty wire lets a right-going pulse through at the allowed timing and left-going pulses at all three;
- `cycle`: set through the oscillator, add, add, CALL by ONE pulse born 13 units before the wall: three pulses
  leave, wire plain, oscillator as it would have been; set, add, CALL from 16 units: two leave;
- `law-1` .. `law-10`: exactly k pulses, the train exact from generation 2k + 34 after a birth 13 units before the
  wall, leading pulse at unit wall + 2 − (t − 28)/2;
- `move`: 2 + 3 = 5 in a store on the left;
- `branch-empty`, `branch-full`: the same pulse sent from the left of a place where a second store may stand: if no
  store is there it goes on and releases the store at the oscillator (three pulses leave); if a store is there it
  is absorbed (2 becomes 3) and the store at the oscillator is untouched.

So the push's forecast 5 holds in its strict sense (one cell removed at least 10 units away, converter restored),
by this object and not by the still life. Limits: a right-going pulse at either of the other two timings is not
harmless; the law is measured (k ≤ 10 on the oracle), not proved; the other 36 oscillators of the push's list were
not re-run at three timings.

## 6 Numbers that came from steppers

- The push's steppers: `check9.py` passes as stated (lab8 against the oracle on the 9 runs of `trigger9.json`, 2,245
  generations; its ring mode; the bias stepper with a held cell; push 8b's stepper on the 6 runs of `call9.json`,
  2,394 generations; `wall9.py`'s inert shortcut on 3,843 cases). It does not cover the oscillators at the wall or
  the burnt outcomes of `cross9.py`.
- Laws to k = 40: the call law is now on the oracle at k = 1..12, 16, 20, 25, 30, 40 and proved for every k; the
  block law of the still life is on the oracle for k ≤ 8 and on the push's stepper to 40.
- "What destroys it", the idle offsets, the bus distances: re-run here, sections 2.1 and 2.3, with oracle rows.
- Still lifes of at most 8 cells: 6,028 placements, 3,780 standing; beside `d^3 f` at seven offsets 147 triggers
  (59 `b^11`, 59 `b^8`, 21 with nothing leaving, 8 `bb`); 59 placements where the stretch falls as `b^6`, and 59
  more where it does not stand and ends as plain wire and the object with no exact block seen. Equal to the push's
  numbers; the second 59 is not in its table. Its 16 "keeps" were not recounted.
- Negatives not rebuilt: section 0, row 20. The single-pulse negative at a crossing is confirmed for this line
  only, not for the 23 placements of the crossing scan.

## 7 The forecasts

The Brier arithmetic is right: squared errors sum to 3.84 (forecast 12 true) or 3.04 (false) over 13.

- Forecasts 5 and 6 are scored true through the call line, whose trigger is two cells made live by hand, while the
  file defines a signal as one pulse made by one cell removed. Forecast 5 is true in the strict sense by section
  5.2; forecast 6 needs the wider reading (a pair of pulses of a second wire). Scored false, 6 would give 0.242 /
  0.180.
- Forecast 5 "by the definition (the still life is unchanged)": by the letter only; that wire is single use.
- Forecast 7 is true as worded for the timing tried; the oscillator fails right-going pulses at two timings in
  three, and beside the wire it is not the free oscillator (a junction).

## 8 What it means

**The operations that now exist on a row of stores** (each a unary count k ≥ 0 at a fixed wall; an empty store is
plain wire):

| operation | by | status |
|---|---|---|
| set to 1 | two pulses that stop each other | oracle (push 8, here with the line in place) |
| add one | a left-going pulse from the right; from the left it also adds but moves the wall one unit | oracle |
| move-and-clear: the left neighbour gets + k, this store 0; into a cap: clear | CALL on a line (a hand-made pair), or one clocked pulse at P3.15f | oracle; proved for every k (line) |
| is it empty | a right-going pulse passes an empty place and is absorbed by a store (which then holds one more) | oracle (`branch-empty`, `branch-full`) |
| all but one, with a zero exit | CALL and a pulse at one relative timing (section 2.4) | oracle, k ≤ 5; measured k ≤ 10 |
| read a threshold | push 8b's reader | does not coexist with write or call (section 4) |

**What add, move and an emptiness test compute.** With increment, move-and-clear, clear and a zero test, and no
decrement, every counter always holds the sum of a set of inputs plus a constant, and no input is ever in two
counters (a move transfers, it does not copy). A zero test on such a counter answers a question about which inputs
are zero and nothing else, and after one test per input a finite control knows every later answer. So whatever the
program, each output is a sum of some of the inputs plus a constant, the sets disjoint, the choice of sets and
constants depending only on which inputs are zero. No copy, no doubling, no subtraction, no comparison of two
counts, no parity: far less than a finite automaton reading its input in unary, which can at least count modulo n.
A fixed reader (count ≥ j for a fixed j) adds finitely many threshold bits and changes nothing else.

**The missing operation that matters most is a decrement that reports zero**: take one off and tell empty from
non-empty. Increment and decrement-with-zero-test on two counters is a Minsky machine; nothing else on the list
(copy, doubling, a comparison) lets data steer control more than a bounded number of times. Section 2.4 shows the
automaton has this collision: at one timing a called store sends on k − 1 and a pulse escapes exactly when it was
empty. It is not yet an operation of a machine, for three reasons, in the order they would have to be met:

1. the count k − 1 leaves; it must be caught again at a callable place (a store one unit after a line), and every
   release goes left, so a counter can only walk leftwards from line to line. Nothing here moves a count to the
   right;
2. the timing is made by hand: a pair on the line and a pulse on the wire at the same generation. No signal of the
   machine makes the calling pair. The clocked P3.15f call is started by one right-going pulse of the store's own
   wire, which is the kind of pulse the zero exit is, so a zero exit could in principle start the next call; this
   was not composed, and whether the one-less collision exists at P3.15f was not tried;
3. the hazards of section 2.3 bound every schedule: no CALL within 4k + 2 generations of the last, none while a
   pulse is near the crossing, adds from the right only.

So the machine today is a hand-operated accumulator: stores that can be set, added to, emptied into their left
neighbour or into nothing, and asked whether they are empty. What it lacks for computation is, first, the decrement
in a form that leaves the count where it can be decremented again, and second, any operation started by a signal the
machine itself produced.

**Bearing on `docs/OWNER-JOURNAL.md`** (the entry of 2026-11-18, "a memory"):

- "two pulses on a wire laid across it do the same without a hand (measured to 40 … under review)": confirmed on the
  oracle and proved for every count on the infinite wire (section 3). The pair itself is still made by a hand.
- "a pair of pulses on another crossing wire reads whether one place is empty without changing it": that reader and
  the call do not live on one store in any place where the reading says something (section 4).
- "nothing found lets what is stored decide what is sent next": two cases on the oracle where it does, both with
  the deciding pulse made by a hand. A pulse sent along the wire releases the store at the oscillator if the place
  before it is empty and is swallowed if a store is there (`branch-empty`, `branch-full`, section 5.2). And at the
  timing of section 2.4 a pulse comes out on the right exactly when the called store was empty, while a non-empty
  store sends one fewer than it held.
- The isolation theme ("nothing yet listens"): the call is speech in one direction. The line acts on the store
  through one cell at one generation and nothing comes back: with its pair it is at every generation the free line,
  and for 17 words at 17 offsets it returns identical whether or not a stretch was there.

## 9 Corrections for the push's README (not applied; the push's files are untouched)

1. Section 2, "pass the crossing and go on unchanged": the line is at every generation the free line; say so, and
   that the store wire receives exactly one cell, (1,2,0) of the crossing unit, at generation 29.
2. Times: the train is exact from 2k + 34; the line is at rest from 42; equal to the hand release from 2k + 32 (not
   "90 + 4k").
3. "A CALL does nothing to an empty wire": add "unless a store pulse is within about 3 units of the crossing when
   the pair reaches it".
4. "Pulses pass under the line in both directions": add that a pulse from the left disarms an armed store.
5. Two CALLs: at least 4k + 2 generations apart.
6. "What destroys it": now on the oracle; two pairs closer than 4k + 2 generations destroy the store wire and in
   most cases leave the line intact.
7. "For every k [conjectured]": proved for the infinite wire (section 3 here).
8. P3.15f: one arrival timing in three on plain wire; at that timing exactly k pulses, k = 1..10; a junction with the
   wire; object and verifier in `research/audit/signals9/`.
9. Bus distances 3..12 work, 2 does not stand; lines down to 77 cells call.
10. The table of small still lifes: 59 further placements where the stretch does not stand and ends as plain wire
    without an exact block.
11. New: the one-less collision of section 2.4.

## 10 Not checked

- The proof by a second reader; the left cap for trains of every length; the oscillator's law beyond k = 10 and any
  proof of it; the still life's block law beyond k = 8 on the oracle and any proof of it.
- Section 2.3 and 2.4 beyond the k listed; the one-less collision with seeds other than line unit 6, with shortened
  lines, at P3.15f, and its composition into a repeatable decrement.
- Coexistence with 8b's other reading placements and reader b8; `coexist9.py seq`, `stand`, `write`, `lineread`
  are st9 with three scenarios on the oracle.
- Section 0, row 20: the scans of still lifes of 9 to 11 cells and of the other oscillators, `cross9.py`,
  `ghost9.py` beyond two cells, `ghostpairs9.py`, `rearm9.py`, the block-meeting table, the fuse, the other release
  lines, the push's 16 "keeps", `site9.py` (not run by the push either).
- Whether the six placements of P3.15f at which the push reports a fall are also junctions.
