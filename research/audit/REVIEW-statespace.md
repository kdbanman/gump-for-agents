# Adversarial review: `research/statespace/` (how much of its state space a seed explores)

2026-11-15. Reviewer: a subagent with its own code in `research/audit/statespace/` (nothing imported from the study;
the study's `vessels.py` is used only to translate cell indices when comparing champion states). Bulk output in
`research/scratch/audit_ss/` (ignored); the small outputs are committed in `research/audit/statespace/out/`.

## Verdicts

| claim | verdict | audit number beside the study's |
|---|---|---|
| 1 exact statistics of the small vessels | **stands**, two wording corrections | 8 vessels × 18 statistics identical (below); "typical 8–14, record 40–94 at 27–30 cells" is true of the table's family records only: over all 34 vessels of 27–30 cells the mean seed visits 4.5–14.4 states and the record 15–94 |
| 2 hull census complete | **stands as stated (≤ 6 layers wide)**; its scope is narrower than the README suggests | same 277 hulls of 1–30 cells, 262 of 2–29; but with widths up to 10 there are 588 hulls of 1–29 cells, more than twice as many, and the count is still rising at width 10 |
| 3 scaling inside N ≤ 30 | **stands with corrections** | slopes of log2 \|f(S)\| 0.88–1.01 and of log2(on cycles) 0.16–0.58 once small sizes are dropped; "linear, not exponential" **fails** as a reading: an exponential fits as well or better; the symmetry claim **stands** (all champions, full automorphism group) |
| 4 the owner's cubes | **stands** for sides 8–15 (recomputed); 16 not recomputed | 23/71/65 (oracle, exact state repeat), 4,218, 24,286, 169,049, 4,460,296, 37,367,092 (engine); side 14 enters at 4,460,296, detected at 4,460,298 |
| 5 0.30 bits per face cell | **stands** (arithmetic) | 0.296 at A = 27, 0.300 at 108 from F4; slope alone 0.299–0.305 bits per cell across the slopes on file (0.2072–0.2117 per cell); the newest 0.2084 gives 0.3007 |
| 6 living face nearly random; share 2^(−0.69 A) | **numbers stand; the inference needs rewording** | top layer alone 0.9860 (study 0.9860), whole 8-layer slab ≤ 0.9585 at K = 18 (study 0.9595 at K = 18, 0.958 at K = 20); a second ordering and sampler of my own; deficits against coins below |
| random-map yardstick | **constant corrected; yardstick misleading** | cycles ½ ln M + 0.635, not + 0.29 (11.0 at 2^30, not 10.7); a random map with gump's own in-degrees visits 18–1,650 states, not 14,500–41,000 |

## 1. Exact statistics (claim 1)

**Method.** `geom.py` builds each vessel from the cube-index neighbour table of `docs/AUTOMATON.md` §2 (the study
builds from doubled offsets), with the same parameter conventions. `geom.py oracle KIND ARGS 12 25` lifts 12 states
(all-live, then random) into `reference/oracle.py`'s array torus (a padded box for a hull; for slabs and tori the
periodic tiling with H = 2n, n Z³ a period, ≥ 3 dead layers across the wrap for a slab) and requires every copy of
every vessel cell to match a pure-python step for 25 generations and every other cell to stay dead. Negative
controls: dropping one neighbour of one cell of `slab 3 1 1 3`, or duplicating one of the 27-cell torus, fails at
generation 0. `aenum.c` tabulates f with a bit-sliced step (64 states per word, 4-bit ripple counters, a transpose),
then heights by a path walk in an 8-bit table, cycle labels pushed outwards one height level per pass, and the image
iteration on bitmaps as an internal check (#height-0 = \|f^T(S)\| in every run). 3,000 table entries per vessel are
checked against the python step (`run_one.sh`). Comparison: `python3 research/audit/statespace/compare.py NAME`.

**Result.** Identical in every one of 18 statistics (N, no-predecessor count, image sizes for every t, states on
cycles, cycles, cycles and states by period, largest and empty basin, mean/median/max transient, mean/median/max
visited, full transient histogram, number of champions, the listed champion states) for:

| vessel | N | kind | no predecessor | on cycles | transient mean / max | visited mean / max | champions |
|---|---:|---|---:|---:|---|---|---:|
| `slab_3_1_1_3` | 27 | 3-layer slab | 96,814,245 | 7,039 | 6.801 / 39 | 7.986 / 40 | 36 |
| `slab_1_0_3_3` | 27 | 3-layer slab, multigraph | 83,082,024 | 44,191 | 8.575 / 51 | 10.216 / 53 | 36 |
| `torus_9_2_1_4_0_1` | 27 | 3D torus | 114,562,737 | 2,683 | 5.805 / 37 | 6.864 / 38 | 216 |
| `torus_5_2_1_1_0_2` | 30 | 3D torus, multigraph | 876,548,183 | 3,508 | 7.057 / 52 | 8.122 / 53 | 20 |
| `hull_-1_3_-5_1_-5_1_-1_7` | 30 | hull, record of 30 | 997,420,100 | 7,875 | 7.135 / 61 | 8.355 / 62 | 4 |
| `hull_-1_3_-5_1_-5_1_-3_5` | 29 | hull, record of 29 | 501,504,160 | 6,283 | 6.235 / 52 | 7.422 / 57 | 14 |
| `hull_-1_3_-5_-1_-5_3_-3_7` | 28 | hull, record of 28 | 249,542,760 | 5,543 | 5.242 / 35 | 6.433 / 38 | 12 |
| `hull_-1_3_-5_-1_-3_5_-3_5` | 28 | hull, still-life basin largest | 253,707,875 | 2,635 | 4.557 / 23 | 5.667 / 24 | 72 |

(`research/audit/statespace/out/NAME.out`; reproduce one with `bash research/audit/statespace/run_one.sh slab 3 1 1 3`,
17 s on two cores; a 30-cell vessel about 2.5 min and 5.3 GB.) The last hull's largest basin is a still life's
(83,564,396 against the empty state's 68,924,150), as the README says.

**Closedness and the multigraphs.** The oracle check is the test of "closed": no cell outside the copies ever became
live, for the slabs (T4/T3), the hulls (T2) and both tori. For the multigraph tori and slab the oracle's own
`np.roll` sum counts a doubled neighbour twice, which is what both enumerators do, so the tiny tori are exactly the
periodic patterns the oracle runs.

**Corrections.** (a) `champion_cycle_period` in `vessels.jsonl` is the first champion's only. In `slab_1_0_3_3` the
36 champions split 24 that die out and 12 that end on a period-2 cycle of 7 live cells (those 12 visit 53 states,
which is where the 53 of the E7 exception comes from); the README's "dies to empty" holds for 24 of 36. In
`hull_-1_3_-5_-1_-5_3_-3_7`, 4 champions end in a still life and 8 on period 3 (the file says 3). (b) The sentence
"a typical seed visits 8–14 states, the most patient 40–94" at 27–30 cells is true of the six rows of the README's
table (and not even all of them: `slab_3_1_1_3` 7.99); over all 34 enumerated vessels of 27–30 cells the mean is
4.5–14.4, the median 4–12, the record 15–94 (`torus_9_2_1_4_0_1`: 6.86 and 38).

## 2. The hull census (claim 2)

`python3 research/audit/statespace/hullcount.py 30 6 --list` (11 s): a search of my own. It does not use the
study's reduction (lo0 = −1, lo1, lo2 mod 4); it lets lo0, lo1, lo2 run over the four odd residues mod 8 (the cube
steps (2,2,0), (2,0,−2), (0,2,−2) shift one diagonal coordinate by 8 each), lists the cells of a box in (s0, s1, s2)
directly from p = ((s0+s1)/2, (s0+s2)/2, (−s1−s2)/2), filters by s3, keeps tight hulls, and removes duplicates by a
canonical form under O_h and translation. Result: exactly the study's hulls, **277 of 1–30 cells (262 of 2–29,
14 of 30)**, the same sets one for one (canonical forms compared).

