# Critic to path

## 2026-11-13. Reply to round 1

Scripts: `critic/lab/path_r1.py` (subcommands named below), `startpoints.py`, `dice_w1.py`. "Checked" = re-derived
or recomputed by me. The board changed since you read it: read its sections "The lead's starting points" (path),
E12, E14 and the lemma exchange (cube lemma).

**Confirmed (checked).** L1 (a), (b), and (c) up to one word; the tables of 1.1; 1.2. Theorem P and P1, line by
line (it needs a < 1 − s̄ strictly; φ ≥ 0 is enough); the worked numbers (`psharp`). L3, L4. The data readings
5.1, 5.2 and the tail slopes of entry 3 (`data`). Your "the only closed sets missing exactly A cells are
complements of faces" is not what the board said but is true for R = 3…7 (the smallest sealed set with no whole
face has 12, 18, 33, 39, 57 > A cells); the minimum itself is now proved for R ≤ 10.

**Broken, or to be reworded.**
1. **L1(c), "each constraint involves a private cell": false at the three corner cells of a hull face.** They
   have 2 in-face neighbours and 2 cells beneath, both shared (R = 5, 7, 13 checked). True at every other cell and
   on periodic faces. The exact sharing is the cube lemma: the face is a disjoint union of cube triples,
   b_a = u_b + u_c + v_a; a one-step death is a condition cube by cube.
2. **Hypothesis H as stated (φ = r^{min(n,K)}) is false.** LR1 (`lr1`): on the measured tables a₁(r) > 1 for every
   r ≤ 0.90 at all four sizes (r = 0.65: 1.117, 1.093, 1.086, 1.075), a₂(r) > 1 for r ≤ 0.70–0.75, a₃(r) > 1 for
   r ≤ 0.55–0.65. Cause: from one cell P(death) = 0.37–0.41 and the mean step is −0.08, −0.02, 0.00, +0.02 (death
   counted as −1): a one-cell face does not drift up. max_k a_k(r) < 1 for no r at A = 30, 45. LR2 (`lr2`): in the
   exact dice model D2(L, 0.472) the best geometric certificate is 0.80–1.02 at L = 8, 10, 12, 14 (it loses all of
   −ln h = 4.40, 5.38, 6.42, 7.58), for the same reason (a₁ = 1.01–1.22 for r = 0.7–0.4).
3. **With φ free on the first rows the certificate works** (linear programme: minimise ε over 0 ≤ φ ≤ 1).
   D2, exact (`lr2b`): bound/h = 8.8, 10.4, 11.5, 12.6, 13.6 at L = 8…16 (loss 2.2–2.6 nats, a = 0.8; φ(1), φ(2),
   φ(3) ≈ 0.9, 0.3, 0.05 at L = 16). Gump, measured rows k < A/2, φ constant from K on (`lr1b`): −ln(bound) = 2.82,
   5.78, 9.53, 14.02 against −ln h = 6.81, 9.82, 13.63, 18.08: **a loss of 4.0 nats at every size** (a = 0.95,
   K/A = 0.43–0.48; φ = 0.84–0.90, 0.56–0.64, 0.32–0.43, then ratios 0.55–0.63). Restate H with φ free. Not
   tested: rows above A/2 (not in the tallies), uniformity in time (the tallies are pooled); A = 63, 84 are
   optimistic (unobserved transitions count as impossible).
4. **G2, gump half: the data do decide against a flash of fixed length.** LR3 (`lr3`): the lag at which the mean
   pre-death population crosses half the living mean is 3.2, 4.7, 5.9, 6.8 generations at A = 30, 45, 63, 84
   (×2.1; √A gives ×1.67), and looking back from the death the mean population is one curve at every size until
   it saturates: 1.6, 3.5, 6.4, 9.7, 13.6, 17.6 at lags 1…6 (A = 84; A = 63: 1.6, 3.5, 6.4, 9.8, 13.0, 16.0). The
   mean remnant loses two to four cells a generation. Toy half: the same F2 entry says the sag over the ten
   generations before is ≤ 12%, so at L = 24 the collapse is about 12 → 9.4 → 2.4 → 0 (the 12 is my arithmetic,
   0.88 × 0.58 × 24); your E2 will tell.
5. **R5.** The degenerate rule has smallest birth count 12, not θ: it inherits "a dead sealed set stays dead"
   but not the converse (thickness.md Lemma 1). The Moore rule carries the remark (read: τ_edge 508 → 163).
6. **G1's error bar.** The limit of the window decrement depends on the assumed approach: on ℓ ≥ 20, g = 0.348
   (c/ℓ), 0.355 (e^{−ℓ/20}), 0.370 (c/ℓ²), 0.373 (e^{−ℓ/10}), all acceptable: 0.35–0.37 from that file. The
   segment slopes (0.34 ± 0.01) are your stronger leg.

**Is B circular?** My judgement: no for gump, yes for the flash part of the toy. In gump one-step drops are
small (item 4), the free φ contracts row by row, and the exponent is the product over ≈ 0.45·A rows: a genuine
reduction of many steps to one. In D2, 7–30% of deaths go straight from n ≥ 7 to empty (the real
toy: 22% at L = 12, ≤ 1% from L = 28, board E9), and the toy's last two steps lose seven of nine cells at once:
there (∗) at the upper rows is itself a statement about exponentially rare one-step drops, and B comes close to
the exponent study's Theorem E.

**Lab, unrequested, bearing on E1 and G1** (`seg`, exact). A ring with two adjacent cells removed is a segment.
D2 on a segment of L cells: ln τ = 6.764, 7.259, 7.740, 8.201, 8.655 at L = 10…14 (steps 0.495, 0.481, 0.461,
0.454) against the ring's 5.384, 5.867, 6.417, 7.006, 7.577 (steps settle at 0.52–0.53 by L = 16–18). The segment
is *longer*-lived than the ring of equal length at every L ≤ 14 (by 2.07 nats at L = 5, 1.08 at L = 14); ring minus
segment rises like 0.7–1.0 × ln L. Compatible with G1's power and with unequal slopes: undecided at these sizes.
An end anchors life too: the end cell of a dense row has k = 2 and is safe.

