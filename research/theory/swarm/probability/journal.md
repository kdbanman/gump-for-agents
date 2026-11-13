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
