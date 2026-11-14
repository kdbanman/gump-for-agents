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

## Round 2 report (interim, paused)

Paused at the lead's request, 2026-11-13. The full round 2 report is the section "Round 2 report" above; this
is the state for whoever resumes.

**Done and committed (I stand behind these as written).**
- Entries 1–4 (round 1), checked by the critic: the dice model E₁(π), its τ, Lemma 1 (sharp one-step minorant),
  Theorem A (modulo F1, F2), Lemma 2 (one-step comparison dead for independent rows).
- Entry 6, Theorem A′: the lower bound needs only conditional weight ≥ p at b = 0 and b = 2; any bulk.
- Entry 7, Lemma 3: d + Qg ≤ ag + ε at every living state, 0 ≤ g ≤ 1, a + ε < 1 ⇒ τ ≥ 1/ε.
- Entry 8, Proposition W (a), (b), (d): exact inequality between a ring (or reflecting interval) and the
  dead-ended interval four cells shorter; (c) the conditional bound under H(n, c).
- Entry 9, Proposition F: τ_L(OP₅(p)) ≤ C·L·β*(p)^L, ln β*(½) = 0.4812.
- Exam entries P-E1, P-E2, P-E3 in `swarm/PREDICTIONS.md`; one library request appended. `claims.md` is current.

**Half-done (not to be leaned on).**
- Proposition W(c) is a dichotomy, not a proof of T2b: H(n, c) with n = O(log L) is not established, and the
  exact tables to L = 19 show the ring falling behind the interval by about 0.065 per cell. The second branch
  ("a free gap serves as the wall") is a heuristic.
- The dead end of entry 7 (no certificate of the form r^{additive health}) rests on a local form of the
  three-move game that is asserted, not written out.
- Theorem A still waits for F1 (critical density of oriented site percolation below 3/4, or Liggett's theorem at
  equality) and F2 (finite-volume survival); neither is on the shelf. Odd L is not written.
- Irreducibility of the chain on a dead-ended interval is not proved (entry 10).
- Round 2 has not been read by the critic; lab requests R5–R9 (report above) are unanswered.

**Next, in order.**
1. Read the critic's reply and the answers to R6, R7 (how long a dying interval needs its walls; how D2 dies).
   If the death is short: bound n* and state T2b for D2 under a checked finite property. If it is a front:
   write the front version of Proposition W (gap ends in place of walls).
2. Score P-E2 and P-E3 against R8, R5 as soon as they are run; they test the end-factor and front pictures.
3. T3, the gump face: with the cube lemma D3 is a product over triples; find out whether any dice law gives a
   percolation anchor, given that a cell with six live in-face neighbours dies whatever the dice (entry 2,
   fact 2). Nothing has been started on this.
4. A certificate for Lemma 3 of contour or matrix-product form, first for OP₅ (where survival is known), then
   for E₁ away from the anchor. Not started.

## 2026-11-14, entry 11: the library's answer on F1 and F2; Theorem A restated on what is in print

