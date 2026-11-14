# Review of `research/theory/class.md` (the class of "gumps")

*Adversarial check by a second agent, 2026-11-14. Scripts: `research/audit/class/` (run commands from there); bulk
output: `research/scratch/audit-class/`. Tags: **[proved]** (argument given or re-derived here), **[computed]** (exact
finite computation), **[measured]** (sample size, error, command). All dynamics below was run with a stepper written
for this review (`aud.c`, 64 bit-sliced replicas on a cell graph; `aud.py`, lattices and vessels) that shares no code
with `research/theory/class/`. `python3 validate.py` → ALL OK: bit-exact against `reference/oracle.py` on gump (64
soups × 40 generations on two tori; the golden side-8 log to its final 384; an octahedral vessel against the oracle
in free space) before any offset was changed, then against naive numpy rolls for face12e, fcc, cross2 and vn.*

*Names. **gump** is the rule as coded in 2012 (coplanar neighbours touch at a corner). **face12e** is the same cells
with the four coplanar neighbours that share an edge. face12e is not gump and nothing below about it is a statement
about gump.*

## Verdict

| part | verdict |
|---|---|
| 1. Proofs | Theorems A–G hold as stated, with three exceptions. (a) Being sealed is a property of a **half-space** (direction and position of the plane), not of a direction, as soon as there are several cell types; clause 1's "proved iff; the hull is the polytope of those rays" is false, and six rows of the lattice table are wrong or incomplete. Gump's own row is unaffected. (b) C4 is wrong as worded (the code computes the right thing). (c) Clause 3 is tagged "proved"; what is proved is conditional, the rest is measured, and the document's own data contradict half of it. |
| 2. face12e | The criterion as written says: no sealed direction at b = 4, not confined, not a gump. In fact [proved + measured]: confined to a box, chaotic on the torus (ρ = 0.398), walls die two sheets at a time after a memoryless wait with ln τ = 6.43 → 14.54 for 16 → 36 wall faces, box lifetimes 10, 60, 439, 9,855, 707,038 for 2³ … 6³ cubes, ending in sparse debris. It passes all three of class.md's tests. The lead's quick look is right on every point it makes. |
| 3. Measured claims | Reproduced: gump caps 6 and 7 slab laws (my ln τ within 0.02 of the author's at four sizes each), walls at K_f + 1, the "38 walls", "14 of 15", the git order of predictions and data. Not reproduced as stated: "identical" (the two laws differ by 2 % in slope, significantly); fcc slope "0.19" (0.181 ± 0.001; the 0.19 leans on one size below the burn-in); "46 of 50" (42 by the scoring rule that was fixed in advance); "8 / 6 / 14" (needs case-by-case judgment: the hull rule depends on an arbitrary size step and by its letter fails cross2, the project's 2D gump). |
| 4. Clause 5 | A threshold drawn between two eroding cases and four weak ones, with two exceptions on the wrong side already in the author's table. On face12e it gives the wrong call or the right one depending on which layer's degree is called K_f. Not a criterion. |
| 5. The class | What can be signed is a list of proved necessary-in-practice structure (sealed half-spaces, no finite sealed set, no armour, two-sided drive) plus a measured regularity (chaotic bulk ⇒ whole-wall memoryless death: 42 of the author's 50 pairs by the rule he fixed in advance, and face12e). No clause predicts chaos or the strength of the law, and "is a gump" is not sharply defined for weak laws. |

**The single most important correction:** replace sealed *directions* by sealed *half-spaces* in Theorem A, clause 1
and the table (§1.2). It is what makes the criterion miss face12e, mis-row bond10, face8 and three 2D lattices, and
it removes the "iff".

## 1. The proofs

### 1.1 Statement by statement

| statement in class.md | verdict | note |
|---|---|---|
| A(i) sealed direction ⇒ confinement | holds | |
| A(ii) c(u) ≥ b ⇒ a birth outside for *some* C | holds | the quantifier is "some C"; see §1.2 |
| "u is sealed iff c(u) ≤ b − 1" | holds, with sealed meaning "for every C" | |
| A(iii) specialisation, rays | holds | |
| A(iv) one type: a⁰ ≥ K − 2b + 2 | holds | |
| A(v) hull | the inclusion holds; "the hull **is** the polytope of those rays", and N1 "necessary … an iff", **fail** for several types | §1.2 |
| B firewalls | holds (one type). With several types the position of the band matters | §2.2 |
| C sealed sets, C1 | hold | |
| C2 dichotomy b ≤ K/2 | holds (one type). Also true on gump's three-type lattice [computed] | §1.4 |
| C3 | holds | |
| C4 slabs | **fails as worded**; holds with "every layer" in place of "the far face" | §1.3 |
| C4 table, bond10 "pierced in a slab of any thickness I tried" | not supported: 3 and 4 layers only | §1.3 |
| C5 | holds | |
| D two-sided threshold lemma | holds; both identities re-checked with my own code | §1.4 |
| E armour, corollary (walls) | hold, as conditionals ("once fully alive") | |
| F reach of caps | holds (one type, tight b) | |
| G no shielded region | holds | |
| Summary clause 3 "[proved]", §5 N3 "proved necessary" | **overstated** | §1.3 |

### 1.2 Sealing belongs to a half-space, not to a direction

**The question.** Is being sealed a property of a direction alone, or of a direction together with the position of
the plane, once there is more than one cell type? **Of the direction and the position.** With one type they
coincide; with several they do not, and the criterion's first clause does not survive as written.

**Theorem A′ [proved].** For a half-space H = {u·p ≤ C} let c(H) = max over cells p ∉ H of |N(p) ∩ H|.
(i) If c(H) ≤ b − 1, the outside of H, once dead, stays dead (any rule with minimum birth count ≥ b).
(ii) If c(H) ≥ b, some configuration inside H has a birth outside H. So **H is sealed iff c(H) ≤ b − 1**.
(iii) c(H) ≤ c(u) = max over types of a⁻_u, with equality whenever a cell of a type attaining the maximum lies on the
first layer beyond the plane. With one cell type that is every C, so c(H) = c(u) and class.md's Theorem A is exact.
(iv) With several types and u rational, a type that is absent from the first layers beyond the plane contributes
only its offsets that reach back far enough: c(H) = max over types τ of #{o ∈ O_τ : u·o ≤ −d_τ}, d_τ the distance
from the plane to the first layer holding τ. This can be smaller than c(u).
(v) A finite pattern stays in the intersection of all sealed half-spaces that contain it, and that set never grows.
It is bounded for every finite pattern iff the normals of the sealed half-spaces positively span.

*Proof.* (i), (ii): class.md's proof of A(i), A(ii) with a⁻_u(p) replaced by |N(p) ∩ H|. (iii): a neighbour of p in H
has u·o < 0, so |N(p) ∩ H| ≤ a⁻_u(p); if p is on the first layer beyond the plane every neighbour with u·o < 0 is in
H. One type means every layer holds a translate of every cell. (iv) is (iii) read type by type; the first layer of a
type is its worst. (v) as A(v); sealed positions of a rational direction repeat periodically, so they exist
arbitrarily far out. ∎

Class.md's c(u) is the maximum of c(H) over C. Its A(ii) is true and says exactly this ("there *are* C …"); the
error is the step from there to "the hull is the polytope of the sealed directions" and to "necessary".

**Counterexample to clause 1 as written, checkable by hand: face12e, b = 4.** Layers along x alternate: odd x
holds only faces with normal x, even x only faces with normal y or z. Offsets of an x-face: (±1, ±1, 0), (±1, 0, ±1),
(0, ±2, 0), (0, 0, ±2); of a y-face: (±1, ±1, 0), (0, ±1, ±1), (±2, 0, 0), (0, 0, ±2).

- c(u) for u = (1, 0, 0): an x-face has 4 offsets with negative x. So c(u) = 4 = b: not a sealed direction. The
  same count gives 4 for body diagonals and 6 for face diagonals. No direction is sealed (`theory.sealed_rays` would
  be empty; the table would print tight b = 5).
- Plane at odd C: the first layer outside, x = C + 1, holds y- and z-faces: 2 neighbours at x = C, 1 at x = C − 1,
  total 3. The next, x = C + 2, holds x-faces, whose neighbours are at x = C + 1, C + 2, C + 3: none inside.
  c(H) = 3: **sealed**.
- Plane at even C: an x-face at C + 1 has 4 neighbours at x = C. Not sealed.

So every finite pattern of face12e B45/S345 stays in a box, although the criterion says it is unconfined.

**Every lattice of the table, re-examined** [computed: `python3 seal.py`; every primitive direction with |u_i| ≤ 5
in 3D, ≤ 8 in 2D, every plane position; `python3 seal.py LATTICE` for detail]. My direction-only numbers
(K, b, a⁰, a⁻, K_f) agree with class.md's table in all 25 rows that print them.

| lattice | types | class.md (directions) | half-spaces | consequence |
|---|---|---|---|---|
| all 20 one-type lattices | 1 | | identical | none, as (iii) requires |
| **gump** | 3 | b = 4, 8 diagonals | identical | none: every diagonal layer holds all three types, and no plane of any other scanned direction is sealed at any position |
| face18, kagome6, hex12 | 3, 3, 2 | b = 6, 3, 6 | identical | none |
| **face12e** (not in the table) | 3 | no sealed direction at b = 4; tight b = 5 | **b = 4**: 6 axis directions, plane through a sheet of face centres | confined to a box at b = 4 |
| **bond10** | 3 | b = 4, octahedron | **b = 3**: 6 axis directions, same planes, c(H) = 2 | tight b is 3, not 4; at b = 4 the hull is octahedron ∩ box |
| **face8** | 3 | b = 3, octahedron | b = 3, the 8 diagonals **and** 6 axis directions (c(H) = 2) | hull is octahedron ∩ box |
| **kagome4** | 3 | b = 3, every direction (convex hull); "finite sealed sets" | **b = 2**: 6 directions, plane just outside a sparse row | B2/S12 is confined and unsealable; the table dismisses the lattice |
| **kagome8** | 3 | b = 5; "finite sealed sets" | **b = 4**: 12 directions | same |
| **hex9** | 2 | b = 5; "finite sealed sets" | **b = 4**: 6 directions | same |
| hex3 | 2 | b = 2, 6 directions | b = 2, many more directions at particular positions | not pursued |

**Checked by dynamics** [measured; 64 soups of density 0.5 per seed, five seed cubes or three seed squares, free
space, 200–300 generations]:

| rule | soup-generations with a live cell outside the position-aware hull | outside class.md's hull | command |
|---|---|---|---|
| face12e B45/S345 | 0 of 64,000 outside the odd box | class.md has no hull; 40,891 outside the diagonal hull, 37,995 outside the tight bounding box | `python3 face12e.py confine` |
| gump B45/S345 (control) | 0 outside the diagonal hull | 44,580 outside the odd box | same |
| bond10 B45/S345 | 0 outside the odd box, 0 outside the diagonal hull | the box is not in class.md | `python3 face12e.py confine-others` |
| face8 B34/S234 | 0 and 0 | the box is not in class.md | same |
| kagome4 B2/S12 | 0 of 57,600 outside the hexagon at sealed positions | class.md: b = 3 only | `python3 others.py kagome` |

A cube-shaped seed of bond10 B45/S345 or face8 B34/S234 never leaves its own cube; class.md's octahedron about that
cube is three times wider.

**What this does to class.md.**

1. Clause 1 is sufficient, not "iff", and "the hull is the polytope of those rays" is false for bond10 and face8
   (the hull is smaller) and for face12e, kagome4, kagome8, hex9 (a hull exists where the text says none, or one
   threshold lower).
2. The table's bond10 row (b = 4, a⁰ = 4, a⁻ = 3, K_f = 7, b/K = 0.40) is the row of a non-tight b. Everything
   class.md concludes from bond10 being the odd one out — "the one chaotic in-reach rule that is not a gump", the
   3/8 rule's "bond10 exception", "C2 has no converse for slabs" — is about a rule with six sealed wall directions
   the analysis did not know it had. Its periodic {111} slabs can be cut by axis firewalls (three layers: even, odd,
   even) and its octahedral hull vessels are not its hulls.
3. For several types a wall is a **band** of layers (between two consecutive sealed positions), not a layer, and
   "the face cell", a⁰, K_f and "reach" are not single numbers (face12e: sheet cells have degree 8, the layer beneath
   11; §2.2, §4).

### 1.3 Smaller corrections

**C4 is wrong as worded.** It says that in a slab of m layers one needs a v₀ with at least b − a⁰/2 projected inward
offsets of reach ≤ m − 1 strictly on each side, and calls m* the least m with such a certificate. That condition
looks at the two boundary layers only. *Counterexample* [computed, `python3 proofs.py c4`]: Z² with offsets (±1, 0),
(±2, 0), ±(1, 2), ±(−1, 2); K = 8, u = (0, 1), a⁰ = 4, a⁻ = 2, tight b = 3, b − a⁰/2 = 1. In a strip of m = 3 rows the
stated condition holds (the offsets (1, 2) and (−1, 2) lie on opposite sides of v₀ = (1, 0) and have reach 2 ≤ m − 1).
But the middle row has no neighbour in rows 1 and 3, and any interval of it is sealed: an end cell has 2 neighbours
outside, 2 ≤ b − 1. Peeling finds a 10-cell sealed interval at m = 3 and nothing at m = 4, 5. *Corrected statement:*
the forward count must be ≥ b for the cells of **every** layer, each with its own reach limits on both sides.
`theory.slab_certificate` does check every layer, so the m* row of the table is not affected. ("Tukey depth ≥ 1 for
every type" is sufficient for the half-in-plane case, not equivalent: what is needed is one v₀ that splits every
type's set.)

**N1 is not proved necessary for confinement, even with one type.** A(ii) exhibits one birth one step outside a
half-space. It does not exhibit a pattern that escapes every bounded region. I have no one-type counterexample; the
statement that is proved is "the half-space is not invariant".

**Clause 3 "[proved]" and N3 "proved necessary".** Proved (Theorem E): a set whose cells have ≥ b − 1 neighbours
inside it and vessel-degree ≤ c − 1 is immortal *once entirely alive*. That such a set becomes entirely alive from a
soup is measured (§3.2), not proved. And the clause as printed, "b + 1 ≤ c ≤ K_f … and c < c_arm", goes beyond
class.md's own data in two places. "c ≤ K_f" has no support when a⁰ < b − 1: sc26 at c = 18 and 19 (beyond K_f = 17;
a⁰ = 8 < 9, so no wall) has memoryless slab laws of 0.13 and 0.16 per cell, the second "strong" by the fixed
cutoff, and no hull was run. "c < c_arm" is contradicted: bond10 at c = 7 = c_arm has growing hull lifetimes
(1,152, 45,120, > 10⁵) and is scored as the one missed "not". The supportable clause is: *no armoured set forms*,
which for one type and a⁰ ≥ b − 1 reads c ≤ K_f in a slab.

**bond10 "tubes through every slab".** The author's own `pits.py bond10 4 M` gives a sealed set for M = 3 (380
cells) and M = 4 (402 cells) and **none** for M = 5, 6, 8 (patches of 988, 1,173, 1,514 cells). My construction
(the corner cut off by three axis planes at odd position, peeled; `python3 proofs.py bond10`) gives 1,176 cells in
a 4-layer slab, none in an 8-layer slab, none in a half-space. The slab runs were 8 layers deep. "A slab of any
thickness I tried" and §8.6 "finite sealed tubes through every slab" should read "slabs of 3 and 4 layers". What
does cut thicker slabs is the axis firewall of §1.2, which is not finite but wraps a periodic face.

