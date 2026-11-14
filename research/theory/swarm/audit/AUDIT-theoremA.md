# Audit: "a deterministic relative with a theorem"

_Auditor: an agent that is neither the critic nor a solver. 2026-11-14._
_Read: `swarm/PROBLEM.md`, `docs/AUTOMATON.md`, `swarm/source/` and `swarm/probability/` (claims and journals,
the latter including entries 11–15, which appeared while this audit was under way),
`swarm/library/notes/oriented-percolation.md`, `research/theory/exponent/theorems.md` §A–B (cited by the
probability line), and three arXiv papers, one of them in two versions (§3). `swarm/critic/` was not opened until parts A and B were committed
(part C). Every number below comes from a script in this directory, written for this audit; none of the critic's
lab code or tables was used. Commands run from `research/theory/swarm/audit/`; their outputs are in `out/`._

Tags used for verdicts: **correct** (I checked the proof line by line and, where a check by enumeration exists,
ran it); **gap** (what is missing is said; "filled" if the missing argument is given here); **wrong**;
**cited** (rests on a statement from the literature that nobody in this repository has read in the primary
source, or whose printed proof is a sketch).

## 0. Summary

| part of the chain | where | verdict |
|---|---|---|
| Row 0 of 𝒜(L) is the dice chain E₁(½, 0, ½), exactly | source S14 | correct; exhaustive check (A2) |
| The chain: irreducible, aperiodic, one quasi-stationary law; exactly geometric wait from it | prob. entry 1; source S8 | correct (A3) |
| Upper bound τ_L ≤ 3·8^L | prob. entry 1; `exponent/theorems.md` B(a) | correct (A3) |
| The row dominates five-parent oriented site percolation of density ½ (OP₅(½)) | prob. Lemma 1(d), Theorem A′; source Theorem L | correct (A4) |
| Blocks of two cells in a drifting frame: two-parent oriented site percolation of density ¾ | prob. entries 3, 11 | correct (A4) |
| Critical density p₅ of five-parent percolation is < ½ if that of two-parent percolation is < ¾ | prob. entry 11 | correct |
| From "the percolation has mean lifetime e^{cn} on a cylinder" to "the row is alive at e^{cn}/2 with probability ≥ ½" | prob. entries 3, 11; library note | small gap, filled (§2.6) |
| From one start to τ_L | prob. entry 1 | correct (A3) |
| F1: critical density of two-parent oriented site percolation < ¾ | Balister–Bollobás–Stacey 1994 | cited (three secondary sources); a second route through Liggett 1995 exists and passes an exact test (§3.2) |
| F2: finite-volume survival on a cylinder for p > p_c, any finite set of parents | Hartarsky–Szabó 2022, Cor. 4.8 | cited (statement read in the paper; its proof there is a sketch) |
| Odd L | prob. entry 11 | correct by the five-parent route; the two-parent route of entry 3 covers even L only (§2.8) |

**The theorem is correct as a conditional statement**: it holds if F1 and F2 hold, and I found no error in any
step written in the two journals. What does not depend on the literature is Theorem U below. What the theorem
says and does not say about gump: §4. Recommended wording for the notebook: §6. Other claims tagged "proved":
part B. Where this audit and the critic differ, and who is right: part C.

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

Row 0 never influences any other row. The map is a cellular automaton in the sense that each cell is updated by
a fixed local rule; the rule of row 0 differs from the rule of the other rows.

### 1.2 The dice chain

For S ⊆ Z_L and y ∈ Z_L let k = |S ∩ {y−2, y−1, y+1, y+2}|. The chain **E** on subsets of Z_L: given S, the cells of
the next set S′ are independent, and

- a cell of S with k = 2 is in S′ (a *safe* cell);
- a cell not in S with k = 0 is not in S′;
- every other cell is in S′ with probability ½.

Equivalently S′ = F(S) ∪ (a fair-coin thinning of E(S) ∖ F(S)), with E(S) = {y : some cell of S within distance 2}
and F(S) = the safe cells. ∅ is absorbing. (E is the probability line's E₁(π) at π = (½, 0, ½), "the anchor":
each edge cell reads b ∈ {0, 2} live cells beneath it, a fair coin, independent over cells and generations.)

Let Q be the transition matrix of E restricted to the 2^L − 1 non-empty sets. It is irreducible and aperiodic
(§2.2). λ_L := its largest eigenvalue, μ_L := the normalised positive left eigenvector (the quasi-stationary law),
and

  **τ_L := 1/(1 − λ_L)** = the mean of T for the chain started from μ_L.

Two percolation models are used. **OP₅(p)** on Z_L or Z: η_{t+1} = {y ∈ E(η_t) : W_{t+1}(y) = 1}, W i.i.d.
Bernoulli(p) (five parents y−2, …, y+2); p₅ := inf{p : OP₅(p) on Z survives from one cell with positive
probability}. **ζ(p)** on Z_K or Z: ζ_{t+1}(i) = V_{t+1}(i)·max(ζ_t(i), ζ_t(i+1)), V i.i.d. Bernoulli(p) (two parents);
p_c := its critical density. τ^{OP₅}_L, τ^ζ_K: the quantity 1/(1 − λ) for these chains on rings.

### 1.3 The theorem

**Theorem U (unconditional).**
1. In 𝒜(L) the edge row (S_t)_{t ≥ 0} is the Markov chain E started from ν₀, exactly, and the rows beneath at
   time t are independent of S₀, …, S_t and have the law they had at time 0.
2. If ν₀ = μ_L then P(T > t) = λ_L^t for every t, and conditionally on {T > t} the whole configuration at time t
   has the initial law. For any ν₀ with ν₀(∅) < 1, P(T > t) = c·λ_L^t·(1 + o(1)) with c > 0.
3. τ_L ≤ 3·8^L (L ≥ 5).
4. With row 0 started full, P(T > t) ≥ P(OP₅(½) on Z_L, started full, is alive at t) for all t and L ≥ 5, and
   τ_L ≥ τ^{OP₅(½)}_L. For even L ≥ 6 moreover P(OP₅(½) on Z_L alive at t) ≥ P(ζ(¾) on Z_{L/2}, started full, alive at t)
   and τ_L ≥ τ^{OP₅(½)}_L ≥ τ^{ζ(¾)}_{L/2}.

**Theorem C (conditional).** If F1 and F2 below hold, there are c > 0 and L₀ such that for all L ≥ L₀

  **e^{cL} ≤ τ_L ≤ 3·8^L.**

There is no other hypothesis. The constants c and L₀ are not explicit (they come from F2).
F2 is used for five parents at density ½ on the cylinder Z_L × N, and F1 to know that ½ is supercritical for
five parents. (For even L one may instead use F2 for two parents at density ¾ on Z_{L/2} × N; this was the
first form of the proof, and it is the form the source line quotes.)

