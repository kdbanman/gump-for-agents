# What a tube's living state carries (research/wraplocal)

2026-11-15. Question: which local property of the living state of a wrapped face with one short loop (a tube)
tracks its price per cell (loop² 12: 0.20437, 13: 0.20602, 16: 0.20717, 19: no clear effect, none: 0.20864; CLAIMS
WL3), and why the effect ends between loop² 19 and 21.

## Forecasts (written before any living-state statistic was measured)

The exact neighbourhood table (`nbhd.py`, section below) had been computed when these were written; no stepping had
been run.

- **F1 (60%).** Face-layer density on a loop² 12 tube differs from a no-short-loop torus of similar area by more than
  5 standard errors.
- **F2 (50%).** The face population's variance per cell, s = Var(N_face)/A, is larger on tubes, ordered 12 > 13 > 16 >
  19 ≥ none, and its relative excess is within a factor 2 of the relative price discount (2.0%, 1.3%, 0.7%).
- **F3 (35%).** One statistic, through a one-parameter relation fixed on loop² 12 and 16, forecasts loop² 13's
  price within twice its error (0.00066 per cell).
- **F4 (60%).** On a no-short-loop torus the connected equal-time correlation of a face cell with the cell one loop
  vector away, |C(w)|, falls in the order 12 > 13 > 16 > 19 > 21: the end of the effect is a correlation length, not
  an exact property of the neighbourhood.
- **F5 (70%).** A tube of loop² 9 lives on a line of its own whose price per cell is further below the open price
  than loop² 12's (more than 2.0% below).
