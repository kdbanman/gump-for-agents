# research/dying2: how wrapped faces die, watched

2026-11-18. Open problem 9 (k), (l): rimmed hull faces pay about 0.231 per cell in ln τ, wide wrapped faces 0.2087,
tubes of loop² 12 less (0.2044 from 54 to 84 cells, 0.2016 from 84 to 108). This study records face deaths, and the
dips that recovered, on four wrapped faces and measures how they die. The rimmed hull face is a separate share:
**`hull/README.md`** (its own stepper, definitions and forecasts). Forecasts for this share: `PREDICTIONS.md`
(committed b851756, before any table), scored below. Tags: **[measured]** (number, command), **[conjectured]**.
All four runs are complete (2,500–8,000 deaths each).

## Short answer

- **[measured] Every wrapped face dies the same way, in the last 4–6 generations.** The mean face is at its stationary
  population until about 12 generations before death (0.96–0.98 of P̄), at 0.82–0.89 at lag 8, then empties: median
  plunge from P̄/2 to empty 4–5 generations; 1.63–1.69 live cells one generation before. The c1 hull face of 63 cells
  (round 1) falls earlier and slower (0.67 at lag 8, median plunge 6).
- **[measured] The point of no return is the same number of cells on every wrapped face: k\* = 2.59–2.73 live
  cells**, and q(k), the chance that a dip reaching k cells ends in death, agrees across the four faces within
  0.01–0.03 at every k ≤ 5 (q(2) = 0.62–0.64, q(4) = 0.27–0.30). It does not scale with the face (0.084 P̄ at 63
  cells, 0.053 P̄ at 96). So the differences between the lifetimes, of size, of shape and of tubes against wide
  faces, all sit in how often a face gets down to a few cells (ν), none in what happens once it is there.
- **[measured] The tube's discount at 84 cells is in reaching the last cells, not in the last cells.** T84 lives
  0.21 shorter in ln τ than E84 (same area). At ≤ 10 cells T84's dip rate is higher by 0.30 in ln ν with q equal; at
  P̄/2 the tube dips more often (+0.56 in ln ν) and such a dip kills it less often (−0.35 in ln q).
- **[measured] Only a tube opens a band while a third of the face is alive.** An empty band 2 cube edges wide across
  the axis (0.4 of the girth) opens on the tubes at a median of 5 generations before death, at 0.34–0.37 P̄ (above
  P̄/2 in 13–17% of deaths); on the wide faces 3–4 generations before, at 0.17–0.18 P̄ (above P̄/2 in < 1%). Once open
  it widens by about 1.0–1.1 cube edges per generation (0.5 per side). Against random thinning to the same count
  the tube's band is wider by 1.2–1.4 cube edges at lag 2 (0.12 of the axis; wide faces 0.07–0.08). But it is no
  long-lived front: at t_h the tube's survivors are only 5% less spread along the axis than random (wide faces 2%).
  **[conjectured]** A tube dies like a wide face that, in its last half-dozen generations, has a preferred direction
  to clump in.
- **[measured] Dying dips are faster falls and looser clumps.** Caught at equal count k (2–6), the faces that go on
  to die had fallen faster (at k = 4, four generations earlier they held 0.8 (W63) to 3.4 (T96) more cells than
  faces that recover) and their survivors are more spread along the axis (X larger by 0.04–0.10), round 4's
  direction on hull faces. Both are more clumped than random thinning.
- **[measured] The layer beneath feels it.** The layer under the dying face falls to 0.55–0.64 of its stationary
  population at lag 2 and partly recovers at the moment of death (0.69–0.80), as on hull faces. The two faces of a
  slab never died in the same generation (0 co-deaths in 15,503).

## Faces

All 8-layer slabs of `research/shape/tslab.py`, soup density 0.4 on all nodes, as `research/gpu-local/eqtorus.py`
(the vessels of `research/gpu-local/README.md`, "Tube and wrapped faces").

