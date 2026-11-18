# Eighth signals push: reading back what signals wrote

2026-11-18. The standing account of push 8. Question: can anything read the count that push 7's line keeps
(`../push7/README.md`, answer (c))? Tags as in `../README.md`: **[proved]** (an exact argument, or a construction the
oracle has stepped), **[measured]** (counts, with the command), **[conjectured]**. Commands run from this directory;
times are wall-clock on a shared 4-core machine. Forecasts: `PREDICTIONS.md`.

## Answers

**A read: yes, of one bit.** A later pulse crosses the line when the store is empty (plain wire B) and is absorbed
when a stretch of wire B′ is present; the stretch survives (one unit longer). On the oracle, on push 7's own lines.

**A destructive read: yes, of the whole count, and it comes out as a signal.** Removing ONE cell beside the stretch
dissolves it into exactly as many left-going pulses as it had units of wire B′, two units apart; the wire is left
plain. On the oracle for push 7's lines n = 1..4 (0, 2, 3, 4 pulses); proved for every length. The pulses are
ordinary pulses of wire B: a second stretch further down the wire absorbs them and grows by that number (the count
moves from one store to another).

**Not found:** a count read set off by a signal that arrives from elsewhere (the trigger is a one-cell change AT the
stretch); a read of the count that leaves it in place; a probe on a second wire; re-arming. Bounds in section 7.

| what | command (prints PASS lines and `ALL PASS`) | time |
|---|---|---|
| lab8's stepper equals the oracle on push 7's line, whole state, every generation 0..900, n = 0..4 | `python3 check8.py` | 43 s |
| the two reads on push 7's line (n = 1..5 written; count read and bit read for n = 1..4), oracle only | `python3 verify_read8.py` | 58 s |
| the memory cell and its protocol (five runs), oracle only | `python3 verify_cell8.py` | 8 s |
| the count read releases exactly k pulses for every k (base facts on the oracle) | `python3 prove_unzip8.py` | 6 s |

## 1. What push 7's standing line is, in letters

Units and letters as in `../README.md` section 9: unit u holds the cells with x in {2u, 2u+1}; every unit of the
family has the two stators (0,1,2), (0,1,4) and a subset of the sites 0 = (1,0,0), 1 = (1,0,2), 2 = (1,0,4),
3 = (0,2,3), written as a hex digit. 7 = wire B, d = wire B′, b = wire C, f = all four sites. All at even
generations (phase 0).

- **[proved by the oracle run, `check8.py` and `verify_read8.py` check A]** Push 7's line after E and n holes
  (N = 80, gun 4, end 70), from generation 880 on: capL on units 0..3 (18 cells, period 2), wire B on units 4..79,
  capR on units 80..84 (21 cells; period 4, only units 80 and 81 are not of period 2). For n ≥ 2 the wire reads
  `7^37 d^n f 7^(38−n)`: wire B′ on units 41..40+n and one unit `f` after it. For n = 1 it is `7^76`. Push 7's
  "edge unit" is the family unit f. (Read from the run: `python3 -c "import wire8 as W, exp8 as X; L,a=W.run_push7(3,880); print(X.hexrle(X.hexletters(L,a,4,80)))"`.)
- **The stretch `d^k f` is one symmetric object.** The half-turn that reverses wire B, (x,y,z) ↦ (−x−2, y, 8−z),
  maps `d^k f` onto itself: the clean wall 7|d on its left and the pair f|7 on its right are images of each other
  (the half-turn is not unit-aligned, hence the different letters). [measured: the image decoded, k = 2, 5]
- **It stands for every k ≥ 1.** k = 1..5 directly (`exp8.cell`, period 2); for k ≥ 5 every run of five units of
  `…777 d^k f 777…` occurs in k = 5, and two generations of a unit depend on five units. [proved]
