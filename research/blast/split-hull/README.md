# research/blast/split-hull: a rare-event sampler for the faces of gump's octahedral hull

Agent `split-hull`, blast of 2026-11-18. Work in progress; this file is rewritten at every commit.

## State (03:52 UTC)

- **Stepper validated [measured]:** `python3 research/blast/split-hull/validate.py 1200` compares `sh.c`'s bit-sliced
  hull stepper with `reference/oracle.py` cell for cell at R = 11 and R = 15 (3 soups, 1,200 generations each), with
  the face population counter, the emptiness bits of the other seven faces, the per-cell age counters, the frozen
  lanes and the packed-configuration round trip; the negative control (one neighbour swapped) fails at generation
  5 and 3. Output: `VALIDATION PASSED`. (Run before the ring of lagged states was added; rerun below.)
- Sampler: forward-flux sampling on the population of one face; being calibrated on R = 9 and 11.
- Forecasts: `PREDICTIONS.md` block 1.
