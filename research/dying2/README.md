# research/dying2: how wrapped faces die, watched

2026-11-18. Open problem 9 (k), (l): rimmed hull faces pay about 0.231 per cell in ln τ, wide wrapped faces 0.2087,
tubes of loop² 12 less (0.2044 from 54 to 84 cells, 0.2016 from 84 to 108). This study records face deaths and the
dips that recovered on four wrapped faces and measures how they die. The rimmed hull face is a separate share:
**`hull/README.md`** (its own stepper, definitions and forecasts). Forecasts for this share: `PREDICTIONS.md`
(committed b851756, before any table). Tags: **[measured]** (number, command), **[conjectured]**.

**State at this writing (05:20 UTC): W63 and T84 complete, T96 interim (707 deaths), E84 running (see "Runs"). Tables are
added as they come.**

## Faces

All 8-layer slabs of `research/shape/tslab.py`, soup density 0.4 on all nodes, as `research/gpu-local/eqtorus.py`
(the vessels of `research/gpu-local/README.md`, "Tube and wrapped faces").

| name | torus | cells A | shortest loop² | axis length Lax (cube edges) | P̄ (this study) | σ_P | ln τ_face (card, GPU) |
|---|---|---:|---:|---:|---:|---:|---:|
| W63 | (1,4),(0,21) | 63 | 21 | 5.61 | 32.583 | 4.942 | 13.1622 ± 0.0007 |
| E84 | (2,4),(0,14) | 84 | 28 | 6.48 | 43.48 (pilot) | 5.65 | 17.547 ± 0.003 |
| T84 | (1,12),(0,28) | 84 | 12 | 9.90 | 43.30 (pilot) | 5.81 | 17.3175 ± 0.0031 |
| T96 | (1,17),(0,32) | 96 | 12 | 11.31 | 49.48 (pilot) | 6.22 | 19.7405 ± 0.0059 |

The "axis" of a face is the in-plane direction perpendicular to its shortest loop vector s; position along it, u,
is periodic with period Lax = covolume / |s| (checked: both lattice generators project to whole multiples of Lax).
On the tubes the girth is |s| = √24 = 4.90 cube edges, so T84 is a tube two girths long and T96 2.3 girths; W63 and
E84 have no short direction and their "axis" is only a reference direction.

## Definitions (from `research/dying/README.md`; what replaces the rim)

- Only face deaths at life age > T0 = 512 are used. t_d = first generation with the face empty; lag l = t_d − t.
  Each death record holds the last min(4096, age − 512) generations of the dying face layer and the layer beneath.
