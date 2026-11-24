# research/blast/density: do coins lengthen a hull face's life by their density or by their independence?

Solver session, 2026-11-24 (from 11:16 UTC). Question (open problem 9 (r)): fair coins at depth ≥ d under the watched
63-cell face of the R = 11 hull, at ε = 1/4, lengthen its life (ln τ +0.003 … +0.670 for d = 6 … 1, pooled; gump
13.633 ± 0.001). Coins differ from the layer they replace in density (0.5 against gump's ≈ 0.42) and in being
uncorrelated with the face. Which one does it?


**In brief (2026-11-24, 13:55 UTC).** Mostly correlation [measured]: at d = 1, coins at each replaced layer's own mean
density keep +0.532 ± 0.011 of the fair coins' +0.678 ± 0.016 (d = 2: +0.244 of +0.332); at the layer's density under
a low face +0.463 ± 0.010. Coins that copy the layer's current state shorten the life (−0.17, −0.43). The mechanism
[measured on four annealed chains; its sufficiency conjectured]: gump's support fades with its face (the replaced core of layer 1
from 0.430 to 0.384 when the face has ≤ 10 cells), the coins' does not (0.42–0.44), and the lives order by that
low-face density; the births per supported dead face cell are the same in every chain, and a face down to one cell
dies as often (0.77) with coins as without, so the coins slow the whole descent rather than rescue the last cell. The
gain vanishes at a coin density of about 0.19: for its face, gump's own layers are worth independent coins of 0.19.
Frozen coins (+1.18) are a separate, disorder effect. Block 4: items 1, 2, 4 true, 3 false.

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
| (d) scan: every depth at p | 0.1 | 5109 (2.5 M) | 2,115 | 13.312 ± 0.022 | −0.322 ± 0.022 |
| | 0.2 | 5102 (3 M) | 1,763 | 13.676 ± 0.024 | +0.043 ± 0.024 |
| | 0.3 | 5103 (3 M) | 1,404 | 13.904 ± 0.027 | +0.271 ± 0.027 |
| | 0.4 | 5104 (2.5 M) | 1,000 | 14.061 ± 0.032 | +0.428 ± 0.032 |
| | 0.5 | = (a) | | | +0.678 ± 0.016 |
| | 0.7 | 5107 (3 M) | 690 | 14.614 ± 0.038 | +0.981 ± 0.038 |

Not run: the scan at 0.6, 0.8, 0.9 (time). Every scan row is one seed.


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
| density under a low face (LOW10) | +0.463 | 0.423 (0.455) | 1.35 | 4.41 | 0.395 | +1.77 |
| mean density | +0.532 | 0.435 (0.467) | 1.37 | 4.43 | 0.397 | +1.78 |

**The LOW10 chain is the density-matched control in effect:** its coins are at 0.384, but the replaced cells of layer 1
(coins and rule-made cells together) end up at 0.428 on average, gump's own 0.430, and at 0.423 under a low face
instead of gump's 0.384. Same density, no fading: +0.463. The four annealed chains are in the same order by this
low-face density as by their lives (0.348, 0.384, 0.423, 0.435 → −0.43, 0, +0.46, +0.53).

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