### 1.4 On gump's own three-type lattice

Section 9 of class.md says C2–C4, F and G are stated for one type. For gump's lattice specifically:

- **A, hull:** exact as stated. Each type's offset set is centrally symmetric, all three types occur in every
  diagonal layer with the same histogram (1, 2, 6, 2, 1), and `seal.py` finds no sealed plane at any position in any
  other scanned direction [computed].
- **B:** verbatim (same histogram for each type): three layers.
- **C2:** "no finite sealed set iff b ≤ K/2 = 6" holds [b ≤ 6: C1, generic forward count 6 for each type; b = 7:
  a 30-cell sealed set inside a cube of radius 2, 1,380 of the 1,386 cells of an L1 ball; `python3 proofs.py c2multi`].
- **D:** needs no lattice. Both energy identities hold exactly at every one of 58 steps on 12 vessels (gump caps 6
  and 7, face12e, fcc, cross2, vn; torus and box), and the cells that deviate from the two pure threshold rules are
  exactly the overcrowded and undercrowded ones (`python3 proofs.py energy` → ALL OK).
- **E, c_arm:** gump and fcc octahedra of 6 layers have armoured cores from c = 8 (54 and 30 cells), none at 6, 7;
  the 120 cells of vessel-degree 7 are there (`python3 proofs.py armour`).
