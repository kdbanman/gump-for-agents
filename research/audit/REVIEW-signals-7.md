# Review: signals, seventh push (`research/signals/push7/README.md`: ends of the rake train at C ≤ 39, the wire-B caps, the line that keeps a count)

Adversarial review, 2026-11-18. Code in `research/audit/signals7/`; every command is run from there. Bulk output:
`research/scratch/audit/signals7/` (ignored by git). Times are wall times on this machine with the other agents'
jobs running (two to three times the unloaded time).

**Steppers.** The judge is `reference/oracle.py`'s `step`, unchanged, called on rectangular arrays (`orc7.py`), in
two forms. *Box*: an array that holds the whole object with a margin and uses no identification at all (nothing wraps;
the four outermost index planes on every side are asserted dead at every generation). *Helix*: the array
(16a, 16, 16b), gcd(a, b) = 1, on which the tube along v = (1,0,−1) closes into a ring of 8ab units; every lattice
shift of the array changes x+y+z and x−y+z by multiples of 16 and the 5 × 5 tube holds the layers −1..7 of both, so
the layers 9, 11, 13 between two windings are dead and stay dead (T3). It is 40 to 100 times cheaper than the square
ring torus of `verify7.py` (229,000 sites against 12.8 million for 448 units), which is what lets the census be put to
the oracle. `python3 check_helix.py` (94 s): helix = box, cell for cell at every generation, for the two trains, the
push's line alone and with E and 0..3 holes (400 generations, two ring lengths), and six events outside the 3 × 3
tube: ALL PASS. `fast7.c` is a ring stepper of my own (the same object as the helix) used only where the oracle
would take hours; `python3 fastcheck.py` (19 s): equal to the oracle at every generation on 12 soups, 5 line runs and
18 census runs: ALL PASS; and every oracle census row below is compared with its fast7 row.
Taken from the push as initial data only: the two train bases and the line (`objects7.json`), the cap cells of
`wireB_caps.json`, the cells of the signal kinds (`signals7.json`, `signals7_5f.json`; each checked to ride, §6).
Nothing of `research/signals/` is imported. The lists of ends were enumerated again (§3), not taken.

## Verdicts

| # | claim | verdict | in one line |
|---|---|---|---|
| 1 | (c) a finite line that keeps a count | **confirmed as an object; "keeps a count" corrected** | oracle, box: period 4 from generation 100 (106 for one hole) for ever; n = 1..6 differ by exactly the cells claimed. What it stores is not the number of holes: see 2 |
| 2 | what is stored | **corrected** | nothing unless the second hole is 3 or more rakes behind the first (2,047 + 599 + 43 words: no exception); then the number of holes, exactly, up to 193 in a 400-unit line, at a place set by the second hole |
| 3 | robustness: other guns and ends, other spacings | **confirmed for spacings 3, 4, 5; refuted for spacings 1, 2** | all 625 pairs of the 5 guns and 125 ends keep the count at 3, 4, 5; "spacings 1 and 2 leave plain wire B" fails for the 12 ends that do not heal holes: they write the count next to the end cap |
| 4 | "the count cannot be read or reset; written once" | **corrected** | not by holes, but the object is the B/B′ counter of the second push: one-cell flips of the standing object add a unit at either end, take one off, or erase it; 44 of 608 flips of the plain object burn all of it |
| 5 | the lists: 90 / 753 / 6,286 ends, 68 / 873 guns; 5 × 5 none at C ≤ 25 | **confirmed, independently** | own CNF and CaDiCaL: the same caps as sets at C ≤ 37, the same counts at C = 39; 89 / 741 / 6,196 and 67 / 867 with an own key |
| 6 | `cdcl7.cpp` | **confirmed on tests** | 400 small CNFs against brute force, 62 larger ones against glucose4 (stops, resumes, splits included), the C = 33 instance: no difference |
| 7 | the census tables (17 events per end) | **confirmed in full; oracle on a sample** | see §4 |
| 8 | (a), (b): no listener, no answer | **confirmed within the bounds, with the criterion tightened** | every row is healed on the whole state or has no rake left in front of the end; "dead" as the push defines it would also hold a changed end that had sent one signal, so that was checked directly |
| 9 | guns: 5 of 67 cap, all absorb U; at C ≤ 39 none survives E, N1, EE | see §5 | |
| 10 | "E alone destroys the line: E kills every gun on file" | **confirmed, with an exception worth having** | E alone, N1, EE, E with K0 or K3 in front: debris. **E with N2 in front: the two leave one hole**, the end heals it and the line runs on unchanged |
| 11 | the count on the infinite train (`record7.py`) | **confirmed** | oracle: n = 1..6, period 2, standing, 0, 2+1, 3+1, .. units |
| 12 | the README's own state | **corrected** | "Runs", "Not checked" and "Forecasts scored" are empty placeholders; the 5 × 5 row "pending" has a result in `objects7.json` that the text does not report; forecasts scored in §7 |

