# G3 / S7 — what is the class of "gumps"?

*Class agent, 2026-11-13. Tags: **[proved]** (argument given here), **[computed]** (exact finite computation, command
given), **[measured]** (n, error, command), **[conjecture]**. Scripts, predictions and data: `research/theory/class/`
(run commands from there). Bulk output: `research/scratch/class/`. Predictions were committed before testing
(`class/PREDICTIONS.md`: commit 5636f1c, then four dated appendices, each committed before the runs it concerns);
the scorecard is §6.*

## Summary

**The class.** For a capped threshold (b, c) — alive next iff n + x ≥ b, except n ≥ c dies — on a lattice with K
neighbours, write a⁻ for the most neighbours a cell has strictly behind a hyperplane direction, a⁰ for those in it,
K_f = K − a⁻ for the degree of a face cell. The rule is a gump when

1. **outside sealed** — b > a⁻ on a spanning set of directions [proved iff; the hull is the polytope of those rays];
2. **inside unsealable** — b ≤ K/2 [proved iff for one cell type: otherwise a discrete zonotope of ≤ 2^(K/2) cells
   can die for good]; so (K − a⁰)/2 < b ≤ K/2;
3. **cap within reach of the faces** — b + 1 ≤ c ≤ K_f, exactly a⁰ − 1 caps [proved: beyond K_f a live face is an
   immortal wall when a⁰ ≥ b − 1; and in a hull from the armour cap c_arm on];
4. **bulk driven on both sides** — a capped threshold is a ferromagnetic and an antiferromagnetic symmetric
   threshold network at once; each alone has period ≤ 2, so non-period-2 behaviour needs overcrowding *and*
   undercrowding events [proved: the two-sided threshold lemma]; whether a given cap is chaotic is **not predicted**;
5. **face not starved** — K_f·ρ/b ≳ 0.85 [measured, post hoc].

Evidence [measured]: of 50 lattice–cap pairs with a chaotic bulk and the cap within reach, 46 have a memoryless
face law (2 starve, 2 are glasses); all 38 pairs beyond reach with a⁰ ≥ b − 1 are walls, no exception.

**New gumps**, each with chaotic torus, memoryless face law and hull lifetimes growing to sparse debris:
**B2/S12 on the von Neumann neighbourhood** (4 neighbours; not predicted), B456/S3456 and B4567/S34567 on the
range-3 cross, **B45/S345 on FCC** (slope 0.19 per face cell, predicted 0.21 ± 0.07), **B34/S234 on BCC**,
B34/S234 on the face lattice with its 8 perpendicular neighbours, B2/S12 on the 6-neighbour cubic lattice (not
predicted), B6789/S56789 on the 18-neighbour cubic lattice, and — thinner hull evidence — B567/S4567 on BCC-14,
B34/S234 on the 3D range-2 cross.

**Two statements in the brief do not survive.** (a) Gump is not the only capped threshold on its lattice:
B456/S3456 has the identical slab face law (0.215 vs 0.212 per cell, five sizes) and lives ≥ 50× longer in
octahedra; B4567/S34567 has it too but freezes in octahedra (armour). (b) "The Moore neighbourhood has no such
rule" is right, but for a sharper reason than a count: with a⁰ = 2 exactly one cap is within reach of a face
(B4/S34), and its bulk is dead; von Neumann has the same structure and its one candidate, B2/S12, works.

**Scorecard** (§6): proved parts never failed. Of 28 "GUMP" calls committed before testing, 8 passed all three
tests, 6 more have the face law but no conclusive hull test, 14 failed (10 because the mean-field guess of the
chaotic cap was wrong); 14 of 15 explicit "not a gump" calls held; two gumps were missed outright.
The mean field picks chaotic caps at chance level and should be dropped.

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

### 1.7 Corollary F — how many caps a face can feel [proved]

One type, tight b (b = a⁻ + 1). Then a⁰ = K − 2b + 2 and K_f = K − b + 1. The cap can act on a face cell only if
c ≤ K_f; beyond that the face is a pure threshold layer (never overcrowded), and a wall if moreover a⁰ ≥ b − 1.
A rule with any births has c ≥ b + 1. So the caps within reach of the faces are

  **b + 1 ≤ c ≤ K − b + 1 — exactly a⁰ − 1 of them.**

The interval is nonempty iff b ≤ K/2, the same condition as unsealability (C2). So the number of neighbours in the
confining hyperplane counts the rules that can be gumps: lattices with a⁰ = 2 (Moore, von Neumann, triangular,
kagome, honeycomb) have b = K/2 and **one** candidate, c = K/2 + 1, the rule B{K/2}/S{K/2 − 1, K/2}; a⁰ = 4 gives three
(cross2: c = 4, 5, 6), a⁰ = 6 five (gump: c = 5…9), a⁰ = 8 seven. Whether a candidate
is chaotic in the bulk is a separate, measured matter (§3–§5).