(Successor to the paused agent, same line. Source for this entry: `library/notes/oriented-percolation.md`, written
by the librarian on 2026-11-14 in answer to the two requests on Theorem A. I opened none of the papers; the tags
are the librarian's.)

**What is in print, and how firmly.**
- (P1) [read in the paper; proof only sketched there] Hartarsky–Szabó 2022 (arXiv:2103.15621), Corollary 4.8:
  oriented site percolation with *any* finite set of parents, on the cylinder Z_n × Z started full. For every
  density above the critical one there are c, C with e^{cn} < E τ < e^{Cn} for n large, and τ/E τ tends in law to a
  standard exponential. Two parents and the five parents y − 2, …, y + 2 are both covered.
- (P2) [abstract] Liggett 1995: p_c^site ≤ 3/4 (two parents). This bounds p_c; survival *at* density 3/4 was not
  seen (second-hand: the hypothesis q ≥ 4p(1 − p) of his Proposition 2.1 allows equality).
- (P3) [second-hand, two later papers; computer-assisted] Balister–Bollobás–Stacey 1994: p_c^site ≤ 0.7491.
- (P4) [read in the paper] Hartarsky–Szabó, Remark 4.6: no percolation at the critical density.
- Not found: any value, rigorous or numerical, for the five-parent critical density; any finite-volume statement
  for an interval with dead ends other than Mountford's (density near 1, 1-dependent).

**Against what Theorem A assumed.**
1. F2 as used in entry 3 ("on a cylinder of circumference K, started full, alive at time e^{cK} with probability
   ≥ ½") is a consequence of (P1): P(τ > E τ/2) → e^{−1/2} = 0.607 and E τ > e^{cK}. The attribution in entry 3
   (Durrett 1984, Durrett–Liu, Durrett–Schonmann, "from memory") was wrong: Durrett 1984 has no finite-volume
   section, the other two are the nearest-neighbour contact process on an interval. The proof does not change.
2. (P1) holds for five parents directly. So the block step is not needed for the finite-volume part, the
   restriction to even L goes, and the threshold of the theorem is the five-parent critical density, as entry 6
   said it would be "if F2 is granted for OP₅".
3. F1 enters only through the question whether the theorem's set of π is empty; see (iii) below.

**Theorem A (form of 2026-11-14; replaces the statement of entry 3).** Let p₅ := inf{p : OP₅(p) on Z survives from
one cell with positive probability}.
(i) Let the edge row over a field b satisfy the hypothesis of Theorem A′ (entry 6) with some p > p₅; for E₁(π) this
is min(π₀, π₂) > p₅. Then there are c > 0 and L₀ with P_full(T > e^{cL}) ≥ ½ for every L ≥ L₀, even or odd, and for
E₁(π): e^{cL} ≤ τ_L ≤ 3p^{−3L}.
(ii) 1/3 ≤ p₅ ≤ 1 − (1 − p_c^site)^{1/2}.
(iii) The set of π in (i) is non-empty iff p₅ < ½ (because min(π₀, π₂) ≤ ½), and p₅ < ½ if p_c^site < 3/4.

*Proof.* (i) By Lemma 1(d), or by Theorem A′ for a general field, S_t ⊇ η_t = OP₅(p) on Z_L, both started full. That
η is the model of (P1) with n = L (parents (y + j, t), |j| ≤ 2; "started full" there means every open site of the
first row is wet, which is one step of OP₅ from the full ring). So P(η alive at time ½e^{cL}) ≥ ½ for L large, and
the bridge of entry 1 turns P_full(T > t) ≥ ½ into τ_L ≥ (t + m)/(Lm ln(1/p) + ln 2). Upper bound: entry 1.
(ii) Lower: Lemma 2(a). Upper: the block step of entry 3 on Z in place of Z_L (blocks {2i + t, 2i + t + 1}, i ∈ Z):
OP₅(p) dominates two-parent site percolation of density 1 − (1 − p)²; if that density exceeds p_c^site the latter
survives, hence so does OP₅(p), so p ≥ p₅. (iii) From (ii). ∎

**Standing of each part.** (i) rests on (P1) and nothing else. (ii) is proved in this journal. Only (iii), that the
theorem is not empty, rests on the third decimal: (P2) alone gives p₅ ≤ ½, which leaves p₅ = ½ and an empty
set possible. Strictness needs (P3), which the library has second-hand; or survival at density exactly 3/4
(Liggett's theorem at equality, unread) together with (P4). So claim 5 is now: **(i), (ii) proved modulo (P1);
non-emptiness modulo (P3).** Exact evidence that is not a proof: the lab's scan (`prob_r2.py op5scan`) reads p₅
between 0.36 and 0.44 on rings of 15–17 cells.

**Why the anchor sits exactly on Liggett's bound, and cannot be moved off it by choosing other dice.** A one-step
worst-case bound has p ≤ ½: a live cell with k = 4 needs b = 0 and one with k = 0 needs b = 2 (entry 2, fact 1). A
child block all of whose cells are within distance 2 of every cell of two adjacent parent blocks has at most two
cells (four consecutive parent cells a, …, a + 3 leave a + 1, a + 2). So the block density is at most
1 − (½)² = 3/4. The anchor is the single point where a one-step comparison with two-parent percolation reaches
the boundary of (P2); to have room one needs a bound on p_c^site below 3/4, or a comparison that is not
one-step.

**Not covered.** Intervals with dead or reflecting ends: (P1) is for cylinders. The exact tables for the anchor on
intervals (0.6236 per cell, lab R9) have no theorem behind them.

## 2026-11-14, entry 12: Lemma 5 (the local three-move game, all arc lengths); claim 13 closed; m_G bounded below

Entry 7 asserted, and the critic confirmed by exhaustion for arcs of m ≤ 7 cells only, that an arc can be emptied
in three generations by the dice near it, whatever the row beyond. Here is the proof for every m.

**Lemma 5.** E₁(π), p := min(π₀, π₂) > 0, I an arc of m cells with m + 12 ≤ L. For every state S of the ring,

    P_S(S₃ ∩ I = ∅) ≥ p^{3m+12}.

More precisely there are values of b_0 on I ⊕ [−4,4], of b_1 on I ⊕ [−2,2] and of b_2 on I, functions of S ∩ (I ⊕ [−6,6])
alone, each of conditional probability ≥ p or forced, after which S₃ ∩ I = ∅ whatever the dice do elsewhere.

*Proof.* Write D := S ⊕ [−2,2] and I_j := I ⊕ [−j, j]. A cell of I_j has its four in-row neighbours in I_{j+2}.
*Move 1 (cells of I₄).* Make S₁ ∩ I₄ = D ∩ I₄: a live cell is kept (possible for every k: its alive-set is {2}, {1,2},
all, {0,1}, {0}), a dead cell with k ≥ 1 is born (alive-sets {2}, {1,2}, {0,1}, {0}), a dead cell with k = 0 stays dead
by itself. Which case applies is read off S on I₆.
*Move 2 (cells of I₂).* A cell y ∈ D has some x ∈ S with |x − y| ≤ 2, and [x − 2, x + 2] ⊆ D contains at least two of
y's neighbours; so in S₁ (which equals D on y ± 2) it has k ≥ 2, with k = 2 exactly when y is an end of an arc of D
facing at least two cells outside D. Kill every live cell of I₂ with k ≥ 3 (b = 2 for k = 3, b ≥ 1 for k = 4) and let
no dead cell of I₂ be born (for a dead cell some value of b always does it: the alive-sets above are proper
subsets). Then S₂ ∩ I₂ = E ∩ I₂, E := the ends of arcs of D that face ≥ 2 cells outside D; these are forced
survivors (live, k = 2).
*No two cells of E are within distance 2.* Let e < e′ ≤ e + 2 be in E. If e is a right end, e + 1 and e + 2 are
outside D, so e′ ∉ D. If e is a left end, e = x − 2 for some x ∈ S, so [e, e + 4] ⊆ D, and e′ ∈ {e + 1, e + 2} has
e′ − 1, e′ + 1, e′ + 2 in D: k ≥ 3, not in E.
*Move 3 (cells of I).* In S₂ a cell of E ∩ I therefore has k = 0 and dies for b ≤ 1; a dead cell of I is kept dead.
Every prescribed value has conditional probability ≥ p given the row (the sets used are {0}, {2}, or contain
one of them), the cells are independent given the row, and 3m + 12 = (m + 8) + (m + 4) + m cells are prescribed.
Cells outside I₄, I₂, I at the three moves are never consulted. ∎

*Smallest case.* m = 1, I = {0}, S ∩ [−6, 6] = {0}: move 1 makes cells −2, …, 2 alive (five births or survivals at
b = 2) and leaves ±3, ±4 dead; move 2 kills −1, 0, 1 (k = 3, 4, 3) and keeps ±3 dead, leaving the forced ends ±2;
move 3 keeps cell 0 dead (it sees ±2: k = 2, so b = 0). Fifteen prescribed dice, as 3m + 12 says.

**Consequences.**
1. Claim 13 (no certificate of Lemma 3 of the form r^{additive local health}) no longer rests on an assertion:
   entry 7 used "three steps later every arc of m cells is empty with probability ≥ p^{3(m+12)}", which Lemma 5
   gives with the better exponent.
2. *Vacancies under the quasi-stationary law.* Let μ, λ = 1 − h be the quasi-stationary law and rate on the ring.
   From μQ³ = λ³μ and P_S(S₃ ∩ I = ∅, S₃ ≠ ∅) ≥ p^{3m+12} − P_S(T ≤ 3), averaged over μ (the last term averages to
   1 − λ³ ≤ 3h):

       μ(I empty) ≥ p^{3m+12} − 3h   for every arc of m ≤ L − 12 cells.

3. *Proposition W(c) without the proviso on m_G.* m_G = μ_ring(cells 1–4 dead) ≥ p^{24} − 3h_ring for L ≥ 16. So
   either τ_ring(L) ≤ 6p^{−24}, or m_G ≥ p^{24}/2 and, under H(n, c),

       τ_ring(L) ≤ 4·τ_dead(L − 4) / (c·p^{24}·w_min^{n+1}).

   T2b for E₁(π) is therefore implied by H(n, c) for one fixed pair (n, c) and all large L, with nothing else.
   (At Bin(2, 0.472): p^{24} = e^{−36.0}; the exact m_G is 0.043. The constant is useless numerically; the point is
   that it does not depend on L.)

**What Proposition W cannot do (recorded so that nobody tries again).** The lab's answer to R6 shows ρ_n ≥ 1 at
L = 12, 15, 18 for every n ≤ 10, and the critic's caution is right: at n = 0, H is the conclusion in other words.
A proof of H(n, c) at fixed n for all L needs the dead-ended interval chain, started from the ring's law on rows
with a four-cell gap, to be within a factor of its own quasi-stationary death rate after n steps, uniformly in
L: a statement about relaxation to a quasi-stationary law, which for a non-monotone chain I cannot get from
anything in this journal. And the wall form of the comparison is the wrong tool for the way these chains die
(lab R7: a gap that grows for a number of generations increasing with the size): holding four fixed cells dead
costs a factor u ≈ π₀(1 − π₂) per generation at the side where the row is still alive, for as long as the
collapse lasts. If that duration grows in proportion to L the loss is itself exponential in L.

## 2026-11-14, entry 13: Lemma 4 (the gump face over dice: every cell can be killed from beneath, hence a monotone comparison over two generations)

Entry 2, fact (2), and graveyard 14 say: no one-step monotone process lies below a gump face over dice, because
the all-alive face dies whatever the dice show. This entry shows that the obstruction is to *one* step only.

**The model F.** Γ: the cells of a face (a periodic patch of a {111} layer, or a hull face), N(y) ⊆ Γ the in-layer
neighbours of y (six in the interior, fewer on a rim), N̄(y) := N(y) ∪ {y}. State S_t ⊆ Γ; for a cell, x = its state,
k = |S_t ∩ N(y)|; b_t(y) ∈ {0, 1, 2, 3} stands for the live cells among the three beneath it. Gump's rule with
n = k + b: y ∈ S_{t+1} iff n ∈ {4, 5} (x = 0) or n ∈ {3, 4, 5} (x = 1). **F(π)**: the b_t(y) i.i.d. with law π.
Alive-sets B(x, k) := {b : alive next}:

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| dead | ∅ | {3} | {2,3} | {1,2} | {0,1} | {0} | ∅ |
| live | {3} | {2,3} | {1,2,3} | {0,1,2} | {0,1} | {0} | ∅ |

(O1) The complement of every B(x, k) contains 0 or contains 3. (This is "gump has no safe face cell",
`exponent/theorems.md` Lemma A(c). It fails for the 2D rule's edge: a live cell with k = 2 survives every b. The
reason is arithmetic: both rules have a survival window of three consecutive values of n, and b takes four
values in gump, three in the 2D rule.)
(O2) For x + k ≥ 1 and k ≤ 5, B(x, k) contains {0}, or contains {3}, or equals {1,2} (the last only for a dead cell
with k = 3; source's remark C18).

**Lemma 4.** Let b be any field with, for all t, y (𝒢_{t,y} as in Theorem A′: everything except b_t(y)),

    P(b_t(y) = 0 | 𝒢_{t,y}) ≥ s,   P(b_t(y) = 3 | 𝒢_{t,y}) ≥ s,   P(b_t(y) ∈ {1,2} | 𝒢_{t,y}) ≥ s″,     σ := min(s, s″).

Then, on a larger probability space, there are marks M_t(y) ∈ {K, G, N}, t ≥ 1, y ∈ Γ, i.i.d. with P(K) = s, P(G) = σ,
those of generation t + 1 independent of everything up to time t, such that
(a) M_{t+1}(y) = K ⇒ y ∉ S_{t+1}, whatever S_t is;
(b) M_{t+1}(y) = G, x + k ≥ 1 and k ≤ 5 at time t ⇒ y ∈ S_{t+1};
(c) with Z_t := {M_t = K} for t ≥ 1, Z_0 any set disjoint from S_0, and

    η_0 := S_0,   η_{t+1} := {y : M_{t+1}(y) = G,  N̄(y) ∩ η_t ≠ ∅,  and  N(y) ∩ Z_t ≠ ∅ or |N(y)| ≤ 5},

one has η_t ⊆ S_t and Z_t ∩ S_t = ∅ for all t; for fixed marks η_{t+1} is non-decreasing in η_t;
(d) P(S_{t+1} = ∅ | past) ≥ s^{|Γ|}, so E_S T ≤ s^{−A} from every state (A = |Γ|).

*Proof.* For the step t → t + 1 the pair (x, k) of a cell is known at time t. Choose κ(x, k) ∈ {0, 3} outside B(x, k)
(O1) and a class γ(x, k) ∈ {{0}, {3}, {1,2}} inside B(x, k) when x + k ≥ 1 and k ≤ 5 (O2), γ := {1,2} otherwise;
κ ∉ γ. Let q_K := P(b_t(y) = κ | 𝒢_{t,y}) ≥ s and q_G := P(b_t(y) ∈ γ | 𝒢_{t,y}) ≥ σ, and with V_t(y) uniform,
independent of everything, set M_{t+1}(y) := K if b_t(y) = κ and V ≤ s/q_K; := G if b_t(y) ∈ γ and V ≤ σ/q_G; := N
otherwise. Given 𝒢_{t,y} and the V of the other cells, M_{t+1}(y) has the law (s, σ, 1 − s − σ) exactly; the other
marks of generation t + 1 and the whole past are measurable with respect to that conditioning. Hence the marks
are i.i.d. and those of generation t + 1 are independent of the past. (a): b = κ ∉ B. (b): b ∈ γ ⊆ B.
(c) by induction: y ∈ η_{t+1} has a cell of η_t ⊆ S_t in N̄(y), so x + k ≥ 1, and a cell of Z_t (dead in S_t) in
N(y), or at most five neighbours, so k ≤ 5; then (b). Z_{t+1} ∩ S_{t+1} = ∅ is (a). (d): all marks K. ∎

*Smallest case.* S_0 = {y₀}, an interior cell, Z_0 = Γ ∖ {y₀}. y₀ is (live, 0) and its six neighbours are (dead, 1):
all seven have B = {3}, κ = 0. So S_1 = η_1 = the cells of N̄(y₀) with b = 3: a lone cell is one step of seven-parent
percolation of density π₃, the exact analogue of entry 2's smallest case.

**What it says.**
- η is oriented site percolation on Γ × N with the seven parents N̄(y), in which the site (y, t + 1) is open iff it
  carries G and one of its neighbours carried K one generation earlier. The cap is paid for by the second
  condition, and it is always met somewhere, because (a) makes every cell dead with probability ≥ s whatever
  the face does. A gump face over such dice therefore does dominate a monotone process; it takes two
  generations to see it. Graveyard 14 should read "no *one-step* comparison".
- (d) is the one-generation upper bound τ ≤ s^{−A} that the 2D rule does not have (there three moves are needed,
  entry 1). It needs the conditional hypothesis: with the cells beneath *shared* inside a cube (the true
  geometry, cube lemma: b_a = u_b + u_c + v_a) two cells of one cube can demand b = 0 and b = 3 of dice that
  share a cell, which is the board's E10. For shared cells the hypothesis holds given the other *cubes*, not
  given the other cells of the same cube, and the marks would have to be built cube by cube; not written.
- F(π) with π₀π₃ > 0 and i.i.d. b is not "random cells beneath": by the cube lemma (3, 0, ·) never occurs
  among the three counts of one cube. F(π) draws the numbers, not the cells. That is the exact relation of this
  dice model to gump.

## 2026-11-14, entry 14: what a percolation anchor for the gump face would need (three proved limits, two gaps)

Lemma 4 gives a monotone process below F. Whether it can carry a theorem like Theorem A:

**1. Its density is at most 0.304.** Three disjoint classes of b are needed, {0}, {3}, {1,2}, so σ ≤ 1/3, with
equality at π₀ = π₃ = π₁ + π₂ = 1/3; then a site is open with probability σ(1 − (1 − s)⁶) = 665/2187 = 0.3041 and a
live cell has at most 7 × 0.3041 = 2.13 open children in the mean. (In the 2D rule two classes suffice, {0}
and {2}, and σ = ½.)

**2. For independent cells beneath it dies at once (the analogue of Lemma 2).** If b is a sum of three
independent Bernoulli(ρ) cells, s = min(ρ³, (1 − ρ)³) ≤ 1/8, and E|η_{t+1}| ≤ 7σ|η_t| ≤ (7/8)|η_t| (at most seven
candidates per live cell, each open with probability ≤ σ): η is extinct after O(log A) generations at every ρ.
As in the 2D rule, a percolation anchor needs coherent dice (weight 1/3 on "all three dead" and on "all three
alive"), and independent layers give nothing.

**3. The method of Theorem A cannot certify it (dead end, with the reason).** Take any comparison of the kind
used in entry 3: disjoint blocks, a block is on when it contains a cell of η, each block has two disjoint child
blocks, and a child's probability is the one guaranteed when the parent holds a single live cell y. Only the
seven cells of N̄(y) can be alive next, so one of the two children contains at most three of them and is on with
probability at most 1 − (1 − σ)³ ≤ 19/27 = 0.7037. That is below every rigorous upper bound on p_c^site (0.7491,
3/4) and below its numerical value 0.7055. With σ = ½ the same count would give 7/8: the geometry of the layer
is not the obstacle, the third class of dice is (a dead cell with exactly three live neighbours is born only
for b ∈ {1, 2}).

**4. Gap: is η supercritical at all?** This is a question about a seven-parent oriented percolation in 2 + 1
dimensions with a one-generation dependence. A rough estimate (critical density of seven-parent site
percolation in 2 + 1 dimensions about 0.20–0.24, by the product z·p_c ≈ 1.4–1.6 seen in the tabulated lattices;
effective density s(1 − (1 − s)^{5…6})) puts the critical value of s = σ near 0.27, below 1/3 but not far. I cannot
prove it and the exact lab cannot decide it. Exam entry P-E4 asks for it by sampling.

**5. Gap: the finite-volume step.** For monotone percolation with i.i.d. sites on Z² × N, "exponential in the
area" at every supercritical density is in print: (P1) with d = 3 gives e^{c n²} on the n × n torus. η does
not fit as printed, for two reasons: the layer is a kagome lattice (three cells per period, no single
neighbourhood on Z²), and the site variables are built from marks K and G that exclude each other at a cell, so
the events "open" are not increasing functions of independent variables in one common order (Harris's
inequality, which the renormalisation uses, is not available as it stands).

So: **T3 is not a theorem.** What stands is Lemma 4 and the three limits; what a theorem "the gump face over
dice (1/3, ·, ·, 1/3) lives e^{cA}" still needs is (4) by a finite, checkable criterion and (5) by an adaptation
of the Bezuidenhout–Grimmett construction. Both are outside what this line can do by hand.

Remark (why area, in dice models). For a monotone relative the area law is no mystery and no new theorem:
it is (P1) in one more dimension. The one-dimensional law of Theorem A and the area law of a face are the same
statement about supercritical oriented percolation on a torus; what is special to gump is only whether a
supercritical monotone process fits beneath the capped rule, and with what dice.

## 2026-11-14, entry 15: Lemma 6 (the chain on an interval is irreducible); errata to entries 11 and 12

Entry 10 left open whether E₁(π) on an interval with dead ends has one class of living states (the ring's
argument fails: in the full interval the two end cells have k = 2 and are forced). It has.

**Lemma 6.** E₁(π) with π₀, π₂ > 0 on the interval J = [1, M], M ≥ 5, cells outside dead. The chain on the non-empty
subsets of J is irreducible and aperiodic. The same holds with reflecting ends.

*Proof.* With π₀, π₂ > 0 the one-step transitions of positive probability are exactly S → S′ with
F(S) ⊆ S′ ⊆ S ∪ N(S), F(S) the live cells with k = 2 and N(S) the dead cells with k ≥ 1 (for every other pair (x, k) the
value b = 0 gives one outcome and b = 2 the other; table of entry 1). Call S *loose* if F(S) = ∅; from a loose S
every subset of D(S) := (S ⊕ [−2,2]) ∩ J is a next state.
(1) S → D(S) is always allowed, so every S ≠ ∅ reaches J.
(2) F(J) = {1, M} (cell 1 sees 2, 3; cell 2 sees 1, 3, 4; cells 3, …, M − 2 see four), so J → {1, M}.
(3) {1, M} is loose (M ≥ 4), so {1, M} → {1}. Then {1} → {3} → {1, 4} (each state loose, each target inside D).
(4) R_i := {1, 4, …, 1 + 3i}, r := 1 + 3i. R_i and R_i ∪ {r + 2} are loose (in the second, r and r + 2 have k = 1, all
other cells k = 0), r + 2 ∈ D(R_i) and r + 3 ∈ D(R_i ∪ {r + 2}). So R_i → R_i ∪ {r + 2} → R_{i+1} as long as r + 3 ≤ M.
(5) The last R = {1, 4, …, r*}, r* ≤ M ≤ r* + 2, is loose and D(R) = J (cells 2 + 3i and 3 + 3i are within distance 2
of 1 + 3i). So R → T for *every* T ⊆ J, in particular R → R.
Chaining (1)–(5), every non-empty S reaches every T. Reflecting ends: cell 1 sees itself, cell 2 twice and cell 3
(k = x₁ + 2x₂ + x₃), so in the full interval every cell has k = 4, J is loose, D(J) = J, and (1) with J → T suffices. ∎

*Smallest case.* M = 5: {1,2,3,4,5} → {1,5} → {1} → {3} → {1,4} = R, and D({1,4}) = [1,5].

Use. On a dead-ended or reflecting interval the quasi-stationary law is unique and charges every living state,
so the lab's τ_dead, τ_refl are what entry 1 defines, and in entry 8 "ρ_n → 1 as n → ∞" holds as stated (entry 10
had withdrawn it). Not done: the three-move bound E_S T ≤ 3p^{−3M} on an interval (near a wall the forced cells
of move 2 are different; I did not redo the game there).

**Errata.**
- Entry 12, "Smallest case": move 2 prescribes cells of I₂ = [−2, 2] only; it kills −1, 0, 1 and does *not* keep ±3
  dead (they are outside I₂ and are not needed: move 3 looks at [−2, 2] only). Of the 3m + 12 = 15 cells counted,
  nine carry a prescribed die (five at move 1, three at move 2, one at move 3) and six are forced.
- Entry 11, "Why the anchor sits exactly on Liggett's bound": the count is for blocks of m cells whose children
  are blocks of m cells. Two adjacent parents cover 2m consecutive cells, and the cells within distance 2 of
  all of them number 6 − 2m; a child needs m of them, so m ≤ 2, and m = 2 gives density 1 − (1 − p)² ≤ 3/4.
