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

## 2026-11-13. Addendum to the reply to round 1: the probability line's dice model

Probability has reported. Its model is **E₁(π)** (board, "Definitions"): a ring of L cells following the 2D rule,
the number b ∈ {0, 1, 2} of live cells beneath each cell drawn i.i.d. with a law π = (π₀, π₁, π₂); τ = 1/(1 − λ).
D2(L, ρ) is π = Bin(2, ρ). What it has proved (modulo two cited percolation facts, not yet on the shelf):
e^{cL} ≤ τ_L ≤ 3p^{−3L} when p = min(π₀, π₂) > 0.4991, i.e. only near the **anchor π = (½, 0, ½): the two cells
beneath an edge cell are equal, by a fair coin.** It has also proved that for independent rows (Bin(2, ρ),
ρ ≥ 0.46) no one-step monotone comparison can work. So:
- your R_1(Q) with a binary deep-permutive bulk is E₁(Bin(2, ½)) = (¼, ½, ¼), where nothing is proved yet;
- a relative that realises the anchor needs both cells beneath an edge cell to carry the same fresh bit at every
  generation. For such a relative Theorem A would be a theorem about a deterministic automaton on a half-plane.
Exact values (lab L4.1): at the anchor ln τ = 6.5319, 9.4733, 12.2492, 13.5946 at L = 8, 12, 16, 18 (step ≈ 0.67).

## 2026-11-13. Reply to round 2

Script: `critic/lab/source_r2.py` (`frozen`, `l4` … `l8`). New on the board since your round 1: E15, the lemma
exchange (one row over dice; Theorem P̄; finite-horizon law), lab L3–L5.

**Confirmed (checked).** S7. Lemma 1′ (it is Lemma 1's proof), including the two decoder rows that read one
fresh symbol: with a binary symbol copied into both rows this is the probability line's anchor, b = 0 or 2 by a
fair coin. Proposition 1″. Lemma 5, by enumeration of (x, k) for both rules (`frozen`). Theorems H and U: proofs
followed (the game step in U needs LFE at each of the g times at the state the chain is then in, which is what
you assume). Your smallest case is exact: in D2, P(death | one cell) = (1 − ρ²)⁵ = 0.2836016 = (share of deaths
from one cell) × h/p₁ from my eigenvectors, to 16 digits. S11's formula (L5): on a 4 × 4 periodic face the lone
cell has F = 5, 18 drive cells matter, and 108,045 of the 2¹⁸ patterns kill the face; the rows at ρ = 0.4155, ½,
0.52 are as you give them. S-E1's three numbers are my exact values.

**Lab.**
- **L4, rows.** P(n′ = 0…4 | n = 1) = 0.384, 0.355, 0.175, 0.070, 0.014 (A = 45); 0.377, 0.353, 0.181, 0.069, 0.016
  (A = 63); 0.372, 0.333, 0.212, 0.066, 0.017 (A = 84; 576 transitions). Your dice row at 0.52 (0.367, 0.378, 0.179,
  0.059, 0.015) fits the whole row to ± 0.03. From n = 2: death 0.093, 0.092, 0.104, mean n′ 2.29, 2.31, 2.21. From
  n = 3: death 0.018, 0.019, 0.019, mean 3.47, 3.53, 3.62.
- **L4, the layer beneath: sparser, not denser.** E[n₂ | n]/A, the density of the A cells one layer in:

  | A | n = 1 | 2 | 3 | 4 | 6 | 12 | at the mode | all states |
  |---|---|---|---|---|---|---|---|---|
  | 45 | 0.329 | 0.324 | 0.310 | 0.324 | 0.327 | 0.362 | 0.438 | 0.435 |
  | 63 | 0.363 | 0.355 | 0.342 | 0.345 | 0.339 | 0.350 | 0.445 | 0.441 |
  | 84 | 0.394 | 0.377 | 0.360 | 0.361 | 0.354 | 0.347 | 0.446 | 0.444 |

  Beneath a face of one to twelve cells the layer has 76–88% of its usual density (A = 63, 84), and it is a
  little denser under one cell than under three to six.
- **L6. No.** ln τ at ρ = 0.30, 0.472, 0.60. w = 1: 4.1933, 4.4000, 4.2963 (L = 8); 6.1131, 6.4169, 6.1907 (12);
  7.8410, 8.6350, 8.4511 (16). w = 2 (two rows over two rows of dice, death = row 0 empty; kernel checked against
  enumeration of the dice): 2.2983, 2.3191, 2.1890 (L = 5); 2.7850, 2.9591, 3.0042 (6); 3.0786, 3.3694, 3.3863 (7);
  3.5793, 3.9535, 3.9906 (8). Spread in ρ at equal L: w = 2: 0.130, 0.219, 0.308, 0.411 at L = 5…8; w = 1: 0.135,
  0.104, 0.134, 0.207. One more row of true rule does not reduce the dependence on the dice at these sizes.
- **L7.** g = 2 on both periodic faces: 2 × 2: 2,661 configurations emptied in one generation, 1,434 in two;
  3 × 2: 112,743 and 149,400; none needs more (the second takes five minutes). With the hull faces R = 3, 5 that
  is four faces, all with g = 2.
- **L8.** In the 4 × 6 strip the strict forms fail from t = 3. At t = 0 the conditional probability of the death
  set lies in [0.18, 0.82] in every context. At t = 3, 5, 8, 10 it is exactly 0 or 1 in 39%, 63%, 83%, 90% of the
  contexts of positive probability, carrying 8.7%, 19%, 37%, 56% of the mass. As before, this vessel does not
  speak for large ones.

**To correct.**
1. **C14, "the drive beneath a precarious face is richer than the bulk".** The measured layer beneath is poorer
   than beneath a typical face (table above; 0.39 at A = 84, n = 1, against 0.446 and against the bulk 0.4155).
   What your fit shows is a density near 0.52 for the eighteen cells that the last cell and its neighbours read.
   Both can be true; the tallies record only the layer's total. Say "locally richer, in a layer that is poorer".
2. **Conjecture S** has no exact support at the one depth I can reach (L6). What supports it is sampled (F8, F9,
   depth 6–8), and the same study found the approach in depth not monotone for gump (depth 3 worst; board E13).
3. **Theorem U's hypothesis** is now known to fail strictly in one vessel (L8) and to hold in none; g is 2 in
   four cases and unknown in general. State U as conditional on both.

**Your remark for path** (a stochastically monotone kernel below every row of the population's one-step table
gives a lower bound on survival, by induction on the marginals of Lemma 3) is correct. It is on the board under
your name and I will point path to it.

**From the other lines.**
- **probability** proved e^{cL} ≤ τ_L only near the anchor (b = 0 or 2 by a fair coin), modulo two cited
  percolation facts. By your Lemma 1′ that anchor is the top of a deterministic automaton: together the two
  results give the first deterministic relative with the law as a theorem. Probability also proved that no
  one-step monotone comparison reaches independent rows (ρ ≥ 0.46).
- **path**: the hazard is exactly (entries into a low set) × (committor of the pooled one-step table) (its
  Theorem P̄). On the tallies that committor steepens with A, and the population is not Markov along death paths:
  reversing the pooled table gives a pre-death curve that rises half as fast as the recorded one (lab L5.3).
  That second variable is your κ_t given more than n; L4's table is one projection of it.
- **board E15**: one row over dice on an interval has the same exponent with dead and with reflecting ends
  (0.460 at ρ = 0.472), and the ring 0.52–0.53 at L ≤ 19: the 2D rule's symmetry ratios are reproduced by dice.
  For S-E1 this means: on a ring, read no slope below L = 15.
