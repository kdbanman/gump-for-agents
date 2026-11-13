# Predictions from the swarm (append-only)

Each entry: date, who, the experiment, the predicted number with an error bar, the reasoning in two lines.
Written before the experiment is run.

## 2026-11-13, path, E1 and E2 (filed at the end of round 1, before any reply from the critic)

**E1. A notch gives the ring ends.** Toy rule (B34/S234, cross2), periodic strips 16 × L run exactly as in
`research/toy2d/law.py` (soups p = 0.4, T0 = 300, cut replicas censored), except that two adjacent cells of row 0
(columns 0 and 1) are removed from the vessel, i.e. dead for ever. Row 15 is left intact as the control.
L = 20, 24, 28, 32; τ_notch(L) = exposure / deaths of row 0.
*Prediction:* the slope of ln τ_notch between L = 20 and L = 32 is **0.345 ± 0.020**, i.e.
ln τ_notch(32) − ln τ_notch(20) = 4.14 ± 0.24, against 5.00 (slope 0.416) for an intact row. No prediction for the
intercept.
*Why (two lines):* a dead stretch of an edge is refilled only from its ends, and next to a cell that can never
live only from one end (path journal, Lemma 1). Every measured edge that has such an anchoring point (box corner,
mirror point) costs 0.34–0.35 per independent cell with a straight law; only the ring, which has none, shows
0.44 falling to 0.38, and its empty-window statistics extrapolate to 0.345 times a power of the length (journal 5.2).
*Refuted if* the notched slope is ≥ 0.39.

**E2. The remnant.** Same rule, intact strips 16 × L. The mean edge population two generations before the
edge's death is **9.8 ± 1.0 cells at L = 32 and at L = 36** (densities 0.31 and 0.27; at L = 36 below half the living
mean 0.577).
*Why:* at L = 12…24 the published densities 0.61, 0.55, 0.46, 0.39 are the counts 7.3, 8.8, 9.2, 9.4: what is
size-independent is the final collapse of a remnant of about ten cells, not a flash from ordinary density
(journal 5.1). *Refuted if* the count is ≥ 11.5 at L = 36 (a density that stops falling near 0.32 or more).
