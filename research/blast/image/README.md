# blast/image: the density law of a wrapped face, from its own image

Agent `image` of the blast of 2026-11-18. Question: derive ρ = ρ∞ − Σ_v f(|v|²) (research/wraplocal) from
quantities measured on a face WITHOUT the loop. Marks: [proved], [measured], [conjectured].

## Answer (04:05 UTC; three production runs, 13 minutes of one core)

1. **The law's form has a proof; its numbers do not yet have a derivation.** A torus is its loop-free cover
   conditioned on the seam's whole history recurring one loop along and reweighted by 1/probability of that history
   (identity ★ below) **[proved; brute-force checked on small automata]**. From ★: loops add to first order, the
   deficit is per cell and independent of the tube's length, it falls with |v| at the rate at which a band of the
   loop-free face and its translate become independent (patterns *and histories* included), and f > 0 exactly when
   the histories that recur at distance v more often than chance are emptier than average.
2. **The picture at one instant carries none of it [measured].** Lowest-order formula (window = what recurs),
   loop² 9, against f = 0.006267: one cell +0.000003 ± 0.000001; the cell and its 6 in-layer neighbours −0.00044 ±
   0.00011 (wrong sign); the cell and its 9 slab neighbours −0.00031 ± 0.00027. The 10-cell pictures at distance 3
   are independent to Z − 1 = (1.0 ± 0.9) × 10⁻³.
3. **The history carries it, and it is the dead that recur [measured].** The cell's own history over 3, 6, 9
   generations gives f_W(9) = +0.00019 ± 0.00011, +0.00062 ± 0.00006 (three runs), +0.00104 ± 0.00022: 3%, 10%, 17% of
   f, right sign, growing with the history's length. Of the 6-generation value, histories that end in three dead
   generations add +0.00061, those ending in three live ones −0.00010, all others +0.00008. A cell that died and
   stayed dead recurs at distance 3 about 1% more often than chance (r − 1 = 0.6–1.2%; "died five generations ago,
   dead since": 1.24% ± 0.05%), a hundred times the pair correlation's 0.009% (C(v)/ρ(1−ρ)).
   **Why emptier: what a face shares with its image is where it has gone quiet, and quiet is mostly dead.**
4. **Summing the first order over the neighbouring cells overshoots, with the right profile [measured].** The
   same tilt read in the 53 face cells round the window (= the first-order sum over those cells' windows) gives
   0.0183 ± 0.0012 at loop² 9 (2.9 f, still rising with the patch: 0.0006, 0.0038, 0.0110, 0.0183 at 1, 7, 25, 53
   cells), so neighbouring windows are redundant and first order is not enough. Its ratio to f is the same at the
   four lengths measured: 2.9 ± 0.2, 2.4 ± 1.1, 2.7 ± 0.8, 3.3 ± 2.3 at loop² 9, 12, 13, 16. **One number (0.34,
   fixed at loop² 9) times a function measured without the loop gives f(12) = 0.0019 ± 0.0009, f(13) = 0.0015 ±
   0.0004, f(16) = 0.0009 ± 0.0006 against 0.0023, 0.0016, 0.0008** — within 1σ, but the errors are 30–70%, the
   number depends on the patch, and loop² ≥ 19 was not reached. This is the brief's target met at four lengths to a
   factor 1.5, not at eight lengths to a few per cent.
5. **The delayed pair correlation exists and is far too small [measured].** C(v, τ) = Cov(x(c,t), x(c+v,t−τ)) at
   loop² 9: +22 ± 9 at τ = 0, +68 ± 9 at τ = 3 (the graph distance of one sublattice), +32 ± 9 at τ = 4 (× 10⁻⁶);
   at loop² ≥ 12 no lag stands out. Pair correlations, equal-time or delayed, are 10⁻⁴ of ρ(1−ρ); the recurrence of
   dead runs is 10⁻².
6. **Not reached:** a closed formula. The single window undershoots (10–17% at loop² 9), the first-order sum
   overshoots (≥ 2.9), and the truth needs the joint recurrence of neighbouring histories (second cluster order).
   The conditioned ensemble (κ) was dropped on the PI's instruction of 03:32.

Forecasts: `PREDICTIONS.md`, blocks 1–3, each committed before its run (39a7868, b0c6402, 87e69d8). Scores below:
2 of 7, 0 of 1 (three not run), 1 of 6 by the letter.


## The identity [proved; checked by brute force on small automata]

Let T be a face torus with a loop vector v, and C its cover unwrapped along v (the same slab with v replaced by
K·v, K ≥ 2; K → ∞ is a face without that loop). Start both from a soup (independent cells) at generation 0 and
look at whole histories x(c, t), 0 ≤ t ≤ t₁. The probability of a history is a product of local factors: the
soup weight of each cell, and for every cell and generation the indicator "x(c, t+1) = rule(x on c and its 12
neighbours at t)". Cut the tube across v into m ≥ 2 bands of cells s₀, …, s_{m−1}, each band **two graph steps
thick** (an inner and an outer half, so that the neighbours of every cell of band j lie in bands j or j ± 1 and each
rule factor touches at most two consecutive bands). Then

    P_T(s₀, …, s_{m−1}) = Π_j 𝒯(s_j, s_{j+1}) / Tr 𝒯^m      (s_m ≡ s₀),

with 𝒯 a non-negative transfer matrix on band histories, and the cover has the same 𝒯 on K·m bands. Comparing the
two products term by term (three lines),

    P_T(s₀, …, s_{m−1}) = P_C(s₀, …, s_{m−1}, and s_m = s₀) / [π(s₀) · Z],        Z = Σ_s P_C(s_m = s | s₀ = s),

where π(s) is the cover's probability of the band history s (for finite K: 𝒯^{(K−1)m}(s, s)/Tr 𝒯^{Km} in place of
π(s)·const). In words: **a torus is its cover conditioned on the seam's whole history recurring one loop along,
divided by how likely that seam history is.** Summing over the bands between,

    P_T(seam history = s) = π(s) · Q(s) / Z,     Q(s) = P_C(s_m = s | s₀ = s) / π(s)     ("recurrence ratio"),

