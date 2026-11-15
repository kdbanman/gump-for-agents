# Signals: can anything in gump carry a signal from one place to another?

Open problem 13 of `research/OPEN-PROBLEMS.md`. Standing account: results, not a diary. Tags: **[proved]** (an exact
argument, an exhaustive search inside stated bounds, or a construction the oracle has stepped), **[measured]**
(counts, with the command), **[conjectured]**. Commands run from `research/signals/`; bulk output goes to
`research/scratch/signals/` (git-ignored). Forecasts and their scores: `PREDICTIONS.md`.

## Answer: yes. L1, L2 and L3 are reached, each with the oracle as judge; and (second push) a carrier has been turned into a clock, a register and a gate

| | what | one command (all print PASS lines and `ALL PASS`) | time |
|---|---|---|---|
| L1 | **pulse B**: 2 flipped cells on a period-2 wire of 5 cells per cube move one cube every 2 generations; the wire behind is exactly as it was | `python3 verify_pulse.py objects/pulse-B.json` | 3 s |
| L1 | the same pulse running the other way | `python3 verify_pulse.py objects/pulse-B-left.json` | 3 s |
| L1 | **pulse A**: 5 cells on another period-2 wire (6 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-A.json` | 3 s |
| L1 | **pulse S**: 32 cells on a **still** wire (5 cells per cube), same speed | `python3 verify_pulse.py objects/pulse-S.json` | 3 s |
| L1, weak sense | **front**: the period-19 wire W00 is converted, one repeat every 19 generations, into a still wire | `python3 verify_front.py objects/F-W00-plus.json` | 20 s |
| L2 | **transmission**: flipping ONE cell at A sends a pulse down wire B; 36 cubes away a standing defect swallows it and is changed; six shots in a row; a control run with A untouched never changes | `python3 verify_transmission.py objects/transmission-B.json` | 30 s |
| L3 | **interaction**: two pulses of wire B meeting head-on pass through each other unchanged, or stop each other and leave a 3-cell standing mark, according to the parity of their separation | `python3 verify_interaction.py objects/interaction-B.json` | 30 s |

| second push | **clock**: wire C between two caps, ONE cell added: a rake shuttles between the caps for ever. A finite object in empty space, 32 + 5N cells, **period 4N + 2** for N units of wire (N = 1, 5, 16, 17, 30 here; every N: `python3 prove_clock.py 8 4`, section 11) | `python3 verify_clock.py objects/clock-C.json` | 4 s |
| second push | **rake**: one extra cell on wire C moves one unit per 2 generations and emits a pulse every 2 generations; a pulse met head-on is swallowed or stops it, by parity | `python3 verify_rake.py objects/rake-C.json` | 3 s |
| second push | **collision gate**: two pulses of wire C meeting head-on: exactly one survives, undelayed, the wire as it was; which one is set by the parity of their separation | `python3 verify_gate.py objects/gate-C.json` | 9 s |
| second push | **register**: the boundary between wire B and wire B' moves one unit towards whichever pulse hits it: written by a one-cell flip on one side, erased by a one-cell flip on the other, exactly | `python3 verify_register.py objects/register-BBp.json` | 5 s |
| second push | pulses of wire C, both ways | `python3 verify_pulse.py objects/pulse-C.json`, `... objects/pulse-C-left.json` | 3 s |

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

| second push: `scat.py`, `sat_reflect.py`, `caps.py`, `caps_any.py` | SAT for a wire's end: caps, reflectors (section 8) | every cap and every model is re-stepped (`sg.Geom`, `sg.step_set`); UNSAT rests on the encoding and on CaDiCaL alone |
| `scatter_table.py`, `clocks.py`, `walls.py`, `family.py`, `seglab.py`, `collisions_C.py`, `soupwires.py`, `clock_family.py`, `capclocks.py` | measurements with `sg.Geom` / `sg.step_set` in closed vessels (the 3 × 3 tube, cut by planes): exact for empty space by T2 | use the checked steppers only; what they found that matters was then put to the oracle |
| `verify_register.py`, `verify_clock.py`, `verify_gate.py`, `verify_rake.py`, `prove_clock.py` | the judge again: `oracle.step` on a cubic torus (in `prove_clock.py` the base cycle) | — |

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
  fronts at the pulse's own speed; pulse against pulse, and pulse against each of 60 standing defects at two distances, sets it
  alight). **Wire B is the robust one: of its 84 one-cell flips 74 heal, 2 leave a standing one-cell defect, 2 emit
  a single pulse (one each way) and 6 start fronts.**
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
whether they started an even or an odd number of units apart. What is strange here: one added cell is enough to
make a stretch of ribbon keep time, and ribbons of this kind come out of random soup about once in 360 tries.

# Second push (2026-11-15): from a carrier to machinery

The lead's six items, where each stands: (1) a bounded track: **reached**, section 11 (a clock of period 4N + 2 for
every N, proved); no corner, no closed polygon. (2) a receiver that stays put: a **register** written from one side
and erased from the other (section 9); no same-side toggle (section 8). (3) a gate: a **collision gate** whose two
outputs leave along the two input lines (section 10); no gate with a separate output line, no crossing. (4) where
wires come from: **pulse-carrying wires are born from soup** (section 12). (5) wire against chaos: section 13.
(6) loose ends: untouched except the caps (section 14).

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
  state after any sequence depends only on the difference of the two counts. It is not a toggle: the same pulse
  twice does not restore it.

## 10. Wire C: two pulses, two rakes, and what happens when they meet

`python3 collisions_C.py` (5 s) prints every case below as text, one hex digit per unit, one line per 2 generations.

- **[proved by the oracle runs]** Wire C (per unit: (0,1,2), (0,1,4), (0,2,3), (1,0,0), (1,0,2) at even
  generations) carries the pulse **p>** (`9f`: remove (1,0,2) of one unit, add (1,0,4) to the next; towards +v) and
  **p<** (`7`: in one unit move (0,2,3) to (1,0,4), which makes that unit a unit of wire B; towards −v), both one
  unit per 2 generations (`verify_pulse.py objects/pulse-C.json`, `... pulse-C-left.json`).
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
  left-going pulses remain. [measured, `collisions_C.py`, `sg.Geom` only] Mirror statement for `5f` against p>;
  and rake against rake: one of the two survives, by parity.

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
- **[proved, computer-assisted] A clock of period exactly 4N + 2 exists for every N ≥ 1.**
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
  one soup-born uniform wire in 46, is a pulse carrier. This corrects the first push's guess that carriers are not
  attractors. Not seen: a pulse itself arising from soup (the settled rings here are uniform by selection; the 875
  wires of section 2 gave none).
- **Grown or placed?** Placed, or born whole on a ring. A wire cannot grow at its end (section 4), and no front that
  lays wire C or B was looked for.
