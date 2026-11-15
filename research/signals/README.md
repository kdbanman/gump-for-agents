# Signals: can anything in gump carry a signal from one place to another?

Open problem 13 of `research/OPEN-PROBLEMS.md`. Standing account: results, not a diary. Tags: **[proved]** (an exact
argument, an exhaustive search inside stated bounds, or a construction the oracle has stepped), **[measured]**
(counts, with the command), **[conjectured]**. Commands run from `research/signals/`; bulk output goes to
`research/scratch/signals/` (git-ignored). Forecasts and their scores: `PREDICTIONS.md`.
Sections 1 to 7: the first push (does anything carry a signal). Sections 8 to 14: the second push (machinery made of
carriers), brought up to date 2026-11-15 10:40 UTC. Sections 15 to 19: the third push (corrected from its review,
`research/audit/REVIEW-signals-3.md`). Sections 20 to 25: the fourth push (a standing emitter of rakes, section 20, and of a two-letter word, section 21b; 2026-11-15 15:00 UTC).

## Answer: yes. L1, L2 and L3 are reached, each with the oracle as judge; and (second push) a carrier has been turned into a clock, a register and a gate

| | what | one command (all print PASS lines and `ALL PASS`) | time |
|---|---|---|---|
| L1 | **pulse B**: 2 flipped cells on a period-2 wire of 5 cells per cube move one cube every 2 generations; the wire behind is exactly as it was | `python3 verify_pulse.py objects/pulse-B.json` | 3 s |
| L1 | the same pulse running the other way | `python3 verify_pulse.py objects/pulse-B-left.json` | 3 s |
| L1 | **pulse A**: 5 cells on another period-2 wire (6 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-A.json` | 3 s |
| L1 | **pulse S**: 32 cells on a **still** wire (5 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-S.json` | 3 s |
| L1, weak sense | **front**: the period-19 wire W00 is converted, one repeat every 19 generations, into a still wire | `python3 verify_front.py objects/F-W00-plus.json` | 20 s |
| L2 | **transmission**: flipping ONE cell at A sends a pulse down wire B; 36 cubes away a standing defect (a B|B′ wall, a unary counter) swallows it and moves one cube towards A; six shots in a row; a control run with A untouched never changes. Capacity d − 1 shots over d cubes (*review*) | `python3 verify_transmission.py objects/transmission-B.json` | 30 s |
| L3 | **interaction**: two pulses of wire B meeting head-on pass through each other unchanged, or stop each other and leave a 3-cell standing mark, according to the parity of their separation (the whole rule for head-on pairs, *review*) | `python3 verify_interaction.py objects/interaction-B.json` | 30 s |

| second push | **clock**: wire C between two caps, ONE cell added: a rake shuttles between the caps for ever. A finite object in empty space, 32 + 5N cells, **period 4N + 2** for N units of wire (N = 1, 5, 16, 17, 30 here; every N: `python3 prove_clock.py 8 4`, section 11) | `python3 verify_clock.py objects/clock-C.json` | 4 s |
| second push | **rake**: one extra cell on wire C moves one unit per 2 generations and emits a pulse every 2 generations; a pulse met head-on is swallowed or stops it, by parity | `python3 verify_rake.py objects/rake-C.json` | 3 s |
| second push | **collision gate**: two pulses of wire C meeting head-on: exactly one survives, undelayed, the wire as it was; which one is set by the parity of their separation | `python3 verify_gate.py objects/gate-C.json` | 9 s |
| second push | **register**: the boundary between wire B and wire B' moves one unit towards whichever pulse hits it: written by a one-cell flip on one side, erased by a one-cell flip on the other, exactly | `python3 verify_register.py objects/register-BBp.json` | 5 s |
| second push | pulses of wire C, both ways | `python3 verify_pulse.py objects/pulse-C.json`, `... objects/pulse-C-left.json` | 3 s |
| second push | **tape**: wire B and wire C are two letters of one medium: EVERY sequence of B units and C units moves rigidly towards −v, one unit per 2 generations (a ring holding all 32 windows of 5 units; with the light cone, a proof for all sequences) | `python3 verify_pulse.py objects/tape-BC.json`; `python3 verify_wall.py` | 3 s; 12 s |
| second push | two more pulses of wire C that reach outside its 3 × 3 tube, first seen coming out of chaos | `python3 verify_pulse.py objects/pulse-C-wide.json`, `... objects/pulse-C-wide-left.json` | 3 s |
| third push | **reader**: capL of the clock eats EVERY word of the B/C tape and remembers nothing: at every even generation the state is capL and the tape moved on (proof for all words by a closed automaton: `python3 prove_reader.py`, 0.3 s) | `python3 verify_reader.py` | 30 s |
| fourth push | **gun**: a 15-cell object of period 4 on the +v end of bare wire C puts a mirror rake on the wire every 4 generations and is exactly as it was each time; nothing is added to start it (section 20) | `python3 verify_gun.py objects/gun-5f.json` | 3 s |
| fourth push | **line**: a cap at rest, N units of bare wire C, the gun. Rakes leave one end, cross the wire and are swallowed at the other, for ever: the object has period exactly 4 from generation 2N on (every N ≥ 2: `python3 prove_line.py`, section 21). Removing ONE cell of one rake makes a one-cell pulse on that stream; the far cap swallows it and the object is then exactly as if nothing had happened | `python3 verify_line.py objects/line-C.json` | 8 s |
| fourth push | **beam**: the mirror-image gun, N units of rake train and a period-4 absorber found by constraint search: an oscillator of period exactly 4 with 33 + 5N cells for every N ≥ 1 (`python3 prove_beam.py`, section 21; N = 1, 2, 9, 24, 41 directly); the same one-cell pulse | `python3 verify_beam.py objects/beam-5f.json` | 12 s |
| fourth push | **divider**: the line with the 24-cell oscillator C8.24a of the clockwork catalogue (period 8) standing beside the wire, outside its tube. Every second rake that passes it becomes a hole; the oscillator is never changed (cell for cell the free oscillator at every generation); the wire beyond carries the train `5f9f`, one mirror rake per 8 generations, and the object has period exactly 8 from generation 2N − 3 (every N ≥ 8: `python3 prove_divider.py`): a standing emitter of a non-constant word (section 21b) | `python3 verify_divider.py objects/divider-C8.json` | 7 s |
| fourth push | **clock with a tail**: the clock's right cap replaced by an 11-cell object inside the wire, with wire C going on behind it; period 4N + 2 as before (N = 3, 5, 8, 16): a rake can be turned by something that has wire on both sides (section 22) | `python3 verify_clock.py objects/clock-C-tail.json` | 5 s |
| third push | **counter**: the wall between wire 8 and wire C moves one unit towards each pulse p< of a train (spacing ≥ 2) and the wire is otherwise exactly as it was. On a ring only: wire 8 has no known cap and burns from a cut end at one unit per generation (*third review*) | `python3 verify_counter.py` | 2 s |

Each verifier steps only with `oracle.masks` and `oracle.step` on a cubic array torus (H = 80 to 128) and compares
whole states cell for cell. `verify_pulse.py`: 100 periods = 2.5 laps of a ring of 40 cubes; the state at generation
2j is the state at generation 0 moved j cubes, and it differs from the pulse-free wire in exactly the moved defect cells.

Vocabulary. A **wire** is a pattern periodic along one lattice vector v (its *repeat*) and bounded across it. A
**front** has different periodic states ahead and behind (a fuse: it uses the medium up); a **pulse** has the same
one. "(p, s)": after p generations the state is itself moved by s repeats. All pulses here run along (1,0,−1) and have
(p, s) = (2, 1) with a repeat of one cube: **half the speed limit**.

### The objects (doubled coordinates; `objects/*.json` hold them in full)

- **Wire B**, per cube along (1,0,−1), i.e. plus every multiple of (2,0,−2): generation 0: (0,1,2), (0,1,4), (1,0,0),
  (1,0,2), (1,0,4); generation 1: (0,0,1), (0,0,5), (0,1,2), (0,1,4), (1,2,2). So (0,1,2), (0,1,4) never change.
  It lies in the 3 × 3 diamond tube 1 ≤ x+y+z ≤ 5, 1 ≤ x−y+z ≤ 5, which is closed by T2, so it is a wire of empty space.
  The half-turn (x,y,z) ↦ (−x−2, y, 8−z) maps it to itself reversed.
- **Pulse B**: flip (13,0,−12) and (14,2,−11) at an even generation. One cell with 6 or more live neighbours
  that was live the generation before (it dies) occurs at the pulse in every generation, none in the bare wire
  [measured; this is the drive the threshold lemma T5 demands, see section 4].
- **Emitter** [proved by the L2 run]: remove the never-changing cell (0,1,2) + k(2,0,−2) at an even generation: the
  wire heals and a pulse B leaves towards +(1,0,−1). Removing (0,1,4) + k(2,0,−2) sends one the other way [measured;
  on the oracle in the review]. The sender can fire every 4 generations; flips at odd generations heal (review §2).
- **Receiver** (`transmission-B.json`): 8 flipped cells over 4 cubes, the end of a stretch of the period-2 wire B′
  (= B with (1,0,2) off and (0,2,3) on): a wall between B and B′, i.e. a unary counter. It swallows every pulse and
  the wall moves exactly one cube towards the sender. So the line between A and the receiver is left exactly as it
  was after each shot and what is written at B is permanent; but **each pulse costs one cube of wire at the
  receiving end**, so a receiver d cubes away takes d − 1 shots: the review ran 35 clean shots over 36 cubes, and
  the 36th, with the wall beside A, sets the whole wire on fire. That is the sense in which L2 holds.
- **Eaters** [measured]: 10 of 150 standing defects of wire B swallow every pulse and stay exactly as they were.
- **The mark** left when two pulses stop each other: (28,2,−25), (29,0,−26), (30,2,−27) up to translation. A later
  pulse from either side is swallowed by it and it becomes a 5-cell standing defect [measured; on the oracle in the
  review].
- **Parity is the whole rule** for a head-on pair (review §2, separations 2 to 44 on rings of 64 and 65): odd
  separations pass, even ones stop. On an odd ring a passing pair stops at its second meeting (the separation has
  changed parity). Pulses going the same way run as rigid trains at every spacing 1 to 12.

## Tools, and how each was checked

| file | what | checked by |
|---|---|---|
| `sg.py`, `sgc.c` | the lattice modulo any period lattice, cut down to diagonal layers (`Geom`); C kernels: dense and sparse steppers, cycle detection, the two-state difference tracker `track` | `python3 check_stepper.py` (5 s, ALL OK): cell for cell against `oracle.step` on five box tori at three densities for 40 generations; the set stepper against the oracle; twisted tori, slabs, tubes and a 3D twisted torus against the set stepper on a lifted patch; a wrong rule (B45/S34) is detected |
| `verify_*.py` | the judge: `oracle.masks`, `oracle.step`, nothing of mine in the stepping | — |
| `extract_wires.py` → `wires/Wnn.json` | the 21 wires and 2 sheets of the notebook entry of 2026-11-15 (nn = line in `research/audit/shape3/zombie_states.txt`): one repeat, phase 0, repeat vector | each re-run on a ring of 6 repeats beside 30 empty cubes: exact period reproduced |
| `wirelab.py`, `plab.py` | rings of a wire on file; the lab for the SAT wires (tube −7 ≤ s₁, s₂ ≤ 13: exact in empty space for anything started within a neighbour step of a 3 × 3 wire) | use `sg.Geom` only |
| `sat_pulse.py`, `sat_defects.py`, `survey.py` | SAT (CaDiCaL 1.5.3 through pysat): pulses with an unknown background; all defects of a given wire; all backgrounds carrying a pulse | every model is re-stepped with `sg.Geom` before it is reported. UNSAT rests on the encoding; `bounds.sh` repeats each instance with Glucose 4 |

| second push: `scat.py`, `sat_reflect.py`, `caps.py`, `caps_any.py` | SAT for a wire's end: caps, reflectors (section 8) | every cap and every model is re-stepped (`sg.Geom`, `sg.step_set`); UNSAT rests on the encoding and on CaDiCaL alone |
| `scatter_table.py`, `clocks.py`, `walls.py`, `family.py`, `seglab.py`, `collisions_C.py`, `soupwires.py`, `clock_family.py`, `capclocks.py` | measurements with `sg.Geom` / `sg.step_set` in closed vessels (the 3 × 3 tube, cut by planes): exact for empty space by T2 | use the checked steppers only; what they found that matters was then put to the oracle |
| `chaoswire.py`, `tapes.py` | a wire against a block of soup in an 11 × 11 tube; pairs of unit types that move rigidly | `sg.Geom`, `sg.step_set` only |
| `verify_register.py`, `verify_clock.py`, `verify_gate.py`, `verify_rake.py`, `verify_wall.py`, `prove_clock.py` | the judge again: `oracle.step` on a cubic torus (in `prove_clock.py` the base cycle) | — |

**Soundness of the SAT search** (`sat_pulse.py`). Ring of N cubes of a closed tube; unknown states at generations
0..p−1; generation p is generation 0 moved s cubes; the cubes 0..K+b−1 are b-periodic along the ring at every
generation; generation 0 is not b-periodic all round. (i) With gcd(s, N) = 1 a solution cannot be a standing defect:
the set D of places where generation 0 is not locally b-periodic obeys D(p) = D(0) + s, and D + s = D would make D
empty or everything. (ii) With K ≥ max(3, s+1) the b-periodic stretch, continued for ever, is itself a solution (each
step agrees with the ring on an interval longer than b), and gluing it to both sides of the defect gives a solution of
the infinite tube: one pulse, the same background on both sides. Every pulse above was then put alone on a ring of
40 or more cubes and stepped by the oracle.

*Corrections of 2026-11-15 (third push), taken from the review `research/audit/REVIEW-signals.md` after checking
each against its evidence: the receiver is a B|B′ counter with capacity d − 1 (table row L2, "Receiver"); pulse B's
overcrowded cell dies (pulse B); the emitter's rate; parity is the whole head-on rule, trains are rigid, the mark's
later behaviour is on the oracle ("The mark"); the duplicate wires (section 1); wire B's flip census (section 3);
corollary 1's argument (section 4); the bounds table (section 6).*

## 1. The wires on file: cuts, flips, kinks

- **[measured] Cutting one repeat out** (`python3 cut_wires.py`, 2 min; ring of 48, every phase, gaps of 1, 2, 3
  and 24 repeats): 12 of the 21 wires burn (W00, W05, W10, W18, W19, W21, W24, W30, W31 in every phase; W15, W20,
  W29 in 4 of 16 phases, W16 in 1), the other 9 are capped within 3 repeats. The caps of W09, W17, W25, W26, W33 hold
  new small clocks (the cut wire's period becomes 38, 57, 190; 48; 80; 208).
- **[measured] The fronts** (`python3 fronts.py`, 7 min; ring of 240; X(t+p) compared cell for cell with X(t)
  moved s repeats, from 8 repeats behind the front to 6 ahead):

  | wire (period, repeat vector) | side | speed | (p, s) | ash |
  |---|---|---|---|---|
  | W00 (19, (1,3,−4)) | +v | 1 repeat / 19 gens | (19, 1) | still, a connected still wire |
  | W00 | −v | 3 repeats / 38 gens | (38, 3) | still: separate 49-cell still lifes, one per 3 repeats |
  | W05, W10 (11, (1,3,−4)) | both | 1 / 11 | (22, 2) | period 12, connected; each repeat one generation behind the last |
  | W15 (16, (2,−4,2)) | +v | 1 / 32 | (32, 1) | period 4 |
  | W18, W21, W30, W31 (9, (3,0,−3)) | +v | 2 / 27 | (27, 2) | period 30 |
  | W19 (9, (3,0,−3)) | −v | 2 / 27 | (27, 2) | period 30 |
  | W24 (22, (3,0,−3)) | both | 1 / 12 | (132, 11) | period 22, not a phase of the wire |

  In cubes per generation: 0.21 to 0.36 of the speed limit. No ash is the wire in another phase. `python3 ash.py`
  (3 min) says what each ash is. Only F-W00-plus has been put to the oracle.
- **[measured] Every one-cell flip** (`python3 flips.py`, 12 min; ring of 32; every cell live in some phase and
  every neighbour of one, in every phase: 57,150 trials): heals 28,337; settles within 3 repeats 17,188; **starts
  a front 11,544 (in 17 of the 21 wires; none in W09, W11, W12, W24; the 21 are 18 up to symmetry, W17 = W20 = W26
  and W18 = W30, so 14 of 18 distinct wires, review §5)**; undecided at 1,500 generations 81; **pulses
  0** (no trial in which the difference ever lay wholly 3 or more repeats from where it was made).
- **[measured] Phase kinks** (`python3 kinks.py`, 30 s; repeats 10–29 of 40 at phase d, the rest at phase 0, every
  d): no boundary between two phases of a wire travels. It stays as a wall a few repeats wide (every d in W11, W24,
  W35; most in W09, W12, W25) or it starts fronts.

## 2. Wires are common; a fifth of them are fuses; sampling finds no pulse

- **[measured]** `python3 harvest.py 3 3 L 20000 --seed L`, L = 1..4 (7 min in all): soups on a ring of L cubes of
  the closed 3 × 3 tube settle into a wire about one time in ten (L = 4: 2,063 of 20,000; 468 distinct by a coarse
  key). Each distinct wire, 40 repeats long, was cut (every phase) and hit (one repeat replaced by soup, 24 times):
  of 875 wires, 167 showed a front, at speeds up to **one cube per generation, the speed limit** (still wires among
  them); **no pulse in 21,000 hits**. Pulses were found only by constraint search.

## 3. Pulses: what the constraint search found

- **[proved, exhaustive SAT within the bounds; models re-stepped]** `python3 survey.py 3 3 9 2 1 --max 30`
  (20 s): in the 3 × 3 tube at least 30 different uniform backgrounds carry a (2,1) pulse at most 4 cubes wide (the
  list was cut at 30, not exhausted). All 30 have period 2, 4 to 6 cells per cube. Each was tested in the wide tube:
  one-cell flips, the pulse alone for a lap, and the pulse against its mirror image where the wire has a reversing
  symmetry. Most wires are fuses for most flips and catch fire when two pulses meet (wire A: 58 of 88 flips start
  fronts at the pulse's own speed; pulse against pulse, and pulse against each of 60 standing defects at two distances, sets it
  alight). **Wire B is the robust one: of its 84 one-cell flips 74 heal, 2 leave a standing defect (one of 1 cell, one of
  2 cells), 2 emit a single pulse (one each way) and 6 start fronts** (the review's own census agrees exactly).
- **[proved, exhaustive SAT]** defects of wire B inside the 3 × 3 tube (`python3 sat_defects.py objects/pulse-B.json
  P S --N n --lo 1 --hi 5`): right-moving (2,1) defects fitting in 5 cubes: exactly 17 (pulse B, other pulses and
  trains; not sorted). Standing defects of period 2 in 4 cubes: more than 1,000 (the list was cut there). Standing clocks of exact
  period 4 in 4 cubes (`--exact`): exactly 28. Wire A: exactly 6 right-movers in 5 cubes; none with (p, s) = (4,1),
  (4,3), (6,1) in 5 cubes.
- **[measured] What a train of pulses does to a standing defect of wire B** (`python3 sat_defects.py
  objects/pulse-B.json 2 0 --N 8 --lo 1 --hi 5 --max 1000 --out ../scratch/signals/d.json; python3 receivers.py
  ../scratch/signals/d.json --pulse objects/pulse-B.json --max 1000`, 10 min): of the first 1,000 period-2 standing
  defects in 4 cubes (the list is longer), 636 catch fire at the first pulse, 109 are eaters, and 255 are walls
  that swallow each pulse and advance one cube (8 pulses each). Of the 28 period-4 clocks: 14 fire, 8 eaters, 6
  walls. **No defect was found that a pulse toggles between two states, none that lets the pulse through and keeps a
  record, and no clock whose phase a pulse shifts.** (17 defects in the wider tube −1..7, 3 cubes: all fire.)
- **[proved, exhaustive SAT] A pulse on a still wire needs room**: in the 3 × 3 tube, uniform still background,
  (p, s) = (2,1): none with defect-plus-sweep ≤ 6 cubes (rings of 7 to 11), one at 7 (pulse S, 32 cells).
- **Bounds of the search with unknown uniform background**: section 6.

## 4. What is proved about carriers in general

- **[proved] A wire cannot grow at its end.** *(Argument corrected 2026-11-15 after the review, §6; one half-space
  is not enough.)* Let D be the set of signed body diagonals d with d·v < 0. A wire bounded across its axis and
  empty beyond its end (along −v) has d·p bounded above on its support for every d in D, so by T2 it stays in the
  intersection of the half-spaces d·p ≤ C_d for ever; and −v is a non-negative combination of the elements of D
  (if −v lies in the cone x ≥ |y|, |z|, then −v = a(1,σ,τ) + b(1,σ,−τ) + c(1,−σ,τ) with a = (|y|+|z|)/2,
  b = (x−|z|)/2, c = (x−|y|)/2). Hence (−v)·p stays below a fixed bound: the support never passes a plane
  perpendicular to v. No front runs from a wire into empty space: fuses burn, nothing lays track.
- **[proved, corollary of T5] A pulse on a wire of period ≤ 2 that has no drive of its own must carry its drive
  with it**: on a ring it is an orbit of period N·p/s > 2 in a finite vessel, so in every lap, hence (by the shift
  symmetry) in every period, some cell has 6 or more live neighbours having been alive the generation before; if the
  bare wire has no such cell they are at the pulse. Measured: wire A and wire B have none; pulse A has 2 per
  generation, pulse B has 1.
- **[conjectured]** Pulses are not attractors: nothing sampled ever settled into one (sections 1, 2), though one
  flip in 42 of wire B emits one. Half the speed limit is the only pulse speed seen.
  *(2026-11-15, second push: the wires that carry pulses ARE attractors: wires B and C arise from random soup,
  section 12. A pulse itself has still never been seen to arise from soup. And on wire C one flip in particular,
  adding the cell (1,0,4), does not make a pulse but a rake, section 10.)*

## 5. Not done, not checked

- UNSAT answers are not certified by a proof checker; they rest on my encoding (the same encoding whose models
  always re-step correctly) and on two solvers agreeing where `bounds.sh` ran both.
- ~~Whether wires A, B, S arise from random soup~~ *(2026-11-15: wire B does, and wire C; section 12. A and S not
  checked.)* Whether any pulse exists in a wire on file, beyond one-cell flips.
- Fronts other than F-W00-plus have not been put to the oracle; nor have the eaters, the mark's later behaviour,
  the left-going emitter, or wire A's collisions (all `sg.Geom` only).
- Two-cell flips of the 21 wires (`python3 flips.py --pairs` is written, hours of one core, not run); the two
  sheets; sheets and crystals as media at all (the lead's S4); unrolling a twisted clock onto a straight track (S5).
- Other directions than (1,0,−1), backgrounds of repeat > 1 cube, tubes wider than 3 × 4, periods above 6.
- A receiver that does not creep (a toggle), a clock whose phase a pulse flips, a gate with an output pulse (in
  wire B a meeting either changes nothing or ends both pulses: that is a coincidence detector with a permanent
  record, not yet a logic gate with a signal out), and a way to end a wire (every wire here is a ring or infinite). *(2026-11-15: sections 8 to 11 take these up.)*

## 6. Bounds of the pulse search with an unknown background

`bounds_table.txt` (from `bash bounds.sh`; every instance with CaDiCaL 1.5.3 and with Glucose 4, which agree
everywhere both finished). Uniform background (repeat one cube, any period dividing p), closed tube M1 × M2 along
(1,0,−1), ring of 13 cubes, defect plus the s cubes it sweeps at most 9 − s cubes (less for s ≥ 3: 5, 3, 1 cubes
for s = 3, 4, 5):

| tube | pulse exists [proved] | no pulse [proved within the bounds, two solvers] | undecided |
|---|---|---|---|
| 2 × 2 (6 cells per cube) | none | (1,1), (2,1), (3,1), (3,2), (4,1), (4,3), (5,1), (5,2), (5,3), (5,4), (6,1), (6,5) | — |
| 2 × 3 (9 per cube) | (2,1) | (1,1), (3,1), (3,2), (4,1), (4,3), (5,1), (5,2), (5,3), (5,4) | (6,1) (300 s) |
| 3 × 3 (14 per cube) | (2,1) | (1,1), (3,1), (3,2), (4,3), (5,2), (5,3), (5,4), (6,5) | (4,1), (5,1), (6,1) (100 s) |

*(2026-11-15, after the review, §4.)* The width bound in one convention: the defect, together with the s cubes it
sweeps, fits in N − K − 1 = 9 − s cubes (for (5,4) and (6,5): 3 and 1 cubes, so those two rows say little). The
3 × 3 rows rest on the encoding, with two solvers agreeing. An independent transfer-graph search that shares nothing
with the encoding and has **no width bound** (`research/audit/signals/transfer.py`) confirms all twelve 2 × 2 rows
and the 2 × 3 rows (1,1), (3,1), (3,2), (4,1), (4,3), (5,1), (5,2), (5,3), (5,4), and adds 2 × 3 (6,5): for these
there is no pulse of any width on any uniform background. It did not finish the 3 × 3 tube.

So within these bounds the only pulse speed is one cube per two generations; in particular there is no pulse at
the speed limit ((1,1)) in any of the three tubes, although fronts at the speed limit exist (section 2). Not
searched: (p, s) with p ≥ 7, the pairs (4,2), (6,2), (6,3), (6,4) (which contain the (2,1) pulses), s = p for p ≥ 2,
backgrounds of repeat 2 or more cubes, wider tubes, other directions.

## 7. What to show a human first

`python3 -c "import plab; ob=plab.load('pulse-B'); g=plab.geom(64); b=plab.background(g,ob); print('\n'.join(plab.kymo(g, plab.with_defect(g,b,ob['defect'],0), b, 60, 2)))"`
draws the pulse as a diagonal of two marks crossing a row of dots (one character per cube, one line per two
generations; a dot is a cube that is exactly as the bare wire). Then `verify_interaction.py`: two such diagonals
cross and go on as if nothing had happened, or, started one cube differently, end in three cells that stay.
What is strange: the smallest carrier of a signal in this universe is two cells on a five-cell-per-cube ribbon;
nothing random ever settled into it; and the constraint search found it in under a second in the first tube tried.

*(Second push.)* Then `python3 show_clock.py 12`: a row of `b`s between two caps, one `f` running to the right
end with a comb of `7`s streaming away behind it, turning into `5f` and running back behind a comb of `9f`s, for
ever, 50 generations a round; make the row one unit longer and the round takes 4 generations more. And
`python3 collisions_C.py`: two marks run at each other and one of them is simply gone, which one depending on
whether they started an even or an odd number of units apart. And `python3 chaoswire.py show 1 --T 240`: a
block of noise in the middle of a wire, and from both sides of it a line of fire running out along the wire at
exactly the speed of a signal, leaving a different debris every time. What is strange here: one added cell is enough to
make a stretch of ribbon keep time, and ribbons of this kind come out of random soup about once in 360 tries.

# Second push (2026-11-15): from a carrier to machinery

The lead's six items, where each stands: (1) a bounded track: **reached**, section 11 (a clock of period 4N + 2 for
every N, proved); no corner, no closed polygon. (2) a receiver that stays put: a **register** written from one side
and erased from the other (section 9); no same-side toggle (section 8). (3) a gate: a **collision gate** whose two
outputs leave along the two input lines (section 10); no gate with a separate output line, no crossing. (4) where
wires come from: **pulse-carrying wires are born from soup**, and wire B is turned into wire C by a moving wall
(sections 12, 10). (5) wire against chaos: **contact destroys the wire every time; two empty layers isolate the
capped end tested, three isolate any wire (T3)** (section 13; corrected 2026-11-15 after the second review). (6) loose ends: untouched except the caps (section 14).

Vocabulary of this part. **Unit** u: the cells with x in {2u, 2u+1}; moving by (2,0,−2) adds 1 to u. "Towards +v"
is towards larger u. A **cap** is a way for a wire to end in empty space and stay as it is (period 2). All states are
described at even generations unless said.

## 8. Ends of wires: caps, and what a pulse does at one

Geometry of every search here: the wire is bare on units < KS (KS = 6); anything at all may be on units ≥ KS inside
the 3 × 3 tube and the two planes x+y−z ≤ C, x−y−z ≤ C (C odd; C + 4 is the same position one unit on, so C mod 4
gives two inequivalent positions). By T2 nothing is ever born beyond the planes, so each solution is a semi-infinite
wire in empty space, exactly. The enumeration is by SAT with every solution blocked until UNSAT: complete inside
the bounds.

- **[proved: exhaustive inside the bounds; behaviour measured] Wire B has caps, and none of them reflects.**
  `python3 caps.py C` (C = 25, 27, 29, 31, 33: 1 s to 4 min): 0, 2, 52, 494, 3,644 caps of period 2 (19 to 47 free
  cells). Each was hit by six pulses B in a row (a finite object in a closed vessel: cap, 70 units of wire, an eater
  at the other end): **3,165 catch fire, 734 swallow every pulse and stay exactly as they were, 293 swallow each
  pulse and move one unit towards the sender. None sends anything back; none has two states that a pulse flips.**
  The smallest eater is 8 cells (`caps.EATER`).
- **[proved within the bounds, one solver] No restoring reflector for pulse B.** `python3 sat_reflect.py T C`: a
  cap of period 2 inside the planes such that the wire with an arriving pulse is, T generations later, the same cap
  with the pulse going back: UNSAT for C = 29 and 33 with T = 8, 10, .., 20, and C = 37 with T = 10, .., 16.
  `--obj pulse-C`: UNSAT for T = 8..14 at C = 29, 31; T = 8, 10, 12 at C = 33, 35, 37; T = 8, 10 at C = 41.
  *(2026-11-15, second review: Glucose 4 reproduces the UNSATs for pulse B at T = 8, 10, 12 and pulse C at T = 8,
  10 (C = 29); odd delays T = 9..15 for pulse B at C = 29 and 33 are UNSAT too. What is excluded, exactly: a cap of
  period 2 in the 3 × 3 tube that is exactly restored by the generation at which the exact left-moving pulse is
  back at unit 3. A reflector whose cap is still settling then, caps of period above 2, and caps outside the tube
  are not excluded.)*
- **[measured] Wire C's caps do send pulses back, but each only once.** `python3 scatter_table.py 28 C --out F`
  (28 = wire C in the survey file; C = 27, 29, 31: seconds to 2 min; C = 33 with `--max 4000`: about 6 min) builds the
  table (cap state, kind of arriving pulse) → (verdict, new cap state, what comes back), closing the set of cap
  states under hits. C = 29: 111 caps, 134 states: 9 reflect the pulse (pulse C in, the left-going pulse C out).
  C = 31: 1,256 caps, 1,493 states: 135 reflect. In **every** one of these 144 cases the cap is changed (in 143 it
  also moves one unit towards the sender), and the next pulse sets the changed cap alight. C = 33 (the first 4,000
  caps only; 7,646 states; four kinds of arrival: p> and three compounds that the caps themselves send back,
  closed under the mirror): 2,108 reflections; 68 of them leave the cap exactly as it was, all turning a compound
  arrival (a rake with a pulse close behind it that eats what the rake emits, kinds `r>`, `s>`) into a single
  pulse; no end turns a single pulse back into such a compound, and the search for a closed cycle of reflections
  between two ends (`Table.cycles`) finds **none**. So no cap in these bounds keeps a single pulse of wire C
  bouncing. (What can be kept bouncing is the rake: section 11.)
- **[measured] The other 29 wires of the survey.** `python3 caps_any.py 29` and `... 33 --max 3000` (10 min):
  all caps of each of the 30 pulse-carrying wires of `survey.py`, each hit once by its wire's pulse. Something
  travels back only in wires 16, 17 and 28, which are wire C and its mirror image C′ (section 9). The verdict
  called `clock` there is misnamed: in the wires probed (`python3 capclocks.py 29 27 11 10 4 3`) it is a slow
  front eating the wire at about one unit per 5 generations.
- **[measured, negative]** Two other formulations were tried and are too slow to say anything: wire, pulse and
  cap all unknown (`sat_reflect_any.py`: UNSAT at T = 8, 10 with C = 33, nothing beyond), and a periodic train
  reflected in steady state (`sat_steady.py`: CaDiCaL does not finish even on an instance known to have a solution).

## 9. A family of four wires, their walls, and a register

- **[measured] The four-site family** (`python3 family.py`, 20 s). Every unit holds the two cells that never change,
  (0,1,2) and (0,1,4), and a subset of four sites: 0 = (1,0,0), 1 = (1,0,2), 2 = (1,0,4), 3 = (0,2,3). A unit is
  written as the hex digit of its subset (site i has value 2^i). Of the 16 uniform choices, 11 are wires of period 2,
  and exactly the four with three sites carry a 2-cell pulse, each in both directions: **B** = 7, **C** = b,
  **B′** = d, **C′** = e. (B′, C, C′ are wires 21, 28, 17 of the survey.) B′ is B under a symmetry of the lattice
  and C′ is C; B and C are different wires (`soupwires.py` checks all 48 rotations and reflections).
  The half-turn (x,y,z) ↦ (−x−2, y, 8−z) maps B and B′ to themselves reversed and exchanges C and C′; the mirror
  (x,y,z) ↦ (z−4, y, x+4) maps wire C at one generation onto wire C at the next, reversed.
- **[measured] Walls between family wires** (same command): nine clean boundaries U|V are stationary. Hit by a
  pulse, B|B′, 8|C, 8|C′, C|8, C′|8 swallow it and move one unit towards the side it came from; 2|C′ and C′|2 burn.
  No wall passes a pulse on, none reflects. `python3 walls.py U --k 3` (U = B, C, B', C'; 90 s each) adds up
  to three arbitrary units between U and each of the 11 wires (16³ × 11 arrangements each): stationary ones 49, 90,
  24, 207; first hit reflects in 0, 17, 0, 40 of them, never twice, and no arrangement comes back to itself.
- **[proved by the oracle run] A register** (`python3 verify_register.py objects/register-BBp.json`, 5 s). A finite
  object: an eater cap, wire B, the wall, wire B′, a cap. A pulse B arriving from the B side moves the wall one unit
  towards the B side; a pulse B′ arriving from the other side moves it one unit back. Each operation is a flip of
  ONE never-changing cell of the wire ((0,1,2) of unit −3, on the B side, at an even generation: *write*; of unit
  13, on the B′ side, at an odd generation: *erase*); 40 generations after each operation of the run
  W E W W E E E W W E the whole state is exactly the object with the wall one unit nearer the side the pulse came
  from. So the wall's position is a counter that one line increments and the other decrements, in place, and the
  state after any sequence depends only on the difference of the two counts **while the wall stays between the
  write and erase sites** (here 16 positions, wall at −2..13; nine writes or eight erases in a row break it; two
  writes 2 generations apart do not make two pulses; a pulse arriving 1 to 31 generations after the last is fine:
  second review, `research/audit/signals2/register_check.py`). "Counter" is the better word than "register". It is
  not a toggle: the same pulse twice does not restore it.

## 10. Wire C: two pulses, two rakes, and what happens when they meet

`python3 collisions_C.py` (5 s) prints every case below as text, one hex digit per unit, one line per 2 generations.

- **[proved by the oracle runs]** Wire C (per unit: (0,1,2), (0,1,4), (0,2,3), (1,0,0), (1,0,2) at even
  generations) carries the pulse **p>** (`9f`: remove (1,0,2) of one unit, add (1,0,4) to the next; towards +v) and
  **p<** (`7`: in one unit move (0,2,3) to (1,0,4), which makes that unit a unit of wire B; towards −v), both one
  unit per 2 generations (`verify_pulse.py objects/pulse-C.json`, `... pulse-C-left.json`).
- *(Corrections of 2026-11-15 from `research/audit/REVIEW-signals-2.md`, checked against its evidence and applied in
  sections 8 to 13: the register's range; the mark left by rake against rake; the clock's transient and ignition
  cells; the soups by ring length; what two empty layers isolate and at what density fire runs at pulse speed;
  what the reflector search excludes.)*
- **[proved by the oracle run] The rake** (`python3 verify_rake.py objects/rake-C.json`, 3 s). Add ONE cell,
  (1,0,4), to a unit of wire C (`f`). It moves towards +v one unit per 2 generations and leaves a p< behind every
  2 generations: at generation 2m the rake is m units on and there are pulses at m−2, m−4, .., −m, exactly
  (checked for m = 1..10). The mirror image (`5f`) runs towards −v and emits p>. A rake is a moving source of
  pulses; nothing stationary that emits was found.
- **[proved by the oracle run] Collision gate** (`python3 verify_gate.py objects/gate-C.json`, 9 s). p> and p<
  meeting head-on: **exactly one of them survives**, undelayed, and the wire is left exactly as it was. If the p<
  starts an even number of units from the first unit of the p>, the p< survives; odd, the p> survives (separations
  10, 12 and 11, 13 on the oracle). As a logic element, with inputs L (a p< is sent) and R (a p> is sent) and the
  outputs read further along the same two lines: even separation, (left out, right out) = (L, R ∧ ¬L); odd,
  (L ∧ ¬R, R). So one line can **inhibit** the other, reusably and without delay. It is not a gate with a third,
  separate output: the wire is one-dimensional and no crossing or corner is known. Contrast wire B (row L3 of
  the first table): there both pass or both stop.
- **[proved by the oracle run] Rake against pulse** (`verify_rake.py`, cases B and C): a p< meeting the rake
  head-on at even separation is swallowed and the rake goes on; at odd separation the rake is stopped and only
  left-going pulses remain. Mirror statement for `5f` against p> (on the oracle in the second review, R3); and rake
  against rake: one of the two survives, by parity, **and a two-unit mark (`dd` in the p> train or `77` in the p<
  train) travels on with the survivor's train** (oracle, review R4).

- **[proved: oracle run + light cone] The tape.** Every boundary between wire B and wire C, in either order,
  moves towards −v at one unit per 2 generations, and so does every pattern made of B units and C units:
  `python3 verify_pulse.py objects/tape-BC.json` (3 s) runs a ring of 40 units, each B or C, in an order that
  contains all 32 possible runs of five; after 2j generations the whole state is itself moved j units, cell for cell
  (j = 1..100). Two generations reach two units, so what a unit becomes depends on a run of five, and all runs
  of five are in the ring: hence **every infinite sequence over {B, C} is an exact solution moving at one unit per
  2 generations**. `python3 verify_wall.py` (12 s) shows single walls and stretches of 1, 2, 3, 7 units on finite
  capped objects. Consequences: p< is one unit of B in wire C, and the left-going pulse of wire B is one unit of C in
  wire B; pulses can follow each other at any spacing; a wall B|C is a front that turns wire B into wire C at pulse
  speed (and C|B the reverse); the pair is a shift register of one bit per unit that reads out at one end. By the
  half-turn the same holds for B and C′ towards +v (not unit-aligned). [measured, `sg.Geom` only] What p> does to
  the tape is decided unit by unit: meeting a B unit at odd separation it erases that unit and goes on; at even
  separation it is swallowed and the unit stays (stretches of 1 to 4 units tried). The collision gate is the case
  of one unit. `python3 tapes.py` (1 s) tests all 120 pairs
  of the 16 unit types in this way: {B, C} is the only pair that moves; four pairs stand still whatever the order
  ({8, b}, {8, e}, {2, e}, {6, a}: binary strings that stay, [measured, `sg.step_set`]).
- **[proved by the oracle runs] Pulses that reach outside the tube.** Moving one cell of a unit of wire C
  outwards, (0,2,3) → (0,2,5), gives a second left-going 2-cell pulse, and its mirror image a second right-going
  one (`verify_pulse.py objects/pulse-C-wide-left.json`, `... pulse-C-wide.json`). (0,2,5) lies outside the wire's
  3 × 3 tube, which is why the searches of section 3 (closed tube) did not have them. They were first seen leaving
  chaos (section 13). [measured] They break both caps of the clock (the wire then burns away); nothing else about
  them is known.

## 11. The clock: a free-standing oscillator of period 4N + 2 for every N

- **The object** (`objects/clock-C.json`). capL (16 cells), N units of wire C, capR (16 cells): 32 + 5N cells in
  empty space, stationary (period 2). capR is state 27 of `scatter_table.py 28 31`; capL is its mirror image one
  generation on. **Lit by adding one cell** ((1,0,4) of the middle unit: a rake), it becomes an oscillator.
- **[proved by the oracle runs]** `python3 verify_clock.py objects/clock-C.json` (4 s): N = 1, 5, 16, 17, 30:
  after a transient the lit object first returns to itself after exactly 6, 22, 66, 70, 122 generations, and no
  cell is ever alive outside the diagonal hull of the unlit object. `... clock-C.json 1 2 3 4 5 6 7 8`: periods
  6, 10, .., 34. [measured, C stepper] `python3 clock_family.py 1 200` (7 s): period exactly 4N + 2 for every
  N from 1 to 200 (up to 802).
- **How it works** (`python3 show_clock.py 12` draws it). The rake runs to capR laying a train of p< behind it;
  capR turns it into the mirror rake, which runs back laying a train of p>; capL turns it again. Each cap swallows
  the train aimed at it, one pulse every 4 generations, and is as it was after each. So the wire is always full:
  behind the rake its own train, ahead of it the tail of the previous one. Travel 2N generations each way, 2 for
  the two turns. Half a period later the clock is its own mirror image [measured, N = 5, 12, 13].
- **[proved, computer-assisted; Claim A also enumerated by the second review's own script for j ≤ 150] A clock of
  period exactly 4N + 2 exists for every N ≥ 1.**
  `python3 prove_clock.py 8 4` (1 s; also passes with bases 12 and 20). N ≤ 8 is the oracle run above. For
  N = N0 + j with N0 = 8 the cycle is built from the cycle X(s) of the base clock (period p = 4N0 + 2, computed
  by the oracle) by cutting the wire at unit m = 4 and inserting j units. Write S|[a,b] for the cells of S in units
  a..b and τ for the move by one unit. A cell's neighbours lie in its own unit or the next ones, so step(S)|[a,b]
  depends only on S|[a−1,b+1]. With tR, tL the generations at which the two rakes pass unit m, ta between tR and
  tL and tb between tL and the next tR, the script checks on the base:
  B1 τ(X(s−2)|[m−1,m]) = X(s)|[m,m+1] for tb−p−3 ≤ s ≤ ta; B2 τ(X(s+2)|[m−1,m]) = X(s)|[m,m+1] for
  ta−3 ≤ s ≤ tb; B3 X(ta+1) = X(ta−3) on units ≤ m+1; B4 X(tb+1) = X(tb−3) on units ≥ m−1; B5 the strip
  [m−1,m+1] looks as it does at tR only once per period. The new cycle shows, at unit m+i (0 ≤ i ≤ j), the base's
  unit m at base time c_i(t): c_i(t) = t − 2i until it reaches ta; then ta−3, ta−2, ta−1, ta repeated j−i times; then
  on by ones until tb; then tb−3, .., tb repeated i times; then on (period p + 4j). Units below m follow c_0 and units
  above m+j follow c_j. Two things make this an orbit. (A) Neighbouring charts agree where they overlap: at every
  t, (c_i, c_{i+1}) is (s, s−2) with s in the range of B1 or (s, s+2) with s in the range of B2. The cases, in
  order of t: both running before ta (s, s−2); i has looped back and i+1 has not, two generations (s, s+2 with
  s = ta−3, ta−2); both looping (difference ±2, s in [ta−3, ta], covered by both); i+1 has left the loop, i in its
  last two steps (s, s+2 with s = ta−1, ta); both running towards tb (s, s+2); i+1 has looped back at tb (s, s−2
  with s = tb−1, tb, which B1 covers one period earlier); both looping at tb (±2); i has left (s, s−2 with
  s = tb+1, tb+2). The script also enumerates all pairs for j ≤ 40. (B) A chart's time advances by one except at
  a loop-back, where B3 or B4 says the two base states agree on the units that chart supplies. Hence, by the light
  cone, the step of the assembled state at unit m+i is the step of the base at unit m: the assembled sequence is
  an orbit of period p + 4j, and by B5 of no smaller period. For j = 1..6 the script also builds the sequence and
  steps it, and checks that the clock lit by one cell falls into exactly this orbit.
  What is **not** proved: that the one-cell ignition leads into the cycle for every N (measured for N ≤ 200); the
  proof gives the cycle itself for every N.
- **[measured, second review]** The lit clock enters its cycle after exactly max(N − 2, 0) generations (oracle at 14
  values of N up to 257; the reviewer's stepper to N = 400). Any of about two cells per unit lights it, not only
  (1,0,4) of the middle unit; other single added cells heal, or give still lifes or small periods (3 to 6, 12).
- **Open problem 12** (periods beyond 66) is thereby answered by a family: every period 4N + 2, i.e. every
  period ≡ 2 mod 4 from 6 up, by one construction.
- **[measured] Other caps** (`python3 clocks.py ../scratch/signals/table_28_31.json`, 1 min; `... table_28_33.json`,
  5 min): with capL kept, 33 of the 1,493 cap states at C = 31 and 237 of 7,646 at C = 33 give shuttle clocks, the
  smallest capR 11 cells. **All have period 4N + 2**; none 4N + c with another c. A clock of period ≡ 0 mod 4
  from this mechanism was not found, and no reason is known.

## 12. Pulse-carrying wires are born from random soup

- **[measured]** `python3 soupwires.py 20000` (7 s; seed 1): 100,000 soups of density 0.4 on rings of 1, 2, 3, 4,
  6 units of the closed 3 × 3 tube; 12,780 settle into a wire of period ≤ 2 that is the same in every unit; 366
  different ones (up to phase). **Ten of them carry a 2-cell pulse in both directions, and were born in 279 soups**:
  four placements of wire B ≅ B′ in the tube (33 + 29 + 24 + 20 soups), four of wire C ≅ C′ (28 + 26 + 23 + 22), and two
  placements of a third wire of 5 cells per unit that is not in the family (37 + 37). So about one soup in 360, and
  one soup-born uniform wire in 46, is a pulse carrier. *(Corrected 2026-11-15, second review, own stepper, 100,000
  soups: by ring length the carriers came 284 from rings of one unit and 21 from rings of two, none from rings of
  3, 4 or 6 units (0 of 60,000). A ring of one unit is a random pattern of period one unit to begin with: what is
  shown is that random patterns of period one or two units settle into a carrier about once in 70; no soup without
  that imposed periodicity did.)* This qualifies the first push's guess that carriers are not attractors. Not seen: a pulse itself arising from soup (the settled rings here are uniform by selection; the 875
  wires of section 2 gave none).
- **Grown or placed?** A wire cannot grow into empty space (section 4). But wire C can be made out of wire B: a
  wall B|C runs along wire B at pulse speed and leaves wire C behind it (section 10, the tape), and a plain cut in
  wire B starts such walls on both sides: `python3 chaoswire.py show 1 --wire B --soup gap --T 160` [measured].

## 13. A wire against living chaos (the owner's note of 2026-11-15)

`chaoswire.py`. The chaos is a block of random soup (density 0.4; 1,854 cells: a piece 12 units long of an 11 × 11 tube round the wire, whose own tube is 3 × 3).
Alone, such a block is still not periodic after 20,000 generations in 12 of 12 runs
(`python3 chaoswire.py life 12 --T 20000`, 1 min), and it never leaves its planes (T2).

- **[measured] A wire that runs through the chaos is destroyed, every time, at pulse speed** *(at density 0.4;
  second review: for wire B at every density tried, but wire C at densities 0.1 to 0.2 mostly burns at 4 generations
  per unit)*.
  `python3 chaoswire.py out 100 --wire W --soup S --quiet` (1 min each; a capped wire of 520 units through the
  block; probes 40 and 80 units from the block on both sides; 400 generations):

  | wire | soup | sides on which a front reached the far probe and the wire was not bare afterwards | speed | something clean passed the far probe before the front |
  |---|---|---|---|---|
  | C | everywhere in the block (the wire inside it is soup too) | 200 of 200 | 2 generations per unit in 199, 4 in 1 | 15: on the −v side the pulse p< 7 times, one other; on the +v side the wide pulse 4 times, p> once, 2 others |
  | C | round an unbroken wire | 200 of 200 | 2 in 199, 4 in 1 | 18: on the −v side the wide pulse, singly or in trains, 10 times; on the +v side the wide pulse 6 times, p> once, one other |
  | B | everywhere | 200 of 200 | 2 in 200 | 0 |
  | B | round an unbroken wire | 200 of 200 | 2 in 200 | 0 |

  The front runs at exactly the speed of a pulse, so nothing sent later can overtake it, and behind it is ash,
  different from run to run, mostly reaching outside the wire's own tube. In wire B the leading edge is usually the
  wall of section 10 turning B into C (or C′), with the ash following. Controls without soup (`--soup gap`: the
  wire merely cut, 12 units missing): wire C burns away to nothing at 4 generations per unit; wire B is converted by
  walls at 2 generations per unit and the converted wire then burns away at 4.
- **[measured] Chaos does make pulses**, about once in 12 sides for wire C (33 of 400): a clean p<, p> or wide
  pulse leaves the chaos and the wire behind it is bare for at least 6 generations. But the front follows at the
  same speed, a fixed distance behind. (Identified by the masks they show at the probe; two runs, seeds 17 and 45
  of the second row, were cut out and gave the wide pulse of section 10.) These are the first pulses in this study
  that arose from anything random.
- **[measured] A capped end beside the chaos** (`python3 chaoswire.py cap 40 --gap G --T 3000 --L 200 --quiet`, 1 min each; wire C
  ending in capL of the clock; the soup, 200 generations old, ends G empty diagonal layers short of the planes that
  bound the cap; 3,000 generations): G = 0 and G = 1: the cap is destroyed in 40 of 40 runs, the wire first changes
  22 to 60 generations after the start, and then burns away to nothing at 4 generations per unit. G = 2: nothing,
  40 of 40.
- **[proved] The isolation is exact.** G = 3 or more: T3 of `docs/AUTOMATON.md` (three dead layers are a firewall).
  G = 2 in this geometry: the script counts the cells outside the block that have both a neighbour in the block and
  a live neighbour in (or are a cell of) the capped wire, at both phases: 2 cells, none of them live, and none can
  reach 4 live neighbours; so every cell outside the block sees what it would see with the wire alone, and each
  side runs as if the other were not there, for ever. With G = 1 there are 28 such cells and 2 can be born.
- *(Correction, 2026-11-15, second review, `research/audit/signals2/isolation.py`: the count above is exact for this
  capped end, but a wire running PAST a slab of chaos two empty layers off is struck at generation 2 in 20 of 20
  soups; at three layers never (T3). Two layers isolate the capped end of wire C; three isolate any wire.)*
- **What this says about the owner's isolation.** Between chaos and a wire there is no weak coupling to use: either
  the two are apart by enough empty layers (three in general, two for the capped end) and nothing passes, ever; or they touch and the wire is consumed
  at pulse speed. The chaos does not forget the wire's signal so much as eat the line. And the ordered remains
  carry *damage* out of the chaos' own hull as far as the wire goes, which nothing in the chaos itself can do (T2).
- **Not done**: a pulse sent into the chaos with the far side compared (there is no surviving far side to
  compare in any geometry tried); other wires, other densities and block shapes, blocks much larger or older; what
  the ashes are; whether some cap or some wider wire withstands contact.

## 14. Second push: not done, not checked, and where to go next

- **Not checked.** UNSAT answers of section 8 rest on my encoding and on CaDiCaL alone (models always re-step).
  Caps were only looked for with period 2 and inside the wire's own 3 × 3 tube. That the one-cell ignition of the
  clock leads into its cycle is measured for N ≤ 200, not proved. Rake against rake, the mirror rake against p>,
  the static pairs of `tapes.py`, the cut-wire controls and everything in section 13 were stepped with `sg` only,
  not with the oracle. The scattering table at C = 33 covers the first 4,000 caps, not all.
- **Not found.** A corner between two wire directions; a closed polygon; a crossing; a gate with a third line; a
  stationary source of pulses; a same-side toggle; a clock of period ≡ 0 mod 4; a reflector for a single pulse.
- **Not touched** (the lead's item 6): the undecided rows of section 6, backgrounds of repeat 2, wider tubes,
  other directions, two-cell flips of the wires on file, the two sheets.
- **Where I would go next.** (1) The tape: what the right-going pulses and the rake do to a general B/C sequence
  (the collision gate is the one-unit case); with caps that read or write units this is a shift register with
  logic on it. (2) The wide pulses: their collisions with p>, p< and the rake, and caps for them, in a tube one
  size up; they show the 3 × 3 tube was too tight a search space. (3) A cap that turns the rake with one more or one
  less generation of delay (for period ≡ 0 mod 4): enumerate caps of period 2 at C = 35, or caps of period 4.
  (4) A corner: needs a search in a region where two tubes of different direction meet; nothing here bears on it.

# Third push (2026-11-15): a machine made of parts

The lead's six items, where each stands: (1) a periodic emitter: **not found**; reduced to a precise question (a
*writer* at the end of the tape, section 15) and excluded in several bounded classes (section 16). (2) clock drives
counter: **not reached** (no emitter); the counting part exists: the 8|C wall counts pulses p< arriving in a train
(section 17). (3) a corner: **not found**; a side-kick scan in all six directions found nothing (section 16).
(4) period ≡ 0 mod 4: **not found, but located**: the period of a shuttle clock is fixed mod 4 by a turn class of
each cap [proved]; inside the 3 × 3 tube every periodic cap that turns the rake has the same class (exhaustive SAT
within bounds), and in the 5 × 5 tube a stationary cap that turns the rake once with the other class, and is destroyed
doing it, exists (section 18; corrected after the third review).
(5) the tape as memory: **capL of the clock eats every word, exactly, and remembers nothing (proved)**; every left
cap in the census either does the same or disturbs the tape (section 17). (6) a wider search space: touched only
(writers and turns in the 5 × 5 tube, section 16, 18).

## 15. The tape at its two ends: readers and writers

By the tape theorem (section 10) wire C with left-going pulses on it is a word over {B, C} moving rigidly towards
−v, one unit per 2 generations. At an even generation unit u holds a B unit or a C unit; at the odd generation
between, unit u holds the odd phase of its own letter (B: (0,0,1) (0,0,5) (0,1,2) (0,1,4) (1,2,2); C: the same with
(0,0,3) for (0,0,5)) [proved: `python3 sat_writer.py --selftest`, 1 s, 50 random words, and the light cone]. So
everything to the left of whatever sits at the +v end of a tape is fixed by the word that end has *written*, and the
−v end of a tape is a *reader*: it receives one letter every 2 generations, whatever it does with it.

- A right cap of wire C (capR of the clock, the 17-cell and 14-cell caps found by `sat_writer.py 2 31 --word C`,
  `... --word B`) writes CCCC… or BBBB…. **A periodic emitter (gun) at the +v end whose output is a train of p< inside
  the 3 × 3 tube is exactly a writer whose word is periodic and not constant**: a state of period T needs a word of
  period T/2. *(Qualified 2026-11-15 after the third review: the equivalence, and so the negatives of section 16, do
  not cover emitters of the wide pulses of section 10 or of anything reaching outside the 3 × 3 tube; emitters whose
  output is a moving object that is not a letter (a mirror rake sent from a +v end, a rake from a −v end, the
  composites `9fb7bf`, `9d…df` of section 17); word periods of 5 or more; emitters beside a wire or in its middle
  (two-sided: section 21); and emitters whose junction disturbs the two units in front of the search region.)* `sat_writer.py T C` searches for one
  directly: T/2 letter variables, the tape units as literals of them, the writer free inside the tube and the planes
  (exact on the infinite lattice by T2 and the tape theorem; models are re-stepped). The other end and the other
  direction are the same problem up to the half-turn and the mirror of section 9.
- **[proved; `python3 prove_reader.py`, 0.3 s] capL of the clock eats every word and remembers nothing.** Closing the
  automaton whose state is the cells of units ≤ 3 at even generations (input: the next letters; a cell's neighbours
  lie in its own unit and the adjacent ones, so 2 generations need 2 more units of tape), the closed set is exactly
  the 16 states "capL + a pure word on units 0..3": at every even generation, for every word, the state is capL and
  the tape moved on, cell for cell. capL is a perfect sink. Same result with U = 4.
  **[oracle] `python3 verify_reader.py`** (12 words of 40 units including all-B, (BC), (BBC) and random words of
  density 0.1 to 0.9, capR at the other end; 30 s): at every even generation the state is exactly
  capL + the word moved on + capR, until the bare clock remains. (`--N 30 --words 8`: 8 s.)
- **[proved within the bounds; `python3 readers.py TABLE.json`] Every left cap in the census is a perfect sink or
  disturbs the tape.** Left caps are the mirror images of the right caps of `scatter_table.py 28 C` (the mirror
  maps wire + right cap, one generation on, onto left cap + wire; it turns clock-C's capR into its capL exactly).
  Classified by the same automaton (units ≤ 3, every word at once): C = 29: 17 sinks, 117 that for some word
  disturb the tape beyond unit 3 (they send something back, grow or move towards the tape, or burn); C = 31: 126 and
  1,367; C = 33 (all 7,646 table states): 702 and 6,944. **No left cap has a memory**: none whose state is changed by
  what it eats while the tape beyond it stays clean (with U = 6 at C = 29, and with words restricted to trains of
  single pulses, `--nobb`, at C = 29 and 31, the same). 8 s, 90 s, about 8 min. So in these bounds a cap at the end
  of the tape can forget or react, not record; the only recorders known are walls that move (section 17).

## 16. Searched for an emitter, a corner and a two-sided turner: absent within these bounds

- **[proved within the bounds; CaDiCaL 1.5.3, models re-stepped] No writer of small period.** `python3 sat_writer.py
  T C` (3 × 3 tube, writer free on units ≥ 6 inside the planes): UNSAT for T = 4, 6, 8 at C = 29 (33 free cells;
  0 s, 5 s, 47 s), T = 4, 6 at C = 31 (40 cells; 1 s, 51 s), T = 4, 6 at C = 33 (47 cells; 1 s, 210 s), T = 4 at
  C = 35 (54 cells; 1 s). "T" means every period dividing T, every non-constant word, so word periods 2, 3, 4 only
  (third review; its fixed-cap controls of the encoding pass: `research/audit/signals3/sat_controls.py`). Not finished: T = 8 at C = 31
  (more than 30 min), T = 4 in the 5 × 5 tube (`--lo -1 --hi 7`) at C = 29 (more than 10 min). The clock is 32 + 5N
  cells with period 4N + 2, so a gun made from a clock would have T ≥ 10 and far more cells: these bounds exclude
  small guns, not clock-sized ones.
- **[measured, sg.Geom] No back-to-back gun with clock-C's capL.** `python3 backtoback.py
  ../scratch/signals/table_28_31.json --gaps -9 -8 -7 -6 -5 -4 -3 -2` (9 min): each of the 1,493 cap states as the
  right end of a long tape, facing capL of a lit clock (N = 5) across gaps of −9 to −2 units: 8,184 arrangements are
  stationary unlit; in none does the turning rake make the facing cap write a letter (12 periods); in 15 the tape
  is disturbed. Reason in part: the lit clock never has a live cell outside the diagonal hull of the unlit one
  (`verify_clock.py`, check C), so it can reach its neighbour only through the few cells at the touching planes.
- **[measured, sg.step_set] No side kick.** `python3 sidekick.py --wire B` and `--wire C` (about 25 min each): a
  second wire (B or C) in every one of its 48 orientations (all six face diagonals) and every even translation that
  brings it within a neighbour step of the lit clock (N = 3) without sharing a cell: 2,751 and 2,874 placements,
  150 and 55 of them stationary unlit, and only those 205 were then lit (third review); **in none of the 205 does
  anything travel out along the second wire** within 3 periods.
  This is also the first search for a corner of any kind: none.
- **[measured, sg.Geom] No two-sided turner of the rake in wire C, in small sizes.** `python3 turners.py
  ../scratch/signals/defC.json` (90 s): the first 3,000 standing defects of wire C in 4 units of the closed tube
  (`sat_defects.py objects/pulse-C.json 2 0 --N 8 --lo 1 --hi 5 --max 3000`, 35 s; the list was cut, not
  exhausted), each hit by p<, p>, the rake and the mirror rake: none turns a rake and stays as it was (196 eat p<,
  725 eat p>; the rest change or burn). Walls V | (up to 3 arbitrary units) | C for the 11 family wires V: 344
  stationary, none turns the mirror rake and stays as it was (`python3 wallturn.py`, 90 s). Rake against
  the wall C|8 or 8|C: the rake does not turn; it becomes the head of a moving wall that turns wire C into wire 8 at
  pulse speed [measured]. A clock between a cap and a two-sided turner that passed its pulses on would be a gun; the
  turning objects known are all one-sided caps.
- Why a gun is hard here, as far as I can see: the only thing that emits is a moving rake; it is turned only by caps
  (one-sided objects); and the caps that turn it are perfect sinks for everything else that reaches them.

## 17. Counting: the 8|C wall counts a train of pulses

- **[proved by the oracle runs] `python3 verify_counter.py`** (2 s): on a ring of 48 units (box torus, `oracle.step`)
  with wire 8 on units 0..11 and wire C on the rest, trains of 1, 2, 5, 7 and 8 pulses p< at spacings 2 to 6:
  after 100 generations the state is exactly the ring with the wall moved one unit per pulse. (A control: two
  pulses one unit apart, i.e. the word BB, does not give the wall moved 2 units.) The third review's own oracle runs
  (`research/audit/signals3/counter_check.py`) confirm trains of up to 27 pulses and irregular spacings.
- **[measured, sg.Geom]** The stationary wall 8|C (wire 8 = the stators and (0,2,3) only, on the left; wire C
  on the right) hit by a train of p< at spacing s (`family.Piece`, 60 generations): for s = 2, 3, 4 the wall moves
  one unit towards the train per pulse and the wire is otherwise exactly as it was. *(Corrected after the third review,
  oracle:)* a run of n ≥ 2 adjacent pulses moves the wall one unit and is **reflected**: BB returns exactly one p>
  (exact, cell for cell); B^n returns a right-going object (`9fb7bf` for n = 3, `9d…df` with n − 2 units of B′ for
  n ≥ 4; kymographs only). So the 8|C wall is a stationary-in-kind reflector of double pulses (it moves one unit each
  time), not of single ones. Wire 8 is not free-standing: a cut end burns at one unit per generation, so the counter
  is shown on a ring only. So a gun of word period ≥ 2 feeding wire C into
  an 8|C wall would be a clock driving a counter, until the wall reaches the gun (the review of the first push saw
  the same end for the B|B′ counter: capacity d − 1). No cap for the free end of wire 8 was looked for. The rake against the wall: section 16.

## 18. Why every shuttle clock has period 4N + 2

- **[proved] The period of a shuttle clock mod 4 is the sum of two cap constants.** A rake f at unit u at an even
  generation t keeps a = t − 2u fixed; the mirror rake 5f ('5' at unit u) keeps b = t + 2u fixed. A cap that is the
  same at every even generation cannot tell the two classes a ≡ 0 and a ≡ 2 (mod 4) apart (the rake looks the same
  at every even generation), so a right cap that turns f into 5f has a turn constant k_R = b − a (mod 4) of its own;
  translating it one unit changes b − a by 4. Likewise a left cap has k_L = a − b. Round a clock a advances by its
  period P, so **P ≡ k_R + k_L (mod 4)**, and for clock-C the pair gives 2. Because the mirror (section 9) is a
  bijection between right and left caps, if every right cap that turns the rake has the same k, every clock has the
  same P mod 4. *(Convention and a gap, third review:)* every right cap measured has k_R = 0 and capL has k_L = 2 (the
  mirror shifts time by one generation, so the mirror image of a k = 0 right cap is a k = 2 left cap); a period-4N
  clock with capL needs a right cap with k_R = 2. And k is proved to be a constant of the cap for a **lone** rake; in a
  clock the rake arrives directly behind a p> train, where the same argument gives a constant that need not be the
  lone one. The two agree for clock-C and all 33 clock caps at C = 31 (measured, `research/audit/signals3/turn_check.py`).
  So the SAT negatives below bound lone turns, not clock turns.
- **[measured, sg.step_set] Every right cap measured turns the rake with k = 0.** `python3 turnclass.py
  ../scratch/signals/table_28_31.json ../scratch/signals/table_28_29.json` (8 min): a lone rake sent at each of the
  1,627 cap states of the two tables: 201 turn it, **all with k = 0**.
- **[proved within the bounds; CaDiCaL, positive control re-stepped] No period-2 cap turns a lone rake with k = 2.**
  `python3 sat_turn.py T C --KS 10` (`--KS 10` moves the cap 4 units on, so C = 47 here is C = 31 of the earlier
  sections): the rake, writing its tape behind it, starts at unit 9; the cap is free on units ≥ 10 inside the tube and
  the planes; at generation T the mirror rake must be at units 4, 5; unit 2 must be the rake's tape throughout (so
  the constants to the left are exact). Class k = 2 is T ≡ 0 mod 4 here. UNSAT for every T = 8, 12, .., 28 at
  C = 43, 45, 47, 49, 51 (26 to 54 free cells; under 3 s each), and T = 8 to 32 at C = 55, T = 8 to 28 at C = 59
  (68, 82 cells; up to 101 s). Class k = 0 is SAT at T = 14 (C ≥ 45) and T = 18 (C ≥ 49), and the caps returned
  turn a lone rake with k = 0 when re-stepped: the encoding finds the turns that exist. Also UNSAT: T = 8 to 28 at
  C = 63 (96 free cells, up to 103 s). **Caps of period 4 and 6** (`--zp 4`, `--zp 6`; such a cap can tell the two
  arrival classes apart, so the argument above does not apply to it): k = 2 UNSAT for T = 8 to 28 at C = 43, 47,
  51, 55 (period 4) and T = 12 to 24 at C = 47, 51 (period 6), up to 91 s each. **But with no cap condition at all**
  (`--zp 0`: any state whatever on units ≥ 10 at generation 0, not periodic) k = 2 turns exist (T = 16 and 20 at
  C = 47, SAT in seconds). So the class is forced by the cap's being periodic, not by the rake and the tape alone.
  So **within these bounds (the 3 × 3 tube) the turn class is forced, and no clock of this kind has period ≡ 0 mod
  4.**
- **[found by SAT, re-stepped with sg.step_set] In the 5 × 5 tube the other class exists.** `python3 sat_turn.py 16
  47 --KS 10 --lo -1 --hi 7` (150 s; T = 8, 12 UNSAT there): a period-2 right cap of 43 cells, reaching outside the
  3 × 3 tube (`objects/turn-k2-cap-5x5.json`), turns a lone rake with **k = 2** (re-stepped by `turnclass.right_turn`:
  k = 2). Put opposite capL of the clock it is not enough: for N = 3..12 the lit object settles (period 1 or 2), the
  cap does not survive the trains or the turn. `python3 k2caps.py T C` enumerates such caps and tries each in a
  clock: at T = 16, C = 47 (5 × 5 tube) **the list is complete at 8 caps** (23 to 44 cells; `python3 k2caps.py 16
  47`, 15 min, ends UNSAT): all 8 turn a lone rake with k = 2 when re-stepped and all 8 die in a clock with capL
  (N = 5, 6: the lit object settles to period 1). *(Third review, oracle, `research/audit/signals3/k2_oracle.py`:)*
  **all 8 are destroyed by the lone turn itself**: the cap and the wire behind the mirror rake burn, with no train
  and no clock involved; two of them (#2, #3) complete one round of 4N + 4 in a clock before dying. So no cap of class
  2 that survives a single turn is known in any tube. (`turnclass.py`'s "restored" flag, printed by `k2caps.py` as
  `(2, False, 64)`, is False for clock-C's own capR too: it compares the cap while p> pulses are still arriving and
  means nothing.) `sat_turn.py ... --eat Te` adds the condition
  that the cap also swallows a lone p> and is exactly restored Te generations later (positive control in the 3 × 3
  tube: `sat_turn.py 14 47 --KS 10 --eat 16`, SAT in 1 s, k = 0); the k = 2 instance with it in the 5 × 5 tube
  (`sat_turn.py 16 47 --KS 10 --lo -1 --hi 7 --eat 16`) had not answered after 11 minutes when this push ended.
  *(Deleted after the third review: "so the 3 × 3 tube was the obstruction to a period-4N clock, not the rake".
  Nothing shows that: the class-2 caps one size up self-destruct.)*
  What the 3 × 3 negative does not cover: caps of period 8 or more or of odd multiples beyond 6, turns in
  which the rake's tape in front of the mirror rake is altered by more than the last two positions (the guard),
  turns slower than T = 28 to 32, clocks whose shuttling object is not this rake. No reason for the forced class is
  known: it is a regularity of periodic caps inside the 3 × 3 tube (period 2, 4, 6 tested), not a theorem; one size up
  class-2 turns exist only as self-destroying ones (above). Section 20 removes the planes from this negative.

## 19. Third push: not done, not checked, and where to go next

- **Not checked.** Everything in sections 16 to 18 except the reader rests on `sg` steppers or on SAT (the encoding
  of `scat.py`, CaDiCaL only); only the reader (section 15) and the counter (section 17) have oracle verifiers. The SAT negatives are exhaustive
  inside their bounds only. The side-kick and back-to-back scans looked 3 and 12
  clock periods ahead and only at N = 3 and 5. `readers.py`'s "disturbs" lumps together caps that reflect, move,
  grow or burn.
- **Not found.** A periodic emitter; a clock that drives a counter; a corner; a period ≡ 0 mod 4; a left cap with a
  memory.
- **Where I would go next.** (1) The gun is now one precise SAT question, `sat_writer.py` with T ≥ 10 and bigger
  planes; the instances grow fast with T, so fix the word (e.g. `--word BCCCC`, a single pulse per 10 generations)
  and seed the writer with a clock's cap. (2) Explain k: the class may come from a parity of the rake's own cells
  at the moment it touches the cap; a proof would settle 4N + 2 for all caps of period 2. (3) **The closest thing to a new result: a period-4N shuttle clock.** It needs a 5 × 5-tube cap of class
  k = 2 that also eats the p> train and is restored after each turn; run `sat_turn.py 16 47 --KS 10 --lo -1 --hi 7
  --eat 16` to the end (and T = 20, C = 51), then `k2caps.py`-style clock tests, then the oracle (`verify_clock.py`
  takes capL/capR from a file). (3b) The k = 2 turns that exist
  without a periodic cap (`sat_turn.py 16 47 --KS 10 --zp 0`) are the place to look for the invariant: what do all
  periodic caps have that those starting states lack? Caps in the 5 × 5 tube are where a period-4N clock could
  still be. (4) A two-sided turner bigger
  than 4 units: `sat_defects.py` cut at 3,000 of an unknown total.

# Fourth push (2026-11-15): something standing writes onto a wire

The picture after three pushes was: pulses are emitted only by a moving rake, rakes are turned only by caps, and the
caps that turn them swallow everything else; nothing that stands still writes onto a wire. Where the brief's items
stand now. (1) An emitter: **a standing object that emits rakes exists** (the gun, section 20) and with a cap at the
far end it is an emitter and a receiver exchanging objects for ever, at any distance (the line, section 21, proved for
every length). What it emits is a rake every 4 generations, the densest possible stream. **A standing emitter of a
non-constant word exists as well** (the divider, section 21b): the line with a period-8
oscillator of the clockwork catalogue standing beside the wire, which turns every second rake into a hole and is
itself never changed; the wire beyond it carries one rake per 8 generations. The constraint searches for such an
object *inside* the tube were all negative (section 23). (2) A corner: not searched. (3) A period-4N shuttle clock: not found; the negative of section 18 now holds
for every period-2 right end of wire C in the 3 × 3 tube, of any length and shape, for turns with T ≤ 36
(section 18's T′ ≤ 28, not its T′ = 32), the guard included (section 22). The beam and the line are free-standing oscillators of period 4 of
every length, but they are not shuttle clocks. (4) A reason: none; the turn-class statement was strengthened, not
explained. (5) The clockwork catalogue against a wire: run as samples (sections 21b, 23): against a wire at rest
the oscillators that survive write nothing (some light a shuttle clock once); against the running stream one of
them is the divider.

How the gun was found. The third push put the emitter as a *writer*: a cap at the +v end of the B/C tape with a
periodic non-constant word. The tape is not the only thing that moves rigidly towards −v on wire C: a mirror rake
does, and so does a train of them. `sat_writer.py` with the tape replaced by a train of mirror rakes (`sat_gun.py`)
returned a gun in one second at the first plane position where one fits.

## 20. The gun: a standing emitter of rakes

- **[measured, C stepper, then exact by the lift] Rigid trains of rakes.** `python3 sat_gun.py --trains` (1 s): one
  mirror rake `5f` on a ring of L units of wire C. For even L = 2..12 the ring settles into a pattern that moves
  rigidly towards −v, one unit per 2 generations: `5f(9f)^(L/2−1)`, mirror rakes L units apart, each swallowing the
  p> train of the one in front of it (the parity rule of section 10 at even separation). For odd L the rake is stopped
  (odd separation). The same for the rake `f` towards +v: `fb(7b)^(L/2−1)`. A ring state unrolled is an exact solution
  of the infinite tube, so each train is an exact solution; `sat_gun.py` asserts the rigid shift cell for cell and
  re-steps the unrolled train with `sg.step_set` before using it. For L = 2 the train `(5f)^∞` is mirror rakes back to
  back: equally a wire of repeat 2 units and period 4.
- **The search** (`sat_gun.py PATTERN C`). As `sat_writer.py`: the train fills units < KS = 6 (unit u at generation t
  holds ring unit (u + t/2) mod L; constants, with units 4, 5 as variables tied to them); unknown are the cells of
  units ≥ 6 inside the 3 × 3 tube and the planes x+y−z, x−y−z ≤ C at generations 0..T−1, T = 2L, the successor of
  T−1 being 0. A model is an exact orbit of period T of the infinite lattice (T2 closes the tube and the planes; the
  train is exact): a bounded object at the +v end from which a mirror rake leaves every T generations. Control: the
  train `7b` is the tape word BC, and `sat_gun.py 7b 29`, `... 31` are UNSAT as `sat_writer.py 4 C` is.
- **[found by SAT; proved by the oracle run] The gun** (`objects/gun-5f.json`; `python3 sat_gun.py 5f 31`, 1 s).
  15 cells at generation 0 (15, 16, 15, 17 by phase), in units 0..2 beyond the wire's last unit, period 4.
  **`python3 verify_gun.py objects/gun-5f.json`** (3 s): Object(30) = capL of the clock + 30 units of **bare** wire
  C + the gun, nothing added. At generation 4j the state is, cell for cell, capL + bare wire + j mirror rakes on the
  2j units next to the gun + the gun as it was, for j = 0..12; the gun's own cells repeat every 4 generations and not
  every 2; no cell leaves the diagonal hull. So a standing object puts a moving object on bare wire once per period
  and returns exactly to its state: the first such thing in this study.
- **[proved within the bounds, CaDiCaL; every model re-stepped] Census** (`python3 sat_gun.py 5f C --all`, 1 to 7 s):
  guns of period dividing 4 for the train `(5f)^∞` inside the planes: C = 29: none; C = 31: exactly 1; C = 33: exactly
  1 (the same); C = 35: 6 solutions (15 to 22 cells), of which one is the C = 31
  gun and one is the C = 31 gun moved one unit towards +v and two generations on: at most four further guns
  (`python3 research/audit/signals4/census_translate.py`, REVIEW-signals-4 §2).
- **[measured, sg.step_set] Starting and stopping** (`python3 gunlab.py start`, 2 s): set against bare wire C, the
  gun in phase 0, 1 or 3 emits at once; in phase 2 it does not (it sheds a mark `77` and the end decays).
  `python3 gunlab.py capL` (1 s): with capL of the clock at the far end the rakes are not swallowed: capL turns them,
  they meet the stream, and capL + N units + gun settles to period 2 after about 6N + 20 generations (N = 1..20). So
  `gun-5f` alone is an emitter for as long as its wire lasts; the line of section 21 is the permanent form.
- **[by symmetry; kymograph `python3 gunlab.py mirror`] The mirror image** ((x,y,z) ↦ (z−4, y, x+4), section 9) is a
  left end that emits rakes `f` towards +v: the wire then reads `…??bfbfbfbf…`: wire C with ONE extra cell (the rake
  cell (1,0,4)) in every second unit, travelling.
- **What it is and what it is not.** It is a bounded standing object of period 4 on the end of bare wire C that
  emits one rake per period and is restored each time. It is not a source of *pulses*: what it emits is rakes at the
  highest rate there is, so no unit between them is left bare, and the stream `(5f)^∞` can equally be read as a
  second wire (repeat 2, period 4) of which the gun is a cap that is not stationary against wire C (the boundary
  between the two wires runs away from it at pulse speed). In the language of section 15 it writes the word 5, f, 5,
  f, …: not constant unit by unit, constant pair by pair. Whether that meets the lead's S16 ("puts at least ten
  pulses on an otherwise undisturbed wire") is a matter of wording that I leave open: ten rakes, yes; ten
  separated pulses on bare wire, no. What a *sparse* emitter would be is exact: a gun for `5f9f` (a rake every 8
  generations), or a standing object in the stream that lets every second rake through. Neither exists in the bounds
  of section 23; the second exists outside them (section 21b).

## 21. The line and the beam: emitter, wire and receiver in one object

- **[proved within the bounds; re-stepped] Absorbers** (`python3 sat_gun.py fb C --dir 1 [--all]`: the same search with
  the rake train `(fb)^∞` running *into* the cap): none at C = 27, 29; exactly 1 at C = 31 (16 cells); exactly 12
  at C = 33. **[measured, sg.step_set] Six ordinary caps on file become absorbers when the stream reaches them**
  (`python3 beamcaps.py ../scratch/signals/table_28_29.json`, under 2 min; `... table_28_31.json`, about 4 min: every
  cap state of the two scattering tables at the end of 4 and 5 units of bare wire beyond a running gun; 1,627
  states, two parities): state 8 at C = 29 and states 14, 21, 34, 488, 969 at C = 31 settle into period 4 with the
  gun alive, at both parities; of the other 3,242 runs 2,128 end at period 1, 1,067 at period 2, 11 at period 3, 22
  at period 4 with the gun dead, and none is a stream with a period above 4 (14 end with a period above 4: in 13 the
  gun is dead, and the fourteenth, period 40, is debris with the wire gone).
- **[proved by the oracle runs] The line** (`objects/line-C.json`; `python3 verify_line.py objects/line-C.json`, 8 s).
  capA (18 cells: the mirror image of state 8 above) + N units of bare wire C + the gun (15 cells), an object of
  33 + 5N cells in empty space, for N = 2, 3, 12, 13, 30: (A) capA with the clock's capR on the other end is
  stationary: it is a cap at rest; (B) the gun's cells repeat every 4 generations from generation 0 on, never
  disturbed; (C) at generation 4j the wire holds j mirror rakes and is otherwise bare; (D) from generation 2N on
  the whole state has period exactly 4, and not from generation 2N − 1; (E) nothing leaves the hull; (F) the pulse,
  below. One standing object sends, another receives, again and again, with any length of wire between: the
  literal form of open problem 13.
- **[proved; base facts on the oracle: `python3 prove_line.py`, 3 s] The line has period exactly 4 from generation
  2N on for every N ≥ 2.** N = 2..7: `python3 verify_line.py objects/line-C.json 2 3 4 5 6 7` (oracle, 2 s). For N ≥ 8, by
  induction. Write X_N(t) for the orbit of Object(N), τ for the move by one unit towards +v, and L_N(t) = X_N(t−2)
  for t ≥ 2, L_N(t) = X_N(t) for t = 0, 1. A cell's neighbours lie in its own unit and the two next to it, so one
  generation of unit u needs units u−1..u+1. Statement S(N, m), with 1 ≤ m ≤ N − 4:
  (P1) X_N has period 4 from generation 2N; (P2) for u = m, m+1 and every t ≥ 0, X_N(t) on unit u−1 moved by τ equals
  L_N(t) on unit u; (P3) X_N(2) = X_N(0) on units ≤ m+1. The script checks S(8, 3) on the oracle (P2 for
  t ≤ 2N + 12, which is enough since both sides have period 4 once t ≥ 2N + 2). Step: define Y(t) as L_N(t) on
  units ≤ m+1 and τX_N(t) on units ≥ m. The two agree on units m, m+1 by P2. Y(0) is Object(N+1) (capA and bare
  wire on the left, wire and the gun at unit N+1 on the right). Y obeys the rule at every unit: a unit ≤ m sees
  only units ≤ m+1, where Y = L_N, and L_N is an orbit there (for t ≥ 2 it is X_N delayed; from 0 to 1 it is X_N;
  from 1 to 2 by P3); a unit ≥ m+1 sees only units ≥ m, where Y = τX_N, an orbit. So Y = X_{N+1}. Then S(N+1, m+1):
  P1 because L_N(t) = X_N(t−2) is periodic for t ≥ 2N + 2 and so is τX_N(t), and the period is not 1 or 2 because
  the gun's own cells have period exactly 4 (`verify_line.py`, check B); P2 at u = m+1, m+2 lies in the right chart
  and reads τ(X_N(t) on unit u−2) = L_N(t) on unit u−1, which is P2 of S(N, m) at u−1; P3 on units ≤ m+1 is
  L_N(2) = L_N(0), and on unit m+2 it is P3 of S(N, m) moved by τ. The script also builds Y for N = 9..14 and
  finds it equal to the oracle's own run of Object(N) at every generation. In words: what crosses the middle of the
  wire is always a rigidly moving pattern (bare wire, then the front, then the train), so a longer wire only delays
  the far end.
- **[proved by the oracle runs] The beam** (`objects/beam-5f.json`; `python3 verify_beam.py objects/beam-5f.json`,
  12 s). The mirror-image gun on the left (14 cells), N units of rake train, the SAT absorber of C = 31 on the right
  (19 or 18 cells by the parity of N): 33 + 5N cells, period exactly 4 for N = 1, 2, 9, 24, 41, hull never left; one
  generation after the stored phase its N units are wire C with the rake cell in every second one and nothing else,
  and the pattern moves one unit per 2 generations from the gun to the absorber.
- **[proved; base facts on the oracle: `python3 prove_beam.py`, 1 s] The beam has period exactly 4 for every
  N ≥ 1.** N = 1..9: `python3 verify_beam.py objects/beam-5f.json 1 2 3 4 5 6 7 8 9` (oracle, 2 s). For N ≥ 10 by
  induction from N to N + 2, with τ² the move by two units towards +v. Statement S(N, m): (Q1) X_N(4) = X_N(0) and
  X_N(2) ≠ X_N(0); (Q2) for u = m, m + 1 and t = 0..3, X_N(t) on unit u − 2 moved by τ² equals X_N(t) on unit u (the
  middle is the rake train, which repeats every two units); (Q3) `left` lies in units < m − 2 and the right end in
  units > m + 1. Step: Y(t) = X_N(t) on units ≤ m + 1 and τ²X_N(t) on units ≥ m. The charts agree on units m, m + 1
  by Q2; each unit sees only its two neighbours, so Y obeys the rule in both charts; Y(0) is Object(N + 2) by Q3
  (the train units alternate, so the move by two keeps them in place, and the right end keeps its parity). So
  Y = X_{N+2}, with period 4 and not 2, and S(N + 2, m) holds (Q2 in the left chart is Q2 of X_N). The script
  checks S(8, 4) and S(9, 4) on the oracle and, as a test the proof does not need, that Y is the oracle's own orbit
  of Object(N) for N = 10..15.
- **[proved by the oracle runs for one pulse; measured for words] The stream carries one-cell pulses.** Remove the
  rake cell (1,0,4) of one rake of the beam: at every second generation from then on the state differs from the
  undisturbed one in exactly ONE cell (the cell (0,2,3) of the unit where a rake should be: that unit is a B unit),
  moving with the rakes; the absorber swallows it and the object is then identical to the undisturbed one, cell
  for cell (`verify_beam.py` check D: N = 24, 41; `verify_line.py` check F on the line, where the pulse is one cell
  at odd generations: N = 12, 13, 30). **Every set of holes heals** on the beam as long as the rake next to the gun
  (unit 0, part of the gun's own state) is left alone, and on the line without condition (`python3 gunlab.py words`,
  45 s: 200 random sets; exhaustively, `python3 research/audit/signals4/holes.py beam 25`: all 4,096 words on the
  beam N = 25 that keep the first rake heal exactly, all 4,096 that remove it change the gun;
  `python3 research/audit/signals4/holes2.py line 16`: all 764 words on the line N = 16 heal, the rake next to the
  gun included). So the stream is a carrier on which a hole is a bit: written by one flipped cell anywhere along it,
  carried to the receiving end at one unit per 2 generations, swallowed there, the whole object restored. Compare
  the transmission of the first push (row L2): there each shot cost one cube of wire at the receiver.
- **What this is not.** The gun writes only the constant stream; what writes holes is in section 21b. The receiving
  cap has no memory of what it swallows (it is restored exactly), so nothing reads the holes either. And both ends
  are needed: the gun's stream on bare wire with nothing to swallow it runs on as a front.

## 21b. The divider: a standing emitter of a non-constant word

- **[proved by the oracle runs] `python3 verify_divider.py objects/divider-C8.json`** (7 s; N = 12, 13, 16, 17, 24;
  also run with N = 8..11, 14, 15, 18..23, 30, 41: all pass, check F being empty at N = 8). Object(N) is the line
  (capA + N units of bare wire C + the gun) and the oscillator **C8.24a** of the clockwork catalogue (24 cells,
  period 8; `research/clockwork/objects/C8.24a.cells`) standing beside the wire at units N − 4 .. N − 2, two
  diagonal layers outside the wire's tube (its cells have x + y + z ≥ 9; the tube is x + y + z ≤ 5): 117 cells at
  N = 12. (A) The oscillator alone has period exactly 8. (B) Its eight phases lie outside the tubes 1 ≤ x+y+z,
  x−y+z ≤ 7 and at generation 0 touch no cell or neighbour of a cell of the line. (C) **In the object, at every
  generation, the live cells inside the support of the free oscillator are exactly the free oscillator's cells of
  that phase: it is never changed.** (D) The gun repeats every 4 generations and not every 2, from generation 0:
  never disturbed. (E) The whole state has period exactly 8 from generation 2N − 3 on, and not from 2N − 4. (F)
  **The word:** at every even generation the wire units between capA and the oscillator read `5f9f5f9f…`, cell
  for cell, moving one unit per 2 generations towards −v, while the two units next to the gun read `5f` every 4
  generations: every second rake that passes the oscillator has become a hole. (G) Without the oscillator the
  object is the line, period 4. (H) Nothing leaves the hull.
- **[proved; base facts on the oracle: `python3 prove_divider.py`, 5 s] Period exactly 8 from generation 2N − 3
  for every N ≥ 8** (and from N = 3 by direct runs, `python3 research/audit/signals4/scan_N.py divider 1 60`). N = 8..13 directly (`python3 verify_divider.py objects/divider-C8.json 8 9 10 11 12 13`); for
  N ≥ 14 by the induction of the line (section 21) with 8 for 4: the oscillator and the gun are carried in the right
  chart τX_N(t), the left chart is X_N(t − 2), and the window lies in the stretch of wire between capA and the
  oscillator, where the train moves rigidly. The script checks S(14, 3) (P1: period exactly 8 from 2N − 3; P2 for
  t ≤ 2N + 20; P3, and that the oscillator lies to the right of the window) and, as a test, that the glued orbit is
  the oracle's own for N = 15..20. The period is not 4 because the oscillator's cells have period exactly 8.
- **What it is.** A bounded standing object that puts a periodic non-constant word on a wire, one mirror rake per
  8 generations with a hole between (the train `5f9f` of section 20), and is exactly as it was after each period;
  the far cap swallows the word and is restored. The action is one-way in the undisturbed orbit: the oscillator changes the
  wire and nothing on the wire changes the oscillator (check C); holes arriving in the stream pass and the object is
  restored, but one cell removed from the rake at the stroke site one generation before the stroke destroys
  oscillator and gun (`python3 research/audit/signals4/hole_oracle.py`, oracle). It is the positive answer to the two searches of section
  23 that came back empty, the gun for `5f9f` and the divider inside the tube: the object that does it stands
  outside the 5 × 5 tube, where neither search looked. For the lead's S16 ("pulses on an otherwise undisturbed
  wire"): between two rakes the wire holds the letter `9f`, which is what a mirror rake always leaves behind it
  (`sat_gun.py --trains`), not bare wire.
- **[measured, sg.step_set] Place and phase.** The oscillator can stand anywhere along the wire. With the wire bare
  at the start and the oscillator moved j units from the stored place (N = 12, 13, 16, 17, every j with the
  oscillator between unit 3 and the gun, all 8 phases; 47 s; no command recorded; a re-run:
  `python3 research/audit/signals4/c824b_bare.py 16`): at its four odd phases nothing happens to the stream
  (period 8 from generation 2N: the line with an oscillator beside it); among the four even phases exactly one
  gives the divider, phase ≡ 2j mod 8 with j the shift from the stored place (the formula 2(j − N) + 4 holds if j
  is the oscillator's highest unit), fixed by the distance to the gun (at shift +2, where the oscillator reaches the
  gun's unit, two phases work); at the other three the gun does
  not survive the start (not analysed).
- **[measured, sg.step_set] The stroke is one cell.** `python3 gunlab.py stroke` (1 s; N = 16): compare the object's
  next state with (its wire part stepped alone) + (the free oscillator stepped alone). They differ in one cell,
  once every 8 generations: (−5, 4, 10) in the gun's frame (unit N − 3, x + y + z = 9) is born, with three live
  neighbours in the oscillator and one in the wire, the cell (1, 2, 2) of that unit, born in the step from generation 8k + 7 to 8k + 8. Everything
  that follows is the wire's own dynamics with that one extra cell: one generation later the wire cell is gone and
  the rake that was passing goes on as a hole. The period of the stroke is twice the period of the stream, hence
  every second rake.
- **[measured, sg.step_set] How it was found.** `python3 clockstream.py --K 150` (5 min): the 99 catalogue
  oscillators, phase 0, 150 random placements each (seed 1) beside units 4..7 of the line with N = 12 already in
  its cycle: 14,850 runs of five periods. 10,383 untouched; in 4,208 the oscillator is lost; 259 kept, of which in
  223 the gun is dead in the final cycle, in 34 the stream is the plain one downstream, and in **2** it is
  modulated: C8.24a (this object) and C8.24b (also period 8, 24 cells; the same train `5f9f`; in the scan over
  places and phases from bare wire it gives the divider only when it stands next to the gun; put beside the running
  line it is a divider at units N − 6, N − 5 for N = 10..30, on a stepper checked against the oracle and on the
  oracle cell for cell at N = 12, 13: `python3 research/audit/signals4/c824b.py --oracle`). With a
  random phase as well (`python3 clockstream.py --K 400 --seed 2 --anyphase --minutes 22`, 22 min, which reached
  88 of the 99, and `... --first 88` for the other eleven, 3 min): 39,600 runs, 27,775 untouched, 11,172 lost, 653
  kept (gun dead 542, stream plain 107, stream stopped at the oscillator with the gun alive 2), and the stream
  modulated in **2**, both C8.24a again in other placements, both with period 8. So among 54,450 sampled
  placements of 99 oscillators the only word written is "rake, hole", and only the two 24-cell oscillators of
  period 8 write it. Not covered: the placements not drawn, places other than units 4..7 of N = 12, oscillators
  above period 52.

## 22. Rake turns without bounding planes, and turners with wire on both sides

`sat_two.py` is `sat_turn.py` with the planes removed. Same set-up: a lone rake at unit 5 at generation 0 with its
tape behind it, the guard at unit 2, the mirror rake `5f` exactly at units 4, 5 at generation T, class
k = (T + 2) mod 4 here (KS = 6).

- **[proved, computer-assisted: UNSAT by CaDiCaL 1.5.3, and by Glucose 4 for T ≤ 20] No right end of wire C of period
  2 in the 3 × 3 tube, of any length and shape, turns a lone rake with class 2 within T = 36 generations.** `python3
  sat_two.py T --open` for T = 4 (0 s), 8, 12, 16, 20, 24, 28, 32, 36: UNSAT in 0, 1, 6, 19, 43, 71, 221, 755 s (`--solver glucose4`:
  T = 8..20 in 0 to 4 s). "Within T": the rake is at unit u at generation 0, every unit up to u is bare wire in the
  end's own state, and the mirror rake `5f` is at units u − 1, u at generation T. Also for ends of period 4 (`--zp 4`: T = 8..20; 0, 3, 9, 47 s) and period 6 (`--zp 6`: T = 8, 12, 16;
  1, 16, 52 s). *What the instance is.* The end Z is free on units 6..U, U = T/2 + 6, and nothing is assumed beyond
  unit U: the rule is imposed, on Z and on the lit trajectory X, only at units ≤ U − 1; unit U of X is tied to Z
  while t ≤ U − 6 and is free afterwards; X = Z wherever the rake's influence (one unit per generation from unit 5)
  has not arrived. *Why UNSAT covers every end.* Let Z* be any state of period 2 of the infinite tube that is bare
  wire C on units < 6, and X* its orbit with the rake. Restricted to units ≤ U they satisfy every clause: the rule
  at units ≤ U − 1 reads only units ≤ U; X* = Z* outside the light cone; the remaining clauses are the turn itself.
  So if a turn of class 2 at T existed the instance would be SAT. (Every U gives a valid relaxation, so the following is not needed for the UNSAT direction.) *Why the far end cannot fake a turn.* Whatever
  unit U does after generation U − 5 needs U − 5 more generations to reach unit 5 and so arrives after T. *What a
  model would not prove.* The far end of a model need not continue; SAT here is not a construction (class 0 is SAT
  at T = 6, 10). Controls: with clock-C's capR fixed as the end, SAT at T = 6 exactly and UNSAT at T = 8..14; with
  the far end cut much nearer than the light cone class 2 becomes SAT, as it must (`--U 7` at T = 8, `--U 8` at
  T = 12, `--U 10` at T = 16, `--U 9` at T = 20).
  *What this covers that section 18 did not:* every plane position at once, caps longer than any plane tried, walls
  to other wires and anything else periodic on the far side. An end may begin with bare units, so the instance
  `sat_turn.py T' C --KS 10` of section 18 (rake at unit 9, mirror rake at units 4, 5 at T') is the case of four
  bare units and T = T' + 8 here: T ≤ 36 contains section 18's T' ≤ 28 for every C, and not its T' = 32 (that one
  stays a negative within its planes). What it does not cover: turns slower than that, the 5 × 5 tube, the guard (a
  turn that alters the tape two units ahead of the mirror rake), a rake arriving behind a p> train as in a clock
  (third review), periods other than 2, 4, 6.
  No reason is known, and the refutation is not local to the wire's end, nor does it need the whole light cone: at
  T = 16 (light cone to unit 14) the instance is UNSAT with the far end cut at unit 11, 12 or 13 and SAT with it at
  unit 10; at T = 8 (unit 10) UNSAT at 8, 9 and SAT at 7; at T = 12 (unit 12) UNSAT at 9 and SAT at 8.
- **[found by SAT; proved by the oracle run] Turners with wire on both sides exist** (`python3 sat_two.py 6 --w 3
  --all`, 30 s: an object free on 3 units, wire C on both sides in the same phase, the turn only). The list is complete at 20 objects
  (re-stepped, `sg.step_set`): 5 turn the rake, swallow the p> train that follows and are restored; 4 are stretches
  of wire 8, where the rake becomes the head of a moving wall (section 16); 1 turns wire C into wire C′ behind the
  mirror rake; 8 burn (the wire is eaten on both sides); 2 are the splitter below. With 4 free units more than 188 (the list was
  cut after 4 minutes; 44 of them restored turners). **`python3 verify_clock.py objects/clock-C-tail.json`** (5 s):
  one of the five (11 cells in 3 units, found by `sat_two.py 6 --w 3 --restore 10`) in place of the clock's right
  cap, with 6 units of wire C and a cap behind it: unlit stationary; lit, period exactly 4N + 2 for N = 3, 5, 8, 16.
  The third push's shooting test (3,000 defects in 4 units, a cut list) had found no two-sided turner.
- **[proved within the bounds; CaDiCaL] None of them leaks.** `python3 two_batch.py emit --T 6 10 14 --w 2 3 4 --dT
  2 4 6 8 12 --V b 7 d e 8` (about 12 min): an object free on w units between wire C and wire V (C, B, B′, C′, 8),
  the far wire V in the one phase relative to wire C that `wire_phases` gives, a lone rake turned at T, the object and the first unit of the far wire exactly restored at T + dT, and the far
  wire not bare anywhere beyond at that moment: UNSAT in all 225 instances (also w = 5, V = C, T = 6, dT = 2..8).
  In the complete list above every object that disturbs the far wire is itself destroyed. What this does not cover:
  an object that is restored only at other moments or never exactly (it swallows a p> every 4 generations), wider
  objects, the 5 × 5 tube, turns of a rake arriving behind a train.
- **[measured, sg.step_set] A splitter.** `python3 gunlab.py split`: the two units `a7` (family units, section 9)
  in wire C are a standing defect; a rake that hits them goes on as a pair of rakes `fbf` and a mirror rake comes
  back. One rake in, three out, the defect used up.
- **[proved within the bounds] Class 2 in the 5 × 5 tube with survival asked for.** `python3 two_batch.py restore
  --T 8 12 --w 2 --dT 2 4 6 --lo -1 --hi 7` (2 min): an object on 2 units of the 5 × 5 tube between wire C and wire
  C that turns a lone rake with class 2 and is exactly restored 2, 4 or 6 generations after the mirror rake is at
  units 4, 5: UNSAT, all six. Three units: not finished.
- **[proved within the bounds, by the complete list and a direct test with sg.step_set] The instance left running in
  section 18 is UNSAT.** `sat_turn.py 16 47 --KS 10 --lo -1 --hi 7 --eat 16` asks for one of the class-2 caps of
  T = 16, C = 47 that also swallows a lone p> and is restored 16 generations later. The list of those caps is
  complete at 8 (section 18), and `python3 eat_direct.py` (2 s) sends the same p> at each of the eight: none is
  restored at any generation up to 120; all eight are destroyed by the one pulse.

## 23. Looked for and not found, with bounds

- **[proved within the bounds] No gun for the train 5f9f in the 3 × 3 tube, small planes.** `python3 sat_gun.py 5fbb
  C` (the train `5f9f`: a mirror rake every 8 generations, period dividing 8): UNSAT at C = 29 (4 s), C = 31
  (131 s) and C = 33 (29 min). Positive control: `python3 sat_gun.py 5f5f 31` (the dense train with a repeat of
  4 units, T = 8) is SAT and returns the gun.
- **[proved within the bounds] No divider.** `python3 sat_div.py 5fbb 5f W` (a standing object on W units inside the
  stream, wire on both sides, no planes: the gun's train in on the right, the train `5f9f` out on the left, all four
  relative positions, the wire in the same phase on both sides, period 8): UNSAT for W = 1, 2, 3 (under 3 s each) and for W = 4 (287, 334, 312, 378 s for the
  four phases); the control `sat_div.py 5f 5f W` returns the train itself. In the 5 × 5 tube (`--lo -1 --hi 7`):
  UNSAT for W = 1 (under 1 s each) and W = 2 (184, 99, 117, 88 s). W = 5 and 5 × 5 with W = 3: not run. With the
  wire one generation out of step on the two sides (`python3 research/audit/signals4/sat_div_parity.py 5fbb 5f W`):
  UNSAT at all four shifts for W = 1..4 in the 3 × 3 tube (W = 4: 309, 324, 277, 283 s) and W = 1 in the 5 × 5 tube. These are
  negatives for objects *inside* the tube on W units; the divider of section 21b stands beside the wire, outside
  the 5 × 5 tube, on three units.
- **[not finished] A pulse gun in the 5 × 5 tube.** `python3 sat_gun.py 7b 29 --lo -1 --hi 7` (a writer of the word
  BC, a p< every 4 generations, in the 5 × 5 tube): no answer in 16 minutes. (The solver's own timeout does not
  fire inside pysat here; the runs were ended from outside.)
  (The train `5f9f` is the gun's stream with every second rake a hole: on the mirror-rake stream a hole reads `9f`
  where a rake reads `5f`. So the last two items are the searches for a standing writer of the word "rake, hole",
  at the end of the wire and inside the stream.)
- **[measured] No far end on file modulates the stream** (`beamcaps.py`, section 21): 1,627 cap states, none gives
  a stream of period above 4.
- **[measured, sg.step_set] No two-sided object on file survives in a stream.** `python3 gunlab.py obstacle
  ../scratch/signals/p4/two_6_3_b.json ../scratch/signals/p4/two_6_4_b.json` (75 s; the lists are written by
  `sat_two.py 6 --w 3 --all --out ...` and `--w 4 --all --minutes 4 --out ...`): each of the 208 two-sided objects
  of section 22 set (a) between the receiving cap and the gun, 1 to 8 units from the gun, and (b) between the
  mirror-image gun and a cap at rest, the same gaps; 3,328 runs to their final cycle. In none is a stream still
  running at the end. Final periods: 1 (1,563 runs), 2 (1,585), 4 (125), 6 (31), 3 and 5 (11), 8, 10, 12, 20, 24 (13):
  "running" means two rakes in a row on the wire at some even generation of the final cycle. The five long cycles
  looked at by hand are small rotors left where the gun stood, with the wire gone or turned into a different
  stationary wire (in one, object 161 at gap 4, a rotor of period 8 on three units); they are not clocks on a wire.
- **[measured, sg.step_set] Two guns facing each other destroy each other.** `python3 gunlab.py duel` (10 s): the gun
  and its mirror image across N = 0..40 units of bare wire, the four phase pairs of one wire parity (the other
  parity is the mirror image); control: the mirror-image gun alone emits rakes. All 164 settle to period 1 or 2.
- **[measured, sg.step_set] No absorber on file reads a hole.** `python3 gunlab.py readers
  ../scratch/signals/p4/abs8_fb_31.json ../scratch/signals/p4/abs4_fb_33.json` (2 min; the lists are written by
  `sat_gun.py fb 31 --dir 1 --mult 2 --all --out ...` and `sat_gun.py fb 33 --dir 1 --all --out ...`, 57 s and 7 s):
  the 13 absorbers of C = 31 and C = 33, each at the end of a long rake train, with ten words of holes (one rake
  removed, the first to the sixth from the absorber; two in a row; every second one of ten). Eleven absorbers heal
  exactly after every word. Two (numbers 5 and 8 of the C = 33 list, 21 and 22 cells) are destroyed by every word,
  a single hole included, and the wire burns after them. None is left alive in a different state: a hole is
  either forgotten or fatal.
- **[proved within the bounds] No end of period 8 at C = 31, receiving or emitting, and no receiving one at C = 33.** `python3 sat_gun.py fb 31
  --dir 1 --mult 2 --all` (57 s): the absorbers of period dividing 8 at C = 31 are the one of period 4 and no
  other; `python3 sat_gun.py 5f 31 --mult 2 --all` (35 s): the same for guns of the full stream. At C = 33
  (`sat_gun.py fb 33 --dir 1 --mult 2 --all`, 14 min) the absorbers of period dividing 8 are the twelve of period 4
  and no other. An absorber of period 8 would count the rakes it swallows mod 2.
- **[measured, sg.step_set] The emitting end has a stationary state too, and no single cell lights it.** `python3
  gunlab.py off` (12 s): the left end of the beam set against bare wire in the stored phase settles within 4
  generations into a stationary cap of 12 cells. Of 327 one-cell flips of it and of the first 8 units of its wire,
  159 heal and 168 do something else; none starts the stream. (The gun of `gun-5f.json` needs nothing: in three
  of its four phases it starts against bare wire.)
- **[measured, sg.step_set; a sample] The clockwork catalogue against a wire: an oscillator that survives does not
  write.** `python3 clockscan.py --K 120 --zone end --out E.jsonl` (3 min) and `--zone side --out S.jsonl` (4 min),
  then `python3 clockscan.py --cycles E.jsonl` (20 s) and `... S.jsonl` (30 s). The 99 oscillators of
  `research/clockwork/objects/C*.cells` (periods 8 to 52), phase 0, each in 120 random placements (a lattice
  symmetry and an even translation; seed 1) that touch a 12-unit wire C between two caps at rest, either at its
  right cap and last two units ("end") or at units 4..7 from the side ("side"), and nothing else: 23,760 runs of
  five periods. End: 5,977 leave no trace at multiples of the period, in 5,738 the oscillator is lost, in 165 it is
  still there after five periods beside a changed target. Side: 7,704, 3,980 and 196. All 361 were followed to
  their final cycle, and in all of them the oscillator is still there. In 306 the wire is static or gone. In 52 a
  **shuttle clock** is running: the placement lit a rake once, as one flipped cell does, and the clock then runs
  beside the oscillator, between a cap and, in the side zone, a wall that the collision left across the wire
  (on either side of it; in the two cases looked at by hand the far part of the wire had become wire B′). Everything outside the oscillator's support then has the clock's
  own period (46 or 50 at the end; 18, 22, 26, 30 at the side: 4N + 2 every time) and the whole has the least
  common multiple (e.g. 550 = lcm(22, 50)). The other three: two wire units beside C18.28c breathe with its
  period 18 and nothing leaves them; two are period-6 debris on a burnt wire. **No letter per period, no wall moved
  per period.** Not covered: the other phases of each oscillator, the placements not drawn (120 of some 10⁴ per
  oscillator and zone: the full list for each of the first five oscillators at the end has 16,000 to 19,000), a
  counter wall as the target, oscillators above period 52. Against the gun's running stream the same catalogue
  gives the divider (section 21b).
- Not run at all: any corner search, the writer search at T ≥ 10, the period-4N clock as a periodic orbit.

## 24. Fourth push: not checked

- The UNSAT answers rest on the encodings (`scat.Problem`, used unchanged; the new regions and trains are in
  `sat_two.py`, `sat_gun.py`, `sat_div.py`) and on CaDiCaL, with Glucose agreeing where stated. Every model
  reported was re-stepped; the objects in `objects/` have oracle verifiers. No proof certificates.
- The divider is verified on the oracle for N = 8..24, 30 and 41 and proved for every N ≥ 8 given the gluing
  argument; that the wire reads `5f9f` (check F) is verified at those N only. Its place-and-phase table, the
  second oscillator C8.24b and the scan that found them are `sg.step_set` only.
- `prove_line.py` and `prove_beam.py` prove the cycles for every N given the inductions of section 21 (a second
  reader should check the two gluing arguments; the base facts are oracle runs). That every word of holes heals
  is measured (200 words), not proved; a closed automaton as in `prove_reader.py` would do it.
- Everything `gunlab.py`, `beamcaps.py`, `clockscan.py`, `clockstream.py` and `eat_direct.py` report is
  `sg.step_set`, not the oracle; the clocks that catalogue oscillators light were not put to the oracle. The two
  catalogue scans are samples (seed 1), not enumerations.
- The census numbers for two-sided objects classify by a 80-generation run with `sg.step_set`; "restored" there
  means equal to the unlit object at some even generation of the last 16.
- The rule "a rake swallows a p< met at even separation" was used to explain the trains; the trains themselves are
  checked directly (ring, then lift), not through that rule.
- The mirror-image gun and the left end's stationary state are `sg.step_set` only.

## 25. Where I would go next

1. **More words.** The divider writes "rake, hole" and nothing else, and 54,450 sampled placements of the
   catalogue gave no other word. Next: an enumeration instead of a sample for the oscillators of period 12, 16
   (none in the catalogue), 24 and 32 near the place where C8.24a works; a second stroke on the sparse train (an oscillator of period 16, or two oscillators) for one
   rake per 16 generations; the gun for `5f9f` itself in wider planes or the 5 × 5 tube (`sat_gun.py 5fbb C`: UNSAT
   at C = 29, 31, 33 in the 3 × 3 tube). Which rakes survive is set by the oscillator's phase alone (four
   generations later the same gun faces the complementary word), and in the undisturbed orbit the wire cannot change that phase (a cell removed at the stroke site destroys the
   oscillator: section 21b).
1b. **A switch.** An oscillator at an odd phase does nothing to the stream and at the right even phase halves
   it. Anything that shifts a catalogue oscillator by one generation or one cell would switch the divider on and
   off: that is a gate on a stream. Nothing of the kind was tried.
2. **A reader.** A far end that is changed by a hole and not by a rake (the 13 absorbers of C = 31, 33 are not:
   section 23). Next: the absorbers of C = 35 and of the 5 × 5 tube (`sat_gun.py fb C --dir 1 --all`), absorbers
   of period 8 at C ≥ 35 (`--mult 2`), each fed one hole (`gunlab.py readers`); a wall that moves one unit per hole
   would be a counter driven through the stream. The two absorbers that a hole destroys are fuses: one hole and the
   wire burns back.
3. **Two streams.** Two guns facing each other on one wire destroy each other at every distance and phase tried
   (section 23). Streams on two parallel wires in a wider tube, or a stream past a clock, were not tried.
4. **Why class 0.** `sat_two.py T --open` answers within minutes up to T = 32 (13 minutes at T = 36, about three
   times longer for each step of 4), and a proof for all T might come
   from the shape of the refutation: at T = 16 it needs the end's periodicity five units in (unit 11), not at the
   wire's end and not to the full light cone (section 22). A proof certificate (DRAT) of the T = 8 instance, read
   for which cells it uses, is the cheapest next look.
5. **The splitter and the off state** suggest a latch: an end with a stationary state and an emitting state. No
   one-cell flip lights it; a pulse or a rake arriving might.
6. **Corners: nothing was run.** As a constraint problem a corner needs a region closed under the rule, and the
   union of two tubes is not one. The smallest closed region holding wire C up to a pair of planes and a wire
   along (1,0,1) leaving from there is the wedge x+y+z, x−y+z ≥ 1 and x+y−z, x−y−z ≤ C (T2 for each of the four
   half-spaces). A window of that wedge with a shell of cells held dead, the rake in on one wire at generation 0
   and a rake required on the other at T, is an exact instance of about the size of the 5 × 5 turn instances. The
   other face diagonals give the other angles. With the gun there is now a second way to look: a stream is a
   standing probe, so any junction can be tested for ever instead of with one rake.
7. **The catalogue as a source of walls.** In the side scan a catalogue oscillator beside the wire cut it: a clock
   ran on one side, between the old cap and a wall made by the collision (to wire B′ in the two cases looked
   at), with the oscillator alive next to it (42 cases of 11,880). Those walls have wire on both sides and something periodic beside them: the
   place to look for a turn whose class depends on the oscillator's phase.

# Fifth push (2026-11-15): a listener

The question: a bounded standing object at the end of the stream or beside it that survives a gap (a rake removed)
and is left in a lasting state different from the one it has when no gap comes, both states stable under the plain
stream. **None was found.** What is excluded, exactly, is in sections 26 to 28; the strongest statement is the
constraint search of section 26 (every end of the stream in the 3 × 3 tube up to C = 39, period 4; and period 8 up
to C = 33), the widest net is the census of section 27 (741 ends, every one fed eight words of gaps, transients up to
1,500 generations), and the only search beside the stream is a sample (section 28). No new object, so nothing new
for the oracle; the controls of each search are stated with it. Forecasts and scores: `PREDICTIONS.md`.

## 26. A listener at the end of the stream as one constraint problem: none in the 3 × 3 tube

- **The instance** (`sat_listen.py C [--mult m] [--multB m'] [--word i,j,..] [--S s] [--M M]`). Three coupled copies
  of the dynamics in one CNF, on the region of `sat_gun.py --dir 1` (units ≥ KS − 2 − M inside the tube and the planes
  x+y−z, x−y−z ≤ C; KS = 6, M = 4), with the rake train (fb)^∞ running into the end:
  **A**, a state of period dividing TA = 4m whose units < KS are the plain train at every generation (exactly an
  absorber of section 21); **B**, the same with period dividing TB = 4m′ and the train's phase advanced by T; **X**,
  a run of T + 1 generations from X(0) = A(0) in which the train arriving from the left carries the word (rake cell
  (1,0,4) removed at generation 0 from the i-th, j-th, … rake counted from unit −4 leftwards: the one-cell hole of
  section 21, which moves with the train, `sat_listen.py` checks it reaches nothing before generation 4), with
  X(T) = B(0); and **B(0) ≠ A(T mod TA)** on the free cells (units ≥ 6): the state after the word is not the state
  the end would be in without it. Cells left of unit 0 are the holed train stepped on its own, and units 0, 1 of X
  are tied to it at every generation; units 2..5 of X are free (the end may disturb the 4 units in front of it during
  the transient, if it heals them). T = 62 for one hole (it reaches unit 6 at generation 20, so the end has 42
  generations to settle), 4 more per further rake of the word.
- **Why UNSAT excludes every such end.** Let E be any end of period dividing TA of the infinite tube inside the planes
  (by T2 the tube and the planes are closed, so the region is exact), X* its real orbit after the word, and suppose
  X* is in some orbit B* of period dividing TB of the same train by generation T and B* is not E's own orbit. If X*
  never changes units 0, 1 (six units in front of the end's first free unit), then X* equals the holed train on all
  units < 2 for all t ≤ T (induction on t: units ≤ 0 at t + 1 see units ≤ 1 at t), so (E, B*, X*) restricted to the
  region satisfy every clause. B is A moved, or A at a different phase relative to the train, or a different end:
  all are allowed, so movers and phase shifts are excluded too. A model would be a listener of the write-once kind
  at least (A → B, B stable); a reusable one is a special case.
- **Controls.** `python3 sat_listen.py 31 --same` (the condition B ≠ A dropped): SAT in 6 s, the C = 31 absorber,
  re-stepped (`sg.step_set`): A and B periodic, the run reaches B, and B is A healed. A control that the "≠" part finds
  real changes: wire B with pulse B (`python3 sat_listen.py C --pattern 77 --event E.json`, E = the two cells of
  `pulse-B.json` moved 12 units back, written by hand to `../scratch/signals/p5/pulseB_ev.json`: `[[-11,0,12],
  [-10,2,13]]`): UNSAT at C = 29 and 31, **SAT at C = 33** (66 s): a period-2 cap A of 21 cells that one pulse turns
  into a different period-2 cap B, re-stepped: A, B periodic, the run reaches B. B differs from A in unit 6, which
  turns from a B unit into a B′ unit: it is the B|B′ wall of section 9 moving one unit towards the sender, the known
  counter. So the encoding finds a mover when one exists.
- **[proved within the bounds; CaDiCaL 1.5.3, every instance with M = 4, S = 40; no model, so nothing to re-step]**
  (`bash listen_batch.sh`, and the instances of `listen_queue.sh`; times are single-core seconds; the log is
  `../scratch/signals/p5/listen_batch.txt`):

  | ends of period (TA, TB) | word (rakes removed) | C (3 × 3 tube) | UNSAT in |
  |---|---|---|---|
  | (4, 4) | one hole | 29, 31, 33, 35, 37, 39 | 6, 11, 22, 38, 199, 1212 s |
  | (4, 4) | two in a row [0,1]; at spacing two [0,2]; three in a row [0,1,2]; three at spacing two [0,2,4] | 31, 33, 35, 37 | 10 to 45 s (C ≤ 35); 295, 136, 328, 143 s (C = 37) |
  | (8, 8) | one hole | 31, 33 | 211, 994 s |

  TA = 8 contains TA = 4 and TB = 8 contains TB = 4, so the last row also excludes an end of period 4 that a gap
  turns into one of period 8 (a counter of rakes mod 2), and an end of period 8 that a gap moves by half a period
  (a toggle). With TA = 8 one hole position covers both arrival times of a hole relative to the end's 8-cycle (the
  end's phases are free in the instance). Holes at every rake of the train are equivalent to the one tried when the
  end has period 4 (one rake per period).
- **Not finished (cut at 25 minutes or more by `watchdog.sh`; pysat's own interrupt does not fire on these):** the
  5 × 5 tube (`--lo -1 --hi 7`) at C = 29 (33 min) and C = 31 (25 min), TA = 4. Even the plain absorber census of the
  5 × 5 tube at C = 31 (`sat_gun.py fb 31 --dir 1 --lo -1 --hi 7 --all`) found no solution in 11 minutes. Not run:
  C = 41 and beyond, TA = 8 at C ≥ 35, words other than the five above, S > 40 (a slower settling), and the
  asymmetric widened tubes except the one in section 29.
- **What this does not exclude.** Ends reaching outside the 3 × 3 tube or beyond the planes; ends that disturb the
  train more than 4 units in front of them during the transient (anything that sends a signal up the stream and gets
  it back later, or not at all); ends that settle more than 42 generations after the last hole arrives (section 27
  covers longer transients for the ends it lists); periods 3, 6, 12, …; other gaps than the one-cell hole; streams
  other than the gun's.
