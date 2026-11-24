# blast/ref-chain: referee's review of the `chain` arm (the lifetime theorems in Lean)

Agent `ref-chain`, 2026-11-24. Refereed: `research/blast/lean/mathlib/GumpMath/Chain*.lean` (15 modules),
`AxiomsChain.lean`, `statements_chain.json`, `notes/chain.md`, against `research/blast/rigour/THEOREMS.md`, its
referee `research/blast/ref-proofs/REVIEW.md` and `research/blast/image/README.md`. Every number below is from my
own code, written from `reference/oracle.py` and the definitions (not from the chain agent's scripts or from
`rigour/`'s code); every Lean claim of mine is a compiled file in this directory. Labels: **[proved: Lean]**
(compiled here), **[proved: paper]**, **[measured]** (exact linear algebra or brute force), **[judgment]**.

## Verdict

The kernel-checked proofs are sound and the hygiene is clean. On the wrapped faces the Lean statements say what
the source says (Lemma 0, one price per orientation, one price per cell on rotation-invariant tori, Theorem 1 with
its constant), on a model of the layer that I confirmed independently against the oracle. The defects are in what
some *statements* leave existential: two families of theorems are satisfiable by witnesses that carry none of the
content their rows describe. None of the numbers broke.

| group | Lean names | Lean statement vs row and source |
|---|---|---|
| Theorem 2, for a given QSD | `tilt_identity`, `neg_log_Z_one`, `tiltMean_antitone`, `price_mem`, `IsQSD.lifetime_eq`, `last_living_law` | **same** (for every QSD μ; no junk value is reachable, see "Junk values") |
| Theorem 2, "on every face" | `tilt_identity_exists`, `ProductKernel.tilt_identity_product`, `surrogate_theorems` | **less**: the QSD is "some QSD"; on every wrapped face the λ = 0 point mass on the all-alive state meets every clause with log τ = 0 (D2) |
| Perron–Frobenius | `exists_pos_eigenvector`, `left_eigen_unique`, `qsd_exists_unique`, `exists_qsd` | **same** as the rows (eigenvalue ≥ 0, not identified as the spectral radius; said) |
| Theorem 1 and its constant | `upper_bound`, `threeCoins_death_ge`, `twoCoins_death_ge`, `upper_bound_coins`, `emax_main`, `emax_fair`, `kagome_upper_bound` | **same**; the per-cell law is gump's rule (68 exact checks against the oracle's BIRTH/SURVIVE) |
| Lemma 0 and prices on wrapped faces | `kagome_lemma0`, `wrapped_lemma0`, `kagome_one_price`, `wrapped_one_price`, `kagome_rotation`, `wrapped_rotation`, `torus_2_0_2_one_price` | **same** as the source; "\|T\| = HD" in the rows is not in Lean (D3; closed here for the 12-cell torus) |
| surrogate on bit masks | `bitP_row`, `bit_surrogate`, `bit_one_class` | `bitP_row`, `bit_one_class`: same. `bit_surrogate`: **less**: its local factorisation L is existential, so "ln τ = Σ c_i" is empty of per-cell content (D1) |
| Lemma R | `routes_first`, `routes_second`, `log_odds`, `routes_concave`, `two_routes_step` | **same** |
| seam identity | `seam_identity`, `seam_identity_obs`, `seam_sharp`, `cover_marginal` | **same** as image's finite-K form (an identity of ring products; the modelling step is a hypothesis, as the rows say). Slightly **less** than it could be: it holds for every L with (F^L)(a,a) > 0 |
| Theorem 3 from (SSM) | `SSM`, `IntSSM`, `SSM.toIntSSM`, `thm3a`–`thm3d` | **same** as an implication, with the referee's K₀/A; `Face.r` is any number and `Face.μ` any QSD (said for r, not for μ) |
| tilt without (SSM) | `tilt_riemann_bounds`, `price_compare`, `price_of_pointwise`, `SSM.einf_continuousOn` | first two: **same**. `price_of_pointwise`: true; its hypothesis asks convergence at the jump point too (D4). `SSM.einf_continuousOn`: the core of the referee's objection, one step short of it (completed here) |
| the rate | `decay_bounds`, `lifetime_from_bounds` | **same**, except that `lifetime_from_bounds` is conditional on r < 1, which the row omits (D6) |
| Fekete with defects | `price_exists_of_sub`, `price_exists_of_super`, `price_interval` | **same** (conditional; the gluing inequalities are not proved, as said) |

## Defects, ranked

