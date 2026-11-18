# REVIEW of split-slab's dice-chain sampler (referee `ref-slab`, 2026-11-18, 04:45-05:20 UTC)

Reviewed: `research/blast/split-slab/README.md` sections 1, 2 and 6 as of 04:40 UTC, `ss.c` (mode `sub`), its data
files `data/sub_*_s2..s4.txt` and its stored dying paths. Marks: **[proved]**, **[measured]**, **[conjectured]**.
`R` = `research/scratch/blast/ref-slab`, `G` = `research/scratch/blast/split-slab`. Every table below is printed by
`bash final.sh > data/final.txt` from the raw files in `data/` (and the path files under `R/out/`).
One core, shared (about 57% of it).

## Verdict in plain words

1. **The surrogate is sound where it can be checked.** By my own stepper (bit-exact against the oracle) the dice
   chain has gump's face lifetime to within 0.02 at 48, 60 (a loop^2 12 tube), 63 and 84 (tube) cells, and its
   natural deaths are gump's deaths: same share of half-face falls to the third digit.
2. **The sampler is correctly built.** I found no fault in the proposal, the acceptance rule, the levels or the
   estimator; its level function is a minimum over a window of the whole path, so the over-full generation and
   the crash are not conditioned against. It is unbiased in expectation for any number of sweeps. Against brute
   force of the same chain it reads -0.015 +- 0.006 (48 cells; 2.4 sd, which I could neither explain nor remove),
   +0.029 +- 0.021 (63), -0.02 +- 0.08 (84): no bias larger than about 0.03 where truth is cheap.
3. **Its weakness is a heavy-tailed estimator, not a bias.** The initial states are never moved and only about one
   proposal per chain and level does anything; the ~2,000 dying chains of a replication descend from 194 initial
   states at 48 cells, 92 at 63, 36 at 120 and **9.5 at 192 (wide; 24 on the tube)**. One replication scatters by a factor e^0.5 at 120
   cells and e^1.0 at 192. With 48+ replications (up to 120 cells) the quoted errors are honest. With 12-16
   replications at 192 cells they are not: the mean is carried by one or two replications.
4. **The 120-cell value may be quoted**, as a forecast from a surrogate and with my pooled number: dice chain
   **24.63 +- 0.05** (102 replications, half of them fresh), hence **24.60 +- 0.07 for gump** in place of
   24.68 +- 0.09, with the sentence "the surrogate's offset from gump is measured by brute force only up to 84
   cells (under 0.02 there)".
5. **The 192-cell numbers may not be quoted as measurements.** "Wide 192 cells lies above the wide-face line" is
   **not established**: my 8 fresh replications read 39.75 +- 0.46, below the line (40.07); all 26 pooled read
   40.25 +- 0.26. The 192-cell tube (38.73 +- 0.18) and "the tube is about 1.5 below the wide torus" hold up
   better, but none of the three is a measurement to its quoted error.
6. **The long-tube shares may be quoted only as a trend, not as numbers.** The recount reproduces split-slab's
   table from its paths, the sampler's paths are representative of natural deaths at 63 and 84 cells, and the
   contrast at 192 cells survives fresh seeds (tube 0.15 +- 0.06, wide torus 0.70 +- 0.05); but the 120-cell
   share is 0.42 to 0.45, not 0.38, the plain averages lean towards the gradual route (replications with a
   higher rate hold more boom and bust), and at 144-192 cells the shares are good to +- 0.1 at best.

## Claim by claim

