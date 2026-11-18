# Rimmed hull faces dying, watched (research/dying2/hull)

2026-11-18. The rimmed half of the dying2 study (the wrapped faces and tubes are in the rest of `research/dying2/`,
another agent's). Vessel: the hull octahedron of `research/gpu/facelaw.py` (soup 0.35 in |p|_1 <= R, exact hull,
8 faces, deaths at age > T0 = 200), R = 11 (faces of 63 cells) and R = 13 (84 cells). Definitions are those of
`research/dying/README.md` (rounds 1-2) and are restated in `PREDICTIONS.md`, which holds the forecasts, committed
(a47fa31) before any production run. Tags: **[measured]** (number, error, command), **[conjectured]**.

**Status (03:40 UTC): R = 11 done and tabled below; R = 13 running (until about 05:05 UTC, then a second seed set). Figure: `hull_dying.svg` (`figure.py`).**

## Short answer (R = 11, A = 63)

- **[measured] A dying hull face is at its stationary population until about 16-20 generations before it is empty,
  then collapses in a median of 7 generations from half its mean; the last generation holds 1.62 live cells.**
  P/P bar = 0.955, 0.676, 0.314, 0.052 at lags 16, 8, 4, 1 (round 1, c1, another recorder and soup 0.4: 0.95,
  0.67, 0.31, 1.61 cells: **agreement**). Quantiles in `data/R11_death_timecourse.csv`.
- **[measured] Point of no return: 2 live cells.** q(k), the chance that a dip from above P bar that reaches k or
  fewer cells ends in death: 0.769 (k = 1), 0.499 (2), 0.298 (3), 0.180 (4), 0.064 (6), 0.014 (9), 0.0032 (12).
  k* = 2.00 = 0.064 P bar (round 2: q(0.1 P bar) = 0.300, p* = 0.079 P bar with the strict "< p P bar" level, which
  is the same point on the integer grid: **agreement**). ln nu(0.9 P bar) = -2.311 (round 2: -2.31).
- **[measured] Dips that recover and dips that die look the same on the way down.** Aligned at the first generation
  with P <= k, the mean population before it is the same for both (k = 3: 27.5 / 27.6 at -8, 19.4 / 18.8 at -4,
  10.7 / 9.5 at -2), and the descent from the last P >= U takes the same time (median 7, IQR 5-10, both). Where
  they part is after the passage: recovering dips are back to half P bar in about 8-16 generations.
- **[measured] Where the last cells sit: on the rim, not in the corners and not in the interior.** Share of the
  lag-1 live cells over the share of stationary live cells: rim row (the row shared with the neighbour face) 1.10,
  row 1 1.01, row 2 0.84, rows >= 3 0.79; within one cube unit of a corner 0.91, 1-2 units 1.17, 2-3 units 1.04,
  farther 0.92. Stationary faces thinned at random give 1.00 +- 0.02 everywhere (the control is geometry only).
- **[measured] And survivors on the rim are the ones that die.** At the first passage of a dip to exactly k cells,
  q rises with the number of those k cells in the rim row: k = 4: 0.061 +- 0.021 (none on the rim), 0.080, 0.101,
  0.130, 0.145 +- 0.027 (all four); k = 6: 0.006, 0.019, 0.022, 0.028, 0.041, 0.043, 0.059. Spread-out survivors
  die more than clumped ones (k = 3: 0.243 against 0.155 either side of the median pair distance 1.73). Survivors
  near corners: a weak, non-monotone effect (k = 4: 0.087, 0.120, 0.142, 0.100 for 0, 1, 2, 3 survivors within 1.5
  units). So the excess of rim cells among the last survivors is the rim's own poor prospects, not rims holding out:
  a remnant in the interior comes back more often.
