# path: journal (append-only)

Line: death as the least unlikely route to empty. A successor should read `claims.md` first (the current list),
then this file. Tags: **[proved]** (proof here), **[sketched]**, **[guessed]**, **[data]** (a reading of numbers
already committed in the repository, with the file; no new runs).

---

## 2026-11-13, entry 1. Conventions

**1.1 The face as a driven system.** V = vessel, F = one face (gump: the layer d·(p − c) = R of a hull, or an
outer layer of a slab; toy: row 0 of a strip or box), A = |F|. For c ∈ F write

- N_F(c) = neighbours of c inside F ("in-face"): at most 6 in gump (exactly 6 away from the rim; T1), at most 4 in
  the toy (x ± 1, x ± 2);
- B(c) = neighbours of c in V \ F ("beneath"): at most m, with **m = 3 in gump** (two in the layer R − 2, one in the
  layer R − 4; T1) and **m = 2 in the toy** ((x,1), (x,2)).

State x_t ∈ {0,1}^V; ξ_t = x_t restricted to F; k_t(c) = number of live cells in N_F(c); b_t(c) = number of live
cells in B(c); n_t = |ξ_t| (face population). With θ = m + 1 (the smallest birth count: 4, 3) both rules read

    ξ_{t+1}(c) = 1   iff   θ ≤ k + b + ξ   and   k + b ≤ θ + 1.            (F)

(gump: n + x ≥ 4 and n ≤ 5; toy: n + x ≥ 3 and n ≤ 4.) The face sees the rest of the vessel only through the
numbers b_t(c) ∈ {0, …, m}. The whole of confinement is the inequality m < θ.

The gump face cell, from (F), b ∈ {0,1,2,3}:

| k (live in-face) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| live cell survives iff | b = 3 | b ≥ 2 | b ≥ 1 | b ≤ 2 | b ≤ 1 | b = 0 | never |
| dead cell is born iff | never | b = 3 | b ≥ 2 | b ∈ {1,2} | b ≤ 1 | b = 0 | never |