**D1. `bit_surrogate` (ChainBits.lean l. 127–146): the prices are of an existential factorisation.**
The conclusion is `∃ hP μ lam (L : … .LocalDeath (Fin A)), IsQSD μ lam ∧ log τ = ∑ i, L.price μ i ∧ log τ ≤ …`.
Local death factors are not unique, so this clause holds with every price but one equal to 0.
[proved: Lean] `RefChainVacuity.lean`, `exists_lumped`: for every killed chain with some `LocalDeath` and any QSD,
there is an `L'` with `log τ = ∑ i, L'.price μ i` and `L'.price μ i = 0` for all i ≠ i0 (`lumped` puts the whole
death probability on i0). So `bit_surrogate` establishes "a QSD exists and ln τ ≤ ε_max·A for it", and nothing
about c_i. The proof's witness is the right L (`ofStochastic_local … a'`); the fix is to name it in the statement,
as `surrogate_theorems` does. Also: `k : ℕ → ℕ → ℕ` is any function with k ≤ 6, not tied to a neighbourhood (more
general, harmless), and μ is existential (D2). The row ("ln τ = Σ_i c_i") reads more than is stated.

**D2. The existential "Theorem 2 on every face" can be met by a junk law.** `KilledChain.exists_qsd` (ChainExist.lean
l. 22), `tilt_identity_exists` (l. 81), `ProductKernel.tilt_identity_product` (ChainLemma0.lean l. 214),
`surrogate_theorems` (ChainInst.lean l. 163) conclude `∃ μ lam, IsQSD μ lam ∧ …` with nothing on λ. `IsQSD` (ChainTilt.lean
l. 205) is any probability left eigenvector, λ = 0 allowed. [proved: Lean] `RefChainVacuity.lean`:
`point_qsd`/`point_lifetime` (a surely-dying state z gives the QSD δ_z, λ = 0, τ = 1); `kagome_all_dies` (on the
kagome layer over every T, the all-alive state dies surely); `junk_tilt_identity_product` (on every wrapped face,
every clause of `tilt_identity_product` holds for δ_all with log τ = 0); `junk_ne_physical` (it is not the law of
`kagome_lemma0`). [measured] the physical value on torus (2,0),(0,2) is ln τ = 3.98. Where Lemma 0 is proved
(wrapped faces) the chain agent's `kagome_one_price` names the right law, so nothing is lost there; on hull faces and
strips, where these existential theorems are all there is, they do not say which τ the identity is about (the
dominant QSD, which the source's `dense.py` computes). A repair: prove that the limit in `exists_qsd` has λ equal to
the largest eigenvalue modulus (Wielandt's root is monotone in the matrix, so r_k ↓ ρ(Q)), or state existence of a
QSD with λ ≥ λ' for every QSD (ν, λ'). The rows say "uniqueness is not claimed"; they do not say that the λ = 0
law is admitted.

**D3. "|T| = HD" (rows `wrapped_one_price`, `torus_2_0_2_one_price` "ln τ = 12·c"; ChainTorus.lean header) is not
in Lean.** The statements have `Fintype.card (Torus H K D)`. True (|ℤ²/Λ| = |det| = HD) but unproved.
[proved: Lean] `card_torus_2_0_2`: card = 4, so `torus_2_0_2_one_price` does give ln τ = 12 c. The general case
is not done here.

**D4. `price_of_pointwise` (ChainTiltLimit.lean l. 80) asks convergence of ⟨E⟩_{s,G_n}/A_n at every s ∈ (0,1].**
At a first-order jump the finite curves need not converge at the jump point itself (if the finite-size transition
points s*(G_n) approach s* from alternating sides at a rate slower than 1/A_n, the value at s* alternates between the
branches), so the hypothesis can fail exactly where the notes say a jump is harmless. Dominated convergence needs
only almost every s. [proved: Lean] `RefChainVacuity.lean`, `price_of_ae`: the same conclusion from convergence
for almost every s. With that version the notes' sentence "a first-order jump along the tilt does not obstruct" is
right as stated; with the original it needs the jump point to behave.

**D5. The notes' list "places where the source needed more than it said" overstates (notes/chain.md, l. 140–158).**
1 (λ > 0 for uniqueness) is a property of Lean's weak `IsQSD`; under the standard definition (P_μ(T > t) > 0,
which the notes mention) the source is right as written. 4 (e_∞ integrable) is redundant whenever (SSM) has content:
[proved: Lean] `SSM.toIntSSM'` derives `IntSSM` with no integrability hypothesis from (SSM) plus arbitrarily small
error terms, using the chain agent's own `SSM.einf_continuousOn`. 5 (division by (F^L)(s,s)) does not arise in
the source, whose covers are whole multiples of the loop; and off multiples the identity still holds wherever
(F^L)(a,a) > 0 (below). 6 ((K) for every cell in every state) is the source's standing assumption, stated as such.
3 is rounding (true: 0.081312·e^{2.509} = 0.99954 < 1, so ln τ ≤ 2.509·A does not follow from the argument; also
the referee's "2.509·A is right" is wrong by the same rounding). 2 (existence of μ off Lemma 0) is a genuine
omission, of a standard fact. 7 is the referee's correction. None is a gap in the mathematics of the source.

**D6. `lifetime_from_bounds` (ChainRate.lean l. 145) is stated as `r < 1 → …`; r < 1 is not proved.** It holds
under (K) (every row of Q sums to less than 1); the row states the bounds unconditionally. Minor.

**D7 (cosmetic).** Row `price_invariant`: "that translations act transitively on each orientation is not
formalised" — it is, in `kagome_one_price` (`tr`, `P_tr`, `a_tr`). Row `emax_main`: "ln τ ≤ 2.509·A is true of
the surrogate" was asserted without proof; on wrapped faces it is true: [proved: paper] cells alive with k = 3 are
the only ones with cost ε_max; each has 3 dead neighbour slots, all outside that set S, and a cell receives at most
6 slots (multiplicities are symmetric), so |S| ≤ 2A/3 and ln τ ≤ max_x E(x) ≤ (2ε_max + ε₂)/3·A = **2.2411·A**
(ε₂ = 1.7044, alive with k = 2). Brute force: max_x E(x)/A = 1.52–1.82 on the five 9- and 12-cell tori
(`python3 emax_bound.py`). (Not for hull faces: rim cells have fewer than 6 neighbours and the count fails.)

## Junk values and vacuity: what I tried that did not break

- `lifetime μ = ∑' t, survival μ t` is a junk 0 when the chain never dies ([proved: Lean] `noDeath_lifetime`).
  Every headline theorem that takes `log (lifetime μ)` carries `LocalDeath` (death = ∏ d_i with d_i > 0), so
  `hazard > 0`, λ = 1 − h < 1, the sum is the geometric series and `log` sits on 1/h > 0 (`tilt_identity`, l. 317).
  `lifetime_from_bounds` guards with r < 1. No theorem uses `lifetime` without one of these.
- `tiltMean` divides by Z(s) = Σ μ e^{−sE} > 0 for a probability μ (`Z_pos`); the interval integrals are of
  continuous integrands (`continuous_tiltMean`), so never the junk 0; `price_of_pointwise`'s ∫ f is of a bounded
  a.e. limit of continuous functions, hence a true integral. `Real.log` of a cost is of d_i ∈ (0,1]. In (SSM),
  ξ = 0 gives r/0 = 0 and a bound K + K₀/A (degenerate, not false); `thm3b`, `thm3c` require ξ > 0; `thm3d`'s
  hypothesis fails for ξ = 0. `K₀/A` with A = 0 is 0 (a face with no cells dies surely; harmless).
- Inhabitants, all compiled in `RefChainVacuity.lean`: `KilledChain`, `LocalDeath`, `IsQSD` (several);
  `ProductKernel`/`SubsetChain` (the kagome kernel, used by `kagome_all_dies`); `Face` and a growing family
  `fam n` (n + 1 independent cells) satisfying `SSM` with e_∞ = log 2, K = K₀ = 0 (`fam_SSM`), and `thm3d` applied
  to it (`fam_price`); `torus_2_0_2_one_price` with an actual `Fintype (Torus 2 0 2)` at (0.44, 0.42)
  (`torus_2_0_2_instantiated`). `[Fintype (Torus H K D)]` is satisfiable exactly when H, D ≠ 0 (`torus_finite`).
- Quantifier order: uniqueness clauses are "∀ ν lam', IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam" after the
  existential: correct. `Irreducible` allows k = 0 (so x → x trivially), which is the right convention.
- `price_invariant`'s hypotheses (a state permutation preserving Q and a cell permutation carrying d_i) are
  discharged in Lean for translations and the rotation; nothing is assumed.

## The model against the automaton

`python3 research/blast/ref-chain/kagome_check.py` (5 s; output `kagome_check.out`) [measured, exhaustive]:
- From `oracle.offsets` alone: the cells of the layer x+y+z = 1 modulo the lattice H·E1 + K·E2, D·E2
  (E1 = (2,−2,0), E2 = (2,0,−2)), in-layer neighbours = offsets with zero sum. Their multisets equal Lean's `nbrs`
  (transcribed from ChainKagome.lean l. 46–49) under (o,(a,b)) ↦ e_o + a·E1 + b·E2, on **16 tori**: (2,0),(0,2);
  (1,1),(0,4); (1,0),(0,4); (1,1),(0,3); (1,0),(0,3); (3,0),(0,3); (4,0),(0,4); (1,4),(0,21); (1,12),(0,28);
  (6,0),(0,6); (1,7),(0,19); (2,1),(0,3); (3,1),(0,2) and the degenerate (1,0),(0,1); (1,1),(0,1); (1,0),(0,2)
  (self-neighbours and multiplicity 2 included). Negative controls: one entry given the wrong orientation fails on
  all 16; one entry shifted by 2e1 fails wherever 2e1 ≠ 0 in T (passes, correctly, on (2,0),(0,2) and H = 1, K = 0).
- The oracle's layer histogram for d = (1,1,1) is {−4: 1, −2: 2, 0: 6, +2: 2, +4: 1} for each orientation: six
  in-layer neighbours and the coins (2,1) beneath.
- `oracle.step` on a 26³ box, random layers S, S−2, …, S−8 and dead layers above: all 405 interior cells of layer S
  are alive next iff rule(x, k_in-layer + b_beneath) with BIRTH = (4,5), SURVIVE = (3,4,5).
- The one-cell law: `python3 gen_cell_law.py > RefChainCellLaw.lean` writes 68 exact identities (`death3` for
  s ∈ {dead, alive}, k = 0…6; `aliveProbR … 2 1` unfolded directly through `Gump.rule`, not through the chain
  agent's lemma; `death2`, k ≤ 2) at (ρ1, ρ2) = (11/25, 21/50) and (1/3, 3/7), values computed in Python from the
  oracle's BIRTH/SURVIVE; all compile [proved: Lean]; a changed value fails (negative control run).
- The convention (H,K),(0,D) of `Torus` is the one of rigour's `exact.csv`: my kernels reproduce its ln τ on all
  five 9- and 12-cell tori to ≤ 7·10⁻¹³ (below). This closes, for those tori, the notes' unchecked identification
  with `geom.py` (up to mirror image, which no lifetime can see).

## Numbers

`OMP_NUM_THREADS=1 python3 research/blast/ref-chain/chain_numbers.py` (18 s; `chain_numbers.out`) [measured;
dense 2^A kernel, dominant left eigenvector by power iteration, residual ≤ 5·10⁻¹⁶; ρ = (0.44, 0.42)].

| torus | ln τ (mine) | exact.csv | tilt identity residual | ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ | c_X, c_Y, c_Z | rot.-inv. |
|---|---|---|---|---|---|---|
| (1,1),(0,3), 9 | 2.694626605944 | 2.694626605944 | −4·10⁻¹⁵ | 0.826 ≤ 2.695 ≤ 9.020 | 0.29940 ×3 | yes |
| (1,0),(0,3), 9 | 3.393524719052 | 3.393524719052 | −2·10⁻¹⁵ | 1.423 ≤ 3.394 ≤ 7.188 | 0.37976, 0.37976, 0.37166 | no |
| (2,0),(0,2), 12 | 3.981836588281 | 3.981836588280 | −5·10⁻¹⁵ | 1.370 ≤ 3.982 ≤ 10.077 | 0.33182 ×3 | yes |
| (1,1),(0,4), 12 | 3.711833898815 | 3.711833898815 | −6·10⁻¹⁵ | 1.124 ≤ 3.712 ≤ 10.908 | 0.33193, 0.29801, 0.29801 | no |
| (1,0),(0,4), 12 | 4.133012406313 | 4.133012406313 | 0 | 1.632 ≤ 4.133 ≤ 9.100 | 0.35027, 0.35027, 0.33272 | no |

On every face: ⟨E⟩_s never increases on 2001 points (largest step −3·10⁻⁴); Σ c_i − ln τ ≤ 6·10⁻¹⁵; the spread of
c_i within an orientation ≤ 5·10⁻¹⁶ (one price per orientation); all c_i ∈ [0, ε_max]; E_μE/A = 0.8398 on (2,0),(0,2)
(THEOREMS.md's number); max ε_i(x) = ε_max = 2.509462. **The rotation hypothesis matters**: the three prices are
equal exactly on the rotation-invariant tori and differ by up to 0.034 on the others. Lemma 0: the class of the
all-X state u is every living state but one (2^A − 2), equals the set of states that can survive, u → y for every
living y, Q u u > 0, and the one other living state (all alive) dies surely and carries the junk QSD (λ = 0,
τ = 1). The same holds on the degenerate tori (1,0),(0,1), (1,1),(0,1), (1,0),(0,2) (`chain_numbers_small.out`).
Riemann bracket, n = 16, (2,0),(0,2): 3.7147 ≤ 3.9818 ≤ 4.2589, width (⟨E⟩₀ − ⟨E⟩₁)/n = 0.544 ≤ ε_max A/n = 1.88;
holds for n = 1, 2, 4, 8, 16 on all five. `decay_bounds`: the Perron root of the class block equals the QSD's λ
to 10⁻¹⁴; P_x(T > t) ≥ (m/M) r^t and P_x(T > t+1) ≤ (M/m) r^t for all x in the class and t < 400 (m/M = 0.10–0.33).
`lifetime_from_bounds` (with E_xT by a linear solve): (2,0),(0,2): 12.09 ≤ E_xT ∈ [14.77, 58.14] ≤ 238.7.
`price_compare` between (2,0),(0,2) and (1,1),(0,4): |Δ(ln τ/A)| = 0.0225 ≤ δ + w/n = 0.273 (n = 4), 0.171 (n = 8).

`python3 seam_check.py` (`seam_check.out`) [measured, brute force over all configurations]: `seam_identity` for
random F ≥ 0 (3×3, 30 % zeros), m = 1…4, L = m and 2m: relative error ≤ 9·10⁻¹⁵, the zero-denominator branch
exercised once. **Off multiples**: for dense F > 0 and L = 1, 3, 2 with m = 2, 3, 4 the identity holds (≤ 4·10⁻¹⁶)
— it needs (F^L)(a,a) > 0, not L ∈ mℤ. The claimed failure is real: F = the 2-cycle, m = 2, L = 1 or 3, two of the
four torus configurations have P_T = ½ and right-hand side 0 (Lean's x/0 = 0); the 3-cycle fails at L = 1, 2 and
holds at L = 3, 6. `seam_sharp`: F = v wᵀ, w·v = 1 (all traces 1): error ≤ 6·10⁻¹⁷; a generic F with traces
1.11, 1.01: relative error 0.22 (the trace hypothesis is needed).

`python3 constants_check.py` (`constants_check.out`) [measured]: the smallest one-cell death probability over
(state, k ≤ 6) is 0.081312 = 0.44²·0.42 at (alive, k = 3); ε_max = 2.5094617 ≤ 2.51, > 2.509; the Taylor
certificate of `emax_main` 0.081312·Σ_{i<16} 2.51^i/i! = 1.000538 ≥ 1; fair coins 1/8, ln 8 = 2.079442 ≤ 2.08; every
(state, k) has b = 0 or b = 3 among its deaths; two coins (2,0), k ≤ 2: smallest death probability 0.3136.
Dobrushin's α = 6·max|a(s,k) − a(s,k+1)| + max|a(0,k) − a(1,k)|: **2.922752** at (0.44, 0.42) (both terms 0.417536);
minimum over a 199 × 199 grid of (0.005…0.995)² and a local refinement **2.625000 at (½, ½)**, no grid point below;
3.49–3.50 near the edges. The notes' numbers are right.

`python3 routes_check.py` (`routes_check.out`) [measured]: `two_routes_step` to 6·10⁻¹⁵ over 200 random cases;
`routes_first`, `routes_second` to 10⁻¹¹ (five-point differences, three routes with linear prices). Example
c_b = 0.88, c_s = 0.585, p = 0.086: exact step 0.60729 = corrected formula; the source's c_s + p(c_b − c_s) = 0.61045.

## Hygiene

- [proved: Lean] `lake env lean ChainAxiomSweep.lean` (11 s): `Lean.collectAxioms` over **all 624 constants**
  declared in the 15 Chain modules (426 theorems, 175 definitions, 23 others): every axiom set ⊆ {propext,
  Classical.choice, Quot.sound}; no `sorryAx`, no declared axiom, no opaque. The only "unsafe/implemented_by"
  constants are compiler artefacts (`Orient.ctorIdx._impl` from `deriving DecidableEq`, `pathF._unsafe_rec`,
  `pathL._unsafe_rec`), not used by any proof. Names written to `chain_names.txt`.
- grep over `Chain*.lean`: no `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by`, `opaque`,
  `local instance`, `set_option maxHeartbeats`. The three instances (`Fintype Orient`, `DecidablePred canLive`,
  `noncomputable instance DecidablePred CanSurvive := Classical.decPred`) and `attribute [instance] Face.fσ …`
  decide nothing a hypothesis depends on (decidability instances are subsingletons).
- Every one of the 62 names in `statements_chain.json` and the 82 in `AxiomsChain.lean` resolves to exactly one
  constant (`python3 names_check.py`, after the sweep has written `chain_names.txt`).
- Re-elaboration: every `GumpMath/Chain*.lean` as committed compiles with `lake env lean` against the built
  dependencies, 0 errors (7–53 s each; `reelab.log`). Oleans are newer than the sources.

## The notes' judgments

- **(SSM) "probably false as stated"** [judgment, agreed]. (i) rests on the referee's two-humped tilted laws
  (data; whether the limit jumps is open); (ii) the Dobrushin numbers are right, but Dobrushin's condition is only
  sufficient, so α > 1 closes one route and is no evidence against mixing; (iii) is heuristic. "Not provable by
  known methods, probably false" is a fair reading, not a result.
- **`SSM.einf_continuousOn` against the referee's objection.** It is the logical core (SSM with arbitrarily small
  errors forces e_∞ continuous on [0,1]) but stops short of "a jump of the per-cell limit refutes (SSM)": it does not
  connect e_∞ to the limit of ⟨E⟩_s/A. [proved: Lean] `RefChainSSM.lean`: `SSM.tilt_limit` (under (SSM), A → ∞ and
  Σ e^{−r_i/ξ} = o(A), ⟨E⟩_{s,G_n}/A_n → e_∞(s) at every s ∈ [0,1]) and `jump_refutes_SSM` (a family whose per-cell
  tilted energies converge on [0,1] to a function not continuous there satisfies no (SSM), whatever e_∞, K, K₀).
  The referee's further point (an integrated version would need the jump position to be shape-independent to
  exponential accuracy, i.e. the conclusion) is not formalised by anyone, and the measurement itself is data.
- **"A first-order jump does not obstruct `price_of_pointwise`"**: right for the a.e. version (`price_of_ae`), see
  D4. It gives only the limit (Theorem 3 (d)), no rate; what it needs, the same pointwise limit for rimmed and
  wrapped families, includes the same jump position in the limit. It does not answer the referee's objection to
  (a)–(c), which concerns exponentially small error terms.

## Not checked

- No face above 12 cells (18-cell tori need 2^18 states; the dense route does not reach them); no hull face or
  strip numerically (the existential theorems are the only ones there, D2); fair coins only through constants.
- `bit_surrogate`/`bitP` against the other agent's `Gump.Dice.Face.P`: not compared (the chain notes say the cast
  is not done; I did not do it either). `aliveProbR` was checked against the oracle's rule, not against `DiceDef`.
- |T| = HD for general H, K, D (only (2,0),(0,2)); that `price_exists_*`' gluing inequalities hold (nobody claims
  they do); the general proof that `exists_qsd`'s λ is the spectral radius (suggested repair of D2, not done).
