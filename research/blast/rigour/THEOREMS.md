# blast/rigour: theorems for the one-layer dice surrogate, and where the others stop

Written 2026-11-18 by agent `rigour`. Every statement is labelled. Proofs are complete unless marked.

## The chain (definition used everywhere here)

A *face graph* G is a finite set V of A cells, each cell i with a list N(i) of in-layer neighbours (at most 6,
repetitions allowed on very small tori) and a number of coins (m1_i, m2_i) ≤ (2, 1). Fix 0 < ρ1, ρ2 < 1.
One generation of the chain **S(G)** from a state x ∈ {0,1}^V: every cell draws, independently of everything,
b_i = Bin(m1_i, ρ1) + Bin(m2_i, ρ2); with k_i(x) = Σ_{j ∈ N(i)} x_j and n = k_i + b_i, the cell is alive next iff
(x_i = 0 and n ∈ {4,5}) or (x_i = 1 and n ∈ {3,4,5}); all cells update at once. So the kernel is a product,

    P(x, x') = Π_i q_i(x'_i | x_i, k_i(x)),

the empty state ∅ is absorbing (a dead cell with k = 0 has n ≤ 3), Q is P restricted to non-empty states,
d(x) = P(x, ∅) = Π_i d_i(x), d_i(x) = 1 − q_i(1 | x_i, k_i(x)).
Graphs: `geom.py` (wrapped faces "torus H K D" = period lattice (H,K),(0,D), every cell with 6 neighbours and
coins (2,1); hull faces; strips), checked against `reference/oracle.py` by `check_graph.py`.
This is gump's rule on the face layer with the three cells beneath every face cell replaced by private coins
(independent *counts*; in gump two neighbouring face cells share a cell one layer in, the "cube lemma").

**Standing assumption (K): every cell can die.** d_i(x) > 0 for every i and x. It holds whenever each cell has its
three coins (live: k ≤ 2 dies on b = 0, k = 3 on b = 3, k = 4 on b = 2, k = 5 on b = 1, k = 6 always; dead: stays dead
on b = 0 for k ≤ 3, on b = 2 for k = 4, on b = 1 for k = 5, always for k = 6), hence on every wrapped face and
strip of `geom.py`; on hull faces the three corner cells have coins (2,0) and two neighbours (k ≤ 2: b = 0
kills or keeps dead), every other cell has three coins (`check_graph.py` prints the counts). **[proved]**

## Lemma 0 (one living class, on wrapped faces) [proved]

*On a wrapped face (every neighbour multiplicity ≤ 5), let L = {x ≠ ∅ : some cell can be alive next}. Then Q is
irreducible and aperiodic on L, every non-empty state outside L goes to ∅ in one step with probability 1, and
every non-empty state is reachable from L. Hence (Darroch–Seneta; `research/theory/exponent/theorems.md` D) the
quasi-stationary law μ is unique, charges every non-empty state, and from μ the death time is exactly geometric:
P_μ(T > t) = λ^t, 1 − λ = h = Σ_x μ(x) d(x), τ := E_μ T = 1/h.*

