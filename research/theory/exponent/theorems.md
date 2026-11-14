# Rigorous statements for the exponent study

*Part of `research/theory/exponent.md` (section 7 there is a summary of this file). Everything here is **[proved]**:
complete arguments, plus a brute-force check where one is cheap (`game_check.py`) — except one sentence of
Lemma A (c), which was false and is corrected in place (2026-11-14), and Remark 1 of E, whose example is withdrawn
(revision of 2026-11-14 after `research/audit/REVIEW-exponent.md` §4, cited R§4; the review checked every proof
here line by line). Notation: the toy is B34/S234 on
the cross `(±1,0), (±2,0), (0,±1), (0,±2)`; the edge is row 0 of a vessel periodic along x with L columns; for an
edge cell x, k = number of live cells among its four in-row neighbours x±1, x±2 and b ∈ {0,1,2} = number of live
cells among the two cells beneath it (rows 1 and 2, same column). Its next state is 1 iff k + b ≤ 4 and
k + b + (own state) ≥ 3.*

## A. Safe and inert cells

**Lemma A.** (i) A live edge cell with k = 2 is alive in the next generation whatever lies beneath it. (ii) A dead
edge cell with k = 0 is dead in the next generation whatever lies beneath it. (iii) In all eight other cases
(state, k) both outcomes occur, each for at least one value of b.

*Proof.* Live, k = 2: n = 2 + b ∈ {2,3,4}, survives. Dead, k = 0: n = b ≤ 2 < 3. Otherwise: live cells survive
exactly for b ∈ {2−k, 3−k, 4−k} ∩ {0,1,2} = {2} (k = 0), {1,2} (k = 1), {0,1} (k = 3), {0} (k = 4); dead cells are born
exactly for b ∈ {3−k, 4−k} ∩ {0,1,2} = {2} (k = 1), {1,2} (k = 2), {0,1} (k = 3), {0} (k = 4): in each case a proper
non-empty subset of {0,1,2}. ∎ (`game_check.py` re-derives the table from the rule.)

Consequences. (a) If the edge is empty at generation t + 1, then at generation t no live edge cell had exactly two
live in-row neighbours (so, for instance, no run of three or more live cells had two dead cells beyond either end; for this example
L ≥ 6, so that the two cells beyond an end are distinct from the run, R§4).
(b) Cells of a dead stretch at distance ≥ 3 from the nearest live edge cell
stay dead: a gap closes only from its two ends, by at most two cells per end per generation.
(c) **Gump has no safe face cell**: a live face cell with k of its 6 in-layer neighbours alive survives iff
3 ≤ k + b ≤ 5 with b ∈ {0,1,2,3} the live cells among its three neighbours beneath, and for every k some b kills it
(k ≤ 2: b = 0; k = 3: b = 3; k = 4: b ≥ 2; k ≥ 5: b ≥ 1). This is a statement about one cell at a time and it is
true.

*Correction, 2026-11-14 (successor; the original sentence is kept here struck through so that readers of older
copies can find it):* ~~"A gump face can always die in one generation given suitable layers beneath; the toy's
edge cannot (Theorem B)."~~ **This was false.** It does not follow from the per-cell statement, because in gump
neighbouring face cells *share* cells beneath them (a cell one layer in neighbours several face cells; the three
faces of one cube form the shared triples, `research/theory/swarm/critic/board.md`, "cube lemma"), whereas in the
toy each edge cell's two cells beneath are its own (which is what makes the game of Theorem B factorise).
Counterexample (board item E10), in the face layer x + y + z = 13 of a hull or periodic slab with every other face
cell dead: live (4,4,5), (4,5,4), (5,4,4), (3,4,6). The cell (4,4,5) has k = 3 and dies only if all three cells
beneath it are alive, (3,4,4) among them; (4,5,4) has k = 2 and dies only if all three beneath it are dead,
(3,4,4) among them. Re-checked 2026-11-14 by direct enumeration of the neighbourhood of `docs/AUTOMATON.md` §2, and
with `python3 face_one_step_interior.py` (`research/theory/swarm/critic/lab/`; deep interior of the R = 13 face,
so no rim is involved). What is true instead (exact, critic's lab, re-run here for R = 3):
`python3 face_one_step.py 3` → 187 of the 512 configurations of the R = 3 hull face cannot be emptied in one
generation whatever the 15 cells beneath are; 180,615 of the 262,144 configurations of the R = 5 face cannot
(`startpoints.py game 5`, board lab L0b.3, not re-run here); every configuration of those two hull faces and of the
periodic faces 2 × 2 and 3 × 2 *can* be emptied in **two** generations (board, "lemma exchange"); larger faces are
unknown. So the contrast with the toy is not "one generation against three" but "two (at least for these small
faces) against three", and no statement about gump faces in general is proved.
Nothing else in this file or in the study's measurements uses the false sentence: Theorem B and B′ concern the toy
only, and the study's gump results are measurements.

