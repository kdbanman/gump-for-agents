# Predictions (append-only)

*Class agent, 2026-11-13. Committed before any dynamics was run on the lattices listed under "Test set".
Nothing above a later "Outcomes" heading is edited after its commit; outcomes are appended below.*

## What I had seen when writing this

- **Training set (dynamics run, used to shape the criterion):** the three lattices the project already knew —
  the face lattice (`gump`, K = 12), the 2D range-2 cross (`cross2`, K = 8), 2D Moore (`moore`, K = 8) — every cap
  c, torus + periodic slab + (face lattice only) octahedral hulls. Results in `research/scratch/class/results.jsonl`,
  summarised in class.md §4. Two things there contradict the brief and shaped what follows:
  (a) on the face lattice the caps c = 7 and c = 8 (B456/S3456, B4567/S34567) show the same memoryless face law as
  gump (c = 6) in periodic slabs, slope 0.21 per face cell in all three; (b) on Moore, B456/S3456 has a memoryless
  row-death law with a small positive slope (≈ 0.05 per cell, L = 28–80) — "erosion" was a small-size reading.
- **Leak, disclosed:** `validate.py` (stepper check, 60 generations, vessels of 150–290 cells) printed final
  populations for four test-set pairs: fcc B45/S345 slab 6×25 → 0 alive; bcc8 B34/S234 slab 6×25 → 96/150 alive;
  sc18 B678/S5678 slab → 0; bond10 B45/S345 slab → 64/288. I did not use these (the fcc and sc18 lines point
  *against* two of my predictions below, which I leave as the criterion gives them).
- **No dynamics** had been run on any other lattice. Everything below comes from `theory.py`, `indices.py`
  (structure numbers, exact peelings, single-site mean field; output in `data/indices.txt`).

## The criterion being tested (class.md has the derivations)

For a lattice with K neighbours per cell and a capped threshold (b, c) — alive next iff n + x ≥ b, except n ≥ c dies:

- **C1 confinement** (proved): half-space {u·p ≤ C} is sealed iff a⁻(u) ≤ b − 1. Take the least b with a spanning
  set of sealed directions ("tight" b); a⁰ = neighbours in the confining hyperplane; K_f = K − a⁻ = face-cell degree.
- **C2 unsealable interior** (proved for one cell type): no finite set can die unconditionally iff b ≤ K/2.
- **C3 no immortal walls** (proved): if a⁰ ≥ b − 1 and c > K_f, a fully live boundary layer lives forever; in a hull
  the s-core of the cells of vessel-degree ≤ c − 1 is immortal once alive (`armour.py`, c_arm). So need c ≤ K_f, c < c_arm.
- **C4 chaotic bulk** (heuristic, from the two-sided threshold lemma): both under- and over-crowding must stay
  frequent. Mean-field proxy at the upper fixed point ρ*: slope f′(ρ*) < −1 **and** undercrowding rate
  u = P(n + x < b) ≥ 0.02 → chaos; 0.008 ≤ u < 0.02 → marginal (training: one froze, one stayed chaotic);
  u < 0.008 → freezes; slope > −1 or no fixed point → dies/settles.
- **Claim:** C1 ∧ C2 ∧ C3 ∧ C4 ⇒ gump (memoryless face death, exponential in face size). C1–C3 with tight b force
  b + 2 ≤ c ≤ K − b + 1, hence b ≤ (K − 1)/2, hence **a⁰ ≥ 4**: the confining hyperplane must hold two lines of
  neighbours. Lattices with a⁰ = 2 (Moore, von Neumann, triangular-6, kagome, honeycomb) have b = K/2: the cap can
  never act on a face (K_f = b + 1 < c), faces are passive threshold layers — walls where a⁰ ≥ b − 1, weakly
  metastable otherwise.

## Scoring rules (fixed now)

- **BULK** — torus (2D: 64 × 64 periods; 3D: 10³ periods), 64 soups at the mean-field density, 4096 generations:
  *chaos* = ≥ 48 soups still running (not period ≤ 2, not equal to a snapshot), activity ≥ 0.05 and ≥ 0.6 × its value
  at T/4. Otherwise die / freeze / glass as printed by `run.py bulk`.
