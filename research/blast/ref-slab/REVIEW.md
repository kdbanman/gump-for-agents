# REVIEW of split-slab's dice-chain sampler (referee `ref-slab`, 2026-11-18, 04:45-05:25 UTC)

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
   force of the same chain it reads -0.021 +- 0.011 (48 cells), +0.029 +- 0.021 (63), -0.02 +- 0.08 (84).
3. **Its weakness is a heavy-tailed estimator, not a bias.** The initial states are never moved and only about one
   proposal per chain and level does anything; the ~2,000 dying chains of a replication descend from 194 initial
   states at 48 cells, 92 at 63, 35 at 120 and **9 at 192**. One replication scatters by a factor e^0.5 at 120
   cells and e^1.0 at 192. With 48+ replications (up to 120 cells) the quoted errors are honest. With 12-16
   replications at 192 cells they are not: the mean is carried by one or two replications.
4. **The 120-cell value may be quoted**, as a forecast from a surrogate, with the pooled number of section (c)
   below in place of 24.68 +- 0.09, and with the sentence "the surrogate's offset from gump is measured by brute
   force only up to 84 cells (under 0.02 there)".
5. **The 192-cell numbers may not be quoted as measurements.** "Wide 192 cells lies above the wide-face line" is
   **not established**: my fresh replications fall on the other side of the line and the pooled excess is
   under 2 of its own (understated) errors.
6. **The long-tube shares may be quoted only as a trend, not as numbers.** The recount reproduces split-slab's
   table from its paths, the sampler's paths are representative of natural deaths at 63 and 84 cells, and the
   contrast at 192 cells (tube against wide torus) survives; but the 120-cell share 0.38 +- 0.03 is not reproduced
   by fresh seeds (see (d)), the plain averages are biased towards the gradual route (replications with a higher
   rate have more boom and bust), and at 144-192 cells each replication holds about ten independent deaths.

## Claim by claim

| # | claim | verdict | my number |
|---|---|---|---|
| 1 | dice chain within 0.02 of gump at 48 and 63 cells (brute force) | **CONFIRMED**, and extended to two tubes | chain - gump anchor: +0.012 +- 0.004 (48), -0.008 +- 0.011 (63), +0.015 +- 0.057 (84 tube); chain - gump by my code on the 60-cell tube (1,8),(0,20): +0.013 +- 0.019 |
| 1' | (asked by the PI) the chain's share of deaths with a half-face fall equals gump's | **CONFIRMED** | 48 cells: 0.5914 +- 0.0019 against 0.5916 +- 0.0019; 63: 0.562 +- 0.006 against 0.558 +- 0.007; 60-cell tube: 0.583 +- 0.007 against 0.580 +- 0.006 |
| 2 | sampler against gump's anchors at 63, 84, 96, 108, 108 cells | **CONFIRMED** as arithmetic on its files (`pool.py` returns its five values); the blindness of 96 and 108 was **NOT TESTED** (I did not audit commit times) | fresh seeds, 63 cells: 13.191 +- 0.020 (112 replications), all 144: 13.187 +- 0.018, i.e. +0.025 +- 0.018 from gump |
| 2' | "exact for that chain" | **CONFIRMED** to 0.02-0.03 where truth is cheap; exact in expectation by construction, see (b) | sampler - brute force of the same chain: -0.021 +- 0.011 (48), +0.029 +- 0.021 (63), -0.02 +- 0.08 (84) |
| 3a | 120-cell tube 24.68 +- 0.09 (chain 24.710 +- 0.078) | **CORRECTED** (inside its error) | see (c): chain, all replications pooled; fresh seeds alone read lower |
| 3b | 144 cells 29.44 +- 0.22 | **NOT TESTED** (8 replications; error itself uncertain) | - |
| 3c | 192-cell tube 38.6 +- 0.25 | **NOT TESTED** beyond a few fresh replications, see (c); the error is understated | see (c) |
| 3d | wide 192-cell torus 40.7 +- 0.26, above the wide line | value **CORRECTED** downwards; "above the line" **NOT ESTABLISHED** | see (c) |
| 4 | wide faces keep the face-wide boom and bust to 192 cells, loop^2 12 tubes lose it: 0.50, 0.50, 0.38, 0.26, 0.17 | recount **CONFIRMED** on its paths; 120-cell value **CORRECTED**; trend at 144-192 **stands qualitatively**, numbers not quotable | see (d) |

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
  into a face of about 10 live cells that then does not die in millions of generations (0 deaths in 4.4% of all
  exposure; most likely a T3 firewall beneath the face, which also cuts the coins off; I did not look inside).
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
  | distinct ancestors of the dying chains (mean; min..max) | 194 (176..216) | 92 (73..109) | ANC120 | ANC192W | ANC192T |
  | sd of ln(rate) of one replication | 0.11 | 0.22 | SD120 | SD192W | SD192T |

  An unbiased estimator with such a tail reads **too long a lifetime in most small samples** and its scatter
  understates its error. That is a statement about 144 and 192 cells, not about 120.