**The density at which the effect vanishes [measured].** With every replaced depth at density p, the gain rises
steadily with p, about +2.5 per unit of density from 0.2 to 0.7 (−0.32, +0.04, +0.27, +0.43, +0.68, +0.98 at p = 0.1,
0.2, 0.3, 0.4, 0.5, 0.7), and **crosses zero at p\* ≈ 0.19** (linear between 0.1 and 0.2; ± 0.01 from the two rows'
errors). For the face, gump's own layers are worth fresh independent coins of density 0.19, less than half their own
density of 0.42. Read as a face law [conjectured]: the face's life depends on the density of its support *while it is
low*, and gump's support delivers there what an independent support of 0.19 would; a model of the face over an
independent bath must use that effective density, not the measured one, and the effective density is set by the
coupling of the face to its first layer (it would have to be computed, not read off the layers).

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
  frozen coins at density 1/2, ε = 1/16 with fair coins, the scan at 0.6, 0.8, 0.9, and the d = 2 second seeds were dropped for time (the machine
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

## Scores of block 4 of `research/blast/noisy/PREDICTIONS.md` (opened 13:52 UTC, after commit 5b07607 held every result above)

| item | forecast | outcome |
|---|---|---|
| 1. at matched density the d = 1 gain is ≥ 0.40 | 70% | **true**: +0.532 ± 0.011 at the layers' mean density (two seeds), +0.463 ± 0.010 at their low-face density. (The 12% for "≤ 0.15": false.) |
| 2. at matched density the d = 2 gain is ≥ 0.18 | 65% | **true**: +0.244 ± 0.013 (one seed); +0.281 ± 0.013 at the low-face density |
| 3. coins at a third of the layer's density (≈ 0.14) still lengthen the d = 1 life | 55% | **false**: p = 0.1 gives −0.322 ± 0.022, p = 0.2 +0.043 ± 0.024; the gain crosses zero at p ≈ 0.19, so at 0.14 the life is shorter (≈ −0.2 by interpolation) |
| 4. no coin density between 0.2 and 0.8 shortens the d = 1 life | 80% | **true as far as measured** (0.2, 0.3, 0.4, 0.5, 0.7 all ≥ 0; 0.6 and 0.8 not run), with the margin at 0.2 only 1.8 σ. Coins whose density *follows* the layer (shuffled) do shorten it, −0.17 and −0.43, but they are not a fixed density. |

The PI's reading ("what they do that gump does not is hand a fading face live cells beneath it at times when gump's own
layer is fading with it") is what the layer diagnostics show: gump's replaced core thins from 0.430 to 0.384 under a low
face, the coin chains' does not (0.423–0.435).

---

## 2026-11-24, second task (from 13:55 UTC): is the equivalent coin density p\* a constant?

Question (the PI): at ε = 1/4, d = 1, 63 cells, coins of density p\* ≈ 0.19 at every replaced depth leave the
watched face's life unchanged. Is p\* a property of gump's support, the same at every replacement rate and face size,
so that a face of gump behaves like a face over independent coins of density p\*? Forecasts: `PREDICTIONS.md`
(committed at 70de9e5 before any row of this task ran; scored at the end of this section).

**New in the program [measured].** `NZD_FULL=1`: full replacement. After every step each cell of the noise region, in
every lane, is set to a fresh coin of its depth's bias, independent of everything (64 lanes at a time, bit-serially
from 16 words of the second stream, so the bias is exactly round(p 2¹⁶)/2¹⁶). This is the PI's "ε = 1": the dart
process cannot reach it (M darts at B squares replace a cell with probability 1 − (1 − 1/B)^M: 0.63 at M = B, the
dart ε = 1; 0.98 at M = 4B), so full replacement is a separate mode, not a dart setting. `NZD_CLUST=c` (with full
replacement): per depth, lane and generation, with probability c every replaced cell of that depth takes one common
coin, else each its own: the density is unchanged and two replaced cells of the same depth are correlated by c (a
count of n such cells has variance (1 + (n − 1) c) times binomial). `row.sh` takes `DO=` from the environment.
`validate.py 1200` passes with both (`data/validate_1200.txt`): full replacement sets every replaced cell to a coin of
the right bias from an all-dead and an all-alive state, changes nothing else, two calls are independent, and outside
the noise region the stepper is the oracle's step of the previous state (200 generations, two lanes, R = 11 and 9);
the clustered coin has the right density, correlation c within a depth and none across; negative controls (a bias
0.21 checked as 0.19; c = 0.3 checked as 0) fail. `zeros.py` locates each zero: a weighted line through the rows with
|Δ| < 0.2 (at least the two that bracket it), p\* = −a/b with its error by the delta method from the row errors (death
counts), scaled by √(χ²/dof) when that exceeds 1, plus the gump reference's error / slope. Gump references: 63 cells
13.633 ± 0.001; 45 cells 9.8177 ± 0.0036 (the watched face: nz's 9.8161 ± 0.0044 pooled with this session's
`R9_gump` row, 9.821 ± 0.006). Every row is one seed; rows are `data/rows/<tag>_s<seed>.txt`, made by
`sh research/blast/density/row.sh <tag> R <seed> GENS M 1 P [NZD_FULL=1] [NZD_CLUST=c] [DO=1]` (the BIAS line of each
file repeats its settings; M = 256 at R = 11 and 64 at R = 9 for ε = 1/4, 64 and 16 for ε = 1/16, 0 with NZD_FULL).

### p\* by replacement and size [measured]

`python3 research/blast/density/zeros.py` (every row listed there with its Δ ± error and deaths):

| replaced | 45 cells | 63 cells |
|---|---|---|
| darts, ε = 1/16 (q = 0.061 a cell and generation) | 0.16 ± 0.03 (slope 0.23 ± 0.07; rows p = 0.1, 0.2, 0.3) | **0.173 ± 0.010** (slope 0.88 ± 0.10; 0.1, 0.2, 0.3) |
| darts, ε = 1/4 (q = 0.221) | **0.180 ± 0.006** (slope 0.93 ± 0.07; 0.1 … 0.3, six rows) | **0.191 ± 0.003** (slope 5 ± 1; 0.175, 0.2) |
| full replacement (q = 1) | **0.266 ± 0.002** (slope 4.0 ± 0.3; 0.26 … 0.31, five rows) | **0.316 ± 0.001** (slope 11 ± 1; 0.30, 0.317, 0.32) |
| full replacement, noise region also at depth ≥ 1 under the other faces (DO = 1) | **0.3848 ± 0.0001** (slope 49 ± 1; 0.38, 0.39) | **0.3854 ± 0.0002** (slope 74 ± 3; 0.38, 0.39) |

