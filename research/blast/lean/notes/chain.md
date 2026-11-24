# The chain arm: the lifetime theorems of `blast/rigour` in Lean

Agent `chain` (Lean arm, theory), 2026-11-24, 11:16 UTC onwards. Source: `research/blast/rigour/THEOREMS.md`,
its referee `research/blast/ref-proofs/REVIEW.md`, the seam identity of `research/blast/image/README.md`.
Files (all new, all mine): `research/blast/lean/mathlib/GumpMath/Chain*.lean` (11 modules),
`research/blast/lean/mathlib/AxiomsChain.lean`, `research/blast/lean/statements_chain.json`, this note.

Every theorem below compiles with no `sorry`, no `native_decide`, and `#print axioms` gives
`[propext, Classical.choice, Quot.sound]` for each (`AxiomsChain.lean`, 54 lines). `sh research/blast/lean/check.sh
--mathlib` passes. Nothing here imports `GumpMath/Dice*.lean`; every theorem is proved from stated hypotheses on a
finite killed Markov chain, and the section *Instantiation plan* says how the concrete surrogate meets them.

## The setting (`ChainTilt.lean`)

- `KilledChain σ`: a finite set σ of living states, `Q x y ≥ 0`, `∑ y, Q x y ≤ 1`; `death x = 1 - ∑ y, Q x y`.
- `IsQSD μ lam`: μ ≥ 0, ∑ μ = 1, μQ = lam·μ (on living states).
- `survival μ t = ∑_y (μ Q^t)_y` = P_μ(T > t); `lifetime μ = ∑' t, survival μ t` = E_μ T. **The path space is not
  constructed**: E_μ T is defined as the sum of the survival probabilities, which is what it equals for an ℕ-valued
  T. `IsQSD.survival_eq`: P_μ(T > t) = λ^t. `IsQSD.lifetime_eq`: τ = 1/h, h = ∑ μ d = 1 − λ.
- `LocalDeath V`: `death x = ∏_{i ∈ V} d_i x` with `0 < d_i ≤ 1` (the product kernel plus (K)); `cost i = -log d_i`
  (ε_i), `energy = ∑_i cost i` (E), `price μ i = ∫₀¹ ⟨ε_i⟩_s ds` (c_i).
- `tiltMean μ E s f = E_μ[f e^{-sE}] / E_μ[e^{-sE}]` (⟨f⟩_s), `Z μ E s = E_μ e^{-sE}`.

## Theorem 2, the tilt identity: done in full

Lean statement (variables of the section: `{σ : Type*} [Fintype σ] [DecidableEq σ] {K : KilledChain σ}`):

```lean
theorem tilt_identity {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) :
    log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧
    log (K.lifetime μ) = ∑ i, L.price μ i ∧
    Antitone (fun s => tiltMean μ L.energy s L.energy) ∧
    tiltMean μ L.energy 1 L.energy ≤ log (K.lifetime μ) ∧
    log (K.lifetime μ) ≤ tiltMean μ L.energy 0 L.energy ∧
    tiltMean μ L.energy 0 L.energy = ∑ x, μ x * L.energy x
```

Around it: `neg_log_Z_one` (the analytic core, −log E_μ e^{−E} = ∫₀¹⟨E⟩_s ds for any probability vector and real E,
by the fundamental theorem of calculus on log Z); `tiltMean_antitone` (d⟨E⟩_s/ds = (N² − MZ)/Z² ≤ 0, Cauchy–Schwarz
as ∑ w (E Z − N)² ≥ 0); `integral_tiltMean_bounds`; `price_mem` (c_i ∈ [0, ε_max]); `IsQSD.last_living_law`
(μ₁ = μ d / h is the law of X_{T−1}: ∑_t P_μ(X_t = x) d(x) = μ(x) d(x)/h).

Existence of μ, for every face (`ChainExist.lean`): `KilledChain.exists_qsd` (every finite killed chain on a nonempty
set has a quasi-stationary law: perturb to Q + J/(k+1), take Wielandt's positive Perron vector, normalise, extract a
convergent subsequence in simplex × [0, 1 + |σ|]); `tilt_identity_exists` (Theorem 2 on every face, hull faces and
strips included, where Lemma 0 is not available); `ProductKernel.tilt_identity_product` (every product kernel
P(x,y) = ∏_i (a_i(x) or 1 − a_i(x)) with 0 ≤ a_i < 1, i.e. S(G) for any face).