(The toy's table is Lemma A of `research/theory/exponent/theorems.md`.) Differences that matter later: the toy has
a *safe* live cell (k = 2 survives for every b); gump has none, and has a *doomed* one (k = 6).

**1.2 What lies beneath, in gump.** Each cell of the layer R − 4 is beneath exactly one face cell, and each cell
of the layer R − 2 is beneath exactly two face cells, which are in-face neighbours of each other. (T1 read from
below: a cell has one neighbour at Δs = +4 and two at Δs = +2. Checked by offsets for an x-normal face cell p,
d = (1,1,1): beneath p are p − (1,1,0), p − (1,0,1), p − (0,2,2); the cell p − (1,1,0) is y-normal, its upward
neighbours are p and p + (−1,0,1), and (−1,0,1) is an in-face offset of p.) So every face cell has one *private*
cell beneath it. In the toy both cells beneath are private to the column.

**1.3 Which τ.** Probability space: the initial state x_0 with a product law (a soup); the dynamics is the
deterministic map. T = first time ξ_t ≡ 0. Per = the set of periodic states (forward invariant).
S_t = {T > t and x_t ∉ Per} (in strips: and not yet cut) is "alive and under observation at t";
D_{t+1} = S_t ∩ {T = t + 1}; the rest of S_t \ S_{t+1} is censored at t + 1. Hazard and censoring rate:

    h_{t+1} = P(D_{t+1} | S_t),      s_{t+1} = P(S_t \ (S_{t+1} ∪ D_{t+1}) | S_t).

The measured h of the board ("Definitions") is the exposure-weighted mean of h_t over t > T0, pooled over faces;
τ = 1/h. Every bound below is on h_t for each t in a stated window, and so passes to that mean.
"Area law" means: constants c, C with e^{−CA} ≤ h_t ≤ e^{−cA + C} on the window. The lower bound on h is the easy
side (board, "Upper bounds of the right form"); the upper bound on h, i.e. τ ≥ e^{cA}, is what nobody has.

**1.4 Words.** A *hole* is a set D ⊆ F on which ξ_t = 0; int_F D = {c ∈ D : N_F(c) ⊆ D}; the *rim* of D is
D \ int_F D. A *flash* is a death in which the face goes from an ordinary population to empty in a number of
generations that does not grow with A. A *front route* is a death in which holes grow for a time that grows with
the linear size of the face.

---

## 2026-11-13, entry 2. Lemma 1 (the rim lemma) and what it does to the picture

**Lemma 1 [proved].** Let D ⊆ F with ξ_t = 0 on D. Then ξ_{t+1} = 0 on int_F D, whatever the rest of x_t is.
Hence ξ_{t+s} = 0 on int_F^s D for every s ≥ 1.

*Proof.* A cell c ∈ int_F D is dead with k_t(c) = 0, so it has n = b_t(c) ≤ m < θ live neighbours. ∎

(For the toy this is Lemma A(ii)/(b) of `exponent/theorems.md`; for gump it is the sentence "a hole in a face
heals from its rim" of the toy2d README. It is the T2 argument applied inside the face.)

Consequences, all [proved], all immediate:

- **(a) The live set of the face spreads at speed ≤ 1 in the in-face graph:** supp ξ_{t+1} ⊆ N_F[supp ξ_t]
  (closed neighbourhood). So n_{t+s} ≤ (4s + 1)·n_t in the toy, and n_{t+s} = O(s²)·n_t in gump. *Recovery from a
  deep dip is slow by a theorem; nothing makes death slow.* Relative to its environment the face is a
  contact-type system: vacuum is locally absorbing, everything else depends on b.
- **(b) Holes persist:** if D contains the in-face ball of radius ρ about c, then c stays dead for ρ generations.
- **(c) A one-step death is |N_F[supp ξ_t]| constraints, one per cell, on the cells beneath:** ξ_{t+1} ≡ 0 iff
  for every live c, k + b ∉ [θ − 1, θ + 1], and for every dead c with k ≥ 1, k + b ∉ {θ, θ + 1}. Dead cells with
  k = 0 impose nothing. By 1.2 each constraint involves a private cell.

*Smallest case by hand (gump, one live cell c, the rest of F dead, c not on the rim).* k(c) = 0: c survives iff all
three cells beneath are alive. Each of its six in-face neighbours has k = 1: born iff all three beneath it are
alive. Every other face cell has k = 0 and stays dead. So n_{t+1} ≤ 7 and the face dies iff seven triples each
contain a dead cell.

---

## 2026-11-13, entry 3. Theorem P: a one-step certificate bounds the hazard, without a Markov property

Setting of 1.3, but nothing about gump is used: (x_t) is any process, S_t ⊇ S_{t+1} ⊔ D_{t+1} any events, Z_t any
statistic defined on S_t (think: the face population n_t, or any function of the face and a few layers beneath).

**Theorem P [proved].** Let φ be a function of the values of Z with 0 < φ ≤ 1, and let a, ε, s̄ ≥ 0 with
a + ε ≤ 1 − s̄. Suppose that for every t ≥ t₀, almost surely on S_t,

    P(D_{t+1} | Z_t, S_t) + E[ φ(Z_{t+1}) 1_{S_{t+1}} | Z_t, S_t ]  ≤  a·φ(Z_t) + ε,          (∗)

and that s_{t+1} ≤ s̄. Then for every t ≥ t₀

    h_{t+1}  ≤  a·(a/(1 − s̄))^{t − t₀}  +  ε·(1 − s̄)/(1 − s̄ − a).

*Proof.* Put w_t = E[φ(Z_t) | S_t] ≤ 1. Multiply (∗) by 1_{S_t} and take expectations (tower property over
σ(Z_t, 1_{S_t}); no other conditioning is used): E[φ(Z_{t+1}); S_{t+1}] + P(D_{t+1}) ≤ a E[φ(Z_t); S_t] + ε P(S_t).
Divide by P(S_t) and use P(S_{t+1}) = P(S_t)(1 − h_{t+1} − s_{t+1}):

    (1 − h_{t+1} − s_{t+1})·w_{t+1} + h_{t+1} ≤ a w_t + ε.                                    (1)

So h_{t+1} ≤ y := a w_t + ε. Also w_{t+1} ≤ (y − h)/(1 − h − s), and (y − h)/(1 − h − s) ≤ y/(1 − s) is equivalent
to y ≤ 1 − s, which holds because y ≤ a + ε ≤ 1 − s̄. Hence w_{t+1} ≤ (a w_t + ε)/(1 − s̄), so
w_t ≤ (a/(1 − s̄))^{t − t₀} + ε/(1 − s̄ − a), and the claim follows from h_{t+1} ≤ a w_t + ε. ∎

**Corollary P1 (the form used).** Take Z integer valued, ≥ 1 on S_t, and φ(z) = r^{min(z, K)} with 0 < r < 1.
If (∗) holds with ε = C·r^K, then after a burn-in of order K, h ≤ C′·r^K with C′ = 2C(1 − s̄)/(1 − s̄ − a):

    −ln h ≥ K·ln(1/r) − ln C′.      If K ≥ κA this is an area law with exponent ≥ κ·ln(1/r).

What (∗) says for this φ, in words: (i) *near-empty faces grow*: for 1 ≤ z < K, the one-step law of Z from Z = z
satisfies P(death) + E[r^{Z′}] ≤ a·r^z (+ C r^K), a < 1; (ii) *no cheap flash*: from z ≥ K,
P(death) + E[r^{min(Z′,K)}] ≤ (a + C) r^K, i.e. a one-step drop of j cells below K has probability O(r^j),
including the drop to zero. The conditioning is on Z_t alone, averaged over everything else with the law the
ensemble actually has at time t. For a deterministic system this is the only kind of conditional statement that
is not trivially 0 or 1, and it is a statement about a measured object: the one-step transition table of the face
population (`Tr[k, k′]` in `research/fluct/qsd.py`).

*Why no Markov property is needed.* One step of total probability is exact for any process:
P(Z_{t+1} = z′, S_{t+1}) = Σ_z P(Z_t = z, S_t)·T_t(z, z′), with T_t the true conditional law at time t. The
theorem only ever composes one step at a time, with the time-t table. What the hypothesis asks is that (∗) hold
for *every* t in the window with the same constants: uniformity in time of a one-step table.

*What it does not do.* For z ≥ K, (∗) assumes that a flash from an ordinary state has probability ≤ (a + C)r^K,
which is already exponentially small in K. So Theorem P does not create the exponential; it transports it: **if
one-step drops of the statistic have an exponential tail at rate ln(1/r) per cell, and small values of the
statistic drift up, then no multi-step route does better than r^K.** It rules out the slow routes, given the
fast ones.

*Sharpness (worked by hand, then by calculator).* Walk on {0, 1, …, K}, absorbed at 0: up with probability p, down
with q = 1 − p < p, the step up from K replaced by staying. With φ(z) = r^z, q/p < r < 1:
E[r^{Z′} | z] = r^z (p r + q/r) for 1 ≤ z < K (the term z′ = 0 is P(death) when z = 1), and at z = K it is
r^K (p + q/r). So (∗) holds with a = p r + q/r < 1, C = p(1 − r), and h ≤ p(1 − r) r^K/(1 − a).
Case K = 2, p = 3/4, r = 1/2: a = 7/8, C = 3/8, bound 3/4; exact h = 1 − λ with λ² − (3/4)λ − 3/16 = 0,
λ = 0.9478, h = 0.0522. Case K = 30, p = 3/4, best r = 0.344: bound 4.0×10⁻¹³; exact 1.8×10⁻¹⁵;
(q/p)^K = 4.9×10⁻¹⁵. Taking r = (q/p)(1 + 1/K) gives bound ≈ e·K·(q/p)^K in general: **the exponent K·ln(p/q) is
recovered exactly, the prefactor is lost by a factor of order K.**

*Reading of the measured numbers [data, soft].* For a walk whose step law does not depend on z, the admissible r
are exactly r₀ < r < 1 where r₀ is the ratio p_z/p_{z+1} of the quasi-stationary tail (row condition and column
condition are the same moment generating function). Gump's tail ratio is ≈ 0.60–0.65 in the middle range
(d ln p_k/dk = 0.43–0.51 for 4 ≤ k ≤ 20 at A = 63, 84, 108; `research/fluct/data/qsd_summary.json`, field `lnp`;
it rises with A: 0.44, 0.46, 0.48, 0.51 at A = 45, 63, 84, 108) and the face population sits at 0.50–0.52·A, so
the certificate would read γ ≥ 0.5 × (0.43–0.51) ≈ 0.22–0.26 if (∗) held up to K ≈ the mean. The measured γ is
0.21–0.22. So the hypothesis, if true with r near the tail ratio, cannot hold all the way up to the mean
population; κ ≈ 0.42–0.5 is the most it can hold to. This is a consistency check on the form, not evidence for (∗).

---

## 2026-11-13, entry 4. What the sealed-set facts are, and what they cannot give

**Lemma 3 (sealed sets are complements of bootstrap-closed sets) [proved].** On any vessel V, with θ = the
smallest birth count: W ⊆ V is sealed iff U = V \ W is closed under θ-neighbour bootstrap percolation (no cell
outside U has θ or more neighbours in U). Consequently, with L_t the live set and ⟨·⟩ the bootstrap closure
(add cells with ≥ θ neighbours in the set, repeat):

    V \ K(t) = ⟨L_t⟩,     L_{t+1} ⊆ ⟨L_t⟩,     ⟨L_{t+1}⟩ ⊆ ⟨L_t⟩,

where K(t) is the largest dead sealed set of `thickness.md`.

*Proof.* "Every cell of W has ≤ θ − 1 neighbours in V \ W" is the definition of both. A sealed W is dead iff
U ⊇ L_t; the smallest closed U ⊇ L_t is ⟨L_t⟩. A cell alive at t + 1 either was alive or had ≥ θ live neighbours,
so it is in the first bootstrap step of L_t. ∎

In this language: T6 says that in three or more layers the complement of any finite set bootstraps to
everything; the critic's exact result (board, lemma exchange) says that in the hulls R ≤ 7 every set of cells
that misses fewer than A cells bootstraps to all of V, and that the only closed sets missing exactly A cells are
the complements of faces. *Smallest case by hand:* one kagome layer, the hexagon ring of six cells: each ring cell
has its two ring neighbours and the opposite ring cell inside, so 3 = θ − 1 neighbours outside; the complement of
the ring is closed. (This is Theorem 4(i) of `thickness.md` re-read.)

**Lemma 4 (top-layer rigidity) [proved].** Let W be sealed in a hull V, d a signed diagonal, and
s* = max{d·p : p ∈ W}. If c ∈ W has d·c = s* and its three d-upward neighbours (two at Δs = +2, one at +4) are
all in V, then *every* other neighbour of c that lies in V is in W. In particular all its in-layer neighbours
in V are in W.

*Proof.* The three upward neighbours are in V \ W because they lie above the top layer of W. That is already 3
neighbours outside W; sealed allows no fourth. ∎

So the top layer of a sealed set, away from the places where it meets the vessel's other faces, is a full layer
of the vessel: sealed sets are bounded by whole {111} sheets. This is the first step toward aim A below; the
work is at the rims, where upward neighbours leave V.

**Remark 5 (the lead's "why area follows from the sealed-set results" is not a theorem as stated) [proved].**
Sealedness, T2, T3 and T6 are statements about the graph and the number θ. They hold verbatim for every
outer-totalistic rule on the same graph whose smallest birth count is θ, for instance the rule "born iff all 12
neighbours are alive, never survive", under which every face is empty at t = 1 (a face cell has at most 9
neighbours in V). So no lower bound on a face's lifetime follows from the sealed-set facts alone. A measured,
non-degenerate instance is already in the repository: Moore B456/S3456 is a capped threshold rule, confined, with
no finite sealed set (toy2d README §2), chaotic on a torus, and its edges *erode*: τ_edge = 508 at L = 12 and 163
at L = 20 (toy2d README §3).
What the sealed-set facts do give is the removal of one obstruction: with a finite sealed set, a dead patch
needs no upkeep and death accumulates (one and two layers). Without one, every hole *can* heal (Lemma 3: it lies
in the bootstrap closure of its complement). Whether it *does*, fast enough, is a property of the chaos, and it
is exactly hypothesis (∗)(i) of Theorem P. The division of labour I propose is therefore:

    structure (T6, Lemma 1):  no hole is protected; a hole can be refilled only from its rim.
    chaos (one hypothesis):   near-empty faces grow, in the one-step exponential sense (∗).
    Theorem P:                then the wait is exponential in the level K up to which (∗) holds.

"Area rather than perimeter" is then the statement K ∝ A. It would fail (K ∝ √A or K = O(1)) exactly if holes
beyond some size tended to grow, i.e. if the vacuum invaded the living face instead of the reverse.

---

## 2026-11-13, entry 5. Three readings of committed data that bear on "flash or front" [data]

No new runs; each is arithmetic on numbers already in the repository. They are here because they change what
this line should try to prove.

**5.1 The toy's edge is not at ordinary density two generations before it dies, once L ≥ 20.**
`research/theory/exponent/PREDICTIONS.md` (outcome of F2) gives the mean edge density two generations before death
as 0.61, 0.55, 0.46, 0.39 at L = 12, 16, 20, 24 (living mean 0.58) and reads it as "a two-generation flash at
every size" (board, graveyard 12). As counts these are 7.3, 8.8, 9.2, 9.4 cells; one generation before death,
3.5, 3.0, 2.6, 2.4 cells. The count is levelling off near 9–10 cells; the density is not constant. What is
size-independent is a final collapse of a remnant of about ten cells. How the edge gets from ≈ 0.58·L cells down to
ten is not in those numbers, and for L ≥ 20 it is not "ordinary until two generations before".
For gump the evidence for a flash is a 10–12 generation plunge on faces of A = 30–84, which are at most about ten
cells across; a front moving one cell per generation would look the same. **Neither system's data decides
between a flash and a front beyond the remnant.**

**5.2 Edges with ends cost 0.34 per independent cell in every geometry; the ring's gap statistics extrapolate to
the same number.** Slopes of ln τ per *orbit* of edge cells (from `research/toy2d/data/law_cross2_B34S234_*.json`,
local slopes between successive sizes):

| edge | orbit space | local slopes per orbit | range |
|---|---|---|---|
| box, no symmetry (`box_none`) | segment, two dead corners | 0.331, 0.347, 0.324, 0.357, 0.342 | L 12–32 |
| box, diagonal mirror (`box_diag`) | segment | 0.330, 0.326, 0.336, 0.391 | L 12–28 |
| strip, mirror ⊥ edge (`mx`) | segment between two mirror points | 2 × (0.174, 0.174, 0.176, 0.169, 0.172) = 0.338–0.352 | L 16–56 |
| box, D4 (`box_d4`) | segment, corner to mirror point | 2 × (0.169, 0.169, 0.177) = 0.338–0.354 | L 20–32 |
| strip, no symmetry | ring | 0.442, 0.407, 0.428, 0.400, 0.421, 0.382 | L 12–36 |
| box, C4 (`box_c4`) | ring with one corner | 0.297, 0.265, 0.283, 0.267, 0.281 | L 16–36 |

And the empty-window probability E(ℓ) of a long ring (`research/theory/exponent/data/gap.json`, key
`gap_H16_L128`): the decrement −ln[E(ℓ+1)/E(ℓ)] is 0.471, 0.434, 0.413, 0.399, 0.390, 0.382, 0.376 at
ℓ = 5, 10, 15, 20, 25, 30, 35, and (decrement − g)·(ℓ + ½) is level in ℓ only for g near 0.345 (g = 0.345: 1.06, 1.11,
1.14, 1.12, 1.12 at ℓ = 15…35; g = 0.355: 0.90, 0.91, 0.88, 0.81, 0.76; g = 0.34: 1.13, 1.21, 1.27, 1.27, 1.29).
That is E(ℓ) ≈ const·ℓ^{−1.1}·e^{−0.345 ℓ}.
So: the stabiliser rule is exact to 2% when the baseline is an edge with ends (this is board E6 seen from the
other side), and the ring's larger, falling slope is consistent with the same exponent 0.345 times a power of L.
**Guess G1: the toy has one exponent, γ₂ = 0.345 ± 0.01, for every geometry; a ring carries an extra factor
≈ L^{+1} in τ; the published 0.41 is pre-asymptotic.** I have no derivation of the power.

**5.3 The C4 box contradicts every local picture I have, including the one above.** Its slope per orbit is
0.277, level over L = 16–36, against 0.340 for the box without symmetry. The rotation sends a cell at distance ϱ
from the centre of the box to a cell at distance √2·ϱ from it, so no cell within L/4 of an edge has an image
nearer than about L/3: locally, near an edge, a C4 state is unconstrained. A front route and a flash route both
price an edge cell by what is within a few cells of it, so both predict the box slope with a changed intercept. Either the C4 slope returns to ≈ 0.34 at larger L (its local slopes show no sign of
it), or the cost of an edge has a part that is not local to the edge. I record this as the fact most likely to
break this line's picture.

---

## Round 1 report

**Definitions fixed** (entry 1): the face as a system driven through b_t(c) ∈ {0..m}, m < θ; hazard h_t among
living unsettled replicas, with censoring; "flash" and "front route".

**Claims.**
- Lemma 1, rim lemma, with (a) speed ≤ 1 for recovery, (b) persistence of holes, (c) a one-step death is one
  constraint per cell of N_F[supp ξ], each involving a private cell beneath. **[proved]**
- Theorem P and Corollary P1: a one-step supermartingale-type inequality (∗) for any statistic of the face, at
  every time of a window, bounds the hazard by ε/(1 − a) after a burn-in; no Markov property; censoring allowed.
  With φ = r^{min(Z,K)}: −ln h ≥ K ln(1/r) − const. Sharp in the exponent on the biased walk. **[proved]**
- Lemma 3: sealed ⟺ complement closed under θ-bootstrap percolation; V \ K(t) = ⟨L_t⟩. **[proved]**
- Lemma 4: the top layer of a sealed set in a hull is a full sheet away from the other faces. **[proved]**
- Remark 5: the area law does not follow from the sealed-set facts alone (a rule with the same graph and θ
  whose faces die at t = 1; a measured non-degenerate example, Moore B456/S3456). **[proved]** for the degenerate
  rule; the Moore example is the README's measurement.
- G1: one exponent γ₂ ≈ 0.345 for the toy in all geometries, rings carrying a power of L. **[guessed]**, from 5.2.

**What I aim to prove.**
- A. *Isoperimetry of sealed sets:* in the hull of every radius R ≥ 3 a non-empty sealed set has at least A(R)
  cells, with equality only for a face (critic: exact for R ≤ 7). Lemma 4 is the first step. This is the
  deterministic content of "area, not perimeter": the cheapest *unconditional* death is a whole face.
- B. *The area law under one hypothesis:* Theorem P with Z = n_t (or a slightly richer statistic), the hypothesis
  being (∗) for the measured one-step table. Next: decide from exact small dice models and from the existing
  tallies whether (∗) can hold with r^K within a polynomial factor of h, and up to which level K/A.
- C. *The route:* state c_flash and c_front as limits, show the exponent is their minimum under the hypotheses of
  B, and say which one it is in each system. 5.1 says the question is open in both.
- D. *Symmetry:* slope = γ/|stabiliser| when the orbit space of the edge is a segment (5.2). C4 is unexplained.

**Weakest step in my own argument.** Part (ii) of (∗): Theorem P assumes that a one-step drop of j cells is
O(r^j), all the way to j = K. That is an exponential-in-K assumption about flashes. The theorem only shows that
slow routes cannot undercut fast ones. If the critic judges that this makes B circular rather than a reduction,
B has to be re-based on a hypothesis about the measure at one time (mixing), and then it coincides with Theorem E
of the exponent study. Second weakness: (∗) must hold uniformly over the window, and I have no argument for that
beyond "the ensemble is quasi-stationary".

**Lab requests.**
- LR1 (existing tallies, no runs; if admissible). From `research/scratch/fluct/qsd_R{7,9,11,13}.npz`, array
  `Tr[k, k′]` (one-step transitions of the face population from k = 1…22; k′ = 0 is death): for
  r ∈ {0.50, 0.55, …, 0.90} and each k, a_k(r) = Σ_{k′} Tr[k,k′]·r^{k′ − k} / Σ_{k′} Tr[k,k′]. Report
  max_k a_k(r), the k where it is attained, and the row totals. (∗)(i) predicts a range of r with
  max_k a_k(r) < 1; Corollary P1 is useful only if that range reaches down to about the tail ratio 0.65.
- LR2 (exact, dice). The w = 1 toy model: ring of L edge cells following (F) with m = 2, the b(x) i.i.d. each
  generation as the sum of two Bernoulli(0.472); L = 8, 10, 12, 14. Compute the quasi-stationary law μ and h;
  the lumped table T(n, n′) = Σ_{|x| = n} μ(x) P(x → {|x′| = n′}) / μ(|x| = n); then, for K = 1…L and r on a grid,
  the smallest ε(r, K, a) for which (∗) holds with φ = r^{min(n,K)} and a = 0.9, 0.95, 0.99, and the resulting
  bound ε/(1 − a) against the true h. Question: how many nats does the population statistic lose?
- LR3 (existing tallies, no runs; if admissible). From the `pre` arrays of the same npz files (last 64
  generations before each death): mean and quartiles of n at lags 1…24 for A = 30, 45, 63, 84, and the lag at
  which the mean falls below half the living mean. A front predicts that this lag grows like √A (about ×1.67 from
  A = 30 to 84); a flash predicts a constant.

**Next.** A (rims of Lemma 4); B after LR1/LR2; a derivation or refutation of the power of L in G1. Candidate exam
entry, not yet filed: in a 16 × 128 *box* (non-periodic), the probability that the ℓ edge cells next to a corner
are all dead has decrement −ln[E_c(ℓ+1)/E_c(ℓ)] = 0.345 ± 0.012 already for 10 ≤ ℓ ≤ 20, with no drift in ℓ
(interior windows of the ring: 0.434 at ℓ = 10, 0.399 at ℓ = 20).

---

## 2026-11-13, entry 6. Exam entries filed (E1, E2)

Filed in `research/theory/swarm/PREDICTIONS.md` at the end of round 1, so that they exist if this line is stopped.
They replace the "candidate exam entry" named in the round 1 report (the corner-window statistic), which I did
not file: its central value depends on an unknown power-law prefactor, and a box with a long edge has short
sides that peel during the run.

- **E1.** Strips 16 × L of the toy with two adjacent cells of row 0 removed (a notch); slope of ln τ of the
  notched row between L = 20 and 32: **0.345 ± 0.020** (intact row: 0.416). Tests G1 ("one exponent; the ring's
  excess is the absence of an end"). Refuted if ≥ 0.39.
  Why the notch anchors a gap: with columns 0, 1 removed, the cell in column 2 has in-row neighbours 0, 1 (gone),
  3, 4; if 3 and 4 are dead it sees at most the two cells beneath it and stays dead. The same on the other side
  (column L − 1 has in-row neighbours L − 2, L − 3, 0, 1). So a dead stretch touching the notch is refilled from
  its far end only (Lemma 1). Two removed cells are needed: across a single removed cell the cells x − 1 and
  x + 1 are still neighbours.
- **E2.** Intact strips: mean edge population two generations before death **9.8 ± 1.0 cells at L = 32 and 36**.
  Tests the reading 5.1. Refuted if ≥ 11.5 at L = 36.

---

## 2026-11-13, entry 7. Corrections after the critic's reply to round 1

(`critic/to-path.md`; lab ids are the board's.)

1. **L1(c) reworded.** "Each constraint involves a private cell" is false at the three corner cells of a hull
   face. The exact statement is the board's cube lemma: the face layer is a disjoint union of triples (the three
   top faces of one cube); beneath a triple lie the three bottom faces u_x, u_y, u_z of the same cube and three
   private cells v_x, v_y, v_z, and b_a = u_b + u_c + v_a. A one-step death is a condition cube by cube. Every face
   cell except the three corners of a hull face has a private cell beneath it; on periodic faces all do.
   Consequence I had not seen: the favoured three-cell remnant (a kagome triangle) is the top of one cube; if the
   rest of the face is dead near it, each of its cells has k = 2 and dies only if u_b = u_c = v_a = 0.
2. **Hypothesis H as stated in round 1 is false** (L1.1, L1.4): with φ = r^{min(n,K)} the rows n = 1, 2 do not
   contract for any useful r, in gump's measured table and in D2. From one cell the face dies with probability
   0.37–0.41 and does not drift up. With φ free on the first rows the certificate works (L1.2, L1.4). H is
   restated in entry 8 as H′. Theorem P itself stands.
3. **G2, gump half, withdrawn.** The existing pre-death histories decide (L1.3): the lag at which a dying face is
   at half its living mean is 3.2, 4.7, 5.9, 6.8 generations at A = 30, 45, 63, 84, and looking back from death
   the mean population is one curve at every size (1.6, 3.4, 6.4, 9.7, 13.6, 17.6 at lags 1…6, A = 84). Gump's
   death is not a flash of fixed length. Entry 11 reads the curve.
4. **R5 reworded.** The rule "born iff 12 alive, never survive" has smallest birth count 12, so it inherits
   "a dead sealed set stays dead" but not the converse (a hole that some outside can refill). Rules that share
   gump's graph *and* θ = 4, hence every sealed-set statement with its converse, are gump's own neighbours with
   one survival count removed (B45/S34, B45/S35, B45/S45): their median lifetimes in the survey's vessel are a few
   tens of generations against gump's 3,420 (`research/CLAIMS.md` Q1; I did not check which number belongs to
   which rule). The measured 2D instance stays Moore B456/S3456. The remark stands: the sealed-set facts do not
   imply the law.
5. **G1's error bar.** What is measured is "edges whose orbit space is a segment cost 0.34 ± 0.01 per orbit, in
   four geometries". The ring's limit is not determined by the committed window statistics (0.35–0.37 depending
   on the assumed approach, L1.6). In D2 the segment is exact to L = 14 (L1.5): its steps are below the ring's, the
   same sign as in the real rule, and too short to decide. G1 remains a guess; E1 tests it.

---

## 2026-11-13, entry 8. Theorem P̄: the pooled form. The hazard is the entry flux times a committor

Theorem P needed its inequality at every time, a contraction a < 1 (which costs a factor 1/(1 − a): three of the
four nats lost in L1.2), and a bound on the censoring rate. None of this is needed if one bounds what is actually
measured: deaths divided by exposure, from the table pooled over the window.

**Setting.** As in entry 3: any process, events S_t ⊇ S_{t+1} ⊔ D_{t+1}, any statistic Z_t on S_t with countably
many values. Fix a window t₀ ≤ t ≤ t₁ and pool:

    N(z)     = Σ_t P(Z_t = z, S_t)                          (exposure at z),     Expo = Σ_z N(z),
    D(z)     = Σ_t P(Z_t = z, D_{t+1})                      (deaths from z),     Deaths = Σ_z D(z),
    F(z, z′) = Σ_t P(Z_t = z, S_t, Z_{t+1} = z′, S_{t+1})   (transitions that stay observed).

Two exact identities: Σ_{z′} F(z, z′) + D(z) ≤ N(z) (the rest is censored), and, because S_{t+1} ⊆ S_t,

    Σ_z F(z, z′) = N(z′) − P(Z_{t₀} = z′, S_{t₀}) + P(Z_{t₁+1} = z′, S_{t₁+1}).                         (I)

**Theorem P̄ [proved].** Let 𝓛 be a finite set of values ("low") and ψ ≥ 0 a function on 𝓛 with

    D(z) + Σ_{z′ ∈ 𝓛} F(z, z′) ψ(z′)  ≤  N(z) ψ(z)      for every z ∈ 𝓛                                  (∗̄)

(ψ is superharmonic, with killing, for the pooled table restricted to 𝓛). Then

    Deaths  ≤  D(𝓛ᶜ) + Σ_{z ∉ 𝓛, z′ ∈ 𝓛} F(z, z′) ψ(z′) + E[ψ(Z_{t₀}); Z_{t₀} ∈ 𝓛, S_{t₀}] − E[ψ(Z_{t₁+1}); Z_{t₁+1} ∈ 𝓛, S_{t₁+1}],

with equality iff (∗̄) holds with equality at every z ∈ 𝓛.

*Proof.* Sum (∗̄) over z ∈ 𝓛: D(𝓛) + Σ_{z,z′ ∈ 𝓛} F ψ(z′) ≤ Σ_{z′ ∈ 𝓛} N(z′) ψ(z′). Replace N(z′) by (I) and cancel the
finite sum Σ_{z,z′ ∈ 𝓛} F(z, z′)ψ(z′) on both sides. Add D(𝓛ᶜ). ∎

In words: **deaths ≤ (direct deaths from above) + Σ over entries into the low set of ψ at the entry point**, plus
a window-boundary term. No Markov property, no uniformity in time, no condition on censoring, no constant a.
If the window is long and the ensemble quasi-stationary the boundary term is w·(Deaths + Censored), w the mean
of ψ over observed states (ψ = 0 off 𝓛), so h̄(1 − w) ≤ [D(𝓛ᶜ) + Σ F ψ]/Expo + w·s̄.

*The best ψ and what the theorem cannot lose.* The smallest solution of (∗̄) is ψ* = (I − T̄_𝓛)⁻¹ d̄ with
T̄ = F/N, d̄ = D/N: the committor "death before leaving 𝓛" of the Markov chain *defined by the pooled table*.
With ψ* the theorem is an identity. So all of the exponent sits in one object:

    h̄ ≈ (rate of entering 𝓛 at z′) × ψ*(z′), summed over z′.

The true process need not be Markov, and ψ* need not equal the true multi-step committor (the tallied p_B);
the identity holds for ψ* regardless, because the pooled table reproduces the pooled flow by construction.

*Worked by hand.* The walk of entry 3 on {0, 1, 2} (up ¾, down ¼, held at 2), 𝓛 = {1}. Quasi-stationary weights
p₁ = 0.2087, p₂ = 0.7913, λ = 0.9478, h = p₁/4 = 0.0522. (∗̄) at z = 1: ψ(1) ≥ d̄(1) = ¼. Entries per unit exposure:
p₂/4 = 0.1978. Entry flux × ψ = 0.0495; boundary term w = ψ(1)p₁ = 0.0522; 0.0495/(1 − 0.0522) = 0.0522 = h. ∎

**Hypothesis H′ (replaces H).** For Z = the population of a hull face of gump, 𝓛 = {1, …, K − 1}, K = κA: the
committor ψ*_K of the pooled one-step table satisfies ψ*_K(k) ≤ C e^{−θk} at the rows k where the population
enters below K, with C, θ, κ independent of A, and no face dies directly from a population ≥ K.
**Then, by Theorem P̄, ln τ ≥ θ(κA − J) − ln C − (window terms)**, J the largest one-step drop into 𝓛.
What is assumed is a property of one-step statistics, level by level: below κA the population has an upward
exponential drift (the content of "holes heal"). What is concluded is the many-step statement.

*Status of H′ against data.* The critic's linear programme (L1.2) is this with a = 0.95: on the measured rows it
gives the measured slope at all four sizes with a constant loss, K/A = 0.43–0.48, φ ratios 0.55–0.63 beyond
k = 3. In the pooled form the loss should all but disappear (lab request LR4). Not tested: rows above A/2 (not
tallied; in the pooled form only their *entries into 𝓛* matter, and those are recoverable from the histogram
and the tallied rows by (I)); sizes beyond A = 84.

*For the 2D rule* the same theorem holds, but there H′ is not a reduction: a fifth to a hundredth of the deaths
go straight from ≥ 7 cells to none and the last steps lose most of the remnant at once (board E9, E14), so the
entry term itself is a statement about exponentially rare one-step events. (The critic's judgement; I agree.)

---

## 2026-11-13, entry 9. Every permanent loss is an extinction on a sealed set

**Lemma 1′ (rim lemma for sealed sets) [proved].** Let W be sealed in V and D ⊆ W dead at time t. Every c ∈ D all
of whose neighbours *in W* lie in D is dead at t + 1. Hence L_{t+1} ∩ W ⊆ N_W[L_t ∩ W] (closed neighbourhood
within W): inside a sealed set life spreads only from life in the set, at speed ≤ 1.

*Proof.* The live neighbours of c are in V \ W, at most θ − 1 of them. ∎

Lemma 1 is the case W = a face (with the outside of the hull). For a T3 firewall W = three layers: a dead patch
of the band is refilled only from its rim *within the band*. Smallest case: a cell of the middle layer of a
three-layer band has 10 neighbours in the band and 2 outside; if the 10 are dead it stays dead.

**Proposition S [proved].** For a sealed W let T_W be the first time W ∩ L_t = ∅. (i) W is dead for all t ≥ T_W.
(ii) K(t) = ∪{W sealed : T_W ≤ t}. (iii) The first time anything is lost for ever, min_W T_W, is the extinction
time of an inclusion-minimal sealed set.

*Proof.* (i) is thickness.md Lemma 1; (ii) is its Lemma 2 (K(t) is the union of the dead sealed sets); (iii): a
dead sealed set contains a minimal sealed set, which is then dead. ∎

So the vessel carries a family of contact-type subsystems, one for each sealed set W (the restriction of the
state to W: vacuum absorbing, births only next to life *in W*, Lemma 1′), driven by the rest; **the skeleton
grows only by their extinctions, and an extinction on W needs all |W| cells dead at one time.**

**What this makes of "why area" [the statement is proved; the hypothesis is not].** The wait for the first
permanent loss is governed by the minimal sealed sets and by how the cost of an extinction grows with the set:

    hull:        the smallest sealed set is a whole face, A cells (exact for R ≤ 10; aim A in general);
    wide slab:   a three-layer band across the torus, ≈ 4.5·m·N cells, smaller than a face once N > 1.5·m (board E12).

If an extinction on W costs in proportion to the level κ|W| up to which partial holes of W are refilled
(hypothesis H′ for W, through Theorem P̄), the wait is exponential in the *area* in a hull and in *N·m* in a wide
slab, and the switch from one to the other at m ≈ N is the place where the two smallest sealed sets cost the
same. Both are measured (0.21 per face cell; 0.12 per band cell; switch at m ≈ N). The lead's sentence "no dead
patch smaller than a whole face is protected, so death cannot nucleate" is right about which sets can die for
good and wrong about "so": the law needs, in addition, that unprotected holes *are* refilled.
The same dichotomy is a theorem in one place on the shelf (`library/notes/ld-contact-percolation.md`, read by
the librarian, not by me): for supercritical percolation low density costs only the perimeter, because a ring of
vacant sites seals a region for free; for the contact process an empty interval costs its length.

*Not done:* (a) the number of minimal sealed sets of size near A (an entropy that a union bound over them would
have to beat; in hulls the measured first loss is a face, so I only bound one given face); (b) the two prices.
Per unit of lateral area a band costs 3 × 0.12 = 0.36 against 0.21 for a face. In this language both are
extinction exponents of contact-type subsystems; nothing here computes either.

---

## 2026-11-13, entry 10. Proposition R: a caricature in which the area law is exact

**Proposition R [proved].** Biased voter dynamics on a finite connected graph G with N vertices, λ > 1: for every
pair of neighbours (x occupied, y vacant), y becomes occupied at rate λ and x becomes vacant at rate 1. The
states ∅ and G are absorbing. Then λ^{−|ξ_t|} is a martingale, and from any ξ

    P_ξ(∅ is reached before G) = (λ^{−|ξ|} − λ^{−N}) / (1 − λ^{−N}).

*Proof.* Each active pair contributes λ(λ^{−(n+1)} − λ^{−n}) + (λ^{−(n−1)} − λ^{−n}) = λ^{−n}[(1 − λ) + (λ − 1)] = 0 to
the generator applied to λ^{−n}. The chain is absorbed almost surely; optional stopping. ∎
*Smallest case:* G = one edge, ξ = one vertex: P(∅) = 1/(1 + λ), and (λ⁻¹ − λ⁻²)/(1 − λ⁻²) = 1/(λ + 1).

What it is for. The model has the rim lemma (births only next to life, vacuum absorbing) and nothing else of
gump (no cap, no drive, monotone). In it the chance that a droplet dies out depends on its *area* alone, not on
its shape or perimeter, with exponent ln λ per cell: ψ(n) = λ^{−n} satisfies (∗̄) with equality. For λ = 1 the same
computation gives 1 − n/N: no exponential. So in the caricature "area law" ⟺ "the rim is biased towards life".
Gump's face replaces λ^{−n} by the committor ψ* of its population table; measured log-slope 0.46–0.55 per cell
(entry 11), i.e. an effective λ of 1.6–1.7.
On the shelf (`library/notes/contact-finite.md` §1, Durrett–Liu Theorem 4, read by the librarian): on {1, …, N}
with vacant sites outside, (1/N) log σ_N → log λ, "because the process is an interval whose two ends are
independent random walks". log λ is the positive root of the edge walk's cumulant equation
λ(e^{−θ} − 1) + (e^{θ} − 1) = 0. That is the proved one-dimensional instance of "exponent = Lundberg root of the
front". That |ξ_t| is a time-changed biased walk in every dimension I state from the two-line proof above, not
from a source.

---

## 2026-11-13, entry 11. Gump's dying face is a shrinking droplet: three readings and one relation

All numbers are from `research/fluct/data/qsd_summary.json` (committed) or from the board's lab table; nothing
is new data. Tags as marked.

**11.1 The remnant curve [data].** Looking back from death, the mean population at lags 1…6 is 1.6, 3.4, 6.4,
9.7, 13.6, 17.6 (A = 84; L1.3), the same at A = 63 until it saturates. Its square root is 1.26, 1.84, 2.53, 3.11,
3.69, 4.20: steps 0.58, 0.69, 0.59, 0.57, 0.51. **√n falls by ≈ 0.59 per generation**: a two-dimensional remnant
whose radius shrinks at constant speed (≈ 0.47 cell-widths per generation if a cell has unit area and the
remnant has density ½). The half-way lag is then (√(n̄/2) − 0.68)/0.586 with n̄ the living mean: 3.3, 4.5, 5.6, 6.7
at A = 30…84 against the measured 3.2, 4.7, 5.9, 6.8. In the other direction the living face refills more
slowly: mean step +0.31, +0.53, +1.14, +1.98 from n = 2, 3, 5, 10 (L1.1), i.e. √n grows by about 0.3 per
generation at n = 10. Death is a *front route*; the remnant is the size-independent object.

**11.2 Two exponents that should be one [data].** The tallied committor p_B(k) (death before the population
returns to A/2) falls by a factor 0.544, 0.584, 0.571, 0.589, 0.565, 0.601, 0.574 per cell for k = 4…10 at A = 63:
log-slope θ_u ≈ 0.55. The quasi-stationary tail rises by a factor 1/0.63 per cell on the same range:
θ_p ≈ 0.46 (0.44, 0.46, 0.48, 0.51 at A = 45, 63, 84, 108 in the middle range). The product p_k·p_B(k) falls by
6–8% per cell at k ≈ 8, which is what a prefactor k^{−0.6} does there: the rate at which a remnant of k cells
moves on grows like its rim, √k. I read both as one exponent θ ≈ 0.50 ± 0.03 with power-law prefactors
**[guessed]**.

**11.3 A relation between the tail slope and γ [sketched].** Suppose (M1) below a level x*A the logarithm of the
quasi-stationary histogram is a straight line of slope θ in the population (a single remnant, whose chance of
dying is e^{−θk}); (M2) above it the histogram is Gaussian with mean ρA and variance σ²A; (M3) the two join with a
common tangent. Then x* = ρ − θσ² and, summing the slopes from the mean down to zero,

    −ln h = A·(θρ − θ²σ²/2) + O(1),      i.e.      γ = θρ − θ²σ²/2.                               (M)

Equivalently γ = −Λ(−θ), Λ the scaled cumulant function of the ordinary face population: the lifetime exponent
is fixed by the remnant's exponent θ and by two numbers of the *living* face, its density and its variance.
Check. The face population has mean 0.532·A − 2.3 (exponent study) and variance 0.385·A + 3.2 (my fit to the
committed var/A at A = 30…165; residuals ≤ 0.2), so (M) predicts a straight law of slope
0.532θ − 0.1925θ². With the measured tail slope at each size: θ = 0.46, 0.485, 0.51 (A = 63, 84, 108) gives
0.204, 0.213, 0.221, against the local slopes of ln τ 0.212 (45→63), 0.212 (63→84), 0.221 (84→108, unverified
GPU value). With θ_u = 0.545 it gives 0.233, too high. With one constant, θ = 0.48, (M) plus an offset 1.80
reproduces the four verified lifetimes to 0.16, 0.04, 0.00, 0.00 nats; that is two parameters and four points on
a nearly straight line, so the fit by itself shows little. The content of (M) is the first check: **the lifetime
slope and its slow rise with A are those of the tail slope**.
What is missing for "sketched → proved": everything; (M1)–(M3) describe a shape. The weakest is (M3): the
tangency point is ≈ 2.9 standard deviations below the mean at A = 84, where I have not checked the histogram
against a parabola (the committed summary stores only the lowest 40 values).

**11.4 What γ is, in this picture [guessed].** γ = −Λ(−θ), and θ is the exponential rate at which the chance of
extinction of a live remnant on an otherwise empty face falls with its population: the analogue of the constant
γ₂ of the contact process, which is defined exactly that way and equals the finite-system exponent
(`library/notes/contact-finite.md` §2, Durrett–Schonmann Theorem 2 (a) = (d), read by the librarian). By
entry 10's caricature θ is the Lundberg root of the rim. I cannot compute θ from the rule.

---

## 2026-11-13, entry 12. Aim A (isoperimetry of sealed sets): what is proved, where the induction stalls

**Corollary 4a [proved].** Let W be sealed in a hull V, d a diagonal, t the top layer of W along d. Call a cell
*d-deep* if its three d-upward neighbours are in V; for a cell p with normal axis a this holds iff t ≤ R − 4,
d′·p ≤ R − 4 for d′ = d with coordinate a flipped, and d′·p ≤ R − 2 for d′ = d with one of the other two
coordinates flipped (the three upward offsets change those d′·p by (0, 0, 4), (0, 2, 0), (2, 0, 0); no other
diagonal increases). If c ∈ W is in layer t and d-deep, then W contains every cell of layer t that can be reached
from c by an in-layer path whose vertices before the last are d-deep, and all downward neighbours in V of the
d-deep cells so reached.
*Proof.* Lemma 4 at c, then at each d-deep cell reached. ∎
So a sealed set that keeps away from the two outer layers of every face contains whole sheets and is far larger
than a face.

**Where a proof of A for all R stalls.** The natural induction is on R with W′ = W ∩ V_{R−2}, which is sealed in
V_{R−2} or empty. If W′ = ∅, W lies in the union of the faces and every face cell of W whose three cells beneath
are in V_{R−2} has all in-face neighbours in W: W contains a whole face. If W′ is a face of V_{R−2}, its cells
have three neighbours beneath outside W, so both upward neighbours of each are in W, and W contains the
interior of a face of V, more than the 3k cells needed (A(R) − A(R − 2) = 3k) once k ≥ 5. The case that is not
handled is |W′| > A(R − 2): it needs a *stability* statement (a sealed set of V_{R−2} with A(R − 2) + δ cells forces
at least 3k − δ cells of W in the outer shell), and I have no approach to that except case analysis at the rims.
I stop here on A: the exact result for R ≤ 10 is the critic's, the general statement stays a conjecture, and
Proposition S does not need it for a given face.

---

## 2026-11-13, entry 13. Errata to entries 7, 11 and 12 (found on re-reading before the round report)

- **Entry 7, item 4.** Now checked in `research/phase/rules.csv` (columns med6, med8, med10 = median lifetime in
  hulls of three sizes): B45/S34: 10.5, 20, 36; B45/S35: 7, 14.5, 22; B45/S45: 6, 12.5, 20; B4/S345: 8, 50, 104;
  gump: 28, 254, 3,420. All four neighbours are classed "chaos" on a torus and share gump's graph and θ = 4.
- **Entry 11.3, relation (M).** The remainder is not O(1): a normalised Gaussian has ln p_peak = −½ ln(2πσ²A), so

      −ln h = A·(θρ − θ²σ²/2) + ½ ln(2πσ²A) + O(1),   local slope of ln τ = θρ − θ²σ²/2 + 1/(2A).

  With the measured tail slopes θ = 0.46, 0.485, 0.51 the predicted local slopes become 0.213, 0.220, 0.226 at
  A ≈ 54, 74, 96, against 0.212, 0.212, 0.221. With or without the logarithm (M) holds to about ± 0.01 in the
  slope and no better; the constant-θ fit quoted there (θ = 0.48, offset 1.80) becomes θ ≈ 0.46 with a flat
  remainder. The O(1) term is not transferable between vessels: with the hull's offset and any plausible mean
  and variance, (M) would put a periodic slab face of 60 cells about 1.5 nats above its measured ln τ. **(M) is a
  statement about slopes only.**
- **Entry 12, "where the induction stalls".** The two sub-cases described as handled (W′ = ∅; W′ a face of
  V_{R−2}) are sketches: I did not check the cells near the rims and corners of the faces, where some of the
  cells beneath a face cell lie on another face. Only Corollary 4a is proved there.

---

## Round 2 report

**Corrected or withdrawn** (entry 7): L1(c) "private cell" (false at hull corners; the cube lemma is the
statement); hypothesis H with φ = r^{min(n,K)} (false, lab L1.1); G2's gump half (the data decide: the collapse
lengthens with the face); R5's example (now gump's own neighbours B45/S34, B45/S35, B45/S45, B4/S345: same graph,
θ = 4, chaotic on a torus, median lifetimes 20–104 where gump has 3,420).

