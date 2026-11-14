# The exam: sampled tests of the swarm's predictions

_Examiner, 2026-11-14. The predictions are in `research/theory/swarm/PREDICTIONS.md` (filed 2026-11-13, before
any of these runs). I wrote none of them. Part 1 (protocols) was committed before any production run; part 2
(results) was written afterwards. Scripts are in this directory; bulk output in `research/scratch/exam/`._

## Part 1. Protocols (fixed before running)

### Common conventions

- **Waiting times.** h = deaths / exposure, where exposure counts replica-generations at age ≥ T0 (age since the
  replica's soup) and a death is counted when the watched line is empty after a step taken from an exposed
  state. τ = 1/h per watched line, ln τ ± 1/√deaths (Poisson). A replica that dies, settles or meets a censoring
  event is reseeded with a fresh soup.
- **Censoring of periodic replicas (deterministic vessels).** A replica is censored (reseeded, not a death) when
  its whole state equals its state two generations back, or equals a snapshot taken at the last multiple of 64,
  4,096 or 262,144 generations: every period ≤ 262,144 is caught within at most 2 × 262,144 generations. At the
  end of every run I report the oldest living replica's age; a replica older than 40 τ would be a suspect
  undetected cycle (probability e^{−40} otherwise).
- **Transverse firewalls.** In periodic vessels three adjacent dead lines of any family that wraps the torus end a
  replica (censored): in 2D strips, three adjacent dead columns (and three adjacent dead interior rows); in gump
  slabs, three adjacent dead layers of each of the three oblique diagonals and three adjacent dead interior
  layers (`xp.gump_slab`'s event list). Counts of these events are reported.
- **Dice models are not censored** (they are Markov chains whose only absorbing state is the dead line).
- **Engine.** `research/theory/exponent/drv.c` (the exponent study's bit-sliced driver, 256 replicas), compiled
  from a copy `exam/drv16.c` whose only change is that the noise density's binary precision PB is 16 bits
  instead of 12 (so ρ = 0.472 is 0.471999 instead of 0.47192). Graphs from `research/theory/exponent/xp.py`.
  For symmetric soups (C-E1): `research/toy2d/t2d.c` (which supports seeding orbits), copied to `exam/t2dx.c`
  with a third snapshot level (262,144) added. New steppers: `exam/parity.c` (S-E1), `exam/ce2.c` (C-E2).
- **Validation before use** (each must pass, else the entry is not run with that code):
  V1 drv16 on D2(L, 0.472) rings, L = 12, 16, against the lab's exact ln τ 6.4169, 8.6350 (within 3σ);
  V2 drv16 on 16 × 16 strips of the 2D rule against `research/toy2d` (ln τ_edge 7.426 ± 0.016; within 3σ combined);
  V3 drv16 on the gump slab 3 × 4 × 12 against the exponent study (7.398 ± 0.007; within 3σ combined);
  V4 parity.c against an independent numpy stepper, bit for bit, on small vessels; and its row 0 rule against
  `research/toy2d/t2d.c` semantics (cross2, B34/S234);
  V5 ce2.c against exhaustive enumeration (numpy, independent code) of all soups at L = 3, k = 1, 2, 3 (exact
  equality of counts), and its sampled −ln P₁, −ln P₂ slopes against the lab's c₁ = 0.551535, c₂ = 0.467693;
  V6 t2dx.c bit-identical output to t2d.c on a short run (same graph, seed), and on the asymmetric gump hull R = 7
  against fluct's ln τ_face = 6.804 (within 3σ; different soup generator, same density 0.35, T0 = 200).
- **Budget rule.** Each run has a target number of deaths and a wall-time cap fixed below; it stops at whichever
  comes first. Stopping depends on time and counts, never on the value.

### P-E1 (probability). D2(L, 0.472) on a ring, slope of ln τ between L = 30 and 38

- Vessel/model: `xp.toy_model(1, L)`: one row of B34/S234 on a ring of L cells (in-row neighbours ±1, ±2), the two
  cells beneath each cell redrawn Bernoulli(0.472) every generation (both noise classes ρ = 0.472).
- Start: row Bernoulli(0.4) (drv's soup), reseeded at death. T0 = 50 (the entry: "ages below 50 not measured").
- L = 30, 34, 38. Targets: 1,500 / 600 / 250 deaths; caps 15 / 25 / 50 min of one core.
- Estimator: slope = (ln τ(38) − ln τ(30))/8 (the entry's "between L = 30 and L = 38"); secondary: weighted LSQ over
  the three sizes. Error from the Poisson errors.
- Holds if the slope lies in 0.48 ± 0.03 and in the entry's band (0.45, 0.51); **refuted** if ≥ 0.51 or ≤ 0.45
  (beyond 2σ of the measurement; otherwise "not decidable").

### Path E1. Notched strips of the 2D rule

- Vessel: `xp.toy_strip(16, L)` (cross2, B34/S234, periodic in x, rows outside dead) with cells (row 0, col 0) and
  (row 0, col 1) removed (neighbours read them as dead; they are not in the row-0 line). Row 15 intact (control).
- Soups p = 0.4, T0 = 300; censored: settling (any period ≤ 262,144), interior firewalls (3 dead rows), transverse
  cuts (3 dead columns), as `law.py`. L = 20, 24, 28, 32.
- τ_notch = exposure / deaths of row 0; τ_15 likewise for row 15.
- Targets 600 row-0 deaths per size; cap 12 min per size.
- Estimator as filed: Δ = ln τ_notch(32) − ln τ_notch(20), slope Δ/12; secondary: LSQ over the four sizes.
- Holds if the slope is within 0.345 ± 0.020 (Δ = 4.14 ± 0.24); **refuted** if ≥ 0.39 (the entry's criterion).
  Control: τ_15 should reproduce the intact strips (slope ≈ 0.41).

### Path E2. Remnant two generations before an edge dies

- Vessel `xp.toy_strip(16, L)` intact, L = 32, 36, p = 0.4, T0 = 300, censoring as E1.
- Statistic: mean population of the dying edge row two generations before the death (drv's pre-death profile, lag
  2: the count at generation t − 2 when the row is empty at t; both edges pooled; deaths at ages ≥ T0 + 66, drv's
  rule for profiles). This is the convention of the exponent study's F2 numbers the entry builds on
  (`report.py endgame`, lag 2). Error by batch means over chunks.
- Targets 400 deaths at L = 32, 300 at 36; caps 15 / 25 min.
- Holds if both means are within 9.8 ± 1.0 (allowing 2σ of the measurement); **refuted** if ≥ 11.5 at L = 36.

### Source S-E1. 2D rule over a parity bulk (new stepper `parity.c`)

- Cells (x, j), x ∈ Z_L, 0 ≤ j ≤ H, H = 400. Row 0: B34/S234 on the cross (in-row ±1, ±2; rows 1, 2 beneath).
  Rows 1…H: alive next iff the number of live cross neighbours is odd (in-row ±1, ±2; rows j ± 1, j ± 2; row 0
  counts; rows < 0 and > H are dead). Start: every cell Bernoulli(½).
- A replica ends when row 0 is empty (death), or at generation ⌊H/2⌋ = 200 (censored). Exposure at ages ≥ 30.
- L = 12, 14, 16; target 6,000 deaths each.
- Holds if each |ln τ − predicted| ≤ 3/√deaths (predicted 6.4282, 7.6056, 8.6764); hazard flat in age (hazard in
  ages 30–99 vs 100–199 equal within 3σ); P(row 0 empty next | one live cell in row 0, age ≥ 30) within 3σ of
  0.2373.

### Path E3. Gump's remnant on a rim-free slab face

- Vessel `xp.gump_slab(5, 4, 8)` (8 layers, periodic in-plane, A = 60 per face; two faces). Soups p = 0.35,
  T0 = 300 (the exponent study's slab convention; qsd.py's is 200, immaterial at τ ≈ 10⁵). Censored: settling,
  interior and oblique (transverse) firewalls.
- (i) mean face population at lags 1–4 before death (drv profile, both faces pooled); (ii) quasi-stationary
  histogram of the face population (living, exposed states; both faces), tail ratio p_k/p_{k+1} averaged
  (arithmetic mean of the 7 ratios) over 6 ≤ k ≤ 12; (iii) fraction of face deaths whose face had one live cell
  the generation before (drv's transition counts).
- Target 3,000 face deaths; cap 20 min.
- Holds by the entry's criteria: lag-3 and lag-4 means within 20% of 6.4 and 9.7, tail ratio in 0.57–0.69;
  sub-claims scored against their stated bars (1.6 ± 0.15, 3.4 ± 0.35, 6.4 ± 0.6, 9.7 ± 1.0; 0.63 ± 0.03;
  62 ± 5%).

### Source S-E2. Driven faces with dice at density ½

- Gump: `xp.gump_slab_model(3, 4, 6)` and `(4, 4, 6)`, noise classes ρ = 0.5, soups p = 0.35, T0 = 300 (the
  exponent study's convention for these models). 2D: `xp.toy_model(8, L)`, L = 16, 20, ρ = 0.5, p = 0.4, T0 = 300.
  Events: the face (edge) line empty = death; firewalls among the dynamic layers censor.
- Targets 4,000 deaths each; caps 10 min each.
- Holds if gump values are within 0.2 nats of 7.398 (A = 36), 9.936 (A = 48) (the entry's refutation threshold),
  scored also against the stated ± 0.08; 2D values against 7.43 ± 0.04, 9.16 ± 0.05.

### Counting C-E2. The 2D rule dead by generation 3 (new stepper `ce2.c`)

- Periodic strips, rows 0–6 (row 0 an edge: nothing above; the rows below 6 cannot reach row 0 by generation 3),
  every cell Bernoulli(½) at generation 0, no warm-up. P_k(L) = fraction of soups with row 0 empty at generation k
  (an empty row 0 stays empty), k = 1, 2, 3, L = 20, 24, 28, 32.
- Sample: up to 10⁹ soups at L = 32, fewer at smaller L (enough for ≥ 1,000 hits where affordable); cap 25 min.
- Estimator: weighted LSQ slope of −ln P₃ on L over the four sizes (binomial errors); also local slopes.
- Holds if the slope is within 0.447 ± 0.012; **refuted** if < 0.430 or > 0.468 (beyond 2σ).

### Counting C-E1 (revised). One mirror on gump hulls

- Vessel `xp.gump_hull(R)`, cube-centred, R = 13, 15, 17 (A = 84, 108, 135). Soups: one Bernoulli(0.35) draw per
  orbit of (x, y, z) ↦ (y, x, z); T0 = 200; settled replicas reseeded (any period ≤ 262,144); a replica ends at
  its first face death. τ_fix = 4 × exposure / (deaths of the four faces d = (+,+,±), (−,−,±)).
- Run after everything else, in the time left; sizes in the order 13, 15, 17; cost estimated from R = 13 first.
- Slope of ln τ_fix between A = 84 and 135 (or the sizes reached), against 0.105 ± 0.009; refuted below 0.094 or
  above 0.118. Also the fraction of first deaths that are fixed faces (predicted > 99%).

## Part 2. Results

Commands are run from this directory (`research/theory/swarm/exam/`); bulk files land in `research/scratch/exam/`.
Machine: 2 cores used. Every ln τ error is 1/√deaths.

### Validations (all passed)

| check | command | result | reference |
|---|---|---|---|
| V1 D2(12, 0.472) ring | `python3 exam.py v1` | 6.4033 ± 0.0113 (7,788 deaths) | exact 6.4169 (−1.2σ) |
| V1 D2(16, 0.472) ring | same | 8.6502 ± 0.0150 (4,439) | exact 8.6350 (+1.0σ) |
| V2 2D strip 16 × 16 | `python3 exam.py v2` | 7.3903 ± 0.0155 (4,145) | toy2d 7.426 ± 0.016 (−1.6σ comb.) |
| V3 gump slab 3 × 4 × 12 | `python3 exam.py v3` | 7.4023 ± 0.0154 (4,244) | exponent study 7.398 ± 0.007 (+0.3σ) |
| V4 parity.c stepper | `python3 check_parity.py` | identical to an independent numpy stepper, 4 vessels, 20–40 generations; light-cone pruning gives byte-identical output to unpruned (`NOPRUNE=1`) | — |
| V5 ce2.c | `python3 check_ce2.py`; `ce2 enum 4` vs the lab's `counting_r1.k2_weights/ring_sum` | L = 3, k = 1, 2, 3: counts equal to numpy enumeration (409,600 / 554,432 / 699,086 of 2²¹); L = 4, k = 2: 57,464,576 of 2²⁸, equal to the lab's transfer matrix | — |
| V5 sampled slopes k = 1, 2 | `python3 ce2_report.py` | 0.5418 ± 0.0073, 0.4791 ± 0.0023 at L = 20–32 | lab c₁ = 0.551535, c₂ = 0.467693 (asymptotic; finite-L slopes approach from above) |

`python3 report.py valid` prints the V1–V3 rows.

### Path E1 — notched strips: **holds**

`python3 exam.py e1 20,24,28,32; python3 report.py e1` (≈ 2 min of one core).

| L | row-0 (notched) deaths | ln τ_notch | row 15 (control) ln τ | toy2d intact row | transverse cuts (censored) |
|---|---|---|---|---|---|
| 20 | 908 | 8.517 ± 0.033 | 9.073 ± 0.044 | 9.055 | 125 |
| 24 | 1,234 | 9.900 ± 0.029 | 10.757 ± 0.044 | 10.768 | 996 |
| 28 | 1,278 | 11.320 ± 0.028 | 12.407 ± 0.048 | 12.368 | 4,726 |
| 32 | 1,297 | 12.666 ± 0.028 | 14.014 ± 0.055 | 14.051 | 20,804 |

ln τ_notch(32) − ln τ_notch(20) = **4.149 ± 0.043**, slope **0.3458 ± 0.0036** (LSQ over the four sizes 0.3465 ±
0.0034, χ² 1.2/2). Predicted 4.14 ± 0.24, slope 0.345 ± 0.020; refutation threshold 0.39. The intact control row in
the same strips has slope 0.412 ± 0.005 and reproduces toy2d's table within 1σ. Settled replicas: 1 in all four
runs; the oldest living replica was never older than the chunk it ran in (no undetected cycle). Interior firewalls
37 / 10 / 3 / 0. **Holds**, to 1/50 of its error bar: a row with a fixed dead anchor has the exponent 0.345 that
path's G1 assigns to every edge with an end, and the intact ring in the same vessel keeps its higher 0.41.

### Source S-E1 — the edge over a parity bulk: **holds**

`gcc -O3 -march=native -o ../../../scratch/exam/parity parity.c`, then in `research/scratch/exam/`:
`./parity run 12 400 85 1212 30 > se1_L12.txt; ./parity run 14 400 280 1414 30 > se1_L14.txt;
./parity run 16 400 810 1616 30 > se1_L16.txt`; `python3 se1_report.py` (≈ 1 min in all). H = 400, censored at 200.

| L | deaths | ln τ measured | predicted | difference / σ | hazard ages 30–99 vs 100–199 | P(row 0 empty next \| one live cell) |
|---|---|---|---|---|---|---|
| 12 | 4,975 | 6.4330 ± 0.0142 | 6.4282 | +0.34σ | 1.589 vs 1.623 × 10⁻³ (z −0.7) | 0.2397 ± 0.0036 (13,822 visits) |
| 14 | 5,776 | 7.5973 ± 0.0132 | 7.6056 | −0.63σ | 4.974 vs 5.050 × 10⁻⁴ (z −0.6) | 0.2410 ± 0.0033 |
| 16 | 5,907 | 8.6746 ± 0.0130 | 8.6764 | −0.14σ | 1.681 vs 1.728 × 10⁻⁴ (z −1.0) | 0.2340 ± 0.0032 |

(The deaths fell slightly short of the 6,000 target at L = 12, 14: the batch count was fixed in advance from a
guessed τ.) Every number is inside its three-sigma window (largest deviation 0.63σ), the hazard is flat in age,
and the one-cell escape probability is (3/4)⁵ = 0.2373 within 1.1σ at each size. Not checked: periodicity of the
whole state (each replica is censored at age 200, so an undetected cycle could add at most 170 generations of
exposure; none can inflate τ). **Holds**: the deterministic automaton's edge has the exact lifetime of the dice
chain D2(L, ½; 1), as Lemma 1 (source journal S2) says; the lemma, the lab's eigenvalues and this stepper agree.

### Counting C-E2 — dead by generation 3: **fails**

In `research/scratch/exam/`: `./ce2 sample 20 390625 141; ./ce2 sample 24 781250 169; ./ce2 sample 28 1171875 197;
./ce2 sample 32 1953125 225` (appended to `ce2.txt`; 2 × 10⁸, 4 × 10⁸, 6 × 10⁸, 10⁹ soups; ≈ 1 min); then
`python3 ce2_report.py`.

| L | soups | dead by gen. 1 | by gen. 2 | by gen. 3 | −ln P₃ |
|---|---|---|---|---|---|
| 20 | 2 × 10⁸ | 3,186 | 21,486 | 143,678 | 7.2385 ± 0.0026 |
| 24 | 4 × 10⁸ | 724 | 6,282 | 65,647 | 8.7149 ± 0.0039 |
| 28 | 6 × 10⁸ | 126 | 1,424 | 22,699 | 10.1824 ± 0.0066 |
| 32 | 10⁹ | 25 | 335 | 8,837 | 11.6366 ± 0.0106 |

Slope of −ln P₃: **0.3676 ± 0.0006** (LSQ, χ² 3.6/2; local 0.369, 0.367, 0.364). Predicted 0.447 ± 0.012; refuted
below 0.430. The same samples give 0.542 ± 0.007 and 0.479 ± 0.002 for k = 1, 2, against the lab's exact
asymptotic c₁ = 0.5515, c₂ = 0.4677 (so the method sees the known exponents; at k = 2 the finite-L slope is about
0.011 above its limit, a correction of the wrong sign to rescue the entry). **Fails**, by 6.6 of its own error
bars. The theorem c₃ ≤ c₂ is respected. What the outcome says, in the entry's terms: the third generation buys
far more than either guide allowed (c₂ − c₃ ≈ 0.10 against the predicted 0.02); c₃ already lies below the steady
exponent of the ring (0.38–0.42 at these lengths) and near path's 0.345 for edges with ends, so the fixed-age
hierarchy falls through the steady value by k = 3, as the critic's board reports for D2 at larger k.

### Path E2 — remnant two generations before an edge dies: **not refuted; the central value misses at L = 36**

`python3 exam.py e2; python3 report.py e2` (≈ 5 min of one core). Intact strips 16 × L, both edges pooled.

| L | edge deaths | ln τ_edge | lag 1 | **lag 2** | lag 3 | lag 4 | living mean |
|---|---|---|---|---|---|---|---|
| 32 | 719 | 13.973 ± 0.037 (toy2d 14.051 ± 0.038) | 2.04 ± 0.09 | **9.09 ± 0.08** | 13.14 ± 0.11 | 13.69 ± 0.17 | ≈ 18.5 |
| 36 | 420 | 15.428 ± 0.049 (toy2d 15.580 ± 0.045) | 1.83 ± 0.03 | **7.99 ± 0.38** | 11.95 ± 0.24 | 13.65 ± 0.50 | ≈ 20.8 |

Errors are batch means over 4 and 6 chunks of unequal size (crude; per-chunk lag-2 means at L = 36 range
7.0–8.5 over the three chunks with ≥ 100 deaths). Censored: 22,089 and 61,992 transverse cuts and firewalls; no
settled replica. (ln τ at L = 36 is 2.3σ below toy2d's table; L = 32 agrees at 1.5σ.)
Predicted 9.8 ± 1.0 at both sizes; refuted if ≥ 11.5 at L = 36. L = 32: inside the bar. L = 36: 7.99, below the
bar's lower end (8.8) by 2.1 of my (rough) errors. The refutation criterion is not met, by a wide margin.
**Verdict: not refuted; the prediction's central value holds at L = 32 and is too high at L = 36.** In the entry's
terms: the edge does not die in a flash from its living density (0.25 and 0.22 of the row two generations out,
against 0.58), and what is left two generations before death is a remnant of 8–9 cells whose size does not grow
with L; if anything it is still falling, which the "size-independent ten-cell remnant" reading did not say. The
pre-death curve (lag 4 ≈ 13.7 at both sizes) also shows the collapse starts three to four generations out.

### Path E3 — gump's remnant on a rim-free slab face: **fails** (lags 3, 4); lag 1, one-cell share and the tail window hold

`python3 exam.py e3; python3 report.py e3` (80 s of one core). Slab 5 × 4 × 8, A = 60, 3,188 face deaths
(ln τ_face = 12.480 ± 0.018, on the lead's slab line −0.091 + 0.2088·60 = 12.44). Censored: 1 interior and 14
oblique (transverse) firewalls, no settled replica, oldest replica 8.8 × 10⁵ generations (≈ 3.4 τ; chunk-limited).

| quantity | predicted (hull curve) | measured on the slab | within bar? | entry's refutation test |
|---|---|---|---|---|
| mean face population, lag 1 | 1.6 ± 0.15 | 1.663 ± 0.013 | yes | — |
| lag 2 | 3.4 ± 0.35 | 4.285 ± 0.035 | no (+26%) | — |
| lag 3 | 6.4 ± 0.6 | 10.70 ± 0.12 | no (+67%) | > 20% off: **refuted** |
| lag 4 | 9.7 ± 1.0 | 18.40 ± 0.18 | no (+90%) | > 20% off: **refuted** |
| tail ratio p_k/p_{k+1}, mean over k = 6…12 | 0.63 ± 0.03 | 0.677 ± 0.002 (ratios 0.683 … 0.662) | no | window 0.57–0.69: passes |
| share of deaths from a one-cell face | 62 ± 5% | 59.4 ± 0.9% | yes | — |

Profile errors: batch means over 4 chunks (crude, but the misses are 20–50 errors wide). Living mean face
population 31.0. **Verdict: refuted by the entry's own criterion** (lag-3 and lag-4 means differ from the hull's by
67% and 90%). In the entry's terms: the last generation (one cell, 60% of deaths) is the same object in hull and
slab, but the remnant's shrinking is not vessel-independent: the slab face goes from ≈ 18 cells to 0 in four
generations where the hull face takes about six, so √n falls by ≈ 1.0 per generation, not 0.59. The tail ratio is
within the refutation window but outside its bar, and slab and hull faces share a lifetime slope without sharing the
remnant curve, which is evidence against relation (M) being what ties them (path journal 11.3). The entry's own
named risk (journal entry 14: the hull's late curve is a corner or rim curve) is the likelier reading.

### Source S-E2 — driven faces over dice at density ½: **holds**

`python3 exam.py se2; python3 report.py se2` (≈ 30 s). Noise layers ρ = ½ (exact at PB = 16).

| model | deaths | ln τ measured | predicted | difference |
|---|---|---|---|---|
| gump D3(3 × 4, ½; w = 6), A = 36 | 12,968 | 7.3967 ± 0.0088 | 7.40 ± 0.08 (slab 7.398) | −0.001 |
| gump D3(4 × 4, ½; w = 6), A = 48 | 5,075 | 9.9446 ± 0.0140 | 9.94 ± 0.08 (slab 9.936) | +0.009 |
| 2D D2(16, ½; 8) | 12,759 | 7.4032 ± 0.0089 | 7.43 ± 0.04 | −0.027 |
| 2D D2(20, ½; 8) | 11,026 | 9.1504 ± 0.0095 | 9.16 ± 0.05 | −0.010 |

Firewall censoring among the dynamic layers: 113, 6, 854, 272 events. All four inside their bars; the gump values
are within 0.01 nats of the deterministic slabs' (criterion 0.2). **Holds.** In the entry's terms: six layers of the
true rule over structureless fair dice give the face exactly the lifetime it has over gump's own bulk, so whatever
randomness the face uses is made within six layers of it. (This was close to known for the 2D rule, exponent study
F9; for gump it is new.)

### Validation V6 (for C-E1)

`python3 ce1.py v6`: t2dx and t2d give identical output files on the R = 7 hull (30,000 generations); asymmetric
R = 7 hull, ln τ_face = 6.8067 ± 0.0012 (643,395 first-face deaths) against fluct's 6.804 ± 0.003.

### Counting C-E1 (revised) — one mirror on gump hulls: **holds**

`python3 ce1.py run 13 240; python3 ce1.py run 15 300; python3 ce1.py run 17 900; python3 ce1.py report`
(≈ 28 min of one core in all; it was affordable because the mirror needs no orbit reduction and a mirror-symmetric
face lives only e^9–e^14 generations).

| R | A | first deaths | of which a fixed face | ln τ_fix = ln(4 · exposure / fixed deaths) | settled |
|---|---|---|---|---|---|
| 13 | 84 | 351,357 | 351,282 (99.98%) | 9.0169 ± 0.0017 | 0 |
| 15 | 108 | 38,784 | 38,784 (100%) | 11.3951 ± 0.0051 | 0 |
| 17 | 135 | 4,051 | 4,051 (100%) | 14.2505 ± 0.0157 | 0 |

Slope of ln τ_fix between A = 84 and 135: **0.1026 ± 0.0003** (local 0.0991 and 0.1058: rising, like the
asymmetric faces' local slopes). Predicted 0.105 ± 0.009, refuted below 0.094 or above 0.118. First face to die
is a fixed face in > 99.9% of replicas (predicted > 99%). The swapped faces died (in mirror pairs) 75 times, all at
R = 13. Not checked: interior firewalls are not censored (as in `fluct/qsd.py`; they cannot remove a face); the
oldest replica (7.6 × 10⁵ generations at R = 17, ≈ 0.5 τ_fix) gives no sign of an undetected cycle.
**Holds.** In the entry's terms: a mirror through the face costs (A + cells on the mirror)/2 independent cells at
the asymmetric price, less a small mirror-line term; the measured slope is 0.47 of the asymmetric faces' ≈ 0.22,
inside the band "half, and not much more than half". The rising local slope (0.099 → 0.106) is the same
pre-asymptotic rise the asymmetric faces show.

### Probability P-E1 — D2(L, 0.472) on a ring, L = 30–38: **not decidable at the refutation line; the central value is disfavoured**

`python3 exam.py pe1 30; python3 exam.py pe1 34; python3 exam.py pe1 38; python3 report.py pe1` (≈ 85 min of one
core: 8, 25 and 51 min; L = 34 and 38 stopped at their caps, before their targets of 600 and 250 deaths).

| L | deaths | exposure | ln τ |
|---|---|---|---|
| 30 | 1,578 | 1.2 × 10¹⁰ | 15.843 ± 0.025 |
| 34 | 572 | 3.4 × 10¹⁰ | 17.900 ± 0.042 |
| 38 | 127 | — | 19.941 ± 0.089 |

Slope between L = 30 and 38: **0.512 ± 0.012** (LSQ over three sizes 0.513 ± 0.009, χ² 0.01/1; local 0.514,
0.510). Predicted 0.48 ± 0.03; refuted if ≥ 0.51 or ≤ 0.45. The measured slope sits on the upper refutation line
(+0.2σ two-point, +0.3σ LSQ): by the protocol fixed in advance this is **not decidable** at this sample, but the
predicted 0.48 lies 2.8σ (two-point) / 3.7σ (LSQ) below the measurement and the interval's exponent 0.460 lies
4–6σ below it. The exact ring steps at L = 15–19 were 0.522–0.528. In the entry's terms: out to L = 38 the ring has
not come down to the dead-ended interval's exponent; it has moved at most from ≈ 0.525 to ≈ 0.51, which is what a
ring that keeps its own exponent (or carries a slowly decaying excess) does, not the "step comes down to 0.48"
the entry expected. Deciding the threshold itself needs about 4× the L = 38 sample (≈ 3.5 core-hours) or L = 46.

## Not run, and not checked

- Every entry in the brief was run. Shortfalls: P-E1 reached 572 and 127 deaths at L = 34, 38 (targets 600, 250;
  time caps); S-E1 4,975 and 5,776 deaths at L = 12, 14 (target 6,000; batch counts fixed in advance).
- E2's and E3's error bars are batch means over 4–6 chunks: rough, though E3's misses are far outside them and
  E2's L = 36 miss is ≈ 2σ.
- S-E1: whole-state periodicity was not checked (each replica is censored at age 200). C-E1: interior firewalls not
  censored (they cannot remove a face).
- The engines were validated against exact values or earlier measurements (V1–V6), not bit for bit against
  `reference/oracle.py`; drv and t2d are the exponent study's and toy2d's engines, whose own validations stand.

## Summary

| entry | predicted | measured | verdict |
|---|---|---|---|
| P-E1 | slope 0.48 ± 0.03 (refuted ≥ 0.51) | 0.512 ± 0.012 | not decidable at the line; 0.48 disfavoured at 2.8σ |
| path E1 | slope 0.345 ± 0.020 | 0.3458 ± 0.0036 | holds |
| path E2 | 9.8 ± 1.0 at L = 32, 36 (refuted ≥ 11.5) | 9.09 ± 0.08, 7.99 ± 0.38 | not refuted; low at L = 36 |
| path E3 | lags 1–4: 1.6, 3.4, 6.4, 9.7; ratio 0.63; 62% | 1.66, 4.29, 10.70, 18.40; 0.677; 59.4% | refuted (lags 3, 4) |
| source S-E1 | 6.4282, 7.6056, 8.6764; 0.2373 | 6.433, 7.597, 8.675 (≤ 0.63σ); 0.234–0.241 | holds |
| source S-E2 | 7.40, 9.94; 7.43, 9.16 | 7.397, 9.945; 7.403, 9.150 | holds |
| counting C-E2 | c₃ 0.447 ± 0.012 (refuted < 0.430) | 0.3676 ± 0.0006 | fails |
| counting C-E1 | slope 0.105 ± 0.009 | 0.1026 ± 0.0003 | holds |