### 1.8 Proposition G — no finite region is shielded [proved]

One type. If b ≤ K/2 < c < b + K/2, then for every finite set W and every configuration there are two
configurations of the outside giving different successors on W. *Proof.* The cell p of W furthest along a generic v
has f ≥ K/2 neighbours outside W and m ≤ K/2 live ones inside; the outside can set n(p) to any value in [m, m + f].
A next state independent of it needs that interval inside B (resp. S) — impossible unless c ≥ b + K/2 — or disjoint
from it — impossible unless b ≥ K/2 + 1 or m ≥ c, i.e. c ≤ K/2. ∎ T6 is the all-dead case. The 2D gump satisfies the
hypothesis; gump itself does not (c = 6 = K/2: a cell with six live neighbours behind it is dead next whatever lies
in front), nor does FCC (4, 6).

## 2. The lattices [computed: `python3 theory.py table`, `python3 indices.py`, `python3 pits.py …`, `python3 armour.py …`]

Tight b = least b with a spanning set of sealed rays; a⁰, a⁻ for a sealed ray; K_f = a⁰ + a⁻ = face-cell degree;
"reach" = caps a face can feel (Cor. F); fw = firewall width; c_arm = least cap with a nonempty armoured core in a
hull of 12 (2D) or 6 (3D) layers. All have b ≤ K/2 except those marked.