Its scope is narrower than the README reads. `hullcount.py 29 10` (2.6 min): with widths up to 10 layers there are
**588 hulls of 1–29 cells against 263**; wider-than-6 hulls start at 4 cells (a 4-cell hull 7 layers wide, a
5-cell one 9 wide), and at 27, 28, 29 cells there are 36, 31, 26 hulls against the census's 8, 8, 3. Hulls of
maximum width 10 still number 46, so the full count is larger again (thin needles can be as long as their cell
count allows). Do those hold longer transients? The four hulls of 29 cells wider than 6 with the most cells that can
be born (27–28 of 29) have longest transients 29, 26, 28, 18 and mean 4.0, 4.0, 3.8, 3.6, against the census
record's 52 and 6.23 (`out/hull_-3_*.out`). No sign of a record outside the census, but it is not excluded.

## 3. Scaling (claim 3)

`python3 research/audit/statespace/fits.py` (from the study's rows; eight of them reproduced above).

- **Ranges.** Dropping vessels below 15 or 21 cells moves the slope of log2 \|f(S)\| over 0.88–1.01 (stated 0.95–0.98)
  and of log2(states on cycles) over 0.16–0.58 (stated 0.2–0.6). The qualitative reading (a constant fraction lost at
  the first step; cyclic states multiplying like local pieces) survives; the stated ranges are fits to N ≥ 9 only.
  The table header says "kagome tori (3–30)" and "3D tori (3–30)" but the fits use N ≥ 9.
- **"Linear, not exponential" fails as a reading.** For the mean seed, an exponential e^(0.02–0.09·N) and a line
  fit with rms residuals within 20% of each other in every family and cut (the exponential is better in the hulls,
  0.32 against 0.39, and in the 2-layer slabs; the line in the kagome tori N ≥ 9, 0.87 against 1.05, and the 3-layer
  slabs, 0.75 against 0.95); for the record, the hull census's per-N maximum of the longest visit fits e^(0.117·N)
  with rms 3.2 against the line's 6.4. Three to ten sizes over N = 9–30 cannot tell a line from a slow exponential.
  What the data do say is that the growth is slow (ln-rate 0.02–0.16 per cell over all fits) — below the face law's
  0.209 per face cell.
- **Symmetry of champions stands.** `python3 research/audit/statespace/autos.py KIND ARGS` computes the full
  automorphism group of the neighbour multigraph (colour refinement and backtracking; any automorphism commutes with
  an outer-totalistic rule) and tests every champion. In all eight vessels above the graph has no automorphism beyond
  the lattice's (orders 2, 2, 2, 8, 12, 20, 36, 54, equal to the study's `sym_order`), no champion of any of them
  (2–216 per vessel) has a nontrivial stabiliser, the champion sets are unions of orbits, and the orbit counts match
  the study's where it gives them.

