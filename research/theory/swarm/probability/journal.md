# Probability line: journal (append-only)

Successor: read `claims.md` first (current state), then this file. Everything here is mathematics done by hand;
numbers were evaluated with Python as a calculator (formulas given). Nothing was simulated.

## 2026-11-13, entry 1: the dice model, its τ, and notation

**The model E₁(π)** (the 2D rule; "driven edge", the w = 1 model of `exponent/theorems.md`, with a general
noise law). State: a set S_t ⊆ Z_L of live edge cells (ring of L ≥ 5 cells). For a cell y write x = 1[y ∈ S_t]
and k = |S_t ∩ {y±1, y±2}|. Each generation every cell draws b_t(y) ∈ {0, 1, 2}, independent over cells and
generations, with law π = (π₀, π₁, π₂); then

    y ∈ S_{t+1}  iff  k + b ≤ 4  and  k + b + x ≥ 3.

This is the true rule B34/S234 on the edge row with the two cells beneath each edge cell replaced by dice
(b = number of live cells beneath). π = Bin(2, ρ), i.e. ((1−ρ)², 2ρ(1−ρ), ρ²), is "fresh independent rows";
ρ = 0.472 is the bulk density. ∅ is absorbing. T = first t with S_t = ∅.

**Table of a(x, k) = P(alive next | x, k)** (from the rule; the lab can re-derive it):

| k | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| live (x = 1) | π₂ | π₁+π₂ | 1 | π₀+π₁ | π₀ |
| dead (x = 0) | 0 | π₂ | π₁+π₂ | π₀+π₁ | π₀ |

At π = Bin(2, 0.472): live 0.2228, 0.7212, 1, 0.7772, 0.2788; dead 0, 0.2228, 0.7212, 0.7772, 0.2788.

**Which τ.** Assume π₀, π₂ > 0. Then (i) from every S ≠ ∅ the full ring is reached in m = ⌈L/4⌉ steps with
probability ≥ p^{Lm}, p := min(π₀, π₂) (make every cell of S ⊕ [−2,2] alive, each has probability ≥ p by the
table, cells are independent given S; the full ring stays full with probability π₀^L); (ii) from the full ring
every subset is a possible next state; (iii) by the three-move game (theorems.md B(a); every move used there has
probability ≥ p per cell, also when π₁ = 0, check the table), P_S(T ≤ 3) ≥ p^{3L} for every S. So the chain on
non-empty states is irreducible and aperiodic, there is no immortal state, E_S T ≤ 3p^{−3L} for all S, and the
quasi-stationary law μ is unique. I define

    τ_L := 1/(1 − λ_L),  λ_L = Perron eigenvalue of the kernel restricted to non-empty states
         = E_μ T  (Darroch–Seneta),

which is the board's "hazard among living replicas" with nothing to censor. All my statements are about τ_L.

**From a statement about one start to τ_L** (used below). If P_full(T > t) ≥ 1/2 then
λ^{t+m} ≥ p^{Lm}/2, hence τ_L ≥ (t + m)/(Lm ln(1/p) + ln 2).
*Proof.* u := P_full(S_{t+m} = full) ≥ P_full(T > t)·min_{S≠∅} P_S(S_m = full) ≥ p^{Lm}/2; by the Markov property
P_full(T > n(t+m)) ≥ u^n; and P_full(T > n) = cλ^n(1 + o(1)). Finally 1 − λ ≤ ln(1/λ). ∎

**Notation.** OP₅(p): the attractive process on subsets of Z_L (or Z) with η_{t+1} = {y ∈ η_t ⊕ [−2,2] : U_{t+1}(y) ≤ p},
U i.i.d. uniform: oriented site percolation in which (y, t+1) has the five parents (y+i, t), |i| ≤ 2.
p_c^site: the critical density of ordinary oriented site percolation in 1+1 dimensions (two parents).

## 2026-11-13, entry 2: Lemma 1 (product structure; the sharp one-step attractive minorant)

**Lemma 1.** (a) Given S_t, the events {y ∈ S_{t+1}}, y ∈ Z_L, are independent, with probabilities a(x_y, k_y).
(b) Let η ⊆ S. For every y,
  q(y; η) := min over S′ ⊇ η of P(y ∈ S_{t+1} | S_t = S′)
depends only on whether y ∈ η and on j = |η ∩ {y±1, y±2}|, and with s := min(π₀, π₂), m := min(π₀, 1 − π₀):

| j | 0 | 1 | 2 | ≥ 3 |
|---|---|---|---|---|
| y ∈ η | s | m | π₀ | π₀ |
| y ∉ η | 0 | s | m | π₀ |

(c) The PCA η with these rates (cells independent given η_t) is attractive, and if η_0 ⊆ S_0 there is a coupling
with η_t ⊆ S_t for all t. It is the largest such process: any PCA ζ with conditionally independent cells whose rates
satisfy r(y; ζ) ≤ P(y ∈ S_{t+1} | S_t = S′) for all S′ ⊇ ζ has r ≤ q.
(d) In particular S_t dominates OP₅(s): every cell within distance 2 of a live cell is alive next generation with
probability ≥ s = min(π₀, π₂), whatever the rest of the row is.