| lattice | d | K | b | hull (sealed rays) | a⁰ | a⁻ | K_f | reach b+1…K_f | fw | m* | c_arm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| vn (range-1 cross) | 2 | 4 | 2 | box (4) | 2 | 1 | 3 | 3 | 2 | – | 4 |
| cross2 | 2 | 8 | 3 | box | 4 | 2 | 6 | 4–6 | 3 | – | 7 |
| cross3 | 2 | 12 | 4 | box | 6 | 3 | 9 | 5–9 | 4 | – | 10 |
| cross4 | 2 | 16 | 5 | box | 8 | 4 | 12 | 6–12 | 5 | – | 13 |
| moore | 2 | 8 | 4 | octagon (8) | 2 | 3 | 5 | 5 | 2 rows, 3 diagonals | – | 8 |
| moore_r2 (5×5) | 2 | 24 | 11 | octagon | 4 | 10 | 14 | 12–14 | 5 | – | 22 |
| star2 (cross2 + diagonals) | 2 | 12 | 5 | box | 4 | 4 | 8 | 6–8 | 3 | – | 9 |
| tri6 | 2 | 6 | 3 | hexagon (6) | 2 | 2 | 4 | 4 | 2 | – | 5 |
| tri12 (2 shells) | 2 | 12 | 6 | dodecagon (12) | 2 | 5 | 7 | 7 | 4 | – | 13 |
| tri18 (3 shells) | 2 | 18 | 8 | hexagon | 4 | 7 | 11 | 9–11 | 3 | – | 16 |
| tristar2 / tristar3 (range 2, 3 on the 3 axes) | 2 | 12 / 18 | 5 / 7 | hexagon | 4 / 6 | 4 / 6 | 8 / 12 | 6–8 / 8–12 | 3 / 4 | – | 11 / 15 |
| kagome6 (gump's layer graph) | 2 | 6 | 3 | hexagon | 2 | 2 | 4 | 4 | 3 | – | 6 |
| hex12 (honeycomb, 3 shells) | 2 | 12 | 6 | dodecagon | 2 | 5 | 7 | 7 | 6 | – | 13 |
| hex3, hex9, kagome4, kagome8 | 2 | 3–9 | 2–5 | — | | | | | | | finite sealed sets (b exceeds the generic forward count) |
| **gump** (faces of the cubic honeycomb) | 3 | 12 | 4 | octahedron (8) | 6 | 3 | 9 | 5–9 | 3 | 3 | 8 |
| face18 (same cells, 18 neighbours) | 3 | 18 | 6 | box (6) | 8 | 5 | 13 | 7–13 | 4 | 3 | 13 |
| bond10 (same cells; bonds sharing an endpoint = edges of the honeycomb sharing a vertex) | 3 | 10 | 4 | octahedron | 4 | 3 | 7 | 5–7 | 2 | none (tubes) | 7 |
| face8 (the 8 perpendicular faces) | 3 | 8 | 3 | octahedron | 4 | 2 | 6 | 4–6 | 2 | ≤ 4 (no certificate) | 6 |
| fcc | 3 | 12 | 4 | octahedron | 6 | 3 | 9 | 5–9 | 2 | 2 | 8 |
| bcc8 | 3 | 8 | 3 | rhombic dodecahedron (12) | 4 | 2 | 6 | 4–6 | 2 | 2 | 6 |
| bcc14 | 3 | 14 | 5 | rhombic dodecahedron | 6 | 4 | 10 | 6–10 | 2 | 2 | 11 |
| sc6 (3D von Neumann) | 3 | 6 | 2 | box | 4 | 1 | 5 | 3–5 | 2 | 1 | 5 |
| sc18 (faces + edges) | 3 | 18 | 6 | box | 8 | 5 | 13 | 7–13 | 2 | 2 | 14 |
| sc26 (3D Moore) | 3 | 26 | 10 | {100} + {110}, 18 faces | 8 | 9 | 17 | 11–17 | 3 | ≤ 4 (no certificate) | 22 |
| cross3d2 (3D range-2 cross) | 3 | 12 | 3 | box | 8 | 2 | 10 | 4–10 | 3 | 1 | 9 |

Checks: `python3 validate.py` → ALL OK (my C stepper against numpy on 15 vessels of 11 lattices, the sealed-set
routine against plain peeling, and the face lattice against the golden side-8 log, 23 generations, final 384);
`python3 confine.py` → ALL OK (Theorem A on 11 lattices: no live cell ever outside the polytope in 200 generations; a
birth outside found for the cheapest unsealed ray where one exists); `python3 energy.py selftest` → ALL OK. `python3 independent.py` re-checks the two headline finds with plain numpy rolls
that share no code with the above: vn B2/S12 torus density 0.465 (gstep 0.468), box lifetimes 128 and 512 at sides
9 and 13 as upper bounds from power-of-two snapshots (gstep medians 110 and 293), no cell outside the bounding box;
fcc B45/S345 torus density 0.392 (gstep 0.394).

## 3. Method and the operational definition [measured throughout]

Own stepper `gstep.c` (64 bit-sliced replicas, any cell graph). Three tests per (lattice, cap):

- **BULK** `run.py bulk`: torus (2D 64² periods, 3D 10³), 64 soups at the mean-field density, 4096 generations;
  *chaos* = ≥ 48 soups not yet periodic (period ≤ 2 or equal to a snapshot), activity (x(t) ≠ x(t−2)) ≥ 0.05 and not
  decaying. **Caveat:** one soup density per rule; a rule with a narrow basin can be misread as dead.
- **SLAB** `run.py face` / `scan.py`: slab along the first sealed ray, periodic along the face, 16 layers deep in
  2D, 8 in 3D; a replica is ended and reseeded at a face death (a whole boundary layer empty); it is **censored**
  when it settles or when a dead sealed set appears that is not a whole face (transverse cut, tube) — the largest
  dead sealed set is computed by peeling every 16 generations; replicas still running at the end are censored too.
  τ_face = 2 × exposure / deaths, exposure counted after a 200-generation burn-in. *(My first estimator dropped the
  still-running replicas and biased every point with < 50 deaths low by up to 2 nats; fixed, all tables recomputed.)*
- **HULL** `run.py life`: the confinement polytope, 64 soups, lifetime = settling time, cap 10⁵–2×10⁵.

Cross-check against toy2d (cross2 B34/S234, strips 16 deep): τ_edge = 280 and 1,635 at L = 12, 16 (theirs 286 and
1,679 ± 26); slope 0.437 ± 0.004 for L = 12–20 (theirs 0.425 over the same range). Gump: 0.212 ± 0.001 per face
cell over A = 27–75 (notebook 0.208).

**GUMP** (scoring rule fixed in PREDICTIONS.md) = bulk chaos ∧ face law (ln τ rises ≥ 1 over the sizes, CV of the
wait in [0.8, 1.25]) ∧ hull lifetimes growing ≥ e per size step, runs ending. *strong* = slope ≥ 0.15 per face cell.

## 4. What the training runs already changed (the three lattices the project knew)

`python3 scan.py gump 4 --cs 5,6,7,8,9,10,11,12`, `scan.py cross2 3`, `scan.py moore 4`, `follow.py gump3`,
`follow.py weak`, `run.py life gump 4 C --R 4|5|6`:

1. **Gump is not the only capped threshold on its lattice that does it.** Caps 6, 7, 8 (B45/S345, B456/S3456,
   B4567/S34567) are all chaotic on the torus (ρ = 0.419, 0.482, 0.548) and in periodic {111} slabs they have the
   *same* memoryless face law: ln τ = 5.48, 7.39, 9.92, 12.50, 15.53 ± 0.20 (c = 6) and 5.42, 7.33, 9.88, 12.59,
   15.92 ± 0.23 (c = 7) at A = 27, 36, 48, 60, 75; slopes 0.212 ± 0.001 and 0.215 ± 0.001; c = 8: 5.98, 7.81, 10.34, 13.46, 16.90 ± 0.35,
   slope 0.214 ± 0.001; CV 0.96–1.02. In octahedra they differ: median lifetime at R = 4, 5, 6 layers
   (L1 radius 8, 10, 12): c = 6: 314, 3,682, > 10⁵; **c = 7: 16,896, > 10⁵** (final density 0.22); c = 8: 192,
   1,024, 4,224 ending *frozen* at density 0.70 — Theorem E's armour (c_arm = 8: the 120 hull-edge cells have
   vessel-degree 7). So B456/S3456 is a second, longer-lived gump on the face lattice; gump is the *lowest* cap that
   works, not the only one. (The phase survey's `rules.csv` already had its 10⁵-capped lifetimes.) **[conjecture]**
   c = 7 outlives c = 6 in hulls because a hull-edge cell (degree 7) is overcrowded at c = 7 only when saturated.
2. **Moore B456/S3456 is not simply "eroding".** Its faces are out of the cap's reach (K_f = 5 < 7), below L ≈ 10 a
   row locks fully alive (a conditional wall), and from L = 28 to 320 the row wait is memoryless (CV 0.86–1.04) with
   ln τ = 6.03, 6.86, 7.66, 8.69, 10.23, 11.60 ± 0.08, 13.41 ± 0.24 at L = 28, 40, 56, 80, 120, 160, 240: a weak,
   slightly concave law, 0.02–0.07 per cell (diagonal faces 0.12–0.23 for L = 8–28). Octagon lifetimes grow like R²
   (31, 100, 192, 332, 610 at R = 6…24), so in practice nothing like gump — but for a quantitative reason.
3. cross2: c = 5 is the only chaotic cap (4 dies, 6–9 freeze); its edge law reproduced; boxes 377 … 19,673 for
   sides 11 … 21 (× e^0.39 per unit side).

## 5. The criterion, ingredient by ingredient

**Proved necessary** (for a capped threshold to show confinement, no local permanent death, and faces that die):

- **N1 sealed outside:** b > a⁻(u) on a positively spanning set of directions (Thm A, an iff).
- **N2 unsealable inside:** b ≤ K/2 (one type; Thm C2, an iff). With N1: (K − a⁰)/2 < b ≤ K/2.
- **N3 cap within reach:** c ≤ K_f = K − a⁻ (Thm E + Cor. F): beyond it a fully live face is immortal when
  a⁰ ≥ b − 1. *Dynamically confirmed without exception:* in all 18 families and 38 lattice–cap pairs with c ≥ K_f + 1,
  a⁰ ≥ b − 1 and anything alive after the burn-in, the boundary layer sits at density ≥ 0.99 with activity 0.00 and
  not one face death was recorded (`data/scan_table.md`, verdict WALL). Where a⁰ < b − 1 the out-of-reach faces are
  either the same in practice (Moore c = 8, tri12 c = 11, tri18 c = 16, 17, the 5×5 Moore c = 22) or passive and
  weakly metastable (Moore c = 7, tri18 c = 15, hex12 c = 11: 0.03–0.09 per cell; sc26 c = 18, 19: 0.13, 0.16). In hulls the same happens
  from c_arm on (fcc c = 8, 9; bcc8 c = 6; sc6 c = 5; gump c = 8: runs unfinished or frozen at density 0.6–0.8).
- **N4 two-sided drive** (Thm D): no period ≥ 3 without both undercrowding-after-life and overcrowding-after-life
  events. Measured in 8 chaotic torus states on 8 lattices: O1 = 0.08–0.12 and U1 = 0.05–0.12 per cell per
  generation (O1 = 0.116–0.122 on gump, cross2, cross3, Moore, vn, fcc — nearly universal, not understood); in
  glasses both fall together to 0.002–0.04 (`python3 energy.py LATTICE b c`).

**Measured, and close to sufficient:**

- **S1** Of the 50 (lattice, cap) pairs the BULK rule calls chaotic with the cap within reach (c ≤ K_f), **46 have
  a memoryless face law** (CV 0.83–1.23 wherever ≥ 50 deaths; `data/laws.md`), slopes 0.05–0.45 per face cell. Two
  are glasses at the classifier's edge whose replicas settle before a face dies (tristar2 c = 8, activity 0.059;
  cross3d2 c = 10). The other two are the lowest chaotic cap of cross4 (c = 7) and of bcc14 (c = 7): the face is starved (bcc14: face
  density 0.19–0.32 against 0.37 in the bulk; cross4: no replica survives the burn-in at any L ≤ 128).