**Claims.**
- **Theorem P̄** (entry 8): for any process and statistic, pooled over a window, Deaths ≤ direct deaths from
  outside a low set 𝓛 + Σ over entries into 𝓛 of ψ(entry point) + a boundary term, for every ψ ≥ 0 superharmonic
  for the pooled one-step table on 𝓛; an identity for the table's own committor ψ*. No Markov property, no
  uniformity in time, no constant a, censoring free. **[proved]**
- **H′** (entry 8): ψ*_K(k) ≤ C e^{−θk} at the entry rows, K = κA, for the population of a gump hull face. Then
  ln τ ≥ θ(κA − J) − const. **[hypothesis; consistent with L1.2 on the tallied rows, A ≤ 84]**
- **Lemma 1′, Proposition S** (entry 9): inside any sealed set life spreads only from life in the set; the
  skeleton grows only by extinctions of these contact-type subsystems; the first permanent loss is the extinction
  of a minimal sealed set. **[proved]** With H′ for the set, this is the precise form of "why area": a face in a
  hull, a band in a wide slab (E12). **[conditional]**
- **Proposition R** (entry 10): for biased voter dynamics on any finite graph a set of n sites dies out with
  probability (λ^{−n} − λ^{−N})/(1 − λ^{−N}): the area law for a droplet, exact, by the martingale λ^{−n}. **[proved]**
  A caricature of the mechanism, not a relative of the rule.
