# blast/ref-proofs: forecasts frozen before data

Breach, stated plainly: the recomputations of rigour's exact rows, the 18-cell simulations (hull_R5, torus_2_0_3)
and the seam enumerations were run with no forecast on file (they were checks of numbers already on file).

## 04:34 UTC, before any line of `data/mc_tube11.txt` beyond the first header existed

My own simulation (`ref.py torus 1 1 D --mc N --mconly`, 2·10⁵ replicas, deaths later than 40 generations after
a fair start) of the surrogate's tube (1,1),(0,D), D = 6, 8, 10, 12, against rigour's rows (weighted ln τ:
5.1064, 6.7278, 8.2757, 9.7304; bust shares 0.8105, 0.7131, 0.5772, 0.4165):

- **P1 (85%).** All four ln τ agree with rigour's within 2.5 combined standard errors.
- **P2 (75%).** All four bust shares agree within 2.5 combined standard errors.
- **P3 (70%).** From my four points alone, −Δ ln h_starve per unit of length over 8→10 and 10→12 both lie in
  [0.54, 0.63] (rigour's reading: constant at 0.585), and −Δ ln h_bust over the same steps both lie in [0.80, 0.95].

## 04:37 UTC, before `tiltmc.py` was run on anything

The population law under the tilted measure μ_s ∝ μ·e^(−sE), by reweighting simulated quasi-stationary states, on
the wide tori (2,0),(0,3) (18 cells) and (3,0),(0,3) (27 cells) and the triangles of 18 and 30 cells. "Two-humped" =
P_s(pop = n) has a local minimum between a sparse and an over-full maximum, the upper maximum at least 1.5 times the
valley, beyond the sampling noise.

- **T1 (55%).** Torus 18 cells, s = 0.3: two-humped. At s = 0.5: two-humped (75%).
- **T2 (45%).** Torus 27 cells, s = 0.3: two-humped. At s = 0.5: two-humped (60%), if the reweighting resolves it
  (effective sample above 10³).
- **T3 (80%).** Both triangles, s = 0.3 and 0.5: one hump.
- **T4 (50%).** On the 27-cell torus at s = 0.3 the weight above the valley is at least 0.15 (fails also if T2 fails).

## Scores (04:45 UTC)

- T1: **passes** at both tilts (18-cell torus, s = 0.3: valley 0.014, upper maximum 0.054; s = 0.5: 0.001, 0.040).
- T2: **passes** at both tilts (27-cell torus, s = 0.3: 0.003, 0.044; s = 0.5: below 0.0005, 0.019; effective samples
  3.7·10⁵ and 1.25·10⁵).
- T3: **passes** (triangles of 18 and 30 cells: one hump at s = 0.3 and 0.5; a flat plateau at s = 0.2 on 30 cells).
- T4: **passes** (weight above the valley 0.235).
- P1: **passes** (ln τ within 0.4σ of rigour's at D = 6, 8, 10, 12).
- P2: **passes**, narrowly (bust shares within 0.5σ at D = 6, 8, 10; at D = 12 mine is 0.4442 ± 0.0064 against
  0.4165 ± 0.0102, 2.3σ).
- P3: **passes** (8→10: 0.581 ± 0.007 and 0.880 ± 0.006; 10→12: 0.588 ± 0.010 and 0.858 ± 0.011).

Seven of seven; none of these forecasts was bold.
