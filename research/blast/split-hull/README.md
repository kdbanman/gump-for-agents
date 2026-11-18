# research/blast/split-hull: a rare-event sampler for the faces of gump's octahedral hull

Agent `split-hull`, blast of 2026-11-18. Aim: ln τ_face of the 135-cell rimmed face (R = 17), which brute force
cannot reach (one death per 6 × 10¹¹ hull-generations). Files: `sh.c` (stepper and sampler), `validate.py` (stepper
against `reference/oracle.py`), `chain.sh` and `variant.sh` (replications), `ana.py` (pooling), `levels.py` (dip rates
by plain running, the lines, the forecasts), `fill.py`, `curate.py`, `PREDICTIONS.md` (forecasts), `paths/` (dying paths). Bulk output: `research/scratch/blast/split-hull/runs/`.

## Short answer (04:34 UTC; point 4 rewritten 06:15 UTC)

1. **The sampler does not reach the 135-cell face, and I can say why [measured].** Forward-flux sampling on the
   face's population, clones separated by deep flips. Weak, unbiased separations (one flip three layers down) leave
   it starved: a dip from 0.9 P̄ to an empty face lasts about 10 generations and a deep flip needs several to
   change the face, so most of the selection acts on clones that are still identical. Strong separations (a sixth
   of the fifth layer flipped, two generations back: the setting I froze) bias it: **estimate − anchor = −0.027 ±
   0.018 at R = 9 and −0.173 ± 0.044 at R = 11**, and at R = 13 it is starved as well (scatter 0.57 per
   replication, 6 effective ancestors). The bias grows as the face thins: +0.1% per stage near 0.8 P̄, +8% and more
   per stage below seven cells. No number for R = 17 comes from it.
2. **Plain running gives a decomposition that forecasts R = 17, 19 and 21 [tables measured, law conjectured].** I
   measured the dip rates ν(p) (first passages of P ≤ p·P̄ per hull-generation, coming from above P̄; no cloning)
   at R = 7 … 21, 2 × 10⁷ to 9.5 × 10⁸ hull-generations per size. With the anchors' lifetimes, −ln q(p) = ln τ + ln ν(p)
   is, for p ≤ 0.6, **a straight line in the area with no rim term** over 45, 63, 84, 108 cells: at p = 0.6 it is
   5.611, 8.668, 12.239, 16.334, i.e. −2.049 + 0.17014·A with weighted χ² 1.1 on 2 (p = 0.5: 1.5; 0.4 and 0.3: below 1),
   while for p ≥ 0.7 it is not a line (χ² 11, 35, 46 at 0.7, 0.8, 0.85). So the rim term of the hull's lifetime (the
   −0.34·k of ln τ = 1.144 + 0.2308·A − 0.342·k) is a property of **how often the face dips to 0.6 P̄**, and what
   happens below has no term growing with the edge. ν(0.6 P̄) is cheap at any size. If the line continues:

   | face | forecast of ln τ_face | "second difference repeats" | "wrapped price takes over" |
   |---|---|---|---|
   | R = 17, 135 cells | **29.223 ± 0.014** | 29.230 | 29.163 |
   | R = 19, 165 cells | **35.779 ± 0.020** | 35.812 | 35.613 |
   | R = 21, 198 cells | **43.007 ± 0.027** | 43.085 | 42.689 |

   The same from other deep levels: 29.220 ± 0.019 (p = 0.5); from levels at fixed density 0.28 instead of a
   fraction of P̄: 29.218 ± 0.012, 35.781 ± 0.021, 43.02 ± 0.05. The errors of the three sizes are not independent
   (one line). In second differences of ln τ: 0.704 ± 0.013, 0.664 ± 0.014, 0.672 ± 0.019 centred on R = 15, 17, 19,
   mean 0.683 ± 0.009 (0.694, 0.690 on file before them; 0.626 would be the wrapped price). These are forecasts resting on a four-point straight
   line, not measurements of τ; one size below the fit the line fails (30 cells: −ln q(0.6) is 0.22 above it, and
   the lifetime's own quadratic misses there by 0.13).
3. **Brute force agrees with the anchors [measured]:** R = 9: ln(8E/D) = 9.8201 ± 0.0055 (32,644 first deaths);
   R = 11: 13.627 ± 0.036 (790). The dip rates agree with `research/dying`'s independent code at 63 cells
   (ln ν = −2.311, −4.164, −6.513, −9.359, −12.48 at P ≤ 28, 21, 15, 9, 3 against its −2.31, −4.16, −6.51, −9.37, −12.43).
   R = 7 under this protocol: 6.8345 ± 0.0024 (180,727 first deaths), not the 6.804 on file (another protocol; a
   hull of that size lives 115 generations, less than the ageing-in).

4. **Dice under the hull: the 135-cell face on a surrogate chain [measured; 05:00 to 06:15 UTC].** Split-slab's subset
   simulation over honest coins, on a hull dice chain (true rule on six layers beneath the watched face inside the
   real hull boundary, fair coins on the two layers below). Chain − gump: +0.001 ± 0.019 (R = 9), −0.044 ± 0.039
   (R = 11; by brute force +0.006 ± 0.030), **+0.051 ± 0.026 (R = 13, blind, 234 replications), +0.059 ± 0.046 (R = 15,
   blind, 460)**. **R = 17: 29.397 ± 0.037 on the chain (385 replications); less the pooled blind offset
   29.344 ± 0.043. R = 19: 36.090 ± 0.070 on the chain (65 replications); less the offset 36.04 ± 0.07.** The
   replications' rates are heavy-tailed and the pooled value comes down as they accumulate (29.50 at 50, 29.45 at
   200, 29.40 at 385; the first large replication arrived near 220). **Value I defend for gump at 135 cells:
   29.34, +0.06, −0.10**: 29.22 and 29.230 are inside it, 29.163 at its lower edge. Section "Dice under the hull",
   subsection "The last run".

## Dice under the hull (second attempt at the measurement itself, 04:45 to 05:35 UTC)

After agent `split-slab` showed that subset simulation over honest dice works on wrapped faces
(`research/blast/split-slab/README.md`, section 6), the same on the hull. Forecast frozen first: `PREDICTIONS.md`
block 4 (commit 1356c1c). Files: `hullgeom.py` (the graph), `hd.c` (split-slab's `ss.c` with one change: rule
cells and dice cells are counted from the graph, NR and ND, instead of 6 and 2 layers of A cells), `dice.sh`.

**The hull dice chain, exactly.** Cells: the hull's cells (|x| + |y| + |z| ≤ R, one odd coordinate) at depth
r = (R − (x + y + z))/2 ≤ 7 beneath the watched face x + y + z = R. Depth 0 to 5: gump's rule, neighbours outside the
hull dead (so the watched face's three rim rows are the real ones, and the three neighbouring faces are real for
their first six rows from the shared edge, with their own layers beneath as far as depth 5). Depth 6 and 7: every
cell replaced after every generation by an independent fair coin. Deeper cells do not exist. No rule cell has a
neighbour deeper than 7 (T1), so every influence on the watched face from below passes the coins. Sizes (A, rule
cells, dice cells): 45, 312, 108 (R = 9); 63, 438, 162; 84, 582, 222; 108, 744, 288; 135, 924, 360 (R = 17).
Convention: one watched face, τ_face = (generations with the watched face alive) / (its deaths); other faces are
not whole in this chain and their deaths are not defined, which matters only where hulls die fast (R = 9: a
gump hull is retired at the first death of any of 8 faces every 2,300 generations).