- **S2 a starvation index (post hoc).** σ = K_f·ρ/b — the neighbours a face cell would see at bulk density, over the
  birth count — is 0.74 and 0.80 in the two eroding cases; every law with σ ≤ 0.88 is weak (Moore 0.74, bond10
  c = 6 0.77, sc18 c = 9 0.85, face18 c = 9 and sc26 c = 17 0.87, cross3 c = 6 0.88: slopes 0.03–0.12) except vn
  (0.70, slope 0.11–0.18, K = 4); every law with σ ≥ 0.89 has slope ≥ 0.10 (30 of them ≥ 0.15). Within a family the slope rises with the cap: cross3 0.06, 0.27, 0.33, 0.40 (c = 6…9);
  cross4 none, 0.10, 0.21, 0.25, 0.29, 0.27 (c = 7…12).
- **S3 hulls.** Where I ran the polytope (§6) the slab law carries over in 14 pairs (vn c = 3, cross2 c = 5, cross3
  c = 7, 8, gump c = 6, 7, fcc c = 6, 7, bcc8 c = 5, face8 c = 5, sc6 c = 3, sc18 c = 10, bcc14 c = 8, cross3d2
  c = 5). It is not yet visible at the sizes run for the weak laws (cross3 c = 6: 121, 344, 869, 1,676 at sides
  17…41; cross4 c = 9, 10: a box lives about as long as an edge of its own length waits). It fails for bond10
  c = 6 (tubes), and at c = K_f (cross3 c = 9, cross4 c = 12) and from c_arm on the hull *freezes* (final density
  0.33–0.8) instead of peeling. So "within reach" needs a margin at the hull's edges and corners. **[conjecture]**
  the exact condition is that the cap can act on every stratum of the hull boundary.

