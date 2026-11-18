# Forecasts of agent split-slab, frozen before the data

## Block 1: 2026-11-18 03:50 UTC, before any run of mine on the 120-cell tube (1,18),(0,40)

Known to me: the anchors of BRIEF-COMMON.md, the PI's update of 03:32 UTC ((1,17),(0,32) 19.7446 ± 0.0042;
(1,16),(0,36) 22.1599 ± 0.0086), my own runs on 48 and 63 cells. Not known: anything measured on the 120-cell tube.

**Prior (no measurement of mine at 120 cells; plain extrapolation of the tube's local slope 0.20226 (84 to 96),
0.20128 (96 to 108), next 0.2008 ± 0.003):**

    ln tau_face, torus (1,18),(0,40), 120 cells = 24.57 ± 0.04      P(truth within the error) = 60%

**Procedure for the measured forecast (fixed now, before the 120-cell run):** the multilevel-splitting sampler does
not beat brute force on gump (README, "Why splitting fails"), so the number of record will come from the exact
bookkeeping 1/tau = nu(p) q(p): nu_A(p) = rate per face-generation of excursions (first passage to <= LAM0 after
>= PA, until the return to >= PA) whose minimum population is <= p, measured by a plain run at each size with
PA = round(0.515 A - s), LAM0 = round(0.515 A - 3 s), s = sqrt(0.415 A); ln q_A(p) = -ln tau_A - ln nu_A(p) from the
anchors at 84, 96, 108 cells (loop^2 12 tubes); ln q_120(p) by the straight line in A through those three;
ln tau_120 = -ln nu_120(p) - ln q_120(p), at the deepest level p with at least 400 excursions at 120 cells, and at
two shallower levels as a check. The same procedure is first run blind on a known case: the 108-cell tube from
78, 84, 96 cells. P(the procedure's 108-cell value lands within 0.04 of 22.1599) = 65%.
P(the 120-cell value so obtained lands within 0.05 of the GPU's) = 55%.

(Block 1 was committed at 03:46 UTC by the machine clock, e9fc172; its heading says 03:50.)

### Block 1, scored on its blind test (04:00 UTC)

The bookkeeping procedure, run on the known 108-cell tube from the anchors at 78, 84 and 96 cells
(`python3 nuq.py data/plain_1_16_36_s101.txt data/plain_1_6_26_s101.txt:16.0932:0.0093 data/plain_1_12_28_s101.txt:17.3175:0.0031 data/plain_1_17_32_s101.txt:19.7446:0.0042`):
level of record p = 14 (430 excursions): **22.171 ± 0.057** against the anchor 22.1599 ± 0.0086: +0.011. Inside
0.04: the forecast held. Shallower levels (p = 18 to 23, statistical error 0.011 to 0.023) come out +0.04 to +0.06
high: ln q is slightly concave in A there, so the rule "deepest level with 400 excursions" matters.

## Block 2: 04:00 UTC, before any run of the subset sampler at 84 cells or more

A second sampler now exists (`ss ... sub`, README section 5): subset simulation on the *dice chain* (6 layers on
the rule over 2 layers of fair coins, one face), exact for that Markov chain; it has been run only once, on 48
cells (8 replications, 9.883 ± 0.053; dice chain by brute force 9.918 ± 0.027; gump 9.9251).

Procedure, fixed now: WD = 6; mu = 0.515 A, s = sqrt(0.415 A); LAM1 = round(mu - 2.5 s), DELTA = 3, 4096 chains
(NBATCH 8), NSWEEP = round(A / 6), KFLIP = 4, TPRE = 32, TWIN = 24; error from independent replications.
Tuning tori: 48 and 63 cells (there the dice chain is also measured by brute force). Then, without further tuning:
63, 84 (1,12),(0,28), 96 (1,17),(0,32), 108 (1,16),(0,36) against the gump anchors; the offset
d = ln tau(dice chain) - ln tau(gump) is whatever these give. The 120-cell value of record is
ln tau(dice chain, 120) - d, with d the mean offset at 84, 96, 108.

Forecasts:
- P(|d| < 0.05 at each of 84, 96, 108, within 2 of my standard errors) = 55%. P(d shows a trend with size larger
  than 0.05 from 84 to 108) = 30%.
- The sampler's 120-cell value: 24.57 ± 0.06 (my prior of block 1 widened by the sampler's own error);
  P(within) = 55%.
- Loop^2 12 tubes beyond: local slope between 120 and 240 cells stays in 0.196 to 0.202 per cell (P = 60%), i.e.
  ln tau(144) = 29.38 ± 0.10, ln tau(192) = 38.9 ± 0.3, ln tau(240) = 48.5 ± 0.5. P(the slope falls below 0.190
  somewhere before 240 cells) = 20%; P(it returns above 0.205) = 10%.
- P(the dying paths at 108 and 120 cells still pass through an over-full generation and a one-generation crash in
  more than half of the deaths) = 70%.

## Block 3: 04:04 UTC. THE 120-CELL TUBE (1,18),(0,40): forecast of record from exact bookkeeping

Nobody's measurement of the 120-cell lifetime exists yet (GPU value expected about 13:00 UTC). Mine is not a
lifetime measurement either: no face died in my 120-cell run (5.5e9 face-generations). It is
ln tau = -ln nu_120(p) - ln q_120(p) with nu_120(p) **measured** (508 excursions to <= 18 cells) and q_120(p)
**continued** from the anchors at 84, 96, 108 cells.

- Frozen procedure of block 1 (straight line in A, deepest level with 400 excursions, p = 18):
  **24.636 ± 0.052** (statistical). `python3 nuq.py data/plain_1_18_40_s101.txt data/plain_1_12_28_s101.txt:17.3175:0.0031 data/plain_1_17_32_s101.txt:19.7446:0.0042 data/plain_1_16_36_s101.txt:22.1599:0.0086`
  Levels p = 16 to 26 give 24.62 to 24.67.
- Known weakness, found on the 108-cell test after block 1 was written: ln q_A(p) is convex in A (the middle
  anchor lies 0.02 ± 0.01 below the chord), and the straight line then overshoots: +0.011 at the test's level of
  record but +0.04 to +0.06 at its shallower levels, which are the ones comparable to p = 18 here
  (ln q about -8.4). The parabola through the three anchors (`nuq_quad.py`, written after the test; on the 108-cell
  test it gives 22.12 to 22.18 at every level, truth 22.160) says 24.562 ± 0.078 at p = 18 and 24.556 ± 0.031 at
  p = 22 to 26.

**Forecast of record: ln tau_face(120-cell tube) = 24.59 ± 0.05.** P(the GPU's value within ± 0.05) = 60%;
P(below 24.64) = 80%; P(below 24.54) = 15%. It rests on: my stepper (bit-exact against the oracle on this torus),
the excursion bookkeeping (it reproduces the anchors at 48, 63, 78 and 84 cells by brute force), the three tube
anchors, and the assumption that ln q_A(18) continues smoothly from 84-108 to 120 cells (it moves by -0.017 to
-0.024 per cell there, about a tenth of the whole slope: nine tenths of the step from 108 to 120 cells is measured).
It implies a local slope from 108 to 120 cells of 0.2025 ± 0.004 per cell: not falling further.

### Block 2b: 04:10 UTC. The sampler was changed after its first runs at 63 and 84 cells (said plainly)

Version 1 (block 2's parameters, proposals uniform in space-time) ran at 48, 63, 84 cells and two replications at
96: 9.920 ± 0.021, 13.227 ± 0.080, 17.381 ± 0.122 (gump anchors 9.9251, 13.1622, 17.3175). Its level counts
scatter by 20-30% between replications at the last four levels (the fade after the crash), so its error is too
large to calibrate anything. Version 2 adds, on every second sweep, proposals confined to the 12 generations of
dice before the chain's minimum (a Metropolis-Hastings move, rejected unless the reverse move is proposable);
everything else as in block 2. Tested on 63 and 84 cells only: 13.129 ± 0.063 and 17.228 ± 0.098. So **84 cells
is now a tuning torus; the blind calibration tori are 96 and 108 cells**, run next without further change,
then 120, 144, 192 (tube and the wide torus (8,0),(0,8)), 240. Block 2's forecasts stand unchanged.
The v1 outputs are kept in `data/v1/`.

## Block 4: 04:40 UTC. Scores, and the sampler's 120-cell number

Block 2 (subset sampler on the dice chain), scored on `python3 table_sub.py`:
- "|d| < 0.05 at each of 84, 96, 108 within 2 standard errors" (55%): **held**, weakly: -0.007 ± 0.060,
  +0.087 ± 0.067, +0.018 ± 0.061 (and -0.005 ± 0.088 on the equilateral 108-cell torus, not in the forecast).
  "A trend larger than 0.05 from 84 to 108" (30%): not seen (+0.025 ± 0.085), not excluded either.
- "The sampler's 120-cell value 24.57 ± 0.06" (55%): the sampler gives 24.710 ± 0.078 for the dice chain,
  **24.68 ± 0.09** after the offset. 0.11 from my forecast: **missed** by the forecast's own error, 1.2 of the
  measurement's.
- Tubes beyond: 144 cells forecast 29.38 ± 0.10, sampler 29.44 ± 0.22: held. 192 cells forecast 38.9 ± 0.3,
  sampler 38.62 ± 0.25: held, at the edge. 240 cells: not run. "Slope stays in 0.196 to 0.202 between 120 and 240"
  (60%): 0.193 ± 0.004 from 120 to 192 cells, so **just below my range**; "falls below 0.190 somewhere" (20%):
  144 to 192 reads 0.191 ± 0.007, undecided; "returns above 0.205" (10%): no.
- "Dying paths at 108 and 120 cells still pass through an over-full generation and a one-generation crash in more
  than half of the deaths" (70%): by the A/2 criterion 0.50 ± 0.04 at 108 cells and 0.38 ± 0.03 at 120:
  **failed at 120 cells** (by the 0.4 A criterion 0.72 and 0.65). I did not expect the tube to leave the route.

The 120-cell tube, two independent numbers of mine, both before the GPU's:
- bookkeeping (block 3, the forecast of record, commit 2398569): 24.59 ± 0.05;
- subset sampler on the dice chain, offset from the tube anchors at 84, 96, 108: 24.68 ± 0.09.
They differ by 0.09 ± 0.10. Weighted together: 24.61 ± 0.045. The forecast of record stays 24.59 ± 0.05 as
committed; if the GPU's value lands above 24.64 the sampler was the better of the two.

New forecast, for whoever runs it (no data of mine or anyone's): the wide 192-cell torus (8,0),(0,8) of gump
itself. The wide line says 40.08; my sampler says 40.72 ± 0.26 on the dice chain. P(gump's value is above 40.30)
= 45%: I do not know whether the wide price rises or my sampler drifts.

Added 04:43 UTC, after one more run (the wide 144-cell torus (4,4),(0,12), 14 replications: 29.74 ± 0.24 against
the wide line's 30.06): the sampler's errors at 144 and 192 cells are too small by up to a factor 2 (wide tori
-0.33 at 144, +0.64 at 192 against the line). Block 4's scores for 144 and 192 cells ("held") therefore mean
little, and my 45% for the wide 192-cell torus above 40.30 goes down to 30%.
