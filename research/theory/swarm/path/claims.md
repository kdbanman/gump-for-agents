# path: claims (final list; end of the closing round, 2026-11-14)

Tags: **proved** (proof in the journal; the critic's verdict in brackets), **sketched** (what is missing is said),
**conjecture**, **fell** (with the reason). A measured regularity is tagged conjecture and marked "measured".

Notation as in `journal.md`, entry 1: face F of A cells, in-face neighbours N_F, m cells beneath (3 gump, 2 toy),
θ = m + 1 the smallest birth count, n_t the face population, h the hazard among living unsettled replicas
(deaths / exposure). From entry 17 on: T̄ is the *pooled one-step table of the population in the living state*
(entry 8), M_k(s) = Σ_{k′} T̄(k, k′)e^{−s(k′ − k)} its row transform, θ_k the local root (largest s with M_k(s) ≤ 1), ψ* the
table's committor. Entries 22–24: continuations c₀ ("rows 1–4 as tallied, stretched with the face") and c₁
("clusters": the root of row 5 down to zero); Φ, C⁺ (23.2); admissible W, W°, W_J, good rows (24.1–24.2); (E),
(R_ε) (24.3); R⁺, B⁺ (23.2, 24.4). "Lab Lx.y" = the board's lab table.

| id | claim | tag | where | smallest case worked by hand |
|---|---|---|---|---|
| L1 | Rim lemma: if a set D of face cells is dead at t, every cell of D all of whose in-face neighbours are in D is dead at t + 1, whatever lies beneath. So (a) the live set of a face spreads at in-face speed ≤ 1 (hence a row of the population's table from n charges at most 7n + 1 values), (b) a hole of in-radius ρ keeps its centre dead for ρ generations, (c) a one-step death is one constraint for each cell of N_F[supp ξ]; by the cube lemma the constraints couple only inside cube triples | **proved** (confirmed, round 1; (c) reworded in entry 7) | entries 2, 7 | gump, one live interior cell: n_{t+1} ≤ 7; the face dies iff each of seven triples beneath contains a dead cell |
| L1′ | Rim lemma for any sealed set W: a dead cell of W all of whose neighbours in W are dead stays dead | **proved** (confirmed; enumerated on three small vessels) | entry 9 | middle layer of a three-layer band: 10 neighbours in the band, 2 outside |
| S | The skeleton K(t) is the union of the sealed sets that have gone extinct; the first permanent loss is the extinction of an inclusion-minimal sealed set, and needs all its cells dead at one time | **proved** (confirmed; enumerated) | entry 9 | a hull: the face (smallest sealed set, exact R ≤ 10, critic) |
| F | face12e, slab with a periodic wall, at least two cubes deep: the wall's sheet Σ plus the layer Λ beneath it is sealed and inclusion-minimal; Σ alone and Λ alone are not sealed; only the cells of Λ have neighbours in the rest of the vessel (3 each) | **proved** (confirmed by integer programme; the lab added: it is the smallest sealed set iff 3·max(N, M) ≤ 5D + 2, L12.8) | entry 20 | a Λ cell: 6 + 2 + 2 + 1 + 1 (in Λ, in Σ, next sheet, next layer, outside) |
| L3 | Sealed ⟺ complement closed under θ-bootstrap percolation; V \ K(t) = bootstrap closure of the live set | **proved** (confirmed) | entry 4 | kagome hexagon ring |
| L4, 4a | Top-layer rigidity; a d-deep top cell of a sealed set drags in its whole deep sheet and what lies under it | **proved** (confirmed) | entries 4, 12 | hull minus its two outer d-layers; a T3 band |
| R5 | The sealed-set facts do not imply the law: B45/S34, B45/S35, B45/S45, B4/S345 share gump's graph and θ = 4 (so every sealed-set statement and its converse), are chaotic on a torus, and have median hull lifetimes 20–104 where gump has 3,420 | **proved** as a statement of which facts are shared (confirmed); the lifetimes are the survey's (`research/phase/rules.csv`) | entries 4, 7, 13 | — |
| P | Theorem P: a one-step inequality (∗) for a statistic at every time of a window bounds the instantaneous hazard by ε(1 − s̄)/(1 − s̄ − a) after a burn-in. No Markov property | **proved** (confirmed) | entry 3 | walk on {0,1,2}: bound 3/4, exact 0.0522 |
| P̄ | Theorem P̄ (pooled form): Deaths ≤ D(𝓛ᶜ) + Σ_{entries into 𝓛} ψ + boundary, for every ψ ≥ 0 superharmonic for the pooled one-step table on a low set 𝓛; identity for the table's committor ψ*. No Markov property, no uniformity in time, no constant, censoring free | **proved** (confirmed) | entry 8 | same walk, 𝓛 = {1}: ψ* = 1/4, entry flux 0.1978, 0.0495/(1 − 0.0522) = 0.0522 = h |
| C | Comparison form of P̄: if every pooled row dominates the same row of a monotone kernel q, the committor of q is a certificate. Corollary: a larger face's committor at fixed k is smaller if its rows dominate the smaller face's | **proved** (confirmed; the monotone rows of q are needed, the critic's counterexample); the corollary's hypotheses are lab L9.2 | entry 18 | 𝓛 = {1}: the hypothesis is (∗̄) for one row |
| T′ | Block bound: if θ_k ≥ θ₀ for k₀ ≤ k < K then ψ*(k) ≤ e^{−θ₀(k − k₀)⁺} | **proved** (confirmed) | entry 17.2 | walk on {0..3}, up ¾: bound 1/9, exact 1/13 |
| T | The local-root sum is an upper bound for the committor's exponent: for non-increasing s_k ≥ θ_k on a block, ψ*(k) ≥ c₀(e^{−Σ s_j} − e^{−S(K)}) | **proved** (confirmed) | entry 17.3 | same walk: 2/27 ≤ 1/13 |
| X | The sum is exact (up to a constant factor) for skip-free rows and for branching rows (ψ = q^k). A three-state branching chain with density-dependent death has 1.695 < 1.863 < 2.234 (block bound, exponent, root sum) | **proved** (confirmed) | entry 17.4 | offspring 0 or 2 with probabilities ¼, ¾: q = 1/3, from two cells 1/9 |
| Q | Conditional area law, final form. (R): θ_k ≥ θ₀ for k₀ ≤ k < K. Then Deaths/Expo ≤ e^{−θ₀(K − k₀)}·Φ + boundary, Φ = the exponential moment of the undershoot of K per unit of exposure (a direct death counted as an undershoot to zero); and Φ ≤ C⁺ if (R⁺): M_z(θ₀) ≤ C⁺e^{θ₀(z − K)} for the visited rows z ≥ K. So R and R⁺ give ln τ ≥ θ₀(K − k₀) − ln C⁺ − window | **proved** from P̄ and T′ (the implication confirmed in round 4; the statement with Φ and R⁺ is the closing round's, not yet checked). Measured: R(0.35, 0.40, 5) holds on all four hull tables (block minima 0.4034, 0.4261, 0.4117, 0.4172), k₀ ≥ 3; Φ = 0.136, 0.103, 0.085, 0.046 and C⁺ ≤ 1.07 on the tallied rows K … A/2; rows above A/2 not tallied. Gives 0.13–0.14 per cell (0.16–0.17 with the measured Φ). R is not derived from the rule (and by R5 cannot follow from the graph and θ) | entries 17.6, 23 | walk on {0..3}, up ¾, held at 3, K = 3, k₀ = 0, θ₀ = ln 3: Φ = ¾p₃ = 0.538, C⁺ = 1.5, bound (Φ/27)/(1 − w) = 0.0208, exact h = 0.0143 |
| V⁻ | For one table: if W is admissible (W(n) − W(n′) ≤ −ln T̄(n, n′) + e) and every row k₀ < n ≤ n₁ is good, (e^e N_n)^{1−δ}M_n(θ₀)^δ ≤ 1, then ψ*(n) ≤ exp(−[(1 − δ)(W(n) − W̄₀) + δθ₀(n − k₀)]⁺); and always ψ*(n) ≥ e^{−W°(n)}. δ = 1 is T′ | **proved** (closing round; checked only by me: 41,773 cases on random tables with no violation and a negative control; the m-fold chains to 2,688 cells) | entry 24.2 | walk on {0..3}, 𝓛 = {1, 2}, e^{θ₀} = √3: row 1 good iff δ ≥ 0.828; δ = 0.9: 1.266 ≤ −ln ψ*(2) = 2.565 ≤ W°(2) = 2.773 |
| V⁻(E) | For a family: if the tables are sub-extensive, ln M^{(m)}_n(s) ≤ mΛ_{n/m}(s) + e_m for all real s (E), with a margin Λ_x(θ₀) ≤ −ε₀ on the block (R_ε), then for δmε₀ ≥ e_m + (1 − δ)ln(mx₁ + 1): −ln ψ*_m(n) ≥ (1 − δ)m(V(n/m) − V̄) + δθ₀(n − k₀), V the quasi-potential of the rates on the low set. Hence liminf −(1/m)ln ψ*_m ≥ V − V̄. The m-fold family of a table is exactly extensive (Lemma E1); if all its rows have positive roots, liminf ≥ V with nothing subtracted. For a gump face the rim lemma (N_n ≤ 7n + 1) makes the bottom cost O(1) when sparse rows have a margin proportional to their population | **proved** (closing round; not yet checked). The proof's threshold on the A = 84 table: m₀ = 41, 197, 489 patches of 84 cells at δ = 0.5, 0.2, 0.1 (block to 0.35A). For gump the hypothesis (E) is untested, and the tables at A ≤ 84 are not extensive copies (4–7% between 45 and 90 cells) | entry 24.3 | Lemma E1 for m = 2: the row from 2k + 1 is T_k ∗ T_{k+1}, transform M_k·M_{k+1} |
| H | Hazard form of V⁻: Deaths/Expo ≤ Φ[ψ] + boundary; with R⁺ and B⁺ (W(n₁) − W(z′) ≤ −ln T̄(z, z′) + e for the rows above the low set) ln τ ≥ (1 − δ)(W(n₁) − W̄₀) + δθ₀(K − k₀) − (1 − δ)(e + ln K) − δ ln C⁺. δ = 1 is Q | **proved** (closing round; not yet checked). B⁺ holds with e = 0 on the tallied rows K … A/2 of the hull tables | entry 24.4 | δ = 1: the smallest case of Q |
| V′ | The critic's form: if every target of a block row either gains c₁ in W or has probability ≤ e^{−a}, and e^{−(1−δ)c₁} + (n₁ + 1)e^{−δa} ≤ 1, then ψ* ≤ e^{−(1−δ)(W − W̄₀)⁺}. Needs a hypothesis on V (a gain across every likely step) that R does not give | **proved**; the example where V alone fails at small m is computed, not proved | entry 24.5 | rows 1, 2, 3 going to 0 with probability 0.01, else up by one: e^{−(1−δ)W} fails at m = 5, 10, holds from m = 20 |
| V | The exponent of the face law is the quasi-potential V of the one-step rates of the pooled table of the living state: ln τ_A = V·A + o(A) if the tables are extensive in the limit with the sparse rows a boundary layer | lower half **proved** (V⁻(E)); upper half **sketched** (24.6: needs a local lower bound for a point and continuity of the rates; on the m-fold chains the exact committor's increment converges to the recursion's value to 3 × 10⁻⁴, lab L12.5). **For gump: conjecture.** The number is calculated from a measured table and must be stated with its continuation: 0.2191 on the A = 84 hull table with own rates and c₁ (0.2180 by `bellman.py`'s Gaussian closure; 0.2054 with c₀), rising with the table (0.2098, 0.2168, 0.2191), against measured slopes 0.212, 0.212, 0.218, 0.221. Bounds: 0.144 ≤ V ≤ 0.2305 | entries 17.5, 21, 22, 24 | formula (2) of 17.5 against four rows of lab L9.1: 0.010, 0.021, 0.043, 0.109 for gaps 0.024, 0.032, 0.051, 0.118 |
| V∞ | The hull's local slope levels off near 0.220 ± 0.006 | **conjecture** (three points; hull faces are mostly rim, E3) | entries 17.5, 21, 22.3 | — |
| R | Biased voter dynamics on any finite graph: λ^{−n} is a martingale; a set of n sites dies out before filling the graph with probability (λ^{−n} − λ^{−N})/(1 − λ^{−N}) | **proved** (confirmed) | entry 10 | one edge, one occupied vertex: 1/(1 + λ) |
| A | In the hull of every radius a non-empty sealed set has at least A(R) cells | **conjecture** beyond R = 10 (exact to R = 10: critic). Not pursued: the induction needs a stability statement | entry 12 | R = 3: 9 cells |
| G1 | (i) In the 2D rule every edge with an end costs 0.34–0.35 per independent cell. (ii) The ring has the same exponent and carries a power of L | (i) **conjecture**, measured in five geometries, the fifth made for the purpose (exam E1: 0.3458 ± 0.0036). (ii) **conjecture**: ring minus anchored row is fitted equally by 1.66(16)·ln L − 4.41 and by 0.065(6)·L − 0.73, L = 20…32. C4 (0.277) unexplained | entries 5, 7, 15.3, 16.1 | — |
| W | Death-age profile model: free ends give no power (proved in the model); a window pinned at both ends ℓ^{−3/2}; one free end ℓ^{−1/2} | **sketched** model; segments agree, windows compatible (lab L9.3). Its ring part **fell** (below) | entries 15.3, 16.1 | segment of 2 cells, steps in {−1, 0, 1}: 3 step values, 3 profiles with minimum 0 |
| F12 | face12e's 0.205 per cell of the layer is a lower living density (0.41 against 0.52) compensated by roots about a sixth higher than gump's at the same fraction of the mean | **conjecture** (no table of that lattice exists; exam E4 b) | entry 20 | — |
| Dr | On hull faces, looking back from death √n falls by ≈ 0.59 per generation at every size A = 30…84 | a data reading that stands on hulls; as a property of the rule it **fell** (exam E3: ≈ 1.0 on a rim-free face) | entries 11.1, 15.1, 16.3 | — |

**Exam entries.**

| entry | predicted | outcome |
|---|---|---|
| E1 | notched ring slope 0.345 ± 0.020 | holds: 0.3458 ± 0.0036 |
| E2 | remnant 9.8 ± 1.0 cells at lag 2, L = 32, 36 | not refuted: 9.09 ± 0.08, 7.99 ± 0.38; central value too high at L = 36 |
| E3 | gump's remnant curve and tail ratio on a rim-free slab face equal the hull's | fails at lags 3, 4 (10.7, 18.4 against 6.4, 9.7) |
| E4 | `bellman.py` on the one-step table of (a) the slab face of 60 cells: 0.211 ± 0.012; (b) the layer beneath a 5 × 5 wall of face12e: 0.205 ± 0.015 | **not run.** Its window cannot tell V from ∫Θ; the closing report says what would (root sum minus the committor's exponent at two sizes) |
| LR11 (a prediction to the lab) | second doubling of the chain of the A = 84 table adds 36.6 ± 1.2 | **missed**: 34.65. Predicted with continuation c₁ for a chain specified with c₀ (entry 22.4) |

**Fell** (each with its reason; none is used above).
- H (Theorem P's hypothesis with φ = r^{min(n,K)}): a one-cell face does not drift up, lab L1.1 (entry 7).
- H′ (ψ*_K(k) ≤ C e^{−θk} with C, θ, κ independent of A): the committor steepens with the face, lab L5.1; replaced by
  hypothesis R of claim Q, and the monotonicity in A it needed is explained by claim C.
- G2, gump half ("gump's data cannot tell a flash from a front"): they can, lab L1.3 (entry 7).
- L1(c) "each constraint involves a private cell": false at the three corners of a hull face (entry 7). R5's
  first example (the rule "born iff 12 alive"): it has birth count 12, not θ (entry 7).
- Relation (M), γ = θρ − θ²σ²/2 (entries 11.3, 13): its tangency assumption fails on the histograms and it is
  0.9–1.6 nats too large at A = 63, 84 (lab L5.4; entry 15.1). "One exponent θ ≈ 0.50 with power-law prefactors"
  (11.2): the roots depend on k and on A (lab L5.2).
- Th (ln τ ≈ A·∫Θ): the local-root sum is not the committor's exponent (lab L9.1); by claim T it is an upper
  bound, by claim X it is exact only without jumps or with root-preserving rows (entry 17). Replaced by claim V.
- W, ring part (a closed ring carries L^{−1/2}): the measured power is 1.3–1.7 in the 2D rule and 0.7–1.3 in three
  dice models, and a product of pair weights gives ½ whatever the weights (entry 16.1).
- "One remnant, the same object in every vessel" (11.1, 11.2, the rationale of E3): refuted by E3 (entry 16.3).
- The exponent from independent cells (mean field): its cheapest route is an overcrowding of the whole face, its
  values do not converge when a second layer is freed, and its sparse faces do not regrow (entry 19).
- Q's side condition as worded in 17.6 ("the downward crossings of K undershoot by a bounded exponential
  moment"): the moment per crossing grows with the face (4.3 → 58 on the m-fold chain, lab L12.3), because
  crossings become rare. Replaced by Φ and R⁺ (entry 23). Also wrong in the round-4 report: "R fails at A = 30"
  (it holds), and "the crossing term is carried by drops of one to three cells" (by count, not by weight).
- The LR11 prediction (above), and with it any statement of "V = 0.218" without its continuation (entry 22).
- E2's "levelling off near 9–10": what is established is that the remnant does not grow.
