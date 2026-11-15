# Signals: can anything in gump carry a signal from one place to another?

Open problem 13 of `research/OPEN-PROBLEMS.md`. Standing account; results, not a diary. Tags: **[proved]** (an exact
argument, or an exhaustive search inside stated bounds), **[measured]** (counts, with the command), **[conjectured]**.
Commands run from `research/signals/`. Bulk output goes to `research/scratch/signals/` (git-ignored).
Forecasts and their scores: `PREDICTIONS.md`.

**Answer so far: yes.** A wire can carry a signal, in two senses.

1. **A pulse** [proved by construction; the oracle is the judge]. On a period-2 wire of 6 cells per cube running
   along (1,0,−1) ("wire A"), five flipped cells move one cube every two generations (half the speed limit), with
   the wire exactly as it was behind them. `python3 verify_pulse.py objects/pulse-A.json` (3 s): on the oracle's
   cubic torus of side 40 cubes, 100 periods = 2.5 laps, the whole state at generation 2j is the state at generation
   0 moved j cubes, cell for cell, and it differs from the pulse-free wire in exactly the five moved cells.
2. **Fronts (fuses)** [measured, one oracle-verified]. Most wires are metastable: a small change converts the wire,
   repeat after repeat at a steady speed, into a different periodic state (the *ash*). The signal travels
   arbitrarily far but uses the medium up. `python3 verify_front.py objects/F-W00-plus.json` (20 s): in the
   period-19 wire W00 the front moves one repeat ((1,3,−4) cubes) every 19 generations for ten periods; behind it
   the clocks have stopped (the ash is still).

Vocabulary. A **wire** is a pattern periodic along one lattice vector v (its *repeat*) and bounded across it. A
**front** has different periodic states ahead and behind; a **pulse** has the same one. "(p, s)": after p
generations the state is itself moved by s repeats.

## Tools, and how each was checked

| file | what | checked by |
|---|---|---|
| `sg.py`, `sgc.c` | geometry of the lattice modulo any period lattice, cut down to diagonal layers (`Geom`); C kernels: dense and sparse steppers, cycle detection, the two-state difference tracker `track` | `python3 check_stepper.py` (5 s, prints ALL OK): cell for cell against `oracle.step` on five box tori at three densities for 40 generations; the set stepper against the oracle; twisted tori, slabs, tubes and a 3D twisted torus against the set stepper on a lifted patch; a wrong rule (B45/S34) is detected |
| `verify_front.py`, `verify_pulse.py` | the judge: `oracle.masks` and `oracle.step` on a cubic array torus, nothing of mine in the stepping | — |
| `extract_wires.py` → `wires/Wnn.json` | the 21 wires and 2 sheets of the notebook entry of 2026-11-15 as cells (one repeat, phase 0, repeat vector); nn = line number in `research/audit/shape3/zombie_states.txt` | each re-run on a ring of 6 repeats with 30 empty cubes beside it: exact period reproduced (printed) |
| `wirelab.py`, `plab.py` | rings of a wire; the pulse lab for wire A | use `sg.Geom` only |
| `sat_pulse.py`, `sat_defects.py` | SAT (CaDiCaL through pysat) for pulses with an unknown background, and for all defects of a given wire | every model is re-stepped with `sg.Geom` before it is reported; UNSAT answers rest on the encoding alone (see "not checked") |

Exactness of vessels. A tube bounded by layers of the two body diagonals perpendicular to (1,0,−1) is closed (T2),
so what happens in such a tube is what happens in empty space. The (1,1,1)-slab rings used for the wires on file are
closed across the slab (T4) but periodic sideways with the images 16 or 40 cubes away; results there are exact as
long as nothing reaches half way to an image, which holds for every case quoted (the oracle run of F-W00-plus is the
check for that one).

## 1. The wires on file: cuts, flips, kinks