- **SLAB** — periodic slab along the first sealed direction, 16 layers deep in 2D (8 in 3D), ≥ 3 face sizes;
  restarts; settled replicas and replicas with a sealed set that is not a whole face are censored (`gstep qsd`).
  *face law* = ln τ_face rises by ≥ 1.0 over the sizes, ≥ 20 deaths at two or more sizes, CV of the wait in [0.8, 1.25].
  *strong* if the slope is ≥ 0.15 per face cell, *weak* if < 0.10.
  *wall* = no face deaths, face activity < 0.02 while replicas keep running or settle with face density > 0.9.
- **HULL** — confinement polytope, 64 soups, ≥ 3 sizes: *grows* = median lifetime × ≥ e per size step at two
  consecutive steps and the runs end (unfinished at the cap counts as growing); *immortal/frozen* = final density
  > 0.3 with settled runs, or unfinished at every size from the smallest.
- **GUMP** = BULK chaos ∧ SLAB face law ∧ HULL grows. A prediction "GUMP" is a hit only if all three hold; a
  prediction "not" is a hit if any fails. Marginal calls (marked ?) are scored separately.

## Test set and predictions

Tight b unless said. Only the caps the mean field allows to be chaotic are listed; **every other cap of each family
is predicted NOT a gump** (bulk dies or freezes) and will be scanned too.

### 2D

| # | lattice | K | a⁰ | b | K_f | c | rule | predicted bulk | predicted verdict | why |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | cross3 (range-3 cross) | 12 | 6 | 4 | 9 | 6 | B45/S345 | chaos | **GUMP**, strong | same (K, a⁰, b) as gump; window 6–9 |
| 2 | cross3 | | | | | 7 | B456/S3456 | chaos | **GUMP**, strong | |
| 3 | cross3 | | | | | 8 | B4567/S34567 | marginal (u = 0.010) | GUMP? | scored separately |
| 4 | cross4 (range-4 cross) | 16 | 8 | 5 | 12 | 7 | B56/S456 | chaos | **GUMP**, strong | |
| 5 | cross4 | | | | | 8 | B567/S4567 | chaos | **GUMP**, strong | |
| 6 | cross4 | | | | | 9 | B5678/S45678 | marginal (0.017) | GUMP? | |
| 7 | star2 (cross2 + diagonals) | 12 | 4 | 5 | 8 | 8 | B567/S4567 | chaos | **GUMP** | a⁰ = 4, c = K_f, c_arm = 9 |
| 8 | tristar2 (tri., range 2 on 3 axes) | 12 | 4 | 5 | 8 | 8 | B567/S4567 | chaos | **GUMP** | |
| 9 | tristar3 | 18 | 6 | 7 | 12 | 10 | B789/S6789 | chaos | **GUMP** | |
| 10 | tristar3 | | | | | 11 | B789(10)/S6789(10) | chaos | **GUMP** | |
| 11 | tri18 (tri., 3 shells) | 18 | 4 | 8 | 11 | 11 | B8–10/S7–10 | chaos | **GUMP** | a⁰ = 4; c = K_f |
| 12 | tri18 | | | | | 12 | B8–11/S7–11 | chaos | not (passive faces: weak or wall) | c > K_f |
| 13 | vn (von Neumann) | 4 | 2 | 2 | 3 | 4 | B23/S123 | chaos (slope −1.12, shaky) | **not: WALL** | a⁰ = 2; c = K_f + 1, a⁰ ≥ b − 1 |
| 14 | tri6 (triangular) | 6 | 2 | 3 | 4 | 5 | B34/S234 | chaos (slope −1.07, shaky) | **not: WALL** | same; c_arm = 5 |
| 15 | kagome6 | 6 | 2 | 3 | 4 | 5 | B34/S234 | chaos (shaky) | **not: WALL** | same |
| 16 | tri12 (tri., 2 shells) | 12 | 2 | 6 | 7 | 9 | B678/S5678 | chaos | not: passive faces — weak law (< 0.10) or none | a⁰ = 2, c > K_f, a⁰ < b − 1 |
| 17 | hex12 (honeycomb, 3 shells) | 12 | 2 | 6 | 7 | 9 | B678/S5678 | chaos | not: as tri12 | |
| 18 | moore_r2 (5 × 5 Moore) | 24 | 4 | 11 | 14 | 15, 16 | B11–14/S10–14, B11–15/S10–15 | chaos | not: passive faces (c > K_f) | window b + 2 ≤ c ≤ K_f = 14 misses the chaotic caps |
| 19 | hex9 (honeycomb, 2 shells) | 9 | 2 | 5 | 6 | 8 | B567/S4567 | mean field says chaos | **not: sealed holes** | b > generic forward count 4: a 292-cell sealed set found by peeling |
| 20 | hex3, kagome4, kagome8 | | | | | all | | | **not** | finite sealed sets (peeling) or no chaotic cap |
| 21 | moore (training, re-test in hulls) | 8 | 2 | 4 | 5 | 7 | B456/S3456 | chaos (seen) | not a clean gump: weak law, hull lifetimes grow slowly if at all | passive faces |