| # | claim | verdict | my number |
|---|---|---|---|
| 1 | dice chain within 0.02 of gump at 48 and 63 cells (brute force) | **CONFIRMED**, and extended to two tubes | chain - gump anchor: +0.012 +- 0.004 (48), -0.008 +- 0.011 (63), +0.015 +- 0.057 (84 tube); chain - gump by my code on the 60-cell tube (1,8),(0,20): +0.013 +- 0.019 |
| 1' | (asked by the PI) the chain's share of deaths with a half-face fall equals gump's | **CONFIRMED** | 48 cells: 0.5914 +- 0.0019 against 0.5916 +- 0.0019; 63: 0.562 +- 0.006 against 0.558 +- 0.007; 60-cell tube: 0.583 +- 0.007 against 0.580 +- 0.006 |
| 2 | sampler against gump's anchors at 63, 84, 96, 108, 108 cells | **CONFIRMED** as arithmetic on its files (`pool.py` returns its five values); the blindness of 96 and 108 was **NOT TESTED** (I did not audit commit times) | fresh seeds, 63 cells: 13.191 +- 0.020 (112 replications), all 144: 13.187 +- 0.018, i.e. +0.025 +- 0.018 from gump |
| 2' | "exact for that chain" | **CONFIRMED** to 0.02-0.03 where truth is cheap; exact in expectation by construction, see (b) | sampler - brute force of the same chain: -0.015 +- 0.006 (48), +0.029 +- 0.021 (63), -0.02 +- 0.08 (84) |
| 3a | 120-cell tube 24.68 +- 0.09 (chain 24.710 +- 0.078) | **CORRECTED** (inside its error); its error is honest | chain: 24.532 +- 0.090 on 48 fresh replications, 24.617 +- 0.061 on all 96, 24.63 +- 0.05 with a fourfold-ensemble run; for gump (minus its offset 0.03 +- 0.04): **24.60 +- 0.07** |
| 3b | 144 cells 29.44 +- 0.22 | **NOT TESTED** (8 replications; error itself uncertain) | - |
| 3c | 192-cell tube 38.6 +- 0.25 | **CONFIRMED** within errors on 8 fresh replications; the error is not a clean standard error | chain: 38.93 +- 0.16 fresh, 38.73 +- 0.18 on all 24 |
| 3d | wide 192-cell torus 40.7 +- 0.26, above the wide line | value **CORRECTED** downwards; "above the line" **NOT ESTABLISHED** (the README's 2.5 sd is **REFUTED** as a significance) | chain: 39.75 +- 0.46 on 8 fresh replications, **40.25 +- 0.26** on all 26; line 40.07: +0.18 +- 0.26 or less sure |
| 4 | wide faces keep the face-wide boom and bust to 192 cells, loop^2 12 tubes lose it: 0.50, 0.50, 0.38, 0.26, 0.17 | recount **CONFIRMED** on its paths; 120-cell value **CORRECTED**; the contrast at 192 cells **CONFIRMED** on fresh seeds; the numbers at 144-192 are good to +- 0.1 only | 120: 0.42 +- 0.02 (plain), 0.45 +- 0.03 (rate-weighted), 80 replications; 192 tube: 0.16 +- 0.04, 0.20 +- 0.07; 192 wide: 0.61 +- 0.05, 0.73 +- 0.06 |

## (a) The surrogate by my own code [measured]

Definition taken from split-slab's README section 6 and `ss.c`: slab torus of 8 layers; layers 0..5 follow B45/S345
on the 12 neighbours; layers 6 and 7 are overwritten after every generation by independent fair coins (density
1/2, fresh per cell and generation); one face, layer 0; a face death is the first generation with layer 0 empty
(it cannot revive: T2's count); lives start from a 0.4 soup, the first 1,000 generations are not counted;
tau_face = face-generations / face deaths.

**Stepper.** `rgeom.py` (graph from doubled coordinates, own canonical form and numbering), `dice.c` (512 lanes,
ripple counter). `python3 rvalidate.py H K D GENS [N]`: a 0.4 soup on the slab tiled into the oracle's cubic torus
must equal `reference/oracle.py`'s whole array at every generation; then the same with one neighbour entry
replaced, which must fail (`data/validate.log`):

| torus | cells | generations | result | negative control |
|---|---:|---:|---|---|
| (4,0),(0,4) | 48 | 1,200 | MATCH state for state | first mismatch at generation 4 |
| (1,4),(0,21) | 63 | 1,200 | MATCH | generation 5 |
| (1,8),(0,20) | 60 | 1,200 | MATCH | generation 1 |
| (1,12),(0,28) | 84 | 1,000 | MATCH | generation 8 |

`python3 graphcheck.py H K D G/g_H_K_D.bin`: split-slab's graph files are the same graphs as mine (cell by cell
through the coordinates, layers included) on all ten tori it used, among them the three it had not validated:
(1,22),(0,48), (1,30),(0,64), (8,0),(0,8) (`data/graphcheck.log`). The coin layers and the sampler's evaluation loop
are checked only through the lifetimes below.

**Lifetimes** (`R/dice R/r_H_K_D.graph brute WD SEED GENS PATHS`; WD = 6 chain, WD = 0 gump with two faces;
`data/brute_*.txt`; errors 1/sqrt(deaths)):

| torus | cells | gump, my code | gump anchor | dice chain, my code (deaths) | split-slab's brute force of the chain | chain - anchor |
|---|---:|---|---|---|---|---|
| (4,0),(0,4) | 48 | 9.9188 +- 0.0039 | 9.9251 +- 0.0004 | 9.9371 +- 0.0038 (67,779) | 9.9407 +- 0.0085 | +0.012 +- 0.004 |
| (1,8),(0,20), loop^2 12 | 60 | 12.398 +- 0.013 | - | 12.411 +- 0.014 (5,189) | - | (chain - my gump: +0.013 +- 0.019) |
| (1,4),(0,21) | 63 | 13.172 +- 0.013 | 13.1622 +- 0.0007 | 13.154 +- 0.011 (7,897) | 13.182 +- 0.027 | -0.008 +- 0.011 |
| (1,12),(0,28), loop^2 12 | 84 | - | 17.3175 +- 0.0031 | 17.333 +- 0.057 (304) | - | +0.015 +- 0.057 |

Commands: `brute 6 11 3000000`, `brute 0 13 1500000` (48); `brute 6 15 2500000`, `brute 0 16 1500000` (60);
`brute 6 12 8000000`, `brute 0 14 3000000` (63); `brute 6 17 20000000` (84).

- The offset at 48 cells is real and small: +0.012 +- 0.004 (3 sd). Nothing larger than 0.02 at 60 to 63 cells,
  nothing larger than 0.12 at 84. **Beyond 84 cells the chain's offset from gump is known only through the
  sampler** (split-slab's +0.029 +- 0.036 on tubes of 84 to 108 cells).
- **A bookkeeping trap [measured].** At 48 cells 38 of 68,266 lives of the chain (44 of 65,963 in gump) settle
  into a thin face (the one I looked at held about 10 live cells for 19,000 generations) that then practically
  never dies: 0 deaths in 4.4% of all exposure in the chain, 2 deaths in 4.8% in gump. [conjectured] A T3
  firewall beneath the face, which also cuts the coins off; I did not look inside.
  Counted in, they raise ln tau by 0.045 (chain) and 0.049 (gump). The 48-cell rows above exclude lives with
  more than half of their 64-generation samples under A/4 (line `STUCK` of the outputs). At 63 cells: 2 of 8,409
  lives, +0.003; at 60 and 84 cells none. split-slab's age cap of 50,000 keeps its own 48-cell number within
  about 0.003 of mine, so its claim is unaffected; in the sampler such a lane stays in the ensemble for good
  (it is never reseeded), which is harmless at these frequencies.
- **The chain dies as gump dies** (`python3 shares.py A brute PATHS`; largest one-generation fall among the 16
  generations before the death):

| torus | cells | gump: fall >= A/2 | chain: fall >= A/2 | gump: fall, from, generations before the death | chain |
|---|---:|---|---|---|---|
| (4,0),(0,4) | 48 | 0.5916 +- 0.0019 | 0.5914 +- 0.0019 | 0.515 A, 0.734 A, 4.87 | 0.515 A, 0.735 A, 4.85 |
| (1,8),(0,20) | 60 | 0.580 +- 0.006 | 0.583 +- 0.007 | 0.510 A, 0.730 A, 5.24 | 0.508 A, 0.729 A, 5.23 |
| (1,4),(0,21) | 63 | 0.558 +- 0.007 | 0.562 +- 0.006 | 0.513 A, 0.734 A, 5.22 | 0.512 A, 0.732 A, 5.25 |
| (1,12),(0,28) | 84 | - | 0.516 +- 0.029 (304 deaths) | - | 0.480 A, 0.708 A, 6.04 |

## (b) Is the subset simulation exact?

**Reading of `ss.c`, mode `sub` [proved, standard; checked line by line].**
- *Level function.* The score of a chain is the minimum of the face population over the last 24 generations of
  its 56-generation path (undefined if the face is dead at generation 32). It is a function of the path, not of
  a state, and nothing conditions on a falling population: a path that over-fills and crashes passes every level
  at once. The classic fault (a ladder the dominant route does not climb in order) is absent.
- *Moves.* A proposal flips 4 dice bits. Uniform sweeps are symmetric. Focused sweeps draw the bits from the 12
  generations before the chain's first minimum g_min and are accepted only if every drawn bit also lies in the
  window of the new chain: the window has the same size before and after (g_min >= 33 > 12, the clamp at 0 is
  never reached), double hits of one bit are counted alike in both directions, so the kernel is reversible for
  the fair-coin law restricted to {score <= level}. Correct.
- *Estimator.* Product of the level fractions, survivors copied round-robin from a uniform random offset (every
  survivor expects the same number of copies). With kernels that leave each conditioned law invariant this
  product is unbiased for P(score = 0) **whatever the number of sweeps** (the unbiasedness of the sequential
  Monte Carlo normalising constant). P(score = 0) = P(alive at 32, dead by 56) = (24/tau)(1 - 44/tau + ...): the
  fixed horizon costs 0.002 at 48 cells and nothing beyond. Replications are averaged as rates (right) and the
  error is their scatter (right, when there are enough of them).
- *What "exact" does not cover.* (i) The initial states are never moved: diversity among them is only lost.
  (ii) Most accepted proposals change nothing. With my counters (`ss_diag.c`, lines `DIAG`): acceptance 0.22
  (uniform) and 0.42-0.56 (focused) at deep levels, but only **0.014 and 0.10 of the proposals** are accepted and
  change the score or the generation of the minimum (120 cells; 0.024 and 0.11 at 63 cells). With NSWEEP = A/6
  that is about **one effective move per chain and level** (0.7 at 63 cells, 1.1 at 120). (iii) Hence the
  genealogy collapses: distinct initial states among the dying chains of one replication, of 4,096 chains:

  | cells | 48 | 63 | 120 | 192 wide | 192 tube |
  |---|---|---|---|---|---|
  | distinct ancestors of the dying chains (mean; min..max) | 194 (176..216) | 92 (73..109) | 36 (26..49) | 9.5 (6..12) | 24 (20..26) |
  | sd of ln(rate) of one replication | 0.11 | 0.22 | 0.50 | 1.18 | 0.63 |

  An unbiased estimator with such a tail reads **too long a lifetime in most small samples** and its scatter
  understates its error. That is a statement about 144 and 192 cells, not about 120.

**Test where truth is cheap [measured]** (fresh seeds 7101-7104; split-slab's frozen parameters:
`WD=6 R/ss_diag G/g_4_0_4.bin sub SEED 64 14 3 8 8 4 32 24 PATHS 12`, `... g_1_4_21.bin sub SEED NREP 20 3 8 10 4 32 24 PATHS 12`):

| cells | sampler, fresh seeds (replications) | sampler, all replications | brute force of the same chain (mine; mine and split-slab's pooled) | sampler - brute force |
|---|---|---|---|---|
| 48 | 9.923 +- 0.006 (384) | - | 9.9371 +- 0.0038; 9.9359 +- 0.0026 (+0.002 for the horizon) | **-0.015 +- 0.006** |
| 63 | 13.191 +- 0.020 (112) | 13.187 +- 0.018 (144) | 13.154 +- 0.011; 13.158 +- 0.010 | **+0.029 +- 0.021** |
| 84 tube | (split-slab's 32:) 17.311 +- 0.060 | - | 17.333 +- 0.057 | -0.02 +- 0.08 |

Chi-square of the three differences against zero: 7.3 on 3 (p = 0.06). The 48-cell difference is 2.4 sd and I
chased it without finding a cause:
- not the age of the lives: `CAP=5000 R/dice R/r_4_0_4.graph brute 6 21 3000000` (lives cut at age 5,000, so ages
  1,000 to 5,000 only) gives 9.9334 +- 0.0041 against 9.9371 +- 0.0038 for all ages;
- not the sampler's pipeline (initial states, evaluation loop, score, horizon): with LAM1 = 0 the program counts
  deaths of fresh chains directly, no levels and no sweeps: 9.943 +- 0.008 (40 runs of 100 replications,
  `direct48.sh`, run from `R`; expected 9.938). One long run of 3,000 replications reads 9.974 +- 0.009, because the
  immortal "stuck" lanes of (a) accumulate in an ensemble that is never reseeded unless a face dies: a second,
  independent sighting of them, and a warning for long runs on small tori only;
- so if it is real it sits in the levels and sweeps, where I found no error, and it has the other sign at 63
  cells. **Bias excluded: more than about 0.03 at 48 cells and 0.07 at 63 cells (2 sd).**
**Not tested: exactness at any size where the genealogy has collapsed** (96 cells and more). There the only
checks are split-slab's against gump's anchors (to 0.06-0.09 each), and the larger ensemble below.

## (c) The new numbers [measured, surrogate]

Fresh seeds 7201-7207 (120-cell tube: `WD=6 R/ss_diag G/g_1_18_40.bin sub SEED 8 44 3 8 20 4 32 24 PATHS 12`),
7301-7303 (wide 192: `... g_8_0_8.bin sub SEED 4 77 3 8 32 4 32 24 PATHS 12`), 7401-7402 (192-cell tube:
`... g_1_30_64.bin ...` same parameters). `python3 pool.py LABEL FILES`: ln tau from the mean rate, error from the
scatter, a bootstrap interval over replications, and the share of the summed rate carried by the largest one.

| face | split-slab's replications | fresh seeds | all pooled | bootstrap 95% of the pooled value | largest replication's share of the summed rate |
|---|---|---|---|---|---|
| 120-cell tube (1,18),(0,40), 4,096 chains | 24.710 +- 0.078 (48) | 24.532 +- 0.090 (48) | **24.617 +- 0.061** (96) | 24.50 .. 24.73 | 0.05 |
| the same with 16,384 chains (NBATCH 32, seed 7260) | - | 24.680 +- 0.100 (6) | with the row above: **24.63 +- 0.05** | | 0.24 |
| wide 192-cell torus (8,0),(0,8) | 40.723 +- 0.257 (12); its later file s5: 40.364 +- 0.296 (6) | 39.754 +- 0.462 (8) | **40.25 +- 0.26** (26) | 39.80 .. 40.80 | 0.24 (0.48 among mine) |
| 192-cell tube (1,30),(0,64) | 38.647 +- 0.245 (16) | 38.932 +- 0.155 (8) | **38.73 +- 0.18** (24) | 38.40 .. 39.09 | 0.18 |

Per-replication ln tau at 192 cells (end of `data/final.txt`): wide 38.41 to 42.97, tube 37.25 to 39.90.

- **120 cells: the quoted error is honest; the value moves down by one of its errors.** The two halves (theirs,
  mine) differ by 0.18 +- 0.12; nine runs with nine seeds agree with each other (`python3 runs.py`, chi-square 2.8
  on 8 for the mean of ln rate); a fourfold ensemble halves the scatter of a replication (0.50 to 0.23 in ln rate,
  141 ancestors instead of 36) and reads the same value. Dice chain: **24.63 +- 0.05**. For gump, with
  split-slab's own offset d = +0.03 +- 0.04 (sampler against anchors on tubes of 84 to 108 cells): **24.60 +- 0.07**
  in place of 24.68 +- 0.09. (This is also where its independent bookkeeping forecast sits: 24.59 +- 0.05.)
  What the error does not contain: any drift of the chain's offset from gump between 84 and 120 cells that brute
  force has not seen, and the unexplained 0.015 of (b).
- **Wide 192 cells: 40.25 +- 0.26 against the wide line's 40.07: +0.18, not established.** My 8 fresh
  replications read 39.75 +- 0.46, below the line; split-slab's own six later ones read 40.36. The scatter of ln
  rate is 1.2 and a quarter to a half of the summed rate sits in one replication, so even +- 0.26 is an
  understatement (a lognormal reading of the same 26 gives 40.19 +- 0.30). The 2.5 sd of the README was the
  small-sample skew of a heavy-tailed estimator: 12 replications, median 41.09, mean-rate value 40.72, and each
  further batch has pulled the value down. Neither "the wide price rises beyond 126 cells" nor "the sampler
  loses accuracy" is needed. To settle it: at least 100 replications of 4,096 chains, or 25 of 16,384 (the same cost, and more
  ancestors survive).
- **192-cell tube: 38.73 +- 0.18** (README 38.65 +- 0.25; consistent). Tube below wide torus at 192 cells:
  1.5 +- 0.3 (README 2.08 +- 0.36); slope of the tube from 108 to 192 cells 0.197 +- 0.002 per cell (README 0.196
  +- 0.003; unchanged). These two survive because the tube keeps more ancestors (24 against 9.5) and scatters
  less (0.63 against 1.18), but they are still sums dominated by a few replications: quote them as "about 1.5
  below" and "about 0.197", with the +- 0.3 drift split-slab already admits.
- The errors quoted at 144 and 192 cells are **not honest as standard errors**; at 63 to 120 cells they are.

## (d) The shares of claim 4 [measured, surrogate]

`python3 shares.py A sub PATHS:SUBFILE ...` (my recount; split-slab's convention: largest one-generation fall among
the 16 generations before the death; per replication first). Two averages: the plain mean over replications
(split-slab's) and the **rate-weighted** mean, sum r_i s_i / sum r_i, which is the consistent estimate of the share
among natural deaths (a replication stands for r_i of the death rate; the plain mean is biased whenever rate and
share are correlated, and they are: last column).

| face | cells | replications with paths | fall >= A/2, plain mean | rate-weighted | largest fall (plain; weighted) | correlation of ln rate with the share | README |
|---|---:|---:|---|---|---|---:|---|
| natural deaths of the chain, (1,4),(0,21) | 63 | 7,896 deaths | 0.562 +- 0.006 | - | 0.512 A | - | (gump 0.558) |
| sampler, (1,4),(0,21), fresh | 63 | 112 | 0.554 +- 0.009 | 0.556 +- 0.008 | 0.512 A | +0.10 | 0.54 +- 0.02 |
| natural deaths of the chain, tube (1,12),(0,28) | 84 | 304 deaths | 0.516 +- 0.029 | - | 0.480 A | - | - |
| sampler, tube (1,12),(0,28), split-slab's | 84 | 16 | 0.501 +- 0.030 | 0.493 +- 0.031 | 0.488 A | -0.31 | 0.50 +- 0.03 |
| tube (1,16),(0,36), split-slab's | 108 | 16 | 0.497 +- 0.043 | 0.537 +- 0.051 | 0.475 A; 0.485 A | +0.60 | 0.50 +- 0.04 |
| wide (6,0),(0,6), split-slab's | 108 | 24 | 0.594 +- 0.028 | 0.579 +- 0.032 | 0.511 A | -0.20 | 0.59 +- 0.03 |
| tube (1,18),(0,40), split-slab's | 120 | 32 | 0.382 +- 0.025 | 0.396 +- 0.033 | 0.439 A | +0.17 | 0.38 +- 0.03 |
| tube (1,18),(0,40), fresh | 120 | 48 | 0.441 +- 0.022 | 0.486 +- 0.039 | 0.458 A; 0.470 A | +0.43 | - |
| tube (1,18),(0,40), all | 120 | 80 | **0.418 +- 0.017** | **0.454 +- 0.029** | 0.451 A; 0.459 A | +0.36 | 0.38 +- 0.03 |
| tube (1,22),(0,48), split-slab's | 144 | 8 | 0.262 +- 0.046 | 0.311 +- 0.048 | 0.409 A; 0.422 A | +0.67 | 0.26 +- 0.05 |
| tube (1,30),(0,64), split-slab's | 192 | 16 | 0.166 +- 0.055 | 0.194 +- 0.099 | 0.344 A; 0.357 A | +0.27 | 0.17 +- 0.06 |
| tube (1,30),(0,64), fresh | 192 | 8 | 0.147 +- 0.063 | 0.200 +- 0.079 | 0.353 A; 0.369 A | +0.73 | - |
| tube (1,30),(0,64), all | 192 | 24 | **0.160 +- 0.042** | **0.196 +- 0.074** | 0.347 A; 0.360 A | +0.36 | 0.17 +- 0.06 |
| wide (8,0),(0,8), split-slab's | 192 | 12 | 0.553 +- 0.076 | 0.686 +- 0.063 | 0.506 A; 0.535 A | +0.72 | 0.55 +- 0.08 |
| wide (8,0),(0,8), fresh | 192 | 8 | 0.701 +- 0.052 | 0.750 +- 0.096 | 0.526 A; 0.531 A | +0.28 | - |
| wide (8,0),(0,8), all | 192 | 20 | **0.612 +- 0.052** | **0.726 +- 0.063** | 0.514 A; 0.532 A | +0.52 | 0.55 +- 0.08 |

- **Recount: CONFIRMED.** My script returns every entry of split-slab's path table from its files (last column).
- **Representative where it can be checked: yes.** Against natural deaths of the same chain the sampler's
  deaths have the same share and the same fall at 63 cells (0.554 +- 0.009 against 0.562 +- 0.006; 0.512 A both)
  and on the 84-cell tube (0.50 +- 0.03 against 0.52 +- 0.03; 0.488 A against 0.480 A), and at 48 cells
  (0.602 +- 0.006 against 0.591 +- 0.002). Natural deaths already show the tube's share falling with length:
  0.583 at 60 cells, 0.516 at 84 (brute force of the chain; wide tori: 0.591 at 48, 0.562 at 63).
- **120 cells: CORRECTED.** 0.38 +- 0.03 was one run of 32 replications; 48 fresh ones give 0.44 +- 0.02, all 80
  give 0.42 +- 0.02 (plain) or **0.45 +- 0.03** (rate-weighted). Runs with different seeds are compatible
  (chi-square 9.4 on 7). The 120-cell tube is thus little below the 84- and 108-cell tubes (0.49 and 0.54,
  rate-weighted), not a step down.
- **Beyond 108 cells the plain mean understates boom and bust.** Where the genealogy has collapsed, replications
  that found a higher rate hold more boom-and-bust deaths (correlation +0.4 to +0.7), so the plain mean leans
  towards the gradual route; the weighted mean is consistent but rests on 6 to 14 effective replications at 144
  and 192 cells. With that said the two 192-cell faces stay far apart on fresh seeds too: tube 0.15 +- 0.06
  (fall 0.35 A), wide torus 0.70 +- 0.05 (fall 0.53 A).
- **What may be said [measured, surrogate]:** on loop^2 12 tubes the share of deaths with a one-generation fall
  of half the face goes 0.58 (60 cells, natural), 0.52 (84, natural), 0.49 to 0.54 (84, 108), 0.42 to 0.45 (120),
  about 0.3 (144), about 0.2 +- 0.1 (192), while wide tori stay at 0.56 to 0.73 from 63 to 192 cells; the largest
  fall shrinks from 0.51 A to 0.35 A on the tube and stays 0.51 to 0.53 A on wide tori. The threshold A/2 sits
  on the middle of the fall's distribution, so the share exaggerates a modest shift of the mean fall; the mean
  fall is the sturdier number. **What may not be said:** "0.38" at 120 cells, or any of the 144- and 192-cell
  shares to better than +- 0.1. Whether the emptying travels along the tube was not looked at.

## Not checked

- Blindness of split-slab's 96- and 108-cell tests (commit order); its sections 3, 4, 5 (splitting on gump, the
  bookkeeping forecast 24.59 +- 0.05); the 144-cell runs; version 1 of the sampler.
- The chain's offset from gump beyond 84 cells; exactness of the sampler beyond 84 cells; whether more sweeps
  or more chains change the 192-cell readings (only the 120-cell tube was run with a fourfold ensemble).
- What the "stuck" lives are inside (firewall or not), and how gump's anchors treat them at 48 cells.
- `ss.c`'s evaluation loop was not validated state for state by me, only through lifetimes; `ss_diag.c` adds
  counters to split-slab's code and changes no number (same seeds give the same REP lines).
