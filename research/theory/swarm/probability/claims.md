# Probability line: claims (current list, after round 3, 2026-11-14)

Models. **E₁(π)**: the edge row of the 2D rule on Z_L (or on an interval) driven by i.i.d. b ∈ {0,1,2} with law π
(journal, entry 1); D2 is π = Bin(2, ρ); the anchor is (½, 0, ½). **OP₅(p)**: five-parent oriented site
percolation; p₅ its critical density. **F(π)**: a gump face driven by i.i.d. b ∈ {0,1,2,3} (entry 13).
τ = 1/(1 − λ) = quasi-stationary mean lifetime. Tags: **proved** (proof in journal), **sketched**, **guessed**.
Outside facts used (library, `notes/oriented-percolation.md`): (P1) Hartarsky–Szabó Cor. 4.8, finite-volume
survival on cylinders for any finite set of parents (printed, proof sketched there); (P3) p_c^site ≤ 0.7491
(Balister–Bollobás–Stacey, second-hand, computer-assisted).

| # | claim | tag | smallest case by hand | journal |
|---|---|---|---|---|
| 1 | Given S_t the cells of S_{t+1} are independent with probabilities a(x, k): live π₂, π₁+π₂, 1, π₀+π₁, π₀; dead 0, π₂, π₁+π₂, π₀+π₁, π₀ (k = 0…4) | proved | (x, k) = (1, 4): alive iff b = 0 | entry 1 |
| 2 | Ring, π₀, π₂ > 0: chain on non-empty states irreducible, aperiodic; E_S T ≤ 3p^{−3L}, p = min(π₀, π₂); if P_full(T > t) ≥ ½ then τ_L ≥ (t + ⌈L/4⌉)/(L⌈L/4⌉ ln(1/p) + ln 2) | proved | full ring → full ring has probability π₀^L | entry 1 |
| 3 | Lemma 1: the sharp one-step attractive minorant has rates (y ∈ η: s, m, π₀, π₀ for j = 0, 1, 2, ≥ 3; y ∉ η: 0, s, m, π₀), s = min(π₀, π₂), m = min(π₀, 1 − π₀); coupling η_t ⊆ S_t; S dominates OP₅(s) | proved | S = {0}: five cells at rate π₂ = one step of OP₅(π₂) | entry 2 |
| 4 | s ≤ ½ for every π (≤ ¼ for independent rows); no *one-step* worst-case comparison for ≥ 2 deterministic rows or a gump face (the all-alive state dies surely). For a gump face a two-generation one exists: claim 19 | proved | two-row slab all alive: every cell has n ≥ 5 | entries 2, 13 |
| 5 | Theorem A (form of entry 11): (i) for min(π₀, π₂) > p₅: e^{cL} ≤ τ_L ≤ 3p^{−3L}, every L ≥ L₀, odd or even; (ii) 1/3 ≤ p₅ ≤ 1 − (1 − p_c^site)^{1/2}; (iii) the set in (i) is non-empty iff p₅ < ½, which holds if p_c^site < 3/4 | (i), (ii) proved modulo (P1); non-emptiness modulo (P3) | L = 6, S₀ = {0}: child blocks {1, 2}, {5, 0} within distance 2 of cell 0 | entries 3, 11 |
| 6 | Lemma 2(a): OP₅(p) dies out for p < 1/3 | proved | right end moves by 2 − X, E X = (1−p)/p | entry 4 |
| 7 | Lemma 2(b): for Bin(2, ρ), ρ ≥ 0.46, the sharp one-step minorant contracts Φ = \|η ⊕ [−2,2]\| by κ < 1 per generation (0.948 at ρ = 0.472): no one-step comparison proves the law for independent rows | proved | η = {0}, ρ = 0.472: E Φ′ = 4.285 < 5 | entry 4 |
| 8 | Any block comparison with conditionally independent blocks over n ≥ 2 generations needs seeding over ≥ 2n − 3 cells in n generations | proved (geometry only) | n = 1: blocks of 2, spacing 2 | entry 4 |
| 9 | T1: a multi-generation criterion for E₁(π) away from the anchor | open; no route by hand | — | entry 7 |
| 10 | T2a dead = reflecting exponent; T2b ring ≤ interval; T2c interval ≤ ring | guessed. T2b: evidence at L ≤ 34 is against it having set in (round 3 report) | — | entries 5, 8, 12 |
| 11 | Theorem A′: (i) of claim 5 for the edge over *any* field b with conditional weight ≥ p at b = 0 and at b = 2 given everything else, p > p₅ | proved modulo (P1) | every alive-set of b contains 0 or 2 | entries 6, 11 |
| 12 | Lemma 3: 0 ≤ g ≤ 1 and d + Qg ≤ ag + ε at every living state, a + ε < 1 ⇒ τ ≥ 1/ε | proved | g = indicator of a bad set fails for E₁ | entry 7 |
| 13 | No certificate of Lemma 3 has the form r^{Φ}, Φ a sum of local non-negative terms (E₁ with π₀, π₂ > 0; also OP₅) | proved (the local game is now Lemma 5) | full arc of n cells: bulk loses health ∝ n, ends gain O(1) | entries 7, 12 |
| 14 | Proposition W: Q_ring = w·Q_dead on rows with cells 1–4 dead, w ≥ w_min = [π₀(1−π₂)]²; h_ring(L) ≥ w_min^{n+1}·P^d_ν(T_d = n+1); m_G ≥ p^{24} − 3h_ring; under H(n, c): τ_ring(L) ≤ max(6p^{−24}, 4τ_dead(L−4)/(c p^{24} w_min^{n+1})); same for reflecting ends | proved; (c) only under H, which is not established for all L | S = {5}: w = (1−π₂)² | entries 8, 12 |
| 15 | Proposition F: τ_L(OP₅(p)) ≤ C·L·β*^L, β* = (p + √(p²+4pq))/(2q); ln β*(½) = 0.4812. An upper bound only: the exact interval exponent of OP₅(½) is 0.380 (lab R5) | proved | p = ½: (β−1)(β²−β−1) = 0 | entry 9 |
| 16 | In monotone models τ_dead ≤ τ_ring at equal length; in D2 the exact tables have the opposite order at every L ≤ 19 | proved (first half); exact data (second) | — | entries 5, 10 |
| 17 | Lemma 5: for every state and every arc I of m ≤ L − 12 cells, P_S(S₃ ∩ I = ∅) ≥ p^{3m+12}, by dice on I ⊕ 4, I ⊕ 2, I only; hence μ(I empty) ≥ p^{3m+12} − 3h | proved | m = 1, S = {0}: nine prescribed dice | entry 12 (+ erratum in 15) |
| 18 | Lemma 6: on an interval of M ≥ 5 cells with dead ends (or reflecting ends) the chain on non-empty states is irreducible and aperiodic | proved | M = 5: full → {1,5} → {1} → {3} → {1,4} → anything | entry 15 |
| 19 | Lemma 4: a gump face over any field b with conditional weight ≥ s at 0, at 3, and ≥ s″ on {1,2}: i.i.d. marks K (prob. s), G (prob. σ = min(s, s″)); K ⇒ dead; the two-generation process η (G now, a K-neighbour one generation ago, a parent in η) lies below the face; E_S T ≤ s^{−A} | proved | S = {y₀}: seven cells, each alive iff b = 3 | entry 13 |
| 20 | Limits of claim 19: σ ≤ 1/3, site density ≤ 665/2187 = 0.3041; for independent cells beneath E\|η′\| ≤ (7/8)\|η\|; any block comparison of Theorem A's kind has density ≤ 19/27 = 0.7037, below every proved upper bound on p_c^site (and below its numerical value 0.7055) | proved | σ = ½ would give 7/8: the third class of dice is the obstacle | entry 14 |
| 21 | The process η of claim 19 at s = σ = 1/3 on a periodic face is supercritical (critical s ≈ 0.27) | guessed (exam P-E4) | — | entry 14 |

Not claimed: anything about D2 = E₁(Bin(2, ρ)) beyond upper bounds and Proposition W; a lifetime law for F(π) (it
would need claim 21 and a finite-volume theorem for a finitely dependent percolation on a kagome torus);
anything about the deterministic rule or gump.