## B. Three generations, never fewer in general

Consider the *game* in which the two rows beneath the edge are chosen freely each generation. By Lemma A, from a
live set S ⊆ Z_L the possible next live sets are exactly the S′ with

  F(S) ⊆ S′ ⊆ S ∪ N(S),  F(S) = {x ∈ S : k_S(x) = 2},  N(S) = {x ∉ S : k_S(x) ≥ 1},

because each cell's outcome depends on its own b only.

**Theorem B.** Let L ≥ 5. (a) From every configuration of the edge row the rows beneath can be chosen so that the
edge is empty after three generations. (b) For L ≥ 9 the lone triple `111` (all other edge cells dead) cannot be
emptied in two.

*Proof.* (a) Let S₀ ≠ ∅. *Generation 1:* take S₁ = S₀ ∪ N(S₀) = {x : dist(x, S₀) ≤ 2} (allowed: forced cells are
kept, every other live cell may be kept, every dead cell with k ≥ 1 may be born). S₁ is the whole ring or a union
of arcs of at least 5 consecutive cells separated by gaps. In S₁ a cell at distance ≥ 2 from both ends of its arc
has k = 4; the cell next to an end has k = 3 (its outer neighbours are the end cell and the first gap cell); an end
cell has k = 2 if the gap it faces is at least two cells long and k = 3 if that gap is a single cell. So F(S₁) is the
set of arc ends that face gaps of length ≥ 2. *Generation 2:* take S₂ = F(S₁) (allowed: everything not forced is
killed, nothing is born). Two cells of S₂ are either the two ends of one arc (≥ 4 apart along the arc) or lie on
opposite sides of a gap of length ≥ 2 (≥ 3 apart), so every cell of S₂ has k = 0 and F(S₂) = ∅. *Generation 3:* kill
them (b ≤ 1 beneath each) and let nothing be born: S₃ = ∅.
(b) S₀ = {2,3,4}: all three cells are forced, so S₁ ⊇ {2,3,4} and S₁ ⊆ {0,…,6}. Emptying at generation 2 needs
F(S₁) = ∅. The leftmost cell of S₁ has no live neighbour on its left (L ≥ 9), so it needs at most one live cell among
its two right neighbours; that rules out leftmost = 2 (3, 4 alive) and leftmost = 1 (2, 3 alive), so 0 ∈ S₁, 1 ∉ S₁,
and symmetrically 6 ∈ S₁, 5 ∉ S₁. Then cell 3 has exactly the neighbours 2 and 4: forced. ∎

*Brute force* (`python3 game_check.py 13`): for L = 5…13 every configuration is emptied in ≤ 3 steps by the strategy
of the proof, and for L = 9…13 the configurations that need three are exactly the L rotations of the lone triple;
all others can be emptied in two (L = 13: 989 in one, 7,189 in two, 13 in three).

**Corollary B′ (driven edge: an exponential upper bound).** Let the edge row be driven by any random field
b_t(x) ∈ {0,1,2} such that, conditionally on the past, the b_t(x), x ∈ Z_L, are independent and each value has
probability ≥ δ > 0 (e.g. the w = 1 model of exponent.md: b the sum of two independent Bernoulli(ρ) cells,
δ = min(ρ², (1−ρ)²)). Then from every state P(edge empty within 3 generations) ≥ δ^{3L}, so
P(T > 3j) ≤ (1 − δ^{3L})^j and **E T ≤ 3 δ^{−3L}**. For ρ = 0.472 (δ = 0.472² = 0.2228, −3 ln δ = 4.505) this is ln τ ≤ 4.50·L + 1.1 against the true
0.53·L: the bound has the right form and a poor constant.

## C. The noisy toy

