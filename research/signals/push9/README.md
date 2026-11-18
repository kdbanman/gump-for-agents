# Signals, push 9: a signal that calls a stored count back out

Written 2026-11-18. The wire, its letters, the store and the cell are push 8's (`../push8/README.md`); the crossing
wires, their survey and the sparse stepper are push 8b's (`../push8b/README.md`). Labels: **oracle** = stepped by
`reference/oracle.py` in a verifier that reads only the JSON object; **measured** = on a stepper that `check9.py`
compares with the oracle on objects of that kind (section 7); **proved**; **conjectured**. Commands are run from
`research/signals/push9/`; times are on the shared 4-core machine.

## The answer

Yes: two objects release a stored count when a signal arrives, both on the oracle.

1. **The call line** (section 2). A capped wire C laid across the store wire, one unit before the wall of the stretch.
   Two pulses of the line in adjacent units (a CALL) pass the crossing and go on unchanged, and the stretch `d^k f`
   leaves as exactly k left-going pulses two units apart; the wire is plain behind them and the line is cell for cell
   what it was. It calls again: set, add, call, set, add, call on the oracle. A CALL does nothing to an empty wire or
   to a stretch that begins anywhere else. A second store on the wire then holds exactly the sum; one line laid
   across two store wires calls both.
2. **The still life at the wall** (section 3). A six-cell still life beside the wire at the wall. The stretch stands
   beside it; a right-going pulse of the store's own wire that arrives at the wall releases the whole stretch as one
   block `b^(2k+2)` of wire C moving left; the still life never changes. A store that receives the block holds k + 1
   more. The wire beside this still life cannot carry a right-going pulse when no stretch is there (section 3,
   hazard), so on its own wire it is single use.

