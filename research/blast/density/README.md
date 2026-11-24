# research/blast/density: do coins lengthen a hull face's life by their density or by their independence?

Solver session, 2026-11-24 (from 11:16 UTC). Question (open problem 9 (r)): fair coins at depth ≥ d under the watched
63-cell face of the R = 11 hull, at ε = 1/4, lengthen its life (ln τ +0.003 … +0.670 for d = 6 … 1, pooled; gump
13.633 ± 0.001). Coins differ from the layer they replace in density (0.5 against gump's ≈ 0.42) and in being
uncorrelated with the face. Which one does it?


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

## Gump's own layers under the watched face [measured]

`NZD_LAYERS=1 nzd 11 brute 1 4000000 0 1 3` (gump, R = 11, 2.04 × 10⁹ hull-generations; `data/layers/gump_R11_s1_4M.txt`).
"core k" = the cells at depth k under the watched face and ≥ 3 under every other face = **the cells a dart replaces**
(9, 9, 18, 18, 21 cells at k = 1 … 5; 57 at k ≥ 6); "full k" = the whole layer (63, 75, 75, 81, 81 cells). Face
population: mean 31.25 of 63; "low" = at most 10 (a third of the mean; 3.4 × 10⁻⁴ of the time) or at most 6 (5 × 10⁻⁵).

| layer | all | face ≤ 20 | face ≤ 15 | face ≤ 10 | face ≤ 6 | face ≤ 4 | face ≤ 2 |
|---|---|---|---|---|---|---|---|
| core 1 (replaced) | 0.4301 | 0.393 | 0.388 | **0.3836** | 0.3919 | 0.401 | 0.417 |
| core 2 | 0.4094 | 0.405 | 0.415 | **0.4280** | 0.4391 | 0.443 | 0.445 |
| core 3 | 0.4149 | 0.415 | 0.418 | 0.4205 | 0.4196 | 0.418 | 0.414 |
| core 4 | 0.4166 | 0.417 | 0.418 | 0.4184 | 0.4179 | 0.417 | 0.418 |
| core 5 | 0.4157 | 0.416 | 0.416 | 0.4160 | 0.4157 | 0.415 | 0.414 |
| core ≥ 6 | 0.4157 | 0.416 | 0.416 | 0.4158 | 0.4160 | 0.416 | 0.415 |
| full 1 | 0.4411 | 0.374 | 0.355 | 0.3425 | 0.3432 | 0.347 | 0.357 |
| full 2 | 0.4571 | 0.443 | 0.445 | 0.4494 | 0.4542 | 0.457 | 0.459 |

- **Only layer 1 fades with its face**, and not much where it is replaced: the core of layer 1 goes from 0.430 to 0.38
  when the face is low; the whole of layer 1 from 0.44 to 0.34. Layer 2's core *rises* (0.41 → 0.43–0.44), deeper
  layers do not move (to ± 0.005). Coins at 0.5 are denser than every replaced layer in every state of the face.
- Lagged correlation (`LAG` lines) between the face's population and the layer's: full layer 1 +0.375 at lag 0, and
  the layer leads: corr(layer at t − L, face at t) = +0.30 at L = 1–2, +0.17 at 4, +0.09 at 8, against +0.09, +0.08, +0.09,
  +0.06 with the face leading; the replaced core of layer 1 only +0.106 at lag
  0 and ≤ 0.05 after; core 2 +0.04; deeper ones < 0.03. The face itself: +0.52 at lag 1, +0.21 at 4, +0.09 at 8.
- Not checked: the deep densities per depth (6, 7, 8 are pooled as "core ≥ 6"); the errors of these densities are not
  computed (correlated samples); a 20,000-generation run on another seed (5) agrees to ± 0.005 at face ≤ 10.

## The control: 63 cells, ε = 1/4 [measured]

Every row: `sh research/blast/density/row.sh TAG 11 SEED GENS M DW BIAS` (output `data/rows/TAG_sSEED.txt`), the table
by `python3 research/blast/density/collect.py`. ε = 1/4 is M = 256 at d = 1 (B = 1,024), M = 128 at d = 2 (B = 512).
ln τ of the watched face = ln(exposure / its deaths) ± 1/√deaths; "− gump" against 13.633 ± 0.001 (this session's own
gump row, seed 5001: 13.644 ± 0.012). Bias strings: MEAN = `1:0.4301,2:0.4094,3:0.4149,4:0.4166,5:0.4157,*:0.4157`,
LOW10 = `1:0.3836,2:0.4280,3:0.4205,4:0.4184,5:0.4160,*:0.4158` (the table above; deeper than 5: the "core ≥ 6" value).

RESULTS_TABLE

