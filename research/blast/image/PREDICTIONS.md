# blast/image: forecasts, frozen before the data

## Block 1: 03:36 UTC 2026-11-18, before any run of mine (only research/wraplocal's tables seen)

Theory to be tested (derivation in README.md): the torus measure is the loop-free measure tilted by the
**recurrence ratio of the seam** (exact for a soup-started CA, transfer operator along the loop):
P_T(pattern π on a window W) = P_c(π) · E_c[Q | π] / Z, and to lowest cluster order E_c[Q | π] ≈ r_W(π) =
P_c(pattern at W+v equals π | pattern at W is π) / P_c(π). So f_W(v) = ρ − Σ_π x_c(π) P2(π,π)/P(π) / Σ_π P2(π,π)/P(π),
everything measured on the loop-free torus (1,18),(0,49), nothing fitted. Windows: one cell; the cell and its 6
in-layer neighbours; the cell and its 9 neighbours in the slab; the cell's own 6-generation history.

| # | forecast | P |
|---|---|---:|
| I1 | the one-cell window gives \|f_W\| < 5% of the measured f at loop² 9 and at 12 (the pair correlation at v is too small: f_W = −C(v)(1−2ρ)/(ρ(1−ρ)) ≈ 0.14·C(v)) | 85% |
| I2 | the 10-cell window (cell + 9 slab neighbours) gives the right sign (emptier, f_W > 0) at loop² 9 and at 12, each resolved at > 2 standard errors | 50% |
| I3 | the 10-cell window gives f_W(9) within a factor 2 of 0.006267 | 25% |
| I4 | the 10-cell window's f_W(12)/f_W(16) lies in [2.1, 3.9] (measured law: 3.02) and is resolved (error < 1) | 12% |
| I5 | f_W(21) of the 10-cell window is not resolved (its error exceeds the measured 0.000181) | 80% |
| I6 | the space-time correlation C(v,τ) = Cov(x(y,t), x(y+v,t−τ)) exceeds 3 × \|C(v,0)\| in absolute value at some τ in 2..10, at loop² 9 or 12, resolved at > 3 standard errors | 55% |
| I7 | f_W grows monotonically with the window (1 cell < 7 cells < 10 cells) at loop² 9 | 55% |

Formula values asked for by the brief, stated before the run: I expect the 10-cell window to carry a minority of f
(my median: 30% of f(9)), with f_W(12)/f_W(16) ≈ 3 ± 2 if resolved and f_W(21) = 0.0000 ± 0.0004 (unresolved).
Conditioned ratio (not to be measured tonight unless the living-state part is done): sign positive (the image
term is larger in a depleted face); size from f_λ = f + λ·δs² with wraplocal's δs²/f = 10.6 at loop² 12: about 6
at the tilt λ ≈ 0.5, about 8 at half population. 50% that a measurement would land within a factor 2 of that.

## Block 2: 03:45 UTC, before the first production run has finished (no production number seen; only 5-snapshot smoke tests, pure noise)

The lag run (`img.py run … SEED 1`): the tilt of the 10-cell window at generation t, read in the cell's own density at
t + k, k = −6..6. (The exact law gives −f at every k once the window is the whole seam; a truncated window gives a
profile, and the first-order sum over windows in time is its sum over k, overlaps not corrected.)

| # | forecast | P |
|---|---|---:|
| L1 | at loop² 9 the shift at k = 0 is the largest in size, and \|shift(±3)\| < half of it | 60% |
| L2 | at loop² 9 the sum over k = −6..6 is between 1.5 and 4 times the k = 0 value | 40% |
| L3 | minus that sum is within a factor 1.5 of f at loop² 9 and at loop² 12 both | 20% |
| L4 | the shift of (x + in-layer neighbour count) under the 10-cell tilt is more than 3 times the shift of x alone at loop² 9 (the tilt lowers the neighbours about as much as the centre) | 50% |

## Block 3: 03:50 UTC, after the first production run (block 1 scored in README), before the history run

Seen: equal-time windows carry nothing (10 cells: −5% ± 4% of f(9)); the cell's own 6-generation history carries
+9% ± 1% of f(9) with the right sign. Also seen: C(v,τ) has a lag pattern of period 4 (about −15 and −30 × 10⁻⁶ at
τ ≡ 1, 2 mod 4, the same at every loop length 12–25) in a run sampled every 4 generations. The block-2 lag run was
stopped unfinished (its window carries nothing); L1–L3 will not be scored.

History run (`img.py hist …`, sampled every 5 generations): windows = the cell's own history over 3, 6, 9, 12
generations, and the 6-generation histories of the cell and one in-layer perpendicular neighbour together.

| # | forecast | P |
|---|---|---:|
| H1 | f_W(9) grows with the history's length: h3 < h6 < h9 < h12 | 55% |
| H2 | the 12-generation history gives more than 15% of f(9) | 40% |
| H3 | … more than 30% of f(9) | 15% |
| H4 | two neighbouring cells' 6-generation histories give more than twice the single cell's at loop² 9 | 35% |
| H5 | sampled every 5 generations, the period-4 lag pattern of C(v,τ) is gone (\|mean over τ ≡ 2 mod 4\| < 12 × 10⁻⁶ at loop² ≥ 12): it was the ensemble's mean density depending on the generation number mod 4, not a correlation | 55% |
| H6 | the mean face density by generation mod 4 differs between two phases by more than 3 × 10⁻⁵ at more than 2.5 standard errors | 40% |
