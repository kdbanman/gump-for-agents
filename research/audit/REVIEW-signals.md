# Review: signals in gump (`research/signals/`, state at bcd5844; `verify_interaction.py`, `objects/interaction-B.json`, `objects/pulse-B-left.json` at 896f44b)

Adversarial review, 2026-11-15. The object: the claim that gump, in which no finite pattern can move through empty
space (T2), carries signals along wires: travelling pulses (L1), a transmission from a sender to a receiver (L2), an
interaction of two pulses (L3), an emitter, a table of constraint-search bounds, fates of flips of the wires on file,
and two corollaries of the structure theorems. Every check below is my own code in `research/audit/signals/`; it
imports nothing from `research/signals/` except where it probes the encoding there on purpose (`sat_probe.py`).
The judge is `reference/oracle.py` (`oracle.step`, which works on any even box; masks built with the same definition
as `oracle.masks` and checked equal to it). Where I used my own sparse stepper (`lat.sstep`, `lat.sstep_ring`) it is
checked against the oracle (`lat.selftest`, and cell for cell on a W00 front for 300 generations). Commands run from
`research/audit/signals/`; bulk output goes to `research/scratch/audit_signals/`. One core, `nice -n 10`.

## Verdict

| claim | verdict | evidence (mine) |
|---|---|---|
| L1 pulse B, its mirror, pulse A, pulse S | **stands** | exact for 100–192 periods (≥ 3 laps) on rings of 9–64 cubes, on box tori and on the cubic `oracle.masks` torus; on the infinite lattice with no torus at all (a 600-cube finite wire, light-cone window); state = bare wire XOR moved defect, nothing outside the 3×3 tube. Pulses A, B run on rings as short as 3 cubes; pulse S needs ≥ 9 |
| L1 front of W00 (19, 1), still ash | **stands** | own run: edge exactly periodic with (19, 1) towards +v, (38, 3) towards −v; ash still on both sides; 300 generations identical to `oracle.step` on the cubic torus |
| L2 transmission, six shots, control | **stands, and goes further than stated** | rebuilt; 35 clean shots (not 6), line A..receiver exactly bare after every shot, control unchanged, same on a ring of 96. The receiver is a wall between wire B and a second period-2 wire B′; each pulse moves it one cube. **The 36th shot (receiver next to A) sets the whole ring on fire** |
| L2 "the line is used again and again" | **overstated** | the line carries exactly d − 1 shots for a receiver d cubes away, then the sender destroys it |
| L3 pass / stop by parity of separation | **stands; parity is the whole rule** for head-on pairs | every separation 2–44 on rings of 64 and 65: odd pass exactly, even stop with the 3-cell mark, no exception. On an odd ring a passing pair stops at its second meeting. Same-direction pairs at every spacing 1–12 run as rigid trains. Mark + a third pulse → 5-cell standing defect (oracle) |
| Emitter; census of wire B's 84 flips | **stands exactly** | own census: 74 heal, 2 standing (1 and 2 cells), 1 pulse right ((0,1,2) at even gen), 1 pulse left ((0,1,4) at even gen), 6 fronts |
| Bounds table, 2×2 "none" rows | **6 of 12 rows confirmed by an independent method, for every width** | transfer-graph search (no SAT): (1,1), (2,1), (3,1), (3,2), (4,1), (4,3): no pulse of any width on any uniform background; see §4 for the rest |
| Bounds table, 2×3 and 3×3 "none" rows | **rest on the encoding** | the encoding passes every test I gave it (geometry, rule clauses, known instances); see §4 |
| "Fronts in 17 of 21 wires" | **true but counts duplicates** | the 21 wires are 18 up to symmetry and phase (W17 = W20 = W26, W18 = W30): fronts in 14 of 18. Spot-checks of W00, W05, W18 agree with the README's speeds, (p, s) and ash periods |
| Corollary 1 (a wire cannot grow at its end) | **true; the argument as written is incomplete** | one half-space does not stop growth along −v; the fix (−v is a positive combination of the diagonals d with d·v < 0) is in §6 |
| Corollary 2 (a pulse carries its drive) | **valid** (T5 on the ring + shift symmetry + locality); one wording error | O1 events: bare wires 0; pulse B 1, A 2, S 2 or 9 per generation. Pulse B's O1 cell is **dead** at t, not "a live cell" |

## 1. L1 from the oracle alone