**Not predicted by anything I have — the chaos window.** Which caps are chaotic on the torus:
cross2 {5}; cross3 {6…11}; cross4 {7…14}; vn {3, 4}; Moore {7}; star2 {9, 10, 11}; tristar3 {13…17}; tri18 {15, 16,
17}; tri12 {11}; hex12 {11}; kagome6 {6}; moore_r2 {22}; tristar2, tri6: none (glass at best); gump {6, 7, 8}; fcc
{6…11}; bcc8 {5, 6, 7}; bcc14 {7…12}; sc6 {3, 4, 5}; sc18 {9…15}; face18 {9…15}; sc26 {17, 18, 19}; cross3d2
{4…10}; bond10 {6…9}; face8 {5} (upper ends are where the scan stopped for sc18, face18, sc26). The single-site mean field is useless here: its "unstable fixed point with
enough undercrowding" rule called 42 pairs chaotic and 25 were; of the 121 it called dead or frozen, 50 are
chaotic (the high caps of every cross and of fcc, bcc, sc among them); and vn c = 3, sc6 c = 3, cross3d2 c = 4 are chaotic although their mean-field
fixed point is *stable* (slope −0.25, −0.70, −0.83). **Mean-field instability is neither necessary nor sufficient.**
One regularity survives: a chaotic cap exists *within reach of the faces* in all 12 families with b/K ≤ 3/8 and in
only 3 of the 17 with b/K > 3/8 (vn, bond10, and sc26 barely, at c = K_f) — 26 of 29.

**The brief's candidate ingredients, judged:**

| ingredient | verdict |
|---|---|
| fraction of the neighbourhood in a confining hyperplane | **Matters, in two exact ways and one empirical.** a⁰ − 1 is the number of caps the faces can feel (Cor. F); a⁰ ≥ b − 1 is what turns an out-of-reach cap into a wall; and with tight b, b/K ≤ 3/8 ⇔ a⁰ ≥ K/4 + 2, which for K = 4, 8, 12 means *half* the neighbourhood (2, 4, 6). It is not the fraction as such: sc18 (0.44), cross3d2 (0.67), bond10 (0.40) also work. |
| birth threshold near a third | b ≤ K/2 is necessary (proved). b/K ≲ 3/8 is the best single predictor of a chaotic in-reach cap existing (26/29), but vn has b/K = ½. |
| the cap | Necessary (without it: threshold lemma, period ≤ 2). Must lie in [b + 1, K_f], below c_arm; then every chaotic cap gives a face law. More than one cap usually works (gump 6–7, cross3 7–8, fcc 6–7, …). |
| mean-field instability of the fixed points | Irrelevant as a criterion (see above). What is true instead is the two-sided lemma. |
| critical thickness | A property of each gump (m* = 1, 2 or 3 by the half-space-depth certificate), not a condition for being one. bond10 shows it can fail to exist: tubes pierce any slab, and bond10 c = 6 is the one chaotic, in-reach rule whose hulls die in linear time (24, 46, 74, 124 at R = 4…7). |

**Class statement [conjecture, with the proved parts marked].** *A capped threshold (b, c) on a cell lattice shows
the gump phenomenon iff (i) [proved iff] a positively spanning set of directions is sealed, b > a⁻; (ii) [proved iff,
one type] no finite set is sealed, b ≤ K/2 — and no finite tube is sealed in a slab; (iii) [proved necessary] the cap
is within reach of the faces and of the hull's lower strata, b + 1 ≤ c ≤ K − a⁻ and c < c_arm; (iv) the bulk is
chaotic at that cap (necessarily driven on both sides); (v) the face is not starved (σ = K_f ρ/b ≳ 0.85). Then every
face dies after a memoryless wait exponential in its size.* The boundary layer is then a contact-type process with
the empty layer as its only absorbing state (exact, by (i)), fed by the bulk; (v) says it is supercritical.

## 6. Predictions and outcomes

