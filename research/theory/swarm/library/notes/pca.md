# Probabilistic cellular automata: ergodicity at high noise, and the space-time Gibbs picture

Request (lead, item 6): Lebowitz–Maes–Speer 1990; the Mairesse–Marcovici survey; criteria for exponential
mixing at high noise. Tags: **[paper]**, **[abstract]**.

## 1. Lebowitz, Maes and Speer 1990

J. L. Lebowitz, C. Maes and E. R. Speer, "Statistical mechanics of probabilistic cellular automata",
J. Statist. Phys. 59 (1990), 117–170, DOI 10.1007/BF01015566. **Abstract only** (Springer; paywalled).

**[abstract]** They "exploit, whenever possible, the correspondence between stationary measures on the
space-time histories of PCAs on Z^d and translation-invariant Gibbs states for a related Hamiltonian on
Z^{d+1}. This leads to a simple large-deviation formula for the space-time histories of the PCA and a proof
that in a high-temperature regime the stationary states of the PCA are Gibbsian." They "demonstrate
uniqueness of the invariant state and exponential decay of correlations in a high-noise regime", discuss
phase transitions at low noise and "review Toom's proof of nonergodicity of a certain class of PCAs".

## 2. Marcovici, Sablik and Taati 2019: an explicit high-noise criterion

Citation and access as in `algebraic-ca.md` §5. Read: §2.2–2.4, §3.2.

**[paper]** A PCA Φ on S^{Z^d} with neighbourhood N is *uniformly ergodic* if it has a unique invariant measure
π and, for every finite A, d_A(t) = sup_x ‖π − Φ^t(x, ·)‖_A → 0.

- **Proposition 2.1.** If d_A(t) ≤ ρ_{|A|}(t) with ρ_n(t) → 0 (the speed depends on the size of A only, not its
  shape), then π is spatially mixing.
- **Theorem 3.5.** Let p_?(Φ) = 1 − Σ_b min_{a_1…a_m} φ(a_1, …, a_m)(b) (one minus the total mass that all the
  local transition laws have in common), and p_c(N) the critical value of (d + 1)-dimensional directed site
  percolation with neighbourhood N (p_c(N) ≥ 1/|N|). If p_?(Φ) < p_c(N), then Φ is uniformly ergodic, π is
  spatially mixing and can be sampled perfectly. Proof: the "envelope" automaton, in which a symbol "?"
  (unknown) spreads only through sites where the update actually looks at its neighbours, is dominated by
  subcritical directed percolation.
- **Proposition 3.6, Corollary 3.7.** A deterministic automaton followed by zero-range noise θ is uniformly
  ergodic if Σ_b min_a θ(a, b) > 1 − p_c(N); for memoryless noise (erase with probability ε, replace by a fresh
  symbol) if ε > 1 − p_c(N).
- Other classes treated (their table): nilpotent rules under small perturbation; rules with a spreading
  symbol; gliders with annihilation; permutive rules with permutation noise (Theorem 3.16, see
  `algebraic-ca.md`); surjective rules with additive noise (only "ergodicity modulo shift"); XOR with any
  positive zero-range noise. Their introduction: the only known one-dimensional rule that stays non-ergodic
  under small positive noise is Gács's; in higher dimensions, Toom's family.

## 3. Not obtained

J. Mairesse and I. Marcovici, "Around probabilistic cellular automata", Theoret. Comput. Sci. 559 (2014),
42–72: not on arXiv; HAL record hal-01194762 has no file; ScienceDirect refuses automated clients. The
update-function formalism it surveys is in Bušić–Mairesse–Marcovici (arXiv:1010.3133), see
`source-requests.md` §1.

## Does it apply here?

- A face or edge driven by independent layers beneath is a PCA on the face (the layers are the noise), but
  the noise is **not zero-range and not positive**: the empty face is absorbing, so the PCA is trivially
  "ergodic" towards the empty state on an infinite face only if it dies, and the interesting object is the
  survival. Theorem 3.5 gives uniqueness (hence, with an absorbing state, extinction), not a lifetime.
  Read the other way, it is a *sufficient condition for a dice model to be boring*: if the dependence of a
  cell's update on its face neighbours is weak enough (p_? < p_c(N)), information does not percolate in
  space-time and the infinite face dies.
- p_?(Φ) is computable by hand for any explicit dice model (it needs only the local transition table), so the
  criterion is a cheap check of which side of the percolation threshold a proposed model is on.
- The Lebowitz–Maes–Speer correspondence (stationary space-time law of a d-dimensional PCA = Gibbs state in
  d + 1 dimensions, with a large-deviation formula) is the standard frame for "the probability of a rare
  space-time configuration is the exponential of minus its cost"; it is proved at high noise. It needs
  positive transition probabilities, which a rule with an absorbing state does not have.

## Corrections to this repository

- `requests.md` item 6, "criteria for exponential mixing at high noise": the explicit criterion I could read
  (Theorem 3.5) asserts uniform ergodicity and spatial mixing; exponential decay of correlations at high noise
  is claimed in the Lebowitz–Maes–Speer abstract, which I could not open further.
- `requests.md` item 6 gives the survey's year as 2014: confirmed (Theoret. Comput. Sci. 559, by the HAL
  record); the page range is from a search listing, not verified.
