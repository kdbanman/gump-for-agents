# counting: claims (current list)

Updated 2026-11-14, end of round 3 (the line's closing round). Proofs are in `journal.md` at the entry named.
"Smallest case" is worked by hand there unless a lab check is named. Notation: journal entry 1.
"Checked" = by the critic (`critic/to-counting.md`, replies to rounds 1 and 2). Claims 19–24 are new and unchecked.

## Standing

| # | claim | tag | where | smallest case |
|---|---|---|---|---|
| 1 | For a map preserving μ: μ(T_H ≤ k) ≤ (k+1) μ(H). For a bijection, mean of T_H over the cycles that meet H ≥ \|X′\|/(2\|H\|) − 1/2; the form with \|X\| needs every cycle to meet H | **proved**, checked | entry 2 | rotation of Z_n, H = {0}: mean (n−1)/2 |
| 2 | The second-order lift (u, v) ↦ (v, f(v) ⊕ u) is a bijection confined to the same hulls; "face empty now" has frequency exactly 2^{−A}; a face of an invertible relative never dies | **proved**, checked on every pair-state of two vessels | entry 3 | one isolated cell |
| 3 | From the uniform soup, λ(T ≤ k) = \|f^{−k}(H)\|/\|X\|: the death-time law is the count of the trapdoor's k-th ancestors | **proved** (identity) | entries 1, 3 | — |
| 4 | 2D rule, strip with ≥ 2k+1 rows: λ(T ≤ k) = tr(M_k^L)/2^{(2k+1)L} ≤ m_k e^{−c_k L}; c_k is also the exact decay rate of empty windows of the infinite edge at generation k; 0 < c_{k+1} ≤ c_k < ln 2 | **proved**, checked | entry 4 | k = 1, L = 5: 2507 of 32,768 (lab: confirmed) |
| 5 | **c_1 = 0.551535, c_2 = 0.467693** (density ½); 0.489963, 0.4671 at density 0.472. **c_3 = 0.36 ± 0.01** (sampled by the examiner: slope 0.3676 ± 0.0006 at L = 20–32) | computed by the lab from claim 4 (c_1, c_2), checked on every state of small strips; c_3 measured | entries 9, 13 | — |
| 6 | Gump slab face, fixed k: e^{−A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A}, c⁻_k > 0 (lone-cube guard). Same for a face12e wall with 3A ln 2 on the left | **proved**, read (gump); face12e unchecked | entries 4, 14 | — |
| 7 | Box edge (free ends): λ(T ≤ k) = [M_k^{L+4k}]_{00}/2^{(2k+1)L}, exponent c⁰_k ≥ c_k; **c⁰_k = c_k for k = 1, 2** | **proved**; equality checked for k = 1, 2, open for k ≥ 3 | entries 5(a), 9 | L = 1, k = 1: 7 of 8; boxes 3 × 5…7 |
| 8 | Mirror through the edge: fixed-age exponent ≥ c_k/2; C4 or one diagonal mirror: exactly c⁰_k; no symmetry inside a light cone | **proved**; (c) checked on the C4 box 7 × 7 | entry 5(b), (c), (e) | 502 of 8,192 |
| 9 | "Mirror = exactly half" at a fixed age | **sketched** (needs a palindromic connecting word in a dominant class); not worth finishing | entry 5(d) | — |
| 10 | Gump: the six cells beneath a top cube's triangle are its own (three shared in a 6-cycle, three private); 40 of 64 triples (b_u, b_v, b_w) achievable; one-generation emptiability is decided cube by cube; λ(T ≤ 1) = 2^{−A} Σ_S Π_q W_q(S) | **proved**, checked (SAT on two periodic faces; the probability form on every state of three slabs) | entries 6, 8 | the critic's counterexample |
| 11 | With the layers beneath empty a gump face dies iff every live cell has k ≤ 2 or k = 6 and every dead cell k ≤ 3 or k = 6; a full face always dies | **proved** (corrected in entry 8), checked | entries 6, 8 | — |
| 12 | Gaps persist: a window of ℓ + 4j dead edge cells at generation k leaves its middle ℓ dead at generation k + j, whatever lies beneath; q_{k+j}(ℓ) ≥ q_k(ℓ + 4j) | **proved**, checked | entry 10 | ℓ = 1, j = 1: 00000 → ··0·· |
| 13 | The fixed-age exponent depends on the soup: c_k(p) ≤ −ln(1 − p) for every k | **proved**, checked | entry 10 | k = 0 |
| 14 | At a fixed age the true rule is a dice model: D2(L, ½; w) from a uniform start has the true rule's λ(T ≤ k) for w ≥ 2k − 1 | **proved**, checked (k = 1 numerically, k ≥ 2 by the argument) | entry 10 | k = 1, w = 1 |
| 15 | Uniform soup: given the edge cell's state s at generation 0, the two cells beneath it are alive at generation 1 with probabilities 85/128, 161/256 (s = 0) and 76/128, 119/256 (s = 1) | **proved**, checked by enumeration | entry 11 | — |
| 16 | Gump face over independent cells of density ρ: a lone cell leaves the face empty next with probability (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴; a lone triangle with probability (1 − ρ)⁶(1 − 2ρ³ + ρ⁵)⁶ | **proved**, checked on the true rule (0.412159, 0.003553 at ½) | entry 12 | ρ = ½: 45 of 64 states beneath the cube |
| 17 | μ(Y₁) ≤ (\|Y₁\| Σ_u μ(u)²)^{1/2} | **proved**; **its hypothesis is false** in every vessel enumerated and cannot hold for a global Rényi entropy (atoms) | entries 7, 8 | — |
| 18 | No finite still pattern of the half-plane keeps its cells' states against an arbitrary outside | **proved**, checked | entry 7 | one cell |
| 19 | Lemma 8, any finite absorbing chain: P_π(T ≤ k) ≤ (1 − λ^k) π(φ) + π(1 − φ) ≤ k h + π(1 − φ), φ the Perron vector with max 1. Hence for dice chains c_∞(π) ≥ min(γ⁻, θ⁻(π)): a fixed-age exponent below the steady one means doomed starts are cheaper; a fixed-age exponent below the cost of doomed starts is an upper bound on the steady one | **proved**; unchecked | entry 13 | two living states, one doomed: equality |
| 20 | Lemma 2′: if g preserves μ and g(H) ⊆ H then μ-almost no point outside H enters H. No relative with an invariant measure charging the living states has a face that dies | **proved**; unchecked | entry 16 | doubling map, H = {0} |
| 21 | face12e wall (Proposition F): the band {sheet, layer beneath} is the absorbing set; the sheet reads only the band; over an empty layer the sheet follows a monotone threshold map and on a box wall n × n is gone in n steps; over an empty sheet the layer follows gump's rule on counts 6 + 2 + 1; on {sheet empty, no cube with four live sides} the band's death is the layer's | **proved** (read off the offsets); unchecked | entry 14 | lone closed cube (still life) |
| 22 | face12e (Proposition G): λ(T ≤ 1) is a vertex model on the lattice of top cubes; one-generation emptiability is 2-SAT there, not cube-local; in the configuration Π₁ (wall n × 4) exactly 32^n(8^n + 2·6^n + 5^n) patterns beneath empty the band and all have the n bottoms of one row equal | **proved** by hand; lab check requested | entry 14 | n = 3: 35,028,992 of 2³⁶ |
| 23 | face12e, sheet empty, one live cell in the layer, independent cells beneath (bottoms ρ_β, private ρ_r): P(band empty next) is the ladder polynomial of entry 14; 3793/8192 = 0.4630 at ½ (gump 0.4122) | **proved** by hand; lab check requested | entry 14 | — |
| 24 | O_h faces: cube-centred (R = 2N+1) and vertex-centred (R = 2N+2) faces have the same area 3T_{N+1}, the same number (A + 3m)/6 of C3v-orbits, m = ⌊N/2⌋+1, the same numbers of in-layer adjacencies; they differ in which triangle orientation tiles them and in the rim (vertex-centred: 3(N+1) rim cells alone in their top cube; shared with a neighbouring face: N+1 against 2(N+1)). The vertex factor is not a count of independent cells | **proved** by hand count; lab check requested | entry 15 | N = 1, both faces written out |

## Guessed

| # | claim | status |
|---|---|---|
| C2 | c_∞(½) > 0 for the 2D rule | **guessed**; out of reach of counting (entries 7, 10); no evidence either way (c_3 ≈ 0.36, decrements 0.084, 0.10–0.11 not shrinking) |

## Withdrawn or failed

- **C1** (the measured exponent of each geometry is lim_k c_k): the limit depends on the soup (claim 13) and the
  two orders of limit differ for a stated reason (claim 12). Entry 10.
- **C1′** (c_∞(π) ≤ γ under a uniform hazard from a fixed age; equality for soups with no cheaper early route;
  density ½ a candidate in the 2D rule): the hypothesis fails exactly in D2 for fair and sparse soups (lab L7) and,
  by the exam, in the true rule at L ≤ 32 (age-2 hazard 5–11 times the steady one, growing like e^{0.06L}); c_3 is
  already below the steady slope of the same rings. What is true is claim 19. Entry 13.
- **Exam entry C-E2** (c_3 = 0.447 ± 0.012): **failed**, 0.3676 ± 0.0006. Its theorem part (c_3 ≤ c_2) holds. Entry 13.
- The comparison of claim 8 with the measured slopes of rings, boxes and C4 boxes (entry 5, last part): rested on C1.
- The collision-entropy hypothesis of claim 17 (entry 8).
- The sign of the crude count in entry 11 (lab: the own-column feedback makes dying by generation 2 cheaper, by 0.003).

## Exam entries

- C-E1, revised (one mirror on gump hulls: slope 0.105 ± 0.009 between A = 84 and 135): not run when this was
  written. No theorem of this line reaches it.
- C-E2: failed (above).
- C-E3 (face12e: a wall with empty sheet and one live cell beneath is dead next generation with probability
  0.44 ± 0.05): filed 2026-11-14. Rests on claim 23 and on the reading of entry 12 that cells beneath a dying
  face act like fair dice.

Not claimed: any lower bound e^{cL} on a lifetime; any statement about the board's τ; any formula for γ.
The line is closed (journal, closing report).
