# counting: claims (current list)

Updated 2026-11-13, end of round 2. Proofs are in `journal.md` at the entry named. "Smallest case" is worked by
hand there unless a lab check is named. Notation: journal entry 1. "Checked" = by the critic (`critic/to-counting.md`).

## Standing

| # | claim | tag | where | smallest case |
|---|---|---|---|---|
| 1 | For a map preserving μ: μ(T_H ≤ k) ≤ (k+1) μ(H). For a bijection, mean of T_H over the cycles that meet H ≥ \|X′\|/(2\|H\|) − 1/2; the form with \|X\| needs every cycle to meet H | **proved**, checked | entry 2 | rotation of Z_n, H = {0}: mean (n−1)/2 |
| 2 | The second-order lift (u, v) ↦ (v, f(v) ⊕ u) is a bijection confined to the same hulls; "face empty now" has frequency exactly 2^{−A}; a face of an invertible relative never dies | **proved**, checked on every pair-state of two vessels | entry 3 | one isolated cell |
| 3 | From the uniform soup, λ(T ≤ k) = \|f^{−k}(H)\|/\|X\|: the death-time law is the count of the trapdoor's k-th ancestors | **proved** (identity) | entries 1, 3 | — |
| 4 | 2D rule, strip with ≥ 2k+1 rows: λ(T ≤ k) = tr(M_k^L)/2^{(2k+1)L} ≤ m_k e^{−c_k L}; c_k is also the exact decay rate of empty windows of the infinite edge at generation k; 0 < c_{k+1} ≤ c_k < ln 2 | **proved**, checked | entry 4 | k = 1, L = 5: 2507 of 32,768 (lab: confirmed) |
| 5 | **c_1 = 0.551535, c_2 = 0.467693** (density ½); 0.489963, 0.4671 at density 0.472 | computed by the lab from claim 4; checked against every state of strips 3 × 5…8 and 5 × 4, 5 × 5 | entry 9 | — |
| 6 | Gump slab face, fixed k: e^{−A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A}, c⁻_k > 0 (lone-cube guard) | **proved**, read | entry 4 | — |
| 7 | Box edge (free ends): λ(T ≤ k) = [M_k^{L+4k}]_{00}/2^{(2k+1)L}, exponent c⁰_k ≥ c_k; **c⁰_k = c_k for k = 1, 2** (lab: the class of the all-dead window is dominant) | **proved**; equality checked for k = 1, 2, open for k ≥ 3 | entries 5(a), 9 | L = 1, k = 1: 7 of 8; boxes 3 × 5…7 |
| 8 | Mirror through the edge: fixed-age exponent ≥ c_k/2; C4 or one diagonal mirror: exactly c⁰_k; no symmetry inside a light cone | **proved**; (c) checked on the C4 box 7 × 7 | entry 5(b), (c), (e) | 502 of 8,192 |
| 9 | "Mirror = exactly half" at a fixed age | **sketched** (needs a palindromic connecting word in a dominant class; not checked) | entry 5(d) | — |
| 10 | Gump: the six cells beneath a top cube's triangle are its own (three shared in a 6-cycle, three private); 40 of 64 triples (b_u, b_v, b_w) achievable; one-generation emptiability is decided cube by cube; λ(T ≤ 1) = 2^{−A} Σ_S Π_q W_q(S) | **proved**, checked (SAT on two periodic faces) | entries 6, 8 | the critic's counterexample |
| 11 | With the layers beneath empty a gump face dies iff every live cell has k ≤ 2 or k = 6 and every dead cell k ≤ 3 or k = 6; a full face always dies | **proved** (corrected in entry 8) | entries 6, 8 | — |
| 12 | Gaps persist: a window of ℓ + 4j dead edge cells at generation k leaves its middle ℓ dead at generation k + j, whatever lies beneath; q_{k+j}(ℓ) ≥ q_k(ℓ + 4j) | **proved** | entry 10 | ℓ = 1, j = 1: 00000 → ··0·· |
| 13 | The fixed-age exponent depends on the soup: c_k(p) ≤ −ln(1 − p) for every k | **proved** | entry 10 | k = 0 |
| 14 | At a fixed age the true rule is a dice model: D2(L, ½; w) from a uniform start has the true rule's λ(T ≤ k) for w ≥ 2k − 1 | **proved** | entry 10 | k = 1, w = 1 |
| 15 | Uniform soup: given the edge cell's state s at generation 0, the two cells beneath it are alive at generation 1 with probabilities 85/128, 161/256 (s = 0) and 76/128, 119/256 (s = 1) | **proved** (hand count) | entry 11 | — |
| 16 | Gump face over independent cells of density ρ: a lone cell leaves the face empty next with probability (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴; a lone triangle with probability (1 − ρ)⁶(1 − 2ρ³ + ρ⁵)⁶ (it dies iff all six cells beneath its cube are dead) | **proved**; lab check requested | entry 12 | ρ = ½: 45 of 64 states beneath the cube |
| 17 | μ(Y₁) ≤ (\|Y₁\| Σ_u μ(u)²)^{1/2} | **proved**; **its hypothesis is false** in every vessel enumerated and cannot hold for a global Rényi entropy (atoms) | entries 7, 8 | — |
| 18 | No finite still pattern of the half-plane keeps its cells' states against an arbitrary outside | **proved**, read | entry 7 | one cell |

## Guessed

| # | claim | status |
|---|---|---|
| C1′ | If the hazard at ages ≥ j₀ is e^{−γL+o(L)} uniformly in L, then c_∞(π) ≤ γ for every soup π, with equality when the soup's first generations offer no cheaper route; density ½ is a candidate for equality in the 2D rule | **guessed**; test requested on D2, where both sides are exact (round 2, request 1) |
| C2 | c_∞(½) > 0 | **guessed**; out of reach of counting (entries 7, 10) |

## Withdrawn

- **C1** (the measured exponent of each geometry is lim_k c_k): the limit depends on the soup (claim 13) and the
  two orders of limit differ for a stated reason (claim 12). Entry 10.
- The comparison of claim 8 with the measured slopes of rings, boxes and C4 boxes (entry 5, last part): rested on C1.
- The collision-entropy hypothesis of claim 17 (entry 8).

Not claimed: any lower bound e^{cL} on a lifetime; any statement about the board's τ.
