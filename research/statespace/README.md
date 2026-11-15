# How much of its state space does a gump seed explore?

2026-11-15. The owner's question (`docs/OWNER-JOURNAL.md`, first note): within a hull there are finitely many states;
for the longest-lived seeds, how many of them are hit, and is there a pattern as the size goes up? Forecasts written
before any enumeration: `PREDICTIONS.md` (the lead's E1–E7, the investigator's I1–I7), scored below.
## Reviewed (2026-11-15)

An adversarial review with its own code (`research/audit/REVIEW-statespace.md`, outputs in
`research/audit/statespace/out/`) re-derived 18 statistics of 8 vessels (27–30 cells) with a separate bit-sliced
enumerator and its own oracle check: **every exact count matches**, as do the hull census (same 277 hulls of width
≤ 6), the champion symmetry (full automorphism groups), the cubes 8–15, the face-law arithmetic and both entropy
upper bounds (its own sampler and ordering). Seven corrections were applied here, each marked "corrected 2026-11-15
(review)": (1) the visited counts quoted are those of each family's largest vessel; over all 34 vessels of 27–30
cells the mean seed visits 4.5–14.4 states and the record 15–94; (2) `champion_cycle_period` was the first champion's
only — every listed champion's end is now in `champion_end`, and `slab_1_0_3_3`'s champions do not all die; (3) the
hull census keeps 263 of at least 588 hulls of 1–29 cells; (4) "linear, not exponential" withdrawn: the growth is
slow, and a line and a slow exponential fit equally well; (5) the random-map cycle constant is ½ ln M + 0.635, and a
uniform random map is a misleading yardstick — against a random map with gump's own in-degrees gump settles 2.6–160
times sooner, not thousands; (6) 0.986 is the top layer seen alone, the share 2^(−0.69·A) bounds one layer's
configurations only, and the deficits against coins are given; (7) "less than chance by 2^(0.2·A)" withdrawn.

Tags: **[proved]** (a theorem, or an exhaustive enumeration whose code was matched to `reference/oracle.py`),
**[measured]** (a sampled number with its error or its convergence shown), **[conjectured]**.

## The answer

1. **A seed visits almost nothing of its state space, at every size.** A deterministic orbit cannot revisit a state
   before it reaches its final cycle, so the states one seed visits are exactly its settling time plus its final
   period [proved].
2. **Where every state can be listed** (vessels of up to 30 cells, 2^30 ≈ 10⁹ states), a typical seed visits a
   handful of states: over all 34 listed vessels of 27–30 cells the mean seed visits 4.5–14.4 states and the most
   patient seed of each vessel 15–94 [proved]. A *uniform* random map on as many states would wander through about
   41,000 before repeating; but most of gump's states have no predecessor, and a random map with gump's own
   in-degrees would visit 18–1,650, so gump settles 2.6–160 times sooner than that fairer yardstick (corrected
   2026-11-15, review).