Rows near each zero have 1,750–7,150 deaths at 63 cells and 9,000–21,000 at 45 cells. The replaced core under
the watched face is 3 cells in each of layers 1 and 2 at 45 cells, 9 at 63 cells; with DO = 1 it is 30 of layer 1's 45
cells at 45 cells and 45 of 63 at 63 cells (the rest of layer 1 lies on another face: the hull's edges).

- **p\* is not a constant [measured].** It rises with the replacement: at 63 cells 0.173, 0.191, 0.316 for q = 0.06,
  0.22, 1; at 45 cells 0.16, 0.180, 0.266, and 0.385 when nearly the whole support is replaced (DO = 1). Between ε = 1/16
  and 1/4 it moves little (63 cells: +0.018 ± 0.010; 45 cells: +0.02 ± 0.03), as the effect there is close to linear
  in q (the slope rises in proportion: 0.88 → ~5 at 63 cells, 0.23 → 0.93 at 45). From 1/4 to full replacement it
  jumps by 0.09–0.13.
- **Nor is it the same at both sizes at full replacement [measured]:** 0.266 ± 0.002 against 0.316 ± 0.001. With the
  63-cell p\* the 45-cell face lives *longer* than gump's: `R9_full_p0.317` gives +0.210 ± 0.007. At ε = 1/4 the two
  sizes agree within 1.6 σ (0.180 ± 0.006, 0.191 ± 0.003).
- **What p\* measures [conjectured].** With partial replacement the coins are mixed with rule-made cells that they hold
  up (part 1: the LOW10 coins at 0.384 raised the replaced cells to 0.423 under a low face), so a low coin density
  already matches gump; p\* ≈ 0.18–0.19 is a property of that mixture, not of gump's support alone. With the replaced
  share growing (full replacement, then DO = 1) p\* climbs towards the density of an independent support that does
  gump's job by itself: 0.385 at 45 cells, a little below gump's own layer densities under a face (layers 1 and 2:
  0.44 and 0.46 overall, 0.34 and 0.45 under a low face; part 1). At 45 cells the replaced core is a smaller share of
  the face's support than at 63 cells (3 of 45 cells against 9 of 63 in layer 1), which is one reason the
  full-replacement p\* differs between the sizes (DO = 1 replaces 2/3 of layer 1 at both).
- **With nearly the whole support replaced, one density serves both sizes [measured].** DO = 1 puts every cell that is
  not on one of the eight faces under full replacement (876 − 366 = 510 cells at 63 cells, 264 at 45): p\* =
  0.3848 ± 0.0001 at 45 cells and **0.3854 ± 0.0002 at 63 cells**, equal to 0.0006 (2.7 σ of the counting errors, which
  are tiny here because the life is so steep in p; seed scatter not measured). A face over independent coins of
  density 0.385 has gump's ln τ at 45 and at 63 cells, so the same slope in A between them (3.815 over 18 cells,
  0.212 a cell). The steepness grows with the face (49 and 74 per unit p, 1.09 and 1.17 per cell), as it should if
  ln τ ≈ A λ(p) + const. An 84-cell row at p = 0.385 (`R13_fullDO1_p0.385`, R = 13, 5 × 10⁶
  generations, only 45 deaths: lives there outlast the run) gives ln τ = 17.857 ± 0.149 against gump's 18.141 ±
  0.005 (`research/blast/noisy/README.md`; all faces, ties included): **Δ = −0.28 ± 0.15**, 1.9 σ low. With a slope near
  100 per unit p at that size this is p\*(84) ≈ 0.388 ± 0.002: consistent with the one density at 2 σ, not decided.
  From one cell that face dies 45 times in 46.
- **The face over a fully independent support is near a threshold [measured at 45 cells].** With DO = 1, Δ = −3.25,
  −3.92, −1.75, −0.49, −0.24, +0.26, +0.73 at p = 0.25, 0.30, 0.35, 0.375, 0.38, 0.39, 0.40: below 0.35 the whole hull
  dies within a few thousand generations (longest life 1,000–6,000; at 0.25 the faces hold 3 cells on average), and
  the life rises by a factor e^1 for every 0.02 in p near p\*. (Below 0.35 the rate is not a stationary one: lives end
  before or soon after the 200 generations of ageing-in; those rows only say "short".)


### Same rate, another way of dying (item 4) [measured]

`python3 research/blast/density/collect.py` (excursion split against the gump rows of the same size). At full
replacement and p = 0.317 (63 cells, `full_p0.317`, 12 M generations, 7,151 deaths, Δ = +0.029 ± 0.012, i.e. at p\*
within 0.002):

| k | 1 | 2 | 4 | 6 | 10 | 15 |
|---|---|---|---|---|---|---|
| Δ ln f_k (descents from ≥ 16 to ≤ k, per hull-generation) | −0.071 ± 0.015 | −0.142 | −0.263 ± 0.008 | −0.341 | −0.434 | −0.420 |
| Δ ln P_k (share of them that die before recovering) | +0.053 ± 0.008 | +0.124 | +0.244 ± 0.015 | +0.322 | +0.415 | +0.401 ± 0.017 |