| name | torus | cells A | shortest loop² | axis length Lax (cube edges) | P̄ (this study) | σ_P | ln τ_face, this study | ln τ_face (card, GPU) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| W63 | (1,4),(0,21) | 63 | 21 | 5.61 | 32.583 | 4.942 | 13.144 ± 0.011 | 13.1622 ± 0.0007 |
| E84 | (2,4),(0,14) | 84 | 28 | 6.48 | 43.483 | 5.650 | 17.559 ± 0.020 | 17.547 ± 0.003 |
| T84 | (1,12),(0,28) | 84 | 12 | 9.90 | 43.296 | 5.813 | 17.351 ± 0.020 | 17.3175 ± 0.0031 |
| T96 | (1,17),(0,32) | 96 | 12 | 11.31 | 49.481 | 6.214 | 19.716 ± 0.020 | 19.7405 ± 0.0059 |

The four lifetimes are within 1.7σ of the card's (−1.7, +0.6, +1.6, −1.2). The "axis" of a face is the in-plane
direction perpendicular to its shortest loop vector s; position along it, u, is periodic with period Lax =
covolume / |s| (checked: both lattice generators project to whole multiples of Lax). On the tubes the girth is
|s| = √24 = 4.90 cube edges, so T84 is two girths long and T96 2.3; W63 and E84 have no short direction and their
"axis" is only a reference direction.

## Definitions (from `research/dying/README.md`; what replaces the rim)

- Only face deaths at life age > T0 = 512 are used (every face death in these runs was). t_d = first generation with
  the face empty; lag l = t_d − t. Each death record holds the last min(4096, age − 512) generations of the dying
  face layer and the layer beneath.