## 1. The line (answer (c)), on the oracle where nothing wraps

`python3 line7a.py box` (5 min; the array 318 × 26 × 328, units −30..119, margin asserted dead at every one of the
1,200 generations of each run). The 419 cells are the record `line-N80-gun4-end70-alone`; E and H are read from the
flips of record `n1`; holes are H moved by 6 units each.

| run | whole array periodic from generation | least period | cells | units 0..81 |
|---|---|---|---|---|
| the line alone | 0 | 4 | 419 | end, train, gun |
| E alone | 278 | 2 | 12 | debris: destroyed, as claimed |
| E and 1 hole | 106 | 4 | 419 | end cap (units 0..3), wire B on 4..79, gun cap (80..) |
| E and n = 2..6 holes | 100 | 4 | 420 | the same with B′ on units 41..40+n and the edge unit at 41+n |

"Periodic from g" is state(g + 4) = state(g) on the whole array, so the object stands for ever: no longer run can add
to that. (A run of 40,000 generations on the helix was made all the same: `python3 line7a.py long`, see §9.) The push
checked period dividing 8 on generations 880..896; the object is periodic 780 generations earlier, with period 4.

Cell for cell (`line7a_box.npz`, generation 1,200): the object of n = 2 is the object of n = 1 with (0,2,3) on and
(1,0,2) off in units 41 and 42 and (0,2,3) on in unit 43; from n to n + 1, n ≥ 2: (1,0,2) of unit 41 + n off and
(0,2,3) of unit 42 + n on. So a wire-B unit is the family unit 7, B′ is d, the edge unit is f (section 9's code), as
the push says; the stretch starts at unit 41 and grows towards the gun. The caps are the end and the gun in a cycle of
their own: equal to the running line's at two of the four generations of a period, different in one unit each at the
other two. My own construction of the line from the cap cells (mirror, alignment searched with oracle steps,
`lines.py`) gives the same 419 cells.

## 2. What the line stores

All runs here are on the oracle (helix ring; `line7b.py`, `line7c.py`, `line7d.py`; each run ends when the whole
array has period 4 and is read at the next generation = 0 mod 4 against the plain object). E at unit e, holes at
rakes h1 < h2 < .. above it (a rake every 2 units).

**The rule, for the push's line (gun 4, end 70).**
- one hole: plain wire B between the caps, whatever h1;
- h2 − h1 = 1 or 2 rakes: **plain wire B, whatever follows.** A word of 195 holes that begins 10, 12 leaves the same
  object as one hole;
- h2 − h1 ≥ 3 rakes: a B′ stretch of exactly n units (n = the number of holes, whatever the later spacings, 1 and 2
  included) and one edge unit, starting at unit (h2 + e − 4)/2.

Tested without exception on: every word of 1, 2 or 3 holes on the 23 rakes between E and the gun (`line7b.py
triples`, 2,047 words, 40 distinct objects, 4 min); 599 random words of 4 to 12 holes (`random 600`, 78 objects);
E at every even unit 6..62 (`epos`); E and holes within 2 units of the gun or of the end (`near`); N = 82, 84, 86,
122 (`line7d.py`); and a 400-unit line (`long 400`, `long 400 4`, `line7c.py dense 400`, `late 400`): n = 1..63 at
spacing 3, n = 1..47 at spacing 4, and 43 dense words of up to 195 holes. **The count is exact up to the most the
geometry allows** (193 holes: a hole on every rake after the second; the stretch then has 193 units). It cannot
saturate: a hole needs 2 units of train and adds 1 unit of stretch, so the stretch ends at or below unit
(N + e − 2)/2 and never reaches the gun. No word with at least one hole above E destroyed the line.

So the object holds (i) one bit, whether the first gap was 3 rakes or more, and if so (ii) the number of holes and
(iii) the place of the second hole: two numbers, not one. For a fixed n there are as many objects as places. It is
not a parity and not a window. It is not "the number of holes" either: the first gap decides whether anything is
kept.

**Where the place comes from.** A hole made at the gun's mouth at generation g (instead of being on the stream at
generation 1) as the second hole puts the stretch at unit 201 + (g − 1)/4 on the 400-unit line (`line7c.py late`):
the place is the time of the second hole, one unit per rake period.