## 4. The owner's cubes (claim 4)

- Sides 8, 9, 10 on the oracle alone (`python3 research/audit/statespace/cube_entry.py 40 100`, `50 200`,
  `55 200`; a hash of every state, exact repeat): the state at generation 24, 72, 66 equals that at 23, 71, 65:
  entry 23, 71, 65, period 1, visited 24, 72, 66.
- Sides 8–14 on the engine (`gump run --cube N --lite`, `out/cubes.txt`): cycle_start 23, 71, 65, 4,218, 24,286,
  169,049, 4,460,296 with detected_gen one generation later for the still lifes and **4,460,298 for side 14**
  (period 2). The engine's detector records the first repeat, which is the exact entry generation
  (`engine/src/instruments.rs`, HaltDetector). The table's "enters at" column is the right one to add the period to.
- Hull and face sizes recomputed independently (`python3 research/audit/statespace/cubehull.py 8 9 10 13 14 16`):
  6,072 / 198, 8,814 / 273, 12,180 / 315, 27,474 / 570, 34,440 / 630, 51,888 / 828, as in the table.
- Side 15 (engine, 6.7 min on one core): extinct, cycle_start = detected_gen = 37,367,092, as in the table.
- Not recomputed: side 16 (2.9 × 10⁹ generations; rests on `research/data/cube16_summary.json`).

## 5. 0.30 bits per face cell (claim 5)

F4: ln τ = −0.091 + 0.2088·A, so log2 τ / A = 0.2964 at A = 27, 0.2985 at 48, 0.3000 at 108, → 0.3012. The slopes on
file (GP9's 0.2072 within a width family, F4's 0.2088, GL3's newest 0.2084 for wrapped faces from 63 cells, GP9's
0.2117 alternative) give 0.2989, 0.3012, 0.3007, 0.3054 bits per cell. "0.296–0.301" stands; "0.30 ± 0.005" is the
honest range. τ is a mean of a memoryless lifetime (F5), so a typical seed's count is the mean's up to ln 2 (half a
bit), negligible at these A.

## 6. Entropy of a living face (claim 6)

