# Signals: can anything in gump carry a signal from one place to another?

Open problem 13 of `research/OPEN-PROBLEMS.md`. Standing account: results, not a diary. Tags: **[proved]** (an exact
argument, an exhaustive search inside stated bounds, or a construction the oracle has stepped), **[measured]**
(counts, with the command), **[conjectured]**. Commands run from `research/signals/`; bulk output goes to
`research/scratch/signals/` (git-ignored). Forecasts and their scores: `PREDICTIONS.md`.

## Answer: yes. L1, L2 and L3 are reached, each with the oracle as judge

| | what | one command (all print PASS lines and `ALL PASS`) | time |
|---|---|---|---|
| L1 | **pulse B**: 2 flipped cells on a period-2 wire of 5 cells per cube move one cube every 2 generations; the wire behind is exactly as it was | `python3 verify_pulse.py objects/pulse-B.json` | 3 s |
| L1 | the same pulse running the other way | `python3 verify_pulse.py objects/pulse-B-left.json` | 3 s |
| L1 | **pulse A**: 5 cells on another period-2 wire (6 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-A.json` | 3 s |
| L1 | **pulse S**: 32 cells on a **still** wire (5 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-S.json` | 3 s |
| L1, weak sense | **front**: the period-19 wire W00 is converted, one repeat every 19 generations, into a still wire | `python3 verify_front.py objects/F-W00-plus.json` | 20 s |
| L2 | **transmission**: flipping ONE cell at A sends a pulse down wire B; 36 cubes away a standing defect swallows it and is changed; six shots in a row; a control run with A untouched never changes | `python3 verify_transmission.py objects/transmission-B.json` | 30 s |
| L3 | **interaction**: two pulses of wire B meeting head-on pass through each other unchanged, or stop each other and leave a 3-cell standing mark, according to the parity of their separation | `python3 verify_interaction.py objects/interaction-B.json` | 30 s |

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
- **Pulse B**: flip (13,0,−12) and (14,2,−11) at an even generation. One live cell with 6 or more live neighbours
  that was alive the generation before occurs at the pulse in every generation, none in the bare wire [measured;
  this is the drive the threshold lemma T5 demands, see section 4].
- **Emitter** [proved by the L2 run]: remove the never-changing cell (0,1,2) + k(2,0,−2) at an even generation: the
  wire heals and a pulse B leaves towards +(1,0,−1). Removing (0,1,4) + k(2,0,−2) sends one the other way [measured].
- **Receiver** (`transmission-B.json`): 8 flipped cells over 4 cubes, the end of a stretch of a variant wire (2
  cells per cube different). It swallows every pulse and its wall moves exactly one cube towards the sender. So
  the line between A and the receiver is left exactly as it was and is used again and again, and what is written at
  B is permanent; but **each pulse costs one cube of wire at the receiving end**. That is the sense in which L2 holds.
- **Eaters** [measured]: 10 of 150 standing defects of wire B swallow every pulse and stay exactly as they were.
- **The mark** left when two pulses stop each other: (28,2,−25), (29,0,−26), (30,2,−27) up to translation. A later
  pulse from either side is swallowed by it and it becomes a 5-cell standing defect [measured].

## Tools, and how each was checked

| file | what | checked by |
|---|---|---|
| `sg.py`, `sgc.c` | the lattice modulo any period lattice, cut down to diagonal layers (`Geom`); C kernels: dense and sparse steppers, cycle detection, the two-state difference tracker `track` | `python3 check_stepper.py` (5 s, ALL OK): cell for cell against `oracle.step` on five box tori at three densities for 40 generations; the set stepper against the oracle; twisted tori, slabs, tubes and a 3D twisted torus against the set stepper on a lifted patch; a wrong rule (B45/S34) is detected |
| `verify_*.py` | the judge: `oracle.masks`, `oracle.step`, nothing of mine in the stepping | — |
| `extract_wires.py` → `wires/Wnn.json` | the 21 wires and 2 sheets of the notebook entry of 2026-11-15 (nn = line in `research/audit/shape3/zombie_states.txt`): one repeat, phase 0, repeat vector | each re-run on a ring of 6 repeats beside 30 empty cubes: exact period reproduced |
| `wirelab.py`, `plab.py` | rings of a wire on file; the lab for the SAT wires (tube −7 ≤ s₁, s₂ ≤ 13: exact in empty space for anything started within a neighbour step of a 3 × 3 wire) | use `sg.Geom` only |
| `sat_pulse.py`, `sat_defects.py`, `survey.py` | SAT (CaDiCaL 1.5.3 through pysat): pulses with an unknown background; all defects of a given wire; all backgrounds carrying a pulse | every model is re-stepped with `sg.Geom` before it is reported. UNSAT rests on the encoding; `bounds.sh` repeats each instance with Glucose 4 |

**Soundness of the SAT search** (`sat_pulse.py`). Ring of N cubes of a closed tube; unknown states at generations
0..p−1; generation p is generation 0 moved s cubes; the cubes 0..K+b−1 are b-periodic along the ring at every
generation; generation 0 is not b-periodic all round. (i) With gcd(s, N) = 1 a solution cannot be a standing defect:
the set D of places where generation 0 is not locally b-periodic obeys D(p) = D(0) + s, and D + s = D would make D
empty or everything. (ii) With K ≥ max(3, s+1) the b-periodic stretch, continued for ever, is itself a solution (each
step agrees with the ring on an interval longer than b), and gluing it to both sides of the defect gives a solution of
the infinite tube: one pulse, the same background on both sides. Every pulse above was then put alone on a ring of
40 or more cubes and stepped by the oracle.

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
  a front 11,544 (in 17 of the 21 wires; none in W09, W11, W12, W24)**; undecided at 1,500 generations 81; **pulses
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
  fronts at the pulse's own speed; pulse against pulse, and pulse against any of 120 standing defects, sets it
  alight). **Wire B is the robust one: of its 84 one-cell flips 74 heal, 2 leave a standing one-cell defect, 2 emit
  a single pulse (one each way) and 6 start fronts.**