**Theorem C.** Let every live cell also die independently with probability ε ∈ (0,1) after each generation of the
toy (any finite vessel; the edge has L cells). Then from every state P(edge empty at the next generation) ≥ ε^L,
hence P(T > t) ≤ (1 − ε^L)^t and **E T ≤ ε^{−L}**.
*Proof.* After the deterministic step at most L edge cells are alive; the noise kills all of them with probability
≥ ε^L, independently of the past. ∎
No lower bound of the form E T ≥ e^{cL} is proved for any ε or for the deterministic rule; see "What is not proved".

## D. The death rate is the quasi-stationary mass of the pre-death set

**Theorem D** (Darroch–Seneta 1965, specialised). Let Q be the transition kernel of a finite Markov chain
restricted to its non-absorbed states S, d(x) = 1 − Σ_y Q(x,y) the probability of absorption in one step, and μ a
quasi-stationary distribution, μQ = λμ. Then started from μ the absorption time is exactly geometric:
P_μ(T > t) = λ^t with **1 − λ = h = Σ_x μ(x) d(x)**. If Q is irreducible and aperiodic on S, μ is unique, and for
every x ∈ S, P_x(T > t) = c(x) λ^t (1 + o(1)) and the law of X_t given T > t converges to μ.
*Proof.* P_μ(T > t) = μQ^t 1 = λ^t; 1 − λ = μ(1 − Q1) = μ(d). The rest is Perron–Frobenius. ∎

**Proposition D′.** The w = 1 driven-edge model with 0 < ρ < 1 is irreducible and aperiodic on the non-empty rows
(L ≥ 5), so Theorem D applies in full: its death time is asymptotically exactly geometric from any living start.
*Proof.* In the game of Theorem B every allowed move has positive probability. From any S ≠ ∅ the moves
S ↦ S ∪ N(S) reach the full ring in at most ⌈L/4⌉ steps. In the full ring every cell has k = 4, so F = ∅ and every
subset of the ring, including the ring itself, is an allowed next state. ∎

For the *deterministic* toy and gump there is no such statement: conditioned on surviving for ever longer times, a
uniformly random initial state concentrates on the basins of immortal cycles (debris that touches every edge;
exponent.md §6.2 counts them exactly). "Memoryless with rate h" is there a measured property of soups with settled
states censored, not a theorem.