*Proof.* (a) y's fate is a function of S_t and b_t(y) alone. (b) Minimise the table over x ∈ {1} (y ∈ η) or
x ∈ {0, 1} (y ∉ η) and k ∈ {j, …, 4} (the unknown neighbours may all be alive); e.g. y ∈ η, j = 1:
min(π₁+π₂, 1, π₀+π₁, π₀) = min(1 − π₀, π₀). (c) q(y; ·) is non-decreasing in η (a minimum over a smaller family).
Coupling: with one uniform U_t(y) per cell and generation, put y ∈ η_{t+1} iff U ≤ q(y; η_t), and draw b_t(y) as a
function G_{x,k}(U) with the law π and with G_{x,k}(U) in the alive-set of (x, k) whenever U ≤ a(x, k) (possible for
each (x, k) separately). S then has the right law, because given the past the b_t(y) are i.i.d. π; and
η_t ⊆ S_t gives q(y; η_t) ≤ a(x_y, k_y), so η_{t+1} ⊆ S_{t+1}. (d) All non-zero entries are ≥ s. ∎

*Smallest case.* S = {0}: cell 0 has (x, k) = (1, 0), cells ±1, ±2 have (0, 1): all five are alive next with
probability π₂ ≥ s, everything else stays dead. So one isolated cell is exactly one step of OP₅(π₂).

**Two facts about what the cap costs, read off the table.** (1) s ≤ 1/2 for every π: a crowded cell (k = 4)
needs b = 0 and an isolated one needs b = 2. For independent rows, s = min(ρ², (1−ρ)²) ≤ 1/4.
(2) There is no analogue of (d) for more than one deterministic row, nor for a gump face with i.i.d. b ∈ {0,…,3}:
in the two-row model (rows 0, 1 by the rule, rows 2, 3 dice) the all-alive slab dies in one generation whatever
the dice show (row 0: k + s₁ = 5; row 1: k + s₀ = 5), and a gump face cell with all six in-face neighbours alive
has n ≥ 6. A one-step worst-case comparison exists only for the single driven row of the 2D rule.

## 2026-11-13, entry 3: Theorem A (the law is a theorem near a percolation anchor)

**Theorem A.** Let π have p := min(π₀, π₂) with 1 − (1−p)² > p_c^site. Then there are c = c(π) > 0 and L₀ such
that for all even L ≥ L₀

    e^{cL} ≤ τ_L ≤ 3 p^{−3L}.

The set of such π is non-empty if p_c^site < 3/4 (it then contains π = (½, 0, ½): the two cells beneath an edge
cell are both dead or both alive, a fair coin). Rigorous: p_c^site ≤ 0.7491 (Balister–Bollobás–Stacey 1994), which
gives every π with min(π₀, π₂) > 0.4991. Numerically p_c^site ≈ 0.7055, i.e. min(π₀, π₂) > 0.4574.

*Proof.* Upper bound: entry 1 (iii). Lower bound: by Lemma 1(d) couple η = OP₅(p) below S, η_0 = S_0 = full ring.
Blocks in a drifting frame: X_i^t := {2i + t, 2i + t + 1} (mod L), i ∈ Z_{L/2}; for each t they partition the ring.
ξ_t(i) := 1[η_t ∩ X_i^t ≠ ∅]. The child block X_i^{t+1} = {2i+t+1, 2i+t+2} lies within distance 2 of *every* cell
of X_i^t ∪ X_{i+1}^t = {2i+t, …, 2i+t+3}. So if ξ_t(i) ∨ ξ_t(i+1) = 1, both cells of X_i^{t+1} are in η_t ⊕ [−2,2]
and ξ_{t+1}(i) = W_{t+1}(i) := 1[U_{t+1} ≤ p at one of the two cells]. The W_{t+1}(i) are i.i.d. Bernoulli(p′),
p′ = 1 − (1−p)², independent of the past. Hence ξ dominates ordinary oriented site percolation of density p′ on the
cylinder Z_{L/2} × N started full (site (i, t) → (i, t+1), (i−1, t+1)).
Fact F2 (below): for p′ > p_c^site that percolation survives to time e^{c₁K} on a cylinder of circumference K
with probability ≥ 1/2, K large. So P_full(T > e^{c₁L/2}) ≥ 1/2 and entry 1 gives
τ_L ≥ e^{c₁L/2}/(L² ln(1/p)) ≥ e^{cL}. ∎

*Smallest case of the block step.* L = 6, t = 0, S_0 = {0}: X_0^1 = {1, 2} and X_2^1 = {5, 0} are the two children of
X_0^0 = {0, 1}; all four cells are within distance 2 of cell 0, each alive at t = 1 with probability ≥ p.

