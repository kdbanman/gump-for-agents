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