- **F, G:** per type the numbers are those of a one-type lattice with K = 12, a⁰ = 6; G's hypothesis fails for gump
  (c = K/2), as class.md says.

## 2. face12e

Cells as gump. A face with normal a and in-plane axes b, c has neighbours ±e_a ± e_b, ±e_a ± e_c (8, as gump) and
±2e_b, ±2e_c (4, in place of gump's ±2e_b ± 2e_c). Rule B45/S345, i.e. (b, c) = (4, 6).

### 2.1 The prediction, committed before any run

`PREDICTION-face12e.md`, commit bcb8122, written from class.md's text and `theory.py` by hand before anything was
run on this lattice and before reading the lead's branch. Disclosed there: `docs/AUTOMATON.md` §2 already carries
the sentence "the hull is a box, not an octahedron", which I had read.

| | the criterion as written (part A of the file) | my own derivation (part B) | outcome |
|---|---|---|---|
| sealed directions at b = 4 | none: c(u) = 4, 4, 6 for axes, body diagonals, face diagonals | half-spaces {x ≤ C}, C odd, are sealed | part B: 0 escapes from the odd box in 64,000 soup-generations |
| hull | the whole space; "not confined" | the box with walls at odd coordinates | box |
| gump or not | **not** (clause 1 fails; clauses 3 and 5 undefined) | — | passes all three tests (§2.2) |
| permanent death | — | two layers at a time; firewall of three layers (even, odd, even) | confirmed [computed + measured] |
| finite sealed sets | — | none in a slab one cube thick; critical thickness one cube | confirmed [computed] |
| reach | — | wall cell degree 8, caps 5…8; wall immortal from c = 9; no armour at c = 6, 7 | c = 9 exact [measured]; **wrong for the 2³ box at c = 7**, where all 24 wall cells form an armoured core (irrelevant at c = 6) |
| torus | "not predicted"; 3/8 rule says chaotic | chaotic, ρ = 0.39–0.42 | chaotic, ρ = 0.398 |
| clause 5 | undefined | σ = 2ρ = 0.78–0.84 < 0.85: "starved or weak" | σ = 0.80; wall not starved, law not weak (§4) |

`theory.py` itself was not run on face12e; `seal.py`, written independently, reproduces the hand counts.

### 2.2 What face12e does

**Structure** [computed, `python3 face12e.py structure`].

| | |
|---|---|
| most neighbours inside {u·p ≤ C} of a cell outside, C = 0, 1, 2, 3 | u = (1,0,0): 4, **3**, 4, **3**; (1,1,1): 4, 4, 4, 4; (1,1,0): 4, 6, 4, 6. (gump: 4, 4, 4, 4; **3, 3, 3, 3**; 5, 5, 5, 5) |
| bands of x-layers sealed for b = 4 | (even, odd, even) only. One, two or four layers, or three starting on a sheet of x-faces, are not |
| at a wall | the wall sheet alone is not sealed (each cell has 4 neighbours beneath); sheet + layer beneath is; three layers are not, four are |
| a filled closed cube | every cell has ≥ 6 live neighbours: dead after one generation (2³, 3³, 5³ cubes) |
| finite sealed sets | single sheet: yes (it is the von Neumann lattice with b = 4 > K/2). Slab one cube thick (odd, even, odd) and thicker: none in an 8 × 8 patch; forward count 4 ≥ b for every cell |
| box of n³ cubes, 3n²(n + 1) cells | vessel degrees 6 (corners of walls), 7 (edges), 8 (wall faces), 10, 11, 12 (inside) |
| armoured core (Theorem E) | none at c = 6 for n = 2, 3, 4; at c = 7 for n = 2 only (24 cells); from c = 8 for n = 3, 4 (48, 72 cells along the box edges) |
| a fully live wall sheet | broken in 64/64 soups at c = 7 and c = 8, in 0/64 at c = 9 and c = 10 (`python3 proofs.py wallprop`): the wall cap is K_f + 1 = 9 with K_f = 8 |

**Torus** [measured, `python3 face12e.py bulk`]: 10³ cubes (3,000 cells), 64 soups per starting density, 4,096
generations. From density 0.25, 0.35, 0.45, 0.55 all 64 soups are still aperiodic, ρ = 0.397–0.400, 47.7 % of cells
differ from two generations before; from 0.15, ρ = 0.382; from 0.70, 63 of 64 soups collapse (mean density 0.0075).
Gump, same test: ρ =
0.415–0.418, activity 45.5 %.

**Walls die whole, two sheets at a time, after a memoryless wait** [measured, `./run_face12e.sh`,
`python3 summary.py`]. Slab of 4 cubes (9 layers) between two odd walls, periodic face of A cube faces, soups of
density 0.45, 200-generation burn-in, a replica ends when a wall sheet and the layer beneath it are empty together
(that state is sealed), τ = 2 × exposure / deaths:

| A (wall faces) | deaths | ln τ | CV of the wait | τ by age of the replica (bins with ≥ 30 deaths) | density: interior / wall sheet / layer beneath |
|---|---|---|---|---|---|
| 16 (4 × 4) | 213,762 | 6.428 ± 0.002 | 1.001 | 608 … 686 | 0.391 / 0.494 / 0.404 |
| 20 (4 × 5) | 75,036 | 7.999 ± 0.004 | 0.999 | 2,818 … 4,102 | 0.394 / 0.502 / 0.406 |
| 25 (5 × 5) | 19,063 | 10.183 ± 0.007 | 0.998 | 24,924 … 31,433 | 0.397 / 0.516 / 0.410 |
| 30 (5 × 6) | 4,306 | 12.089 ± 0.015 | 0.983 | 165,846 … 203,821 | 0.397 / 0.517 / 0.410 |
| 36 (6 × 6) | 619 | 14.542 ± 0.040 | 0.991 | 1.82 × 10⁶ … 2.41 × 10⁶ | 0.397 / 0.520 / 0.411 |

Slope 0.410 ± 0.001 per wall face (successive intervals 0.39, 0.44, 0.38, 0.41). Six cubes deep instead of four,
A = 25: 10.235 ± 0.011 (0.05 higher).

- *Which layer dies.* The wall sheet alone is empty far more often and comes back: first emptiness of the sheet has
  ln τ = 5.03 (A = 16) and 7.87 (A = 25), 4 and 10 times more frequent than a permanent death. First emptiness of
  the layer beneath alone has ln τ = 6.39 and 10.18, the same as the permanent death. **The event that kills a wall
  is the death of the layer of y/z-faces beneath the sheet.** That layer has 2A cells with 6 in-layer neighbours, 2
  one layer in and 1 two layers in — the counts of a gump face cell (fcc: 6 and 3) — and per cell of it the slope
  is 0.205 (gump 0.212, fcc 0.181, both B45/S345).
- *Transverse cuts.* [[CUTS]]

**Boxes** [measured, `python3 face12e.py life n cap`, 64 soups, density 0.45; lifetime = first t with
x(t) = x(t + 2)]:

| box | cells | median lifetime (quartiles) | final density | empty endings |
|---|---|---|---|---|
| 2³ | 36 | 10 (6 – 13) | 0.127 | 34/64 |
| 3³ | 108 | 60 (38 – 100) | 0.084 | 28/64 |
| 4³ | 240 | 439 (279 – 594) | 0.042 | 21/64 |
| 5³ | 450 | 9,855 (6,159 – 17,848) | 0.017 | 26/64 |
| 6³ | 756 | 707,038 (471,287 – 1,477,905) | 0.010 | 25/64 |
| 7³ | 1,176 | none of 64 finished in 300,000 | | |

Ratios 6.0, 7.3, 22, 72: faster than exponential in the side, as a wait exponential in the wall area requires
(ln of the ratio over the increase of n²: 0.36, 0.28, 0.35, 0.39).

**How a box dies** [measured, `python3 face12e.py layers 5 80000`]: [[LAYERS]]

By class.md's operational definition (bulk chaos ∧ face law with CV in [0.8, 1.25] ∧ hull lifetimes growing by more
than e per size step, runs ending) face12e B45/S345 is a gump, *strong* (slope ≥ 0.15) however the face is counted.