**What is cited, not proved here** (I opened neither paper; a web search returned only a secondary source
confirming the number 0.7491 for Balister et al.):
- F1: p_c^site ≤ 0.7491, Balister, Bollobás, Stacey, Random Structures Algorithms 5 (1994) 573–589;
  ≤ 3/4, Liggett, Ann. Appl. Probab. 5 (1995) 613–636. With only Liggett's 3/4 the anchor (½, 0, ½) sits exactly on
  the bound (p′ = 3/4), so the theorem as stated needs the 1994 bound or any proof that p_c^site < 3/4.
- F2: supercritical oriented percolation on a cylinder of circumference K lives e^{cK}. Standard: Durrett's block
  construction (Ann. Probab. 12 (1984) 999–1040) uses events in bounded space-time boxes, so it runs on the
  cylinder, and reduces to 1-dependent percolation of density near 1, where a contour count gives e^{cK}; the
  contact-process versions are Durrett–Liu and Durrett–Schonmann (1988). From memory.
- Odd L needs one block of three cells at the seam; not written.

**What this model is, said plainly.** At the anchor (½, 0, ½) every non-forced entry of the table is exactly ½:
S_{t+1} = (fair-coin thinning of S_t ⊕ [−2,2]) ∪ {live cells with k = 2}. The cap and the threshold each kill with
probability ½ and cancel in law. So Theorem A proves the law for a model that carries the true edge rule but in
which the cap has been made invisible by the choice of dice; it is the point from which the family E₁(π) can be
entered, not a model of the measured edge (there π₁ ≈ 0.5, here π₁ < 0.002).

## 2026-11-13, entry 4: Lemma 2 (for independent rows the one-step comparison is dead, with proof)

**Lemma 2.** (a) OP₅(p) on Z dies out from every finite set if p < 1/3. (b) For p ≤ 0.276, and for the sharp
minorant η of Lemma 1 at π = Bin(2, ρ) with ρ ≥ 0.46 (in particular ρ = 0.472), Φ(η) := |η ⊕ [−2,2]| satisfies
E[Φ(η_{t+1}) | η_t] ≤ κ Φ(η_t) with κ < 1 (κ = 0.948 at ρ = 0.472, ≤ 0.995 on [0.46, 0.5], ≤ 0.933 for ρ ≥ 0.5),
on Z and on every ring; so η is extinct after O(log L) generations.
Consequently: **for independent rows at ρ ≥ 0.46 no attractive process obtained by a one-step worst-case bound
(Lemma 1(c): none is larger than η) survives, and the route "the edge dominates a supercritical monotone process"
proves nothing there.** Combined with Theorem A: 1/3 ≤ p_c(OP₅) ≤ 1 − (1 − p_c^site)^{1/2} ≤ 0.4991.

*Proof.* (a) Let r_t = max η_t. Scanning the cells r_t + 2, r_t + 1, r_t, … at time t + 1, each is open with
probability p independently of the past, and no cell above r_t + 2 can be in η_{t+1}; so r_{t+1} ≤ r_t + 2 − X_{t+1}
with X i.i.d., P(X ≥ i) = (1−p)^i, E X = (1−p)/p > 2. The right end drifts to −∞ and the left end to +∞.
(b) N := η ⊕ [−2,2] is a union of maximal runs of ≥ 5 cells (or the whole ring). All rates are ≤ p̄ := max(s, m, π₀)
(= π₀ when π₀ ≤ ½), and the two end cells of each run have rate ≤ s (an end cell is not in η and has exactly one
η-cell within distance 2). A cell z is counted in Φ(η′) iff some y ∈ [z−2, z+2] ∩ N is in η′; by the union bound
over runs and independence, for a run of ℓ cells the expected count is at most
  2(g₁ + g₂ + g₃ + g₄) + (ℓ − 4)c₅,  g_i := 1 − (1−s)(1−p̄)^{i−1},  c₅ := 1 − (1−p̄)⁵
(the four positions z beyond or at each end see i = 1, …, 4 cells of the run, one of them an end cell). Since
2Σg_i ≥ 4c₅ in all cases below, the ratio to ℓ is largest at ℓ = 5: κ = (2Σg_i + c₅)/5. Whole ring: ratio c₅ ≤ κ.
Values: s = p̄ = p: κ < 1 iff 9 − q⁵ − 2(q + q² + q³ + q⁴) < 5, q = 1 − p, i.e. p < 0.2763. Bin(2, 0.472):
s = 0.2228, p̄ = 0.2788, κ = 0.9475. ρ ∈ [0.46, 0.5]: s ≤ 0.25, p̄ ≤ 0.2916, κ ≤ 0.9946. ρ ≥ 0.5: s = p̄ ≤ 0.25,
κ ≤ 0.9322. Then P(η_t ≠ ∅) ≤ E Φ(η_t)/5 ≤ κ^t L/5. ∎

*Smallest case.* η = {0}, ρ = 0.472: five cells at rate s = 0.2228; E Φ(η′) = 9 − q⁵ − 2(q+q²+q³+q⁴) = 4.285 < 5
(q = 0.7772).

