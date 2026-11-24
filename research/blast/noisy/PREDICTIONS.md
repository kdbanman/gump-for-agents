# Forecasts of research/blast/noisy (epsilon-noisy gump on the whole hull), frozen before the data

Same agent as `research/blast/split-hull` (second phase). Each block: UTC time, what was known, the forecasts with
probabilities; scores are added below each block when the data are in.

## Block 1: 11:33 UTC 2026-11-18, before any brute force of the noisy chain at 63 cells or more

Known: the stepper is gump at M = 0 (oracle, R = 11 and 15). Brute force at 45 cells (N has 9 cells there, all
six layers under the watched face and three under the opposite one): the watched face's ln tau is 9.816, 9.822,
9.821, 9.820, 9.821, 9.827 (+- 0.0044 each) at eps = 0, 0.016, 0.031, 0.094, 0.30, 1.0, so no offset to 0.01 even
with N all coins, while the eight-face value rises to 9.868 at eps = 1 (the other faces, noise three layers under
them, live longer). The sampler on the noisy chain at 63 cells, twelve replications per setting, scatters by 0.35
to 0.8 of the mean per replication (the dice chain: 0.22), acceptance 0.63 with 5 flips, 0.28 with 15.

Offset = ln tau of the watched face on the noisy chain (lives ended by the watched face, alone or tied, per
hull-generation with all eight alive) minus the same at eps = 0.

- 63 cells (N has 57 cells), eps = 0.30: offset +0.02, P(between -0.01 and +0.05) = 70%; P(positive) = 70%.
- 63 cells, eps = 0.10: P(|offset| < 0.02) = 75%. eps = 0.03 and 0.01: P(|offset| < 0.015 each) = 80%
  (the runs give +- 0.010, so this is nearly a statement that nothing will be seen).
- P(the offset at 63 cells is monotone in eps over 0.01, 0.03, 0.1, 0.3 beyond its errors) = 25%.
- The other seven faces at 63 cells: P(the eight-face value 8E/D at eps = 0.3 is above gump's 13.633 by more than
  0.03) = 65%.