*Proof.* Let M(x) be the set of cells that can be alive next: live with k ≤ 5, or dead with 1 ≤ k ≤ 5 (three
coins). By (K) and the product form, the possible next states of x are exactly the subsets of M(x).
(1) If M(x) ≠ ∅ then x → {i} for any i ∈ M(x). If M(x) = ∅, x → ∅ surely.
(2) Singletons communicate: in the state {i} a neighbour j has k_j = multiplicity of i in N(j) ∈ [1,5], so
{i} → {j}; the layer is connected.
(3) Let X be the cells of one orientation (say normal axis x) and u = X. A cell of orientation X has among its six
in-layer neighbours exactly two of each orientation (offsets ±(0,2,−2); ±(1,−1,0); ±(1,0,−1)), and so has every
cell; translations preserve orientation, so this holds with multiplicity on every torus. Hence in u every cell has
k = 2 and M(u) = V: **every state is a possible successor of u**, u itself included (aperiodicity).
(4) u is reachable from a singleton {i}, i ∈ X. The X cells form lines along (0,2,−2). Along its line a
singleton grows to the whole line ℓ (live cells have k ≤ 2 and may survive; a dead X cell with a live X neighbour
has k ≥ 1 and may be born; everything else may stay dead). Given a union S of complete X lines: first S → S ∪ Y_S,
Y_S = the Y cells with a neighbour in S (they have 1 ≤ k ≤ 2; cells of S have k = 2 and may survive). In S ∪ Y_S a
cell of S has k = 2 + 2 = 4 and may survive, the Y cells may die, and an X cell p′ of the lines ℓ ± (2,−2,0), ℓ ⊂ S,
is dead with k ∈ {1, 2} (its Y neighbours p′ ± (1,−1,0) each have the X neighbours p′ and p′ ± (2,−2,0)), so it may
be born: S ∪ Y_S → S ∪ {lines ℓ ± (2,−2,0)}. The translations (0,2,−2) and (2,−2,0) generate the layer's
translation lattice, so finitely many rounds give u.
(1)–(4): from any x ∈ L one reaches a singleton, then u, then any state. ∎

For hull faces and strips the same structure is **[measured]**, not proved: `dense.py` finds one dominant eigenvalue
(|λ₂/λ₁| = 0.62–0.81 on the 9-cell shapes) and `qsd.c` from the uniform start agrees with it to 13 digits.

## Theorem 1 (upper bound; B1 of the brief) [proved]

*For S(G) under (K), with ε_i(x) = −ln d_i(x), E(x) = Σ_i ε_i(x) and ε_max = max_{i,x} ε_i(x) < ∞:*

    ln τ(G) ≤ E_μ[E] ≤ ε_max · A.

*With three coins per cell ε_max = −ln min(ρ1²ρ2, (1−ρ1)²(1−ρ2)) (a live cell with k = 3 dies only on b = 3; a
live cell with k = 2 only on b = 0): 2.509 at (ρ1, ρ2) = (0.44, 0.42), 2.079 at (½, ½).*

*Proof.* h = Σ_x μ(x) e^{−E(x)} ≥ exp(−E_μ[E]) (Jensen), and E ≤ ε_max A. ∎

The middle term is a living-state observable: E_μ[E]/A = 0.84 on the 12-cell torus (2,0),(0,2) against the exact
ln τ / A = 0.332 (`qsd … tilt`, line `E_cumulants_per_cell`): the bound is 2.5 times the truth, the worst-case
constant 7.6 times.

**What deterministic gump needs for the same statement.** Exactly this hypothesis, which is false as it stands:
(FE₁) *given the whole past, every pattern of counts (b_i) beneath the face has conditional probability ≥ δ^A.*
In gump the counts of neighbouring face cells share cells (cube lemma), so some states of a face cannot be emptied
in one generation whatever lies beneath (board E10; 187 of the 512 states of the R = 3 hull face). The weakest
hypothesis that would do is (FE_g): *there are g and δ > 0 such that from every state of the vessel, conditionally on
the past, the face is empty g generations later with probability ≥ δ^A.* Then τ ≤ g δ^{−A}. For a deterministic
vessel "conditionally on the past" has no content (the future is a function of the present); the statement has
to be made for the stationary ensemble of a slab with w ≥ 5 layers over coins, where the unknowns are g (two
generations suffice on the faces the swarm enumerated; unknown beyond 18 cells) and δ.

## Theorem 2 (the tilt identity: ln τ is exactly a sum of local costs) [proved]

