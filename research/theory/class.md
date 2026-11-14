# G3 / S7 — what is the class of "gumps"?

> **Revised 2026-11-14** after the adversarial review `research/audit/REVIEW-class.md` (cited below as R§; its
> scripts are in `research/audit/class/`, run from there). Every change is listed, with the review section that
> required it, in the last section, "Changes in the revision of 2026-11-14".
>
> **Revised a second time 2026-11-14 after `research/theory/class/followup/OUTCOMES.md`** (cited below as F§; the
> follow-up's forecasts, committed before its runs, are `followup/PREDICTIONS.md`, commit 59e0683; its commands run
> from `research/theory/class/followup/`). Its results have one author and are tagged **[measured; one author]**,
> except the face12e symmetric-box lifetimes, which the lead re-derived with separate code
> (`research/audit/class/lead_check_box.py`). Every change is listed in the last section, "Changes in the second
> revision of 2026-11-14".

*Class agent, 2026-11-13; revised 2026-11-14. Tags: **[proved]** (argument given here), **[computed]** (exact finite
computation, command given), **[measured]** (n, error, command), **[conjecture]**, and **[not independently
checked]** for a claim of the original that the review lists as not repeated (R, "Not checked"); untagged numbers
that the review re-measured carry an R§ reference. Scripts, predictions and data: `research/theory/class/` (run
commands from there). Bulk output: `research/scratch/class/`. Predictions were committed before testing
(`class/PREDICTIONS.md`: commit 5636f1c, then four dated appendices, each committed before the runs it concerns;
in git order this holds, R§3.4); the scorecard is §6.*

*Names. **gump** is, everywhere in this repository, the rule as coded in 2012 (the four coplanar neighbours touch at
a corner). **face12e** is the same cells with the four coplanar neighbours that share an edge — the neighbourhood the
repository's owner intended in 2012. face12e is not gump.*

## Summary

**The class** (the statement the review signs, R§5.1, with the original material that survives). For a capped
threshold (b, c) — alive next iff n + x ≥ b, except n ≥ c dies — on a cell lattice with any number of cell types.
For a half-space H = {u·p ≤ C} write c(H) for the most neighbours inside H that a cell outside H has; for a
direction u, a⁻ (a⁰) for the most neighbours a cell has strictly behind (in) the plane.

1. **Confinement [proved]** (Theorem A). If the half-spaces with c(H) ≤ b − 1 have positively spanning normals,
   every finite pattern stays in the intersection of the sealed half-spaces containing it, that hull never grows,
   and the pattern is eventually periodic. With one cell type c(H) depends on the direction only and this reads
   b > a⁻ on a positively spanning set of directions; the hull is then the polytope of the sealed rays. This is a
   sufficient condition. *Not proved:* the converse for patterns (that without such a family something escapes).
   Out of sample [measured; one author, F§1]: kagome8 and hex9 at their position-aware b = 4, caps 5–8, 0 escapes
   from the predicted hull in 1,536 soups × 300 generations, where the direction-only version of this clause (b = 5)
   predicted no confinement at b = 4; the same soups leave the position-free polygon (64 … 36,987 soup-generations).
2. **No local permanent death [proved]** (Theorem C). If some generic v gives every cell type at least b forward
   offsets, no finite set of cells is sealed. With one type this is b ≤ K/2 and is an iff (C2); on gump's lattice it
   is an iff too [computed at b = 7, R§1.4]. Together with 1, for one type: (K − a⁰)/2 < b ≤ K/2. In a wall band or a
   thin slab the same count must hold for the cells of every layer (C4) [three layers for gump (T6), one cube for
   face12e (R§2.2), the m* column of §2 for the rest, not independently checked].
3. **Armour [proved, conditional; measured]** (Theorem E). A set whose cells have ≥ b − 1 neighbours inside it and
   vessel-degree ≤ c − 1 is immortal once entirely alive. That it then forms from soups is measured: where such a set
   exists and a⁰ ≥ b − 1, no wall ever died — all 38 scanned pairs (recounted, R§3.3), fcc c = 10 and face12e c = 9
   (R§3.2, zero deaths). The supportable form of the clause is *no armoured set forms*; for one type, tight b and
   a⁰ ≥ b − 1 it reads c ≤ K_f = K − a⁻ in a slab, which leaves exactly a⁰ − 1 caps, b + 1 ≤ c ≤ K_f, that a face
   can feel (Cor. F, [proved]). The printed form "b + 1 ≤ c ≤ K_f and c < c_arm" goes beyond the data: sc26 c = 18, 19
   (beyond K_f, a⁰ < b − 1) have memoryless slab laws, and bond10 c = 7 = c_arm has growing hull lifetimes (R§1.3).
   *Observed cases outside the clause* [measured; one author]: (a) **walls that freeze without armour** — kagome4
   B2/S12 has an empty Theorem-E core (c ≤ 4), yet its wall rows lock into static patterns of density 2/3 that spread
   inward, at 27–44 % of the wall-death rate over n = 6 … 18; frozen walls did not die on the time scales run
   (F§2; "Where … wrong or silent" 2). (b) **chaos peeling beneath an immortal armoured band** — hex9 c = 8: the
   armoured outer pair of layers sits at density 1.000 and never dies, but in strips the pair beneath it dies
   memorylessly (ln τ = 6.94 → 12.08 for n = 10 → 16); in hulls no permanent dead set appeared in 2 × 10⁶ generations
   (F§1, item 3). The clause says neither that armour-free walls can freeze nor what happens under an armoured band.
4. **Two-sided drive [proved]** (Theorem D). In a finite vessel an orbit of period ≥ 3 has overcrowded-after-life
   and undercrowded-after-life events for ever; a capped threshold is a ferromagnetic and an antiferromagnetic
   symmetric threshold network at once, and either pure threshold rule alone reaches period ≤ 2. Whether a given cap
   is chaotic is **not predicted**.
5. **Whole-wall death [measured].** With 1–3 in force, no armour, and a torus state that is chaotic at that cap,
   the wall band dies as a whole after a wait that is memoryless and roughly exponential in the wall's area (ln τ
   rising roughly linearly; the rate per cell can drift). Re-measured with independent code (R§3.1, §2.2, §2.4): gump
   caps 6 and 7 (0.212 and 0.216 per cell, five sizes), fcc cap 6 (0.181, five sizes), face12e caps 6, 7, 8 (0.41 per
   wall face; five sizes at cap 6), and more roughly bond10 B345/S2345 in slabs. Out of sample [measured; one author,
   F§1–§3]: **hex9 B456/S3456** (memoryless at seven lengths, CV 0.97–1.02, but concave: the rate per wall cell falls
   from 0.69 to 0.53 over n = 8 … 20, a straight line rejected); **kagome4 B2/S12** 0.772 ± 0.003 per wall-row cell,
   straight over n = 6 … 18, once frozen walls are censored (clause 3 (a)); **bond10 B34/S234** in slabs 0.492 ± 0.001
   per wall face, six sizes. In the original data: 42 of 50 pairs by the rule fixed in advance, 46 by the original
   count (R§3.3).
6. **Lifetime in the hull [measured].** Hull lifetimes grow and end in sparse debris wherever a hull was run to
   completion at three or more sizes; *whether they grow as the slab wall law dictates depends on the vessel*. They
   do, within the precision of the tests, for: gump cap 6 octahedra and fcc cap 6 (original runs, re-run at two and
   three sizes, R§3.1) — for gump only approximately: an octahedral face is about 0.8–0.9 nats tougher than a
   rim-free slab face at A = 108 (0.91 ± 0.06, 0.88 after the firewall correction; `research/gpu/README.md`,
   `research/audit/REVIEW-gpu-pr12.md`); face12e cap 6 boxes to 7³ (R§2.2: 10, 60, 439, 9,855, 707,038 for 2³ … 6³;
   7³ median ≈ 1.6 × 10⁸, estimated from 16 of 128 finished by 3 × 10⁷, [measured; one author], F§4; box lifetimes
   0.34–0.37 of τ_wall against 1/6 for six independent walls, so here too the walls are somewhat tougher in a box);
   vn B2/S12 (0.11 per unit of side up to side 81, R§3.3). They **do not** for bond10 B34/S234 at b = 3
   [measured; one author, F§3]: boxes of 4³ live about 10⁹ generations (4 of 64 died by 10⁸) against 600–1,500
   forecast from the slab law; columns (two pairs of walls) are 24–196× tougher per wall than slabs of the same area.
   There the layer beneath a wall's sheet contains the neighbouring walls' edge rows, which stay dense (0.67–0.71
   against 0.50 for sheet cells away from edges), so a wall cannot die while its neighbours live. A box is therefore
   not a set of independent slab walls: an **edge term** is needed, small for gump and face12e, enormous for bond10,
   and it is not yet understood (counting the column excess per edge still leaves bond10's 4³ box 10–100× short:
   corners or several edges at once cost more). hex9 B456/S3456 hulls grow (24 → 4,102 for R = 2 … 7, debris
   0.29 → 0.04) but on unequal sides, not a rate test (F§1).
7. **[conjecture]** Under 1–3 and a chaotic bulk the wall band is a metastable process whose only absorbing state is
   the empty band, with a wait exponential in its area. Nothing is conjectured, because nothing is known, about which
   caps are chaotic or about how strong the law is. The original fifth clause, "face not starved, K_f·ρ/b ≳ 0.85",
   is withdrawn as a criterion: it is a post-hoc line between two eroding cases and the weak laws above them, and on
   face12e it gives either verdict depending on which layer's degree is called K_f (§5 S2, R§4).

This is a list of proved structure with a measured regularity on top. It is not an "iff", and "gump" has no sharp
edge on the weak side: vn B2/S12 (0.12 per cell), cross3 B45/S345 (0.05) and Moore B456/S3456 rows (0.02–0.07)
differ in a rate (R§5.1).

Evidence [measured]: of 50 lattice–cap pairs with a chaotic bulk and the cap within reach, 42 have a memoryless face
law by the scoring rule fixed in PREDICTIONS.md; four more (face8 c = 5, bcc8 c = 6, sc6 c = 4, 5) have 1–15
deaths at their second size, which the original counted as laws (R§3.3). All 38 pairs beyond reach with a⁰ ≥ b − 1
that have anything alive after the burn-in are walls, no exception (recounted; only 25 of the 38 have a chaotic
bulk, R§3.3).