What is done by hand. For 2: one live cell removed, at least 10 units from every store and from the still life
(push 8's pulse). For 1: two dead cells of the line's tube made live in one generation, 15 units of the line (23
doubled sites, max-norm) from the store wire; they become the pair of pulses. No way of making that pair from one
pulse was found, and no call by a single pulse that leaves the second wire standing (section 5).

| claim | command | time |
|---|---|---|
| the call line on the oracle: `cycle`, `move`, `idle`, `idle-empty`, `chain`, `bus` | `python3 verify_call9.py` | 106 s |
| the still life on the oracle: `trigger`, `control`, `loop`, `write-then-call`, `smallest-loop`, `sum`, `call-far`, `clear`, `one` | `python3 verify_trigger9.py` | 62 s |
| every stepper and shortcut used here = the oracle | `python3 check9.py` | @@CHECKT@@ |
| the call law, k = 1..40 | `python3 call9.py --law` | @@LAWT@@ |
| the block law, k = 1..40, both parities | `python3 cell9.py --law` | 16 s |
| the CALL acts as push 8's hand release | `python3 reduce9.py` | @@REDT@@ |

## 1 Vocabulary

Wire B runs along v = (1,0,−1); unit u = the cells with x in {2u, 2u+1}; one hex letter per unit (`7` plain wire B,
`d` wire B′, `f` the edge unit, `b` a left-going pulse = one unit of wire C, `6f` a right-going pulse). A **store**
holding k is the stretch `d^k f`; its **wall** is between the unit before the first `d` and the first `d`. Pulses move
one unit per two generations. `R@u`, `L@u`: the stator (0,1,2), (0,1,4) of unit u removed at an even generation (a
right-going, a left-going pulse). The **cell** is push 8's: left cap, N units, right cap; both caps swallow pulses.
A **block** `b^n` is n adjacent units of wire C moving left as one piece; a right-going block of m pulses is
`6 e^(m−1) f`.

## 2 The call line

**Object.** Push 8b's capped wire C (`wires.capped_C`), 26 units along (1,1,0), 162 cells, placed by the symmetry
`lab.SYMS[11]` and the translation of `xlab9.CALL` so that it crosses the store wire at one unit c, the *crossing*
(the line's own unit 3; it has 21 units before the crossing and 4 after). The cells are `runs[].extra` in
`objects/call9.json`. Found by `cross9.py` (section 5) among push 8b's survey of crossing placements.

**CALL.** In the line's own frame, the cells (0,0,1) and (2,−2,1) of a unit made live at an even generation become
two right-going pulses of wire C in adjacent units and nothing else (`call9.SEED`; of all one-cell changes of a unit
of wire C in the 5 × 5 tube, both phases, none makes one pulse; among two-cell changes this is the only one that
makes exactly the pair [measured, not kept as a script]). The pair moves one unit per two generations, reaches the
crossing 30 generations after a launch 15 units before it, and is swallowed by the line's far cap; 42 generations
after the launch the line is at rest.

**What it does.**

- **[oracle: `idle-empty`]** Store wire and line stand together as the two alone, and a CALL across an empty wire
  changes nothing.
- **[oracle: `cycle`, `move`; measured k = 1..40: `call9.py --law`]** If the first unit of a stretch `d^k f` is
  c + 1, a CALL releases it: the wire carries exactly k left-going pulses two units apart (`b7b7…b`), then nothing;
  the line is at rest and unchanged. The pulses are swallowed by the left cap or added by a store on their way.
- **[oracle: `idle`; measured for a stretch beginning at c + 1 + o, o = −4..7, o ≠ 0, not kept as a script]** A
  stretch anywhere else is not called.
- **[oracle: `cycle`]** Pulses of the store wire pass under the line in both directions, and two pulses that stop
  each other there leave their mark `d f` beginning at c + 1 as on plain wire. So the whole life of a count goes
  through the oracle with the line in place: set (R@c−12, L@c+15), add one (L@c+15), add one, CALL: three pulses
  leave; the cell and the line are as at the start; then the same again with one addition: two pulses leave.
- **[oracle: `move`, `chain`]** A count moved exactly: two stores holding 1 and 3, CALL at the right one: the left
  store holds 4. With two stores holding 2 and 3 and a line at each: CALL at the right one gives 5 in the left one
  and the left line does not disturb the pulses that pass under it into its own store (the stretch grows at its
  right edge, the wall stays one unit after the crossing); CALL at the left one: five pulses leave, the wire is empty.
- **[oracle: `bus`]** One line across two parallel store wires (the second moved by 5 units of the line, (10,10,0)),
  stores holding 1 and 3 on the first and 1 and 2 on the second: one CALL releases three pulses on the first wire and
  two on the second. Wires 4, 5, 6 and 8 line units apart work on the stepper; other distances were not tried.
- **[measured: `reduce9.py`]** @@REDUCE@@

**What destroys it** [measured on push 8b's stepper at k = 3, not kept as scripts, not on the oracle]. At a crossing
with a stretch beside it, one pulse of the line, three adjacent pulses, or two pulses with a plain unit between them
destroy the store wire and the line (on an empty wire all three pass). A left-going pair from the line's far side
also calls, at one of the launch positions tried. A CALL while store pulses are under the line was not tried.

**For every k** [conjectured; route]. Push 8 proved that removing the stator (0,1,2) of the unit before the wall
releases exactly k pulses for every k (`../push8/prove_unzip8.py`). `reduce9.py` shows for k = 1..40 that the CALL is
that removal at a fixed generation and that the line takes no part afterwards. What is missing for a proof is the
same two facts for every k: both are local to the crossing, and the pulse train passing under the line is periodic
(period 4), so push 8's gluing argument should carry over; it was not written.

## 3 The still life at the wall

**Object.** The atlas still life S6b (six cells), placed for a stretch whose first unit is unit 0 at
`cell9.TRIG` = (0,0,9), (0,1,8), (1,0,8), (1,2,10), (2,1,10), (2,2,9). Its cell (0,1,8) is a neighbour of the
stator (−2,1,6) of the unit before the wall (one more live neighbour for that stator); no other cell of it is a
neighbour of a live cell of the wire, and six dead cells have neighbours in both.

- **[oracle: `trigger`, `control`; measured k = 1..40 and both parities of the pulse: `cell9.py --law`]** The stretch
  stands beside it. A right-going pulse arriving at the wall releases the whole stretch as one block `b^(2k+2)` moving
  left; the wire is plain; the still life is as it was. Without the still life the pulse is absorbed (count + 1).
- **[measured, n = 1..12, lab8 rings, not kept as a script]** A stretch absorbs a block `b^n` as ⌈n/2⌉. So the
  released count arrives in another store as k + 1 (the calling pulse is counted).
- **[oracle: `loop`, `write-then-call`, `smallest-loop`]** Stores 1 and 3, one cell removed between them: the left
  store holds 1 + 4. A store written by three left-going pulses (they pass the still life) and then called: 1 + 5.
  The smallest loop made: a cell of 24 units, 166 cells in all, two stores holding 1 and 1, one cell removed 10 units
  from each: the left store holds 1 + 2.
- **[oracle: `call-far`; the other three measured at k = 3]** The still life moved one unit away from the stretch
  (towards −v): block `b^(2k+5)`, worth k + 3. Moved one unit towards the stretch: the stretch does not stand (it
  leaves as `b^(2k)` with no pulse). Two units towards it: no effect (the pulse is absorbed as usual). Two or more
  units away: as on plain wire (hazard below).
- **[oracle: `sum`]** The half-turn image (`cell9.TRIGM`) at the right edge of a store is triggered by a left-going
  pulse and releases a right-going block. Two stores holding p and q released towards each other by two cells
  removed in one generation: the blocks meet and stand as one new store holding p + q + 1 (2 + 3 + 1 on the oracle;
  p, q = 1..5 at the right parity of the distance on lab8; at the wrong parity the trains reach the bare still
  lifes and the wire burns).
- **[measured, a, b = 1..8, lab8 rings]** A right-going block of 2a pulses and a left-going block of 2b meeting at
  an even gap stand as `d^(a+b−1) f`; at an odd gap each loses min(a, b, 2) pulses and the rest go on separately.
- **[oracle: `clear`]** The six faces of one cube (atlas S6a, `cell9.CUBE`) before the wall: the arriving pulse
  empties the store and nothing comes out (k = 1..9 on lab8; k = 3 on the oracle).
- **[oracle: `one`]** S6b in another place (`cell9.ONE`): the arriving pulse empties the store and one block `bb`
  (worth 1) leaves whatever k was (k = 1..9 on lab8; k = 3 on the oracle).

**Hazard** [measured]. On plain wire with no stretch at the wall place, a right-going pulse that reaches the trigger
still life turns the wire into a growing front of wire 8: the wire is lost. Left-going pulses pass. A block or a
second pulse arriving at a wall after the release also burns the wire. The cube eats left-going pulses on plain wire
and turns a right-going one into a block. So after a release nothing may be sent from the left past the still life
again; no word of at most 2 family units sent at the bare still life restores a stretch there (`python3 rearm9.py
--K 2`, 12 s, 480 runs; K = 3 not run).

## 4 Operations on counts

| operation | object | effect | status |
|---|---|---|---|
| call, exact | call line | k pulses out; another store + k | oracle (`move`, `chain`) |
| call, repeatable | call line | set, add, call, again | oracle (`cycle`) |
| call two wires at once | call line across two store wires | each store out as its own k | oracle (`bus`) |
| call + 1 | S6b at the wall | block worth k + 1 | oracle (`loop`) |
| call + 3 | S6b one unit further | block worth k + 3 | oracle (`call-far`) |
| clear | cube before the wall | k → 0, nothing out | oracle (`clear`) |
| constant | S6b at `ONE` | k → 0, a block worth 1 out for every k ≥ 1 | oracle (`one`), k = 1..9 measured |
| sum of two | S6b and its image, two pulses | p, q → one store p + q + 1 | oracle (`sum`) |
| halve a block | any store | `b^n` → ⌈n/2⌉ | measured, n = 1..12 |

Not found: a copy (a release that leaves the count behind), a doubling, a subtraction, a comparison. All additions
here are push 8's absorption; the new operations are the calls, the clear and the constant.

## 5 The scans, with their bounds

**Catalogue objects beside the wire** (`beside9.py`, then `wall9.py`, summaries by `sum9.py`; lab8 rings).
Every placement = 48 orientations × every phase × every even translation for which the closed neighbourhoods of
object and wire meet without a common cell, modulo sliding along the wire; kept if the pair returns exactly after
lcm(2, P) generations. Then each standing placement is put with its highest unit at wall − 1 + e, e = −3..3, beside
`d^3 f` (ring of 60 units), and sent nothing, or a right-going pulse born 11 or 12 units before the wall; read after
76 generations.

| objects | standing placements | pulse on plain wire | at the wall of `d^3 f` |
|---|---|---|---|
| the 13 still lifes of at most 8 cells | 3,780 | see below | 147 triggers (59 `b^11`, 59 `b^8`, 21 erased, 8 `bb`); 59 where the stretch falls without a pulse (`b^6`); 16 where it grows and a standing defect is left |
| the 81 still lifes of 9 to 11 cells | 69,773 | see below | @@STILL911@@ |
| 37 oscillators (28 of period 3 and 9 of period 4: the catalogue's oscillators of period ≥ 3 and union ≤ 22 cells, in catalogue order up to P4.14c; the other 48 were not run) | 51,223 | @@OSCPULSE@@ | @@OSC@@ |

Commands: `python3 beside9.py --sel still --max-cells 8 --out F` then `python3 wall9.py F --out G` (94 s) and
`python3 sum9.py G`; `--sel still --min-cells 9 --max-cells 11` (971 s in one process; the wall scan in four parts of
about 370 s each, `--part i/4`); `--sel osc --max-cells 99 --max-union 22` (stopped after 37 objects, 542 s; the wall
scan in two parts, @@OSCT@@).

- **[measured]** Still lifes (73,553 standing placements): 62,094 pass both pulses with everything restored; 1,670
  eat a pulse of one direction; 613 turn `b` into `bb`; 413 give `b^5` after three laps of a ring of 24; 8,760 leave
  the ring or the object changed otherwise. **No placement reflects a pulse.**
- **[measured]** Every trigger found among the still lifes (the stretch stands, the pulse releases it, the object is
  unchanged) is one of four kinds by what leaves: `b^8` (= `b^(2k+2)`), `b^11` (= `b^(2k+5)`), `bb`, nothing. In every
  one of them a right-going pulse on plain wire burns the wire or is changed: **no trigger in these scans is harmless
  to the pulses of an empty wire.**
- **[measured]** @@SITE@@

**One cell held live** (`python3 ghost9.py`, 80 s; `lab9.c`'s stepper with a constant added to the neighbour counts):
972 cells of tube radius 3..8 in the units −4..4 round the wall of `d^3 f`. Some release the stretch when a pulse
arrives (among them (0,1,8), a cell of the still life, and (−2,1,10)); none of those lets a right-going pulse pass on
plain wire. Pairs made of one of those two cells and any of the other 971 (`python3 ghostpairs9.py`, 75 s + 64 s):
none. So no object that acts through one or two fixed live cells can be a reusable same-wire trigger within radius 8.

**A pulse on a second wire** (`python3 cross9.py B --part i/2`, 66 s + 85 s; `python3 cross9.py C --part i/2`,
71 s + 65 s; push 8b's stepper; needs push 8b's survey files in `research/scratch/signals/p8b/`). Every placement of
push 8b's survey of a capped wire B or C crossing wire B that stands beside plain wire (434 and 312), with the
crossing at wall − 1 + j, j = −3..4, beside push 8's cell holding `d^3 f`; probes on the second wire: one pulse, or
two in adjacent units, each at two launch positions.

| second wire | (placement, j) that stand | probes | store emptied, second wire as it was | store emptied, second wire destroyed | store wire destroyed, second wire as it was |
|---|---|---|---|---|---|
| wire B | 3,176 | 12,704 | 0 | 104 | 14 |
| wire C | 2,428 | 9,712 | 12 (all with two pulses; 6 placements) | 0 | 10 |

- **[measured]** The 12: the call line and its mirror launch (`b7b7b` out; g = 11, t = (−4,2,−4), j = 0, and g = 35 at
  the other phase); a line at the far edge of the store that releases it to the right as `6f6f6f` (g = 14 and 38,
  t = (4,6,6), j = 4); and one that gives `bb5f9f9f` (g = 22 and 30, j = −1). Only the first was taken further.
- **[measured]** The 104 with wire B: one pulse on the second wire, the store leaves as exactly k separate pulses
  (`(b7)^k` or `(6f)^k`; k = 1..5 at 7 placements) and the second wire burns down to 12 standing cells. A fuse: a
  single-pulse call that works once.
- **[measured]** No single pulse on a crossing wire empties the store and leaves the second wire standing.

## 6 What failed or was not found

- A same-wire trigger that can be used twice (hazard, section 3; the scans of section 5).
- A call by one pulse of a second wire that keeps that wire (section 5); a way to turn one pulse of wire C into the
  adjacent pair (one-cell and two-cell changes only were tried).
- A reflector of pulses among 73,553 still-life placements.
- A copy, a doubling, a subtraction, a comparison of counts.
- The constraint search with the known release as target (direction 3 of the brief) was not attempted.

## 7 Tools, and how each is checked against the oracle

`python3 check9.py` (@@CHECKT@@): @@CHECK@@

| file | what it is |
|---|---|
| `lab9.py`, `lab9.c` | helpers on push 8's `lab8` (placements, ring boxes, letters) and the stepper with a constant bias |
| `beside9.py`, `wall9.py`, `sum9.py`, `site9.py` | the catalogue scans of section 5 |
| `ghost9.py`, `ghostpairs9.py`, `rearm9.py` | the censuses of held cells and the re-arming words |
| `cell9.py` → `objects/trigger9.json`, `verify_trigger9.py` | the still life's runs and their oracle verifier |
| `cross9.py`, `xlab9.py` | the crossing scan and the line's placement |
| `call9.py` → `objects/call9.json`, `verify_call9.py` | the call line's runs and their oracle verifier |
| `reduce9.py` | the CALL compared with push 8's hand release |
| `check9.py` | steppers against the oracle |

Both verifiers lay the start state on the oracle's cubic torus, compare the whole torus with the stated letters (+ the
standing objects) at every check, apply the stated cell changes, and refuse an operation nearer than 10 units to a
store or a still life (for the CALL: nearer than 20 doubled sites to any cell of a store wire). `verify_call9.py`
also computes that the start cells and their torus images are more than 12 sites apart and checks at every generation
that every live cell is within 4 sites of a start cell, which makes the torus run the run on the infinite lattice.
`verify_trigger9.py` relies on the size of its torus (side 2(N + 16)) without that computation.

## 8 Not checked

- The laws for k > 40, and any proof for every k (section 2, route).
- "What destroys it" (section 2), the idle offsets other than + 4, the bus distances other than 5, the block
  arithmetic, the clear and the constant for k other than 3: stepper only, not on the oracle.
- The line's behaviour when a CALL and a store pulse are at the crossing together; two CALLs closer than 44
  generations; lines shorter than 26 units; a smallest call cell (the oracle runs use 50 and 64 units).
- The other release lines of the crossing scan (`6f6f6f` to the right, `bb5f9f9f`) beyond k = 3.
- The oscillators of the catalogue beyond the 37 listed, periods 5, 6 and 10, and period-2 objects, beside the wire.
- Still lifes of 12 cells or more; objects that touch the wire's tube from two sides; anything in the tube itself.
- The scans use `d^3 f` only; a trigger that needs another k would be missed.

## 9 Forecasts

Scored in `PREDICTIONS.md`.

## 10 Where next

1. **A count that calls a count.** The released pulses are pulses of wire B two units apart; a CALL is two adjacent
   pulses of wire C. A junction from wire B into the line that turns two B pulses into the pair (push 8b's survey has
   junction placements) would let one store's release call another: the first loop with no hand in it after the
   start.
2. **The proof for every k** of the call law, by the route of section 2.
3. **The line to the right** (`6f6f6f` at the far edge) with the call line on the same store: a store that can be sent
   either way on command.
4. **A copy.** A call that leaves the stretch standing while the pulses leave was not seen in any scan; the keeps of
   section 5 (the stretch grows and a defect stands) are the nearest thing and were not examined.
5. **The fuse** as a one-shot call by a single pulse: 12 cells remain; whether they can be rebuilt by a signal is open.