*For S(G) under (K), and for s ∈ [0,1], let μ_s(x) ∝ μ(x) e^{−sE(x)} and ⟨·⟩_s its mean (μ_0 = μ, the living
state; μ_1 = the law of the last living state before death). Then*

    ln τ(G) = ∫₀¹ ⟨E⟩_s ds = Σ_{i ∈ V} c_i(G),   c_i(G) = ∫₀¹ ⟨ε_i⟩_s ds ∈ [0, ε_max],

*and s ↦ ⟨E⟩_s is non-increasing, so ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀. On a wrapped face c_i depends only on the orientation
of the cell i (translations act transitively on each of the three orientations), so ln τ(Λ) = (A/3)(c_X + c_Y + c_Z),
and c_X = c_Y = c_Z when Λ is invariant under the rotation by 2π/3 (equilateral tori): a wrapped face has, exactly
and at every size, at most three local prices, whose mean is ln τ / A.*

*Proof.* Z(s) = E_μ[e^{−sE}] is smooth and positive, Z(0) = 1, Z(1) = Σ_x μ(x) Π_i d_i(x) = Σ_x μ(x) d(x) = h
(Lemma 0, or Theorem D for any quasi-stationary μ). (ln Z)′(s) = −⟨E⟩_s and (ln Z)″(s) = Var_s(E) ≥ 0. Integrate
from 0 to 1 and expand E = Σ_i ε_i. μ_1(x) = μ(x) d(x)/h is the law of X_{T−1} under P_μ. ∎

*Check.* `./qsd graph 0.44 0.42 4000 1e-13 0 tilt` prints Σ_i c_i (32-point Gauss–Legendre in s) beside ln τ:
they agree to 12 digits on every shape run (e.g. hull R = 3: 2.483715746334 both).

What the identity is for. It turns "the price per cell" into an expectation of a *local* observable, at the cost of
an integral over a one-parameter family of measures that interpolates between the living face and the dying one.
(i) A wrapped face has *exactly* one price per cell at every size; a rimmed face has an exact price map
(`price_map`), and "rim term", "corner term" are sums of c_i − c_bulk over cells. (ii) Shape can enter only
through the dependence of the local means ⟨ε_i⟩_s on the far geometry, at some s. (iii) The cumulant expansion
ln τ = κ₁ − κ₂/2 + κ₃/6 − … of E under μ is the Taylor series of −ln Z at s = 0 evaluated at s = 1. It is useless
here: on the 12-cell torus the partial sums are 10.08, 1.82, −2.27, 3.15 against 3.98. A Gaussian "tangent"
estimate in the *energy* is therefore not available; the tilt has to be followed, not expanded.

## Theorem 3 (structure of the exponent; B4 of the brief) [proved, conditional on (SSM), which is not proved]

Let 𝒢 be a class of face graphs cut from the kagome layer (wrapped faces, and polygons with a free rim). For a
cell i of G let r_i(G) be the largest r such that the ball of graph radius r about i in G is isomorphic to the ball
in the infinite layer (so r_i ≤ distance to the rim, and r_i < half the length of the shortest loop through i).

**(SSM) Uniform strong spatial mixing along the tilt.** There are e_∞: [0,1] → ℝ and K, ξ < ∞ such that for all
G ∈ 𝒢, i ∈ G, s ∈ [0,1]:  |⟨ε_i⟩_{s,G} − e_∞(s)| ≤ K e^{−r_i(G)/ξ}.

*Theorem. Under (SSM), with c_∞ = ∫₀¹ e_∞(s) ds:*
*(a) |ln τ(G) − c_∞ A| ≤ K Σ_i e^{−r_i(G)/ξ} for every G ∈ 𝒢.*
*(b) Wrapped faces with shortest loop of graph length ℓ: |ln τ − c_∞ A| ≤ K A e^{−(ℓ−1)/2ξ}.*
*(c) Polygons with n_r cells at graph distance r from the rim: |ln τ − c_∞ A| ≤ K Σ_r n_r e^{−r/ξ} ≤ K′·(rim length).*
*(d) Hence along any sequence in 𝒢 with rim length/A → 0 and ℓ → ∞, ln τ / A → c_∞: **the same number for rimmed
and wrapped faces. Two bulk prices are impossible under (SSM).** A difference of 0.02 per cell between a rimmed and
a wrapped family at 63–108 cells must then be one of: a rim term linear in the rim (b·rim/A is 0.02 at these
sizes for b of order 0.05–0.1 per rim cell), corner terms, or a failure of (SSM).*