- **k = 1, `df`, is the first push's mark**: the three cells left when two pulses of wire B stop each other
  (`../README.md`, "The mark") are site 3 on and site 1 off in one unit and site 3 on in the next. So a stretch can
  be started on plain wire B by two pulses, and "a later pulse … becomes a 5-cell standing defect" there is k = 2.
- capL and capR are saved in `objects/caps.json`. capL turned round by the half-turn is a right cap of period 2
  (20 cells); `exp8.cell` uses it in place of capR.

## 2. The signals of wire B, and what a stretch does to each

`signals8.py` is the sixth push's method (section 30 there) on a standing background: flip, run 60 generations, cut
the difference from the undisturbed run into clusters, test each for a rigid move of one unit per 2 generations.

- **[measured] One-cell changes of wire B** (`python3 signals8.py wire`, 1 s; every cell of the 5 × 5 tube of one
  unit, both phases, 76 events): 66 vanish, 6 start fronts, 2 leave a standing one-cell defect ((0,0,3) at phase 0,
  (0,2,3) at phase 1), 1 becomes the right-going pulse and 1 the left-going pulse. The first push's census of the
  3 × 3 tube agrees.
- **[measured] Two-cell changes** (`python3 signals8.py wire --pairs`, 6 s; every pair inside the 3 × 3 tube on two
  adjacent units, 574 events): 149 vanish, 309 fronts or unresolved, 46 a single pulse, the rest pairs of pulses and
  standing defects. No new mover.
- **[measured] Words** (`python3 words8.py --K 3`, 33 s; every word of up to 3 family units in wire B, 3,840
  events): 34 vanish, 3,238 are fronts or unresolved; every rigid outcome is made of four movers and their trains:

  | mover | letters (phase 0) | direction | cells |
  |---|---|---|---|
  | R, pulse B of the first push | `6f` | +v | 2 |
  | L, the left-going pulse | `b` (one unit of wire C) | −v | 2 |
  | R⁺ | `d6f`; with a tail, `(cf)^i d 6 e^j f` (seen: i ≤ 2, j ≤ 2) | +v | 4 + |
  | L⁺ | `b5f`; with a tail, `b^i (5f)^j (9f)^l` (seen: `b5f9f`, `bb5f`, `b5f5f9f`, `bb5f9f`) | −v | 4 + |

  The half-turn exchanges R with L and R⁺ with L⁺. R⁺ carries a unit of wire B′ along behind a pulse. L⁺ is a pulse
  followed by a mirror rake `5f` of wire C, and `9f` is wire C's own right-going pulse: these are pieces of wire C's
  machinery riding in wire B behind a B|C wall. (Each rides a ring of 40 units: `exp8.ring_test`.)
- Wire B′ is wire B under two lattice symmetries, each with a shift of one generation: (x,y,z) ↦ (z−4, y, x+4) and
  (x,y,z) ↦ (−z−4, y, 10−x) (found by search over the 48). So its signals are the images of these. As a check,
  the one-cell census inside a stretch of 60 units (`python3 signals8.py wire --bg d --T 40`, 1 s) gives the same
  counts: 66 vanish, 6 fronts, 2 standing one-cell defects, one pulse each way. Words in wire B′ were not run.
- **[measured] A stretch absorbs everything that arrives.** `python3 unzip8.py absorb` (2 s): each mover above, and
  pairs of them, sent at `ddf` from its own side at two distances: every one is absorbed and the stretch is longer
  on the side that was hit: by 1 for `6f`, `6ef`, `b`, `bb`; by 2 for `d6f`, `d6ef`, `b5f`, `bb5f`, and for two
  separate pulses; by 3 for `cfd6f`, `b5f9f`; by 4 for `b5f5f9f` and two `d6f` or two `b5f`. Nothing comes back and
  nothing comes out on the far side. A stretch is a sponge with a count: the register of the second push, on both
  sides.
- **[measured] Nothing put next to it gets through either.** `python3 words8.py --K 3 --mid dddf --at left` and
  `--at right` (35 s each): every word of up to 3 family units on the three units before the stretch (after its
  edge): 576 (922) events end in something rigid or standing, and in none of them is there any difference beyond
  the stretch. The other 3,264 (2,918) are fronts and were not followed.