**The sampler** is split-slab's, unchanged (its README has the exact statement; `hd.c` mode `sub`): a chain is an
initial state (a snapshot of 512 stationary lanes of the dice chain, 64 generations apart) plus 56 generations of
coins; score = minimum population of the watched face over generations 33 to 56 (chains whose face is dead at
generation 32 do not count); P(score = 0) = 24/τ; levels LAM1, LAM1 − 3, …, 0; at each level the chains at or below
it refill an ensemble of 4,096 and are moved by NSWEEP Metropolis sweeps of KFLIP coin flips (even sweeps uniform
in space-time, odd sweeps in the 12 generations before the chain's minimum, accepted iff the score stays at or
below the level and the reverse move is proposable). Frozen parameters (block 4): LAM1 = round(P̄ − 2.5 σ_P) = 10,
18, 28, 38, 51 for R = 9 … 17; NSWEEP = round(A/6) = 8, 10, 14, 18, 22; KFLIP 5; TPRE 32, TWIN 24, WBACK 12.
`sh research/blast/split-hull/dice.sh R SEED NREP`. Error: scatter of independent replications' rates.

<!-- DICE -->
**Results (06:14 UTC)** (`python3 research/blast/split-hull/dice_ana.py`, `dice_fill.py`; brute force of the chain:
`DICE=1 shd R SEED 0 GENS`, the base run of `sh.c` with the coins switched on):

| R | cells | what | replications | ln τ, dice chain | gump anchor | chain − gump |
|---|---:|---|---:|---|---|---|
| 9 | 45 | brute force of the chain | 3,248 deaths | 9.837 ± 0.018 | 9.819 | +0.018 ± 0.018 |
| 9 | 45 | sampler (tuning size) | 32 | 9.820 ± 0.019 | 9.819 | +0.001 ± 0.019 |
| 11 | 63 | brute force of the chain | 275 deaths | 13.70 ± 0.06 | 13.633 | +0.07 ± 0.06 |
| 11 | 63 | sampler (tuning size) | 32 | 13.589 ± 0.039 | 13.633 | -0.044 ± 0.039 |
| 13 | 84 | sampler, **blind** | 234 | 18.192 ± 0.025 | 18.141 | **+0.051 ± 0.026** (2.0 errors) |
| 15 | 108 | sampler, **blind** | 460 | 23.399 ± 0.045 | 23.3392 | **+0.059 ± 0.046** (1.3 errors) |
| 17 | 135 | sampler, **the new size** | 385 | **29.397 ± 0.037** | none | forecast 29.223 ± 0.014 |

Both blind calibrations pass the rule set beforehand (within two errors); nothing was tuned after block 4. The two
blind sizes together sit +0.053 ± 0.022 above gump (all four sizes: +0.015 ± 0.014). Scatter of one replication's
rate, as a fraction of the mean: 0.11, 0.22, 0.39, 0.95, 0.73, 0.56 at R = 9, 11, 13, 15, 17, 19; the largest replication carries 4%, 4%, 1%, 3%, 3%, 6% of the sum; zero-rate replications: 0.