*Proof.* (a) is Theorem 2 with the triangle inequality. (b): r_i ≥ (ℓ − 1)/2. (c): r_i = distance to the rim for a
polygon without loops; Σ_r n_r e^{−r/ξ} ≤ (rim cells)·C(ξ) for convex polygons. (d) follows. ∎

*Refinement (stated, proof the same).* If in addition the local means near a straight rim, and near a corner of each
angle, converge at the same rate to those of the half-plane and of the wedge (SSM for the reference geometries),
then ln τ(G) = c_∞ A + b·(rim length) + Σ_corners a(angle) + O(e^{−(shortest side)/ξ}) on polygons, and
ln τ(Λ) = c_∞ A + A·Σ_v g(v) + (higher order in the images) on tori, where the sum is over loop vectors and
g(v) = O(e^{−|v|/2ξ}) is the first-order effect of one periodic image on the integrated local mean: **additivity
over loop vectors is the first order of an image expansion, and it is a discount per cell, proportional to A.**
In this form a total discount growing like (length)² at fixed girth is impossible: every discount is ≤ ε_max·A and,
under (SSM) for the infinite tube of that girth, ln τ = c_tube(girth)·A + O(1).

**Where (SSM) can fail, exactly.** (SSM) at s = 0 is spatial mixing of the living state (measured in gump: f falls
like e^{−2.3|v|}). The identity needs it for *every* s ≤ 1, i.e. for the face conditioned to be ever closer to
death. It fails iff the tilted family has a phase transition at some s* < 1 in the limit of large faces: two
coexisting kinds of face (full and sparse) at the same tilt, a jump of ⟨E⟩_s/A at s*, Var_{s*}(E) of order A²,
and correlations as long as the face. Then the bulk term is still ∫ of the two branches, but the corrections are
no longer rim-local: the interface between the two kinds of face inside the face (its length, where it can end)
enters, and that is what distinguishes a tube (two straight interfaces round the girth), a wide torus (a closed
interface) and a polygon (an interface that can end on the rim or sit in a corner). **So the PI's "sweep or flash"
and "long correlations at the point of no return" are one question, and it is decidable on the surrogate:
is s ↦ ⟨E⟩_s/A a smooth curve as A grows, or does it steepen into a jump?** `qsd … tilt` prints the curve
(`tilt_path`); the README gives it for the shapes solved.

For gump itself the hypothesis is the same statement about the slab over coins (w ≥ 5), with E replaced by
−ln P(face empty g generations later | present state): no longer a sum over cells, but a sum over the cube
triples of the face up to interaction through shared cells. Not proved; the measured facts that bear on it are
"a depleted face thins as one thing" (for a flash) and "single deaths are lopsided" (against).

## Lemma R (routes; curvature is minus the variance of the branch prices) [proved]

*Let the deaths of a family of faces indexed by a size A be partitioned into routes r (any measurable property of
the path before death), h(A) = Σ_r h_r(A), p_r = h_r/h, c_r = −d ln h_r/dA. Then*

    d ln τ/dA = Σ_r p_r c_r,     d² ln τ/dA² = −Var_p(c) + Σ_r p_r c_r′,

*and for two routes d ln(p₁/p₂)/dA = c₂ − c₁. In particular two routes each exactly exponential in A give a ln τ
that is concave, with slope moving from the larger price (small A, if that route has the larger prefactor) to the
smaller, and the curvature is −p(1−p)(c₁ − c₂)².*