- **The remnant** (entry 11): looking back from death √n falls by ≈ 0.59 per generation at every size: death is
  a shrinking droplet **[data]**. Committor slope 0.55 and tail slope 0.46 are one exponent θ ≈ 0.50 with
  power-law prefactors **[guessed]**. **(M)** γ = θρ − θ²σ²/2 (+ 1/(2A) in the local slope): the lifetime slope
  from the tail slope and the mean and variance of the living face; holds to ± 0.01 on the slopes at
  A = 54–96 **[sketched; slopes only, entry 13]**.
- **Corollary 4a** (entry 12) **[proved]**; aim A stays a conjecture beyond R = 10 and I have stopped working on it.
- G1 (one exponent for the 2D rule, rings carrying a power of L) and exam entries E1, E2: unchanged, **[guessed]**.

**Weakest steps.** (1) H′ can be checked only where deaths are already frequent. What would make it a law is
that ψ* is one function of k for all A (the remnant does not know the face); I have the critic's four tables
and no argument. (2) (M) describes a shape (parabola joined to a line); assumption M3 is unchecked and its
remainder is vessel-dependent. (3) For the 2D rule this round adds nothing: there Theorem P̄'s entry term is
itself the rare event. (4) The C4 box (entry 5.3) is still unexplained.

**Lab requests.** LR4–LR7 are arithmetic on the existing tallies; LR8′ is exact.
- LR4. For A = 30, 45, 63, 84 and K = ⌈0.3A⌉, ⌈0.4A⌉: ψ*_K = (I − T̄_{<K})⁻¹ d̄ from `Tr` (rows 1…K − 1); its values
  and local log-slopes; whether ψ*_K(k), k ≤ 10, is the same function at the four sizes. Then the identity of
  Theorem P̄: entries into {< K} from the tallied rows K ≤ k < KMAX, plus entries from rows ≥ KMAX obtained from
  identity (I) (histogram `H` minus tallied inflow), each times ψ*, over exposure, against h̄; and which entry
  rows carry the sum.
- LR5. Per row k < KMAX: mean and variance of the one-step change, and the root r_k ∈ (0, 1) of
  Σ_{k′} T̄(k, k′) r^{k′−k} = 1. The droplet reading predicts r_k level for k ≥ 6, equal across sizes (0.60–0.63),
  and a mean step growing like √k.
- LR6. The pre-death curve predicted by the pooled table alone (time-reversed chain T̃(k′ → k) ∝ N(k) T̄(k, k′),
  started from the death shares), lags 1…6, against 1.6, 3.4, 6.4, 9.7, 13.6, 17.6. Is n Markov along death paths?