and for any window W of cells and generations inside the seam, exactly,

    P_T(pattern π on W) = P_C(π on W) · E_C[ Q | π on W ] / Z.                                   (★)

Nothing here is specific to gump: it holds for any deterministic or probabilistic cellular automaton started from a
product measure, at every finite time, and so for the long-lived living state.

`python3 research/blast/image/chk_identity.py` (1 s): elementary automata 110, 30, 22 on rings of 4–6 cells against
their 2- and 3-fold covers, every history enumerated: the ratio P_T / P_C(·, seam recurs) depends on the strip's
history only through the seam's (largest spread 3 × 10⁻¹⁵), and with a seam ONE cell thick (not a separator) it
does not (spread 0.84): PASS.

What (★) says about the law:
- **Loops add** to first order: a torus with several short loops has one recurrence factor per loop direction, and
  Q − 1 is small.
- **Per cell, whatever the tube's length**: Q is a property of the seam, local along the tube.
- **The rate e^(−2.3|v|)** is the decay of the dependence between a band of the loop-free face and its translate by
  v, patterns and histories included: the gap of 𝒯. It is a *static* property of the loop-free living state's
  space-time measure, not a signal travelling round: hence no trace of the speed limit, and a Euclidean
  dependence on |v| rather than on the graph distance.
- **The pair correlation need not carry it.** f is Cov_C(x_c, Q)/Z: the excess recurrence of whole patterns,
  weighted by whether their centre is alive. The one-cell window gives f₁ = −C(v)(1−2ρ)/(ρ(1−ρ)) ≈ 0.14·C(v),
  which is 10⁻⁵ or less.
- **Sign**: f > 0 iff the patterns (histories) that recur at distance v more often than chance are emptier at
  their centre than the average pattern.

## The lowest-order formula and its test [measured]

If the rest of the seam is independent of the window and of its image, E_C[Q | π on W] is the window's own
recurrence ratio r_W(π) = P_C(pattern at W+v is π | pattern at W is π)/P_C(π), and (★) becomes a formula in
loop-free quantities with nothing fitted:

    f_W(v) = ρ − Σ_π x_c(π) P₂(π,π)/P(π) / Σ_π P₂(π,π)/P(π),