### 3D

| # | lattice | K | a⁰ | b | K_f | c | rule | predicted bulk | predicted verdict | why |
|---|---|---|---|---|---|---|---|---|---|---|
| 22 | fcc ({111} faces, octahedron) | 12 | 6 | 4 | 9 | 6 | B45/S345 | chaos | **GUMP**; slope 0.21 ± 0.07 per face cell | gump's numbers |
| 23 | fcc | | | | | 7 | B456/S3456 | chaos | **GUMP** | |
| 24 | fcc | | | | | 8 | B4567/S34567 | marginal | not in hulls (c_arm = 8), slab law if chaotic | |
| 25 | bcc8 ({110} faces, rhombic dodecahedron) | 8 | 4 | 3 | 6 | 5 | B34/S234 | chaos | **GUMP** | cross2's numbers |
| 26 | bcc8 | | | | | 6 | B345/S2345 | marginal | not (c_arm = 6) | |
| 27 | bcc14 | 14 | 6 | 5 | 10 | 7, 8 | B56/S456, B567/S4567 | chaos | **GUMP** both | |
| 28 | sc6 (3D von Neumann, box) | 6 | 4 | 2 | 5 | 4 | B23/S123 | chaos | **GUMP** | a⁰ = 4; window {4, 5}; c_arm = 5 |
| 29 | sc6 | | | | | 5 | B234/S1234 | freeze | not | |
| 30 | sc18 (faces + edges, box) | 18 | 8 | 6 | 13 | 8, 9, 10 | B67/S567 … | chaos | **GUMP** all three | |
| 31 | sc26 (3D Moore) | 26 | 8 | 10 | 17 | 13, 14, 15 | B10–12/S9–12 … | chaos | **GUMP** all three | a⁰ = 8 ≥ 4 although a⁰/K = 0.31 |
| 32 | cross3d2 (3D range-2 cross, box) | 12 | 8 | 3 | 10 | 5, 6 | B34/S234, B345/S2345 | chaos | **GUMP** both, strongest slope of the 3D set | b/K_f = 0.3 |
| 33 | bond10 (edges of the cubic honeycomb sharing a vertex) | 10 | 4 | 4 | 7 | 6 | B45/S345 | chaos | **GUMP** | c_arm = 7 |
| 34 | bond10 | | | | | 7 | B456/S3456 | chaos | not in hulls (armour), slab law holds | c = c_arm |
| 35 | face8 (face lattice, 8 perpendicular only) | 8 | 4 | 3 | 6 | 5 | B34/S234 | chaos | **GUMP** | |
| 36 | face18 (face lattice, 18) | 18 | 8 | 6 | 13 | 8, 9, 10 | B67/S567 … | chaos | **GUMP** all three | |

### Quantitative side-predictions

- **Q1 (cap-independence).** On one lattice the slab slope I is the same for every chaotic cap with c ≤ K_f, to
  ± 15% (seen on the face lattice: 0.211, 0.213, 0.208). Reason offered: a face dies of starvation; the cap is idle
  there. To be tested on cross3 (c = 6, 7), fcc (6, 7), sc18 (8, 9, 10).
