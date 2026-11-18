# blast/holes: the price of a hole in a living face (agent `holes`, 2026-11-18, second phase)

The question: is the price per cell of a face's lifetime the bulk cost of emptiness in the living state,
−ln P(Ω empty at an instant) = c·|Ω| + σ·|∂Ω| + O(1) with c = 0.2087, and does the hull's 0.231 sit in the rim
rows of the living state? **Answer: no to both, at every size plain running reaches.** Labels: [proved],
[measured], [conjectured]. `S` below is `research/scratch/blast/holes` (binary: `gcc -O3 -march=native -o
$S/holes holes.c -lm`). Full tables: `data/torus_table.txt`, `data/hull_table.txt` (output of `ana.py`);
lifetimes: `data/life.txt`, `data/life_tori.txt`; forecasts: `PREDICTIONS.md`.

## 0. What stands

1. **The bulk cost of a hole is about 0.26 per cell, not 0.2087, and it is flat [measured].** On the 12 × 12 × 8
   torus, the mixed second difference of −ln P over rhombi of a × b unit cells (3ab cells; it removes every term
   that depends on a alone or on b alone, so perimeter and corners), per cell, is FINAL_M_SUMMARY. No value
   reached is inside the PI's 0.195–0.222. The earlier "0.226 at 36 cells, falling into the lifetime range"
   (notebook, 2026-11-15) was the second difference along a × a, a × (a+1), which is not free of the single-variable
   curvature (f(3,4) − 2f(3,3) + f(2,3) = −0.064).