**Test where truth is cheap [measured]** (fresh seeds 7101-7104; split-slab's frozen parameters:
`WD=6 R/ss_diag G/g_4_0_4.bin sub SEED 64 14 3 8 8 4 32 24 PATHS 12`, `... g_1_4_21.bin sub SEED NREP 20 3 8 10 4 32 24 PATHS 12`):

| cells | sampler, fresh seeds (replications) | sampler, all replications | brute force of the same chain (mine; mine and split-slab's pooled) | sampler - brute force |
|---|---|---|---|---|
| 48 | 9.916 +- 0.010 (128) | - | 9.9371 +- 0.0038; 9.9377 +- 0.0035 | **-0.021 +- 0.011** |
| 63 | 13.191 +- 0.020 (112) | 13.187 +- 0.018 (144) | 13.154 +- 0.011; 13.158 +- 0.010 | **+0.029 +- 0.021** |
| 84 tube | (split-slab's 32:) 17.311 +- 0.060 | - | 17.333 +- 0.057 | -0.02 +- 0.08 |

Chi-square of the three differences against zero: 5.6 on 3 (p = 0.13). No bias is established; one larger than
about 0.05 is excluded at 48 and 63 cells. The 48-cell difference is 1.9 sd; AGE48.
**Not tested: exactness at any size where the genealogy has collapsed** (96 cells and more). There the only
checks are split-slab's against gump's anchors (to 0.06-0.09 each), and the larger ensemble below.

## (c) The new numbers [measured, surrogate]

Fresh seeds 7201-7207 (120-cell tube: `WD=6 R/ss_diag G/g_1_18_40.bin sub SEED 8 44 3 8 20 4 32 24 PATHS 12`),
7301-7303 (wide 192: `... g_8_0_8.bin sub SEED 4 77 3 8 32 4 32 24 PATHS 12`), 7401-7402 (192-cell tube:
`... g_1_30_64.bin ...` same parameters). `python3 pool.py LABEL FILES`: ln tau from the mean rate, error from the
scatter, a bootstrap interval over replications, and the share of the summed rate carried by the largest one.

TABLE_C

READING_C

## (d) The shares of claim 4 [measured, surrogate]

`python3 shares.py A sub PATHS:SUBFILE ...` (my recount; split-slab's convention: largest one-generation fall among
the 16 generations before the death; per replication first). Two averages: the plain mean over replications
(split-slab's) and the **rate-weighted** mean, sum r_i s_i / sum r_i, which is the consistent estimate of the share
among natural deaths (a replication stands for r_i of the death rate; the plain mean is biased whenever rate and
share are correlated, and they are: last column).

TABLE_D

READING_D

## Not checked

- Blindness of split-slab's 96- and 108-cell tests (commit order); its sections 3, 4, 5 (splitting on gump, the
  bookkeeping forecast 24.59 +- 0.05); the 144-cell runs; version 1 of the sampler.
- The chain's offset from gump beyond 84 cells; exactness of the sampler beyond 84 cells; whether more sweeps
  or more chains change the 192-cell readings (only the 120-cell tube was run with a fourfold ensemble).
- What the "stuck" lives are inside (firewall or not), and how gump's anchors treat them at 48 cells.
- `ss.c`'s evaluation loop was not validated state for state by me, only through lifetimes; `ss_diag.c` adds
  counters to split-slab's code and changes no number (same seeds give the same REP lines).