- **Q2 (ordering in 2D).** I(cross3 c = 6) ≥ I(cross2 c = 5) = 0.42 > I(star2), I(tristar2) > I(Moore rows) ≈ 0.05.
  Low confidence on the first inequality.
- **Q3 (hull armour).** For c ≥ c_arm hull runs do not end in sparse debris: final density > 0.3 or unfinished
  (bcc8 c = 6, bond10 c = 7, sc6 c = 5, face lattice c = 8 — the last seen in training).
- **Q4 (two-sided drive).** In every chaotic torus state both drives are present: undercrowded-after-life (U1) and
  overcrowded-after-life (O1) events at rates > 0.01 per cell per generation; in every glass/frozen state at least
  one of them is < 0.002. (The lemma only says both are needed for period ≥ 3; the rates are the prediction.)

### What the brief's candidate ingredients would predict instead (for contrast, scored too)

"Half the neighbourhood in the confining hyperplane, threshold near a third, one cap per neighbourhood":
GUMP for cross3, fcc, bcc8 (one cap each); **not** for sc26 (a⁰/K = 0.31), tri18 (0.22), star2 / tristar2 (0.33),
bond10 (0.40); silent on sc6 (a⁰/K = 0.67, b/K = 0.33). Rows 7, 8, 11, 31, 33 and the second caps of rows 2, 5, 23,
27, 30, 32 discriminate between the two criteria.

---

## Stage 2 — appended after the first two test families (cross3, cross4), before looking at any other

*Same day. Seen so far from the test set: the cross3 and cross4 scans (2D), nothing else — the 2D scan is still
running and I have not read its output beyond cross4; no 3D run has been started. (Also seen: `energy.py selftest`
printed torus densities for tri6 c = 5 (0.576, chaotic) and fcc c = 6 (0.391, chaotic).)*

What cross3/cross4 showed (misses of stage 1, recorded here so they are not forgotten): the bulk is chaotic over a
much wider range of caps than the mean-field proxy allows (cross3 c = 6…11, cross4 c = 7…14); faces at the low caps
are **weak** (cross3 c = 6: ln τ = 5.7, 7.2, 9.8 at L = 28, 48, 96, i.e. 0.05–0.08 per cell, and dead within ten
generations at L = 12), strong only near c = K_f (cross3 c = 9: 0.42 per cell; cross4 c = 12: 0.29), walls at
c = K_f + 1 exactly as the armour lemma says. So Q1 (cap-independence of the slope) is false in 2D, and
"C1–C4 ⇒ strong gump" is false: the strength of a face needs its own index.

**New index (stage-2 hypothesis).** Treat the boundary layer as a contact-type process fed by the bulk, with the
empty layer as its absorbing state. A lone live face cell survives iff all its a⁻ = b − 1 inward neighbours are
alive, and each of its a⁰ in-layer neighbours is born under the same condition, so its mean offspring is

  R₁ = (a⁰ + 1) · ρ^(b−1)   (ρ = bulk density; a priori ρ ≈ 0.87 × mean-field ρ*).

2D training + cross3/cross4: R₁ = 1.12 (cross2, slope 0.42), 1.19 (cross3 c = 9, 0.42), 0.92 (cross4 c = 12, 0.29),
0.63 (Moore, 0.05), 0.42 (cross3 c = 6, 0.06). 3D training: R₁ = 0.50, 0.78, 1.15 for the face lattice c = 6, 7, 8,
all with slope 0.21 — so in 3D the threshold is lower and I do not understand the flat slope.

**Stage-2 calls** (they overrule the stage-1 "GUMP" verdicts where they differ; both are scored):