**R = 17 (135 cells) [measured on the dice chain; a surrogate for gump]:** ln τ = 29.397 ± 0.037 (385 replications; jackknife 0.037; mean of the replications' logarithms 29.516 ± 0.022).
Minus the offset of the blind sizes: **29.344 ± 0.043** for gump; with no offset: 29.397 ± 0.037.
Against the forecast 29.223 ± 0.014: +0.121 ± 0.045 (offset removed), +0.174 ± 0.040 (raw).
If instead the offset drifts linearly with the area (weighted line through the four sizes: +0.00111 ± 0.00063 per cell,
+0.094 ± 0.047 at 135 cells): **29.303 ± 0.060** for gump. In errors of each reading, the candidates sit at:
| reading of the offset | value for gump | 29.230 (second difference repeats) | 29.223 (my forecast) | 29.163 (wrapped price) |
|---|---|---|---|---|
| none (the chain is gump) | 29.397 ± 0.037 | +4.5 | +4.4 | +6.3 |
| constant, from the blind sizes | 29.344 ± 0.043 | +2.6 | +2.7 | +4.2 |
| linear in the area | 29.303 ± 0.060 | +1.2 | +1.3 | +2.3 |
<!-- /DICE -->

**After the first report (05:25 to 05:45 UTC): more replications, variations of the chain, and a warning about the errors.**
- **The offset [measured].** R = 13 with 234 replications: chain − gump = **+0.051 ± 0.026**. R = 15 with 184:
  **+0.008 ± 0.086**; its error GREW from 0.074 (48 replications) because one replication in 130 of the second seed
  came out with 13 times the typical rate (ln τ_k = 20.74 against a median 23.60) and another large one turned up in
  six further replications. The replications' rates are heavy-tailed at 108 cells (skewness of ln τ_k −1.8), so the
  mean rate is under-estimated until a large replication arrives, and the quoted error of any batch without one is
  too small. Pooled offset of the two sizes: +0.047 ± 0.025; with the tuning sizes +0.001 ± 0.019 (R = 9) and
  −0.044 ± 0.039 (R = 11) there is no clear drift: about +0.05 at 84 cells, nothing measurable at 45, 63 or 108.
- **Variations of the chain at R = 11, by brute force [measured]** (`DICE=1 [DDEP=8 | DPM=58 | DSIDE=3] shd2 11 SEED 0 450000`;
  gump 13.633): the chain as defined **13.639 ± 0.030** (1,097 deaths; with the earlier run 13.652 ± 0.027); coins two
  layers deeper (depth 8 and 9) **13.632 ± 0.030**: no change; coins at the living density of those layers (0.453,
  measured in gump: `DENS=1 shd2 11 601 0 1500`) instead of 0.5: **13.703 ± 0.031**, +0.064 ± 0.044 from the chain and
  if anything away from gump. So at 63 cells the chain sits on gump (+0.006 ± 0.030) and neither depth nor density
  explains an offset. The third variation (coins only where at least three layers beneath every other face, the
  rest of the hull by rule) gave 12.461 ± 0.017 and is **not a valid test as run**: the neighbouring faces are then
  whole and die, and my chain code does not retire the hull when they do.
- **R = 17, three ways [chain measured; readings for gump are inference]** (29.445 ± 0.041 on the chain, 125 replications):

  | reading | value for gump | against 29.230 | against 29.22 ± 0.02 (dip-rate forecast) | against 29.163 |
  |---|---|---|---|---|
  | the chain itself | 29.445 ± 0.041 | +5.2 errors | +5.1 | +6.9 |
  | less the pooled blind offset | 29.398 ± 0.048 | +3.5 | +3.5 | +4.9 |
  | less an offset linear in the area | 29.364 ± 0.070 | +1.9 | +2.0 | +2.9 |

  **Which I believe: the second, with a wider and lopsided error than quoted, roughly 29.40 +0.06/−0.15.** The
  data do not ask for a linear offset (no drift from 45 to 108 cells). But the quoted ± 0.04 is the scatter of 125
  replications among which no large one has appeared (largest share of the sum 3%); at 108 cells such a
  replication appeared once in about 100 and moved the estimate down by 0.07. So: 29.163 is 4.9 quoted errors
  below the reading and still about 2 below if the downward error is tripled; 29.230 and the forecast 29.22 are
  3.5 quoted errors below it, about 1.5 once the tail is allowed for. At face value the hull's second difference
  at k = 8 would be 0.86 ± 0.05, not 0.69. **The reading leans that way and I would not claim it**: my odds that
  gump's 135-cell value is above 29.30 are about 3 to 2; that it is below 29.20, about one in ten. What would
  settle it: 500 replications at R = 17 and 500 at R = 15 (about 3 core-hours), watching the largest replication's
  share of the sum.
- **How the watched face dies on the chain [measured, surrogate]** (`sh dice_paths.sh R 91 N; python3 dice_paths.py`;
  6, 6, 5 replications at R = 13, 15, 17; means over replications):

  | R | cells | fall ≥ A/2 in one generation | fall ≥ 0.4 A | largest fall | fade: last P > 0.9 P̄ to empty | last P > 0.5 P̄ to empty | last live cells on the rim line (share of cells) | inside (share of cells) |
  |---|---:|---|---|---|---|---|---|---|
  | 13 | 84 | 0.001 ± 0.001 | 0.034 ± 0.008 | 0.25 A from 0.55 A | 10.9 ± 0.3 | 8.4 ± 0.4 | 0.54 ± 0.02 (0.46) | 0.07 ± 0.01 (0.11) |
  | 15 | 108 | 0.013 ± 0.005 | 0.087 ± 0.031 | 0.28 A from 0.57 A | 11.0 ± 0.4 | 8.9 ± 0.3 | 0.49 ± 0.04 (0.42) | 0.11 ± 0.02 (0.17) |
  | 17 | 135 | 0.003 ± 0.002 | 0.095 ± 0.029 | 0.25 A from 0.52 A | 11.4 ± 0.2 | 9.2 ± 0.2 | 0.48 ± 0.03 (0.38) | 0.14 ± 0.01 (0.22) |

  The half-face bust does not rise with size (0.1%, 1.3%, 0.3%); falls of 0.4 A go from 3% to 9%. The fade
  lengthens by half a generation from 84 to 135 cells: the face still empties everywhere at once. The last one
  or two cells sit on the rim line 1.2 to 1.3 times as often as its share of the face, and inside 0.65 times.


### The last run (05:45 to 06:15 UTC): three cores of replications at R = 17 and 15, one at R = 19

Fresh seeds, each run with its own 512 stationary lanes (10 to 12 replications per run; `sh dice.sh R SEED N` with
seeds 1001.., 2001.. at R = 17, 3001.. at R = 15, 4001.. at R = 19). `python3 dice_run.py`, `dice_ana.py`:

| R | cells | replications | ln τ, dice chain | scatter of one replication | largest replication's share | chain − gump |
|---|---:|---:|---|---:|---:|---|
| 13 | 84 | 234 | 18.192 ± 0.025 | 0.39 | 0.015 | +0.051 ± 0.026 |
| 15 | 108 | 460 | 23.399 ± 0.045 | 0.95 | 0.031 | +0.059 ± 0.046 |
| 17 | 135 | 385 | **29.397 ± 0.037** | 0.73 | 0.026 | less the pooled offset +0.053 ± 0.022: **29.344 ± 0.043** |
| 19 | 165 | 65 | **36.090 ± 0.070** | 0.56 | 0.062 | less the pooled offset: 36.037 ± 0.073 |

Running pooled values (every 50 replications, in the order the runs were made):

```
R = 15: 460 replications in 26 runs (each run has its own stationary lanes)
    n    -ln<rate>   +-      largest share   lognormal estimate
    50   23.424   0.072     0.058          23.429
   100   23.333   0.132     0.134          23.405
   150   23.361   0.093     0.092          23.414
   200   23.367   0.080     0.069          23.423
   250   23.367   0.069     0.056          23.421
   300   23.393   0.060     0.048          23.442
   350   23.379   0.052     0.040          23.422
   400   23.379   0.050     0.035          23.426
   450   23.400   0.045     0.032          23.443
   460   23.399   0.045     0.031          23.441
  all: scatter of one replication 0.95 of the mean; sd of ln tau_k 0.440, skewness -1.82; the 3 largest replications carry 0.068 of the sum; smallest and median ln tau_k 20.74, 23.59
  per run (>= 5 replications): 26 runs, their -ln<rate> from 22.58 to 23.71, sd 0.253
R = 17: 385 replications in 30 runs (each run has its own stationary lanes)
    n    -ln<rate>   +-      largest share   lognormal estimate
    50   29.498   0.079     0.069          29.509
   100   29.457   0.048     0.033          29.464
   150   29.440   0.044     0.032          29.449
   200   29.453   0.043     0.029          29.467
   250   29.412   0.051     0.041          29.442
   300   29.410   0.045     0.034          29.438
   350   29.405   0.040     0.029          29.429
   385   29.397   0.037     0.026          29.420
  all: scatter of one replication 0.73 of the mean; sd of ln tau_k 0.440, skewness -1.08; the 3 largest replications carry 0.053 of the sum; smallest and median ln tau_k 27.09, 29.56
  per run (>= 5 replications): 30 runs, their -ln<rate> from 28.82 to 29.89, sd 0.203
R = 19: 65 replications in 13 runs (each run has its own stationary lanes)
    n    -ln<rate>   +-      largest share   lognormal estimate
    50   36.070   0.082     0.080          36.073
    65   36.090   0.070     0.062          36.090
  all: scatter of one replication 0.56 of the mean; sd of ln tau_k 0.491, skewness +0.08; the 3 largest replications carry 0.129 of the sum; smallest and median ln tau_k 34.69, 36.20
  per run (>= 5 replications): 13 runs, their -ln<rate> from 35.77 to 36.30, sd 0.146
```

**What the last run shows.**
- **The heavy tail has been met at 135 cells.** Through 200 replications the pooled value sat at 29.44 to 29.50 with the
  largest replication carrying 3% of the rate; near replication 220 one came out 2.5 below the median in ln τ and the
  pooled value fell to 29.41, then drifted to 29.40 by replication 385. At 108 cells the same happened near replication 80
  (23.42 → 23.33) and the value then settled at 23.37 to 23.39. So at both sizes the pooled value starts high and
  comes down by 0.05 to 0.09 when the first large replication arrives, and the errors quoted before that were too
  small. The estimator's finite-sample bias is upward in ln τ and grows with size (the chains move only about half a
  percent of their coins per level, so an ensemble is a few families).