The rate is gump's, the way there is not. Over independent coins the face dips below 16 cells a third less often
(Δ ln f_15 = −0.42), but a dip is 1.5 times as likely to end in death (Δ ln P_15 = +0.40), and the excess risk is spread
along the whole descent: +0.16 between 15 and 4 cells, +0.19 between 4 and 1, +0.05 at the last cell. **At one cell the
face dies with probability 0.81 (gump: 0.77).** The same at 45 cells (`R9_full_p0.27`, Δ = +0.013): Δ ln f_4 = −0.154,
Δ ln P_4 = +0.144, Δ ln P_1 = +0.028 ± 0.005. Reading [conjectured]: in gump many of the face's dips are shared with its
support (part 1: the layer fades with the face and leads it), and a dip driven by the support is undone when the
support recovers; over independent coins a dip is the face's own, rarer, and harder to undo.

**With the whole support replaced (DO = 1) the difference is far larger [measured]:** at 63 cells, between p = 0.38
(Δ = −0.40) and 0.39 (+0.34), Δ ln f_15 = −1.77 and −2.11, Δ ln P_15 = +2.18 and +1.78, Δ ln P_1 = +0.235 ± 0.006 and
+0.224 ± 0.007; at 45 cells (0.38, 0.39) Δ ln P_1 = +0.221, +0.218 ± 0.003. **Over independent coins of the equivalent
density a face that has fallen to one cell dies 96–98% of the time, against gump's 77%,** and dips below 16 cells are
6 to 8 times rarer while each is 6 to 9 times deadlier. The face is also fuller (mean 34.7 of 63 against 31.25, spread
5.0 against 5.2; at 45 cells 24.2 against 21.6). The rate is matched at both sizes by one density; the way of dying is
not matched at all.

### Clustering at fixed density (item 5) [measured]

Full replacement with clustered coins, same density (`NZD_CLUST=c`):

| | c = 0 | c = 0.1 | c = 0.3 |
|---|---|---|---|
| 45 cells, p = 0.27 | +0.013 ± 0.011 | −0.043 ± 0.010 (effect −0.056 ± 0.015) | −0.157 ± 0.010 (effect −0.170 ± 0.015) |
| 63 cells, p = 0.32 | +0.030 ± 0.015 | −0.260 ± 0.013 (**effect −0.290 ± 0.020**) | not run |

**Clustering of the support shortens the life at fixed density**, and much more under the larger face: c = 0.1 (a
count of 9 replaced cells then has 1.8 times the binomial variance, which is what gump's replaced core of layer 1 has
under a low face, part 1) costs 0.29 in ln τ at 63 cells, as much as lowering the density by 0.026 (slope 11). This
separates the two variables that moved together in part 1: both matter. The clustering of c = 0.1 is worth a density
of 0.026 at 63 cells and 0.014 at 45 (effect / slope). Not run: clustering at ε = 1/4, or a clustering that copies
gump's (here every replaced cell of a depth shares the common coin, near or far).

### The density scan at ε = 1/4, p = 0.8 (the PI's block 4, item 4) [measured]

`e4_p0.8` (3 M generations, 607 deaths): Δ = **+1.109 ± 0.041**. The scan at ε = 1/4 is now −0.32, −0.08, +0.04, +0.27,
+0.43, +0.68, +0.98, +1.11 at p = 0.1, 0.175, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8: no density between 0.2 and 0.8 shortens
the life (0.6 not run).

### One density at both sizes, tested directly [measured]

Rows at p = 0.385 itself, DO = 1, full replacement: 45 cells `R9_fullDO1_p0.385` (10⁶ generations, 25,307 deaths)
Δ = **+0.009 ± 0.007**; 63 cells `fullDO1_p0.385` (4 × 10⁶, 2,523 deaths) Δ = **−0.028 ± 0.020**. Both are gump's
life within 1.4 σ, as the interpolated zeros said (+0.01 and −0.03 expected). Its excursions at 63 cells: Δ ln P_1 =
+0.234 ± 0.006 (death from one cell 0.97), Δ ln f_15 ≈ −2.0, Δ ln P_15 ≈ +2.0.

### Answer to the question [measured, with the reading conjectured]

No: p\* is not a property of gump's support alone. With part of the support replaced it is a property of the mixture
of coins and the rule-made cells they prop up: 0.17–0.19 at ε = 1/16 and 1/4 (nearly the same at 45 and 63 cells),
0.27 and 0.32 at full replacement of the 3 or 9 cells under the middle of the face. Only when nearly the whole support
is coins (DO = 1, two thirds of layer 1 and everything below) does one density, **0.385**, give gump's life at both
45 and 63 cells (at p = 0.385 itself: +0.009 ± 0.007 and −0.028 ± 0.020), so the face law's slope as well as a point;
at 84 cells one row reads −0.28 ± 0.15 (1.9 σ, 45 deaths), not decided. Even then a face of gump is not a face over coins in its
way of dying: over coins it is fuller, dips 6–8 times less often below a quarter of its cells, and dies from one cell
96–98% of the time instead of 77%. Its rate is reproduced; its excursions are not.

