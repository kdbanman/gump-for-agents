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

| row (d = 1 unless noted) | the coin of a replaced cell | seeds (generations) | deaths | ln τ | − gump |
|---|---|---|---|---:|---:|
| gump | (no noise) | 5001 (12 M) | 7,283 | 13.644 ± 0.012 | +0.011 ± 0.012 |
| (a) fair | 1/2 | 5101 (12 M) | 3,738 | 14.311 ± 0.016 | **+0.678 ± 0.016** (noisy/ pooled: +0.670) |
| (b) mean density | MEAN | 5111, 5112 (2 × 12 M) | 8,648 | 14.165 ± 0.011 | **+0.532 ± 0.011** (seeds +0.533, +0.532) |
| (c) density under a low face | LOW10 | 5121, 5122 (2 × 12 M) | 9,266 | 14.096 ± 0.010 | **+0.463 ± 0.010** (seeds +0.446, +0.481; χ² 2.8 on 1) |
| conditioned, all states | P(alive \| m live face neighbours) of gump, overall: depth 1 `c0.3753/0.4495/0.4454`, depth 2 `c0.4218/0.3970`, deeper MEAN | 5151 (12 M) | 4,478 | 14.130 ± 0.015 | +0.497 ± 0.015 |
| conditioned, low face | the same given face ≤ 10: `1:c0.3447/0.5165/0.5071,2:c0.4224/0.4305`, deeper LOW10 | 5141 (12 M) | 4,713 | 14.079 ± 0.015 | +0.446 ± 0.015 |
| shuffled, whole layer | the current state of a random cell of the whole layer at that depth | 5131 (12 M) | 8,718 | 13.464 ± 0.011 | **−0.169 ± 0.011** |
| shuffled, replaced core | the current state of a random replaced cell at that depth (`NZD_SRC=core`) | 5132 (6 M) | 5,679 | 13.199 ± 0.013 | **−0.434 ± 0.013** |
| frozen | MEAN, drawn once per life and held (`NZD_FROZEN=1`; N not stepped) | 5161 (12 M) | 2,258 | 14.815 ± 0.021 | +1.182 ± 0.021 |
| ε = 1/16 | MEAN, M = 64 | 5171 (12 M) | 6,250 | 13.797 ± 0.013 | +0.164 ± 0.013 |
| d = 2 (a) fair | 1/2 | 5201 (12 M) | 5,283 | 13.965 ± 0.014 | **+0.332 ± 0.014** (pooled +0.315) |
| d = 2 (b) mean | MEAN | 5211 (12 M) | 5,768 | 13.877 ± 0.013 | **+0.244 ± 0.013** |
| d = 2 (c) low | LOW10 | 5221 (12 M) | 5,561 | 13.914 ± 0.013 | **+0.281 ± 0.013** |
SCAN_ROWS


## The answer: mostly correlation, and it acts through the density the face's support has while the face is low

**Density alone is the smaller part [measured].** Coins at each replaced layer's own mean density keep **0.532 ± 0.011**
of the fair coins' 0.678 ± 0.016 at d = 1 (two seeds that agree to 0.001), and 0.244 of 0.332 at d = 2. The extra
density of fair coins (0.5 against 0.41–0.43) is worth +0.146 ± 0.020 at d = 1 and +0.088 ± 0.019 at d = 2: real, a
fifth to a quarter of the effect. The rest, +0.53 (d = 1) and +0.24 (d = 2), is there at gump's own density.

**Matching the density more carefully does not remove it [measured].** Coins at the density gump's replaced layer has
*when the face is low* (0.384 in layer 1): +0.463 ± 0.010 (two seeds, 1.7 σ apart). Coins that reproduce, cell by
cell, gump's dependence on the face above (the chance that a replaced cell is alive given how many of its face
neighbours are alive, overall or given a low face): +0.497 ± 0.015 and +0.446 ± 0.015. None of these coins is denser
than gump's layer in the state that matters, and all of them lengthen the life by a factor of 1.6.