- **[proved, exhaustive SAT]** defects of wire B inside the 3 × 3 tube (`python3 sat_defects.py objects/pulse-B.json
  P S --N n --lo 1 --hi 5`): right-moving (2,1) defects fitting in 5 cubes: exactly 17 (pulse B, other pulses and
  trains; not sorted). Standing defects of period 2 in 4 cubes: at least 150 (cut off). Standing clocks of exact
  period 4 in 4 cubes (`--exact`): exactly 28. Wire A: exactly 6 right-movers in 5 cubes; none with (p, s) = (4,1),
  (4,3), (6,1) in 5 cubes.
- **[measured] What a train of pulses does to a standing defect of wire B** (`python3 receivers.py
  ../scratch/signals/B_3x3_2_0_--N_8.json --pulse objects/pulse-B.json`): of 150 period-2 defects, 109 catch fire at
  the first pulse, 10 are eaters, 31 are walls that advance one cube per pulse (8 pulses each). Of the 28 period-4
  clocks: 14 fire, 8 eaters, 6 walls. No defect was found that a pulse toggles between two states, and no clock whose
  phase a pulse shifts.
- **[proved, exhaustive SAT] A pulse on a still wire needs room**: in the 3 × 3 tube, uniform still background,
  (p, s) = (2,1): none with defect-plus-sweep ≤ 6 cubes (rings of 7 to 11), one at 7 (pulse S, 32 cells).
- **Bounds of the search with unknown uniform background**, ring of 13 cubes (defect plus sweep ≤ 9 − s cubes),
  two solvers each (`bash bounds.sh`; table in `research/scratch/signals/bounds.log`, summarised in section 6).

## 4. What is proved about carriers in general

- **[proved] A wire cannot grow at its end.** A wire that ends (empty beyond some point along −v) lies in a
  half-space d·p ≤ C for some body diagonal d with d·v < 0 (the four diagonals span space, so some ±d has d·v < 0),
  and T2 keeps it there. No front runs from a wire into empty space: fuses burn, nothing lays track.
- **[proved, corollary of T5] A pulse on a wire of period ≤ 2 that has no drive of its own must carry its drive
  with it**: on a ring it is an orbit of period N·p/s > 2 in a finite vessel, so in every lap, hence (by the shift
  symmetry) in every period, some cell has 6 or more live neighbours having been alive the generation before; if the
  bare wire has no such cell they are at the pulse. Measured: wire A and wire B have none; pulse A has 2 per
  generation, pulse B has 1.
- **[conjectured]** Pulses are not attractors: nothing sampled ever settled into one (sections 1, 2), though one
  flip in 42 of wire B emits one. Half the speed limit is the only pulse speed seen.

## 5. Not done, not checked

- UNSAT answers are not certified by a proof checker; they rest on my encoding (the same encoding whose models
  always re-step correctly) and on two solvers agreeing where `bounds.sh` ran both.
- Whether wires A, B, S arise from random soup (the harvest's 12 period-2 wires of 5 cells per cube were not
  compared with wire B up to symmetry). Whether any pulse exists in a wire on file, beyond one-cell flips.
- Fronts other than F-W00-plus have not been put to the oracle; nor have the eaters, the mark's later behaviour,
  the left-going emitter, or wire A's collisions (all `sg.Geom` only).
- Two-cell flips of the 21 wires (`python3 flips.py --pairs` is written, hours of one core, not run); the two
  sheets; sheets and crystals as media at all (the lead's S4); unrolling a twisted clock onto a straight track (S5).
- Other directions than (1,0,−1), backgrounds of repeat > 1 cube, tubes wider than 3 × 4, periods above 6.
- A receiver that does not creep (a toggle), a clock whose phase a pulse flips, a gate with an output pulse (in
  wire B a meeting either changes nothing or ends both pulses: that is a coincidence detector with a permanent
  record, not yet a logic gate with a signal out), and a way to end a wire (every wire here is a ring or infinite).

## 6. Table of bounds (unknown uniform background, ring of 13 cubes)

See `research/scratch/signals/bounds.log` after `bash bounds.sh`; the lines available when this file was last
brought up to date are copied in `bounds_table.txt`.