Not covered: any vessel other than the ring Z_L (an interval with dead ends, say); any τ other than the one
defined in §1.2.

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

**F2** (library note §3; statement read in the paper, proof there a sketch). Setting: "a neighbourhood
X ⊂ Z^d \ {0}, finite, |X| ⩾ 2, with ⟨x, u⟩ > 0 for all x ∈ X for some u […]; the group generated by X is Z^d […]
For d = 2 this covers one-dimensional oriented site percolation with any finite set of parents:
X = {(0,1),(1,1)} (two parents) and X = {(−2,1), …, (2,1)} (five parents) both qualify".
> Corollary 4.8 [paper, v3 p. 14; Theorem 17 in v1, §5.5]. GOSP on the quotient graph with vertex set
> T_n^{d−1} × Z (torus of side n in the space directions; for d = 2, a cylinder of circumference n). Extinction
> time τ^T = sup{t ⩾ 0 : T_n^{d−1} × {0, −1, −2, …} → T_n^{d−1} × {t}} (i.e. started full). […] For all p > p_c
> there exist c, C ∈ (0, ∞) such that τ^T / E_p[τ^T] → E (standard exponential) in law, and
> e^{c n^{d−1}} < E_p[τ^T] < e^{C n^{d−1}} for n large enough.

The theorem uses only: for d = 2, the five parents, p = ½ > p₅: **E[τ^T] > e^{cn} for n large**. (I re-read §1.1
and the corollary in arXiv:2103.15621v3, pp. 2–3 and 14; the library's transcription is accurate. See §3.3.)

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
In 𝒜(L) the comparison is pathwise and uses no auxiliary randomness. With S₀ = η₀ = full it gives the first
inequality of U.4.

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

### 2.5 Blocks: OP₅(p) dominates two-parent percolation of density 1 − (1 − p)². **Correct.**

(Prob. entry 3 on the ring Z_L, L = 2K; entry 11 on Z.) Blocks X_i^t = {2i + t, 2i + t + 1}, i ∈ Z_K (ring, indices
mod L) or i ∈ Z; for each t they partition the ring (the line).
ξ_t(i) := 1[η_t ∩ X_i^t ≠ ∅], V_{t+1}(i) := 1[W_{t+1} = 1 somewhere in X_i^{t+1}].
*Claim.* ξ_{t+1}(i) ≥ V_{t+1}(i)·max(ξ_t(i), ξ_t(i+1)), and the V are i.i.d. Bernoulli(1 − (1 − p)²).
*Proof.* X_i^t ∪ X_{i+1}^t = {2i+t, …, 2i+t+3} and X_i^{t+1} = {2i+t+1, 2i+t+2}: each of the two child cells is within
distance 2 of each of the four parent cells. So if a parent block meets η_t, both child cells lie in E(η_t), and
the child block meets η_{t+1} iff V_{t+1}(i) = 1. The blocks X_i^{t+1} are disjoint, so the V_{t+1}(i) are
independent, each 1 with probability 1 − (1 − p)², independent of the past. ∎
By induction ζ_t ≤ ξ_t for the two-parent percolation ζ driven by the same V. Consequences:
(a) *on the ring, p = ½, L even:* {ζ_t ≠ ∅} ⊆ {η_t ≠ ∅}, the second inequality of U.4;
(b) *on Z:* if 1 − (1 − p)² > p_c then ζ survives from one site with positive probability, hence OP₅(p) survives
from one cell, hence p ≥ p₅. So **p₅ ≤ 1 − (1 − p_c)^{1/2}, and p₅ < ½ iff this bound is < ½ iff p_c < ¾.**
(Entry 11 (ii), (iii).) Under F1, p₅ ≤ 1 − √0.2509 = 0.4991.

Two cells is the largest block for which this works (2m consecutive parent cells leave 6 − 2m cells within
distance 2 of all of them; a child needs m), and ½ is the largest density any law of b can give (a cell with
k = 4 needs b = 0, a cell with k ≤ 1 needs b = 2). So **¾ is the largest block density a one-step comparison
can reach for the 2D rule's edge**, which is why the theorem sits exactly on the value ¾ of Liggett's bound
(entry 11 says the same; §3).

*Eigenvalues* (not in the journals). E, OP₅(½) and ζ(¾) on rings are irreducible and aperiodic on non-empty
states (ζ: from one occupied site the set can grow by one site per step to the full ring; from the full ring
every subset is a next state; OP₅ likewise). For such chains P_full(T > t) ~ c·λ^t with c > 0, so the ordering of
the survival probabilities from the full ring orders the eigenvalues: λ_L ≥ λ^{OP₅(½)}_L (all L ≥ 5) and
λ^{OP₅(½)}_L ≥ λ^{ζ(¾)}_{L/2} (L even). This is the rest of U.4. ∎

*Check* (`a4_domination.py`, item (2)): for L = 6, 8, 10, 12, every η, every W and both parities of t, the
block inequality holds for every i, and the V are exactly i.i.d. Bernoulli(¾) under uniform W. Item (3): exact
survival curves, P(OP₅(½) on Z_L alive at t) ≥ P(ζ(¾) on Z_{L/2} alive at t), t ≤ 400, L = 6..14.
`python3 a5_percolation.py 20 20 16`, item (1), and `python3 a9_probability_round3.py`, item (5): 1 − λ for the
three chains (odd L: first two):

| L | 𝒜(L) | OP₅(½) on Z_L | ζ(¾) on Z_{L/2} |
|---|---|---|---|
| 6 | 7.83×10⁻³ | 1.72×10⁻² | 2.45×10⁻² |
| 10 | 3.21×10⁻⁴ | 2.13×10⁻³ | 7.11×10⁻³ |
| 16 | 4.79×10⁻⁶ | 1.46×10⁻⁴ | 1.88×10⁻³ |

### 2.6 From F2 to "alive at time e^{cn}/2 with probability ≥ ½". **Small gap, filled.**

Entry 3 quoted F2 from memory as "survives to time e^{cK} with probability ≥ ½". The printed statement (§1.4) is
about the mean E[τ^T] and a limit in law; entry 11 and the library's note bridge the two with the limit in law
(P(τ > E τ/2) → e^{−1/2}). The following needs only the lower bound on the mean, and settles the convention
"started full". Let η be OP₅(½) on Z_n (or ζ on Z_K), started full.

(i) *Conventions.* In the paper a path may start from any site at height ≤ 0 and must then pass through open
sites; a path that reaches height t leaves height 0 from some site, so {τ^T ≥ t} ⊆ {η_t ≠ ∅} for η₀ full. Hence
T^η > τ^T and E T^η ≥ E τ^T > e^{cn}.
(ii) *Lemma.* Let a_t = P(η_t ≠ ∅ | η₀ = full). Then a_{s+t} ≤ a_s a_t (η is monotone in its initial state and the
full state is the largest). So for every integer t₀ ≥ 1, E T^η = Σ_{t ≥ 0} a_t ≤ t₀ Σ_{j ≥ 0} a_{t₀}^j = t₀/(1 − a_{t₀}),
i.e. **a_{t₀} ≥ 1 − t₀/E T^η**. With t₀ = ⌊e^{cn}/2⌋: a_{t₀} ≥ ½. ∎

With U.4: P_full(T > ⌊e^{cL}/2⌋) ≥ ½ in 𝒜(L) for L ≥ L₀ (five parents, n = L).
*Check* (`a5_percolation.py`, item (4)): for ζ(¾) at K = 3..10, P(T ≥ E T/2) = 0.61 ≥ ½ (it tends to e^{−1/2}).

### 2.7 From one start to τ_L. **Correct.**

(Prob. entry 1.) If P_full(T > t) ≥ ½ then τ_L ≥ (t + m)/((Lm + 1) ln 2), m = ⌈L/4⌉.
*Proof.* u := P_full(S_{t+m} = full) ≥ P_full(T > t)·min_{S ≠ ∅} P_S(S_m = full) ≥ 2^{−Lm−1} (Markov property at
time t; §2.2). By the Markov property at the times j(t + m), P_full(T > n(t + m)) ≥ u^n. And
P_full(T > n) ≤ C λ_L^n (§2.2). So u ≤ λ_L^{t+m}, (t + m) ln(1/λ_L) ≤ (Lm + 1) ln 2, and 1 − λ ≤ ln(1/λ). ∎
With §2.6: τ_L ≥ e^{cL}/(2(L²/4 + L + 1) ln 2) ≥ e^{c′L} for any c′ < c and L large.
*Check* (`a3_chain.py`, item (6)): with t* the largest t with P_full(T > t) ≥ ½ (computed exactly), the bound
holds for L = 5..12 (L = 12: t* = 9010, bound 351, τ_L = 13007).

### 2.8 Assembly; the two routes; odd L. **Correct, given F1 and F2.**

*Five-parent route (entry 11; every L).* F1 ⇒ p₅ < ½ (§2.5(b)) ⇒ F2 applies to five parents at density ½ on the
cylinder Z_L × N ⇒ E T^η > e^{cL} ⇒ (§2.6) P_full(T > e^{cL}/2) ≥ ½ ⇒ (§2.7) τ_L ≥ e^{c′L}. With §2.3 this is
Theorem C. The blocks are used on Z only, where parity does not matter.
*Two-parent route (entry 3; even L).* §2.5(a) on the ring, F1 ⇒ ¾ > p_c, F2 for two parents on Z_{L/2} × N, then
§2.6 and §2.7. On a ring of odd length this route does not close: every arrangement of two-cell blocks leaves
one cell over; if the spare cell drifts with the blocks the block graph is a cylinder of circumference (L+1)/2
with one column of density ½, and if it stays put it is a strip with closed sides. The five-parent route
avoids the question.

Both routes use F2 as printed (it is stated for every finite set of parents). They differ in how much of it:
the first needs it for a neighbourhood with range 2, the second only for the classical two-parent model.

### 2.9 What is not explicit

c and L₀. From exact numbers (§3.6, not a proof): the two-parent route would give about 0.14 per cell, the
five-parent route at most 0.42, against the automaton's own 0.67 at L = 18.

## 3. Are the literature facts enough?

### 3.1 What exactly is needed

Theorem C needs one statement about a classical model:

> **(F)** OP₅(½) on the ring Z_n, started full, has mean extinction time ≥ e^{cn} for n large

(or, for even L, the same for ζ(¾) on Z_K). F1 ∧ F2 ⇒ (F), and (F) ⇒ Theorem C by §§2.3–2.7, with no further
input. So the theorem is conditional on (F), and through it on F1 and F2. As the library records them, **F1 and
F2 are enough**: the model of F1 (two parents, sites) is the model of the blocks; the vessel of F2 (a cylinder)
is the vessel of the automaton (a ring); the neighbourhood is admissible; "started full" matches (§2.6).

### 3.2 F1 (p_c < ¾): two routes, both second-hand

(a) *Balister–Bollobás–Stacey 1994, p_c ≤ 0.7491.* Not opened by anyone here (Wiley; not open). Secondary
sources: Hartarsky–Szabó (quoted in §1.4; I re-read the passage in v1, pp. 28–29); Holmes–Salisbury (library
note; not re-read by me); and a third, found for this audit, Köhler-Schindler and Sulser, arXiv:2405.07345v1,
p. 5: "the upper bound p_c^site(Z⃗²) ≤ 0.7491 [BBS94]", with the footnote "As pointed out in [BBS94], the upper
bound p_c^site(Z⃗²) ≤ 0.72599 given in [BBS93] is not correct. It should have been p_c^site(Z⃗²) ≤ 0.762." So the
corrected 1993 bound is above ¾ and only the 1994 paper gives F1 by this route. It is computer-assisted, and
the margin is 0.0009.

(b) *Liggett 1995 at equality, plus "no percolation at criticality".* The library's note leaves open whether
Liggett's theorem gives survival at density exactly ¾. From what Ráth and Valesin print it does, in two lines.
I re-read arXiv:1912.09825v3, Appendix 7.2 (pp. 59–61):
- Proposition 7.3 ("a special case of [Li95, Proposition 2.1]"): "If p ≥ 3/4 then F is positive and
  non-increasing, moreover Σ_k F(k) < ∞", for an explicit F; ψ([n, ∞)) = F(n) defines a gap law and Ψ the
  stationary renewal measure with that gap law.
- "Equation (1.4) in [Li95] gives" for every finite A ⊂ Z: Ψ(η⁰ ∩ A = ∅) ≥ P(η⁰ ∩ η₁^A = ∅) (η⁰ ~ Ψ independent
  of the percolation, η₁^A one step of ζ from A), and "this can be iterated to yield
  Ψ(η⁰ ∩ A = ∅) ≥ P(η⁰ ∩ η_n^A = ∅), n ∈ N".

Hence P(η_n^A = ∅) ≤ Ψ(η⁰ ∩ A = ∅) < 1 for all n: ζ(p) survives from A = {0} with probability ≥ Ψ(η⁰(0) = 1)
= 1/Σ_k F(k) for every p ≥ ¾. At p = ¾ the quoted formulas give a = 1, b = −1/3, Σ_k F(k) = 3/2: **survival
probability ≥ 2/3 at density exactly ¾.** Then p_c < ¾ follows from θ(p_c) = 0 (Hartarsky–Szabó, Remark 4.6,
read in v3 p. 13: "θ(p_c) = 0 following from Theorems 4.1 and 4.2"; originally Bezuidenhout–Grimmett).
This route does not use a computer. It is still second-hand: I have not seen Liggett's Proposition 2.1 or (1.4).

*Exact test of the quoted statements at p = ¾* (`python3 a6_liggett_at_three_quarters.py`, rational arithmetic):
F(k) > 0 and non-increasing for k ≤ 401; k^{3/2}F(k) → 0.2992, and Σ_k F(k) = 3/2 from the generating function;
the inequality holds for all 64 sets A ⊆ {0..6} containing 0, **with equality exactly when A is an interval**,
which is the signature of a Holley–Liggett renewal measure and makes a transcription error at p = ¾ unlikely.
And (`a5_percolation.py`, item (5)) the exact probability that ζ(¾) from one site is alive at time n is 0.8047 at
n = 21 and falling slowly, above 2/3 as it must be. This tests the statement; it does not prove it for all A.

So F1 has two independent supports. Neither has been read in the primary source.

### 3.3 F2 (finite-volume survival): printed for a cylinder, proof sketched

I read it in arXiv:2103.15621v3, p. 14, and the sketch in v1, Appendix A.4. The corollary is introduced with
"for completeness let us mention a consequence of the restart arguments concerning GOSP on tori", and after it:
"The proofs rely on Theorems 4.2, 4.3 and 4.7 (see [23, App. A.4] for a sketch following [34])". The sketch for
the lower bound on the mean: embed boxes of the block construction in the torus so that the process dominates
a two-parent percolation "with finite dependence range and parameter close to 1", then Liggett–Schonmann–Stacey
and the same statement for two-parent percolation near density 1. For d = 2 this is the oriented-percolation
form of Durrett–Liu / Durrett–Schonmann 1988 (contact process); the ingredients are classical. I regard F2 as
reliable. It is not proved here, and its printed proof is a sketch.

### 3.4 Ring and interval

The automaton is on a ring, the percolation on a cylinder: F2 as printed is what is needed. **The theorem as
stated does not need an interval.** An interval with dead ends would be needed for a variant of 𝒜 with a dead
cell on each side of the row (the probability line's T2; its exact tables for such vessels have no theorem
behind them, as entry 11 says). For that one needs supercritical oriented percolation in a strip with closed
sides to live e^{cK}; the library found no printed statement beyond density near 1 (Mountford's Fact 2.1).

### 3.5 What survives without the literature

Theorem U: the exact identification, the exactly geometric law, τ_L ≤ 3·8^L, and
τ_L ≥ τ^{OP₅(½)}_L ≥ τ^{ζ(¾)}_{L/2}: *the edge of 𝒜(L) lives at least as long as five-parent percolation of density ½
on the same ring.* Plus the exact values of §3.6.

No exponential lower bound survives unconditionally, and no weaker version with more room exists inside this
proof:
- *Another density.* Every law of b gives block density ≤ ¾ (§2.5). So Liggett's printed bound p_c ≤ ¾ (his
  abstract) is never enough by itself; strictness is needed, from §3.2(a) or (b).
- *Five parents directly.* The condition is p₅ < ½. The truth is probably far inside (the probability line
  quotes a lab scan placing p₅ between 0.36 and 0.44; my exact steps of ln τ^{OP₅(½)}_L are 0.42 per cell at L = 20
  and those of ζ(¾) are 0.29 per block, §3.6), but the only *proof* of p₅ < ½ on offer is the block bound, which
  is F1 again. A finite certificate for p₅ < ½ (the renormalisation criterion of Balister–Bollobás–Stacey as
  restated by Hartarsky–Szabó, v1 Theorem 24, run exactly for OP₅(½)) would replace F1 by a computation with a
  wide margin; that criterion is itself printed with a sketched proof, and I did not attempt it.
- *A proof from scratch* of (F) would be a block construction down to density near 1 and a contour count.
  Not attempted.

### 3.6 What exact numbers say (evidence, not proof)

`python3 a3_chain.py 18`, item (5). ln τ_L for 𝒜(L) (Collatz–Wielandt brackets on 1 − λ_L agree to 8 digits):

| L | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ln τ_L | 3.8228 | 4.8496 | 5.7232 | 6.5319 | 7.3516 | 8.0428 | 8.7556 | 9.4733 | 10.1847 | 10.8849 | 11.5701 | 12.2492 | 12.9241 | 13.5946 |
| step | | 1.027 | 0.874 | 0.809 | 0.820 | 0.691 | 0.713 | 0.718 | 0.711 | 0.700 | 0.685 | 0.679 | 0.675 | 0.671 |

The four values quoted in source S14 (iii) (L = 8, 12, 16, 18) are reproduced to the last digit. The step is
still falling by about 0.004 per cell at L = 18: "≈ 0.67 per cell" is a local slope, not an asymptote.

`python3 a5_percolation.py 20 20 16`, items (2), (3). Steps of ln τ on rings:

| model | K or L = 10 | 15 | 20 | reading |
|---|---|---|---|---|
| ζ(0.60) on Z_K | 0.018 | 0.003 | 0.0006 | subcritical: ln τ bounded (2.89) |
| ζ(0.7055) on Z_K | 0.170 | 0.110 | 0.082 | near critical: step × K ≈ 1.64, a power law |
| ζ(0.75) on Z_K | 0.362 | 0.313 | 0.2935 | step × K grows linearly: exponential, c ≈ 0.27–0.29 per block |
| ζ(0.85) on Z_K | 1.123 | 1.095 | 1.081 | exponential |
| OP₅(½) on Z_L | 0.485 | 0.435 | 0.4165 | exponential, c ≤ 0.42 per cell |

So at the sizes that can be computed (F) is visibly true, for two parents at ¾ and for five at ½, and ¾ is
clearly on the supercritical side of the near-critical behaviour at 0.7055.

## 4. In what sense is 𝒜(L) deterministic, and what does the theorem say about gump?

**It is a deterministic map with a random initial condition, and nothing more.** The update of §1.1 involves no
chance. All randomness is in the initial state: a tape of independent fair bits, each written twice, which the
conveyor carries to the edge two rows per generation; each bit is read once, at one generation, by one cell.
In the language of dynamics: 𝒜(L) is the skew product (S, ω) ↦ (G(S, ω₁), σω) over the one-sided Bernoulli shift
σ on tapes ω = (ω₁, ω₂, …), ω_i ∈ {0,1}^{Z_L} uniform; G is one step of the edge rule. Every finite Markov chain
with rational transition probabilities can be written this way (source C1′), so the construction carries no
information beyond the chain E. The base is "provably mixing" only in the trivial sense that it is a Bernoulli
shift read through its own generator. With the quasi-stationary start, μ_L ⊗ (tape) is a conditionally
invariant measure of an open system with escape rate −ln λ_L, exactly.

**The randomness is not self-made.** Three precise differences from gump and from the 2D rule in a vessel:
1. *Budget.* The edge consumes L fresh bits per generation, for ever: L·τ_L ≥ e^{cL} bits over a lifetime. The
   system is infinite; cut off at H rows it is the chain E for ⌊H/2⌋ generations and then a deterministic
   one-dimensional automaton over an empty tape. A finite vessel of gump holds N bits in all (source C3).
2. *No feedback, no dynamics in the bulk.* The bulk neither reads the edge nor transforms what it carries.
   (In the variant of S14 the bulk is a parity automaton started from its invariant uniform measure, and it may
   read the edge; the row read by the edge is still an invertible re-encoding of initial bits: checked, A2.)
3. *The drive is not the rule's.* The two cells beneath an edge cell are always equal (π₁ = 0; in the rule's own
   bulk b = 1 has probability about ½), fresh at every generation, independent across cells.