**From elsewhere.** E12: sealed bands in slabs are smaller than a face once N > 1.5·m and death does nucleate
there, at 0.12 per cell against 0.21: aim A is a statement about hulls. Shelf: Durrett–Schonmann 1988 has a
proved "area above, perimeter below" dichotomy (`library/notes/ld-contact-percolation.md`); Mountford 1993
Prop. 1.2, "fast regeneration ⇒ memoryless" (`notes/contact-finite.md` §3), bears on uniformity in time. The
reports of source and counting are not read yet; overlaps with them will be on the board.

**Admissibility.** LR1 and LR3 read `research/scratch/fluct/qsd_R*.npz` (not in git; deaths and exposure equal
the committed `qsd_summary.json` exactly). They can be reproduced only while that directory exists.

## 2026-11-13. Reply to round 2

Script: `critic/lab/path_r2.py` (`pbar`, `deep`, `lr4` … `lr8`). The tallies it reads are now a committed file,
`critic/lab/data/fluct_tables.npz`. New on the board since round 1: E15, the lemma exchange (one row over dice;
Markovian projection; finite-horizon law), lab L2–L5.

**Confirmed (checked).** Theorem P̄: identity (I), the cancellation, the worked walk (`pbar`). Lemma 1′ and
Proposition S. Proposition R: the proof, and every starting set on four small graphs. Corollary 4a's inequalities
for d-deep cells (hulls R = 7, 9, 11; `deep`). The lifetimes of gump's four neighbours in `phase/rules.csv`. The
arithmetic of 11.1 and the committor ratios of 11.2.

**Lab.**
- **LR4.** ψ*_K hardly depends on K (K = 0.3A and 0.4A agree to three digits at k ≤ 10 for A ≥ 45). **It is not
  one function for all A:** ln[ψ*(A)/ψ*(63)] at k = 4, 7, 10 is +0.10, +0.22, +0.33 at A = 45 and −0.04, −0.04, −0.15
  at A = 84 (at A = 30: +0.32, +0.47 at k = 4, 7). Its log-slope over k = 5…10 is 0.51–0.54, 0.53–0.57, 0.55–0.60 at
  A = 45, 63, 84. Only the first three values are nearly common (0.74–0.75, 0.45–0.47, 0.24–0.27 for A ≥ 45). The
  identity holds exactly, as it must (it is algebra once the arrivals from untallied rows are taken from (I)).
  The sum is carried by small steps across the level: rows K, K + 1, K + 2 give 0.85, 0.61, 0.51, 0.41 of it at
  A = 30…84 (K = 0.3A), entering at K − 1 … K − 3. No face died directly from n ≥ K, except 26 at A = 30, K = 9.
- **LR5.** The root r_k is not the same at the four sizes: over k = 5…8 it is 0.62–0.65, 0.573–0.589, 0.554–0.565,
  0.545–0.556 at A = 30, 45, 63, 84, and within a size it rises with k (A = 84: 0.556, 0.576, 0.598, 0.669 at
  k = 8, 15, 20, 30). The mean step grows faster than √k: mean/√k = 0.50, 0.56, 0.68, 0.77, 0.81 at k = 4, 6, 10, 15,
  20 (A = 84); the variance is about 0.75·k up to k ≈ 12.
- **LR6. No: n is not Markov along death paths.** The reversed pooled chain gives 1.6, 2.9, 4.3, 5.9, 7.7, 9.8 at
  lags 1…6 (A = 84) where the recorded histories have 1.6, 3.4, 6.4, 9.7, 13.6, 17.6 (A = 45, 63 alike). A dying
  face comes down about twice as fast as faces of the same population do on average.
- **LR7.** Local slope of ln p_k at k = 12: 0.372, 0.444, 0.485 at A = 45, 63, 84; 0.555 ± 0.05 at A = 108 (488
  counts; 0.49 over k = 16–20). A = 135 has 61 counts at k = 20 and none below 8; A = 165 none: not measurable.
  **M3 fails as a tangency.** At A = 84 (mean 42.45, variance 35.55) the histogram leaves its parabola near n = 28
  and its slope is below both of your branches down to n ≈ 14: at n = 28, 23, 18, 14 the slope is 0.343, 0.414,
  0.458, 0.476 where the parabola has 0.406, 0.547, 0.688, 0.800 and θ = 0.485; x*·A is 25.
- **LR8′** (D2(0.472), exact quasi-stationary law). Segment of 18: the corner decrement is 0.508, 0.475, 0.486,
  0.504, 0.518, 0.529 at ℓ = 3…8 and falls with the length of the segment (ℓ = 4: 0.535, 0.498, 0.482, 0.475 at
  M = 12, 14, 16, 18). Ring of 18: 0.608, 0.605, 0.608, 0.610, 0.609, 0.610 at ℓ = 3…8; a centred window of the
  segment gives the same. On a ring of 128 the exponent study's sampled windows (agreeing with mine at ℓ ≤ 4)
  go on down: 0.575, 0.550, 0.530, 0.511 at ℓ = 10, 15, 20, 25, and (decrement − 0.46)·(ℓ + ½) = 1.2, 1.4, 1.4, 1.3.

**To correct.**
1. **H′, "C, θ, κ independent of A": not on these tables.** The committor steepens with the face, as the tail
   does and as the lifetime slope does (board E2). Between A = 63 and 84 the change is within the noise for k ≤ 7
   (the A = 84 rows have 576 transitions at k = 1, 3,329 at k = 5), so a limit is possible; A ≤ 45 is not in it.
2. **The check of (M) in 11.3 differentiates at fixed θ while θ rises with A.** With each face's own mean,
   variance and θ, A(θρ − θ²σ²/2) is 11.47 and 16.41 at A = 63, 84; the histogram's ln p(mean) − ln p(1) is 10.55
   and 14.85. The difference quotient of (M) is 0.235 against 0.205. The excess is the region where M3 fails.
3. **11.1 and E3, "one remnant whose population walk does not know the vessel":** the shrinking speed is a
   property of the conditioned paths, not of the population's one-step table (LR6). Something besides n is
   carried along a death path (fluct README: the layer beneath sags to 0.62–0.75 of its mean). Theorem P̄ is
   untouched; the droplet reading needs that second variable.

**G1, from the other lines** (board E15). In D2 an interval with dead ends and one with reflecting ends have
the same exact exponent, 0.460 per cell (converged to three decimals at 16–19 cells), and the ring has 0.52–0.53;
ln τ_ring − ln τ_dead is fitted by −4.30 + 1.21 ln L. With LR8′: the ring's window decrement tends to that 0.46
with a power ℓ^{−1.3}. This is your G1 in a model with dice, with the same three ratios as the 2D rule. The
probability line holds the statement for dice models (its T2), counting the fixed-horizon version (c⁰_k = c_k,
verified at k = 1, 2); the power of L is yours.

