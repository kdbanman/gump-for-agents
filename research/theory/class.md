# G3 / S7 — what is the class of "gumps"?

*Class agent, 2026-11-13. Tags: **[proved]** (argument given here), **[computed]** (exact finite computation, command
given), **[measured]** (n, error, command), **[conjecture]**. Scripts, predictions and data: `research/theory/class/`
(run commands from there). Bulk output: `research/scratch/class/`. Predictions were committed before testing
(`class/PREDICTIONS.md`, commits 5636f1c, cb98e1b and the stage-3 note after it); the scorecard is §6.*

@@SUMMARY@@

## 1. The abstract setting, and what can be proved in it

### 1.1 Setting

A **cell lattice** is a discrete set V ⊂ R^d, invariant under a full-rank lattice Λ of translations with finitely
many orbits (*cell types*), together with a finite set of offsets O(p) ⊂ R^d ∖ {0} for each cell p, depending only on
its type, such that N(p) = p + O(p) ⊂ V and the relation is symmetric: q ∈ N(p) ⇔ p ∈ N(q). K(p) = |O(p)|.
*One type* means V is a single Λ-orbit; then O = −O and K is even. (`lattices.py` holds 29 of them — square, triangular,
honeycomb and kagome families, the face lattice of the cubic honeycomb with four neighbourhoods, FCC, BCC, simple
cubic with 6, 18, 26, the 3D cross — each checked for symmetry.)

A **rule** is outer-totalistic (B, S); b = min B ≥ 1. The **capped threshold** (b, c) is B = {b, …, c−1},
S = {b−1, …, c−1}: *alive next iff n + x ≥ b, except that n ≥ c dies*. Gump is (4, 6) on the face lattice; the 2D
gump is (3, 5) on the range-2 cross; Conway's Life is (3, 4) on Moore (not confined: b = 3 < 4).

A **vessel** is a subset V′ ⊆ V whose outside is dead forever. For a linear functional u (a *direction*) write

  a⁻_u(p) = #{o ∈ O(p) : u·o < 0},  a⁰_u(p) = #{u·o = 0},  a⁺_u(p) = #{u·o > 0},  c(u) = max_p a⁻_u(p).

When u(V) is discrete, the level sets of u are *layers* and (a_k) = number of offsets at layer offset k is the layer
histogram (T1). For one type, a⁻ = a⁺ = (K − a⁰)/2.

### 1.2 Theorem A — confinement [proved]

**(i)** If c(u) ≤ b − 1, then for every C the set {p : u·p > C}, once dead, is dead forever (every rule with minimum
birth count ≥ b). **(ii)** If c(u) ≥ b this fails: there are C and a configuration inside {u·p ≤ C} whose successor has
a live cell outside. So *u is sealed for b iff c(u) ≤ b − 1*.
**(iii)** If u′ is a specialisation of u (sign(u′·o) ∈ {0, sign(u·o)} for every offset o) then c(u′) ≤ c(u). Hence the
least c(u) is attained on the finitely many *rays* (directions orthogonal to d − 1 independent offsets), and the set
U_b of sealed directions is a union of faces of the arrangement of the hyperplanes o^⊥, closed under specialisation.
**(iv)** For one type: a generic direction has c(u) = K/2. So if b > K/2 every direction is sealed (a pattern never
leaves its convex hull); if b ≤ K/2 exactly the non-generic directions with **a⁰_u ≥ K − 2b + 2** are sealed — in the
plane a finite set of rays.
**(v) Hull.** A finite pattern X stays inside hull_b(X) = ∩_{u ∈ U_b} {p : u·p ≤ max_X u·x} forever, and the hull never
grows. It is bounded iff U_b positively spans; then every finite pattern is eventually periodic.

*Proof.* (i) A dead cell p with u·p > C has at most a⁻_u(p) ≤ b − 1 neighbours in {u·q ≤ C}, all others are dead.
(ii) Take p with a⁻_u(p) ≥ b, put C = max{u·(p + o) : u·o < 0} < u·p and make exactly b of those neighbours alive:
p has n = b ∈ B. (iii) Moving from u to u′ only turns negative signs into zeros. Any u specialises to a ray because
the offsets span R^d. (iv) O = −O. (v) Apply (i) to each sealed u with C = max_X u·x; the new maxima are no larger. ∎

