# Where the face-law exponent comes from

*Exponent agent, 2026-11-13. PROGRAM nodes M1–M4, E2; OPEN-PROBLEMS items 3–4. Tags: **[proved]** argument in
`exponent/theorems.md`; **[measured]** with n, error and command; **[conjecture]**. Commands run from
`research/theory/exponent/`; bulk output is in `research/scratch/exponent/` (git-ignored), curated numbers in
`exponent/data/`, forecasts and their scores in `exponent/PREDICTIONS.md` (append-only, committed before the runs).
"Toy" = B34/S234 on the range-2 cross (`research/toy2d`); an edge of L cells, periodic. "Truth" for the toy =
deterministic strips 16 × L measured here (they agree with toy2d where both exist); for gump = `research/fluct`.*

PENDING-VERDICT

## 1. Tools

- `drv.c` + `xp.py` — bit-sliced replicas (256 per run) of an outer-totalistic rule on an arbitrary **directed**
  cell graph whose cells are *dynamic*, *noise* (i.i.d. Bernoulli, redrawn every generation) or dead; optional death
  noise ε; quasi-stationary sampling with restarts; censoring of settled states (period ≤ 2 every generation,
  snapshots at 64 / 4096 / 262144), of strips cut by three dead columns and of interior firewalls; histogram and
  one-step transitions of the boundary population, empty-window statistics, the last 64 generations before every
  death. **[measured] validation** (`python3 validate.py` → ALL OK): bit-exact against a numpy stepper for 300
  generations (two vessels); toy L = 12, 16: τ = 284 ± 4, 1651 ± 18 (toy2d: 286, 1679 ± 26); gump hull R = 9:
  first-peel mean 2306 ± 36 (fluct: 2300 ± 6); the noise path against the exact solution of §4 (ln τ = 4.390 ± 0.018,
  6.418 ± 0.010, 8.622 ± 0.012 simulated against 4.3999, 6.4168, 8.6348 exact at L = 8, 12, 16).
- `exact1d.c` — the one-row model solved exactly (power iteration on the killed kernel, 2^L states, L ≤ 22).
- `fg.c` — the exact functional graph of the toy on every state of a small vessel (N ≤ 32); `fg_check.py` → ALL OK
  against direct enumeration for five vessels with N ≤ 18.
- `regrow.py`, `clone_corr.py`, `sync_check.py`, `mfld.py`, `game_check.py` — single experiments, described where used.
- `jobs.py` (run lists), `report.py` (every table below), `figures.py`.

PENDING-BODY