**Also from elsewhere.** Source's Lemma 3 is the projection behind P̄, for the top layers instead of the
population; its "class of drive kernels" is where LR6's second variable would live. Board, "starvation": in a
face with at most three live cells no live cell is overcrowded, so the last deaths are by n ≤ 2.

## 2026-11-14. Reply to round 3 (interim: entry 15 and the interim report)

Script: `critic/lab/path_r3.py` (`th`, `mono`, `age`, `sealed`); the "how D2 dies" tables are `prob_r2.py r7`.
"Confirmed" = re-derived or recomputed by me. Board ids: L9.1–L9.4, L8.3. You sent nothing to the lab; the three
items of "Next (1), (2)" in your interim report are answered here because they are the tests your two unfinished
pieces name.

### 1. Standing of the claims

- **15.1, your three corrections:** they agree with the lab tables they cite. Nothing to add.
- **Claims tagged proved** (L1, L1′, S, P, P̄, L3, L4/4a, R, R5): confirmed in rounds 1 and 2. New this round, by
  enumeration (`sealed`): on every state and every sealed set of the hull R = 2v (1,824 sealed sets, 86 minimal),
  the 2D box 3 × 4 (445; 36) and the 2D strip 2 × 6 (324; 59), a dead cell of a sealed set whose neighbours in the
  set are dead is dead next (L1′), the union K of the dead sealed sets never loses a cell, and at each of the
  216, 685, 229 states where K first becomes non-empty it contains an inclusion-minimal sealed set that had a live
  cell one generation earlier (S).
- **W, "free ends give no power" [proved in the model]:** confirmed (profiles with minimum 0 on a segment
  correspond one to one to step sequences, so the sum is W^{L−1}). The ring, pinned-window and one-free-end powers
  are the standard return, bridge and meander estimates; not re-derived.
- **Th and H′ (inequality form):** tested below. As stated, Th is not supported; the collapse of θ in k/A is.

### 2. Your "Next (1)": the local roots on the committed tables (`th`)

θ_k = −ln r_k exists for k ≥ 2 (A = 30, 45) or k ≥ 1 (A = 63, 84) up to the last tallied row K − 1 (15, 22, 31, 42),
which is the mean population to within one cell.

| A | Σ_{k<K} θ_k | −ln ψ*(K − 1) (same table) | −ln h | Σθ per cell | −ln h per cell |
|---|---|---|---|---|---|
| 30 | 4.87 | 5.24 | 6.81 | 0.162 | 0.227 |
| 45 | 8.72 | 8.64 | 9.82 | 0.194 | 0.218 |
| 63 | 13.10 | 12.57 | 13.63 | 0.208 | 0.216 |
| 84 | 18.07 | 17.08 | 18.08 | 0.215 | 0.215 |

Slopes between successive sizes: Σθ 0.257, 0.243, 0.237; −ln h 0.201, 0.212, 0.212.
- **The agreement at A = 84 (18.07 against 18.08) is a crossing, not a law.** Σθ runs 1.94, 1.10, 0.54, 0.00 below
  −ln h at the four sizes and its slope is 0.03–0.05 per cell above the hazard's.
- **The local-root sum is not the committor's exponent.** With ψ* the committor of the same pooled table (so no
  second data set is involved): −ln[ψ*(k)/ψ*(3)] against Σ_{3≤j<k} θ_j at A = 84 is 4.11 / 4.10 (k = 10), 6.84 / 6.97
  (15), 9.35 / 9.66 (20), 13.32 / 14.36 (30), 15.40 / 17.42 (40). The excess near the top of each table (k = 15, 20, 30,
  40 at A = 30, 45, 63, 84) is 0.45, 0.98, 1.46, 2.02 nats: it grows with A, about 0.03 per cell. Row by row at A = 84, −d ln ψ*/dk against θ_k:
  0.583 / 0.607 (k = 5), 0.553 / 0.585 (10), 0.463 / 0.514 (20), 0.284 / 0.402 (30), 0.139 / 0.160 (40).
  The WKB step assumes the one-step law changes little over one step. Here the step has standard deviation
  2.0, 2.8, 3.8, 4.5, 5.0 cells at k = 5, 10, 20, 30, 40 while θ falls by 0.01–0.03 per row beyond k = 15.
- What Theorem P̄ does give on these tables: −ln h − (−ln ψ*(K − 1)) = 1.18, 1.06, 1.00 at A = 45, 63, 84, the entry
  flux, nearly constant. So the committor carries the whole A-dependence, as your identity says, and its
  exponent between sizes is 0.219, 0.214 per cell (45 → 63 → 84).
- **The collapse holds.** θ at x = k/A = 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45: A = 45: 0.548, 0.519, 0.485, 0.453,
  0.407, 0.328, 0.213; A = 63: 0.565, 0.533, 0.500, 0.463, 0.411, 0.332, 0.223; A = 84: 0.573, 0.540, 0.504, 0.466,
  0.411, 0.333, 0.228; A = 30 lies 0.03–0.09 lower. 63 and 84 agree to 0.008.
- **2·mean/variance reproduces θ_k** to 1–7% for k ≥ 4 (A = 84: 0.557 / 0.585 at k = 10, 0.501 / 0.514 at 20,
  0.405 / 0.402 at 30).
- **ψ*_A(k) at fixed k is non-increasing in A** for k = 1…12 over the four sizes, with one exception: k = 2,
  A = 63 → 84, ×1.058, which is one standard error (the A = 84 table has 840 transitions from n = 2 and 342 deaths
  in all). Values (A = 30, 45, 63, 84): k = 4: 0.197, 0.150, 0.135, 0.130; k = 8: 0.0320, 0.0186, 0.0139, 0.0127;
  k = 12: —, 0.00284, 0.00166, 0.00130. Note what this can and cannot give: monotonicity in A at fixed k bounds
  ψ*_A(k) by the smallest face's committor only for k below half the smallest face (k ≤ 15); the bound you want
  runs to k = κA.

### 3. The pointer you were owed: source's monotone comparison, and what the tables say about it

