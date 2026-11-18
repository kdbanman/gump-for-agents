# Rimmed hull faces dying, watched (research/dying2/hull)

2026-11-18. The rimmed half of the dying2 study (the wrapped faces and tubes are in the rest of `research/dying2/`,
another agent's). Vessel: the hull octahedron of `research/gpu/facelaw.py` (soup 0.35 in |p|_1 <= R, exact hull,
8 faces, deaths at age > T0 = 200), R = 11 (faces of 63 cells) and R = 13 (84 cells). Definitions are those of
`research/dying/README.md` (rounds 1-2), restated in `PREDICTIONS.md`, which holds the forecasts, committed
(a47fa31) before any production run. Tags: **[measured]** (number, error, command), **[conjectured]**.
Figure: `hull_dying.svg` (`figure.py`). Numbers below: R = 11 from seeds 1100-1102 (10 minutes); R = 13 from seeds 1300-1302 and 1310-1312 pooled
(100 + 105 minutes).

**STATUS (07:00 UTC): complete; nothing running.**

## Short answer

| | A = 63 (R = 11) | A = 84 (R = 13) |
|---|---|---|
| face deaths recorded (lives) / dumped with history | 42,494 / 4,500 | 8,891 / 8,705 |
| ln tau_face = ln(8E/F), T0 = 200 (GPU value) | 13.6429 +- 0.0049 (13.636) | 18.151 +- 0.011 (18.141) |
| P bar, sigma_P (face-generations at age > T0) | 31.253, 5.24 | 42.448, 5.96 |
| P / P bar at lags 32, 16, 8, 4, 2, 1 | 0.998, 0.955, 0.676, 0.314, 0.114, 0.052 | 0.999, 0.951, 0.611, 0.233, 0.081, 0.038 |
| live cells at lag 1: mean (5%, median, 95%) | 1.62 (1, 1, 4) | 1.61 (1, 1, 4) |
| plunge, last P >= P bar/2 to empty: median (IQR, 5-95%) | 7 (5-9, 3-14) | 8 (6-10, 4-15) |
| final excursion, last P >= U to empty: median (IQR) | 10 (7-14) | 11 (8-14) |
| q(k), death after a dip reaching <= k: k = 1, 2, 3, 4, 6, 9 | 0.769, 0.499, 0.298, 0.180, 0.064, 0.0139 (errors 0.0018 ... 0.0001) | 0.770, 0.496, 0.296, 0.176, 0.060, 0.0122 (0.0039 ... 0.0001) |
| point of no return k* (q = 1/2) | 2.00 cells (0.064 P bar) | 1.98 cells (0.047 P bar) |
| ln nu(min <= 3) per face-generation | -12.43 | -16.93 |
| edge / vertex / opposite neighbours at death, over P bar | 0.772 / 0.960 / 0.999 | 0.806 / 0.970 / 0.999 |
| last live cells (lag 1) over stationary share: rim row, row 1, row 2, rows >= 3 | 1.10, 1.01, 0.84, 0.79 | 1.12, 1.06, 0.83, 0.79 |
| same, by corner distance < 1, 1-2, 2-3, >= 3 cube units | 0.91, 1.17, 1.04, 0.92 | 0.92, 1.22, 1.10, 0.92 |
| which face dies: chi2 against uniform (7 dof); co-deaths | 5.9; 1 | 7.7; 0 |

In words:

- **[measured] The decision is made in the last two or three cells, and it hardly depends on the size of the
  face.** Once a dip from above P bar has reached k live cells, the chance it ends in death is the same at 63 and
  84 cells within errors for k <= 3 (0.769 / 0.770, 0.499 / 0.496, 0.298 / 0.296) and 2-12% lower on the larger
  face for k = 4-9 (0.064 / 0.060 at k = 6, 5 sigma; 0.0139 / 0.0122 at k = 9). A face that reaches two cells dies
  half the time; at three, 30%; at six, 6%. So of the 4.51 nats between the two lifetimes, at most 0.13 (ln q(9)
  ratio) is in the last nine cells; the rest is in how often a dip gets down there (ln nu(min <= 3): -12.43
  against -16.93). In units of P bar the point of no return moves
  down (0.064 to 0.047): it is a number of cells, not a fraction.