P the law of the window's pattern and P₂ the joint law of the patterns at W and W+v. It converges to f as W grows
to the seam. Windows tried: `c1` the cell; `c7` the cell and its 6 in-layer neighbours; `c10` the cell and its 9
neighbours in the slab (which fixes the cell's next state); `h6` the cell at 6 consecutive generations.

Production runs on (13,0),(0,13) (commands under Method; outputs in `data/`):

| loop² | one cell | cell + 6 in-layer | cell + 9 in slab | own history, 6 gen. (3 runs) | own history, 9 gen. | f (wraplocal) |
|---:|---:|---:|---:|---:|---:|---:|
| 9 | +0.000003 ± 0.000001 | −0.000438 ± 0.000106 | −0.000314 ± 0.000272 | **+0.000620 ± 0.000058** | +0.001041 ± 0.000224 | 0.006267 |
| 12 | 0.000000 ± 0.000001 | −0.000074 ± 0.000042 | +0.000205 ± 0.000279 | +0.000093 ± 0.000049 | +0.000005 ± 0.000218 | 0.002317 |
| 13 | 0.000000 ± 0.000001 | +0.000124 ± 0.000028 | −0.000076 ± 0.000090 | +0.000114 ± 0.000033 | −0.000161 ± 0.000297 | 0.001605 |
| 16 | 0.000000 ± 0.000001 | −0.000039 ± 0.000134 | −0.000316 ± 0.000276 | +0.000162 ± 0.000064 | −0.000113 ± 0.000188 | 0.000768 |
| 19 | 0.000000 ± 0.000001 | −0.000059 ± 0.000115 | +0.000070 ± 0.000182 | +0.000042 ± 0.000062 (1 run) | — | 0.000275 |
| 21 | 0.000000 ± 0.000000 | +0.000029 ± 0.000088 | +0.000143 ± 0.000138 | +0.000079 ± 0.000085 (1 run) | — | 0.000181 |
| 25 | 0.000000 ± 0.000001 | +0.000117 ± 0.000159 | +0.000403 ± 0.000257 | +0.000087 ± 0.000103 (1 run) | — | 0.000079 |

(`data/rec_s11_out.txt`, `data/hist_s21_out.txt`, `data/patch_s31_out.txt`; the 6-generation column is the weighted
mean of the three runs, χ² 0.3, 1.4, 0.5, 1.9 on 2. Errors are from only 4 blocks per run: each is itself uncertain
by about 40%.) The 6-generation history's share of f is 9.9 ± 0.9%, 4.0 ± 2.1%, 7.1 ± 2.1%, 21 ± 8% at loop² 9, 12,
13, 16: not one number (χ² 9 on 3), so the single window is not "f up to a constant". The 12-generation history
(4,096 patterns) and two neighbouring cells' 6-generation histories were too noisy to use (+0.0006 ± 0.0012 and
+0.0014 ± 0.0010 at loop² 9).

**Which histories** (`python3 research/blast/image/img.py anapat research/scratch/blast/image/rec_13_0_13_s11.npz`
→ `data/rec_s11_histories.txt`; oldest generation first): at loop² 9, 100000 recurs 1.24% ± 0.05% above chance,
010000 1.12% ± 0.13%, 001000 0.76% ± 0.12%, 110000 0.66% ± 0.11%, 000000 0.63% ± 0.13%, 111111 0.34% ± 0.04%.
At loop² 12 the same ones lead, at 0.18–0.29%.

**The first-order sum over neighbouring windows** (`img.py patch`, `data/patch_s31_out.txt`): minus the shift, under
the tilt of ONE cell's 6-generation history, of the live count of the face cells within 0, 1, 2, 3 in-layer steps
of it (1, 7, 25, 53 cells; by translation symmetry this is the sum, over the windows of those cells, of their
first-order effect on one cell):

| loop² | 1 cell | 7 cells | 25 cells | 53 cells | 53 cells / f | f |
|---:|---:|---:|---:|---:|---:|---:|
| 9 | 0.000642 ± 0.000097 | 0.003775 ± 0.000316 | 0.011027 ± 0.000756 | 0.018293 ± 0.001211 | 2.92 ± 0.19 | 0.006267 |
| 12 | 0.000139 ± 0.000082 | 0.000617 ± 0.000509 | 0.002760 ± 0.001333 | 0.005664 ± 0.002567 | 2.44 ± 1.11 | 0.002317 |
| 13 | 0.000156 ± 0.000086 | 0.000570 ± 0.000289 | 0.001543 ± 0.000745 | 0.004288 ± 0.001297 | 2.67 ± 0.81 | 0.001605 |
| 16 | 0.000032 ± 0.000150 | 0.000667 ± 0.000249 | 0.000723 ± 0.000937 | 0.002514 ± 0.001763 | 3.27 ± 2.29 | 0.000768 |

The sum has not converged at 53 cells (radius about 1.5 lattice units, half the loop at loop² 9) and already exceeds
f threefold: when one cell's dead run recurs, its neighbours' recur with it, and adding each window's effect counts
the same event many times. The patch is a disc round the window; the exact formula wants the strip between the seam
and its image, which was not separated here. With the 9-generation window the 53-cell sums are 0.0202 ± 0.0021,
0.0016 ± 0.0029, 0.0070 ± 0.0013, 0.0026 ± 0.0021.