Full text, with what I had seen at each stage: `PREDICTIONS.md`. Data: `data/scan_table.md` (every cap of 27
families), `data/laws.md` (every face law), `data/hulls.txt` (every hull run).

**New gumps (bulk chaos + memoryless face law + hull lifetimes growing, sparse debris):**

| lattice, rule | slab law: ln τ at face sizes | slope / face cell | hull medians (64 soups) | predicted? |
|---|---|---|---|---|
| **vn B2/S12** (2D, 4 neighbours) | 5.62, 7.08, 8.23, 9.26, 10.67, 12.53, 14.49 ± 0.24 at L = 12…80 | 0.18 → 0.11 | boxes of side 9…33: 110, 293, 640, 1,443, 2,752, 5,376, 8,763; final density 0.03 | **no — called "dies or freezes"** |
| cross3 B456/S3456 (2D) | 5.96, 8.23, 11.31 at L = 20, 28, 40 | 0.27 | sides 13…25: 109, 364, 978, 3,081 | yes (stage 1) |
| cross3 B4567/S34567 | 6.60, 9.28, 13.27 | 0.33 | sides 11…19: 96, 212, 331, 900, 1,403 | marginal call, yes |
| **fcc B45/S345** | 4.61, 6.85, 9.25, 11.97, 14.68 ± 0.24 at A = 25…81 | 0.19 (predicted 0.21 ± 0.07) | octahedra R = 3…7: 162, 832, 9,847, > 10⁵, > 10⁵; final density 0.01–0.04 | **yes** |
| fcc B456/S3456 | 4.08, 9.35, 15.26 ± 0.30 | 0.22 | 4,617, > 10⁵ (60/64 unfinished at R = 4) | yes |
| **bcc8 B34/S234** | 8.27, 10.80, 16.45 ± 0.16 at A = 25, 36, 49 | 0.24–0.43 (uneven) | rhombic dodecahedra R = 3…5: 916, 17,600, > 10⁵ | **yes** |
| **sc6 B2/S12** (3D von Neumann) | 9.20, 11.91, 17.75 ± 0.27 | 0.25–0.45 (uneven) | boxes R = 2, 3: 2,752, > 10⁵ | **no** |
| sc18 B6789/S56789 | 5.87, 10.03 at A = 49, 81 | 0.13 | 355, 10,107, > 10⁵ | yes |
| bcc14 B567/S4567 | 4.11, 8.32, 13.73 | 0.17 | 57, 164, 627 | yes |
| cross3d2 B34/S234 | 3.61, 7.73, 13.04 | 0.17 | 87,889 (24/64 unfinished), > 10⁵ | yes |
| face8 B34/S234 (face lattice, 8 perpendicular neighbours) | 9.97, 16.99 ± 0.35 at A = 27, 48 | ≈ 0.33 (two sizes) | octahedra R = 4, 5, 6: 1,516, 15,716, > 10⁵ | yes |

Slab laws without a hull test, or with an inconclusive one (so not claimed as gumps): cross4 c = 8–12; fcc c = 8, 9
(hull armoured: frozen); bcc8 c = 6 (armoured); bcc14 c = 9, 10; sc6 c = 4 (R = 2 hull ends dense, 0.64), c = 5
(hull freezes in 33–320 generations); sc18 c = 9, 11, 12, 13; face18 c = 9–13; sc26 c = 17; cross3d2 c = 4, 6–9;
bond10 c = 7 (1,152, 45,120, > 10⁵, final density 0.27–0.33).

**Scorecard.**