**New gumps**, each with chaotic torus, memoryless face law and hull lifetimes growing to sparse debris:
**B2/S12 on the von Neumann neighbourhood** (4 neighbours; not predicted; box lifetimes re-run to side 81, R§3.3),
B456/S3456 and B4567/S34567 on the range-3 cross, **B45/S345 on FCC** (slope 0.181 ± 0.001 per face cell
re-measured, R§3.1; predicted 0.21 ± 0.07), **B34/S234 on BCC**, B34/S234 on the face lattice with its 8
perpendicular neighbours (on 8 slab deaths at its second size, R§3.3), B2/S12 on the 6-neighbour cubic lattice (not
predicted; one finished hull size), B6789/S56789 on the 18-neighbour cubic lattice, and — thinner hull evidence —
B567/S4567 on BCC-14, B34/S234 on the 3D range-2 cross (one finished hull size). Found by the review (R§2):
**face12e B45/S345**, which has the whole phenomenon in a box — it is the neighbourhood the repository's owner
intended in 2012 (coplanar neighbours sharing an edge); gump, everywhere in this repository, is the rule as coded
(coplanar neighbours touching at a corner); face12e is not gump. Torus ρ = 0.398; walls die two sheets at a time
after a memoryless wait, ln τ = 6.43 → 14.54 for 16 → 36 wall faces (0.410 ± 0.001 per wall face, 0.205 per cell of
the layer that dies); box lifetimes 10, 60, 439, 9,855, 707,038 for 2³ … 6³ cubes, ending in sparse debris
(R§2.2; the wall law confirmed by the lead's own code, NOTEBOOK 2026-11-14); 7³ ≈ 1.6 × 10⁸ (estimated) and, from
soups with full cubic symmetry, median lifetimes of only 3 … 103.5 generations at 4³ … 12³ (§6). Found by the follow-up
[measured; one author, F§1]: **hex9 B456/S3456** (honeycomb with 9 neighbours, b = 4, c = 7): confined, chaotic torus
(ρ = 0.537), memoryless whole-wall death at seven lengths with a concave law, hull lifetimes growing to sparse debris.
Candidates: kagome4 B2/S12 (the plain kagome lattice at b = 2), now on a clean strip law at seven lengths (F§2) but
with walls that also freeze; bond10 at its tight b = 3 (B34/S234: clean slab law; its boxes grow enormously,
262 → ~10⁹ from 3³ to 4³, but not as its slab law dictates, clause 6; B345/S2345: slab law only, R§2.4).

**Two statements in the brief do not survive.** (a) Gump is not the only capped threshold on its lattice:
B456/S3456 has a slab face law equal to gump's within 0.2 in ln τ at five sizes (slopes 0.2121 ± 0.0004 and
0.2156 ± 0.0005, differing by 1.6 ± 0.3 %; the laws cross, R§3.1) and lives ≥ 50× longer in octahedra (72× at R = 4
in the review's runs); B4567/S34567 has a slab law too but freezes in octahedra (armour). (b) "The Moore
neighbourhood has no such rule" is right, but for a sharper reason than a count: with a⁰ = 2 exactly one cap is
within reach of a face (B4/S34), and its bulk is dead; von Neumann has the same structure and its one candidate,
B2/S12, works. [not independently checked: the Moore scans]

**Scorecard** (§6): proved parts never failed. Of 28 "GUMP" calls committed before testing, 8 passed all three
tests by the original's judgment; mechanically, by the scoring rule fixed in advance, 4 pass, 6 if a step into an
unfinished size counts (R§3.3). 6 more have the face law but no conclusive hull test, 14 failed (10 because the
mean-field guess of the chaotic cap was wrong); 14 of 15 explicit "not a gump" calls held (five because the torus
dies at the named cap, so the stated reason was not tested, R§3.3); two gumps were missed outright (vn c = 3,
confirmed by the review's box re-run; sc6 c = 3, on one finished hull size). The hull test's wording has changed
(§3): "× ≥ e per size step" depended on the step and by its letter failed cross2 and vn; it is now a rate per unit
of side compared with the slab slope. The mean field picks chaotic caps at chance level and should be dropped.
Out of sample (F, scorecard; [measured; one author]): of 12 follow-up forecasts committed before the runs, 9 held
(confinement on kagome8 and hex9; hex9 c = 7 whole-wall memoryless death, "linear" only approximately; armour at
hex9 c = 8; hex9 hulls; kagome4's slope, though its stated cause was wrong; no pits; bond10 c = 6 frozen boxes;
face12e 7³ count; face12e symmetric boxes), one was supported in part (of three hypotheses for bond10's boxes,
"a wall cannot die while its neighbours live" held, the other two were refuted), one was a guess (chaotic cap), and
one failed as its author expected:
bond10's box lifetimes from its slab law (× 10⁶ short), which is what makes clause 6 wrong as first written.

## 1. The abstract setting, and what can be proved in it

### 1.1 Setting

A **cell lattice** is a discrete set V ⊂ R^d, invariant under a full-rank lattice Λ of translations with finitely
many orbits (*cell types*), together with a finite set of offsets O(p) ⊂ R^d ∖ {0} for each cell p, depending only on
its type, such that N(p) = p + O(p) ⊂ V and the relation is symmetric: q ∈ N(p) ⇔ p ∈ N(q). K(p) = |O(p)|.
*One type* means V is a single Λ-orbit; then O = −O and K is even. (`lattices.py` holds 29 of them — square, triangular,
honeycomb and kagome families, the face lattice of the cubic honeycomb with four neighbourhoods, FCC, BCC, simple
cubic with 6, 18, 26, the 3D cross — each checked for symmetry. face12e, the review's, is in `research/audit/class/aud.py`.)

A **rule** is outer-totalistic (B, S); b = min B ≥ 1. The **capped threshold** (b, c) is B = {b, …, c−1},
S = {b−1, …, c−1}: *alive next iff n + x ≥ b, except that n ≥ c dies*. Gump is (4, 6) on the face lattice; the 2D
gump is (3, 5) on the range-2 cross; Conway's Life is (3, 4) on Moore (not confined: b = 3 < 4).

A **vessel** is a subset V′ ⊆ V whose outside is dead forever. For a linear functional u (a *direction*) write

  a⁻_u(p) = #{o ∈ O(p) : u·o < 0},  a⁰_u(p) = #{u·o = 0},  a⁺_u(p) = #{u·o > 0},  c(u) = max_p a⁻_u(p).

When u(V) is discrete, the level sets of u are *layers* and (a_k) = number of offsets at layer offset k is the layer
histogram (T1). For one type, a⁻ = a⁺ = (K − a⁰)/2.

### 1.2 Theorem A — confinement by sealed half-spaces [proved]

*(The review's Theorem A′, R§1.2, with its proof. The original stated Theorem A for directions; that version follows
it below, is exact for one cell type, and is an upper bound in general.)*

For a half-space H = {p : u·p ≤ C} let c(H) = max over cells p ∉ H of |N(p) ∩ H|.

**(i)** If c(H) ≤ b − 1, the outside of H, once dead, stays dead (any rule with minimum birth count ≥ b).
**(ii)** If c(H) ≥ b, some configuration inside H has a birth outside H. So **H is sealed iff c(H) ≤ b − 1**.
**(iii)** c(H) ≤ c(u) = max over types of a⁻_u, with equality whenever a cell of a type attaining the maximum lies on
the first layer beyond the plane. With one cell type that is every C, so c(H) = c(u) and the direction version below
is exact.
**(iv)** With several types and u rational, a type that is absent from the first layers beyond the plane contributes
only its offsets that reach back far enough: c(H) = max over types τ of #{o ∈ O_τ : u·o ≤ −d_τ}, d_τ the distance
from the plane to the first layer holding τ. This can be smaller than c(u).
**(v) Hull.** A finite pattern stays in the intersection of all sealed half-spaces that contain it, and that set never
grows. It is bounded for every finite pattern iff the normals of the sealed half-spaces positively span; then every
finite pattern is eventually periodic.

*Proof.* (i) A dead cell p ∉ H has at most |N(p) ∩ H| ≤ b − 1 live neighbours, all others being dead. (ii) Take p ∉ H
with |N(p) ∩ H| ≥ b and make exactly b of those neighbours alive: p has n = b ∈ B. (iii) A neighbour of p in H has
u·o < 0, so |N(p) ∩ H| ≤ a⁻_u(p); if p is on the first layer beyond the plane every neighbour with u·o < 0 is in H.
One type means every layer holds a translate of every cell. (iv) is (iii) read type by type; the first layer of a
type is its worst. (v) Apply (i) to each sealed H containing the pattern; the new maxima are no larger. Sealed
positions of a rational direction repeat periodically, so they exist arbitrarily far out. ∎

**Directions (the original Theorem A; for one type it is Theorem A).** **(i′)** If c(u) ≤ b − 1, then for every C the
set {p : u·p > C}, once dead, is dead forever. **(ii′)** If c(u) ≥ b this fails for *some* C: there is a
configuration inside {u·p ≤ C} whose successor has a live cell outside. So *u is sealed at every position iff
c(u) ≤ b − 1*; c(u) is the maximum of c(H) over C (R§1.2).
**(iii′)** If u′ is a specialisation of u (sign(u′·o) ∈ {0, sign(u·o)} for every offset o) then c(u′) ≤ c(u). Hence the
least c(u) is attained on the finitely many *rays* (directions orthogonal to d − 1 independent offsets), and the set
U_b of directions sealed at every position is a union of faces of the arrangement of the hyperplanes o^⊥, closed
under specialisation.
**(iv′)** For one type: a generic direction has c(u) = K/2. So if b > K/2 every direction is sealed (a pattern never
leaves its convex hull); if b ≤ K/2 exactly the non-generic directions with **a⁰_u ≥ K − 2b + 2** are sealed — in the
plane a finite set of rays.
**(v′)** hull_b(X) = ∩_{u ∈ U_b} {p : u·p ≤ max_X u·x} is invariant and never grows. For one type it is the hull of (v).
With several types it is invariant but need not be the smallest invariant polytope, and the sealed half-spaces may
positively span where U_b does not (R§1.1, §1.2).
*Proof.* (i′) as (i) with a⁻_u(p) ≥ |N(p) ∩ H|. (ii′) Take p with a⁻_u(p) ≥ b, put C = max{u·(p + o) : u·o < 0} < u·p
and make exactly b of those neighbours alive. (iii′) Moving from u to u′ only turns negative signs into zeros. Any u
specialises to a ray because the offsets span R^d. (iv′) O = −O. ∎

So *for one cell type the half-space statement reduces to the old one*: a half-space is sealed iff its direction is,
and the hull is the polytope whose facet normals are the sealed rays. Only the step from (ii′) to "the hull is the
polytope of the sealed directions" and to "necessary" fails with several types (R§1.2).

*Counterexample to the direction version on several types, by hand: face12e, b = 4* (R§1.2). Layers along x
alternate: odd x holds only faces with normal x, even x only faces with normal y or z. An x-face has 4 offsets with
negative x, so c(u) = 4 = b for u = (1, 0, 0) (also 4 for body diagonals, 6 for face diagonals): no direction is
sealed. But for a plane at odd C the first layer outside, x = C + 1, holds y- and z-faces with 2 neighbours at x = C
and 1 at x = C − 1, total 3; the next, x = C + 2, holds x-faces with no neighbour inside: c(H) = 3, **sealed**. At
even C an x-face at C + 1 has 4 neighbours at x = C: not sealed. So face12e B45/S345 is confined to a box with walls
at odd coordinates [measured: 0 escapes from the odd box in 64,000 soup-generations, `python3 face12e.py confine` in
`research/audit/class/`].

*Hull shapes* [computed, `python3 theory.py table` (directions); `python3 seal.py` in `research/audit/class/`
(half-spaces, every primitive direction with |u_i| ≤ 5 in 3D, ≤ 8 in 2D, every position); §2]: the polytope whose
facet normals are the sealed half-spaces' normals — rectangle (every cross), octagon (Moore, b = 4), hexagon
(triangular; kagome4 at b = 2), octahedron (gump, FCC), octahedron ∩ box (face8 at b = 3; bond10 at b = 4), box
(bond10 at its tight b = 3, face12e at b = 4), rhombic dodecahedron (BCC), box (simple cubic 6 and 18, 3D cross), the
18-faced {100}+{110} solid (3D Moore, b = 10). Gump's row is exact: every diagonal layer holds all three types with
the same histogram, and no plane of any other scanned direction is sealed at any position (R§1.4). In every 3D
lattice of §2 no 1-dimensional family of directions is sealed at the tight b, so the hull is a polytope [not
independently checked]. The completeness of the half-space scan is argued, not proved (R, "Not checked").

This is Eppstein's bounding-box/diamond argument (PRIOR-ART topic 1) for an arbitrary lattice and direction; the
iff for half-spaces, the specialisation order and (iv′) are what is added.

### 1.3 Theorem B — firewalls [proved]

Let u be a sealed rational direction on a one-type lattice, layers numbered consecutively, (a_k) the histogram,
A(j) = Σ_{k ≥ j} a_k, r = max{k : a_k > 0} the reach. A band of w consecutive layers is sealed (stays dead whatever
lies on both sides) iff

  max_{1 ≤ j ≤ w} [A(j) + A(w + 1 − j)] ≤ b − 1.

If b is tight (b = A(1) + 1) this forces w ≥ r + 1, and then no pair of neighbours straddles the band: the two
sides never influence each other again. w = 2r always suffices.

*Proof.* A cell in the j-th layer of the band has A(j) neighbours below the band and A(w + 1 − j) above it. With
j = 1 and A(1) = b − 1 the condition gives A(w) = 0, i.e. w > r. For w = 2r one of j, 2r + 1 − j exceeds r. ∎
Gump: A = (3, 1), w = 3 (verbatim on gump's three types, which share the histogram, R§1.4). Cross of range r:
A(j) = r − j + 1, w = r + 1. FCC, BCC, simple cubic: w = 2. With several types the position of the band matters
(R§1.1): face12e's sealed band at b = 4 is three x-layers (even, odd, even) only; one, two or four layers, or three
starting on a sheet of x-faces, are not (R§2.2). (`theory.firewall_width` handles several types by direct
enumeration of directions; widths other than gump's, fcc's and face12e's are not independently checked.)

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
(The kagome hexagon of T6 and the Moore octagon for b = 5 are instances.) The dichotomy also holds on gump's
three-type lattice [computed, R§1.4: b ≤ 6 by C1 with generic forward count 6 for each type; at b = 7 a 30-cell sealed
set inside a cube of radius 2, `python3 proofs.py c2multi` in `research/audit/class/`]. Together with Theorem A for
one type:

  **outside sealed and inside unsealable  ⇔  (K − a⁰)/2 < b ≤ K/2.**

For several types C1 gives "no finite sealed set if some generic v has ≥ b forward offsets for every type"; where
that fails sealed sets may exist (honeycomb with 9 neighbours, b = 5: a 292-cell sealed set by peeling,
`python3 indices.py hex9`) [computed]. hex9's half-space tight b is 4, not 5 (R§1.2), and the review's table lists it
with kagome8 (b = 4) and kagome4 (b = 2) as confined and unsealable at that b. At b = 4 both have full-lattice
forward count 4 = b (no finite sealed set), no C1 certificate at a wall (best 3), and no finite sealed set found by
peeling at one wall [computed; one author, `python3 structure.py 2d` in `followup/`]; yet no pits appeared on hex9
strips at n ≥ 12 (3 in 215,000 events at n = 8, 10), consistent with the certificate being sufficient, not necessary
(F§1, "Where … wrong or silent" 5).

**C3 (faces cannot die piecewise).** In a half-space vessel {u·p ≥ h₀} of a one-type lattice, with u sealed, let ō
denote projection to the plane u^⊥. If some in-plane v₀ (generic for the in-plane offsets) has

  #{inward offsets o (u·o > 0) with v₀·ō ≥ 0} ≥ b − a⁰/2,

there is no finite sealed set: no finite part of a face can die for good. *Proof.* C1 with v = v₀ + εu, ε → 0⁺: a
boundary cell has a⁰/2 in-layer forward neighbours plus those inward ones; deeper cells have at least as many. ∎

**C4 (slabs and critical thickness; corrected wording, R§1.3).** In a slab of m layers one needs a single v₀ such
that **the cells of every layer** — each with its own reach limits on both sides, and for every cell type — have at
least b forward neighbours (C1 with v = v₀ ± εu). The original wording looked only at the two boundary layers ("at
least b − a⁰/2 projected inward offsets of reach ≤ m − 1 strictly on each side"), which is not enough:
*counterexample* [computed, `python3 proofs.py c4`]: Z² with offsets (±1, 0), (±2, 0), ±(1, 2), ±(−1, 2), K = 8,
u = (0, 1), tight b = 3; in a strip of 3 rows the boundary condition holds but the middle row has no neighbour in rows
1 and 3, and peeling finds a 10-cell sealed interval at m = 3 (nothing at m = 4, 5). `theory.slab_certificate`
checks every layer, so the m* row below is unaffected. Call m* the least m with such a certificate. In the "half
in-plane" case b = a⁰/2 + 1, "0 has half-space (Tukey) depth ≥ 1 among the projected offsets for every type" is
sufficient, not equivalent: what is needed is one v₀ that splits every type's set (R§1.3). **This is what gump's
identity ē = −2(ā + b̄) certifies**: it is a positive linear relation 2ā + 2b̄ + ē = 0, i.e. 0 lies inside the triangle
of the three projected inward offsets, and ē is only available from the third layer on; with two layers the three
types' pairs {p₁,p₂}, {p₂,p₃}, {p₃,p₁} (p₁ + p₂ + p₃ = 0) cannot be split by one line.
[computed, `theory.py table` for the certificate, `pits.py LATTICE b M` for explicit sealed sets by peeling; columns
other than gump's and face12e's not independently checked:]

| lattice | gump | face18 | FCC | BCC (8 and 14) | sc18 | sc6 | 3D cross r = 2 | bond10 at b = 4 | face8 | face12e (R§2.2) |
|---|---|---|---|---|---|---|---|---|---|---|
| m* (certificate) | 3 | 3 | 2 | 2 | 2 | 1 | 1 | none at any m | none at any m | one cube (odd, even, odd) |
| sealed set found in m* − 1 layers | yes (2: 108 cells) | yes | yes | yes | yes | — | — | at 3 and 4 layers (380, 402 cells), **none** at 5, 6, 8 (R§1.3) | 2 layers yes, 4 no | single sheet: yes |

So "three layers" is special to gump's lattice among those with a diagonal hull; FCC and BCC need two, the
simple-cubic crosses one, face12e one cube. **bond10 at b = 4** (one above its tight b = 3, §2) has no certificate at
any m, and finite sealed sets in slabs of 3 and 4 layers only (`pits.py bond10 4 M`; the review's own construction:
1,176 cells in 4 layers, none in 8 layers, none in a half-space, `python3 proofs.py bond10`). The original claim
that "a slab of any thickness I tried can be pierced by a finite dead tube", and with it "bond10 is a
counterexample to the converse of C2 for slabs", is withdrawn: the slab runs were 8 layers deep, and what ends
those replicas other than a face death is a transverse firewall, not a tube (§6, R§1.3). In two dimensions a strip
can always be cut by a transverse firewall, which is finite, so m* does not exist there.

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
`python3 energy.py selftest` → ALL OK (both identities, every step, 10 vessels on 6 lattices). Re-checked with
independent code: both identities exact at every one of 58 steps on 12 vessels (gump caps 6 and 7, face12e, fcc,
cross2, vn; torus and box), `python3 proofs.py energy` → ALL OK (R§1.4).

### 1.6 Theorem E — armour (immortal walls) [proved]

In a vessel V′ let W be a set of cells each having at least b − 1 neighbours in W and at most c − 1 neighbours in V′.
If W is entirely alive at some time it is alive forever. *Proof.* Each cell then has b − 1 ≤ n ≤ c − 1. ∎
The largest such W is the (b − 1)-core of the subgraph induced on the cells of vessel-degree ≤ c − 1 (`armour.py`).
This is a conditional: that W becomes entirely alive from a soup is measured (§5 N3), not proved (R§1.3). Re-checked:
gump and fcc octahedra of 6 layers have armoured cores from c = 8 (54 and 30 cells), none at 6, 7
(`python3 proofs.py armour`, R§1.4).

**Corollary (walls).** With u sealed, face-cell degree K_f = a⁰ + a⁻: if a⁰ ≥ b − 1 and **c ≥ K_f + 1**, a fully
live boundary layer of a slab is immortal — the face can never die, the hull can never shrink past it. With several
types a wall is a **band** of layers between two consecutive sealed positions, not a layer, and "the face cell", a⁰
and K_f are not single numbers (face12e: wall-sheet cells have degree 8, the layer beneath 11, R§1.2); the type-free
form is "Theorem E's armoured core is empty". For face12e it gives caps 5…8 and a wall from c = 9, as measured
(R§2.4, §3.2).

### 1.7 Corollary F — how many caps a face can feel [proved]

One type, tight b (b = a⁻ + 1). Then a⁰ = K − 2b + 2 and K_f = K − b + 1. The cap can act on a face cell only if
c ≤ K_f; beyond that the face is a pure threshold layer (never overcrowded), and a wall if moreover a⁰ ≥ b − 1.
A rule with any births has c ≥ b + 1. So the caps within reach of the faces are

  **b + 1 ≤ c ≤ K − b + 1 — exactly a⁰ − 1 of them.**

The interval is nonempty iff b ≤ K/2, the same condition as unsealability (C2). So the number of neighbours in the
confining hyperplane counts the rules that can be gumps: lattices with a⁰ = 2 (Moore, von Neumann, triangular,
kagome6, honeycomb) have b = K/2 and **one** candidate, c = K/2 + 1, the rule B{K/2}/S{K/2 − 1, K/2}; a⁰ = 4 gives three
(cross2: c = 4, 5, 6), a⁰ = 6 five (gump: c = 5…9), a⁰ = 8 seven. Whether a candidate
is chaotic in the bulk is a separate, measured matter (§3–§5). With several types Cor. F does not apply as stated:
on kagome4 at b = 2 the printed form puts c = 3 out of reach of the wall row (degree 2, a⁰ = 0), while the
Theorem-E form allows it, and B2/S12 there has a strip law (R§2.4).

### 1.8 Proposition G — no finite region is shielded [proved]

One type. If b ≤ K/2 < c < b + K/2, then for every finite set W and every configuration there are two
configurations of the outside giving different successors on W. *Proof.* The cell p of W furthest along a generic v
has f ≥ K/2 neighbours outside W and m ≤ K/2 live ones inside; the outside can set n(p) to any value in [m, m + f].
A next state independent of it needs that interval inside B (resp. S) — impossible unless c ≥ b + K/2 — or disjoint
from it — impossible unless b ≥ K/2 + 1 or m ≥ c, i.e. c ≤ K/2. ∎ T6 is the all-dead case. The 2D gump satisfies the
hypothesis; gump itself does not (c = 6 = K/2: a cell with six live neighbours behind it is dead next whatever lies
in front), nor does FCC (4, 6).

## 2. The lattices [computed: `python3 theory.py table`, `python3 indices.py`, `python3 pits.py …`, `python3 armour.py …`; half-spaces: `python3 seal.py` in `research/audit/class/`]

Tight b = least b with a positively spanning family of sealed half-spaces (Theorem A; "spanning" in the original
must read *positively* spanning — `theory.confinement` tests linear rank, which is equivalent for every lattice
here, where c(−u) = c(u), R§1.1); a⁰, a⁻ for a sealed ray; K_f = a⁰ + a⁻ = face-cell degree; "reach" = caps a face can
feel (Cor. F); fw = firewall width; c_arm = least cap with a nonempty armoured core in a hull of 12 (2D) or 6 (3D)
layers. All have b ≤ K/2 except those marked. The review's direction-only numbers (K, b, a⁰, a⁻, K_f) agree with this
table in all 25 rows that print them; position changes nothing for the one-type lattices, gump, face18, kagome6 and
hex12, and changes the rows marked † (R§1.2). The fw, m* and c_arm columns are not independently checked except for
gump, fcc and face12e (R, "Not checked").

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
| hex3 | 2 | 3 | 2 | finite sealed sets (b > K/2); 6 sealed directions, and more at particular positions, not pursued (R§1.2) | | | | | | | |
| † kagome4 (plain kagome; 3 types) | 2 | 4 | **2** (directions: 3) | hexagon: 6 half-spaces, plane just outside a sparse row (R§1.2) | — | — | wall row 2 (with the dense row beneath: 4) | Cor. F: none; Theorem-E form: c = 3 | — | – | none for c ≤ 4 (F) |
| † kagome8 (3 types) | 2 | 8 | **4** (directions: 5) | 12 half-space directions, C even (R§1.2; F) | — | — | wall layers: orbit A 4, 7, 8; orbit B 4, 6, 6, 8 (F) | Theorem-E form: 5–7 (F) | — | – | 8 (F) |
| † hex9 (honeycomb, 9 neighbours; 2 types) | 2 | 9 | **4** (directions: 5) | 6 half-space directions (one orbit), C ≡ 0, 2 (mod 3) (R§1.2; F) | — | — | wall layers 6, 7, then 9 (F) | Theorem-E form: 5–7 (F) | — | – | 8 (F) |
| **gump** (faces of the cubic honeycomb; corner-touching coplanar neighbours) | 3 | 12 | 4 | octahedron (8); exact with half-spaces | 6 | 3 | 9 | 5–9 | 3 | 3 | 8 |
| † **face12e** (same cells; edge-sharing coplanar neighbours — the owner's 2012 intent; *not gump*) | 3 | 12 | **4** (directions: 5) | box: 6 axis half-spaces through a sheet of face centres (odd coordinate); no sealed direction | 4 (sheet) | 4 | 8 (sheet); 11 (layer beneath) | 5–8 (Theorem-E form) | 3 (even, odd, even) | one cube | 8 (boxes 3³, 4³); 7 in the 2³ box |
| face18 (same cells, 18 neighbours) | 3 | 18 | 6 | box (6) | 8 | 5 | 13 | 7–13 | 4 | 3 | 13 |
| † bond10 (same cells; bonds sharing an endpoint = edges of the honeycomb sharing a vertex), tight b | 3 | 10 | **3** | box: 6 axis half-spaces at odd positions, c(H) = 2 (R§1.2) | — | — | — | — | 3 (axis: even, odd, even) | — | 6 (boxes 2³ … 5³; F) |
| † bond10 at b = 4 (one above tight; the original row) | 3 | 10 | 4 | octahedron ∩ box | 4 | 3 | 7 | 5–7 | 2 (diagonal) | no certificate; sealed sets at 3, 4 layers only | 7 |
| † face8 (the 8 perpendicular faces) | 3 | 8 | 3 | octahedron ∩ box (8 diagonals and 6 axis half-spaces, c(H) = 2) | 4 | 2 | 6 | 4–6 | 2 | ≤ 4 (no certificate) | 6 |
| fcc | 3 | 12 | 4 | octahedron | 6 | 3 | 9 | 5–9 | 2 | 2 | 8 |
| bcc8 | 3 | 8 | 3 | rhombic dodecahedron (12) | 4 | 2 | 6 | 4–6 | 2 | 2 | 6 |
| bcc14 | 3 | 14 | 5 | rhombic dodecahedron | 6 | 4 | 10 | 6–10 | 2 | 2 | 11 |
| sc6 (3D von Neumann) | 3 | 6 | 2 | box | 4 | 1 | 5 | 3–5 | 2 | 1 | 5 |
| sc18 (faces + edges) | 3 | 18 | 6 | box | 8 | 5 | 13 | 7–13 | 2 | 2 | 14 |
| sc26 (3D Moore) | 3 | 26 | 10 | {100} + {110}, 18 faces | 8 | 9 | 17 | 11–17 | 3 | ≤ 4 (no certificate) | 22 |
| cross3d2 (3D range-2 cross) | 3 | 12 | 3 | box | 8 | 2 | 10 | 4–10 | 3 | 1 | 9 |

Rows marked † changed in the revision (R§1.2, §5.2 item 1). Entries marked (F) are from the follow-up's
`structure.py` [computed; one author; F's `PREDICTIONS.md`, "Exact facts"]. **Run** at the new b: face12e at b = 4
(in depth, R§2; boxes to 7³ and O_h-symmetric boxes to 12³, F§4), kagome4 at b = 2 and bond10 at b = 3 (roughly,
R§2.4; then strips of 41 rows, slabs, columns and boxes, F§2–§3), kagome8 and hex9 at b = 4 (F§1: tori, confinement,
hex9 strips and hulls at c = 7, 8). Torus results at b = 4 [measured; one author, four soup densities, one size]:
kagome8 c = 5 dies, 6 dies or freezes, 7 glass (ρ = 0.677, activity 0.013), 8 freezes — no chaotic cap in reach; hex9
c = 5, 6 die, **c = 7 chaotic** (ρ = 0.537, activity 0.48), **c = 8 chaotic** (ρ = 0.619; armoured walls). bond10 at
b = 3: every box cell has vessel degree 5 (sheet) or 10, edges lowering none; armoured core 24 cells (sheet corners)
at c = 6, 7, none at c = 4, 5 (F). The axis firewalls of
bond10 (b = 3, 4), face8 (b = 3) and face12e (b = 4) were found by peeling (R§1.3). A cube-shaped seed of bond10
B45/S345 or face8 B34/S234 never leaves its own cube; the octahedron about that cube is three times wider (R§1.2).

Checks: `python3 validate.py` → ALL OK (my C stepper against numpy on 15 vessels of 11 lattices, the sealed-set
routine against plain peeling, and the face lattice against the golden side-8 log, 23 generations, final 384);
`python3 confine.py` → ALL OK (Theorem A, direction version, on 11 lattices: no live cell ever outside the polytope in
200 generations; a birth outside found for the cheapest unsealed ray where one exists); `python3 energy.py selftest`
→ ALL OK. `python3 independent.py` re-checks the two headline finds with plain numpy rolls that share no code with
the above: vn B2/S12 torus density 0.465 (gstep 0.468), box lifetimes 128 and 512 at sides 9 and 13 as upper bounds
from power-of-two snapshots (gstep medians 110 and 293), no cell outside the bounding box; fcc B45/S345 torus
density 0.392 (gstep 0.394). The position-aware hulls are checked by dynamics in the review (R§1.2:
`python3 face12e.py confine`, `confine-others`, `python3 others.py kagome`): 0 escapes in every case, and gump's
patterns do leave face12e's odd box (44,580 soup-generations outside it), as they should.

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
  With several types the slab must end at sealed positions and the face is the wall band (R§1.2); the original runs
  used direction-only slabs.
- **HULL** `run.py life`: the confinement polytope, 64 soups, lifetime = settling time, cap 10⁵–2×10⁵.

Cross-check against toy2d (cross2 B34/S234, strips 16 deep): τ_edge = 280 and 1,635 at L = 12, 16 (theirs 286 and
1,679 ± 26); slope 0.437 ± 0.004 for L = 12–20 (theirs 0.425 over the same range). Gump: 0.212 ± 0.001 per face
cell over A = 27–75 (notebook 0.208; the review 0.2121 ± 0.0004, R§3.1).

**GUMP** (scoring rule fixed in PREDICTIONS.md) = bulk chaos ∧ face law (ln τ rises ≥ 1 over the sizes, ≥ 20 deaths
at two or more sizes, CV of the wait in [0.8, 1.25]) ∧ hull lifetimes growing ≥ e per size step at two consecutive
steps, runs ending (unfinished at the cap counting as growing). *strong* = slope ≥ 0.15 per face cell. (The "≥ 20
deaths" condition was in the fixed rule but missing from the original's summary of it, R§3.3.)

**Wording changed in the revision (R§3.3, §5.2 item 8).** The hull clause "× ≥ e per size step" depends on the step,
which was chosen per family, and by its letter fails cross2 B34/S234 (the project's reference 2D gump; ratios 2.38,
2.23, 2.09, 2.30, 2.05 per step of 2) and vn B2/S12 (2.66, 2.18, 2.25, 1.91, 1.95, 1.63 per step of 4). The hull test
is now: *the median lifetime grows at a rate per unit of side (ln of the ratio over the side increase) comparable with
the slab slope*. Rescored with it (rates from R§3.3): cross2 0.36–0.43, steady, against slab 0.437 — passes; vn
0.245 → 0.122 per unit of side to side 33 and 0.11 from 33 to 81 (`python3 vnbox.py`), against strip 0.12 at
L = 64–80 — passes; cross3 c = 7 (B456/S3456, ratios 3.34, 2.69, 3.15 per step of 4, i.e. ln(ratio)/4 ≈ 0.30, 0.25,
0.29) against slab 0.27 — passes, where the old rule failed it by one step; cross3 c = 6 (B45/S345) 0.13 → 0.08 against
slab 0.05 — grows at its weak law's rate. So the line between vn (0.12, "a gump") and cross3 c = 6 ("a miss", weak) is
a factor of two in a rate, not a difference in kind; the strength cutoff that would separate them was never fixed.
The tallies in §5–§6 are stated by the rule fixed in advance unless said otherwise.

## 4. What the training runs already changed (the three lattices the project knew)

`python3 scan.py gump 4 --cs 5,6,7,8,9,10,11,12`, `scan.py cross2 3`, `scan.py moore 4`, `follow.py gump3`,
`follow.py weak`, `run.py life gump 4 C --R 4|5|6`:

1. **Gump is not the only capped threshold on its lattice that does it.** Caps 6, 7, 8 (B45/S345, B456/S3456,
   B4567/S34567) are all chaotic on the torus (ρ = 0.419, 0.482, 0.548) and in periodic {111} slabs they have
   nearly the same memoryless face law: ln τ = 5.48, 7.39, 9.92, 12.50, 15.53 ± 0.20 (c = 6) and 5.42, 7.33, 9.88,
   12.59, 15.92 ± 0.23 (c = 7) at A = 27, 36, 48, 60, 75; slopes 0.212 ± 0.001 and 0.215 ± 0.001; c = 8: 5.98, 7.81,
   10.34, 13.46, 16.90 ± 0.35, slope 0.214 ± 0.001; CV 0.96–1.02. Re-measured with independent code (R§3.1): slopes
   0.2121 ± 0.0004 and 0.2156 ± 0.0005, ln τ within 0.02 at four sizes each; but the c = 6 and c = 7 laws are *not
   identical*: they cross (c = 7 shorter-lived by 0.05 at A ≤ 48, longer-lived by 0.12 and 0.18 at A = 60, 75), the
   slopes differ by 1.6 ± 0.3 %, and the boundary densities differ (0.52 at c = 6, 0.62 at c = 7). Equal within 0.2 in
   ln τ over ten units of ln τ. (c = 8 not re-measured.) In octahedra they differ: median lifetime at R = 4, 5, 6
   layers (L1 radius 8, 10, 12): c = 6: 314, 3,682, > 10⁵; **c = 7: 16,896, > 10⁵** (final density 0.22); c = 8: 192,
   1,024, 4,224 ending *frozen* at density 0.70 — Theorem E's armour (c_arm = 8: the 120 hull-edge cells have
   vessel-degree 7). The review's runs agree within the quartile spread of 64 soups (c = 6: 299 at R = 4, 4,671 at
   R = 5; c = 7: 21,450 at R = 4, final density 0.23; 72× at R = 4, R§3.1). So B456/S3456 is a second, longer-lived
   gump on the face lattice; gump is the *lowest* cap that works, not the only one. (The phase survey's `rules.csv`
   already had its 10⁵-capped lifetimes.) **[conjecture]** c = 7 outlives c = 6 in hulls because a hull-edge cell
   (degree 7) is overcrowded at c = 7 only when saturated.
2. **Moore B456/S3456 is not simply "eroding"** [not independently checked]. Its faces are out of the cap's reach
   (K_f = 5 < 7), below L ≈ 10 a row locks fully alive (a conditional wall), and from L = 28 to 320 the row wait is
   memoryless (CV 0.86–1.04) with ln τ = 6.03, 6.86, 7.66, 8.69, 10.23, 11.60 ± 0.08, 13.41 ± 0.24 at L = 28, 40, 56,
   80, 120, 160, 240: a weak, slightly concave law, 0.02–0.07 per cell (diagonal faces 0.12–0.23 for L = 8–28).
   Octagon lifetimes grow like R² (31, 100, 192, 332, 610 at R = 6…24), so in practice nothing like gump — but for a
   quantitative reason.
3. cross2: c = 5 is the only chaotic cap (4 dies, 6–9 freeze); its edge law reproduced; boxes 377 … 19,673 for
   sides 11 … 21 (× e^0.39 per unit side; by the review's ratios 0.36–0.43 per unit of side, steady — it fails the
   old "× e per size step" hull clause only because the step was 2, §3).

## 5. The criterion, ingredient by ingredient

**Proved** (for a capped threshold to show confinement, no local permanent death, and faces that die):

- **N1 sealed outside — sufficient:** a positively spanning family of half-spaces with c(H) ≤ b − 1 (Thm A). For
  one type: b > a⁻(u) on a positively spanning set of directions. That this is *necessary* for confinement is not
  proved, even with one type: A(ii) exhibits one birth one step outside a half-space, not a pattern that escapes
  every bounded region (R§1.3). The original "an iff" is withdrawn.
- **N2 unsealable inside:** b ≤ K/2 (one type; Thm C2, an iff; also an iff on gump's lattice, R§1.4). With N1:
  (K − a⁰)/2 < b ≤ K/2. Several types: C1's forward count for every type; in a band or slab, for every layer (C4).
- **N3 no armour [proved conditional + measured]** (Thm E + Cor. F): beyond the reach a fully live face is immortal
  when a⁰ ≥ b − 1; that such a face forms from soups is measured, not proved (R§1.3). The type-free form is "the
  armoured core of Theorem E is empty"; for one type and a⁰ ≥ b − 1 it reads c ≤ K_f = K − a⁻. *Dynamically confirmed
  without exception:* in all 18 families and 38 lattice–cap pairs with c ≥ K_f + 1, a⁰ ≥ b − 1 and anything alive
  after the burn-in, the boundary layer sits at density ≥ 0.99 with activity 0.00 and not one face death was
  recorded (`data/scan_table.md`, verdict WALL). Recounted (R§3.3): 60 such pairs were scanned in 20 families; 38 in
  18 families have anything alive after the burn-in, and in all 38 every slab run has boundary density 1.00 and zero
  face deaths; the verdict column says WALL for 26 and "freeze" for 12; the torus is chaotic in only 25 of them, frozen
  in 12, glass in 1. Re-derived out of sample (R§3.2): fcc c = 10 = K_f + 1 (0 deaths at A = 25, 49, boundary density
  1.000; c = 9 dies, ln τ = 11.23 ± 0.02 at A = 49 against the original 11.10) and face12e c = 9 (0 deaths; caps 6, 7,
  8 die). Where a⁰ < b − 1 the out-of-reach faces are either the same in practice (Moore c = 8, tri12 c = 11, tri18
  c = 16, 17, the 5×5 Moore c = 22) or passive and weakly metastable (Moore c = 7, tri18 c = 15, hex12 c = 11:
  0.03–0.09 per cell; sc26 c = 18, 19: 0.13, 0.16 — so "c ≤ K_f" has no support when a⁰ < b − 1: sc26 c = 19 is
  "strong" by the fixed cutoff, and no hull was run, R§1.3). In hulls the same happens from c_arm on (fcc c = 8, 9;
  bcc8 c = 6; sc6 c = 5; gump c = 8: runs unfinished or frozen at density 0.6–0.8) — with one exception in the
  original's own data: bond10 c = 7 = c_arm (at b = 4) has growing hull lifetimes (1,152, 45,120, > 10⁵, R§1.3).
  Out of sample [measured; one author, F§1, §3]: hex9 c = 8 (armoured outer pair, degrees 6 and 7) and bond10 c = 6
  at b = 3 (24-cell corner core; 128 of 128 boxes of 3³, 4³ freeze with it fully alive, no wall sheet dead) behave as
  the clause says; but under hex9's armoured band the next band still dies memorylessly in strips, and kagome4 B2/S12
  walls freeze with no armoured set at all (summary, clause 3 (a), (b)).
- **N4 two-sided drive** (Thm D): no period ≥ 3 without both undercrowding-after-life and overcrowding-after-life
  events. Measured in 8 chaotic torus states on 8 lattices: O1 = 0.08–0.12 and U1 = 0.05–0.12 per cell per
  generation (O1 = 0.116–0.122 on gump, cross2, cross3, Moore, vn, fcc — nearly universal, not understood); in
  glasses both fall together to 0.002–0.04 (`python3 energy.py LATTICE b c`) [rates not independently checked].

**Measured:**

- **S1** Of the 50 (lattice, cap) pairs the BULK rule calls chaotic with the cap within reach (c ≤ K_f), **42 have a
  memoryless face law by the scoring rule fixed in advance** (R§3.3; the original said 46). Fail by that rule: cross4
  c = 7 and bcc14 c = 7 (the face is starved: bcc14 face density 0.19–0.32 against 0.37 in the bulk; cross4 no
  replica survives the burn-in at any L ≤ 128), tristar2 c = 8 (a glass at the classifier's edge whose replicas
  settle before a face dies, activity 0.059), four with 1–15 deaths at their second size that the original counted
  as laws — face8 c = 5 (10,265 and 8 deaths), bcc8 c = 6 (29,860 and 1), sc6 c = 4 (63,117; 5; 15), sc6 c = 5
  (13,625 and 1) — and cross3 c = 8 (CV 1.29 at A = 40 with 66 deaths). cross3d2 c = 10, which the original excluded
  as a glass, meets the rule (219 and 422 deaths, CV 1.02–1.03). So "CV 0.83–1.23 wherever ≥ 50 deaths" is false by
  one entry (cross3 c = 8: 1.29; also in `laws.md`). Slopes 0.05–0.45 per face cell (`data/laws.md`).
- **S2 a starvation observation (post hoc; no longer a criterion, R§4).** σ = K_f·ρ/b — the neighbours a face cell
  would see at bulk density, over the birth count — is 0.74 and 0.80 in the two eroding cases (bcc14 c = 7,
  cross4 c = 7); the laws with σ ≤ 0.88 are weak (Moore 0.74, bond10 c = 6 0.77, sc18 c = 9 0.85, face18 c = 9 and
  sc26 c = 17 0.87, cross3 c = 6 0.88: slopes 0.03–0.12) except vn (0.70, slope 0.11–0.18, K = 4); every law with
  σ ≥ 0.89 has slope ≥ 0.10 (30 of them ≥ 0.15). The review's verdict (R§4): the line at 0.85 was drawn after the
  fact; of the four pairs below it two erode and two (vn c = 3, bond10 c = 6) have a memoryless law; above it, the
  rank correlation of σ with the slope among the 36 pairs with a law is 0.03 (p = 0.9); out of sample on face12e
  σ = 0.80 with K_f = 8 (the wall sheet; "starved") or 0.90 with K_f = 9 (the y/z-faces; passes by 0.05), while the
  wall is the densest layer (0.52 against 0.40 inside) and the law is strong; on kagome4 σ = 0.48 or 0.96 depending
  on the layer. An index that flips with the choice of layer cannot be scored. *What would make it a criterion:* fix in
  advance which layer K_f refers to (naturally the layer whose emptiness is the permanent event) and state "a
  chaotic pair with σ < 0.85 has no face law with slope ≥ 0.10 per cell"; vn B2/S12 (σ = 0.70, 0.12 per cell at
  L = 64–80) already falsifies that. A direct description of starvation is in `faces.tsv`: the boundary density is
  below the interior's in both eroding cases and above it in every strong law re-measured (gump 0.52 / 0.41, fcc
  0.46 / 0.39, face12e 0.52 / 0.40). Within a family the slope rises with the cap: cross3 0.06, 0.27, 0.33, 0.40
  (c = 6…9); cross4 none, 0.10, 0.21, 0.25, 0.29, 0.27 (c = 7…12) [not independently checked].
- **S3 hulls.** Where I ran the polytope (§6) the slab law carries over in 14 pairs (vn c = 3, cross2 c = 5, cross3
  c = 7, 8, gump c = 6, 7, fcc c = 6, 7, bcc8 c = 5, face8 c = 5, sc6 c = 3, sc18 c = 10, bcc14 c = 8, cross3d2
  c = 5); of these sc6 c = 3 and cross3d2 c = 5 rest on one finished hull size and face8 c = 5 on 8 slab deaths at its
  second size (R§3.3); face8's octahedra are invariant vessels but not its hulls (octahedron ∩ box, §2). Only vn's,
  gump's (R = 4, 5) and fcc's (R = 3–5) hull runs were repeated by the review. It is not yet visible at the sizes run
  for the weak laws (cross3 c = 6: 121, 344, 869, 1,676 at sides 17…41; cross4 c = 9, 10: a box lives about as long as
  an edge of its own length waits). bond10 at b = 4 (one above tight; octahedral vessels, which are not its hulls)
  dies in linear time at c = 6 (24, 46, 74, 124 at R = 4…7; why was not examined, R "Not checked"), and at c = K_f
  (cross3 c = 9, cross4 c = 12) and from c_arm on the hull *freezes* (final density 0.33–0.8) instead of peeling,
  except bond10 c = 7. **[conjecture]** "Within reach" needs a margin at the hull's edges and corners: the exact
  condition is that the cap can act on every stratum of the hull boundary. Out of sample [measured; one author,
  F§3, §4]: the slab law does **not** carry over to bond10 B34/S234's boxes at b = 3 (4³ ≈ 10⁹ against 600–1,500
  forecast; columns 24–196× tougher per wall than slabs; summary, clause 6), although its cap reaches every degree
  there (degrees 5 and 10 only, no armour at c = 5) — the edges act through density, not degree; it does carry over
  for face12e boxes to 7³ (16 of 128 finished by 3 × 10⁷, forecast 9–33).

**Not predicted by anything I have — the chaos window** [2D scans not independently checked]. Which caps are chaotic
on the torus: cross2 {5}; cross3 {6…11}; cross4 {7…14}; vn {3, 4}; Moore {7}; star2 {9, 10, 11}; tristar3 {13…17};
tri18 {15, 16, 17}; tri12 {11}; hex12 {11}; kagome6 {6}; moore_r2 {22}; tristar2, tri6: none (glass at best); gump
{6, 7, 8}; fcc {6…11}; bcc8 {5, 6, 7}; bcc14 {7…12}; sc6 {3, 4, 5}; sc18 {9…15}; face18 {9…15}; sc26 {17, 18, 19};
cross3d2 {4…10}; bond10 at b = 4 {6…9}; face8 {5} (upper ends are where the scan stopped for sc18, face18, sc26).
Added by the review (R§2.4, §3.2): face12e {6…10} (5 dies); bond10 at b = 3 {4…8}; kagome4 at b = 2: c = 3 chaotic,
c = 4 freezes. The single-site mean field is useless here [not independently checked]: its "unstable fixed point with
enough undercrowding" rule called 42 pairs chaotic and 25 were; of the 121 it called dead or frozen, 50 are chaotic
(the high caps of every cross and of fcc, bcc, sc among them); and vn c = 3, sc6 c = 3, cross3d2 c = 4 are chaotic
although their mean-field fixed point is *stable* (slope −0.25, −0.70, −0.83). **Mean-field instability is neither
necessary nor sufficient.** One regularity survives: a chaotic cap exists *within reach of the faces* in all 12
families with b/K ≤ 3/8 and in only 3 of the 17 with b/K > 3/8 (vn, bond10, and sc26 barely, at c = K_f) — 26 of 29.
Since the revision: bond10's entry is its b = 4 family, one above tight (at b = 3, b/K = 0.3, it is on the expected
side); kagome4 at b = 2 (b/K = ½, chaotic at a cap the Theorem-E form puts in reach) is a second exception like vn;
face12e (b/K = ⅓) is on the expected side. The 26 of 29 was not recounted with these changes. Out of sample
[measured; one author, F§1]: kagome8 at b = 4 (b/K = ½) has no chaotic cap in reach, as the rule expects; **hex9 at
b = 4 (b/K = 0.44) is chaotic at c = 7**, within reach, an exception (the follow-up counts it the third, after vn and
kagome4).

**The brief's candidate ingredients, judged:**

| ingredient | verdict |
|---|---|
| fraction of the neighbourhood in a confining hyperplane | **Matters, in two exact ways and one empirical** (one type). a⁰ − 1 is the number of caps the faces can feel (Cor. F); a⁰ ≥ b − 1 is what turns an out-of-reach cap into a wall; and with tight b, b/K ≤ 3/8 ⇔ a⁰ ≥ K/4 + 2, which for K = 4, 8, 12 means *half* the neighbourhood (2, 4, 6). It is not the fraction as such: sc18 (0.44), cross3d2 (0.67), bond10 at b = 4 (0.40) also work. With several types a⁰ is not a single number (face12e, kagome4: §1.6, §1.7). |
| birth threshold near a third | b ≤ K/2 is necessary for no finite sealed set (proved, one type). b/K ≲ 3/8 is the best single predictor of a chaotic in-reach cap existing (26/29), but vn and kagome4 have b/K = ½ and hex9 (c = 7 chaotic) 0.44 [measured; one author, F§1]. |
| the cap | Necessary (without it: threshold lemma, period ≤ 2). Must leave no armoured set (Theorem E); for one type with a⁰ ≥ b − 1 that is c ≤ K_f. More than one cap usually works (gump 6–7, cross3 7–8, fcc 6–7, face12e 6–8 in slabs, …). |
| mean-field instability of the fixed points | Irrelevant as a criterion (see above). What is true instead is the two-sided lemma. |
| critical thickness | A property of each gump (m* = 1, 2 or 3 by the certificate; one cube for face12e), not a condition for being one. bond10 at b = 4 has no certificate at any m and finite sealed sets in slabs of 3 and 4 layers only (R§1.3); its c = 6 octahedra die in linear time (24, 46, 74, 124 at R = 4…7), but octahedra are not its hulls and b = 4 is not its tight b, so it is no longer "the one chaotic in-reach rule that is not a gump" without qualification. |

**Class statement.** Superseded by the summary's seven clauses (R§5.1). The original's remark survives as clause 7's
conjecture: the boundary layer (with several types, the wall band) is then a contact-type process with the empty
band as its only absorbing state (exact, by clause 1), fed by the bulk.

## 6. Predictions and outcomes

Full text, with what I had seen at each stage: `PREDICTIONS.md`. Data: `data/scan_table.md` (every cap of 27
families), `data/laws.md` (every face law), `data/hulls.txt` (every hull run).

**New gumps (bulk chaos + memoryless face law + hull lifetimes growing, sparse debris):**

| lattice, rule | slab law: ln τ at face sizes | slope / face cell | hull medians (64 soups) | predicted? |
|---|---|---|---|---|
| **vn B2/S12** (2D, 4 neighbours) | 5.62, 7.08, 8.23, 9.26, 10.67, 12.53, 14.49 ± 0.24 at L = 12…80 [not independently checked] | 0.18 → 0.11 | boxes of side 9…33: 110, 293, 640, 1,443, 2,752, 5,376, 8,763; final density 0.03. Review re-run (R§3.3, `vnbox.py`, upper bounds within × 2): 8,889 at side 33, 345,930 at 65, about 2.1 × 10⁶ at 81: 0.11 per unit of side | **no — called "dies or freezes"** |
| cross3 B456/S3456 (2D) | 5.96, 8.23, 11.31 at L = 20, 28, 40 | 0.27 | sides 13…25: 109, 364, 978, 3,081 (passes the revised hull test, §3) | yes (stage 1) |
| cross3 B4567/S34567 | 6.60, 9.28, 13.27 | 0.33 | sides 11…19: 96, 212, 331, 900, 1,403 | marginal call, yes |
| **fcc B45/S345** | 4.61, 6.85, 9.25, 11.97, 14.68 ± 0.24 at A = 25…81; review: (4.872, not comparable), 6.837, 9.226, 11.913, 14.959 ± 0.035 (R§3.1) | **0.181 ± 0.001** (R§3.1; the original's 0.19 leans on A = 25, where the wait is half the burn-in; from A = 36 the original's own numbers give 0.174). Predicted 0.21 ± 0.07: holds, but an interval of a third either way is not a sharp test | octahedra R = 3…7: 162, 832, 9,847, > 10⁵, > 10⁵; final density 0.01–0.04 (review: 132, 958, 11,503 at R = 3, 4, 5) | **yes** |
| fcc B456/S3456 | 4.08, 9.35, 15.26 ± 0.30 | 0.22 | 4,617, > 10⁵ (60/64 unfinished at R = 4) | yes |
| **bcc8 B34/S234** | 8.27, 10.80, 16.45 ± 0.16 at A = 25, 36, 49 | 0.24–0.43 (uneven) | rhombic dodecahedra R = 3…5: 916, 17,600, > 10⁵ | **yes** |
| **sc6 B2/S12** (3D von Neumann) | 9.20, 11.91, 17.75 ± 0.27 | 0.25–0.45 (uneven) | boxes R = 2, 3: 2,752, > 10⁵ (one finished size; R = 3, 4, 5 unfinished at density 0.40, R§3.3) | **no** |
| sc18 B6789/S56789 | 5.87, 10.03 at A = 49, 81 | 0.13 | 355, 10,107, > 10⁵ | yes |
| bcc14 B567/S4567 | 4.11, 8.32, 13.73 | 0.17 | 57, 164, 627 | yes |
| cross3d2 B34/S234 | 3.61, 7.73, 13.04 | 0.17 | 87,889 (24/64 unfinished), > 10⁵ (one finished size) | yes |
| face8 B34/S234 (face lattice, 8 perpendicular neighbours) | 9.97, 16.99 ± 0.35 at A = 27, 48 (8 deaths at the second size: fails the fixed slab rule, R§3.3) | ≈ 0.33 (two sizes) | octahedra R = 4, 5, 6: 1,516, 15,716, > 10⁵ (octahedra are invariant but face8's hull is octahedron ∩ box, §2) | yes |
| **face12e B45/S345** (the review's, R§2; the owner's intended 2012 neighbourhood, not gump) | 6.428, 7.999, 10.183, 12.089, 14.542 ± 0.040 at A = 16, 20, 25, 30, 36 wall faces; CV 0.98–1.00; lead's own code 6.427, 8.005, 10.186 (NOTEBOOK 2026-11-14) | 0.410 ± 0.001 per wall face; 0.205 per cell of the layer beneath, whose death is the permanent event | boxes 2³ … 6³: 10, 60, 439, 9,855, 707,038; none of 64 finished at 7³ in 300,000; final density 0.127 → 0.010. 7³ [measured; one author, F§4]: 16 of 128 finished by 3 × 10⁷ (forecast 9–33), median ≈ 1.6 × 10⁸ by an exponential estimate, not measured directly; ln ratio per unit of n² 0.42 from 6³ to 7³ against 0.39 from 5³ to 6³ | not called (by the direction-only clause 1: "not confined, not a gump"; PREDICTION-face12e.md) |
| **hex9 B456/S3456** (honeycomb, 9 neighbours, 2 types, b = 4, c = 7) [measured; one author, F§1] | strips between sealed walls, depth 2n + 7: 6.121, 7.505, 8.822, 10.023, 11.162, 12.239, 13.289 ± 0.004–0.011 at n = 8, 10, …, 20 wall cells; CV 0.97–1.02; hazard flat; 3 pits in 215,000 events | **concave**: local 0.692, 0.658, 0.601, 0.569, 0.538, 0.525 per wall cell (straight line rejected, χ² ≈ 2,900 on 5 dof) | hexagonal-seed hulls R = 2 … 7: 24, 88, 355, 727, 1,195, 4,102 (64 of 64 finished each); final density 0.29 → 0.04; sides unequal, not a rate test | chaos only guessed (p = 0.35); the strip forecast, conditional on chaos, held |

Slab laws without a hull test, or with an inconclusive one (so not claimed as gumps): cross4 c = 8–12; fcc c = 8, 9
(hull armoured: frozen); bcc8 c = 6 (armoured; 1 death at its second slab size); bcc14 c = 9, 10; sc6 c = 4 (R = 2
hull ends dense, 0.64), c = 5 (hull freezes in 33–320 generations); sc18 c = 9, 11, 12, 13; face18 c = 9–13; sc26
c = 17; cross3d2 c = 4, 6–9; bond10 at b = 4, c = 7 (1,152, 45,120, > 10⁵, final density 0.27–0.33). Found by the
review, rough (R§2.4): kagome4 B2/S12 (hexagon at b = 2; torus ρ = 0.482; strip ln τ = 7.24 … 12.85 at 4 … 12 wall-row
cells, CV drifting to 1.23, transverse cuts not censored; hexagon medians about × 2 per unit of R, upper bounds from
R = 6); bond10 at b = 3, B34/S234 and B345/S2345 (slab ln τ = 8.04, 12.71 and 7.78, 12.23 at 16, 25 wall faces, about
0.5 per wall face; boxes of 4³ unfinished in 300,000 at c = 5; at c = 6 endings dense, 0.54–0.65).

Followed up [measured; one author]. **kagome4 B2/S12** in strips of 41 rows (F§2): the review's drift came not from
transverse cuts (there are none at 41 rows) but from walls that freeze (static, density 2/3, at 0.27–0.44 of the
wall-death count); with frozen walls censored, ln τ = 8.285, 9.867, 11.405, 12.970, 14.380, 15.959, 17.387 at
n = 6, 8, …, 18 wall-row cells, CV 0.97–1.02 (0.81 at n = 18, truncated), slope 0.772 ± 0.003 per wall-row cell
(0.257 per cell of the two-row band); forecast 0.70 ± 0.08; ln τ insensitive to depth (25, 41, 57 rows) and to the
freezing censor (256 vs 1,024 generations: 0.02). Hexagon lifetimes not re-run. **bond10 B34/S234 at b = 3** (F§3):
slab law, cuts censored, ln τ = 4.616, 6.156, 8.050, 10.072, 12.620, 15.161 at A = 9, 12, 16, 20, 25, 30 wall faces,
slope 0.492 ± 0.001; columns 7.795, 10.359, 13.33 at A = 9, 12, 16 (24×, 67×, 196× the slab's τ); boxes 3³ median 292
(first wall death at ln τ per wall 7.87 ± 0.07, the 3 × 3 column's value, not the slab's), 4³ no permanent dead set in
64 × 10⁷, 4 of 64 dead by 10⁸, median ≈ 10⁹ (a factor ~2 either way on 4 events). So it has every signature in slabs
and boxes that grow enormously, but not by its slab law (summary, clause 6). At c = 6 (B345/S2345) every box freezes
with its corner armour alive (3³ median 17, 4³ 2,063).

**face12e with full cubic symmetry** (one coin per O_h orbit about the box centre, density 0.45, 64 soups, c = 6;
F§4 [measured; one author]; symmetry preserved at every step, `three_d.py symcheck 6`): median lifetimes

| box | 4³ | 5³ | 6³ | 7³ | 8³ | 9³ | 10³ | 11³ | 12³ |
|---|---|---|---|---|---|---|---|---|---|
| median (quartiles) | 3 (2–5) | 9 (5–10) | 9.5 (6–13) | 19 (12–36) | 19 (12–25) | 33.5 (24–57) | 35.5 (26–60) | 100.5 (57–162) | 103.5 (68–154) |
| without symmetry (R§2.2; 7³ F estimate) | 439 | 9,855 | 707,038 | ≈ 1.6 × 10⁸ | | | | | |
| lead's independent re-derivation | 3 | 7.5 | 8 | | 18 | | | | |

Full cubic symmetry is fatal within tens of generations: 74,000× shorter than without symmetry at 6³ (88,000× by the
lead's median), 146× at 4³; 16–54 of 64 soups per size end empty. The lead's check (`python3 lead_check_box.py sym N
R [SEED]` in `research/audit/class/`, no code shared with the follow-up; it reuses the stepper of
`lead_check.py`, which equals `reference/oracle.py` on gump's offsets, with face12e's offsets; lifetime = exact transient length, other soups) agrees to within 1–1.5 generations, which is
within the quartile spread. Medians come in equal pairs (7³, 8³; 9³, 10³; 11³, 12³);
growth 0.028 per unit of n², no law fitted (the lifetimes are dominated by the first transient). Forecast 10–100 for
4³ … 8³ and ≥ 10³× shorter at 6³: held, more extreme than forecast.

**Scorecard.** Tallies by the original's count, with the review's recount (R§3.3) where it differs. The hull rule's
wording changed in the revision (§3); the tallies below use the rule as fixed in advance.

| what was predicted | hits | misses | notes |
|---|---|---|---|
| Stage 1 "GUMP" calls (28 lattice–cap pairs) | 8 by judgment (cross3 c = 7; fcc c = 6, 7; bcc8 c = 5; bcc14 c = 8; sc18 c = 10; cross3d2 c = 5; face8 c = 5). Mechanically 4 (fcc 6, bcc8 5, bcc14 8, sc18 10); 6 if a step into an unfinished size counts (fcc 7, cross3d2 5); cross3 c = 7 misses the old hull rule by one step (ratio 2.69) and passes the revised one; face8 c = 5 misses the slab rule (8 deaths at its second size) | 14 | 6 more have the slab law but no conclusive hull test. Misses: bulk not chaotic at the cap I named (star2, tristar2, tristar3 ×2, tri18, sc18 c = 8, face18 c = 8, sc26 ×3), starved faces (cross4 c = 7, bcc14 c = 7), weak (cross3 c = 6), tubes (bond10 c = 6: in fact transverse firewalls, at b = 4, one above tight). The 6 and the 14 recount as stated; tristar2 c = 8 is "bulk not chaotic" here but one of the 50 chaotic pairs in S1 (R§3.3). |
| Stage 1 marginal calls (4) | 3 | 0 | cross4 c = 9: slab law only |
| Stage 1 explicit "not a gump" (15 pairs: walls, passive faces, sealed holes) | 14 | 1 (bond10 c = 7 behaves like one) | walls on vn c = 4, tri6, kagome6 as called; Moore weak; hex9 dead. Five of the 14 hold because the torus dies at the named cap (tri18 12, tri12 9, hex12 9, moore_r2 15, 16), so the stated reason was not tested; three (hex3, kagome4, kagome8) were scanned at the direction-only b (R§3.3) |
| Stage 1 blanket "every other cap is not" | — | **2 gumps missed (vn c = 3, sc6 c = 3)** and ≥ 12 further slab laws at caps the mean field called frozen | the mean-field window is the failed part. vn's miss confirmed by the review's box re-run to side 81; sc6's rests on one finished hull size |
| fcc slope 0.21 ± 0.07 | 1 (0.181 re-measured, R§3.1; the original said 0.19) | | the interval is wide |
| Q1 cap-independent slope | fcc (0.18, 0.22, 0.18; only the first re-measured) | cross3 (0.06–0.40), sc18 | holds on plateaus in 3D (also gump — 1.6 % apart at caps 6, 7, R§3.1 — cross3d2 0.15–0.19 over six caps, sc18 0.13 over three; face12e 0.42, 0.41, 0.41 at caps 6, 7, 8 out of sample, R§3.2), fails in 2D |
| Q2 ordering in 2D | Moore lowest | cross3 c = 6 is far weaker than cross2 | |
| Q3 hull armour from c_arm (5 new pairs) | 4 (fcc c = 8, 9; bcc8 c = 6; sc6 c = 5) | bond10 c = 7 (ends at density 0.27–0.33, but lifetimes grow) | this miss is the original's own datum against the printed clause 3 (R§1.3) |
| Q4 both drives in every chaotic state | 9 of 9 | the "one drive < 0.002 in glass" half: glasses keep both at 0.01–0.04 | |
| Stage 2 (R₁ index), informative calls (19) | 13 | 5 (sc18 and face18 c = 9, 10; sc26 c = 17), 1 half | called the bcc14 c = 7 erosion; useless across lattices in 3D [not independently checked] |
| Stage 3 (bond10 c = 6 not a gump) | hull lifetimes linear; non-face endings overtake face deaths (0.13, 0.28, 1.04 per face death at A = 27, 48, 75; review 0.11, 0.18, 0.77 — and they are transverse two-layer firewalls of another diagonal, not tubes, R§1.3) | the slab wait still grows, 0.062 per cell | concerns b = 4, one above tight [not independently checked otherwise] |
| Stage 4 (R₁ inside cross3/cross4, 7 slopes + monotonicity) | 3 (cross3 c = 8; cross4 c = 7 none; monotone in both) | 5, all underestimates | [not independently checked] |
| Stage 5 (chaos at a low cap iff b/K ≤ 0.38, nine 3D families) | 8 | 1 (bond10 is chaotic at c = 6) | bond10's family is b = 4, one above tight [not independently checked] |
| The brief's ingredients on the eight discriminating rows | 7 | 1 (bond10 c = 7) | better than my stage 1 there; "one cap per neighbourhood" wrong on gump, cross3, fcc |
| Follow-up, clause 1 (P1.1): confinement on kagome8, hex9 at b = 4, caps 5–8 | 1 (0 escapes, 1,536 soups) | 0 | [measured; one author, F§1] |
| Follow-up, clauses 2, 3, 5 on hex9 c = 7 strips (P1.3), hulls (P1.5), armour at c = 8 (P1.4) | 3 | 0 | P1.3 "linear" only approximately (concave); P1.4 holds as stated, the band beneath the armour dies in strips (clause 3 silent); P1.5 not a rate test [F§1] |
| Follow-up, kagome4 slope 0.70 ± 0.08 and no pits (P2.1, P2.2) | 2 | 0 | 0.772 ± 0.003; the stated cause of the review's drift (cuts) was wrong: frozen walls [F§2] |
| Follow-up, bond10 at b = 3 (P3.1 boxes from the slab law; P3.2 c = 6 frozen; P3.3 hypotheses) | 2 (P3.2; P3.3's H2) | 1 (P3.1: × 10⁶ short, expected by its author) | H1 alone and H3 refuted; clause 6 wrong as first written [F§3] |
| Follow-up, face12e (P4.1 7³ count; P4.2 symmetric boxes) | 2 | 0 | 16 of 128 (forecast 9–33); 74,000× at 6³; P4.2 re-derived by the lead [F§4] |
| Follow-up guess: a chaotic in-reach cap on kagome8 and on hex9, p = 0.35 each | — | — | kagome8 none; hex9 c = 7 (and c = 8, armoured) |

Honest reading: the proved parts of the criterion (sealing, reach, walls, armour) never failed and explain every
"not a gump" above the reach — but clause 1 as first written (sealed *directions*) would have called face12e, a
lattice I never saw, wrongly, and mis-rowed bond10, face8, kagome4, kagome8 and hex9 (R§1.2). The part that was
supposed to pick the cap (mean field) performed at chance, and it is where the two unpredicted gumps came from. Four
gumps predicted from the criterion before any dynamics on those lattices passed all three tests on first try (fcc
B45/S345 with its slope, bcc8 B34/S234, cross3 B456/S3456, face8 B34/S234 — the last on 8 slab deaths at its second
size), and four more with thinner hull evidence. (The original sentence said "three" and listed four.)

## 7. Why the Moore neighbourhood fails, and why the known gumps are or are not unique

- **Moore.** A line holds a⁰ = 2 of its 8 neighbours, so b = K/2 = 4 and (Cor. F) exactly **one** cap is within
  reach of a face: c = 5, the rule B4/S34. It dies [measured; not independently checked]. The only chaotic Moore cap
  is c = 7, where a face cell (5 neighbours) can never be overcrowded: its rows are conditional walls when short and
  weakly metastable when long (§4.2). The same holds for every a⁰ = 2 lattice: one candidate each —
  triangular B3/S23 (freezes), kagome6 B3/S23 (freezes), honeycomb B2/S12 (glass), tri12/hex12 B6/S56 (dies) —
  **except von Neumann, whose one candidate B2/S12 is chaotic, and it is a gump** (§6). So Moore fails for a
  structural reason (one candidate) plus a contingent one (that candidate's bulk is dead); toy2d's "a line holds too
  few of its neighbours" is the first half. (The plain kagome lattice, which the table first dismissed, has
  B2/S12 as a candidate with all three signatures at its half-space tight b = 2, R§2.4.)
- **cross2** has three caps in reach, 4, 5, 6: 4 dies, 6 freezes, 5 is the gump — unique [measured], as claimed.
- **gump's lattice** has five, 5…9: 5 dies, 9 is glass, 8 is armoured in octahedra, **6 and 7 are both gumps** (§4.1).
  The uniqueness claimed in the brief is false there; minimality is true. On the same cells with the edge-sharing
  coplanar neighbours (face12e) caps 6, 7, 8 all have the slab law and 9 is a wall (R§3.2).

## 8. Surprises

1. The smallest gump has four neighbours: **B2/S12 on the von Neumann neighbourhood** — alive next iff n + x ≥ 2,
   unless n ≥ 3. Bounding-box confinement (2 > 1), no finite sealed set (2 ≤ 2), firewall of 2 rows, density 0.468,
   edge law memoryless over four decades of τ. My criterion said it could not be chaotic; toy2d's table had its
   numbers (half the neighbourhood on a line, threshold fraction 0.38) and nobody ran it. Its boxes keep growing at
   0.11 per unit of side to side 81, the strip slope (R§3.3). Its 3D sibling on the six face-neighbours of the cubic
   lattice, also B2/S12, is a gump too (on one finished hull size).
2. Three dimensions is full of them: FCC, BCC, simple cubic (6 and 18), the 3D cross, the face lattice with 8, 12
   (face12e, R§2) or 18 neighbours. Two dimensions has the crosses (range 1, 2, 3; range 4 in slabs only), the
   honeycomb with 9 neighbours at B456/S3456 (concave wall law; F§1), and the plain kagome lattice with B2/S12 at
   b = 2 (R§2.4; a clean strip law once walls that freeze are censored, F§2), both of which the original table
   dismissed [the last two measured; one author].
3. The wall cap is exact: in every family the boundary goes from dying to immortal between c = K_f and c = K_f + 1.
   Reproduced for fcc (c = 9 → 10) and, out of sample, on face12e (c = 8 → 9) (R§3.2).
4. In 3D the face law barely notices the cap (gump: 0.212 and 0.216 for c = 6, 7, ln τ within 0.2 at five sizes,
   slopes 1.6 % apart, although the densities are 0.42 and 0.48, R§3.1; face12e 0.42, 0.41, 0.41 at c = 6, 7, 8 with
   wall densities 0.5 to 0.77, R§3.2); in 2D it depends on it strongly. I have no explanation.
5. A hole cut into a living cross2 edge closes at 0.94 cells per generation per end with diffusivity 0.84, so "one
   hole growing against the healing drift" would cost v/D = 1.1 per cell; the measured exponent is 0.42–0.44
   (`python3 gap.py cross2 3 5 128 16 80 12 0.5`). A face does not die that way — consistent with the notebook's
   "a dying face is a starved face". [not independently checked]
6. bond10 (withdrawn as first stated, R§1.3): it has no finite sealed set in the lattice, and finite sealed sets in
   slabs of 3 and 4 layers only, not "tubes through every slab"; what ends its 8-layer slab replicas other than a face
   death is a transverse firewall. Its b = 4 family, the one I studied, is one above its tight b = 3, at which it is
   confined to a box with six wall directions my analysis did not know it had, is chaotic at every cap 4…8, and has
   strong slab laws at two caps (R§2.4). So "the one chaotic in-reach rule that is not a gump" holds only for b = 4 in
   octahedral vessels.
7. (From the review and the notebook, 2026-11-14.) The neighbourhood the owner meant to write in 2012, face12e, is a
   gump in a box: the slip of 2012 changed the shape of the die, not the phenomenon. Its wall dies by the death of the
   layer beneath the sheet, at 0.205 per cell of that layer, against gump's 0.212 per face cell under the same rule.

## 9. Not checked / known weaknesses

- **Bulk classes rest on one soup density and 4096 generations.** "Dies"/"freezes" may hide a narrow chaotic basin
  (seen once: tristar3 c = 13 dies from ρ₀ = 0.50 but is chaotic from 0.65). The chaos windows of §5 are lower bounds.
- Slab laws use small periodic faces (A ≤ 81 cells in 3D; 2–5 sizes; two sizes only for cross4 c = 9–11, sc18,
  sc26, face18 c = 10–13, bcc8 c = 6, sc6 c = 4, 5), one face orientation per lattice (both for Moore), slabs 8
  layers deep in 3D. bcc8 and sc6 are uneven between odd and even widths (ln τ/A = 0.33, 0.30, 0.34 and
  0.37, 0.33, 0.36; sc6 c = 4 is *longer*-lived at A = 36 than at 49) — not understood, and it is why I give ranges.
  For several-type lattices the original slabs were direction-only (§3).
- Hull tests are 64 soups at 3–7 sizes with a cap of 10⁵–2×10⁵; several "gumps" rest on one finished size
  (sc6 c = 3, cross3d2 c = 5). No hull test for cross4 beyond side 25, sc18 c ≠ 10, face18, sc26 (including c = 18,
  19). The octahedral vessels of bond10 and face8 are not their hulls (§2).
- The weak laws (cross3 c = 6: 0.05 per cell to L = 160; Moore rows; hex12 c = 11: 0.03–0.04 to L = 96) are slightly
  concave; I cannot exclude a crossover to a sub-exponential law at larger sizes.
- Symmetric seeds, the straight tail to n = 1, the rate function: not touched for any new gump (nor for face12e).
- Theorems C2–C4, 1.7 and 1.8 are stated for one cell type; the face lattice has three (handled by computing the
  certificate per type; C2 also verified on gump's lattice, R§1.4); honeycomb and kagome families only through C1 and
  peeling.
- The validation run printed 60-generation populations of four test pairs before the predictions were committed
  (disclosed in PREDICTIONS.md). Git shows the predictions committed before the data; when the runs were made rests on
  untracked files, consistent with the stated order (R§3.4).
- I did not read Eppstein's proof or any primary source; no web access was used.
- **Not independently checked by the review** (R, "Not checked"): every 2D scan, the vn strip law, Moore rows, the
  weak laws, the O1/U1 rates of N4, the gap-healing test (§8.5), stages 2–5 of the scorecard, all hull runs except
  vn's, gump's at R = 4, 5 and fcc's at R = 3–5; the fw, m* and c_arm columns except for gump, fcc and face12e; the
  mean-field numbers and R₁; `thickness.md` and `threshold.md`. The completeness of the half-space scan (`seal.py`,
  |u_i| ≤ 5 in 3D, ≤ 8 in 2D) is argued, not proved; hex3's extra sealed directions grow with the bound. bond10 at
  b = 4: what makes its octahedra die in linear time. face12e: one cap in depth (c = 6), walls of 16–36 faces.
- **The follow-up (F) has one author** and its own "Not checked" list; only the face12e symmetric-box medians were
  re-derived (by the lead). In particular: kagome8 and hex9 tori at one size and four densities; hex9 c = 7 strips of
  one depth (2n + 7) and hulls of one shape with unequal sides; why hex9 c = 8 hulls show no permanent death while its
  strips do; kagome4's frozen-wall censor is a chosen rule (that frozen walls never thaw: 5 of 5 survivors static at
  10⁵) and its hexagons were not re-run; bond10's 4³ box lifetime rests on 4 deaths, its edge cost on columns of
  3 × 3, 3 × 4, 4 × 4, corners not isolated, 5³ boxes not run, the c = 6 slab law not re-measured; face12e's 7³ is a
  count of finishers, not a median; symmetric boxes at c = 6 only, one seed. The slab driver's ending classification
  (wall / deep firewall / cut / pit / periodic / frozen) has no independent implementation; the stepper `fu.c` was
  checked against numpy and the review's stepper for 100 generations on small vessels (`python3 fu.py validate`).

## 10. Open

1. **The chaos window** — why cross-r, FCC, BCC, SC are chaotic from c = b + 2 (or b + 1) up to and past K_f while
   star2, the triangular families and the 5×5 Moore are chaotic only above K_f. Theorem D says what must be present;
   nothing says when it is. The b/K ≤ 3/8 rule (23/27 here; §5 says 26 of 29 — the two counts were never reconciled)
   wants a reason; vn, kagome4 and hex9 (c = 7, b/K = 0.44) are the instructive exceptions.
2. **The slope.** What fixes I, why it is cap-independent on 3D plateaus (gump caps 6, 7 differ by 1.6 %), and what
   decides whether a wall starves; σ = K_f ρ/b is not that measure (§5 S2). Why face12e's dying layer costs 0.205 per
   cell, close to gump's 0.212.
3. **Hull strata.** A proof or measurement of "the cap must reach the edges and corners": gump c = 7 and fcc c = 7
   live 30–50× longer than c = 6 in octahedra with the same slab law; cross3 c = 9 and cross4 c = 12 freeze in boxes;
   bond10 at b = 3 has boxes far more robust than its periodic slabs (R§2.4).
   **The edge term of clause 6** [measured; one author, F§3]: what a box edge costs a dying wall, and why it is about
   0.9 nats for a gump octahedral face at A = 108, a factor ~2 in face12e's box lifetimes, and 0.52–0.66 nats per edge
   cube in bond10's columns, with corners (or several edges at once) costing more still in its 4³ box (≈ 10⁹ against
   2 × 10⁶ – 2 × 10⁷ for the first wall death from the column excess). No formula is proposed; the bond10 mechanism (dense edge rows in the band beneath the
   sheet) is described, not derived.
4. Is O1 ≈ 0.12 per cell per generation in every chaotic capped threshold a theorem?
5. The 2D gumps are now a family (range-r crosses, r = 1, 2, 3; hex9 B456/S3456; perhaps kagome4 B2/S12): the cleanest place to try
   M2–M4 is the range-1 member, B2/S12, with four neighbours.
6. **The converse of clause 1**: does an unconfined capped threshold have unbounded patterns? No proof, no
   counterexample (R§1.3).
7. **Walls that freeze without armour** (kagome4 B2/S12, F§2): what forms the static rows of density 2/3, whether they
   ever thaw, and whether any other rule does this; whether clause 3 can be stated so as to cover it.
8. **Under armour** (hex9 c = 8, F§1): the band beneath an immortal armoured band dies memorylessly in strips, but
   hulls showed no permanent death in 2 × 10⁶; why the two vessels differ.
9. **Concave wall laws** (hex9 c = 7: 0.69 → 0.53 per wall cell; also under armour at c = 8; gump's own local slopes
   drift, `research/STATUS.md`): whether the rate per cell tends to a limit, and what clause 5 should say beyond
   "roughly exponential".
10. **Symmetry** (face12e, F§4): why full cubic symmetry is fatal within tens of generations in face12e boxes when in
    gump a symmetric cube of side 13 still lives about 10⁵ (NOTEBOOK 2026-11-14, with the lead's untested
    conjecture: a symmetric box wall has only about n²/8 independent cells).

## Reproduce

```sh
cd research/theory/class
cc -O3 -march=native -o ../../scratch/class/gstep gstep.c -lm; cp ../../scratch/class/gstep ../../scratch/class/gstep_gap
python3 lattices.py; python3 validate.py; python3 confine.py; python3 energy.py selftest      # all "ALL OK"
python3 independent.py                                                                        # numpy-only re-check of vn and fcc
python3 theory.py table; python3 indices.py > data/indices.txt                                # §2 (no dynamics)
python3 pits.py bond10 4 4; python3 pits.py gump 4 2; python3 pits.py gump 4 3; python3 armour.py gump 4 6
python3 scan.py gump 4 --cs 5,6,7,8,9,10,11,12; python3 scan.py cross2 3; python3 scan.py moore 4   # training
./run2d.sh; ./run3d.sh                                    # test set -> scan2d.log, scan3d.log (first stated as ≈ 45 + 45 min on one core; the file times show about half that, R§3.4)
python3 follow.py stage4; python3 follow.py weak; python3 follow.py gump3; python3 follow.py hulls2d; python3 follow.py vn
python3 follow.py hulls3d fcc:4:6:3,4,5,6,7:0.42 bcc8:3:5:3,4,5,6:0.5 sc6:2:3:2,3,4,5:0.4      # (lattice:b:c:sizes:soup density)
python3 follow.py more3d; python3 gap.py cross2 3 5 128 16 80 12 0.5
python3 summarize.py scan > data/scan_table.md; python3 summarize.py laws > data/laws.md; python3 summarize.py faces > data/faces.tsv
```
Single runs: `python3 run.py bulk|face|life LATTICE b c [--n N --m M --R R --sec S --p P]`.

The review's numbers used in this revision (half-spaces, face12e, kagome4, bond10 at b = 3, recounts, re-measured
slab laws) are reproduced from `research/audit/class/` by the commands of its own Reproduce block, among them:

```sh
cd research/audit/class
python3 validate.py; python3 seal.py; python3 seal.py face12e                       # stepper check; sealing by half-space
python3 proofs.py c4; python3 proofs.py c2multi; python3 proofs.py bond10; python3 proofs.py energy
python3 proofs.py wallprop; python3 proofs.py armour
python3 face12e.py structure; python3 face12e.py confine; python3 face12e.py confine-others; python3 face12e.py bulk
./run_face12e.sh; ./run_measured.sh gump; ./run_measured.sh fcc; ./run_extra.sh; ./run_last.sh   # tens of minutes
python3 others.py kagome; python3 vnbox.py; python3 summary.py; python3 recount.py
python3 lead_check.py slab 4 4 8000 2048 1                                          # the lead's check of face12e's wall law
python3 lead_check_box.py sym N R [SEED]                                            # the lead's check of face12e's symmetric boxes
```

The follow-up's numbers (F) are reproduced from `research/theory/class/followup/` by its own Reproduce block, among
them (about 2.5 h of two cores in all):

```sh
cd research/theory/class/followup
python3 fu.py validate; python3 structure.py 2d; python3 structure.py bond10          # seconds
for L in kagome8 hex9; do for c in 5 6 7 8; do python3 two_d.py bulk $L $c; python3 two_d.py confine $L $c; done; done
./run_hex9.sh; ./run_hex9b.sh; ./run_kagome4b.sh; ./run_bond10.sh; ./run_face12e.sh
python3 box_hazard.py 3 1000000 4; python3 box_state.py 4 box; python3 box_state.py 4 column
python3 three_d.py box bond10 5 4 100000000 3 4096; python3 three_d.py box face12e 6 7 30000000 13 4096   # ~25, ~30 min
python3 analyse.py slab ../../../scratch/class_followup/FILE.jsonl [nwalls] [sizekey]; python3 analyse.py life FILE
```

## Changes in the revision of 2026-11-14

Each line names the review section (R§) or notebook entry that required it.

1. Head note "Reviewed … not yet revised" replaced by a dated revision line with pointers (task; R§5.2).
2. Added the names paragraph: gump is the rule as coded; face12e is the owner's intended 2012 neighbourhood and not gump (R preamble; NOTEBOOK 2026-11-14).
3. Summary's five-clause criterion replaced by the review's seven-clause statement, each clause tagged, keeping Cor. F's a⁰ − 1 count and Theorem D's reading (R§5.1).
4. Clause 1 / Theorem A: sealed half-spaces in place of sealed directions; Theorem A′ with its proof; the direction version kept as exact for one type; "iff" and "the hull is the polytope of those rays" dropped for several types (R§1.2, §5.2 item 1).
5. face12e hand counterexample added to §1.2 (R§1.2).
6. "Spanning" corrected to "positively spanning" in the summary and §2 (R§1.1).
7. Theorem A(v′): hull_b noted as not the smallest invariant polytope with several types (R§1.1).
8. Theorem B: position of the band matters with several types; face12e's three-layer band (R§1.1, §2.2).
9. C2: verified on gump's three-type lattice at b = 7 (R§1.4).
10. hex9's half-space tight b = 4 noted in §1.4 (R§1.2).
11. C4 reworded to "the cells of every layer", with the review's counterexample; Tukey-depth condition marked sufficient, not equivalent (R§1.3, §5.2 item 5).
12. C4 table: bond10 entry corrected to sealed sets at 3 and 4 layers only, none at 5, 6, 8; face12e column added (R§1.3, §2.2).
13. "bond10 is a counterexample to the converse of C2 for slabs" and "tubes through every slab" withdrawn; non-face endings are transverse firewalls (R§1.3, §5.2 item 2).
14. Theorem D: the review's independent re-check of both identities cited (R§1.4).
15. Theorem E: marked conditional; armour re-check cited; multi-type walls are bands, type-free form "armoured core empty" (R§1.3, §1.4, §2.4).
16. Cor. F: noted as one-type; kagome4 case where the printed form and the Theorem-E form disagree (R§2.4).
17. §2 table: rows for kagome4 (b = 2), kagome8 (b = 4), hex9 (b = 4), bond10 (tight b = 3, box; the b = 4 row kept as non-tight, octahedron ∩ box), face8 (octahedron ∩ box) corrected; face12e added; gump's row stated exact; run / not-run marked; unchecked columns tagged (R§1.2, §5.2 item 1, "Not checked").
18. §2 Checks: the review's position-aware confinement checks cited (R§1.2).
19. §3: slab method's multi-type caveat; the "≥ 20 deaths" condition of the fixed rule restored (R§1.2, §3.3).
20. §3: hull test reworded to a rate per unit of side compared with the slab slope; vn, cross2, cross3 c = 6, 7 rescored (cross3 c = 7 rate is arithmetic on the review's ratios) (R§3.3, §5.2 item 8).
21. §4.1 and summary: "identical slab face law" → equal within 0.2 in ln τ at five sizes, slopes 0.2121 and 0.2156, differing by 1.6 %; octahedron lifetimes re-measured (R§3.1, §5.2 item 9).
22. §4.2, §5 N4, chaos window, mean field, stages 2–5, gap test: tagged not independently checked (R "Not checked").
23. §4.3: cross2's box rate per unit of side noted (R§3.3).
24. N1: "necessary … an iff" → sufficient; necessity not proved (R§1.3, §5.2 item 6).
25. N3 / clause 3: tagged proved conditional + measured; restated as "no armoured set"; sc26 c = 18, 19 and bond10 c = 7 cited as data against the printed form; "38 walls" recount (60 scanned, 25 chaotic) added (R§1.3, §3.3, §5.2 item 3).
26. N3: fcc c = 10 and face12e c = 9 walls added (R§3.2).
27. S1: "46 of 50" → 42 by the fixed rule, the four low-death pairs and cross3 c = 8 named, cross3d2 c = 10 passes; "CV 0.83–1.23" corrected (R§3.3, §5.2 item 7).
28. S2 / clause 5: demoted to an observation; the review's analysis and a falsifiable form given (R§4, §5.2 item 4).
29. S3: one-finished-size and 8-death caveats; bond10 b = 4 qualified (R§3.3, §5.2 item 8).
30. Chaos window: face12e, bond10 at b = 3, kagome4 at b = 2 added; bond10's b = 4 entry qualified; 26/29 not recounted (R§2.4, §3.2, §1.2).
31. Ingredients table: bond10 rows qualified; cap row restated via Theorem E (R§1.2, §1.3).
32. §5 class statement superseded by the summary (R§5.1).
33. §6 table: fcc slope 0.19 → 0.181 ± 0.001, prediction still holds (R§3.1, §5.2 item 10); vn box re-run added; sc6 and cross3d2 one-finished-size noted; face8 8 deaths noted; face12e row added (R§2.2, §3.3).
34. §6: kagome4 B2/S12 and bond10 at b = 3 listed as rough candidates (R§2.4).
35. Scorecard: GUMP calls mechanical recount 4 / 6 vs 8 by judgment; "not a gump" caveats; tristar2 inconsistency; Stage 3 endings re-identified as transverse firewalls; fcc and Q1 entries corrected; scoring rule's wording change stated (R§3.3, §1.3, §3.1, §5.2 item 8).
36. "Honest reading": "three gumps" corrected to four (the original listed four) — editorial, found in this revision.
37. §7: kagome4 and face12e notes (R§2.4, §3.2).
38. §8.2: "two dimensions has only the crosses" → adds kagome4 B2/S12 as a candidate; face12e added to 3D (R§2.4, §5.2 item 11).
39. §8.3, §8.4: out-of-sample confirmations and the 1.6 % qualification (R§3.1, §3.2).
40. §8.6 rewritten (R§1.3, §2.4); §8.7 added (R§2; NOTEBOOK 2026-11-14).
41. §9: review's not-checked list added; git-order finding (R§3.4, "Not checked").
42. §10: converse of clause 1 added; 23/27 vs 26/29 inconsistency flagged; face12e and bond10 b = 3 questions (R§1.3, §2.4).
43. Reproduce block: "≈ 45 + 45 min" corrected to about half by the file times; the review's commands added (R§3.4, §5.2 item 12).

Review items not applied: none. Two things neither the review nor the original resolves: the b/K ≤ 3/8 tally is
"26 of 29" in §5 and "23/27" in §10 of the original; and R§5.1 clause 5 names as exceptions only eroding walls and
glassy bulks, while by its own recount (R§3.3) the fixed rule also fails four pairs on too few deaths and cross3 c = 8
on its CV.

## Changes in the second revision of 2026-11-14

Each line names the section of `research/theory/class/followup/OUTCOMES.md` (F) that required it; "W" is its section
"Where the revised class statement is wrong or silent", "NC" its "Not checked".

1. Head line added; F results tagged [measured; one author] except the face12e symmetric-box medians, re-derived by the lead (F§4(b); `research/audit/class/lead_check_box.py`).
2. Clause 1: out-of-sample confinement on kagome8 and hex9 at b = 4, 0 escapes in 1,536 soups, where the direction-only version predicted none (F scorecard P1.1, §1, W5).
3. Clause 3: two observed cases outside the clause, tagged measured — kagome4 walls that freeze without a Theorem-E set (27–44 % of the wall-death rate), hex9 c = 8 chaos peeling beneath an immortal armoured band in strips, no death in hulls (F§1, §2, W2, W3).
4. Clause 5: "exponential in the wall's area" → "roughly exponential"; hex9 B456/S3456 added with its concave rate (0.69 → 0.53); kagome4 0.772 ± 0.003 per wall-row cell (frozen walls censored); bond10 B34/S234 slab slope 0.492 ± 0.001; kagome4 and bond10 B34/S234 removed from the "more roughly" list, B345/S2345 kept there (F§1–§3, W4).
5. Clause 6 restated: lifetimes grow everywhere run, but follow the slab wall law only in some vessels (gump octahedra approximately, with the 0.8–0.9-nat rim term at A = 108 from `research/gpu/`; fcc; face12e boxes to 7³; vn), not in bond10 B34/S234 boxes (4³ ≈ 10⁹ against 600–1,500; columns 24–196×; dense edge rows beneath the sheet); an edge term is needed and not understood; no formula given (F§3, §4(a), W1).
6. Summary "new gumps": face12e 7³ and symmetric boxes; hex9 B456/S3456 added; kagome4 and bond10 b = 3 candidates updated (F§1–§4, W7).
7. Summary scorecard paragraph: the twelve follow-up forecasts and their outcomes (F scorecard).
8. §1.4: hex9 and kagome8 structure at b = 4 (no certificate, no finite sealed set found) and the absence of pits on hex9 strips; "no rule was run on hex9 or kagome8" removed (F§1, W5; `PREDICTIONS.md` "Exact facts").
9. §2 table: kagome8 and hex9 rows filled (sealed positions, wall-layer degrees, Theorem-E reach 5–7, c_arm 8); kagome4 c_arm; bond10 tight-b c_arm 6 (boxes); note below the table: "Not run: kagome8 and hex9" replaced by what was run, with their torus results and bond10's box degrees and armour (F§1, §3; `PREDICTIONS.md` "Exact facts").
10. §5 N3: hex9 c = 8 and bond10 c = 6 armour confirmed out of sample; the two cases outside clause 3 cross-referenced (F§1, §3, scorecard P1.4, P3.2).
11. §5 S3: the slab law does not carry over to bond10 boxes at b = 3 although its cap reaches every degree there; carries over to face12e 7³ (F§3, §4(a)).
12. §5 chaos window and ingredients table: kagome8 (no chaotic cap in reach, as the rule expects) and hex9 c = 7 (b/K = 0.44) as a further exception to b/K ≤ 3/8 (F§1, W6).
13. §6: hex9 B456/S3456 row added to the new-gumps table; face12e row extended with 7³; follow-up paragraph on kagome4 (frozen walls, clean law) and bond10 at b = 3 (slab, columns, boxes, c = 6); table of face12e O_h-symmetric box medians 4³ … 12³ with the lead's independent medians (F§2, §3, §4).
14. §6 scorecard table: six rows for the follow-up forecasts (F scorecard).
15. §8.2: hex9 B456/S3456 added to 2D; kagome4's "transverse cuts not censored" replaced by the frozen-wall finding (F§1, §2).
16. §9: stale "kagome8 and hex9 not run", "whether bond10's 4³ boxes ever die" and "face12e boxes to 6³" removed; F's own not-checked list summarised (F NC).
17. §10: item 1 adds hex9 as an exception; item 3 adds the edge term; item 5 adds hex9; new items 7–10 (frozen walls, under armour, concave laws, symmetry) (F W1–W4, §4(b)).
18. Reproduce: the lead's box check and the follow-up's commands added (F "Reproduce").

Items of the brief not applied: none.

Inconsistencies found and not resolved:

- **Count of exceptions to b/K ≤ 3/8.** F (§1, W6) calls hex9 c = 7 the *third* exception, "after vn and kagome4".
  §5 of this document lists the original exceptions as vn, bond10 (its b = 4 family) and sc26 (barely), and then adds
  kagome4; by that list hex9 is the fourth or fifth, depending on whether bond10 and sc26 still count. §5 above quotes
  the follow-up's count without adopting it; neither count is chosen, and the 26/29 vs 23/27 discrepancy noted in the
  first revision is still open.
- **Under-armour deaths and "no wall death".** F's method counts as a wall death any whole parallel layer within
  depth 3 of a 2D wall, and in its §1 the deaths of the pair beneath hex9's armoured band are such events; yet its
  scorecard scores P1.4 ("c = 8 armour: no wall death") as holding. Whether P1.4 meant the armoured band only is not
  stated; this document reports the band's immortality and the deaths beneath it separately.
- **face12e symmetric medians.** The follow-up's 9, 9.5, 19 at 5³, 6³, 8³ and the lead's 7.5, 8, 18 differ by
  1–1.5 generations (within the quartiles). Whether the two use the same definition of lifetime (the lead's is the
  exact transient length) was not checked; hence the shortening at 6³ is 74,000× by the follow-up's median and
  88,000× by the lead's.