**C(v, τ)** (`data/rec_s11_out.txt`, × 10⁻⁶, ± 9): loop² 9: +22, +6, −7, +68, +32, −7, −23 at τ = 0..6. In that run
(sampled every 4 generations) every loop length from 12 to 25 shows the same lag pattern of period 4 (about −15
and −30 at τ ≡ 1, 2 mod 4, 0 at τ ≡ 0, 3), i.e. something that does not depend on distance; in the run sampled every
5 generations (`data/hist_s21_out.txt`, ± 25) it is absent. Most likely an artifact of the estimator, not physics: the density subtracted is the mean at the
snapshot generations, the lagged cell is taken at generations of another phase mod 4, and a chance difference of
3–6 × 10⁻⁵ between the sample means of the phases (their error is 2–5 × 10⁻⁵) produces exactly such a pattern at every
distance at once. A direct look (`img.py phase 13 0 13 128 700 41`, 8,192 replicas, `data/phase_s41_out.txt`) finds no
stable dependence of the mean face density on the generation mod 4 (generations 400–700: −39 ± 18, −11 ± 4, +6 ±
23, +43 ± 13 × 10⁻⁶; 200–399: −5, −26, +25, +6); not pursued.

## Why the rate, and why the sign [conjectured, on the measurements above]

- A cell is dead-and-staying-dead when its neighbourhood sits outside the birth window for several generations: a
  quiet spot. Quiet spots are correlated over a longer range, and far more strongly, than occupation (1% against
  0.01% at 3 units). On a torus a quiet spot one loop away is the same quiet spot, so quiet is favoured, and quiet is
  mostly dead (dead runs recur twice to four times as much as live runs): the face is emptier. Nothing in ★ could
  make it fuller unless live runs recurred more than dead ones.
- The fall e^(−2.3|v|) is then the decay of the correlation of quiet between a band and its translate: a static
  length of the loop-free state (0.43 units), not a travel time. The 6-generation recurrence excess Z_W − 1 falls
  from 1.64 × 10⁻³ at loop² 9 to 0.49, 0.27, 0.30 × 10⁻³ at 12, 13, 16 (f: 1, 0.37, 0.26, 0.12 of f(9)).
- This is the same object as a death seen small: a dip is a quiet region that grows. So the living-state deficit
  and the lifetime discount would share a carrier (quiet recurring round the loop) without the one being a multiple
  of the other. Not tested here.

## Forecasts scored (`PREDICTIONS.md`)

| | outcome |
|---|---|
| I1 (85%) one-cell window < 5% of f at 9, 12 | **passes** (0.05%) |
| I2 (50%) 10-cell window right sign at 9 and 12 at > 2 SE | **fails** (−0.0003 ± 0.0003, +0.0002 ± 0.0003) |
| I3 (25%) 10-cell window within a factor 2 of f(9) | **fails** (−5% ± 4%) |
| I4 (12%) its f(12)/f(16) in [2.1, 3.9], resolved | **fails** (not resolved) |
| I5 (80%) its f(21) error above 0.000181 | **fails** as worded (error 0.000138; value +0.00014, unresolved) |
| I6 (55%) a delayed C(v,τ) above 3 × \|C(v,0)\| at > 3 SE at loop² 9 or 12 | **passes** by the letter (loop² 9, τ = 3: 68 against 22, ± 9) |
| I7 (55%) f_W grows with the window, 1 < 7 < 10 cells | **fails** (+0.000003, −0.00044, −0.00031) |
| L1–L3 | not run (the lag run was for the 10-cell window, which carries nothing; stopped unfinished) |
| L4 (50%) the 10-cell tilt lowers x + in-layer neighbours by > 3 × x alone | **fails** (neither resolved) |
| H1 (55%) h3 < h6 < h9 < h12 at loop² 9 | **fails** by the letter (0.00019, 0.00068, 0.00104, then 0.0006 ± 0.0012) |
| H2 (40%), H3 (15%) 12-generation history > 15%, > 30% of f(9) | **fail** (10% ± 19%, unresolved) |
| H4 (35%) two neighbouring cells' histories > twice one cell's | passes by the letter (2.1×), **not resolved** (± 1.4) |
| H5 (55%) the period-4 lag pattern gone when sampled every 5 | **fails** by the letter (mean at τ ≡ 2: +17 × 10⁻⁶, threshold 12), though the pattern itself is gone and +17 is within the run's common offset (± 25) |
| H6 (40%) density by generation mod 4 differs by > 3 × 10⁻⁵ at > 2.5 SE | **fails** (32 ± 17 × 10⁻⁶) |