| what was predicted | hits | misses | notes |
|---|---|---|---|
| Stage 1 "GUMP" calls (28 lattice–cap pairs) | 8 (cross3 c = 7; fcc c = 6, 7; bcc8 c = 5; bcc14 c = 8; sc18 c = 10; cross3d2 c = 5; face8 c = 5) | 14 | 6 more have the slab law but no conclusive hull test. Misses: bulk not chaotic at the cap I named (star2, tristar2, tristar3 ×2, tri18, sc18 c = 8, face18 c = 8, sc26 ×3), starved faces (cross4 c = 7, bcc14 c = 7), weak (cross3 c = 6), tubes (bond10 c = 6). |
| Stage 1 marginal calls (4) | 3 | 0 | cross4 c = 9: slab law only |
| Stage 1 explicit "not a gump" (15 pairs: walls, passive faces, sealed holes) | 14 | 1 (bond10 c = 7 behaves like one) | walls on vn c = 4, tri6, kagome6 as called; Moore weak; hex9 dead |
| Stage 1 blanket "every other cap is not" | — | **2 gumps missed (vn c = 3, sc6 c = 3)** and ≥ 12 further slab laws at caps the mean field called frozen | the mean-field window is the failed part |
| fcc slope 0.21 ± 0.07 | 1 (0.19) | | |
| Q1 cap-independent slope | fcc (0.19, 0.22, 0.18) | cross3 (0.06–0.40), sc18 | holds on plateaus in 3D (also gump, cross3d2 0.15–0.19 over six caps, sc18 0.13 over three), fails in 2D |
| Q2 ordering in 2D | Moore lowest | cross3 c = 6 is far weaker than cross2 | |
| Q3 hull armour from c_arm (5 new pairs) | 4 (fcc c = 8, 9; bcc8 c = 6; sc6 c = 5) | bond10 c = 7 (ends at density 0.27–0.33, but lifetimes grow) | |
| Q4 both drives in every chaotic state | 9 of 9 | the "one drive < 0.002 in glass" half: glasses keep both at 0.01–0.04 | |
| Stage 2 (R₁ index), informative calls (19) | 13 | 5 (sc18 and face18 c = 9, 10; sc26 c = 17), 1 half | called the bcc14 c = 7 erosion; useless across lattices in 3D |
| Stage 3 (bond10 c = 6 not a gump) | hull lifetimes linear; tube endings overtake face deaths (0.13, 0.28, 1.04 per face death at A = 27, 48, 75) | the slab wait still grows, 0.062 per cell | |
| Stage 4 (R₁ inside cross3/cross4, 7 slopes + monotonicity) | 3 (cross3 c = 8; cross4 c = 7 none; monotone in both) | 5, all underestimates | |
| Stage 5 (chaos at a low cap iff b/K ≤ 0.38, nine 3D families) | 8 | 1 (bond10 is chaotic at c = 6) | |
| The brief's ingredients on the eight discriminating rows | 7 | 1 (bond10 c = 7) | better than my stage 1 there; "one cap per neighbourhood" wrong on gump, cross3, fcc |

Honest reading: the proved parts of the criterion (sealing, reach, walls, armour) never failed and explain every
"not a gump" above the reach; the part that was supposed to pick the cap (mean field) performed at chance, and it
is where the two unpredicted gumps came from. Three gumps predicted from the criterion before any dynamics on those
lattices passed all three tests on first try (fcc B45/S345 with its slope, bcc8 B34/S234, cross3 B456/S3456, face8 B34/S234),
and four more with thinner hull evidence.

## 7. Why the Moore neighbourhood fails, and why the known gumps are or are not unique