**Second estimate.** `entropy.py` has its own sampler (geom.py neighbours, own numpy step; the geometry of
`slab 16 0 16 8` checked against the oracle, `geom.py oracle slab 16 0 16 8 3 10`) and its own ordering: layers from
the top down, every cell of a higher layer counted as "earlier", K nearest earlier cells as context, Miller–Madow,
half-sample beside it. Sample: 64,000 snapshots, 32 replicas, soup 0.4, burn-in 2,000, every 3 generations, seed 11
(the study's 1 and 2). `python3 research/audit/statespace/entropy.py sample 16 8 64000 3 2000 11 OUT.npz`, then
`entropy.py marginal OUT.npz 7 20`, `entropy.py chain OUT.npz 20`, `entropy.py marginal OUT.npz 3 18` (about 6 min
in all). Densities top to bottom 0.518, 0.435, 0.406, 0.416, 0.416, 0.406, 0.435, 0.518, as the study's.

| | K = 0 (coins) | 10 | 14 | 18 | deficit against coins at K = 18 |
|---|---:|---:|---:|---:|---:|
| top layer alone (marginal) | 0.9991 | 0.9867 | 0.9864 | 0.9860 | **≥ 0.0131** |
| layer below the top alone | 0.9876 | — | 0.9803 | 0.9800 | ≥ 0.0076 |
| a bulk layer alone (t = 3) | 0.9794 | — | 0.9738 | 0.9736 | ≥ 0.0058 |
| whole 8-layer slab (joint, chain rule) | 0.9851 | 0.9681 | 0.9620 | 0.9585 (half: 0.9579) | **≥ 0.0266** |
| per layer, conditional on all layers above (t = 6 … 0) | | | | 0.959, 0.945, 0.954, 0.955, 0.949, 0.958, 0.962 | 0.024–0.037 |

(K = 20 is biased at 64,000 snapshots: half-sample 0.93.) Compression (lzma, `entropy.py lz`) gives 1.000 bits per
cell for both: useless as a bound here, as expected for a field this close to coins.

**Is it an upper bound?** Yes, up to sampling bias: conditioning on a subset of the past can only raise a
conditional entropy, so each K gives an upper bound on the entropy rate of the sampled ensemble; the plug-in bias
runs the other way (too low), and full and half samples agree to ≤ 0.0006 for K ≤ 18. **0.986 is the top layer
alone** (its marginal field), not conditional on the layers under it; conditioned on the layers above, a layer
carries 0.945–0.962.

**For the lead's question (deficit against coins of the same density).** An upper bound on h is a lower bound on the
deficit h_coin(ρ) − h. Measured lower bounds: top layer seen alone 0.013 (flat from K = 10: it is pinned, not
still growing); one layer seen alone 0.006–0.008; the joint slab 0.027 and still growing by about 0.002 per two
context cells. So a deficit as small as 0.02 for the slab cannot be an artefact of finite context: finite context can
only hide redundancy, never create it. The things that could make it an artefact are sampling bias (bounded above
by about 0.001 here) and the ensemble itself (a never-dying 16 × 16 face from soup 0.4, not a small face conditioned
on survival). The striking split: a single layer seen by itself is within 0.006–0.013 bits per cell of coins; most
of the slab's redundancy (0.027 and up) lives in the correlations *between* layers. Against the bulk coin value
0.979 (ρ = 0.4155), the bulk layer alone (0.9736) is 0.006 short.

**The inference.** "A face of A cells can be in 2^(0.99·A) states, so the share is 2^(−0.69·A)" compares the number of
typical configurations of one layer with the number of whole-vessel states one seed passes through. As a statement
about the top layer it is right but must be read as a bound: the seed's visited states show at most 2^(0.30·A)
distinct top layers, so it sees at most a share 2^(−0.69·A) of the typical top layers (and h = 0.986 is pinned
closely enough that the exponent is good to ±0.002). As an answer to the owner's question ("how many of the possible
states are hit") the denominator is wrong: the states are the vessel's, 2^N with N ≫ A (side 13: N = 27,474,
A = 570), or, restricted to what a living seed can look like, the typical set of the whole chaotic region, at least
2^(0.95·D·A) for a chaotic slab of D layers. Either way the share is far smaller than 2^(−0.69·A) — of order
2^(−0.95·D·A) — so the sentence survives only as "at most 2^(−0.69·A) even of one layer's configurations".

## 7. The random-map yardstick

