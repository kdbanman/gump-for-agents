# counting: claims (current list)

Updated 2026-11-13, end of round 1. Proofs are in `journal.md` at the entry named. "Smallest case" is worked by
hand there unless a lab check is named. Notation: journal entry 1.

| # | claim | tag | where | smallest case |
|---|---|---|---|---|
| 1 | For a map preserving μ: μ(T_H ≤ k) ≤ (k+1) μ(H). For a bijection, mean of T_H over the cycles that meet H ≥ \|X′\|/(2\|H\|) − 1/2 (X′ = their union); the form with \|X\| needs every cycle to meet H | **proved** | entry 2 | rotation of Z_n, H = {0}: mean (n−1)/2, equality |
| 2 | The second-order lift (u, v) ↦ (v, f(v) ⊕ u) of gump or the 2D rule is a bijection confined to the same hulls; "face empty now" has frequency exactly 2^{−A}; no state enters {face empty twice running}. A face of an invertible relative never dies | **proved** | entry 3 | one isolated cell: (1,0) ↔ (0,1) for ever |
| 3 | From the uniform soup, D_k = λ(T ≤ k) = \|f^{−k}(H)\|/\|X\|: the death-time law is the count of the trapdoor's k-th ancestors; empty-face states have e^{(ln 2 − c)A} times the average number of ancestors | **proved** (identity) | entries 1, 3 | — |
| 4 | 2D rule, strip with ≥ 2k+1 rows: D_k(L) = tr(M_k^L)/2^{(2k+1)L} ≤ m_k e^{−c_k L}; c_k = (2k+1) ln 2 − ln ρ(M_k) is also the exact decay rate of empty windows of the infinite edge at generation k | **proved** | entry 4 | k = 1, L = 5: 2507 of 32,768 states (lab check requested) |
| 5 | 0 < c_{k+1} ≤ c_k ≤ c_1 < ln 2; c_∞ = lim c_k exists | **proved** | entry 4 | c_1: 16 × 16 matrix, table of w(s, k) |
| 6 | 0.273 ≤ c_1 ≤ 0.562 | **proved** (hand arithmetic; exact value requested) | entry 4 | — |
| 7 | Gump slab face, fixed k: e^{−A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A}, c⁻_k > 0 | **proved** | entry 4 | k = 0 trivial; guard = one top cube |
| 8 | Box edge (free ends): λ(T ≤ k) = [M_k^{L+4k}]_{00}/2^{(2k+1)L}, exponent c⁰_k ≥ c_k | **proved** | entry 5(a) | L = 1, k = 1: 7 of 8 |
| 9 | Mirror through the edge: exponent ≥ c_k/2 (ring); same for the D4 box | **proved** | entry 5(b) | — |
| 10 | C4 or one diagonal mirror (box): exponent exactly c⁰_k, as without symmetry | **proved** | entry 5(c) | — |
| 11 | Equality c⁰_k = c_k and "mirror = exactly half" | **sketched**: needs the all-dead window in a dominant class of M_k; argument for k = 1 given, finite check requested; nothing for k ≥ 2 | entry 5(d) | cap …1111 0 1 00 |
| 12 | Under a G-symmetric soup, a set whose k-generation dependence cone meets each G-orbit at most once has the same law as under the free soup; in a C4 box nothing differs before age ≈ L/8 away from the corners | **proved** | entry 5(e) | — |
| 13 | Gump: the cells beneath a face layer split cube by cube (three shared in a 6-cycle, three private); 40 of the 64 triples (b_u, b_v, b_w) are achievable; a slab-face configuration can be emptied in one generation iff every top cube's kill sets meet that set; λ(T ≤ 1) = 2^{−A} Σ_S Π_q W_q(S) | **proved** | entry 6 | the critic's counterexample: K = {3} and K = {0} in one cube |
| 14 | A full gump face dies in one generation whatever lies beneath | **proved** | entry 6 | k = 6 ⇒ n ≥ 6 |
| 15 | μ(Y₁) ≤ (\|Y₁\| Σ_u μ(u)²)^{1/2}: if two independent soups agree on the top three rows at generation j with probability ≤ 2^{−3L} e^{(c_1−δ)L}, then λ(T = j+1) ≤ m_1^{1/2} e^{−δL/2} | **proved** (Cauchy–Schwarz); the hypothesis is untested | entry 7 | — |
| 16 | No finite still pattern of the half-plane keeps its cells' states against an arbitrary outside | **proved** (furthest cell) | entry 7 | one cell: 4 free neighbours |
| C1 | The measured exponent of each geometry is lim_k c_k of that geometry | **guessed**; three of its four consequences for the 2D rule are contradicted by measured slopes at L ≤ 36–56 (0.28 / 0.34 / 0.41) | entries 5, 7 | — |
| C2 | c_∞ > 0 | **guessed**; I believe it is out of reach of counting alone | entry 7 | — |

Not claimed: any lower bound e^{cL} on a lifetime; any statement about the board's τ that does not go through C1.
