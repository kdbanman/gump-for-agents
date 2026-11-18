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

**1. Corner-free strips pay the hull's price, not the wrapped one, in the only sense in which a strip has a
price: the mixed second difference [measured].** For the symmetric strips of 8 and 10 rows at L = 4 and 5
(48 to 75 cells), [τ(10,5) − τ(10,4)] − [τ(8,5) − τ(8,4)] in ln, over its 3 cells: **see table below** (raw; a
girth-4 correction of the size seen on wrapped tubes would lower it by 0.005). The hull's second differences
give 0.2306 ± 0.0012 (k = 5…8). So the 0.231 is not made by corners. It is 2σ from 0.2087 on this measurement
alone.

**2. Width and length do not cost the same [measured]: the death of a rimmed strip is not isotropic.**
Per cell of added **length** at fixed width (8 rows): 0.2454 (L 3→4), 0.2312 ± 0.0014 (4→5), 0.217 ± 0.003 (5→6);
at 10 rows 0.2311 ± 0.002 (4→5). Per cell of added **width** at fixed length: 0.169 and 0.174 (L = 3, 8→10→12
rows), 0.1953 ± 0.0010 (L = 4, 8→10), 0.2024 ± 0.0022 (L = 5, 8→10). Neither is 0.209 or 0.231. In the form
ln τ = a0 + c·A − α·w + β·L (w rows, A cells) the data at L ≥ 4 want c ≈ 0.23, **α ≈ 0.21 per row** (each row is
cheaper than its cells by about 0.9 cell) and β ≈ 0 within ± 0.14 (`fit.py`). The hull's own fit has the same
shape: ln τ = 1.13 + 0.2306·A − 0.337·k, i.e. −0.17 per row of the triangle's height.
The fall of the length price with L at 8 rows (0.231 → 0.217) is partly the short way round (at L = 4 the strip
is a tube of girth 4: a wrapped tube's discount of 0.0015 per cell would turn 0.2312 into 0.226 and leave 5→6
alone); whether it goes on falling towards 0.209 at L ≥ 7 I could not reach (84 cells).

**3. No support zone that ends within 6 rows of a rim [measured, short strips only].** The cost of two more rows,
g(L) = ln τ(w+2, L) − ln τ(w, L), at L = 3: 1.525 (8→10 rows), 1.561 (10→12), see table for 12→14; at L = 4:
2.344 (8→10), see table for 10→12. It does not fall as the rows are added further from both rims. (L = 3 and 4
are tubes of girth 3 and 4, where a row is cheap anyway; the test at L ≥ 5 needs 90 cells.)
g(5) = 3.036 ± 0.032 from strips; the hull's step from k = 4 to 5, which adds a row pair of length 5, is 3.015.

**4. A face's lifetime depends on its neighbours and on what is behind it, strongly, when those are small
[measured].** An 8-row face of the same shape lives ln τ = 11.090, 13.864, 16.47 (L = 4, 5, 6) beside 8-row faces
over depth 8, and 11.051, 13.643, 15.350 beside 6-row faces over depth 6 (prism(8,6,L)): −0.04, −0.22, −1.12. A
6-row face lives 8.635, 10.542, 12.175 beside 8-row faces (depth 8) and 8.560, 9.850, 10.215, 10.166 (L = 4…7)
in the 6×6 rod, where ln τ **stops growing with length**: the thin rod dies as a rod (or its faces die by a band
that then runs along the rod), at a rate that no longer falls with L. So "depth and neighbours do not matter" is
a statement about thick slabs; a prism must be at least 8×8 layers to be read as a face law. Not separated here:
depth against neighbour width (see the (8,10,L) rows if present in the table).

**5. Rim kinds differ by order one [measured].** Adding a sparse row beyond a dense sharp rim row ((7,7,4) →
(8,8,4), 4 cells) raises ln τ by 1.490 (0.37 per cell); adding a dense row beyond a sparse sharp rim row
((8,8,4) → (9,9,4), 8 cells) by 0.859 (0.107 per cell). A dense row at the sharp rim is nearly free to kill:
its cells have 6 neighbours inside the vessel (below).

**6. The hull's five values are not reproduced with nothing free, and cannot be from strips alone
[argued + measured].** A strip gives only the sum of an obtuse and a sharp rim; an all-obtuse polygon is the
hull's triangle itself. What strips do give with nothing fitted to hulls: the k² coefficient (0.231 ± 0.011
against 0.2306). Using the strip law as it stands for a triangle (w = 2k rows): 1.71 + 0.2305·A − 0.2106·2k gives
9.97, 13.70, 18.12, 23.23 at k = 5…8 against 9.820, 13.635, 18.141, 23.339: within 0.15, the residual linear in
k (+0.085 per unit k). One linear term is left free, as in the hull's own fit.

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
**ln τ_face(135) = 29.222 ± 0.030**, P(nearer 29.230) = 72%, P(nearer 29.163) = 28%; **ln τ_face(165) =
35.79 ± 0.08**. Basis: the hull's two equal second differences, the strips' mixed second difference equal to
them (no corners needed), and no fall of the row cost with width up to 12 rows. Against: the length price at 8
rows falling with L (0.231 → 0.217), which if it is not all a girth effect says the price does bend.

## Bust or starve (the PI's test, `bust.py`)

See `data/bust_out.txt` and the section "Results added last" below.

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