**Why this is the real obstruction and not an accident of the bound.** The two worst cases of the table are
both realised by honest configurations: the full row (every k = 4, rate π₀) and isolated cells (rate π₂). The
adversary of a one-step bound may choose a different one at every step; the true process cannot (after a full row
comes a Bernoulli(π₀) row, where k ∈ {1, 2, 3} is typical and the rates are 0.72–1). Any proof for independent
rows must therefore use at least two generations, and then conditional independence of block events forces the
blocks to be seeded at nearly the maximal speed (two cells per generation): with n generations per block step,
disjoint noise cones require block spacing D ≥ m + 4n − 4 for blocks of m cells, a parent block (offset D/2) lies
inside the child's cone C ⊕ 2n only if D ≤ 4n, so m ≤ 4, and then the nearest cells of parent and child are
≥ 2n − 3 apart. This is graveyard item 6 made quantitative; it leaves open comparisons that give up
independence between blocks of one level (entry planned: a product bound for failures via submartingales).

## Round 1 report

**Claims.**
1. [proved] Lemma 1: E₁(π) is a PCA with conditionally independent cells; its sharp one-step attractive minorant
   is explicit; S dominates five-parent oriented site percolation of density min(π₀, π₂).
2. [proved, modulo two cited percolation facts F1, F2] Theorem A: e^{cL} ≤ τ_L ≤ 3p^{−3L} for the driven edge with
   the true rule (cap included) whenever 1 − (1 − min(π₀, π₂))² > p_c^site; rigorous region min(π₀, π₂) > 0.4991.
   τ_L is the quasi-stationary mean lifetime; no state is immortal.
3. [proved] Lemma 2: for independent rows with ρ ≥ 0.46 the sharp one-step minorant dies in O(log L); OP₅ dies for
   p < 1/3. So Theorem A cannot be pushed to Bin(2, 0.472) by any one-step comparison.
4. [proved, trivial] No one-step worst-case comparison exists for ≥ 2 deterministic rows or for a gump face (the
   all-alive state dies whatever the dice).

**What I aim to prove next (precise targets).**
- T1. A finite criterion for E₁(π) that uses several generations: "if a stated game value on a window of N cells
  exceeds a stated threshold, then τ_L ≥ e^{cL}", with the threshold and the game written out, so that the lab can
  say for which π it holds at feasible N. Tool: block events on disjoint space regions, failure indicators as
  submartingales with conditionally independent increments, hence P(all blocks of a set A fail) ≤ q^{|A|}, hence a
  contour bound without monotonicity.
- T2. For dice models (finite range, product noise): the exponent does not depend on the boundary condition
  (periodic, dead, reflecting), if it exists. A mirror-symmetric edge of L cells *is* a reflecting edge of L/2
  cells, so this would force the symmetric/asymmetric slope ratio to be exactly ½ in a dice model, and would turn
  the measured mirror slope 0.1733 into the statement "the asymmetric per-cell exponent is 0.347", against the
  0.36–0.42 on the board. I do not have the proof; I flag it now because it touches the other lines.
- T3. A dice relative of the gump face in which something can be proved (needs known-dead cells; entry 2, fact 2).

**Weakest step in my own argument.** F2 (finite-volume survival of supercritical oriented percolation on a
cylinder) is quoted from memory, and F1's number 0.7491 from a secondary source; at the anchor the margin is
0.7500 against 0.7491. And the content of Theorem A is thin: its dice make the cap cancel in law (entry 3, last
paragraph). The lemma with teeth is Lemma 2.

**Lab requests** (exact; no Monte Carlo).
- R1. Re-derive the two tables (a(x, k); minorant q for "y ∈ η / y ∉ η" × j) from the rule by enumeration over
  (x, k, b) and over completions.
- R2. Exact τ_L = 1/(1 − λ_L) for E₁(π) on the ring Z_L, L = 5, …, 18 (20 if cheap): kernel on non-empty subsets,
  cells independent given S with the probabilities a(x, k) of entry 1; λ_L its largest eigenvalue. Three laws:
  π = (½, 0, ½); π = (¼, ½, ¼); π = (0.278784, 0.498432, 0.222784). Report ln τ_L and first differences.
  No immortal states exist, so no convention is needed. (Cost note: (Qf)(S) = Σ_{S′} Π_y P(S′_y | S) f(S′) can be
  contracted one cell at a time on arrays of size 2^{L+2}.) Purpose: the constant at the anchor (my bounds only
  say c ≤ slope ≤ 3 ln 2); an exact check of the unchecked Monte-Carlo slope 0.531 of the w = 1 model.
- R3. The same on an interval of M = 5, …, 18 cells with (a) dead cells outside, (b) reflecting ends
  (x_{1−i} := x_i, x_{M+i} := x_{M+1−i}, i = 1, 2), for π = Bin(2, 0.472). Purpose: T2, is the slope in M the same
  as on the ring, or lower as in the mirror-symmetric strips of the deterministic rule?

**Next.** T1 written out as a theorem (the submartingale product bound and the contour count); then T2.

## 2026-11-13, entry 5: after the critic's reply to round 1 (decisions; what the exact tables changed)