- LR7. d ln p_k/dk over 8 ≤ k ≤ 20 at A = 108, 135, 165 (`H` of R = 15, 17, 19); and at A = 63, 84 the histogram
  against the parabola of its own mean and variance down to x* = ρ − θσ² (assumption M3).
- LR8′. D2(ρ = 0.472), quasi-stationary law μ. (a) Segment, L = 12 and 14: E_c(ℓ) = μ(cells 1…ℓ dead),
  ℓ = 1…L − 4. (b) Ring, L = 16 or 18: E(ℓ) = μ(a fixed window of ℓ cells dead). The front picture predicts: the
  corner decrement −ln[E_c(ℓ+1)/E_c(ℓ)] is level from small ℓ at some θ_c; the ring's decrement approaches θ_c
  from above; both lifetime steps tend to θ_c. A level corner decrement near 0.45 with a ring decrement that
  stays near 0.52 would refute "one exponent" in D2.

**Next.** If LR4 shows ψ* universal: state the area law for gump as one theorem under H′ with the remnant
defined on an infinite face, and look for the weakest property of the cells beneath a rim that gives the
upward drift. Otherwise: the 2D rule, where the open question is the route (E2).

---

## 2026-11-13, entry 14. Exam entry E3 filed

In `research/theory/swarm/PREDICTIONS.md`: on the periodic slab face of 60 cells (5 × 4 × 8), (i) mean population
of the dying face at lags 1–4: 1.6 ± 0.15, 3.4 ± 0.35, 6.4 ± 0.6, 9.7 ± 1.0; (ii) tail ratio p_k/p_{k+1} over
6 ≤ k ≤ 12: 0.63 ± 0.03; (iii) 62 ± 5% of deaths from one cell. It tests the claim behind H′ and (M) that the
remnant is one object in every vessel. What could break it: in a hull the last remnant may sit at a corner or on
the rim (hull faces outlive slab faces of equal area by a constant factor 1.7–1.9, which I read as an anchoring
of the last remnant, an O(1) effect); if so the hull's curve at lags 1–2 is a corner curve and the slab's will
differ.

---

## 2026-11-13, entry 15. After the critic's reply to round 2: corrections, and two pieces of unfinished work

Written when the group was paused; nothing here was sent to the lab. Lab ids are the board's.

**15.1 Corrections (I accept all three).**
- **H′, "C, θ, κ independent of A", is false on the tables** (lab L5.1): the committor ψ* of the pooled table
  steepens with the face (log-slope over k = 5…10: 0.51–0.54, 0.53–0.57, 0.55–0.60 at A = 45, 63, 84). What the
  critic's numbers do show: at fixed k, ψ*_A(k) *falls* as A grows (ln[ψ*(A)/ψ*(63)] = +0.32, +0.47 at A = 30;
  +0.10, +0.22, +0.33 at A = 45; −0.04, −0.04, −0.15 at A = 84, for k = 4, 7, (10)). A lower bound on τ needs only
  an inequality ψ*_A(k) ≤ C e^{−θ₀k} up to k = κA with one θ₀ > 0; a committor that is monotone in A would give
  it from the smallest face. I have not tested monotonicity beyond these twelve numbers. Theorem P̄ is untouched.
- **Relation (M) is withdrawn as a quantitative statement** (lab L5.4). Its tangency assumption M3 fails: at
  A = 84 the histogram's slope lies below both branches from n ≈ 28 down to n ≈ 14; the formula is 0.9–1.6 nats
  too large at A = 63, 84 and its difference quotient is 0.235 against 0.205. My check in 11.3 was wrong in the way
  the critic says (it differentiated at fixed θ while θ rises with A). What survives is only the identity of
  Theorem P̄, h = entries × ψ*, which makes the tail slope and the committor slope the same function up to the
  rate at which a face of k cells moves on.
- **"One remnant whose population walk does not know the vessel" (11.1, 11.2, the rationale of E3) is not
  supported.** The pooled one-step table, reversed from the deaths, gives 1.6, 2.9, 4.3, 5.9, 7.7, 9.8 at lags 1…6
  where the histories have 1.6, 3.4, 6.4, 9.7, 13.6, 17.6 (lab L5.3): a dying face comes down twice as fast as faces
  of the same population do on average, so something besides n is carried along a death path. The reading
  "√n falls by 0.59 per generation" stands as a statement about conditioned paths. E3 stays filed; its two
  lines of reasoning are weaker than I wrote.

**15.2 Unfinished: the exponent as an integral of local roots [guessed; arithmetic not done on the tables].**
The critic's roots r_k of Σ_{k′} T̄(k, k′) r^{k′−k} = 1 (lab L5.2) are not one number, but θ = −ln r_k looks like a
function of x = k/A for A ≥ 45: 0.60 (x = 0.08, A = 84), 0.59 (0.095, 84), 0.58 (0.10, 63), 0.54 (0.14, 45),
0.55 (0.18, 84), 0.51 (0.24, 84), 0.40 (0.36, 84); A = 30 lies below (0.455 at 0.22). For a chain whose one-step
law varies slowly with the level, the committor is ψ*(K) ≈ exp(−Σ_{k<K} θ_k) (the usual WKB evaluation), so with
Theorem P̄ the law would read ln τ ≈ A·∫₀^ρ θ(x) dx. A straight line through the seven values, cut off at the mean
density, integrates to about 0.21. This is eight numbers read off the critic's reply and a ruler; the sum
Σ_k θ_k over the committed tables (`critic/lab/data/fluct_tables.npz`) is the first thing to compute. Also from
L5.2: mean step ≈ 0.5–0.8·√k and variance ≈ 0.75·k, and 2·mean/variance reproduces the roots to about 5% at
k = 10, 15, 20 (0.57, 0.53, 0.48 against 0.58, 0.55, 0.51). If this holds up, γ is the quasi-potential of the
population's effective one-step dynamics, with drift and variance as its only inputs.

**15.3 Unfinished: the power of L in one dimension (G1) [sketched model; mixed scorecard].**
*Readings of committed data* (`research/theory/exponent/data/gap.json`, key `gap_H16_L128`, and the seven
lifetimes of `research/toy2d/data/law_cross2_B34S234.json`; calculator fits, not new data):
- ln E(ℓ) = c − gℓ − b ln ℓ, free b: (g, b) = (0.351, 0.97), (0.346, 1.09), (0.345, 1.13) on ℓ = 10–38, 15–38, 20–40.
  With an offset, E ∝ (ℓ + ℓ₀)^{−b} e^{−gℓ} on ℓ = 8–40: b = 1: ℓ₀ = 1, g = 0.351, rms 0.0068; b = 3/2: ℓ₀ = 5,
  g = 0.340, rms 0.0033; b = 2: ℓ₀ = 9, g = 0.331, rms 0.0020. **The file does not determine the power.** With
  b = 3/2 the exponent is 0.340, the box-edge slope.
- The ring's lifetime follows the window probability with *no* factor L: τ(L)·E(L − m)·L^p is constant over
  L = 12…36 with χ² = 20 (p = 0, m = 6), 45 (p = ½), 248 (p = 1), on 7 points.
*A mechanism.* For cells that are dead now let T(x) ≥ 0 be the number of generations x has been continuously
dead (the death-age profile). Model: the weight of a profile is a product over neighbouring pairs of a
symmetric function w(T(x+1) − T(x)), W = Σ_j w(j). Then, exactly or by standard random-walk facts (the last two
cited from memory):
  - a whole segment with free ends dying now (min T = 0): Σ = W^{L−1}, no power (each sequence of steps
    corresponds to exactly one profile with minimum 0) **[proved, in the model]**;
  - a whole ring dying now: W^L × P(the step walk returns to 0 after L steps) ~ L^{−1/2};
  - a window of a long row, both ends next to living cells (ends pinned near 0, T ≥ 0): ~ ℓ^{−3/2};
  - a window with one end at a dead wall (free there) and one pinned: ~ ℓ^{−1/2}.