3. **At these sizes nothing is chaotic yet.** Visited states grow slowly with size (a line and an exponential of
   ln-rate 0.02–0.16 per cell fit about equally well, against the face law's 0.21; corrected 2026-11-15, review); one seed
   sees a fraction of about 2^−(0.8 to 0.9)·N of its vessel's states. What does shrink fast is what can still happen: after one
   generation 57–98% of all states can no longer occur (they have no predecessor), and at the end only 2^(0.4–0.57)·N remain — thousands of
   still lifes and small oscillators (periods up to 70).
4. **Your 2012 cubes, counted exactly:** the side-16 cube visited 2,919,617,676 ≈ 2^31.4 distinct states, out of
   2^51,888 for its hull; sides 8–16 all visited 0.0005–0.0008 bits per hull cell [proved from the runs].
5. **The pattern that extrapolates is the face law.** A seed lives as long as its faces, and a face of A cells lives
   e^(0.209·A) generations, so a seed visits about 2^(0.30·A) states: 0.30 bits per face cell, constant from A = 27 to
   135 [measured]. The symmetric cubes reach 0.15–0.29 bits per cell of their effective (symmetry-reduced) face,
   rising towards 0.30.
6. **A share of what?** Not of nothing: a living face is almost random. Its top layer, seen alone (not conditioned on
   the layers under it), carries 0.986 bits per cell; the whole chaotic face slab at most 0.958 per cell [measured].
   So one layer of a face of A cells shows about 2^(0.99·A) typical configurations, and a seed passes through at most
   2^(0.30·A) of them before the face dies: **at most** a share 2^(−0.69·A) of even one layer's configurations
   (2^−33 for a 48-cell face). Of the states of the whole chaotic region (D layers, at least 2^(0.95·D·A) typical
   states) the share is far smaller, of order 2^(−0.95·D·A). Against coin flips of the same density the face falls
   short by at least 0.006–0.013 bits per cell in one layer seen alone and at least 0.027 in the slab jointly, most of
   it in the correlations between layers (corrected 2026-11-15, review).
7. **Against chance:** gump visits fewer states than a random map at every size. For large faces the comparison with
   a random map on one layer's 2^A states (2^(A/2) visits) is only indicative — a layer is driven by the layers
   beneath it, not an autonomous map — and a random map on the states the face actually lives in would visit at least
   2^(0.47·D·A). The states are there; what ends the exploration is the face going quiet.

## A. Exact: vessels whose 2^N states were all listed

### The vessels [proved]

`vessels.py` builds four kinds; for each, every cell outside it is dead forever, so the state space is exactly
{0,1}^N:

- **Diagonal hulls** `hull LO0 HI0 … LO3 HI3`: the cells p (doubled coordinates) with LO_d ≤ d·p ≤ HI_d on the four
  body diagonals d. A seed inside stays inside forever by T2 (`docs/AUTOMATON.md`): a cell beyond a bound has at most
  3 live neighbours. **Every** diagonal hull of 2–29 cells that is at most 6 layers wide along each diagonal was
  enumerated (262 hulls up to translation and O_h; list in `data/hulls_W6_upto30.txt`, from `vessels.py hulls 30 6`,
  whose search is complete by the argument in its docstring), plus six of the fourteen 30-cell ones (those 3 or 5
  layers wide along the first diagonal in which every cell can be born). The census is complete for width ≤ 6, but that
  restriction keeps only 263 of at least 588 hulls of 1–29 cells (the review's search up to width 10,
  `research/audit/statespace/hullcount.py 29 10`, still rising at width 10; wider hulls start at 4 cells; at 27, 28,
  29 cells 36, 31, 26 hulls against the census's 8, 8, 3). The four most born-capable wide 29-cell hulls have longest
  transients 18–29 against the census record's 52: no sign of a record outside the census, but it is not excluded
  (corrected 2026-11-15, review). Small hulls are thin: in many of them some cells have fewer than 4 neighbours inside and can never be born
  (column "born-capable" in `data/tables.md`).
- **Slab tori** `slab p q r m`: m consecutive {111} layers on the in-plane torus (i,j) ~ (i+p,j) ~ (i+q,j+r); closed
  by T4 (a pattern in m consecutive layers stays in them). Families m = 3 (the thinnest slab with no finite sealed
  set, T6; every lattice of index 1–3: 9, 18, 27 cells), m = 2 and m = 1 (the kagome layer; per index the lattice with
  the longest shortest loop, N = 3k up to 30).
- **3D tori** `torus a b c d e f`: Z³ modulo a lattice of index k (3k cells), per index the lattice with the longest
  shortest vector. Tiny tori are multigraphs: a cell can be its own neighbour's neighbour twice (column "multi" in
  `data/vessels.jsonl`); the dynamics is that of the periodic patterns of the lattice, which is what the oracle runs.

### How the enumeration was checked

`enum.c` builds the table f(s) for all 2^N states. `validate.py` lifts random states of each vessel into the oracle's
array torus (a padded box for a hull; for a slab or torus a periodic tiling of an n-torus with nZ³ a period of the
vessel and, for a slab, at least three dead layers across the wrap, which T3 keeps dead) and steps them with
`oracle.step`; every copy of every vessel cell must agree with `enum.c` at every generation, and every other cell must
stay dead. Run by `run.py` on **every** vessel: 40 random states × 40 generations, then the first 8 champions over
their whole transient plus one period (`validated` field of each row). A deliberately wrong rule (birth on 4 only) is
caught at generation 1–4 on a hull and a slab. Independent cross-checks that came for free: the 12-cell vertex star
(T10: 2,750 seeds die, 107 nonempty still lifes, 195 two-cycles) is reproduced exactly; lattices equivalent by symmetry
(the three index-2 slabs, three of the four index-3 slabs) give identical maps; the image iteration stops exactly at
t = longest transient, as it must. Every one of the 301 champion files is verified on the oracle alone by
`champion.py` (transient and period, 1 minute in all). **Independent code:** `research/theory/exhaust.c` (another
agent's enumerator, its own counting code) gives, for the eight kagome and 2-layer tori listed by both (15–30 cells),
the same garden-of-Eden counts, the same cycles by period, the same longest and mean transients and even the same
champion states (`research/theory/exhaust_results.txt`; e.g. `slab 5 1 2 1`: 945,497,517 states without a
predecessor, 56,067 cyclic states, transient 56 from 0x39a4f93, in both).

### Results for the largest vessel of each family [proved]

M = 2^N. "Visited" = transient + period of the final cycle = distinct states on the orbit. These are each family's
largest vessel; over all 34 listed vessels of 27–30 cells the mean seed visits 4.5–14.4 states (median 4–12) and the
record 15–94 (`torus_9_2_1_4_0_1`: 6.86 and 38). How each champion ends: `champion_end` in `data/vessels.jsonl` (every
listed champion, up to 256 per vessel; `python3 research/statespace/champ_periods.py`); the field
`champion_cycle_period` is the first champion's only (corrected 2026-11-15, review).

| family | vessel | N | no predecessor | log2 \|f(S)\| | on cycles (cycles; periods) | largest basin | transient mean / median / max | visited mean / median / max | champions |
|---|---|---:|---:|---:|---|---|---|---|---|
| diagonal hull | `hull_-1_3_-5_1_-5_1_-1_7` | 30 | 0.929 | 26.19 | 7,875 (5,900; 1,2,3,4,5,6,16) | empty, 0.251 | 7.14 / 5 / 61 | 8.35 / 6 / 62 | 4 seeds, 2 orbits of 2 symmetries, none symmetric; all end in a 16-cell still life |
| 3-layer slab | `slab_1_0_3_3` (≡ `3_0_1`, `3_2_1`) | 27 | 0.619 | 25.61 | 44,191 (22,651; 1,2,3,4,6,8,10,12) | empty, 0.288 | 8.57 / 7 / 51 | 10.22 / 9 / 53 | 36 seeds, 3 orbits of 12; 24 die out, 12 end on a 7-cell period-2 cycle (corrected 2026-11-15, review) |
| 3-layer slab | `slab_3_1_1_3` | 27 | 0.721 | 25.16 | 7,039 (4,060; 1,2,3,4,6,10) | empty, 0.563 | 6.80 / 6 / 39 | 7.99 / 7 / 40 | 36 seeds, 1 orbit of 36; all end in a 9-cell still life |
| 2-layer slab | `slab_5_1_1_2` | 30 | 0.787 | 27.77 | 8,386 (5,435; 1,2,3,4,5,6,8,70) | empty, 0.666 | 12.91 / 10 / 88 | 14.41 / 12 / 94 | 60 seeds, 3 orbits of 20; all end on a 12-cell period-3 cycle |
| kagome torus | `slab_5_1_2_1` | 30 | 0.881 | 26.93 | 56,067 (41,768; 1,2,3,4,6,8) | empty, 0.627 | 7.43 / 6 / 56 | 8.57 / 7 / 57 | 40 seeds, 2 orbits of 20; all end in a 7-cell still life |
| 3D torus | `torus_5_2_1_1_0_2` | 30 | 0.816 | 27.56 | 3,508 (2,118; 1,2,4,6,8,18) | empty, 0.935 | 7.06 / 6 / 52 | 8.12 / 7 / 53 | 20 seeds, 1 orbit of 20; all die out |

`slab_1_0_3_3` is a multigraph (its in-plane torus has a loop of one step); `slab_3_1_1_3` is the equilateral index-3
torus. In two hulls (28 and 30 cells) the largest basin is a still life's, not the empty state's; in every other listed
vessel of ≥ 9 cells it is the empty state's.

Every vessel: `data/tables.md` (`python3 research/statespace/analyze.py tables`). Hull census per N (every hull of N
cells at most 6 layers wide; selected rows): `python3 research/statespace/analyze.py hullsizes`:

| N | hulls | no predecessor (min–max) | log2 \|f(S)\|/N (max) | on cycles (max) | mean transient (max) | longest transient (its hull) |
|---:|---:|---|---:|---:|---:|---|
| 12 | 18 | 0.700–0.984 | 0.855 | 498 | 1.91 | 6 |
| 15 | 16 | 0.831–0.968 | 0.829 | 535 | 2.25 | 10 |
| 18 | 14 | 0.896–0.970 | 0.818 | 690 | 2.83 | 17 |
| 21 | 11 | 0.917–0.974 | 0.829 | 1,161 | 3.58 | 20 |
| 24 | 12 | 0.914–0.956 | 0.852 | 2,297 | 4.44 | 26 |
| 25 | 9 | 0.892–0.964 | 0.871 | 3,538 | 4.48 | 26 |
| 26 | 9 | 0.931–0.963 | 0.851 | 2,553 | 4.44 | 30 |
| 27 | 8 | 0.927–0.968 | 0.860 | 4,123 | 5.38 | 41 (`hull_-1_3_-5_1_-5_1_-1_5`) |
| 28 | 8 | 0.930–0.970 | 0.863 | 5,543 | 5.24 | 35 (`hull_-1_3_-5_-1_-5_3_-3_7`) |
| 29 | 3 | 0.934–0.943 | 0.865 | 6,283 | 6.23 | 52 (`hull_-1_3_-5_1_-5_1_-3_5`) |
| 30 | 6 of 14 | 0.929–0.958 | 0.873 | 7,898 | 7.14 | 61 (`hull_-1_3_-5_1_-5_1_-1_7`) |

### The image after t generations [proved]

log2 |f^t(S)| / N, the bits per cell of the states still possible after t generations, for every t until it stops
(full lists: `image_t` in `data/vessels.jsonl`):

| vessel | N | t = 1 | 2 | 3 | 5 | 10 | 20 | 30 | 40 | 50 | stops at t (= longest transient) | final (on cycles) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hull_-1_3_-5_1_-5_1_-1_7` | 30 | 0.873 | 0.798 | 0.742 | 0.663 | 0.547 | 0.455 | 0.436 | 0.432 | 0.432 | 61 | 0.431 |
| `slab_1_0_3_3` | 27 | 0.948 | 0.912 | 0.886 | 0.846 | 0.773 | 0.669 | 0.600 | 0.575 | 0.572 | 51 | 0.572 |
| `slab_5_1_1_2` | 30 | 0.926 | 0.883 | 0.851 | 0.804 | 0.728 | 0.635 | 0.570 | 0.519 | 0.480 | 88 | 0.434 |
| `slab_5_1_2_1` | 30 | 0.898 | 0.828 | 0.775 | 0.701 | 0.612 | 0.552 | 0.532 | 0.527 | 0.526 | 56 | 0.526 |
| `torus_5_2_1_1_0_2` | 30 | 0.919 | 0.856 | 0.816 | 0.757 | 0.661 | 0.537 | 0.450 | 0.401 | 0.393 | 52 | 0.393 |

The loss is front-loaded in the hulls (half the eventual loss in bits by t = 3 in 143 of 152 hulls of ≥ 15 cells)
and slow in the 2- and 3-layer slabs (a quarter to a third by t = 3).

### Transients and visited states [proved]

Distributions over all 2^N seeds are in `transient_hist` and `visited_hist`. They are short-tailed: the number of
seeds not yet settled after t generations falls by a roughly constant factor per generation (in the 27-cell slab
2^25.2, 2^22.2, 2^19.1 at t = 10, 20, 30: a factor 2^-0.3 per generation), so there is no long-lived population at
these sizes — the transients are not yet the face law's exponential lives.

### Champions [proved]

The seed with the longest transient, per vessel, is in `data/champions/NAME.txt` with the one command that verifies
it on the oracle (`python3 research/statespace/champion.py data/champions/NAME.txt`). In no vessel of 19 or more
cells is any listed champion fixed by a nontrivial symmetry of the vessel (stabiliser 1 for the first 64 listed;
at 12–18 cells a few are). Champions come in whole orbits of the symmetry group: in the 3-layer 27-cell slab
`slab_3_1_1_3`, the 36 champions are one orbit of its 36 symmetries. What they look like: a population that hovers
near half the cells and then collapses in the last few generations (the 27-cell slab `slab_3_1_1_3` champion: 9–18
live cells for 37 generations, then a 9-cell still life; the 3D torus's die out; of `slab_1_0_3_3`'s 36, 24 die out
and 12 end on a 7-cell period-2 cycle); the 2-layer 30-cell champion wanders for 88 generations
and lands on a period-3 cycle.

### Scaling [proved for the numbers; the extrapolation is conjectured]

Least-squares lines over each family's listed vessels of N ≥ 9 only (`python3 research/statespace/analyze.py
scaling`; hulls: all 226 of N ≥ 9 pooled, mixed shapes). The ranges depend on the cut: with N ≥ 15 or 21 the review
finds slopes 0.88–1.01 for log2 |f(S)| and 0.16–0.58 for the states on cycles (`research/audit/statespace/fits.py`):

| family | log2 \|f(S)\| | log2 (on cycles) | mean transient | longest transient |
|---|---|---|---|---|
| diagonal hulls (fitted N 9–30) | 0.971 N − 3.4 | 0.576 N − 4.3 | 0.17 N − 0.4 | 1.5 N − 15 |
| 3-layer slabs (fitted 9, 18, 27) | 0.981 N − 1.0 | 0.516 N + 0.9 | 0.33 N − 0.6 | 2.4 N − 18 |
| 2-layer slabs (fitted 12–30) | 0.958 N − 0.8 | 0.328 N + 4.2 | 0.60 N − 5.0 | 4.6 N − 54 |
| kagome tori (fitted 9–30) | 0.949 N − 1.4 | 0.483 N + 2.0 | 0.25 N − 0.1 | 1.9 N − 15 |
| 3D tori (fitted 9–30) | 0.983 N − 2.2 | 0.219 N + 5.4 | 0.27 N − 1.5 | 2.2 N − 22 |

- **[proved, within the listed range]** The states with a predecessor are 2^(0.95–0.98 N − c): a constant fraction,
  not a vanishing one, is lost at the first step (57–98% of all states have no predecessor; 2–43% keep one), so in bits per cell the
  image after one step creeps *up* towards 1 as N grows (0.86–0.95 at N = 27–30).
- **[proved, within the range]** The states on cycles number 2^(0.2–0.6 N): they multiply like independent local
  pieces (still lifes and small oscillators placed side by side), so log2 of their number is roughly linear in N with a
  family-dependent slope; the hull values scatter by shape.
- **[proved, within the range]** Visited states (typical and record) grow slowly: the mean seed visits 4.5–14.4
  states at N = 27–30, the record 15–94. Three to ten sizes cannot tell a line from a slow exponential: in the review's
  fits an exponential of ln-rate 0.02–0.09 per cell (mean seed) fits as well as a line, and for the hull census's
  per-N record e^(0.117·N) fits better (rms 3.2 against 6.4). All rates are below the face law's 0.209 per face cell.
  As a share of the space the visited fraction is about 2^(−0.9 N) for the mean seed and 2^(−0.8 N) for the record.
  (Corrected 2026-11-15, review: this read "linear in N, not exponentially".)
- **[conjectured]** Extrapolation. Nothing at N ≤ 30 lives long enough to be on the face law: the slabs' faces have
  A = N/m = 9–30 cells, below the A ≈ 36 at which the face law's lifetimes become exponential (NOTEBOOK 2026-11-12).
  The listed sizes show the *pre-chaotic* regime. The two regimes join, we conjecture, where the face law's
  e^(0.21·A) overtakes the slow growth of the transient seen here, i.e. near A ≈ 30–40 cells per face; that is
  also where the 3-layer slabs' mean transient (2.0, 5.5, 8.6 at A = 3, 6, 9) would have to keep rising by 0.2 in ln
  per cell — it already slows (local slopes 0.33 then 0.15 per cell).

## B. Vessels too large to list: the owner's closed cubes and the face law

A seed's visited states are exactly (generation at which it enters its final cycle) + (period) [proved]. Closed
cubes of side n (the owner's 2012 seeds, `docs/AUTOMATON.md` §4) live in their diagonal hull, the regular octahedron
of radius R = 3n − 2 about the cube's centre (a vertex for even n); A = cells of one of its 8 faces (outermost
layer). Sides 8–13: engine = legacy log; 14, 15: `gump run --cube N --lite` (this study; 14 enters its period-2 cycle at
4,460,296, two generations before the notebook's detected 4,460,298); 16: `research/data/cube16_summary.json`.
`python3 research/statespace/large.py` → `data/large_cubes.csv`.

| side | hull cells | A | enters final cycle at | period | states visited | log2 | bits per hull cell | bits per face cell (A) | bits per A/7.7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 6,072 | 198 | 23 | 1 | 24 | 4.58 | 0.0008 | 0.023 | 0.178 |
| 9 | 8,814 | 273 | 71 | 1 | 72 | 6.17 | 0.0007 | 0.023 | 0.174 |
| 10 | 12,180 | 315 | 65 | 1 | 66 | 6.04 | 0.0005 | 0.019 | 0.148 |
| 11 | 16,416 | 408 | 4,218 | 1 | 4,219 | 12.04 | 0.0007 | 0.030 | 0.227 |
| 12 | 21,420 | 459 | 24,286 | 1 | 24,287 | 14.57 | 0.0007 | 0.032 | 0.244 |
| 13 | 27,474 | 570 | 169,049 | 1 | 169,050 | 17.37 | 0.0006 | 0.030 | 0.235 |
| 14 | 34,440 | 630 | 4,460,296 | 2 | 4,460,298 | 22.09 | 0.0006 | 0.035 | 0.270 |
| 15 | 42,636 | 759 | 37,367,092 | 1 (extinct) | 37,367,093 | 25.16 | 0.0006 | 0.033 | 0.255 |
| 16 | 51,888 | 828 | 2,919,617,675 | 1 | 2,919,617,676 | 31.44 | 0.0006 | 0.038 | 0.292 |

- **[proved]** The side-16 cube visited 2^31.44 of its hull's 2^51,888 states; every closed cube 8–16 visited between
  0.0005 and 0.0008 bits per hull cell.
- **[measured]** Per face cell the cubes visit 0.02–0.04 bits; per cell of the *effective* symmetric face (A/7.7, the
  notebook's law for O_h-symmetric soups, CLAIMS row on symmetric faces) 0.15–0.29, rising with size towards the
  asymmetric face law's 0.30. Symmetry spends area: a cube's 8 faces live in lockstep, so its face is effectively 7.7
  times smaller than it looks (single draws per side; scatter about 3×, notebook 2026-11-12).
- **[measured] The face law** (CLAIMS F4, ln τ_face = −0.091 + 0.2088·A, A = 27–90, GPU points to 135): an asymmetric
  face of A cells is alive for 2^(0.301·A − 0.13) generations; a seed whose life is one such face visits that many
  states: 0.296 bits per face cell at A = 27, 0.300 at 108, 0.301 at 459 (extrapolated), against one bit per cell in
  all of the face's own layer. An octahedral seed lives about as long as the sum of its successive faces' lives, which
  the first plateau dominates (68–80% of the expected life, notebook 2026-11-12), so per face cell of its first face it
  too visits about 0.30 bits (the 1.7–1.9× robustness of octahedral faces adds under 1 bit).


## C. A share of what?

**Exactly, in the listed vessels [proved].** The set of states that can occur after t generations is the image of
f^t (table above): 2^(0.86–0.95 N) after one generation, 2^(0.39–0.57 N) at the end. The *Shannon* entropy of the
time-t ensemble (uniform seeds pushed t steps; `entropy_t` in `data/vessels.jsonl`, computed for N ≤ 28 from exact
preimage counts) falls much faster, because most seeds pile into a few basins: in the 27-cell 3-layer slab
`slab_1_0_3_3` it is 0.92, 0.78, 0.47, 0.34 bits per cell at t = 1, 3, 10, 30. Restricted to the seeds not yet settled
(the "living" ensemble of a small vessel) it is 0.92, 0.81, 0.68, 0.49, 0.38 bits per cell at t = 1, 3, 10, 30, 40 —
and the living seeds themselves die off by a factor 2^-0.3 per generation. In the 28-cell hull record it is 0.34 bits
per cell at t = 10, 0.20 at t = 25. Small vessels have no long-lived ensemble: their "living" states thin out and
lose entropy together.

**For large faces [measured].** Living faces were sampled from a face slab: 8 {111} layers on the 16 × 16 in-plane
torus `slab 16 0 16 8` (A = 768 cells per layer, 6,144 cells; such a face never dies), soup 0.4, 2,000 generations of
burn-in, 32 replicas, snapshots every 3 generations. The numpy stepper (`qsd.py`) equals `oracle.step` on this slab
for 300 generations (`qsd.py validate 16 8 300`). Densities by layer, top to bottom: 0.518, 0.435, 0.406, 0.416, 0.416,
0.406, 0.435, 0.518 (the notebook's faces ≈ 0.51, bulk 0.4155). Estimator: conditional entropy of a cell given its K
nearest cells in a lexicographic past (the chain rule makes the sum over a unit cell's cells an upper bound on the
entropy per unit cell that decreases to it as K grows); plug-in counts pooled over translates and snapshots with the
Miller–Madow correction, and the same on half the data to show where the sample runs out. Checked first on fields
with a known answer on the same geometry (`qsd.py selftest 16 8`, 4,000 snapshots): iid Bernoulli(0.42), exact
0.9815, estimated 0.9815 for K ≤ 12; a causal Markov field with exact entropy 0.8474, estimated 0.8476 from K = 6 (where
the true context is complete) to K = 12, with the half-data column separating from the full one once bias sets in.

| K (context cells) | 0 | 4 | 8 | 12 | 16 | 18 | 20 | 22 |
|---|---|---|---|---|---|---|---|---|
| whole 8-layer face slab, bits per cell (256,000 snapshots) | 0.9851 | 0.9793 | 0.9717 | 0.9648 | 0.9610 | 0.9595 | 0.9580 | (0.952, biased: half-data 0.927) |
| top layer alone, its own marginal field (64,000 snapshots) | 0.9991 | 0.9916 | 0.9873 | 0.9866 | 0.9862 | 0.9860 | (0.983, biased) | |

- **[measured]** The top layer of a living face, seen by itself (its own marginal field, *not* conditioned on the
  layers under it), carries **0.986 bits per cell** (flat to ±0.0005 from K = 10 to 18). A face of A cells can show
  about 2^(0.986·A) different top layers. Conditioned on the layers above it, a layer carries 0.945–0.962 (review).
- **[measured]** The whole face slab carries **at most 0.958 bits per cell** (K = 20; full and half samples agree to
  0.0007), still falling by about 0.0015 per two context cells; the limit is probably 0.94–0.958 [conjectured lower
  end]. The chaos keeps nearly all of the entropy a cell can have.
- **[measured] Deficits against coin flips of the same density** (an upper bound on the entropy is a lower bound on
  the deficit; review's own sampler and ordering, `research/audit/REVIEW-statespace.md` §6): one layer seen alone
  falls short by at least 0.013 (top layer), 0.008 (the next), 0.006 (a bulk layer); the 8-layer slab jointly by at
  least 0.027 and still growing with K — most of the slab's redundancy lives in the correlations *between* layers.
- So: **one layer of a face of A cells has about 2^(0.99·A) typical configurations, and a seed's orbit shows at most
  2^(0.30·A) of them before the face dies: at most a share 2^(−0.69·A) of even one layer's configurations** (2^−33 for
  A = 48, 2^−390 for the side-13 hull's A = 570). This is a bound on one layer only. The seed's states are states of the
  whole vessel: of the typical states of a chaotic region D layers deep (at least 2^(0.95·D·A)) it sees a share of
  order 2^(−0.95·D·A), and of the vessel's 2^N far less (corrected 2026-11-15, review).

Not done: the quasi-stationary ensemble of a *small* face conditioned on survival (A = 48–108) was not sampled; the
large face stands in for it (entropy per cell is intensive), which is an assumption.


## D. Against chance

Uniform random map on M = 2^N states (expectations): visits 1.2533·√M states from a random start before repeating;
a share e⁻¹ = 0.368 of states has no predecessor; √(πM/2) states lie on cycles; about ½ ln M + 0.635 cycles
(corrected 2026-11-15, review: + 0.29 was written before, giving 10.7 and 9.6 where 11.0 and 10.0 are right).

| vessel | N | visited, mean (random map) | no predecessor (e⁻¹) | on cycles (random map) | cycles (random map) |
|---|---:|---|---|---|---|
| `hull_-1_3_-5_1_-5_1_-1_7` | 30 | 8.35 (41,068) | 0.929 (0.368) | 7,875 (41,069) | 5,900 (11.0) |
| `slab_1_0_3_3` | 27 | 10.22 (14,520) | 0.619 | 44,191 (14,520) | 22,651 (10.0) |
| `slab_5_1_1_2` | 30 | 14.41 (41,068) | 0.787 | 8,386 (41,069) | 5,435 (11.0) |
| `slab_5_1_2_1` | 30 | 8.57 (41,068) | 0.881 | 56,067 (41,069) | 41,768 (11.0) |
| `torus_5_2_1_1_0_2` | 30 | 8.12 (41,068) | 0.816 | 3,508 (41,069) | 2,118 (11.0) |

**A fairer yardstick** (review §7): gump's image after one step is only 2–43% of the states, and a random map with the
same in-degree sequence (each step lands on y with probability d_y/M) repeats after about √(πM²/(2 Σ d_y²)) steps
(a birthday approximation, not a simulation):

| vessel | uniform random map | random map with gump's in-degrees | gump, mean visited |
|---|---:|---:|---:|
| `slab_3_1_1_3` | 14,520 | 777 | 7.99 |
| `slab_1_0_3_3` | 14,520 | 1,651 | 10.22 |
| `torus_9_2_1_4_0_1` | 14,520 | 18 | 6.86 |
| `hull_-1_3_-5_1_-5_1_-3_5` (29) | 29,040 | 375 | 7.42 |

- **[proved]** At every listed size gump visits thousands of times fewer states than a *uniform* random map, but only
  2.6–160 times fewer than a random map with its own in-degrees: most of the gap is the concentration of
  in-degrees (in the 27-cell torus 7% of all states map straight to the empty state), not the dynamics (corrected
  2026-11-15, review). Gump also has far more
  states without a predecessor (0.57–0.98 against 0.37 at N ≥ 15), and has hundreds to thousands of times more
  distinct cycles: a random map has a handful of big cycles, gump a crowd of tiny ones (local still lifes and
  oscillators: of the cyclic states, a median 92% have period ≤ 2 over the 174 vessels of N ≥ 15, at least 68% in each). The number of
  states on cycles is on the random map's scale, 2^(N/2), above it in the slabs and kagome tori, below it in hulls
  and 3D tori.
- **[measured] Large vessels.** The face law visits 2^(0.30·A), the cubes 2^(0.15–0.29·A/7.7). A random map on one
  layer's 2^A states would visit 2^(A/2), but a layer is not an autonomous map (it is driven by the layers beneath
  it); a random map on the states the face actually lives in would visit at least 2^(0.47·D·A), so gump explores
  less than chance by far more than the one-layer factor 2^(0.2·A) suggests, and that factor should not be quoted
  (corrected 2026-11-15, review). The face's own states are not few: 2^(0.99·A) per layer seen alone (section C). It
  is not a shortage of states that ends a seed's exploration but the chance of the face going quiet.

## E. Forecasts, scored

Forecasts are in `PREDICTIONS.md`, written before any enumeration; numbers from `python3 research/statespace/score.py`.

| | forecast (chance) | outcome |
|---|---|---|
| E1 | almost every state has no predecessor; states with one grow as 2^(sN), s 0.75–0.95 (70%) | **fails.** 57–98% have none, and log2 \|f(S)\| rises with slope 0.95–0.98 per cell (only the kagome tori, 0.949, inside): the first step removes a roughly constant *fraction*, not a per-cell rate |
| E2 | cyclic states 2^(aN), a 0.2–0.5; almost all period 1 or 2 (55%) | **half.** a = 0.22, 0.33, 0.48 in the 3D tori, 2-layer slabs, kagome tori; 0.58 in hulls and 0.52 in 3-layer slabs. Period ≤ 2: median 92% of cyclic states, minimum 68% |
| E3 | longest/mean transient at least doubles from smallest to largest listed (60%) | **holds** in 4 of 5 families (hulls 2.6 → 8.6, kagome 1.8 → 7.5, 3D tori 1.4 → 7.4, 3-layer slabs 2.5 → 6.0); 2-layer slabs 3.46 → 6.82, ×1.97 |
| E4 | mean settling time already exponential in face cells, rate 0.15–0.25 (40%) | **fails.** Fits of ln(mean transient) give 0.06 per cell (hulls), 0.07 (kagome), 0.08 (tori), below the band; the 3- and 2-layer slabs' 0.20 and 0.17 come from 3–5 points that bend down. (A slow exponential and a line fit about equally well, review) |
| E5 | the champion has no symmetry of the vessel (65%) | **holds** in every vessel of ≥ 19 cells (first 64 champions each); a few smaller vessels have symmetric champions |
| E6 | more than half the eventual loss in bits within three generations (60%) | **fails as a rule.** True in 143 of 152 hulls of ≥ 15 cells and 5 of 6 kagome tori; false in every 2- and 3-layer slab (26–36%) and 4 of 6 3D tori |
| E7 | a seed visits fewer than 2^(A/2) states, gump explores less than chance (75%) | **holds** for the face law (0.30 < 0.5 per face cell), the cubes, and the mean seed of every listed slab (A = N/m). One exception: the 27-cell 3-layer slab's champions visit 52–53 > 2^4.5 states |
| I1 | the empty state has the largest basin everywhere; more than half the seeds in every hull (60%) | **fails.** Two hulls (28, 30 cells) have a still life's basin largest; in 72 of 226 hulls of ≥ 9 cells, including 41 of the 43 hulls of ≥ 25 cells, the empty state drains under half (as little as 23%) |
| I2 | mean transient below 12 everywhere, not exponential (70%) | **fails narrowly**: the 2-layer 30-cell slab's is 12.91; the second half holds |
| I3 | longest transient below 2N everywhere (55%) | **fails**: 56 at N = 24 and 88 at N = 30 (2-layer slabs), 61 at N = 30 (hull) |
| I4 | more than 80% without predecessor at N ≥ 15 (85%) | **fails**: 57–79% in the 2- and 3-layer slabs |
| I5 | cyclic states fewer than √(πM/2) at N ≥ 20 (60%) | **fails** in 9 of 108 vessels (3-layer slabs, kagome and 2-layer tori: up to 3× more) |
| I6 | champion below 0.25, mean seed below 0.15 bits per cell at the largest N (60%) | **holds**: 0.17–0.22 and 0.09–0.13 |
| I7 | entropy per cell of the living ensemble 0.80–0.95, bulk and top layer (60%) | **fails**: the top layer carries 0.986; the slab at most 0.958 — the chaos is closer to random than forecast |


## What each number rests on, and what was not checked

- **What the exact numbers rest on.** `enum.c` (one table of f over all 2^N states) and `vessels.py` (the neighbour
  lists); checked against `reference/oracle.py` on 40 random states × 40 generations and the champions of every
  vessel, by the full champion trajectories of all 301 vessels on the oracle alone, by T10's vertex star, by
  identical maps for symmetric lattices, and by `research/theory/exhaust.c` on eight tori. Not every state was
  stepped by the oracle; a bug that touches only rare states would need a state the checks did not draw.
- **Not enumerated:** hulls wider than 6 layers along some diagonal (thin needles of few cells exist); 8 of the 14
  hulls of 30 cells; anything above 30 cells (the table needs 4·2^N bytes; N = 32 would need 16 GB). Exact Shannon
  entropies of the time-t ensemble only for N ≤ 28.
- **Symmetry of champions** was tested on the first 64 champions of each vessel against the lattice symmetries that
  map the vessel to itself (`Vessel.symmetries`), not against all graph automorphisms; orbit counts are given only
  when all champions were listed (≤ 256).
- **Part B** uses the face law and the symmetric-soup law (A/7.7) as recorded in the notebook and CLAIMS (F4 and the
  symmetric-face entries), not re-measured; each cube is a single draw with about 3× scatter in lifetime. The cube
  numbers themselves (cycle start and period) are exact runs of the engine, which matches the oracle and the legacy logs
  through side 13.
- **Part C:** the slab entropy is an upper bound still falling at K = 20 (0.958); the limit was not reached, and no
  lower bound was computed. The faces sampled are large (A = 768) and never die; the entropy of small faces
  *conditioned on survival* was not measured. One sample, one in-plane lattice (16 × 16), one soup density (0.4).
- **The conjectured junction** of the listed (linear) regime with the face law (exponential) near A ≈ 30–40 cells
  per face is not tested: no vessel in between was enumerated or sampled for this.


## Reproduce

```
cc -O2 -march=native -o research/scratch/ss_enum research/statespace/enum.c -lm
cd research/statespace
python3 vessels.py hulls 40 6 > ../scratch/ss_hulls40.txt        # every hull <= 40 cells, <= 6 layers wide (data/hulls_W6_upto30.txt)
python3 run.py list hull | while read k a; do python3 run.py one $k $a --family hull; done   # also slab3all slab1 slab2 torus
python3 run.py one hull -1 3 -5 1 -5 1 -3 5 --family hullbig     # one vessel: validate, enumerate, champion file
python3 analyze.py tables; python3 analyze.py hullsizes; python3 analyze.py scaling; python3 score.py
python3 champion.py data/champions/slab_3_1_1_3.txt               # a champion on the oracle alone
python3 large.py                                                  # part B tables (needs research/scratch/ss/cube14.json, cube15.json:
                                                                  #   engine/target/release/gump run --cube 14 --lite | tail -1)
python3 qsd.py validate 16 8 300; python3 qsd.py selftest 16 8    # part C stepper and estimator checks
python3 qsd.py sample 16 8 256000 3 2000 2 ../scratch/ss/qsd_P16_M8_big.npz
python3 qsd.py entropy ../scratch/ss/qsd_P16_M8_big.npz 0,1,2,3,4,5,6,7 24
python3 qsd.py entropy ../scratch/ss/qsd_P16_M8.npz 7 22          # top layer alone (64,000-snapshot sample, seed 1)
python3 figure.py
```
Times on one core: a 27-cell vessel 50–65 s, a 30-cell one 3–4 min (6.4 GB); the hull census ≤ 27 cells about 25 min.