**What the theorem says about the 2D rule:** one thing. The edge's local rule, as a map (row, two rows beneath)
↦ row, has the property that every cell within distance 2 of a live cell is alive next for b = 0 or for b = 2.
Over a drive that gives each of those two values conditional probability ≥ p > p₅, the edge therefore lives
e^{cL} (Theorems A′, L). At the anchor the rule's two mechanisms, the threshold and the cap, each act as a fair
coin and are indistinguishable in law: the chain E is OP₅(½) plus safe cells.

**What it does not say.** Nothing about the lifetime of an edge of the 2D rule in a strip or box run by the rule
itself, and nothing about gump. Its exponent (0.67 at L = 18) is not the measured 0.36–0.42. And the method
provably stops short of both: for independent rows beneath at the bulk density the best one-step monotone
minorant dies in O(log L) generations (prob. Lemma 2(b); checked, part B); the hypothesis of Theorem L fails
for the rule's own statistics (a lone cell needs b = 2, probability about 0.22–0.34, against 0.4991); a gump
face cell with six live in-face neighbours dies whatever is beneath it (source C18), and the two-generation
substitute (prob. Lemma 4) has block density at most 19/27 < p_c (prob. claim 20).

## 5. Checks run for part A

All by scripts in this directory; `out/*.log` holds the outputs. One core; the longest takes five minutes.

