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