Nor does D′ extend to gump's driven-face models (the swarm's D3, `xp.gump_model`, `xp.gump_slab_model`), although they
are finite chains with fresh noise every generation: they are not irreducible on the living states. The six faces of
the cube centred at (6,0,0) alive in `gump_model(7, 4)`, every other dynamic cell dead, is a fixed point whatever the
noise does (every dynamic cell's next state is forced); the vertex cube is immune in every hull model with w ≥ 4 and
a cube in the face interior in every hull or periodic model with w ≥ 5 (R§1.3; `research/audit/exponent/trap.py`).
So these chains have a second absorbing class besides death; Theorem D applies to the chain killed on both, and model
runs must censor repeating dynamic states. Whether the toy models with w ≥ 2 have such states is not settled here.

## E. What mixing hypothesis gives exponential-in-L lifetimes

Let μ be quasi-stationary (Theorem D) for a chain whose absorbed set is "edge row empty", and let ν be the law of
the edge row one generation after a μ-distributed state, so that h = ν(the whole row is empty). Cut Z_L into
consecutive blocks B₁, …, B_J of m cells (J = ⌊L/m⌋), and write A_j for "B_j is empty".

**Theorem E.** (a) If for some θ < 1 and all j, ν(A_j | A₁ ∩ … ∩ A_{j−1}) ≤ θ, then h ≤ θ^J and
**τ = 1/h ≥ θ^{−⌊L/m⌋}**. (b) In particular, if ν is ψ-mixing along the row in the sense that
ν(A ∩ B) ≤ (1 + Ψ) ν(A) ν(B) whenever A and B are determined by sets of cells at distance ≥ m, and
ν(A_j) ≤ q with (1 + Ψ) q < 1, then τ ≥ [(1 + Ψ) q]^{−⌊L/2m⌋}. (c) If, conversely, ν(cell x empty | all other
cells) ≥ δ for all x, then τ ≤ δ^{−L}.
*Proof.* (a) h ≤ ν(∩_j A_j) = Π_j ν(A_j | A₁ … A_{j−1}) (equality when mJ = L; otherwise the blocks miss L − mJ
cells). (b) (Ψ ≥ 0.) Apply the hypothesis to the ⌊J/2⌋ odd-numbered blocks in turn: B_{2i+1} is at distance ≥ m
from B₁ ∪ B₃ ∪ … ∪ B_{2i−1}, and using only ⌊J/2⌋ of them handles the wrap-around. (c) Chain rule over cells. ∎

Two remarks (both revised 2026-11-14, R§4).
1. **Correlation decay against ratio mixing: the example is withdrawn (R§4).** The earlier text said that
   exponentially decaying correlations are not the right hypothesis (PROGRAM M2, OPEN-PROBLEMS item 3 as worded) and
   gave the mixture ν = (1 − a) ν₀ + a δ_∅, a = e^{−√L}, with ν₀ having exponentially decaying correlations and
   ν₀(row empty) = e^{−cL}. ~~"Every covariance of observables bounded by 1 changes by at most 4e^{−√L}, so
   correlations at distance r ≤ L/2 are still bounded by C e^{−r/ξ} + 4e^{−√L}, while ν(row empty) ≥ e^{−√L}: the
   wait is sub-exponential."~~ **The example does not satisfy its own hypothesis.** The covariance of the indicators
   "cell x empty", "cell y empty" under ν is a(1 − a)(1 − ν₀(x empty))(1 − ν₀(y empty)) + (1 − a) Cov₀ ≈ a/4 at
   *every* distance, so correlations stop decaying at distance ≈ ξ√L: the family does not have exponentially
   decaying correlations with constants uniform in L, which is what M2 / item 3 mean. (For single-cell covariances to
   stay below C e^{−r/ξ} up to r = L/2 the weight must be a ≲ e^{−L/(2ξ)}, which makes the wait exponential again: no
   mixture of this kind can be a counterexample.) What the example does show: **an additive correlation floor of
   order e^{−√L} suffices to break the implication** from small covariances to an exponential wait. Whether
   exponential correlation decay with uniform constants implies an exponential wait, or a ratio (ψ- or hyper-)
   mixing bound of the kind that makes large deviations multiply (Bryc; Deuschel–Stroock) is really needed, is
   **open**. The critic's board (graveyard 3, "checked") repeats the same example and has the same gap.
2. **The hypothesis of (a) is a statement about the ring's own quasi-stationary law, and it is not measured.** For
   the ring of L cells it says that the empty-block probabilities of ν satisfy the ratio bound for every block, i.e.
   for empty-window lengths up to L. What exponent.md §4 measures is the empty-window probability E(ℓ) of a
   different system — the long 16 × 128 deterministic strip, for which no quasi-stationary law exists (Theorem D,
   remark above) — for ℓ ≤ 41 only (E(ℓ + 1)/E(ℓ) ≤ 0.688 for 5 ≤ ℓ ≤ 41). The measurement makes the hypothesis
   plausible for ℓ ≤ 41; it does not supply it (R§4), and Theorem E does not turn it into "τ ≥ e^{cL} with c = the
   smallest measured decrement of −ln E".

## What is not proved

- Any lower bound τ ≥ e^{cL}, for the deterministic toy, the noisy toy, or the driven-edge models. For the w = 1
  model this is the survival of a non-attractive one-dimensional probabilistic cellular automaton. The standard
  route (a block event that reproduces itself whatever the outside does, then comparison with oriented
  percolation) fails at the first step for a structural reason: the rule is not monotone, and an unknown outside
  contaminates two cells per side per generation — the same speed at which anything can spread — so no finite block
  can guarantee its neighbours. A proof would need a different idea (e.g. a monotone functional of the pair
  "configuration, set of safe cells").
  *Note, 2026-11-14 (successor):* the critic's board (`research/theory/swarm/critic/board.md`, graveyard item 6)
  accepts only the second reason. The comparison theorem with oriented percolation (Durrett, *Ten lectures*,
  Thms 4.1–4.3) assumes no monotonicity; what blocks it is that the good event must work for every configuration
  outside the block, and an unknown outside contaminates two cells per side per generation. With dice beneath (the
  driven-edge models) the adversary is only the rest of the same row. The board also reports a lower bound
  e^{cL} proved since by another line for a dice law near "b = 0 or 2 by a fair coin" (probability's Theorem A,
  modulo two cited percolation facts): a claim of that line, not checked here, and not for the w = 1 model
  with independent rows.
- Existence of the limit lim L⁻¹ ln τ_L for any of the systems.
- That the deterministic rule is the ε → 0 limit of the noisy one (measured in exponent.md §9, not proved).