### Scores of `PREDICTIONS.md` (this task)

| item | forecast | outcome |
|---|---|---|
| 1. p\*(1/16, 63) within 0.05 of p\*(1/4, 63) | 65% | **true**: 0.173 ± 0.010 against 0.191 ± 0.003 |
| 2. p\*(1/4, 63) in [0.17, 0.21] | 75% | **true**: 0.191 ± 0.003 |
| 3a. p\*(full, 63) within 0.05 of p\*(1/4, 63) | 40% | **false**: 0.316 ± 0.001 |
| 3b. … and higher | 60% | **true** |
| 4. slope at p\* ≥ 1.5 times larger at full replacement | 70% | **true**: 11 ± 1 against 5 ± 1 (63 cells); 4.0 against 0.93 (45) |
| 5. p\*(1/4, 45) within 0.05 of p\*(1/4, 63) | 50% | **true**: 0.180 ± 0.006 |
| 6. at full replacement the 63-cell p\* gives the 45-cell face gump's life within ± 0.03 | 40% | **false** as stated (DO = 3): +0.210 ± 0.007. With DO = 1 the two p\* agree to 0.0006, which would pass; that setting was not the one forecast. |
| 7a. at full replacement and p\*, P(death from 1 cell) = 0.77 ± 0.03 | 75% | **false**: 0.81 (DO = 3), 0.96–0.98 (DO = 1) |
| 7b. … and every Δ ln f_k, Δ ln P_k within ± 0.06 | 45% | **false**: up to ± 0.42 (DO = 3), ± 2.2 (DO = 1) |
| 8. ε = 1/4, p = 0.8: Δ > 0; in [1.0, 1.5] | 97%; 60% | **true; true**: +1.109 ± 0.041 |

The PI's block 5 (`research/blast/noisy/PREDICTIONS.md`, read after the above was committed), as these rows bear on it,
for the PI to score: (1) p\*(1/16) within 0.03 of p\*(1/4) at 63 cells: 0.173 against 0.191, yes; (2) p\*(full) below
0.17, or within 0.04 of 0.19: no (0.316); (3) the 45-cell p\* at 1/4 within 0.03 of the 63-cell one: 0.180 against
0.191, yes; (4) at full replacement and the 63-cell p\*, the 45-cell life within 0.15 of gump's: no with DO = 3
(+0.210 ± 0.007), yes with DO = 1 (+0.009 ± 0.007 at p = 0.385).

### Not checked (second task)

- Every row is one seed; the scatter between seeds of the steep DO = 1 rows (where an error of 0.0002 in p\* rests on
  counting alone) is not measured.
- p\*(1/4, 63) rests on two rows near the zero (0.175 with 5,320 deaths, 0.2 with 1,763); the planned 0.225 row was
  dropped for the 84-cell row. The curve is not straight over 0.1–0.3 at 63 cells (slope 3.6 then 2.3), so wider
  windows give other values (0.188 from 0.1 and 0.2).
- Full replacement at DO = 3 and DO = 1 are different hulls: with DO = 1 the other faces also sit on coins, and below
  p ≈ 0.35 lives end within the ageing-in, so those rows are not stationary rates.
- Not run: the dart process at ε = 1 (M = B, replacement 0.63; ~30 minutes a row at 63 cells); 84 cells except the one
  DO = 1 row; clustering at ε = 1/4 or a gump-like (local) clustering; 0.6 in the scan; frozen coins at other densities.
- The two full-replacement modes were validated against the oracle outside the noise region and statistically inside
  it; the excursion split was validated in part 1 (one Python recount).

### Reproduce (second task)

```sh
python3 research/blast/density/validate.py 1200       # VALIDATION PASSED, with the full and clustered modes
S=research/scratch/blast/density; gcc -O3 -march=native -o $S/nzd_cur research/blast/density/nzd.c -lm
#   (the rows ran on nzd_prod4 (44ce0cc) and, for NZD_CLUST, nzd_prod5 (578b461); the current nzd.c prints the same lines)
NZD_FULL=1 NZD_BIN=nzd_cur sh research/blast/density/row.sh full_p0.317 11 8737 12000000 0 1 0.317
DO=1 NZD_FULL=1 NZD_BIN=nzd_cur sh research/blast/density/row.sh fullDO1_p0.38 11 8786 4000000 0 1 0.38
NZD_FULL=1 NZD_CLUST=0.1 NZD_BIN=nzd_cur sh research/blast/density/row.sh fullc0.1_p0.32 11 8752 8000000 0 1 0.32
sh research/blast/density/row.sh e16_p0.2 11 8620 8000000 64 1 0.2          # darts, eps = 1/16
sh research/blast/density/row.sh R9_e4_p0.2 9 8902 400000 64 1 0.2         # 45 cells, eps = 1/4
#   every other row: tag, seed, generations and settings in the file name and its BRUTE and BIAS lines (data/rows/)
python3 research/blast/density/zeros.py     # every p* of the table, with the rows used
python3 research/blast/density/collect.py   # the excursion split per size
# exploration (300,000 generations, seed 77, not used for any number): data/explore/full63_p*.txt
```