- **[measured] Cutting one repeat out** (`python3 cut_wires.py`, 2 min; ring of 48, every phase, gaps of 1, 2, 3
  and 24 repeats): 12 of the 21 wires burn (W00, W05, W10, W18, W19, W21, W24, W30, W31 in every phase; W15, W20,
  W29 in 4 of 16 phases, W16 in 1), the other 9 are capped within 3 repeats. The caps of W09, W17, W25, W26, W33 hold
  new small clocks (the cut wire's period becomes 38, 57, 190; 48; 80; 208).
- **[measured] The fronts** (`python3 fronts.py`, 7 min; ring of 240, cell-for-cell comparison of X(t+p) with X(t)
  moved s repeats on a window from 8 repeats behind the front to 6 ahead):

  | wire (period, repeat vector) | side | speed | (p, s) | ash |
  |---|---|---|---|---|
  | W00 (19, (1,3,−4)) | +v | 1 repeat / 19 gens | (19, 1) | still, a connected still wire |
  | W00 | −v | 3 repeats / 38 gens | (38, 3) | still: a row of separate 49-cell still lifes, one per 3 repeats |
  | W05, W10 (11, (1,3,−4)) | both | 1 / 11 | (22, 2) | period 12, connected; each repeat one generation behind the last |
  | W15 (16, (2,−4,2)) | +v | 1 / 32 | (32, 1) | period 4 |
  | W18, W21, W30, W31 (9, (3,0,−3)) | +v | 2 / 27 | (27, 2) | period 30 |
  | W19 (9, (3,0,−3)) | −v | 2 / 27 | (27, 2) | period 30 |
  | W24 (22, (3,0,−3)) | both | 1 / 12 | (132, 11) | period 22, not a phase of the wire |

  In cube units per generation these are 0.21 to 0.36 of the speed limit. No ash is the wire in another phase.
  What the ash is: `python3 ash.py` (3 min).
- **[measured] Every one-cell flip** (`python3 flips.py`, 12 min; ring of 32; every cell live in some phase and
  every neighbour of one, in every phase: 57,150 trials): heals 28,337; settles within 3 repeats 17,188; **starts
  a front 11,544 (in 17 of the 21 wires; none in W09, W11, W12, W24)**; undecided at 1,500 generations 81; **pulses
  0** (no trial in which the difference ever lay wholly 3 or more repeats from where it was made). Table:
  `research/scratch/signals/flips_singles.log`.
- **[measured] Phase kinks** (`python3 kinks.py`, 30 s; repeats 10–29 of 40 at phase d, the rest at phase 0, every
  d): no boundary between two phases of a wire travels. Either the boundary stays where it is as a wall a few
  repeats wide (all d in W11, W24, W35; most in W09, W12, W25), or it starts fronts.
- Two-cell flips of the wires on file: `python3 flips.py --pairs` exists and was not run to the end (see "not done").

## 2. Wires are common, and a fifth of them are fuses

- **[measured]** `python3 harvest.py 3 3 L 20000 --seed L` for L = 1..4 (7 min in all): random soups on a ring of
  L cubes of the closed 3 × 3 diamond tube along (1,0,−1) settle into a wire about one time in ten (L = 4: 2,063 of
  20,000; 468 distinct by a coarse key). Each distinct wire, laid 40 repeats long, was cut (every phase) and hit
  (one repeat replaced by soup, 24 times): of 875 wires, 167 showed a front at least once, at speeds up to **one
  cube per generation, the speed limit** (still wires among them); **no pulse in 21,000 hits**. So fronts are found
  by sampling and pulses are not: the pulse below is not an attractor of anything tried.

## 3. The pulse

- **[proved]** `objects/pulse-A.json`; found by `python3 sat_pulse.py 3 3 7 2 1` (0.1 s). Wire A, per cube along
  (1,0,−1): three cells that never change, (0,−2,3), (0,−1,2), (0,−1,4), and three that alternate between
  (0,0,1), (0,0,3), (0,0,5) and (1,−2,2), (1,0,0), (1,0,4). The pulse is the five cells
  (9,−2,−6), (10,−2,−7), (10,−1,−8), (11,−2,−8), (12,0,−11) flipped at an even generation; (p, s) = (2, 1).
  The half-turn (x,y,z) ↦ (−x−2, y, 8−z) maps wire A to itself reversed, so the image of the pulse runs the other way.
- **[proved, by exhaustive SAT]** `python3 sat_defects.py objects/pulse-A.json 2 1 --N 9 --lo 1 --hi 5`: inside the
  3 × 3 tube, wire A has exactly 6 right-moving (2,1) defects that fit in 5 cubes (5, 7, 9, 10, 10, 14 differing
  cells; not yet sorted into single pulses and pairs), and none with (p, s) = (4,1), (4,3) or (6,1) in 5 cubes.
- **[measured] Wire A is itself a fuse.** Of its 88 one-cell flips (44 cells per cube, 2 phases) 29 heal, 1 leaves
  a stationary defect and 58 start fronts in both directions at one cube per two generations, the pulse's own speed.
- **[measured] Two pulses meeting head-on set the wire alight** (both parities of the distance): two fronts leave
  the meeting point at one cube per two generations. So does a pulse meeting any of 120 stationary defects of the
  wire tried (`python3 collide.py …`). Not yet verified with the oracle; see section 5.

## 4. What is proved about carriers in general

- **[proved] A wire cannot grow at its end.** A wire that ends (empty beyond some point along −v) lies in a
  half-space d·p ≤ C for some body diagonal d with d·v < 0 (the four diagonals span space, so some ±d has d·v < 0),
  and by T2 that half-space bounds it forever. So no front runs from a wire into empty space: fuses burn, they do
  not lay track.
- **[proved, corollary of T5] A pulse on a still or period-2 wire has an overcrowded cell in every period.** On a
  ring the pulse is an orbit of period N·p/s > 2 in a finite vessel, so by the threshold lemma it has cells with 6
  or more live neighbours that were alive the generation before; the background has none, so they are at the pulse.
  (Pulse A: yes, checked by the oracle run implicitly; a direct count is in "not done".)

## 5. Not done, not checked

- UNSAT answers of the SAT scripts are not independently certified (no proof log checked, no second encoding). SAT
  answers are: every model is re-stepped.
- Bounds of the pulse search with unknown background so far: tube 3 × 3, ring of 13 cubes, uniform background
  (repeat 1 cube), defect of width ≤ 8 cubes including its sweep: (p, s) = (1,1) UNSAT, (3,1) UNSAT, (3,2) UNSAT,
  (2,1) SAT; (4,1) did not finish in 10 minutes.
- Two-cell flips of the 21 wires; flips of the two sheets; sheets and crystals as media in general.
- L2 (a transmission through a medium left as it was, to an object that is altered) and L3 beyond "collision sets
  the wire alight": in progress.
