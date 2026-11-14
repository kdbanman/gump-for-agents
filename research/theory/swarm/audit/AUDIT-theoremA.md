# Audit: "a deterministic relative with a theorem"

_Auditor: an agent that is neither the critic nor a solver. 2026-11-14._
_Read: `swarm/PROBLEM.md`, `docs/AUTOMATON.md`, `swarm/source/` and `swarm/probability/` (claims and journals),
`swarm/library/notes/oriented-percolation.md`, `research/theory/exponent/theorems.md` §A–B (cited by the
probability line), and three arXiv papers (§3). `swarm/critic/` was not opened until parts A and B were committed
(part C). Every number below comes from a script in this directory, written for this audit; none of the critic's
lab code or tables was used. Commands run from `research/theory/swarm/audit/`; their outputs are in `out/`._

Tags used for verdicts: **correct** (I checked the proof line by line and, where a check by enumeration exists,
ran it); **gap** (what is missing is said; "filled" if the missing argument is given here); **wrong**;
**cited** (rests on a statement from the literature that nobody in this repository has read in the primary source).

## 0. Summary

| part of the chain | where | verdict |
|---|---|---|
| Row 0 of 𝒜(L) is the dice chain E₁(½, 0, ½), exactly | source S14 | correct; exhaustive check (A2) |
| The chain: irreducible, aperiodic, one quasi-stationary law; exactly geometric wait from it | prob. entry 1; source S8 | correct (A3) |
| Upper bound τ_L ≤ 3·8^L | prob. entry 1; `exponent/theorems.md` B(a) | correct (A3) |
| The row dominates five-parent oriented site percolation of density ½ | prob. Lemma 1(d), Theorem A′; source Theorem L | correct (A4) |
| Blocks of two cells in a drifting frame: two-parent oriented site percolation of density ¾ on a cylinder of circumference L/2 | prob. entry 3 | correct, for even L (A4) |
| From "the percolation lives e^{cK}" to "the row is alive at e^{cK}/2 with probability ≥ ½" | prob. entry 3; library note | small gap, filled (§2.6) |
| From one start to τ_L | prob. entry 1 | correct (A3) |
| F1: critical density of two-parent oriented site percolation < ¾ | Balister–Bollobás–Stacey 1994 | cited (three secondary sources); a second, independent route exists (§3.2) |
| F2: finite-volume survival on a cylinder for p > p_c | Hartarsky–Szabó 2022, Cor. 4.8 | cited (statement read in the paper; its proof there is a sketch) |
| Odd L | not claimed | gap, not filled (§2.9) |

**The theorem is correct as a conditional statement**: for even L it holds if F1 and F2 hold. The part that does not
depend on the literature is stated as Theorem U below. What the theorem says and does not say about gump: §4.
Recommended wording for the notebook: §6. Other claims tagged "proved": part B.

---

# Part A. The chain

## 1. Self-contained statement

### 1.1 The automaton 𝒜(L)

Fix an integer L ≥ 5.

- **Cells.** (x, j) with x ∈ Z_L (a ring of L columns) and j ∈ {0, 1, 2, …} (rows; row 0 is "the edge").
  Each cell is 0 (dead) or 1 (alive). The state space is {0,1}^{Z_L × N}.
- **Update** (synchronous, deterministic). Write y for the present configuration, y′ for the next.
  - Row 0 follows the 2D rule B34/S234 on the cross, with nothing above it: let
    n = y(x−2, 0) + y(x−1, 0) + y(x+1, 0) + y(x+2, 0) + y(x, 1) + y(x, 2). Then y′(x, 0) = 1 iff
    (y(x, 0) = 0 and n ∈ {3, 4}) or (y(x, 0) = 1 and n ∈ {2, 3, 4}).
  - Every other row copies the row two below: y′(x, j) = y(x, j + 2) for j ≥ 1.
- **Initial condition** (the only randomness). Row 0 is a random subset S₀ of Z_L with a law ν₀ to be chosen.
  Independently of S₀, let ξ_{x,i} (x ∈ Z_L, i ≥ 1) be independent fair bits; put
  y₀(x, 2i − 1) = y₀(x, 2i) = ξ_{x,i}.
- **Death.** T = the first generation at which row 0 is empty. Once empty, row 0 stays empty (a dead cell of an
  empty row has n ≤ 2).