- **[measured] On average a death is a whole-face collapse of about 16 generations, the same at both sizes and one
  generation slower at 84 cells.** Before lag ~20 the dying face is at its stationary population (and the 4,000
  generations before that are flat at 1.00 +- 0.01: no slow run-up). Round 1 (c1, another recorder, soup 0.4) gave
  0.95, 0.67, 0.31 at lags 16, 8, 4 and 1.61 cells at lag 1 at A = 63: **agreement** to 0.01.
- **[measured] Dips that die and dips that recover look identical on the way down.** Aligned at the first
  generation with P <= k, the mean population before it agrees within about 1 cell at every offset (k = 3, A = 63:
  27.5 / 27.6 at -8, 19.4 / 18.8 at -4, 10.7 / 9.5 at -2), and the descent from the last P >= U takes the same time
  (median 7 at A = 63, 8 at A = 84, both kinds; `data/R*_equal_depth.csv`). They part only after the passage:
  recovering dips are back to half P bar about 8 (A = 63) to 10 (A = 84) generations after it.
- **[measured] Where the last cells sit: by the rim, next to (not in) the corners, away from the interior.** The
  rim row (shared with the edge neighbour) holds 1.10-1.14 of its stationary share of the last live cells, rows 2
  and deeper 0.76-0.84. The three corner cells themselves (stationary occupancy 0.26) are slightly under-represented
  (0.91-0.93), the cells one to two units from a corner over-represented (1.17-1.24). A stationary face thinned at
  random gives 1.00 +- 0.03 everywhere, so this is not geometry. Per-cell maps: figure panels D, E.
- **[measured] And survivors on the rim and spread-out survivors are the ones that die.** q at the first passage of
  a dip to exactly k cells, by how many of the k sit in the rim row (`data/R*_condq.csv`):

  | k | A | 0 on rim | 1 | 2 | 3 | 4 | 5 | 6 |
  |---|---|---|---|---|---|---|---|---|
  | 4 | 63 | 0.061 +- 0.021 | 0.080 | 0.101 | 0.130 | 0.145 +- 0.027 | | |
  | 4 | 84 | 0.061 +- 0.013 | 0.089 | 0.105 | 0.111 | 0.130 +- 0.021 | | |
  | 6 | 63 | 0.006 +- 0.013 | 0.019 | 0.022 | 0.028 | 0.041 | 0.043 | 0.059 +- 0.040 |
  | 6 | 84 | 0.011 +- 0.010 | 0.017 | 0.024 | 0.028 | 0.036 | 0.044 | 0.066 +- 0.042 |

  Spread matters more: survivors more spread than the median pair distance die 1.3-1.7 times as often (k = 3:
  0.243 against 0.155 at A = 63, 0.247 against 0.149 at A = 84). The rim effect is partly the spread (rim cells lie
  along three edges) but not wholly: among clumped remnants, those with more than half their cells on the rim die
  about 1.5-2 times as often (k = 6: 0.038 against 0.020 at both sizes; k = 4: 0.112 against 0.074 at A = 63,
  0.095 against 0.073 at A = 84); among spread remnants the rim adds less and at k = 3 (A = 84) nothing.
  Survivors near corners: a weak, non-monotone effect. So the excess of rim cells among the last survivors is the
  rim's poorer prospects, not the rim holding out; a remnant that keeps a clump in the interior comes back.