### 2.3 Against the lead's quick look

Read after the above: `git show origin/claude/edge-neighbour-tangent:research/tangents/edge-neighbours/README.md`
and `edge.py` (same offsets as mine). Not checked out, not merged.

| lead's statement | mine | |
|---|---|---|
| diagonal layers hold 4, 4, 4: no octahedron | a⁻ = a⁰ = a⁺ = 4 for every type; 40,891 soup-generations outside the diagonal hull | agree |
| axis plane at odd c: a face at c + 1 sees ≤ 2 + 1, at c + 2 none; pattern stays in its box closed at the next odd plane (16 soups, 400 generations) | same count; 0 escapes in 320 soups × 200 generations; 37,995 soup-generations outside the tight box | agree |
| a filled closed cube dies in one generation | every cell of a closed box has ≥ 6 = c live neighbours; closed cubes of 2³, 3³, 5³ → 0 alive after one step | agree |
| torus density about 0.40 from 0.15, 0.3, 0.5; collapse from 0.7 | 0.397–0.400 from 0.25–0.55 (0.382 from 0.15); 63/64 collapse from 0.7 | agree |
| boxes: 4³ median about 500 (450–770), 5³ 8,700 (5,800–15,100), 6³ none in 60,000, 7³ none in 40,000; resolution 256, density 0.4 | 439 (279–594), 9,855 (6,159–17,848), 707,038, none in 300,000; exact settling time, density 0.45 | agree within the lead's resolution and sample |
| it dies a slab at a time (population plateaus 193, 156, 120 in 5³) | [[LAYERS-SHORT]] | agree |
| "the live-box read-out flickers at even coordinates" | explained: the wall sheet alone empties 4–10 times as often as a wall dies, and comes back | agree |
| not looked at: memoryless? cost per cell? firewall? debris? | memoryless (CV 0.98–1.00, flat hazard over 2¹¹ in age); 0.41 per wall face; three layers (even, odd, even); debris of density 0.01–0.02, 40 % of endings empty | new |
| "both rules are gumps" | yes, by class.md's three tests | agree |

