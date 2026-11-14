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

## 2026-11-14. Reply to round 3 (S13–S16 and the interim report)

Script: `critic/lab/source_r3.py` (`a`, `l`, `c18`, `ins`). "Confirmed" = re-derived or recomputed by me. Board ids:
L10.1–L10.4. F1 and F2 are still not on the shelf.

### 1. The three claims you list as unchecked

- **C16, Theorem A.** (i) **Confirmed.** The argument: y_t(x, 1) = y₀(x, 2t + 1) = ξ_{x,t+1} = y₀(x, 2t + 2) = y_t(x, 2), a bit
  not read before. By enumeration (`a`): 𝒜(5) with six rows beneath, all 2²⁰ starts (row 0 and the fifteen bits):
  the two cells beneath every edge cell are equal at every generation, and for every S₀ the law of (S₁, S₂, S₃) is
  that of E₁(½, 0, ½), to the last digit, over all 2²⁰ paths. With the bit 0 the cell follows B34/S234 on its four
  in-row neighbours and with the bit 1 B12/S012, as your table says. The exact geometric wait from μ_L ⊗ start
  follows as in your Proposition 1″. (ii) is the probability line's and stands modulo F1, F2; 3·8^L is its bound
  at p = ½. (iii) The four numbers are lab L4.1.
  One number to add to your table of differences. "≈ 0.67 per cell" is the ring's step at L = 18, still falling
  (0.685, 0.679, 0.675, 0.671 at 15…18). On an interval the same chain has step **0.6236**, with dead ends and with
  reflecting ends alike, converged to four decimals from 18 cells (lab L8.5; ln τ = 12.9993 and 12.8704 at 19
  cells). The ring's excess over it is 0.84/L at L = 18 and shrinking.
- **C17, Theorem L. Confirmed.** Proof re-derived: INS(p) given the row and the other cells' drive implies each
  indicator has conditional probability ≥ p given the earlier ones in any order; the thinned ω is i.i.d.
  Bernoulli(p) and independent of (z, W); W′ ⊆ Z_{t+1}; only the law of the pair at one time is carried. An exact
  example in which the drive is neither a product nor independent of the row (`l`; ring of 6; b = 2c with c drawn
  each generation from an Ising ring whose coupling is +0.2 or −0.2 according to the parity of the row's
  population): INS holds with p = 1/(1 + e^{0.8}) = 0.3100, and at every t = 1…8, from three starts, a coupling with
  W_t ⊆ Z_t exists (a linear programme over the 3⁶ nested pairs). Against OP₅(0.6) the programme is infeasible at
  t = 1, so the test can fail.
  Remark (c), exactly, in the one vessel where it can be computed (`ins`; 2D strip 4 × 6, uniform start, every
  state; a = P(x alive next | the edge row, the cells beneath the other edge cells), over cells within distance 2
  of a live cell): the smallest a is 0 from t = 1 on; the share of the mass with a = 0 is 0.2%, 1.9%, 2.6%, 6.6%,
  14.8%, 27.5% at t = 1, 2, 3, 5, 8, 10; the share with a < 0.4991 is 40–48% at every t ≥ 1 (22.6% at t = 0, where the
  cells beneath are still nearly fair dice). So INS(p) fails there for every p > 0, as finite energy did (L8). The caution of round 2 applies
  again: that strip is extinct by generation 21 and has no steady state.
  Remark (d), the lag-k form: right if "the corresponding domination" means that K_t^{(k)}(z, ·) dominates the
  k-step law of a monotone comparison process started from z, for every z. Not checked beyond that sentence.
- **C18. Confirmed** by the rule table (`c18`): six live in-face neighbours kill a gump face cell for every
  b ∈ {0, 1, 2, 3}; a dead face cell with three live in-face neighbours is born iff b ∈ {1, 2}; every 2D edge cell
  within distance 2 of a live one is alive for b = 0 or for b = 2.

S13: the three corrections agree with the lab tables they cite.

### 2. The two computations you suggested "if someone continues"

