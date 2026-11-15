# How a face dies: forecasts and operational definitions

Committed before any run whose output could bear on them. Definitions below are fixed; later changes go in dated
notes at the end, the original text stays.

## The lead's forecasts (2026-11-15, written before any run), verbatim

Setting: R = 11 cube-centred hull, faces of 63 cells, groups as in the edge ladder; a death is the first face death of a life as `research/theory/symmetric/run.py` counts it. Rows are counted from each edge of the face inward; lag ℓ means ℓ generations before the death.

- L1 (a deduction from the ladder, not from pictures). The steps are equal in ln τ (−2.18, −2.17, −2.12). If a tied edge were an independent local channel for death, rates would add and two and three tied edges would give 10.82 and 10.43, not 9.29 and 7.17. So a death is an event of the whole face, to which each free edge adds a cost.
- L2. c1: just before death the rim outlives the interior. At lag 4 the mean occupancy of rows 1–2 along an edge is at least 1.5 times the interior's. Confidence 65%.
- L3. csz: along the mirrored edge that ratio is below 1.2, and lower than along each free edge by a factor of at least 1.3. Confidence 60%.
- L4. D2h: the ratio is within 0.8–1.2 on all three edges. Confidence 60%.
- L5. c1, the neighbours: over the last 16 generations before a face dies, each adjacent face's population stays within 10% of its stationary mean on average (confidence 75%), and so do its rows 1–2 along the shared edge, within 15% (confidence 55%).
- L6. Where emptying begins (the centroid of the vacated cells at the first generation from which the face's population stays below half its stationary mean): in csz it is nearer the mirrored edge than either free edge in 45–70% of deaths, against one third by chance; in c1 each edge gets one third within the error. Confidence 50%; I cannot derive this one.
- L7. The final plunge is faster when more edges are tied: the median time from that generation to the death shrinks by at least 25% from c1 to D2h. Confidence 55%.
- What would count against the "living neighbour" reading: in c1 the rim rows are not the late survivors (L2's ratio below 1.1), and csz shows no difference between its tied and free edges.

## Operational definitions (fixed 2026-11-15, before any run)

**Systems and runs.** `oct_11_c_G` for G = c1, csz, c2v, d2h, built by `research/theory/symmetric/geom.py`,
stepped by a copy of `research/theory/symmetric/sy.c` that adds a ring buffer of the last H = 512 generations of
every replica and writes it out at each death. Same seeds, generations and protocol as the symmetric study's
tabulated runs: c1 seed 1, 600,000 generations; csz seed 1, 400,000; c2v seed 1, 200,000; d2h seed 2, 400,000
(soup 0.4, events every 4 generations). The modified stepper's lives file must be byte-identical to `sy`'s for the
same arguments (this is the check that the replay reproduces every death time), and a sample of written histories
is stepped by the Rust engine on the full cell set and must agree at every generation.

**Which deaths.** A death is a life that ends F or X (as `run.py` counts) at age > T0 = 512 generations. At most
the first 3,000 such deaths of each run (in the order they are written) are used; all of them if fewer.

**Death generation and lags.** The life ends at a check (every 4 generations). From the history, t_d is the first
generation at which some face orbit has no live cell (dead for ever by T2). Lag ℓ is the state at generation
t_d − ℓ: lag 0 is the first generation with the face empty, lag 1 the last with any of its cells alive.

**The dying face.** A face orbit empty at t_d. If several face orbits are first empty at the same t_d, each is a
sample with weight 1/k (k the number of them); the count of such deaths is reported. For a symmetric group one face
of the orbit stands for it (the others are its images, with identical canonical pictures).

**Canonical face.** The face with sign vector σ ∈ {±1}³ (cells with σ·p = 11, all doubled coordinates of σ⊙p ≥ 0)
is mapped to the +++ face by p → σ⊙p. Edge a ∈ {x, y, z} of the canonical face is the row of cells with coordinate
a = 0 (shared with the face across the plane a = 0). Tied edges: csz z; c2v x and y; d2h x, y and z; c1 none.

**Rows, bands, interior.** Row k along edge a: cells of the canonical face with coordinate a = k − 1 (doubled units;
row 1 is the shared rim row of 12 cells, row 2 the 6 cells with a = 1). The **edge band** B_a ("rows 1–2 along an
edge") is rows 1 and 2 minus the three apex cells (11,0,0), (0,11,0), (0,0,11): 16 cells; neighbouring bands share
two cells near each corner, which count in both. The **interior** I is the 18 cells with min(x, y, z) ≥ 2 (every
face cell that is in no band and is not an apex).

**Occupancy and ratio.** occ_S(ℓ) = mean over death samples (weighted) of the fraction of the cells of S alive at
lag ℓ. The ratio along edge a at lag ℓ is occ_{B_a}(ℓ) / occ_I(ℓ) (ratio of means). Errors: bootstrap over deaths
(1,000 resamples), one standard deviation. Where a forecast speaks of "an edge" in c1, the three edges are pooled
(mean of the three bands); each is also reported. In csz the free-edge ratio is the pooled x, y value and each is
also reported.

**Null control (stationary).** Every gens/10 generations of the job, each replica with age > T0 has its state
recorded; a record is kept only if its life then lasts at least 64 more generations and does not end settled (S);
records of lives open at the end of the job are kept if 64 generations remain after them. For each group, every
face orbit of every kept record is a null sample (canonical map as above). From these: P̄ the stationary mean face
population (cells of the 63 alive), ρ_i the stationary occupancy of each canonical cell, the stationary band and
interior occupancies, and the stationary ratio.

**L2–L4** use the ratio at lag 4 as defined. L2 holds if the pooled c1 ratio ≥ 1.5. L3 holds if the csz z ratio
< 1.2 and (x ratio)/(z ratio) ≥ 1.3 and (y ratio)/(z ratio) ≥ 1.3. L4 holds if all three D2h ratios are within
0.8–1.2. A forecast is "undecided" if the decision flips within one bootstrap standard deviation of the number.

**L5** (c1 only). The adjacent faces of a dying face σ are the three faces σ with one sign flipped; each is put in
its own canonical frame, where the shared edge is again edge a. Part 1: the mean over death samples, the three
neighbours and lags 1–16 of (neighbour face population)/P̄ lies in [0.90, 1.10]. Part 2: the same for the
neighbour's band along the shared edge, occ/(stationary band occupancy), in [0.85, 1.15]. The per-lag curves are
reported too.

**L6.** P(t) is the dying face's population. t_h is the earliest generation t ≤ t_d with P(t') < P̄/2 for every
t' in [t, t_d]. If P < P̄/2 over the whole recorded history (512 generations back from the check), the death is
censored (counted, excluded from L6, counted as Δ > history for L7). The vacated-cell centroid is
c = Σ_i w_i p_i / Σ_i w_i over the canonical face cells, w_i = ρ_i − x_i(t_h). The edge it is nearest is the a
minimising c_a (distance from edge a is proportional to c_a). L6 holds for csz if the fraction with argmin = z is
in [0.45, 0.70]; for c1 if each edge's fraction is within two binomial standard errors of 1/3. (For c1 this is
forced by the ensemble's symmetry and so tests the code, not the dynamics.)

**L7.** Δ = t_d − t_h. L7 holds if median Δ(d2h) ≤ 0.75 · median Δ(c1) (censored deaths enter the median as
"larger than any measured"). Medians of csz and c2v are reported.

## My own forecasts (2026-11-15, before any run)

- K1 (60%). L5 part 2 fails: the neighbour's band along the shared edge is depressed by more than 15% on average
  over lags 1–16, since the shared rim row is common to both faces and is empty at lag 0. Part 1 holds.
- K2 (55%). L2 fails: the c1 lag-4 ratio is below 1.5. (A rim cell has 7 neighbours inside the hull against 9 for
  an interior cell; I expect the rim to be held up by the neighbour only weakly, not to outlive the interior.)
- K3 (50%). The c1 median plunge Δ is between 8 and 64 generations.
- K4 (50%). In D2h the lag-4 ratio is below 1 on all three edges (with every neighbour in lockstep the rim, having
  fewer neighbours, empties first).

## Notes added after the data (2026-11-15)

1. No definition above was changed. The scores are in README.md.
2. Added after seeing the first results, so not forecasts: `explore.py` (each region's occupancy over its own
   stationary value; the layers beneath the dying face; a version of L6 that ranks edges by relative deficit, because
   the pre-registered deficit centroid w_i = ρ_i − x_i inherits the stationary profile: a face that empties in
   proportion to ρ has its centroid pulled away from a depleted edge), and the stationary occupancy by row.

# Round 2 (committed 2026-11-15, after round 1, before any round-2 run)

## THE LEAD'S FORECASTS, ROUND 2 (2026-11-15, after round 1, before any round-2 run), verbatim

What I now think and want tested: a death is a fast collapse of the whole face from an ordinary-looking state, ties change how often a collapse starts and not how it runs, and the face population P alone may or may not be the variable that decides. Known going in: sigma_P is 5.24 in c1 and 6.37 in D2h (your README); a Gaussian extrapolation of P to zero gives ln tau about 17.8 for c1 (measured 13.63) and 7.0 for D2h (measured 7.17), so it is not obviously right or wrong.

A. Excursions, from long stationary traces of each face's population P(t), fresh seeds, all four groups at A = 63. For levels p = 0.9, 0.8, ..., 0.1 of the stationary mean: nu(p), the rate per face per generation of excursions that start above the mean and reach p; and q(p), the fraction of those that end in the face's death before P is back above the mean. (Then nu(p) q(p) should equal the death rate at every level: use that as the check.)
- A1. In c1 the level where q = 1/2 lies between 0.25 and 0.5 of the mean: a face that has lost 40% of its cells usually recovers. Confidence 50%.
- A2. In c1, ln nu(p) follows the Gaussian const - (Pbar - p)^2 / (2 sigma_P^2) to within 1.0 down to p = 0.6 Pbar. Confidence 50%.
- A3. The ladder is in nu, not in q: at p = 0.5 Pbar, q differs by less than a factor of 3 between c1 and D2h, while nu differs by more than e^4. Confidence 55%.
B. Single deaths: is the fade uniform inside each death, or a hole at a random place that spreads (which the mean maps would hide)? Use a statistic of your choosing, fixed in advance, that compares the spatial concentration of the missing cells at the start of the final plunge with faces of the same population drawn from the stationary sample.
- B1. Uniform: the concentration is within 15% of the stationary comparison in c1 and in D2h. Confidence 55%.
C. Births or deaths: in the run-up, which fails first?
- C1. Births: at the generation from which P stays below 0.8 Pbar, births per empty site are down by at least 30% against stationary while survival per live cell is down by at most 15% (c1). Confidence 55%.
D. Is the ladder a function of the stationary state? Measure Pbar and sigma_P for c1, csz, c2v, D2h at A = 84 (the symmetric study has ln tau there: steps -2.64, -2.65, -2.84), stationary sampling only.
- D1. At A = 84 the stationary population falls by 2.8 to 3.1 cells per tied edge (the A = 63 figure of 2.5 scaled by the edge length), and ln tau lost per stationary live cell lost is 0.86 +- 0.10, as at A = 63 (0.885, 0.850, 0.844 from your table). Confidence 50%.
- D2. Neither P^2/(2 sigma^2) nor any other function of (Pbar, sigma_P) alone reproduces all eight ln tau values (two sizes, four groups) to within 0.5. Confidence 60%.

## Round-2 definitions (fixed before any round-2 run)

Common. Round-1 definitions hold unless restated (canonical face, bands, interior, lags, T0 = 512, t_h). P(t) is the
number of live cells of one face (63 cells); for a symmetric group one face per face orbit ("per face" means per
face orbit, as nf in `run.py`). P̄ and σ_P at A = 63 are round 1's null values (P̄ = 31.29, 28.83, 26.29, 23.77;
σ_P = SD of P over the null faces: 5.24, 5.56, 5.96, 6.37), fixed, not re-estimated.

**A (excursions).** New stepper `ex.c` (a copy of `sy.c`, lives file again checked byte-identical to `sy`'s for the same
arguments) computes every face orbit's P at every generation, for every replica, and follows excursions online.
Fresh seeds: c1 seed 11, 1,200,000 generations; csz seed 11, 400,000; c2v seed 11, 200,000; d2h seed 12, 400,000
(512 replicas, soup 0.4, checks every 4). Only generations at life age > T0 count. An excursion starts at the first
generation t with P(t) < P̄ after a generation with P ≥ P̄ (the previous generation must also be at age > T0). It ends
recovered at the first later generation with P ≥ P̄, dead when that face's orbit is empty (P = 0), or censored (the
life ends for another reason first: another face's death, settling, or the end of the job). For each excursion the
minimum P reached and the end type are recorded. Exposure E_f = face-orbit generations at age > T0. "Reaches level p"
means min P < p·P̄. ν(p) = (excursions reaching p) / E_f; q(p) = (those ending dead) / (those reaching p and not
censored). Check: ν(p)·q(p) against the face death rate (face deaths at age > T0 counted from the same run, per E_f);
they agree up to censored excursions, whose share is reported. Errors: Poisson / binomial.
- A1: p* = the level where q crosses 1/2, linear interpolation on the grid p = 0.05, 0.10, …, 0.95. Holds if
  0.25 ≤ p* ≤ 0.5.
- A2: G(p) = −(P̄ − pP̄)²/(2σ_P²) with c1's σ_P = 5.24; the constant is fixed by matching ln ν at p = 0.9. Holds if
  |ln ν(p) − const − G(p)| ≤ 1.0 at p = 0.8, 0.7, 0.6.
- A3: holds if 1/3 < q_c1(0.5)/q_d2h(0.5) < 3 and ν_d2h(0.5)/ν_c1(0.5) > e^4.

**B (concentration).** Fresh histories from `sd.c` (round 1's stepper): c1 seed 21 600,000; d2h seed 22 400,000 (and
csz seed 21 400,000, c2v seed 21 200,000, reported, not scored), first 3,000 deaths, H = 512, lives files checked
against `sy`. At t_h of each death (round-1 definition) take the live cells of the dying face, k of them. Statistic
S = distance (doubled units, in the face plane) from the centroid of the live cells to the centroid of the face
weighted by ρ (the stationary occupancy of each canonical cell); a fade that is a hole at one place moves the
live-cell centroid away from the hole and makes S large. Comparison: for each death, 20 stationary faces drawn at
random from that group's null sample (round-1 definition, regenerated by these runs), each thinned uniformly at random
to exactly k live cells (if a drawn face has fewer than k live cells, draw again). Concentration ratio = mean S
(deaths) / mean S (thinned stationary). Deaths with k < 2 are skipped (counted). Error: bootstrap over deaths. B1
holds if the ratio is within 0.85–1.15 in both c1 and d2h. Secondary statistic, reported, not scored: the fraction of
live-live pairs among the kagome-adjacent pairs (in-face perpendicular neighbours) touching a live cell, against the
same thinned comparison.

**C (births or deaths).** Same fresh histories. t_8 = the earliest generation t ≤ t_d from which P < 0.8 P̄ holds at
every generation up to t_d (censored if over the whole history). At the step t_8 → t_8 + 1, over the dying face's 63
cells, pooled over deaths: birth rate b = Σ (dead at t_8, alive at t_8+1) / Σ (dead at t_8); survival s = Σ (alive at
both) / Σ (alive at t_8). Stationary reference: the same pooled over every step at lags 256 → 255, …, 500 → 499 of the
same histories. C1 holds (c1) if b/b_stat ≤ 0.70 and s/s_stat ≥ 0.85. All four groups reported; also at t_h and at
lags 16, 8, 4.

**D (A = 84 stationary).** `oct_13_c_{c1,csz,c2v,d2h}`, `sd.c` with no dumps (MAXD 0), seeds 31, 1 replica set,
200,000 generations each (null sampling at ten times, round-1 rule: kept if the life lasts 64 more generations and does
not end settled). P̄ and σ_P over every face orbit of every kept record. ln τ at A = 84 are the symmetric study's: c1
18.141 (GPU), csz 15.506, c2v 12.857, d2h 10.022; at A = 63 13.634, 11.456, 9.291, 7.168.
- D1: steps ΔP̄ (c1→csz, csz→c2v, c2v→d2h) at A = 84 each in 2.8–3.1, and each Δln τ/ΔP̄ in 0.76–0.96.
- D2: holds if both of these leave some residual above 0.5 on the eight points: (i) ln τ = a + b·P̄²/(2σ_P²), least
  squares; (ii) ln τ = a + b·P̄ + c·σ_P, least squares. (A good fit of either fails D2.)

## My round-2 forecasts

- K5 (50%). The c1 level where q = 1/2 is between 0.4 and 0.7 (higher than A1's range): once a face is down to about
  half it rarely comes back.
- K6 (60%). A2 fails with ν above the Gaussian at p = 0.6 (the tail is fatter than Gaussian, as the extrapolation's
  17.8 against 13.6 suggests).
- K7 (50%). B1 fails in c1: S at t_h exceeds the thinned stationary by more than 15% (a collapse starts somewhere,
  and information travels one cube per generation).
- K8 (55%). A3's q part holds and the ν part holds.

# Round 3 (committed 2026-11-15, after round 2, before any round-3 run)

## THE LEAD'S FORECASTS, ROUND 3 (2026-11-15, after round 2, before any round-3 run), verbatim

- T1 (one curve across sizes, c1). nu(p), q(p), Pbar, sigma_P for c1 at cube-centred R = 9, 11, 13 and, for the levels you can reach, R = 15. (a) -ln nu(0.5)/A at A = 84 agrees with A = 63 (0.103) within 5%. Confidence 60%. (b) The straight-line slope of ln nu per live cell lost, fitted over 0.1 <= p <= 0.45 (or as deep as the data go at A = 84, stated), is within 7% of 0.499. Confidence 55%.
- T2 (coexistence). In c1 stationary faces caught at P <= 0.3 Pbar, the occupancy profile against distance from the survivors' centroid is flat-topped: the inner half of the survivors sit in a region whose occupancy is at least 0.8 of the stationary value, and the profile falls from there to below 0.2 of stationary within 2 rows. Confidence 50%.
- T3 (where the survivors sit). In csz faces at P <= 0.3 Pbar, after correcting for the stationary profile (your round-1 lesson), the survivors' centroid is nearest the tied edge in fewer than 25% of cases (one third by chance): a thin face holds on at its free edges. Confidence 45%.
- T4 (how a thin face refills). In c1 recoveries from P <= 0.3 Pbar, at least 70% of the first ten births on the face are within two cells of a face cell that was alive at the bottom of the dip (regrowth from the clump), against the fraction expected if births fell on empty cells at random, which you compute. Confidence 55%.
- What would count against the reading: the curves at different sizes do not collapse per site (T1a off by more than 15%), and depleted faces show no clump with an edge (T2's profile falls smoothly over the whole face).

## Round-3 definitions (fixed before any round-3 run)

**Stepper.** `ex3.c` = `ex.c` with faces of up to 127 cells and dumps of deep excursions: for every excursion whose
P reaches ≤ M3, the face orbit's 63 cell states at every generation from the first with P ≤ M3 to the end of the
excursion (cap 512 generations, flagged if truncated), with its end type and minimum. Checked before use: on a short
D2h run its lives file, excursion table and P histogram are identical to `ex.c`'s. Every production lives file is
compared with `sy`'s.

**Runs** (soup 0.4, checks every 4, T0 = 512, 512 replicas):
- c1, cube-centred, R = 9 (A = 45) seed 51, 400,000 generations; R = 11 (A = 63) seed 52, 1,200,000, M3 = 9
  (= ⌊0.3·31.29⌋); R = 13 (A = 84) seed 53, 1,200,000; R = 15 (A = 108) seed 54, 1,200,000.
- csz, R = 11, seed 52, 400,000, M3 = 8 (= ⌊0.3·28.83⌋).
- P̄ (which sets the excursion threshold) and σ_P: R = 11 c1 31.29 and csz 28.83 (round 1); R = 13 42.49 (round 2);
  R = 9 and 15 from a null run of `sd.c` (seed 41, 100,000 generations, no dumps, round-1 null rule) made before the
  `ex3` run, rounded to 0.01.
- Slab, without a forecast: `hex_4_1_c1` (a face torus of area 63, eight layers, no rim) if
  `python3 research/theory/symmetric/validate.py 1500 hex_4_1_c1` prints ALL OK; P̄ from `sd.c` null seed 41
  100,000 generations; `ex3` seed 55, 400,000 generations. A life also ends at a firewall there (censoring).

**T1.** ν(p) as round 2 (levels p = 0.05 … 0.95, min P < p·P̄). (a) −ln ν(0.5)/A at A = 84 against the same at
A = 63 from the round-3 R = 11 run; holds if within 5% (the round-2 value 0.1034 is reported too). (b) Slope s: least
squares of ln ν(p) against p·P̄ (live cells) over the levels 0.10 ≤ p ≤ 0.45, weighted by the number of excursions,
levels with fewer than 20 excursions dropped (the range used is stated); s per live cell lost; holds if |s/0.499 − 1|
≤ 0.07 at A = 84. The same fit is reported at every size, and the straight part's extrapolation to p = 0 divided by A.

**Caught faces.** The first recorded state of each deep excursion (the first generation with P ≤ M3), all end
types; faces with fewer than 3 live cells skipped (counted). In-plane coordinates as round 2 (doubled units); ρ_i
the round-2 c1 / csz null occupancy of canonical cell i (fresh seeds, round 2); row spacing ℓ = √1.5 doubled units.

**T2** (c1, R = 11). For each caught face: survivors' centroid c (unweighted mean of the live cells' positions);
r_half = median distance of the live cells from c. Relative occupancy of a region = Σ over faces of live cells in it
/ Σ over faces of Σ ρ_i over its cells. Inner region: d ≤ r_half. Shells j = 0, 1, 2, …: r_half + jℓ < d ≤ r_half +
(j+1)ℓ. Holds if inner ≥ 0.8 and shell j = 1 < 0.2. Control: the same for a stationary face thinned uniformly to the
same k (one per caught face).

**T3** (csz, R = 11). Corrected centroid of a caught face: Σ_i (x_i/ρ_i) p_i / Σ_i (x_i/ρ_i), canonical (x, y, z);
nearest edge = argmin of its coordinates. Holds if the fraction nearest the tied edge z is below 0.25. Control: the
same for thinned stationary csz faces.

**T4** (c1, R = 11). Recovered deep excursions, not truncated. Bottom = first generation in the record with P equal
to the excursion's minimum; B = live cells there. Births on the face at t → t+1 (dead at t, alive at t+1) for t =
bottom, bottom+1, …, until the cumulative count reaches 10 (all births of the last such generation counted). "Within
two cells" = graph distance ≤ 2 from B in the in-layer neighbour graph of the face (each cell's 6 in-layer gump
neighbours that lie in the face). Observed fraction pooled over excursions. Random: for each counted generation, the
fraction of the face's empty cells at t within distance ≤ 2 of B, weighted by that generation's births. Holds if the
observed fraction ≥ 0.70 (the random figure is reported beside it).

## My round-3 forecasts

- K9 (60%). T1a holds: −ln ν(0.5)/A is size-independent within 5% (Gaussian and tail parts both scale with A if P̄ and
  σ_P² do).
- K10 (50%). T1b fails: the slope per cell at A = 84 is more than 7% below 0.499.
- K11 (60%). T2 fails: no plateau of 0.8 in the inner region (the survivors of a thin face are a loose clump, not a
  patch of stationary soup).
- K12 (55%). T4: the observed fraction exceeds the random one by less than 0.10, because distance 2 already covers
  most of a 63-cell face around ~9 survivors.