*Hull shapes* [computed, `python3 theory.py table`; §2]: the polytope whose facet normals are the sealed rays —
rectangle (every cross), octagon (Moore, b = 4), hexagon (triangular), octahedron (face lattice, FCC), rhombic
dodecahedron (BCC), box (simple cubic 6 and 18, 3D cross), the 18-faced {100}+{110} solid (3D Moore, b = 10).
In every 3D lattice of §2 no 1-dimensional family of directions is sealed at the tight b, so the hull is a polytope.

This is Eppstein's bounding-box/diamond argument (PRIOR-ART topic 1) for an arbitrary lattice and direction; the
iff, the specialisation order and (iv) are what I add.

### 1.3 Theorem B — firewalls [proved]

Let u be a sealed rational direction on a one-type lattice, layers numbered consecutively, (a_k) the histogram,
A(j) = Σ_{k ≥ j} a_k, r = max{k : a_k > 0} the reach. A band of w consecutive layers is sealed (stays dead whatever
lies on both sides) iff

  max_{1 ≤ j ≤ w} [A(j) + A(w + 1 − j)] ≤ b − 1.

If b is tight (b = A(1) + 1) this forces w ≥ r + 1, and then no pair of neighbours straddles the band: the two
sides never influence each other again. w = 2r always suffices.

*Proof.* A cell in the j-th layer of the band has A(j) neighbours below the band and A(w + 1 − j) above it. With
j = 1 and A(1) = b − 1 the condition gives A(w) = 0, i.e. w > r. For w = 2r one of j, 2r + 1 − j exceeds r. ∎
Gump: A = (3, 1), w = 3. Cross of range r: A(j) = r − j + 1, w = r + 1. FCC, BCC, simple cubic: w = 2.
(`theory.firewall_width` handles several types by direct enumeration.)

### 1.4 Theorem C — sealed sets [proved]

W ⊆ V′ is **sealed** if each of its cells has at most b − 1 neighbours in V′ ∖ W. A dead sealed set stays dead whatever
happens elsewhere; if W is not sealed some configuration with W dead has a birth in W; unions of sealed sets are
sealed, so the largest dead sealed set K(t) only grows. (Lemmas 1–2 of `thickness.md`, verbatim with 3 → b − 1.)

**C1 (forward-count criterion).** Let v be a linear functional. If every cell p of the vessel has at least b
neighbours q in the vessel with v·q > v·p, the vessel contains no finite nonempty sealed set.
*Proof.* A cell of a finite W maximising v has all those ≥ b neighbours outside W. ∎

**C2 (dichotomy, one type, full lattice).** Finite sealed sets exist **iff b > K/2**.
*Proof.* If b ≤ K/2 take v generic: every cell has K/2 ≥ b forward neighbours (C1). If b ≥ K/2 + 1, choose one
offset o_1, …, o_{K/2} from each ± pair and let Z = {Σ_{i ∈ I} o_i : I ⊆ {1, …, K/2}} (a discrete zonotope, ≤ 2^{K/2}
cells). For z = Σ_I o_i and each j, z + o_j ∈ Z if j ∉ I and z − o_j ∈ Z if j ∈ I: every cell of Z keeps at least one
neighbour of each ± pair inside Z, so at most K/2 ≤ b − 1 outside. ∎
(The kagome hexagon of T6 and the Moore octagon for b = 5 are instances.) Together with Theorem A(iv):

  **outside sealed and inside unsealable  ⇔  (K − a⁰)/2 < b ≤ K/2.**

For several types C1 gives "no finite sealed set if some generic v has ≥ b forward offsets for every type"; where
that fails sealed sets may exist (honeycomb with 9 neighbours, b = 5: a 292-cell sealed set by peeling,
`python3 indices.py hex9`) [computed].

