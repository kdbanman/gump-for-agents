# research/blast/density: do coins lengthen a hull face's life by their density or by their independence?

Solver session, 2026-11-24 (from 11:16 UTC). Question (open problem 9 (r)): fair coins at depth ≥ d under the watched
63-cell face of the R = 11 hull, at ε = 1/4, lengthen its life (ln τ +0.003 … +0.670 for d = 6 … 1, pooled; gump
13.633 ± 0.001). Coins differ from the layer they replace in density (0.5 against gump's ≈ 0.42) and in being
uncorrelated with the face. Which one does it?

(Account in progress; results below are filled in as rows finish.)

## Files

- `nzd.c`: the brute-force path of `research/blast/noisy/nz.c` (copied; `nz.c` is not edited) with coins whose bias
  depends on the depth of the cell (depth under the watched face, `(R − (x+y+z))/2`), a shuffled coin (the current
  state of a random cell of the same layer), frozen coins, and diagnostics: the watched face's excursions (`REC`), the
  layers' densities by the face's population (`LAYER`, `BYPOP`), lagged correlations (`LAG`), and the face's births
  split by the support below (`DRIFT`). Header comment = the exact statement of each.
- `validate.py`: the checks below. `row.sh`, `queue.sh`: one row; a worker that takes rows from a queue file.
- `collect.py`: the table of rows, pooled by tag, and the excursion decomposition.
- `data/`: `validate_1200.txt`, `rows/` (every row's full output), `layers/` (the layer measurements).
- Bulk: `research/scratch/blast/density/`.

## The program and its validation [measured]

`python3 research/blast/density/validate.py 1200` → `VALIDATION PASSED` (`data/validate_1200.txt`):

1. With no noise the stepper is gump bit for bit against `reference/oracle.py` at R = 11 and R = 9 (3 soups × 1,200
   generations, every cell, the watched population, the other faces' emptiness); negative control (one neighbour
   swapped) fails at generation 4 and 7.
2. The coins: with a different bias at each depth (0.1, 0.9, 0.3, 0.42, 0.7 …) the share of the cells of N at depth d
   set alive (dead) by one noise call from an all-dead (all-live) state is q p_d (q (1 − p_d)) within 5 σ, q = 1 − (1 −
   1/B)^M; nothing outside N changes; the fair path and bias 1/2 through the comparison path give 1/2; the shuffled
   coin's sources match their definition, change nothing on an all-alive or all-dead hull, and copy the source's
   alive share. Negative control: coins of bias 0.6 checked as 0.5 fail.
3. With every bias 1/2 and the same seed, the BRUTE line is nz.c's, character for character, in five settings (R = 11
   at d = 1, 2, 6 with ε = 1/4; R = 9 at d = 6; no noise). Negative controls: bias 1/2 through the comparison path
   (`NZD_GENERAL=1`, the same law from another stream) and another seed give different lines.
4. The excursion counts (`REC`) are recomputed in Python from a dump of every lane's watched population and
   other-face bit (R = 9, 30,000 generations) and agree exactly.
5. The layer groups have the sizes of their definition; the group "face" reproduces the watched population.

A biased coin is a comparison of 16 bits of a second random stream with round(p 2¹⁶): its bias is that integer / 2¹⁶
(printed). The main stream (number, squares and order of the darts, the soups) is the one nz.c uses whatever the bias.
