## Why "0.2099 against 0.2087" is bookkeeping [proved; three lines]

Write n_A(p) for the number of face-generations with population p, ℓ_A(p) for the number of launches at p, E for the
exposure, M for the deaths. Then ν = n/E, d = ℓ/n, and ν(p)·d(p) = ℓ(p)/E = w_A(p)/τ, where w_A = ℓ/M is the launch
histogram (it sums to 1). The "sum rule" Σ ν·d = 1/τ is therefore Σ w_A = 1: true for ANY rule that gives each death
one launch generation, whatever the dynamics. Taking logarithms at p = θA and differentiating in A, for any set of
sizes and any (common) way of fitting the slope,

    I_up(θ) + J(θ)  =  [slope of ln τ over the sizes used]  −  d/dA ln( √A · w_A(θA) ).        (*)

The left side contains nothing that is not in the lifetimes and in the shape of the launch histogram. If the hump is
a Gaussian of s.d. σ_A ∝ A^γ cells around θ*A, the second term at θ* is (γ − ½)·d ln A/dA, so

    min_θ [I_up + J] = c_τ(sizes used) + (γ − ½)/A,   and   I_up + J − min = the narrowing of the hump in θ.

- If ν and d both obey a large-deviation law at fixed θ (the Laplace picture claim 2 assumes), the hump is √A wide
  (γ = ½) and the minimum IS the lifetime's slope over the sizes used, identically. The sum over p then adds only a
  constant to ln τ (boom's √A in front of ν is the right normalisation for that case, and only for that case).
- If the hump keeps its shape as a fraction of A (γ = 1, what claim 1 says in words), I_up + J is flat in θ, there
  is no minimum, and the sum over p contributes −ln A to ln τ (a term that does grow with A; slope −1/A).
So the number can only come out near 0.2087 if the lifetimes of the sizes used have that slope. They do not:
the anchors' slope is 0.2158 for 48→63, 0.2120 for a line through 48, 63, 75, 0.2068 for 63→75.
