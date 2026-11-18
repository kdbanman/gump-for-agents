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
