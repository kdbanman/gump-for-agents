# Follow-up of the class statement: outcomes, scored against PREDICTIONS.md

*Class follow-up agent, 2026-11-14.* Forecasts: `PREDICTIONS.md` (commit 59e0683, before any production run).
Names: **gump** is the 2012 rule as coded (coplanar neighbours touching at a corner); **face12e** has the coplanar
neighbours sharing an edge; face12e is not gump. Clause numbers refer to the seven-clause summary of
`research/theory/class.md`.

**Code and trust.** Stepper `fu.c` (64 bit-sliced replicas on any cell graph, plus bit-sliced peeling for the largest
dead sealed set). `python3 fu.py validate` → ALL OK: offsets of kagome4, kagome8, hex9 equal to
`research/theory/class/lattices.py`, of face12e and bond10 to `research/audit/class/seal.py`; `fu_step` equals an
independent numpy gather stepper **and** the review's `aud_step` cell for cell, 100 generations × 64 replicas, on 9
vessels of 5 lattices (tori, strips, boxes); bit-sliced peeling equals plain set peeling on 480 states. `fu_life`
reproduces the review's box medians exactly when given the same seed (face12e 4³: 439, quartiles 279–594; bond10
3³ B34/S234: 262.5, 146–511), as it must (same RNG construction). All runs below use other seeds unless said.
All commands are run from `research/theory/class/followup/`; outputs in `research/scratch/class_followup/`; tables
by `python3 analyse.py slab FILE [nwalls] [sizekey]` and `python3 analyse.py life FILE`.

**Waiting-time method (every slab, strip and column).** Replicas start as soups of density 0.45 and are reseeded
when they end. Every 8 generations the largest dead sealed set D is computed. Endings: *wall death* (D contains a
whole layer parallel to the walls within depth 3 of a wall in 2D, depth 1 in 3D; counted), *deep firewall* (a whole
layer deeper inside; censored), *cut* (D meets both walls, contains no whole layer; censored), *pit* (any other
nonempty D; censored), *periodic* (equal to the state two generations back or to a snapshot taken at a power-of-two
age; censored), and, for kagome4 only (§2), *frozen wall* (both wall rows unchanged between t − 2 and t at 128
consecutive checks = 1,024 generations; censored). τ per wall = (walls) × exposure / wall deaths, exposure at age > 200;
error on ln τ = 1/√deaths. Hazard = τ in three or more consecutive age bins (log2 bins merged to ≥ max(20, deaths/5)
deaths each). "Oldest" = age of the oldest replica alive at the end.

## 1. kagome8 and hex9 at b = 4

**Confinement (P1.1): holds.** `python3 two_d.py confine LAT c` (192 soups of density 0.5 in hexagonal seeds of
radius 3, 4, 5, free space on a 96-torus, 300 generations, each cap 5–8): **0** soup-generations with a live cell
outside the position-aware hull, for all 8 (lattice, cap) pairs. Outside the position-free polygon: 64 … 26,298
(kagome8), 975 … 36,987 (hex9); beyond the seed's support in eight unsealed directions: 98 … 56,289. The test can
see an escape; none occurred.

**Torus (P1.2; clause 4 predicts nothing).** `python3 two_d.py bulk LAT c` (64 soups × 4 densities 0.2–0.65,
4,096 generations; kagome8 12,288 cells, hex9 10,584):

| cap | kagome8 | hex9 |
|---|---|---|
| 5 (B4/S34) | dies (density ≤ 0.014) | dies |
| 6 (B45/S345) | dies or freezes (1 of 64 soups aperiodic, activity 0.002) | dies (debris 0.07) |
| 7 (B456/S3456) | **glass**: 7–18 of 64 aperiodic, ρ = 0.677, activity 0.013 | **chaotic**: 64/64 aperiodic from 0.35–0.65, ρ = 0.537, activity 0.48 (from 0.2: 19/64, a dilute basin) |
| 8 (B4567/S34567) | freezes (ρ = 0.77, 0/64 aperiodic) | **chaotic**: 64/64, ρ = 0.619, activity 0.45 |