`nice -n 10 python3 l1_pulses.py` (about 4 min; output `research/scratch/audit_signals/l1_all.txt`).

For each of the four pulses (cells read from the object files by `git show`):

- **Rings on box tori** (2N, 20, 2N) for N = 9, 10, 11, 13, 16, 17, 31, 64, (80, 40, 80) for N = 40, and the cubic
  `oracle.masks` torus H = 48 (N = 24): the bare ring has exactly the stated period; at every generation t = 2j the
  whole torus equals generation 0 moved j cubes and equals the bare ring of that generation XOR the defect moved j
  cubes (nothing else differs anywhere); at every generation every live cell lies in the closed tube
  1 ≤ x+y+z ≤ 5, 1 ≤ x−y+z ≤ 5 (transverse coordinates (x+z, y) taken modulo the torus). Runs: max(100 periods,
  3 laps). All PASS. Pulse S's cells go outside its bare wire's own footprint (s₂ up to 5 where the bare wire has
  s₂ ≤ 3) but never outside the tube.
- **No transverse images at all**: own sparse stepper on the lattice modulo the ring translation N·v only, rings of
  N = 3 … 14, 3 laps. A, B and B-left run on every ring from N = 3; pulse S fails on N ≤ 8 and runs from N = 9.
- **No torus at all**: a finite piece of 600 cubes of the wire on the infinite lattice, the pulse started at cube 200
  (400 for the left-mover), 240 generations. Inside the light-cone window [t+1, L−2−t] (the cut ends cannot have
  reached it: one cube per generation), the state is the bare infinite wire at every generation, and at even t exactly
  bare XOR the moved defect; at odd t the difference stays within 4 cubes of the pulse (2 cells for B, 5 for A, 35 for
  S). All PASS.

Torus artefacts looked for and excluded: wrap-around along the wire (ring length from 3 to 64 changes nothing for A
and B; S needs 9), the pulse meeting itself (same), the legacy array-index torus (proper even tori only; the cubic
`oracle.masks` torus and box tori agree; the sparse ring and the infinite piece have no box at all), transverse
images (box tori with images 18–128 units away, and none). The wire is free-standing: the bare wire alone, in empty
space, keeps its period (infinite piece, interior). Nothing leaks sideways (tube check at every generation).

## 2. L2 and L3, own construction

**L2.** `nice -n 10 python3 l2_transmission.py 48 40` and `... 96 40` (each ~3 min; `l2_48.txt`, `l2_96.txt`). The
ring of wire B with the stored receiver cells flipped; the cell A = (8,1,−6) flipped every 120 generations from
generation 4; signalled, control and bare runs side by side.

- Shots 1 to 35: after each, stationary (period 2); the cells differing from the bare wire are the previous record
  plus exactly 2 new cells one cube nearer A, nothing lost; every cube from A up to the receiver is exactly bare;
  half-way, the cells in transit are 2 (one pulse B) between A and the receiver, nothing anywhere else (in particular
  nothing travels from A the other way round the ring). The control is unchanged to generation 4,324.
- **Shot 36** (receiver's front 1 cube from A): the ring catches fire (240 cells differ, every cube; on the ring of 96,
  120 cells over cubes 1..95 and not stationary). So a receiver d cubes away takes d − 1 shots.
- The ring of 96 (far side 60 cubes instead of 12) gives the same 35 shots and the same failure at 36: the wrap is
  irrelevant.
- **What the receiver is** (`python3 receiver_wire.py`): every record cube is wire B with (1,0,2) off and (0,2,3) on
  (per-cube representatives). That pattern, repeated, is itself a period-2 wire ("B′", 5 cells per cube). The receiver
  is a stationary wall between B and B′ (the 8 stored cells are B′ for a few cubes plus the far wall back to B); a
  pulse arriving from the B side is stopped at the wall and the wall advances one cube. It is a unary counter: its
  position records how many pulses have arrived.
- **Rate** (`nice -n 10 python3 l2_gap.py`, `l2_gap.txt`): two flips of A, g generations apart. Even g ≥ 4: two pulses
  received; g = 3 also works; g = 2: only one reception; odd g ≥ 5: only one (a flip at an odd generation heals);
  g = 1: the wire burns. So A can send a pulse every 4 generations.

**L3.** `nice -n 10 python3 l3_interaction.py` (tens of minutes; `l3.txt`; the "mark" lines of that file come from an earlier placement, the d = 22, 24 runs below are the current script). Pulses from `pulse-B.json` and
`pulse-B-left.json`; d = (first cube of the left pulse) − (first cube of the right pulse) at generation 0.

