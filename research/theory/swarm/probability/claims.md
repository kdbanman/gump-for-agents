# Probability line: claims (current list)

Model: E₁(π), the edge row of the 2D rule on Z_L driven by i.i.d. b ∈ {0,1,2} with law π (journal, entry 1).
τ_L = 1/(1 − λ_L) = quasi-stationary mean lifetime; no immortal states when π₀, π₂ > 0.
Tags: **proved** (proof in journal), **sketched** (what is missing is said), **guessed**.

| # | claim | tag | smallest case by hand | journal |
|---|---|---|---|---|
| 1 | Given S_t the cells of S_{t+1} are independent with probabilities a(x, k): live π₂, π₁+π₂, 1, π₀+π₁, π₀; dead 0, π₂, π₁+π₂, π₀+π₁, π₀ (k = 0…4) | proved | (x, k) = (1, 4): alive iff b = 0 | entry 1 |
| 2 | For π₀, π₂ > 0: chain on non-empty states irreducible, aperiodic; E_S T ≤ 3p^{−3L} for all S, p = min(π₀, π₂); if P_full(T > t) ≥ ½ then τ_L ≥ (t + ⌈L/4⌉)/(L⌈L/4⌉ ln(1/p) + ln 2) | proved (uses theorems.md B(a), which the critic has read) | full ring → full ring has probability π₀^L | entry 1 |
| 3 | Lemma 1: the sharp one-step attractive minorant has rates (y ∈ η: s, m, π₀, π₀ for j = 0, 1, 2, ≥ 3; y ∉ η: 0, s, m, π₀), s = min(π₀, π₂), m = min(π₀, 1 − π₀); coupling η_t ⊆ S_t; S dominates OP₅(s) | proved | S = {0}: five cells at rate π₂ = one step of OP₅(π₂) | entry 2 |
| 4 | s ≤ ½ for every π (≤ ¼ for independent rows); no one-step worst-case comparison for ≥ 2 deterministic rows or a gump face (the all-alive state dies surely) | proved | two-row slab all alive: every cell has n ≥ 5 | entry 2 |
| 5 | Theorem A: if 1 − (1 − min(π₀, π₂))² > p_c^site then e^{cL} ≤ τ_L ≤ 3p^{−3L} (even L ≥ L₀). Non-empty region: contains (½, 0, ½) | proved modulo cited F1 (p_c^site ≤ 0.7491) and F2 (supercritical oriented percolation on a cylinder lives e^{cK}); odd L not written | L = 6, S₀ = {0}: child blocks {1, 2}, {5, 0} within distance 2 of cell 0 | entry 3 |
| 6 | Lemma 2(a): OP₅(p) dies out for p < 1/3; hence 1/3 ≤ p_c(OP₅) ≤ 0.4991 | proved (upper end uses F1) | right end moves by 2 − X, E X = (1−p)/p | entry 4 |
| 7 | Lemma 2(b): for Bin(2, ρ), ρ ≥ 0.46, the sharp minorant contracts Φ = \|η ⊕ [−2,2]\| by κ < 1 per generation (0.948 at ρ = 0.472): dies in O(log L). So no one-step comparison proves the law for independent rows | proved | η = {0}, ρ = 0.472: E Φ′ = 4.285 < 5 | entry 4 |
| 8 | Any block comparison with conditionally independent blocks over n ≥ 2 generations needs seeding over ≥ 2n − 3 cells in n generations | proved (geometry only) | n = 1: blocks of 2, spacing 2: the drifting pairs of Theorem A | entry 4 |
| 9 | T1: a multi-generation criterion for E₁(π). Its general form is Lemma 3 (claim 12); no certificate found; Durrett's comparison theorem needs a block event failing with probability < 6^{−36}, out of reach of exact computation | open | — | entry 7 |
| 10 | T2 split by the exact tables: T2a dead = reflecting exponent; T2b ring ≤ interval; T2c interval ≤ ring. T2b and "reflecting ≤ dead": conditional on H (claim 14). T2c and "dead ≤ reflecting": nothing | guessed (T2b: exam P-E1) | — | entries 5, 8 |
| 11 | Theorem A′: the lower bound of Theorem A for the edge over *any* field b with conditional weight ≥ p at b = 0 and at b = 2 given everything else (1 − (1−p)² > p_c^site); and Theorem A on min(π₀, π₂) > p_c(OP₅) ≥ 1/3 if F2 is granted for OP₅ | proved modulo F1, F2 | every alive-set of b contains 0 or 2: (live, 4) → {0}, (dead, 1) → {2} | entry 6 |
| 12 | Lemma 3: 0 ≤ g ≤ 1 and d + Qg ≤ ag + ε at every living state, a + ε < 1 ⇒ τ ≥ 1/ε | proved | g = indicator of a bad set fails for E₁ (a one-cell state) | entry 7 |
| 13 | No certificate of Lemma 3 has the form r^{Φ}, Φ a sum of local non-negative terms (E₁ with π₀, π₂ > 0; also OP₅) | proved up to the local three-move game (asserted) | full arc of n cells: bulk loses health ∝ n, ends gain O(1) | entry 7 |
| 14 | Proposition W: Q_ring = w·Q_dead on states with cells 1–4 dead, w ≥ [π₀(1−π₂)]²; h_ring(L) ≥ w_min^{n+1}·P^d_ν(T_d = n+1); under H(n, c): τ_ring(L) ≤ 2τ_dead(L−4)/(c·m_G·w_min^{n+1}); same for reflecting ends | proved ((a), (b), (d) unconditional; (c) under H, which is not established) | S = {5}: w = (1−π₂)² | entry 8 |
| 15 | Proposition F: τ_L(OP₅(p)) ≤ C·L·β*^L, β* = (p + √(p²+4pq))/(2q); ln β*(½) = 0.4812 | proved | p = ½: β²(2 − β) = 1 ⟺ (β−1)(β²−β−1) = 0 | entry 9 |
| 16 | In monotone models τ_dead ≤ τ_ring at equal length; in D2 the exact tables have the opposite order at every L ≤ 19 | proved (first half); exact data (second) | — | entries 5, 10 |

Not claimed: anything about E₁(Bin(2, 0.472)) beyond the upper bound; anything about the deterministic rule or gump.