*Proof.* ln τ = −ln Σ_r h_r; differentiate twice, using h_r′ = −c_r h_r. ∎ (For integer A read differences; the
statement is then exact for the mixture of exponentials and approximate otherwise.)

Use (README, claim 5; **[measured]**): on the surrogate's tube (1,1),(0,D) the log-odds of "bust" against "starve"
fall by 0.29 per unit of length and the step of ln τ falls from 0.85 to 0.69 between D = 7 and D = 13, by p·0.29 to
within the errors: a price that falls with length there is the crossover between two branches of one killed chain.
The two-branch structure is also the expected failure of (SSM) in Theorem 3: at the tilt where the two kinds of
dying face have equal weight the tilted measure is a mixture and its local means are not local.

## Where the others stop

**B2 (a lower bound e^{cA}).** Not proved, for any density. What is established here:
- *No monotone one-step minorant* (board, graveyard 14) is confirmed in the strongest form for S(G): by (K) no
  cell is ever safe, and by Lemma 0 (3) there is a state from which the face dies in one step with the *largest*
  possible entropy of outcomes; any comparison must use several generations.
- *The smallest block cannot be one unit cell wide* **[measured, exact]**: free strips one unit cell wide are
  subcritical, ln τ = 2.80, 2.64, 2.45, 2.31 for 9, 12, 15, 18 cells (falling with length), and patches 1 × D have
  ln τ ≈ 1.9–2.1 at every length. Strips two unit cells wide do grow (README table). A block event must
  therefore live on at least 2 unit cells of width, and the exact transfer product reaches 18 cells with a free
  rim: the block probability "a 2 × 3 patch alive at time 0 has a live cell in each half at time T whatever its
  outside does" can be computed exactly only as a game against the outside (min over outside histories), which
  `qsd.c` does not do.
- *The statement a block proof needs* (not computed): there are a block B (≥ 2 unit cells wide), a time T, a set
  H of block states and ε < ε₀ (ε₀ the constant of the comparison theorem for the 2+1-dimensional 1-dependent
  oriented percolation) such that for every state outside B and every history of the cells outside the 3 × 3
  blocks around B, P(B and its six neighbours are in H at time T | B in H at time 0) ≥ 1 − ε. The dice make the
  outside history adversarial only through the block's rim, one cell per generation; the cap makes the minimum
  over outsides non-trivial (an outside can overcrowd the rim). That minimum is a finite game; nobody has run it.

**B3 (inequalities between shapes).** No inequality is proved. Three are *refuted exactly* for the surrogate as
general statements (README, claim 3): "a tube dies before a wide face of equal area" (false at 9, 12 and 15 cells:
the girth-one tube outlives every other torus solved; and by Monte Carlo tubes of loop² 3 and 4 outlive the wide
tori at 18–42 cells), "ln τ increases with length at fixed width" (false for strips one unit cell wide), "a free
rim costs" (false at 12 and 18 cells: the strips 2 × 2, 2 × 3 and 3 × 2 with two free rims outlive every wrapped
face of equal area; at 18 cells one of the three tori is exact and two are Monte Carlo). Any true inequality must
assume loops and widths above a threshold. The covering relation
is exact only for one step: a state of Λ lifted to an m-fold cover Λ′ has d_{Λ′}(lift x) = d_Λ(x)^m and
P_{Λ′}(lift x → lift y) = P_Λ(x → y)^m; the symmetric states are not invariant under the dice, so nothing follows
for τ. Gluing: two faces with no edges between them have ln τ = max, not the sum (an empty half stays empty), so
super-multiplicativity τ(G₁ ∪ G₂) ≳ τ(G₁) τ(G₂) is *the* content of the area law (each half reseeds the other),
and it is the lower bound B2 in another form.

**B4.** Theorem 3 is the conditional form. Unconditionally only Theorem 2 is proved (the decomposition, the
bounds ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀, and one price per cell on each wrapped face).