## 3. The two caps of push 7's line

- **[measured] capL swallows every left-going pulse** (both parities of place and of time; the whole object
  restored). **capR swallows a right-going pulse at one of its two arrival phases and is destroyed at the other**:
  the line burns down to 12 cells. Of 18 right-moving words tried at two distances each, only a single `6f`, `d6f`,
  and pairs with an even gap (`6f6f`, `6f776f`, `6f7d6f`) at the right distance leave the line alive.
  (`python3 unzip8.py caps`, 3 s.) On the oracle: `verify_read8.py`, check B for n = 1 (swallowed when the cell is
  removed at a generation ≡ 2 mod 4, here 882) and check C for n = 1 (capL).
- **[measured] capL erases a stretch that touches it.** With the stretch's first unit next to capL the stretch is
  turned, from the left, into units of wire C that capL swallows; 4k + 4 generations later the object is the plain
  line (k = 1..6). A stretch one unit away from capL stands. At capR the same contact destroys the line.
  (`python3 unzip8.py caps`.)
- With capL turned round as the right cap (`exp8.cell`) the object has period 2 and both caps swallow pulses at
  every phase. The cell of section 6 uses that. capL also swallows the whole train of a count read, k = 1..12,
  leaving exactly the empty cell (`unzip8.py caps`).
- **Re-arming: not found.** No right-moving word tried turns capR back into a gun (it swallows or dies), and the
  dead gun is the only source of rakes the line had. What a stretch can be turned into is section 5: at most one
  mirror rake with its own pulses, `b5f(9f)^k`, which leaves.

## 4. The bit read: a pulse crosses an empty store and is absorbed by a full one

- **[proved by the oracle run] On push 7's lines** (`verify_read8.py`, check C). At generation 882 remove ONE cell,
  the stator (0,1,4) of unit 70 (a left-going pulse is born there).
  - n = 1 (plain wire B): 60 generations later the pulse is 30 units on, past the place where a stretch would be;
    at generation 1082 the whole state is the untouched n = 1 line (capL swallowed it).
  - n = 2, 3, 4: the pulse is absorbed, and at generation 1082 the whole state is, cell for cell, **the object that
    n + 1 holes write**. A pulse does to the store what one more hole would have done.
- So the outcome of a later signal depends on what the earlier signals wrote, and the store survives; what is read
  is one bit (stretch or no stretch), and the count is changed by the reading. A right-going pulse from the other
  end reads the same bit, but on push 7's line it then meets capR (section 3); on the cell of section 6 both
  directions are safe.

## 5. The count read: one cell beside the stretch, and the count leaves as a train of pulses

- **[proved by the oracle run] On push 7's lines** (`verify_read8.py`, check B). At generation 882 remove ONE cell:
  the stator (0,1,2) of unit 40, the unit of wire B next to the stretch's first unit (the same cell for every n).
  - n = 2, 3, 4: at generation 922 the whole state is the n = 1 line with exactly n units of wire C in it, at units
    23, 25, …: **n left-going pulses two units apart**. At generation 1103 the whole state is the n = 1 line: the
    stretch is gone, capL has swallowed the pulses.
  - n = 1: the same cell makes one right-going pulse (at units 59, 60 at generation 922); capR swallows it and the
    line is as it was.
  So the count 0, 2, 3, 4 written by holes comes back out as 0, 2, 3, 4 pulses, and the line is reset to the plain
  standing line. The store is lost: a destructive read.