- **The offset is the same at the two blind sizes**, about +0.05 (table). Part of it is that upward bias, part the
  chain itself (+0.006 ± 0.030 at 63 cells by brute force; split-slab's slab chain +0.02).
- **The value I defend for gump's 135-cell face: 29.34, +0.06, −0.10.** It is the chain less the pooled offset; the
  downward error is wider because the offset at 135 cells cannot be smaller than at 84 to 108 if it is a sampling
  bias, and may be larger. **29.22 (the dip-rate forecast) and 29.230 are inside it, at about 1.2 of the downward
  error; 29.163 is at about 1.8.** The chain does not establish that the second difference grows: 0.81 ± 0.05 at face
  value, 0.69 if the offset at 135 cells is 0.17 instead of 0.05.
- **165 cells:** the chain less the same offset reads 36.04 ± 0.07 from 65 replications, with no large
  replication met yet (so, by the pattern above, probably 0.05 to 0.1 too high): against 35.78 (dip-rate route),
  35.81 (second difference repeats), 35.61 (wrapped price). Like the 135-cell reading before its tail was met, it sits
  about 0.25 above the dip-rate route; the increment from 135 to 165 cells, 6.69 ± 0.08, is close to the ordinary one (6.56 by
  the dip-rate route, 6.58 if the second difference repeats, 6.45 at the wrapped price).
- **Where a real discrepancy would have to sit.** If the dip-rate line and the chain are both right, −ln q(0.6) bends up
  by about 0.13 between 108 and 135 cells. Gump's own plain-running tables say it is not between 0.6 and 0.5 P̄
  (passage cost against the trend of 45 to 108 cells: 0.000 ± 0.017 at 135 cells, −0.010 ± 0.038 at 165) and show
  +0.09 ± 0.07 between 0.5 and 0.4 P̄, the deepest plain running reaches at that size. The chain puts its whole
  excess over the trend of its own smaller faces at the very end (tables below: +0.11 to +0.16 at every level from
  0.45 P̄ down to 0.1 P̄ at 135 cells, +0.26 to +0.35 at 165: all of it already in the passage from the last seven or
  eight cells to none). That is the stretch plain running
  cannot check at 135 cells, and it is also where the sampler's replications scatter most; so the excess is
  either a real dearer end game on large faces or the unmet part of the tail. I lean to the second.

Level by level on the chain (`python3 dice_levels.py`) and gump's own deep passages (`python3 bend.py`):

```
c(p) = ln P(S <= p P-bar) - ln P(S = 0) on the dice chain (replications in brackets)
   R  cells    p = 0.6           p = 0.45          p = 0.4           p = 0.3           p = 0.2           p = 0.1       
   9    45     nan +- nan   4.355 +- 0.016   3.885 +- 0.015   2.922 +- 0.013   1.890 +- 0.010   0.858 +- 0.005   [32]
  11    63     nan +- nan   6.688 +- 0.036   5.970 +- 0.035   4.471 +- 0.031   2.906 +- 0.024   1.340 +- 0.012   [32]
  13    84  12.297 +- 0.025   9.557 +- 0.025   8.536 +- 0.024   6.424 +- 0.023   4.213 +- 0.019   1.955 +- 0.011   [234]
  15   108  16.389 +- 0.045  12.750 +- 0.045  11.413 +- 0.044   8.607 +- 0.042   5.673 +- 0.036   2.663 +- 0.020   [460]
  17   135  21.097 +- 0.037  16.457 +- 0.037  14.752 +- 0.036  11.171 +- 0.035   7.414 +- 0.029   3.531 +- 0.017   [385]
  19   165  26.335 +- 0.070  20.600 +- 0.068  18.492 +- 0.066  14.049 +- 0.056   9.368 +- 0.040   4.505 +- 0.024   [65]
weighted straight line in the area through R = 9..15 (R = 13, 15 where a size has no level that high), and the larger faces against it:
  p = 0.6: slope 0.1705 +- 0.0021 per cell (two sizes: no test);  R = 17: 21.097 against 20.994: excess +0.103 +- 0.106;  R = 19: 26.335 against 26.110: excess +0.226 +- 0.177
  p = 0.45: slope 0.1333 +- 0.0006 per cell, chi2 3.2 on 2;  R = 17: 16.457 against 16.343: excess +0.114 +- 0.058;  R = 19: 20.600 against 20.341: excess +0.259 +- 0.092
  p = 0.4: slope 0.1193 +- 0.0006 per cell, chi2 2.9 on 2;  R = 17: 14.752 against 14.618: excess +0.135 +- 0.057;  R = 19: 18.492 against 18.197: excess +0.295 +- 0.089
  p = 0.3: slope 0.0899 +- 0.0005 per cell, chi2 4.9 on 2;  R = 17: 11.171 against 11.007: excess +0.164 +- 0.054;  R = 19: 14.049 against 13.704: excess +0.346 +- 0.079
  p = 0.2: slope 0.0597 +- 0.0004 per cell, chi2 5.5 on 2;  R = 17: 7.414 against 7.257: excess +0.157 +- 0.045;  R = 19: 9.368 against 9.048: excess +0.320 +- 0.061
  p = 0.1: slope 0.0283 +- 0.0002 per cell, chi2 6.3 on 2;  R = 17: 3.531 against 3.401: excess +0.130 +- 0.025;  R = 19: 4.505 against 4.250: excess +0.255 +- 0.035

end game at fixed numbers of cells: c_abs(L) = ln P(S <= L cells) - ln P(S = 0)
   R  cells    L = 3             L = 6             L = 9             L = 12            L = 18          last levels
   9    45   1.259 +- 0.007   2.693 +- 0.012   4.042 +- 0.015     nan +- nan     nan +- nan   [7, 4, 1, 0]  [32]
  11    63   1.277 +- 0.012   2.780 +- 0.024   4.290 +- 0.030   5.740 +- 0.035   8.359 +- 0.039   [9, 6, 3, 0]  [32]
  13    84   1.321 +- 0.007   2.893 +- 0.015   4.485 +- 0.020   6.048 +- 0.023   9.032 +- 0.025   [7, 4, 1, 0]  [234]
  15   108   1.305 +- 0.010   2.925 +- 0.021   4.562 +- 0.031   6.188 +- 0.037   9.352 +- 0.043   [8, 5, 2, 0]  [460]
  17   135   1.330 +- 0.008   2.994 +- 0.015   4.689 +- 0.021   6.366 +- 0.027   9.654 +- 0.033   [9, 6, 3, 0]  [385]
  19   165   1.346 +- 0.010   3.037 +- 0.019   4.772 +- 0.024   6.495 +- 0.029   9.884 +- 0.042   [8, 5, 2, 0]  [65]

passage 0.85 -> 0.6: 1.705, 2.345, 3.170, 4.114 at R = 9..15; line slope 0.03838 per cell (chi2 45.9 on 2);  R = 17: 5.241, line 5.137, excess +0.105 +- 0.010;  R = 19: 6.486, line 6.288, excess +0.198 +- 0.014;  R = 21: 7.875, line 7.555, excess +0.320 +- 0.020
passage 0.6 -> 0.5: 0.850, 1.274, 1.781, 2.349 at R = 9..15; line slope 0.02383 per cell (chi2 0.6 on 2);  R = 17: 2.994, line 2.994, excess -0.000 +- 0.017;  R = 19: 3.699, line 3.709, excess -0.010 +- 0.038;  R = 21: 4.687, line 4.496, excess +0.191 +- 0.112
passage 0.5 -> 0.4: 0.930, 1.420, 1.989, 2.645 at R = 9..15; line slope 0.02718 per cell (chi2 0.0 on 2);  R = 17: 3.463, line 3.376, excess +0.087 +- 0.073
passage 0.4 -> 0.3: 0.990, 1.513, 2.105, 2.786 at R = 9..15; line slope 0.02870 per cell (chi2 0.2 on 2)
passage 0.6 -> 0.4: 1.780, 2.694, 3.770, 4.994 at R = 9..15; line slope 0.05101 per cell (chi2 0.2 on 2);  R = 17: 6.457, line 6.370, excess +0.087 +- 0.072
```

## Deliverable 1: the stepper [measured]

`python3 research/blast/split-hull/validate.py 1200`: `sh.c`'s bit-sliced hull stepper equals `reference/oracle.py`
cell for cell at R = 11 and R = 15 (3 soups × 1,200 generations each, lanes 0, 37, 2047), together with the face
population counter, the emptiness bits of the seven other faces, the age counters, the ring of lagged states (the
state two generations ago), frozen lanes and the packed-configuration round trip. Negative control (one neighbour
swapped): fails at generation 5 (R = 11) and 3 (R = 15). Last line: `VALIDATION PASSED`. Geometry: 2,064 cells and
108 per face at R = 15, as on file.

## Deliverable 2: calibration of the sampler [measured]

Parameters were frozen at 03:52 UTC after only four tuning seeds at R = 11 (which gave 13.604 ± 0.06 and looked
fine): M = 300,000 trials a stage, LAG = 2, one flip per 6 sites of S, levels 3 cells apart, H = 0.5, stores of
100,000. Twelve fresh replications then showed the bias. `sh chain.sh R R001 N`, `python3 ana.py`:

| R | cells | replications | pooled ln τ | anchor | estimate − anchor | scatter of one replication | effective ancestors |
|---|---:|---:|---|---|---|---:|---:|
| 9 | 45 | 12 | 9.792 ± 0.018 | 9.819 | −0.027 ± 0.018 | 0.064 | 320 |
| 11 | 63 | 12 | 13.461 ± 0.044 | 13.633 | **−0.173 ± 0.044** | 0.153 | 33 |
| 13 | 84 | 4 | 17.79 ± 0.26 | 18.141 | −0.35 ± 0.26 | 0.57 | 6 |
| 15 | 108 | 0 | not run: at 0.57 scatter and a bias already shown, it would have cost ten minutes for nothing | 23.339 | | | |

"Effective ancestors": (Σn)²/Σn² over the first-level crossings the stored deaths descend from, median over
replications. It falls by about 10 for every 4 in ln τ: at R = 17 a replication would hang on one crossing.

**Where the bias enters** (`python3 levels.py`, part 1: the sampler's ν(L) against plain running, same definition):

| R = 11, level L (P ≤ L) | 28 | 25 | 22 | 19 | 16 | 13 | 10 | 7 | 4 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| sampler − brute force, ln ν | −0.000 | +0.001 | +0.004 | +0.009 | +0.014 | +0.036 | +0.064 | +0.101 | +0.178 | +0.36 |
| in combined errors | −0.5 | +1.5 | +2.8 | +2.5 | +1.8 | +2.8 | +3.0 | +3.0 | +3.2 | +3.4 |

(At L = 1 brute force has only 106 excursions. R = 13, four replications: +0.009 at P ≤ 29, +0.025 at 23, +0.043 at 20 (6 errors), +0.17 at 11.) Flipping a sixth of
the fifth layer beneath a face makes every further loss of three cells more likely, slightly while the face is
full and by a tenth to a fifth when it is nearly empty. **What bias I can exclude:** none below 0.17 at 63 cells for the
frozen setting; the sampler is not calibrated. For the weak setting (one flip at depth three, no lag; six
replications before the freeze: 13.69 ± 0.16) a bias above 0.4 is excluded and nothing finer.

A second separation, **donor swap** (everything five layers and more beneath the watched face replaced, two
generations back, by the same cells of an independent hull from the base run; `sh variant.sh 11 11201 6 2 0 swap2 1`):
13.534 ± 0.117 at R = 11 (6 replications, scatter 0.24): −0.10 ± 0.12, neither cleared nor convicted.

## Deliverable 3: R = 17. Not measured; forecast instead

See point 2 above and `PREDICTIONS.md` block 3 (frozen 04:11 UTC, commit 3946e01, on the first tables; the longer
runs since then moved every ν within its error).
`python3 research/blast/split-hull/levels.py`, parts 2 to 4. Brute-force dip rates (threshold-free: ln ν
interpolated linearly in L at L = p·P̄; Poisson errors 0.001 to 0.06, printed by the script):

<!-- DIPTABLE -->
```
PART 2: brute-force dip rates at fixed fractions of P-bar (threshold-free), per hull-generation and per face
   R    A   P-bar   sigma_P  ln nu(0.85)  ln nu(0.8)  ln nu(0.7)  ln nu(0.6)  ln nu(0.5)  ln nu(0.4)  ln nu(0.3)
   9   45   21.597   4.564      -2.503     -2.797     -3.455     -4.208     -5.058     -5.988     -6.978
      (Poisson errors)            0.000      0.000      0.001      0.001      0.002      0.003      0.004     exposure 7.51e+07
  11   63   31.255   5.224      -2.620     -2.994     -3.881     -4.965     -6.239     -7.659     -9.172
      (Poisson errors)            0.000      0.000      0.001      0.002      0.003      0.006      0.012     exposure 8.18e+07
  13   84   42.432   5.972      -2.732     -3.215     -4.402     -5.902     -7.683     -9.672    -11.777
      (Poisson errors)            0.000      0.000      0.000      0.001      0.002      0.008      0.021     exposure 4.3e+08
  15  108   55.203   6.701      -2.891     -3.492     -5.026     -7.005     -9.354    -11.999    -14.785
      (Poisson errors)            0.000      0.000      0.001      0.002      0.006      0.021      0.097     exposure 3.89e+08
  17  135   69.488   7.433      -3.061     -3.809     -5.763     -8.302    -11.296    -14.759        nan
      (Poisson errors)            0.000      0.000      0.001      0.003      0.012      0.069        nan     exposure 7.97e+08
  19  165   85.361   8.160      -3.268     -4.176     -6.599     -9.754    -13.453        nan        nan
      (Poisson errors)            0.000      0.000      0.001      0.005      0.034        nan        nan     exposure 7.97e+08
  21  198  102.762   8.915      -3.493     -4.592     -7.546    -11.368    -16.055        nan        nan
      (Poisson errors)            0.000      0.000      0.002      0.011      0.110        nan        nan     exposure 9.51e+08

  ln tau (anchor) + ln nu(p) = -ln q(p): what is left of the lifetime once the attempt rate at p is taken out
   R    A   -ln q(0.85)  -ln q(0.8)  -ln q(0.7)  -ln q(0.6)  -ln q(0.5)  -ln q(0.4)  -ln q(0.3)
   9   45      7.316      7.022      6.364      5.611      4.761      3.831      2.841
  11   63     11.013     10.639      9.752      8.668      7.394      5.974      4.461
  13   84     15.409     14.926     13.739     12.239     10.458      8.469      6.364
  15  108     20.448     19.848     18.314     16.334     13.985     11.340      8.555
  second differences in the edge k (9,11,13 and 11,13,15); ln tau itself gives 0.694, 0.690:
    p = 0.85: 0.698  0.644     slopes per cell 45-63, 63-84, 84-108: 0.2054 0.2093 0.2100
    p = 0.8: 0.669  0.635     slopes per cell 45-63, 63-84, 84-108: 0.2010 0.2041 0.2051
    p = 0.7: 0.598  0.589     slopes per cell 45-63, 63-84, 84-108: 0.1882 0.1898 0.1906
    p = 0.6: 0.514  0.524     slopes per cell 45-63, 63-84, 84-108: 0.1698 0.1700 0.1706
    p = 0.5: 0.430  0.464     slopes per cell 45-63, 63-84, 84-108: 0.1463 0.1459 0.1470
    p = 0.4: 0.351  0.377     slopes per cell 45-63, 63-84, 84-108: 0.1191 0.1188 0.1196
    p = 0.3: 0.283  0.288     slopes per cell 45-63, 63-84, 84-108: 0.0900 0.0906 0.0913

PART 4: weighted straight-line fit of -ln q(p) and the forecasts with errors
  p = 0.85: -ln q = -2.098 + 0.20845 A  (slope error 0.00019; chi2 46.4 on 2)   R = 17: 29.104 +- 0.014;  R = 19: 35.564 +- 0.019;  R = 21: 42.669 +- 0.025
  p = 0.8: -ln q = -2.166 + 0.20354 A  (slope error 0.00019; chi2 35.1 on 2)   R = 17: 29.121 +- 0.014;  R = 19: 35.594 +- 0.019;  R = 21: 42.727 +- 0.025
  p = 0.7: -ln q = -2.184 + 0.18962 A  (slope error 0.00019; chi2 11.1 on 2)   R = 17: 29.177 +- 0.014;  R = 19: 35.702 +- 0.019;  R = 21: 42.906 +- 0.025
  p = 0.6: -ln q = -2.049 + 0.17014 A  (slope error 0.00019; chi2 1.1 on 2)   R = 17: 29.223 +- 0.014;  R = 19: 35.779 +- 0.020;  R = 21: 43.007 +- 0.027
  p = 0.5: -ln q = -1.822 + 0.14627 A  (slope error 0.00020; chi2 1.5 on 2)   R = 17: 29.220 +- 0.019;  R = 19: 35.766 +- 0.040;  R = 21: 43.194 +- 0.113
  p = 0.4: -ln q = -1.526 + 0.11903 A  (slope error 0.00028; chi2 0.4 on 2)   R = 17: 29.303 +- 0.073
  p = 0.3: -ln q = -1.223 + 0.09029 A  (slope error 0.00052; chi2 0.2 on 2)   
  second differences in k of ln nu(0.6 P-bar): -0.180+-0.013  -0.166+-0.013  -0.194+-0.013  -0.154+-0.014  -0.162+-0.019   (centred on R = 11 ... 19)

PART 5: levels at fixed density x (L = x A): weighted straight-line fit of ln tau + ln nu and forecasts
  x = 0.42: slope 0.20117, chi2 313.3 on 2, residuals +0.083 -0.005 +0.018 +0.074   R = 17: 29.032 +- 0.010;  R = 19: 35.456 +- 0.015;  R = 21: 42.521 +- 0.019
  x = 0.38: slope 0.19160, chi2 162.1 on 2, residuals +0.059 -0.004 +0.013 +0.053   R = 17: 29.099 +- 0.010;  R = 19: 35.578 +- 0.015;  R = 21: 42.719 +- 0.019
  x = 0.34: slope 0.17864, chi2 43.2 on 2, residuals +0.030 -0.003 +0.007 +0.027   R = 17: 29.168 +- 0.010;  R = 19: 35.695 +- 0.015;  R = 21: 42.887 +- 0.020
  x = 0.31: slope 0.16680, chi2 9.5 on 2, residuals +0.014 -0.002 +0.004 +0.011   R = 17: 29.206 +- 0.011;  R = 19: 35.751 +- 0.016;  R = 21: 42.955 +- 0.022
  x = 0.28: slope 0.15347, chi2 0.8 on 2, residuals +0.002 -0.000 -0.002 +0.007   R = 17: 29.218 +- 0.012;  R = 19: 35.781 +- 0.021;  R = 21: 43.023 +- 0.046
  x = 0.25: slope 0.13898, chi2 1.1 on 2, residuals -0.000 +0.001 -0.004 +0.008   R = 17: 29.217 +- 0.019;  R = 19: 35.778 +- 0.048;  R = 21: 43.003 +- 0.158
  x = 0.22: slope 0.12335, chi2 0.3 on 2, residuals -0.000 +0.001 -0.003 +0.008   R = 17: 29.212 +- 0.043;  R = 19: 35.727 +- 0.151

PART 6: the 30-cell face (R = 7), outside the fit. Brute force here: ln tau = 6.8345 +- 0.0024 (180727 first deaths; on file 6.804, another protocol), P-bar 13.682
  p = 0.85: -ln q = 4.421; the line of 45..108 cells says 4.156; difference +0.266
  p = 0.8: -ln q = 4.209; the line of 45..108 cells says 3.940; difference +0.269
  p = 0.7: -ln q = 3.754; the line of 45..108 cells says 3.504; difference +0.250
  p = 0.6: -ln q = 3.277; the line of 45..108 cells says 3.055; difference +0.222
  p = 0.5: -ln q = 2.774; the line of 45..108 cells says 2.566; difference +0.208
  p = 0.4: -ln q = 2.240; the line of 45..108 cells says 2.045; difference +0.195
  p = 0.3: -ln q = 1.677; the line of 45..108 cells says 1.485; difference +0.191
  (the lifetime's own quadratic 1.144 + 0.23083 A - 0.3418 k says 6.702 at 30 cells: it misses by +0.132)
```
<!-- /DIPTABLE -->

What the forecast rests on, and what would break it: (a) the anchors (the 108-cell one, ± 0.0099, gives most of the
forecast's error); (b) P̄ from each run's 300-generation pilot (± 0.015 cells, allowed for as ± 0.005 in ln ν; the
fixed-density levels of part 5 need no P̄ and give the same forecasts); (c) the conjecture that the line continues.
If the 135-cell face is 29.163, −ln q(0.6) must fall 0.06 below a line that four sizes follow to 0.006. The choice
of p ≤ 0.6 was made after seeing which fits are lines (`PREDICTIONS.md`, scores of block 2); the shallow levels,
which are not lines, would say 29.11 to 29.18. Checks inside the larger hulls' own data, needing no lifetime:
- ln ν(0.6) − ln ν(0.5) must be linear in the area if both lines hold: 0.850, 1.274, 1.781, 2.349, 2.994 ± 0.012,
  3.70 ± 0.03 at 45 … 165 cells; steps per cell 0.0236, 0.0241, 0.0237, 0.0239, 0.0235. It is.
- The second differences in k of ln ν(0.6 P̄) are −0.180, −0.166, −0.194, −0.154, −0.162 (± 0.013, 0.013, 0.013, 0.014,
  0.019) centred on R = 11 … 19: the three that reach beyond the anchors average −0.173 ± 0.009. With the line's
  3 × 0.17014 = 0.5104 that makes the lifetime's second difference 0.683 ± 0.009 through 198 cells (0.694, 0.690 on
  file for the first two); the wrapped price would need −0.116. The last two (0.664, 0.672 for the lifetime) are
  each about 1.5 errors below 0.691: a slow decline is neither shown nor excluded; a drop to 0.626 is excluded
  if the line holds.
- One size down it fails (part 6): the 30-cell face is 0.19 to 0.27 above every line.

## Deliverable 4: the prefactor [tables measured; the reading is conjecture]

- **ln τ + ln ν(p) is linear in A only for p ≤ 0.6, and its slope is not the wrapped price.** Slopes per cell of
  −ln q(p): 0.2085 (p = 0.85), 0.2036 (0.8), 0.1896 (0.7), 0.1702 (0.6), 0.1463 (0.5), 0.1191 (0.4), 0.0903 (0.3). The
  slope passes through the wrapped faces' 0.2087 at p ≈ 0.85, where −ln q is not a line (χ² 46 on 2): a coincidence
  of the level. There is no level at which "attempt rate removed" leaves the wrapped slope and a straight line.
- **How ν scales with A and the rim.** At fixed p, ln ν(p) is close to a quadratic in the edge k. For p = 0.6: −0.059
  per cell and +0.305·k from the three smallest sizes (second differences above). The lifetime's rim term is −0.342·k: nine tenths of it is the
  attempt rate's. Fits of −ln q(p) with a term b·k give b = −0.29 (p = 0.85), −0.26 (0.8), −0.14 (0.7), −0.03 (0.6),
  −0.07 (0.5), −0.05 (0.4): the rim acts on the passage from about 0.85 P̄ down to 0.6 P̄, and little below.
  Shallow rates fall slowly with size: ln ν(0.85) = −2.503, −2.620, −2.730, −2.891, −3.063, −3.264, −3.490 at
  45 … 198 cells. P̄ = 21.60, 31.25, 42.43, 55.20, 69.49, 85.36, 102.76 and σ_P = 4.56, 5.22, 5.97, 6.70, 7.43, 8.16, 8.92.
- **Reading [conjectured].** A rimmed face looks dearer per cell than a wrapped one because its dips to about
  0.6 P̄ get rarer with size faster (the rim's fuller and thinner rows and empty corners enter the stationary
  fluctuations of P), not because the collapse below 0.6 P̄ has a cost growing with the edge. This is a
  statement among hull faces. It does not say a wrapped face has the same q: `research/dying` round 3 found the
  63-cell torus's tail cheaper per live cell lost (0.427 against 0.499), so q differs by a factor between the two
  kinds of face; my tables say only that for rimmed faces that factor does not grow with the edge.

## Deliverable 5: reactive paths

`paths/R9.txt`, `R11.txt`, `R13.txt` (300, 300, 100 paths; `python3 curate.py 25` from the frozen sampler's runs, one
path per ancestor per replication). **Caveat: these come from the flip sampler, biased by −0.03, −0.17 and more;**
its dying paths carry flips five layers down. Format: header lines; a line `C` with the doubled coordinates of
the face's cells in order; then per path `seed ancestor T k age[0..A−1] P pop[−15..0]`: T generations from the
crossing of ⌊0.9 P̄⌋ to the empty face, k faces empty at the death, age = generations before the death at which
that cell was last alive (255 = 255 or more), then the face population at the last 16 generations.
- Duration T: 8.95 ± 0.09 (R = 9), 9.93 ± 0.21 (R = 11), 12.5 ± 1.0 (R = 13) generations.
- Deaths containing a one-generation fall of half the face (the PI's "bust"): 2.1% at R = 9 (anatomy's brute force:
  1.6 to 2.2%), 0.9% at R = 11 (dominated by a few ancestors; median replication 0.01%), none in 4 replications at
  R = 13. **The sampler cannot tell whether the bust share grows with size:** a bust is a crossing that is already
  deep, such crossings are rare among the 100,000 stored, and the downward levels never look for them. The
  forecast of point 2 does not have this weakness (ν and the anchors count every route).

**The bust route by plain running [measured]** (`shb3 R SEED 0 GENS > runs/fall_R<R>.txt`, lines `B` and `F`; added
after the PI's note; this is exact gump, not the sampler). Rate of one-generation falls of at least half the face,
per hull-generation and face: ln = −10.784 ± 0.029 (R = 9, 1,167 falls), −13.163 ± 0.080 (R = 11, 157), −15.23 ± 0.20
(R = 13, 25), about −18.2 (R = 15, one fall); the face stands at 0.79 to 0.80 of its area just before. None ended on
an empty face in the same generation. So such falls get rarer by 0.10 to 0.13 per cell, half as fast as deaths
(0.21 to 0.22 per cell): there are 0.38 of them per death at 45 cells, 1.6 at 63, 18 at 84, of order 170 at 108.
Against all arrivals below 0.6 P̄ they are a share e^−6.6, e^−8.2, e^−9.3 at 45, 63, 84 cells. For the bust share
of deaths to stay near 2% (anatomy: 45 and 63 cells) the chance that a bust ends in death must fall from about
5% to 1.2% to 0.1%; if it falls more slowly on larger faces, busts take over and lifetimes come out **below** the
forecast of point 2: this is the named way that forecast can fail, and I could not measure that chance.

## What failed, a line each

- One flip three layers down at the crossing (no lag): unbiased within 0.16 at R = 11 but scatter 0.4 to 0.5 per
  replication at 3 × 10⁵ trials a stage; coarser levels (6, 9 cells) no better.
- One flip one layer down: 12.96 ± 0.10 at R = 11 (8 replications at 3 × 10⁴ trials): biased by −0.67.
- Lag 2, a sixth of the fifth layer (frozen): biased −0.17 at R = 11. Lag 2, one flip: scatter 0.4 (3 seeds).
- Donor swap: −0.10 ± 0.12 at R = 11, scatter 0.24: no better.
- Freezing after four seeds: the four gave 13.604 ± 0.06; twelve gave 13.461 ± 0.044.

## Not checked

- Dice chain: whether its offset from gump stays near +0.09 at 135 cells (the two blind sizes bound a drift only to
  ± 0.001 per cell); convergence of the Metropolis sweeps (doubling NSWEEP) at any size; coins at the living density
  instead of fair coins (the PI's suggestion; not tried); the chain itself by brute force beyond R = 11 (13.70 ± 0.06
  there, 275 deaths); replications of one run share the 512 stationary lanes (64 generations apart), R = 17 has
  three seeds (40 replications each), the calibration sizes one seed each.
- Whether the −ln q(0.6) line continues beyond 108 cells: that is the forecast itself. It fails at 30 cells.
- Levels at fixed density instead of fixed fractions of P̄; the same decomposition on wrapped faces (the test that
  would say whether the two prices differ only in the attempt rate).
- The sampler at R = 15 and R = 17; lag 3 or 4 with a single flip; whether the donor swap is unbiased.
- The dependence of ν on the home level ⌈P̄⌉, which sits 0.2 to 0.8 cells above P̄ depending on the size: it can
  move the shallow rates by about 0.01 and should not matter at 0.6 P̄; not tested. Seeds: one to three runs per
  size, pooled; no run-to-run scatter beyond Poisson was looked for.
- P̄ beyond the 300-generation pilots (agreement with `research/dying`'s exposure means: 21.60, 55.19 there; 21.60,
  55.18 here). Settled lives: none seen (no hull reached age 100,000, no trial timed out).
- The bust channel at large sizes (see deliverable 5).

## The sampler, exactly (for the referee who rewrites it from the oracle)

**Vessel.** Cells: p ∈ Z³ (doubled coordinates) with exactly one odd coordinate and |x| + |y| + |z| ≤ R, R odd.
Neighbours: the oracle's twelve; a neighbour outside the vessel is dead (T2 makes this the infinite lattice's own
dynamics). Face f (eight sign patterns d): the cells with d·p = R; counts 45, 63, 84, 108, 135, 165, 198 for
R = 9 … 21, hull sizes 510, 876, 1,386, 2,064, 2,934, 4,020, 5,346. The **watched face** is d = (+,+,+); P is the
number of its live cells. A face is *empty* when none of its cells is alive; adjacent faces share their rim row.

**Why forward-flux sampling.** The death rate is exactly (rate of first crossings of a level, coming from above
P̄) × (chance that such a crossing continues to an empty face before returning above P̄): the ν·q bookkeeping of
`research/dying`. Forward-flux sampling (Allen, Frenkel, ten Wolde) estimates the second factor as a product of
conditional probabilities between levels with a fixed number of trials per stage; the product of the stage
fractions is an unbiased estimate of the rate (not of its logarithm), trials are plain runs of the true rule that
fit the lanes of a bit-sliced stepper, and there are no weights to carry. Level function: P itself.

**Base run** (gives the flux and the first store). 2,048 independent hulls. A hull starts as a soup (each cell
alive with probability 0.35), age 0; every generation its age grows by 1. After each generation: if any of the
eight faces is empty the hull is replaced by a fresh soup (age 0); it is a *first death* if the generation is
counted. A hull-generation is *counted* (exposure += 1) when the hull's age after the step exceeds 200 and the
counting phase is on. Phases, in global generations: 200 of burn-in; 300 of pilot, in which P̄ and σ_P are the mean
and standard deviation of P over hulls older than 200; then λ_A = ⌈P̄⌉ and λ₀ = ⌊0.9 P̄⌋ are fixed; 100 generations
to let the flags settle; then the counting phase, until 100,000 configurations are stored.
Each hull carries a flag (0 at a soup and at the end of the pilot). From age 100 on: if P ≥ λ_A the flag becomes 1;
else if P ≤ λ₀ and the flag is 1, the flag becomes 0 and this is a **crossing** (it counts if the generation is
counted; a generation at which another face is empty and P > 0 ends the hull and is no crossing; an empty watched
face with the flag at 1 is a crossing). Φ₀ = crossings / exposure. Each counted crossing is stored with
probability H = 0.5. **What is stored is the hull's state LAG = 2 generations before the crossing** (plus, as
passengers, each face cell's age since it was last alive and the last 16 values of P as of the crossing).

**Levels.** λ₀, λ₀ − 3, λ₀ − 6, …; the first value ≤ 0 is replaced by 0, the last level (the empty face).

**Stage i** (from λ_i to λ_{i+1}). M = 300,000 trials. Trial j starts from stored configuration π(j mod N_i), π a
uniform random permutation of the N_i configurations of level i, drawn afresh for the stage. The start state is
the stored (two-generations-old) state with ⌈|S|/6⌉ **perturbations**, applied one after another: with probability
½ "kill" (one live cell of S, chosen uniformly, dies), otherwise "revive" (one dead cell of S, chosen uniformly,
comes alive); if the kind drawn has no candidate the other kind is done. **S**: the cells with x + y + z = R − 10
(the fifth layer beneath the watched face's layer) and d·p ≤ R − 4 for the seven other sign patterns (|S| = 21, 36,
54, 75, 99, 126, 156 for R = 9 … 21). Then the true rule runs. The first two generations are a **replay**: nothing
at depth five can change the face layer within two generations (a cell's neighbours are at most two layers up,
T1), so after two generations the watched face is exactly the parent's face at its crossing or success, with its
whole history, while the layers beneath it already differ between clones. (Checked in every trial by comparing P
with the parent's: `replaybad 0` in every RESULT line.) From that generation on (trial age 2, 3, …), in this order:
(1) P = 0: success (in the last stage with weight 1/k, k the number of faces empty at that generation);
(2) another face empty: failure; (3) P ≤ λ_{i+1}: success; (4) P ≥ λ_A: failure; (5) age above 20,000: failure,
booked as a timeout (none occurred). On success the state stored for level i + 1 is the trial's state **two
generations before** the success. If a stage has more than 100,000 successes a uniform subset of 100,000 is kept
(reservoir sampling). p̂_i = (sum of success weights) / M.

**Estimator.** 1/τ̂ = Φ₀ · ∏ p̂_i; ν̂(λ_i) = Φ₀ · ∏_{j<i} p̂_j; q̂ = 1/(τ̂ ν̂). By the symmetry of the eight faces the rate
at which the watched face is among the first to empty (ties shared) is 1/τ_face = deaths / (8 · exposure), the
anchors' definition (fresh soups of 0.35, ageing-in 200, a hull retired at its first death).

**Error procedure.** K independent replications of everything (base run, pilot, stores, stages; seeds R·1000 + k).
Pooled value ln τ = −ln(mean of the K rates 1/τ̂_k); error = standard deviation of the rates / (√K · mean), with
a jackknife beside it (`ana.py`). The mean of the K logarithms is printed too; it is biased upward by about half
the variance of one replication's logarithm.

**Brute-force dip rates** (`shb R SEED 0 GENS`: the base run alone, with a counting phase of GENS generations; no
cloning, no flips, so this part is plain gump). Each hull carries m, the smallest P seen since P was last ≥ λ_A
(reset when P ≥ λ_A and at a soup). At a counted generation at which P ≥ λ_A, or at which the hull is retired
(some face empty), the excursion ends and, if m < λ_A, is booked once with its minimum (0 if the watched face is
empty; min(m, P) if another face is). ν(L) = (excursions booked with minimum ≤ L) / exposure: the rate of first
passages below L+1 coming from above P̄, the same quantity as the sampler's Φ₀·∏p̂. "Threshold-free" ν(p): ln ν
interpolated linearly between the integer levels on either side of p·P̄. First deaths and exposure give
ln(8E/D) as in the anchors. `levels.py` pools all `runs/brute_R<R>*.txt` (counts and exposures add).

**Why the lag.** Gump is deterministic, so clones must be separated, and a separation deep enough to be harmless
takes generations to reach the face, while the whole dip from 0.9 P̄ to an empty face lasts about ten generations.
Flipping one cell three layers down at the moment of the crossing left the estimator starved (scatter 0.4 to 0.5 of
one replication at R = 11 with 3 × 10⁵ trials a stage, half the replications 0.5 too high), and flipping one layer
down biased it (12.96 ± 0.10 against 13.633: `./sh` with the earlier depth argument; rows in "What failed").
Starting each clone two generations in the past moves the flips to depth five, lets the true rule launder them for
two generations, and still has the clones differ directly beneath the face at the moment of the crossing.

**Passengers.** Per face cell an 8-bit age (generations since last alive, saturating at 255), stepped with the
state and stored with it; and the last 16 values of P. Neither enters the dynamics or the selection.

## Reproduce

```sh
python3 research/blast/split-hull/validate.py 1200            # stepper against the oracle, R = 11 and 15 (~1 min)
S=research/scratch/blast/split-hull; mkdir -p $S/runs
gcc -O3 -march=native -o $S/shb research/blast/split-hull/sh.c -lm    # (shf, shs, shb, shb2, shb3 in scratch: this file at
                                                                      #  successive commits; the sampler part is unchanged)
$S/shb 17 17900 0 40000 > $S/runs/brute_R17.txt              # plain running: dip rates, P-bar, first deaths (~90 s)
#   runs used: R 7: 7900 x 60000 | 9: 9900 x 40000 | 11: 11900 x 40000 | 13: 13900 x 60000 | 15: 15900 x 40000, 15901 x 150000
#   17: 17900 x 40000, 17901 x 200000, 17902 x 150000 | 19: 19900 x 20000, 19901 x 170000, 19902 x 200000
#   21: 21900 x 15000, 21901 x 150000, 21902 x 300000 | 13 also 13901 x 150000   (seed x GENS; files brute_R<R>[_b|_c].txt)
#   falls: fall_R<R>.txt from seeds 9903 x 30000, 11903 x 40000, 13903 x 50000, 15903 x 40000
python3 research/blast/split-hull/levels.py                   # sampler against brute force; the lines; the forecasts
sh research/blast/split-hull/chain.sh 11 11001 12             # 12 replications of the frozen sampler at R = 11 (~5 min)
python3 research/blast/split-hull/ana.py                      # pooled values, nu and q by level, path statistics
sh research/blast/split-hull/variant.sh 11 11201 6 2 0 swap2 1    # donor swap
python3 research/blast/split-hull/curate.py 25                # paths/R*.txt from the runs' path files
python3 research/blast/split-hull/fill.py                     # pastes levels.py's tables into this README
# one replication by hand:  sh R SEED M LAG NFLIP STEP H PATHFILE CAP [MODE]
research/scratch/blast/split-hull/shf 11 11001 300000 2 -6 3 0.5 - 100000
```
