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
