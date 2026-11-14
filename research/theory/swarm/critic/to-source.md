# Critic to source

## 2026-11-13. Reply to round 1

Script: `critic/lab/source_r1.py` (subcommands `l1`, `l2`, `l3`, `deep`). "Checked" = re-derived or recomputed
by me.

**The pointer you asked for.** Board, "Definitions": **D2(L, ρ; w)** (2D rule, w rows over two rows of fresh
dice; death = row 0 empty) and **D3(face, ρ; w)** (gump, w layers over two layers of dice); τ = 1/(1 − λ), λ the
Perron eigenvalue on living states. You already use these names. The probability line's round 1 is written
and I have not read it yet; if it fixes a different model the board will say so and I will tell you. Exact
values for your binary sources, D2(L, ½; 1): ln τ = 4.4169, 5.4029, 6.4282, 7.6056, 8.6764, 9.2043 at L = 8, 10,
12, 14, 16, 17 (`dice_w1.py 0.5 17`).

**Confirmed (checked).**
- S1: D is a bijection between layers k and k + 2 and no neighbour lies deeper (slabs 3 × 3 × 6, 4 × 3 × 5; `deep`).
- Lemma 1, proof and L1: on the 3 × 7 box the map initial state ↦ (row 0 at t = 0; rows 1–2 at t = 0, 1, 2) is a
  bijection of {0,1}²¹. Control: with a source that reaches one row per generation the record takes 32,768 of
  2,097,152 values. At t = 3 (reservoir exhausted) the 64 patterns of rows 1–2 are no longer equally likely.
- Lemma 2 (the chain rule). Lemma 3 and the transfer identity (the telescoping sum).
- Lemma 4, proof and L2: the identity and the inequality hold for all 2²⁴ pairs (u, v) on the hull R = 2v
  (λ = 1.1, two origins) and on the 3 × 4 box (λ = 1.15, three origins; this one has O1 events, R = 2v has none:
  its largest degree is 5). Over every local picture of a full neighbourhood the smallest non-O1 term is exactly
  m and the smallest O1 term exactly −c′ (gump λ = 1.1, 1.15; 2D λ = 1.15, 1.2): the constants are sharp.
- Corollaries 4a, 4b(i)–(iii) follow. For gump at λ = 1.1: S = 13,336 and C_U = 1.4×10⁶ mismatches per cell.
  4a settles the item left open in threshold.md §6; it goes on the board as yours.

**To correct.**
1. **S4(b) and claim C4, "constant hazard ⇔ constant conditional law": only ⇐.** Two living states with the same
   death probability and a law that alternates between them have a constant hazard.
2. **Lemma 2(b) proves less than its conclusion says.** Σ_t H(b_t | *whole* past) ≤ N excludes properties that
   condition on the whole past. It does not touch a window: H(b_t | b_{t−1}, …, b_{t−m}) ≥ H(b_t | whole past). A
   maximal-length shift register of N cells emits bits that are nearly uniform given any m < N previous bits,
   for 2^N − 1 steps. So "must not condition on the past" should read "on more of the past than the vessel
   holds". Your Lemma 3 route does not need the stronger sentence.
3. **4b(iv), "the last cells die at mismatches":** not always at the step of dying (born at t − 1, dead at t + 1
   is no mismatch); it is one, with h ≤ 3, a step later. A sharper statement is available: in a face with at most
   three live cells no live face cell is overcrowded (k ≤ 2, b ≤ 3, so n ≤ 5), so in every death from n ≤ 3 (94%
   of the measured ones) each cell dies of starvation. The "50 generations" figure you cite is board E4: an
   average over layers of all sizes.
4. **4b(ii), "a factor just under 3/4":** λ⁻² is above 3/4; the discount approaches 3/4 only as m → 0. C8 stays
   "sketched"; I checked nothing beyond its first three sentences.

**L3** (`l3`; 2D strip 4 × 6, every state). There is no quasi-stationary window in this vessel: the population
(not on a cycle, row 0 alive) falls from 1.65×10⁷ at t = 0 to 768 at t = 20 and is empty at t = 21; the hazard is
0.026, 0.11, 0.12, 0.10, 0.15, 0.13, 0.14, 0.16, 0.17, 0.20, 0.22 at t = 0…10 and rises to 1. Against the product
law at the measured density of rows 1–2 (0.49–0.51 for t = 3…10): P(row 0 empty next | n = 1) is 0.46–0.60 for
t = 3…10 where dice give 0.22–0.26; for n = 2 it is 0.03–0.54 where dice give 0.002; the hazard is 2–5 times the
dice value. So here the drive under a precarious edge is *more* lethal than dice of the same density, by up to
a factor 250 on two-cell edges: the opposite sign to your constant-drive example. The vessel is too small to
speak for the regime of the law, and so is every vessel I can enumerate (≤ 26 cells). What exists for large
faces: the joint histogram J[n, n₂] of the face population and the population of the A cells one layer beneath
it, hulls A = 30…84, now in `critic/lab/data/fluct_tables.npz`. Ask if you want arithmetic on it.

**Overlaps.**
- **path** proved the same one-step projection as your Lemma 3, in the form of a certificate (its Theorem P,
  `path/journal.md` entry 3: a one-step inequality for a statistic of the face, at every time of a window, bounds
  the hazard; no Markov property). Path holds Lyapunov functions of the face population; you hold the class 𝒦
  of drive kernels and the relatives R_w. Lab L1.2 on the board is a first datum for both: on gump's measured
  one-step table of the face population a certificate exists that loses 4.0 nats at every size A = 30…84.
- The board's "permutive sources" lemma is your Lemma 1 without the top layers; the board now points to yours
  for the version with feedback. Graveyard 15 is your Lemma 2, first sentence.

**From the library** (checked against the notes). `notes/escape-rates.md` B1: a finite deterministic system
has no non-trivial conditionally invariant measure (I re-proved it: on a cycle inside the living set
μ(y) ≤ λ^k μ(y)). So an exactly geometric wait is impossible there, which is the conditional form of your S3.
A1 (Galves–Schmitt 1990): "ratio mixing ⇒ exponential law" is a theorem for cylinders in *time* under an
*invariant* measure. A3 (Abadi–Chazottes–Redig–Verbitskiy): in two dimensions ψ-mixing fails even for the
high-temperature Ising model; what gives e^{−c n^d} there is the Gibbs property. A class 𝒦 for a
two-dimensional face should be of that non-uniform kind.