My guess was 0.35 for a chaotic in-reach cap on each: kagome8 has none (the b/K ≤ 3/8 regularity holds there), hex9
has one (c = 7; a third exception to that regularity after vn and kagome4, b/K = 0.44).

**hex9 B456/S3456 (c = 7) strips (P1.3): the wall dies whole and memorylessly; ln τ is exponential in the wall
length but not a straight line.** `./run_hex9.sh` (strips between the sealed walls of direction u = (2, 1),
2n + 7 values of u·p deep, n = wall cells; n = 18 rerun at depth 41, see "dead ends"):

| n | wall deaths | ln τ | CV | τ by age bin (deaths) | cuts / deep firewalls / pits / periodic | oldest |
|---|---|---|---|---|---|---|
| 8 | 74,854 | 6.121 ± 0.004 | 0.97 | 503, 436, 434 | 10,634 / 23,638 / 2 / 110 | 904 |
| 10 | 48,542 | 7.505 ± 0.004 | 0.99 | 1,880, 1,770, 1,790 | 20,105 / 12,285 / 1 / 6 | 2,816 |
| 12 | 34,408 | 8.822 ± 0.005 | 1.01 | 6,760, 6,760, 6,810 | 12,248 / 7,391 / 0 / 0 | 8,496 |
| 14 | 22,015 | 10.023 ± 0.007 | 1.01 | 22,900, 22,400, 22,400 | 13,358 / 2,871 / 0 / 0 | 23,640 |
| 16 | 17,983 | 11.162 ± 0.007 | 1.00 | 70,900, 70,500, 69,900 | 16,279 / 1,287 / 0 / 0 | 80,448 |
| 18 | 12,329 | 12.239 ± 0.009 | 1.00 | 206,000, 207,000, 205,000, 210,000 | 15,395 / 482 / 0 / 0 | 213,584 |
| 20 | 8,656 | 13.289 ± 0.011 | 1.02 | 580,000, 600,000, 597,000, 590,000 | 6,006 / 181 / 0 / 0 | 835,984 |

Local slopes per wall cell: 0.692, 0.658, 0.601, 0.569, 0.538, 0.525 (± 0.003–0.007): the law is **concave** —
the cost per wall cell falls by a quarter over seven nats of ln τ; a straight line is rejected (χ² ≈ 2,900 on 5 dof).
Memorylessness is clean at every size (hazard flat to 3 %). Pits: 3 in 215,000 permanent events — none at the larger
sizes. 90–99 % of wall deaths are the outermost pair of layers; the rest are the next pair dying under a live
outer pair (`walls_by_depth` in the JSON). By the scoring of P1.3 this **holds** (memoryless, wall death not pits,
ln τ rises by 7.2); "ln τ linear in the wall's length" holds only as "exponential with a slowly falling rate". Hull
lifetimes (P1.5, `python3 two_d.py life hex9 7 R 4000000`, hull of the hexagonal seed of radius R): medians 24, 88,
355, 727, 1,195, 4,102 at R = 2 … 7 (all 64 finished each), final density 0.29 → 0.04: growing, sparse debris; the
hull's sides are of unequal length (its first side dies within 16–330 generations), so this is not a clean rate test.
*Not run:* kagome8's two strip orientations at a chaotic cap (there is none).

**Armour (P1.4): holds as stated, with a twist.** At c = 8 the hull and the strips of hex9 have an armoured core (the
outer pair of layers, degrees 6 and 7 ≤ c − 1). In strips (`two_d.py slab hex9 8 B n 2n+7 G`): the outer pair sits at
density **1.000** in every old replica and **never dies** (0 events at depth 0–1), but the pair beneath it dies, memorylessly:
ln τ = 6.943 ± 0.003 (n = 10, 162,970 deaths, CV 0.99), 10.606 ± 0.013 (n = 14, 6,269 deaths, CV 1.00, hazard flat),
FILL(n = 12, 16). So under armour the chaos still recedes, layer band by layer band, at 0.92 per wall cell — it peels
*off* the immortal skin. Clause 3 is right that the armoured wall is immortal and silent about this. kagome8 at
c = 7, 8 (not chaotic): every strip replica freezes or dies before the burn-in.