- **[measured] Neighbours:** the three edge neighbours lose 19-23% by the moment of death, mostly in the shared rim
  row (which is the dying face's own; round 1 measured this split at A = 63), the vertex neighbours 3-4%, the
  opposite face nothing. They start to fall about 16 generations before death, with the dying face.

**[conjectured] For the theory session.** The rimmed-face price (0.231 per cell against 0.209 wrapped) cannot be
in the endgame, which is size-independent here; it must be in nu, the rate at which dips reach a few cells, and the
hull face's own contribution to that is its rim: the rim row is where a thin hull face's survivors gather (it is
denser in the living face, 0.48-0.50 at the edge row against 0.26 at corners) and where they do worst. The direct
test is the wrapped faces' q(k) and nu(k) from the other half of this study: if their q(k) matches these to the same
0.005, the two prices are all in nu.

## Forecasts, scored (`PREDICTIONS.md`)

| | forecast | found | |
|---|---|---|---|
| H1 | ln tau within 2 sigma of the GPU | +1.4 sigma (63), +0.9 sigma (84) | held |
| H2 | P bar within 0.15 / 0.25 | 31.253, 42.448 | held |
| H3 | A = 63 lag 4 in 0.26-0.36, lag 8 in 0.60-0.74, lag 16 >= 0.90 | 0.314, 0.676, 0.955 | held |
| H4 | plunge median 6-8 at 63, longer by 0-2 at 84 | 7, 8 | held |
| H5 | k* 2-3.5 (63) and 2-4 (84); smaller in P bar at 84 | 2.00, 1.98; 0.064 -> 0.047 | 63 held (at the edge), 84 **failed** by 0.02; second part held |
| H6 | q(3) at 84 within x1.5 of 63 | 0.296 against 0.298 | held (far inside) |
| H7 | rim-row share of last cells over stationary in 1.05-1.40 | 1.10, 1.12 | held |
| H8 | last cells under-represented within 1.5 units of a corner | 1.13, 1.15 (over; the 9 cells within 1 unit: 0.91, 0.92) | **failed** |
| H9 | uniform over the 8 faces | chi2 5.9, 7.7 on 7 | held |
| H10 | edge nb 0.70-0.88, vertex and opposite >= 0.93 at death | 0.772 / 0.806; 0.960 / 0.970; 1.00 | held |
| H11 | dying dips descend faster than recovering ones | same medians (7 / 7, 8 / 8) | **failed** |
| H12 | a recovered dip's minimum more clumped than a dying face at equal count | pair distance 1.71 vs 2.08 (k = 3), 2.30 vs 2.50 (6) at 63; 1.90 vs 2.36, 2.61 vs 2.84 at 84 | held |

"Against my reading" (rim holding out, corners irrelevant): H7 held but the reading behind it did not: the rim
excess is there because rim remnants die, not because the rim is fed and holds out (the q-by-class table).

## Agreement with research/dying (rounds 1-4, A = 63 c1 and A = 84, soup 0.4, other recorders)

- Time course and lag-1 count: agree (above). Neighbours at death 0.772 against round 1's 0.77.
- q and the point of no return: round 2 q(0.1 P bar) = 0.300 against q(3) = 0.298 here; p* = 0.079 P bar there with
  the strict level "min < p P bar", the same integer point (min <= 2) as k* = 2 here.
- ln nu(0.9 P bar) = -2.311 (round 2 -2.31). P bar 31.253 (round 1 review 31.25), 42.448 (round 2: 42.49 +- 0.09).
- Round 3's "the patch sits on the rim side of its centroid more often than on the centre side (not quantified)" is
  quantified here (rows). Round 2's lopsidedness and round 4's company were not recomputed.

## What was measured, and what each number rests on

- **Recorder `hd.c`**: research/gpu-local/cpu/fr.c's bit-sliced stepper (256 lanes per thread, AVX2), copied, on the
  hull's neighbour table (`hullvessel.py`: fl.Vessel as hullface.py builds it, numpy only, no GPU). Events every
  generation: a face empty (kind 1), period 1-2 (kind 2), cycles caught by snapshots at multiples of 2^10, 2^14,
  2^18 (kind 3; none occurred). Per lane, rings of the 8 face populations (4,096 generations) and of the face-layer
  cells (366 / 510; 1,024 generations), dumped at deaths (first 1,500 per thread: 4,500 at R = 11, 8,705 of 8,891 at R = 13) and at recovered
  dips (first 300 per minimum value 1..12 / 1..17 per thread; 1,024 generations of populations, 256 of states).
  Null: every lane at age > 2,000 every 9,973 generations (30,000 face-states per thread, 8 faces each).
  Excursions follow round 2 exactly, U = 32 and 43.
- **Stepper = engine, every generation** (`validate.py 11 3000 7`, `validate.py 13 3000 8`; `data/validate.log`):
  5 lanes (0, 63, 64, 130, 255) of hd.c's own soups, 3,000 generations each size, against `gump run --cells` in
  open space (the hull is exact): all equal; the production face counter equals numpy on 256 lanes x 8 faces x
  3,000 generations. Negative controls: the engine one generation later differs in 2,999 of 2,999 generations; one
  flipped face node differs in 3,000 of 3,000.
- **Each dump is checked as read** (`analyze.py`): ring populations equal popcounts of the stored states (first 300
  deaths and dips); the named face is empty at the last generation and not one before (all deaths); a recovered dip
  ends at P >= U with its minimum where the header says and nothing lower in its excursion (all).
- **End to end**: ln tau_face from the lives files against the GPU's values (table); dead excursions equal face
  deaths (42,489 / 42,494; 8,891 / 8,891); ν·q = death rate by construction.

## Reproduce (from the repository root; P = C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe)

    P research/dying2/hull/hullvessel.py 11; P research/dying2/hull/hullvessel.py 13      # vessels (scratch)
    P -u research/dying2/hull/validate.py 11 3000 7; P -u research/dying2/hull/validate.py 13 3000 8   # VALIDATE OK
    bash research/dying2/hull/run.sh 11 0.1667 1100      # 10 min x 3 threads: 4.5e9 replica-generations
    bash research/dying2/hull/run.sh 13 1.6667 1300      # 100 min x 3 threads: 4.0e10 (machine shared: ~1.7e6 /s/thread)
    bash research/dying2/hull/run.sh 13 1.75 1310        # the second R = 13 seed set: 4.5e10
    P -u research/dying2/hull/analyze.py 11 run_11_s1100               # ~1 min -> data/R11_*.csv, R11_analyze_out.txt
    P -u research/dying2/hull/analyze.py 13 run_13_s1300 run_13_s1310  # likewise R = 13
    P -u research/dying2/hull/condq.py 11 run_11_s1100                 # -> data/R11_condq.csv, R11_condq_out.txt
    P -u research/dying2/hull/condq.py 13 run_13_s1300 run_13_s1310
    P research/dying2/hull/figure.py                                   # hull_dying.svg

The R = 11 production ran an earlier build (`hd.exe`) that wrote excursion lines down to minimum 12 instead of 4;
nothing else differs, and no table uses those lines. Bulk output (~1.6 GB) is in `research/scratch/dying2-hull/`.

## Tables (`data/`)

`R{R}_death_timecourse.csv` (dying face by lag 0..4000: mean, 5/25/50/75/95%, neighbours), `R{R}_excursions.csv`
(nu, q by k), `R{R}_equal_depth.csv` (dying against recovering, aligned at the first P <= k), `R{R}_positions.csv`
(row and corner shares over stationary, pair distance), `R{R}_cells.csv` (per canonical cell: row, corner distance,
stationary occupancy, occupancy at lag 1), `R{R}_condq.csv` (q at first passage to exactly k, by where the
survivors sit), `R{R}_analyze_out.txt`, `R{R}_condq_out.txt` (the printed tables), `validate.log`.

## Not checked

- No second code for the dying statistics: one recorder, whose stepper is engine-checked (5 lanes x 3,000
  generations per size) and whose counter is checked on all lanes; the event logic is checked end to end only
  through ln tau and the dump checks.
- The null samples are not conditioned on the face living on (round 1: < 0.01 effect in c1).
- q by class uses weights from the hist files for the capped recovered dumps; errors are effective-count binomial,
  approximate. The rim x spread split is one cut (median spread, half the cells on the rim); no regression.
- Where the last cells sit is measured on the dying face only; the edge neighbour's rim row is the same cells, but
  the neighbour's own interior was not mapped.
- Recovered dips are capped per minimum value (900 or more per value) and are the first ones of each run, not a
  random sample in time (the runs are stationary after T0, so this should not matter; not tested).