A cell of row 0 never influences any other row. The map is a cellular automaton in the sense that each cell is
updated by a fixed local rule; the rule of row 0 differs from the rule of the other rows.

### 1.2 The dice chain

For S ⊆ Z_L and y ∈ Z_L let k = |S ∩ {y−2, y−1, y+1, y+2}|. The chain **E** on subsets of Z_L: given S, the cells of
the next set S′ are independent, and

- a cell of S with k = 2 is in S′ (a *safe* cell);
- a cell not in S with k = 0 is not in S′;
- every other cell is in S′ with probability ½.

Equivalently S′ = F(S) ∪ (a fair-coin thinning of E(S) ∖ F(S)), with E(S) = {y : some cell of S within distance 2}
and F(S) = the safe cells. ∅ is absorbing. (E is the probability line's E₁(π) at π = (½, 0, ½): each edge cell
reads b ∈ {0, 2} live cells beneath it, a fair coin, independent over cells and generations.)

Let Q be the transition matrix of E restricted to the 2^L − 1 non-empty sets. It is irreducible and aperiodic
(§2.2). λ_L := its largest eigenvalue, μ_L := the normalised positive left eigenvector (the quasi-stationary law),
and

  **τ_L := 1/(1 − λ_L)** = the mean of T for the chain started from μ_L.

### 1.3 The theorem

**Theorem (unconditional part, "U").**
1. In 𝒜(L) the edge row (S_t)_{t ≥ 0} is the Markov chain E started from ν₀, exactly, and the rows beneath at
   time t are independent of S₀, …, S_t and have the law they had at time 0.
2. If ν₀ = μ_L then P(T > t) = λ_L^t for every t, and conditionally on {T > t} the whole configuration at time t
   has the initial law. For any ν₀ with ν₀(∅) < 1, P(T > t) = c·λ_L^t·(1 + o(1)) with c > 0.
3. τ_L ≤ 3·8^L (L ≥ 5).
4. Let L ≥ 6 be even, K = L/2, and let ζ be two-parent oriented site percolation of density ¾ on the cylinder
   Z_K × N started full: ζ₀ = Z_K, ζ_{t+1}(i) = V_{t+1}(i)·max(ζ_t(i), ζ_t(i+1)) with V i.i.d. Bernoulli(¾).
   Then, with row 0 started full, P(T > t) ≥ P(ζ_t ≠ ∅) for all t; and τ_L ≥ τ^ζ_K, where τ^ζ_K = 1/(1 − λ^ζ_K) is
   the same quantity for ζ.

**Theorem (conditional part, "C").** If F1 and F2 below hold, there are c > 0 and L₀ such that for all even L ≥ L₀

  **e^{cL} ≤ τ_L ≤ 3·8^L.**

There is no other hypothesis. The constants c and L₀ are not explicit (they come from F2).

Not covered: odd L (§2.9); any vessel other than the ring Z_L; any τ other than the one defined in §1.2.

### 1.4 The two statements from the literature, as the library's note gives them

Model (library note, top): "*Two-parent oriented site percolation* (2dOP below): sites of Z × Z₊ open
independently with probability p; (y, n+1) is reached iff it is open and one of its two parents (y, n), (y+1, n)
is reached". p_c is its critical density.

**F1** (library note §1; not read in the primary source by anyone here):
> [secondary: Hartarsky–Szabó, arXiv:2103.15621v1, §5.7.2, pp. 28–29] "In [1993] and the later refinement,
> [1994], a two-dimensional renormalisation argument was used together with extensive computer calculations to
> conclude that p_c^OP ⩽ 0.7491 (there is a misprint in [1993] as explained in [1994]). Subsequently Liggett
> [1995] proved p_c^OP ⩽ 3/4 without resorting to a computer."

The theorem uses only: **p_c < ¾**.

**F2** (library note §3; statement read in the paper, proof there a sketch):
> Corollary 4.8 [paper, v3 p. 14; Theorem 17 in v1, §5.5]. GOSP on the quotient graph with vertex set
> T_n^{d−1} × Z (torus of side n in the space directions; for d = 2, a cylinder of circumference n). Extinction
> time τ^T = sup{t ⩾ 0 : T_n^{d−1} × {0, −1, −2, …} → T_n^{d−1} × {t}} (i.e. started full). […] For all p > p_c
> there exist c, C ∈ (0, ∞) such that τ^T / E_p[τ^T] → E (standard exponential) in law, and
> e^{c n^{d−1}} < E_p[τ^T] < e^{C n^{d−1}} for n large enough.