## 2. kagome4 B2/S12 (b = 2), strips 41 rows deep

**A third ending the review's strips did not separate: the wall freezes.** Without freezing censored
(`two_d.py slab kagome4 3 A n 40 G 3`, `kagome4_slab.jsonl`), the hazard falls with age (n = 6: τ 3,650 → 18,900
from the youngest to the oldest bin; n = 14: 1.8 × 10⁶ → 4.5 × 10⁶) and the CV is 1.06–1.12. `python3 strip_state.py
kagome4 3 A 8 40 300000` (64 strips, no reseeding) shows why: in the survivors the two wall rows lock into a static
pattern of density 0.667 (activity 0.000 at age 10⁵ in all 5 survivors), and the freeze spreads inward (rows 2–5
static too, rows 6–11 activity 0.22, deeper 0.42). A frozen wall is not an armoured set of Theorem E (the wall row has
degree 2 and no neighbour in its own row; the armoured core is empty for c ≤ 4); it is a dynamically formed wall.

**With frozen walls censored the law is straight and memoryless (P2.1 holds in number; its stated mechanism was
wrong).** `./run_kagome4b.sh`:

| n | wall deaths | ln τ | CV | τ by age bin | frozen (censored) | cuts / pits / periodic | oldest |
|---|---|---|---|---|---|---|---|
| 6 | 13,877 | 8.285 ± 0.009 | 0.97 | 3,760, 4,050, 4,090 | 5,616 | 0 / 0 / 0 | 6,136 |
| 8 | 6,442 | 9.867 ± 0.013 | 1.02 | 18,500, 19,200, 19,400, 20,100 | 2,850 | 0 / 0 / 0 | 24,776 |
| 10 | 2,834 | 11.405 ± 0.019 | 1.01 | 89,500, 89,100, 90,800 | 1,146 | 0 / 0 / 0 | 138,056 |
| 12 | 1,191 | 12.970 ± 0.029 | 0.98 | 427,000, 422,000, 435,000 | 447 | 0 / 0 / 0 | 1,202,520 |
| 14 | 582 | 14.380 ± 0.042 | 0.98 | 1.96, 1.61, 1.69 × 10⁶ | 203 | 0 / 0 / 0 | 3,449,536 |
FILL

**Slope FILL per wall-row cell** (weighted fit; local slopes 0.791, 0.769, 0.783, 0.705 ± 0.008–0.025), i.e. FILL per
cell of the two-row band (3n cells). Forecast 0.70 ± 0.08: inside. The forecast's reason (cuts) was wrong: at 41 rows
there are no cuts at all; the drift of the review's 17-row series came from walls that froze and from settled strips.
Freezing is itself a competing ending with nearly the same size dependence (frozen / wall deaths = 0.40, 0.44, 0.40,
0.38, 0.35 at n = 6 … 14): in a hexagon roughly a quarter to a third of the walls will freeze rather than die.
Freezing censor checked for sensitivity: 256 instead of 1,024 frozen generations changes ln τ at n = 8 by 0.02
(9.853 vs 9.872 ± 0.023). Depth: FILL. No pits (P2.2 holds).

## 3. bond10 at its tight b = 3

**Slab law, cuts censored (B34/S234, c = 5)**, `./run_bond10.sh`, slab of 4 cubes, periodic wall of A faces:

| A | wall deaths | ln τ | CV | τ by age bin | cuts / deep / periodic | oldest |
|---|---|---|---|---|---|---|
| 9 | 2,527 | 4.616 ± 0.020 | 0.92 | 122, 84, 87 | 11 / 195 / 36 | 224 |
| 12 | 32,036 | 6.156 ± 0.006 | 0.98 | 515, 462, 452 | 772 / 1,849 / 136 | 656 |
| 16 | 21,412 | 8.050 ± 0.007 | 1.01 | 3,130, 3,010, 3,200, 3,190 | 317 / 720 / 46 | 10,280 |
| 20 | 10,614 | 10.072 ± 0.010 | 0.99 | 24,000, 23,400, 23,900, 23,300 | 609 / 215 / 10 | 60,616 |
| 25 | 1,689 | 12.620 ± 0.024 | 1.01 | 310,000, 304,000, 297,000 | 89 / 12 / 0 | 642,752 |
| 30 | 400 | 15.161 ± 0.050 | 0.91 | 3.95, 4.08, 3.14 × 10⁶ | 130 / 1 / 0 | 4,371,288 |