Source (its round 2 report; checked; board, lemma exchange): *if q is a stochastically monotone kernel on
{0, …, A} with 0 absorbing, and at every time t every row of the true one-step kernel of the population dominates
the same row of q, K_t(n, ·) ⪰ q(n, ·), then the law of n_t dominates λ₀qᵗ, hence P(T > t) ≥ P_q(T > t); with ⪯
throughout, the reverse.* No Markov property of the population is used (it goes through the Markovian
projection). It is an alternative to a certificate for Theorem P̄: a comparison chain instead of a function ψ.
On the pooled tables (`mono`):
- each pooled table is stochastically monotone in every tallied row: the largest violation of "row k + 1
  dominates row k" is below 10⁻⁴ at all four sizes;
- at equal k the larger face's row dominates the smaller's, up to small real violations in the lowest rows:
  max of (F_{A′} − F_A) = +0.007 (45 against 30, at k = 3; about eight standard errors), +0.002 (63 against 45, not
  significant), +0.04 (84 against 63, at k = 2: 840 transitions, about 2.4 standard errors). Death column, A = 30, 45, 63, 84: 0.409, 0.384, 0.377,
  0.372 from one cell; 0.098, 0.093, 0.092, 0.104 from two; 0.0185, 0.0182, 0.0190, 0.0187 from three; 0.0066, 0.0054,
  0.0046, 0.0044 from four.
Two limits of what this shows. The lemma needs the domination for the kernel at each time, and a pooled table is
an average over time. And a dying face comes down twice as fast as the pooled table says (lab L5.3), which is
compatible with the lemma (it needs no Markov property) only if the rows of K_t do not sink along the way.

### 4. Your "Next (2)": D2 exactly (ring, ρ = 0.472)

**The row before death** (law ∝ μ(S)·P_S(T = j); `prob_r2.py r7`; the probability line asked for the same table):

| | j = 1 | 2 | 3 | 4 | 6 | 8 | steady |
|---|---|---|---|---|---|---|---|
| ring of 14, population | 2.77 | 6.29 | 7.82 | 8.49 | 8.94 | 9.03 | 9.05 |
| ring of 14, longest dead arc | 10.61 | 6.40 | 4.32 | 3.45 | 2.92 | 2.83 | 2.81 |
| ring of 18, population | 2.37 | 6.71 | 9.30 | 10.50 | 11.36 | 11.56 | 11.62 |
| ring of 18, longest dead arc | 14.52 | 9.21 | 5.98 | 4.46 | 3.44 | 3.22 | 3.15 |
| interval of 18 (dead ends), population | 1.37 | 3.30 | 6.22 | 8.27 | 10.36 | 11.23 | 11.96 |
| interval of 18, larger wall gap | 11.86 | 8.22 | 5.76 | 4.18 | 2.49 | 1.73 | 1.04 |

The ring dies by one dead arc growing from both ends, the interval by one gap leaving one wall; the interval's
collapse is the longer one (its population is still 13% low six generations before death at M = 18, the ring's
2%), and both lengthen with the vessel. In neither is the last step a flash from ordinary density.

**The age of a dead cell in an empty window** (`age 18`; quasi-stationary process on a ring of 18; x the central
cell of a window of ℓ empty cells; age = number of generations x has been dead, the present one counted):

| ℓ | 1 | 3 | 5 | 7 | 9 | 11 | 13 |
|---|---|---|---|---|---|---|---|
| mean age | 1.99 | 1.95 | 2.14 | 2.30 | 2.45 | 2.57 | 2.67 |
| P(age = 1) | 0.520 | 0.518 | 0.435 | 0.381 | 0.336 | 0.295 | 0.259 |
| P(age ≥ 6) | 0.035 | 0.029 | 0.037 | 0.045 | 0.053 | 0.060 | 0.066 |
| window decrement per cell | | 0.740 | 0.607 | 0.609 | 0.610 | 0.618 | 0.635 |

Ring of 16: 1.99, 1.93, 2.11, 2.25, 2.38, 2.49 at ℓ = 1…11; ring of 12: 1.97, 1.89, 2.05, 2.17 at ℓ = 1…7. Of your three
alternatives: not ∝ ℓ (a gap opening by two cells at each end per generation would add ℓ/4 generations to the
age of its centre; the table adds 0.05–0.10 per cell, and less as ℓ grows), not constant; the increase from ℓ = 5 to 13 (0.53 generations)
is what c·√ℓ gives with c = 0.4, and the range is too short to tell that from a logarithm. A quarter to a half of
the central cells of these windows died in the last generation.

### 5. The power of L (your G1 and the scorecard of 15.3): exact numbers from the other lines' requests

- **Three one-row dice models, ring against free-ended interval, exact to 18–19 cells** (board E15, L8.1, L8.5).
  (ring's step of ln τ − interval's) × L, which is the local power of L in τ_ring/τ_interval:
  OP₅(½) (five-parent oriented percolation, where death by a front is a theorem): 0.76, 0.74, 0.72, 0.71 at L = 12,
  15, 18, 19, still falling; the anchor (½, 0, ½): 0.92, 0.88, 0.87, 0.84 at L = 15…18; D2(0.472): 0.99, 1.03, 1.19, 1.31
  at L = 16…19, rising. Your profile model says ½ for this power. In all three the interval's step has converged
  (0.3815, 0.6236, 0.460).
- **At a fixed age the ring's excess exists where the exponents are provably equal** (counting's lab, L7.5): the
  probability that D2 is dead by generation k has the same exponent on a ring and on a dead-ended interval
  (k = 2, 3), the interval's local slope is on it from L = 10, and the ring's is 0.022, 0.014, 0.003, 0.0003 above at
  L = 10, 18, 32, 58 (k = 2, fair soup): an exponential approach at fixed k, slower for larger k.
- **A bound on D2's ring from the transient side** (L7.2, L7.4): from a product row at the steady density the
  hazard at age 5 has exact asymptotic exponent 0.4992 and equals the ring's steady hazard to 0.2% at L = 14–18.
  Either that equality breaks beyond L = 18 or the ring's step (0.52–0.53 at L ≤ 19) comes down to 0.499 or less.

### 6. Overlaps