- Head-on, d = 2 … 44 on rings of 64 and 65: **odd d: pass** (state exactly bare XOR both pulses where they would be
  had they never met), **even d: stop**, stationary, exactly 3 cells left, at cubes d/2 .. d/2+1. No exception, no
  fire, smallest separations included (d = 2 stops, d = 3 passes). In interaction-B.json's convention ("sep") the
  offset is d = sep + 13, so its sep 20, 22 pass and 21, 23 stop, as claimed.
- Second meeting on the ring (t = N + d + 16): on the even ring every passing pair passes again; on the **odd ring
  every passing pair stops at the second meeting** (its separation has become d + N, of the other parity). So "by the
  parity of their separation" is the whole rule for a head-on pair. It is complete because, with p = 2 and a period-2
  wire, a pulse exists only at the wire's even phase: the integer separation is the only parameter a pair has.
- Same direction, d = 1 … 12 (both directions): after 2N generations the state is exactly the pair moved; trains
  of any spacing ≥ 1 cube run rigidly (they never interact).
- The mark (d = 22, 24) hit by a third pulse from either side, ring of 96: a 5-cell standing defect remains
  (stationary at t = 160, 162, 200). This was "[measured]" with `sg.Geom` only; it holds under the oracle.

## 3. Emitter and the 84 flips of wire B

`nice -n 10 python3 flips_B.py` (~4 min; `flipsB.txt`). Candidates: the cells of one cube that are live in some phase
(8) or neighbours of such a cell: 42; each flipped at generation 0 and at generation 1; ring of 64, oracle; fates by
the difference from the bare wire at even generations ≥ 60.

Result: **74 heal, 2 standing, 2 single pulses, 6 fronts**, exactly the README's count.
- pulse right: remove (0,1,2) at an even generation; pulse left: remove (0,1,4) at an even generation (each the
  exact moved pulse, alone);
- standing: add (0,0,3) at even generation (1 cell); add (0,2,3) at odd generation (2 cells at even generations).
  The README's "a standing one-cell defect" is true of one of the two;
- fronts: remove any of (1,0,0), (1,0,2), (1,0,4) at even, or (0,0,1), (0,0,5), (1,2,2) at odd generation, i.e.
  removing any one of the cells that blink. "Robust" is relative: one cell in 14 of those that matter burns the wire.

## 4. The bounds

**Reading the encoding** (`sat_pulse.py`, `sat_defects.py`). Rule clauses: correct in all cases (birth 4, 5;
survival 3, 4, 5; ≥ 6 dead; short neighbour lists handled); totalizer correct including the cap at 6. Tube: cells
outside are absent (dead), which is exact by T2. Ring: generation P at cube u is generation 0 at u − S. Stretch: cubes
0 .. K+B−1 periodic at every generation 0 .. P−1; defect: generation 0 not B-periodic somewhere. I found no way for the
encoding to miss a pulse whose difference from the background, over one period, fits in the N − K − 1 cubes outside
the stretch. Two remarks: (i) the "width" in the table (`N − K − 1 − S`) and the README's sentence ("defect plus the s
cubes it sweeps at most 9 − s") describe the same bound differently and conservatively; for (5,4) and (6,5) the width
is 3 and 1 cubes, so those two "none" rows say almost nothing; (ii) the soundness argument (ii) needs the neighbour
range of the encoding's ring units to be 1, which I checked (below).

**Probing it** (`nice -n 10 python3 sat_probe.py`, `sat_probe.txt`):
- G: for tubes 2×2, 2×3, 3×3 and rings of 7 and 13, `harvest.tube`'s cells and neighbour lists equal an independent
  construction from `oracle.offsets` (6, 9, 14 cells per cube); its ring units have the right size and neighbour
  range 1 (its partition into units is not mine, which does not matter).
- R: the per-cell CNF, built with the encoding's own totalizer, admits exactly the B45/S345 successor for every one of
  the 2^(k+1) assignments of a cell with k = 12, 9, 5, 3, 2 neighbours.