**Coins that follow the layer shorten it [measured].** A replaced cell that copies the *current* state of a random cell
of its layer has the layer's density at every moment and is placed at random. The face then dies sooner: −0.169 ±
0.011 (copying from the whole layer), −0.434 ± 0.013 (copying from the replaced cells themselves). Random placement is
not what helps; independence from the face is.

**The variable that orders the chains [measured on four chains; that it is the controlling one is conjectured].** The
layer diagnostics (`NZD_LAYERS=1`, `python3 research/blast/density/chains.py data/layers/lay*.txt`) give, while the
watched face has at most 10 cells:

| chain | Δ ln τ | replaced layer-1 core alive, face ≤ 10 (≤ 4) | its count's variance / binomial, face ≤ 10 | supply (dead face cells with all 3 cells below alive), face 1–10 | births per unit supply | drift of the face (births − deaths per generation), face 1–10 |
|---|---:|---|---:|---:|---:|---:|
| shuffled core | −0.434 | 0.348 (0.351) | 2.47 | 4.13 | 0.386 | +1.59 |
| gump | 0 | 0.384 (0.407) | 1.81 | 4.19 | 0.395 | +1.69 |
| LOW10_CHAIN
| mean density | +0.532 | 0.435 (0.467) | 1.37 | 4.43 | 0.397 | +1.78 |

In gump the replaced core of layer 1 thins from 0.430 to 0.384 when the face is low (the whole layer 1 from 0.44 to
0.34): **the support fades with its face.** Coins do not respond to the face, and they hold up the rule-made cells
around them, so in the noisy chain the same cells stay at 0.435 under a low face (0.467 under a face of ≤ 4 cells), and
their count is less clustered (variance 1.37 of binomial against 1.81). The shuffled coins import the fading of the
layer they copy (0.348) and cluster the replaced cells (2.47). The supply of supported dead face cells rises with that
density; **the conversion of supply into births is the same in all chains** (0.386–0.397); the drift of a low face
rises by 0.1 per generation from gump to the coins and falls by 0.1 with the shuffle. Density and clustering move
together across these chains, so which of the two (or the joint law of the triple below a face cell) is the operative
one is not separated here.

**Not a last-moment rescue [measured].** `collect.py` splits ln τ = −ln f_k − ln P_k, f_k = descents of the face from
≥ 16 cells to ≤ k per hull-generation, P_k = the share of them that end in death before the face is back at ≥ 16. In
every chain, **P_1 is gump's 0.77 to within ± 0.02** (Δ ln P_1 from −0.021 to +0.011, errors ± 0.01): a face down to one cell
dies as often with coins under it as without. The coins act on the whole descent: at d = 1 fair, Δ ln f_k = −0.23 at
k = 15 (dips below 16 are rarer, consistent with the mean population 31.25 → 31.42 and its spread 5.24 → 5.16),
−0.60 at k = 4, −0.65 at k = 1; the passage from 15 to 4 cells carries −0.37 of the −0.68. The shuffled rows are the
mirror image (+0.18, +0.44 at k = 1).

**What this says about what kills a face [conjectured].** The face and the first layer under it fail together: when
the face thins, layer 1's cells lose their face neighbours and thin too (gump's layer 1 leads the face's population
by one to two generations: correlation +0.30 at lags 1–2), which removes the supply of supported dead face cells, which
slows the face's recovery. Coins cut this loop and lengthen the life; copied coins tighten it and shorten it. The face's
lifetime is a property of the face and its first two layers as one coupled system (depth 6 does nothing, d = 2 → 1
adds +0.35 through 9 cells), so a face law that treats the support as an independent bath of gump's density
overestimates the life (by 0.53 in ln τ at 63 cells). The effect grows with the rate of replacement: +0.164 ± 0.013
at ε = 1/16 against +0.532 at ε = 1/4 (mean density).