**C3 (faces cannot die piecewise).** In a half-space vessel {u·p ≥ h₀} of a one-type lattice, with u sealed, let ō
denote projection to the plane u^⊥. If some in-plane v₀ (generic for the in-plane offsets) has

  #{inward offsets o (u·o > 0) with v₀·ō ≥ 0} ≥ b − a⁰/2,

there is no finite sealed set: no finite part of a face can die for good. *Proof.* C1 with v = v₀ + εu, ε → 0⁺: a
boundary cell has a⁰/2 in-layer forward neighbours plus those inward ones; deeper cells have at least as many. ∎

**C4 (slabs and critical thickness).** In a slab of m layers the far face needs the mirror condition, so one needs a
single v₀ with at least b − a⁰/2 of the projected inward offsets of reach ≤ m − 1 strictly on **each** side, for
every cell type. Call m* the least m with such a certificate. In the "half in-plane" case b = a⁰/2 + 1 the condition
is that 0 has half-space (Tukey) depth ≥ 1 among those projected offsets for every type simultaneously. **This is
what gump's identity ē = −2(ā + b̄) certifies**: it is a positive linear relation 2ā + 2b̄ + ē = 0, i.e. 0 lies inside
the triangle of the three projected inward offsets, and ē is only available from the third layer on; with two
layers the three types' pairs {p₁,p₂}, {p₂,p₃}, {p₃,p₁} (p₁ + p₂ + p₃ = 0) cannot be split by one line.
[computed, `theory.py table` for the certificate, `pits.py LATTICE b M` for explicit sealed sets by peeling:]

| lattice | gump | face18 | FCC | BCC (8 and 14) | sc18 | sc6 | 3D cross r = 2 | bond10 | face8 |
|---|---|---|---|---|---|---|---|---|---|
| m* (certificate) | 3 | 3 | 2 | 2 | 2 | 1 | 1 | none at any m | none at any m |
| sealed set found in m* − 1 layers | yes (2: 108 cells) | yes | yes | yes | yes | — | — | **yes in 4 layers** | 2 layers yes, 4 no |

So "three layers" is special to the face lattice; FCC and BCC need two, the simple-cubic crosses one. **bond10 is a
counterexample to the converse of C2 for slabs**: no finite sealed set in the full lattice (b = 4 ≤ 5), but a slab of
any thickness I tried can be pierced by a finite dead tube. In two dimensions a strip can always be cut by a
transverse firewall, which is finite, so m* does not exist there.

**C5.** As in `thickness.md` Thm 3: on a torus every component of a sealed set wraps; in a hull vessel every component
touches the outside (whenever C1 holds for the full lattice).

### 1.5 Theorem D — the two-sided threshold lemma [proved; identities checked]

Finite vessel, symmetric adjacency A (any graph), capped threshold (b, c); n = Ax.

- **Lower rule U** "alive next iff n + x ≥ b": energy E(t) = −x(t)ᵀ(A + I)x(t−1) + (b − ½)(|x(t)| + |x(t−1)|).
  The capped rule differs from U exactly at overcrowded cells (n ≥ c), and E(t+1) − E(t) = D − Q with Q ≥ 0 and
  D = Σ over **O1 events** (n_i(t) ≥ c and x_i(t−1) = 1) of (n_i + x_i − b + ½). (This is T5.)
- **Upper rule C** "alive next iff n ≤ c − 1": a symmetric threshold network with weights −A, so it too reaches
  period ≤ 2. Energy E′(t) = +x(t)ᵀA x(t−1) − (c − ½)(|x(t)| + |x(t−1)|). The capped rule differs from C exactly at
  **undercrowded** cells (n + x ≤ b − 1), and E′(t+1) − E′(t) = D′ − Q′ with Q′ ≥ 0 and
  D′ = Σ over **U1 events** (n_i(t) + x_i(t) ≤ b − 1 and x_i(t−1) = 1) of (c − ½ − n_i).