- **[measured] Neighbours:** the three edge neighbours fall to 0.772 of P bar at the moment of death (their shared
  rim row is the dying face's own), the three vertex neighbours to 0.960, the opposite face stays at 0.999. Which
  face dies: uniform (5,258-5,418 per face of 42,494; chi2 5.9 on 7); one co-death.
- Calibration: ln tau_face = ln(8E/F) = **13.6429 +- 0.0049** (42,494 face deaths), GPU 13.636 (+1.4 sigma); P bar =
  31.253 (round 1 review 31.25).

## What was measured, and what each number rests on

- **Recorder `hd.c`**: research/gpu-local/cpu/fr.c's bit-sliced stepper (256 lanes per thread, AVX2), copied, on the
  hull's neighbour table (`hullvessel.py`, built with fl.Vessel as hullface.py does, numpy only). Events every
  generation: a face empty (kind 1), period 1-2 (kind 2), cycles caught by snapshots (kind 3; none occurred at
  R = 11). Per lane: a ring of the 8 face populations (4,096 generations) and of the 366 face-layer cells (1,024),
  dumped at the first 1,500 deaths per thread (4,500 in all, lags to 4,095) and at the first 300 recovered dips per
  minimum value 1..12 per thread (900 per value: 1,024 generations of populations, 256 of states). Null: every
  lane at age > 2,000 every 9,973 generations (90,000 face-states x 8 faces). Excursions follow round 2 exactly, with
  U = 32 (P >= 32 is "above P bar = 31.25").
- **Stepper = engine, every generation** (`validate.py 11 3000 7`, `validate.py 13 3000 8`): 5 lanes (0, 63, 64,
  130, 255) of hd.c's own soups, 3,000 generations, against `gump run --cells` in open space: all equal at both
  sizes; the face counter equals numpy on all 256 lanes x 8 faces x 3,000 generations. Negative controls: the engine
  one generation later differs in 2,999 of 2,999 generations; one flipped face node differs in 3,000 of 3,000.
  Log: `data/validate.log`.
- **Every dump is checked as it is read** (`analyze.py`): ring populations equal popcounts of the stored states (first
  300 deaths and dips); the named face is empty at the last generation and not one before (all 4,500); a recovered
  dip ends at P >= U with its minimum where the header says and nothing lower in the excursion (all).
- **End to end**: ln tau_face from the lives file against the GPU's value (above); dead excursions 42,489 against
  42,494 face deaths (the 5 are deaths at age 201 and the co-death).

Commands (from the repository root, P = C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe):

    P research/dying2/hull/hullvessel.py 11; P research/dying2/hull/hullvessel.py 13     # vessels
    P -u research/dying2/hull/validate.py 11 3000 7                                     # VALIDATE OK
    bash research/dying2/hull/run.sh 11 0.1667 1100       # 10 min, 3 threads: 4.5e9 replica-generations
    P -u research/dying2/hull/analyze.py 11 run_11_s1100  # ~1 min -> data/R11_*.csv, data/R11_analyze_out.txt
    P -u research/dying2/hull/condq.py 11 run_11_s1100    # ~20 s  -> data/R11_condq.csv, data/R11_condq_out.txt

(The R = 11 production ran an earlier build, `hd.exe`, that wrote excursion lines down to minimum 12 instead of 4;
nothing else differs, and no table uses those lines.)

## Tables (`data/`)

`R{R}_death_timecourse.csv` (dying face by lag: mean, 5/25/50/75/95%, neighbours), `R{R}_excursions.csv` (nu, q by
k), `R{R}_equal_depth.csv` (dying vs recovering aligned at first P <= k), `R{R}_positions.csv` (row and corner
shares over stationary, pair distance), `R{R}_cells.csv` (per canonical cell: row, corner distance, stationary
occupancy, occupancy at lag 1), `R{R}_condq.csv` (q at first passage to exactly k, by where the survivors sit).

## Not checked

- No second code for the dying statistics (one recorder; its stepper is engine-checked on 5 lanes x 3,000
  generations per size, its counter on all lanes).
- The null samples are not conditioned on the face living on afterwards (round 1 showed < 0.01 effect in c1).
- q by class uses weights from the hist files for the capped recovered dumps; its errors (effective-count
  binomial) are approximate.