**Holes that arrive after the wire B has formed.** They are still counted. On the 400-unit line with E at 8 and holes
at 24, 30, a third hole at any rake up to 398 adds its unit to the stretch at unit 17 (62 words, `late`): the hole at
398 meets the upper edge near unit 207 at generation ≈ 390, and the unit is added some 380 generations later, 190
units away, long after the lower cap has formed (generation ≈ 45). The carrier is a pulse of wire B running down from
the upper edge (the walls of section 9 move one unit towards a pulse). TODO-late2

**Holes below E** (between E and the end, so that they never meet it) change nothing: 65 words, the end heals the
hole before the lower edge arrives (`line7c.py below`).

**The other ends.** `python3 line7c.py robust 3 --gun g` (85 s per gun; all 5 guns × all 125 ends of
`wireB_caps.json`, each line built by `lines.build`, alone of period 4, then E at 32 and n = 1..4 holes from 48):
**625 of 625 pairs** give plain, then n units at unit 41. The push sampled 45. Spacings 4 and 5: 625 of 625 each,
at units 42 and 43 (`robust 1 2 4 5 --gun g`, 5 min per gun; `python3 robust_report.py` prints the tally: 2,500 runs
per spacing). **Spacings 1 and 2 are not "the same plain wire B for every n":** that holds for the 113 ends that heal
holes (2,260 of 2,260 runs at each spacing) and fails for all 12 that do not (ends 729..740 of
`wireB_caps.json`, the vector `d…dhd cap`), with every one of the five guns: 120 of their 240 runs at spacing 1 and
180 of 240 at spacing 2 leave a stretch (the others are n = 1, and n = 2 at spacing 1). With those ends the pulses that ride down the wire B behind the
lower edge (REVIEW-signals-6 §3) are not swallowed: each adds a unit of B′ next to the end cap. `python3 line7e.py
729 4` (3 min): first gap 1: n − 2 units at unit 6; first gap 2: n units at unit 6; first gap ≥ 3: n units at
(h2 + e − 4)/2 as before; every word of 1..3 holes (2,047) and 17 dense words on 400 units (195 holes: 193 units), no
exception. So with one of the twelve the line counts every word of two or more holes, in one of two places.

**Other signals in E's place or in its way** (`python3 line7d.py`, 15 s):
- U in place of E: U alone is absorbed by the gun and the line runs on; with holes it leaves plain wire B for every
  n and every spacing tried (1..4). **The count needs E.**
- N1 or the pair EE: the line is destroyed, with or without holes.
- E with K0 or K3 in front of it (then holes or not): destroyed (the puncher of section 31 reaches the gun). N4:
  216 cells of debris.
- **E with N2 in front of it: one hole is left**, and nothing else: on a ring of 240 units the difference from the
  train after the meeting is exactly H at every even offset 6..40. In the line the end heals that hole and the line
  is, cell for cell, the running line again (from generation 96). This is a meeting the sixth push and its review did
  not run (N2 against anything), and it is the second way an up-signal is turned into a down-signal by a meeting
  (U with K3 leaves one H, REVIEW-signals-6 §3). It is also an antidote: an N2 between an echo and the gun saves the
  gun.

## 3. The enumeration, and what "within the bound" is

**The bound.** C is not a cell count. An end is a state of period dividing 4 of the 3 × 3 tube that equals the plain
train on every unit below some unit u₀ at every generation; translated so that u₀ = 6 (a translation by one unit
with two generations is a symmetry, so this loses nothing), all its cells at all generations must lie inside the two
planes x+y−z ≤ C, x−y−z ≤ C. Unit 6 begins near 21, one unit is 4, so C = 39 allows about 4.5 units: 68 cell sites
(33, 40, 47, 54, 61, 68 sites at C = 29..39). "The ends at C ≤ 39" are therefore **all ends of period dividing 4,
inside the 3 × 3 tube, whose part that differs from the train is at most 4.5 units long**. Beyond the planes and
outside the tube nothing is ever born (T2), so the instance is exact for the infinite lattice.