The theorem uses only: for d = 2, parents {(0,1), (1,1)}, p = ¾: **E[τ^T] > e^{cn} for n large**. (I re-read the
corollary in arXiv:2103.15621v3, p. 14; the library's transcription is accurate. See §3.3.)

## 2. The proof, step by step

Notation: for a row S and a cell y, x = 1[y ∈ S], k as in §1.2, b = number of live cells beneath y (rows 1, 2).
By the rule, y is alive next iff k + b ≤ 4 and k + b + x ≥ 3 (equivalent to the birth/survival lists: A1). The set
A(x, k) of values of b ∈ {0, 1, 2} for which the cell is alive next is

| k | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| live | {2} | {1,2} | {0,1,2} | {0,1} | {0} |
| dead | ∅ | {2} | {1,2} | {0,1} | {0} |

(`python3 a1_rule_and_table.py`). For b uniform on {0, 2} this gives the probabilities of §1.2.

### 2.1 Row 0 is the chain E. **Correct.**

*Claim (source S14).* y_t(x, 1) = y_t(x, 2) = ξ_{x,t+1} for all t ≥ 0.
*Proof.* Rows j ≥ 1 are shifted two rows up per generation: y_t(x, j) = y₀(x, j + 2t). So
y_t(x, 1) = y₀(x, 2(t+1) − 1) = ξ_{x,t+1} and y_t(x, 2) = y₀(x, 2(t+1)) = ξ_{x,t+1}. ∎
Hence b_t(x) = 2ξ_{x,t+1}, and S_{t+1} is a function of S_t and (ξ_{x,t+1})_x. The bits with index t + 1 are
independent of S₀ and of the bits with index ≤ t, hence of S₀, …, S_t: (S_t) is a Markov chain with the kernel of
§1.2. The rows beneath at time t are the bits with index > t, in the same paired arrangement: independent of
(S₀, …, S_t), with the initial law. This is U.1.

*Check* (`python3 a2_automaton.py`, part (a)): the map of §1.1 was run on the full array for every S₀ and every
table of bits ξ ∈ {0,1}^{L·t}, (L, t) = (5, 3), (6, 2), (6, 3), (8, 2). Rows 1 and 2 equal ξ_{·,s+1} at every time
s < t, and the number of bit tables producing each trajectory (S₁, …, S_t) equals 2^{Lt}·∏ Q(S_{i−1}, S_i) with
zero error (all numbers are dyadic).

*The variant from the uniform product measure* (source S14, second paragraph; S2 Lemma 1, S8 Lemma 1′): rows 1
and 2 both copy row 3 (y′(x,1) = y′(x,2) = y(x,3)); rows j ≥ 3 follow "alive next iff an odd number of the eight
cross neighbours is alive" and read rows 1, 2; start: rows ≥ 3 i.i.d. fair bits, rows 0–2 arbitrary. Claim: row 0
is the chain E from generation 1. **Correct.** The proof of Lemma 1 (S2) is right: (i) by induction on t,
y_t(p) = Π(y₀(D^t p); y₀ on rows < j + 2t) with Π(·; c) a bijection, for a source cell p in row j, D the shift two
rows down; (ii) therefore, given the rows < w + 2t at time 0, the map from rows w + 2t, …, w + 2t + K at time 0 to
rows w, …, w + K at time t is triangular with bijective diagonal, hence a bijection; (iii) the top rows up to
time t and the drive up to time t − 1 are functions of rows < w + 2t at time 0. I checked each of the three
inclusions of row indices. *Check* (`a2_automaton.py`, parts (b), (c)): with rows 3..H enumerated exhaustively
(L = 5; 2 and 3 generations; several fixed top rows) the sequence (row 3 at times 0..t−1) takes each of its
2^{Lt} values equally often; and for R₁(parity) of S2 (row 0 by the rule, all rows beneath by parity, two-way
coupling) the map (rows 1..2t at time 0) → ((rows 1, 2) at times 0..t−1) is a bijection for every S₀
((L, t) = (5, 2), (3, 4), (4, 3)).

### 2.2 The chain is irreducible and aperiodic on non-empty sets; exactly geometric wait. **Correct.**

(Prob. entry 1; `exponent/theorems.md` D′; source S8 Prop. 1″.)
- From the full ring every cell has k = 4, so each is alive next with probability ½ independently: every subset,
  the full ring included, is reached in one step with probability 2^{−L}.
- From any S ≠ ∅ the move S ↦ E(S) has probability ≥ 2^{−L} (each non-safe cell of E(S) is alive with
  probability ½; safe cells are in E(S)). E^m(S) is the full ring for m = ⌈L/4⌉ (an arc grows by two cells at each
  end), and E(full) = full. So P_S(S_m = full) ≥ 2^{−Lm}.
So Q is irreducible and aperiodic, λ_L is simple with positive left and right eigenvectors, and
P_S(T > t) = c(S)·λ_L^t·(1 + o(1)), c(S) > 0. From μ_L: P_{μ}(T > t) = μ_L Q^t 1 = λ_L^t, and the law of S_t given
T > t is μ_L. With §2.1 (the rows beneath at time t are independent of S₀..S_t and of the event {T > t}, which is
an event of S_t) this is U.2.
*Check* (`python3 a3_chain.py 18`, items (2), (3), (5)): the kernel is uniform on [F(S), E(S)] for every S
(L ≤ 10); both bullet points hold for L = 5..10; from μ₈, |P(T > t) − λ^t| < 10^{−14}.

### 2.3 Upper bound: P_S(T ≤ 3) ≥ 8^{−L} for every S, hence τ_L ≤ 3·8^L. **Correct.**

(`exponent/theorems.md` Theorem B(a), used in prob. entry 1.) The allowed next sets from S are exactly the S′
with F(S) ⊆ S′ ⊆ E(S), each with probability 2^{−|E(S)∖F(S)|} ≥ 2^{−L}. Strategy: S₁ = E(S₀); S₂ = F(S₁);
S₃ = F(S₂). Claim: S₃ = ∅.
*Proof.* S₁ is the ring or a union of arcs of ≥ 5 cells. In an arc, a cell at distance ≥ 2 from both ends has
k = 4; the cell next to an end has k = 3 (the end cell and two cells inward; the first gap cell is dead); an end
cell has k = 2 if the gap it faces has ≥ 2 cells and k = 3 if it has one. So S₂ = the arc ends facing gaps of
length ≥ 2. Two such cells are ≥ 4 apart along an arc or ≥ 3 apart across a gap: every cell of S₂ has k = 0, so
F(S₂) = ∅. ∎ Then P(T > 3j) ≤ (1 − 8^{−L})^j and E_S T ≤ 3·8^L for every S; τ_L = E_{μ} T. This is U.3.
*Check* (`a3_chain.py`, item (4)): the strategy empties every non-empty row, with every move allowed, for
L = 5..16 (exhaustive); exactly, min_S P_S(T ≤ 3) = 3.8×10^{−4} at L = 9 against 8^{−9} = 7.5×10^{−9}.
The bound is far from sharp: ln(3·8^L) = 38.5 at L = 18, where ln τ_L = 13.59.

### 2.4 The row dominates five-parent oriented site percolation of density ½. **Correct.**

(Prob. Lemma 1(d) and Theorem A′; source Theorem L.) *Statement.* There are random variables W_t(y) ∈ {0, 1}
(t ≥ 1, y ∈ Z_L), functions of S₀ and the bits ξ, that are i.i.d. fair bits, such that
η_{t+1} := {y ∈ E(η_t) : W_{t+1}(y) = 1}, η₀ ⊆ S₀, satisfies η_t ⊆ S_t for all t.
*Proof.* For y ∈ E(S_t) not safe, A(x, k) contains exactly one of 0, 2 (table); put W_{t+1}(y) = 1[2ξ_{y,t+1} ∈ A]. For every
other y put W_{t+1}(y) = ξ_{y,t+1}. Given S₀ and the bits of index ≤ t (which determine S_t), W_{t+1}(·) is the
image of the fresh bits ξ_{·,t+1} under a coordinatewise bijection, so it is uniform on {0,1}^L and independent of
the past; hence all W are i.i.d. fair. If η_t ⊆ S_t then E(η_t) ⊆ E(S_t), and a cell y ∈ E(S_t) with
W_{t+1}(y) = 1 is alive at t + 1 (by the definition of W if it is not safe, surely if it is). ∎
In 𝒜(L) the comparison is pathwise and uses no auxiliary randomness.

*The general forms.* Theorem A′ (prob. entry 6: any field b with conditional weight ≥ p at b = 0 and at b = 2
given the past and the other cells of the same generation) and Theorem L (source S15: the same from the
equal-time kernel only, giving domination of the one-time marginal laws) are both **correct**. In A′ the
sequential thinning is the standard one; the auxiliary uniforms must be added to the filtration, which changes
nothing. In L the induction is on marginal laws through the Markovian projection (S4 Lemma 3), and the
conclusion P(T > t) ≥ P(W_{t−t₀} ≠ ∅) needs only marginals because an empty edge is absorbing. A′'s hypothesis
implies L's (average the conditional probability), so L is the stronger theorem.

*Check* (`python3 a4_domination.py`, items (1), (3), (4)): for every S and every bit vector, c ↦ W is a bijection
and E(S) ∩ W ⊆ S′ (L = 5..9; all η ⊆ S for L ≤ 7); exact survival curves from the full ring satisfy
P(row alive at t) ≥ P(OP₅(½) alive at t) for t ≤ 400, L = 6..14; and for a drive that is correlated across cells
and depends on the row (a Gibbs law with INS(0.4047), L = 6) the law of the edge dominates OP₅(0.4047) on every
event {meets C}, t ≤ 6.

### 2.5 Blocks: two-parent oriented site percolation of density ¾ on a cylinder. **Correct for even L.**

(Prob. entry 3.) L = 2K. Blocks X_i^t = {2i + t, 2i + t + 1} (mod L), i ∈ Z_K; for each t they partition the ring.
ξ_t(i) := 1[η_t ∩ X_i^t ≠ ∅], V_{t+1}(i) := 1[W_{t+1} = 1 somewhere in X_i^{t+1}].
*Claim.* ξ_{t+1}(i) ≥ V_{t+1}(i)·max(ξ_t(i), ξ_t(i+1)), and the V are i.i.d. Bernoulli(¾).
*Proof.* X_i^t ∪ X_{i+1}^t = {2i+t, …, 2i+t+3} and X_i^{t+1} = {2i+t+1, 2i+t+2}: each of the two child cells is within
distance 2 of each of the four parent cells. So if a parent block meets η_t, both child cells lie in E(η_t), and
the child block meets η_{t+1} iff V_{t+1}(i) = 1. The blocks X_i^{t+1}, i ∈ Z_K, are disjoint, so the V_{t+1}(i) are
independent, each 1 with probability 1 − (½)² = ¾, independent of the past. ∎
By induction ζ_t ≤ ξ_t for ζ of U.4 driven by the same V. So with S₀ = η₀ = full:
{ζ_t ≠ ∅} ⊆ {η_t ≠ ∅} ⊆ {S_t ≠ ∅} = {T > t}. This is the first half of U.4.

Two cells is the largest block for which this works: a cell within distance 2 of every cell of two adjacent
blocks of m cells exists only if 2m − 1 ≤ 4. And ½ is the largest density any law of b can give (a cell with
k = 4 needs b = 0, a cell with k ≤ 1 needs b = 2). So **¾ is the largest block density this argument can reach
for the 2D rule's edge**, which is why the theorem sits exactly at the value ¾ of Liggett's bound (§3).

*Check* (`a4_domination.py`, item (2)): for L = 6, 8, 10, 12, every η, every W and both parities of t, the
inequality holds for every i, and the V are exactly i.i.d. Bernoulli(¾) under uniform W. Item (3): exact
survival curves, P(OP₅(½) on Z_L alive at t) ≥ P(ζ on Z_{L/2} alive at t), t ≤ 400, L = 6..14.

*Second half of U.4* (not in the journals; it removes the polynomial loss of §2.7). ζ and OP₅(½) are also
irreducible and aperiodic on non-empty states (ζ: from one occupied site the set can grow by one site per step
to the full ring; from the full ring every subset is a next state). For three such chains with
P_full(T^E > t) ≥ P_full(T^{OP₅} > t) ≥ P_full(T^ζ > t) and each side ~ c·λ^t with c > 0, the eigenvalues are ordered:
λ_L ≥ λ^{OP₅(½)}_L ≥ λ^ζ_{L/2}. ∎
*Check* (`python3 a5_percolation.py 20 20 16`, item (1)): 1 − λ for the three chains, L = 6..16:

| L | 𝒜(L) | OP₅(½) on Z_L | ζ on Z_{L/2} |
|---|---|---|---|
| 6 | 7.83×10⁻³ | 1.72×10⁻² | 2.45×10⁻² |
| 10 | 3.21×10⁻⁴ | 2.13×10⁻³ | 7.11×10⁻³ |
| 16 | 4.79×10⁻⁶ | 1.46×10⁻⁴ | 1.88×10⁻³ |

### 2.6 From F2 to "alive at time e^{cK}/2 with probability ≥ ½". **Small gap, filled.**

The probability journal quotes F2 as "survives to time e^{c₁K} with probability ≥ ½" (from memory); the printed
statement (§1.4) is about the mean E[τ^T] and a limit in law. The library's note bridges the two with the
limit in law. The following needs only the lower bound on the mean.

(i) *Conventions.* In the paper's definition a path may start from any site at height ≤ 0 and must pass through
open sites; a path reaching height t passes through height 0, so {τ^T ≥ t} ⊆ {ζ_t ≠ ∅} for ζ started full
(ζ₀ is full whether or not the sites of height 0 are open). Hence T^ζ > τ^T and E T^ζ ≥ E τ^T > e^{c₁K}.
(ii) *Lemma.* Let a_t = P(ζ_t ≠ ∅ | ζ₀ = full). Then a_{s+t} ≤ a_s a_t (ζ is monotone in its initial state and the
full state is the largest). So for every integer t₀ ≥ 1, E T^ζ = Σ_{t ≥ 0} a_t ≤ t₀ Σ_{j ≥ 0} a_{t₀}^j = t₀/(1 − a_{t₀}),
i.e. **a_{t₀} ≥ 1 − t₀/E T^ζ**. With t₀ = ⌊e^{c₁K}/2⌋: a_{t₀} ≥ ½. ∎
With U.4: P_full(T > ⌊e^{c₁L/2}/2⌋) ≥ ½ in 𝒜(L), for even L ≥ 2K₀.
*Check* (`a5_percolation.py`, item (4)): for ζ at K = 3..10, P(T^ζ ≥ E T^ζ/2) = 0.61 ≥ ½ (it tends to e^{−1/2}).

### 2.7 From one start to τ_L. **Correct.**

(Prob. entry 1.) If P_full(T > t) ≥ ½ then τ_L ≥ (t + m)/((Lm + 1) ln 2), m = ⌈L/4⌉.
*Proof.* u := P_full(S_{t+m} = full) ≥ P_full(T > t)·min_{S ≠ ∅} P_S(S_m = full) ≥ 2^{−Lm−1} (Markov property at
time t; §2.2). By the Markov property at the times j(t + m), P_full(T > n(t + m)) ≥ u^n. And
P_full(T > n) ≤ C λ_L^n (§2.2). So u ≤ λ_L^{t+m}, (t + m) ln(1/λ_L) ≤ (Lm + 1) ln 2, and 1 − λ ≤ ln(1/λ). ∎
With §2.6: τ_L ≥ e^{c₁L/2}/(2(L²/4 + L + 1) ln 2) ≥ e^{cL} for any c < c₁/2 and L large. This is Theorem C, given
F1 (which makes ¾ supercritical, so that F2 applies).
*Check* (`a3_chain.py`, item (6)): with t* the largest t with P_full(T > t) ≥ ½ (computed exactly), the bound
holds for L = 5..12 (L = 12: t* = 9010, bound 351, τ_L = 13007).

(The same conclusion follows from U.4's τ_L ≥ τ^ζ_K and this lemma applied to ζ itself.)

### 2.8 F1 and F2. **Cited.** See §3.

### 2.9 Odd L. **Gap, not filled; not claimed by either line** ("odd L not written").

The drifting blocks need L even. For odd L every arrangement of two-cell blocks leaves one cell over, and I
found none that gives a cylinder: with the spare cell drifting with the blocks, the block graph is the cylinder
of circumference (L+1)/2 with one column of density ½ in place of ¾; with a fixed spare cell it is a strip with
closed ends. The first needs a survival theorem for percolation with a defect column, the second F2 for a strip
(equivalently, for the ring with one cell removed, an interval of L − 1 cells with dead ends). Neither is among
the statements the library has (§3.4). So for odd L the theorem is conditional on more than F1 and F2.