Perron–Frobenius, built here because Mathlib has none (`ChainPerron.lean`): `exists_pos_eigenvector` (an irreducible
non-negative matrix on a finite set has a strictly positive eigenvector, eigenvalue ≥ 0: Wielandt's argument,
maximising min_i (Av)_i/v_i on the compact image of the simplex under the positive matrix ∑_{k≤N} A^k);
`exists_pos_left_eigenvector`; `left_eigen_pos`; `left_eigenvalue_eq`; `left_eigen_unique`;
`KilledChain.qsd_exists_unique` (one irreducible class C with Q u u > 0 for some u ∈ C, every other state dying surely
and entered from C ⇒ exactly one QSD with λ > 0, charging every state); `KilledChain.price_invariant` (with that
uniqueness, a symmetry (g of states preserving Q, π of cells carrying d_i along) gives c_{πi} = c_i: one price per
orbit, the "one price per orientation" clause).

**Differentiability of the top eigenvalue is not needed**, and was not built: the paper's tilt is a tilt of μ, not of
the matrix, and Z(s) = ∑_x μ(x) e^{−sE(x)} is a finite sum of exponentials.

## Theorem 1, Lemma 0, Lemma R: done; Lemma 0's geometry is a hypothesis

- `KilledChain.upper_bound`: log τ ≤ E_μ[E] ≤ ε_max·A, for any chain with local factors and any QSD.
- The constant (`ChainCoins.lean`): `threeCoins_death_ge` (a cell with coins (2,1) and k ≤ 6 dies with probability
  ≥ min(ρ1²ρ2, (1−ρ1)²(1−ρ2)): every one of its 14 death events contains b = 0 or b = 3); `twoCoins_death_ge` (hull
  corners, coins (2,0), k ≤ 2: the same bound; the rule used is `Gump.rule` by `aliveNext_eq_rule`); `upper_bound_coins` (log τ ≤ −log min(...)·A); `emax_main`
  (−log(0.44²·0.42) ≤ 2.51, via e^{2.51} ≥ ∑_{i<16} 2.51^i/i!); `emax_fair` (≤ 2.08 at ½, ½).
- Lemma 0 (`ChainLemma0.lean`, `ChainInst.lean`): `SubsetChain.lemma0` (states = subsets of the cells; possible
  successors of x = subsets of M(x) (step (1)); hypotheses: (2) singletons communicate, (3) some u has M(u) = V,
  (4) u reachable from a singleton; conclusion: the states with M ≠ ∅ form one irreducible class, Q u u > 0, every
  other state dies surely, every state is entered from u); `SubsetChain.lemma0_qsd` (hence exactly one QSD with
  λ > 0, positive everywhere); `ProductKernel.supp` (step (1) for product kernels with (K)); `KilledChain.one_class`
  (the abstract form: some living u with Q u y > 0 for every living y, and every state that can survive one step
  reaches u ⇒ uniqueness and positivity; this is the form to instantiate on bit-mask states).