| script | what it checks | result |
|---|---|---|
| `a1_rule_and_table.py` | threshold form of B34/S234; alive-sets A(x, k); table a(x, k) at three laws; least non-forced probability ≥ min(π₀, π₂) | ALL OK |
| `a2_automaton.py` | 𝒜(L) run as a map on the array, all initial conditions: rows 1, 2 = fresh bits; law of the edge trajectory = chain E, exactly, (L, t) = (5,3), (6,2), (6,3), (8,2); the parity variant (uniformity of the read row); source Lemma 1 as a bijection | ALL OK |
| `a3_chain.py 18` | engine against dense kernel; kernel uniform on [F(S), E(S)]; irreducibility; three-move game L ≤ 16 and min_S P_S(T ≤ 3) ≥ 8^{−L}; λ_L, τ_L for L = 5..18 with brackets; geometric law from μ; "one start to τ" | ALL OK |
| `a4_domination.py` | W is a bijective image of the fresh bits and E(S) ∩ W ⊆ S′; block inequality for all (η, W), L ≤ 12; survival curves ordered, L ≤ 14; Theorem L for a correlated row-dependent drive | ALL OK |
| `a5_percolation.py 20 20 16` | eigenvalue ordering of U.4; lifetimes of ζ(p) on Z_K (K ≤ 20) and OP₅(½) on Z_L (L ≤ 20); lemma of §2.6; survival of ζ(¾) from one site | ALL OK |
| `a6_liggett_at_three_quarters.py` | the quoted Liggett statements at p = ¾, exactly | ALL OK |
| `a9_probability_round3.py`, item (5) | λ_L ≥ λ^{OP₅(½)}_L for L = 5..15, odd and even | ALL OK |

