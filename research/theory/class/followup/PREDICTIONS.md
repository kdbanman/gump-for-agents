# Follow-up of the class statement: forecasts, committed before the production runs

*Class follow-up agent, 2026-11-14.* The statement tested is the seven-clause summary of `research/theory/class.md`
(revised 2026-11-14), cited as clause 1 … 7. Names: **gump** is the rule as coded in 2012 (coplanar neighbours
touching at a corner); **face12e** has the coplanar neighbours sharing an edge. face12e is not gump.

**What I had seen when writing this.** class.md, `research/audit/REVIEW-class.md` (§1.2, §2, §2.4, §5) with its raw
outputs in `research/scratch/audit-class/` (kagome4 strips and hexagons, bond10 at b = 3 slabs and boxes, face12e
slabs and boxes), `PREDICTION-repaired.md`, `research/STATUS.md` storyline item 4 (gump's symmetric soups). Before
writing I ran only exact, dynamics-free computations: `python3 fu.py validate` (stepper check) and
`python3 structure.py 2d`, `python3 structure.py bond10` (sealing by direct count, layer structure, forward counts,
finite sealed sets by peeling, armoured cores; output in `research/scratch/class_followup/structure2d.txt`). No
soup has been run on kagome8 or hex9 by anyone. For items 2–4 the review's rough numbers were known to me; where a
forecast is made from them, the forecast says which of its inputs it uses.

Conventions for every waiting time below: τ per wall = (number of walls) × exposure / wall deaths, exposure
counted at age > 200; error on ln τ = 1/√deaths; a size with fewer than 20 deaths is not a point. A replica ends
at the first check (every P generations) at which the largest dead sealed set D (bit-sliced peeling, `fu.c`) is
nonempty; it is a **wall death** if D contains every cell of a boundary layer, a **cut** if D meets both walls
otherwise, a **pit** otherwise; cuts, pits and replicas periodic with any period (state equal to the one two
generations back or to a snapshot taken at a power-of-two age) are censored and reseeded. "Memoryless" = CV of the
waits in [0.8, 1.25] **and** τ in each of at least three age bins within a factor 1.5 of the mean.

## Exact facts the forecasts rest on (`structure.py`, no dynamics)

| | kagome8 (K = 8, 3 types), b = 4 | hex9 (K = 9, 2 types), b = 4 | kagome4 (K = 4), b = 2 |
|---|---|---|---|
| sealed half-spaces | 12 directions, C even (direct count agrees with `seal.py`) | 6 directions, C ≡ 0, 2 (mod 3) | 6 directions, C even |
| full-lattice forward count (C1) | 4 = b: no finite sealed set | 4 = b: none | 2 = b: none |
| wall layers (outermost first) | orbit A (u = (1,0)): degrees 4, 7, 8; orbit B (u = (2,1)): 4, 6, 6, 8 | 6, 7, then 9 | 2, 4 |
| C1 certificate at a wall (v = ±g ± εu) | none (best 3, 2 < b) | none (best 3) | yes (2) |
| finite sealed set at one wall, peeling windows of 15 periods × up to 10 layers | none found | none found | none found |
| shortest transverse cut (full-width window) | 2 periods | 4 periods | 2 periods |
| armoured core (Theorem E), strips | none for c ≤ 7; orbit A from c = 8 (wall + next row); orbit B none at c = 8 | none for c ≤ 7; from c = 8 | none for c ≤ 4 |
| armoured core, hull of a hexagonal seed (R = 3, 5) | none for c ≤ 7; 48, 84 cells at c = 8 | none for c ≤ 7; 42, 78 at c = 8 | none for c ≤ 4 |

bond10 at b = 3 (box with walls at odd coordinates): every cell of a box has vessel degree 5 (wall sheets, no
in-sheet neighbour) or 10, at every size 2³ … 5³ — the box edges do not lower any degree. Armoured core: none at
c = 4, 5; **24 cells at c = 6, 7 in every box** (the corner cells of the sheets). Sealed: a sheet with the layer beneath
(and unions of such bands); not the sheet alone, not an edge or corner piece.

## Item 1 — kagome8 and hex9 at b = 4

Caps within reach and free of armour (Theorem-E form of clause 3): **c = 5, 6, 7** on both lattices
(B4/S34, B45/S345, B456/S3456). c = 8 has an armoured core in the hull on both.

- **P1.1 (clause 1, proved).** Every finite pattern stays in the intersection of the sealed half-spaces containing it,
  at every cap. *Refuted by* a single live cell outside, in any soup at any generation. Expected: 0 escapes; and
  many soup-generations outside the tight (position-free) polygon and outside the seed's support in unsealed
  directions, showing that the test can see an escape.
- **P1.2 (clause 4: no prediction).** Whether the torus is chaotic at c = 5, 6, 7 is not predicted. My guess, from
  the b/K ≤ 3/8 regularity of class.md §5 (kagome8 b/K = 0.50, hex9 0.44, both on the "unlikely" side; vn and
  kagome4 are the exceptions): a chaotic in-reach cap exists with probability 0.35 on each lattice.
- **P1.3 (clauses 2, 3, 5), conditional on a chaotic torus at c ∈ {5, 6, 7}.** In strips between two sealed walls the
  wall dies as a whole (wall deaths, no pits), memoryless, ln τ linear in the wall length at four or more lengths,
  slope > 0. Pits are not excluded by a proof (no C1 certificate at a wall), only by the peeling search; *refuted* if
  pits are ≥ 10 % of the permanent events at the largest length, or if wall deaths are not memoryless, or if ln τ
  does not rise by ≥ 1 over the lengths run. Clause 5 does not say how large the slope is; my guess 0.2–0.8 per
  cell of the outermost layer.
- **P1.4 (clause 3).** At c = 8, where the hull has an armoured core (and the orbit-A strip of kagome8 too, and hex9's
  strip): no wall death in orbit-A strips of kagome8 or in hex9 strips, if anything stays alive after the burn-in.
  kagome8's orbit-B strip has no armour at c = 8: clause 3 is silent there.
- **P1.5 (clause 6), if P1.3 holds.** Median hull lifetimes grow at a rate per unit of hull side comparable with the
  strip slope; endings sparse.

## Item 2 — kagome4 B2/S12, strip law with cuts censored

The review's strips (17 rows, cuts not censored) gave ln τ = 7.24, 8.77, 10.27, 11.59, 12.85 at n = 4 … 12 wall-row
cells, local slope 0.77 → 0.63, CV drifting to 1.23. Shortest transverse cut: 2 periods of the strip (exact), so in
17-row strips cuts compete from n ≈ 8.

- **P2.1.** With cuts censored and strips deep enough that cuts are rarer than wall deaths, the wall death is
  memoryless at every length (CV in [0.8, 1.25], flat hazard), and ln τ is linear in n with slope **0.70 ± 0.08 per
  wall-row cell** (≈ 0.23 per cell of the two-row band) over n = 6 … 16; the concavity of the review's series is the
  cut contamination. *Refuted by* a local slope that still falls by more than its errors allow between the first and
  the last pair of lengths, or by CV outside the range.
- **P2.2.** No pits (C1 certificate at the wall exists, so none can occur).

## Item 3 — bond10 at its tight b = 3

Slab law (review, periodic slabs 4 cubes deep, A wall faces): c = 5 ln τ = 8.04, 12.71 at A = 16, 25 → 0.52 per wall
face; c = 6: 7.78, 12.23 → 0.49.

- **P3.1 (forecast from the slab law, walls independent).** A box of n³ has six walls of n² faces; the first wall
  death comes after τ(n²)/6, later ones are shorter (smaller walls). c = 5: ln τ(A) ≈ 8.04 + 0.52 (A − 16) gives
  τ(4) ≈ 6, τ(9) ≈ 80, τ(16) ≈ 3,100, τ(25) ≈ 3.3 × 10⁵; box median lifetimes **2³: ≲ 10, 3³: 20–60, 4³: 600–1,500,
  5³: 5 × 10⁴ – 1.5 × 10⁵.** The review's measured 3³ = 262 and 4³ > 300,000 already contradict this at 3³ (× 5–10)
  and 4³ (× > 200). So the forecast is expected to fail; the question is why.
- **P3.2 (clause 3) at c = 6.** Every box has a 24-cell armoured core at its corners, one corner piece in every wall's
  sheet. Clause 3 predicts: once the core is alive no wall of the box can die, so a c = 6 box ends frozen with its
  corners alive (dense endings) unless walls die before the core forms; lifetimes do not follow the slab law.
  *Refuted by* a c = 6 box whose final state has a dead corner piece with all walls dead, after the core was alive.
- **P3.3 (hypotheses for c = 5, to be tested).** H1: the box wall band is larger than the slab's (the layer beneath
  a sheet includes the edge cells of the four neighbouring walls' sheets): predicts box walls tougher by a factor
  e^{0.17 × extra cells} ≈ 4 at 4³ — *not enough*, so H1 alone is refuted if box walls are > 20× tougher. H2: a wall
  cannot die while a neighbouring wall lives (edge support): predicts that "columns" (two pairs of walls, periodic in
  the third axis) are as robust as boxes and far more robust than slabs of the same wall area, and that in boxes the
  first permanent event, if any, is never a single wall. H3: boxes never die at all at c = 5 beyond 3³ (an absorbing
  state not reachable): refuted by any 4³ box reaching an empty or periodic state, or any permanent wall death.
  My guess before running: H2, 50 %.

## Item 4 — face12e B45/S345

- **P4.1 (box of 7³).** From the wall law (local slope 0.41 per wall face; ln τ(49) = 14.54 + 0.41 × 13 = 19.9 ± 0.4)
  and the measured ratio box median / τ(n²) = 0.37, 0.34 at 5³, 6³: **median ≈ 1.5 × 10⁸**; from the box series
  directly (ln of the 5³ → 6³ ratio per unit of n², 0.39, times 13): 1.1 × 10⁸. Forecast: **median 1.3 × 10⁸, 90 %
  interval 5 × 10⁷ – 3 × 10⁸.** Not reachable to the median in my budget (26,000 generations per second for 64
  replicas: ≈ 1.5 h of one core per 64 soups to reach 1.3 × 10⁸). Reachable test instead: 128 soups to T = 3 × 10⁷;
  with a roughly exponential lifetime distribution of median M, the expected number finished is 128 (1 − 2^(−T/M)):
  **15 (range 9–33) for M = 1.3 × 10⁸ (5 × 10⁷ – 3 × 10⁸).** *Refuted by* fewer than 5 or more than 45 finished.
- **P4.2 (O_h-symmetric soups).** In a symmetric state the six walls are copies of each other and die together, and
  each wall has about n²/8 independent faces (its stabiliser in O_h has order 8). Taking gump's result (one
  fundamental domain; ln τ_sym ≈ intercept + slope × A/|stabiliser|, intercept ≈ that of the asymmetric law, here
  ≈ 0) over to face12e: first wall death ln τ ≈ 0.41 n²/8, i.e. a few to a few tens of generations for n ≤ 8, so the
  box lifetime is the time to strip the walls one pair after another: **median lifetimes 10–100 for 4³ … 8³, growing
  slowly with n; at 6³ shorter than asymmetric soups by a factor ≥ 10³ (expected ~10⁴; asymmetric 707,038).**
  *Refuted by* a symmetric 6³ median above 7 × 10⁴ (less than 10× shorter), or by symmetric lifetimes growing with n
  as fast as the asymmetric ones (ln ratio per unit of n² ≥ 0.2). The symmetry of the state must be preserved at every
  generation (checked).