**Frozen coins are a different effect [measured; the explanation is conjectured].** Coins at the mean density drawn
once per life and held give +1.182 ± 0.021, twice the fresh coins' gain, although in that chain the replaced core under
a low face is *sparser* than gump's (0.305; 0.249 at ≤ 4), the supply lower (4.05), the conversion lower (0.329), the
drift lower (+1.52). A frozen substrate is quenched disorder: a life on a sparse substrate falls low often, a life on
a full one hardly ever, and the mean life (what the exposure-to-deaths ratio measures) is dominated by the good
substrates (longest life 2.15 × 10⁶ against 1.0–1.8 × 10⁶ elsewhere). That would make the conditional densities a
selection, not a response, and the gain a Jensen effect. Not checked: the distribution of lifetimes by substrate.

## Not checked, and what is weak

- **Second seeds** were run for (b) and (c) at d = 1 only; every other row is one seed. The conditioned rows use
  tables from a 20,000-generation run (seed 5); the 2 × 10⁶-generation run (`data/layers/lay_gump_d1_s6001.txt`)
  gives the same to ± 0.003 except two thin cells of the low-face table (core 1 with two live face neighbours 0.500
  against 0.507 used; core 2 with one, 0.443 against 0.431).
- The layer diagnostics of the noisy chains are short (5 × 10⁵ to 10⁶ generations); their ln τ are not used. Their
  densities at face ≤ 4 rest on ~10⁴ hull-generations, correlated.
- Density and clustering of the support are not separated (they move together in the chains measured); the joint law
  of the three cells under a dead face cell was not measured directly (only the supply, which counts it).
- 45 and 84 cells: not run (84 cells is out of reach of brute force at this cost: ~40 deaths per 12 M generations);
  frozen coins at density 1/2, ε = 1/16 with fair coins, and the d = 2 second seeds were dropped for time (the machine
  ran at load 6–10 on four cores, rows took 25–55 minutes instead of 12).
- The shuffle from the whole layer at depths 6–8 copies from layers whose densities were not measured.
- `nzd.c`'s REC counting is checked against a Python recount on one short run (R = 9); the layer diagnostics only by
  their group sizes and by the face group reproducing the population.

## Reproduce

```sh
python3 research/blast/density/validate.py 1200            # VALIDATION PASSED (data/validate_1200.txt)
S=research/scratch/blast/density; gcc -O3 -march=native -o $S/nzd_prod research/blast/density/nzd.c -lm
NZD_LAYERS=1 $S/nzd_prod 11 brute 1 4000000 0 1 3          # gump's layers (data/layers/gump_R11_s1_4M.txt; 15 min)
sh research/blast/density/row.sh mean_d1 11 5111 12000000 256 1 1:0.4301,2:0.4094,3:0.4149,4:0.4166,5:0.4157,*:0.4157
#   every row: the line "BIAS seed ..." of its file in data/rows/ gives the bias string; tags and seeds as in the table;
#   env: shuffled NZD_SRC=core (core) or nothing (whole layer) with BIAS s; frozen NZD_FROZEN=1; layer runs NZD_LAYERS=1
#   binaries: rows up to shuf_d1 ran on scratch nzd_prod (nzd.c at commit 32aafd9), the conditioned rows on nzd_prod2
#   (edbebd1), frozen and eps = 1/16 on nzd_prod3 (f9b2f1c), layer runs on nzd_lay/nzd_lay2 (edbebd1 / the VAR lines),
#   the 4 M gump layer run on a build just before 32aafd9 (same stepper; it differed only in the noise code, unused at M = 0);
#   later versions only add modes and diagnostics, and validate.py passed on each (nz.c's BRUTE lines unchanged).
python3 research/blast/density/collect.py                    # the table, pooled by tag, and the excursion split
python3 research/blast/density/chains.py research/blast/density/data/layers/lay*.txt   # the support table
python3 research/blast/density/drift.py research/blast/density/data/layers/lay_gump_d1_s6001.txt research/blast/density/data/layers/lay_mean_d1_s6111.txt
```