---

## 2026-11-24, third task (from 15:05 UTC): the coincidence, the skin depth, 84 cells

Forecasts: `PREDICTIONS.md`, third block (committed at 7a84d46 before any run; scored at the end). New in the program:
per-cell densities in layer runs (`CELL` lines: each cell's density over the counted hull-generations, overall and
given the watched face has ≤ 20, 15, 10, 6, 4, 2 cells; a group's density is the mean of its cells'; checked on a
20,000-generation run against the group lines: equal to 5 decimals for the face, layer 1 and its core);
`cells.py FILE` prints every group by depth k and least depth j under the other faces ("DO ≥ j k"), its minimum over
the thresholds, and the bias strings below. The brute path is unchanged (`validate.py 1200` passes; the rows ran on
`nzd_prod4`, commit 44ce0cc).

### 1. The coincidence p\* ≈ gump's support at its thinnest: an accident [measured]

`NZD_LAYERS=1 nzd 9 brute 9901 2000000 0 1 3` and `nzd 11 brute 9911 1000000 0 1 3` (gump; `data/layers/lay3_gump_R9_s9901.txt`,
`lay3_gump_R11_s9911.txt`), then `python3 research/blast/density/cells.py FILE`. Density in gump, overall → its minimum
over the face thresholds (at which):

| cells of layer 1 (depth 1 under the watched face) | 45 cells | 63 cells |
|---|---|---|
| all of layer 1 (45; 63 cells) | 0.435 → 0.319 (≤ 4) | 0.441 → 0.341 (≤ 6) |
| **the ones the coins replace in the DO = 1 rows** (not on another face: 30; 45 cells) | 0.442 → **0.357** (≤ 4) | 0.444 → **0.367** (≤ 10) |
| at depth ≥ 2 under the other faces (9; 18) | 0.426 → 0.393 (≤ 6) | 0.429 → 0.386 (≤ 10) |
| the core, depth ≥ 3 under the others (3; 9) | 0.428 → 0.390 (≤ 6) | 0.430 → **0.384** (≤ 10) |
| every cell the DO = 1 coins replace, all depths (264; 510) | 0.426 → 0.420 (≤ 6) | 0.424 → 0.420 (≤ 15) |

The coins of the DO = 1 rows (density p at every cell not on a face) give gump's life at p\* = 0.3848 (45 cells) and
0.3854 (63 cells). The cells they replace in layer 1 have, in gump, 0.357 and 0.367 at their thinnest, 0.02–0.03 lower;
everything they replace, 0.420; the whole of layer 1, 0.32–0.34. Only the 9-cell core at 63 cells, at the ≤ 10
threshold, lands on p\* (0.3844); at 45 cells the core's minimum is 0.390 and it is reached at another threshold. **The
coincidence does not survive**: it compares the coins with a group they mostly do not replace, at one threshold, at one
size. (Not checked: errors of these conditional densities; they rest on 3 × 10³ to 2 × 10⁷ correlated hull-generations
depending on threshold and size. The 63-cell values agree with the 4 M-generation group run of part 1 to 0.002.)

---

## 2026-11-24, corrections after the referee (`research/blast/ref-density/REVIEW.md`, commit 07d2708)

The referee reproduced the rows with its own code and seeds (gump 13.632 ± 0.014; fair +0.653 ± 0.020; mean density
+0.535 ± 0.026; core copy −0.445 ± 0.020; layer copy −0.183 ± 0.018; zero of the scan 0.199 ± 0.007; d = 2 mean
density +0.303, 2.0 σ above mine). Its defects are in the reading. The earlier sentences stay above as written; these
corrections replace them where they conflict.

