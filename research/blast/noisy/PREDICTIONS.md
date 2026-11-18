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
