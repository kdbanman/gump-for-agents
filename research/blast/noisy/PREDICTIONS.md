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