No disagreement. Not looked at by either of us: symmetric seeds, the tail of the lifetime law beyond 6³.

### 2.4 What face12e does to the criterion

**As written it is called wrongly**: clause 1 fails (no sealed direction), so "not confined, not a gump".

**The smallest change** that calls face12e and keeps every existing call:

1. Clause 1: *a positively spanning family of sealed half-spaces, c(H) ≤ b − 1* (Theorem A′). For one type this is
   the old clause. The hull is the intersection of the sealed half-spaces.
2. Clauses 3 and 5 refer to "the face cell" and K_f = K − a⁻. With several types a wall is a band of layers. Clause
   3 has a type-free form already in the document: *Theorem E's armoured core is empty*. For face12e that gives
   caps 5…8 and a wall from c = 9, as measured. Clause 5 has no type-free form (§4).

With that change, every one-type lattice, gump, face18, kagome6 and hex12 are called exactly as before. Four table
rows acquire a smaller tight b and with it rules that class.md never ran: **bond10 at b = 3, kagome4 at b = 2,
kagome8 and hex9 at b = 4**. So "calls every lattice in the table correctly" cannot be claimed for the changed
criterion without running those. I ran two, with the predictions committed first (`PREDICTION-repaired.md`,
commit 1a32ea9):

**kagome4 at b = 2** (the plain kagome lattice, K = 4; the table says "finite sealed sets (b exceeds the generic
forward count)" and the scan ran it at b = 3 only, where it freezes). `python3 others.py kagome`,
`others.py kagome slab n gens`, `others.py kagome life R cap`:

| | predicted | outcome |
|---|---|---|
| confinement | exact: hexagon at six sealed lines | 0 of 57,600 soup-generations outside it; 39,576 outside the tight hexagon; 49,683 beyond the seed's support in other directions |
| finite sealed sets | none (forward count 2 = b) | [proved by C1] |
| permanent edge death | two rows (sparse wall row + dense row) | the wall row alone empties with ln τ = 5.85, 6.17 at n = 6, 10 wall cells and comes back; the two rows together: below |
| B2/S12 on the torus | my guess: chaotic (class.md's 3/8 rule: no) | chaotic: 64/64 soups aperiodic at 4,096 from every density tried, ρ = 0.482, activity 0.39 |
| B23/S123 on the torus | — | not chaotic (freezes at density 0.71) |
| strip law, B2/S12, 17 rows deep | my guess: a law | ln τ = 7.24, 8.77, 10.27, 11.59, 12.85 ± 0.04 at n = 4, 6, 8, 10, 12 wall-row cells: 0.77 → 0.63 per wall cell; CV 1.00, 1.04, 1.07, 1.12, 1.23 |
| hexagons R = 2 … 10 | — | medians 67, 460, 1,028, 2,571, then ≤ 8,195, ≤ 16,387, ≤ 32,771 (R = 6, 7, 8), ≤ 131,075 (R = 10): about × 2 per unit of R, the strip rate; final density 0.31 → 0.04 |

So the plain kagome lattice carries a rule with all three signatures, on a lattice the table excludes; "two
dimensions has only the crosses" (§8.2) needs it added or tested away. Caveats: my strip runs do not censor
transverse cuts, which are finite in 2D (settled replicas are 20–50 % as many as the deaths from n = 6 on, and the CV
drifts to the edge of the accepted range); the hexagon endings from R = 6 on are long-period oscillators found by
snapshot at powers of two, so those medians are upper bounds within a factor 2. By clause 3 as printed the cap is
out of reach of this wall (the wall-row cell has degree 2 < c = 3, and a⁰ = 0); by the Theorem-E form it is fine.

**bond10 at b = 3** (the table has b = 4). `python3 others.py bond10 [slab|life …]`:

| | predicted | outcome |
|---|---|---|
| confinement | exact: box with odd walls; leaves the diagonal hull | 0 of 64,000 soup-generations outside the box; 52,925 outside the diagonal hull |
| torus | my guess: chaotic at some cap ≤ 6 | chaotic at every cap 4 … 8: ρ = 0.286 (B3/S23, half the soups die from density 0.5), 0.400 (B34/S234), 0.475, 0.546, 0.635 |
| slab (4 cubes deep, wall + layer beneath) | — | B34/S234: ln τ = 8.04 ± 0.01, 12.71 ± 0.07 at 16, 25 wall faces, no death at 36 in 3.2 × 10⁷ replica-generations; CV 1.00, 0.92. B345/S2345: 7.78, 12.23 ± 0.06, 17.97 (one death); CV 1.00, 1.01 |
| boxes n = 2 … 5 | my guess: growing | B34/S234: 5, 262, then **none of 64 finished in 300,000** at n = 4 and n = 5 (at n = 4 no wall has died after 20,000 generations in any soup, although a periodic wall of the same area waits 3,100). B345/S2345: 5, 15, 2,053, unfinished; endings dense (0.54–0.65) |

At its real tight b, bond10 has strong slab laws (0.5 per wall face) at two chaotic caps. Its boxes are far more
robust than its periodic slabs: the sheets of adjacent walls interlock along the box edges (each wall-sheet cell
has all its neighbours beneath, and at an edge those belong to the next wall's sheet). Whether B34/S234 in a box
of 4³ ever dies I do not know. So the changed criterion is not shown to call bond10 correctly; what is shown is
that class.md's bond10 conclusions concern b = 4, one above tight.

kagome8 and hex9 at b = 4 were not run.

## 3. The measured claims

### 3.1 Slab laws, re-measured

{111} slabs 8 layers deep, periodic faces of the author's shapes, soups of density 0.45, burn-in 200, a replica
ends when a boundary layer is empty or when it becomes periodic (censored); `./run_measured.sh gump`,
`./run_measured.sh fcc`, `python3 summary.py`. Unlike the author I do not censor replicas that acquire a dead sealed
set other than a face (1 % of endings in his gump runs, 16 % at fcc A = 25).

[[MEASURED]]

### 3.2 "Walls, no exception"

Row re-derived: **fcc at c = 10 = K_f + 1** (B456789/S3456789; torus chaotic; a⁰ = 6 ≥ b − 1), against c = 9 = K_f,
with my stepper (`./run_measured.sh fcc`, last four lines):

| cap | A | face deaths | replica-generations at risk | boundary density | interior | class.md |
|---|---|---|---|---|---|---|
| 9 | 49 | 1,677 | 6.3 × 10⁷ | 0.728 | 0.499 | law, ln τ = 11.10 (mine 11.23 ± 0.02) |
| 10 | 25 | **0** | 1.3 × 10⁶ | **1.000** | 0.532 | WALL, ρ_f 1.00, 0 deaths |
| 10 | 49 | **0** | 6.3 × 10⁷ | **1.000** | 0.614 | WALL, ρ_f 1.00, 0 deaths |

Reproduced: between c = K_f and c = K_f + 1 the boundary goes from dying every 75,000 generations to never, and
it sits at density 1.000 from soups of density 0.45. The same holds on face12e, a lattice the author never saw: a
wall sheet (degree 8, 4 in-sheet neighbours) set fully alive over a random interior is broken in 64/64 soups at
c = 7 and c = 8 and in 0/64 at c = 9 and c = 10 (`python3 proofs.py wallprop`). [[F12CAPS]]
The count "38, no exception" is recounted in §3.3.

### 3.3 Recounts from the committed data (`python3 recount.py`)

Sources: `data/scan_table.md` (every cap: torus class, slab counts), `data/faces.tsv` (every slab run),
`data/hulls.txt`, `PREDICTIONS.md`. The scoring rule applied is the one fixed in PREDICTIONS.md before testing:
face law = ln τ rises ≥ 1.0 over the sizes, ≥ 20 deaths at two or more sizes, CV in [0.8, 1.25]; hull grows =
median × ≥ e per size step at two consecutive steps, runs ending, unfinished at the cap counting as growing.

| claim in class.md | recount | verdict |
|---|---|---|
| "50 lattice–cap pairs with a chaotic bulk and the cap within reach" | 50 (16 families) | holds |
| "46 have a memoryless face law (2 starve, 2 are glasses)" | **42** by the fixed rule. Fail: cross4 c = 7 and bcc14 c = 7 (starved, as stated), tristar2 c = 8 (glass, as stated), and five the author counts as laws: **face8 c = 5** (deaths at the two sizes: 10,265 and 8), **bcc8 c = 6** (29,860 and 1), **sc6 c = 4** (63,117; 5; 15), **sc6 c = 5** (13,625 and 1), **cross3 c = 8** (CV 1.29 at A = 40 with 66 deaths). The pair the author excludes as a glass, cross3d2 c = 10, meets the rule (219 and 422 deaths, CV 1.02–1.03). | holds only if one death at the second size is accepted as a law; "46" → "42 by the rule, 4 more with fewer than 20 deaths at the second size" |
| "CV 0.83–1.23 wherever ≥ 50 deaths" | cross3 c = 8, A = 40: 66 deaths, CV 1.29 (also in `laws.md`) | false by one entry |
| "all 38 pairs beyond reach with a⁰ ≥ b − 1 are walls, no exception … 18 families" | 60 such pairs scanned in 20 families; 38 in 18 families have anything alive after the burn-in; in all 38 every slab run has boundary density 1.00 and zero face deaths. The verdict column says WALL for 26 and "freeze" for 12; the torus is chaotic in 25, frozen in 12, glass in 1 | holds. Worth saying that only 25 of the 38 have a chaotic bulk |
| "28 'GUMP' calls: 8 passed all three, 6 slab law without conclusive hull, 14 failed" | 28 calls. Mechanically: 4 pass all three (fcc 6, bcc8 5, bcc14 8, sc18 10); 2 more if every step into an unfinished size counts (fcc 7, cross3d2 5: one finished size each); cross3 7 misses the hull rule by one step (ratios 3.34, **2.69**, 3.15); face8 5 misses the slab rule (8 deaths at its second size). Those are the author's 8. The 6 and the 14 recount as stated (10 + 2 + 1 + 1), with tristar2 c = 8 counted as "bulk not chaotic" here but as one of the 50 chaotic pairs in S1 | 8 / 6 / 14 stands as a judgment, not as a mechanical score |
| "14 of 15 explicit 'not a gump' calls held" | 15 pairs, 14 hold, bond10 c = 7 is the miss. Five of the 14 hold because the torus dies at the named cap (tri18 12, tri12 9, hex12 9, moore_r2 15, 16), so the stated reason, passive faces, was not tested; three (hex3, kagome4, kagome8) were scanned at the direction-only b (§1.2) | holds as counted |
| "two gumps were missed outright (vn c = 3, sc6 c = 3)" | see below | the hull evidence for both is thinner than for rules scored as misses |

**The hull rule is not well defined, and decides the headline.** "× ≥ e per size step" depends on the step, which
was chosen per family. By the letter, the project's reference 2D gump fails it (cross2 B34/S234, sides 11…21 in
steps of 2: ratios 2.38, 2.23, 2.09, 2.30, 2.05), and so does **vn B2/S12**, class.md's headline find (sides 9…33
in steps of 4: 2.66, 2.18, 2.25, 1.91, 1.95, 1.63, every one below e and falling). cross3 B45/S345 (sides 17…41 in
steps of 8: 2.84, 2.53, 1.93) is scored as a failed call, "too weak to grow in boxes". Per unit of side the rates
are: cross2 0.36–0.43, steady; vn 0.245 → 0.122, halving; cross3 c = 6 0.13 → 0.08. [[VNBOX]]
sc6 B2/S12 is called a gump on one hull size that finished (R = 2: 2,752; R = 3, 4, 5 all unfinished at 10⁵ with
density 0.40, i.e. still full).

### 3.4 Were the predictions committed before their tests

**In git order, yes** (`git log -- research/theory/class research/theory/class.md`, 2026-11-13, UTC):

| time | commit | content |
|---|---|---|
| 18:08:33 | 1dac6f9 | lattices, theory, stepper, validation (no data) |
| 18:26:50 | 5636f1c | PREDICTIONS.md stage 1 (36 rows, scoring rules), `data/indices.txt` (no dynamics) |
| 18:33:19 | cb98e1b | stage 2 |
| 18:35:43 | 18200e8 | stage 3 (bond10) |
| 18:37:21 | ff40077 | stage 4 |
| 18:41:07 | c9ac532 | stage 5 |
| 19:17:27 | f7e9d44 | first data: `scan2d.log`, `scan3d.log`, `scan_table.md` |
| 19:30 – 19:50 | 8089630 … f3e200f | `faces.tsv`, `hulls.txt`, `laws.md`, outcomes, class.md |

PREDICTIONS.md is append-only across these commits (lines added / removed: 46/0, 15/0, 22/0, 18/0, 30/0), and the
fcc slope 0.21 ± 0.07 is in the 18:26 commit.

