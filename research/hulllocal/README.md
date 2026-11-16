# The living state of a hull face (research/hulllocal)

2026-11-16. Question: is the face layer of a living octahedral hull (radius 15, faces of 108 cells; radius 13, 84)
occupied differently from a wrapped face (a face torus on an 8-layer slab), in its interior or near its rim, enough
to join the two prices per cell (rimmed 0.2307 ± 0.0047, wrapped 0.2087; CLAIMS CN2) through the tube relation
discount = 1.85 × density deficit (research/wraplocal)? That relation would need the hull interior denser by 0.012.

## Forecasts (written and committed before any stepping was run)

Nothing had been stepped or measured when these were written; only the cell counts of the vessels were known
(hull R = 15: 2,064 cells, face 108; R = 13: 1,386, face 84).

- **P1 (65%).** The face-layer density in the interior of the R = 15 hull face (cells three or more layers from
  every other face) equals that of a long-loop wrapped face measured by the same code within 0.001.
- **P2 (25%).** It exceeds the wrapped value by more than 0.004.
- **P3 (10%).** The excess is between 0.008 and 0.018.
- **P4 (70%).** The rim cells (in the face layer of a second face as well, or one layer from it) differ in density
  from the interior by more than 0.01, either sign.
- **P5 (60%).** The rim is *less* dense than the interior (against the lead's H5).
- **P6 (80%).** Wrapped faces on slabs of 8, 12 and 16 layers have face densities equal within 0.0005; the layer
  beneath likewise.
- **P7 (60%).** The rim's density excess or deficit, summed over the face, per unit of rim length, is the same at
  R = 13 and R = 15 within two standard errors.
- **P8 (65%).** Occupation explains less than a quarter of the price difference: 1.85 × |interior excess| < 0.0055.

## Answer

- **The interior of a hull face is occupied as a wrapped face is [measured].** Deep in the face (cells five or more
  layers from every other face, R = 17 to 25) the face-layer density exceeds the long-loop wrapped value by
  +0.00021 ± 0.00001 (R = 17), +0.00011 (21), +0.00008 ± 0.000002 (25), falling with R. The interior as asked
  (r ≥ 3) is *less* dense: −0.00100 ± 0.000003 at R = 15, −0.00134 at 13, falling to −0.00043 at 25. Both are the
  tail of a rim profile, not a per-cell difference. The relation would need **+0.012**. That is excluded by a
  factor of more than 50 at every radius, and the measured difference has the wrong sign at the radius asked.
- **The per-cell part, the whole face included [fitted].** The face's total excess E(R) = Σ (ρ_cell − ρ_w) over its
  cells, fitted as a + bR + cA over R = 11 to 25, gives c = −0.00012 ± 0.00003 per cell (± 0.00007 with the χ² of
  17 on 4 folded in; −0.00014 against ρ∞ = 0.517742 instead of this code's 0.517717). Through κ = 1.85 that is
  **−0.0002 ± 0.0001 per cell, against the +0.0220 ± 0.0047 that separates the two prices**. Occupation explains
  none of it: at most 1% in size, and with the wrong sign.
- **The rim is a rim term [measured].** The profile perpendicular to an edge, away from the corners, by r (layers
  to the nearest other face), as ρ − ρ_w at R = 21: r = 0 (the edge row, a cell in two face layers) **+0.0607**,
  r = 1 **−0.0214**, r = 2 +0.0041, r = 3 and 4 −0.0008, r = 5 and 6 +0.0001. It is a damped oscillation, about a
  factor 5 per row pair, the same at R = 13, 15, 21 to 10⁻⁴. The corners (the 3 cells in four face layers: 0.175,
  their neighbours on the edge 0.303) carry a constant −1.712 ± 0.001 cells per face at every R from 11 to 25. The
  edges carry **+0.0541 ± 0.0002 cells per cell of rim length** (b/3, rim = 3R cells), linear in R: the
  second differences of E over R are −0.0023, −0.0014, +0.0015, −0.0023 (each ± 0.001 to 0.0015), all zero.
  H5's "within three steps of the rim denser by more than 0.01" is true of the edge row only. The next row is
  less dense by 0.021, and r ≤ 2 averaged over cells is less dense than the interior (−0.0068 at R = 15, rim
  region including corners; +0.0225 per rim cell for the edge region alone without corners).
- **Depth does not matter [measured].** Wrapped faces on slabs of 8, 12, 16, 24 layers ((6,0,6), 108 cells):
  face layer 0.517725, 0.517713, 0.517717, 0.517716 (± 0.000003). The layer beneath: 0.434709, 0.434740,
  0.434738, 0.434740. 8 against 16 differs by +0.000008 ± 0.000004 in the face layer and −0.000029 ± 0.000003 in
  the layer beneath; the same on (2,4,14), 84 cells. Only the 8-layer slab's middle layers (k = 3, which touch the
  other face's k = 3) differ: 0.41584 against 0.41508. Under the hull's face interior the layers k = 1 to 4 tend
  to the thick slab's values (R = 21: 0.43514, 0.40559, 0.41508, 0.41631 against 0.43474, 0.40573, 0.41508,
  0.41629), and the octahedron's core (≥ 5 layers from every face) is at 0.41550, the thick slab's bulk.
- **The other occupation statistics agree too [measured].** Deep interior (r ≥ 5, R = 21) against the wrapped
  face ((6,0,6), 16 layers): a dead face cell's mean live neighbours 4.2623 against 4.2631 (in-layer 3.0160 to
  3.0167 against 3.0173); births per cell per generation 0.19816 against 0.19818. At r ≥ 3 (R = 15) the
  differences are 0.1% in size, with the signs of the rim tail. The share of live face cells with 3 to 5 live
  neighbours is 0.61608 there against 0.61720 per live cell, and 0.31834 against 0.31954 per cell. Converted by
  wraplocal's profiles into an equivalent density deficit, none of these exceeds 0.0016, so none comes within a
  factor 10 of what the price asks.