- **probability**: Proposition W (ring against the dead-ended interval four cells shorter: an exact inequality
  h_ring(L) ≥ w^{n+1}·P(the interval started from the ring's law on rows with a four-cell gap dies at step n + 1))
  is the same question as your G1 in D2, from the side of inequalities; its exam P-E1 predicts the ring's slope
  0.48 ± 0.03 at L = 30–38. Your W model and that proposition have not been put side by side by anyone.
- **counting**: fixed-age matrices of D2 on rings and intervals (above). Its finding that at horizon 2 the true
  2D rule's cheapest death from a fair soup goes through a *full* edge (98.7% alive at generation 1, then
  overcrowded; L7.7) is the channel of board E9 and bears on "flash or front" at small ages only.
- **source**: besides the comparison lemma of §3, its Theorem L (round 3) transfers the one existing dice theorem
  to any bulk under an equal-time condition on the drive; it concerns the 2D edge near the anchor, not
  populations.
- One-step death probabilities of every gump face configuration of ≤ 3 cells over dice are now exact (board,
  lemma exchange, "small faces under dice"): rows of the table Theorem P̄ runs on, with the shape resolved. The
  two orientations of a three-cell triangle differ by a factor 4 (0.0036 and 0.0009 at density ½).

## 2026-11-14. Reply to round 4 (entries 16–21 and the round 4 report; lab requests LR9–LR12)

Script: `critic/lab/path_r4.py` (`props`, `lr9`, `lr10`, `lr11`, `lr12`, `fits`, `limit`, `ext`, `cross`, `supersol`; `lr12` takes about
15 min, everything else about two minutes together). All of it is exact arithmetic on the curated tallies
`critic/lab/data/fluct_tables.npz` (rows k ≤ A/2 of the hull faces A = 30, 45, 63, 84) or on the lattice; no runs.
Committors are computed by elimination without pivoting (no subtraction of nearly equal numbers), and agree with
numpy's solver to 10⁻¹⁴ in the logarithm where both are usable. "Confirmed" = proof re-derived and the finite
content computed. Board ids: L12.1–L12.10.

### 1. Standing of the claims

| claim | verdict | how |
|---|---|---|
| T′ (17.2), block bound | **confirmed** | proof (e^{−θ₀(k−k₀)⁺} is a supersolution; Theorem P̄'s comparison); worked case (walk on {0…3}, up ¾: ψ*(2) = 1/13 ≤ 1/9); 23,850 cases on 4,000 random tables, half with censored mass (`props`) |
| T (17.3), root sum as a bound from the other side | **confirmed** | proof; worked case 2/27 ≤ 1/13; 7,023 cases on 2,000 random tables |
| X (17.4 a, b, c) | **confirmed** | (a) 2,000 random skip-free chains inside the stated range; (b) offspring 0 or 2 with probabilities ¼, ¾: q = 1/3 and q² harmonic; (c) 1.695 < 1.863 < 2.234 |
| two-patch identity (17.6) | **confirmed** | rows convolve, transforms multiply; it is the construction of LR11 |
| Q (17.6) | **confirmed as an implication**; one side condition ("C bounded") does not hold as worded and one is known on half its range, §2 | from P̄ and T′, line by line |
| C and its corollary (entry 18) | **confirmed**; the monotone rows of q are needed | 3,000 random monotone kernels with a dominating pooled table, censoring included (largest excess of ψ* over ψ_q 6 × 10⁻¹⁵). Without monotone rows it fails: q(1, ·) = 0.99 δ₁ + 0.01 δ₃, q(2, ·) = 0.9 δ₀ + 0.1 δ₃, K = 3; the table with row 1 moved to 2 dominates q row by row and has ψ*(1) = 0.891 > ψ_q(1) = 0 |
| F (entry 20) | **confirmed** | (i), (ii) on the neighbour lists of walls 3 × 3 … 5 × 5 (`counting_r3.py structure`); (iii) by integer programme: in every vessel tried W is sealed and no non-empty proper subset is (§5) |
| V (17.5, 21) | sketched, as you tag it. The limit statement holds on the chains you asked for; your number for it does not come out of the request as written; §3 | LR10, LR11 |
| 16.1, the two fits of the E1 table | arithmetic confirmed (1.656 ± 0.165 ln L − 4.41, χ² 0.25; 0.065 ± 0.006 L − 0.73, χ² 0.32) | `fits` |
| entry 21's table | reproduced with the cancellation-free solver (17.137, 34.829, 70.472, 142.215) | `limit` |
| entry 19 (dead end) | your script reproduces your table when run (50 s); I did not audit the closure | `python3 path/mf_deadend.py 100` |

Nothing tagged proved was found wrong.

### 2. Theorem Q: which hypotheses do the work, and what the tables say (LR9, `lr9`)

**R(κ, θ₀, k₀).** min of θ_k over k₀ ≤ k < ⌈0.35A⌉, and the row where it is attained:

| A | k₀ = 1 | k₀ = 2 | k₀ = 3 | k₀ = 4, 5 | largest root | roots non-increasing from |
|---|---|---|---|---|---|---|
| 30 | 0.000 (row 1) | 0.276 (row 2) | 0.390 (row 3) | **0.4034** (row 10) | 0.483 at row 5 | row 5 |
| 45 | 0.000 | 0.331 | 0.4261 (row 15) | **0.4261** | 0.556 at row 5 | row 5 |
| 63 | 0.005 | 0.340 | 0.4117 (row 22) | **0.4117** | 0.590 at row 5 | row 5 |
| 84 | 0.049 | 0.226 | 0.4172 (row 29) | **0.4172** | 0.615 at row 4 | row 12 (row 4 if rises below 0.01 are ignored) |

So **R(0.35, 0.40, 5) holds on all four tables**, A = 30 included (by 0.003; your "fails at A = 30" was about the
roots at fixed x, which are lower there, not about the block minimum). k₀ can be 3 from A = 45 on; it cannot be 2
or 1 at any size: one or two cells have no usable root (rows 1 and 2 at A = 84: 0.05 and 0.23, on 576 and 840
exposures). The roots are not non-increasing at A = 84 before row 12, which matters for T's "+ const", not for Q.

**"No face dies directly from K cells or more."** Tallied rows K ≤ k ≤ A/2: 1, 0, 0, 0 deaths (A = 30, 45, 63, 84).
Rows above A/2 are not in the tallies, so the condition is known on half of its range only.

**"The crossings undershoot by a bounded exponential moment."** Not bounded, and harmless (`lr9`, `cross`).
On the tallies C = E_cross[e^{θ₀(K − z′)}] = **2.42, 3.08, 3.70, 4.45** at A = 30, 45, 63, 84 (θ₀ = the block's minimum; ln C/A =
0.029, 0.025, 0.021, 0.018). On the m-fold chain of the A = 84 table, with the chain's own stationary law
(restarted at the top row at death; Grassmann–Taksar–Heyman elimination, no subtractions; at m = 1 it gives 4.34
against the tallies' 4.45):

| cells | 84 | 168 | 336 | 672 | 1344 |
|---|---|---|---|---|---|
| C | 4.34 | 6.56 | 11.5 | 23.7 | 58.4 |
| ln C per cell | 0.0175 | 0.0112 | 0.0073 | 0.0047 | 0.0030 |
| mean undershoot K − z′, cells | 2.50 | 2.79 | 3.04 | 3.16 | 3.19 |
| mean start z − K, cells | 5.6 | 10.4 | 19.6 | 39.0 | 80.1 |
| log-slope of the living law at K | 0.297 | 0.339 | 0.356 | 0.3635 | 0.369 |

The mean undershoot is bounded (about three cells); its exponential moment at θ₀ is not. The reason is one
line: crossings come from z = K + j with weight μ(z) ∝ e^{σj}, σ the living law's log-slope at K, so the undershoot
has law ∝ e^{−σu}·G(u) with G the tail of the σ-tilted down-step, whose length is of order A; and σ = V′(κ) is
smaller than the root Θ(κ) ≥ θ₀ (0.37 against 0.41 here; your own first-order formula V′ = Θ − ½|Θ′|b says so).
Then C grows like exp(A·max_y ∫_y^κ (θ₀ − V′)), a rate of order 0.0005 per cell here (increments of ln C per cell
between successive m: 0.0049, 0.0033, 0.0022, 0.0013). So the conclusion of Q should read
ln τ ≥ (θ₀κ − ε)A − const with ε = limsup ln C/A, or θ₀ should be taken at most the living law's log-slope at K
(then C is bounded); either way the exponent 0.14 is not touched in the second decimal.
The remark that "the crossing term is carried by drops of one to three cells" holds by count (91%, 86%, 80%,
78% of the crossings land one to three cells below K at A = 30…84; 68% in the limit) and no longer by weight:
share of the ψ*-weighted entry flux by depth of landing (1–3 cells | 4–6 | 7 or more): 0.70 | 0.28 | 0.02 at A = 30;
0.55 | 0.35 | 0.11 at 45; 0.41 | 0.34 | 0.25 at 63; **0.33 | 0.30 | 0.36 at 84**.

**What Q gives on the tables.** With the block's own minimum as θ₀ and k₀ = 5: θ₀(K − 1 − k₀) = 2.02, 4.26, 7.00, 10.01
(0.067A … 0.119A). Best block over (κ, k₀): 2.94, 5.26, 7.82, 10.85 (slopes between sizes 0.155, 0.142, 0.144). The
bound on the hazard through the tallied entries (flux times the block certificate over exposure): −ln = 4.42,
6.96, 9.88, 13.51 against −ln h = 6.81, 9.82, 13.63, 18.08 (slopes 0.169, 0.162, 0.173 against 0.201, 0.212, 0.212). And
the identity cannot be closed on the tallies: 3%, 14%, 15%, 11% of the deaths from the low set are not accounted
for by tallied entries with the exact ψ* (entries from rows above A/2 are missing).
So: **Q is a theorem, its main hypothesis R holds on every table, and it proves about two thirds of the
exponent** (0.13–0.14 per cell by the block, 0.16–0.17 if the flux is credited). The one-step fact it rests on
(a sparse face regrows at an exponential rate bounded below up to a third of its area) is measured, pooled
over the living ensemble, and not derived, as you say.

**Collapse (the rest of LR9).** Per cell of the face, at x = k/A, sizes 30, 45, 63, 84:

| | x = 0.15 | 0.25 | 0.35 | 0.45 |
|---|---|---|---|---|
| mean step / A | 0.0256, 0.0285, 0.0300, 0.0309 | 0.0343, 0.0399, 0.0426, 0.0442 | 0.0372, 0.0431, 0.0463, 0.0485 | 0.0230, 0.0279, 0.0313, 0.0338 |
| variance / A | 0.108, 0.108, 0.111, 0.114 | 0.158, 0.168, 0.1745, 0.179 | 0.195, 0.213, 0.2255, 0.2346 | 0.232, 0.258, 0.276, 0.288 |
| third cumulant / A | 0.009, 0.025, 0.030, 0.036 | 0.010, 0.020, 0.024, 0.024 | 0.005, 0.000, −0.004, −0.009 | −0.040, −0.062, −0.085, −0.101 |
| root | 0.481, 0.548, 0.5645, 0.573 | 0.437, 0.485, 0.500, 0.504 | 0.386, 0.407, 0.411, 0.411 | 0.198, 0.213, 0.223, 0.228 |

The roots collapse better than the cumulants they are made of: from A = 63 to 84 the root moves by less than 1%
at x = 0.25–0.40 (2.6% at 0.45), the mean step per cell by 3–8% and the variance per cell by 2–5% (they move
together, which is why the root moves less), and the third cumulant has not collapsed at x = 0.15 or 0.45.
Variance per live cell is 0.64–0.87 at A = 84. At x = 0.05 the root is 0.14, 0.36, 0.51, 0.61:
no collapse at the sparse end, where the row is a fixed number of cells (1.5 to 4), not a fixed density.
**Extensivity fails by a measurable amount at these sizes** (`ext`): two independent faces of 45 cells, built
from the A = 45 table, have −ln ψ*(top) = 17.10–17.60 (0.190–0.196 per cell); the line through the measured tables
gives 18.39 at A = 90 (0.204 per cell). Two or three faces of 30: 0.164–0.176 per cell against 0.198–0.204. A face
of mA cells is harder to empty than m faces of A cells, by 4–7% from A = 45 and by 12–20% from A = 30.

### 3. Claim V (LR10, LR11)

**The limit statement is right on the chains you asked for.** m-fold chain of the A = 84 table (`lr11`),
−ln ψ* at the top row and its increment per cell between successive m:

| m (cells) | as requested (rows 1, 2, … of the table at the bottom) | increment | variant: below 5m cells, clusters of 5 (T₅^{∗a} ∗ T_c) | increment |
|---|---|---|---|---|
| 1 (84) | 17.077 | | 17.077 | |
| 2 (168) | 34.407 | 0.2063 | 35.001 | 0.2134 |
| 4 (336) | 69.057 | 0.2063 | 71.381 | 0.2165 |
| 8 (672) | 138.255 | 0.2059 | 144.665 | 0.2181 |
| 16 (1344) | 276.504 | 0.2057 | 291.725 | 0.2188 |
| recursion with the same rows' own rates (LR10 b) | | **0.2054** | | **0.2191** |

In both families the increment converges to the value of recursion (3) run with each row's own rate (Legendre
transform of the row), to 3 × 10⁻⁴ at m = 16. Both sides of (1) for these chains: block bound 0.131–0.133 (0.142–0.144
in the variant), sum of roots 0.2153–0.2155 (0.227–0.230) per cell: the committor's exponent is strictly between
them and is not the root sum, as you say.

**Your prediction for LR11 misses as the request is written, and holds on the chain your calculator assumes.**
Predicted: the second doubling adds 36.6 ± 1.2. Exact: **34.65**; first doubling 17.33. In the variant: **36.38**
(first 17.92). The difference is the bottom of the chain. The request stretches rows 1–4 of the table with m
(roots 0.05, 0.23, 0.53, 0.62), so the sparse end of a face of 84m cells is m patches of one to four cells each;
`bellman.py` continues the root of row 5 (0.607) down to zero. Four rows of 0.607 against 0.05 + 0.23 + 0.53 + 0.62
is 1.0 nat per 84 cells, 0.012 per cell: the whole gap between 0.2054 and 0.2191. The measured tables side with the
calculator's assumption in kind: rows 1 and 2 have small roots at every size (a boundary layer of fixed width in
k, not in x), so they should cost O(1), not O(A). Record the miss and its reason; do not record it as a hit.

**The numbers for V on each table** (`lr10`; S at the top tallied row over A, grids of ½ to 1/16 cell
extrapolated; allowing rising steps changes nothing at grid ¼):

| | A = 45 | 63 | 84 |
|---|---|---|---|
| (a) `bellman.py` on every row's root and variance (rows ≥ 5) | 0.2056 | 0.2148 | **0.2180** |
| its ∫Θ; first-order value; block bound | 0.2167; 0.2087; 0.1424 | 0.2269; 0.2178; 0.1438 | 0.2305; 0.2204; 0.1440 |
| (b) each row's own rate, rows as tallied | 0.1867 | 0.1997 | 0.2054 |
| (b) own rates, clusters of 5 below row 5 | 0.2098 | 0.2168 | **0.2191** |
| the same with Gaussian rates from each row's mean and variance | 0.2061 | 0.2119 | 0.2140 |
| the table's own −ln ψ*(top row)/A | 0.1919 | 0.1996 | 0.2033 |
| slope of −ln ψ*(top row) from the size before | 0.226 | 0.219 | 0.214 |

- Your 0.218 is reproduced from the rows (0.2180), and the typed-in data give the same. With exact rates it is
  0.2191; with a Gaussian of each row's mean and variance 0.2140. So the Gaussian closure is good to 0.5% when it
  is fed (root, variance) and 2% low when fed (mean, variance): the skewness matters, and feeding the root
  absorbs most of it. The minimising path with exact rates (42, 39.5, 35.5, 30.5, 25.5, 21.0, 17.2, 14.0, 11.2, 9.0,
  7.0, 5.5, 4.2, 3.2) has the shape of yours: four or five cells a generation, then a factor 0.78.
- **V rises with the table**: 0.2056, 0.2148, 0.2180 (a); 0.2098, 0.2168, 0.2191 (b). The steps shrink by a factor
  of about three (0.007, 0.002); if that continues the limit is 0.220, your guess. Three points.
- **Finite-size direction.** For one fixed table the increment per cell approaches V from below (0.2134 from 84 to
  168 cells against 0.2191), as in your entry 21. The measured slopes at A = 84–135 are 0.218 and 0.221, around V of
  the A = 84 table, where a fixed table would show 0.213–0.215. So the table is still changing with A (the roots
  and cumulants above; `ext`), and V of the largest table is not yet the asymptotic exponent.

**Which hypotheses carry V, and are the measured facts compatible with them?**
1. *Extensivity of the pooled one-step law.* Between A = 63 and 84 the roots collapse to 1% at x = 0.25–0.40, the
   first two cumulants to 2–8%; a doubled face of 45 is 4–7% easier to empty than a real face of 90. Compatible as a limit, not reached
   at A ≤ 84. The slab's face (E3) has a different late curve; nothing says its table is the hull's.
2. *The sparse end costs O(1)* (the continuation below row 5). Compatible with the tables in kind (above); the
   number moves by 0.012 per cell between the two continuations, more than the gap between V and ∫Θ.
3. *Decreasing paths suffice.* Confirmed for the recursion with exact rates. Not confirmed for the faces: rows
   above A/2 are untallied.
4. *The pooled table.* By Theorem P̄ the hazard is exactly the entry flux times the committor of this table, so
   V is a statement about a measured table, exact in the extensive limit. It turns "why area" into two measured
   one-step facts (extensivity, positive roots up to a fixed density) and derives neither from the rule. You say
   so; the report's sentence "the exponent is the discrete-time quasi-potential of the population's one-step
   law" should carry "of the pooled table measured in the living state" every time.

**The half of V that bounds ln τ from below is within reach of your own tools** (`supersol`). Take the m-fold
chain of a table and let W(n) = m·V(n/m) be the value of the recursion on the chain's own states, with each row's
own rate I and rising steps allowed, so that W(n) ≤ m·I(n → n′) + W(n′) for every n′. Chernoff's bound for a point
gives q(n, n′) ≤ e^{−m·I(n → n′)} with no further assumption (n′ = 0 included). For ψ = e^{−(1−δ)W}:

    Σ_{n′} q(n, n′)·ψ(n′)/ψ(n)  ≤  Σ_{n′} exp(−m·[δ·I + (1 − δ)·(I + V(y) − V(x))]),    x = n/m, y = n′/m.

Both brackets are ≥ 0 (the second is Bellman's inequality). The first vanishes only at the row's mean y = x + b(x),
and there the sum of the two is at least (1 − δ)(V(x + b) − V(x)) > 0. So on any range of densities where the drift
b and V′ are bounded below, every term is ≤ e^{−m·c(δ)}, there are at most mA + 1 terms, and ψ is a supersolution of
(∗̄) for m ≥ m₀(δ): Proposition T′ with the full exponent. Exactly, on the m-fold chain of the A = 84 table (clusters
of 5 at the bottom), the rows on which ψ is a supersolution:

| δ | m = 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|
| 0.2 | 4…42 (to the top) | 8…84 (top) | 8…168 (top) | 8…336 (top) | 8…672 (top) |
| 0.1 | 5…30 (0.71 of the top) | to 0.81 | 0.89 | 0.95 | 0.98 |
| 0.05 | 6…26 (0.62) | 0.74 | 0.83 | 0.89 | 0.95 |
| 0.02 | 13…14 (0.33) | 0.36 | 0.66 | 0.78 | 0.88 |

and where the block reaches the top row, ψ* ≤ ψ/ψ(n₀) holds, as it must. The two boundary layers (a few rows at the
bottom; the last few per cent below the mean, where b and V′ vanish) cost o(A). Written out this is **Theorem Q
with (1 − δ)·V in place of θ₀κ, for exactly extensive tables**: it contains Q (V ≥ sup κΘ(κ)), needs no Gaussian
closure and no restriction to decreasing paths, and leaves the extensivity of the real tables as the one
measured hypothesis. The other half (ψ* ≥ e^{−(1+δ)W}, a tube around the minimising path) needs a local lower
bound for each step and is not needed for a lower bound on ln τ.

### 4. Exam

- **E1 (holds), E2 (not refuted, central value high at L = 36), E3 (fails).** The consequences you draw in entry 16
  are the right ones and nothing is reinterpreted: "one remnant in every vessel" and relation (M) are withdrawn,
  Dr is restricted to hulls, "levelling off near 9–10" is withdrawn, the ring part of W is withdrawn with the
  correct reason (a product of pair weights gives L^{−1/2} whatever the weights). One caution: "the lag-2 count has
  a maximum near L = 24–32" rests on one point with a crude error (7.99 ± 0.38; chunks 7.0–8.5); "does not grow" is
  what is established.
- **E4 (filed).** Two remarks for whoever scores it. (i) The window (refuted beyond ± 0.025) is twice the distance
  between V and the withdrawn Th (∫Θ exceeds V by 0.0125 at A = 84): the entry cannot tell them apart. Ask also
  which of V, ∫Θ and the table's own slope is nearest the measured one. (ii) On the hull tables V of a table
  against the measured slope at the next sizes is 0.2056 against 0.212 (A = 45), 0.2148 against 0.212 (63), 0.2180
  against 0.218 and 0.221 (84): either sign, up to 0.006. Entry 21's fixed-table effect (slope 0.003–0.007 below V)
  is hidden by the drift of the table, which has the other sign. All of it is inside your bars.

### 5. LR12 and Lemma F (`lr12`; log `research/scratch/critic/r4_lr12.log`)

Periodic walls N × M, slab D cubes deep, integer programme over all cells (scipy's `milp`), then the
inclusion-minimal sealed sets found one by one by forbidding supersets.
- **Lemma F (iii)**: in walls 3 × 3 and 4 × 4 with D = 2, 3, 4, wall 3 × 5 with D = 2 and wall 5 × 5 with D = 4, W is
  sealed and the programme "a non-empty sealed proper subset of W" is infeasible.
- **The smallest sealed set has min(3NM, (5D + 2)·min(N, M)) cells**: 27 (3 × 3; D = 2, 3, 4), 48 (4 × 4; at D = 2 a tie
  between W and the eight transverse bands), **36 < 45 for 3 × 5, D = 2** (a transverse band is smaller than W),
  75 (5 × 5, D = 4). So **W is the smallest iff 3·max(N, M) ≤ 5D + 2**. At the measured slabs (D = 4, walls up to
  6 × 6: 18 < 22) it is, strictly.
- **Other inclusion-minimal sealed sets**: transverse bands (three consecutive y- or z-layers, even, odd, even:
  (5D + 2)·N cells: 36, 51, 66, 68, 88, 110); interior bands of three x-layers (even, odd, even: 5NM cells: 45, 80,
  125; only for D ≥ 3; at D = 2 the set of x-layers {2, 3, 4} is sealed but contains a smaller one); and irregular
  sets that are neither (39 cells in 3 × 3 × 2, by x-layer 3, 17, 6, 7, 6; 51 in 3 × 5 × 2; 56 in 3 × 3 × 3; 64 in
  4 × 4 × 2). The search for further ones was cut at 20 s per programme in the larger vessels: the list of
  shapes is not proved complete; the minima are.

### 6. Verdict on the line, and on the closing round

What stands as proved: T′, T, X, C (monotone q), F, the two-patch identity, Q as an implication; with the
earlier L1, L1′, S, P, P̄, R, R5. What fell this round, by your own hand and correctly: Th, the ring part of W,
"one remnant", the mean-field value. What is unproved and carries the line's main statement: V (a limit theorem
for extensive chains, standard in kind, not proved here and not obtained from the library) and every link from
the rule to the table (R, extensivity).

**A closing round is worth running only as a short one, and not for new mathematics.** LR10 and LR11 are
answered above; E4 does not need to be waited for (its window cannot refute V, §4). The round should do three
things and stop:
1. *State V with its continuation.* "γ = V[rates of the pooled table], the sparse end counted as O(1)": 0.2191 on
   the A = 84 hull table with exact rates (0.2180 Gaussian on root and variance), rising with the table (0.2098,
   0.2168, 0.2191), against measured slopes 0.212, 0.218, 0.221. Record the LR11 miss as a miss of the request as
   written, with the reason.
2. *Repair Q's statement*: replace "C bounded" by ln C ≤ εA (or take θ₀ no larger than the living law's
   log-slope at K) and say "by count" in the sentence on drops of one to three cells; say that R holds at A = 30
   too and that k₀ ≥ 3.
3. *One proof, which is yours to write*: the supersolution half of V for exactly extensive tables (§3, last
   part: Chernoff's point bound, Bellman's inequality, a uniform slack away from the two boundary layers). It
   would turn "V [sketched]" into "ln τ ≥ (1 − δ)·V·A − const for the m-fold family [proved]", with Theorem Q as
   the special case of one block, and it would say exactly what is assumed about the rule: that the pooled
   one-step law of a face of mA cells is, in the limit, the m-fold convolution of that of A cells. The lab's
   table (δ = 0.2 at every m; δ = 0.05 on 95% of the rows at 1,344 cells) says the statement is true on the
   chains that matter. If it resists a day's work, say where, and close.
Do not spend the round on the ring's power of L or on the sparse-face root from the rule: both are named in
your report as outside this toolkit, and I agree.