**What git cannot show** is when the runs were made. Two untracked traces are consistent with the stated order and
do not prove it. `research/scratch/class/results.jsonl` (983 records, no timestamps) is in append order: the
training lattices (cross2, moore, gump) fill records 0–102, the first test-set record (cross3) is number 103, then
the 2D families in `run2d.sh` order, then 3D. File times: `gstep` built 18:02:56; `scan2d.log` last written
18:50:41; `scan3d.log` 19:16:48. So the 3D scan ran after all five stages; the 2D scan ended 24 minutes after the
stage-1 commit and the cross3 and cross4 scans that stage 2 cites fit in the 6.5 minutes between stages 1 and 2 only
if the scan started right at the commit (16 families in at most 24 minutes is 1.5 minutes each, so it fits). I
cannot exclude that the 2D scan started before 18:26:50; nothing contradicts the account. (class.md's "≈ 45 + 45
min on one core" for the two scans is about twice what the file times allow.)

## 4. Clause 5: "face not starved, K_f·ρ/b ≳ 0.85"

**It is a fit to two points, with two exceptions on the same side.** From class.md's own tables
(`python3 recount.py`, last blocks; σ from the torus density of `scan_table.md`):

| σ | pair | face |
|---|---|---|
| 0.70 | vn c = 3 | memoryless law, 0.12–0.18 per cell; called a gump |
| 0.74 | bcc14 c = 7 | eroding (no law) |
| 0.77 | bond10 c = 6 | memoryless law, 0.06 per cell |
| 0.80 | cross4 c = 7 | eroding (no law) |
| 0.85–0.88 | sc18 c = 9, face18 c = 9, sc26 c = 17, cross3 c = 6 | laws of 0.06–0.12 |
| ≥ 0.89 | 34 pairs with a law | slopes 0.10 … 0.44 |

- The line at 0.85 was drawn after the fact between the two eroding cases it was introduced to explain and the
  weak laws just above them. Of the four pairs below it, two erode and two have a memoryless law. Above it, two
  of 46 have none by the author's count (tristar2 c = 8 at σ = 1.03, cross3d2 c = 10 at 2.19, both put down to a
  glassy bulk).
- As a predictor of strength it carries nothing above the line: among the 34 pairs with σ ≥ 0.89 and a law, the
  rank correlation of σ with the slope is −0.04 (p = 0.8); over all 42 it is 0.38, all of it from the eight pairs
  below 0.89 being weak.
- **Out of sample it has no success.** face12e: with K_f as the summary defines it (K minus the most neighbours
  behind the plane: 12 − 4 = 8, the wall-sheet cell) σ = 8 × 0.398 / 4 = 0.80, the value of cross4 c = 7, and clause
  5 says starved. The wall is the densest layer of the slab (0.52 against 0.40 inside) and the law is strong
  (0.41 per wall face, 0.205 per cell of the layer that dies). With K_f as `theory.py table` would print it (the largest a⁰ + a⁻ over
  types: 9, the y/z-faces) σ = 0.90 and clause 5 passes by 0.05. kagome4 B2/S12 (§2.4): σ = 0.48 with K_f = 2 (the
  wall row), 0.96 with K_f = 4. An index that flips with the choice of layer cannot be scored.

**What would make it a criterion, and what would falsify it.** Fix in advance which layer K_f refers to (the natural
choice after §2.2 is the layer whose emptiness is the permanent event) and the statement "a chaotic pair with
σ < 0.85 has no face law with slope ≥ 0.10 per cell". Then one memoryless law of slope ≥ 0.10 at σ < 0.85
falsifies it. vn B2/S12 (σ = 0.70; 0.12 per cell at L = 64–80, 0.18 at L = 12–20) already does, and class.md
exempts it for having K = 4. A direct measure exists and is already in `faces.tsv`: the boundary density against
the interior density. It is below the interior in both eroding cases (bcc14 c = 7: 0.19–0.32 against 0.32–0.38)
and above it in every strong law I re-measured (gump 0.52 / 0.41, fcc 0.46 / 0.39, face12e 0.52 / 0.40). That is
a description of starvation, not a prediction of it; no a-priori index in class.md predicts it (stage 2's R₁ scored
13 of 19, stage 4's 3 of 8, by the author's count).

## 5. Verdict on the class

### 5.1 The strongest statement I would sign

For a capped threshold (b, c) — alive next iff n + x ≥ b, except n ≥ c dies — on a cell lattice with any number of
cell types:

1. **Confinement [proved].** If the half-spaces with c(H) ≤ b − 1 have positively spanning normals, every finite
   pattern stays in the intersection of the sealed half-spaces containing it, that hull never grows, and the
   pattern is eventually periodic. With one cell type this reads b > a⁻ on a positively spanning set of directions.
   *Not proved:* the converse for patterns (that without such a family something escapes).