- 84 cells (N has 168 cells), eps = 0.1: offset +0.03 +- 0.03; P(below +0.06, the dice chain's offset there) = 75%.
- The sampler against brute force at 63 cells, eps = 0.1, 100 replications or more: P(within two errors) = 80%.
- Scatter of one replication of the sampler at 63 cells: P(it is larger at eps = 0.03 than at eps = 0.1, at the
  setting I end up freezing) = 65%.

## Block 2: 12:27 UTC. The sampler's parameters frozen; forecasts for 84 cells (brute force), 108 cells (blind), 135 cells

**Frozen for every size** (`run_sub.sh`): N = depth >= 6 under the watched face and >= 3 under the others; darts on a
board of B >= 4|N| squares; LAM1 = round(P-bar - 2.5 sigma_P) = 18, 28, 38, 51, 65 for R = 11 ... 19; DELTA 3; NBATCH 8
(4,096 chains); **NSWEEP = round(0.6 A)** = 38, 50, 65, 81, 99; **KFLIP 15**; TPRE 32; TWIN 24; WBACK 12; runs of 10
replications, each run with its own 512 stationary lanes. eps values: **1/4, 1/16, 1/64** at every size
(M = B/4, B/16, B/64). Tuned on 63 cells (KFLIP 5/15/30/40/100, NSWEEP 10/20/40, eps 0.012 to 0.3) and on 84 cells
(24 replications each at eps 1/256, 1/64, 1/16, 7 at 1/4, with NSWEEP 50). One replication was made at R = 17 before
the freeze, for timing, with NSWEEP 45 at eps = 1/64 (it read 29.40); nothing else above 84 cells has been run.

Known now. Brute force, watched face minus gump: 45 cells: +0.006, +0.005, +0.004, +0.005, +0.011 (+- 0.006) at
eps = 1/64 ... 1; 63 cells: +0.010, +0.001, +0.032, -0.009 (+- 0.010) at eps = 0.012, 0.031, 0.10, 0.30 (the +0.032
is being repeated with another seed). The sampler at 63 cells with 40 sweeps: 13.629 +- 0.019 (eps 0.10), 13.647 +-
0.021 (0.031), 13.638 +- 0.037 (0.012); gump 13.633. The sampler at 84 cells (24 replications each): 18.218 +- 0.046
at eps = 1/16, 18.00 +- 0.11 at 1/64, 17.8 +- 0.4 at 1/256 (two replications carry half its rate), 18.24 +- 0.08 at
1/4 (7 replications); gump 18.141. Scatter of one replication at 84 cells: 0.20, 0.22, 0.53, 2.0 at eps = 1/4, 1/16,
1/64, 1/256.

Forecasts.
- **84 cells, brute force** (`prod_A_brute84.sh`): offset at eps = 1/16: +0.04 +- 0.04; P(above +0.03) = 50%; P(above
  +0.10) = 8%. At eps = 1/64: P(|offset| < 0.03) = 60%. (If the first is above +0.03 the PI's conjecture, that the
  dice chain's offset is all truncation, is in trouble: here nothing is truncated.)
- **84 cells, sampler at eps = 1/16, 200 replications (running)**: P(above gump by more than 0.03) = 60%; P(within two
  errors of the brute force of the same eps, when that exists) = 85%.
- **108 cells, blind** (`prod_B_108.sh`; gump 23.3392 +- 0.0099): P(the weighted mean over the three eps is within two
  of its errors of gump) = 55%; P(the line's intercept at eps = 0 is) = 75%; P(the intercept's error is 0.08 or
  less) = 45%; P(the eps = 1/16 value alone is above gump by more than 0.05) = 45%.
- **135 cells** (`prod_C_135.sh`): the intercept at eps = 0: **29.27 +- 0.08** is my forecast of what the method will
  say (my dip-rate forecast is 29.223 +- 0.014, the dice chain's readings 29.26 to 29.34). P(nearer 29.230 than
  29.163) = 75%; P(above 29.30) = 30%; P(the intercept's error after one round is 0.06 or less) = 25%.
- Efficiency: P(one replication at 135 cells and eps = 1/64 scatters by more than the mean) = 55%; P(at eps = 1/16,
  by more than 0.6 of the mean) = 50%.

### Amendment to block 2, 12:53 UTC, before any run above 84 cells

Timed at 84 cells, a replication costs 10, 21 and 55 s at eps = 1/64, 1/16, 1/4, and the part that grows is the
darts, in proportion to eps |N|: at 135 cells eps = 1/4 would cost about 600 s per replication. So **at 108 and 135
cells the three values are eps = 1/16, 1/32, 1/64**, not 1/4, 1/16, 1/64 (1/4 stays at 63 and 84 cells, where it is
cheap). The lever arm for the line in eps shrinks from 16 to 4; the forecasts of block 2 stand as written, with "the
three eps" meaning these. New since block 2: brute force at 63 cells, eps = 0.10 with a second seed, pooled +0.005 +-
0.007 (the +0.032 was a fluctuation), and eps = 1/16: +0.001 +- 0.010; the sampler at 84 cells and eps = 1/16 stands at
18.180 +- 0.037 after 63 replications (gump 18.141).

## Scores of block 1 (13:20 UTC)

- 63 cells, eps = 0.30, offset between -0.01 and +0.05 (70%): **yes** (-0.009 +- 0.010); positive (70%): **no**.
- eps = 0.10: |offset| < 0.02 (75%): **yes** (+0.005 +- 0.007, two seeds; the first alone read +0.032). eps = 0.03 and
  0.012: |offset| < 0.015 each (80%): **yes** (+0.001, +0.010).
- Monotone in eps beyond its errors (25%): **no**; there is no offset to be monotone (seven rows, mean +0.003 +- 0.004).
- The eight-face value at eps = 0.3 above gump by more than 0.03 (65%): **yes** (+0.061 +- 0.004).
- 84 cells by brute force: not run yet (stage A1).
- Sampler against brute force at 63 cells within two errors (80%): **yes** at the three frozen eps (+0.019 +- 0.018,
  +0.003 +- 0.018, -0.024 +- 0.023; 100 replications each).
- Scatter larger at eps = 0.03 than at 0.10 (65%): a tie in tuning (0.14 against 0.13 at 40 sweeps); with the frozen
  setting 0.21, 0.15, 0.13 at eps = 1/64, 1/16, 1/4: yes in direction.

## Scores of block 2 (16:39 UTC; written by the PI, the agent having finished, from `python3 research/blast/noisy/fit.py`)

- 84 cells by brute force (`prod_A_brute84.sh`): **not run** (the usage window closed first). Its three forecasts
  are not scored.
- 84 cells, sampler at eps = 1/16: 18.173 +- 0.029 after 100 replications (200 were planned), +0.032 +- 0.029 above
  gump. Above gump by more than 0.03 (60%): **yes, by 0.002, which is no evidence either way.** Within two errors of
  the brute force: not scored, there is no brute force.
- 108 cells, blind (gump 23.3392 +- 0.0099), final: 23.422 +- 0.025, 23.228 +- 0.119, 23.368 +- 0.065 at eps = 1/16,
  1/32, 1/64 (440, 300, 360 replications).
  - Weighted mean within two of its errors of gump (55%): **no** (+0.069 +- 0.025, 2.8 errors).
  - The line's intercept within two errors (75%): **yes** (-0.025 +- 0.083).
  - The intercept's error 0.08 or less (45%): **no**, narrowly (0.082).
  - The eps = 1/16 value alone above gump by more than 0.05 (45%): **yes** (+0.083 +- 0.027).
- 135 cells (`prod_C_135.sh`): **not run**, by the PI's decision: an intercept good to 0.08 at 108 cells cannot
  separate 29.230 from 29.163. The forecasts for it and the two on efficiency at 135 cells are not scored. At 108
  cells one replication scatters by 0.52, 2.06 and 1.23 of the mean at eps = 1/16, 1/32, 1/64.

## Block 3 (PI; frozen 17:58 UTC 2026-11-18, before the lead's rebuild has reported and before `diag.sh` has finished)

Seen when this was written: `tails.py` on the committed rows (at 108 cells the largest replication is 20, 35 and 7
times the mean at eps = 1/64, 1/32, 1/16; at 63 cells 1.4 to 2.0 times), and the ancestry lines of the first five
108-cell replications of `diag.sh` (about 50 distinct initial chains at the last level). Not seen: any brute force
of the chain above 63 cells; the odd-sweeps-off runs.

The claim [conjectured]: **the +0.083 +- 0.027 at 108 cells and eps = 1/16 is the sampler's, not the chain's**: an
unbiased estimate whose law has a rare heavy tail reads high in ln tau in most samples, and its error bar from the
scatter does not know about the part of the tail it has not caught. An argument from the night's numbers: the
dice chain, which replaces every deep cell every generation, was off by +0.024 and +0.060 at 63 and 84 cells by
brute force; a chain that replaces a sixteenth as often should be off by thousandths.

1. Brute force of the noisy chain at 84 cells and eps = 1/16 (anyone's code): within 0.015 of gump (18.141),
   given an error of 0.01 or less: **80%**. Above gump by more than 0.03: 7%.
2. Brute force at 84 cells at a large eps (0.25 to 1): above gump by 0.01 to 0.06: 60%; more than 0.06: 15%.
3. The sampler at 108 cells and eps = 1/16 with the odd sweeps off (WBACK 0), 300 or more replications: within two
   combined errors of the value with them on (23.422 +- 0.025): **75%**. Its scatter of one replication larger
   than 0.52: 70%.
4. In the full ancestry runs (30 replications at each eps, 108 cells): the median number of distinct initial
   chains at the last level is between 35 and 70 at every eps: 75%. The replication with the largest rate in
   each set has a largest-family share above the median's: 65%.
5. A sampler that also moves the initial states, or a longer run of this one (2,000 replications at eps = 1/16),
   brings the 108-cell value to within 0.03 of gump: 65% (not planned; written so that it can be scored).

### Scores of block 3, items 3 and 4 (19:37 UTC; `ana.py` and `anc.py` on `data/runs_diag/`)

3. Odd sweeps off at 108 cells and eps = 1/16, 420 replications: 23.330 +- 0.043. Within two combined errors of the
   value with them on (75%): **held, narrowly** (0.092 +- 0.050 below, 1.8 errors). Scatter above 0.52 (70%):
   **held** (0.88). What I did not forecast: with the odd sweeps off the value agrees with gump (-0.009 +- 0.044).
4. Median number of distinct initial chains at the last level between 35 and 70 at every eps (75%): **held** (47, 54,
   56). The replication with the largest rate has a largest-family share above the median's (65%): **held** at all
   three eps (0.40 against 0.22; 0.71 against 0.18; 0.32 against 0.15).
Items 1 and 2 wait for a brute force at 84 cells; item 5 is not planned yet.

### Block 3, items 1 and 2, as far as they can be scored (20:52 UTC)

1. Brute force at 84 cells and eps = 1/16: **not run by anyone** (the lead's rebuild ran eps = 1/4). Open.
2. Brute force at 84 cells at a large eps: the rebuild has +0.027 +- 0.038 at eps = 1/4 (725 deaths). In 0.01 to 0.06
   (60%): **held in value**, with an error as wide as the interval; it does not separate the alternatives.

### Block 3, item 1 again (22:16 UTC)

Still no brute force at 84 cells and eps = 1/16. The sampler, exact for the chain, has it at +0.002 +- 0.012 (odd
sweeps on, 1,050 replications) and +0.005 +- 0.011 (off, 1,040) from gump: within 0.015, as forecast, by another
route than the one the forecast named. Left open as written.

## Block 4 (PI; frozen 2026-11-19, 20:30 UTC, before anyone has run the density control)

The control (the lead's proposal): the depth series' d = 1 and d = 2 rows at 63 cells and eps = 1/4, with each coin
drawn at the replaced layer's own mean density in gump on the same hull instead of 1/2. Fair coins gave +0.670 and
+0.315 (pooled over two codes). Seen when this was written: the audit's layer densities on a wrapped slab (0.518,
0.434, 0.406 of a layer for the face and the two layers under it) and its remark that the layer under a nearly
empty hull face is fuller than under a wrapped one. Not seen: any run with biased coins.

My reading [conjectured]: most of the gain is the loss of correlation, not the density. At rate 1/4 the coins move
a layer's density by a quarter of the way from about 0.43 to 0.5, which is small; what they do that gump does not
is hand a fading face live cells beneath it at times when gump's own layer is fading with it.

1. At matched density the d = 1 gain is at least 0.40 (of the 0.67): **70%**. At most 0.15: 12%.
2. At matched density the d = 2 gain is at least 0.18 (of the 0.315): 65%.
3. Coins at a density well below the layer's own (a third of it) still lengthen the d = 1 life: 55%.
4. The sign never turns: no coin density between 0.2 and 0.8 at d = 1 shortens the watched face's life: 80%.


### Scores of block 4 (13:55 UTC 2026-11-24; from the `density` agent's rows, `research/blast/density/README.md`, commit 9a105d3; one code, not yet refereed)

| item | forecast | outcome | Brier |
|---|---|---|---|
| 1 | d = 1 gain at matched density ≥ 0.40: 70% (≤ 0.15: 12%) | +0.532 ± 0.011 (two seeds): **true** | 0.09 |
| 2 | d = 2 gain at matched density ≥ 0.18: 65% | +0.244 ± 0.013 (one seed): **true** | 0.12 |
| 3 | coins at a third of the layer's density still lengthen the d = 1 life: 55% | the scan gives −0.32 at 0.1 and +0.04 at 0.2, zero near 0.19; a third of 0.43 is 0.14: **false** | 0.30 |
| 4 | no coin density between 0.2 and 0.8 shortens the life: 80% | true as far as run: +0.04 at 0.2 (1.8 σ above zero), positive at 0.3 … 0.7, 0.8 not run: **provisionally true** | 0.04 |

What I had right: the gain is mostly the loss of correlation (0.53 of 0.68 survives at matched density). What I had
wrong: I thought any live support helps a fading face. It does not; below a density of about 0.19 independent coins
are worse for the face than gump's own layer, and coins that copy the layer's current state shorten the life.

## Block 5 (PI; frozen 13:55 UTC 2026-11-24, before any run at ε other than 1/4 with coins of density near 0.19, and before any run at 45 cells with biased coins)

The question: `density` found that at ε = 1/4, d = 1, 63 cells, coins of density p* ≈ 0.19 leave the life unchanged.
Is p* a property of gump's support (the same at every replacement rate and face size), so that a face of gump is a
face over independent coins of density p*? At ε = 1 the support is fresh coins every generation: the one-layer dice
picture on the hull.

My reading [conjectured]: no single density does it. The gain at matched density grows less than in proportion to ε
(+0.164 at 1/16, +0.532 at 1/4), and at full replacement all of the support's memory is gone, so a lower density
is needed to cancel a larger gain.

1. p*(ε = 1/16) is within 0.03 of p*(ε = 1/4), at 63 cells and d = 1: 60%.
2. p*(ε = 1) is below 0.17: 55%. It is within 0.04 of 0.19: 35%.
3. p* at 45 cells and ε = 1/4 is within 0.03 of the 63-cell value: 55%.
4. With ε = 1 and the p* that matches gump at 63 cells, the 45-cell life is within 0.15 of gump's in ln τ (one
   density gives the face law's slope as well as one point): 35%.

### Scores of block 5 (15:04 UTC 2026-11-24; from `density`'s second task, `research/blast/density/README.md`, commit b7f5904; one seed per row, one code)

| item | forecast | outcome | Brier |
|---|---|---|---|
| 1 | p*(1/16) within 0.03 of p*(1/4) at 63 cells: 60% | 0.173 ± 0.010 against 0.191 ± 0.003: **true** | 0.16 |
| 2a | p*(full replacement) below 0.17: 55% | 0.316 (coins under the face's middle), 0.385 (every cell not on a face): **false, and in the wrong direction** | 0.30 |
| 2b | p*(full replacement) within 0.04 of 0.19: 35% | **false** | 0.12 |
| 3 | p* at 45 cells within 0.03 of the 63-cell value at ε = 1/4: 55% | 0.180 ± 0.006 against 0.191 ± 0.003: **true** | 0.20 |
| 4 | with full replacement, the 63-cell p* gives the 45-cell life within 0.15: 35% | as I specified it (coins under the middle): +0.210 ± 0.007, **false**; with every cell not on a face a coin: +0.009 ± 0.007 | 0.12 |

What I had wrong: I reasoned that more replacement means a larger gain to cancel, hence a lower p*. The opposite
happens. At partial replacement most of the support is still made by gump's rule from the coins, and p* describes
that mix; with nothing but coins under it a face needs far denser coins (0.32 to 0.385) to live as long as it does
in gump, and below about 0.35 a hull on coins alone dies at once.

## Block 6 (PI; frozen 15:04 UTC 2026-11-24, before any of these runs)

Seen when written: `density`'s two hand-backs. In particular: with every cell not on a face replaced by a fresh
coin every generation, p = 0.385 gives gump's life at 45 and 63 cells (+0.009 ± 0.007, −0.028 ± 0.020), the 84-cell
row reads −0.28 ± 0.15 on 45 deaths, the face dies differently (dips rarer and deadlier), and gump's own layer
under the 63-cell face has density 0.384 when the face is at most 10 cells (its minimum over the thresholds tried).

1. Gump's layer 1 under the 45-cell face, conditioned on a low face, has a minimum over thresholds within 0.005 of
   0.385: 45%. (If p* on coins alone is the support's density at its thinnest, this should hold at every size.)
2. The 84-cell row at 0.385 with at least 300 deaths is below −0.10: 70%. (One density does not give the face
   law's slope; p* creeps up with the size.)
3. Full replacement from depth d with coins at each layer's own mean density, 63 cells: Δ(1) > +2: 75%;
   Δ(2) between +0.3 and +1.5: 55%; |Δ(3)| < 0.15: 45%; |Δ(4)| < 0.05: 45%.
4. At the smallest d with |Δ| < 0.1, the face's way of dying is gump's: from one cell it dies between 74% and 80%
   of the time, and dips below 16 cells are within 20% of gump's frequency: 60%.

### Scores of block 6 (17:03 UTC 2026-11-24; from `density`'s third task, `research/blast/density/README.md`, commit 2d67675; one code, not yet refereed)

| item | forecast | outcome | Brier |
|---|---|---|---|
| 1 | the 45-cell layer's minimum under a low face within 0.005 of 0.385: 45% | the core's lowest is 0.390, the cells the coins actually replace thin to 0.357: **false** (the coincidence is an accident) | 0.20 |
| 2 | the 84-cell row at 0.385 below −0.10: 70% | −0.165 ± 0.043 on 559 deaths: **true** | 0.09 |
| 3a | Δ(1) > +2 at 63 cells: 75% | under the watched face +1.186 ± 0.037: **false** (true only with coins under every face, +3.53) | 0.56 |
| 3b | Δ(2) in (+0.3, +1.5): 55% | +0.694 ± 0.029: **true** | 0.20 |
| 3c | \|Δ(3)\| < 0.15: 45% | +0.295 ± 0.023: **false** | 0.20 |
| 3d | \|Δ(4)\| < 0.05: 45% | +0.016 ± 0.012 (two seeds): **true** | 0.30 |
| 4 | at the first d that matches, the way of dying is gump's: 60% | d = 4: death from one cell 0.765–0.776 (gump 0.770), dips within 0.005 in the logarithm: **true** | 0.16 |

What I had wrong: I expected the face alone over a bath at gump's density to live more than e² longer; under the
watched face only it is e^1.19, because the rims keep their real layers. What I did not expect to be so clean: the
step from three real layers to four removes all of the excess that can be measured, at both sizes and on both kinds
of face.