- *Dice rows of small shapes* (`counting_r2.py small`; exact; P(face empty next) at ρ = 0.4155, ½, 0.52). Two cells
  in one cube: 0.194, 0.0783, 0.060. Two adjacent cells in different cubes: 0.156, 0.0572, 0.043. Two cells adjacent
  across a hexagon: 0.214, 0.0877, 0.068. Near, not adjacent: 0.154–0.282, 0.056–0.123, 0.042–0.097. The triangle of
  one cube: 0.0172, 0.0036, 0.0023. The triangle of the other orientation (three cubes): 0.0052, 0.0009, 0.0006.
  Measured: 0.09–0.10 from two cells, 0.018–0.019 from three. The two-cell value sits among the dice values at
  ρ ≈ ½, as the one-cell row does at 0.52. The three-cell value is five to eight times the cube triangle's at
  ρ = ½ and 0.52; with 38% cube triangles (one vessel) it is reached at ρ = ½ only if the other three-cell
  faces are loose placements (0.03–0.037 each), not paths (≤ 0.01).
- *INS in the 4 × 6 strip:* above.

### 3. Your assessment (S16): do I agree that the line has given what it can?

Yes, as an independent line, for these reasons.
1. **Aim (a) is done as far as any dice theorem exists.** Every dice model with rational local randomness is the
   top of a deterministic automaton (C1, C1′, both confirmed), with an exact geometric wait (C1″), and for the
   one dice model that has a lower bound the joint statement is written and confirmed (Theorem A). Nothing in
   your toolkit can add a lower bound; that is the probability line's work.
2. **Aim (b) has an answer, and it is negative for every property tried.** Lemma 3 reduces the death law to the
   equal-time kernel κ_t; Lemma 2 and Lemma 5 exclude conditions on the past; Theorems H, U and L say what
   equal-time conditions would give. Each of those conditions fails strictly where it can be computed. Theorem L
   also shows that the obstacle to the one existing theorem is not the bulk: it fails already for honest dice
   at the bulk density.
3. **What is left open is not reachable by permutivity, entropy or projection.** Conjecture S is a statement
   about dice models at depth (the lab reaches depth 2 exactly and finds no screening; S-E2 will test depth 6).
   The class 𝒦 needs a dice theorem that tolerates cells kept alive with probability near ¼; that is the
   probability line's T1, not started.

Two reservations, which do not change the verdict.
- "The hypotheses fail in the one enumerable vessel" is weaker evidence than it sounds, in both directions. The
  strip 4 × 6 has no steady state, and exact zeros of a conditional probability in a vessel of 24 cells are partly
  an effect of its size (few states remain; 33,294 contexts at t = 10). Whether κ_t in a long-lived vessel has
  insertion tolerance at some small p is not known and cannot be learned exactly; it would take tallies of the
  drive given the face in a sampled run, which this group does not do.
- The line should be recalled for one job if the occasion arises: when probability has a multi-generation
  criterion (T1) or a dice theorem for a gump face (T3), the lag-k form of Theorem L and the deterministic
  relative are short work for which the lemmas are already here. C18 says what a relative of the gump face must
  allow (b ∈ {1, 2} for births next to three live cells; no protection from overcrowding).

### 4. Overlaps and news

- **probability, Theorem A′** (its entry 6, round 2; confirmed) is the same transfer statement as your Theorem L:
  its hypothesis is P(b_y = 0 | everything else) ≥ p and P(b_y = 2 | everything else) ≥ p with "everything else"
  including the whole past, and its conclusion a coupling of paths. Your hypothesis is implied by it (tower
  property) and is strictly weaker; your conclusion is the domination of the law at each time, which is what a
  survival bound uses. Neither line had seen the other's statement.
- **probability, exact** (lab L8.1): five-parent oriented site percolation at p = ½, the minorant your Theorem L
  and its Theorem A use, has interval step 0.3815 and ring step 0.4191 at 19 cells; a rough reading of rings of
  15–17 cells puts its critical density between 0.36 and 0.44 (proved: ≥ 1/3). So the comparison can reach at most
  p > 0.36–0.44, far above what independent dice at the bulk density supply (0.22).
- **counting, exact** (lab L7.8): from a soup of density ½ the cheapest one-generation death of a gump face is the
  crowded face (87% alive; 0.4807 per cell on a strip three cubes wide, against 0.5101 for the thin route); at the
  bulk density 0.4155 the thin route wins (0.3404). This is your remark C18 with numbers.
- **path** has been given your monotone comparison for a projected statistic, with what the pooled tables show:
  each is a stochastically monotone kernel, and at equal population the larger face's row dominates the
  smaller's up to +0.007 in the distribution function (lab L9.2).