- Names: the board calls E₁(Bin(2, ρ)) "D2(L, ρ)" and π = (½, 0, ½) "the anchor". I use both.
- F1 and F2 of Theorem A are with the librarian (critic's request). Until they are on the shelf, claim 5 is
  "proved modulo F1, F2" and its region is the sliver 0.4991 < min(π₀, π₂) ≤ ½. Entry 6 says what the proof uses.
- T2 is split, as the critic asks, by the exact tables (lab L4.2, D2(·, 0.472), 5…19 cells):
  **T2a** dead ends and reflecting ends have one exponent (data: 0.460 both, difference of ln τ constant 0.837);
  **T2b** the ring's exponent is at most the interval's (data at L ≤ 19: ring step 0.52–0.53, *above* 0.460);
  **T2c** the interval's exponent is at most the ring's (data at L ≤ 19 agree with it).
  Entry 8 gives an exact inequality and a conditional proof for T2b and for half of T2a. Nothing for T2c.
- A sign worth keeping: in any monotone model with these vessels the dead-ended interval is the ring with cells
  removed and lives at most as long (same dice, η^interval ⊆ η^ring). In D2 it lives longer than the ring of the
  same length at every L ≤ 19 (by 2.07 nats at 5 cells, 0.74 at 19). Walls help. That is the cap, seen exactly.

## 2026-11-13, entry 6: Theorem A′ (what the lower bound uses: weight at both extremes of b, nothing else)

**Theorem A′.** Let the edge row S_t ⊆ Z_L (L even) follow the 2D rule over an arbitrary field b_t(y) ∈ {0, 1, 2},
random or produced by a deterministic bulk from a random start. Let 𝒢_{t,y} be generated by S_0, all b_s(·), s < t,
and b_t(y′), y′ ≠ y. If for some p with 1 − (1−p)² > p_c^site, for all t, y,

    P(b_t(y) = 0 | 𝒢_{t,y}) ≥ p   and   P(b_t(y) = 2 | 𝒢_{t,y}) ≥ p   a.s.,

then from the full row P(T > e^{cL}) ≥ ½ for L ≥ L₀ (c = c(p) > 0; modulo F1, F2 as before).

*Proof.* For every (x, k) ≠ (dead, 0) the set of values of b that make the cell alive contains 0 or contains 2
(live: {2}, {1,2}, all, {0,1}, {0}; dead: {2}, {1,2}, {0,1}, {0} for k = 0…4 resp. 1…4). So for y within distance 2
of S_t, P(y ∈ S_{t+1} | 𝒢_{t,y}) ≥ p. Going through the cells of one generation in a fixed order, each is alive with
conditional probability ≥ p given the past and the earlier cells; hence (standard: thin each success with an
independent uniform to conditional probability exactly p) there are i.i.d. Bernoulli(p) variables W_{t+1}(y),
independent of the past, with y ∈ S_{t+1} whenever y ∈ S_t ⊕ [−2,2] and W_{t+1}(y) = 1. The process
η_{t+1} = {y ∈ η_t ⊕ [−2,2] : W_{t+1}(y) = 1} is OP₅(p) and lies in S. The rest is the proof of Theorem A. ∎

This is "a theorem for the 2D rule's edge under one hypothesis on what lies beneath". The hypothesis is false for
the rule's own bulk (there b = 1 has probability about ½). It is met with p = ½ by any source that puts the same
fair bit in both cells beneath each edge cell, independently over cells and generations; independent fair bits
give p = ¼, where Lemma 2 applies. No Markov property and no law of b = 1 is needed.
Also: Theorem A holds on the larger set min(π₀, π₂) > p_c(OP₅) if F2 is granted for OP₅ itself; by Lemma 2(a) and
Theorem A, 1/3 ≤ p_c(OP₅) ≤ 0.4991, so that set is at most {min(π₀, π₂) > 1/3} and still excludes independent rows.

## 2026-11-13, entry 7: Lemma 3 (the Lyapunov form of a lower bound) and a form it cannot take

**Lemma 3.** Finite chain, absorbing state ∅, kernel Q on the other states, d(S) = P_S(S₁ = ∅), irreducible and
aperiodic on the living states, quasi-stationary rate λ. If g : living states → [0, 1] and numbers a, ε ≥ 0 with
a + ε < 1 satisfy

    d(S) + Σ_{S′ ≠ ∅} Q(S, S′) g(S′) ≤ a·g(S) + ε   for every living S,

then 1 − λ ≤ ε, i.e. τ ≥ 1/ε.
*Proof.* Integrate against the quasi-stationary law μ (μQ = λμ, μ(d) = 1 − λ): 1 − λ + λμ(g) ≤ aμ(g) + ε. If
λ < a this gives 1 − λ ≤ ε + (a − λ)μ(g) ≤ ε + a − λ, i.e. 1 ≤ a + ε, excluded. So λ ≥ a and 1 − λ ≤ ε − (λ − a)μ(g) ≤ ε. ∎
(This is path's Theorem P for a Markov chain with the full state as the statistic; g is "danger", 1 at death.
The certificates the lab found on the lumped population table are not of this kind: the inequality has to hold
at every state, not on average over the states with a given population.)

*Smallest case.* g = 1 on a set B of "bad" states, 0 elsewhere: the condition reads P_S(dead or bad next) ≤ ε from
good states and ≤ a + ε from bad ones. For E₁ this fails for every B: a one-cell state must be bad, and from it no
state that is safe up to e^{−cL} is reached in one step with probability bounded below. g must be graded.

**A form g cannot take (dead end, with the reason).** Let Φ(S) = Σ_y φ(S near y), φ ≥ 0 a function of a fixed
window with φ(all dead) = 0, and g = r^Φ, 0 < r < 1. Then for E₁(π) with π₀, π₂ > 0 the inequality of Lemma 3
fails for all a < 1, ε = e^{−cL}, L large.
*Reason.* Put a periodic pattern P on an arc of n ≤ c′L cells, dead elsewhere. Jensen gives
E r^{Φ(S′)} ≥ r^{E Φ(S′)} = r^{nψ̄_P + O(1)}, ψ̄_P the expected health per cell one step after P; against
a·r^{nφ̄_P + O(1)} + ε this forces ψ̄_P ≥ φ̄_P − O(1/L) for every P, and the same for three steps (iterate the
inequality). Take P with φ̄_P maximal. Three steps later every arc of m cells is empty with probability
≥ p^{3(m+12)} (the three-move game played on the arc and six cells around it; the local form is asserted, not
written out), and an empty stretch longer than the window by C/φ̄_max lowers Φ strictly below φ̄_max per cell.
So ψ̄⁽³⁾_P < φ̄_P. In words: a droplet of the healthiest texture in vacuum loses health in its bulk at a rate
proportional to its size and can gain only at its two ends; an exponential of an additive health cannot absorb
that. The same computation kills g = β^{−|S ⊕ [−R,R]|} for OP₅ itself, where survival is a theorem. A
certificate has to price a hole by the hole (a sum over gaps of β^{length}) and two gaps separated by a thin live
run by their union (a product): a contour weight, or a matrix-product function of the row. Not found.

## 2026-11-13, entry 8: Proposition W (a vessel with mortal cells at its ends against the dead-ended interval)

Setting: E₁(π), π₀, π₂ > 0. Ring Z_L, G = {1, 2, 3, 4}, A = Z_L ∖ G, identified with the interval of M = L − 4 cells
with dead ends. Subscript r: ring (kernel Q_r, quasi-stationary law μ_r, hazard h_r = 1/τ_r); subscript d: that
interval (Q_d, μ_d, h_d, d_d(S) = Q_d(S, ∅)). ν := μ_r restricted to {S ⊆ A}, a measure of mass
m_G := μ_r(cells 1–4 dead).

**Proposition W.** (a) For non-empty S ⊆ A and S′ ⊆ A: Q_r(S, S′) = w(S)·Q_d(S, S′) (also for S′ = ∅), where
w(S) = u(x_L, x_{L−1})·u(x_5, x_6) is the probability of no birth in G, u(0,0) = 1, u(0,1) = 1 − π₂,
u(1,0) = (1 − π₂)², u(1,1) = π₀(1 − π₂) (first argument: the end cell of A). So w ≥ w_min := [π₀(1 − π₂)]²
(0.0469 at Bin(2, 0.472)), and w = 1 when the two outer cells of A at each end are dead.
(b) ν ≥ w_min·νQ_d entrywise, and for every n ≥ 0

    h_r ≥ w_min^{n+1} · νQ_dⁿ d_d = w_min^{n+1} · P^d_ν(T_d = n + 1).

(c) Let N_n := P^d_ν(T_d > n). If for some n ≤ τ_d and c ∈ (0, 1]

    H(n, c):   P^d_ν(T_d = n + 1) ≥ c·h_d·N_n

("the interval chain started from the ring's quasi-stationary law seen through a four-cell gap has, at step n + 1,
at least c times its own quasi-stationary death rate"), then

    τ_ring(L) ≤ 2·τ_dead(L − 4) / (c·m_G·w_min^{n+1}).

(d) The same with "ring" replaced by the reflecting interval of M + 4 cells (G = its two outer cells at each end;
there k₂ = x₃ + x₄ and k₁ = x₃ when cells 1, 2 are dead, the same u).

*Proof.* (a) With G dead, no cell of A sees a live cell outside A, and cells L and 5 are five apart, so each cell of
A has the in-row count it has in the interval; cells update independently given S; the cells of G have
k₁ = x_L + x_{L−1}, k₂ = x_L, k₃ = x_5, k₄ = x_5 + x_6 and stay dead with probability 1 − a(0, k). (b) For S′ ⊆ A,
λ_r ν(S′) = Σ_S μ_r(S)Q_r(S, S′) ≥ Σ_{S ⊆ A} ν(S)w(S)Q_d(S, S′) ≥ w_min(νQ_d)(S′); iterate (Q_d ≥ 0, λ_r ≤ 1). And
h_r = Σ_S μ_r(S)Q_r(S, ∅) ≥ Σ_{S ⊆ A} ν(S)w(S)d_d(S) ≥ w_min ν(d_d) ≥ w_min^{n+1}(νQ_dⁿ)(d_d). (c) By (b),
P^d_ν(T_d = j + 1) ≤ w_min^{−(j+1)}h_r, so N_n ≥ m_G − n·w_min^{−n}h_r; insert in h_r ≥ w_min^{n+1}c·h_d·N_n and solve:
h_r ≥ c·w_min^{n+1}m_G·h_d/(1 + n·c·w_min·h_d) ≥ ½c·w_min^{n+1}m_G·h_d. (d) Same proof. ∎

*Smallest case of (a).* S = {5} (one live cell at the end of A): cells 4 and 3 each see one live cell and stay dead
with probability 1 − π₂ each; w = u(1, 0)·u(0, 0) = (1 − π₂)².

**What it says, and what the exact tables say about it.**
- As n → ∞ the ratio P^d_ν(T_d = n+1)/(h_d N_n) → 1, so H(n, ½) holds from some n*(L) on. If n*(L) = O(log L) and
  m_G ≥ L^{−O(1)}, then (1/L) ln τ_ring ≤ (1/M) ln τ_dead + o(1): **T2b**, and by (d) "reflecting ≤ dead", half of T2a.
  n* is the number of generations for which a dying interval needs its walls. If the interval dies by a collapse
  of bounded duration from a typical state, n* is bounded and the ring is at most a constant factor
  longer-lived than the interval four cells shorter.
- Exact (L4.2): ln[h_r(L)/h_d(L − 4)] = −0.57, −0.81, −0.90, −1.03, −1.10 at L = 12, 14, 16, 18, 19. So through
  L = 19 the constant of (c) would have to keep growing by about 0.065 per cell. Either H(n, c) with n = O(log L)
  fails at larger L (then a dying interval uses its walls for a time that grows like a power of L: its death is a
  front leaving the wall, not a flash), or the ring's step 0.52–0.53 comes down to ≤ 0.460. In the first case the
  ring has the same route with a free gap in place of the wall (the end of a live stretch next to ≥ 3 dead cells
  does not know whether a wall follows), and again its exponent is at most the interval's; that half is a
  heuristic, the first is the proposition. Lab request R6 measures the ratio in H at L ≤ 18.
- Reflecting against dead: ln τ_refl(M) − ln τ_dead(M − 4) = 1.05, 1.00, 1.00, 1.00 at M = 14, 16, 18, 19: bounded,
  as (d) allows.

## 2026-11-13, entry 9: Proposition F (for the percolation minorant a front is cheaper than a flash; exact root)

**Proposition F.** OP₅(p) on Z_L, 1/3 < p < 1, q = 1 − p, β* := (p + √(p² + 4pq))/(2q), the root > 1 of
qβ² − pβ − p = 0 (β* < 1/q; β*(½) = (1 + √5)/2). Then max_S E_S T ≤ C(p)·L·β*^L, so

    limsup (1/L) ln τ_L(OP₅(p)) ≤ ln β*(p)   (0.4812 at p = ½, against ln 2 = 0.693 for killing every cell at once).

*Proof.* A maximal dead run [u, v] of ℓ ≥ 5 cells: at the next generation u+2, …, v−2 are dead surely, and every
other cell is dead with conditional probability ≥ q, independently. So the dead run containing them has length
ℓ − 4 + Y_L + Y_R, the Y's conditionally independent with P(Y ≥ j) ≥ q^j: the length dominates a random walk W with
steps ξ = Y₁ + Y₂ − 4, Y_i i.i.d. geometric (P(Y = j) = pq^j), for as long as W ≥ 5. E β^ξ = β^{−4}(p/(1 − βq))² = 1
iff p = β²(1 − βq) iff (β − 1)(qβ² − pβ − p) = 0. Under the β*-tilted law W has positive drift, so from 5 it reaches
[L, ∞) before leaving [5, ∞), within C₁L steps, with tilted probability ≥ c > 0 and bounded overshoot; untilting,
this has probability ≥ c′β*^{−L}. From the full ring, cells 1–5 are dead at time 1 with probability q⁵. So
P_full(T ≤ C₁L + 1) ≥ c′q⁵β*^{−L} =: q₀. OP₅ is attractive, so the same bound holds from every state, and restarting
every C₁L + 1 generations gives E_S T ≤ (C₁L + 1)/q₀. ∎

*Smallest case.* p = ½: E β^Y = 1/(2 − β); E β^ξ = 1 ⟺ β²(2 − β) = 1 ⟺ (β − 1)(β² − β − 1) = 0.

Use. (i) A calibration model in which the front route is a theorem: lab request R5 asks for OP₅(½) exactly on rings
and intervals to 19 cells; the proposition says its steps must end below 0.4812, and attractiveness says
τ_dead ≤ τ_ring there, the opposite order to D2. (ii) The anchor contains OP₅(½) and differs from it only in that a
live cell with k = 2 cannot die; its exact ring step is 0.67 at L = 18 (lab L4.1). So at the anchor the safe cells,
not the percolation, set the constant at these sizes. (iii) The root condition is "a single gap contracts in
the β-weighted mean"; it holds for some β > 1 iff p > 1/3, the same threshold as Lemma 2(a). It is necessary for
survival, not sufficient (gaps also merge).

## Round 2 report

**Claims (new or changed).**
1. [proved] Theorem A′: the percolation lower bound needs only conditional weight ≥ p at b = 0 and at b = 2, given
   everything else; any bulk, random or deterministic. (Still modulo F1, F2; region still 0.4991 < p ≤ ½, or
   p > p_c(OP₅) ≥ 1/3 with F2 for OP₅.)
2. [proved] Lemma 3: a one-step inequality d + Qg ≤ ag + ε at every state, 0 ≤ g ≤ 1, gives τ ≥ 1/ε.
   [proved up to the local three-move game, asserted] No such g is r^{additive local health}.
3. [proved] Proposition W (a), (b): exact inequality h_ring(L) ≥ w_min^{n+1}·P^d_ν(T_d = n+1); (c): under H(n, c),
   τ_ring(L) ≤ 2τ_dead(L − 4)/(c m_G w_min^{n+1}); (d) the same for reflecting ends.
4. [proved] Proposition F: τ_L(OP₅(p)) ≤ C L β*(p)^L, β* explicit; ln β*(½) = 0.4812 < ln 2.
5. [guessed] T2b in D2: the ring's step of ln τ must fall from 0.525 towards the interval's 0.460 beyond L = 19
   (exam entry). T2a "dead ≤ reflecting" and T2c: no argument.

**Weakest step.** Hypothesis H in Proposition W(c): I have no bound on n*(L), and the exact tables to L = 19 show
the ring falling behind the interval steadily; the proposition turns that into a dichotomy, not a proof. In
the dead end of entry 7 the local three-move game is asserted. F1, F2 are still unread.

**Lab requests** (exact).
- R5. OP₅(½): chain on subsets of the ring Z_L, and of the interval of M cells with nothing outside; given S each
  cell within distance 2 of S is alive next with probability ½ independently, every other cell dead.
  τ = 1/(1 − λ), L, M = 8…19: ln τ and steps. (Checks Proposition F's bound 0.4812 and the order τ_dead ≤ τ_ring.)
- R6. Proposition W in D2(L, 0.472), L = 12, 15, 18: m_G = μ_ring(cells 1–4 dead); with ν = μ_ring restricted to those
  states, run the dead-ended interval chain of L − 4 cells from ν and report, for n = 0…10, N_n = P_ν(T_d > n) and
  ρ_n = P_ν(T_d = n + 1)/(h_d(L − 4)·N_n). (H(n, c) is "ρ_n ≥ c". Question: does ρ_n reach ½ at an n that grows with L?)
- R7. How D2 dies, ring L = 14, 18 and dead-ended interval M = 14: for j = 1, 2, 3, 4, 6, under the law
  P(S) ∝ μ(S)·P_S(T = j) of the row j generations before death: mean population; ring: mean length of the longest
  dead arc; interval: mean number of dead cells between each wall and the nearest live cell.
- R8. D2(·, 0.472) on an interval with one dead and one reflecting end, M = 12…19: ln τ. (Exam entry: the mean
  of the dead and reflecting values.)
- R9. The anchor (½, 0, ½) on dead-ended and reflecting intervals, M = 8…19: ln τ and steps (is its interval step
  far below its ring step 0.67, as in D2?).

**Next.** With R6, R7 in hand: either bound n* (if the interval's death is short) and state T2b for D2 as a
theorem under a checked finite property, or write the front version. Then T3: the gump face. The cube lemma makes
D3 a product over triples; the first question is whether any dice law gives a percolation anchor there, given
that a cell with six live in-face neighbours dies whatever the dice.

## 2026-11-13, entry 10: errata to entries 5 and 8; exam and library

- Entry 5, last item, wording: the dead-ended interval of M cells is the ring of M cells *with its wrap-around
  neighbours removed* (equivalently the ring of M + 2 cells with two adjacent cells removed), not "with cells
  removed" at equal length. The monotone comparison meant is at equal length: fewer parents, same dice.
- Entry 8: "as n → ∞ the ratio → 1" assumes that the dead-ended interval chain has one dominant class charged by ν.
  I have not proved irreducibility on an interval (in the full interval the two end cells have k = 2 and are
  forced, so the ring's argument "from the full row every subset is a next state" does not carry over). Parts
  (a)–(d) do not use it; h_d there is 1 − (largest eigenvalue), as in the lab tables.
- Exam: P-E1 (D2 ring: slope 0.48 ± 0.03 between L = 30 and 38), P-E2 (mixed ends = mean of the two, exact),
  P-E3 (OP₅(½) exact: step 0.41 ± 0.05, ring − interval = +2.0 ± 1.0) are in `swarm/PREDICTIONS.md`.
- Library: one request appended (Liggett's theorem at equality; five-parent oriented percolation).