The test of the theorem's statement at small L is `a3_chain.py` (τ_L between the proved lower comparison and
3·8^L, growing by a factor ≈ 2 per cell) together with `a2_automaton.py` (the automaton itself has that law).

## 6. Judgment

**Yes, it is worth recording, as a conditional theorem about a relative, in words that do not oversell it.**
The mathematics inside the repository is complete and correct: every step from the automaton to the two
percolation facts is proved in the journals, and I could verify each by hand and by enumeration. What is not
proved here is classical percolation theory, cited at second hand (F1) or from a printed sketch (F2); both are
very likely true, and F1 has two independent supports. The result is new only in its packaging: it is the
probability line's dice theorem with the dice stored in the initial condition. Its value to the project is as a
fixed point and a foil: the simplest system with the 2D rule's own edge in which "lifetime exponential in the
length, memoryless" is a theorem, and a precise list of what a proof for the rule itself may not use (§4).

Proposed wording for the notebook:

> **A deterministic relative of the 2D rule with an exponential law [proved, conditional on two published
> percolation statements; audited 2026-11-14, `swarm/audit/AUDIT-theoremA.md`].** Let 𝒜(L) be the automaton on
> Z_L × N in which row 0 follows B34/S234 on the cross and every other row copies the row two below it, started
> with independent fair bits beneath row 0, each written into two consecutive rows. Then row 0 is exactly a
> Markov chain (each cell within distance 2 of a live cell is alive next with probability ½, except that a live
> cell with two live in-row neighbours survives surely); from its quasi-stationary law the edge dies after an
> exactly geometric wait with mean τ_L; τ_L ≤ 3·8^L; and τ_L is at least the corresponding lifetime of
> five-parent oriented site percolation of density ½ on the ring Z_L. *If* (F1) the critical density of
> two-parent oriented site percolation is below ¾ (Balister–Bollobás–Stacey 1994, computer-assisted; or
> Liggett 1995 at equality with Bezuidenhout–Grimmett; all second-hand here) *and* (F2) supercritical oriented
> site percolation on a cylinder of circumference n lives e^{cn} (Hartarsky–Szabó 2022, Cor. 4.8; printed with a
> sketched proof), *then* e^{cL} ≤ τ_L for all large L. Exact: ln τ_L = 6.5319, 9.4733, 12.2492, 13.5946 at
> L = 8, 12, 16, 18. This is a deterministic map with a random initial condition, a tape read once; it is not
> self-made randomness and says nothing about gump or about the 2D rule in a vessel run by the rule. With this
> tape the two cells beneath an edge cell are always equal and the rule's cap and threshold are both fair
> coins. The same argument cannot reach independent rows beneath (prob. Lemma 2) or a gump face (source C18).

Grade suggested for `research/CLAIMS.md`: proof audited by an independent reader; conditional on F1, F2;
numbers reproduced by a second implementation.

---

# Part B. The other claims tagged "proved"