- K: known answers: 3×3, N = 9, (2,1): SAT, model re-stepped by the oracle; 3×3 still, N = 11: UNSAT and N = 12: SAT
  (pulse S's room, as claimed), re-stepped; 2×3, N = 13, (2,1): SAT, re-stepped.

**An independent method** (`transfer.py`; shares nothing with the encoding: own tube, own local rule checked
against `oracle.step`, no SAT). A pulse with (p, s) on a uniform background is a cycle through the all-background node
in a de Bruijn graph whose nodes are windows of s + 1 space-time columns (a column = one cube at generations
0 .. p−1); every constraint is between adjacent cubes and splits by generation. Closing the set of windows from which
the background node can be reached (or reachable from it) decides the question **for every width**, when the closure
is finite. Positive controls: 2×3 (2,1) finds pulses on 8 background columns (all re-stepped by the oracle); 3×3
(2,1) restricted to wire B's background finds a pulse (re-stepped).

RESULTS_PLACEHOLDER

**Which "none" rows I stand behind.** 2×2: (1,1), (2,1), (3,1), (3,2), (4,1), (4,3) — no pulse of any width on any
uniform background (two methods that share nothing). STAND_MORE_PLACEHOLDER
All 2×3 and 3×3 "none" rows rest on the encoding alone (two solvers agree, the encoding passes every test above, but
no second method). The two narrow rows (5,4), (6,5) say little at any rate.

## 5. The wires on file

`nice -n 10 python3 wires_distinct.py` (5 s): the 21 wires on file are **18 up to the 48 symmetries, translation and
phase**: W17 = W20 = W26 and W18 = W30 (explicit maps printed). All five duplicates fire, so "fronts in 17 of 21"
is "fronts in 14 of 18 distinct wires".

`nice -n 10 python3 fronts_check.py W00 W05 W18 --oracle` (~25 min; `fronts.txt`), own sparse ring stepper:

| wire | flips at phase 0 (ring of 40, 250 gens) | front +v | front −v | ash |
|---|---|---|---|---|
| W00 (19, (1,3,−4)) | 137 candidates: 94 front, 43 heal | (19, 1) exact | (38, 3) exact | still both sides (+v 24 cells/repeat; −v 16.3 per repeat = 49 per 3 repeats); not a wire phase |
| W05 (11, (1,3,−4)) | 224: 83 front, 141 heal | (22, 2) | (22, 2) | period 12 both sides |
| W18 (9, (3,0,−3)) | 115: 69 front, 30 heal, 16 local | (27, 2) | none (one-sided) | period 30 |

All agree with the README's front table and with its flip census (W00 137 candidates, as in `flips_singles.jsonl`; its
front fraction there, 69%, equals mine at phase 0). For W00 the sparse ring run was compared cell for cell with
`oracle.step` on the cubic torus of side 60 for 300 generations: identical. I did not check connectivity of the
W00 +v ash ("a connected still wire").

## 6. The corollaries

**Corollary 1** ("a wire cannot grow at its end"). The README argues: the ended wire lies in a half-space d·p ≤ C with
d·v < 0, and T2 keeps it there. That keeps it from crossing one oblique plane, but does not stop growth towards −v:
with one half-space the pattern could advance along −v while drifting so that d·p stays below C (e.g. for
d = (−1,1,1), v = (1,0,−1), the direction w = (0,−2,1) has d·w < 0 and w·v < 0). The conclusion is nevertheless
true, by this argument: let D = {signed body diagonals d with d·v < 0}. A wire bounded across its axis and empty
beyond its end has d·p bounded above on its support for every d ∈ D, so by T2 it stays in ∩_{d∈D} {d·p ≤ C_d}
forever. And −v is a non-negative combination of the elements of D (if −v lies in the cone of a cube facet,
say x ≥ |y|, |z|, then −v = a(1,σ,τ) + b(1,σ,−τ) + c(1,−σ,τ) with a = (|y|+|z|)/2, b = (x−|z|)/2, c = (x−|y|)/2, and
the diagonals with positive weight have d·(−v) > 0). Hence (−v)·p ≤ Σ λ_d C_d for ever: the support never passes a
fixed plane perpendicular to v. Hypotheses: everything beyond the end is empty (and stays so: no other pattern there),
the wire is bounded transversally, the rule's smallest birth count is ≥ 4 (T2). Wording to fix in the README, not the
claim.