**An independent enumeration** (`enum7.py`: own region, own CNF with a sequential counter in full equivalences, the
train's four generations by oracle steps, the rule imposed on the region and on the last unit of the train;
pysat CaDiCaL 1.5.3; every model at C ≤ 37 re-stepped on the oracle; `enum_split.py` splits a long run on balanced
cells, each part ending in UNSAT):

| instance | push | here | time |
|---|---|---|---|
| receiving, 3 × 3, C = 29 / 31 / 33 / 35 | – / – / – / 90 | 0 / 1 / 12 / 90, the caps of the fourth and fifth pushes' lists as sets | 0, 1, 5, 16 s |
| receiving, C = 37 | 753 | 753, the same caps as the fifth push's list | 112 s |
| receiving, C = 39 | 6,286 | **6,286** (32 parts, each UNSAT) | 15 min + 19 min of an abandoned split |
| guns, C = 31 / 33 / 35 / 37 | 68 at 37 | 1 / 1 / 6 / 68, the caps of the sixth push's lists | 1, 2, 9, 18 s |
| guns, C = 39 | 873 | **873** (16 parts, each UNSAT) | 6 min |
| receiving, 5 × 5, C = 23 / 25 | 0 / 0 | 0 / 0 | 0, 1 s |
| receiving, 5 × 5, C = 27 | pending | TODO-fb5 | |

Distinct ends (`final_checks.py`; own key: the orbit over one period translated so that the first unit that ever
differs from the train is unit 0, with the time shift the translation needs): TODO-counts. The counts check
themselves: an end that fits at C − 4k is listed again k units on, so entries(C) = Σₖ distinct(C − 4k):
753 = 741 + 12, 6,286 = 6,196 + 89 + 1, 873 = 867 + 5 + 1.