2. **A hole pays more per cell than the death of a closed face of its own shape [measured].** Lifetimes of the
   small closed tori a × b measured with the same stepper (`data/life_tori.txt`) have mixed second differences per
   cell of 0.2148 ± 0.0014 at (3.5, 3.5) and 0.226 ± 0.005 at (3.5, 4.5); holes of the same shapes: FINAL_HOLE_M35.
   "−ln P(hole) − ln τ(closed torus of that shape)" is not a function of the perimeter alone: at perimeter 16 it
   is 8.77 (2 × 6), 9.42 (3 × 5), 9.55 (4 × 4). (For 3 × 6 against 4 × 5, the PI's pair, it is: 11.00 and 11.01.)
3. **The interior of a hull face is a wrapped face to one part in ten thousand per cell [measured].** In the hull
   of radius 29 (faces of side 15, 360 cells) rhombi of 12 to 27 cells with every unit cell three or more rows from
   every rim have the torus's −ln P to FINAL_INT; two rows in, the same; one row in, a 3 × 3 patch is 0.010 ± 0.002
   DEARER (11.995 against 11.985).
4. **The rim zone of the living state carries no surplus [measured].** A patch that touches the rim is CHEAPER:
   3 × 3 on the rim −0.98, in the corner −3.21; a strip against the rim is cheaper than the same rhombus in the
   interior by 0.33, 0.37, 0.39 per unit of rim for 1, 2, 3 rows. The rim row itself costs 0.436 per cell of added
   length (0.547 for a one-row strip in the interior). The cost per cell of each further row, from the mixed
   second difference of strips of w rows by l units against the rim, is at or below the torus value at the same
   (w, l): FINAL_RIM_M. The 0.022 between 0.231 and 0.2087 is not in the living state's cost of emptiness near
   the rim.
5. **Hull-face-shaped holes: the rims cooperate [measured].** For an upright triangle of side s (the shape of a
   hull face of 3s(s+1)/2 cells) turning one living edge into a real rim lowers −ln P by 0.86, 1.32, 1.76 (s = 3,
   4, 5); the second edge by 2.21, 2.75, 3.30; and the lifetime of the hull face of that side (all three) lies
   another 0.82, 2.44, 3.68 below the corner triangle, FINAL_D6 at s = 6. Edge costs do not add, and "corner
   triangle = hull face + an edge cost linear in s" fails.
6. **How a patch empties [measured].** In the interior, by a crash of the patch and the layer beneath it: 83%,
   71%, 70% of new emptyings of 2 × 2, 3 × 3, 4 × 4 contain a one-generation fall of half the patch's cells; the
   mean path of a 3 × 3 patch is 0.52, 0.545, 0.41, 0.13, 0 of its cells (normal 0.517) while the cells of the
   second layer under it go 0.43, 0.45, 0.34, 0.16, 0.22 (normal 0.435). The boom is weak: FINAL_LAUNCH. On the rim
   the bust share is 66%, 50%, 50%; in the corner 33%, 23%, 22%: corners fade.
7. **A new anchor, and what it does to the formulas [measured; the reading is conjecture].** The 18-cell hull
   face (radius 5): ln τ_face = 4.855 ± 0.015 (`data/life.txt`; same mode gives 6.805 ± 0.002, 9.824 ± 0.003,
   13.632 ± 0.014 at 30, 45, 63 cells against the anchors 6.804, 9.819, 13.633). The hull's second differences per
   cell are then 0.355, 0.266, 0.231, 0.230 at k = 4…7. The rows formula (a price per row of depth, which makes
   the second difference step every third side) fits the five anchors with χ² 0.02 and misses the 18-cell face by
   0.27. A rim term, one asymptotic price and one geometric transient (formula S, `model.py`) fits all six with
   χ² 0.6 on 1 at a price of **0.223 (0.2175 … 0.227)**; with the price fixed at 0.2087, χ² 6.4 on 2; at 0.2307,
   4.1 on 2.

Frozen forecast (`PREDICTIONS.md`, block B, commit e2e2b6e, before looking at `noisy/`): **135 cells 29.21 ± 0.03,
165 cells 35.75 ± 0.06, 198 cells 42.96 ± 0.11.** These are extrapolations of the anchors (plus the 18-cell face):
the static measurement supplied no number for them.

## 1. Stepper, validation, definitions

`holes.c`: own bit-sliced graph stepper (256 lanes = independent replicas, random soup of density 1/2), written
from `reference/oracle.py` and `docs/AUTOMATON.md`. Vessels: `slab n L` (L `{111}` layers, period lattice
(n,0),(0,n)), `hull R` (octahedron |x|+|y|+|z| ≤ R).

Validation (`validate_log.txt`; `$S/holes val slab 12 8 21 1200 0 F && python3 validate.py F`, `… val hull 29 0 22
1000 0 F`): three lanes compared with the oracle state for state at every generation, slab 12 × 12 × 8 over 1,200
generations and hull R = 29 over 1,000 (the whole oracle array, so a birth outside the vessel would show): identical,
all states distinct. With one swapped neighbour (`NEG = 1`) the comparison fails at generation 3 (slab) and 7
(hull). Hull R = 21 over 1,500 generations: identical (run once, earlier binary, same `step`).

Counter check: with the two orientation classes averaged as the GPU table did, 2 × 2, 2 × 3, 3 × 3, 3 × 4 read
6.2542, 8.7926, 12.1281, 15.4008 ± 0.0019 against 6.254, 8.793, 12.128, 15.3999/15.3979 on file.

Definitions. A **unit cell** is the three cells of the face layer that are faces of one cube and point out of
the vessel (a kagome triangle); on the hull face (1,1,1) they are (i, j, m) = (⌊x/2⌋, ⌊z/2⌋, ⌊y/2⌋), i + j + m =
k − 1, and i, j, m are the distances in rows from the three rims. A **rhombus a × b** at (I0, J0) is the unit
cells I0 ≤ I < I0 + a, J0 ≤ J < J0 + b; a **triangle of side s** is I ≥ I0, J ≥ J0, I + J ≤ I0 + J0 + s − 1 (a
hull face's shape). **Class P** uses the outward triangles (the only kind that tiles a hull face), **class Q** the
inward ones (the three faces of a cube that point into the vessel); on the torus both exist and P is the likelier
to be empty (2 × 2: 6.160 against 6.358). Hull tables are class P; torus numbers are class P unless said.
f = −ln P(empty at an instant), counted every generation over every translate (torus: 144 positions, two faces)
or by position (hull: 8 faces × 3 rotations, with the mirror image pooled). M(a+½, b+½) = f(a+1, b+1) − f(a+1, b) −
f(a, b+1) + f(a, b). **Errors: delete-one jackknife over the 8 groups of 32 lanes of a run (independent
replicas), never over translates.**

Runs (one each): `$S/holes run slab 12 8 101 56000000 1000 $S/slab12_s101.txt 1` (FINAL_SLAB_GENS generations ×
256 lanes; face density 0.51774; no face ever empty) and `$S/holes run hull 29 0 201 10400000 1000
$S/hull29_s201.txt 1` (FINAL_HULL_GENS; face density 0.52195; no face ever empty). Tables: `python3 ana.py torus
$S/slab12_s101.txt`, `python3 ana.py hull $S/hull29_s201.txt --torus $S/slab12_s101.txt`. The raw counts are in
`data/slab12_s101.txt` and `data/hull29_s201.txt.gz`.

## 2. The wide torus [measured]

−ln P of an empty a × b rhombus, class P (the full table, class Q and the hit counts are in `data/torus_table.txt`):

FINAL_TORUS_F

Bulk cost per cell, M(a+½, b+½)/3, class P (class Q is 0.001 to 0.005 higher):

FINAL_TORUS_M

- Along a = 1.5 it falls slowly with the long side; along a = 2.5 it is flat at 0.26 from b = 2.5 to 5.5; the one
  value at a = 3.5 agrees. A geometric continuation of the diagonal (0.2932, 0.2646, FINAL_DIAG3) would end near
  0.25. Nothing reached is below 0.25. Not reached: any M at a ≥ 4.5 (it needs the 5 × 5 patch, −ln P ≈ 28).
- Perimeter: a strip one unit cell wide costs 1.642 per unit of length (0.547 per cell), two wide 2.41, three
  wide 3.21; with c = 0.26 the edge costs about 0.43 per lattice unit of perimeter (with c = 0.2087 it would be
  0.66: the "0.66 to 0.69 per unit" on file is tied to the assumed bulk price).
- The cost of one more unit of length of a strip keeps falling with the length for strips 2 and 3 wide (2.534,
  2.515, 2.466, 2.437, 2.419, 2.410 for a = 2): the single-variable curvature that made the old estimator fall.
- Triangles of side s, upright (class P): 1.9718, 4.9190, 8.7451, 13.307 ± 0.002, 18.55 ± 0.02 (s = 1…5); their
  second differences per cell 0.293, 0.245, 0.232 ± 0.003 are not perimeter-free either (the same turned by 180°:
  4.878, 8.648, 13.148, 18.36).

Holes against closed tori of the same shape (`data/life_tori.txt`: `$S/holes life slab NX NY SEED BATCHES T0
TMAX`, first empty face, hazard after T0, τ_face = 2/hazard; 4 × 4 reads 9.928 ± 0.003 against 9.9251/9.9324 on
file, 4 × 5 12.471 ± 0.013 against 12.4865):

FINAL_HOLE_TORUS

Caution: my 3 × 6 and 2 × 8 tori read 10.943 ± 0.008 and 8.450 ± 0.004 where `research/constant/out/points.txt`
has 11.0824 and 9.4888. Those shapes are the ones with a large "fw%" there; I did not find out which lives that
table drops. The 4 × 4 and 4 × 5 values agree.

## 3. The hull face of 360 cells [measured]

Interior against torus (difference in −ln P, hull − torus):

FINAL_HULL_A

The same rhombus against its distance d from a rim (the other rims three or more rows away):

FINAL_HULL_B

Corner rhombi (two sides on rims): FINAL_HULL_C

Strips of w rows against a rim and l units along it, ends three or more rows from the other rims, g(w, l):

FINAL_HULL_D

Cost per cell of row w+1 from the mixed second difference, rim strips | the torus at the same (w, l):

FINAL_HULL_DM

Triangles of side s as holes, with two, one and no real rim, and the hull face itself (ln τ; 18 cells: this work):

FINAL_HULL_E

How a patch empties, by position (`P` lines; an event is a patch empty now and not empty in any of the four
generations before; "bust" = a one-generation fall of at least half the patch's cells within the last nine):

FINAL_HULL_F

## 4. Lifetimes by first face death [measured]

`$S/holes life hull R 0 SEED BATCHES T0 TMAX`: 256 lanes from soup, a lane leaves the risk set when one of its
faces is empty (death) or its state repeats with a period of 12 or less (censored); hazard = deaths / lane-
generations at risk after T0; τ_face = 8/hazard. `data/life.txt`:

| hull radius | cells | this mode | anchor |
|---|---:|---|---|
| 5 | 18 | **4.855 ± 0.015** (4.8556 ± 0.0006 over generations 41–100; 4.857, 4.852, 4.856 in windows of 20; the error is my allowance for the window: 21–40 reads 4.899, 101–120 reads 4.879) | none |
| 7 | 30 | 6.8048 ± 0.0019 (an earlier run with half the batches: 6.8148 ± 0.0026) | 6.804 ± 0.003 |
| 9 | 45 | 9.8239 ± 0.0033 | 9.819 ± 0.003 |
| 11 | 63 | 13.6315 ± 0.0139 | 13.633 ± 0.008 |

Radius 3 (9 cells) has no steady hazard (4.28, 4.44, 4.56, 4.82 in successive windows): not a number.
A hull of radius 5 has 114 cells and its eight faces share most of them; whether its faces belong to the same
family as the larger ones is a judgement (the forecasts are given with and without it).

## 5. Formulas for the hull face and the forecasts

`python3 model.py`. Anchors: 6.804, 9.819, 13.633, 18.141, 23.3392 at k = 4…8, plus 4.855 at k = 3.

- **Rows formula R**: ln τ = C + Σ_r c_r·A_r(k), A_r the number of cells r rows from the nearest rim. [proved]
  The second difference of A_r in k is 3 for k − 3r ∈ {0, 1, 2} and 0 otherwise, so the second difference of ln τ
  is 3c_⌊k/3⌋: constant over three consecutive sides. Fitted: C = 1.7585, c_0 = 0.1572, c_1 = 0.2666, c_2 = 0.2307,
  χ² 0.02 on 1; from 30–84 cells it gives the 108-cell face as 23.343 ± 0.028 (23.3392). It says 4.589 at 18
  cells; measured 4.855 ± 0.015. **Refuted as an exact form** (if the 18-cell face counts). Its 135-cell value is
  "the second difference repeats", 29.231 ± 0.025.
- **A power of the area in front** (τ ∝ A^(−p)·e^(0.2087·A + b·k)), fitted on 45–108 cells: p = 1.55, χ² 0.26 on
  1, but 6.741 at 30 cells (anchor 6.804) and 29.202 at 135.
- **Formula S**: ln τ = a + b·k + 1.5·c·k(k+1) + B·r^k. All six anchors: c free 0.2230 (0.2175 … 0.2270), r = 0.31,
  χ² 0.61 on 1 → 29.207 (29.177 … 29.232), 35.746 (35.677 … 35.801), 42.954 (42.830 … 43.051). c = 0.2087: χ² 6.42
  on 2 (29.137); c = 0.2307: χ² 4.05 on 2 (29.256). Without the 18-cell face: c free 0.2295 (0.2175 … 0.2320),
  29.225; c = 0.2087 is then χ² 1.51 on 1 with r = 0.535 (29.179): the five anchors alone do not refute a
  geometric transient towards the wrapped price.

None of these has "at most one fitted number", and none takes a number from the living state: sections 2 and 3
say why it could not be done (no rim surplus to put in; a bulk cost of emptiness that is neither price).

## 6. Forecasts and scores

Mine, block A (`PREDICTIONS.md`, commit 7ebacea, before any code): FINAL_SCORE_A

The PI's block 5: (1) bulk cost on the torus 0.2087 ± 0.008: **missed** (0.26; outside 0.195–0.222, so by its own
criterion "the price of a face is the price of a hole in an unbounded face" is dead, with the caveat of item 1
that only holes up to 3 × 6 and 4 × 5 unit cells were reached). (2) interior patches within 0.010 per cell of
the torus: **held** (within 0.0001). (3) rim-row patches dearer by 0.02 per cell or more: **missed** (they are
cheaper, and the mixed differences show no surplus). (4) a model from the two measurements: **could not be
built**. (6) is for the 135-cell measurement.

## 7. Failed, not checked, next

Failed or dropped: the rows formula (killed by the 18-cell face); "2·corner − rim = ln τ + constant" for triangle
holes (off by −0.31, +0.38 at s = 4, 5); extrapolating the bulk cost with a sum of two decaying functions (χ² 43
on 9; the fitted "asymptote" moves from 0.19 to 0.25 with the cut); a lifetime for the 9-cell hull face.

Not checked: more than one run per vessel (errors come from the eight lane groups of one run each); another
hull radius, slab thickness or torus size; patches beyond −ln P ≈ 24; why two of my narrow-torus lifetimes differ
from the table on file; whether the censoring of the `life` mode (periods up to 12) lets long-period debris into
the 18-cell number; the triangle "turned by 180°" on the hull; nobody has rewritten the stepper or the counters.

Next step I would take: lifetimes of rimmed faces that are not triangles. A vessel cut by eight diagonal
half-spaces with unequal constants has hexagonal and trapezoidal faces; a hexagon of 84–96 cells has cells four
rows from every rim where the 108-cell triangle has none, at a lifetime plain running reaches. If its price by
mixed second differences is 0.209, the hull's 0.231 is the triangle's transient; if 0.23, it is the rim's price.
(The side faces must be made to outlive the watched one.) On the static side: count patches that hold at most
two or three cells, not none, to see whether the 0.05 per cell is the price of the instant.