The constants: expected distinct states visited from a random start Σ_k (M)_k/M^k = 41,068 at M = 2^30 (14,520 at
2^27) — correct; expected cycles ½ ln M + 0.635 (exactly Σ_k (M)_k/(k M^k): 11.03 at 2^30, 9.99 at 2^27), not
½ ln M + 0.29 (the README's 10.7 and 9.6). Neither changes a conclusion.

Is a uniform random map the right yardstick? Not alone. Gump's image after one step is 2–43% of the states, and a
map's rho length is set by how concentrated its in-degrees are. A random map with gump's own in-degree sequence (each
step lands on y with probability d_y/M) has a birthday time of about √(πM²/(2 Σ d_y²)): with Σ d_y² from
`INDEG=1 research/scratch/audit_ss/aenum FILE /dev/null /dev/null`:

| vessel | uniform random map | random map, gump's in-degrees | gump, mean visited |
|---|---:|---:|---:|
| `slab_3_1_1_3` | 14,520 | 777 | 7.99 |
| `slab_1_0_3_3` | 14,520 | 1,651 | 10.22 |
| `torus_9_2_1_4_0_1` | 14,520 | 18 | 6.86 |
| `hull_-1_3_-5_1_-5_1_-3_5` (29) | 29,040 | 375 | 7.42 |

So gump still settles sooner than a map with its own in-degrees, but by factors of 2.6–160, not thousands; most of the
README's "thousands of times" is the in-degree concentration, not the dynamics. (In the 27-cell torus 7% of all
states map straight to the empty state.) For large faces the README's "2^(A/2)" puts a random map on one layer's
2^A states, but the face's layer is not an autonomous map (it is driven by the layers under it); a random map on
the states the face actually lives in would visit at least 2^(0.47·D·A), so "less than chance" holds more strongly,
and the factor "2^(0.2·A)" is an artefact of the one-layer choice.

## Corrections the README needs (for an editor)

1. "The answer" 2 and Scaling: "8–14 / 40–94" → "8–14 / 40–94 in the largest vessel of each family (over all 34
   vessels of 27–30 cells: mean 4.5–14.4, record 15–94)"; and the table row `slab_3_1_1_3` (7.99) is already below 8.
2. Champions: `slab_1_0_3_3` "dies to empty" → "24 of its 36 champions die out, 12 end on a period-2 cycle of 7 cells
   (these visit 53 states)". `champion_cycle_period` in `vessels.jsonl` is the first champion's; say so, or list the
   periods of all (e.g. `hull_-1_3_-5_-1_-5_3_-3_7`: 4 still lifes, 8 period 3).
3. Hull census: add that the ≤ 6-wide restriction keeps 263 of at least 588 hulls of 1–29 cells (widths ≤ 10:
   `research/audit/statespace/hullcount.py 29 10`), that wider hulls start at 4 cells, and that the four most
   born-capable wide 29-cell hulls have longest transients 18–29 (record 52). Replace "a 12-cell one 7 layers wide".
4. Scaling: state that the ranges are N ≥ 9 fits (0.88–1.01 and 0.16–0.58 with N ≥ 15 or 21); replace "grow
   linearly in N, not exponentially" by "grow slowly: a line and an exponential of ln-rate about 0.05 (mean) or
   0.11 (record) per cell fit about equally well"; fix the table header ranges "3–30" (fits use N ≥ 9).
5. Section D: cycles of a random map ½ ln M + 0.635 (11.0, 10.0), not + 0.29; add the in-degree yardstick
   (18–1,650 states, so 2.6–160×, not "thousands of times"), or soften "thousands of times sooner than chance" to
   "than a uniform random map".
6. Section C and Answer 6: say that 0.986 is the top layer's own marginal field; that the share 2^(−0.69·A) is an
   upper bound on the share of one layer's configurations and that the share of the vessel's states is of order
   2^(−0.95·D·A) or smaller; give the deficits against coins (top layer ≥ 0.013, one bulk layer alone ≥ 0.006, the
   slab ≥ 0.027 and still growing — most of it between layers).
7. Answer 7: the random map on "the face's 2^A states" is not the face's dynamics; drop "by 2^(0.2·A)" or say it is
   for one layer only.

## What was not checked

- The side-16 cube run (not affordable). The A/7.7 symmetric-face law.
- Shannon entropies `entropy_t` of the time-t ensemble (my enumerator does not compute them).
- Kagome and 2-layer slabs (already cross-checked by `research/theory/exhaust.c`); the 8 unenumerated 30-cell hulls.
- The face law itself (F4/GL3 taken as on file); small faces conditioned on survival (the study's own gap).
- A lower bound on the face entropy (none attempted); entropy at other soup densities or in-plane lattices.
- The in-degree yardstick is a birthday approximation, not a simulation of a random map with that degree sequence.
