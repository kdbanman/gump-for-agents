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