- **Moore.** A line holds a⁰ = 2 of its 8 neighbours, so b = K/2 = 4 and (Cor. F) exactly **one** cap is within
  reach of a face: c = 5, the rule B4/S34. It dies [measured]. The only chaotic Moore cap is c = 7, where a face
  cell (5 neighbours) can never be overcrowded: its rows are conditional walls when short and weakly metastable when
  long (§4.2). The same holds for every a⁰ = 2 lattice: one candidate each — triangular B3/S23 (freezes), kagome6
  B3/S23 (freezes), honeycomb B2/S12 (glass), tri12/hex12 B6/S56 (dies) — **except von Neumann, whose one candidate
  B2/S12 is chaotic, and it is a gump** (§6). So Moore fails for a structural reason (one candidate) plus a
  contingent one (that candidate's bulk is dead); toy2d's "a line holds too few of its neighbours" is the first half.
- **cross2** has three caps in reach, 4, 5, 6: 4 dies, 6 freezes, 5 is the gump — unique [measured], as claimed.
- **gump's lattice** has five, 5…9: 5 dies, 9 is glass, 8 is armoured in octahedra, **6 and 7 are both gumps** (§4.1).
  The uniqueness claimed in the brief is false there; minimality is true.

## 8. Surprises

1. The smallest gump has four neighbours: **B2/S12 on the von Neumann neighbourhood** — alive next iff n + x ≥ 2,
   unless n ≥ 3. Bounding-box confinement (2 > 1), no finite sealed set (2 ≤ 2), firewall of 2 rows, density 0.468,
   edge law memoryless over four decades of τ. My criterion said it could not be chaotic; toy2d's table had its
   numbers (half the neighbourhood on a line, threshold fraction 0.38) and nobody ran it. Its 3D sibling on the six
   face-neighbours of the cubic lattice, also B2/S12, is a gump too.
2. Three dimensions is full of them: FCC, BCC, simple cubic (6 and 18), the 3D cross, the face lattice with 8 or
   18 neighbours. Two dimensions has only the crosses (range 1, 2, 3; range 4 in slabs only).
3. The wall cap is exact: in every family the boundary goes from dying to immortal between c = K_f and c = K_f + 1.
4. In 3D the face law barely notices the cap (gump: 0.212 and 0.215 for c = 6, 7, with ln τ equal to ± 0.1 at five
   sizes although the densities are 0.42 and 0.48); in 2D it depends on it strongly. I have no explanation.
5. A hole cut into a living cross2 edge closes at 0.94 cells per generation per end with diffusivity 0.84, so "one
   hole growing against the healing drift" would cost v/D = 1.1 per cell; the measured exponent is 0.42–0.44
   (`python3 gap.py cross2 3 5 128 16 80 12 0.5`). A face does not die that way — consistent with the notebook's
   "a dying face is a starved face".
6. bond10: no finite sealed set in the lattice, yet finite sealed tubes through every slab — C2 has no converse for
   slabs — and it is the one chaotic in-reach rule that is not a gump.

## 9. Not checked / known weaknesses

- **Bulk classes rest on one soup density and 4096 generations.** "Dies"/"freezes" may hide a narrow chaotic basin
  (seen once: tristar3 c = 13 dies from ρ₀ = 0.50 but is chaotic from 0.65). The chaos windows of §5 are lower bounds.
- Slab laws use small periodic faces (A ≤ 81 cells in 3D; 2–5 sizes; two sizes only for cross4 c = 9–11, sc18,
  sc26, face18 c = 10–13, bcc8 c = 6, sc6 c = 4, 5), one face orientation per lattice (both for Moore), slabs 8
  layers deep in 3D. bcc8 and sc6 are uneven between odd and even widths (ln τ/A = 0.33, 0.30, 0.34 and
  0.37, 0.33, 0.36; sc6 c = 4 is *longer*-lived at A = 36 than at 49) — not understood, and it is why I give ranges.
- Hull tests are 64 soups at 3–7 sizes with a cap of 10⁵–2×10⁵; several "gumps" rest on two finished sizes
  (sc6 c = 3 on one). No hull test for cross4 beyond side 25, sc18 c ≠ 10, face18, sc26.
- The weak laws (cross3 c = 6: 0.05 per cell to L = 160; Moore rows; hex12 c = 11: 0.03–0.04 to L = 96) are slightly
  concave; I cannot exclude a crossover to a sub-exponential law at larger sizes.
- Symmetric seeds, the straight tail to n = 1, the rate function: not touched for any new gump.
- Theorems C2–C4, 1.7 and 1.8 are stated for one cell type; the face lattice has three (handled by computing the
  certificate per type); honeycomb and kagome families only through C1 and peeling.
- The validation run printed 60-generation populations of four test pairs before the predictions were committed
  (disclosed in PREDICTIONS.md).
- I did not read Eppstein's proof or any primary source; no web access was used.

## 10. Open

1. **The chaos window** — why cross-r, FCC, BCC, SC are chaotic from c = b + 2 (or b + 1) up to and past K_f while
   star2, the triangular families and the 5×5 Moore are chaotic only above K_f. Theorem D says what must be present;
   nothing says when it is. The b/K ≤ 3/8 rule (23/27) wants a reason; vn is the instructive exception.
2. **The slope.** What fixes I, why it is cap-independent on 3D plateaus, and whether σ = K_f ρ/b ≈ 0.8 is a real
   threshold (a directed-percolation point for the face) or an accident of 50 cases.
3. **Hull strata.** A proof or measurement of "the cap must reach the edges and corners": gump c = 7 and fcc c = 7
   live 30–50× longer than c = 6 in octahedra with the same slab law; cross3 c = 9 and cross4 c = 12 freeze in boxes.
4. Is O1 ≈ 0.12 per cell per generation in every chaotic capped threshold a theorem?
5. The 2D gumps are now a family (range-r crosses, r = 1, 2, 3): the cleanest place to try M2–M4 is the range-1
   member, B2/S12, with four neighbours.

## Reproduce

```sh
cd research/theory/class
cc -O3 -march=native -o ../../scratch/class/gstep gstep.c -lm; cp ../../scratch/class/gstep ../../scratch/class/gstep_gap
python3 lattices.py; python3 validate.py; python3 confine.py; python3 energy.py selftest      # all "ALL OK"
python3 independent.py                                                                        # numpy-only re-check of vn and fcc
python3 theory.py table; python3 indices.py > data/indices.txt                                # §2 (no dynamics)
python3 pits.py bond10 4 4; python3 pits.py gump 4 2; python3 pits.py gump 4 3; python3 armour.py gump 4 6
python3 scan.py gump 4 --cs 5,6,7,8,9,10,11,12; python3 scan.py cross2 3; python3 scan.py moore 4   # training
./run2d.sh; ./run3d.sh                                    # test set (≈ 45 + 45 min on one core) -> scan2d.log, scan3d.log
python3 follow.py stage4; python3 follow.py weak; python3 follow.py gump3; python3 follow.py hulls2d; python3 follow.py vn
python3 follow.py hulls3d fcc:4:6:3,4,5,6,7:0.42 bcc8:3:5:3,4,5,6:0.5 sc6:2:3:2,3,4,5:0.4      # (lattice:b:c:sizes:soup density)
python3 follow.py more3d; python3 gap.py cross2 3 5 128 16 80 12 0.5
python3 summarize.py scan > data/scan_table.md; python3 summarize.py laws > data/laws.md; python3 summarize.py faces > data/faces.tsv
```
Single runs: `python3 run.py bulk|face|life LATTICE b c [--n N --m M --R R --sec S --p P]`.