*Scorecard.* Segments: no power (exact in D2 to three decimals; straight laws in the 2D rule): **agrees**.
Windows: the 2D rule fits (ℓ + 5)^{−3/2} e^{−0.340ℓ}; in D2 the sampled decrement minus 1.5/(ℓ + ½) is 0.432, 0.453,
0.457, 0.452 at ℓ = 10, 15, 20, 25 against the exact 0.460: **compatible, not decided**. Rings: the model says
hazard ≈ L × (window probability), which the 2D rule's seven lifetimes reject (χ² 248); and in D2 the ring's steps
at L = 15–18 are level at 0.522–0.526, i.e. 0.062–0.066 above 0.460, where the return probability of any walk with
geometric steps gives at most 0.040 (calculator, 0.02 ≤ u ≤ 0.3): **disagrees at every accessible size**. Corner
windows in D2 (lab L5.5: 0.475 at ℓ = 4 on a segment of 18, still falling with the segment's length) are already
near 0.46, not near 0.46 + 1/(2ℓ) = 0.57: **disagrees, at a small ℓ**.
So the ordering "free ends: none; no free end: a power" comes out, and the powers do not. A reading I have not
tested: at these sizes a ring dies in two or three generations (board E14), a flat profile, and its slope is
the flash cost; the walk regime needs many steps of the profile. The object T(x) is, I believe, the height of
the dual contour of the contact-process proofs (planar duality in `library/notes/contact-finite.md` §2), whose
Ornstein–Zernike corrections are exactly these powers; I have not opened a source for that.

---

## Round 3 report (interim, paused)

**Done.** The three corrections of 15.1 (H′ as stated false on the tables; relation (M) withdrawn; the remnant
is a property of conditioned paths). `claims.md` is current. Exam entries E1, E2, E3 are in
`swarm/PREDICTIONS.md` and I leave them as filed (E3 with the weaker rationale noted in 15.1).

**Half-done.**
- 15.2: γ = ∫₀^ρ θ(x) dx with θ(x) the local root of the population's one-step law. Missing: the sum over the
  committed tables against −ln h at the four sizes; the collapse of θ in k/A; rows above A/2 (not tallied).
- 15.3: the power of L. A profile model gives no power for free ends and powers for rings and windows; the
  window fit is compatible, the ring is not at any accessible size. Missing: an exact test in D2 of whether the
  death-age profile fluctuates at all (see below); a source for the contour reading.
- H′ in its inequality form (ψ*_A(k) non-increasing in A): read off twelve numbers, not tested.

**What my line has given, as I would rank it.** Proved and checked: the rim lemma and its sealed-set form
(L1, L1′), Proposition S (every permanent loss is the extinction of a minimal sealed set), Theorems P and P̄
(the hazard from a one-step table, no Markov property), Proposition R, R5. Conditional: "why area in a hull, a
band in a wide slab" (S plus a hypothesis on refilling). Not achieved: a formula for γ; any theorem for gump
or the 2D rule themselves.

**Next, when resumed** (nothing started). (1) Lab: Σ_k θ_k and 2·mean/variance per row from
`critic/lab/data/fluct_tables.npz`, summed to the mean, against −ln h; θ against k/A at the four sizes; ψ*_A(k)
against A at fixed k. (2) Lab, exact in D2 on a ring of 16–18: the mean population 1…6 generations before death
from the exact reversed chain, and the mean age of the central cell of an empty window of ℓ cells: O(1) (flash),
growing (profile walk), or ∝ ℓ (fronts). (3) Library: Ornstein–Zernike corrections for the dual contour of the
one-dimensional contact process in a strip, on a cylinder and in a half-plane.

---

_From here on the journal is kept by the successor on this line (the first agent was paused in round 3). Read
before writing: the critic's reply to round 3 (`critic/to-path.md`; lab ids L9.1–L9.4), the examiner's outcomes
(`swarm/exam/OUTCOMES.md`), and the one item of another line the critic pointed to (source's remark on a monotone
comparison, `source/journal.md`, the paragraph "A remark for the critic to route"). Lab ids below: the reply to
round 3 names L9.1–L9.4 without assigning them; I use L9.1 for its local-root tables (`path_r3.py th`, §2), L9.2
for the monotone-comparison tables (`mono`, §3), L9.3 for the age table (`age`, §4), L9.4 for the sealed-set
enumeration (`sealed`, §1). If the board numbers them otherwise, read these as the script names._

## 2026-11-14, entry 16. The exam: E1 holds, E2 is not refuted, E3 fails. What each does to the claims

**16.1 E1 holds** (`swarm/exam/OUTCOMES.md`, part 2). Strips 16 × L of the 2D rule, row 0 with columns 0 and 1
removed, row 15 of the same strips intact:

| L | ln τ, notched row | ln τ, intact row | intact − notched |
|---|---|---|---|
| 20 | 8.517 ± 0.033 | 9.073 ± 0.044 | 0.556 ± 0.055 |
| 24 | 9.900 ± 0.029 | 10.757 ± 0.044 | 0.857 ± 0.053 |
| 28 | 11.320 ± 0.028 | 12.407 ± 0.048 | 1.087 ± 0.056 |
| 32 | 12.666 ± 0.028 | 14.014 ± 0.055 | 1.348 ± 0.062 |

Slope of the notched row 0.3458 ± 0.0036 (predicted 0.345 ± 0.020; refuted from 0.39 on); intact row 0.412 ± 0.005.

**What it settles [measured].** An edge with an end costs 0.34–0.35 per independent cell in five geometries now:
box corner, diagonal mirror, mirror across the edge, D4 (entry 5.2), and a fixed dead anchor, the last one made
for the purpose and measured to 1%. Two dead cells, a change of the vessel of size O(1), take 0.066 per cell off
the measured slope of the same row at the same lengths. This is the first half of G1.

**What it leaves [arithmetic on the table above].** The second half of G1 ("the ring has the same exponent and
carries a power of L") is not decided. The last column is fitted equally by 1.66(16)·ln L − 4.41 (χ² 0.25 on 2)
and by 0.065(6)·L − 0.73 (χ² 0.32 on 2). If it is a power (L − c)^b, then b = 1.7, 1.5, 1.3 for c = 0, 3, 6.
- The profile model W (15.3) gives ½ for a closed ring, and gives it for *every* choice of step weights: the
  count of closed profiles is W^L·P(a walk with these steps returns after L steps), and the local limit theorem
  makes that L^{−1/2} whatever the steps. So the real rule's 1.3–1.7, like D2's 1.0–1.3 (critic, reply to round 3,
  §5), cannot be met by changing the weights. **The ring part of W is withdrawn.** A model that could give
  more needs weights that are not a product over neighbouring pairs: for instance different local weights
  where the death-age has a local maximum (a gap was nucleated inside living cells) and where it has a local
  minimum (two gaps met). I have no derivation and do not pursue it.
- The two readings differ in what they predict beyond L = 36: under a power the ring's local slope is
  0.346 + b/(L − c), that is 0.38 at L = 48 and 0.37 at L = 64; under two exponents it stays at 0.41.
- Counting's entry C-E2 (same file: a ring from a fair soup is dead by generation 3 with slope 0.3676 at
  L = 20–32, below the ring's steady local slope there) I do not use: an exponent at a fixed age from a soup
  bounds the steady exponent in neither direction.

**16.2 E2 is not refuted; its central value is too high at L = 36.** Mean population of the dying edge, intact
strips (same file):

| L | lag 1 | lag 2 | lag 3 | lag 4 | living mean |
|---|---|---|---|---|---|
| 32 | 2.04 ± 0.09 | 9.09 ± 0.08 | 13.14 ± 0.11 | 13.69 ± 0.17 | 18.5 |
| 36 | 1.83 ± 0.03 | 7.99 ± 0.38 | 11.95 ± 0.24 | 13.65 ± 0.50 | 20.8 |

Predicted at lag 2: 9.8 ± 1.0 at both; refuted from 11.5 at L = 36. What stands of reading 5.1: the edge does
not die in a flash from its ordinary density (two generations out it holds 0.25 and 0.22 of the row, against
0.58), the collapse starts three to four generations out, and the remnant does not grow with L. What was
wrong: "levelling off near 9–10". The lag-2 count is 7.3, 8.8, 9.2, 9.4, 9.1, 8.0 at L = 12, 16, 20, 24, 32, 36: it
has a maximum near L = 24–32. I have no account of the fall (one size, two rough standard errors).

**16.3 E3 fails.** Rim-free slab face, A = 60, living mean 31.0 (same file):

| | lag 1 | lag 2 | lag 3 | lag 4 | tail ratio, k = 6…12 | deaths from one cell |
|---|---|---|---|---|---|---|
| predicted (the hull's curve) | 1.6 | 3.4 | 6.4 | 9.7 | 0.63 ± 0.03 | 62 ± 5% |
| slab | 1.66 | 4.29 | 10.70 | 18.40 | 0.677 ± 0.002 | 59.4 ± 0.9% |

What it does to the claims.
- **Dr is a statement about hull faces only.** "√n falls by 0.59 a generation at every size" holds on hulls of
  A = 30…84. On a rim-free face with the same living mean (31.0; the hull of A = 63 has 31.2) √n falls by about
  1.0: the last 18 cells go in four generations, where the hull takes six or seven.
- **"One remnant, the same object in every vessel" is refuted**, except for the last generation (lag 1 and the
  one-cell share agree). Its rationale was already weakened in 15.1; relation (M), which was to tie the two
  vessels' slopes through a common tail, is withdrawn there, and the tails differ (0.39 per cell on the slab,
  0.46 on the hull of A = 63). The risk named in entry 14 is the likelier reading: the hull's late curve is a
  rim or corner curve.
- **For entry 17 below.** The hull tables (A ≤ 84, faces that are mostly rim) are not the asymptotic object.
  The root curve read from them need not be the slab's; with a shallower tail the slab's roots at low density
  are presumably smaller. Entry 17 is a statement about each vessel's own table, and exam entry E4(a) asks
  whether it holds on the slab's.
- **For "flash or front".** The population alone hides most of what happens in a death. The pooled chain of
  the hull tables comes down half as fast as the hull's recorded histories (L5.3), and its minimising path
  (17.5) would need about ten generations for what the slab does in four. Theorem P̄ is exact for the hazard
  all the same; but a one-step hypothesis on the population (R of Theorem Q) describes an average over
  whatever second variable a death path carries (the layer beneath), not a mechanism.

---

## 2026-11-14, entry 17. The local roots: what they give exactly, and why their sum is not the exponent

Claim Th of 15.2 (ln τ ≈ A·∫Θ, Θ the local root as a function of k/A) is **withdrawn**: on the committed tables
the local-root sum is not the committor's exponent (lab L9.1: near the top of each table it exceeds the
committor's own exponent by 0.45, 0.98, 1.46, 2.02 nats at A = 30…84, and its slope between sizes is 0.03–0.05
per cell above the hazard's). This entry proves which inequality
holds, proves where equality holds, and says what the exponent is instead. Nothing here uses a property of
gump: T is the pooled one-step table of any statistic, as in entry 8.

**17.1 Setting.** T(k, k′) for k ≥ 1, k′ ≥ 0, row sums ≤ 1 (the missing mass is censored); k′ = 0 is death,
d(k) = T(k, 0). Low set 𝓛 = {1, …, K − 1}. ψ* = ψ*_K is the committor of entry 8 (death before leaving 𝓛 in
any other way): the smallest non-negative solution of ψ(k) = d(k) + Σ_{k′ ∈ 𝓛} T(k, k′)ψ(k′), extended by
ψ*(0) = 1 and ψ*(k) = 0 for k ≥ K. Row transform and local root:

    M_k(s) = Σ_{k′ ≥ 0} T(k, k′)·e^{−s(k′ − k)}   (s ≥ 0),          θ_k = max{ s ≥ 0 : M_k(s) ≤ 1 }.

M_k is convex with M_k(0) ≤ 1, and tends to infinity if the row can go down; so {s : M_k(s) ≤ 1} = [0, θ_k] and
M_k(s) ≥ 1 for s ≥ θ_k. With r = e^{−s} this is the lab's r_k (Σ_{k′} T̄(k, k′)·r^{k′−k} = 1, death counted as k′ = 0).

**17.2 Proposition T′ (block bound) [proved].** Let 0 ≤ k₀ < K and θ₀ ≥ 0 with M_k(θ₀) ≤ 1 for every
k₀ ≤ k < K, k ≥ 1 (that is, θ_k ≥ θ₀ on the block). Then ψ*(k) ≤ e^{−θ₀(k − k₀)⁺} for every k.

*Proof.* ψ(k) = e^{−θ₀(k − k₀)⁺} is a supersolution on 𝓛. For k ≤ k₀ it equals 1, and d + Σ T ψ ≤ 1 because
ψ ≤ 1. For k₀ ≤ k < K: ψ(k′) ≤ e^{−θ₀(k′ − k₀)} for every k′ ≥ 0 (for k′ < k₀ the right side exceeds 1), so
d(k) + Σ_{k′ ∈ 𝓛} T(k, k′)ψ(k′) ≤ Σ_{k′ ≥ 0} T(k, k′)e^{−θ₀(k′ − k₀)} = e^{−θ₀(k − k₀)}·M_k(θ₀) ≤ ψ(k). The smallest
non-negative solution lies below every non-negative supersolution. ∎

With Theorem P̄: Deaths ≤ D(𝓛ᶜ) + Σ_{z ≥ K > z′} F(z, z′)·e^{−θ₀(z′ − k₀)⁺} + (boundary term). This is Corollary P1
of entry 3 with the first k₀ rows left free, which is what the lab's linear programme found necessary (L1.2).
*Smallest case.* Walk on {0, 1, 2, 3}, up ¾, down ¼, K = 3: θ₁ = θ₂ = ln 3; with k₀ = 0 the bound is
ψ*(2) ≤ 1/9, and ψ*(2) = (1/9)/(1 + 1/3 + 1/9) = 1/13.

**17.3 Proposition T (the local-root sum is an upper bound for the exponent) [proved].** Let 1 ≤ k₀ < K and
let s_{k₀} ≥ s_{k₀+1} ≥ … ≥ s_{K−1} ≥ 0 satisfy M_k(s_k) ≥ 1 (for instance s_k = max_{k ≤ j < K} θ_j, which is θ_k itself
when the roots are non-increasing on the block). Suppose every state of 𝓑 = {k₀, …, K − 1} leaves 𝓑 with
probability one. Put S(k) = Σ_{k₀ < j ≤ k} s_j on 𝓑 and S(K) = S(K − 1) + s_{K−1}. Then for k ∈ 𝓑

    ψ*(k)  ≥  c₀·( e^{−S(k)} − e^{−S(K)} ),        c₀ = e^{−s_{k₀}·k₀} · min_{0 ≤ j < k₀} ψ*(j),

    i.e.   −ln ψ*(k)  ≤  Σ_{k₀ < j ≤ k} s_j  +  ln(1/c₀)  −  ln(1 − e^{−(S(K) − S(k))}).

*Proof.* Extend S by S(k) = −s_{k₀}(k₀ − k) for k < k₀ and S(k) = S(K − 1) + s_{K−1}(k − K + 1) for k ≥ K. Its
increments are non-increasing, so S is concave on the integers, and for k ∈ 𝓑 the number s_k (the increment
into k) is a slope of S at k: S(k′) − S(k) ≤ s_k·(k′ − k) for all k′ ≥ 0. Hence g = e^{−S} satisfies, on 𝓑,
Σ_{k′} T(k, k′)g(k′) ≥ g(k)·M_k(s_k) ≥ g(k): g is subharmonic for the chain with kernel T (censored mass sent to a
state where g = 0). g is bounded on what the chain can reach before and at its exit time σ from 𝓑, so
g(k) ≤ E_k g(Z_σ) ≤ P_k(Z_σ < k₀)·e^{s_{k₀}k₀} + e^{−S(K)}: below k₀, g ≤ e^{s_{k₀}k₀}; at or above K, g ≤ e^{−S(K)}. So the
chain leaves 𝓑 downward with probability at least e^{−s_{k₀}k₀}(e^{−S(k)} − e^{−S(K)}), and from where it lands it dies
before leaving 𝓛 with probability at least min_{j < k₀} ψ*(j) (strong Markov property of the table's chain). ∎

*Smallest case.* The same walk, k₀ = 1, K = 3, k = 2: (1/3)(1/3 − 1/9) = 2/27 = 0.0741 ≤ ψ*(2) = 1/13 = 0.0769.

So, whenever the roots decrease, **Σθ is an upper bound for −ln ψ*, and hence for ln τ** (Theorem P̄ is an
identity for ψ*, and the entry flux is a constant, 1.0–1.2 nats on the tables, L9.1): **the side that was never
in doubt.** On the tables the roots decrease from k ≈ 5 on (L5.2, L9.1), and the lab's column has
−ln[ψ*(k)/ψ*(3)] below Σ_{3 ≤ j < k} θ_j at k = 15, 20, 30, 40 (6.84 / 6.97, 9.35 / 9.66, 13.32 / 14.36, 15.40 / 17.42).
Together with 17.2, when the roots are non-increasing on the block:

    (K − 1 − k₀)·min_{k₀ ≤ k < K} θ_k   ≤   −ln ψ*(K − 1)   ≤   Σ_{k₀ < j < K} θ_j + ln(1/c₀) − ln(1 − e^{−θ_{K−1}}).         (1)

(The last term is the price of not leaving through the top; it is large when K is put at the mean, where the
root vanishes, and is the reason to compare slopes in k or differences between sizes, as the lab did.)

**17.4 Where the sum is exact [proved].**
- *(a) Skip-free rows.* If T(k, ·) charges only k − 1, k, k + 1 (probabilities d_k, ·, u_k; no censoring), then
  r_k = d_k/u_k and, with π_j = r₁⋯r_j, ψ*(k) = (π_k + … + π_{K−1})/(1 + π₁ + … + π_{K−1}) (gambler's ruin). If every
  r_k ≤ r̄ < 1 this lies between (1 − r̄)·e^{−Σ_{j ≤ k} θ_j} and e^{−Σ_{j ≤ k} θ_j}/(1 − r̄), **however fast θ_k varies with k**.
  Check: the walk above, k = 2: π₂ = 1/9, and 1/13 lies between (2/3)/9 and (3/2)/9.
- *(b) Branching rows.* If T(k, ·) is the law of a sum of k independent copies of one offspring variable with
  generating function f, then M_k(s) = (f(e^{−s})·e^{s})^k: every row has the same root, θ = −ln q with q = f(q) the
  extinction probability, q^k is harmonic, and q^k − q^K ≤ ψ*_K(k) ≤ q^k. Check: offspring 0 or 2 with probabilities
  ¼, ¾: q = 1/3; from two cells 1/16 + (6/16)(1/9) + (9/16)(1/81) = 1/9.
- *(c) The smallest case with a gap.* Binary branching whose death probability depends on the population:
  from 1 cell, 0 or 2 cells with probabilities 0.2, 0.8; from 2 cells each cell independently leaves 0 or 2 with
  probabilities 0.3, 0.7; K = 3. Roots: r₁ = 0.2/0.8, r₂ = 0.3/0.7, so θ₁ = 1.386 > θ₂ = 0.847. Committor:
  ψ*(2) = 0.09/(1 − 0.42) = 0.155, −ln ψ*(2) = 1.863. Block bound (k₀ = 0): 2 × 0.847 = 1.695. Root sum: 2.234.
  The committor's exponent lies strictly between the two, and the reason is visible: the row from 2 can reach
  0 in one step, at a price set by its own root alone, without paying the larger root of the row it jumps over.

**17.5 Why the face is not in 17.4, and what the exponent is.** The face population's row from k has standard
deviation 2.0, 2.8, 3.8, 4.5, 5.0 cells at k = 5, 10, 20, 30, 40 (A = 84) and its root falls by 0.004–0.024 per
row: neither skip-free nor root-preserving.

*The second-order statement [sketched; checked by hand on four rows].* Write ψ* = e^{−S} and suppose S varies
smoothly over the length of one jump. Expanding E_k[e^{−(S(k′) − S(k))}] = 1 to first order in the curvature S″
gives S′(k) = θ_k + S″(k)·E_θ[Δ²]/(2|E_θ[Δ]|), E_θ the row's law of Δ = k′ − k tilted by e^{−θ_kΔ}. For a Gaussian row
with mean μ_k and variance σ_k² (then θ_k = 2μ_k/σ_k², and the tilted row has mean −μ_k), with S″ ≈ θ′_k:

    S′(k) ≈ θ_k − |θ′_k|·(σ_k² + μ_k²)/(2μ_k).                                                              (2)

Against the lab's rows at A = 84 (θ_k, −d ln ψ*/dk from L9.1; σ_k from the same reply; μ_k from its mean/√k
at k ≤ 20 and from θσ²/2 at k = 30; |θ′| from differences of the listed roots):

| k | θ_k | −d ln ψ*/dk | gap | formula (2) |
|---|---|---|---|---|
| 5 | 0.607 | 0.583 | 0.024 | 0.0044 × 2.28 = 0.010 |
| 10 | 0.585 | 0.553 | 0.032 | 0.0071 × 2.90 = 0.021 |
| 20 | 0.514 | 0.463 | 0.051 | 0.0112 × 3.80 = 0.043 |
| 30 | 0.402 | 0.284 | 0.118 | 0.0242 × 4.52 = 0.109 |

(At k = 40 the correction exceeds the root and the expansion is void.) The gap is the curvature of the root
times the reach of a jump.

*Scaling form.* When the one-step law is extensive, μ_k = A·b(x), σ_k² = A·v(x), θ_k = Θ(x) at x = k/A (the collapse
of L9.1: A = 63 and 84 agree to 0.008), (2) reads

    V′(x) = Θ(x) − ½·|Θ′(x)|·b(x)     per cell,    plus a total of ∫ |Θ′|/Θ dx nats that does not grow with A.

**The correction does not vanish as A grows**, because the jump is extensive: b is a density per generation
(0.02–0.05). Th was the statement b = 0, the limit of infinitely many infinitesimal steps.

*The exact statement [sketched].* If the laws of (k′ − k)/A under T_A(⌊xA⌋, ·) satisfy a large-deviation
principle with speed A and rate I(x → y), then −(1/A)·ln ψ*_A(⌊xA⌋) → V(x), the smallest cost of a finite path to 0:

    V(x) = min_y [ I(x → y) + V(y) ],   V(0) = 0;   equivalently V is the largest function with V(0) = 0 and
    V(x) − V(y) ≤ I(x → y) for all x, y.                                                                     (3)

This is the discrete-time quasi-potential; for density-dependent chains it is in the literature (I cite from
memory Morrow–Sawyer 1989 for Wright–Fisher-type chains, Klebaner–Zeitouni 1994 for density-dependent branching,
Kifer's 1988 book; none opened; a request is in `library/requests.md`). What I have proved are the two finite
statements 17.2 and 17.3, which in this limit read

    sup_κ κ·Θ(κ)  ≤  V(ρ)  ≤  ∫₀^ρ Θ(x) dx      (Θ non-increasing; ρ the mean density),

with equality on the right for branching rows (17.4 b) and in the limit b → 0 (17.4 a).

*Numbers* (`python3 bellman.py` in this directory: a calculator that evaluates (3) with the Gaussian rate
I = (y − x − b)²/2v, b = Θv/2, on eleven roots and five standard deviations copied from the critic's replies to
rounds 2 and 3; nothing is fitted):

| | per cell |
|---|---|
| block bound, sup κΘ(κ), attained at κ = 0.35 | 0.144 |
| **V(ρ), recursion (3)** | **0.218** (0.214 … 0.221 when the variance is multiplied by 1.25 … 0.8) |
| first-order value, ∫Θ − ½∫\|Θ′\|b | 0.220 |
| local-root integral ∫Θ | 0.2295 |
| measured: slope of ln τ, 45 → 63 → 84 → 108 → 135 | 0.212, 0.212, 0.218, 0.221 |
| measured: slope of −ln ψ*(K − 1) between tables, 45 → 63 → 84 (L9.1) | 0.219, 0.214 |

So: **the exponent of the face law is the discrete-time quasi-potential of the population's one-step law, a
functional of two functions of the density, the local root Θ and the step variance v**; the local-root integral
overshoots it by 5% and the block bound undershoots by a third. This replaces Th. It is a statement about the
pooled table, to which Theorem P̄ reduces the hazard exactly; it is not derived from the rule.

Three remarks.
1. *The minimising path* of (3) (printed by the script, as populations at A = 84): 36.5, 32.0, 27.1, 22.5, 18.3,
   14.5, 11.3, 8.8, 6.7, 5.1, 3.9, 2.9, 2.2, 1.7: four to five cells a generation down to about 18, then a factor
   0.77 a generation, the geometric descent of a branching chain conditioned to die (17.4 b). This is the path
   of the *pooled chain* (the lab's reversed chain has ratios 0.79, 0.77, 0.73 at 9.8 → 4.3, L5.3); the recorded
   histories fall about twice as fast on hulls and three times as fast on the slab (16.3), and nothing here
   explains that. For the pooled chain the time from half the mean to death grows like ln A, not √A.
2. *"The cost per cell is still rising"* (PROBLEM.md, second row of the table). With the roots as they are at
   A = 84 the slope is 0.218. Between A = 63 and 84 the roots at fixed x rose by 0.008, 0.007, 0.004, 0.003, 0.000,
   0.001, 0.005 at x = 0.15, …, 0.45 (45 → 63: 0.017 at x = 0.15). If that is the tail of the drift, the hull's
   local slope levels off at **0.220 ± 0.006** **[guessed]**; the measured 0.218 and 0.221 are at it. After 16.3
   this is worth less than it looks: faces of A ≤ 84 are mostly rim, and the roots may go on drifting towards
   the slab's.
3. *What a formula from the rule would have to supply*: Θ and v. The low-density end, Θ(0+) ≈ 0.60, is the
   per-cell extinction exponent of a sparse face; 2·(mean step)/(variance) reproduces it from a growth of about
   22% a generation and a variance of 0.79 per cell at k = 5–10. Entry 19 shows that independent cells do not
   give it.

**17.6 "Why area", restated as one conditional theorem.**
*Two-patch identity [proved].* If a face is the union of two patches that step independently given their
populations k₁, k₂, the row transform of the total is M¹_{k₁}(s)·M²_{k₂}(s). So s is below the root of the union as
soon as it is below both patch roots; two equal patches at equal populations have the root of one; means and
variances add. Collapse of the roots in k/A is one-step extensivity.

**Theorem Q [proved from P̄ and T′].** Fix κ, θ₀ > 0 and k₀. Suppose that for every face size A of a family the
pooled one-step table of the face population has θ_k ≥ θ₀ for all k₀ ≤ k < K := ⌈κA⌉ (hypothesis R(κ, θ₀, k₀)).
Then over any window

    Deaths ≤ D(n ≥ K) + Σ_{z ≥ K > z′} F(z, z′)·e^{−θ₀(z′ − k₀)⁺} + E[ψ(Z_{t₀})],

so if no face dies directly from K cells or more and the downward crossings of K undershoot by a bounded
exponential moment (E_cross[e^{θ₀(K − z′)}] ≤ C; on the tables the crossing term is carried by drops of one to
three cells, L5.1), then ln τ ≥ θ₀·(κA − k₀) − ln C − (window term).
On the numbers of L9.1 and L5.2, R(0.35, 0.40, 5) holds at A = 45, 63, 84 (roots at x = 0.35: 0.407, 0.411, 0.411;
roots at k = 5…8: 0.53–0.61; decreasing in between) and fails at A = 30 (roots 0.03–0.09 lower). The exponent it
proves is 0.14, two thirds of the measured one. I have not seen the rows themselves; the lab should confirm
min_{5 ≤ k < 0.35A} θ_k and say how small k₀ can be taken (request LR9).
What is assumed is a one-step property, row by row: sparse faces regrow, with an exponential rate bounded
below, up to a fixed fraction of the area. What makes the hypothesis scale with A is extensivity. What is
concluded is the many-step statement. The hypothesis is not derived from the rule, and R5 (entry 4) says it
cannot follow from the graph and θ alone.

---

## 2026-11-14, entry 18. A comparison form of Theorem P̄, and why the committor falls with the size of the face

The critic's pointer (reply to round 3, §3) is source's remark: if a stochastically monotone kernel q is
dominated row by row by the true one-step kernel of the population *at every time*, then P(T > t) ≥ P_q(T > t).
The lab found the pooled tables monotone and ordered in A, and noted that a pooled table is an average over
time, which that lemma does not cover. In the pooled setting the certificate of Theorem P̄ needs less.

**Lemma C [proved].** Let q be a stochastic kernel on {0, 1, 2, …} with 0 absorbing, whose rows 1, …, K − 1 are
stochastically non-decreasing in the row index. Let ψ_q be its committor for 𝓛 = {1, …, K − 1} (death before
reaching K or more; ψ_q(0) = 1, ψ_q(k) = 0 for k ≥ K). Suppose that every row k ∈ 𝓛 of the pooled table, with its
censored mass placed at +∞, dominates the same row of q:

    d̄(k) + Σ_{k′ ≤ j} T̄(k, k′)  ≤  q(k, [0, j])     for every j ≥ 0.

Then ψ_q is a supersolution of (∗̄) on 𝓛, so Theorem P̄ holds with ψ = ψ_q, and ψ* ≤ ψ_q.

*Proof.* (i) ψ_q is non-increasing in k. Couple two copies of the q-chain from k₁ ≤ k₂ so that they stay
ordered while both are in 𝓛 (monotone rows). If the upper copy reaches 0 before reaching K, the lower copy,
which is below it until then, has reached 0 no later and has not reached K. (ii) For a non-increasing function
vanishing at +∞, the mean under a dominating law is smaller:
d̄(k) + Σ_{k′ ∈ 𝓛} T̄(k, k′)ψ_q(k′) ≤ Σ_{k′} q(k, k′)ψ_q(k′) = ψ_q(k). ∎

*Smallest case.* 𝓛 = {1}, K = 2: ψ_q(1) = q(1, 0), and the hypothesis at j = 0 is d̄(1) ≤ q(1, 0) = ψ_q(1), which is
(∗̄) for one row.

No uniformity in time is needed, because Theorem P̄ bounds deaths over exposure in the window, which is the
measured hazard, and uses the pooled table only through (∗̄).

**Corollary [proved; its hypotheses are the lab's L9.2].** If the table of a face of A cells is monotone on
its rows below K, and the table of a face of A′ cells dominates it row by row there, then ψ*_{A′}(k) ≤ ψ*_A(k) for
k < K. The lab found both hypotheses to hold on the four tables up to small violations in rows 2 and 3
(largest excess of a distribution function 0.007, 0.002, 0.04), and found ψ*_A(k) non-increasing in A for
k ≤ 12 with one exception of one standard error. So the monotonicity that H′ (inequality form, 15.1) needed is
the many-step shadow of a one-step ordering: *a larger face regrows from k cells at least as well as a smaller
one*. As the critic says, this bounds ψ*_A(k) only for k below half the smallest face; reaching k = κA needs a
comparison chain that grows with A, and the only family I can name is the extensive one of 17.6.

---

## 2026-11-14, entry 19. Dead end: the exponent from independent cells (mean field)

Tried because entry 17 reduces γ to two functions and "a formula from the rule alone" is on the list of what
would count. Recorded with its numbers so that nobody repeats it.

**The closure.** Treat every cell of a layer as an independent coin: a cell of layer ℓ with density x_ℓ is alive
next with probability F_ℓ = x_ℓ·P(n ∈ S) + (1 − x_ℓ)·P(n ∈ B), n a sum of independent binomials over the layers
of its neighbours (gump: 6 in its layer, 2 and 1 in the next two layers on each side; fcc: 6, 3, 3; the 2D
rule: 4, 1, 1; face12e: entry 20). The layer populations are then binomial, the one-step rate is
I = Σ_ℓ w_ℓ·KL(y_ℓ ‖ F_ℓ(x)), and (3) gives a number from the rule and the lattice alone. V1: the face fluctuates, the
layers beneath are pinned at the closure's own profile. V2: the top two layers fluctuate.
`python3 mf_deadend.py 100` (a calculator; about a minute):

| system | closure's densities: face, next layer, bulk (measured) | V1 | V1, decreasing paths only | V2 | measured |
|---|---|---|---|---|---|
| gump B45/S345 | 0.565, 0.466, 0.444 (0.517, —, 0.411) | 0.187 | 0.318 | 0.130 | 0.209–0.212 |
| gump lattice B456/S3456 | 0.679, 0.547, 0.521 (0.62, —, —) | 0.247 | 0.696 | 0.086 | 0.2156 |
| fcc B45/S345 | 0.577, 0.410, 0.444 (0.465, —, 0.394) | 0.162 | 0.258 | 0.085 | 0.181 |
| 2D rule B34/S234 | 0.664, 0.576, 0.520 (0.577, —, 0.472) | 0.447 | 0.684 | 0.348 | 0.346 (ends), 0.41 (ring) |
| face12e, per wall face | sheet 0.640, layer 0.454, bulk 0.444 (0.52, 0.41, 0.397) | — | — | 0.283 | 0.410 |

(Measured densities: `research/audit/REVIEW-class.md` §2.2, §3.1; toy2d README. V2 still falls by about 0.005 from
a 61² to a 101² grid.)

**Why it is a dead end.**
1. *Its cheapest route is one the faces do not take.* The minimising path of V1 does not go down: it
   oscillates with period two and growing amplitude, reaches density 0.79 (gump), 0.78 (fcc), 0.93 (2D rule),
   and then loses nearly everything in one generation to overcrowding (gump: 0.79 → 0.17), below the closure's
   threshold, whence it decays for nothing. V2 does the same with both layers dense (0.73 and 0.65, then 0.22
   and 0.16). Gump's faces die the other way: overcrowding events become rarer before a death (0.035 per cell
   against 0.073; PROBLEM.md, the overcrowding row) and the layer beneath sags. Independent cells make a
   simultaneous overcrowding of a whole face far too cheap. The nearness of V1 to the measured exponents
   (−11%, +14%, −10%, +29%) is that of a different event. Restricted to paths of decreasing density, the route
   the faces do take, the closure gives 0.32, 0.70, 0.26, 0.68: 40% to 220% too much.
2. *It does not converge.* Freeing a second layer lowers the value by 22–65%, to 30–60% below the measured
   exponents in three dimensions; a third layer can only lower it further.
3. *Its one-step statistics have the wrong shape.* For gump the closure's face map has F(x) < x below
   x = 0.07–0.09: a sparse face of independent cells does not regrow (one live cell has 7p³ ≈ 0.6–0.7 expected
   successors). Its local root is absent below x = 0.07, is 0.18 at x = 0.10, and rises to 1.18 at x = 0.35.
   The measured root is 0.60 at x = 0.06–0.10 and *falls* to 0.41 at x = 0.35. The measured sparse face regrows
   because its live cells are clustered (the favoured three-cell state is the top of one cube); the closure
   has no clusters. And the real exponent is made mostly at low density (∫₀^{0.25} Θ is 62% of ∫Θ), where the
   closure has nothing.
4. *A false positive.* For the edge of Moore B456/S3456 (2 in-row neighbours, 3 beneath) one layer over the
   closure's bulk gives 0.33, by a decreasing path; the measured edges erode (τ_edge falls with L; toy2d
   README §3).
5. Gump's four neighbours of R5 come out smaller than gump (one layer over the closure's bulk: B45/S34 0.119,
   B45/S35 0.053, B45/S45 0.045, B4/S345 0.016, gump 0.181), but in the wrong order for B4/S345, which has the
   longest measured lifetimes of the four.

**What survives.** Only the form: an extensive one-step law and a discrete-time path. And a warning for (3): the
recursion has to be allowed rising paths before it is trusted. In entry 17.5 I restricted it to decreasing
ones, because the tables hold no rows above the mean; what licenses that for gump is a measurement, not the
recursion: no face died directly from the mean or above at A ≥ 45, and the crossing term of Theorem P̄ is
carried by drops of one to three cells (L5.1). A formula from the rule needs the growth of sparse *clusters*
over the true layers beneath, a spatial problem that densities do not see.

---

## 2026-11-14, entry 20. The second lattice (face12e) in the language of Proposition S

Face12e: gump's cells and rule, the four coplanar neighbours at ±2e_b, ±2e_c (edge-sharing) instead of
±2e_b ± 2e_c. Vessel of the measured wall law (`research/audit/REVIEW-class.md` §2.2): a slab between two walls
at odd x, periodic in y and z; wall = sheet of x-normal cells at x = C. Write Σ for that sheet (A cells) and Λ
for the y- and z-normal cells at x = C − 1 (2A cells).

**Lemma F [proved, by the offsets].** In a slab at least two cubes deep, periodic in the wall directions:
(i) a cell of Σ has 4 neighbours in Σ, 4 in Λ, 4 outside the vessel, none elsewhere;
(ii) a cell of Λ has 6 neighbours in Λ (4 perpendicular ones at (C − 1, y ± 1, z ± 1), 2 coplanar ones along its
own line), 2 in Σ, 2 in the next sheet x = C − 2, 1 in the next layer x = C − 3, 1 outside the vessel;
(iii) W = Σ ∪ Λ is sealed (θ = 4), and it is inclusion-minimal: no non-empty proper subset of W is sealed.
*Proof.* (i), (ii): an x-normal cell p has neighbours p ± 2e_y, p ± 2e_z (same sheet) and p ± e_x ± e_y, p ± e_x ± e_z
(layers x ± 1). A y-normal cell p at x = C − 1 has p ± 2e_x (x = C + 1, outside, and x = C − 3), p ± 2e_z (in Λ),
p ± e_y ± e_x (x-normal, in the sheets x = C and x = C − 2), p ± e_y ± e_z (z-normal, in Λ). (iii) Cells of Σ have no
neighbour in V \ W, cells of Λ have exactly 3: sealed. Let W′ ⊆ W be sealed and non-empty. If W′ contains a cell
of Λ, that cell already has its 3 allowed outside neighbours in V \ W, so all its 8 neighbours in W are in W′;
Λ is connected through in-layer neighbours and every cell of Σ is next to a cell of Λ, so W′ = W. If W′ ⊆ Σ, each
of its cells has 4 neighbours in Λ, outside W′: not sealed. ∎

So Σ alone is not sealed (the audit's "the wall sheet alone is not sealed" and its measurement that the sheet
alone empties 4–10 times as often as a wall dies, and comes back), and by Proposition S a permanent loss at a
wall is the extinction of W: the audit's "a wall dies when the sheet and the layer beneath are empty together".
In W only the cells of Λ see the rest of the vessel, 3 neighbours each, exactly as a gump face cell sees what
is beneath it; the cells of Σ see only W. That is the structural reason for counting the law per cell of Λ.
*Not proved:* that W has the fewest cells among sealed sets of the slab (3A; a transverse band of three layers
has more at the measured sizes). Lab request LR12.

**What the formula of entry 17 gives there.** No number without that lattice's own one-step table: γ is a
functional of Θ and v, and these are not inherited from gump. What can be said:
- The statistic should be the population of Λ (2A cells, mean density 0.41), with "death" its emptiness, which
  the audit found to have the same waiting time as the permanent death (ln τ 6.39 against 6.43, 10.18 against
  10.18).
- The measured 0.205 per cell of Λ is γ/ρ = 0.50 per unit of mean density, against gump's 0.41–0.43
  (0.212/0.517 on slabs, 0.218/0.505 on the hull tables). The root vanishes at the mean density. If Λ's root
  curve were gump's, compressed to [0, 0.41] at equal step variance per live cell, the exponent would be
  (0.41/0.505) × 0.218 = 0.177; to give 0.205 Λ's roots must be about a sixth higher than gump's at the same
  fraction of the mean density. So, as far as this framework sees, the near-equality of the two exponents per
  cell (0.205; 0.209–0.212) is **not** explained by "the same neighbour counts": it is a lower density
  compensated by a steeper root, which the two extra neighbours in the sheet would have to supply. **[guessed]**
- The test is exam entry E4 (filed today): tally Λ's one-step table at one size, run `bellman.py` on its roots
  and variances, and compare with 0.205.
For fcc the same ratio is 0.181/0.465 = 0.39, close to gump's; I have no table for it either.

---

## Round 4 report

**Exam** (entry 16). E1 holds: notched row 0.3458 ± 0.0036 (predicted 0.345 ± 0.020), intact row of the same
strips 0.412. G1's first half (every edge with an end: 0.34–0.35) is measured in a geometry made to test it; its
second half (the ring carries a power) is undecided by the same table (ring minus notched grows like
L^{1.7 ± 0.2} or like 0.065·L). E2 is not refuted but its number is too high at L = 36 (7.99 ± 0.38 against
9.8 ± 1.0): no flash, a remnant of 8–9 cells that does not grow. E3 fails: on a rim-free face the last 18 cells
go in four generations (hull: six or seven); the last generation alone is common to both vessels.

**Fell.** "One remnant, the same in every vessel" (E3): refuted; Dr holds on hulls only. Th (ln τ = A·∫Θ):
withdrawn; the sum is an upper bound (T), exact only without jumps or with root-preserving rows (17.4). The
ring part of W (power ½): withdrawn; a product of pair weights cannot give more than ½ (16.1). The mean-field
value (entry 19): a dead end; its cheapest route is an overcrowding of the whole face, which gump's faces do
not take.

**Claims.**
- **T′, T** (17.2, 17.3): for any one-step table, (K − k₀)·min θ_k ≤ −ln ψ*(K − 1) ≤ Σ θ̂_k + const, the first from
  a supersolution, the second from a concave subsolution. **[proved]**
- **Exactness** (17.4): the sum is the exponent for skip-free rows and for branching rows. **[proved]**
- **Q** (17.6): under R(κ, θ₀, k₀) (local roots ≥ θ₀ for k₀ ≤ k < κA, at every size), ln τ ≥ θ₀(κA − k₀) − const.
  **[proved; the hypothesis is one-step, holds on the lab's numbers at A = 45, 63, 84 with (0.35, 0.40, 5), and
  is not derived from the rule]** It gives 0.14 per cell.
- **C** (entry 18): pooled rows dominating a monotone kernel make that kernel's committor a certificate for
  Theorem P̄; no uniformity in time. Corollary: the committor at fixed k falls with the size of the face
  because larger faces' rows dominate. **[proved; hypotheses are lab L9.2]**
- **V** (17.5): the exponent is the discrete-time quasi-potential (3) of the population's one-step law;
  V′ = Θ − ½|Θ′|b to first order. **[sketched]** Evaluated on the critic's numbers for A = 84: 0.218, between the
  proved bounds 0.144 and 0.2295; measured 0.212–0.221. Reading: the hull's local slope levels off at
  0.220 ± 0.006. **[guessed]**
- **F** (entry 20): in face12e the wall's sheet plus the layer beneath is an inclusion-minimal sealed set; only
  the layer's cells see the rest of the vessel. **[proved]**

**Weakest step.** V. Its two bounds are proved; the value between them is a Gaussian closure fed with eleven
roots and five standard deviations copied from the critic's replies, run on decreasing paths only (licensed
for gump by a measurement, no deaths from above the mean, not by an argument), and extensivity of the one-step
law is seen at two sizes (63, 84) of a vessel whose faces are mostly rim (E3). Second: entry 17 is about the
pooled table. Theorem P̄ makes that exact for the hazard, but hypothesis R is a property of the chaos, the
population hides the second variable a death path carries (16.3), and I have no route from the rule to R:
entry 19 shows the obvious closure failing exactly where the exponent is made (sparse faces).

**Lab requests** (all exact or arithmetic on `critic/lab/data/fluct_tables.npz`).
- LR9. Per row and size: mean, variance and third cumulant of the one-step change divided by A, against x = k/A
  (do they collapse as the roots do?); min_{k₀ ≤ k < 0.35A} θ_k at each size for k₀ = 3, 4, 5 (hypothesis R of
  Theorem Q); the smallest k from which the roots are non-increasing.
- LR10. Recursion (3) on the rows themselves: (a) Gaussian, `bellman.py table.json` with every row's θ_k and
  variance, at each size, against the slopes 0.201, 0.212, 0.212; (b) with each row's own rate
  I_k(j) = sup_s[−s(j − k) − ln M_k(s)] in place of the Gaussian.
- LR11. The extensive chain, exactly: q(2k, ·) = T̄₈₄(k, ·) ∗ T̄₈₄(k, ·), q(2k + 1, ·) = T̄₈₄(k, ·) ∗ T̄₈₄(k + 1, ·) (rows as laws
  on {0, 1, …}, T̄(0, ·) the point mass at 0), low set {1, …, 2K − 2}; then the same doubling once more. Predicted:
  the second doubling adds 168 × (0.218 ± 0.007) = 36.6 ± 1.2 to −ln ψ* at the top row; the first adds half that
  up to a constant of order one nat (the doubled chain's lowest rows are two independent small faces, which
  regrow worse than one). Also both sides of (1) for q.
- LR12. Smallest sealed sets of the face12e slab (periodic wall 3 × 3 or 4 × 4, two to four cubes deep), by the
  enumeration used for hulls: is the sheet plus the layer beneath (3A cells) the smallest, and which other
  inclusion-minimal ones are there?

**Exam.** E4 filed: `bellman.py` on the one-step table of (a) the rim-free gump slab face of 60 cells, predicted
0.211 ± 0.012; (b) the layer beneath a 5 × 5 wall of face12e, predicted 0.205 ± 0.015 per cell.

**Whether to go on.** One closing round is worth having once LR10, LR11 and the outcome of E4 exist: to
state γ = V[Θ, v] with the lab's exact numbers or to withdraw it. Beyond that I see no route on this line to a
new proved step about the rule itself: what is missing is a derivation of the sparse-face root from the rule
(a branching of clusters over the true layers beneath), and the power of L on a ring, and neither is a
large-deviation question.