*Proof of the second.* By symmetry of A, E′(t+1) − E′(t) = −Σ_i (x_i(t+1) − x_i(t−1))(c − ½ − n_i(t)). Where the cell
obeys C: a rise 0 → 1 needs n ≤ c − 1, a fall needs n ≥ c; either way the term is −|c − ½ − n| ≤ −½. Where it does
not (n ≤ c − 1 but x(t+1) = 0, i.e. n + x ≤ b − 1) the term is x_i(t−1)(c − ½ − n_i) ≥ 0. ∎

**Consequences.** (a) No O1 events from some time on ⇒ period ≤ 2; no U1 events from some time on ⇒ period ≤ 2.
(b) Every orbit of period ≥ 3 has both kinds; over a period ΣD = ΣQ and ΣD′ = ΣQ′. (c) *A capped threshold is the
conjunction of a ferromagnetic and an antiferromagnetic symmetric threshold network, each a gradient system; it can
only be chaotic where both constraints stay active.* A bulk that is dense enough never to starve a cell is governed
by C alone and freezes; one sparse enough never to overcrowd is governed by U alone and freezes. This is the
structural reason a cap that is too high gives glass and one that is too low gives dust.
For any outer-totalistic rule the same works with any pair of thresholds and the exceptions as drive.
`python3 energy.py selftest` → ALL OK (both identities, every step, 10 vessels on 6 lattices).

### 1.6 Theorem E — armour (immortal walls) [proved]

In a vessel V′ let W be a set of cells each having at least b − 1 neighbours in W and at most c − 1 neighbours in V′.
If W is entirely alive at some time it is alive forever. *Proof.* Each cell then has b − 1 ≤ n ≤ c − 1. ∎
The largest such W is the (b − 1)-core of the subgraph induced on the cells of vessel-degree ≤ c − 1 (`armour.py`).

**Corollary (walls).** With u sealed, face-cell degree K_f = a⁰ + a⁻: if a⁰ ≥ b − 1 and **c ≥ K_f + 1**, a fully
live boundary layer of a slab is immortal — the face can never die, the hull can never shrink past it.

### 1.7 Corollary F — the window, and why the confining plane must hold two lines [proved, given F2]

One type, tight b (b = a⁻ + 1). Then a⁰ = K − 2b + 2 and K_f = K − b + 1.
- **F1** The cap can act on a face cell only if c ≤ K_f = K − b + 1; beyond that the face is a pure threshold layer
  (never overcrowded), and a wall if moreover K ≥ 3b − 3.
- **F2** [measured, no exception in 29 families; mean-field: f′(ρ*) > −1] the cap c = b + 1 never gives a chaotic
  bulk (B is the single count b; Life, (3, 4) on Moore, is the famous marginal member and it settles).
- Hence a capped threshold with a chaotic bulk and faces the cap can reach needs **b + 2 ≤ c ≤ K − b + 1**, so
  K ≥ 2b + 1, i.e. **b < K/2 strictly and a⁰ ≥ 4**: the confining hyperplane must contain at least two lines of
  neighbours. Lattices with a⁰ = 2 (Moore, von Neumann, triangular, kagome, honeycomb with ≤ 12) have b = K/2 and
  K_f = b + 1: every chaotic cap is out of reach of their faces.

### 1.8 Proposition G — no finite region is shielded [proved]

One type. If b ≤ K/2 < c < b + K/2, then for every finite set W and every configuration there are two
configurations of the outside giving different successors on W. *Proof.* The cell p of W furthest along a generic v
has f ≥ K/2 neighbours outside W and m ≤ K/2 live ones inside; the outside can set n(p) to any value in [m, m + f].
A next state independent of it needs that interval inside B (resp. S) — impossible unless c ≥ b + K/2 — or disjoint
from it — impossible unless b ≥ K/2 + 1 or m ≥ c, i.e. c ≤ K/2. ∎ T6 is the all-dead case. The 2D gump satisfies the
hypothesis; gump itself does not (c = 6 = K/2: a cell with six live neighbours behind it is dead next whatever lies
in front), nor does FCC (4, 6).

@@REST@@