Slope **0.492 ± 0.001 per wall face** (local 0.51, 0.47, 0.51, 0.51, 0.51), memoryless; the review's 8.04 and 12.71
at A = 16, 25 are reproduced within 0.09.

**Forecast P3.1 from this law (walls independent) fails, and the reason is found: in a box the walls hold each other
up along the edges.**
- *Columns* (walls on x and y, periodic in z; `three_d.py column bond10 5 n m G`), τ per wall at wall area A = n·m:
  A = 9 (3 × 3): ln τ = 7.795 ± 0.003 against the slab's 4.616 (24× tougher); A = 12 (3 × 4): 10.359 ± 0.006 against
  6.156 (67×); A = 16 (4 × 4): 13.33 ± 0.02 against 8.05 (196×). Memoryless (CV 0.98–1.03). The excess is 0.52–0.66
  nat per cube of edge.
- *Why* (`python3 structure.py bond10`, `python3 box_state.py 4 box|column`): the wall that dies is a sheet plus the
  layer beneath it, and in a box the layer beneath a sheet contains the edge rows of the four neighbouring walls'
  sheets. Vessel degrees stay 5 and 10 everywhere (edges lower no degree, so this is not Theorem E armour at c = 5),
  but the edge rows are dense — **0.67–0.71** in a 4³ box against 0.50 for sheet cells away from edges and 0.37–0.40
  beneath — and in a 4³ box 12 of each wall's 16 sheet cells are edge-row cells. A wall cannot die while its
  neighbours' edge rows live, and they live as long as their own walls do.
- *Boxes.* 3³ (`python3 box_hazard.py 3 1000000 4`, 256 boxes, settling censored): first permanent wall death
  ln τ per wall = 7.87 ± 0.07 — equal to the 3 × 3 column, not the slab (4.62); 29 of 256 boxes settle into a
  periodic state before any wall dies; median lifetime 292 (quartiles 142–515, seed 2). 4³ (`three_d.py box bond10
  5 4 1e7 2 64`): **no permanent dead set of any kind in 64 boxes × 10⁷ generations** (none finished; FILL long run);
  so τ per wall > ~1 × 10⁹, against 3,100 in the slab and 6 × 10⁵ in the 4 × 4 column. The box of 4³ and larger is out
  of reach not because it cannot die but because each wall carries four edges.
- *c = 6 (B345/S2345), P3.2: holds.* Every box has a 24-cell armoured core (three sheet cells at each corner,
  degree 5 = c − 1). `three_d.py bond10c6 n 200000`: 3³ boxes freeze at median 17 generations, 4³ at 2,063, every one
  of 64 + 64 with the core fully alive, no wall sheet dead, final density 0.60 and 0.52.

## 4. face12e B45/S345 (not gump)

FILL

## Where the revised class statement is wrong or silent

FILL

## Dead ends and corrections made during the work

- The first hex9 strip at n = 18 was built 43 deep; my sealing test looked only at a window of the plane that did
  not reach u·p = 43 and wrongly called that position sealed, so the strip's top was a lone, unsealed layer
  (ln τ came out 7.3). Fixed in `structure.sealed_C` (sealing is periodic in C; the test now reduces C); the
  record is kept in `hex9_c7_slab_INVALID_unsealed_top.jsonl`; every other strip was at a truly sealed position
  (checked after the fix); n = 18 rerun at depth 41.
- "Wall death = the boundary layer in the dead sealed set" missed deaths of the second band under a live outer
  band (hex9) — classification widened to any whole parallel layer within depth 3 (2D) / 1 (3D), deeper ones
  censored as firewalls.

## Not checked

FILL