- Lemma R (`ChainRoutes.lean`): `routes_first` (d log τ/dA = ∑ p_r c_r), `routes_second` (d/dA ∑ p c = −∑ p (c − c̄)²
  + ∑ p c′), `log_odds`, `routes_concave` (constant prices ⇒ concave log τ, any number of routes),
  `two_routes_step` (the referee's exact discrete step c_s − log(1 − p(1 − e^{−(c_b − c_s)}))).

## The seam identity and Theorem 3: done; (SSM) is a hypothesis, and a weaker one is proved sufficient

Seam (`ChainSeam.lean`): bands in a finite set B, transfer matrix F ≥ 0; torus of m = M+1 bands cut at the seam,
(a, xs); cover of N = m + L bands cut at the seam and at its image, (a, xs, c, ys). `coverW_eq_ringL` and
`torusW_eq_ringL`: the cut weights are the products of F round the ring. `sum_pathF` (Chapman–Kolmogorov),
`torusZ`/`coverZ` (normalisations Tr F^m, Tr F^N), `cover_marginal`, **`seam_identity`**: for F ≥ 0 and L = k·m,
P_T(a, xs) = P_C(a, xs, image = a)·Tr F^N / (Tr F^m · (F^L)(a,a)); `seam_identity_obs` (the window form ★ for any
observable); `PT_seam`; `seam_sharp` (the referee's K = 2 form, P_C(seam, rest, image = seam) = P_T(seam, rest)·
P_T(seam), under Tr F^m = Tr F^{2m} = 1). The modelling step, that gump's space-time weight factorises into one F on
bands two graph steps thick and that the cover has the same F, is the hypothesis (the ring weight), not derived.

Theorem 3 (`ChainSSM.lean`): `Face` bundles a chain, local factors, a QSD and a number r_i per cell. `SSM` is the
paper's hypothesis with the referee's repair: |⟨ε_i⟩_{s,G} − e_∞(s)| ≤ K e^{−r_i/ξ} + K₀/A for all G, i,
s ∈ [0,1]. `IntSSM` is what the proof uses: the same bound on c_i(G) − c_∞. `SSM.toIntSSM` (needs e_∞ integrable),
`thm3a` (|log τ − c_∞A| ≤ K ∑ e^{−r_i/ξ} + K₀), `thm3b` (r_i ≥ (ℓ−2)/2 ⇒ ≤ K A e^{−(ℓ−2)/2ξ} + K₀), `thm3c` (at most
C·R cells at each integer distance ⇒ ≤ K C R/(1 − e^{−1/ξ}) + K₀), `thm3d` (A → ∞ and ∑ e^{−r_i/ξ} = o(A) ⇒
log τ/A → c_∞).

Weaker hypothesis, proved sufficient (`ChainTiltLimit.lean`): `tilt_riemann_bounds` ((1/n)∑_{k=1}^{n}⟨E⟩_{k/n} ≤
log τ ≤ (1/n)∑_{k=0}^{n−1}⟨E⟩_{k/n} on every face, width ≤ ε_max A/n, from monotonicity alone) and
**`price_of_pointwise`**: along any sequence of faces with costs ≤ ε_max, if ⟨E⟩_{s,G_n}/A_n → f(s) for every
s ∈ (0,1] — at any rate, not uniformly, with no spatial locality, and with jumps of f allowed — then
log τ/A → ∫₀¹ f. So Theorem 3 (d)'s "one price for rimmed and wrapped faces" follows from the two families having the
same pointwise limit of the per-cell tilted energy; a first-order jump along the tilt (the referee's two humps) does
not obstruct it.

## Places where the source needed more than it said

1. **A quasi-stationary law needs λ > 0 to be unique.** The all-alive wrapped face dies surely, so the point mass on
   it solves μQ = λμ with λ = 0 (τ = 1). Lemma 0's "the quasi-stationary law μ is unique" holds among λ > 0
   (`qsd_exists_unique`, `lemma0_qsd`), which the usual definition (P_μ(T > t) > 0) contains silently.
2. **Existence of μ on faces without Lemma 0** (hull faces, strips) is used and not proved in the source: proved
   here for every finite killed chain (`exists_qsd`); uniqueness there remains unproved.
3. **The constant 2.509 is a truncation.** ε_max = −ln(0.44²·0.42) = 2.50946… > 2.509; the argument gives
   ln τ ≤ 2.50946·A, proved as ≤ 2.51·A. (ln τ ≤ 2.509·A is true of the surrogate, but not by this argument.)
4. **c_∞ = ∫e_∞ needs e_∞ integrable** (`SSM.toIntSSM` takes it as a hypothesis); and only the integrated bound is
   used by (a)–(d), so the hypothesis "uniform in s" is stronger than the proof needs.
5. **The seam identity divides by the cover's recurrence weight (F^L)(s,s)**, which can vanish. For F ≥ 0 and a
   cover a whole number of loops long this happens only where the torus's own weight vanishes
   (`pow_mul_diag_ge`: (F^{jm})(a,a) ≥ ((F^m)(a,a))^j), so the identity holds there with both sides 0; for a cover
   whose extra length is not a multiple of the loop it can fail. The sharp K = 2 form needs Tr F^m = Tr F^{2m} = 1
   (the referee's Z = 1), assumed here.
6. **Lemma 0's step (1)** ("by (K) and the product form, the possible next states of x are exactly the subsets of
   M(x)") needs (K) for every cell in every state; proved for product kernels (`ProductKernel.supp`).
7. Lemma R's discrete form: the source's version was already corrected by the referee; the corrected one is proved.

## Instantiation plan (for `GumpMath/Dice*.lean`)

The other agent's chain (`Gump.Dice.Face.P ρ1 ρ2 : Matrix (Fin (2^A)) (Fin (2^A)) ℚ`, states as bit masks, the empty
face 0 absorbing, a_i(x) = `aliveProb ρ1 ρ2 (m1 i) (m2 i) (k x i) (testBit x i)`) is exactly the shape of
`ChainInst.lean`. With S = Fin (2^A), o = 0, P = its matrix cast to ℝ, V = Fin A:

| hypothesis of `surrogate_theorems` | why it holds for the surrogate | how to check |
|---|---|---|
| `hP`: P ≥ 0 | products of a_i, 1 − a_i ∈ [0, 1] | their `P_nonneg`, cast |
| `hrow`: ∑_y P x y = 1 | ∏_i (a_i + (1 − a_i)) expanded over bit masks | induction on A splitting y by its top bit (about 40 lines if not already in `Dice*`) |
| `hprod`: P x 0 = ∏_i (1 − a_i x) | testBit 0 i = false | `simp` |
| `ha0`, `ha1`: 0 ≤ a_i < 1 (K) | every cell has coins (2,1) and k ≤ 6, or (2,0) and k ≤ 2 (hull corners) | `decide` on the face's `m1`, `m2`, `nb` lengths; then 1 − aliveProb = `death3`/`death2` (a finite case check over s, k) and `threeCoins_death_ge`/`twoCoins_death_ge` |
| `hatom`: 1 − a_i ≥ min(ρ1²ρ2, (1−ρ1)²(1−ρ2)) | the same two lemmas | as above |

Then `surrogate_theorems` gives, for that face, a QSD, log τ = ∑_i c_i (Theorem 2) and log τ ≤ 2.51·A at
(0.44, 0.42) with `emax_main` (Theorem 1). Their `Gump.Dice.IsQSD` (nonneg, vanishing at 0, total 1, eigen on
non-empty y) converts to mine by `KilledChain.isQSD_of` field for field, so their certified λ-interval
(`qsd_bounds`) and my `IsQSD.lifetime_eq` (τ = 1/(1 − λ)) connect directly. For uniqueness on a wrapped face, use
`KilledChain.one_class` with u = the cells of one orientation: (i) Q u y > 0 for every y ≠ 0, because in u every
cell has k = 2 (two in-layer neighbours of each orientation), so 0 < a_i(u) < 1 for every i and every product term is
positive; (ii) every state that can survive reaches u: x → {i} for i ∈ M(x), singletons → neighbouring singletons
(k_j = multiplicity ≤ 5), and the line-growth path of THEOREMS.md (4) from an X-singleton to u, given per face as an
explicit list of states (each a subset of M of the previous), checked by `decide`. With uniqueness,
`price_invariant` and the translations (bit-mask permutations, a finite check) give one price per orientation.

## What is not done, and the obstacle in each case

- **Lemma 0's geometric steps (2)–(4) for every wrapped face.** They need the kagome layer on the torus (H,K),(0,D)
  as a Lean object, i.e. the other agent's `torus` face; they are hypotheses here (`lemma0`, `one_class`), checkable
  face by face. That translations act transitively on each orientation is likewise not formalised.
- **(SSM) is not proved, and as stated it is probably false** (judgment below).
- **The existence of the price per cell, unconditionally.** Proved: existence and a two-sided interval
  [(a_n − C′)/n, (a_n + C)/n] from one face, under gluing inequalities with defects (`ChainPrice.lean`:
  `price_exists_of_sub`, `price_exists_of_super`, `price_interval`, Fekete's lemma applied to a + C and C′ − a); and
  existence from pointwise convergence of the per-cell tilted energy (`price_of_pointwise`). The fact that blocks it:
  no gluing inequality is known for S. Super-multiplicativity τ(G₁ ∪ G₂) ≥ e^{−C′}τ(G₁)τ(G₂) is the open lower
  bound B2 in another form (two faces with no edges between them have log τ = max, not the sum, so the inequality
  must quantify reseeding across the seam); sub-multiplicativity needs a bound on how much reseeding across a seam
  can lengthen life, and conditioning on survival is a global event that does not factorise over bands, which is why
  the seam identity (a statement about soup-started histories) does not give it.
- Not built because not needed: perturbation theory of the top eigenvalue; that Wielandt's eigenvalue is the spectral
  radius; convergence to the QSD from an arbitrary start.

## Judgment on (SSM), with reasons, and the first step

(SSM) asks that the tilted local means be local *uniformly in s ∈ [0,1]*. Three facts weigh against it for the
surrogate. (i) The referee's tilted laws are two-humped on wrapped faces for s ≳ 0.3, with valley/peak ratio growing
1.2, 3.9, 15 at 12, 18, 27 cells: a first-order transition along the tilt is forming, at which e_∞ would jump while
every finite curve is continuous, so no bound uniform in s can hold near the jump. (ii) Even at s = 0 (spatial mixing
of the quasi-stationary law itself) the standard route is closed: Dobrushin's interaction coefficient of the one-step
kernel, α = 6·max_{s,k}|a(s,k) − a(s,k+1)| + max_k|a(0,k) − a(1,k)|, is 2.923 at (0.44, 0.42) and at least 2.625 at
every coin density (minimum at ½, ½; script below), against the contraction threshold 1. (iii) The QSD is a law
conditioned on survival, a global event, so even a contracting kernel would not make it a Gibbs measure of a local
specification. So: not provable by known methods, and probably false as stated.

What the conclusion actually needs is much weaker and is now a theorem (`price_of_pointwise`): pointwise convergence
of ⟨E⟩_{s,G}/A at each s, with the same limit for the families compared. The first step towards proving that would
be the case s = 0, convergence of E_μ[E]/A, a density-like bulk average of the living state, along one family
(a tube or strip lengthened one unit at a time). Even that needs a gluing inequality for the quasi-stationary law
of two pieces, and that inequality is the same obstacle as in the price section above. A weakened form proved
unconditionally: the Riemann bracket (`tilt_riemann_bounds`), which makes ln τ computable to within ε_max A/n from
n + 1 tilted means, jump or no jump.

## Bearing on the owner's questions

The tilt identity is now a theorem in Lean at full generality: the lifetime of every face of the surrogate is
exactly a sum of local costs (`tilt_identity`, `ProductKernel.tilt_identity_product`), and the price of a cell
depends only on its orbit (`price_invariant`). The new observation: the measured "two kinds of face at one tilt"
does not stop the price from existing. `price_of_pointwise` shows a jump along the tilt is harmless to the
existence and universality of the price per cell; what would make the prices of rimmed and wrapped faces differ is
a different pointwise limit of the per-cell tilted energy, not the jump itself.

## Reproduce

    export PATH=$HOME/.elan/bin:$PATH; cd research/blast/lean/mathlib
    lake build GumpMath.ChainTilt GumpMath.ChainPerron GumpMath.ChainExist GumpMath.ChainLemma0 GumpMath.ChainCoins \
      GumpMath.ChainRoutes GumpMath.ChainSeam GumpMath.ChainSSM GumpMath.ChainPrice GumpMath.ChainInst GumpMath.ChainTiltLimit
    lake env lean AxiomsChain.lean            # every line: [propext, Classical.choice, Quot.sound]
    cd ../../../.. && sh research/blast/lean/check.sh --mathlib
    python3 research/blast/lean/statements.py # merges statements_chain.json (rewrites STATEMENTS.md)

Dobrushin's coefficient (the judgment above; 1 s):

    python3 -c "
    from math import comb
    rule=lambda s,n:(3<=n<=5) if s else n in(4,5)
    def al(r1,r2):
     P=[0]*4
     for c1 in range(3):
      for c2 in range(2): P[c1+c2]+=comb(2,c1)*r1**c1*(1-r1)**(2-c1)*r2**c2*(1-r2)**(1-c2)
     a={(s,k):sum(P[b] for b in range(4) if rule(s,k+b)) for s in(0,1) for k in range(7)}
     return 6*max(abs(a[s,k]-a[s,k+1]) for s in(0,1) for k in range(6))+max(abs(a[0,k]-a[1,k]) for k in range(7))
    print(al(.44,.42), min(al(i/100,j/100) for i in range(1,100) for j in range(1,100)))"

## Not checked

- No second reader has gone through these Lean statements against the source; the rows of `statements_chain.json`
  are my reading. In particular `Face.r` is an arbitrary number per cell: the source's r_i (largest isomorphic ball,
  coin counts included) is not formalised, so (b) and (c) take their geometric inputs as hypotheses.
- The instantiation plan was not carried out: no theorem here is about the other agent's `Gump.Dice.Face.P`. That
  its a_i matches `death3`/`death2` is a claim about two definitions read side by side, not checked by Lean.
- The Dobrushin numbers are from the script above only (no second code).
