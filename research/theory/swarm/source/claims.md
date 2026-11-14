# source: claims (current list)

Tags: **proved** (proof in `journal.md`, section given), **sketched** (what is missing is said), **guessed**.
Notation of journal S1: layers 𝓛_k (face = 𝓛_0), deep neighbour D, top process Z_t (w layers), drive b_t
(𝓛_w ∪ 𝓛_{w+1}), dice chains D_w(ν) and D_w[κ], relatives R_w(Q).

| # | claim | tag | where | smallest case worked by hand |
|---|---|---|---|---|
| C1 | **Exact source.** In R_w(Q) (true rule in the top w layers, any deep-permutive rule below, two-way coupling), started from (any law on the top) ⊗ (uniform on the source), the source at time t is uniform and independent of the top's whole past; the top w layers are exactly the dice chain D_w(ν). Holds for the 2D rule and for gump (D is a bijection between layers), any cross-section. | proved | S2 | one column, w = 1, rule-90 source with the face XORed into its first cell: y_1(1) = y_0(2) ⊕ X_0, y_2(1) = y_0(3) ⊕ y_0(1) ⊕ Φ(X_0, y_0(1)) |
| C2 | **Differences from gump** of "gump on parity": rule below depth w; half-infinite reservoir; no T5 below depth w; fresh entropy for ever. Kept: lattice, neighbourhood, T2 at the face, T3 and T6 inside the top w layers, peeling of the first w faces. | proved (each line is a remark on a proof in AUTOMATON.md) | S2 table | — |
| C3 | **Accounting.** For a deterministic map of a finite set, Σ_t H(b_t ∣ past of b) ≤ log₂∣Ω∣. Exact dice last at most N/(2A·H₂(ρ)) generations in a vessel of N cells; over a lifetime the drive's conditional entropy given its past is ≤ N/τ per generation. | proved | S3 | R_1 with a binary source of H layers: exact for ⌊H/2⌋ generations, equal to the bound |
| C4 | **Markovian projection.** For any vessel and initial law, the death time of a gump face has the law of the absorption time of D_w[κ_t], κ_t(β ∣ z) = P(two layers beneath show β ∣ top w layers show z), both at time t. Transfer identity P(T > R) − (λ_0 P^R)(alive) = Σ_t E[((K_{t+1} − P)V_{R−t−1})(Z_t)]. Constant hazard ⇔ the conditional law of (Z_t, b_t) given alive and unsettled is constant in t. | proved | S4 | Z′ = Z·b with a constant drive b_0 ~ Bernoulli(½): κ_0(1∣1) = ½, κ_t(1∣1) = 1 after; P(T > t) = ½ |
| C5 | **Local threshold lemma.** With a_i = λ^{−d_i}, 1 < λ² < 4/3 (2D: 3/2): m·Σ_{non-O1 mismatches} a_i² ≤ (12λ+1+θ′)S + c′·Σ_{O1 events} a_i², on finite or infinite vessels. | proved | S5 | one isolated live cell: K(1) − K(0) = θ′ − 1 ≥ m |
| C6 | **Uncapped rule on infinite configurations:** every cell has at most C_U mismatches, uniformly; each cell is eventually of period ≤ 2. (Open in threshold.md.) | proved | S5, Cor. 4a | the advancing front of threshold.md: a cell reads 0,0,1,1,1,…: two mismatches |
| C7 | **A threshold bulk is not a source** (entropy rate zero at any finite set of cells, even with an infinite random reservoir); in gump the non-period-2 activity of a face is bounded by a constant per cell plus O1 events discounted by λ^{−2⌈k/2⌉} at depth k; non-overcrowded deaths dissipate. | proved (the entropy statement uses: a cell's series is determined by two values and its mismatch times) | S5, Cor. 4b | — |
| C8 | A one-way periodic source of period P gives an immortal fraction, not a lifetime, unless P ≳ τ; so a finite source needs ≥ log₂ τ cells. | sketched: the fixed-map structure and immortality at a fixed point are proved; "P(T < ∞) ≈ P·h" assumes coalescence within one turn | S6 | Z′ = Z·b, P = 1: the example of C4 |
| C9 | A class 𝒦 of state-dependent dice exists that contains gump's κ_t and on which a lifetime lower bound e^{cA} holds uniformly. | guessed (this is Aim B; nothing proved) | S4 | — |

Not checked by anyone but me: everything. Lab checks requested for C1 (L1) and C5 (L2).