2. **No local permanent death [proved].** If some generic v gives every cell type at least b forward offsets, no
   finite set of cells is sealed. With one type this is b ≤ K/2 and is an iff; on gump's lattice it is an iff too
   [computed at b = 7]. In a wall band or a thin slab the same count must hold for every layer [three layers for
   gump (T6), one cube for face12e (mine), the author's m* column for the rest, not re-derived].
3. **Armour [proved, conditional].** A set whose cells have ≥ b − 1 neighbours inside it and vessel-degree ≤ c − 1 is
   immortal once entirely alive. **[measured]** Where such a set exists and a⁰ ≥ b − 1 it does form from soups and no
   wall ever dies: all 38 scanned pairs (author's data, recounted), fcc c = 10 and face12e c = 9 (mine, zero deaths).
4. **Two-sided drive [proved].** In a finite vessel an orbit of period ≥ 3 has overcrowded-after-life and
   undercrowded-after-life events for ever; either pure threshold rule alone reaches period ≤ 2.
5. **Whole-wall death [measured].** With 1–3 in force, no armour, and a torus state that is chaotic at that cap, the
   wall band dies as a whole after a wait that is memoryless and exponential in the wall's area. Re-measured with
   independent code: gump caps 6 and 7 (0.212 and 0.216 per cell, five sizes), fcc cap 6 (0.181, five sizes),
   face12e cap 6 (0.41 per wall face, five sizes; new). In the author's data: 42 of 50 pairs by the rule fixed in
   advance, 46 by his count; the exceptions are two eroding walls (cross4 c = 7, bcc14 c = 7) and glassy bulks.
6. **Lifetime in the hull [measured].** Where a hull was run to completion at three or more sizes, lifetimes grow
   as the wall law dictates and end in sparse debris: gump cap 6 and fcc cap 6 (author's runs), face12e cap 6
   (mine: 10, 60, 439, 9,855, 707,038), vn B2/S12 (0.11 per unit of side up to side 65, mine).
7. **[conjecture]** Under 1–3 and a chaotic bulk the wall band is a metastable process whose only absorbing state
   is the empty band, with a wait exponential in its area. **Nothing is conjectured, because nothing is known,**
   about which caps are chaotic (class.md says so) or about how strong the law is (clause 5 does not do it).

This is a list of necessary structure with a measured regularity on top. It is not an "iff", and "gump" has no
sharp edge on the weak side: vn B2/S12 (0.12 per cell), cross3 B45/S345 (0.05) and Moore B456/S3456 rows
(0.02–0.07) differ in a rate, and class.md calls the first a gump and the other two not.

### 5.2 What class.md should change

1. **Theorem A, clause 1, the table:** sealed half-spaces in place of sealed directions (§1.2). Drop "iff" and "the
   hull is the polytope of those rays" for several types. Correct the rows: bond10 (tight b = 3; at b = 4 the hull
   is octahedron ∩ box), face8 (octahedron ∩ box), kagome4 (b = 2), kagome8 and hex9 (b = 4); add face12e. Say that
   gump's row is exact.
2. **bond10:** withdraw "the one chaotic in-reach rule that is not a gump", "C2 has no converse for slabs" as
   phrased, and "tubes through every slab" (3 and 4 layers only, by the author's own script). Its b = 4 family is
   one above tight and has six wall directions the analysis missed.
3. **Clause 3:** tag it [proved conditional + measured]; state it as "no armoured set" (Theorem E), which needs no
   choice of "the face cell"; note sc26 c = 18, 19 and bond10 c = 7 as its own data against the printed form.
4. **Clause 5:** demote to an observation about two cases, or define K_f for a multi-layer wall and state what
   would refute it (§4).
5. **C4:** "for the cells of every layer" (§1.3).
6. **N1:** necessity for confinement is not proved; say "sufficient".
7. **S1:** "46 of 50" → "42 by the scoring rule; four more (face8 c = 5, bcc8 c = 6, sc6 c = 4, 5) have 1–15 deaths
   at their second size"; correct "CV 0.83–1.23 wherever ≥ 50 deaths" (cross3 c = 8: 1.29).
8. **Scorecard and the hull test:** replace "× e per size step" by a rate per unit of side compared with the slab
   slope; rescore vn, cross2, cross3 c = 6, 7 with it; say that sc6 B2/S12 and cross3d2 B34/S234 rest on one finished
   hull size, face8 B34/S234 on 8 slab deaths at its second size. tristar2 c = 8 is "chaotic" in S1 and "bulk not
   chaotic" in the scorecard.
9. **"Identical slab face law"** → "equal within 0.1 in ln τ at five sizes; the slopes differ by 2 %" (§3.1).
10. **fcc slope** 0.19 → 0.18 (the 0.19 leans on A = 25, where the wait is half the burn-in); the prediction
    0.21 ± 0.07 still holds.
11. **§8.2** "two dimensions has only the crosses": kagome B2/S12 is a candidate with all three signatures (§2.4).
12. **Reproduce block:** "≈ 45 + 45 min" for the scans is about twice what the file times show.

## Not checked

- **Completeness of the half-space scan.** `seal.py` scans primitive integer directions with |u_i| ≤ 5 (3D) and
  ≤ 8 (2D). Irrational directions cannot gain from position (every type is dense in height). For the face lattices
  position enters only through the parity of the u_i and through offsets with |u·o| = 1, and all such patterns occur
  within the bound; that is an argument, not a proof. hex3's extra sealed directions grow with the bound and were
  not pursued.
- **Table columns not re-derived:** fw, m* (except gump by T6, fcc by hand, face12e), c_arm (except gump, fcc,
  face12e). The mean-field numbers and R₁ were not looked at.
- **Measurements not repeated:** every 2D scan, the vn strip law, Moore rows, the weak laws, the O1/U1 rates of N4,
  the gap-healing test of §8.5, stages 2–5 of the scorecard (I recounted stage 1 and the two headline tallies
  only), all hull runs of class.md except vn's.
- **Censoring.** My slab runs censor replicas that become periodic but not replicas that acquire a dead sealed set
  other than a face, which the author's do. It is immaterial for gump at A ≥ 27 and fcc at A ≥ 36 (agreement within
  0.02–0.06) and it is why I have no like-for-like number at fcc A = 25. For face12e see "transverse cuts" in §2.2.
  For kagome4 strips it matters and those numbers are rough.
- **face12e:** one cap in depth (c = 6); walls of 16–36 faces, rectangles only; slab depth 4 cubes (6 cubes at
  one size gives ln τ higher by 0.05, not followed up); boxes to 6³; no symmetric seeds; no study of the debris.
- **bond10 at b = 3:** whether its boxes of 4³ and larger ever die. **kagome8, hex9 at b = 4:** not run.
- **The converse of clause 1** (an unconfined capped threshold has unbounded patterns): no proof, no
  counterexample.
- `thickness.md` and `threshold.md`, which class.md cites for T5 and T6, were not reviewed; I re-derived only what
  class.md states. No outside source was consulted. The lead's `edge.py` was read, not run.
- The time order of the author's runs relative to his prediction commits (§3.4) rests on untracked files.

## Reproduce

```sh
cd research/audit/class
python3 validate.py                 # stepper against reference/oracle.py and numpy rolls        (10 s)  ALL OK
python3 seal.py; python3 seal.py face12e      # sealing by direction and by half-space, all 30 lattices   (2 s)
python3 proofs.py energy; python3 proofs.py c4; python3 proofs.py c2multi
python3 proofs.py bond10; python3 proofs.py wallprop; python3 proofs.py armour                 # seconds each
python3 face12e.py structure; python3 face12e.py confine; python3 face12e.py confine-others    # 1 s, 20 s, 20 s
python3 face12e.py bulk; python3 face12e.py bulk 6 gump                                        # 3 s each
./run_face12e.sh                    # face12e slabs and boxes                                    (about 12 min)
python3 face12e.py layers 5 80000; python3 face12e.py cuts 4 4000 8; python3 face12e.py cuts 5 60000 2
./run_measured.sh gump; ./run_measured.sh fcc      # part 3 slab laws                            (25 + 12 min)
./run_extra.sh                      # kagome4 b = 2, bond10 b = 3, vn boxes, face12e other caps   (about 15 min)
python3 summary.py                  # the tables of this report from the outputs above
python3 recount.py                  # the tallies of section 3.3 and 4 from the author's committed data
```
Predictions: `PREDICTION-face12e.md` (commit bcb8122, before any run on face12e), `PREDICTION-repaired.md` (commit
1a32ea9, before any run on kagome4 at b = 2 or bond10 at b = 3). The stepper is `aud.c` (built on first use into
`research/scratch/audit-class/libaud.so`) driven by `aud.py`.