**Corollary 2** ("a pulse on an undriven wire carries its drive"). Valid as stated, from T5: for a (2,1) pulse on a ring of
N ≥ 2 cubes the state has period exactly 2N > 2 (x(2j) is x(0) moved j cubes, which differs from x(0) for 0 < j < N
because the pulse moves, and odd generations are another phase of the wire); the ring in the closed tube is a finite
vessel, so every period of the orbit contains an O1 event; the shift symmetry x(t+p) = σ^s x(t) moves an event at t to one at t + p, so every window of p
generations has one; a cell far from the pulse has the same neighbourhood at t and t−1 as in the bare wire, so if the
bare wire has none, the events are within a neighbour step of the pulse. Measured (`python3 drive.py`, ring of 24,
47 generations): bare wires A, B, S: 0 O1 events; pulse B (either way): 1 per generation; pulse A: 2; pulse S: 2 and 9
alternately. Wording: README §"The objects" says "one **live** cell with 6 or more live neighbours that was alive the
generation before"; for pulse B that cell is **dead** at t in all 47 generations (overcrowded cells die). T5's event
is "overcrowded at t, live at t−1" (for pulses A and S about three quarters of the event cells are live at t, for B
none). The corollary is about the ring; on the infinite wire it transfers by locality once the ring is longer than the
pulse's neighbourhood (A and B run on rings of 3 cubes, S on 9).

## 7. The write-up

- **What a signal is here.** One pulse = one bit (present or absent) moving at one cube per 2 generations, half the
  speed limit; latency 72 generations over the 36 cubes of the L2 line. Pulses travel in trains at any spacing ≥ 1
  cube without interacting, so the line could hold a bit every cube; the emitter at A can fire every 4 generations
  (one bit per 4 generations, every 2 cubes). The receiver is a unary counter; it reads presence, not pattern.
- **Does L2 deserve the name?** Yes, as a transmission of a permanent record: a one-cell change at A causes, 36 cubes
  away and only there, a permanent change, repeatably, with an untouched control, and the line between returns
  exactly to its old state. What it is not: a reusable channel with a fixed receiver. The receiver's "creep" is its
  record; its capacity is d − 1 for distance d, and the next shot burns the line. Better wording: "a counter at the far
  end: each pulse moves a B|B′ wall one cube towards the sender; d − 1 pulses fit".

### Should change in the README

1. L2: state the capacity and the failure: 35 shots work over 36 cubes; the 36th (receiver adjacent to A) sets the
   whole wire on fire. "Used again and again" → "used d − 1 times".
2. L2: say what the receiver is (a wall between B and the period-2 wire B′ = B with (1,0,2) off, (0,2,3) on; a counter).
3. §4 corollary 1: replace the one-half-space argument by the cone argument (§6 above).
4. "The objects", pulse B: "one live cell with 6 or more live neighbours that was alive the generation before" →
   "one cell with 6 or more live neighbours that was live the generation before (it dies)".
5. §1 flips: "in 17 of the 21 wires" → note the 21 are 18 up to symmetry (W17 = W20 = W26, W18 = W30): 14 of 18.
6. Wire B's census: "2 leave a standing one-cell defect" → one 1-cell, one 2-cell standing defect.
7. L3: add that parity is the whole rule for head-on pairs (d = 2..44 checked), that on an odd ring a passing pair
   stops at its second meeting, and that same-direction trains of any spacing are rigid.
8. The mark's later behaviour (5-cell standing defect) now holds under the oracle; upgrade from "sg.Geom only".
9. §6 table: "[proved within the bounds, two solvers]" → "rests on the encoding; two solvers agree"; mark the 2×2 rows
   confirmed for every width by the independent transfer-graph search; say that (5,4) and (6,5) bound the defect to
   3 and 1 cubes; state the width once, in one convention.
10. The emitter's rate: A can be fired every 4 generations (§2); flips at odd generations heal.

### Not checked

- Fronts other than W00, W05, W18 (and the README's ash table for W15, W19, W21, W24, W30, W31); W00 +v ash
  connectivity; the kinks, cuts and harvest (§1–2 of the README) beyond the three spot-checks; two-cell flips.
- The 1,000-defect receiver census, the 17 right-movers and 28 clocks of `sat_defects.py`, the 30 backgrounds of
  `survey.py`, wire A's collisions and its 88 flips.
- `bounds_table.txt` rows other than those named in §4; UNSAT answers are not certified by a proof checker in either
  method (my transfer-graph closures are exhaustive enumerations, not certificates).
- The 3×3 transfer search over all 693 backgrounds of period dividing 2 did not finish in 20 minutes (only wire B's
  background was run to the end).
- Whether a pulse exists on a background of repeat ≥ 2 cubes, in other directions, or in wider tubes (as in the
  README's own list).
