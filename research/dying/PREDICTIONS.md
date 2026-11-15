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