| lattice | a⁰, a⁻ | caps → R₁ (a priori) | stage-2 call |
|---|---|---|---|
| star2, tristar2 | 4, 4 | c = 8 → 0.32 | weak or no face law (slope < 0.10) — *reverses stage 1* |
| tristar3 | 6, 6 | c = 10, 11, 12 → 0.05, 0.09, 0.15 | **no face law (erosion)** — *reverses* |
| tri18 | 4, 7 | c = 11 → 0.01 | **no face law** — *reverses* |
| tri12, hex12, moore_r2 | 2–4, 5–10 | < 0.05 | no face law (stage 1 said weak or none) |
| vn, tri6, kagome6 | 2, 1–2 | 0.9–1.9 | walls (unchanged) |
| fcc | 6, 3 | c = 6 → 0.40; c = 7 → 0.65 | face law at both (c = 6 borderline) |
| bcc8, face8 | 4, 2 | c = 5 → 1.02 | face law, strong |
| bcc14 | 6, 4 | c = 7, 8 → 0.15, 0.28; c = 9, 10 → 0.44, 0.64 | **none at c = 7; marginal at 8** — *reverses*; face law at 9–10 if the bulk is chaotic there |
| sc6 | 4, 1 | c = 4 → 2.3 | face law, strong |
| sc18, face18 | 8, 5 | c = 8, 9, 10 → 0.05, 0.10, 0.16; c = 12, 13 → 0.36, 0.52 | **none at 8–10** — *reverses*; face law only at c ≥ 12 if chaotic there |
| sc26 | 8, 9 | every cap < 0.03 | **no face law at any cap** — *reverses* (agrees with the brief's "fraction in the plane" intuition) |
| cross3d2 | 8, 2 | c = 5, 6 → 1.05, 1.47 | face law, strong |
| bond10 | 4, 3 | c = 6 → 0.42 | face law (borderline) |

3D threshold used: face law iff R₁ ≳ 0.35 (the face lattice at 0.50 is the only calibration point); 2D: strong iff
R₁ ≳ 0.9, weak for 0.35–0.9, none below.

---

## Stage 3 — one more call, appended before any bond10 dynamics was run

*Seen since stage 2: star2 and tristar2 scans (2D). The 3D queue has not reached bond10.*

`python3 pits.py bond10 4 4` (exact peeling) finds a **finite sealed set spanning all four layers of a 4-layer
{111} slab** of bond10 (402 cells of a 637-cell patch), although the full lattice has none (b = 4 ≤ K/2 = 5) and no
pit was found in a half-space. The forward-count certificate fails for bond10 at every thickness (the three inward
offsets of a cell lie in an open half-plane after projection). So on bond10, unlike gump, a slab can be pierced by a
finite dead tube. **Call:** bond10 c = 6 is *not* a gump even if its bulk is chaotic — in slabs "sealed, not a
face" endings will not be rare compared with face deaths and their rate will grow with the face area, so the wait
does not grow exponentially with the face. (This overrules stage 1 row 33 and the stage-2 "borderline face law".)
The same peeling finds nothing in 4 layers of face8 and sc26 (2 layers: sealed sets in both).

---

## Stage 4 — out-of-sample test of R₁ inside the cross families (appended before measuring)

*Seen since stage 3: tristar3 scan. The first scan measured cross3 only at c = 6 (after a manual re-run at L = 28–96)
and c = 9, cross4 only at c = 12; the other caps died before the burn-in at L = 12 and were not followed up.*

With the measured torus densities, R₁ = (a⁰ + 1)ρ^(b−1):

| family | cap | ρ (torus) | R₁ | call (2D: strong ≥ 0.9, weak 0.35–0.9, none < 0.35) |
|---|---|---|---|---|
| cross3 | 7 | 0.452 | 0.65 | weak: slope 0.05–0.15 per cell |
| cross3 | 8 | 0.502 | 0.89 | strong or nearly: slope 0.15–0.42 |
| cross4 | 7 | 0.334 | 0.11 | **no face law** (wait saturates or falls with L) |
| cross4 | 8 | 0.401 | 0.23 | no face law |
| cross4 | 9 | 0.436 | 0.33 | none or barely (slope < 0.05) |
| cross4 | 10 | 0.478 | 0.47 | weak (0.03–0.12) |
| cross4 | 11 | 0.524 | 0.68 | weak-to-middling (0.08–0.2) |

Monotone claim, whatever the thresholds: within each family the slope increases with the cap up to c = K_f.
To be measured at L up to ~100 (m = 16–24), same censoring.
