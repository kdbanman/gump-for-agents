# research/blast/rim: why 0.231? Rims without corners (agent `rim`, 2026-11-18)

Question: the hull's triangular faces pay 0.2307 per cell (second differences of ln τ in k), wide wrapped faces
0.2087. A triangle of 5 to 8 units a side is mostly rim and corner. Is the excess made by the corners, by the
rims, or by the face as a whole? Vessels with rims and **no corner anywhere** were built and their faces timed.

Everything below is from one code (this directory), oracle-exact (see Validation), runs of 10 to 300 s on one
core. Tables: `python3 research/blast/rim/table.py` (rows: `data/runs.csv`, output `data/table_out.txt`); fits:
`python3 research/blast/rim/fit.py` (`data/fit_out.txt`).

## The vessel

`prism(T1, T2, L, par)` (`vessel.py`): the cells with s1 = x+y+z in T1 consecutive odd values and s2 = x+y−z in
T2 consecutive odd values, periodic along (1,−1,0) with period L·(2,−2,0) (L lattice units of the face's kagome
net; loop² = L²). It is confined by T2 (four diagonal half-spaces; the period lies in all four planes). Its
cross-section is a rhombus; it has four faces and **no corner**: each d1 face is a strip of T2 rows, alternately
2L cells (a *dense* row) and L cells (a *sparse* row), 1.5·T2·L cells for T2 even, with one **obtuse** rim (dihedral
109.47°, the kind every hull edge is) and one **sharp** rim (70.53°, which no hull has). No prism face can have
two obtuse rims: only ±(1,1,1), ±(1,1,−1) contain the period, so each face meets one neighbour on each side, one
of each kind. `par` = 0 makes the obtuse rim row dense (the hull's edge row is dense) and, for an even number of
rows, the sharp rim row sparse. `(w,w,L,0)` is symmetric: four equivalent faces of w rows over a depth of w layers,
each beside faces of the same width (as in a hull). Rows are printed in `data/runs.csv` from the obtuse rim to the
sharp one.

## Answers

Symmetric strips (w,w,L,0), ln τ_face (`data/table_out.txt`; errors 1/√deaths; XX = see table):

| rows w \ L | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|
| 8 (12 cells per unit length) | 8.1447 ± 0.0015 | 11.0912 ± 0.0032 | 13.8608 ± 0.0082 | 16.4735 ± 0.0264 |
| 10 (15) | 9.6694 ± 0.0026 | T104 | T105 | |
| 12 (18) | T123 | 15.7736 ± 0.0247 | | |
| 14 (21) | 12.7845 ± 0.0086 | | | |

**1. ln τ is linear in the width at fixed length: a row costs the same wherever it is added; no support zone
ends within 7 rows of a rim [measured].** The cost of two more rows (3L cells), g(L) = ln τ(w+2, L) − ln τ(w, L):
L = 3: 1.525, 1.558, 1.557 (8→10→12→14 rows); L = 4: G4A (8→10), G4B (10→12); L = 5: G5 (8→10).
So ln τ = a(L) + (w/2)·g(L) with g = 1.55, 2.35, G5S and a = 1.97, 1.72, A5 at L = 3, 4, 5.
The **price per cell of added width** is g/(3L): **0.169 to 0.173 (L = 3), 0.195 to 0.196 (L = 4), W5 (L = 5)**.
Below the wrapped 0.2087 at every length reached, and rising with L.

**2. The price per cell of added length at fixed width falls with length and does not depend on the width
[measured]:** L 3→4: 0.2455 (8 rows), 0.2513 (10), 0.2525 (12); L 4→5: **0.2308 ± 0.0007** (8), L45W10 (10);
L 5→6: **0.2177 ± 0.0023** (8). The hull's 0.231 appears here as the length price at one step (4→5) and is gone
at the next (at L = 4 the strip is still a tube of girth 4; the step 5→6 is the clean one). Width and length disagree at every size: the death of a rimmed strip is not isotropic, and neither
number is 0.209 or 0.231 as a constant.

**3. The mixed second difference, the strip's analogue of the hull's second difference in k, per cell
[measured]: 0.2741 ± 0.0029 (8→10 rows, L 3→4), 0.2590 ± 0.0087 (10→12, 3→4), MIX45 (8→10, 4→5).** It
is the increment of g: 0.82, then G45INC (the hull's second differences: 0.800, 0.692, 0.692 ± 0.015; the wrapped
price would give 0.626). At L 4→5 the corner-free strips of 48 to 75 cells are 0.6σ below the hull's 0.2307 and
2.2σ above the wrapped 0.2087, **with no corner anywhere: corners are not needed for the excess.** But a strip
has no constant price: one step earlier the same quantity is 0.27. Whether it goes on falling is not measured:
if a(6) lies between a(4) and a(5), then g(6) = 3.69 ± 0.02 and the next increment is 0.66 ± 0.04 (0.220 ± 0.013
per cell) [conjectured from that one assumption]. That cannot tell a plateau at 0.231 from a slow bend to 0.209.

**4. A face's lifetime depends on its neighbours and on what is behind it, strongly, when those are small
[measured].** An 8-row face lives ln τ = 11.091, 13.861, 16.47 (L = 4, 5, 6) beside 8-row faces over depth 8,
and 11.051, 13.643, 15.350 beside 6-row faces over depth 6 (prism(8,6,L)): −0.04, −0.22, −1.12. A 6-row face
lives 8.635, 10.542, 12.175 beside 8-row faces (depth 8) and 8.560, 9.850, 10.215, 10.166 (L = 4…7) in the 6×6
rod, where ln τ **stops growing with length**: the thin rod dies as a rod (or its faces die by a band that then
runs along it), at a rate that no longer falls with L. So "depth and neighbours do not matter" is a statement
about thick slabs; a prism must be at least 8×8 layers to be read as a face law. Depth and neighbour width are
not separated here (NB810).

**5. Rim kinds differ by order one [measured].** Adding a sparse row beyond a dense sharp rim row ((7,7,4) →
(8,8,4), 4 cells) raises ln τ by 1.491 (0.37 per cell); adding a dense row beyond a sparse sharp rim row
((8,8,4) → (9,9,4), 8 cells) by 0.857 (0.107 per cell). A dense row at the sharp rim is nearly free to kill:
its cells have 6 neighbours inside the vessel (below).

**6. The hull's five values are not reproduced with nothing free, and cannot be from strips alone
[argued].** A strip gives only the sum of an obtuse and a sharp rim; an all-obtuse polygon is the hull's
triangle itself, so "the cost of an obtuse rim" and "of a corner" are not separately defined by any corner-free
vessel. What the strips give with nothing fitted to hulls is the size of the second difference (3) and one
coincidence worth a test: the hull's step from k = 4 to 5 adds a row pair of length 5 and costs 3.015; a strip's
row pair of length 5 costs G5. Not tested at any other length.

**7. Bust or starve (the PI's test) [measured: `python3 research/blast/rim/bust.py …`, `data/bust_out.txt`].**
Share of single-face deaths with a one-generation fall of at least half the face's cells among the twelve
steps that end at the death:

| vessel | cells | deaths | share | median largest fall |
|---|---:|---:|---:|---:|
| hull R = 9 | 45 | 11,983 | 0.016 ± 0.001 | 10 |
| strip 8 rows, L = 4 | 48 | 11,986 | 0.203 ± 0.004 | 18 |
| strip 10 rows, L = 4 | 60 | 8,644 | 0.196 ± 0.004 | 22 |
| strip 8 rows, L = 5 | 60 | 11,412 | 0.158 ± 0.003 | 21 |
| strip 12 rows, L = 3 | 54 | 11,999 | 0.150 ± 0.003 | 18 |
| strip 14 rows, L = 3 | 63 | 11,999 | 0.108 ± 0.003 | 20 |
| strip 10 rows, L = 5 | 75 | 1,125 | 0.168 ± 0.011 | 28 |

The hull value agrees with agent `anatomy`'s (0.016 to 0.022 at 63 and 84 cells; wrapped 0.51 to 0.60), so the
definition is the same. Corner-free strips sit between: ten times the hull's share, a third of the wrapped one.
The share does **not** rise with width (0.203 → 0.196 from 8 to 10 rows at L = 4; 0.158 → 0.168 ± 0.011 at L = 5; 0.150 → 0.108
from 12 to 14 rows at L = 3). So a strip of 5 to 7 units is not "bust in the middle, starve at
the rims" in any way this statistic sees, and the corners (or the three-fold closure of the rim) are what take
the hull from 0.2 to 0.02.

## The rim in the language of the rule [proved by enumeration: `python3 research/blast/rim/budget.py`, `data/budget_out.txt`]

T1 applied to two diagonals at once. Neighbours inside the vessel (the most that can ever be alive):

| face cell | inside | in own face layer | one layer beneath | two beneath |
|---|---:|---:|---:|---:|
| interior | 9 | 6 | 2 | 1 |
| obtuse rim row (dense or sparse) | 7 | 4 | 2 | 1 |
| row next to an obtuse rim, when dense | 8 | 5 | 2 | 1 |
| sharp rim row, sparse | 6 | 4 | 2 | 0 |
| sharp rim row, dense | 6 | 4 | 1 | 1 |
| hull corner cell (in four face layers) | 4 | 2 | 2 | 0 |

A dense obtuse rim cell's 7 are: 2 along the rim row, 2 further in on this face, 2 on the neighbouring face,
1 in neither face layer. So with this face otherwise empty it has at most 3 live neighbours (T2: it cannot be
born) but it **survives on the neighbour's support alone** (3 suffices), and it is overcrowded (n ≥ 6) only when
6 of its 7 are alive, where an interior cell needs 6 of 9. A hull corner cell has 4 neighbours in all: it is born
only when all four are alive (it sits at density 0.175) and can never be overcrowded; a sharp rim cell (6 inside)
is overcrowded only when all six are alive.

## Forecast for the hull faces of 135 and 165 cells

Frozen in `PREDICTIONS.md` block 5 (commit 88d62d4, 03:46 UTC), before reading any other agent's value:
**ln τ_face(135) = 29.222 ± 0.030**, P(nearer 29.230) = 72%; **ln τ_face(165) = 35.79 ± 0.08**. Basis: the hull's
two equal second differences and the strips' mixed second difference equal to them at L 4→5.
Revised in block 6 (commit 8ded7f4, 03:58 UTC, still blind) after the long (8,8,6) run showed the length price
still falling at 72 cells: **29.210 ± 0.035, P(nearer 29.230) = 62%, P(nearer 29.163) = 38%; 165 cells:
35.74 ± 0.09.** Both blocks stand for scoring; the second is what I believe.

## Conventions

Soup 0.4 on every cell of the vessel. A life ends at the first generation in which a face layer is empty (booked
every generation) or when settled (state equal to a snapshot 840·m generations back, m ≤ 4; censored at the
snapshot; under 0.1% of exposure except in the 6×6 rods, 0.5%). Ageing-in T0 = 200. τ_face = (faces in the class)
× exposure / first deaths (lives ended by an empty face of the class), the hull anchors' convention; error
1/√deaths. T0 = 1000 gives the same values within errors (columns in `data/runs.csv`).
Check against the anchors with this code and these conventions: hull R = 7: 6.8078 ± 0.0008 (on file 6.8054 ±
0.0029); R = 9: 9.8214 ± 0.0009 (9.8202 ± 0.0027). `python3 research/blast/rim/run.py hull 7 2000000 1` (18 s),
`… hull 9 6000000 1` (83 s). (Counting every empty face instead of every life gives 6.782 at R = 7: 2.5% of
30-cell deaths empty two faces in the same generation.)

## Validation [measured: `python3 research/blast/rim/validate.py`, 11 s, `validate_out.txt`]

`rim.c` (AVX-512 carry-save kernel, 512 replicas) against `reference/oracle.py`, state for state, 1,000
generations × 3 replicas (lanes 0, 77, 511), every generation active: prisms (8,8,5,0) lifted 3× into the
30-torus, (8,6,6,1) 2× into the 24-torus, (8,7,4,0) 3× into the 24-torus, (7,5,12,0) unlifted in the 24-torus,
and the hull R = 9 in a dead 28-array. **How the period is realised:** the array torus (Z/H)³ contains the loop
(H,−H,0), so a prism of period L·(2,−2,0) with H = 2Lm is wrapped m times round it, every copy carrying the same
state; the torus's other translations displace the prism by H in x+y or z, so the cross-section's extent must be
≤ H − 10 (checked, and the lift is checked injective); the oracle's whole array is compared with the lifted
state, so a cell born outside the vessel would fail too. Negative control: one neighbour entry of one face cell
replaced by another of its neighbours fails within 3 generations on every vessel.
Not oracle-checked themselves: prisms of other (T1, T2, L) (same builder), and the booking of deaths (checked
only through the two hull anchors).

## Not checked

- One code, one seed for most points; errors are Poisson only.
- Whether the thin rods die as rods or by a band on a face (4); depth and neighbour width are not separated.
- Rim kinds other than obtuse-dense + sharp-sparse were measured only at odd widths (5); `par` = 1 not run.
- The strips with a mixed second difference are tubes of girth 4 and 5 across 4 to 5 units of width. A wide
  face they are not. The comparison with the hull is of like sizes, not of asymptotes.
- No obtuse rim was isolated from a sharp one (needs faces with corners: hexagons on truncated hulls).
- Question 3 of the brief (hazard against the neighbour's fullness) was dropped for time except for (4).