- **What does differ is at the rim and in the face's dynamics as a whole [measured].** Edge-row cells turn over
  less: 0.162 births per cell per generation against 0.198, with density 0.578. The face population's variance
  per cell is 0.4149 ± 0.00002 at R = 15 against 0.3783 for the wrapped face (+9.7%), and 0.4232 at 13. Its
  excess over A × 0.37825 grows almost linearly in R (3.65 at R = 11 to 4.92 at R = 25), but not exactly: a + bR + cA
  fits it with χ² 214 on 4, c = +0.0036 per cell. So the variance carries the one non-rim, area-like difference
  found, +1% per cell. On tubes a larger variance went with a *lower* price, so this too points the wrong way, if
  it points at all.

**What it means for the two prices.** Occupation with κ = 1.85 explains 0.0000 ± 0.0001 of the 0.022 per cell
(the fitted c gives −0.0002, the wrong sign). The hull face's occupation differs from a wrapped face's only by a
constant corner term and a term linear in the rim. CN2's 0.2307 comes from second differences that cancel both.
Whatever makes a rimmed face pay 0.231 per cell is not in its one-point occupation, nor in the nearest-neighbour
statistics that tracked the price on tubes. Candidates left: the way the face dies (from the corners, where the
density is 0.175, or along the edge rows, against a wrapped face with no such place), and correlations or
fluctuations at the scale of the face (the variance's per-cell excess, the non-linear part). A face dies through a
rare collective fluctuation; its mean occupation is the wrong place to look for a price that differs this way.

## Definitions

- **Hull** of radius R (odd): the cells p with |d·p| ≤ R for the four body diagonals d. This is the exact hull of
  the soup region |p|₁ ≤ R (research/fluct `fl.octa_hull(R)`, centre a cube centre), the vessel of the card's
  hull-face runs. R = 11, 13, 15, 17, 19, 21, 25 give faces of 63, 84, 108, 135, 165, 198, 273 cells. Soup 0.35 in
  |p|₁ ≤ R, as the card's runs.
- **Face** f = (d, σ): the face layer σ d·p = R. **Depth** of a cell below face f: k = (R − σ d·p)/2, in layers
  (k = 0: the face layer). **r** of a cell, for face f: the minimum depth below the six other faces (not f, not
  its opposite). r = 0 means the cell is also in a second face's layer. Every face has 3R such cells, R per edge;
  "the edge row" or "rim" is r = 0. **Interior**, as asked: k = 0, r ≥ 3 (18 cells per face at R = 15, 9 at 13).
  **Deep interior**: r ≥ 5. Under the face interior, layer k: r ≥ k + 3. **Corner region**: cells with r ≤ 2 whose
  second-nearest other face is less than 5 layers away; **edge region**: the other r ≤ 2 cells. Orbits of face cells
  under the face's C3v are labelled by the sorted depths below the 3 edge-sharing and the 3 corner-sharing faces
  (`profile.py`).
- **Wrapped face**: the slab of m layers s = (1,1,1)·p ∈ {1, …, 2m−1}, in-plane periods 2(X, Y, −X−Y) with (X, Y)
  in the lattice of (h, k), (0, d) (research/wrap's torus (h,k,d)). The face layers are t = 0 and m−1, and layer
  k beneath is t = k or m−1−k. Soup 0.4. Tori: (6,0,6) 108 cells, loops² 36 × 3; (2,4,14) 84, 28 × 3;
  (1,18,49) 147, no loop ≤ 48. Reference **ρ_w = 0.517717**, the (6,0,6) face on 16 layers. It agrees with
  research/wraplocal's ρ∞ − 3 f(36) and with (1,18,49) at 0.517743 ± 0.000002 within 2.6 × 10⁻⁵. Every comparison
  above changes by that much at most if the other reference is used.
- **Conditioning.** A replica is retired from the generation in which any face layer of its vessel (8 for a hull,
  2 for a slab) is empty, and contributes nothing after it. Burn-in 1,000 generations from the soup, then 4,000
  measured. Losses: R = 11, 1,004 of 65,536 replicas in burn-in; R = 13, 24; R = 15, 1; R ≥ 17, none; slabs ≤ 22.
  Stationarity: the two halves of each window agree to ≤ 2 × 10⁻⁵ in every class, and the R = 15 hull with 4,000
  generations of burn-in gives 0.516725 ± 0.000004 against 0.516720 ± 0.000003 (interior), 0.511058 against
  0.511062 (whole face).

## How it was measured

- **Stepper** (`hl.c`, `hl.py`): this study's own. Graphs built from the doubled coordinates and the offsets of
  docs/AUTOMATON.md. C bit-sliced B45/S345, 64 replicas per word, with per-cell accumulators: live, births, dead
  cells' live-neighbour sum (total and in the cell's own layer w.r.t. its nearest face's diagonal), live cells
  with n ∈ {3,4,5}; per face, the population's first two moments. `python3 research/hulllocal/hl.py check`
  (95 s, `data/check_out.txt`) passes all of these:
  - the closed cube of side 9 in the hull of radius 25 reproduces the 2012 log `reference/golden/legacy_cube_side09_H50.txt`
    at all 71 generations;
  - three replicas in three words equal `reference/oracle.py` cell for cell at every generation, on the hulls
    R = 15 and 13 (600 generations, embedded in an array torus of 40 and 36) and on the slabs (2,2,12) with 8, 12
    and 16 layers (400 generations, the cubic 24-torus) and (6,0,6) with 8 (150 generations, the 36-torus).
  `python3 research/hulllocal/negcontrol.py`, a negative control (one neighbour entry duplicated), fails as it
  should. The (1,18,49), (2,4,14), (6,0,6) slabs with 12, 16 and 24 layers and the hulls of R ≠ 13, 15 were not
  oracle-checked themselves. They are built by the same code that passed.
- **Runs** (`prod.sh`, `prod2.sh`): 32 blocks × 2,048 replicas (hull25: 16), each block its own soup seed, run 3 at
  a time. The whole set took about 25 minutes on 3 cores, 25 to 230 s per vessel (`data/prod_log.txt`). Errors are
  the scatter of block means. Raw accumulators: `research/scratch/hulllocal/*.npz` (not in git).
- **Reductions:** `python3 research/hulllocal/ana.py TAG …` (per class: ρ, halves, births, dead n, dead n in-layer,
  3–5 shares; `data/ana_out.txt`). `python3 research/hulllocal/profile.py 0.517717 hull13_s2 hull15_s1 hull21_s10`
  (orbit by orbit; `data/profile_out.txt`). `python3 research/hulllocal/edgeprof.py 0.517717 hull15_s1 hull21_s10
  hull25_s11` (the edge profile; `data/edgeprof_out.txt`). `python3 research/hulllocal/rimfit.py 0.517717 0.37825
  hull11_s7 hull13_s2 hull15_s1 hull17_s8 hull19_s9 hull21_s10 hull25_s11` (E(R), its parts, second differences,
  the a + bR + cA fits; `data/rimfit_out.txt`, 30 s).

## Numbers

Hull face of R = 15 against the wrapped (6,0,6) face, 16 layers (`data/ana_out.txt`):

| class | cells/face | ρ | births/cell/gen | dead: mean live nbrs | dead: in-layer | live 3–5 / live |
|---|---:|---:|---:|---:|---:|---:|
| edge row r = 0 (with corners) | 45 | 0.507207 ± 0.000009 | 0.14042 | 2.7297 | 1.5542 | 0.72315 |
| r = 1 | 18 | 0.498329 ± 0.000004 | 0.18995 | 4.2984 | 2.9921 | 0.61883 |
| r = 2 | 27 | 0.522203 ± 0.000003 | 0.19755 | 4.2594 | 3.0432 | 0.62170 |
| interior r ≥ 3 | 18 | 0.516720 ± 0.000003 | 0.19838 | 4.2667 | 3.0221 | 0.61608 |
| layer beneath, r ≥ 4 | 9 | 0.435552 ± 0.000003 | 0.20669 | 4.7894 | 2.5712 | 0.52546 |
| wrapped face layer | 108 | 0.517717 ± 0.000003 | 0.19818 | 4.2631 | 3.0173 | 0.61720 |
| wrapped layer beneath | 108 | 0.434738 ± 0.000002 | 0.20675 | 4.7974 | 2.5783 | 0.52442 |

R = 13 (84 cells): interior 0.516378 ± 0.000005, edge row 0.496171 (more corner share), r = 1 0.498743, r = 2 0.522324.

Hull faces by radius (`data/rimfit_out.txt`; ρ_w = 0.517717):

| R | A | interior r ≥ 3: ρ − ρ_w | deep r ≥ 5: ρ − ρ_w | E total | E corners | E edges | Var excess |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 63 | −0.002086 ± 0.000009 | – | −1.3639 | −1.7120 | +0.3543 | 3.652 |
| 13 | 84 | −0.001339 ± 0.000005 | – | −1.0402 | −1.7127 | +0.6845 | 3.772 |
| 15 | 108 | −0.000997 ± 0.000003 | – | −0.7188 | −1.7116 | +1.0107 | 3.957 |
| 17 | 135 | −0.000791 ± 0.000003 | +0.000209 ± 0.000008 | −0.3987 | −1.7121 | +1.3372 | 4.151 |
| 19 | 165 | −0.000650 ± 0.000002 | +0.000137 ± 0.000004 | −0.0771 | −1.7113 | +1.6634 | 4.344 |
| 21 | 198 | −0.000556 ± 0.000002 | +0.000111 ± 0.000003 | +0.2422 | −1.7121 | +1.9894 | 4.546 |
| 25 | 273 | −0.000425 ± 0.000001 | +0.000082 ± 0.000002 | +0.8851 | −1.7118 | +2.6428 | 4.918 |

Errors on E: ± 0.0004 to 0.0008; on the Var excess, ± 0.002 to 0.007. Fit E = a + bR + cA: a = −3.141, b = +0.1623 ±
0.0005 (+0.0541 per rim cell), c = −0.000117 ± 0.000032 (χ² 17.0 on 4). [fitted]

## Forecasts and scores

Mine (P1–P8, frozen in e723451):

| forecast | outcome |
|---|---|
| **P1 (65%)** interior equals wrapped within 0.001 | **passes, barely, as defined**: r ≥ 3 at R = 15 is −0.000997 ± 0.000003. At R = 13 it is −0.00134 and fails; the deep interior passes by a factor 5 |
| **P2 (25%)** exceeds by > 0.004 | **fails** (lower, not higher) |
| **P3 (10%)** excess 0.008–0.018 | **fails** |
| **P4 (70%)** rim differs from interior by > 0.01 | **passes**: edge row +0.06 (away from corners), r = 1 −0.021, whole r = 0 class −0.0095 at R = 15 |
| **P5 (60%)** the rim is less dense | **fails as worded for the edge row** (+0.061 away from corners). The r = 0 class with corners (−0.0095) and the r = 1 row (−0.018) are less dense; the rim *region* summed per face, corners included, is less dense at R ≤ 19. Scored a fail |
| **P6 (80%)** 8, 12, 16 layers equal within 0.0005, beneath too | **passes** (differences ≤ 3 × 10⁻⁵) |
| **P7 (60%)** rim excess per unit rim length equal at R = 13 and 15 within 2σ | **fails as worded**: the total per unit rim is −0.0267 at 13 and −0.0160 at 15, because the corners are a constant. With corners separated, the edge term is linear in R (+0.0541 per rim cell, second differences zero) |
| **P8 (65%)** occupation explains < a quarter (1.85 × \|excess\| < 0.0055) | **passes** (0.0002) |

The lead's (`research/wrap/PREDICTIONS.md`), scored for the lead to overrule:

| forecast | outcome |
|---|---|
| **H1 (35%)** interior exceeds wrapped by > 0.004 | **fails** (−0.0010 at R = 15) |
| **H2 (20%)** excess 0.008–0.018 | **fails** |
| **H3 (50%)** interior equals wrapped within 0.001 | **passes** at R = 15 (−0.000997 ± 0.000003, inside by 3 × 10⁻⁶; R = 13 would fail at −0.0013). The deep interior passes clearly |
| **H4 (25%)** 8 vs 16 layers differ by > 0.0005 | **fails** (0.000008 ± 0.000004) |
| **H5 (60%)** within three steps of the rim denser than the interior by > 0.01 | **fails as a statement about the region** (r ≤ 2 at R = 15, corners included: 0.5099 against 0.5167). It **holds for the edge row away from the corners** (+0.061), with r = 1 −0.021 beneath it |

## Not checked

- Only one code (this one). It is oracle-exact on two hulls and four slabs, and the hulls of R = 11, 17 to 25 and
  the slabs (1,18,49), (2,4,14) and (6,0,6) with more than 8 layers rely on the same builder. No second agent has
  read it.
- The soup (0.35 inside |p|₁ ≤ R) and the 1,000-generation burn-in come from the card's runs. One longer burn-in
  was run (R = 15, 4,000: unchanged to 5 × 10⁻⁶). Lifetimes are conditioned only on no face death in the window, so a
  bias towards replicas near death is negligible: with τ_face ≈ e²³ none occurred at R ≥ 17.
- The hull vessel is the exact octahedron. The card's vessel is the same by its definition, and fl.octa_hull gives
  the same bounds, but its graph was not compared node by node with this one.
- Space-time correlations, the hazard near the corners, and the face's approach to death (the low-population
  states) were not measured: the price may live there.
- The variance's per-cell excess (+0.0036) comes from a fit with χ² 214 on 4. It is not a clean per-cell number.

## Where to go next

- **Where hull faces die.** Condition on a face's population falling below some n (rare-event or long runs on
  R = 11, 13) and map which cells are alive last. If the corners, which are empty 83% of the time, or the r = 1 row
  are where the last fluctuation is decided, the difference of prices belongs to the death path, not to the living
  state.
- **A rimmed face without corners.** A slab face with one straight rim (a half-open slab cut by a second diagonal
  face) has the edge rows without the 0.175 corners. It would separate a corner price from an edge price, and
  give the price of an edge directly.
- **The variance.** The face population's variance is the one statistic with an area-like excess (+1% per cell,
  not a clean fit). Its space-time structure (the face-mode autocorrelation, as research/wraplocal measured on
  tubes) is the next local-ish quantity to try against the 10% price difference.