- **[proved; base facts on the oracle: `python3 prove_unzip8.py`, 6 s] Exactly k pulses for every k ≥ 1.** On the
  infinite wire, with the stretch's first unit at w, removing the stator (0,1,2) of unit w − 1 at phase 0 leaves
  plain wire B with k left-going pulses two units apart, the leading one at unit w + 2 − t/2. k ≤ 10 directly; for
  k > 10 by the gluing argument of `../README.md` section 21 (the argument is in the script's docstring: the orbit
  for k + 1 is the orbit for k on the left of a moving seam and the same orbit one unit on and two generations
  late on the right; the script finds the seam path for k = 10 on the oracle and, as a test, checks the glued orbit
  against the oracle's own run of k = 11). A second reader should check the argument.
- **[measured] Which changes release a stretch** (`python3 unzip8.py census`, 16 s; `d^3 f`; every cell of the
  5 × 5 tube on the ten units from 3 before the stretch to 3 after its edge, both phases: 760 one-cell events):

  | outcome 100 generations later | events |
  |---|---|
  | healed | 526 |
  | **the stretch released as a rigid train, the wire plain behind it** | **134** (67 to the left, 67 to the right) |
  | fronts and fire | 72 |
  | a standing defect at or near the stretch | 10 |
  | count + 1 (a pulse made and absorbed) | 8 |
  | count − 1 (a stator removed inside the stretch: a pulse of wire B′ is born and a wall moves inwards) | 6 |
  | a pulse leaves, the stretch as it was | 4 |

  The trains, to the left (to the right: their mirror images, `6f6f6f`, `6e^6f`, `cfcfd6f`, …): k separate pulses
  `b7b7b` (13 events), a block of adjacent units of wire C `b^6`, `b^7`, `b^8` (23), a pulse with one mirror rake
  and k or more of wire C's pulses `b5f9f9f…` (22), and shorter trains when the cell is inside the stretch (9).
- **[measured] The products are exact functions of k** (`python3 unzip8.py law`, 20 s; k = 1..40 each):

  | one cell, at phase 0 unless said | what leaves to the left |
  |---|---|
  | stator (0,1,2) of the unit before the stretch removed | `(b7)^k`: k pulses |
  | site (1,0,2) of that unit removed | `(b7)^k` |
  | stator (0,1,4) of that unit removed at phase 1 | `(b7)^k` |
  | **(1,4,2) of that unit made live (a cell outside the wire's 3 × 3 tube)** | `(b7)^k` |
  | (0,2,3) of the stretch's first unit removed | `(b7)^(k−1)` |
  | (0,2,3) of the unit before the stretch made live | `b5f(9f)^k` |
  | stator (0,1,4) of the unit before the stretch removed | `b5f(9f)^(k+1)` |
  | site (1,0,4) of the unit before the stretch removed | `b^(2k+2)` |

  Why a stator removed two units away adds one and the same stator next to the stretch releases it: both make a
  right-going pulse; born next to the wall it is not yet a pulse when the wall is in reach. In letters, the unit
  before the wall turned into `5` (row 2) or `3` (row 8) unzips the stretch, and so does a unit `b` or `9` put
  there; every mover of section 2 that travels towards the wall arrives with `f` at its front and is absorbed.
- **[measured] The count moves to another store** (`python3 unzip8.py catch`, 2 s; k = 1..12; on the oracle for
  k = 3, `verify_cell8.py` run `transfer`): with a second stretch `df` 20 units to the left, the count read of a
  store holding k leaves the left stretch holding k + 1 and the right one gone, exactly.

## 6. The memory cell

`objects/cell8.json`, `cell8.py` (how it is built), `python3 verify_cell8.py` (oracle only; cubic torus).

**The cell**: capL + N units of wire B + capL turned round: 38 + 5N cells, period 2, in empty space. Its state is
the count k ≥ 0 and the place of the stretch. Every operation removes ONE live cell at an even generation: `R@u` =
the stator (0,1,2) of unit u (a right-going pulse is born), `L@u` = the stator (0,1,4) of unit u (a left-going one).

| operation | how | effect |
|---|---|---|
| set | `R@u` and `L@u′` in the same generation, u′ − u odd | the two pulses stop each other between u and u′ and leave `df`: count 1. (u′ − u even: they pass, both caps swallow, nothing is written.) |
| add one | `R@u` two or more units before the stretch, or `L@u` two or more units after its edge | count + 1, on the side the pulse came from |
| bit read | the same pulse | empty cell: the pulse crosses and the far cap swallows it, the cell is as it was. Otherwise: absorbed |
| count read | `R@u` with u the unit next to the stretch's first unit | k left-going pulses leave, two units apart; the left cap swallows them (or a second stretch counts them); the cell is empty |
| take one off | the stator (0,1,2) of a unit inside the stretch | count − 1 (the left wall moves in; (0,1,4): the edge moves in) [measured, `unzip8.py census`; not in the oracle runs] |

- **[proved by the oracle runs] `python3 verify_cell8.py`** (8 s). Each run is checked on the whole torus against
  states built from letters, not against another run.
  - `smallest`: **N = 7, 73 cells**: set (`R@5`, `L@10`: `777df77`), add one (`L@10`: `777ddf7`), count read
    (`R@6`: ten generations later `b7b7777`, two pulses), empty again at generation 360. N = 7 is the shortest wire
    on which set, add one and a count read with two separate pulses on the wire at once all work
    (`python3 cell8.py --search`, 2 s: every place for each operation, N = 4, 5, 6: none; N = 7: four; [measured]).
  - `count` (N = 24): set, three pulses add one each (from the right, the left, the right), count read: `b7b7b7b`,
    then the empty cell.
  - `transfer` (N = 24): two stores holding 1 and 3; the count read of the right one; the left one holds 4.
  - `bit-empty`, `bit-set` (N = 24): the bit read, both answers.
- What the cell is not: its count read is started by a cell removed next to the stretch, so the reader has to know
  where the stretch begins. On push 7's line that place is the same for every n (unit 40). The cell holds one
  stretch per empty run of wire; several stretches on one wire are several stores, and pulses do not pass a store.

## 7. Looked for and not found, with bounds

- **[measured] A count read set off by an arriving pulse: none among 48 standing structures.**
  `python3 latch8.py --k 3 --pairs --words 3` (2 min 40 s): every one-cell change on the five units before `d^3 f`
  and its first unit (456), every two-cell change on the three units before it and its first unit (2,943), every
  word of up to 3 family units ending at the unit before it (3,840): 7,239 candidates, of which 48 distinct
  structures stand (period dividing 4, the caps untouched, within 12 units of the wall). Each was sent a right-going
  pulse at two distances. Outcomes: absorbed as usual; absorbed with nothing changed (two structures, `6?` and `6??`
  in front of the wall, are eaters: the stretch behind them no longer counts from that side); the wire to the left
  turned into wire C; fire. **None releases the stretch.** The same with `d^2 f` and every word of up to 4 family
  units (`python3 latch8.py --k 2 --words 4`, about 20 minutes of one core): 65,991 candidates, 148 standing
  structures, none releases the stretch (24 absorb as usual; in 75 the pulse turns the wire on its left into wire C
  or the stretch grows behind an untouched structure; 84 end in a standing state that is not made of family units;
  113 in fronts or fire, not looked at one by one).
- **[measured] A probe on a second wire: none among parallel placements of a second wire B.** `python3 probe8.py
  scan --out S.json` (37 s): wire B under each of the 8 symmetries that keep the axis, at both phases, moved by every
  even vector (0, b, c) with |b|, |c| ≤ 14: 3,600 placements beside uniform wire B and beside uniform wire B′ (ring
  of 8 units, 40 generations). 2,808 touch neither; 404 are coupled to both and stand with both; 36 stand with both
  and are coupled to one only; 22 stand beside wire B and break beside wire B′, 18 the reverse; the rest overlap or
  break with both. The 440 that stand with both were given a pulse on the second wire (`probe8.py ride S.json`,
  24 s; ring of 24 units, one lap): in 320 it rides beside both wires, in 112 beside neither, and in 8 it rides
  beside wire B′ and not beside wire B. Those 8 (`probe8.py ride S.json --out R.json`; `python3 probe_kymo.py 1 1 6
  -4 L --k 0`): beside plain wire B the pulse sets the second wire on fire; in 4 of them the first wire is left
  exactly as it was, in 4 it burns too. But none of the 8 stands beside a stretch even without a pulse: the
  stretch's two ends break the pair (`probe_kymo.py … --k 3`, last line). The 320 were then run with a stretch `d^3 f` on the first wire (`probe8.py ride S.json --both --out G.json;
  probe8.py ringstretch G.json`, 53 s; ring of 48 units, one lap): in 8 the pair does not stand with a stretch; in
  the other 312, for both pulses, **the whole state after one lap is exactly as it was**: the pulse passes the
  stretch and its two ends and nothing is changed on either wire. So no parallel second wire B reads, and none
  disturbs. The 40 placements that stand beside one of the two wires and break beside the other are detectors of a
  crude kind (the second wire burns when the first is written); not followed. Not tried: wire C as the second wire,
  wires crossing at an angle, pulses of the FIRST wire beside a second wire, oscillators. One fact for a later
  search: a single cell made live OUTSIDE the wire's tube, (1,4,2) of the unit before the stretch at phase 0,
  releases the count as k pulses (section 5), so a probe need only deliver that one cell.
- **[measured] Re-arming: not found** (section 3).
- **A read of the count that leaves it in place: not found.** Everything that reaches a stretch from outside is
  absorbed (section 2), and everything that releases it removes it (section 5). The count is also in the place of
  the edge (unit 41 + n on push 7's line), and left-going pulses made between the edge and the right cap move the
  edge one unit each, so the number of pulses the gap can take is a second, slower destructive read; not built.

## 8. Tools, and how each was checked

| file | what | checked by |
|---|---|---|
| `lab8.c`, `lab8.py` | stepper on a box in sheared coordinates (x, y, x + z), dead outside or a ring; a pure-Python set stepper | `python3 check8.py` (43 s, ALL PASS): against `oracle.step` on push 7's line with E and n = 0..4 holes, whole state, every generation 0..900 (box torus 200 × 16 × 200); ring mode against the oracle on a cubic torus H = 64 (wire B with a pulse, 200 generations); dead mode against the set stepper on soup |
| `wire8.py`, `exp8.py` | the family's letters, push 7's line, the caps, `line` (push 7's caps) and `cell` (capL at both ends) | used by everything; the objects they build are the ones the oracle verifiers step |
| `signals8.py`, `words8.py`, `unzip8.py`, `latch8.py`, `probe8.py`, `probe_kymo.py` | the censuses of sections 2, 3, 5, 7 (`probe8.py finite` and `probe_look.py` use capped finite wires whose caps disturb many placements: superseded by `ringstretch`) | lab8 only; what they found that matters is in the three oracle scripts |
| `make8.py`, `cell8.py` | write `objects/line7-read.json`, `objects/cell8.json`; `cell8.py` asserts every check in lab8 before writing | — |
| `verify_read8.py`, `verify_cell8.py`, `prove_unzip8.py` | the judge: `oracle.step` and numpy only, reading only the JSON objects | — |

## 9. Not checked

- **Oracle and lab.** On the oracle: the two reads on push 7's line (n = 1..4; the written lines n = 1..5), the cell's
  five runs, and the base facts of the proof. Everything else (the censuses of sections 2, 3, 5, 7, the laws for
  k ≤ 40, the catch for k ≤ 12, the search for the smallest cell) is lab8 only; lab8 equals the oracle on push 7's
  line and on a ring (`check8.py`).
- **The proof** of "k pulses for every k" is an argument in `prove_unzip8.py`'s docstring with its base facts
  checked for K0 = 10 (and 12); it uses the tape theorem of `../README.md` section 10 for the time after the last
  check. No second reader has gone through it. The other seven release laws of section 5 are measured to k = 40.
- **Push 7's own verifier was not run.** Its line records were stepped here from their initial cells by the oracle
  (`check8.py`, `verify_read8.py` check A: standing with period dividing 4 at generation 882, the five objects
  different). Only the line of gun 4 and end 70 at N = 80 was used; with the other pairs the wire is the same but
  whether those left caps swallow the released pulses was not checked.
- **"Nothing crosses a stretch"** is for the movers of section 2 and for the rigid or standing outcomes of the word
  census. Fronts (3,264 and 2,918 events) were not followed; fire can cross anything.
- **The right-going release** (67 of the 760 events) and "take one off" were seen at k = 3 in the census only. The
  bit read with a right-going pulse on push 7's line is not in an oracle run (the count read at n = 1 is: it is the
  same pulse into capR at its safe phase).
- **Section 7's negatives** are for the structures and placements listed: one side of the stretch (the other is its
  mirror image), one arriving pulse at two distances, structures within 12 units, second wire B parallel only.
  Outcomes that end in fronts were counted, not examined.
- The census classes `other` of `signals8.py` and `words8.py` lump fronts with anything that is neither standing nor
  moving at one unit per 2 generations at generation 60; a slow mover would be in there.

## 10. Forecasts scored

Sixteen forecasts (`PREDICTIONS.md`, written before the first run). Outcomes: true 1, 2, 3, 9, 10, 12, 15, 16; false
4, 5, 6, 7, 8, 11, 13, 14. Mean squared error (Brier) 0.101; always saying 0.5 would give 0.25.

- Right and confident: the push-7 line reproduces (1), the stepper (2), a clean boundary swallows and moves (3).
- Right but under-confident: a destructive read of the count (12, given 0.40) and a cell with an oracle verifier
  (15, given 0.50).
- Wrong: "the edge unit does something else" (4, given 0.45): the stretch is symmetric and its edge is the image of
  its wall. "Both caps survive a pulse" (7, given 0.45): capL does; capR dies at one of its two arrival phases.
- Low and false, as forecast: something crosses a stretch (5), something is reflected (6), a cap returns a signal
  (8), a count read that keeps the count (11), an outside probe (13), re-arming (14).
- Not foreseen at all: that a stretch can be released whole by one cell and comes out as its own count in pulses.
  The forecasts imagined reads as scattering of an arriving signal, and in that sense only the one-bit read exists
  here.

## 11. Where I would go next

1. **A trigger that travels.** The count read needs one cell at the wall; nothing that rides wire B towards the wall
   delivers it, and 196 standing structures in front of the wall do not convert a pulse into it. Three routes:
   (a) as one constraint problem (the form of `sat_listen.py`, now with a known answer to ask for): a standing
   structure before the wall, an arriving pulse, and k pulses leaving with the wire plain; (b) a wire crossing at an
   angle that delivers the outside cell (1,4,2): nothing but parallel placements was scanned; (c) a catalogue
   oscillator beside the wall, as in the divider: a stroke at that cell would be a clocked read.
2. **A count read that keeps the count.** The transfer moves k to a second store as k + 1 and empties the first.
   A release that leaves `df` behind would make it a copy up to one unit; none among one-cell changes (the trains
   seen are k, k − 1, k − 2 pulses with the stretch gone); two-cell changes at the wall were not classified by k.
3. **What a wire of stores computes.** Each store takes +1 from either side, −1 from inside, passes nothing, and
   releases its count to the left or to the right as pulses that the next store adds. An empty stretch of wire
   between two pulses makes a new store when they meet at odd distance. That is a row of counters with addition
   between neighbours and a coincidence detector; whether it is more than that is open.
4. **Re-arming.** The release `b5f(9f)^k` is one mirror rake with k pulses of wire C behind a B|C wall: wire B can be
   turned back into a piece of the rake's medium, one rake at a time. A release that leaves a train of rakes, or
   an end that fires when a rake arrives through wire B, was not looked for.
5. The 40 placements of a second wire that stands beside wire B and breaks beside wire B′ (or the reverse).