- The rows I did not test numerically: `last_living_law` (identity-level only), `log_odds`, `routes_concave`,
  `thm3a`–`thm3c` (implications from hypotheses no face is known to satisfy), `price_exists_*`.
- The chain notes' Dobrushin script was not run; my own code gives the same numbers. The source's SSM-related
  measurements (two humps) were not rerun.
- The 2.2411·A bound (D7) is checked by brute force only on 9- and 12-cell tori; its proof is on paper here.

## Files

`ChainAxiomSweep.lean` (axiom sweep; writes `chain_names.txt`), `RefChainVacuity.lean` (D1, D2, D3, D4, D5,
inhabitants, junk lifetime), `RefChainSSM.lean` (the objection completed), `gen_cell_law.py` →
`RefChainCellLaw.lean` (68 one-cell identities), `kagome_check.py` (geometry and step vs oracle),
`chain_numbers.py` (QSD, tilt, prices, Lemma 0, Riemann, rate), `seam_check.py`, `constants_check.py`,
`routes_check.py`, `emax_bound.py`, `names_check.py`, and their `.out` files; `reelab.log`. Lean: `cd research/blast/lean/mathlib && lake env lean
/home/user/gump-for-agents/research/blast/ref-chain/<File>.lean`; Python: `OMP_NUM_THREADS=1 python3
research/blast/ref-chain/<script>.py` from the repository root (each script finds `reference/oracle.py` itself).