- t_h = earliest t ≤ t_d with P(t') < P̄/2 for all t' in [t, t_d]; plunge Δ = t_d − t_h (round 1, L6/L7).
- Excursions (round 2): from the first generation with P < P̄ after one with P ≥ P̄ (both at age > T0) to the first
  later generation with P ≥ P̄ (recovered), a face death (dead) or another end of the life (censored; none occurred:
  no firewall and no settled life in any run). Tallied for every excursion online, by minimum. ν(≤k) = excursions
  with minimum ≤ k per face-generation at age > T0; q(k) = dead / (dead + recovered) among them; k* = the k where q
  crosses 1/2 (linear in k). "Round-2 levels": reaching p means minimum < p·P̄. P̄ for the threshold was fixed from
  a pilot (`dy.py pbar`, 200,000 generations × 256 lanes); each production run's own P̄ agrees with it to 0.002.
- **No rim, no corners.** A wrapped face is translation invariant, so where the last cells sit can only be said
  relative to each other. Used instead: the **axial extent X** of the survivors (1 − the largest circular gap between
  their u values, as a fraction of Lax; X = 0 for one cell), against a **random-thinning null** (stationary faces
  from the null samples, thinned uniformly to the same count). A **cut** is an empty band across the axis at least
  one cube edge wide (largest gap × Lax ≥ 1); the "final cut" begins at the first generation of the last unbroken run
  of generations with a cut before t_d. *Added after the forecasts:* the same with 2 cube edges, because a 1-edge gap
  is already common in the stationary tube (its mean largest gap is 0.94 edges).
- "Caught at k": the first generation of the excursion with P ≤ k (round 4's first-passage catch), for dying faces
  (their final excursion) and recovered ones (every recovered excursion with minimum ≤ KDUMP = 5, 6, 6, 7 for W63,
  E84, T84, T96 is recorded, the last 512 generations to recovery; none started earlier than that).

## Numbers [measured]

Commands: `dyan.py 1 4 21 kmax=5`, `dyan.py 2 4 14 kmax=6`, `dyan.py 1 12 28 kmax=6`, `dyan.py 1 17 32 kmax=7`
(P = the venv python, from the repository root; 3–15 minutes each) → `data/<A>_<KK>_<B>_report.txt` (everything
below) and the csv tables `_lags` (P/P̄ and the layer beneath by lag, mean and quantiles 10/25/50/75/90),
`_excursions` (ν, q by k), `_band` (X, band width and their nulls by lag), `_catches`, `_catch_traj` (P around the
catch, dying and recovered), `_cutstart_hist`. Errors: q(k) binomial, 0.005–0.01 at k ≤ 5; X ± 0.001–0.002 at t_h.

| | W63 | E84 | T84 | T96 |
|---|---|---|---|---|
| deaths; recovered dips recorded | 8,000; 31,723 | 2,500; 19,148 | 2,500; 19,628 | 2,503; 33,434 |
| P/P̄ at lag 1, 2, 3, 4 | 0.052, 0.131, 0.323, 0.567 | 0.038, 0.094, 0.229, 0.448 | 0.038, 0.090, 0.210, 0.421 | 0.034, 0.080, 0.181, 0.372 |
| P/P̄ at lag 6, 8, 12, 16 | 0.776, 0.894, 0.977, 0.992 | 0.719, 0.860, 0.969, 0.989 | 0.697, 0.845, 0.966, 0.996 | 0.645, 0.824, 0.961, 0.991 |
| median plunge Δ (quartiles) | 4 (3–6) | 5 (3–7) | 5 (4–7) | 5 (4–7) |
| last passage below 0.5, 0.3, 0.15 P̄ to death (medians) | 4, 3, 2 | 5, 4, 3 | 5, 4, 3 | 5, 4, 3 |
| live cells at lag 1 | 1.69 | 1.66 | 1.63 | 1.68 |
| layer beneath (/ stationary) at lag 4, 2, 0 | 0.76, 0.55, 0.69 | 0.70, 0.58, 0.74 | 0.70, 0.61, 0.77 | 0.68, 0.64, 0.80 |
| **k\*** (q = 1/2) | **2.73** (0.084 P̄) | **2.63** (0.061 P̄) | **2.59** (0.060 P̄) | **2.62** (0.053 P̄) |
| q(1), q(2), q(3), q(4), q(5) | 0.860, 0.641, 0.447, 0.304, 0.201 | 0.853, 0.633, 0.422, 0.277, 0.179 | 0.846, 0.623, 0.413, 0.274, 0.177 | 0.855, 0.625, 0.422, 0.275, 0.176 |
| ln ν(≤k) at k = 2, 5, 10 | −12.70, −11.54, −9.44 | −17.10, −15.84, −13.63 | −16.88, −15.62, −13.33 | −19.25, −17.98, −15.63 |
| ln ν at 0.9, 0.7, 0.5 P̄ (round-2 levels) | −1.95, −4.17, −6.83 | −2.01, −4.65, −8.66 | −2.20, −4.44, −8.10 | −2.16, −4.86, −8.89 |
| tail slope of ln ν(≤k), 0.1–0.45 P̄, per live cell | 0.424 | 0.446 | 0.473 | 0.484 |
| [ln ν(0.9) + ln τ]/A | 0.178 | 0.185 | 0.180 | 0.183 |
| X at t_h / random thinning (ratio) | 0.728 / 0.742 (0.981) | 0.777 / 0.789 (0.985) | 0.746 / 0.784 (0.952) | 0.763 / 0.803 (0.950) |
| X at lag 2 / random thinning | 0.398 / 0.471 | 0.381 / 0.461 | 0.341 / 0.460 | 0.335 / 0.458 |
| 1-edge cut: final cut opens, median lag; mean P/P̄ then | 4; 0.35 | 5; 0.33 | 6; 0.49 | 6; 0.51 |
| 2-edge cut: median lag (quartiles); mean P/P̄ then; share opening above P̄/2 | 3 (2–5); 0.18; 0.008 | 4 (2–6); 0.17; 0.004 | 5 (3–7); 0.34; 0.13 | 5 (4–8); 0.37; 0.17 |
| empty band (cube edges) at lag 8, 4, 2, 1: deaths / random thinning | 0.91/0.84, 1.96/1.80, 3.38/2.97, 4.08/3.72 | 1.04/0.96, 2.44/2.33, 4.01/3.49, 4.78/4.34 | 1.76/1.49, 4.13/3.60, 6.53/5.35, 7.61/6.63 | 2.03/1.66, 4.91/4.25, 7.53/6.13, 8.80/7.57 |
| X at count = k, k = 2…5: dying / recovered / random | .18/.15/.26, .31/.25/.39, .40/.34/.49, .47/.41/.55 | .18/.14/.25, .29/.24/.39, .39/.33/.49, .46/.39/.55 | .16/.11/.25, .27/.21/.39, .37/.29/.49, .43/.35/.55 | .15/.11/.25, .27/.20/.39, .37/.28/.48, .42/.34/.55 |
| P 4 generations before the catch at k = 4: dying / recovered | 32.4 / 31.6 | 43.3 / 40.9 | 42.1 / 39.6 | 46.6 / 43.2 |
| recovered dips, P̄/2 to minimum (median, minima 1–KDUMP); minimum back to P̄ | 3–4; 8–11 | 3–5; 9–13 | 3–5; 11–15 | 3–5; 12–17 |

Remarks on the table:

- ν(≤k)·q(k) equals the face death rate at every k to 10⁻⁴ (every death ends an excursion and nothing was censored:
  a code check), and q from the dumped catches equals the online q at every k ≤ KDUMP to four digits.
- **Against the c1 hull face of 63 cells** (round 1 and 2): lag 16, 8, 4 at 0.95, 0.67, 0.31 (W63 0.99, 0.89, 0.57);
  median plunge 6 (4–8) against 4 (3–6); p* = 0.079 P̄, about 2.5 cells (W63 2.73); ln ν(0.9), ln ν(0.7),
  ln ν(0.5) = −2.31, −4.16, −6.51 (W63 −1.95, −4.17, −6.83); tail slope 0.50 per cell (W63 0.42);
  [ln ν(0.9) + ln τ]/A 0.180 (W63 0.178). The wrapped face makes shallow dips more often, pays less per further
  cell lost, and the two come out at nearly the same lifetime (13.16 against 13.63).
- **From 63 to 84 cells (W63 to E84, 0.210 per cell in ln τ):** ln ν(≤2) falls by 4.40 and q(2) by 0.008; ln ν(0.9)
  by 0.06. The price per cell is paid entirely on the way down to two cells.
- **Tubes against E84:** the tubes are at the same depth fraction later in their dips (P/P̄ lower at lags 2–8), a
  slower last stretch; and their survivors are clumped along the axis from about lag 8 on (X deficits at lag 4:
  T84 0.054, T96 0.058, E84 0.017, W63 0.028).

## Forecasts, scored (`PREDICTIONS.md`)

| | forecast (probability) | found | |
|---|---|---|---|
| 1 | W63 within 0.08 of c1 at lags 16, 8, 4; median Δ 5–8 on all faces (70%) | 0.99, 0.89, 0.57 against 0.95, 0.67, 0.31; Δ 4, 5, 5, 5 | **failed** (later and steeper than a hull face) |
| 2 | median Δ: T84 and E84 within 1; T96 within 1 of T84 (65%) | 5, 5; 5 | held |
| 3 | k* 2–4 on W63, 2–5 on the others (65%) | 2.73; 2.63, 2.59, 2.62 | held |
| 4 | 1.4–1.9 live cells at lag 1 (70%) | 1.63–1.69 | held |
| 5 | W63 ln ν(0.7) in [−4.8, −4.2] (60%) | −4.17 | **failed** by 0.03 (as frequent as on the hull face, not rarer) |
| 6 | ≥ half of E84 − T84 in ln ν at P̄/2 (55%) | +0.56 in ln ν, −0.35 in ln q (the opposite sign) for a 0.21 gap | held (the ν part is more than all of it) |
| 7 | T96: final cut opens ≤ 12 generations before death in the median death (65%) | 6 | held |
| 8 | T96: X at t_h ≥ 10% below random thinning (70%) | 5.0% below | **failed** |
| 9 | X/X_null at t_h: E84 within 0.05 of T84 (50%) | 0.985 against 0.952 | held (but the 0.033 is many errors; the tube clumps more) |
| 10 | dying more spread than recovered at equal k, 2–5 (60%) | yes, on all four faces at every k | held |
| 11 | W63 layer beneath at lag 4: 0.6–0.85 (65%) | 0.76 | held |
| 12 | co-deaths ≤ 1/1000; ν·q identity (95%) | 0 of 15,503; exact | held |

## Runs

| face | command (from the repository root, P = `C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe -u`) | seeds | thread-hours |
|---|---|---|---|
| W63 | `P research/dying2/dy.py run 1 4 21 1.0 63001 32.58 5 threads=1 nullsh=14 H=4096 R=512 maxdeath=8000 maxrec=40000 chunk=2` | 63001 | 0.09 |
| T84 | `bash research/dying2/chain84.sh` (first line) | 84001 | 1.77 |
| E84 | `bash research/dying2/chain84.sh` (second line) | 84101 | 2.04 |
| T96 | `P research/dying2/dy.py run 1 17 32 5.5 96001 49.48 7 threads=3 nullsh=17 H=4096 R=512 maxrec=30000 chunk=10`, then `... run 1 17 32 1.5 96004 ... threads=1 ...` | 96001–96004 | 18.0 |

The pilot P̄: `P research/dying2/dy.py pbar A KK B gens=200000` (5 s each). Records and stats live in
`research/scratch/dying2/run_A_KK_B/` (3.7 GB, not kept in git); the tables in `data/` are made from them by `dyan.py`.
Throughput on this shared machine: 5–6 × 10⁶ lane-generations per second per thread with the recording on.

## Checks [measured]

- **Stepper = engine, every generation** (`dy.py step A KK B`, the method of `research/gpu-local/cpu/fr.py step`
  with dy.exe's own trace mode; 2,000 generations, 3 engine soups × 3 lanes each, the other lanes random): all equal
  on (1,4),(0,21), (2,4),(0,14), (1,12),(0,28), (1,17),(0,32). Negative controls (next generation; one node
  flipped): 300 of 300 differ on each. `dy.c` is a copy of `research/gpu-local/cpu/fr.c` whose step, events and
  reseeding are unchanged; it adds the per-lane face count, the ring buffer, the excursion tallies and the records.
- **Records and tallies against numpy** (`dy.py events A KK B GENS SEED PBAR KDUMP NULLSH H R`): an independent numpy
  stepper (counting rule) runs lanes 0–127 from dy.c's soups with fr.py's event tests and its own implementation of
  the excursion rules, ring buffer and dumps, and must give the same lives, the same records bit for bit and the
  same tallies (exposure, ΣP, ΣP², the P histogram, the excursion table by minimum and end type, deaths inside and
  outside excursions). (1,4),(0,10) × 8, 30,000 generations, H = 256, R = 128, KDUMP = 3: lives (11,580), records
  (2,270 deaths, 2,977 recovered dips, 199 null) and tallies IDENTICAL. (1,17),(0,32) × 8 (A = 96: all 7 bits of
  the counter, 12-byte layers), 6,000 generations, H = 1024, R = 512, KDUMP = 40: lives (128), records (66,559
  recovered dips, 1,280 null; no death in so short a run, so the script prints FAIL for want of one) and tallies
  (318,198 excursions; the P histogram to its top) IDENTICAL; 27 minutes.
- In the analysis (asserted for every record): each death record ends with the first empty generation and has a
  live face one generation before; each recovered record's minimum after its start equals its header's.

## Not checked

- Lanes 128–255 against numpy (same code as 0–127). Death records were checked against numpy only on the 30-cell
  vessel; on the 96-cell tube only recovered and null records (the same writer).
- The null samples are taken at fixed generations, not conditioned on the life going on (round 1 conditioned on 64
  more generations; it moved P̄ by < 0.01 there); the null draws faces with at least k live cells, which biases it
  slightly towards fuller faces (at lag 32 the random-thinning band is 0.01–0.07 edges narrower than the deaths').
- The axial extent is one projection. The spread around the girth, two-dimensional clumping (graph distances, as
  round 4's company C) and the position of the last cells relative to the band were not measured.
- No bootstrap errors on the medians and band widths; no second code for anything here; no adversarial review.
- Each 84-cell face has one seed; T96 has four (their death counts 719, 778, 759, 247 for 3, 3, 3, 1 threads × 5.5,
  5.5, 5.5, 1.5 h are consistent with one rate; not tested formally).