- t_h = earliest t ≤ t_d with P(t') < P̄/2 for all t' in [t, t_d]; plunge Δ = t_d − t_h (round 1, L6/L7).
- Excursions (round 2): from the first generation with P < P̄ after one with P ≥ P̄ (both at age > T0) to the first
  later generation with P ≥ P̄ (recovered), a face death (dead) or another end of the life (censored). Tallied for
  every excursion online, by minimum. ν(≤k) = excursions with minimum ≤ k per face-generation at age > T0;
  q(k) = dead / (dead + recovered) among them; k* = the k where q crosses 1/2. P̄ for the threshold is fixed from a
  pilot run (`dy.py pbar`, 200,000 generations × 256 lanes); the production run's own P̄ agrees to 0.001 on W63.
- **No rim, no corners.** A wrapped face is translation invariant, so where the last cells sit can only be said
  relative to each other. Used instead: the **axial extent X** of the survivors (1 − the largest circular gap between
  their u values, as a fraction of Lax; X = 0 for one cell), against a **random-thinning null** (stationary faces from
  the null samples, thinned uniformly to the same count). A **cut** is an empty band across the axis at least one cube
  edge wide (largest gap × Lax ≥ 1); the "final cut" begins at the first generation of the last unbroken run of
  generations with a cut before t_d.
- "Caught at k": the first generation of the excursion with P ≤ k (round 4's first-passage catch), for dying faces
  (their final excursion) and recovered ones (every recovered excursion with minimum ≤ KDUMP = 5, 6, 6, 7 for W63,
  E84, T84, T96 is recorded, the last 512 generations to recovery).

## W63, (1,4),(0,21), 63 cells [measured]

Run: `dy.py run 1 4 21 1.0 63001 32.58 5 threads=1 nullsh=14 H=4096 R=512 maxdeath=8000 maxrec=40000 chunk=2`
(0.09 thread-hours, seed 63001); tables: `dyan.py 1 4 21 kmax=5` (3 minutes) → `data/1_4_21_*.csv`,
`data/1_4_21_report.txt`. 8,000 face deaths at age > 512, 31,723 recovered dips with minimum ≤ 5, 124,664 null
faces. Its own ln τ_face = 13.144 ± 0.011 (GPU 13.1622 ± 0.0007: −1.7σ). No co-death of the two faces.

**The final dip is four generations long.** Mean P/P̄ by lag (quantiles 10/50/90 in brackets):

| lag | 0 | 1 | 2 | 3 | 4 | 6 | 8 | 12 | 16 | 32 | 256 | 3583 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P/P̄ | 0 | 0.052 | 0.131 | 0.323 | 0.567 (0.06/0.34/1.44) | 0.776 | 0.894 (0.25/0.98/1.23) | 0.977 | 0.992 | 0.999 | 1.001 | 0.999 |
| layer beneath / stationary | 0.694 | 0.584 | 0.553 | 0.611 | 0.764 | 0.871 | 0.937 | 0.988 | 0.997 | 0.999 | 1.001 | 0.998 |

- Median plunge Δ = 4 generations (quartiles 3–6, mean 5.0). From the last passage below 0.5, 0.3, 0.15 P̄ to
  death: median 4, 3, 2 generations (90%: 9, 8, 6). Live cells at lag 1: mean 1.69 (one cell in 60%, two in 23%).
- Against the c1 hull face of the same area (round 1: 0.95, 0.67, 0.31 at lags 16, 8, 4; median Δ 6, quartiles
  4–8; 1.61 cells at lag 1), the wrapped face stays at its stationary population longer and falls faster: at lag 8
  it is still at 0.89 of P̄ against 0.67. The mean curve over the last 32 generations is a step, not a slope.
- The layer beneath dips with the face (0.55 at lag 2) and partly recovers at the moment of death, as on hull faces.

**Point of no return: 2.73 live cells (0.084 P̄)**, as on the c1 hull face (0.079 P̄, about 2.5 cells).

| k (live cells) | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 16 (0.49 P̄) | 22 (0.68) | 29 (0.89) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| q(k) | 0.860 | 0.641 | 0.447 | 0.304 | 0.201 | 0.134 | 0.058 | 0.025 | 1.8e−3 | 1.3e−4 | 1.4e−5 |
| ln ν(≤k) | −12.99 | −12.70 | −12.34 | −11.95 | −11.54 | −11.13 | −10.29 | −9.44 | −6.83 | −4.17 | −1.95 |

- ν(≤k)·q(k) equals the face death rate at every k to 10⁻⁴ (no censored excursion ends below 30 cells here; a
  code check, not a finding).
- At round 2's levels: ln ν(0.9) = −1.95, ln ν(0.7) = −4.17 (c1 hull: −2.31, −4.16), ln ν(0.5) = −6.83 (c1:
  −6.51). The tail of ln ν(≤k) over 0.1–0.45 P̄ has slope 0.424 per live cell (unweighted; c1 hull 0.50).
  Per site: [ln ν(0.9) − ln ν(0.5)]/A = 0.077 (c1 hull 0.067), [ln ν(0.9) + ln τ]/A = 0.178 (c1 hull 0.180).
  **So the wrapped face makes shallow dips more often than the hull face and each further cell lost costs it less
  (0.42 against 0.50 per cell); the two lifetimes at 63 cells come out nearly equal (13.16 against 13.63) from
  different shapes of the dip curve.**

**Where the survivors sit (no rim: the axial extent X).** At t_h (11.8 live cells on average) X = 0.728 ± 0.001
against 0.742 for random thinning to the same counts (ratio 0.981): almost no clumping half way down. At lag 4, 2, 1
(faces with ≥ 2 live cells): X = 0.651, 0.398, 0.272 against 0.679, 0.471, 0.338. The survivors draw together only in
the last two or three generations. The final cut begins at a median lag of 4 (quartiles 3–6, 90% 9); the empty band
is 0.91, 1.26, 1.96, 2.59, 3.38, 4.08 cube edges wide at lags 8, 6, 4, 3, 2, 1 (of 5.61): a band that widens by
about 0.7 cube edges per generation in the last four generations, which is the face emptying everywhere at once
read along one direction, not a front.

**Dying against recovered at equal depth.** Caught at the first generation with P ≤ k:

| k | q (from catches = from the online table) | X dying (count = k) | X recovered (count = k) | X random thinning | P four generations before the catch: dying / recovered |
|---|---|---|---|---|---|
| 2 | 0.641 | 0.183 | 0.150 | 0.258 | 30.24 / 28.23 |
| 3 | 0.447 | 0.307 | 0.254 | 0.393 | 32.10 / 30.67 |
| 4 | 0.304 | 0.399 | 0.340 | 0.486 | 32.43 / 31.58 |
| 5 | 0.201 | 0.470 | 0.407 | 0.554 | 32.28 / 31.91 |

- Both are clumped against random thinning; the faces that go on to die are **more spread out** than those that
  recover (by 0.05–0.06 in X at every k), round 4's direction on hull faces.
- **A death is a faster fall.** Before the catch, dying and recovering dips have the same population until about 4
  generations before; then the dying ones fall from higher (at k = 2, P = 30.2 against 28.2 four generations
  earlier, 11.5 against 9.4 two generations earlier). Recovered dips descend from P̄/2 to their minimum in a median
  of 3–4 generations (minima 1–5), deaths in 4; they climb back to P̄ in 8–11.

## T84 and T96, the loop² 12 tubes [measured]

T84: `bash research/dying2/chain84.sh` (first line; 1.77 thread-hours, seed 84001), 2,500 deaths, 19,628 recovered
dips (minimum ≤ 6), own ln τ_face 17.351 ± 0.020 (GPU 17.3175: +1.6σ). T96 (interim, 05:07 UTC: 679 deaths in the
stats, 707 records; seeds 96001–96003, 5.5 thread-hours so far), own ln τ_face 19.680 ± 0.038 (GPU 19.7405: −1.6σ).
Tables: `dyan.py 1 12 28 kmax=6`, `dyan.py 1 17 32 kmax=7` → `data/1_12_28_*`, `data/1_17_32_*`. No co-deaths.

| | W63 | T84 | T96 (interim) |
|---|---|---|---|
| P/P̄ at lag 1, 2, 3, 4 | 0.052, 0.131, 0.323, 0.567 | 0.038, 0.090, 0.210, 0.421 | 0.034, 0.078, 0.173, 0.353 |
| P/P̄ at lag 6, 8, 12, 16 | 0.776, 0.894, 0.977, 0.992 | 0.697, 0.845, 0.966, 0.996 | 0.623, 0.810, 0.961, 0.984 |
| median plunge Δ (quartiles) | 4 (3–6) | 5 (4–7) | 6 (4–7) |
| live cells at lag 1 | 1.69 | 1.63 | 1.68 |
| layer beneath at lag 2 / at death | 0.55 / 0.69 | 0.61 / 0.77 | 0.65 / 0.80 |
| **k\*** (q = 1/2) | **2.73** (0.084 P̄) | **2.59** (0.060 P̄) | **2.63** (0.053 P̄) |
| q(1), q(2), q(3), q(4), q(5) | 0.860, 0.641, 0.447, 0.304, 0.201 | 0.846, 0.623, 0.413, 0.274, 0.177 | 0.871, 0.622, 0.428, 0.282, 0.182 |
| ln ν(≤k) at k = 2, 5, 10 | −12.70, −11.54, −9.44 | −16.88, −15.62, −13.33 | −19.20, −17.97, −15.63 |
| ln ν at 0.9, 0.7, 0.5 P̄ (round 2 levels) | −1.95, −4.17, −6.83 | −2.20, −4.44, −8.10 | −2.16, −4.86, −8.89 |
| tail slope over 0.1–0.45 P̄ (per live cell) | 0.424 | 0.473 | 0.485 |
| [ln ν(0.9) + ln τ]/A | 0.178 | 0.180 | 0.183 |
| X at t_h / random thinning | 0.728 / 0.742 (0.981) | 0.746 / 0.784 (0.952) | 0.767 / 0.804 (0.954) |
| X at lag 2 / random thinning | 0.398 / 0.471 | 0.341 / 0.460 | 0.318 / 0.445 |
| band ≥ 1 cube edge: final cut opens, median lag; P/P̄ then | 4; — | 6; 0.49 | 6; 0.51 |
| band ≥ 2 cube edges (added after the forecasts): opens at median lag (quartiles); P/P̄ then; share opening above P̄/2 | 3 (2–5); 0.18; 0.008 | 5 (3–7); 0.34; 0.13 | 6 (4–8); 0.36; 0.16 |
| empty band (cube edges) at lag 8, 4, 2, 1: deaths / random thinning | 0.91/0.84, 1.96/1.80, 3.38/2.97, 4.08/3.72 | 1.76/1.49, 4.13/3.60, 6.53/5.35, 7.61/6.63 | 2.13/1.76, 5.20/4.44, 7.71/6.28, 8.85/7.56 |

**The point of no return is the same number of cells on every wrapped face: 2.6–2.7.** q(k) at k ≤ 5 agrees across
W63, T84 and T96 within 0.02–0.04 (the errors are 0.005–0.01), so what makes a tube or a larger face live longer or
shorter is entirely in how often a face gets down to a few cells, not in what happens once it is there. (The c1 hull
face of 63 cells: about 2.5.)

**A tube's death starts as a band, but only at a third of the mean.** On the tubes an empty band two cube edges wide
(0.4 of the girth) opens at a median of 5–6 generations before death, when the face is still at 0.34–0.36 of P̄ (in
13–16% of deaths above P̄/2); on W63 the same band opens 3 generations before, at 0.18 of P̄. Once open it widens by
about 1.0 (T84) to 1.1 (T96) cube edges per generation over the last 6–8 generations, 0.5 per side, and the
survivors at lag 2 occupy a third of the tube's length. Against random thinning to the same counts the band is
wider by 0.3 cube edges at lag 8, 0.5–0.8 at lag 4 and 1.2–1.4 at lag 2: the axial clumping is real and about twice
the wide face's in units of the axis (X deficit 0.12–0.13 at lag 2 against 0.07), but most of the band is the face
emptying as a whole: at t_h the tube's survivors are only 5% less spread along the axis than random (the wide face
2%). [conjectured] A tube dies like a wide face that has, in its last half-dozen generations, a preferred direction
to clump in; nothing seen here is a front that runs along the tube over tens of generations.