One line each; the order within each table is my view of importance. "A7 (3)" means item (3) of
`a7_other_claims.py`; A8 = `a8_threshold_lemma.py`; A9 = `a9_probability_round3.py`; A10 = `a10_claim13.py`.

## B1. Probability line (`probability/claims.md`, list after round 3)

| # | claim | verdict | basis |
|---|---|---|---|
| 5, 11 | Theorem A (entry 11 form) and A′ | **correct, conditional on F1, F2** | part A |
| 19 | Lemma 4: a gump face over dice with weight ≥ s at b = 0, at b = 3 and ≥ s″ on {1,2} lies above a monotone two-generation percolation; E T ≤ s^{−A} | **correct** | proof read; tables B(x, k), (O1), (O2) by enumeration; (a), (b), η′ ⊆ S′, Z′ ∩ S′ = ∅ for all 512 states × 4⁹ dice tables of a 9-cell 6-regular face (A9 (3), (4)). Its hypothesis is per cell given all else; in gump's geometry cells of one cube share cells beneath, as entry 13 says |
| 7 | Lemma 2(b): the sharp one-step minorant at Bin(2, ρ), ρ ≥ 0.46, contracts Φ = \|η ⊕ [−2,2]\| by κ < 1 | **correct** | proof read (end cells of a run have rate s; union bound over runs; ratio largest at run length 5); exact maximum of E Φ′/Φ over all η on Z_L, L = 5..14: 0.919 ≤ κ = 0.9475 at ρ = 0.472; threshold 0.2763 reproduced (A7 (2)) |
| 3 | Lemma 1: the sharp one-step attractive minorant; coupling; domination of OP₅(s) | **correct** | table reproduced by minimising over all supersets on Z_7, four laws (A7 (1)); attractiveness and maximality are immediate from the definition |
| 17 | Lemma 5: any arc of m ≤ L − 12 cells is emptied in three generations with probability ≥ p^{3m+12}, whatever the rest of the row | **correct** | proof read (the three moves; no two forced ends within distance 2); exact min over all S of P_S(S₃ ∩ I = ∅), L ≤ 16, m ≤ 4, two laws: far above the bound (A9 (1)) |
| 2 | ring chain irreducible, aperiodic; E_S T ≤ 3p^{−3L}; from one start to τ | **correct** | §§2.2, 2.3, 2.7 |
| 18 | Lemma 6: the chain on a dead-ended (or reflecting) interval is irreducible and aperiodic | **correct** (dead ends: proof read and graph checked, M = 5..11, A9 (2); reflecting ends: proof read only) | |
| 14 | Proposition W: Q_ring = w·Q_dead on rows with four dead cells; h_ring ≥ w_min^{n+1}P_ν(T_d = n+1); the conditional bound under H(n, c) | (a), (b) **correct** (A7 (3): identity to 10^{−16}, inequality for n ≤ 7, L = 9..11); (c) and the round-3 form with m_G ≥ p^{24} − 3h: algebra **correct**; they are conditional on H, which is not established | |
| 15 | Proposition F: τ_L(OP₅(p)) ≤ C·L·β*^L, ln β*(½) = 0.4812 | **correct**; the tilted hitting estimate is standard and not written out | algebra of the root checked; exact steps of ln τ for OP₅(½) on rings are below 0.4812 from L = 11 on (0.4165 at L = 20; A5 (3)) |
| 6 | Lemma 2(a): OP₅(p) dies out for p < 1/3 | **correct** | proof read (right edge moves by at most 2 − X, X geometric) |
| 12 | Lemma 3: d + Qg ≤ ag + ε everywhere, a + ε < 1 ⇒ τ ≥ 1/ε | **correct** | proof read; g = 1 − v/max v (v the right eigenvector) satisfies the inequality with equality at a = λ, ε = 1 − λ, the boundary case a + ε = 1, so the conclusion cannot be improved |
| 1, 4 | the table a(x, k); s ≤ ½; no one-step comparison for two rows or a gump face | **correct** | A1; A7 (7) |
| 16 | monotone models: τ_dead ≤ τ_ring at equal length | **correct** (first half) | same dice, fewer parents; OP₅(½), M = 5..14 (A7 (4)). The second half is the critic's exact data, not audited |
| 20 | limits of Lemma 4: σ ≤ 1/3, density ≤ 665/2187; contraction 7/8 for independent cells beneath; block density ≤ 19/27 | arithmetic **correct** (A9 (6)); the last statement is true for the kind of block comparison described in entry 14.3, not for "any comparison" | |
| 8 | "any block comparison with conditionally independent blocks over n ≥ 2 generations needs seeding over ≥ 2n − 3 cells" | the arithmetic is **correct**; the framing (equal blocks, parents at half spacing, independence from disjoint noise cones) is narrower than "any" | proof read only |
| 13 | no certificate of Lemma 3 of the form r^{additive local health} | **correct**; entry 7 is an outline, and it closes (proof in §C3; this row read "not verified" when part B was first committed, see §C2). The proof gives more than is claimed: for fixed health and r the smallest admissible ε stays above a constant for all large L and every a ≤ 1. "L large" matters: one such g has ε falling like e^{−0.43L} on L = 8..16 before its floor | proof written out; A10: on a grid of 72 certificates (two laws, three healths, three r, four a) every one has a positive floor, 1.5×10⁻⁸ to 0.31, from a droplet of 3 to 71 cells |

Not audited (not tagged proved): 9, 10, 21.

## B2. Source line (`source/claims.md`, round 3)