1. **The mechanism's ordering fails [corrected].** Part 1's "The variable that orders the chains", "the four annealed
   chains are in the same order by this low-face density as by their lives", the LOW10 paragraph's "Same density, no
   fading: +0.463" read as a mechanism, and "What this says about what kills a face": withdrawn as a mechanism. The
   referee's chain that copies from the whole layer has the replaced layer-1 core at 0.386 under a low face (my own
   `LAYER` diagnostic on its run: 0.3858; gump 0.3838), is *less* clustered than gump (1.65 against 1.81 of binomial)
   and denser in layer 2, and lives 0.18 shorter; the p = 0.2 chain is thinner under a low face than gump (0.354 after
   the darts, the referee's run) and lives as long, and the p = 0.1 chain (0.311) outlives the core copy (0.348). **What survives [measured]:**
   the numbers of the support table; the conversion of supply into births is the same in every chain measured; the
   coins act along the whole descent and hardly at the last cell (P₁ within ± 0.02 of 0.77 at ε = 1/4, with a drift
   along the scan of at most 0.03 of Δ ln τ, as the referee notes); at full replacement, clustering at fixed density
   shortens the life (third task, measured cleanly there). **What does not:** that the low-face density, or the
   clustering, of the replaced core orders or sets the life. What sets it is open.
2. **"Layer 1 leads the face by one to two generations" [corrected].** The cross-correlation of the whole layer 1 with
   the face peaks at lag 0 (+0.375 against +0.296 at lags 1 and 2); nothing leads in the sense of a displaced peak.
   The asymmetry is directional and points from the layer to the face (the referee's Granger comparison: the layer's
   past adds +0.038 to the explained share of the face's variance, the face's past adds +0.007 to the layer's). The
   loop sentence ("when the face thins, layer 1's cells lose their face neighbours and thin too, which removes the
   supply") put the strong arrow where the data have the weak one. The replaced core carries little of either.
3. **"Density is a fifth to a quarter of the effect" [corrected: it depends on what is matched].** Along fair → coins
   at gump's mean density it is 0.146 ± 0.020 (a fifth). But coins at gump's mean density make a denser support than
   gump's: the rule-made density of the replaced cells is +0.010 above gump's at depths 1–4 (the referee). Matched on
   the realized density of the replaced core (the LOW10 chain: 0.428 after the darts against gump's 0.430), the share
   is 0.678 − 0.463 = 0.215 ± 0.019, about a third. Both are attributions along one path, not properties of the chain.
4. **p\* is a coin bias, not a support density [corrected].** At ε = 1/4 the p = 0.2 chain's replaced core reads 0.40
   after the darts (0.456 before; the referee). "For its face, gump's own layers are worth independent coins of
   density 0.19, less than half their own density" is withdrawn; what stands is "coins of bias 0.19, refreshing 22% of
   the replaced cells per generation, give gump's life". Every density quoted for a noisy chain in part 1 is read
   **after the darts** (`step(); noise; observe()`): the state the next step reads, a mix of the generation's fresh
   coins and rule-made cells. At full replacement (second and third tasks) every replaced cell is a coin when it is
   read, so there **the replaced cells' density equals the coin bias** and p\* is a density of those cells; the
   cells not replaced are rule-made. "An independent bath of gump's density overestimates the life by 0.53" was darts
   at ε = 1/4, not a bath; the bath is the third task's skin row A, d = 1 (below).
5. **"Random placement is not what helps; independence from the face is" [corrected].** The copy rows add a
   correlation gump does not have (a voter move among the replaced cells; within-population variance 2.10 against
   1.80 in the referee's core copy), so they do not isolate independence from the face; and the conditioned coins,
   which depend on the face, keep +0.45 to +0.50. What coins remove is not a cell's correlation with the face above it
   alone; the layer's memory and the correlations among replaced and unreplaced cells are open candidates.
6. **Seeds shared the coin stream [corrected in the program].** The second stream started at seed · G + 99991, G its
   own increment, so seed s + 1's coins were seed s's shifted by one word (`research/blast/ref-density/seedstream.py`).
   Part 1's "two seeds that agree to 0.001" (5111, 5112; 5121, 5122) were not independent replications in their
   coins (their darts were; the referee's independent code agrees with the values), and all biased and
   full-replacement rows up to commit 315062c draw their coins from offsets of one sequence (each row is a valid
   sample of its chain; rows are not independent of one another in their coins). From commit 7c64966 the second
   stream starts from a hash of the seed (`NZD_OLDSTREAM=1` restores the old start for the earlier rows);
   `validate.py` checks it: the coin fields of seeds 5000 and 5001 at p = 0.385 agree on 0.528 of cells (independent:
   0.526), 0.619 with the old start (the negative control). In the third task the 84-cell chunks are pooled only from
   the fixed binary, and the one repeated row (skin A, d = 4, 63 cells) uses it.

### 2. The skin depth at full replacement [measured]

Every cell at depth ≥ d under the watched face is a fresh coin every generation (full replacement), at the mean density
gump has *at that depth among the replaced cells* (overall, not conditioned on the face; `cells.py` on the layer runs
above, e.g. at 63 cells column A uses `1:0.4301,2:0.4094,3:0.4149,4:0.4166,5:0.4157,6:0.4157,7:0.4165,8:0.4150`). In
these rows the replaced cells' density, when the face's next step reads them, is exactly the coin bias. Column A: depth
≥ d under the watched face and ≥ 3 under the other seven (the face keeps d real layers in its middle, its rims keep
more). Column B: depth ≥ d under every face (every face keeps exactly d real layers; B with d = 3 is A with d = 3). Rows:
`DO=<3|d> NZD_FULL=1 sh research/blast/density/row.sh <tag> R <seed> GENS 0 d <biases>` (seeds in the table's files,
`data/rows/{R9_,}skin{A,B}_d*_s*.txt`; 10⁶ generations at 45 cells, 4 × 10⁶ at 63, one 8 × 10⁶ repeat on the fixed
stream); table: `python3 research/blast/density/skin.py`. "Dips" = descents from ≥ H to < H per hull-generation (H = 16
at 63 cells, 11 at 45: a quarter of the face); "deadliness" = the share of them that end in death before the face is
back at H; P₁ = the share of descents to ≤ 1 cell that die (gump: 0.7726 ± 0.0013 at 45 cells, 0.770 ± 0.004 at 63).

| rows | Δ ln τ | Δ ln dips | Δ ln deadliness | P₁ |
|---|---:|---:|---:|---:|
| 45 cells, A, d = 1 (the bath of gump's own densities) | +0.564 ± 0.009 | −0.293 | −0.268 | 0.768 ± 0.003 |
| 45, A, d = 2 | +0.342 ± 0.008 | −0.139 | −0.199 | 0.767 ± 0.003 |
| 45, A = B, d = 3 | +0.169 ± 0.008 | −0.055 | −0.111 | 0.764 ± 0.003 |
| **45, A, d = 4** | **+0.004 ± 0.007** | +0.005 | −0.004 | 0.771 ± 0.002 |
| 45, B, d = 1 (every face on coins below itself) | +2.338 ± 0.020 | −2.441 | +0.108 | **0.915 ± 0.005** |
| 45, B, d = 2 | +0.884 ± 0.010 | −0.467 | −0.413 | 0.767 ± 0.004 |
| **45, B, d = 4** | **−0.006 ± 0.007** | +0.002 | +0.007 | 0.771 ± 0.002 |
| 63 cells, A, d = 1 (the bath) | +1.186 ± 0.037 | −0.662 | −0.512 | 0.784 ± 0.013 |
| 63, A, d = 2 | +0.694 ± 0.029 | −0.283 | −0.400 | 0.759 ± 0.011 |
| 63, A = B, d = 3 | +0.295 ± 0.023 | −0.088 | −0.196 | 0.758 ± 0.009 |
| **63, A, d = 4** (two seeds, pooled; +0.007 ± 0.020 and +0.020 ± 0.015) | **+0.016 ± 0.012** | +0.002, +0.001 | +0.003, −0.010 | 0.765, 0.776 ± 0.007 |
| 63, A, d = 5 | +0.027 ± 0.021 | −0.005 | −0.011 | 0.766 ± 0.008 |
| 63, A, d = 6 | +0.010 ± 0.020 | −0.005 | +0.006 | 0.764 ± 0.008 |
| 63, B, d = 1 | +3.530 ± 0.118 | −3.315 | −0.204 | **0.878 ± 0.036** |
| 63, B, d = 2 | +1.439 ± 0.041 | −0.700 | −0.728 | 0.763 ± 0.015 |
| **63, B, d = 4** | **+0.016 ± 0.020** | −0.001 | −0.004 | 0.763 ± 0.008 |
| 63, B, d = 5 | −0.012 ± 0.020 | −0.001 | +0.024 | 0.785 ± 0.007 |

**A face with four real layers under it (the face and depths 1–3) dies at gump's rate and in gump's way**, at both
sizes and in both columns: from d = 4 on, every Δ ln τ is within 1.4 σ of zero (the eight rows with d ≥ 4: weighted mean
+0.003 ± 0.004; the six at 63 cells +0.013 ± 0.008), and so are the frequency of dips (|Δ ln| ≤ 0.005), their
deadliness (≤ 0.024) and the death from one cell (0.763–0.785 against 0.770). With three real layers the face lives
longer by 0.17 (45 cells) and 0.30 (63 cells), the excess growing with the face, and most of it is in the deadliness of
a dip (−0.11, −0.20) rather than in how often it dips (−0.06, −0.09). With two the excess is 0.34–1.44; with one (the
face alone over coins at gump's own densities, column B) +2.3 and +3.5, and only that row changes the death from one
cell (0.88–0.92). **So the face law, rate and excursions both, is a property of a skin four layers thick [measured at
45 and 63 cells; that it holds at larger faces is conjectured]**: below depth 3 gump's support can be replaced by
independent fresh coins of its own mean density, layer by layer, without any measurable change (to ± 0.02 in ln τ, ±
0.01 in the excursion statistics); above it, it cannot. This is also the corrected form of part 1's "an independent bath
of gump's density overestimates the life": a bath from depth 1 (A, d = 1) adds +0.56 at 45 cells and +1.19 at 63.

Reading [conjectured]: the coins differ from gump's layers in memory and in correlations (with the face and among
themselves), and those differences matter only within three layers of the face; gump's layers at depth ≥ 4 carry no
information about the face that the face can use (part 1: their density does not move with the face, ± 0.005, and
their correlation with it is < 0.01). Not checked: d = 4 at ε < 1 (darts); whether it is "depth ≥ 4" or a smooth decay
that drops below the errors there (d = 3 → 4 removes 0.17 and 0.30; d = 4 → 5 nothing measurable).