---

## Second review (2026-11-24, after the chain agent's repairs f32bb82 and the Link modules 9fde4a9)

Refereed: the repaired `Chain*.lean` (now 16 modules with `ChainSharp.lean`), the 17 `Link*.lean` modules,
`notes/link.md`, `statements_link.json`, `AxiomsLink.lean`. Nothing in the shared tree was rebuilt; my files load the
built `.olean`s through `lake env lean`, one process at a time, each under 0.6 GB of anonymous memory
(watched; a full kernel re-run of a reachability check exceeded 3 GB and was stopped, see (3)).

**Verdict.** D1–D7 are closed in the statements, not only in the rows. The Link theorems (`hull3_full`,
`torus103_full`, `torus113_full`, `strip13_full`, `patch13_full`, `torus202_full`) say what their rows say, about
`Gump.Dice.Face.P` itself, and every number and every asserted equality of prices agrees with my own code. I found no
new defect of substance; three small qualifications are below.

### (1) The seven defects, re-attacked

- **D1 closed.** `bit_surrogate` (ChainBits.lean l. 129–145) now names the factor: `L.dc i x = 1 − aliveProbR (cell i)`.
  My `lumped` factorisation (`RefChainVacuity.lean`) no longer meets the statement (its factors are not those).
- **D2 closed.** `IsDominantQSD` (ChainExist.lean l. 29–34): a QSD with λ ≥ λ′ for every QSD (ν, λ′), λ ≥ Q u u,
  P_x(T > t) ≤ C_ε(λ + ε)^t for all x, and ≥ λ^t for some x at each t. [proved: Lean] `RefChainLink.lean`:
  on every wrapped face a dominant law has λ > 0 (`dominant_lam_pos`) and is therefore the unique physical law
  (`dominant_is_physical`); the λ = 0 point mass on the all-alive state is **not** dominant (`junk_not_dominant`);
  in general the dominant λ is unique (`dominant_lam_unique`, from `max` alone) and so is τ (`dominant_lifetime_unique`).
  Nothing in the structure is trivially true; where Q = 0 every law is dominant, with λ = 0 and τ = 1, which is right.
  Qualification (minor): the notes say "not proved: that this λ is the spectral radius"; `decay_up` and `decay_lo`
  together give λ = ρ(Q) at once on paper (‖Q^t‖_∞ = max_x P_x(T > t) and Gelfand's formula). The law μ itself is
  unique only where Lemma 0 is proved; on a reducible face prices of a dominant law could depend on the choice.
  My old `junk_tilt_identity_product` still compiles (it is about `tilt_identity` for any QSD, which is still true)
  but no existential theorem is met by it any more.
- **D3 closed**: `torus_card` (|T| = HD for H, D > 0), `wrapped_one_price_HD`, `torus_2_0_2_twelve`.
- **D4 closed**: `price_of_ae` (my statement, taken over). **D6 closed**: `lifetime_from_bounds_K` proves r < 1 from (K).
- **D5 closed**: the section "places where the source needed more" is gone from `notes/chain.md`.
- **D7 closed**: the `price_invariant` row is corrected; `kagome_sharp_bound` (ChainSharp.lean) proves my paper bound,
  ln τ ≤ 2.2412·A for every QSD on the kagome layer (rightly marked "not for hull faces"; and not yet a theorem about
  `Face.P` on tori, as `notes/link.md` says, since the bijection between the dice cell lists and `Orient × Torus` is
  not formalised — my `kagome_check.py` is the numerical evidence for it).
- My `RefChainVacuity.lean` and `RefChainSSM.lean` still compile against the new modules.

### (2) `hull3_full` and its siblings, clause by clause

- `chain F hd` is `ofStochastic (fun x y => ((F.P ρ1 ρ2 x y : ℚ) : ℝ)) F.empty …` (LinkBridge.lean l. 103): the killed
  chain of `Face.P` itself at `F.empty = ⟨0, _⟩` (DiceBound.lean l. 58). `extend` puts 0 at the empty state and is
  harmless (`toDice` proves the dice agent's `IsQSD`, whose `empty` field requires exactly that).
- Uniqueness is over all `(chain F).IsQSD ν λ′` with λ′ > 0, on the living states `{x // x ≠ F.empty}`: the right
  quantifier and space. `CanSurvive x` = ∃ y, Q x y > 0; `survFrom t x` = ((Q^t)·1)(x) = Σ_{living y} (Q^t)(x, y)
  = P_x(T > t) for the killed chain (its identification with the dice agent's `Face.survival` is not stated, as the
  notes say). The decay clause is two-sided and about that quantity.
- `L` is `localDeath (hull 3) sdens (cellsOK_of_tab …)` (checked `rfl` in `RefChainLink.lean`); the densities are
  ρ1 = 11/25, ρ2 = 21/50 (`rfl`).
- [measured] `link_numbers.py` (faces built from DiceDef's cell lists, `red` and `coin`, with neighbours and coins
  from the oracle's offsets, not from the dice tables; `link_numbers.out`):

| face | λ (float64) | ln τ | prices c_i | classes asserted | classes of equal c_i |
|---|---|---|---|---|---|
| hull 3 | 0.91656736559488 | 2.483715746334 | corners 0.0481050722, others 0.3899000883 | {0,3,8}, rest | the same |
| torus (1,0),(0,3) | 0.96640992756960 | 3.393524719052 | 0.3797575033 ×6, 0.3716598997 ×3 | {0,1,3,4,6,7}, {2,5,8} | the same |
| torus (1,1),(0,3) | 0.93243239359285 | 2.694626605944 | 0.2994029562 ×9 | one | one |
| strip 1×3 | 0.93912167365926 | 2.798878056925 | 0.2774035020 ×6, 0.3781523483 ×3 | {0,2,3,5,6,8}, {1,4,7} | the same |
| patch 1×3 | 0.84747380605665 | 1.880418934121 | 0.19133, 0.19529, 0.11279, 0.27277, 0.33605 (mirror pairs) | {0,8},{1,7},{2,6},{3,5},{4} | the same |
| torus (2,0),(0,2) | 0.98134864699392 | 3.981836588281 | 0.3318197157 ×12 | one | one |

  Every equality the theorems assert holds (to 10⁻¹¹), and every class is exactly as coarse as the numerics allow
  (no two cells in different classes have equal prices). In extended precision (`link_lambda_ld.py`, numpy
  longdouble, exact rational alive probabilities) λ agrees with the five 19-digit certified intervals to
  0–2·10⁻¹⁸, i.e. to the precision of the arithmetic; the 19th digit is the dice agent's certificate's, not
  re-derived here. The certificates' u (207, 10, 3, 14, 73; 7 on the 12-cell torus) make every cell alive-able and
  lead to every living state in one step; every state that can survive reaches u (largest distance 3, 2, 2, 3, 4; 2);
  the states that die surely are none on the hull, strip and patch, the full face on the tori; 4,094 of 4,095 living
  states can survive on the 12-cell torus. All as the notes' table says.

### (3) The certificates and the symmetry checks

Soundness is by construction: `Data.tabOK_spec` turns a passing table check into equality with `Face.nb`, `Face.m1`,
`Face.m2` and `aliveNum` for every cell; `reachOK` requires, for every state that can survive, a successor allowed by
the support (`stepD`, tied to `Face.P` by `Q_pos_iff`) and a strictly smaller `dist`; `symOK` requires σ to permute
the neighbour multisets and coin counts and the state action to move bits accordingly. A passing check implies what
is used. [proved: Lean] `RefChainLink.lean`: the kernel **rejects** a certificate with one wrong next state (492 → 493:
cell 0 dead with no live neighbour cannot be born), one wrong distance, a cell permutation that swaps a corner with a
rim cell, a true symmetry σ0 paired with the state action of σ1, a coin table with one entry changed, and a neighbour
table with one list changed (each `= false` by `decide +kernel`; the true certificate passes). The wrong next state
was placed near the top of the table so that the kernel meets it after 19 rows: a run through all 512 rows of the
hull-3 check exceeded 3 GB of anonymous memory and was stopped. The five `Link<Face>Sym.lean` sources are newer than
their oleans (rewritten after the build, content as committed): I re-elaborated all five from source, 0 errors,
19–45 s each, ≤ 0.56 GB.

### (4) Which faces satisfy the hypotheses

`face_theorems` needs `CellsOK` (coins (2,1), or (2,0) with at most two neighbours); `face_theorems_allcoins` covers
every face whose `coin` is constantly true (every `torus`, `strip`, `patch`). [measured] `cellsok_check.py`: every hull
face `hull R`, R = 1, 3, …, 15 (3 to 108 cells), satisfies `CellsOK` (three corners (2,0) with 2 neighbours; rim
cells (2,1) with 4; interior (2,1) with 6); even R give no cells. For general R it is not proved in Lean (the notes
say so; per face it is `cellsD` by the kernel).

### (5) Hygiene

[proved: Lean] `LinkAxiomSweep.lean` (`LinkAxiomSweep.out`): `collectAxioms` over all **1,078 constants** of the
16 Chain and 17 Link modules (779 theorems): only propext, Classical.choice, Quot.sound; no declared axiom, no
opaque, no `sorryAx`; the only unsafe/implemented_by constants are the three compiler artefacts of the first review.
No `sorry`, `native_decide`, `admit`, `axiom`, `implemented_by`, `opaque` in any `Link*.lean` or `ChainSharp.lean`
(`set_option maxRecDepth 100000` only). Every name in `statements_link.json` (14), `AxiomsLink.lean` (35),
`statements_chain.json` (72) and `AxiomsChain.lean` (98) resolves to exactly one constant (`link_names.txt`). The
Link rows are honest, including what is not proved (no certified λ on the 12-cell torus; Lemma 0 for `Face.P` only face
by face; `survFrom` vs `Face.survival`).

### Not checked (second review)

The 19th digit of the λ intervals (dice agent's certificates, not re-derived); a complete kernel re-run of any
reachability certificate (memory); `LinkTorus202.lean`'s tables and trees beyond what its own `decide +kernel` checks
(its prices and support were checked numerically above); the dice agent's `lntau_le_regular` and `regular_torus202`;
`CellsOK` for hull faces beyond 108 cells; the generator scripts (not in the repository; nothing they compute is
trusted by the kernel).

Files added: `link_numbers.py`, `link_lambda_ld.py`, `cellsok_check.py` (with `.out`), `RefChainLink.lean`
(`RefChainLink.out`), `LinkAxiomSweep.lean` (`LinkAxiomSweep.out`, `link_names.txt`).