| # | claim | verdict | basis |
|---|---|---|---|
| C16, C17 | Theorem A; Theorem L | **correct**; A conditional on F1, F2 | part A |
| C1, C1′, C1″ | exact source with feedback; any top with rational local randomness; exact conditionally invariant measure | **correct** | §2.1; A2 (b), (c). "No finite deterministic system has one": immediate (in a finite deterministic system every state that dies does so within \|Ω\| steps) |
| C5, C6 | Lemma 4 (localised threshold lemma) and Corollary 4a: under the uncapped rule on any subset of the lattice, finite or infinite, every cell has at most C_U mismatches, so is eventually of period ≤ 2 | **correct** | proof read line by line (the identity for K(t+1) − K(t); the three cases; the bounds −2θ′S ≤ K ≤ c′S). On orbits of gump and of the uncapped rule on a torus of 4³ cubes and of the 2D rules on a 12 × 12 torus: identity to 10^{−13}, every term bound, and the inequality at every T ≤ 300, λ = 1.05, 1.1, 1.15 (2D: 1.1, 1.2). C_U = 1.41×10⁶ at λ = 1.1 reproduced from sphere sizes (S = 13351) (A8). I did not test an infinite configuration |
| C7 | a threshold bulk is not a source; weights λ^{−2⌈k/2⌉}; death from n ≤ 3 is by starvation | **correct** as consequences of C5/C6; d = ⌈k/2⌉ and S = A(1 + 2/(λ² − 1)) checked by hand | |
| C10 | frozen drive cells: the next state of a cell of 𝓛_w is fixed by (x, k) unless k + x = 3 or k = 5 (2D: k + x = 2 or k = 4); the three-unknown and two-unknown cases | **correct** | enumeration (A7 (6)) |
| C13 | lone interior gump face cell over dice: P(death) = (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴, E n′ = 7ρ³; 2D: (1 − ρ²)⁵, 5ρ² | **correct** | my own enumeration of the lattice: 18 cells are read, 108,045 of 2¹⁸ patterns kill at ρ = ½; closed form matched at ρ = 0.4155, 0.52 (A7 (5)) |
| C3, C4 | entropy accounting; Markovian projection | **correct** | one-line proofs read. C4's converse was withdrawn in S7, rightly |
| C11, C12 | Theorems H and U (hazard between exponential moments; lifetime ≤ g·δ^{−gU}) under finite energy of the drive | **correct as implications** | proofs read; U needs only marginals, as its proof says. Their hypotheses are stated by the source line itself to fail in the one vessel examined; I did not re-examine that, nor the "cube lemma" beyond one cube (A7 (5)), nor g = 2 for gump |
| C18 | a gump face can overcrowd itself; a dead face cell with three live in-face neighbours is born only for b ∈ {1, 2} | **correct** | A7 (7) |
| C2 | table of differences between gump and "gump on parity" | the rows I checked (T2 at the face uses only the rule at and outside the face; exact dice for ⌊H/2⌋ generations) are right; the table is descriptive | |

Not audited (not tagged proved): C8, C9, C14, C15.

---

# Part C. Comparison with the critic

Written after parts A and B were committed (commit `91967c5`); `critic/to-probability.md` and
`critic/to-source.md` were opened only then. The critic's replies cover the probability line's rounds 1 and 2
(entries 1–10) and the source line's rounds 1–3.

## C1. What the critic has not reviewed

There is no reply to the probability line's round 3 (entries 11–15). So the critic has not seen Theorem A in
its final form (the five-parent route, which is what covers odd L), nor the use of F1 and F2 as the library
recorded them, nor claims 17–20 (Lemmas 4, 5, 6 and the limits of Lemma 4). Its replies of rounds 2 and 3 say "F1
and F2 are still not on the shelf"; the library's note has appeared since. For these items §§2.5–2.8, §3 and
the rows 5/11, 17, 18, 19, 20 of table B1 are the only independent check there is.

## C2. Where we differ, and who is right

On every step of the chain that both of us examined the verdicts agree: the identification of row 0 with the
chain, the upper bound, the domination of OP₅(p), the block step, the bridge from one start to τ_L, Theorems A′
and L. The numbers computed by both, with different code, agree to every printed digit: ln τ_L at the anchor
for L = 8, 10, 12, 14–18; ln τ of OP₅(½) on rings of 8–19 cells; the suprema 0.9262, 0.9187, 0.9322 of Lemma 2(b)
(the critic: on a ring of 14; here: over rings of 5 to 14 cells); 108,045 of 2¹⁸ for the lone gump cell; sphere
sizes 1, 12, 70, 212, 464, 820; and the law of the edge of 𝒜(5) by enumeration.

| item | critic | this audit | who is right |
|---|---|---|---|
| probability claim 13 (no certificate r^{additive health}) | "reduction confirmed" (round 2) | part B as first committed: "not verified, I would tag it sketched" | **the critic.** The outline of entry 7 is a complete argument once its three steps are written down (§C3). I was too cautious; table B1 now says "correct" |
| the same claim, its reach | no remark | the floor under ε exists for every health but can lie far below what small rings show: g = 0.6^{\|S ⊕ [−2,2]\|} with a = 0.9 at the anchor has smallest admissible ε = 9.1×10⁻³, 3.8×10⁻³, 1.6×10⁻³, 7.0×10⁻⁴, 2.9×10⁻⁴ at L = 8, …, 16 (a factor e^{−0.43} per cell), and its floor is 2.5×10⁻⁷, reached by a droplet of 21 cells (A10) | an addition, not a contradiction. The claim is about L → ∞; nobody should read "dead end" as "useless at the sizes one can compute" |
| the constant S of source Corollary 4a at λ = 1.1 | 13,336 | 13,350.9 | **this audit**, by 0.1%. The critic's script sums spheres to radius 59; with my sphere sizes that partial sum is 13,335.92 and the rest is 15.03 (A8, item (d)). C_U = 1.41×10⁶ either way, but C_U is an upper bound and needs the whole sum |
| how fragile F1 is | the theorem's region is "non-empty only by the third decimal of F1" (round 1) | true of the route through 0.7491; a second route (Liggett's theorem at density exactly ¾, plus no percolation at the critical point) puts the anchor inside with no decimal at stake (§3.2(b)) | both. The critic's sentence is right about the *width* of the proved region (min(π₀, π₂) > 0.4991) and incomplete about its non-emptiness. Both routes are second-hand |
| from F2 to "alive at time t with probability ≥ ½" | confirmed the bridge "P_full(T > t) ≥ ½ ⇒ τ_L", which takes the probability as given; F2 itself not yet available to it | F2 as printed gives a mean and a limit in law, and starts paths from any site at height ≤ 0; §2.6 gets the probability from the mean alone and settles the convention | no disagreement; a link only this audit examined. Small gap, filled |
| probability claim 8 (block comparisons need seeding at near-maximal speed) | "read, correct" | the arithmetic is correct for equal blocks on a brick lattice made independent by disjoint noise cones; the claim list says "any block comparison with conditionally independent blocks" | both on the mathematics. The claim list's wording is wider than the proof; the journal's own text carries the restriction |
| OP₅(½): steps of ln τ against Proposition F's 0.4812 | "below 0.4812 from L = 10" | "from L = 11 on" | same numbers (step 9 → 10 is 0.4850, step 10 → 11 is 0.4701); by the critic's own table the first step below the bound ends at L = 11 |
| test of Theorem L | a coupling with W_t ⊆ Z_t found by linear programming at each t ≤ 8, ring of 6, a drive from an Ising ring coupled to the row's parity | P(edge meets C at t) ≥ P(OP₅(p) meets C at t) for every set C and t ≤ 6, ring of 6, a Gibbs drive depending on the row, p = 0.4047 (A4) | consistent; two different tests of the same statement |

I found no verdict of the critic's on these two lines that I think is wrong.

## C3. Probability claim 13, written out