**Dying against recovered at equal depth (tubes).** The faces that go on to die are more spread out along the axis
than those that recover, at every k (T84, count = k: X = 0.158, 0.272, 0.366, 0.432, 0.489 against 0.109, 0.205,
0.292, 0.348, 0.395 for k = 2…6; T96 alike), and they fell faster: at k = 4, P four generations before the catch was
42.1 against 39.6 (T84), 47.1 against 43.1 (T96).

## Runs

| face | command | seeds | started (UTC) | state |
|---|---|---|---|---|
| W63 | above | 63001 | 03:17 | done, 8,000 deaths |
| T84 | `bash research/dying2/chain84.sh` (first line) | 84001 | 03:24 | done 05:11, 2,500 deaths |
| E84 | `chain84.sh` (second line) | 84101 | 05:11 | running, to 2,500 deaths or 2.5 h |
| T96 | `dy.py run 1 17 32 5.5 96001 49.48 7 threads=3 nullsh=17 H=4096 R=512 maxrec=30000 chunk=10` | 96001–96003 | 03:17 | running, 3 threads, about 210 deaths per hour |

## Checks [measured]

- **Stepper = engine, every generation** (`dy.py step A KK B`, the method of `research/gpu-local/cpu/fr.py step`
  with dy.exe's own trace mode; 2,000 generations, 3 engine soups × 3 lanes each, the other lanes random): all equal
  on (1,4),(0,21), (2,4),(0,14), (1,12),(0,28), (1,17),(0,32). Negative controls (next generation; one node
  flipped): 300 of 300 differ on each. The step function is fr.c's, unchanged.
- **Records and tallies against numpy** (`dy.py events A KK B GENS SEED PBAR KDUMP NULLSH H R`): an independent numpy
  stepper (counting rule) runs lanes 0–127 from dy.c's soups with fr.py's event tests and its own implementation of
  the excursion rules, ring buffer and dumps, and must give the same lives, the same records bit for bit and the
  same tallies (exposure, ΣP, ΣP², the P histogram, the excursion table by minimum and end type, deaths inside and
  outside excursions). (1,4),(0,10) × 8, 30,000 generations, H = 256, R = 128, KDUMP = 3: lives (11,580), records
  (2,270 deaths, 2,977 recovered dips, 199 null) and tallies IDENTICAL. (1,17),(0,32) × 8 (A = 96: all 7 bits of
  the counter, 12-byte layers), 6,000 generations, H = 1024, R = 512, KDUMP = 40: lives (128), records (66,559
  recovered dips, 1,280 null; no death in so short a run, so the script prints FAIL for want of one) and tallies
  (318,198 excursions; the P histogram to its top) IDENTICAL; 27 minutes.
- In the analysis: every death record ends with the first empty generation and has a live face one generation
  before; every recovered record's minimum equals its header's; q from the dumped catches equals the online q at
  every k ≤ KDUMP (W63: to four digits).

## Not checked

- Lanes 128–255 against numpy (same code as 0–127). Death records were checked against numpy only on the 30-cell
  vessel; on the 96-cell tube only recovered and null records (the same writer).
- The null samples are taken at fixed generations, not conditioned on the life going on (round 1 conditioned on 64
  more generations; it moved P̄ by < 0.01 there).
- No second code for anything here; no adversarial review.