**Is "none within the bound" a theorem?** It is a finite computation with three parts, each now done twice by
unrelated code: the list (two encodings, two solvers: cdcl7 and CaDiCaL; no UNSAT certificate from either), the runs
(step7 and the oracle / fast7), the classification. What it covers is exactly: the ends above; the 17 events of §4
(not "any word of holes or any down-running signal": eight words, the six down-signals known and two pairs, each at
one distance; for a period-4 end one distance is every arrival phase); outcomes read at the generation the disturbance
is 80 units up the stream. It does not cover period 8 (the README's row is pending), the 5 × 5 tube beyond C = 25,
ends longer than 4.5 units, or words other than the eight (a word whose holes are more than 14 rakes apart is covered
by the single hole: every heal is complete, on the whole state, within 53 generations).

**Does the enumeration silently exclude anything?** Not that I can find. Periods 1 and 2 are in (dividing 4). An end
that disturbs the train in front of it at some generation of its cycle is in: its u₀ is lower and it must fit from
there. The dedup key of `census7.py` normalises each generation separately and could in principle merge two ends;
my key cannot, and gives the same counts. `pool7.py`'s tree could not be re-run here (Windows process flags; its
cube files are on the owner's machine), so "every cube DONE" is the push's word; the count 6,286 is what I can vouch
for.

**`cdcl7.cpp`** (`cdcl_test.py`; the file compiled unchanged with g++ −O2): `small` (15 s): 400 random CNFs of 6 to
16 variables with a random projection and a random cube, 148 of them unsatisfiable, 9,474 projected solutions:
equal to brute force over all assignments, 400 of 400. `medium` (2 s) and `hard` (8 s): 50 random 3-CNFs of 60 to 210
variables near the threshold (up to 58,690 conflicts, so restarts and clause deletion run): equal to glucose4's
enumeration. `resume` (13 s): 12 instances stopped by the time limit 70 times and resumed from the solver's own
file, and split as `pool7.py` splits (the parent's solutions copied into four children): the union equals glucose4.
`ends 33` (31 s): my CNF at C = 33: 12 solutions, DONE, the same caps. One property to know: a stopped run keeps
its solutions but no learnt clause, so a part whose last proof does not fit in one time slice never ends; pool7's
splitting is what handles that. `ends7.cpp` was dropped by the push and nothing rests on it; not tested.

## 4. The census of ends

`census7a.py` rebuilds the 17 events from the README's description and classifies each (end, event) with the push's
criteria on units that are exact for the semi-infinite train (the end stands on a finite train on a ring of 448
units; the cut tail cannot reach unit u before generation u + 405). `--fast` runs it on fast7; without, on the oracle.

TODO-census

**What "dead" hides.** The push calls a row dead when the disturbance has reached 80 units up the stream and the end
is not equal to the undisturbed end. An end that had changed and sent a single signal up would be "dead" by that test
and would be exactly the listener looked for. So for every dead row two things are recorded at that generation: how
many of the 70 units between there and the end differ from the undisturbed run, and how many rake units are left on
them (the plain train has 35). TODO-dead. There are two kinds of death: a fire that leaves nothing (70 of 70 units
differ; in most of these the end's own cells are still there, without a train), and a front that strips the rakes and
leaves bare wire C, which a slower fire then eats (44 or 51 of 70 differ: the bare-wire units equal the train's own).
In no row is a rake left. So "no end is left alive and changed" is right in the sense that matters: **healed on the
whole state, or the train is gone.**

## 5. Guns

TODO-guns

## 6. The other claims and tools

- **Signal kinds** (`python3 kinds7.py`, 1 s): all 22 kinds of the two files satisfy the two-generation identity on
  the oracle (ring of 96 units, whole ring), in the stated direction. Review 6's nine signals mapped into the absorber
  frame by the mirror: K3 is the push's D7, N2 is D6, N3 is D3. So the ends were sent every known down-signal (H, K0,
  K3, N2, N3, N4) and the pairs HH, K0K0; the README's "K0, D3, D4 (= two K0)" lists N3 between two names without
  saying so. The one-cell tallies (24 / 66 / 22) were not recounted.
- **The count on the infinite train** (`python3 record7a.py`, 1 min, oracle, end 70 on a finite train, units ≥ −54
  exact to generation 300): n = 0: the end untouched. n = 1..6: least period 2 on generations 150..166 and 250..266,
  equal at 158 and 258, a stretch of 0, 2, 3, 4, 5, 6 units and one edge unit, pairwise different. As claimed (the
  push counts the edge unit in). In this frame the letters are mirrored (wire B reads d, the stretch 7).
- **The 125 and the 113**: TODO-125.
- **The push's own checkers on this machine**: TODO-push.

## 7. The forecasts

The README's "Forecasts scored" is a placeholder; `PREDICTIONS.md` was not edited. Scored here against what the push
found.

| # | forecast | p | outcome | Brier |
|---|---|---|---|---|
| 1 | the transfer-matrix enumerator reproduces the 741 | 0.85 | **no**: that enumerator was dropped (2.8 million successor states); the 741 were reproduced by a SAT solver written instead | 0.72 |
| 2 | the set of all 3 × 3 ends of period 4 is infinite | 0.55 | not resolved (1, 12, 89, 741, 6,196 at C = 31..39, a factor 8 per step, but no cycle was exhibited) | – |
| 3 | the 5 × 5 tube closed to 6 units beyond the train | 0.5 | **no**: closed at C ≤ 25, under 2 units | 0.25 |
| 4 | 5 × 5 census more than ten times the 3 × 3 one at the same bound | 0.6 | **no** where closed (0 against 0) | 0.36 |
| 5 | a listener found | 0.07 | no | 0.005 |
| 6 | an end that answers a hole with U | 0.08 | no | 0.006 |
| 7 | a 5 × 5 gun that survives E | 0.05 | void: no 5 × 5 gun census | – |
| 8 | an end that stops the lower edge of wire B and stands | 0.15 | **yes**: 125 of 741, 1,223 of 6,196 | 0.72 |
| 9 | every 5 × 5 end heals or is destroyed by H | 0.8 | yes on the one 5 × 5 end in `objects7.json` | 0.04 |
| 10 | period 8 adds nothing beyond C = 33 | 0.6 | not resolved (pending) | – |
| 11 | some 5 × 5 end answers a down-signal with an echo | 0.35 | no on the one end | 0.12 |

Eight resolved, mean Brier 0.28 (a constant 0.5 scores 0.25). The two large misses are the method (1, 3, 4: the plan
was a transfer matrix and the 5 × 5 tube; the work done was SAT in the 3 × 3 tube one step further) and the one
positive result (8), which was given 0.15.

## 8. What it means

**Is it the first memory in gump?** No. A state that signals write, that persists, and that differs by input has
been on file since the first two pushes, and the standing line is one of those objects:
- the wall B|B′ that swallows a pulse and moves one unit (`objects/transmission-B.json`, first push), and the second
  push's `objects/register-BBp.json`: a finite object in empty space, cap, wire B, wall, wire B′, cap, whose wall is
  moved one unit by each pulse from either side (section 9 of `research/signals/README.md`: "counter is the better
  word");
- the wall 8|C of the third push, which counts isolated pulses.
The object the line ends as is that register with two walls (B, a stretch of B′, B) and two new caps, and it behaves
as one: a pulse from above or below adds a unit at that end of the stretch, other one-cell changes take a unit off
or erase it (§2, `line7c.py flips 3`).

**What is new, and it is real.**
1. *The caps.* 125 ends and 5 guns of the **rake train** (1,223 and 78 at C ≤ 39) are also ends of wire B. So a
   running line, the system in which every train signal lives, turns itself into a capped register instead of
   burning or being converted for ever. This is question (r) of the sixth push answered yes.
2. *The writing is done by train signals.* Holes are what every bare end heals and forgets, or dies of (§4). Here a
   word of holes leaves a standing trace for the first time: the number of holes, exactly and without bound
   (to 193 in a 400-unit line), with the time of the second hole as the place. Question (g) of the fourth push (a
   standing object left in a different lasting state by a hole than by a rake) is met by the line as a whole and
   by no end.
3. *It is generic.* Every one of the 625 pairs of caps at C ≤ 37 does it; TODO-pairs39

**What limits it** (and the README says most of this): the write needs E, which nothing in the line makes (in the
push and here E is put on by hand; the only standing source on file is the reflector end, cap A with C18.23a beside
it, answering a hole); it happens once, because the train is spent; nothing is stored unless the second hole comes 3
rakes or more behind the first (with a healing end), so the line cannot tell a lone hole from a close pair followed by
anything.

**What is still missing for a listener** (open problem 13 (p): a state that a later signal can read back).
- *A read.* In push 7 nothing comes out of the object. The walls swallow what reaches them; the caps swallow the
  pulse made by flipping (0,1,4) in the plain object and it stands unchanged (the pulse made by (0,1,2) burns the whole
  object from the plain state, 44 flips of 608). What a pulse of each kind does at each of the 125 + 5 caps was not
  mapped. A read needs something whose *output* depends on the stretch: a pulse that passes plain wire B and is
  stopped by a stretch would do, if anything stood beyond the cap to receive it; no cap passes or reflects a pulse
  (section 9: no wall of the family does either).
- *The way back.* The count is written by train signals and stands in wire B. Nothing known turns a wire-B pulse into
  a rake, a hole or an E: no gun takes its timing from wire B. So even a read would speak a language the next line
  of this kind does not hear. This is the gap between the two halves of the signals work (wires and pulses since
  the first push; the train and its signals since the fourth), and the line is the first bridge across it, one way.
- *A trigger from inside.* E by hand. A line whose end is the reflector and whose gun is one of the five would make
  its own E from the first hole and then count the rest; whether the reflector end stops the lower edge of wire B was
  not tested by the push or here (it is not a bare end, so it is not among the 741).
- *Re-arming.* Written once. A reset would be a way from capped wire B back to a running train.
- *The listener in the strict sense* (an end left alive and changed while the train still runs) does not exist within
  the bounds (§4): every end at C ≤ 39 heals on the whole state or loses its train.

Two smaller things this review adds to the stock: **E meeting N2 leaves exactly one hole** (§2; with U against K3 the
second meeting that turns an up-signal into a down-signal, and one that saves the gun), and the twelve non-healing
caps, with which the line counts every word of two or more holes and writes the count at the end cap instead of in
mid-wire.

Pushes 8 and 9 (in the tree, built on this line, not reviewed here) take up the read.

## 9. Not checked

TODO-notchecked