**Statement.** E₁(π) on Z_L with p = min(π₀, π₂) > 0. Let φ ≥ 0 be a function of the row in a window of radius
R, with φ(all dead) = 0 and φ ≢ 0; Φ(S) = Σ_y φ(S near y); 0 < r < 1; g = r^Φ. Then there are ε₀ > 0 and L₁, depending
on φ, r and π only, such that for every L ≥ L₁, every a ≤ 1 and every ε < ε₀ the inequality of Lemma 3,
d(S) + Σ_{S′ ≠ ∅} Q(S, S′)g(S′) ≤ a·g(S) + ε, fails at some living S. In particular it fails with ε = e^{−cL} for L
large, which is the claim. (If φ ≡ 0 then g ≡ 1 and the inequality reads 1 ≤ a + ε.)

*Proof.* (1) Because Φ(∅) = 0, the left side is E_S g(S₁) =: (Pg)(S), P the kernel with ∅ absorbing. If the
inequality holds at every living state with a ≤ 1, then Pg ≤ g + ε everywhere (at ∅ both are 1), so
P³g ≤ Pg + 2ε ≤ a·g + 3ε at every living state. (2) By Jensen E_S g(S₃) ≥ r^{E_S Φ(S₃)}.
(3) Let m(ℓ) be the largest Φ of a set inside an arc of ℓ cells of Z. Two sets at distance > 2R have additive
Φ, so ℓ ↦ m(ℓ − 2R) is superadditive; by Fekete's lemma m(ℓ − 2R)/ℓ tends to its supremum φ* > 0. Hence
m(ℓ) ≤ φ*(ℓ + 2R) for every ℓ, and m(ℓ)/ℓ → φ*.
(4) Let S lie in an arc J of n cells and L ≥ n + 2R + 13. Then S₃ lies in J ⊕ [−6, 6], which has n + 12 cells; cut
it into N = ⌊(n + 12)/(2R + 1)⌋ disjoint arcs I_i of 2R + 1 cells and a remainder. If K is the set of i with
S₃ ∩ I_i = ∅, the rest of S₃ lies in at most |K| + 1 arcs, pairwise at distance > 2R, of total length
n + 12 − (2R + 1)|K|, so by (3) Φ(S₃) ≤ φ*(n + 12 + 2R − |K|). By Lemma 5 (claim 17) each I_i is empty at time 3
with probability ≥ q := p^{6R+15}, whatever S is. Taking expectations (no independence is needed):
E_S Φ(S₃) ≤ φ*(n + 12 + 2R − qN) =: U(n).
(5) Choose S in J with Φ(S) = m(n). Since m(n)/n → φ* and U(n) ≤ φ*n(1 − q/(2R + 1)) + const, there is n₁ with
U(n₁) ≤ m(n₁) − 1. For L ≥ L₁ := n₁ + 2R + 13, (1), (2) and (4) give
3ε ≥ r^{U(n₁)} − a·r^{m(n₁)} ≥ r^{m(n₁)−1}(1 − r) =: 3ε₀. ∎

The same proof with one generation in place of three (an arc of m cells is empty next with probability
≥ (1 − p)^m) gives the statement for OP₅(p), p < 1, a monotone model whose long life at densities near 1 is
classical: the obstruction is in the form of g, not in the model.

*Check* (`python3 a10_claim13.py`, 20 s; exact, every state, L = 8, 10, …, 16; anchor and Bin(2, 0.472); healths
|S|, |S ⊕ [−2,2]| and the number of live cells with one to three live neighbours; r = 0.3, 0.6, 0.9; a = 0.5, 0.9, 0.99,
1). With ε*(L) the smallest ε for which the inequality holds at every living state: ε* ≥ 1 − λ_L whenever
a + ε* < 1 (Lemma 3 itself); max_S [E_S g(S₃) − a·g(S)] ≤ 3ε* (step (1)); ε* is constant from L = 12 on in 31 of the
72 cases and at least 55 times 1 − λ₁₆ in all. For a droplet S (the pattern 1 or 11110 on n ≤ 400 cells, dead
elsewhere) E_S g(S₁) − a·g(S) is a floor under ε*(L) for every L ≥ n + 9, computed by a transfer matrix (checked
against the kernel at L = 16). The best such floor is positive in all 72 cases, between 1.5×10⁻⁸ and 0.31, at
droplets of 3 to 71 cells; one generation already suffices on this grid.

## C4. What each of us has that the other has not

Only in this audit: the unconditional comparison of eigenvalues (Theorem U.4, end of §2.5); the lemma of §2.6; why
the two-parent route stops at even L (§2.8); the second route to F1 with its exact test (§3.2(b), A6); the
three-move strategy checked for every state up to L = 16 and the automaton enumerated at L = 6 and 8 (A2, A3);
§4 on what "deterministic" means here.
Only with the critic, and not audited here: the anchor and OP₅(½) on intervals (steps 0.6236 and 0.3815), every
table for independent rows, the tables of how the row dies, the coupling test by linear programming, the
4 × 6 strip. Nothing in parts A or B depends on them.

---

# Not checked

- **The primary sources.** Balister–Bollobás–Stacey 1994; Liggett 1995 (Project Euclid refuses automated
  clients: not obtained); Bezuidenhout–Grimmett 1990; Liggett's 1999 book. F1 and F2 are taken as the library's
  note and three arXiv papers print them (Hartarsky–Szabó v1, v3; Ráth–Valesin v3; Köhler-Schindler–Sulser v1).
  I did not re-read Holmes–Salisbury or Gomes–Pereira.
- **The proof of F2.** I read the corollary and the sketch, not the theorems it rests on (4.2, 4.3, 4.7 of
  Hartarsky–Szabó).
- **Liggett's inequality for all finite A.** Tested exactly for A ⊆ {0, …, 6} at p = ¾ only.
- **Large L.** Everything exact is for L ≤ 18 (chain), K ≤ 20 (percolation), L ≤ 16 (exhaustive strategy checks).
  Eigenvalues are in double precision, bracketed by Collatz–Wielandt ratios; the exhaustive checks of §2.1 and
  the Liggett test are exact.
- **Intervals.** Nothing about 𝒜 with dead or reflecting ends, beyond Lemma 6 and Proposition W(a), (b).
- **The constant c.** No explicit value was derived.
- **Theorems H and U's hypotheses; the cube lemma in general; g = 2 on gump faces; claim 8 of the probability
  line beyond a reading.** See part B.
- **The critic's computations that have no counterpart here** (§C4): the anchor and OP₅(½) on intervals, every
  table for independent rows (D2), the coupling test of Theorem L by linear programming, the 4 × 6 strip.
  Remark (d) of Theorem L (the lag-k form) has been checked by nobody.
- **The exam entries** (`swarm/PREDICTIONS.md`, `swarm/exam/`): not read.
- **The measured facts** quoted in §4 (0.36–0.42 for the 2D rule; statistics of the rule's bulk): taken from
  `PROBLEM.md` and the journals, not re-measured.