My formula's values asked for before the test: I expected the 10-cell window to carry 30% of f(9); it carries none.


## Method

- Vessel: the 8-layer slab on the torus (13,0),(0,13) (507 cells per face; shortest loop² 169; for every v used
  the nearest other image is ≥ |v| + 2.5 away, asserted in `img.py`). Graph from
  `research/audit/shape/geom_check.my_slab` (AUTOMATON.md's cube-index table).
- Stepper: bit-sliced numpy, 64 replicas per word (the scheme of research/wraplocal/live.py, retyped in `img.py`).
  `python3 research/blast/image/img.py check 13 0 13 1000` and `check 11 0 11 1000`: replica 0 equals
  `reference/oracle.py` cell for cell at each of 1,000 generations; with one neighbour entry replaced it fails
  at generation 2. PASS (5 s).
- Runs (4,096 replicas from 0.4 soups, 300 generations of burn-in; 5–7 minutes of one core each; outputs under
  `research/scratch/blast/image/`, reductions in `data/`):
  `python3 research/blast/image/img.py run 13 0 13 64 300 210 4 11`, then `… ana …/rec_13_0_13_s11.npz` (windows c1,
  c7, c10, h6; C(v,τ); 207 snapshots, one every 4 generations);
  `… hist 13 0 13 64 300 100 5 21`, then `… anahist …/hist_13_0_13_e5_s21.npz` (h3, h6, h9, h12, two cells; every 5);
  `… patch 13 0 13 64 300 100 5 31`, then `… anapatch …/patch_13_0_13_s31.npz` (h6, h9 read in patches).
  Patterns of several cells are tabulated per class (face, axis) of the cell; errors are the scatter of 4 blocks
  of 1,024 replicas. A first version pooled the classes and gave Z − 1 = 0.8 for the 10-cell window (the two faces'
  codes do not overlap); it was caught on a 5-snapshot test and no production number comes from it.

## Not checked

- The identity is proved for a soup start at finite time and checked by enumeration on one-dimensional automata
  only; not checked by enumeration on gump itself (the seam's history is too large), and "the living state" is
  taken to be its long-time limit before the face dies.
- Every loop-free number is from ONE torus, (13,0),(0,13), one stepper, 4,096 replicas, 100–210 snapshots; errors
  from 4 blocks. No second code. The slab graph is `geom_check.my_slab`, checked here against the oracle on this
  torus and on (11,0),(0,11) only.
- The first-order sum was taken over a disc, not over the strip between the seam and its image, and only up to 53
  cells; second cluster order (joint recurrence of two neighbouring histories, with the overlap subtracted) was not
  computed. Loop² 19–28 were not reached by the history windows at useful precision.
- Histories of interior cells (the layers beneath the face) were not used as windows; the seam of the slab
  contains them.
- Whether dead runs recur because of static voids or of travelling quiet fronts was not separated.
- The period-4 lag pattern of C(v,τ) in the first run is put down to the estimator (see above) on an argument, not on a
  rerun with the lagged means subtracted properly; C(v,τ) at loop² ≥ 12 is therefore known only to about ± 3 × 10⁻⁵.
- The conditioned (dying) ensemble and κ: not measured (dropped by instruction). The observation that the brief's
  tangent formula c = λρ − λ²s²/2, with wraplocal's variance rise (δs² = 0.0245 at loop² 12) and λ = 0.5, gives a
  discount of 0.0042–0.0044 against the measured 0.00427 ± 0.00018 (and 0.0017–0.0018 against 0.00147 ± 0.00014
  at loop² 16) is arithmetic on numbers on file, written before the PI's note that the discount is quadratic in
  the tube's length; not pursued.

## Where to go next

Second cluster order for history windows: the joint recurrence of the 6-generation histories of a cell and each of
its neighbours (pair windows of 12 bits need about 30 times the present statistics: a C stepper), with the
single-window terms subtracted, summed over the strip between the seam and its image. If the dead-run reading is
right, a cheaper route is a two-state coarse field q(c,t) = "dead for the last 3 generations": measure its
correlation function K(u) on the loop-free face to 10⁻⁶ out to 5.3 units, and test f(v) ∝ Σ_u K(u+v)·(density
response to q at displacement u) at all eight loop lengths.

