# Lab notebook

Newest entries at the bottom. Each claim is tagged **[proved]**, **[measured]** or
**[conjecture]**, with the command that reproduces it where applicable.

## 2026-11-12 — first contact (lead)

- **[measured]** `reference/oracle.py` reproduces the original's population logs for closed
  cubes of side 8, 9, 10, 11 at every generation
  (`python3 reference/oracle.py legacy-cube 60 --compare reference/golden/legacy_cube_side11_H60.txt`).
  None of those four runs ever touches the torus seam.
- **[proved]** Octahedral confinement, the 3-layer firewall, and the closed kagome
  sub-automata (T1–T4 in `docs/AUTOMATON.md`); brute-force checked by `reference/check_theory.py`.
  This explains the original README's observations: cubes become "8-sided dice" because
  growth is free along the axes but impossible across `{111}` planes; everything
  "grows, evolves, then collapses" because every finite seed is trapped in a finite hull.
- **[measured]** The original's population plots for sides 11 and 13 show a long noisy plateau
  followed by a **staircase** collapse (several lower plateaus, then death).
- **[conjecture]** The staircase is T3 in action: each step is an irreversible event in which
  `{111}` layers go permanently dead — the hull shrinks or a firewall splits the octahedron
  into causally disconnected pieces — and the plateau height tracks the surviving volume.
  Test: per-layer population kymograph along a body diagonal.
- **[measured]** The original's unfinished `population38.txt` is a side-19 cube (gen-1
  population `12n² − 36n + 48 = 3696` identifies `n`). It sat at ≈150k cells for 296k
  generations. Its hull radius (55) exceeds the torus half-width (50), so it wrapped and
  filled the whole torus: ≈0.40 live fraction of its 3·50³ = 375k cells. So the chaotic
  phase has a density near 0.4 and, unconfined on a torus that size, outlives 3×10⁵ generations.
  *(Corrected: an earlier version of this entry miscounted the torus as 500k cells and said 0.30.)*
- **[measured]** Side-13's plateau (≈7700) is the same density: its hull at R=33 holds 19,686 cells (0.39).
- **[measured]** A random soup confined to a single `{111}` layer stays in the layer and
  decays within ~10 generations to a small still life (one trial: 12 cells).

### Open questions (unordered)

1. Does the staircase conjecture hold? What sets the plateau lifetimes?
2. Lifetime vs size for closed cubes beyond side 13 (23, 71, 65, 4218, 24286, 169049, …).
   Were the side-12/13 legacy runs affected by the torus (their hulls slightly exceed it)?
3. Lifetime *statistics* for random soups in an octahedral vessel of radius R: is the
   escape memoryless (exponential), and how does the rate scale — volume, surface, layers?
4. Is the chaotic phase stable in the infinite system, or only metastable? How does it die:
   firewalls nucleating in the bulk, or erosion from the walls?
5. Census of the ash: still lifes, oscillators (are there any?), their symmetry and layer structure.
6. The kagome sub-automaton (one layer), and the 2- and 3-layer slabs, as automata in their own right.
7. Front speeds along the axes; damage spreading; mean-field vs measured density.
8. Neighbouring rules on the same lattice (any min-birth ≥ 4 rule is confined): is B45/S345 special?

## 2026-11-12 — the staircase is the octahedron peeling, one `{111}` layer at a time (lead)

Side-11 closed cube, oracle run, per-layer populations along `d = (1,1,1)` recorded every
generation (script: `research/experiments/kymo11.py`).

- **[measured]** Hull radius (outermost live layer, doubled units about the centre) over time:
  31 → 29 (gen 2) → 27 (gen 5), then **27 for 3,285 generations**, then
  **25 at gen 3290, 23 at gen 3477, 21 at gen 3796**, then everything dies at gen ≈4218.
  Monotone, as T2 demands.
- **[measured]** Mean population on each plateau: ≈4150, ≈3300, ≈2550, ≈2000.
  Ratios to the first: 0.79, 0.61, 0.48. Predicted by hull volume `(R/27)³`: 0.79, 0.62, 0.47.
  **Plateau height ∝ R³; each stair is the loss of exactly one layer from every face.**
- **[measured]** The outermost live layer (the triangular face, 315 sites at R=27) carries
  ≈123 live cells — density ≈0.39, the same as the bulk (≈0.38–0.40). The face is as busy as
  the interior right up until it dies. *(Corrected: I first compared against a wrong bulk figure.)*
- **[measured]** No interior firewall ever forms in this run; all loss is from the outside in,
  until a final collapse from R=21 in which all remaining layers die within ~30 generations.

Interpretation (**[conjecture]**, the working model going forward):

> Chaos lives in the bulk; death comes from the faces. Each `{111}` face is a quasi-2D
> active layer that can never be re-seeded once empty (T2). Its extinction is a rare
> large-deviation event, so the waiting time to peel should be ≈ exponential in the face's
> *effective* area — the area divided by the order of the symmetry acting on it.

What this predicts, and what would falsify it:

1. Waiting times to peel are memoryless (exponentially distributed) at fixed geometry,
   with `ln(mean) ≈ a + c·A_eff`.
2. O_h-symmetric seeds die enormously faster than asymmetric soups of the same size (the
   fundamental domain of a face is 1/6 of it) — the original README noticed exactly this.
   Asymmetric octahedral soups should show comparable lifetimes at radius ≈ R/√6.
3. A torus has no faces, so a torus-filling soup should be effectively immortal — the
   original's unfinished side-19 run. Only a spontaneous 3-layer interior firewall can kill it.
4. Clean test geometry: an m-layer `{111}` slab on a torus (two free faces, no edges or
   corners). Peeling time vs cross-section area isolates the face mechanism; and thinning
   slabs ask a new question — **is there a critical thickness below which chaos cannot
   sustain itself?** (One layer dies in ~10 generations.)
5. Closed-cube lifetimes (4218, 24286, 169049 for n = 11, 12, 13) should continue roughly as
   `ln τ ≈ a + b·n²` with b ≈ 0.077: about 1.3×10⁶, 1.3×10⁷, 1.4×10⁸ generations for n = 14, 15, 16.
   (Three single samples cannot yet distinguish n² from n or n³ — that is the point of running them.)

## 2026-11-12 — atlas of small objects (atlas agent)

Code, catalogue (1307 objects, every one re-stepped by the oracle) and exact search spaces:
`research/atlas/README.md`. Commands below assume `S=research/scratch/atlas` and the binaries built as in that README.

**Still lifes**
- **[proved, exhaustive]** The smallest still lifes have **6 cells; there are exactly 4** (up to translations × O_h):
  the closed cube `S6a`, the kagome hexagon `KS6a`, two cube corners kissing at a vertex `S6b`, and `S6c`.
  Strict still lifes by size n = 6…16: **4, 2, 7, 9, 27, 45, 228, 851, 3388, 12255, 47578**
  (`$S/sl 16 -s`, ≈30 CPU-min; `still_stats.py`). The ratio is ≈3.9 per added cell from n = 12 on. All still lifes,
  including pseudo ones, that are R-connected (graph distance ≤ 2), n = 6…14: 4, 2, 7, 9, 27, 45, 717, 2177, 7598 (`$S/sl 14`).
- **[proved]** Layer thickness of strict still lifes (minimum over the 4 diagonals) at n = 16: 1 layer 15,
  2 layers 1690, 3 layers 20757, 4 layers 20514, 5 layers 4501, 6 layers 100, 7 layers 1. One-layer (kagome) still lifes exist for
  n = 6, 9, 11, 12, 13, …; the 2D search (`$S/osc 1 24 -k`, all R-connected, n = 6…24):
  1, 0, 0, 1, 0, 1, 2, 3, 4, 8, 15, 30, 58, 130, 253, 452, 1217, 2192, 4788. Cross-check: identical to the 3D one-layer subset for n ≤ 14.
- **[proved]** **The vertex star is a closed vessel.** The 12 faces incident to one lattice vertex form a 5-regular graph
  (8 triangles, one per cube corner); any cell outside it has ≤ 2 neighbours in it, so it can never be born. The 4096-state
  "star automaton" has 107 non-empty still lifes and 195 two-cycles, and every state settles within 3 generations (2750 die).
  Up to symmetry, 10 still lifes and 14 period-2 oscillators live entirely inside one star, including the vertex star itself
  `S12a` (12 cells, full O_h), three of the four 6-cell still lifes, and 11 of the 13 smallest oscillators (`vertex_star.py`).
  Most of the small fauna is the cube or a piece of a vertex star.

**Oscillators: they exist, and they are everywhere**
- **[proved, exhaustive]** Period 2: the smallest union is 9 cells; classes by union size 9, 10, 11, 12, 13: **3, 6, 4, 11, 10**
  (`$S/osc 2 13`, 11 min). The smallest phase is 6 cells (`P2.6a`: 3 stator cells plus a 3-fold "propeller" rotor of 6).
  All 13 with union ≤ 11 are *flips* (phase 1 is congruent to phase 0), and their rotors are perfect matchings of **hinges**:
  a live face swings 90° onto a face sharing an edge. For larger p2 from soups this holds for only about half (88/170).
- **[proved, exhaustive]** No period-3 oscillator has union ≤ 12 (`$S/osc 3 12`, 20 min), and none of period 4 has union ≤ 10 (`$S/osc 4 10`).
  The smallest from soups: p3 union 13 (`P3.11a`), p4 union 14 (`P4.11a`). Hence **the smallest p3 has union exactly 13** (lower bound exhaustive, attained by `P3.11a`; uniqueness at 13 unchecked).
- **[measured]** Soups in octahedral vessels (26,900 soups, L1 radius 5–9, ρ = 0.25–0.6, `harvest.py`) leave oscillators in 11%
  of runs. Object periods seen: **1–16, 20, 22, 48, 66**. Recurrent high-period objects: `P14.17a` (union 24, 88 times),
  `P16.15a` (union 30, 37 times), `P10.15a` (15), `P15.22a` (11), `P22.20a` (6), `P11.23a` (4); common low periods: `P3.13a` (165),
  `P5.17a` (149), `P2.6a` (119). `P11.23a` and `P13.22a` have prime periods.
  `P48.34a` (56 cells) and `P66.27a` (45 cells) are single neighbour-connected objects whose rotors are not composites:
  50 of 56 and 40 of 45 cells carry the full period. `P10.17a` and `P14.20a` have no stator at all (36 cells, all moving).
- **[measured]** The most common ash (3D soups): cube `S6a` (4024), vertex star `S12a` (2755), `S12i` (928), `S9a` (422).

**Kagome automaton (one layer, 6 neighbours)**
- **[proved]** The smallest kagome oscillator is period 2 with union 18 (a 12-cell stator around a hexagon whose alternate
  cells blink: a triangle rotating 60° each step), and it is the only one with union ≤ 18. There is no kagome p3 with union ≤ 18
  (`$S/osc 2 18 -k`, `$S/osc 3 18 -k`).
- **[measured]** Soups on a 24 × 24 torus (1728 cells, 300 per density, `kagome_soup.py 24 300 3 --census`): lifetime and ash density
  both peak near ρ ≈ 0.6–0.75 (median μ ≈ 35, ash ≈ 0.20 of cells). μ (median) = 1, 3, 6, 13, 26, 35, 35, 34, 19 at ρ = 0.05, 0.2, 0.3, 0.4,
  0.5, 0.6, 0.7, 0.8, 0.9. Lifetime grows only logarithmically with area (mean 4.6 → 11.9 from N = 4 to 16 at ρ = 0.4).
  Ash is hexagons (`KS6a`, ~38% of objects), then `KS9a`, `KS11a`. Kagome oscillators are rare and large (soups: p3 ≥ 33 cells,
  p4 ≥ 27); at ρ ≥ 0.5 the ash forms R-connected networks of hundreds of cells, some wrapping the torus.

**Legacy ash** (`legacy_ash.py`; every final state has full O_h symmetry)
- **[measured]** Side 9 (54 cells) = one cube `S6a` at the centre + **8 kagome hexagons, one on each `{111}` face**, at (±7,±7,±7).
  Side 11 (36) = **6 cubes at the 6 octahedron vertices** (±20, 0, 0)… Side 10 (264) = **18 vertex stars `S12a`** (12 isolated, 6 packed
  into a 72-cell pseudo still life at the centre) + 6 × `S8b`. Side 8 (384) = one O_h-symmetric cluster of twelve 32-cell
  still lifes `S32a`.

**Thickness: the critical thickness is 3 layers** (m-layer `{111}` slab on an N × N in-plane torus, 3N²m cells, ρ = 0.4,
`thickness.py`; mean lifetimes τ̄ to the final cycle)
- **[measured]** m = 1: τ̄ = 4.6, 6.5, 8.3, 10.2, 11.9 for N = 4, 6, 8, 12, 16. m = 2: 44, 53, 61, 74, 82, 92, 101 for N = 4, 6, 8, 12, 16, 24, 32.
  Both grow **logarithmically** in area: independent local deaths, no sustained chaos.
- **[measured]** m = 3: τ̄ = 75, 488, 2592, 13598, 76458 for N = 3…7 (200/100/100/100/50 soups). m = 4: 149, 2780, 33657 (N = 3, 4, 5).
  m = 5: 246, 9701 (N = 3, 4). For N ≥ 8, 39/40 (N = 8) and 40/40 (N = 12) m = 3 soups and 20/20 m = 4 soups (N = 8)
  had not settled after 5×10⁴ generations, holding density ≈ 0.47. That is higher than the 3D bulk (≈ 0.30): thin slabs are "all surface".
  [Corrected 2026-11-13 (audit, finding W2): the 3D bulk is 0.4155 (re-run: 0.415516 ± 0.000003 on 64³), not 0.30, which came from the miscount corrected in the first entry. Slabs are dense because faces are (face density ≈ 0.51); asymmetric confined chaos is 0.434.]
  **ln τ̄ is linear in N, not N²**: slope ≈ 1.7 per unit N for m = 3 (1.87, 1.67, 1.66, 1.72), ≈ 2.7 for m = 4, ≈ 3.7 for m = 5.
- **[measured]** Mechanism: in 30/30 soups (N = 5, m = 3) and 30/30 (N = 4, m = 4), death came right after the first
  **transverse T3 firewall**: three consecutive empty `{111}` layers along one of the *other* three diagonals cut the slab
  (median 99 resp. 44 generations before death, at 94% resp. 98% of the lifetime), and at death all three transverse directions were cut.
  For m = 2 that is not how death happens: 6/30 soups die without any firewall (`slab_firewall.py 5 3 30 0.4 31`, `… 4 4 30 0.4 32`, `… 6 2 30 0.4 33`).
- **[conjecture]** A slab of thickness m ≥ 3 is metastable and dies only by a spontaneous transverse firewall, a dead band of
  ≈ 3 × (cross-section of one transverse layer) ∝ m·N cells. Hence ln τ ≈ σ·m·N, exponential in the area of a *transverse cut*
  and not in the slab's volume or face area. The same reading fits the octahedral vessels: ln τ̄ = 3.9, 4.6, 5.6, 6.7, 8.5 for
  L1 radius 5–9, roughly ∝ R² (cross-section) (`harvest.py`). Test at larger N with the Rust engine: (i) ln τ ∝ N, not N²;
  (ii) slope ∝ (m − m₀) with m₀ ≈ 1.3; (iii) the first transverse firewall precedes death.

## 2026-11-12 — engine online; legacy series fully reproduced (lead)

- **[measured]** `engine/` (Rust, AVX-512 bit-sliced) matches the oracle state-for-state and
  all six legacy logs at every generation (`python3 engine/scripts/check_golden.py`; add
  `<log> <H>` for the big ones). Side 12 and 13 match in open space *and* on the legacy torus:
  **the original's lifetimes for sides 8–13 are all free of torus artefacts.**
  Side 13's 169,049 generations take ≈1 s. Single core ≈4×10¹⁰ cell-updates/s.
- **[measured]** Side 13 peels exactly like side 11 (`gump run --cube 13 --events F --every 50`):
  hull radius 37 → 33 within 50 generations, then layer |s|=33 dies at ≈130,200, 31 at 145,850,
  29 at 156,800, 27 at 166,650, 25 at 168,200, final collapse 169,049. Plateau populations
  7731, 6374, 5189, 4160, 3288 = 0.37–0.39 × the cell count of the current hull.
- **[measured]** Residence times at each radius, symmetric octahedra, one sample each:
  side 11: R=27: 3285, 25: 187, 23: 319, 21: 422 · side 13: R=33: 130k, 31: 15.6k, 29: 10.9k,
  27: 9.9k, 25: 1.5k, 23: 0.85k. Noisy (single draws) but rising ≈3× per layer of radius.
- **[measured]** (engine agent, 48 runs per radius, p=0.3 asymmetric octahedral soups)
  median lifetime 17, 110, 2846, ≈1.4×10⁵ for R = 6, 8, 10, 12; none of 48 halt within 2×10⁵
  at R = 14, 16. Asymmetric soups at R≈12 already outlive the symmetric side-13 cube (R=33) —
  the symmetry penalty predicted by the face-extinction model, qualitatively.
- **[measured]** Oscillators exist: periods 2, 3, 4, 5, 8, 14 seen in soup ash
  (`gump run --soup 0.3 --radius 8 --rng 20` → period 14, 18 cells).
- Web app (`web/`) v1 verified: `node test/run.mjs` 49/49; GPU path bit-exact on the golden logs.

## 2026-11-12 — closed cubes 14 and 15; web views (lead)

- **[measured]** Closed cube side 14: **4,460,298** generations, ends in a period-2 oscillator
  of 528 cells. Side 15: **37,367,092** generations, ends **extinct** (population 0).
  (`research/experiments/cubes.sh 14 15`; layer-death events in `research/scratch/cubes/`.)
  Both peel layer by layer like 11 and 13. Series for n = 11…15: 4218, 24286, 169049,
  4460298, 37367092; ln τ = 8.35, 10.10, 12.04, 15.31, 17.44 — about +2.3 per side, single
  draws each, so not yet able to separate ln τ ∝ n from ∝ n².
- **[measured]** Vertex star re-verified independently by the lead: a star cell sees 5 star
  cells, no outside cell sees more than 2, all 4096 states stay inside and settle within
  3 generations (2750 die; still lifes of 6, 7, 8, 9, 12 cells; period-2 with 6–9 cells).
  In the dual (bond) picture the star is the 12 edges of a dual cube and the closed cube is
  the 6 bonds at a dual vertex.
- **[conjecture → lead]** From the web viewer's `{111}` slicer, one snapshot (side 11, gen 1500):
  the outermost face layer's live cells form a ring with an empty middle and empty corners.
  If typical, a face is not a homogeneous 2D layer. Being measured by the peeling study.

## 2026-11-12 — the chaotic state as a phase; gump's neighbourhood in rule space (phase agent)

Code, commands and `rules.csv`: `research/phase/README.md`. Figures: `research/figures/phase_bulk.png`,
`phase_spread.png`, `phase_rulemap.png`. Numpy stepper `research/phase/gl.py` is bit-exact vs the engine (`check_numpy.py`).

**Bulk (tori, which have no faces)**
- **[measured]** Steady density **ρ\* = 0.41552 ± 0.00002** on 16³, 32³ and 64³ tori (3×10⁴ gens each, block errors), the same
  at all sizes. **It is not 0.39**: see the vessel item below. Global-density susceptibility χ = N·Var(ρ)/ρ(1−ρ) = 3.16 ± 0.05, size-independent
  (`$G run --soup 0.3 --torus 64 --rng 7 --gens 30000 --every 1 --lite --format csv --out long64.csv`).
- **[measured]** Local statistics (4 × 64³ snapshots, 300 gens each, `bulk.py`): survival probability of a live cell s = 0.500, birth probability
  of a dead cell b = 0.356, turnover (cells changed per cell per gen) 0.4157 ≈ ρ\* (because s ≈ ½); mean live run 1.99 gens, dead run 2.79,
  both close to geometric; single-cell autocorrelation 0.144, 0.066, 0.043, 0.019 at lags 1–4 (correlation time ≈ 1 gen).
- **[proved]/[measured]** Mean field f(p) = (1−p)P[Bin(12,p)∈{4,5}] + p·P[Bin(12,p)∈{3,4,5}] has fixed points 0, 0.178 (unstable) and
  0.444 with slope −1.55, i.e. **unstable**: the mean-field attractor is a 4-cycle 0.319 → 0.486 → 0.369 → 0.511 (mean 0.421). The first step of
  uncorrelated soups matches f(p0) to ≤ 0.001 at all 25 densities, as it must. On the lattice the uniform mode is stable but rings:
  global-density autocorrelation −0.44, −0.10, +0.34, −0.23, 0.0, +0.12 (spectral peak period ≈ 2.7–3), lag-1 return slope −0.44.
- **[measured]** The correction is overdispersion, not centre–neighbour correlation: mean neighbour count is 5.03 (live) / 4.96 (dead) vs
  binomial 4.99, but the variance is 3.67 / 4.17 vs 2.91 (×1.26 / ×1.43). A beta-binomial with intra-neighbourhood correlation 0.035–0.04
  puts the fixed point at 0.416–0.42 with slope −0.6…−0.8 (stable). One measured number fixes both the density and its stability.
- **[measured]** Basin: whole-torus soups (5 per point, 32³–128³, 3000 gens) reach chaos iff 0.12 ≲ p0 ≲ 0.66. **Both edges sit where the
  first-step density f(p0) ≈ 0.06**; outside, the soup drops to sparse periodic debris (absorbing). Near the edges chaos nucleates locally
  and invades (one 64³ soup at p0 = 0.66 sat at ρ ≈ 0.03 with confined active pockets for > 2000 gens before invading).
- **[measured]** Correlations are very short and **isotropic**: S(k) (12 snapshots of 64³, `sk.py`) agrees in ⟨100⟩, ⟨110⟩ and ⟨111⟩ cones at
  every |k| within errors; Ornstein–Zernike fit S = 0.40 + 2.77/(1 + ξ²k²), **ξ = 0.68 ± 0.01 cube**, S(k→0) ≈ 3.2 = χ. Real space: opposite faces
  of a cube +0.09, corner-sharing coplanar neighbours −0.02, edge-sharing perpendicular +0.02, one cube along [111] −0.001 ± 0.0003; nothing
  above 0.003 beyond 2 cubes. No in-layer vs cross-layer anisotropy is detectable despite the 6 / 2+2 / 1+1 coupling.
- **[measured]** Torus lifetimes (40 soups each, `ensemble --torus N --runs 40`, cap 10⁶): N = 3: 49, N = 4: 1.4×10³, N = 5: 9×10⁵ (MLE, 27 of 40 ended),
  N = 6, 7, 8: 0 of 40 ended. ln τ / N² = 0.43, 0.45, 0.55: consistent with death needing a transverse cut of area ∝ N².

**Chaos proper**
- **[measured]** Damage from one flipped cell (40 trials, 64³, `damage.py`): **40/40 spread, none healed**. The cloud is a **sphere**: Euclidean front speed
  0.826 ± 0.002 (axes), 0.874 ± 0.002 (face diagonals), 0.846 ± 0.002 (body diagonals) cubes/gen. That is 83% of the speed limit along axes but only
  49% of it along ⟨111⟩ (limit √3). Damage crosses `{111}` planes freely; T2 is a property of the vacuum, not of the chaos.
- **[measured]** Chaos invading vacuum (planar fronts on a 72³ torus, 4 trials, `front_planar.py`): **{100} 0.177 ± 0.001, {110} 0.165 ± 0.001, {111} exactly 0**
  cubes/gen. Fronts are 5× slower than damage. The growth shape of a seed is the Wulff-like shape of v(n) = 0 on {111}: the octahedron, approached
  at ~0.17 cubes/gen (box seed: axis tips advance 0.18 cubes/gen until the hull vertex; `front.py`).

**Confined chaos: the 0.39 is a symmetry artefact**
- **[measured]** Asymmetric octahedral soups (p 0.35, L1 radius 33, gens 2000–30000): density **0.434 ± 0.001**, with the face layer **enhanced** (0.51–0.52,
  next layer 0.44, then bulk 0.40–0.42; 6 soups). The O_h-symmetric side-13 cube in the same hull: 0.390 (time average, 1.2×10⁵ gens), with cells on
  mirror planes at **0.31** and off-plane cells at 0.39 (15 snapshots). So the "≈0.39" in STATUS describes symmetric seeds; the bulk phase is 0.4155 and
  confined asymmetric chaos is denser still because faces are denser. The face enhancement also explains the 0.47 of thin slabs (atlas entry).
  Peeling agent: an asymmetric face is a dense layer, not a ring; the ring/empty-middle snapshot may be a mirror-plane effect.

**Rule space** (960 rules: B ⊆ {4..7} non-empty × S ⊆ {2..7}; `survey.py`, `rulemap.py`, table `research/phase/rules.csv`)
- **[measured]** Whole-torus soups (24³, 4 densities): chaos 421, slow 15, freeze 132, die 392. Unconfined chaos is generic once 4 ∈ B and B has a second count:
  rules with chaos per birth set (of 64 S-sets): B4 13, B45 47, B46 37, B47 27, B456 61, B457 59, B467 49, B4567 63; without 4: B5 2, B56 18,
  B57 11, B567 31, B6 1, B67 2, B7 0. Chaotic densities 0.30–0.59.
- **[measured]** Confined chaos is the discriminating property. In an octahedral vessel (L1 radius 10, 16 soups), 146 rules have median lifetime ≥ 10³;
  142 of them have 4 ∈ B. Gump (median 3420) is longer-lived than 832 of the 960. **B45/S345 is one of the 50 minimal elements of the long-lived set:
  removing any bit collapses it** (B4/S345 104, B5/S345 21, B45/S45 20, B45/S35 22, B45/S34 36 gens) **while adding most bits extends it**:
  B456/S345 5.7×10³, B457/S345 8.9×10³, B45/S2345 ≥ 10⁵, B45/S3457 ≥ 10⁵. Gump sits on the edge of the region, at a corner, not in its interior.
  [Note 2026-11-13 (audit, finding I5): 10⁵ is the survey's cap; the next bullet re-ran B45/S3457 with a cap of 10⁶.]
- **[measured]** B45/S3457 is the neighbour to look at: medians 79, 3.5×10⁴, ≥ 10⁶ for radius 6, 8, 10 (gump: 28, 254, 3420), i.e. ~100× per radius step vs
  gump's ~10×; torus density 0.458. B45/S2345: 90, 1203, 6×10⁵. (`$G ensemble --soup 0.35 --radius 6 --runs 16 --vary rule=… --vary radius=5,7,9`.)
  [Corrected 2026-11-13 (audit, finding I5): the command above does not give these numbers; the radii are 6, 8, 10 (not 5, 7, 9) and the cap is 10⁶. Reproduces exactly (79, 34,970, and 16/16 still running at 10⁶ for radius 10): `for R in 6 8 10; do $G ensemble --soup 0.35 --radius $R --runs 16 --rng 1 --vary 'rule=B45/S3457' --gens 1000000; done`, median of `cycle_start` per radius.]
- **[measured]** B45/S3456 (adding survival at 6) is qualitatively different: a **glassy** rule. On a 32³ torus activity decays from 5% to 0.2% of cells per gen
  over ~5000 gens at density 0.51, and the whole torus locks into cycles of period 120, 2280, 3312, 3960 (4 soups). In vessels it freezes fast (59).
- **[measured]** Oscillator-rich neighbours: in B567/S23456 85% of vessel soups end in a period > 1 cycle (gump 19%) and live long (1.7×10⁴); periods up to
  140 (B456/S4567), 98 (B467/S34567).
- **[measured]** Birth at 3 (tori only): B34/S345 (ρ 0.40), B35/S345 (0.41), B345/S345 (0.43), B3/S345 (0.36) sustain chaos from every p0 incl. 0.7, and invade
  vacuum across `{111}` planes too (a 24-cube vacuum gap filled within 40 gens). No confinement, no octahedra.

## 2026-11-12 — density, again (lead)

- **[measured]** Lead's independent check of the phase study's headline: 32³ torus soup,
  generations 1000–6000, mean density **0.4152** (`gump run --soup 0.3 --torus 32 --rng 5
  --gens 6000 --every 20 --lite --format csv --out F`). The earlier entries' "bulk ≈0.39–0.40"
  came from O_h-symmetric seeds and the legacy torus run; the bulk value is 0.4155, symmetric
  octahedra sit at ≈0.39 because mirror-plane cells are depleted, and asymmetric octahedral
  soups have *denser* faces (≈0.51) than bulk. So "the face is hot" is true for asymmetric
  seeds and was wrong-for-the-right-reason in my first entry.

## 2026-11-12 — reading the smallest fauna as text (lead)

`gump show --cells F [--orbit]` draws a pattern as its stack of kagome layers. Read that way:

- **[measured]** closed cube (S6a) = two triangles in *adjacent* layers (3 + 3).
- **[measured]** S6b = two triangles with one *empty* layer between them (two cube corners
  meeting at a vertex).
- **[measured]** vertex star (S12a) = triangle + kagome hexagon + triangle (3 + 6 + 3):
  it is S6b with the kagome-hexagon still life slotted into the gap. Both halves are still
  lifes on their own, and so is their union.
- **[measured]** the smallest oscillator (P2.6a, "propeller") = one fixed triangle, and in the
  next layer the hexagon's two alternate triangles taking turns: a blinking half-star.

## 2026-11-12 — how chaos dies: one face law, two kinds of cut (peeling agent)

Code, tables, method: `research/peeling/README.md`. New tool `peeling/rep.c`: 64·W bit-sliced replicas on any finite
cell graph, bit-exact vs gump (`python3 research/peeling/validate.py`). Key new geometry: slabs on a **skewed in-plane
torus** (face area A = 3·N1·N2 independent of thickness m; on gump's cubic torus A ≥ 3(m+3)², and such faces never peel).
Runs are 512 per batch unless stated (p = 0.4 slabs, 0.3 octahedra); censored runs enter through exposure-time MLEs;
CIs are 95% (χ²). Figures: `research/figures/peel_face_law.png`, `research/figures/peel_cuts.png`.

**Faces.**
- **[measured]** Flat faces (slab, m = 8, no edges) die at **τ_face = exp[(−0.09 ± 0.06) + (0.209 ± 0.002)·A]**
  generations, A = cells in the face layer; 8 near-square tori, A = 27–90, τ from 2.8×10² to 1.6×10⁸; residuals ≤ 0.18 in
  ln τ. Waiting times are exponential for A ≥ 36 (CV 0.96–1.05, KS p 0.5–0.96); not for A ≤ 27 (transient-dominated).
  Prefactor ≈ 1 generation. Independent of thickness once m ≥ 7: first peel at A = 48 is 9.9, 10.4, 10.3, 10.4, 10.4 ×10³
  for m = 7, 8, 9, 10, 12. Area, not shape: 4×4 and 3×5 tori agree; elongated ones (2×8, 3×8) die sooner, by transverse
  firewalls (below). (`python3 research/peeling/slabs.py 4 4 8 400000`; table `peeling/slab_area.csv`.)
- **[measured]** **Octahedral faces obey the slab law; edges and corners do not dominate.** Asymmetric soups, first peel
  after t0 = 200, ×8 faces: τ_face = 1.3×10⁴, 7.3×10⁵, 7.1×10⁷ at A = 45, 63, 84 (R = 9, 11, 13) vs slab law 1.1×10⁴,
  4.8×10⁵, 3.9×10⁷ — octahedral faces are 1.2–1.8× *more* robust. The per-face hazard over every hull state of every
  history (pooled, faces of A = 14–84) follows the same line. First peels are exponential (CV 1.06 at R = 11).
  (`python3 research/peeling/octa.py 11 0.3 1000000; python3 research/peeling/octa_hazard.py; python3 research/peeling/octa_report.py`.)
  [Corrected 2026-11-13 (audit, finding W3): the first-peel table counted runs whose hull had already shrunk before t0, whose faces are smaller (R = 9: CV 1.26, 1,620). `octa_hazard.py` now keeps only runs with the full hull at t0 and `octa_first.csv` is regenerated (`python3 research/peeling/octa_hazard.py; python3 research/peeling/octa_report.py`). R = 9, 11, 13 now give means 2.29×10³, 9.95×10⁴, 9.4×10⁶ (R = 9: 295 runs, CV 1.03; the engine with the lead's protocol gives 2,459 ± 97), i.e. τ_face = 1.8×10⁴, 8.0×10⁵, 7.5×10⁷ and factors 1.7, 1.7, 1.9 over the slab law: "1.2–1.8× more robust" should read **1.7–1.9×**, in line with the lead's 1.6–1.9×. The next bullet's p = 0.2 row ("median A 35, CV 4.3") and the symmetric first-peel rows moved with the same filter (p = 0.2 now has only 6 established runs); the per-face hazards, which the A/7.7 fits use, are unchanged.]
- **[measured]** Once the hull is filled, density does not matter: R = 11 first-peel means 0.91, 1.08, 1.00, 1.04 ×10⁵ for
  p = 0.3, 0.4, 0.5, 0.6. Below that the chaos never fills the hull: p = 0.2 peels from small faces (median A 35, CV 4.3),
  p = 0.15 dies in the transient in 93% of soups.
- **[measured]** **O_h symmetry: same law, effective area A/7.7, not A/6.** Symmetric soups (cube-centred, R = 23–35;
  128–256 runs): ln τ = −0.14 + 0.0272·A over per-state hazards with A ≥ 198, i.e. A_eff = A/(7.7 ± 0.2) against the slab
  constant. Vertex-centred symmetric soups (as even closed cubes) live 1.5× longer at equal face area (R = 28 vs 27: 5.8 vs
  4.0 ×10³; 32 vs 31: 8.2 vs 5.4 ×10⁴). **[conjecture]** the extra loss beyond A/6 is the phase study's depleted mirror-plane cells.
  [Note 2026-11-13 (audit, finding I8): the face-law figure (`research/peeling/figures.py`, `K_SYM`) plots symmetric faces at A/8.0, not the A/7.7 quoted here.]
- **[measured]** Time-averaged occupancy of the side-11 cube's outer face over its 3000-gen plateau (150 samples, 8 faces):
  interior 0.47, edge rows 0.38, corners 0.22 — **not a ring**; the viewer's ring was one snapshot. A face dies suddenly:
  90–230 live cells until ≈10 generations before extinction, last survivors 2–3 rows from the edge (side 11 at gen 3289,
  side 13 at 130,191) (`python3 research/peeling/faceocc.py OUT 200 3200 20 -- --cube 11`, `python3 research/peeling/lastcells.py 3200 3300 27 -- --cube 11`).

**Thin slabs and the cheapest cut** (the lead's hypothesis).
- **[measured]** m′ ≤ 2 sustains no chaos (≤ 10³ gens at any A tested). For m = 3–6, slabs die by a **transverse T3 firewall**
  with ln τ_fw = −1.4 + 0.54·N·m + 0.22·N (14 batches, N = 4–7, rms residual 0.27), i.e. ≈0.12 per cell of the 3-layer
  band that must die. Faces cost 0.209 per cell — **no single constant per dead cell** (ratio ≈ 0.55), though per cell of
  cross-section the firewall costs ≈0.36 vs 0.21. The cheapest-cut picture holds qualitatively: the first event switches from
  firewall to peel at m ≈ N (N = 4: firewall first in 397/512 at m = 4, 175 at m = 5, 35 at m = 6; N = 5: 426 at m = 5, 93 at m = 6)
  (`peeling/slab_fw.csv`). For an octahedron the faces are its smallest {111} sections, so peeling wins.
- **[measured]** A peeling slab does not die "at" a critical thickness: the wait per peel is flat for m′ ≥ 6–7, falls 2–20× at
  m′ = 4–5 as the firewall channel opens, and histories end at m′ = 2–4 (A = 48: 117 extinct, 116/172/94 freeze at m′ = 2/3/4),
  after a transverse firewall in 510/512 (`peeling/slab_thickness.csv`, `slab_end.csv`).

**Bulk.**
- **[measured]** Whole-torus soups (no faces) die by sudden global freeze or extinction, not by firewalls (0/512 and 6/351
  had a firewall first): mean life 1.18 [1.08, 1.28] ×10³ at N = 4, 8.7 [7.9, 9.7] ×10⁵ at N = 5, none of 512 within 10⁶ at
  N = 6, 7, 8 (mean > 1.7×10⁸). The bulk channel matters only below ≈ 600 cells (`python3 research/peeling/torus.py 5 0.3 1000000`).

**Closed cubes.**
- **[measured]** With nothing fitted to the cubes, the symmetric-soup law (residence at hull radius R = exponential with mean
  τ_sym(A(R)), ×1.5 for even n) accounts for the series: the observed lifetimes of n = 11–15 sit at quantiles 0.37, 0.45, 0.33,
  0.93, 0.73 of the predicted distributions, and the 24 residence times / predicted means are consistent with Exp(1) (KS p = 0.71).
  The first plateau is 68–80% of the expected life, so single cubes scatter by ~3×. The growth is exp(c·A_eff) with A ∝ n²:
  ln τ ≈ quadratic in n, as the first notebook entry guessed (`python3 research/peeling/cubes_report.py`; `peeling/cube_lifetime.csv`).
- **[conjecture]** n = 16: mean 2.4×10⁸, 90% interval [3.9×10⁷, 6.3×10⁸]; n = 17: ≈6×10⁹.

## 2026-11-12 — why symmetric seeds are different: mirror depletion and lockstep (phase agent)

Scripts `research/phase/sym.py`, `sym_torus_life.sh`, `fig_sym.py`; figure `research/figures/phase_symmetry.png`. Symmetric torus soups are
made by `sym.py soup G N 0.35 RNG out.gump` (mirrors taken mod 2N) and then run by the engine. The engine's own `--sym` on a whole torus did not give
symmetric chaos in a quick test (the soups died at gen 2). It was not investigated further. Vessels use the engine's `--sym` (open space).

- **[measured]** Density by symmetric-site class, 32³ tori, groups d2h / th / td / oh, 2 soups × 12 snapshots each, after 3000 gens:
  off mirrors 0.41–0.42 (bulk); on one coordinate mirror **0.345–0.353**; on one diagonal mirror **0.322–0.331**; on two coordinate mirrors (an axis)
  0.226–0.263; on two diagonal mirrors 0.200; on two coordinate + two diagonal mirrors (the [100] axes of O_h) 0.363
  (`sym.py classes G 32 snaps…`). The depletion is confined to the plane. Half a cube off a diagonal mirror the density is 0.378, and one cube off it is back
  at 0.42–0.43, consistent with ξ ≈ 0.7.
- **[proved]** The lead's mechanism is right in kind. A site's 12 neighbours fall into orbits of its stabiliser, and all cells in one orbit share a state.
  On one coordinate mirror the orbits are 4 pairs + 4 singles, so for independent orbits Var(n) is 1.67× binomial. On one diagonal mirror they are
  5 pairs + 2 singles (1.83×), on an axis 4+2+2+2+2 (2.67×), and on two diagonal mirrors 4+4+2+2 (3.33×). The orbit mean field (each orbit an
  independent Bernoulli, self-consistent over all sites, time-averaged over the mean-field 4-cycle, no free parameters; `sym.py mf G 6`) gives:

  | site class | orbit mean field | measured |
  |---|---|---|
  | bulk | 0.421 | 0.4155 |
  | 1 coordinate mirror | 0.37–0.39 | 0.35 |
  | 1 diagonal mirror | 0.38 | 0.32–0.33 |
  | axis (2 coordinate) | 0.25 | 0.23–0.26 |
  | 2 diagonal | 0.24 | 0.20 |

  It gets the ordering right, gets the doubly-fixed sites right, and gives about half of the single-plane depletion.
  **Exception:** on the 4-mirror [100] axes all three orbits have multiplicity 4, so n ∈ {0, 4, 8, 12}. Then n = 4 falls in both the birth and the
  survival window, and those sites are *less* depleted (measured 0.363, mean field 0.447). The arithmetic of the window matters, not only the variance.
- **[measured]** The side-11/13 "ring" is the time-averaged structure of a symmetric face (side-13 cube, outer layer R = 33, 15 snapshots × 8 faces):
  - centroid (on 3 diagonal mirrors) 0.19, corners 0.16, medians 0.26, face edges (coordinate mirrors) 0.29;
  - a ring of 0.42–0.44 between them;
  - the whole face averages 0.37.

  An asymmetric face is uniform at 0.50–0.53 (6 soups at R = 33). So the symmetric face is a depleted, mirror-cut ring.
- **[measured]** Lifetimes (median; vessels: p 0.35, 32 soups at R ≤ 14 and 16 at R ≥ 16, cap 10⁶; tori: 8 soups, 40 for asymmetric N ≤ 5):

  | vessel R | c1 | d2h | td | oh |
  |---|---|---|---|---|
  | 8 | 234 | 24 | 2.5 | 3 |
  | 10 | 3.8×10³ | 133 | 9 | 6 |
  | 12 | 1.1×10⁵ | 567 | 13 | 17 |
  | 14 | ≥ 10⁶ | 1.2×10⁴ | 30 | 20 |
  | 16 | | 6.2×10⁵ | 38 | 32 |
  | 20 | | ≥ 10⁶ | 370 | 88 |
  | 26 | | | 6.5×10³ | 1.0×10³ |
  | 33 | | | ≈ 10⁶ | 2.5×10⁵ |

  Tori with no hull and no faces show the same pattern. Lifetime ≈ 10⁶ is reached at N ≈ 5–6 (c1), 8 (d2h), 13–16 (td), 16 (oh). Medians:
  d2h 1.2×10³ at N = 6; td 22, 93, 3.1×10⁴ at N = 6, 8, 12; oh 12, 41, 786, 6×10⁵ at N = 6, 8, 12, 16.
- **[measured → conjecture] Rule of thumb for the peeling study: a symmetric system lives like an asymmetric one with c × (its fundamental domain)
  of volume, c ≈ 1.5–3.5.** Match radii (vessels) or sizes (tori) at equal median lifetime and take the volume ratio:
  - vessels: d2h 0.41–0.46 of the volume (c ≈ 3.3–3.7), td 0.064–0.070 (c ≈ 1.5–1.7), oh 0.044–0.050 (c ≈ 2.1–2.4);
  - tori: d2h ≈ 0.25 (c ≈ 2), td ≈ 0.05 (c ≈ 1.2), oh ≈ 0.03 (c ≈ 1.5).

  So symmetry acts mostly by **lockstep**: a symmetric system has only one fundamental domain's worth of independent chaos, and it dies when that does.
  It acts the same way without a hull. Mirror planes are depleted but do not act as weak planes in any strong sense: a mirror domain lives *longer* than
  an asymmetric box of the same volume (c > 1), not shorter. The face picture still matters for vessels (d2h faces are uncut but in lockstep; td/oh faces
  are also cut along their medians), but the order of magnitude follows from |G| alone. For the legacy series: side 13 (R = 33, oh) lived 1.7×10⁵,
  close to oh's median here (2.5×10⁵), and like an asymmetric vessel of R ≈ 12.

## 2026-11-12 — independent check of the face law; two studies reconciled (lead)

- **[measured]** Through the main engine only (`python3 research/experiments/verify_face_law.py 9 240`
  and `… 11 120 2000000`): asymmetric octahedral soups, p = 0.35, wait from generation 60 to the
  first face death among runs whose hull is still the full octahedron.
  R=9 (A=45): mean 2.60×10³ ± 0.17×10³ (221 runs), CV 1.03 → τ_face 2.1×10⁴.
  R=11 (A=63): mean 9.4×10⁴ ± 0.9×10⁴ (118 runs), CV 0.99 → τ_face 7.5×10⁵.
  Waits are exponential; slope between the two radii 0.199 ± 0.006 per face cell (study: 0.209 ±
  0.002 on flat slabs); octahedral faces 1.6–1.9× tougher than the flat-slab line. Agrees.
  [Note 2026-11-13 (audit, finding I1): the 0.199 comes from the 240-run R = 9 sample, which was a 1.7σ high draw (reproduced exactly with the same seeds: 2,599.8 ± 174.9; 1,024 soups give 2,313 ± 75). With 2,300 the slope from R = 9 to 11 is 0.212. The independent anchor is the engine-only end-game check, `face_endgame_check.py`: −ln h/A = 0.2183 at A = 45.]
- **[measured]** Engine bug found by the phase study and reproduced: `--sym` soups on a whole
  torus are overfilled (`gump run --soup 0.35 --torus 16 --sym oh --rng 3` → seed population
  11,388 of 12,288). Open-space symmetric soups unaffected. Reported to the engine.
- **Unresolved, probably compatible:** the peeling study binned the symmetric side-11 face
  coarsely (interior 0.47, edges 0.38, corners 0.22: "not a ring"); the phase study binned the
  side-13 face by symmetry class (centroid 0.19, medians 0.26, corners 0.16, band 0.42–0.44:
  "ring is real"). Both are consistent with a face whose mirror lines are depleted. An
  occupancy-map instrument has been requested to settle it.
- **[measured, two studies]** Why symmetric seeds die fast: mostly **lockstep** (one
  fundamental domain of independent chaos — holds on tori with no faces at all), with mirror
  depletion a second-order extra. Peeling study: effective face area A/7.7 for O_h (not A/6).
  Phase study: lifetime of a symmetric system ≈ that of an asymmetric one with c × (volume/|G|),
  c ≈ 1.5–3.5.

## 2026-11-12 — the face of a symmetric seed, settled (lead)

- **[measured]** `gump occupancy --cube 13 --from 10000 --to 110000 --layer 33` (re-run by the
  lead; 100,000 frames, the hull is at radius 33 throughout): the outer face of the
  O_h-symmetric side-13 cube is depleted at its centre (≈0.2), along the three lines joining
  the centre to the edge midpoints (0.2–0.3 against 0.4–0.5 either side) and at its corners;
  mean 0.42. `gump occupancy --soup 0.3 --radius 33 --rng 1 --from 10000 --to 110000 --layer 33`
  (engine agent's run): an asymmetric face of the same size is uniform at 0.52–0.54 out to the
  rim, only the three corners lower. So the "ring" seen in the viewer is real and is a
  property of the symmetric *state* (its mirror lines), not of faces. The phase study had this
  right; the peeling study's coarser bins averaged it away.
- **[measured]** Engine round three verified by the lead: 27 tests, 7/7 golden; `--sym oh` on a
  16³ torus now seeds 3,738 of 12,288 cells (0.30; ~256 independent orbits) and runs chaotic.
  `gump ensemble --layer-deaths` gives exact peel generations from packed ensembles;
  `engine/scripts/face_law.py` reproduces `research/experiments/verify_face_law.py`.

## 2026-11-12 — where the 0.209 comes from: the far tail of a living face's fluctuations (lead)

`python3 research/experiments/face_fluct.py 11 60000 1 2 3 4 5 6 7 8` and `… 13 150000 1 2`:
asymmetric octahedral soups, the population n of each outer face layer sampled every
generation, using only runs in which no face died (fixed geometry; 3 runs at R=11, 2 at R=13,
1.4M and 2.4M face-generations).

- **[measured]** A living face is overdispersed and left-skewed: mean 0.496 / 0.505 per site,
  variance 0.437 / 0.421 per site (binomial would be 0.25), skew −0.2; autocorrelation 0.5 at
  lag 1, gone by lag ~20.
- **[measured]** The empirical rate function I(x) = −ln P(n/A ≤ x) / A agrees between the two
  sizes where they overlap — I(0.15) = 0.127 (A=63) and 0.137 (A=84); I(0.25) = 0.084 and 0.092 —
  so P(n/A ≤ x) ≈ exp(−A·I(x)) with a size-independent I, as a large-deviation principle requires.
- **[measured]** A Gaussian with the measured mean and variance matches I(x) for
  x ≈ 0.15–0.25 but overshoots further out: at x = 0.06 the data give 0.175, the Gaussian 0.214;
  extrapolated to x = 0 the Gaussian gives 0.28–0.30.
- **[conjecture]** The face law's constant is I(0). Continuing the measured curve from
  x = 0.06 to 0 gives ≈0.20 (a linear continuation gives 0.204; the curve is flattening),
  against 0.209 ± 0.002 from extinction times. If so, a face's death needs no special
  mechanism: τ_face ≈ 1 / P(the face is empty under its ordinary stationary fluctuations),
  about one independent "attempt" per generation, which is why the law's prefactor is
  ≈1 generation. The "sudden collapse" is what the cheap last stretch of the rate function
  (below x ≈ 0.1) looks like in time. Caveats: an extrapolation, two sizes, five runs.
  A direct test: push the tail measurement to x → 0 at smaller A, or by importance sampling.

## 2026-11-12 — side 16 outlives its prediction; in symmetric faces the cost per site grows with size (lead)

- **[measured]** `research/experiments/cube_ckpt.sh 16` (checkpointed `gump run --cube 16`). At generation
  **1,025,000,000** the side-16 cube is alive: population 16,080, hull radius 42 on all four diagonals —
  *no face layer has died yet*. The run was stopped there by the session's limit on background jobs, not by the
  automaton. The state is kept in `research/data/cube16_gen1025000000.gump`; resume with
  `gump run --snapshot research/data/cube16_gen1025000000.gump` (≈10⁵ generations/s on one core).
- **The prediction failed at its stated confidence.** The peeling entry above gave mean 2.4×10⁸, 90% interval
  [3.9×10⁷, 6.3×10⁸], of which the first plateau (R = 42, A = 693) is ≈2.0×10⁸. An exponential wait with that
  mean survives to 1.025×10⁹ with probability e^−5.3 ≈ 0.5%. (The lead had written down 10⁹ beforehand as the
  point where the law would be in trouble.) In hindsight the series was already leaning: sides 14 and 15 sit at
  quantiles 0.93 and 0.73 of their predictions, and two single residences are 5.5× and 7.2× their predicted means
  (side 14 at R = 30; side 15 at R = 37, 33.2M generations against 4.6M) — a KS test over 24 residences does not see tails.
  [Corrected 2026-11-13 (audit, finding I8): with the mean 2.0×10⁸ the probability is e^−5.1 ≈ 0.6%.]
- **[measured]** The face is ordinary. `gump occupancy --snapshot research/data/cube16_gen1025000000.gump --from 0
  --to 20000 --layer 45`: 0.4–0.5 in six domains, 0.3–0.4 along the three mirror lines, 0.2 at the centre, 0.1–0.2
  in the corners; no cell frozen, no persistent structure protecting it.
- **[measured]** Fluctuations of the cubes' living outer faces, sampled every generation
  (`python3 research/experiments/sym_face_fluct.py FROM TO -- SEED`; all 8 faces are images of one, so one layer
  is read). J(x) = −ln P(n/A ≤ x); "c" = cube-centred, "v" = vertex-centred.

  | seed, window | R | A | mean /site | var /site | J(0.25) | J(0.20) | J(0.15) | J(0.10) | J/A at 0.25, 0.20, 0.15 (×10⁻³) |
  |---|---|---|---|---|---|---|---|---|---|
  | `--cube 13`, 200–130,000 | 33 c | 459 | 0.421 | 2.95 | 3.85 | 5.35 | 6.81 | 8.08 | 8.4, 11.7, 14.8 |
  | `--cube 14`, 200–2M | 36 v | 513 | 0.441 | 2.97 | 4.79 | 6.31 | 8.16 | 10.01 | 9.3, 12.3, 15.9 |
  | `--cube 15`, 2.5M–4.5M | 37 c | 570 | 0.435 | 2.81 | 5.05 | 6.80 | 8.85 | 10.90 | 8.9, 11.9, 15.5 |
  | `--cube 15`, 200–2M | 39 c | 630 | 0.441 | 2.76 | 5.72 | 7.71 | 10.10 | – | 9.1, 12.2, 16.0 |
  | side-16 checkpoint, 2M gens | 42 v | 693 | 0.454 | 2.83 | 6.73 | 8.98 | – | – | 9.7, 13.0, – |

  The variance per site is 6.4–6.9× the asymmetric face's 0.43 (six lockstep copies, a little more). At equal depth
  the cost **per site is not constant**: it rises 4–8% from A = 459 to 630 (cube-centred) and 4–6% from 513 to 693
  (vertex-centred), at every depth measured; J itself grows by 1.47 for an area ratio of 1.37, and by 1.41 for 1.35.
  The mean density rises with it (0.421 → 0.454): the depleted mirror lines and corners are a shrinking share of
  a larger face. The side-15 face at R = 37 is unremarkable on this measure, so its long residence is not explained.
- **[conjecture]** The symmetric law ln τ = −0.14 + 0.0272·A is a local fit (per-state hazards, A = 198–513) to
  something whose cost per site still climbs slowly with size — a boundary term from the mirror lines, of relative
  order 1/√A — so it under-predicts beyond its range. At an exponent of 19 each 1% is a factor 1.2: carrying the
  measured 5–11% (fixed-depth J/A; Gaussian μ²/2v) to extinction moves the side-16 first plateau from 2×10⁸ to
  roughly 5×10⁸–1.6×10⁹, where surviving 10⁹ is unremarkable. The asymmetric law (0.209 per site, tested directly
  to A = 84) is not touched by this; what failed is the proportional transfer "effective area A/7.7".
  Direct test: residence times of O_h-symmetric soups at R = 37 and 39, next item.
- **[measured]** **The direct test confirms it.** `python3 research/experiments/sym_soup_peels.py 37 64 1e8` and
  `… 39 24 4e7` (O_h-symmetric cube-centred soups run to their end or the cap; residence at each hull radius,
  mean = exposure / deaths; validated first at R = 27: 4903 [4140, 6012] at A = 315 against the law's 4576):

  | A (R) | deaths | mean residence [95%] | ln | law | ln − law |
  |---|---|---|---|---|---|
  | 630 (39) | 13 of 24 | 5.4×10⁷ [3.5, 11.9]×10⁷ | 17.81 | 17.00 | +0.82 |
  | 570 (37) | 64 + 10 | 8.9×10⁶ [7.2, 11.8]×10⁶; 9.7×10⁶ | 16.00; 16.09 | 15.36 | +0.64; +0.72 |
  | 513 (35) | 64 + 10 | 1.66×10⁶ [1.34, 2.20]×10⁶; 6.3×10⁵ | 14.32; 13.35 | 13.81 | +0.51; −0.47 |
  | 459 (33) | 63 + 10 | 2.29×10⁵; 3.4×10⁵ | 12.34; 12.75 | 12.34 | −0.01; +0.40 |
  | 408 (31) | 63 | 5.8×10⁴ | 10.97 | 10.96 | +0.01 |
  | 360 … 234 | 60, 53, 52, 41 | | 9.56, 8.27, 7.08, 6.41 | | −0.09, −0.15, −0.20, +0.19 |

  The law holds up to A ≈ 460 and is low by a factor 1.9 at A = 570 (74 deaths) and 2.3 at A = 630. ln τ / A climbs
  from 0.0269 (A = 459) to 0.0283 (A = 630), +5% — the same drift the face fluctuations showed (+4–8% in J/A over the
  same range) in minutes of sampling instead of an hour of waiting for deaths.
- **[measured]** Fits to all cube-centred symmetric residences with A ≥ 234 (the peeling study's per-state hazards
  plus these batches; 36 points, 2,365 deaths; weights = deaths):
  proportional `a + bA`: b = 0.0287, χ² = 59.9; with curvature `a + bA + cA²`: 0.564 + 0.02178·A + 9.09×10⁻⁶·A², χ² = 41.6;
  `a + bA + c√A`: χ² = 42.1; **slope pinned to the asymmetric constant over the face's six lockstep copies,
  `a + (0.209/6)·A + c√A`: 1.57 + 0.0348·A − 0.236·√A, χ² = 47.4** — better than the free proportional fit with the
  same number of parameters. (The lead's batches alone give the same ordering: 29.8, 20.9, 21.2, 24.4 on 20 points.)
  [Superseded 2026-11-13 (audit, finding I3): the refit with all data to A = 693 is 0.698 + (0.209/6)·A − 0.196·√A (`python3 research/fluct/sym_fit.py`, `research/fluct/data/sym_residence.csv`); STATUS 4 quotes it.]
- **[conjecture]** So "effective area A/7.7" was never a constant. The data are consistent with the simplest
  symmetry argument — a face is six independent-chaos domains in lockstep, cost 0.209·A/6 — minus a boundary term
  from the mirror lines that grows only like √A. The divisor 7.7 is what that looks like around A ≈ 350 and it drifts
  towards 6 as faces grow. Not established: the free fits prefer an even steeper asymptote (b ≈ 0.042 ± large), and
  the vertex-centred ×1.5 has only been measured at A ≤ 408.
- **Revised expectations** (curved fits, cube-centred; add ln 1.5 for even n if the vertex factor carries over):
  A = 693 → ln τ = 19.5–20.0, so the side-16 first plateau has mean ≈ 4–7×10⁸ instead of 2×10⁸, and being alive at
  1.025×10⁹ is a 10–25% event rather than a 0.5% one. Side 17 (A = 828): ≈2–6×10¹⁰ (was 6×10⁹). The legacy side-19
  cube, properly confined (A = 1053): 10¹³–10¹⁴ on these fits, far outside any data.
  [Note 2026-11-13 (audit, finding U3): `python3 research/fluct/sym_fit.py` now prints the A = 1053 extrapolation: ln τ = 31.0–32.1 over the fits, i.e. 3×10¹³–8×10¹³; one range, 10¹³–10¹⁴, is used everywhere. An extrapolation, not a measurement.]

## 2026-11-13 — clockwork: the long periods are short loops that close with a twist (clockwork agent; checked by the lead)

Full study, scripts and 94 new oscillators: `research/clockwork/README.md`. The lead re-derived the headline facts
with an independent set-based stepper written from the rule text (periods, the symmetry carrying phase 0 to
phase k, per-cell periods of P66.27a, C48.24a, C36.33a, C12.43a, C40.24a: all as stated).

- **[proved] P66.27a is a 33-step loop that returns as its own mirror image.** It is a plate three kagome layers
  thick whose diagonal hull has 45 cells, all of them live in some phase; by T2 the hull is a closed box, so the
  object is one cycle of a 45-bit map. Phase t+33 = phase t reflected in the plane x + y = 6. 40 cells have period
  66, the 3 cells on the mirror have period 33, 2 are stator. No cell has period 2, 3, 6, 11 or 22: nothing in it
  is a gear. (`python3 research/clockwork/verify.py …`; `gump show --cells research/clockwork/views/P66.27a.cells --orbit --max-chars 200000`.)
- **[proved] Twist lemma.** In a box with symmetry group G (which commutes with the box map F), let a cycle of
  period P first return to a symmetric image of itself after L generations, F^L(x) = g·x. Then P = m·L, where m is
  the order of g acting on the cycle, m ∈ {1, 2, 3, 4, 6} for subgroups of O_h, and any cell fixed by g has period
  dividing L. (g ↦ phase shift is a homomorphism from the cycle's symmetries to Z_P; its image is cyclic.) This is
  what Life catalogues call an oscillator's "mod" (there period/mod ∈ {1, 2, 4}); the cubic lattice adds 3 and 6.
- **[measured] All four twist orders occur, and choosing a box for its symmetry finds them.**
  Sampling random states of boxes picked for their symmetry (`python3 research/clockwork/portrait.py …`, commands in
  the README): **C48.24a, period 48 = 6 × 8**, in a 42-cell box with a six-fold rotoreflection — every 8 generations
  the whole plate reappears turned 60° about (−1,1,1) and inverted; **C36.33a, 36 = 4 × 9** (quarter turn about a
  cube axis every 9 generations; fills the 60-cell vertex-centred octahedron); **C12.43a, 12 = 6 × 2** (same box);
  **C40.24a, 40 = 2 × 20**. None of these four was ever seen in soup. (The catalogue's P15.22a, seen 11 times in
  soup, is 3 × 5: a third of a turn about (1,1,1) every 5 generations.) This chooses m, not L: SAT for a prescribed
  (g, L) stalls beyond ≈27 cells and L ≈ 5.
- **[measured] Census of small closed boxes.** All 402 diagonal hulls three layers thick with 15–66 cells, 50,000
  random states each (`python3 research/clockwork/box_census.py enum 3 15 66; … run 3 50000; … report 3`,
  ≈45 CPU-min): 9,700 distinct R-connected oscillators of period ≥ 3 (the atlas had 329). Four-layer boxes give
  far less (139 boxes, longest new period 28). P66.27a itself has a basin of 4.1×10⁻⁴ in its own box and turned up in 112 of the 113 census boxes
  that contain that box: it is rare in soup because soup rarely leaves an isolated plate of that shape
  [conjecture], not because it is a delicate attractor.
- **[measured] 249 of the 9,700 are compound clocks, and two of the "new periods" exist only that way** (lead;
  `python3 research/experiments/census_twist.py`, 15 s, re-steps every census object with its own stepper). In
  249 objects no cell has the full period: they are two (rarely three) sub-clocks of coprime periods on a shared
  frame — C44.26a is a period-4 rotor and a period-11 rotor (7 and 14 cells) on 14 stator cells; C30.32a is 5 with
  6; nine of the thirteen saved period-20s are 4 with 5. Since every cell keeps its sub-clock's period whatever
  the phase of the other, nothing passes between the rotors (Life calls such periods "trivial"). 22 of the 94
  saved objects are of this kind. With them set aside, the new periods are 17, 18, 19, 21, 24, 25, 26, 28, 32,
  34, 35 from the census and 36, 40 from the symmetric boxes; 30 and 44 are not periods of any single loop found.
- **[measured] The twist does not pick long loops; it multiplies ordinary ones** (lead; same command). Among the
  9,451 indivisible census objects, twisted ones are a steady 3–8% at every quotient length L (L ≥ 3: 295 of
  9,278; L ≥ 7: 30 of 670; L ≥ 12: 9 of 120; L ≥ 16: 5 of 66), while the number of objects falls steeply with L.
  Doubling (or ×6) therefore throws the twisted minority far out into the tail of *periods*: every indivisible
  object of period 26, 34, 48 or 66 is twisted. Ranked by L, the longest loop is untwisted — C35.29a, L = 35, 37
  of its 47 cells carrying the full period — and P66.27a's loop of 33 is second. So the longest clock on record is
  the second-longest loop, counted twice. Among oscillators that fill their own hull (period ≥ 7), 16 of 21 are
  twisted (agent's count).
- **[conjecture]** Periods well beyond 66 are there to be found by the same route: a loop of quotient length ≈30
  in a box with a 4- or 6-fold symmetry would have period 120–200. The search problem is that large symmetric
  boxes rarely settle into a cycle that spans them.
- **[measured] Fragile, and settable.** 6,600 single-cell flips of P66.27a (every cell of the union and its
  neighbour shell, phases 0–32; `python3 research/clockwork/perturb.py P66.27a`, 5 min): 30% heal (median 1
  generation), 14% die, 55% break into other objects; a lone extra cell just outside the box breaks it 43% of the
  time. Five of the 2,001 heals come back phase-shifted (by 10, 20, 25, 34, 47 generations). No travelling signal
  was found anywhere in it: the changing cells stay spread over the plate every generation.
- Not settled: whether P66.27a is the only period-66 cycle of its box (SAT did not finish; none other with basin
  above ≈5×10⁻⁶); whether any of these objects can carry or gate a signal.

## 2026-11-13 — side 16 at 1.75×10⁹ (lead)

- **[measured]** `research/experiments/cube_ckpt.sh 16`, second 2-hour job: alive at generation 1,750,000,000,
  hull radius 42, no face lost; checkpoint `research/data/cube16_gen1750000000.gump`. Its instantaneous population
  (13,320) is far below the 16,080 of the earlier checkpoint, but that is ordinary lockstep fluctuation: over
  60,000 generations from either checkpoint the total population has mean 15,800, s.d. 1,050, range 10,800–19,800,
  and the time-averaged layer profiles agree to 1 part in 300. The state is statistically unchanged.
- Surviving this long is a 2–10% event even under the corrected fits of the previous entry (first-plateau means
  4.4–7.5×10⁸ with the vertex factor): every estimate so far has been too low, in the same direction.

## 2026-11-13 — side 16 loses its first face at 2.36×10⁹; a forecast made in advance holds (lead)

- **[measured]** `research/experiments/cube_ckpt.sh 16`, fourth 2-hour job: all eight faces of the side-16 cube
  died together, last alive at generation **2,362,434,048** (events are sampled every 64). The hull went from
  radius 42 to 40 on every diagonal (A = 693 → 630). Event log so far: `research/data/cube16_events.jsonl`;
  states before and after: `research/data/cube16_gen1750000000.gump`, `…gen2525000000.gump` (alive, population
  13,968, hull radius 40). To see the peel again: copy the 1.75×10⁹ checkpoint to
  `research/scratch/cubes/cube16.ckpt.gump` and run the script (≈1.5 hours on one core).
- **Scorecard for the first plateau.** One exponential wait T constrains its mean only to [T/3.7, T/0.025] =
  [6.4×10⁸, 9.3×10¹⁰] at 95%, so this is a test of predictions, not a measurement of the mean.

  | prediction of the mean | made | T / mean | P(wait ≥ T) |
  |---|---|---|---|
  | peeling law, effective area A/7.7: 2.0×10⁸ | before the run | 11.8 | 7×10⁻⁶ |
  | curved fits to symmetric soups, ×1.5 vertex factor: 4.4–7.5×10⁸ | at 1.0×10⁹ | 5.4–3.1 | 0.5–4% |
  | clones of the 1.025×10⁹ state with Fleming–Viot restarts (`research/fluct/`): 1.04×10⁹, 90% CI 0.63–2.1×10⁹ | at 1.5×10⁹ | 2.3 (1.1 at the CI's top) | 10% (32%) |

  The fluctuation agent turned the last line into a forecast for the running cube — death at median 2.2×10⁹,
  90% interval 1.50–5.2×10⁹ — and committed it (`research/fluct/PREDICTIONS.md`, commit 2e72d57, 01:28:41Z) about
  two hours before the peel (event file written 03:43Z). The outcome sits at the 58th percentile of that forecast.
  It is the first out-of-sample prediction in this project that has held. It is also wide (a factor 3.5), is
  conditional on the cube having reached 1.45×10⁹, and its own mean still leans low; one event cannot say more.
  [Note 2026-11-13 (audit, finding I8): the table's "at 1.5×10⁹" is a rounding; the forecast was conditioned on the cube being alive at 1.45×10⁹ (`research/fluct/PREDICTIONS.md`).]
- **What was wrong with the lead's fits.** They were fitted to *cube-centred* symmetric soups and carried to this
  *vertex-centred* hull by a factor 1.5 measured only at A ≤ 408. If the clone estimate is right the factor at
  A = 693 is 2–3.5, not 1.5. **[conjecture]** The vertex-centred advantage grows with face size. Untested directly.
- **The second plateau is running long too.** R = 40, A = 630, vertex-centred; alive at 2,525,000,000, i.e. 1.6×10⁸
  generations in. Cube-centred symmetric soups at the same area gave a mean of 5.4×10⁷ [3.5, 11.9]×10⁷ (entry of
  2026-11-12), 8×10⁷ with the ×1.5: the cube has already stayed twice that (a 13% event; 5% without the factor).

## 2026-11-13 — a face dies off the end of a straight line (fluctuation agent; checked by the lead)

Full study: `research/fluct/README.md` (tools, tables, negative results), figure `research/figures/fluct_tail.png`.
Question put to the agent: is a face's death just the far tail of its ordinary fluctuations (entry of 2026-11-12,
"where the 0.209 comes from"), or does it need a mechanism of its own?

- **[measured] It is the tail, and the tail is now measured to its last cell instead of extrapolated.** For
  asymmetric octahedral soups at R = 7, 9, 11, 13 (A = 30, 45, 63, 84) the quasi-stationary distribution of a face's
  population n was sampled down to n = 1 together with the death rate h per face-generation. ln P(n = k) is a
  straight line from k ≈ 10 down to k = 1 (each cell fewer costs a factor ≈ 0.65), and the death rate is that line's
  next point: h / P(n=1) = 0.645, 0.613, 0.601, 0.594, against P(1)/P(2) ≈ 0.66. The end-game does not depend on
  size: 62–63% of deaths are from one surviving cell, 23–25% from two; a face at n = 1 dies rather than recovers
  with probability 0.67–0.72; the point of no return is n ≈ 1.5. All of exp(−0.2·A) is in the chance of being
  down to one cell. Endpoint: −ln h / A = 0.2268, 0.2182, 0.2164, 0.2152 → **I(0) = 0.2077 ± 0.0014 + 0.55/A**,
  i.e. the face law's 0.209 (`python3 research/fluct/analyze_qsd.py`, `analyze_tail.py`).
  *Lead's check with the engine only* (`python3 research/experiments/face_endgame_check.py 9 16000`: 13,765 first
  peels, kymograph every generation): mean first-peel time 2312 ± 20 (agent 2300 ± 6), −ln h/A = 0.2183,
  h/P(1) = 0.621, P(k)/P(k+1) = 0.658, 0.499, 0.778, 0.650, 0.630, 0.652, 0.655 … for k = 1, 2, 3 …, deaths from
  n = 1 / 2 / 3: 62 / 23 / 10%. R = 7: −ln h/A = 0.2274 (agent 0.2268). Also `python3 research/fluct/validate.py` → ALL OK
  (the agent's orbit-reduced bit-sliced stepper against `gump run`, every generation, five cases).
- **[measured] Correction to the lead:** the R = 9 first-peel mean is 2300, not 2.60×10³ ± 0.17×10³ (entry of
  2026-11-12); and near n = 0 the curve is straight in n, not "flattening". Extrapolating from n/A ≥ 0.1, which is
  all one has on large faces, misses ln h by 0.5–0.8 nats: the 0.20 the lead got that way was right partly by luck.
  [Corrected 2026-11-13 (audit, finding I1): the start time is not the cause. Re-running the lead's command reproduces 2,599.8 ± 174.9 exactly (same seeds); the same protocol with 1,024 soups gives 2,313 ± 75 at T0 = 60 and 2,307 ± 77 at T0 = 200. The 240-run sample was a 1.7σ high draw: sampling noise, not a protocol difference.]
- **[measured] The last ember is a triangle** (lead; `python3 research/experiments/near_death_shapes.py 9 300 1000`,
  a from-the-rule stepper, 1,263 face-generations at n = 3). The only irregularity on the line is an excess at
  n = 3 (P(2)/P(3) = 0.50, P(3)/P(4) = 0.78). 38% of three-cell faces are one shape: three faces round a single
  cube corner, a triangle of the kagome layer. It holds for 1.9 generations on average (up to 15), and when it
  changes it usually grows (n ≥ 4: 60%; straight to 0: 1%). Two-cell faces are an edge-sharing pair 54% of the time.
- **[measured] n is the only simple coordinate and a poor one.** For faces with 1 ≤ n ≤ 4, n removes 16–18% of
  the uncertainty about die-or-recover; the layer below adds 2–5%; no linear mix does better. A dying face is
  ordinary until ≈16 generations before the end, then falls in 10–12, on top of a layer below that only sags to
  0.6–0.75 of its mean and has recovered to 0.7–0.9 at the moment of death (`coord.py`, `predeath.py`).
- **[measured] Negative result: splitting along n does not help.** Forward-flux sampling is unbiased (within
  0.1–0.2 nats at R = 9, 11) but gains nothing: two clones differing by one flipped cell have 55–95% correlated
  fates, because the plunge is faster than a perturbation spreads. The rare event is a rare configuration reached
  in ten generations, not a slow rare path. What reaches big symmetric faces instead is brute force on an O_h
  orbit-reduced stepper (`research/fluct/fl.c`): the side-16 state is 946 nodes and 64 copies run at 3–7×10⁶
  replica-generations per second per core.
- **[measured] Symmetric faces** (same stepper; `research/fluct/data/sym_residence.csv`): cube-centred O_h soups
  give ln τ = 10.99, 12.47, 14.15, 15.88, 17.80, 19.71 at A = 408 … 693 (1,087 … 20 deaths), agreeing with the
  lead's gump batches at every size and with the lead's curved fit to A = 693. The same end-game appears in units
  of orbits (deaths from n = 3, 6, 9, 12; a favoured nine-cell state). Vertex-centred values are in the next entry.
- **Not settled:** whether 0.208 per site holds beyond A = 84 for asymmetric faces (one peel at A = 108; the rate
  function collapses to A = 135, which is indirect); the asymptotic symmetric slope (fits differ by 0.6 nats at A = 828).

## 2026-11-13 — the side-16 cube ends at 2,919,617,676; it outlived its own copies (lead)

- **[measured]** `research/experiments/cube_ckpt.sh 16` ran to its end: **still life at generation 2,919,617,676**,
  96 cells (`research/data/cube16_summary.json`, events `research/data/cube16_events.jsonl`). The prediction made
  before the run was 2.4×10⁸ (90%: 3.9×10⁷–6.3×10⁸): low by a factor 12. Schedule (hull radius: residence):

  | R (A) | 42 (693) | 40 (630) | 38 (570) | 36 (513) | 34 (459) | 32 (408) | 30 | 28, 26 | 24 | 22 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | generations | 2.362×10⁹ | 5.237×10⁸ | 3.08×10⁷ | 2.71×10⁶ | 7,040 | 27,712 | 128 | 1,344 | 256 | 64 |

  The last 37,000 generations took seven layers. What is left is twelve copies of the still life **S8b** (four faces
  round an edge, capped by a 2×2 plate), two on each half of the three coordinate axes, 2.75 and 9.25 cube-widths
  from the centre. S8b is also in the ash of the legacy side-10 cube. (Side 15, by contrast, went extinct.)
- **Forecasts for the second peel** (`research/fluct/PREDICTIONS.md`, both committed and pushed while the cube was
  at ≈2.55×10⁹): from fits, median 2.60×10⁹, 90% 2.531–2.89×10⁹ — the peel at **2,886,100,480** is inside, at its
  95th percentile; from 64 copies of the 2.525×10⁹ state (τ = 8.2×10⁷, 31 deaths), 90% 2.529–2.78×10⁹ — **missed**.
- **[measured] The ensemble mean at R = 40 is not in doubt.** Three independent estimates on the agent's orbit
  stepper: copies of the cube at 2.525×10⁹: 8.2×10⁷ (31 deaths); copies of the cube at 2.875×10⁹, eleven million
  generations before it actually peeled: 5.7×10⁷ (65 deaths; lead,
  `python3 research/fluct/qsd.py snap <state> v 900 1 lite`); fresh vertex-centred O_h soups: 8.2×10⁷ (46 deaths;
  lead, `qsd.py sym 40 v 900 1 lite`). Pooled 7.1×10⁷. **The cube itself stayed 5.24×10⁸ at R = 40: 7.4 means,
  probability 6×10⁻⁴ for an exponential wait.**
- **[measured] Vertex-centred series completed** (lead; `qsd.py sym R v …` at R = 32, 34, 38, 40; table
  `research/fluct/data/sym_residence.csv`, `python3 research/fluct/sym_fit.py`). τ_vertex / τ_cube at equal area:
  1.51, 1.52, 1.53, 1.60, 1.49, 1.31 ± 0.17 at A = 360 … 630 — a constant ≈1.5 — and **3.1 (ln 1.12 ± 0.29) at
  A = 693**, where the vertex value rests on copies of the cube (24 deaths) and soups (5 deaths) and the cube-centred
  one on 20 deaths. So the lead's conjecture of two entries ago (the factor *grows* with size) is wrong as stated:
  it is flat to A = 630; R = 42 alone is high, by 2.4σ. One-hour runs to firm up both numbers at A = 693 are the
  next entry.
- **[measured] Every large plateau of cubes 13–16 against the ensemble mean at the same hull**
  (`python3 research/experiments/cube_vs_ensemble.py`): of 16 plateaus with A ≥ 408, three lasted more than 4 means
  (side 15 at R = 37 and 33: 4.2 each; side 16 at R = 40: 7.4; 0.29 expected, P = 0.003) and three less than 0.05
  (0.78 expected); the sum of T/τ is 26.5 against 16 (P = 0.011). [Corrected 2026-11-13 (audit, finding 1): this test is post hoc — it
  includes the side-16 plateaus that prompted it; sides 13–15 alone sum to 12.8 means against 10, P ≈ 0.18. Not
  evidence; a question for fresh lineages.] **[conjecture]** Residences of whole cubes are
  over-dispersed relative to the memoryless ensemble — both tails. The ensembles themselves are exponential to 30
  means (hazard flat in age, 66,555 deaths at R = 30). No mechanism is known: a clone is the cube's own state with
  one orbit flipped, and inherits anything slow. It may be luck at the 1% level. Open.
- **Caveat on the orbit stepper at small sizes** (lead): `qsd.py`'s symmetric ensembles over-count exposure when
  chaos settles into debris that keeps cells in the outer layer — at R = 24 (vertex) it reports τ = 6.2×10⁴ where
  single engine runs give 630 (300 soups; 65 end still or periodic with the face layer occupied); R = 28: 6,930
  against 5,550; R = 30: 2.18×10⁴ against 2.07×10⁴ ± 0.09×10⁴; R = 29 (cube-centred): 1.44×10⁴ against
  1.36×10⁴. Probably oscillating debris of a period its settle test does not cover. Negligible where chaos cannot
  settle before a face dies (R ≥ 32: settles are under 2% of deaths; none from R = 36). Use the engine below R = 30.

## 2026-11-13 — radius 42 is not a special size; what is odd is the cube (lead)

- **[measured]** Three one-hour ensembles of fresh O_h soups on the orbit stepper:
  `QSD_SALT=xa python3 research/fluct/qsd.py sym 42 v 3500 1 lite`, the same with `QSD_SALT=xb`, and
  `QSD_SALT=xa … sym 41 c 3500 1 lite` (the salt gives an independent ensemble with its own file and seeds).
  Vertex-centred R = 42: 24 and 16 deaths in 1.28×10¹⁰ replica-generations each; with the agent's 5, **45 deaths,
  τ = 7.1×10⁸ (90%: 5.6–9.2×10⁸)**. Cube-centred R = 41: 38 deaths; with the agent's 20, **58 deaths,
  τ = 3.5×10⁸ (2.9–4.4×10⁸)**. Table: `python3 research/fluct/sym_fit.py`.
- **The vertex/cube factor at A = 693 is 2.0 (ln 0.70 ± 0.20)**, 1.5σ above the flat 1.5 of A = 360–630. The 3.1 of
  the previous entry leaned on the copies of the cube; fresh soups do not show it. R = 42 is an ordinary size.
  [Note 2026-11-13 (audit, finding I2): 2.0 is for fresh soups only (45 vertex deaths against 58 cube deaths). `sym_fit.py` pools the cube's own copies into the vertex value and gives ln 0.87 ± 0.18, factor 2.39; it now prints both, labelled.]
- **Copies of the cube against fresh soups in the same hull:** at R = 42, copies of the 1.025×10⁹ state give
  1.08×10⁹ (24 deaths) against the soups' 7.1×10⁸ — a ratio of 1.5, ln 0.42 ± 0.25, 1.7σ. At R = 40 copies and
  soups agree (8.2 and 5.7 against 8.2 ×10⁷). No clear difference.
- **The cube itself:** its first plateau, 2.362×10⁹, is 3.3 soup means (P = 0.036), or 2.8 means of soups and copies
  pooled (P = 0.06). `python3 research/experiments/cube_vs_ensemble.py` now reads: side 16's four largest plateaus
  at 2.8, 7.4, 2.6 and 1.2 means; all 16 large plateaus of cubes 13–16 sum to 27.2 means against 16 (P = 0.008).
  [Corrected 2026-11-13 (audit, finding 1): post hoc, as above; the P-value should not be quoted as evidence.]
  The puzzle of the previous entry stands and is now only about cube lineages, not about one hull size. Open.
- The side-17 forecast is unchanged by the extra R = 41 data (fits give ln τ(828) = 23.7–24.2; forecast 24.0 ± 0.4).

## 2026-11-13 — where the chaos comes from; nothing dies locally in three layers (lead and theory agent)

Notes with full proofs and commands: `research/theory/threshold.md`, `research/theory/thickness.md`. Programme:
`research/theory/PROGRAM.md`. The lead proposed the lemma and checked the agent's audit with separate code.

- **[proved] The threshold lemma.** In a finite vessel gump is a symmetric threshold automaton with one exception.
  The *uncapped* rule "alive next iff n + x ≥ 4" has the Goles–Olivos energy E(t) = −x(t)ᵀ(A + I)x(t−1) +
  3.5(|x(t)| + |x(t−1)|) (ordered pairs), which never increases and drops by ≥ ½ for every cell with
  x(t+1) ≠ x(t−1); so it reaches period ≤ 2 within 26N + 1 steps. Gump differs from it exactly at *overcrowded*
  cells (n ≥ 6, where gump says dead). For gump the change of energy is an **exact identity ΔE = D − Q**: Q the
  dissipation at non-overcrowded cells, D the drive, which enters only at overcrowded cells that were alive two
  steps earlier ("O1 events"). Consequences: an orbit with no O1 events from some time on has period ≤ 2; over any
  cycle total drive equals total dissipation; every oscillator of period ≥ 3 has O1 events, at least about a tenth
  as many per period as it has cells of period ≥ 3. The lemma is false for infinite configurations (uncapped fronts
  advance forever). Checks: `python3 research/theory/check_threshold.py` (all 329 catalogued objects of period ≥ 3
  have an overcrowded cell; the uncapped rule on 80 soups freezes in ≤ 8 steps); the identity holds at every one of
  300 steps of a chaotic orbit in the lead's own code and in `research/theory/energy.py`.
  Citation status: the agent read two secondary sources for the energy argument (arXiv 1108.2974, 2309.01854);
  the primary papers (Goles & Olivos 1980; Goles, Fogelman-Soulié & Pellegrin 1985) were not opened.
- **[measured]** (agent, `research/theory/overcrowd.py`) In bulk chaos 40% of cells are overcrowded every generation
  and 11.5% are O1 events; activity is 3.9 changes per O1 event (proved ceiling 20). On octahedron faces the O1 rate
  is 0.073, and 0.035 in the 50 generations before a face dies. Period-≤2 debris has none. The drive rate, not E
  itself, separates chaos from debris.
- **[disproved] "One layer always freezes to period ≤ 2"** (the lead's hoped-for theorem, PROGRAM S6). The one-layer
  automaton has oscillators of periods 3–12, including 5, 7 and 11, with rotors of 3–15 cells in large still
  stators (`research/theory/kagome_osc.json`; re-stepped by the lead: periods and one-layer thickness confirmed).
  Typical one- and two-layer soups do still freeze; that is a statement about typical states, not all states.
- **[proved] Sealed sets, and why the threshold is three layers** (agent; proof read and checked by the lead).
  Call a set of cells *sealed* if each of its cells has ≤ 3 neighbours outside it. A dead sealed set stays dead
  whatever happens elsewhere, unions of sealed sets are sealed, so the largest dead sealed set K(t) only grows:
  this is the skeleton, made exact. **In one layer a 6-cell hexagon ring is sealed, and so is every half-plane (a
  one-layer pattern never leaves its convex hull); in two layers a 36-cell set is sealed. In three or more layers,
  and in 3D, no finite set is sealed.** The proof takes the cell of the set furthest along a generic in-plane
  direction: it has 3 in-layer neighbours beyond it, and in a boundary layer either one of its two neighbours in the
  next layer or — because their in-plane offsets satisfy ē = −2(ā + b̄) — its one neighbour two layers on. That
  last neighbour exists only if there is a third layer. In an octahedral vessel every sealed set therefore touches
  the outside: **unconditional death cannot start in the interior; it can only come in from a face or span the
  vessel as a firewall**, which is what the peeling study measured.
- **[measured]** (agent) In one-layer soups K covers 25% of cells at t = 0 and 92% at t = 5, and the rest breaks
  into finite pockets by t ≈ 3; two layers take ≈ 50 generations; in three layers K stays empty.
- **[conjecture]** Thin slabs cannot sustain chaos because the unsealed region stops percolating; reduced in
  `thickness.md` §4 to a percolation statement that a computer-assisted block argument might prove.
- Not done: minimality of the 36-cell two-layer set outside a finite patch; the smallest sealed set of a thick
  torus slab beyond N = 4 (it is one whole face layer at N = 3, 4).

## 2026-11-13 — audit corrections (lead's session; findings in `research/AUDIT-2026-11-13.md`)
An agent that did none of the work audited all of it, assuming it wrong until reproduced. It re-derived T1–T4, the
twist lemma, the threshold lemma and the sealed-set theorem, and found bit-exactness intact; it also found the
errors noted in brackets through this notebook. The most serious was the lead's: the "cubes are over-dispersed,
P ≈ 0.01" count was post hoc (finding 1). Standing checks now exist: `bash research/check.sh` (20 exact checks,
≈ 25 s; run in CI on every pull request) and `research/CLAIMS.md` (71 headline claims graded A–D).
Corrections to older entries are bracketed notes placed after the statement they correct. Items that have no older
statement to annotate:
- **[measured]** (audit I7) The numpy oracle reproduces the side-12 log at every generation, with no torus divergence
  and no edge contact (5.5 min): `python3 reference/oracle.py legacy-cube 65 --compare <orig>/dev/cubic_init_results/population24.txt`.
  The engine matches sides 12 and 13.
- (audit I6) A "lifetime" is the generation at which the final state is entered (the engine's `cycle_start`); the
  side-14 (4,460,298) and side-16 (2,919,617,676) figures are `detected_gen`, 1–2 generations later (AUTOMATON §4).
- (audit U2) The ≈10⁴¹ generations per face quoted for an asymmetric soup in the side-13 hull is the face law
  extrapolated fivefold in area (A ≤ 90 measured, A = 459 asked); a **[conjecture]**, not a measurement. The side-19
  figure (10¹³–10¹⁴) is likewise an extrapolation of the symmetric fits.
- (audit U4) The face-law constants are fitted by `python3 research/peeling/face_law_fit.py`: −0.091 ± 0.047 +
  (0.2088 ± 0.0009)·A over the m = 8 slab batches with A ≥ 27 (the quoted ±0.06, ±0.002 are conservative).
- (audit T1, T2) `reference/oracle.py --compare`, `reference/check_theory.py` (T1) and `research/peeling/validate.py`
  now exit non-zero on a mismatch; `validate.py` creates `research/scratch/peeling/` itself.

## 2026-11-13 — a 2D gump: the phenomenon is a class (toy-2D agent; central law checked by the lead)

Full study: `research/toy2d/README.md` (forecasts in `research/toy2d/PREDICTIONS.md`; figures
`research/figures/toy2d_law.png`, `toy2d_box.png`). Question (PROGRAM G1): does any 2D rule do what gump does?

- **[measured] Yes: B34/S234 on the square lattice with the range-2 cross neighbourhood** (±1,0), (±2,0), (0,±1),
  (0,±2) — "alive next iff n + x ≥ 3, except that a cell with n ≥ 5 dies", gump's construction one dimension down.
  Confined to its bounding box, which only shrinks **[proved]**; steady chaos inside (density 0.472); a whole edge
  row dies after a memoryless wait with **ln τ_edge = 0.73 + 0.416·L** for L = 12–36 (τ from 286 to 5.8×10⁶
  generations; 495–4,067 deaths per size; strips 16 deep, periodic along the edge); ln P(n = k) of a living edge is
  straight down to k = 1 and the death rate is its next point; the threshold lemma (T5) holds with the exceptions
  exactly at overcrowded cells **[proved]**; no finite sealed set exists (T6 analogue) **[proved]**. It is the only
  capped threshold on that neighbourhood that sustains confined chaos, as gump is minimal in its own rule family.
  *Lead's check* (own numpy stepper, `python3 research/experiments/toy2d_check.py 12 16 20 24`): ln τ_edge = 5.85,
  7.43, 9.13, 10.88 at L = 12, 16, 20, 24 (108–415 deaths each) against the law's 5.72, 7.39, 9.05, 10.71; slope
  0.42. The lead's first version of this check gave nonsense (τ ≈ 20,000 at L = 12) because it counted settled
  debris as living edges; strips that settle or are cut must be censored — the same trap as `qsd.py` below R = 30.
- **[proved] Why the Moore neighbourhood is the wrong analogue** (agent): a lattice line holds only 2 of the 8 Moore
  neighbours, so confinement forces birth at ≥ 4 of 8, a majority threshold; a `{111}` plane holds 6 of gump's 12
  and a line holds 4 of the cross's 8, which lets the threshold sit near a third. **[measured]** No capped-threshold
  Moore rule sustains confined chaos; 93 of the 711 longest-lived Moore rules do die edge by edge but need survival
  at low counts (best measured: B45/S23467, ln τ = 4.32 + 0.259·L for L = 24–44).
- **[measured] Symmetry, with forecasts made first.** A mirror perpendicular to the edge multiplies the slope by 0.42;
  the full square symmetry by exactly 0.50: halved in the exponent, as two lockstep copies should. **Forecast
  failed:** symmetries that fix no edge were predicted to cost nothing; four-fold rotation lowers the slope (0.274
  against 0.343) and the diagonal mirror misses its predicted factor. Not understood.
- **[measured] Face versus firewall, again.** Long strips are cut across by three dead columns before an edge dies
  (from L ≈ 24–28 at depth 16); counted separately, the edge law stays linear. In an L×L box the cut costs 3L cells
  against L for an edge, so edges win.
- **A coincidence to be suspicious of:** the 2D slope per edge cell, 0.416, is twice gump's 0.208 per face cell to
  three figures. No reason is known; do not build on it.
- Not settled: the slope beyond L = 36; why four-fold symmetry shortens life; the full rate function; rules the
  first screen dropped (B34/S234 itself was added by hand); the triangular lattice.

## 2026-11-13 — cube-like seeds wait like soups; the cubes' long stays are luck or something only side 16 has (lineage agent; checked by the lead)

Question (OPEN-PROBLEMS 6): the legacy cubes 13–16 sat on some plateaus far longer than the ensemble means. Do
runs from structured seeds wait differently from soups? Study in `research/lineage/` (README, scripts, all
17,195 plateaus in `data/plateaus.csv.gz`). Engine-only single runs; 2,728 distinct lineages.

- **[measured] No.** 1,248 plateaus of deterministic cube-like seeds (cubes with surface orbits removed, hollow
  cubes, cube 13 inside a side-15 shell), at hull radius 31–37 (cube-centred) and 32–38 (vertex-centred): T/τ has
  mean 0.99, CV 1.02, 27 beyond 4τ where 22.9 are expected. 3,261 soup plateaus: mean 0.98, CV 1.00. Two-sample
  KS p = 0.98. `python3 research/lineage/analyze.py`.
- **[measured] No memory from one plateau to the next**: Spearman ρ = −0.013 over 1,201 consecutive pairs.
- **[measured] The 16 cube plateaus are still a ~1% outlier** against this (3 of 16 beyond 4τ against 27 of 1,248:
  Fisher p = 0.005), and the weight is side 16: sides 13–15 alone sum to 12.8τ against 10 (P = 0.18). The statistic
  was still chosen after side 16 finished. Side 16's own sizes (vertex-centred R ≥ 40) are out of reach of single
  engine runs, so "something only very large cubes have" is not excluded; nothing at R ≤ 38 trends toward it.
- **[measured once, small] A state carries a slow variable.** For 150 source states, four copies each with one orbit
  flipped: copies are exponential (CV 0.95), but their mean wait rises with the source's own remaining wait
  (Spearman +0.2, p ≈ 0.01; bottom to top third 0.89 → 1.1–1.2 τ). The two batches use the same lineages 20,000
  generations apart, so this is one observation, not two. Far too weak for the cube puzzle (it would give ~2.2%
  beyond 4τ; the cubes need ~19%). What the variable is: unknown. Needs a replication on other sources.
- [measured] About 1% of peels are followed by a second within 0.005τ; otherwise the hazard after a peel is flat from the start.
- Not followed up: cube-in-shell runs at 35c and 37c ran short (0.78 and 0.74 of the soup mean; 77 and 36 deaths).

Lead's check, sharing no code with the agent's analysis and taking the reference lifetimes from the soup lineages
in the same file rather than from the orbit-stepper ensembles (`python3 research/experiments/lineage_check.py`):
structured mean 1.00, CV 1.02, 26 beyond 4τ (22.7 expected); KS against soups p = 0.99; consecutive plateaus
ρ = −0.016 ± 0.040 (626 pairs at reliable radii); P(≥ 3 of 16 beyond 4τ at the structured rate) = 0.0045; copies
against own wait ρ = +0.19 and +0.23 (permutation p 0.010, 0.003). The data's cube 13 and 14 rows match the
schedules already on record. Not checked: the runs themselves were not repeated, and the seed generator is the agent's.

## 2026-11-13 — the area law has a name: supertransients (swarm librarian; two sources re-opened by the lead)

- **[read]** Deterministic chaos that lasts a time exponential in system size and then collapses abruptly, with
  exponentially distributed lifetimes, is a known numerical phenomenon in physics (*supertransients*, from
  Crutchfield–Kaneko 1988; *stable chaos* for cellular-automaton-like coupled maps). Houghton et al. 2010 report
  τ(L) = exp(AL + B) with "Poisson statistics", and collapse only with non-periodic boundaries. Nothing is proved
  in any source the librarian could open. Notes, with each statement tagged by how far the source was read:
  `research/theory/swarm/library/notes/supertransients.md`; index of 59 sources: `library/shelf.md`.
- Our earlier survey missed this (`PRIOR-ART.md` §3 said "no precedent" for a deterministic system; narrowed there
  today). What may still be ours: confinement and firewall as theorems, collapse by layers, the exponent set by
  the area of one face, the tail measured to one cell, the symmetry effects.
- **[read]** Contact process: exponential in volume in d ≥ 2 is Mountford 1999; Durrett–Liu and Durrett–Schonmann
  are one-dimensional. No finite-size exponential-lifetime theorem without monotonicity was found.
- Lead's check: opened arXiv 0902.2545 and eprints.whiterose.ac.uk/10731 (abstract level): titles, authors and the
  quoted claims match the notes. Not checked: the other 57 sources. Several primaries (Tél–Lai 2008,
  Bramson–Neuhauser 1994, Crutchfield–Kaneko 1988) sit behind publisher pages that refuse agents.

## 2026-11-13 — GPU ensembles: larger faces cost more per cell; two forecasts hold (GPU session; reviewed; lead's check)

The second session's work (`research/gpu/`, data in `research/data/gpu_facelaw/`; merged as pull request 8 after an
adversarial review, `research/audit/REVIEW-gpu-pr8.md`).

- **[measured] Asymmetric octahedral faces beyond A = 84.** ln τ_face = 23.376 ± 0.031 at A = 108 (1,059 peels) and
  29.34 ± 0.25 at A = 135 (16 peels). With the verified smaller sizes (6.804, 9.819, 13.633, 18.077 at A = 30…84)
  the local slopes are 0.201, 0.212, 0.212, 0.218, 0.221: the cost per cell is still rising. My extrapolated
  "0.2077 ± 0.0014" is retired: its fit missed one of its own points by 28 standard errors. The limit is unknown.
  Rim-free slab faces sit at 0.2088 ± 0.0009 (A = 27–90), so part of the rise may be the rim: these faces are
  mostly rim cells (swarm board E3).
- **[measured] Symmetric faces; forecasts written first.** Cube-centred A = 759: 21.903 ± 0.031; A = 828:
  24.175 ± 0.072 (my forecast 24.0 ± 0.4: inside); vertex-centred A = 759: 22.409 ± 0.040. Vertex/cube factor 1.66
  at A = 759. Local slope 759 → 828: 0.0329 ± 0.0011 (0.209/6 = 0.0348). Side 17's first plateau: τ ≈ 3.2×10¹⁰.
  Caveat (review): the cube-centred death rate falls with age in both runs (p = 0.04, 0.01).
- **[measured] Memoryless at R = 36, 38, 40** (vertex-centred O_h soups; τ = 2.25×10⁶, 1.25×10⁷, 8.63×10⁷), which
  reaches one of side 16's sizes. About 0.5–1% of peels are followed by the next layer within ~20 generations
  (the same double peels the lineage study saw).
- **τ at R = 40 and the side-16 puzzle.** `cube_vs_ensemble.py` used 7.1×10⁷, which pools soups with copies of the
  cube itself. With the soup value the R = 40 plateau is 6.1 τ (P = 0.002), not 7.4, and the sixteen-plateau sum has
  P = 0.016, not 0.008. Still post hoc; a little weaker.
- **How it was checked.** Reviewer: every table re-derived from committed data; kernel B emulated on a CPU and
  compared with `fl.c` and the engine (exact; broken kernels caught); an independent CPU run at A = 84
  (18.154 ± 0.025 against 18.141); duplicate-soup search (none beyond chance). Lead: A = 108 and A = 135 from the raw
  death lists with separate code (23.376, 29.341), and the split of A = 108 deaths by age (596 before half-time, 463
  after; 587 and 472 expected for a memoryless wait with reseeding). Not checkable here: execution on the GPU
  itself, and any size ≥ 108 against a second implementation.
- Corrections to the pull request's own wording are at the top of `research/gpu/README.md`.

## 2026-11-14 — the coplanar neighbours are the corner-touching four (asked by the owner)

The owner, looking at the neighbourhood figure on the overview page: "of the coplanar neighbors, each cell watches
its axial neighbors, not its corner neighbors." Checked, because the whole structure hangs on it.

- **Read (the 2012 source).** `dev/gump/environment.pde` lines 221-225: for a face with `x` odd the coplanar reads
  are `(x, y±2, z±2)`, both shifted together. Those are the four faces that touch it at a corner. The four that
  share an edge with it in its own plane, `(x, y±2, z)` and `(x, y, z±2)`, are never read. `docs/AUTOMATON.md` §2
  already says this.
- **Measured.** With the edge-sharing four swapped in, the oracle disagrees with the 2012 logs from generation 1
  (side 8: log 528, variant 0; side 9: log 696, variant 0: a closed cube dies at once, every face being
  overcrowded). With the corner-touching four it matches every generation, as before.
- **Counted (the lead, two lines, not audited).** Layer histogram along a body diagonal: corner-touching gives
  1, 2, 6, 2, 1 (T1), so an empty face outside a diagonal plane sees at most 3 and the hull is an octahedron.
  Edge-sharing gives 4, 4, 4, so diagonal planes leak. But across an axis plane through face centres (`x = c`,
  `c` odd, everything beyond it empty) an edge-sharing face at `c+1` sees 2 + 1 = 3 and one at `c+2` sees none, so
  that variant is confined to its bounding **box** instead. Two soups (density 0.4, box of half-width 8) agree:
  under the variant the largest coordinate goes 8 → 9 and stays there for 80 generations with about 1,000 faces
  alive, while the L1 radius passes its starting hull (23 → 25); under gump the L1 radius stays 23 and the
  largest coordinate grows 8 → 20.
- So the "8-sided die" of 2012 is the signature of the corner-touching choice.
- **It was a slip.** The owner, the same day: "i made a mistake in 2012! i intended to use edge neighbors, not
  corner neighbors. that was the whole point haha. so i made a mistake writing the code, and actually used corner
  neighbors, but didn't notice for 14 years". And: the edge version is "just a tangent, probably belongs on a
  branch, not in main. to avoid potential future confusion." So **gump, here and everywhere in this repository,
  is the rule as coded and run**: the corner-touching four. A quick look at the intended rule (chaotic on a torus;
  shut in its box; lifetime climbing steeply with box size; dies a slab of cubes at a time) is on the branch
  `claude/edge-neighbour-tangent` under `research/tangents/edge-neighbours/`, and is not to be merged.

Reproduce: `python3 research/experiments/axial_variant.py` (about a minute).

## 2026-11-14 — GPU round two: slabs, age, cube-like seeds (GPU session's pull request 12; reviewed; lead's check)

The three experiments asked for after pull request 8. Data and scripts arrive with pull request 12 (`research/gpu/`,
`research/data/gpu_facelaw/`); the adversarial review is `research/audit/REVIEW-gpu-pr12.md` (scripts in
`research/audit/gpu_pr12/`). Forecasts were committed before the runs (`research/gpu/PREDICTIONS.md`, checked from
commit order). Every table number re-derives from the committed data with the reviewer's own code; the slab kernel
equals the engine and `fl.c` on a CPU.

- **[measured] Symmetric soups do not age.** Cube-centred O_h soups at R = 43 (A = 759), 2,304 replicas, 5,971 face
  deaths, ages to 2.6 τ: censored Weibull shape k = 1.020 (1.000–1.042); pooled with the earlier run, 1.011
  (0.993–1.028), ln τ = 21.889 ± 0.012. The falling death rate the first review saw at R = 43 (k = 0.94) was noise;
  the one at R = 45 (k = 0.84, 0.72–0.96) has not been re-run. Per-bin hazard is flat to ±13%.
- **[measured] Cube-like seeds at vertex-centred R = 40 wait like an exponential, plateau by plateau.** 3,857
  lineages from deterministic O_h seeds (cube 14 plus the surface of side 16 with 1–3 surface orbits removed) that sit
  at R = 40 at generation 1000, followed through 40, 38, 36: mean T/τ = 0.991, 1.011, 0.983 (± 0.016), CV 0.99–1.00,
  KS inside the 5% band. Waits beyond 6.1 τ: 8 (8.7 expected). **What it does not show:** these are not the side-16
  cube (which sits at R = 42 at generation 1000 and reached R = 40 only after 2.5×10⁹ generations), and lineages
  still at R ≥ 42 at generation 1000 are left out. Successive plateaus are weakly correlated (40 → 38: ρ = +0.049,
  p = 0.002), carried by lineages that peel early: a transient after the burst.
- **[measured] Rim-free slab faces stay on the old line through A = 108.** Slab 6×6×8, periodic in plane, p = 0.4:
  447 first deaths, ln τ_face = ln(2 × exposure/deaths) = 22.470 ± 0.047; the line −0.091 + 0.2088·A (fitted to
  A = 27–90) gives 22.459. An octahedral face of the same area (23.376) is **0.91 ± 0.06 nats tougher**, like with
  like (the same estimator; density 0.35 against 0.4 makes no difference: 9.823 against 9.820 at A = 45).
- **[not settled] Whether the cost per cell rises beyond A = 108 in a rim-free face.** The 6×7×8 run (A = 126, 122
  first deaths, 26.138 ± 0.091, which reads as a local slope of 0.204 ± 0.006) counts any outer-layer death, and a
  slab also dies by a transverse three-layer firewall, after which a face dies within a small fraction of the wait
  (reviewer's CPU run at 4×7×8: 94 of 94; the statistic there reads 0.51 below the line from this alone). The cheapest
  cut of 6×7×8 is 216 cells in one direction. Extrapolating `research/peeling/slab_fw.csv` (ln τ_fw ≈ 12.1 at cut 108,
  17.0 at cut 144, 0.137 per cell) gives ln τ_fw(216) ≈ 27.0 ± 0.3, so 25 (18–38) of the 122 deaths are expected to be
  firewalls; corrected, ln τ_face(126) ≈ 26.36 and the slope 108 → 126 is ≈ 0.216, the octahedral value. The data
  cannot tell 0.204 from 0.216. The session's reading "the octahedral rise is a rim effect" is withdrawn at the
  review's request; what makes octahedral faces tougher (rim, eight faces sharing edges, a thick interior, shape) is
  not separated. Asked of the GPU session: the same run with firewalls detected.
- **A design rule that falls out.** In an N×N×8 slab the face costs ≈ 0.63·N² and the cheapest firewall ≈ 4.9·N
  (cut 36·N at 0.137 per cell), so firewalls overtake faces near N = 7–8: eight-layer slabs cannot measure the face
  law beyond A ≈ 110 without detecting firewalls; thicker slabs can.

Lead's check: the slab table from the JSON (22.470, 26.138, slope 0.2038 ± 0.0057), and the expected firewall count
from `slab_fw.csv` by hand (24–29 central, 21–39 over ± 0.3 in ln τ_fw). Reproduce the review:
`python3 research/audit/gpu_pr12/slab_rederive.py <checkout of PR 12>`, `fw_competition.py`, `weibull_own.py`,
`cubelike_own.py` (see the review for arguments).

## 2026-11-14 — the class theory attacked; the rule the owner meant to write is a gump in a box (class checker; lead's check)

`research/theory/class.md` (the class agent's characterisation of gump-like rules, 2026-11-13) was checked by a
second agent told to assume it wrong: `research/audit/REVIEW-class.md`, scripts in `research/audit/class/`, its own
stepper anchored bit-exact to `reference/oracle.py`. Its out-of-sample test was the neighbourhood the owner intended
in 2012 (the four coplanar neighbours share an edge), there and here called **face12e**. face12e is not gump; gump
is the rule as coded. The checker committed what class.md predicts for face12e before running anything on it
(`research/audit/class/PREDICTION-face12e.md`, commit bcb8122).

- **[proved] Sealing belongs to a half-space, not to a direction** (the review's Theorem A′). For H = {u·p ≤ C} let
  c(H) be the most neighbours inside H that a cell outside H has. The outside of H, once dead, stays dead iff
  c(H) ≤ b − 1 (b the least birth count). With one cell type this depends on u alone and is class.md's Theorem A.
  With several types it depends on where the plane sits. class.md's theorems A–G survive as stated (one wording
  slip in C4); what fails is its first clause, "outside sealed iff b > a⁻ on a spanning set of directions; the hull
  is the polytope of those rays", and six rows of its table. Gump's own row is exact: every diagonal layer holds all
  three face types.
- **[proved, by hand; the lead had the same count on 2026-11-14] face12e is confined to a box.** No direction is
  sealed at b = 4 (an x-face has 4 neighbours behind any plane x = C just below it), so class.md as written says
  "not confined, not a gump". But a plane through a sheet of face centres (x = C, C odd) is sealed: beyond it a face
  at C + 1 has 2 + 1 = 3 neighbours inside, a face at C + 2 none. [measured] 0 escapes from the odd box in 64,000
  soup-generations.
- **[measured] face12e B45/S345 has the whole phenomenon.** Torus: chaotic from densities 0.25–0.55, ρ = 0.398
  (gump 0.416). Slabs four cubes deep between two walls, periodic N × M wall: a wall dies as a whole (the sheet of
  wall faces and the layer of perpendicular faces beneath it empty together; that band is the smallest sealed one),
  after a wait with CV 0.98–1.00 and a hazard flat in age:

  | wall faces A | 16 | 20 | 25 | 30 | 36 |
  |---|---|---|---|---|---|
  | ln τ (checker) | 6.428 ± 0.002 | 7.999 ± 0.004 | 10.183 ± 0.007 | 12.089 ± 0.015 | 14.542 ± 0.040 |
  | ln τ (lead, own stepper) | 6.427 ± 0.006 | 8.005 ± 0.005 | 10.186 ± 0.008 | | |

  Slope 0.410 ± 0.001 per wall face. The wall sheet alone empties 4–10 times as often and comes back; the event that
  kills a wall is the death of the layer beneath it, which has 2A cells. Per cell of that layer the cost is
  **0.205**, against gump's 0.212 per face cell (same rule; the layer's cells have the neighbour counts of a gump
  face cell: 6 in the layer, 2 one layer in, 1 two layers in, plus 2 outward in the sheet). Observed, not explained.
  Boxes of n³ cubes: median lifetimes 10, 60, 439, 9,855, 707,038 for n = 2…6; none of 64 finished at n = 7 in
  300,000. A 5³ box stands intact for two thirds of its life and then loses 11 of its 15 layers of cubes, each as a
  whole; 2 cubes of 125 remain (median). The lead's quick look on the tangent branch agrees on every point it made.
- **So the slip of 2012 changed the shape of the die, not the phenomenon**: octahedron (corner-touching, gump) or
  box (edge-sharing, face12e). Both are confined, chaotic and die a face at a time by a rare memoryless event whose
  cost is linear in the face's area.
- **[measured, rougher] Three more lattices change status under the repaired clause.** bond10 is tight at b = 3,
  not 4 (box with odd walls; chaotic at every cap 4–8; strong slab laws at two caps; its boxes of 4³ did not die in
  300,000 generations, unexplained). The plain kagome lattice at b = 2 (class.md dismissed it): B2/S12 is confined to
  a hexagon, chaotic (ρ = 0.48), with a strip law (ln τ = 7.24 … 12.85 at 4 … 12 wall cells) and growing hexagon
  lifetimes: a candidate second 2D gump, on rough evidence (transverse cuts not censored). kagome8 and hex9 at b = 4
  were not run.
- **What the class statement is now** (the review's §5.1; each clause tagged there): confinement by a positively
  spanning family of sealed half-spaces [proved]; no finite sealed set when some generic direction gives every cell
  type ≥ b forward neighbours [proved]; armour, i.e. an immortal wall once the cap exceeds the wall cells' degree
  [proved, conditional; no exception in 38 + 2 cases]; non-period-2 behaviour needs both overcrowding and
  undercrowding [proved]; and, given a chaotic bulk and no armour, whole-wall memoryless death exponential in the
  wall's area [measured: 42 of the class agent's 50 lattice–cap pairs by the rule fixed in advance, plus face12e].
  **Nothing predicts which caps are chaotic or how strong the law is**; class.md's fifth clause ("face not starved",
  K_f·ρ/b ≳ 0.85) is a fit to two cases and flips on face12e with the choice of layer. "Gump" has no sharp edge on
  the weak side.
- Corrections to class.md's numbers: "identical slab law" for B456/S3456 → equal within 0.2 in ln τ at five sizes,
  slopes 0.2121 and 0.2156; fcc slope 0.19 → 0.181 ± 0.001; "46 of 50" → 42 by the pre-fixed rule; the scorecard's
  "8 / 6 / 14" is a judgment. The full list is the review's §5.2; class.md carries a note at its head until revised.

Lead's check (`research/audit/class/lead_check.py`: numpy on a cell graph, no shared code; `validate` equals the
oracle with gump's offsets): `python3 lead_check.py slab 4 4 8000 2048 1` → 6.427 ± 0.006, hazard flat in age
(τ = 613, 620, 635, 620 in four age bins); `slab 4 5 40000 2048 2` → 8.005 ± 0.005; `slab 5 5 100000 2048 3` →
10.186 ± 0.008 (15,171 deaths, 12 minutes). A first version that censored only
period-2 states read 6.495 and 8.027: replicas that settle into longer cycles never die and inflate τ at old ages.
The same trap as the PR 12 reviewer's with `fl.c`; any wall-law estimator must censor every period.

## 2026-11-14 — a deterministic relative of the 2D rule with an exponential law (swarm: source and probability lines; fresh-reader audit; lead's check)

The first result of the theory swarm to pass an audit by a reader who is neither a solver nor the critic
(`research/theory/swarm/audit/AUDIT-theoremA.md`; its scripts `a1`–`a10` there share nothing with the critic's lab).

**The automaton 𝒜(L).** Cells (x, j), x on a ring of L columns, rows j = 0, 1, 2, … Row 0 follows the 2D rule
B34/S234 on the range-2 cross with nothing above it. Every other row copies the row two below. Initial state: any
row 0; beneath it independent fair bits, each written into two consecutive rows. The update is deterministic; the
only randomness is the initial tape, which the conveyor brings to the edge two rows a generation.

- **[proved; audited]** Row 0 is exactly a Markov chain: a cell within distance 2 of a live cell is alive next with
  probability ½, except that a live cell with two live in-row neighbours survives surely. From its quasi-stationary
  law the edge dies after an exactly geometric wait of mean τ_L, and τ_L ≤ 3·8^L. τ_L is at least the lifetime of
  five-parent oriented site percolation of density ½ on the same ring.
- **[proved, conditional; audited]** *If* (F1) the critical density of two-parent oriented site percolation is
  below ¾ (Balister–Bollobás–Stacey 1994, p_c ≤ 0.7491, computer-assisted; nobody here has read the primary paper;
  the audit adds a second route through Liggett 1995 at exactly ¾) *and* (F2) supercritical oriented site
  percolation on a cylinder of circumference n lives e^{cn} (Hartarsky–Szabó 2022, Cor. 4.8; read in the paper, its
  proof there is a sketch), *then* e^{cL} ≤ τ_L ≤ 3·8^L for all large L, odd or even. No unconditional exponential
  lower bound survives.
- **[exact]** ln τ_L = 6.5319, 9.4733, 12.2492, 13.5946 at L = 8, 12, 16, 18 (the audit's `a3_chain.py 18`): about
  0.67–0.71 per cell, against 0.36–0.42 measured for the 2D rule's own edge in a strip.

**What it is not.** The audit's own words are the right ones: a deterministic map reading a random tape once. The
edge consumes L fresh bits a generation for ever; the bulk neither reads the edge nor transforms what it carries;
the two cells beneath an edge cell are always equal, which the rule's own bulk does not do. It is not self-made
randomness, and it says nothing about gump or about the 2D rule in a vessel run by the rule. The method provably
stops short of both (the audit's §4: for independent rows beneath at the bulk density the best one-step monotone
minorant dies in O(log L) generations; a gump face cell with six live in-face neighbours dies whatever is beneath).
Its use to the project is as a fixed point: the simplest system with the 2D rule's own edge in which "memoryless,
exponential in the length" is a theorem, with a precise list of what a proof for the rule itself may not use.

The audit also went through every other claim tagged "proved" in the probability and source lines (its part B):
all correct, one worded too widely (probability claim 8). It found no wrong verdict of the critic's. Counting's and
path's proved claims have not had a fresh reader.

Lead's check (`research/audit/swarm/lead_check_theoremA.py`, plain numpy, no shared code):
`python3 lead_check_theoremA.py literal 8 4000 512 1` (the map on the whole array, tape of 8,000 rows) →
ln τ = 6.519 ± 0.019; `lazy 8 20000 4096 2` (rows 1, 2 drawn fresh each generation) → 6.535 ± 0.003;
`lazy 12 60000 4096 3` → 9.463 ± 0.007. Exact: 6.5319, 9.4733. The swarm's examiner, separately, measured the
variant with a parity bulk at L = 12, 14, 16 inside 0.7σ of the corresponding exact chain
(`research/theory/swarm/exam/OUTCOMES.md`, S-E1). Not checked by the lead: the proofs line by line (the auditor
did), the two literature statements (nobody has, in the primary sources).

## 2026-11-14 — the swarm's predictions examined: four hold, two fail, two undecided (examiner; lead's check)

An examiner who wrote none of the predictions ran the eight sampled entries of `research/theory/swarm/PREDICTIONS.md`
(filed 2026-11-13). Protocols, validations and every command: `research/theory/swarm/exam/OUTCOMES.md` (protocols
committed before any production run, commit 530ed79). All numbers below are **[measured]**; ln τ errors are 1/√deaths.

| entry | predicted | measured | verdict |
|---|---|---|---|
| path E1: a 2D edge with a two-cell notch | slope 0.345 ± 0.020 per cell | 0.3458 ± 0.0036 (L = 20–32); the intact edge of the same strips 0.412 ± 0.005 | holds |
| source S-E1: the 2D edge over a parity bulk | ln τ = 6.4282, 7.6056, 8.6764 (the exact dice chain) at L = 12, 14, 16 | 6.433, 7.597, 8.675, all inside 0.63σ; hazard flat in age | holds |
| source S-E2: faces over fair dice | gump 7.40, 9.94 (A = 36, 48); 2D 7.43, 9.16 | 7.397 ± 0.009, 9.945 ± 0.014; 7.403 ± 0.009, 9.150 ± 0.010 | holds |
| counting C-E1: gump hull faces with one mirror | slope 0.105 ± 0.009 per cell | 0.1026 ± 0.0003 (A = 84–135; local 0.099, 0.106) | holds |
| counting C-E2: 2D edge dead by generation 3 | c₃ = 0.447 ± 0.012 | 0.3676 ± 0.0006 | fails |
| path E3: gump's remnant on a slab face equals the hull's | face population 1.6, 3.4, 6.4, 9.7 at 1–4 generations before death | 1.66, 4.29, 10.70, 18.40 (slab 5×4×8) | fails (lags 3, 4) |
| path E2: 2D remnant two generations before death | 9.8 ± 1.0 at L = 32 and 36 | 9.09 ± 0.08, 7.99 ± 0.38 | not refuted; low at L = 36 |
| probability P-E1: one row on dice, ring, L = 30–38 | slope 0.48 ± 0.03, refuted if ≥ 0.51 | 0.512 ± 0.012 | undecided at the line; 0.48 disfavoured at 2.8σ |

What the outcomes say, beyond the scores:

- **Six layers are enough for gump.** A gump slab face with six layers on the rule and fresh fair coins beneath has
  the lifetime of the face over gump's own deterministic bulk to 0.01 in ln τ (7.397 against 7.398 at A = 36; 9.945
  against 9.936 at A = 48). Whatever the face needs from the bulk, it needs only as noise, made within six layers.
  (The exponent study says the same with four to five layers; its review is in progress.)
- **A mirror halves the price.** A face cut by one mirror plane costs 0.1026 per cell, 0.47 of an asymmetric
  face's ≈ 0.22 at these sizes, and the first face to die is a mirror-fixed one in more than 99.9% of 394,192 replicas.
  This is "symmetry is fatal" at its simplest: half the cells are copies.
- **An edge with an end is cheaper.** Two dead anchor cells lower the 2D edge's exponent from 0.412 to 0.346,
  as the path line derived. Rings and intervals are different vessels; quote which.
- **The remnant is not universal.** The last generation is the same object in hull and slab (one cell, 59% of
  deaths; 62% on hulls), but the slab face falls from 18 cells to none in four generations where a hull face takes
  about six. Path's "one remnant in every vessel" is withdrawn by its author (round 4).
- **Fixed-age exponents are not the death rate.** The chance that a fresh soup's edge is dead by generation k
  falls through the steady exponent already at k = 3 (0.368 against 0.38–0.42): it describes the soup's transient.
  Counting's bridge C1′ is withdrawn by its author (round 3).

Lead's check (`research/audit/exponent/lead_check.py`, numpy, no shared code; validated on the one-row chain):
`python3 lead_check.py 8 16 5000 0.5 4096 21` → 7.424 ± 0.010 and `8 20 14000 0.5 4096 22` → 9.155 ± 0.013, against
the examiner's 7.403 ± 0.009 and 9.150 ± 0.010 for S-E2's two 2D points (1.5σ and 0.3σ). For S-E1 the lead simulated
the conveyor variant instead (previous entry). Not re-derived by the lead: the gump points of S-E2, C-E1, and the
failures. The examiner's engines were validated against exact values and earlier measurements (its V1–V6), not bit
for bit against the oracle; its E2 and E3 error bars are rough (batch means over 4–6 chunks).

## 2026-11-14 — the revised class statement tested where nobody had run it (class follow-up; lead's check)

Forecasts committed first (`research/theory/class/followup/PREDICTIONS.md`, commit 59e0683), then the runs
(`followup/OUTCOMES.md`: every command, the scorecard, what was not checked). The stepper `fu.c` equals an independent
numpy stepper and the review's `aud_step` cell for cell on nine vessels of five lattices (`python3 fu.py validate`).
All **[measured]** unless tagged. Names: face12e is the edge-neighbour rule, not gump.

- **Confinement by half-spaces holds out of sample.** kagome8 and hex9 at the position-aware tight b = 4 (class.md
  before its revision had b = 5 and no confinement): 0 escapes from the predicted hull in 1,536 soups, caps 5–8.
- **A new gump-type rule: hex9 B456/S3456.** Chaotic torus, whole-wall memoryless death at seven wall lengths
  (ln τ = 6.12 → 13.29 for n = 8 … 20, CV 0.97–1.02, flat hazard, 3 pits in 215,000 events), hull lifetimes growing to
  sparse debris. But the wall law is **concave**: 0.69 falling to 0.53 per wall cell. "Linear in the area" is only
  approximate there. (kagome8 has no chaotic cap within reach.)
- **kagome4 B2/S12: 0.772 ± 0.003 per wall-row cell**, straight over seven lengths, memoryless (forecast 0.70 ±
  0.08). The drift the review saw was not transverse cuts, as forecast, but **walls that freeze**: static rows of
  density 2/3 that spread inward, at 27–44% of the wall-death rate, with no armoured set in the sense of Theorem E.
- **bond10 B34/S234: box walls are not slab walls.** Slab law 0.492 ± 0.001 per wall face (six sizes, memoryless).
  The forecast for boxes of 4³ from that law, 600–1,500 generations, **fails by a factor 10⁶**: no box had any
  permanent death by 10⁷; 4 of 64 died by 10⁸; median ≈ 10⁹. The reason was found: the layer beneath a wall's sheet
  contains the edge rows of the four neighbouring walls' sheets, and those rows stay dense (0.67–0.71 against 0.50),
  so a wall cannot die while its neighbours live. Columns (two pairs of walls) are 24–196× tougher per wall than slabs
  of the same area. Clause 6 of the class statement (hull lifetimes follow the wall law) is wrong for this rule as
  written; it needs an edge term. Gump has the mild form of the same thing (an octahedral face is 0.91 nats tougher
  than a rim-free one at A = 108; entry "GPU round two"); why bond10's edges cost so much more is not known.
- **face12e, larger boxes.** 7³: forecast from the wall law median 1.3 × 10⁸, so 15 (9–33) of 128 boxes finished by
  3 × 10⁷; observed 16 of 128. The box series keeps steepening (0.42 per unit of n² from 6³ to 7³).
- **face12e with full cubic symmetry dies at once.** One coin per O_h orbit, density 0.45, 64 soups per size: median
  lifetimes 3, 9, 9.5, 19, 19, 33.5, 35.5, 100.5, 103.5 generations for boxes of 4³ … 12³, against 439, 9,855,
  707,038 and ≈ 1.6 × 10⁸ for soups without symmetry at 4³ … 7³: 74,000 times shorter at 6³. About half of the
  symmetric soups end empty. Symmetry is fatal in gump too (a symmetric face behaves like one of area A/7.7 or so),
  but there a symmetric cube of side 13 still lives 10⁵ generations and side 16 lived 2.9 × 10⁹. Under the rule the
  owner meant to write in 2012, a symmetric random start in a box of this size is over in tens of generations.
  **[conjecture, the lead's]** The difference is geometric: face12e's hull is a box whose walls are mirror planes'
  neighbours, so a symmetric state has six identical walls of very few independent cells each (n²/8), while gump's
  octahedral faces are cut by mirrors only along lines. Not tested. Legacy-shaped seeds (the 2012 cube runs) under
  face12e are on the owner's tangent branch, not here.

Where the class statement is now known to be wrong or silent (for its next revision): clause 6 for bond10 (edges);
clause 3 on walls that freeze without armour (kagome4) and on chaos peeling away beneath an immortal armoured band
(hex9 c = 8, strips); clause 5 should say "roughly linear" (hex9). hex9 c = 7 (b/K = 0.44) is a third exception to
the b/K ≤ 3/8 rule of thumb for chaos.

Lead's check (`research/audit/class/lead_check_box.py`: its own box graph and orbit construction on the stepper of
`lead_check.py`; lifetime = exact length of the transient): `python3 lead_check_box.py sym N 256 1` for
N = 4, 5, 6, 8 → medians 3 (2–5), 7.5 (5–11), 8 (5–11), 18 (11–25) with 9, 18, 24, 50 orbits (follow-up: 3, 9, 9.5,
19; same orbit counts); `asym 4 128 2 20000` → 414 (283–596) against the review's 439. Not re-derived by the lead:
hex9, kagome4, bond10, the 7³ boxes. The follow-up's classification of endings (wall, deep firewall, cut, pit,
frozen) has no independent implementation.

## 2026-11-14 — slab faces with the firewall channel resolved (GPU session's pull request 14; reviewed; lead's check)

The rerun the review of pull request 12 asked for. Periodic slabs N×M×8, two faces of A = 3·N·M cells; a life ends at
its first event, a face death or a transverse firewall (three adjacent dead oblique layers wrapping the torus), and
each channel gets its own rate. Forecasts were committed before the runs (`research/gpu/PREDICTIONS.md`). Review:
`research/audit/REVIEW-gpu-pr14.md` (every number stands; four text fixes, made). **[measured]**

| slab | A | cheapest cut | face deaths / firewalls | ln τ_face | ln τ_fw per direction |
|---|---|---|---|---|---|
| 3×6×8 (validation) | 54 | 108 | 1,917,760 / 276,769 | 11.084 ± 0.001 (CPU table 11.10) | 12.327 ± 0.002 (12.18 ± 0.12) |
| 4×7×8 (validation) | 84 | 144 | 45,878 / 32,840 | 17.465 ± 0.005 (17.43–17.51) | 17.106 ± 0.006 (17.16) |
| 6×6×8 | 108 | 216, three directions | 592 / 13 | 22.568 ± 0.041 | 26.79 ± 0.28 |
| 6×7×8 | 126 | 216, one direction | 92 / 29 | 26.405 ± 0.104 | 26.87 ± 0.19 |

- All three forecasts for 6×7×8 hit: face 26.30 ± 0.15, firewall 27.0 ± 0.4, firewall-first share 10–30% (24%).
  The review of pull request 12 had put the corrected face value near 26.3 and the firewall rate at 27.05 ± 0.30.
  At 6×6×8 the share forecast hit (2.1% against 0.5–4%) and the face forecast missed by 0.01 (22.49 ± 0.07).
- The firewall rate depends on the cut alone: 26.79 ± 0.28 and 26.87 ± 0.19 per direction at cut 216 in a square and
  a non-square slab.
- Pooled A = 108 (this run with the earlier unscreened one): 22.537 ± 0.031. Slope 108 → 126: **0.215 ± 0.006** per
  cell. The line through A = 27–90, −0.091 + 0.2088·A, is 0.08 ± 0.03 and 0.19 ± 0.10 below the two points (before the
  line's own extrapolation error of 0.06–0.12).
- **Not decided, and there are two readings.** (i) Rim-free faces get a little dearer per cell past A ≈ 100, as
  octahedral faces do (0.216–0.221). (ii) The cost per cell is constant and the *width* of the periodic face matters:
  in the CPU table the residual from the A-only line rises with the slab's short side (3: about −0.05; 4: 0.00;
  5: +0.11; 6: +0.08, +0.19), and the reviewer's fit a + b·A + c·(short side), c = 0.114 ± 0.038, b = 0.2057 ± 0.0014,
  predicts 22.564 at 6×6×8 and 26.267 at 6×7×8. The fit is post hoc (the term was chosen after looking). The test
  has been asked of the GPU session: 4×9×8 against 6×6×8 at the same A = 108 (reading (ii) predicts 0.23 ± 0.08
  lower, reading (i) no difference), and width families s = 3 … 6 at high precision.
- The review's independent check: a CPU run of 3×6×8 with the `rep.c` stepper (25,088 lives) gives 11.076 ± 0.007,
  12.310 ± 0.018, 12.7% firewall-first; with the GPU's detection rules applied to those histories, 11.082, 12.325,
  12.61% against the GPU's 11.084, 12.327, 12.61%. Counting a firewall life to its detection rather than its
  formation biases 3×6×8 by +0.006 and +0.015 and nothing measurable at A ≥ 84.

Lead's check (`python3 research/audit/gpu_pr14_lead_check.py research/data/gpu_facelaw`, own decoding of the per-life
data): 5,213, 4,664 and 4,673 lives; exposure, counts, both rates, the shares, the pooled value 22.537 ± 0.031 and the
slope 0.2149 ± 0.0060 all reproduce; the face hazard is flat in the age of the life (three bins of equal exposure:
22.53, 22.59, 22.59 at 6×6×8). Not checked by anyone here: the GPU runs themselves (no second GPU run); cycles longer
than 128 generations (none can be seen; bounded only at 3×6×8); a channel-resolved CPU run at 4×7×8 or larger.

## 2026-11-14 — where the exponent lives: a few layers of the rule over noise (exponent study, written up by a successor; adversarial review; lead's check)

The study of 2026-11-13 was cut off before its report; a successor wrote `research/theory/exponent.md` from its files.
An adversarial reviewer then re-derived the gump half with code and seeds of its own
(`research/audit/REVIEW-exponent.md`; steppers equal to the oracle, `research/audit/exponent/`), and the lead the 2D
half (`research/audit/exponent/lead_check.py`). What stands after both, all **[measured]** unless tagged:

- **The face law's exponent is set in a thin boundary layer driven by noise.** Keep the rule on the top w layers of a
  face and replace everything beneath by fresh coin flips every generation.
  - Gump, periodic slab faces: with w = 5 the model's ln τ equals the deterministic slab's to within 0.015 at
    A = 27, 48, 60 and is +0.02 ± 0.04 at A = 75 (reviewer's own runs; the A = 75 slab is new, 15.660 ± 0.027;
    A = 36 was not re-run). With w = 4 it is 0.06–0.07 high.
  - Gump, octahedral hull faces: within 0.05 at A = 45, 63, 84 (truth 9.823, 13.644, 18.148 ± 0.028), but deep models
    (w = 6, 8) settle 0.03–0.04 *below* the truth (4–5σ at A = 45), and w = 4's closeness is partly a crossing
    (w = 3 far above, w ≥ 5 below). That "four to five layers" suffice for hulls was noticed after the runs.
  - 2D rule (B34/S234 on the range-2 cross): eight rows over coins against deterministic strips 16 × L. Lead's own
    code: 5.654, 7.425, 9.136, 10.855 ± 0.010–0.018 at L = 12, 16, 20, 24 against the strips' 5.644, 7.407, 9.142,
    10.788: within 0.02 at the three smaller sizes, 0.067 ± 0.027 above at L = 24. The coin density hardly matters
    (the study: ρ = 0.30 and 0.60 move ln τ by ≤ 0.02; the lead at ρ = 0.5: 7.424, 9.155).
  - The swarm's exam found the same independently for gump with six layers (entry above, S-E2).
- **New trap, found by the reviewer:** the noise-driven models can settle. With w ≥ 4 the six faces of a cube at a
  hull's vertex are a fixed point whatever the coins do, and with w ≥ 5 so is a cube anywhere on the face
  (`research/audit/exponent/trap.py`): the face then never dies. Uncensored, the R = 7, w = 4 model reads 6.94
  instead of 6.54. Model runs must censor repeating boundary states like any other vessel.
- **In the 2D rule the lifetime tracks the chance of an empty window, but the formula is a fit.**
  τ_edge(L) = 12.1/E(L − 6.5), with E(ℓ) the probability that ℓ given consecutive cells of a long living edge are
  empty, was found after the runs; χ² is 17.3 on 5 degrees of freedom at the quoted errors; fitted to L = 12–28 it
  predicts L = 32 and 36 low by 0.08 and 0.07. "The exponent is the decay rate of E" does not stand: the lifetimes
  use only windows up to ℓ ≈ 30. The window cost with honest errors (5 × 10¹¹ samples, jackknife): 0.387 ± 0.006
  per cell at ℓ = 34 → 42.
- **[proved]** (`exponent/theorems.md`; checked by the reviewer, brute force to L = 14 where possible): upper bounds
  of the right form only (E T ≤ 3δ^{−3L} for a driven edge; ≤ ε^{−L} with noise) and a lower bound conditional on a
  ratio-mixing hypothesis that has not been measured in the system it is applied to. Lemma A(c) was false and is
  corrected (187 of 512 configurations). Nothing derives the constant.
- **Does not stand as written:** "0.416 ≈ 2 × 0.208 is a coincidence" (the measured ratio range 1.6–2.0 has 2 at its
  edge: not established either way); "gump faces cost 0.403 per live cell" (the fit has an intercept 0.085 ± 0.025
  and the area law fits better); the reading of the exact small-vessel census (the enumeration is right, `fg.c`
  equals brute force on eight vessels, but "debris, not chaos, breaks the random-map heuristic" does not follow:
  7 of 17 vessels with N ≥ 24 have no long immortal cycles where 22–197 were predicted).

The review lists thirteen corrections to `exponent.md`; an editor is applying them. What this changes for the
project: the open problem "why about 0.21 per cell" no longer needs gump's bulk. It is a question about five or six
layers of the rule over independent coins, a probabilistic cellular automaton of finite depth, for which lifetimes
can be computed exactly at small sizes and sampled at large ones without the deterministic bulk. Not checked by
anyone: the report's §§2, 6.1, 8–10 tables, the gump two-generation face game, `fg.c` beyond N = 24.

## 2026-11-14 — the theory swarm is closed: no proof of the area law; what it did establish

Four solver lines (probability, counting, path, source), a librarian, four critic passes, an examiner and one
fresh-reader audit, 2026-11-13 to 14, on one problem: why the wait before a face dies is exponential in its area, by
mathematics alone. The closing table is at the top of `research/theory/swarm/critic/board.md` (the board is closed);
proofs are in each line's `journal.md`, verdicts in `critic/to-<line>.md`. In the critic's words, which are the right
strength: **no line proved the area law for gump or for the 2D rule, and no line derived the constant from the
rule.** "Why area" and "what is the constant" are open.

What stands, and who checked it:

- **A deterministic relative with an exponential law** (probability and source; critic and the independent audit):
  entry of this date above, CLAIMS SW1. Conditional on two published percolation statements not verified here at
  the source. Not self-made randomness.
- **Exact reductions for gump** (path; one critic per round, no second reader): every permanent loss is the
  extinction, at one instant, of an inclusion-minimal sealed set; the death rate equals the entry flux into a low set
  times the committor of the pooled one-step population table, with no Markov assumption (P̄); the exponent lies
  between a block bound and a sum of local roots, with equality for skip-free tables.
- **A conditional area law** (path's Theorem Q; one critic): ln τ ≥ θ₀(κA − k₀) − ln Φ *if* sparse faces regrow at a
  rate bounded below on rows k₀ … κA of the table (hypothesis R). R(0.35, 0.40, 5) holds on the four measured hull
  tables (A = 30–84); it is not derived from the rule. It accounts for 0.13–0.14 of the 0.21 per cell (0.16–0.18
  with the measured entry term). The sharper Theorem V⁻ stands as mathematics but adds at most 0.35 nats at the
  measured sizes, and its hypothesis (sub-extensive tables) fails on rows above 0.3·A between the tallied sizes.
- **Fixed-age theory of soups** (counting; one critic): the chance that a fresh soup's edge is dead by generation k
  is a transfer-matrix quantity, exactly computable. It describes the transient, not the steady law (its exam
  entry failed, and the author withdrew the bridge).
- **Exact facts about face12e and symmetric faces** (counting; one critic): a lone cell on a face12e sheet dies in
  one generation with probability 3793/8192; cube- and vertex-centred O_h faces have equal orbit counts, so the
  factor between them is a boundary effect.

One number is left as a conjecture: the quasi-potential V = 0.2191 per cell at A = 84, a functional of a measured
table with a stated continuation, to be compared only with hull slopes at A ≥ 84 (0.218, 0.221). The alternative
0.2054 is contradicted by the tallies.

What fell, each for a stated reason (the board's graveyard): closures by independent cells; fixed-age exponents as
the law; "ln τ = A·∫θ"; "one remnant in every vessel"; the ring exponent coming down to the interval's; every
equal-time transfer hypothesis. Exam: five entries hold, four fail or missed, two undecided, three not run (C-E3,
path E4, P-E4).

Facts the swarm leaves without an account: the constant for either rule; the rise of the cost per cell with A; the
symmetric slopes and the vertex/cube factor; face12e's 0.205 and fcc's 0.181.

Not checked by anyone: the two percolation statements at the source; any link from the rule to the pooled table;
counting's and path's proofs by a reader other than one critic (the audit covered probability and source only);
path's closing theorems were written and checked on the same day. The lead read the closing table and the
audit, re-derived the relative's lifetime (entry above), and proved nothing here.

Where this leaves the problem, with the exponent study's result of the same day: the constant belongs to five or
six layers of the rule over independent noise, and the reductions above say what has to be computed there (the
committor of a population table, or better a direct transfer-matrix calculation at finite depth). That is a smaller
problem than the one the swarm was given.

## 2026-11-14 — equal areas, different lifetimes: the shape of a periodic face matters (GPU session's pull request 16; reviewed; lead's check)

The question left open by the entry "slab faces with the firewall channel resolved": is the cost per cell of a slab
face rising with area, or does the face's width matter? The GPU session ran fourteen periodic gump slabs s×M×8
(two faces of A = 3·s·M cells each; soup 0.4; every life ended at its first event, a face death or a transverse
firewall counted as its own channel; ln τ_face = ln(2 × exposure / face deaths)), in four families by short side s.
Review: `research/audit/REVIEW-gpu-pr16.md` (independent recomputation, fits, an independent CPU run). The lead's
re-derivation: `python3 research/audit/gpu_pr16_lead_check.py research/data/gpu_facelaw` (results in its docstring).

| s | ln τ_face at A = … (share of lives ended by a firewall) | slope within the family |
|---|---|---|
| 3 | 11.082 (54; 13%), 14.621 ± 0.003 (72; 87%), 18.046 ± 0.011 (90; 99.6%) | 0.1966 then 0.1902: curved |
| 4 | 12.486 (60), 14.971 ± 0.002 (72), 17.465 ± 0.005 (84), 19.943 ± 0.018 (96), 22.373 ± 0.042 (108; 99.2%) | 0.2072 ± 0.0001 |
| 5 | 15.661 ± 0.003 (75), 18.786 ± 0.011 (90), 21.890 ± 0.040 (105), 25.046 ± 0.073 (120; 92%) | 0.2082 ± 0.0006 |
| 6 | 22.568 ± 0.041 (108; 2%), 26.405 ± 0.104 (126; 24%) | 0.213 ± 0.006 |

- **[measured, three pairs; one confirmed by independent code] At equal area the narrower face dies sooner.**
  4×9 against 6×6 at 108 cells: −0.196 ± 0.059. 3×8 against 4×6 at 72 cells: −0.349 ± 0.004. 3×10 against 5×6 at
  90 cells: −0.740 ± 0.016. The reviewer's CPU run (a different stepper, checked against the engine on both slabs,
  channels resolved) gives −0.344 ± 0.020 for the pair at 72 cells. The same slab in both orientations agrees to
  −0.002 ± 0.003. The session's own forecast, committed before the runs, was "area only"; it missed, and says so.
- **[measured] The face hazard does not depend on the age of the life** from about 200 generations on, in every slab
  with age histograms (review, claim 3), so the rates are not rates of young states even where firewalls end 99% of
  lives. Under the launch caps used, the detection-time bias is at most +0.006 (s = 3) and +0.0015 (s = 4), in the
  direction that makes the gaps look larger, and far below them.
- **[measured] Width 3 is a different animal.** Its line is curved (the quadratic term is nine standard errors from
  zero) and its chord, 0.196 per cell, is well below the others. Its last point is also the one where 99.6% of lives
  end in a firewall, so "curved" and "biased by the competing channel" are not separated there: with the cheapest cut
  at 36·s cells, width and firewall share are one variable by design. Within s = 4 the share runs from 0.5% to 99%
  and the line does not bend.
- **[measured] For widths 4 to 6 the data do not need a width-dependent cost per cell.** One slope, 0.2072 ± 0.0001,
  with an intercept rising with the short side (0.053, 0.121, 0.203 for s = 4, 5, 6), fits at χ² = 8.4 on 8 (reviewer
  and lead, separately). So does a model with one parameter fewer, ln τ = a + 0.2117·A − 0.054·M with M the long
  side (χ² = 5.6 on 9). The two cannot be told apart here: within a family both are straight lines, and they differ
  only in predicting b(5) = 0.2072 or 0.2081 and b(6) = 0.2072 or 0.2087, where the measurements are 0.2082 ± 0.0006
  and 0.213 ± 0.006. Either way **the correction to the area law is linear in a side length**, about +0.07 per unit
  of short side at fixed area, or −0.05 per unit of long side.
- **[consequence, measured] The old slab line's slope was inflated by mixing widths.** Fitted with area alone, the
  slabs with s ≥ 4 give 0.2085 per cell (and a hopeless χ² of 512 on 10), above every family's own slope, because
  wider slabs were also the larger ones. The 0.2088 of the CPU table (CLAIMS F4, A = 27–90, mixed widths) is a slope
  of that kind. The session's conjecture that 0.2088 averages narrow slabs *down* from an octahedral 0.216–0.221 has
  the sign wrong and does not stand (review, claim 4): b(5) is thirteen standard errors below 0.216.
- **[open] The cost per cell of a wide periodic face** is 0.2072 if the width enters as an offset and 0.2117 if the
  long side does; b(6) = 0.213 ± 0.006 allows both. Deciding needs b(5) to about ± 0.0003 (some 2,500 face deaths at
  5×8×8, where there are 189), or a seventh width, each about fifty times the cost of the last. Octahedral faces
  (0.216–0.221 measured) are not periodic and have edges; nothing here connects the two numbers.
- **[conjecture, lead]** A term linear in a side is what a line-like object would cost: if the event that kills a
  face has to close around the short way of the torus (or is helped by a seam along the long way), its price
  carries a term in that length. A bulk finite-size effect would instead fall off exponentially in the width. Not
  tested; the place to look is where on the face the last cells die, by width.
- Not checked: the GPU runs were not repeated on a second GPU; no CPU check at 90 or 108 cells (too slow); whether
  near-firewall states raise the face hazard at s = 3 (the per-state data were not kept).

## 2026-11-14 — the shortest way round: twisted faces at equal area (shape experiment, forecasts first; adversarial review with an independent stepper; lead's check)

The entry above left a correction to the area law that is linear in "a side" of the periodic face, and a conjecture:
that the variable is the shortest closed loop of the face torus (its systole). Rectangular s×M slabs cannot test
this, because side and shortest loop are the same thing. Slabs whose in-plane period lattice is twisted can: the
lattice generated by (a, k) and (0, b) in the cube coordinates (i, j) of `research/peeling/geom.py` has the same area
A = 3ab for every k, and loops of squared length x² + xy + y² (the two in-plane axes are at 60°). Experiment:
`research/shape/README.md` (forecasts in `PREDICTIONS.md`, committed before the runs; every torus stepped by code
checked against the engine generation by generation). Review: `research/audit/REVIEW-shape.md` (own bit-sliced
stepper with its own layer indexing, checked against the engine on seven tori; geometry rebuilt from AUTOMATON.md's
table; fixed seeds). Lead: `python3 research/audit/shape_lead_check.py` (tables from the counts; lattice classes).

| shortest loop² (length) | tori at A = 72 | ln τ_face, experiment | review's independent run |
|---|---|---|---|
| 9 (3.00) | 3×8; (8,2),(0,3) | 14.613 ± 0.010 | 14.614 ± 0.014 |
| 12 (3.46) | (4,4),(0,6); (2,5),(0,12) | 14.877 ± 0.010 | 14.866 ± 0.016 |
| 13 (3.61) | (4,3),(0,6) in three presentations | 14.921 ± 0.008 | |
| 16 (4.00) | 4×6 (two presentations); (6,1),(0,4); (6,3),(0,4) | 14.973 ± 0.007 | 14.966 ± 0.008 |
| 19 (4.36) | (2,3),(0,12) | 15.011 ± 0.014 | 15.020 ± 0.017 |
| 21 (4.58) | (4,1),(0,6) | 15.066 ± 0.014 | 15.035 ± 0.009 |

- **[measured, two independent codes] At 72 cells the lifetime of a periodic face rises with its shortest loop**, in
  both sets of runs. Different shapes with the same shortest loop agree: χ² = 1.1 on 4 over distinct shapes (two at
  9, two at 12, three at 16). The control passed: the twist k = 2 of 4×6 is the same torus as 4×6 under the
  automaton's symmetries and the flip of the slab, and gives 14.974 against 14.968.
- **[measured, two independent codes] The shortest loop is not the only variable.** At 60 cells two different tori
  with the same shortest loop (squared 16) differ: 4×5 gives 12.490 ± 0.003 and (5,1),(0,4) gives 12.471 ± 0.003
  (0.019 ± 0.004). The experiment topped up that pair because the gap looked interesting; the review reran both with
  fixed seeds and no stopping rule and found 0.0177 ± 0.0042, and the top-up alone already shows 0.021 ± 0.005. The
  lead's remark: the two differ in their second-shortest loop (squared 21 and 19), and the one with the shorter
  second loop dies sooner; at 72 cells the three shapes at 16 have second loops 27, 28, 31 and agree. One pair is
  not a law, and the review notes the ordering does not repeat (insignificantly) at 72.
- **[measured] Two other candidates are refuted.** Distance counted in steps on the lattice (the tori with loop² 12
  and 13 have step-distance 4, like 4×6, and lie 0.096 ± 0.012 and 0.052 ± 0.011 below it), and proneness to
  transverse firewalls (it predicted those tori above 4×6).
- **[measured] Not a firewall artefact.** Tori whose shortest row closes after six or more cells have no firewall
  channel to speak of (the review saw 2 firewalls in 2.25 × 10¹⁰ life-generations on (4,1),(0,6)) and lie on the same
  curve as tori with 5% and 87% firewall endings. Loop length 3 still always comes with the cheapest cut, so the
  doubt recorded above about width 3 is not removed.
- **[measured] Sizes.** At 72 cells the rise is about 0.15 per unit of loop length between 3.46 and 4.58
  (+0.075 ± 0.010 from 4 to 4.58, both runs pooled); length 3 sits 0.19–0.24 below that line. The effect is larger
  at 72 cells than at 60 in every comparison (ratio 1.3 to 2.3: from loop² 12 to 16 the gap is 0.051 ± 0.005 at 60
  and 0.096 ± 0.012 at 72), so for loops shorter than 4 the shortest loop changes the cost per cell, by about 0.004
  per cell between 3.46 and 4, as width 3 did in the rectangular families.
- **[measured, one code; statistic not reviewed] How a face ends.** It holds about 37 of its 72 cells until about
  13 generations before its death and then empties in 6–8 generations, the same on three tori; the last cells show
  no band along the short loop.
- **The lead's forecast** (lifetime a function of the shortest loop alone, sizes from the rectangular offsets):
  the ordering held everywhere; "alone" failed at 60 cells; the sizes missed (+0.075 at loop² 21 where +0.04 was
  forecast; 14.877 and 14.921 at 12 and 13 where 14.78 and 14.83 were forecast).
- **[reading, lead]** A periodic face feels its own wrap-around: the shorter the ways round, the cheaper its death,
  with no sign of saturation by length 4.6 at 72 cells. So every cost per cell measured on a periodic slab so far
  carries a wrap-around term, and the wide-face constant is not yet isolated from it. The line-like-object picture
  that suggested the experiment is not shown: the death has no visible geometry, and a second loop matters.
- Not checked: no GPU or second-machine run; seven of the thirteen presentations at 72 and three tori at 60 were
  run by one code only; the event detectors (as opposed to the stepping) were not validated against the engine;
  `research/shape/loopsum.py` (a sum over loop classes that did not explain the pair at 60) was not reviewed.

## 2026-11-14 — the path line's proofs read a second time (independent audit; the lead re-ran one exact check)

When the swarm closed, the path line's results (exact reductions for gump and a conditional area law) had been
checked by one critic each and by nobody else. A second reader has now gone through every claim tagged proved,
forming verdicts before opening anything the critic wrote, and recomputing with code written from
`docs/AUTOMATON.md`: `research/theory/swarm/audit/AUDIT-path.md` (scripts `p0_lib.py` … `p7_tallies.py` beside it,
each a few minutes; outputs in `audit/out/`).

- **[proved; read twice and recomputed] Correct as stated:** P̄, C, T′, T, X, V⁻, Lemma E1 and V⁻(E), R, P, L1,
  L1′, L3, L4, F (and R5, read only). P̄ was tested as an exact identity in rational arithmetic on all 2²² states of
  a 22-cell gump vessel, on hidden Markov chains, and on 6.4 × 10⁶ face-generations of a hull face; the structure
  lemmas by enumeration of every state of a small face and the cells beneath it (2²⁴). The lead re-ran the first of
  these (`cd research/theory/swarm/audit && python3 p1_pbar_exact.py`, 31 s): the output equals the audit's log.
- **[correction] The slogan for P̄ leaves out two terms.** The identity is: deaths = direct deaths from above the
  low set + entry flux × committor of the pooled one-step table + a term at the start of the window − a term at its
  end. On the audit's A = 30 sample the window term is 7.8% of the deaths.
- **[correction] The conditional area law holds from (R) + (Φ) + (W), not from "R and R⁺" as worded.** (i) The
  window term is not controlled by R and R⁺: the audit gives an example satisfying both whose hazard is 45 times the
  bound. Its Proposition W fills the gap (the term vanishes if the window starts above the threshold row, or is
  bounded in a quasi-stationary window when censoring is at most c times the hazard and (1 + c)w < 1; measured at
  A = 30: censoring 6.8 times the hazard, (1 + c)w = 0.56). (ii) R⁺ and B⁺ taken as suprema over every visited row
  fail at the top rows (a full rim-free face dies in one step); the corrected statement uses a set of rows and the
  living weight of the rows left out. With these, the step from the hypothesis to "exponential in the area" is
  airtight. The hypothesis (R) itself (local roots at least θ₀ on rows k₀ … κA of the pooled table of the living
  ensemble) is a statement about the rule that is known only from measured tables: the audit reproduced it from the
  lab's tallies at A = 30 … 84 and on its own sample at A = 30. It is not derived.
- **[correction] Lemma S is narrower than worded.** "Lost for ever" is not "inside the dead sealed set": the end
  state of the side-8 cube has 96 cells that are dead for ever and lie in no dead sealed set. The statement that
  every permanent loss is the extinction of a minimal sealed set needs minimality relative to what is already
  sealed (the audit's Proposition S′, proved there).
- Smaller: the row for V′ in `path/claims.md` omits a hypothesis without which it is false (the journal's statement
  has it); the last sentence of V⁻(E) about gump's bottom rows is a remark, not a proof, and nothing rests on it;
  one illustrative number in P is 1.62 × 10⁻¹⁵, not 1.8 × 10⁻¹⁵.
- Not checked by the audit: the claims not tagged proved (V's upper half, V∞, A, G1, W, F12, Dr, the exam
  entries); hypothesis (E) on real tables; path's own scripts; sizes other than A = 30 for its own sample (one
  seed); whether a full rim-free face is reachable after the first generation.
- What this changes: nothing in the swarm's bottom line (no proof of the area law; the constant not derived). The
  conditional result is now stated with its true hypotheses and has been read by two independent readers. The same
  audit for the counting line is still owed.

## 2026-11-14 — every torus of a given area: the lifetime is not a function of area and shortest loop (census at A = 48, 60 and part of 72; forecasts first; adversarial review with an independent stepper; lead's check)

- What was done (`research/shape2/README.md`): every class of periodic face (period lattice (a,k),(0,b) up to the
  twelve symmetries) was measured at A = 48 (9 classes) and A = 60 (10 classes), and five more at A = 72. Candidate
  laws were fitted on the already published values and their forecasts committed before the runs (80906fe). The
  review (`research/audit/REVIEW-shape2.md`) re-ran 16 of the 24 rows with its own stepper, seeds fixed beforehand
  (3cf07a5): they agree with the tables (χ² 25 / 16).
- **Measured: the cost per cell depends on the shortest closed loop of the face, and saturates.** d ln τ_face / dA
  from A = 48 to 60 (in brackets, 60 to 72): loop² 3: 0.115 (0.111); 4: 0.141 (0.135); 7: 0.192 (0.187);
  12: 0.207 (0.205); 13: 0.209 (0.206); 16: 0.2125 (0.208). The review's own runs give 0.1144, 0.1415, 0.1922,
  0.2076, 0.2127 for 48 → 60. So a face only √3 or 2 cells around still lives exponentially long in its area, at
  about half to two thirds of the wide-face cost, and the wide-face figure is reached near loop² 12. On the thin
  tori the hazard is flat in age, almost nothing settles, and face death is permanent (review, claim 2): it is the
  same kind of object, not a different regime.
- **Measured: above loop² 12 the shortest loop no longer orders the classes at A = 48.** The four classes with
  loop² 12, 12, 13, 16 span 0.016; the 4×4 face (loop² 16) lies 0.0135 ± 0.0021 below the (12; second loop 19)
  class (review). At A = 60 the step from loop² 12 to 16 is +0.056 to +0.063, at A = 72 about +0.10: the shape term
  grows with the area.
- **Measured: a second variable at equal shortest loop.** A = 48, loop² 12, second loop² 16 against 19:
  +0.0151 ± 0.0017 (two codes pooled; 0.0156 ± 0.0021 from the review alone). A = 60, loop² 16, second loop² 19
  against 21: four runs with two codes, 0.0186 ± 0.0041, 0.0177 ± 0.0042, 0.0061 ± 0.0049, 0.0132 ± 0.0028; pooled
  0.0142 ± 0.0019 (χ² 4.7 / 3; the lead's arithmetic from these four gives the same). This replaces the 0.019 of
  the entry "the shortest way round". A third pair (A = 60, loop² 12) has the same sign but is 1.8σ. In each pair the
  face with the shorter second loop dies sooner. What the variable is has not been found: the second-shortest loop
  fits the sign in three pairs, which is not a test.
- **Refuted: every candidate law.** L1, L2, L3p, L3-const and L4 fail at each area. L3-area appeared to pass at
  A = 60 on the census's own run (χ² 5.4 / 5); on the review's independent values it fails (22.7 / 5) and with all
  runs pooled it fails (45.4 / 5), and five of its six classes were ones it had been fitted on. No law in area and
  shortest loop describes the data at any area.
- Corrections the review made to the tables. The loop² 4 rows carry a resolution bias: a face death and a firewall
  in the same 16-generation check window are all booked as firewalls; resolved per generation the A = 48 value is
  about 9.47, not 9.489 (six times its stated error; the slope is not affected, 0.1415 against 0.1414). The loop² 1
  and loop² 4 tori are multigraphs (a cell counts one neighbour twice), so they are not gump on a smaller face in
  the strict sense. Loop² 3 has a firewall channel after all (one in 2 × 10⁹ life-generations). The loop² 1 rate
  means nothing and is to be blanked.
- Lead's check: `python3 research/audit/shape2_lead_check.py` recomputes all 24 rows and the costs per cell from the
  raw counts. The pooled pair differences were recomputed from the four published differences.
- Not checked: nothing at A = 72 was rerun (the bracketed costs rest on one code); the loop² 13 class at A = 60;
  the census's post-hoc fits (`explore.py`); event detection against the engine (stepping was validated, on all 13
  tori); whether the pair difference grows with the age of the life (a 2σ hint; a cap-free rerun of the pair at
  ± 0.002, about two core-hours, would settle it).
- Reading (conjecture). The lifetime of a periodic face is ln τ = c·A + (a term set by how the face closes on
  itself), and that term is not small, not constant in A, and not a function of one length. Two consequences.
  The constant c of an unwrapped face cannot be read off any one family of tori to better than about ± 0.004:
  the families give 0.205 to 0.2125 at these sizes. And the thin tori are a new handle for theory: a face three
  cells around is a quasi-one-dimensional system with a cost per cell (0.11) that a transfer matrix over the
  short direction might reach exactly, with 0.14, 0.19, 0.21 as the next rungs.

## 2026-11-14 — consistency corrections (consistency pass; numbers traced to data or scripts)

- **Local slopes of octahedral faces** (entry "GPU ensembles", lines 905–906): "0.201, 0.212, 0.212, 0.218, 0.221"
  mixes two values of ln τ_face at A = 84: 18.077 (CPU, 342 deaths) for 63 → 84 and 18.141 ± 0.005 (GPU, 34,026
  deaths) for 84 → 108. With 18.141 throughout: **0.201, 0.212, 0.215, 0.218, 0.221**, the GPU README's table
  column; with 18.077 throughout, 0.201, 0.212, 0.212, 0.221, 0.221. (Arithmetic on the lifetimes 6.804, 9.819,
  13.633, ·, 23.376, 29.34 at A = 30, 45, 63, 84, 108, 135.) [INCONSISTENCIES A2]
- **Vertex/cube factors** (entry "side-16 cube ends", line 710): the six factors "1.51, 1.52, 1.53, 1.60, 1.49,
  1.31 at A = 360 … 630" have five sources: `sym_residence.csv` has no cube-centred row at A = 360, and no version
  of the csv ever had one (checked back to d09388a, where the row set was added); `python3 research/fluct/sym_fit.py`
  prints the five at A = 408 … 630. Where 1.51 came from was not found. The flat ≈1.5 holds over **A = 408–630**;
  line 739's "A = 360–630" likewise. The 3.1 (ln 1.12 ± 0.29) at A = 693 is right: pooled vertex value (24 copies +
  5 soups) against the csv's 19.705 for `sym41c`; the fluctuation README's 3.3 used 19.64, a value the csv does not
  give (now corrected there). [B2, B3]
- **Density at R = 11** (entry "how chaos dies", line 307): from the regenerated `research/peeling/octa_first.csv`
  the first-peel means for p = 0.3, 0.4, 0.5, 0.6 are **1.00, 1.08, 1.00, 1.05 × 10⁵** (99,545; 108,090; 100,483;
  105,280), not 0.91, 1.08, 1.00, 1.04. The conclusion (density does not matter once the hull is filled) stands. [B12]
- **Thickness at A = 48** (same entry, line 298): `peeling/slab_area.csv` gives 9,878.7, 10,354.1, 10,323.0,
  10,345.8, 10,346.9, i.e. **9.9, 10.4, 10.3, 10.3, 10.3 × 10³** for m = 7, 8, 9, 10, 12 (the last two were
  written 10.4). [B13]
- **Side-16 first-peel forecast** (entry "side 16 loses its first face", line 629): with the committed forecast's
  inputs (8 deaths in 8.3×10⁹ replica-generations, alive at 1.45×10⁹; `predict.py`'s Lomax law) the outcome
  2,362,434,048 sits at quantile **0.566, the 57th percentile**, not the 58th. (`fluct/PREDICTIONS.md`'s "≈ 0.55" is
  the same quantity, rounded down.) [B14]
- **4 × 6 × 8 slab face** (entry "equal areas, different lifetimes", line 1353): the run's own value is
  **14.970 ± 0.002** (`python3 research/audit/gpu_pr16/recompute.py research/data/gpu_facelaw`); 14.971 is what one
  gets by pooling it with the same slab in the other orientation, 6 × 4 × 8 (14.972). The table's row is the width-4
  family, so 14.970 is the entry. [B6]
- **Count of claims** (entry "audit corrections", line 802): the ledger had 71 rows on 2026-11-13; it has 108 now.
  [C2; the same sentence is at `research/AUDIT-2026-11-13.md:4`, which is right for its date]
- **Index of sources** (entry "supertransients", line 889): `research/theory/swarm/library/shelf.md` now has 73 rows,
  not 59. [C4]
- **Exam score** (heading at line 1112 against line 1325): the heading counts the examiner's eight sampled entries
  (four hold, two fail, two undecided); line 1325 counts every entry of the board's closing table (five hold, four
  fail or missed, two undecided, three not run). Both are right for their sets. [C5]
- **Gump's slab slope in comparisons with other rules** (entry "the class theory attacked", line 1034, "gump's 0.212
  per face cell"): that is the area-only slope of slab faces of mixed widths over A = 27–75 (`theory/class.md`:488–489;
  0.2121 ± 0.0004 in `audit/REVIEW-class.md`:399). CLAIMS F4 (0.2088, A = 27–90) and GP9 (0.2072 within a width
  family; 0.2085 area-only over s ≥ 4) are the same kind of slope over other sets of faces. [B11]
- **Shortest-loop step 12 → 16 at A = 60** (line 1435: 0.051 ± 0.005): `shape/README.md` gives 0.052 ± 0.005 from
  the same classes (12.481 − 12.429); the census (line 1508, CLAIMS SH4) gives +0.056 to +0.063 with every class.
  The 0.051/0.052 difference was not traced (rounding of unrounded group means is likely, not checked). [B8]
- Lead's spot checks of this list: the five slopes by arithmetic; `python3 research/fluct/sym_fit.py` (0.698134,
  −0.195996; vertex-centred points start at A = 360, cube-centred ones do not); the R = 11 means in
  `research/peeling/octa_first.csv`; the A = 48 rows of `research/peeling/slab_area.csv`; 14.970 and 14.972 from
  `research/audit/gpu_pr16/recompute.py`. All as stated. Not re-checked by the lead: the csv's history, the quantile
  0.566, the shelf's row count. Source of the list: `docs/paper/INCONSISTENCIES.md` (34 places found while a
  manuscript-style draft was written, `docs/paper/draft.md`), resolved in 629fd03…15b1b4c; the ledger's ids K1–K3
  of the class study are now K9–K11, and its tally was recounted mechanically (108 rows: A 40, B 40, C 27, D 1; the
  earlier "A 43" had misread areas such as "A = 84" as grades).

## 2026-11-14 — a forecast before the run: empty patches on a face too large to die (asked of the GPU session, 21:22 UTC)

- The experiment: a periodic slab 12 × 12 × 8 (A = 432 per face; no face should die), and on its faces the
  frequency with which a patch (rhombi of 3ab cells from 1×1 to 6×6; strips 1×b) is entirely dead.
- Why: every measured cost per cell carries a wrap-around term (periodic faces, 0.205–0.2125) or a rim (octahedral
  faces, 0.215–0.221). If a face dies as "an empty patch the size of the face" (`research/theory/exponent.md`,
  section 4; compatible with the 2D toy, never tested for gump), then ln P(patch empty) = const − c·cells −
  σ·perimeter, with c the cost per cell of an unwrapped face.
- **Forecast (conjecture, the lead's, before any run):** for rhombi from 2×2 up, c = 0.21 ± 0.015. Outside
  0.17–0.25 the static picture fails for gump. No forecast for σ.
- Not done: nothing has been run. The request and its acceptance terms are in the message to the GPU session; the
  result will come as a pull request and be reviewed as before.

## 2026-11-14 — the counting line's proofs read a second time (independent audit; the lead re-ran one check)

- What was done: a second reader who had not seen the swarm audited every claim tagged proved in
  `research/theory/swarm/counting/claims.md` (22 claims, and the computed constants of claim 5), with its own code
  written from `docs/AUTOMATON.md`. Verdicts were committed before the critic's files were opened
  (e769776, 7f7dd9c) and reading them changed none. Report: `research/theory/swarm/audit/AUDIT-counting.md`;
  scripts `c0_lib.py` … `c6_compare_critic.py` in the same directory, logs in `audit/out/`.
- **Result: nothing tagged proved is wrong and no proof is missing.** 19 claims correct as stated (1–4, 6–8, 10,
  12–18, 21–24); one correct after filling a gap (19: the lemma takes a law on living states, the corollary applies
  it to product laws that charge the dead row; setting φ = 0 there closes it); two with one sentence true but
  narrower than worded:
  - claim 11, "a full face always dies", holds only on a rim-free face (the full face of the hull R = 3 over empty
    layers keeps 6 of its 9 cells);
  - claim 20, "no relative with an invariant measure charging the living states has a face that dies", needs the
    measure positive on every living state (gump on one cube: the point mass on the full cube is invariant, and 49
    other living states die).
- **One computed constant was wrong in the fourth digit** [exact]: the fixed-age exponent c₂ at density 0.472 is
  0.466846, not 0.4671. The critic's lab stopped its power iteration at 400 steps. The lead re-ran
  `cd research/theory/swarm/audit && OMP_NUM_THREADS=1 python3 c6_compare_critic.py` (1 min): the critic's own
  matrix gives 0.467096 at 400 iterations and 0.466846 at 3,000 and 10,000. c₁ = 0.551535, c₂ = 0.467693 (density
  ½) and 0.489963 are confirmed. The number 0.4671 appears only in the swarm's files (journal entry 9, the critic's
  reply and board), not in the ledger.
- Remarks of the audit outside the list (no verdict): "the density no longer matters at horizon 2" holds only for
  0.467 ≤ p ≤ 0.5 (c₂(0.44) = 0.411, c₂(0.40) = 0.334); "counting gives lifetimes ≥ c√L" needs inf c_k > 0, which
  is the line's unproved guess C2, and what is proved gives only k ≲ √(log L).
- Not checked by the audit: claim 9 (sketched), C2 (guessed), c₃ (measured), every number quoted from the exam or
  the lab's samples; Theorem 3 by computation for k ≥ 3; claim 14 at k = 3; claim 10 on the vertex-centred hull
  R = 4 beyond 14 of 512 face configurations. The lead re-ran only `c6`.
- What this changes: nothing in the swarm's bottom line. Both lines of the closed swarm that had proofs (path and
  counting) have now been read by two independent readers; the errors found were in wordings and in one
  convergence, none in a proof.

## 2026-11-14 — corrections from the fact-check of the manuscript draft (traced by a subagent; spot-checked by the lead)

- **Memoryless slab faces (entry of 2026-11-12, "how chaos dies"; ledger F5).** "CV 0.96–1.05, KS p 0.5–0.96 for
  A ≥ 36" is what the four m = 8 batches of the face-law fit (`research/peeling/face_law_fit.py`'s selection) with
  A ≥ 36 and a test give: 3×4, 3×5, 4×4, 4×5 (A = 36–60), CV 0.964–1.045, KS p 0.519–0.96; the fit's batches at
  A ≥ 72 have no test (55–475 of 512 runs censored at the cap). Over all 14 batches of `research/peeling/slab_area.csv` with A ≥ 36 and a test,
  p runs 0.042–0.974 (one below 0.05, 4×5×10) and CV 0.962–1.06. `python3 -c "import csv; [print(r['N1'],r['N2'],r['m'],r['cv'],r['ks_p']) for r in csv.DictReader(open('research/peeling/slab_area.csv')) if r['ks_p']!='nan' and int(r['A'])>=36]"`.
- **SH4 (entry "every torus of a given area").** The 0.0135 ± 0.0021 by which 4×4 lies below the (12; 19) class at
  A = 48 is the review's value; the census (`research/shape2/data/A48.csv`, 9.93842 − 9.93237, each ± 1/√F) gives
  0.0061 ± 0.0028. Pooled by inverse variance: 0.0108 ± 0.0017 (6.4 SE); agreement χ² = 4.4 on 1 (p = 0.036); with
  the error scaled by √χ², 3.0 SE. "Not ordered by shortest loop" stands.
- **Table 8 of the shape2 study, loop² 4, 60 → 72:** `research/shape2/data/explore_report.txt` and
  `python3 research/audit/shape2_lead_check.py` give 0.1353 (± 0.0008); `research/shape2/README.md`:189 prints
  0.1346 ± 0.0010.
- **Engine-only R = 9 (entry "a face dies off the end of a straight line").** Re-running
  `python3 research/experiments/face_endgame_check.py 9 16000` reproduces 13,765 peels, exposure 31,826,744,
  mean 2312.1 ± 19.7, −ln h/A = 0.2183, so ln τ_face = ln(8 × 2312.1) = 9.825 ± 0.009.
- **Twist lemma (entry of 2026-11-13).** The step giving m ∈ {1, 2, 3, 4, 6} is now written out in
  `research/clockwork/README.md`: G (the box's lattice symmetries p ↦ Rp + t, R ∈ O_h) embeds in O_h by linear
  part (a translation fixing a finite set is trivial), elements of O_h have orders 1, 2, 3, 4, 6 (R^c diagonal for
  c the order of R's permutation), and m divides the order of any g with k(g) = P/m. The hypothesis that G
  consists of lattice symmetries was implicit before.
- **Side-16 face deaths** 2,362,434,048 and 2,886,100,480 are last-alive generations (checks every 64); by the
  first-empty definition they lie in 2,362,434,049–112 and 2,886,100,481–544 (`research/data/cube16_events.jsonl`).
- Lead's checks: the counts for F5 from `slab_area.csv` (14 batches, p 0.042–0.974, one below 0.05); the pooled
  SH4 value by arithmetic (0.0108 ± 0.0017, χ² 4.5 on 1); the twist lemma's new step read line by line (the linear-part
  map is injective on the symmetries of a finite box; orders in O_h are 1, 2, 3, 4, 6; m divides the order of g): it
  holds for lattice symmetries, which is now a stated hypothesis. Not checked by the lead: the R = 9 re-run, the
  side-16 event file, whether the oscillator search (`find_map`) only ever uses lattice symmetries.
- Source: `docs/paper/FACTCHECK.md` (30 discrepancies in `docs/paper/draft.md`; all resolved or recorded there). The
  draft's novelty wording now follows `research/PRIOR-ART.md` strictly: three results (sealed sets, the boundary
  layer over noise, the shape dependence) had no recorded search; a third prior-art pass is running.

## 2026-11-14 — prior art, third pass (three results that had never been searched), and a conjecture it suggests

- Why: the fact-check of the manuscript draft found that three results called "apparently new" had no recorded
  search. A librarian searched (`research/PRIOR-ART.md`, "Third pass, 2026-11-14"; queries listed there). An
  adversarial pass on its "not found" verdicts is running and may change what follows.
- **The boundary layer over noise: the method is known; the result was not found.** Carretero-González, Ørstavik,
  Huke, Broomhead, Stark, PRL 83 (1999) 3633 (arXiv:chao-dyn/9904009, read in full by the librarian) drive a small
  window of a chaotic coupled-map lattice with white noise at its edges and recover the statistics of the large
  lattice. Ours is the mirror construction (keep the boundary layer, randomise the interior) and compares
  lifetimes, which nobody found does.
- **Shape of a periodic domain: an equilibrium analogue exists.** Caselle, Gliozzi, Vinti, Phys. Lett. B 302 (1993)
  74 (arXiv:hep-lat/9212013, read in full by the librarian): the tunnelling rate through an Ising interface on a
  periodic L₁ × L₂ cross-section is Z_cw(τ)·e^{−σL₁L₂}, the shape entering through the modular parameter τ of the
  torus (a Dedekind eta function), tested at equal area. Nothing found for chaotic transients, nucleation or
  extinction times, or for the shortest loop as the controlling length.
- **Sealed sets: an instance of a known notion.** Blocking words (Kůrka; Blanchard–Tisseur, arXiv:math/0312137):
  a word that disconnects the two sides for ever. Three dead layers are the simplest case in one lattice
  direction. "The largest sealed set only grows" follows from the definition: a remark, not a result.
- **Also found: the tail formula exists.** Sugimura and Kori, PRE 92 (2015) 062915 (arXiv:1512.08333): a transient's
  lifetime as the inverse of the stationary probability of the last state before absorption times an exit rate.
  Our "the death rate is the next point of the stationary tail" (M1) is an instance; their tail is assumed
  Gaussian, ours is measured to one cell.
- Not obtained: Tél–Lai 2008 (an author copy answered 503), dos Santos et al. 2008 (full text), others listed in
  the file. Not searched: what cites Houghton et al. 2010; lifetimes of topological memories on tori; pipe-flow and
  Kuramoto–Sivashinsky lifetimes against domain shape (the adversarial pass is asked to).
- **Conjecture (the lead's, not tested; passed to the analyst of `research/constant/` to state and test).**
  The wrap-around term of a periodic face is a sum over the face's nonzero period vectors of a function decaying
  over a correlation length: ln τ = a + A·[c − g·Σ_v f(|v|/ξ)]. Reasons: read off the census, the deficit of the
  cost per cell from about 0.215 is 0.100, 0.074, 0.023, 0.008, 0.006, 0.0025 at shortest loop² 3, 4, 7, 12, 13, 16,
  which falls roughly exponentially in the loop length (about e^{−1.6 s}) and not as its inverse square, so the
  massless (capillary-wave) form of Caselle et al. is less likely than a massive one; a sum over images gives a
  shape term that grows with area, as measured; and it gives a second variable of the measured sign (a shorter
  second loop adds a term, so the face dies sooner). If it holds, ξ should be close to the correlation length of the
  chaotic state measured independently (about 0.7 cube). Blind test: the pairs being measured in `research/shape3/`.

## 2026-11-14 — prior art, third pass: what the adversarial review changed

- The review (`research/PRIOR-ART.md`, "Adversarial review of the third pass"; 13 more works on the shelf, §11)
  tried to refute each "not found" of the entry above. One sub-claim fell, the rest stand with caveats.
- **Refuted: "nobody uses the shortest loop of a torus as the length that controls a lifetime."** Nardi and Zocca
  (arXiv:1708.09677, read in full by the reviewer) prove, for zero-field Ising and Potts dynamics on a K × L torus,
  a tunnelling exponent Γ = 2·min{K, L} + 2 and an exponential limit law: the shorter side, at leading order.
  Still not found: a chaotic, turbulent, nucleation or extinction lifetime depending on the shape of a torus at
  fixed area, or a twist dependence (nearest: Tuckett et al., PRX 9 (2019) 041031, where the failure of a quantum
  memory on a twisted lattice is controlled by a gcd of its dimensions).
- **"Death comes in through the boundary" is not ours.** Vidmar and Rappel, PRE 99 (2019) 012407
  (arXiv:1808.01991): the death rate of spiral-defect chaos is proportional to the length of the non-conducting
  boundary. The reduction of a lifetime to a thin layer over noise was still not found.
- **The tail formula is textbook.** 1/τ = Σ (exit rate × quasi-stationary probability) is standard theory of
  quasi-stationary distributions (Assaf–Meerson 2017, eq. 6); Nemoto and Alexakis (JFM 912 (2021) A38) use it for
  pipe-flow puffs. Correction to the entry above: Sugimura and Kori measure their distribution, they do not assume
  it. What remains ours in M1 is the measurement itself: a count followed down to one cell, with the exit rate
  measured, in a deterministic automaton.
- **Sealed sets are a 9-core.** A set is sealed when each cell has at least 9 of its 12 neighbours inside it, so
  the largest dead sealed set is the 9-core of the dead cells, equivalently the complement of the live set's
  closure under threshold-4 bootstrap percolation. The lead checked this from the definition (T6) and added it to
  `docs/AUTOMATON.md` as a remark. The reviewer's further reading (T6's "no finite sealed set" as a statement about
  that bootstrap rule being not subcritical in the sense of Gravner–Griffeath) is the reviewer's own and is not
  checked.
- Also on the shelf now: Lilienkamp, Christoph, Parlitz, PRL 119 (2017) 054101 (abstract only): in three
  dimensions transient lifetimes grow only above a critical thickness, the shape of our "three layers are needed".
- Not obtained: citation lists of Houghton et al. 2010 and Sugimura–Kori 2015 (the index refused), Tél–Lai 2008.
  Not searched: in-field Ising nucleation on rectangular tori (Borgs–Chayes–Tetali 2012 is the next lead),
  pipe-puff lifetime against pipe length, Boolean-network frozen cores.
- Where this leaves the list of what may be new (conjecture about the literature, as good as three searches): the
  face-area law in a vessel whose walls are theorems; the lifetime reproduced by five layers over coins; the
  dependence on the shape and twist of a periodic face for a chaotic transient, with a second variable; the
  exponential cost of symmetry. Not new: confinement by a high birth threshold, supertransients, the tail formula,
  boundary-controlled death, blocking sets.

## 2026-11-14 — is there one asymptotic cost per cell? The data in hand allow 0.207 to 0.219 (joint analysis of every family; adversarial review; lead's checks)

- What was done: `research/constant/` (README, `fit.py`, `load.py`, `shape_models.py`) fits every family of measured
  face lifetimes (periodic slabs by width, twisted tori, hull faces, symmetric faces; 64 points, all recomputed from
  tracked data), models stated before fitting, each scored on held-out largest sizes. No new simulation. Review:
  `research/audit/REVIEW-constant.md` with its own loader and fits (`research/audit/constant/`). The lead re-ran
  `python3 research/constant/fit.py` (35 s) and checked the inputs against earlier independent numbers (width-family
  slopes 0.2072, 0.2082: `research/audit/gpu_pr16_lead_check.py`; hull local slopes 0.2010, 0.2119, 0.2146, 0.2181,
  0.2209 by arithmetic on 6.8054, 9.8202, 13.6346, 18.1407, 23.3761, 29.3411).
- **Measured, model-free:** hull faces' local slopes at A = 63–108 (0.2146, 0.2182 ± 0.0013) lie above the slopes of
  periodic faces within a width family (0.2072 ± 0.0001, 0.2082 ± 0.0006), and the hull's are rising.
- **Fitted (review's version, which replaces the analysis's):** periodic slab faces give c = 0.207–0.216 depending on
  the form (statistical error about ± 0.003 once the width law is free: 0.2127 ± 0.0031); hull faces with one
  correction term give 0.218–0.232 depending on the term (1/A: 0.2181; 1/k: 0.2193; ln A: 0.2226; rim ∝ side:
  0.2317; all fit and forecast the held-out A = 108 and 135), and 0.2156 with a saturating slope.
- **The analysis's headline, "two families in tension; one constant only with a two-term hull correction, p ≈ 0.01",
  does not stand as stated.** The size of the tension runs from 1.7σ to 15σ across defensible pairs of forms, and a
  single constant passes with ordinary parameters: c = 0.2179 (hull correction 1/A; joint p 0.28; every residual
  ≤ 1.6σ) or 0.2155 (saturating hull slope). **Verdict: the data allow one asymptotic constant anywhere from about
  0.207 to 0.219; they do not fix it, and they do not show that there are two.** Preferring the periodic value
  (0.2085) is a judgement, not a result.
- **The lead's conjecture of the previous entries (wrap-around = a sum over period vectors decaying over a
  correlation length) is refuted as a law.** Neither that form nor the capillary-wave form fits at any scope
  (census A = 48 + 60: χ² 20,925/13 and 48,004/14), neither carries between thin and wide faces (thin tori shift the
  intercept as well as the slope), and both give the second variable its measured sign at about a quarter of its
  size (+0.004 against +0.0151, +0.0142). What survives as a description: the deficit of the cost per cell falls
  roughly exponentially in the shortest loop, but the decay length depends on the classes used (0.71–0.74 with the
  thin tori, 1.05 ± 0.10 or 0.42 ± 0.09 without), so its agreement with the chaotic state's correlation length is
  not established. The capillary-wave coefficient "κ = −1.01 ± 0.01 (the Ising value)" of the analysis does not
  stand: its jackknife error is ± 0.28 and it drifts from −0.72 to −1.43 between A = 48 and 72.
- Forecasts committed before data (`research/constant/PREDICTIONS.md`): (A) for the GPU patch experiment, blind;
  (B) for the pairs of `research/shape3/`, blind only on the analyst's word for some pairs (rows were in the tree
  minutes earlier; the analyst reported having seen four); (C) for a family of equilateral tori under three
  readings, with the outcomes that refute each (6c21dbd).
- Measurements proposed, as rated by the review: equilateral tori (useful: the widest periodic lever; they decide
  whether the periodic slope still rises with width, about 0.208 → 0.211 under one constant); equal-area hull faces
  with different rims (only if corners are matched: hexagonal faces of different side ratios); the width-6 slope
  (does not decide; withdrawn).
- Not checked by the review: the massive lattice-sum fits and their 0.2063; the symmetric-face fits; the 2D toy.
  Raised and open: whether the GPU kernel's settled-state test can miss settled lives of the kind the pairs
  experiment met in its own stepper (it would inflate large lifetimes in both families).

## 2026-11-14 — the asymptotic constant: what the corrected analysis adds (addendum to the entry above)

- The analyst applied the review's corrections (`research/constant/README.md`, 3fbd2a1) and reproduced every
  number of the review it checked. Over 84 pairings of a hull form with a periodic form, 36 pass with one constant
  at p ≥ 0.01 (c = 0.2072 to 0.2190) and 13 at p ≥ 0.05 (up to 0.2179). The write-up now quotes 0.213 ± 0.006 as a
  range, not a standard error.
- **Fitted, and the useful part: the passing readings split in two.** Every one with c ≤ 0.214 needs a two-term
  correction on hull faces. Every one with c ≥ 0.2155 needs the cost per cell of a periodic face to approach c as
  slowly as 1/s in the width s; with 1/s² or an exponential approach none passes. So either the hull's rim is
  complicated, or wide periodic faces are still far from their limit. (Conjecture, the lead's: the second is hard to
  square with the thin tori, where the deficit falls roughly exponentially in the shortest loop; that argues for the
  lower half of the range. Not tested.)
- The analyst and the review differ on what would decide (README, "Where the analysis and the review differ"):
  the analyst holds that hull A = 108 at 10⁴ deaths (about 4 GPU-hours) would eliminate 35 of the 36 single-constant
  readings if the value stays where it is; the review called that point not decisive. For the equilateral tori the
  analyst's forecasts under the single-constant readings are local slopes 0.2117 → 0.2136, with the existing 6×6 run
  already 2.7–3.2σ below them (`research/constant/PREDICTIONS.md`, part C and its addendum; committed before any of
  those runs exist). Neither measurement has been run; both need the GPU.

## 2026-11-14 — empty patches on a face too large to die: the forecast missed as stated, and the perimeter-free cost falls into the lifetime range (GPU session's pull request 18; adversarial review with an independent CPU stepper; lead's recomputation)

- What was done (`research/gpu/README.md`, section "Empty patches on a large living face"; raw counts
  `research/data/gpu_patches/`): a periodic slab 12 × 12 × 8 (A = 432 per face), 3.04 × 10¹⁰ replica-generations,
  no face death, settling or firewall in any replica. At every generation, on both faces, the number of translates
  of each fixed patch shape (rhombi a × b of 3ab cells, strips 1 × b, hexagonal balls) whose cells are all dead.
  Forecasts were committed before any code (312b0bc; the lead's is in this notebook, entry "a forecast before the
  run").
- **Measured** (ln P of an empty patch; reproduced digit for digit by `python3 research/audit/gpu_pr18_lead_check.py
  research/data/gpu_patches/patches_s81*_A10G.csv`; confirmed up to 4×4 by the reviewer's own stepper and counter
  on the CPU, |z| ≤ 1.9): rhombi 2×2 −6.254, 2×3 −8.793, 3×3 −12.128, 3×4 −15.400, 4×4 −19.423 ± 0.007,
  4×5 −23.318 ± 0.047 (654 hits), 5×5 −28.4 ± 0.6 (4 hits), none at 5×6 and 6×6. Strips cost a flat 0.55 per cell.
  At 36 cells a 1 × 12 strip is e^−4.5 as likely as the 3 × 4 rhombus. Persistence (empty again one generation
  later) falls with size, 0.38 → 0.10.
- **The lead's forecast is missed as stated.** It said the fit ln P = const − c·cells − σ·perimeter over the rhombi
  from 2×2 would give c = 0.21 ± 0.015, and that outside 0.17–0.25 "the static picture fails". The fit gives
  c = 0.264, σ = 0.119, and does not describe the data (χ² 3,369 / 3; its c moves to 0.211 or 0.249 when the
  smallest shapes are dropped). So the criterion was badly designed: it presumed the two-term form. The miss is a
  failure of that form, not evidence about the static picture.
- **Post hoc (the lead's reading after seeing the data, checked by the review and re-derived by the GPU session):**
  along a sequence of similar shapes (a × a, or a × (a+1)) the second difference of ln P removes the constant and
  any term linear in the side (perimeter, corners, the two orientations). It gives a perimeter-free cost per cell of
  0.273, 0.252, 0.237, **0.2185 ± 0.008** at middle shapes of 12, 18, 27, 36 cells: still falling, and at the
  largest size inside the lifetime laws' range. It does not remove a logarithm or a 1/a term. Extrapolations that
  fit give 0.21 (corrections ∝ 1/n) or 0.16 (∝ 1/√n); the review's range for the asymptote is 0.16–0.24.
  **So: compatible with "a face dies as an empty patch of its own size at about 0.21 per cell"; not established.**
- Found by the review: the patches are built from the three +faces of a cube, so the two faces of the slab carry
  the two inequivalent orientations of each shape, and the table averages them (the inner orientation is more often
  empty, by about 0.007 per perimeter pair; no effect on second differences). The incremental cost "0.32–0.42 per
  cell, well above the lifetime range" of the first write-up included the added perimeter and was not comparable.
- **Open: the 4×5 point.** The reviewer's CPU run has it at −23.75 ± 0.16 (43 hits), 1.9–2.6σ below the GPU's.
  The last second difference rests on it (with the CPU value it would be about 0.29). The reviewer is running ten
  times longer; until that is in, 0.2185 ± 0.008 is the GPU's number with one unresolved cross-check.
- Not checked: the GPU code was read, not run, by the review; patches beyond 4×5 (they need a biased estimator);
  dependence on slab thickness, soup density and face size; whether a 12 × 12 face is in the same state as the face
  of a small dying slab; emptiness in the layers beneath.
- The analyst's blind forecast for this experiment (`research/constant/PREDICTIONS.md`, part A: c = 0.212 ± 0.015,
  σ > 0 at about 0.086 per cut pair, −ln P = 5.0, 9.5, 15.3, 22.4, 30.8 for 2×2 … 6×6) is to be scored against the
  table: measured −ln P at 2×2, 3×3, 4×4 is 6.25, 12.13, 19.42 against its 5.0, 9.5, 15.3 (the lead's arithmetic:
  low by 1.3, 2.6, 4.1); σ's sign is right, its size 0.119 against 0.086 under the failing two-term fit.

## 2026-11-15 — the second variable at equal shortest loop: not found. The effect is gone by A = 72 and changes sign on short loops (pairs experiment, forecasts first; adversarial review with its own stepper; lead's recomputation)

- What was asked: two periodic slab faces with the same area and the same shortest closed loop can differ in
  lifetime (entries "the shortest way round" and "every torus of a given area": +0.015 at A = 48, +0.014 at
  A = 60, the one with the shorter second loop dying sooner). Which variable is that? `research/shape3/`: five
  candidate formulas, each fitted on the three known pairs only, forecasts committed (46baf66) before any run;
  eight-layer slabs, renewal lives from 0.4 soups, no age cap.
- **Proved** (an identity, and an enumeration repeated by the review, `python3 research/audit/shape3/enum_check.py`):
  the reduced Gram matrix (Q1, 2B, Q2) of a face torus of index n = A/3 has Q1·Q2 − B² = 0.75 n². So within a
  group of equal area and equal shortest loop² Q1, one number fixes the lattice; second loop, third loop, angle and
  Re τ are the same information. At every n ≤ 28 no two classes share a Gram matrix, so lattice-scale quantities
  (rows, transverse layers, firewall cuts) are functions of it too. Hence candidates can differ only in the *form*
  of the dependence, never in sign within a group. Groups with Q1 ≥ 12 exist at A ≤ 84 only for A = 48, 60, 72
  and 84 (at 72: one pair and one triple).
- **Measured** (d = ln τ_face of the member with the longer second loop minus the other; from the raw per-job
  counts, `python3 research/audit/shape3_lead_check.py`):

  | pair | A | loop² | d | independent stepper (review) |
  |---|---:|---:|---|---|
  | P1 | 48 | 12 | +0.0144 ± 0.0019 (pooled with earlier runs +0.0148 ± 0.0013) | |
  | P3 | 60 | 12 | +0.0075 ± 0.0033 (pooled +0.0069 ± 0.0024) | |
  | T01, T12 | 72 | 16 | −0.0062 ± 0.0041, +0.0005 ± 0.0041 (correlated −0.5: they share a torus) | one job on the shared torus, 0.8σ from theirs |
  | N72 | 72 | 12 | +0.0018 ± 0.0061 | |
  | Q36 | 36 | 9 | **−0.0223 ± 0.0007** | **−0.0220 ± 0.0009** |
  | Q45 | 45 | 9 | +0.0076 ± 0.0013 | +0.0085 ± 0.0014 |
  | Q54 | 54 | 9 | −0.0020 ± 0.0019 | |
  | Q63 | 63 | 9 | +0.0017 ± 0.0020 | |

  At A = 72 "no difference" fits (χ² 2.9 on 3 with the covariance, `python3 research/audit/shape3/score_check.py`).
  On the short loop the difference is large at A = 36 and of the *opposite* sign, positive again at 45, and zero
  within error at 54 and 63. P1 shows no growth of the difference with the age of a life (the 2σ hint on the
  A = 60 loop² 16 pair was not retested: that pair was not rerun).
- **Candidates** (`research/shape3/PREDICTIONS.md`; the review's wording, which replaces the write-up's "survives
  out of sample"): under the committed rule all five are refuted (χ² ≥ 111 on 7). On the three loop² ≥ 12
  differences alone, a split chosen after the data, the two forms that decay with the second direction (a sum
  over closed loops Σ e^(−1.41|v|) with amplitude ∝ A; a modular form e^(−2πh) cos 2π Re τ) are not rejected (χ² 6.6
  and 8.6 on 3, p 0.09 and 0.04), but zero fits better; the three size-free forms (linear in the second loop, linear
  in the angle, cos 2π Re τ) are excluded there too (p ≤ 8 × 10⁻⁶ with the covariance). No candidate can give a
  negative difference, so none describes loop² 9.
- Scored as owed: the analyst's two wrap-around models (`research/constant/PREDICTIONS.md`, part B: massless and
  massive, fitted to lifetimes of wide faces) forecast +0.0008, +0.0008, +0.0001, 0.0000 for T01, T12, N72, Q63:
  Σz² = 3.7 on 4 (the lead's arithmetic), not refuted there, and indistinguishable from zero. They were already
  refuted as a theory of the effect by P1, Q36 and Q45. "The shorter second loop dies sooner" (CLAIMS SH2) holds at
  A = 48 and 60, fails at A = 36, and is empty at A = 72.
- **Reading [conjectured, the lead's].** There is no second geometric variable in the sense looked for. The
  equal-loop differences are at most 0.02, irregular in sign on small faces and gone at A = 72, while the
  dependence on the shortest loop itself grows with area (entry "every torus of a given area"). That is what a
  commensurability effect looks like (how the chaotic state's short-range structure fits round a small torus), not
  a term of a large-face law. If so it does not enter the question of the asymptotic constant; the test is that
  equal-loop differences stay below 0.005 at every A ≥ 72 (A = 84 has two pairs with loop² ≥ 12).
- Checked by the review (`research/audit/REVIEW-shape3.md`; own stepper `st.c`, bit-exact against the engine on
  seven tori, events every generation, a settled test that catches any period): the sign change (table), the
  labels (which member has the longer second loop), the counts (all 35 job rows recount from the raw event files),
  the forecasts' commit order. Not checked: Q54, Q63, P3, N72 and two of the three triple tori were not rerun; the
  review's event detectors agree with the experiment's but are not themselves validated against the engine; the
  per-job counts of unrecognised settled lives on (1,3,12) are overdispersed (11, 0, 3, 1) and unexplained.
  Absolute values from the experiment's stepper carry the 8-generation event window (+0.003 to +0.004 in ln τ at
  A = 36, where a life lasts 800 generations; nothing in the differences).

## 2026-11-15 — lives that settle and are not recognised ("zombie lives"): found in three steppers, measured, and bounded in every earlier run (CPU: two lines and a review; GPU: bounds from the committed logs, pull request 20)

- **The failure.** Every lifetime measurement here restarts or censors a replica that has settled into a periodic
  state without losing a face. The CPU steppers recognised "settled" by comparing with the state 840 generations
  earlier, which catches only periods dividing 840. A replica in a cycle of any other period is never recognised,
  never has a face death, and adds exposure until the run ends or an age cap cuts it. Found independently on
  2026-11-14 by the thin-face line (`research/theory/thin/README.md`: a whole-slab cycle kept both faces alive for
  3.6 × 10⁷ generations) and by the pairs experiment (`research/shape3/README.md`: 14 of 512 replicas at the end
  of a cap-free A = 36 job, 1.7% of the exposure, +0.017 in ln τ).
- **Measured** (`research/audit/REVIEW-shape3.md`, claim 3): such a state exists (42 cells on the torus (1,4,12),
  period 16; `python3 research/audit/shape3/zombie_check.py`, the engine confirms the period; the lead re-ran it);
  periods seen 9, 11, 13, 16, 19, 22, 48, 52. Rate: 35 of 1.01 × 10⁷ lives at A = 36 (3.5 × 10⁻⁶), about 4 × 10⁻⁶
  at A = 48. Detected settling of every period falls steeply with area (hundreds per 5 × 10⁵ lives at A = 48, none
  or one per job at A = 72).
- **Bound on earlier CPU results** (same review, `capcount.py`): with the age caps those runs had, the shift in
  ln τ is at most 0.0004 at A = 48 (counted from event files), 0.0007 at A = 60 (assuming every settled life
  carried a full cap), 10⁻⁵ at A = 72 and in the census's own runs. No published difference in `research/shape`,
  `research/shape2` or their reviews can move by more than its error. Fixed going forward: the pairs stepper
  compares with snapshots 840·m generations back for m ≤ 128 (misses only periods with p/gcd(p, 840) > 128; the
  largest period among 13,000 settled lives was 52); the review's stepper and the thin line's use doubling
  snapshots, which catch any period.
- **GPU kernels** (the GPU session read its code and logs; no runs; `research/gpu/README.md`, "Zombie lives";
  `python3 research/gpu/zombies.py`): periods 1–2 are detected exactly, periods up to 128 in most runs (not in the
  hull runs R11–R17 of pull request 8, nor in the patch runs, which step one generation per launch); **no age
  cap**. Bound, from deaths at old ages against hazard × exposure (one-sided 95%; "all ages" assumes such replicas
  appear at a constant rate): R11 (A = 63) ≤ 1.3 × 10⁻⁴; R13 (A = 84) ≤ 2.0 × 10⁻³ beyond 3.3 mean lives and
  ≤ 6.7 × 10⁻³ at all ages, against a statistical error of 0.005; symmetric R43 s501 ≤ 1.2 × 10⁻² against 0.013;
  slab 4×8×8 ≤ 1.0 × 10⁻² against 0.018; the rest ≤ 2 × 10⁻³. The lead recomputed R11 and R13 with separate code
  and an exact Poisson bound (`python3 research/audit/gpu_pr20_lead_check.py`: same figures). These are upper
  bounds on a possible upward bias, not measured biases; no bound excludes zero.
- **Not bounded:** runs shorter than about one mean life give no age test (hull R15 at A = 108 and R17 at
  A = 135, symmetric R43 s201, R44, R45, slabs 6×6×8 and 6×7×8, five of the wider firewall-resolved slabs). There
  the argument is a rate: moving R15 by its error would need 2–3% of lives to be of this kind, against
  < 10⁻⁴ wherever it can be measured and a detected settling rate that falls with size. **That the rate does not
  rise with vessel size is assumed, not shown [conjectured].** Patch counts (pull request 18) show no signature
  (4×5 hits per seed 216, 213, 225, even over halves of each run).
- Owed: a guard in the GPU drivers before any further lifetime run (doubling snapshots, or an age cap at 30 mean
  lives; described in `research/gpu/AGENT.md`, not written, since it cannot be tested without the GPU).

## 2026-11-15 — the thinnest face: no derivation; its cost per cell is about 0.099 (0.093 to 0.107), half a wide face's, and the census's 0.115 and 0.111 were local slopes (theory line; adversarial review with its own stepper; lead's re-run of the refits)

- What was asked (`research/theory/thin/`, 2026-11-14): the census found that a periodic face whose shortest
  closed loop is one cube step (loop² 3; the torus with periods (1,1), (0,b); a ring of b sites of three cells,
  A = 3b) costs 0.115 and 0.111 per cell instead of 0.21. Derive that number: put noise beneath the face, then
  solve a one-dimensional problem exactly.
- **No number was derived from the rule**, for three stated reasons, each of which the review confirmed:
  - *Noise is enough only from five layers* [measured]: the rule on the top w layers over coins (density 102/256)
    gives the deterministic ln τ within +0.006 ± 0.003 at w = 5 (review, own stepper: +0.0017 ± 0.0018) and is off
    by +0.049 at w = 4 (review +0.0497 ± 0.0023) and by 0.4–2.3 at w ≤ 3. Five layers are 15 cells per site. The
    same depth as on wide faces (entry "where the exponent lives", 2026-11-14).
  - *The exactly solvable model is the wrong one* [exact]: one layer over coins has ln τ = 3.967199 on a ring of
    5 sites and 2.453108, 4.192750 on segments of 2 and 5 (reproduced to all digits by the review's own enumeration,
    `python3 research/audit/thin/exact.py`); its slope is 22% above gump's, and two better closures are 11% and
    5.6% above.
  - *The face dies by fronts* [measured]: looking back from the death, the live part is an island shrinking from
    both ends (population 1.70, 4.05, 7.36, 10.14, 12.58, 15.16 at successive steps back, review at b = 32; the
    line's 1.7, 4.1, 7.3, 10.1, 12.6, 14.8), over a time proportional to its length. The cost per site is a
    large-deviation rate of a front in a medium five layers deep.
- **Measured instead.** Ring lifetimes (ln τ 8.6470, 10.0199, 11.3448, 12.6482, 13.9233, 15.1644 at b = 16 … 36)
  bend: the cost per cell is 0.1144, 0.1104 over A = 48–72 (the census's two numbers, which are therefore local
  slopes, not a constant), 0.1081 ± 0.0003 over 72–84 and 0.1067 ± 0.0004 over 84–96 (review's own rings), about
  0.103 at 108. A face with two free ends (a ring with a wall of dead face sites) gives a straight 0.0993 ± 0.0003
  per cell from A = 75 to 135 (review: 0.2981 ± 0.0003 and 0.2978 ± 0.0006 per site over n = 21, 29, 37).
- **The long-face limit: about 0.099 per cell, range 0.093–0.107.** The line's "0.099 ± 0.004" did not survive
  review as an error bar: it was the spread of the correction forms the line had chosen. Forms it had not tried
  fit its data as well and land outside (segments with a √n term 0.093; rings with a ln b term 0.094; the wall
  front with a third term up to 0.105; the review's own rings allow 0.107). The lead re-ran
  `python3 research/audit/thin/refit.py`: same table; it also shows that a √b correction would allow 0.08 on the
  line's six rings (χ² 0.7 on 3); the review's more precise rings reject that form (χ² 11.7 on 3), which is why
  its range leaves it out. If the four
  routes (rings, segments, empty windows, the front's distance from a wall) share one limit, the overlap is
  0.097–0.102 [conjectured].
- So the thinnest face costs about half of what a wide one does per cell (0.21), with the same five-layer depth
  and no derivation of either number. What sets the ratio is open.
- Found on the way, by the line and again by its review: lives that settle unrecognised (entry above). The
  review's tail check of the line's raw files finds such exposure in two model runs, worth 2 × 10⁻⁴ in ln τ:
  nothing quoted moves.
- Forecasts (`research/theory/thin/PREDICTIONS.md`, 14, each committed before its run; none edited afterwards):
  the review finds the line's tally generous (two "halves" are mostly misses, one clause failed, one value lies
  outside its interval).
- Not checked by the review: b = 20 and 36, segments of 45 and 61 sites, its own window and wall runs (those two
  routes were refitted from the line's histograms), the coin-density forecast, 12 layers, the two better closures,
  the wider torus. `research/audit/REVIEW-thin.md`; seven corrections are being applied to the write-up.

## 2026-11-15 — corrections found while the manuscript draft was brought up to date (traced by a subagent, `docs/paper/FOR-LEAD.md`; applied by the lead)

- Entry of 2026-11-14 "is there one asymptotic cost per cell?": the hull local slope from A = 84 to 108 is
  **0.2181 ± 0.0013**, not 0.2182 ((23.3761 − 18.1407)/24 = 0.21814). CLAIMS CN1 corrected; CN1 now also carries
  the addendum's statement (36 of 84 pairings pass, c = 0.2072–0.2190).
- Entry of 2026-11-15 "lives that settle and are not recognised": "the rest ≤ 2 × 10⁻³" should read ≤ 2.1 × 10⁻³
  (symmetric R38 is 2.1 × 10⁻³ in `research/gpu/README.md`). And one run is missing from the list with no bound:
  the slab 4×7×8 (A = 84), whose log has no age bins (`python3 research/gpu/zombies.py` prints so). CLAIMS ZL2
  corrected; the GPU session's README omits it too and has been told.
- CLAIMS GP10: the part that rests on the GPU alone (4×5 and beyond) is graded B−, as the legend requires, not B.
- New ledger rows for forecasts that had none: TH7 (the thin line's 14 forecasts as rescored by the review: 8 hit,
  2 half, 2 mostly missed, 2 missed) and CN2 (the analyst's forecasts for the patches and the pairs, scored by the
  lead; graded C). Ledger: 126 rows (`python3 research/audit/claims_tally.py`).

## 2026-11-15 — what the unrecognised settled states are: five new clocks, a 4 × 13 compound, and wires (naturalist's identification of 37 states; lead's check with a stepper written from the rule document)

- The 37 settled states of period 9 to 52 that the review of the pairs experiment logged (entry "lives that
  settle and are not recognised"; `research/audit/shape3/zombie_states.txt`, from 8-layer slabs on the tori
  (1,3,12), (1,4,12), (1,4,15), (1,5,15), (2,2,8)) were identified against the catalogue
  (`research/clockwork/README.md`, section "Found by accident in lifetime runs, 2026-11-15";
  `cd research/clockwork && python3 zombies.py --write`, about 80 s).
- **None needs the walls** [proved, by stepping]: each repeats its cycle cell for cell on the same torus with
  the slab widened to 24 layers.
- **14 are finite objects of free space** [proved, by a lift whose orbit maps one-to-one onto the slab's]. Four
  are in the catalogue (P9.20a, P13.22a, the twisted P16.15a, P3.13a). **Five are new**: C9.24a, C9.28a, C11.29a,
  C13.24a and **C52.33a**. The lead re-derived all five with a stepper written from `docs/AUTOMATON.md` §2 alone
  (`python3 research/audit/clockwork_zombies_lead_check.py`): periods 9, 9, 11, 13, 52; populations 24–25, 28–33,
  29–34, 24–28, 33–38; unions 27, 35, 36, 30, 42.
- **Period 52 is a compound, not a loop** [proved for the cell periods; the dependence by subset tests]: no cell
  has period 52. Of its 42 cells 24 are still, 4 turn with period 4 and 14 with period 13 (the lead's stepper
  gives the same split). The period-13 part cannot run without a still chunk that in turn needs the period-4 part,
  and no moving cell's next state depends on the other clock: a 4-clock and a 13-clock on a shared frame, like
  C44.26a (4 with 11). One of the two period-48 states is P16.15a beside P3.13a, touching and exchanging nothing.
- **21 are wires** [measured]: the moving part has no finite lift to free space, but lives on a strip that is
  periodic along one short vector of the torus, so in the infinite lattice it is an infinite oscillating line.
  Periods 9, 11, 13, 16, 19, 22, along (3,0,−3), (1,3,−4) or (2,−4,2). Every state of period 19 here is a wire.
  **2 are sheets** [measured]: they fail on every strip and on covers up to 3 × 3 and close only on their own
  torus; one, of period 48, is a mirror-twisted cycle of the torus (1,4,12): phase t + 24 is the mirror image of
  phase t under a mirror that is a symmetry of that torus [proved], the construction of P66.27a with the box
  replaced by a torus.
- So the lifetime runs' "zombies" are mostly not clocks one could put in a box: more than half are objects that
  exist only because a small torus lets a line close on itself. That fits their rate falling steeply with area.
  Wires and sheets are a kind of object the catalogue (finite objects only) does not hold.
- Not checked: whether a wire's moving part could be held by a finite stator ("needs the torus" is measured on
  lifts of the given states, not proved); whether wires of one period and direction are the same wire; sheets on
  covers beyond 3 × 3; stability and basins of the new objects. The census lists the new objects were matched
  against are git-ignored scratch files of the clockwork line.

## 2026-11-15 — the symmetric collapse: pairing faces across an edge is what costs; "a penalty along the mirror lines" does not stand as told (theory line with 38 forecasts; adversarial review running the unreduced system with its own stepper; lead's re-run of the validation and tables)

- What was asked (`research/theory/symmetric/`, PROGRAM M5): derive the three fitted ingredients of the law for
  fully symmetric faces, ln τ ≈ 0.698 + (0.209/6)·A − 0.196·√A (CLAIMS S2) and the factor of about 1.5 between
  centrings (S3), from the asymmetric law and geometry. The notebook's picture since 2026-11-12 was "six lockstep
  domains minus a mirror-line term".
- **No derivation came out.** What did:
- **Proved** (checked by the review's own computation, one lemma apart): a G-symmetric state evolves exactly as
  gump on the orbit graph, and for free actions the factor 1/|G| is exact. Inside a {111} face the only mirrors
  are the three diagonal ones and their translates. A coordinate mirror never preserves a face: it exchanges two
  hull faces and fixes the rim row they share. (A lemma about cells far from fixed cells is false as stated; no
  measurement uses it.)
- **Measured, by two codes** (the line's orbit stepper, bit-exact against the engine on 41 systems, lead's re-run
  `python3 research/theory/symmetric/validate.py`; and the review's stepper on the full unreduced system,
  `research/audit/symmetric/`): in an octahedral vessel at A = 63 (R = 11, cube-centred), ln τ_face is

  | symmetry imposed | line | review |
  |---|---|---|
  | none | 13.634 ± 0.018 | 13.638 ± 0.010 |
  | one coordinate mirror (one edge of every face in lockstep) | 11.456 ± 0.011 | 11.444 ± 0.010 |
  | two (two edges) | 9.291 ± 0.008 | 9.312 ± 0.009 |
  | three, D2h (three edges) | 7.168 ± 0.003 | 7.171 ± 0.009 (35% of exposure in settled lives; bracket 7.02–7.29) |
  | inversion (pairs faces that share no edge) | 13.578 ± 0.014 | 13.574 ± 0.014 |

  **Each edge shared with a face that is forced to die at the same moment costs about 2.15, additively; pairing
  faces that share no edge costs at most about 0.1.** A twofold rotation about an edge, split by which faces it
  pairs (the review's correction: the line had pooled them), costs 2.54 ± 0.02 on the edge-sharing faces
  (cube-centred; 1.96 ± 0.02 vertex-centred) and about 0.1 on the opposite ones: no mirror is needed.
- **Measured:** a mirror, a threefold axis or both, imposed on a rim-free periodic slab face, *lengthen* its life
  against the asymmetric torus of equal area (+0.4 to +1.65 at 36–72 quotient cells; one pair rerun by the review:
  +0.926 ± 0.014 against the line's +0.872 ± 0.013), by an amount that shrinks with size. The line had forecast a
  loss.
- **What may be said, in the review's wording:** in a fully symmetric face the lockstep rim lies on a coordinate
  mirror, so "rim" and "mirror" cannot be separated there; and faces with diagonal mirrors and free rims (T_d) fall
  below the mirror-free ones (T) by an amount growing like √A, so a diagonal-mirror share of up to about a third
  of the −0.196 is not excluded. **So the 2026-11-12 picture is corrected, not reversed: the cost is mainly that
  edge-sharing faces die together and cannot hold each other up, and "the chaos runs thin along mirror lines" is
  not the mechanism of most of it.** [the mechanism itself is conjectured: nobody looked at the faces]
- **The 1/6:** slope × order of the face's stabiliser is 0.2091 ± 0.0016 for T faces (threefold axis, free rims,
  A = 108–198) and 0.2035 ± 0.0024 for T_d (A = 315–459), 3–5% lower. "c/6 within 5%" is supported; "exactly c/6"
  is not shown, and c itself is only known to 0.207–0.219. A wedge is not a torus of A/6 cells: mirror-bounded
  quotients outlive the equal-area torus by an offset that shrinks with size.
- **The √A term:** the rim's marginal cost is 0.45–0.55 per rim period over 5.5–9 periods (three families). With
  0.408·√A periods in a wedge that is a coefficient of −0.19 to −0.22, close to the fitted −0.196, **but the review
  shows the agreement is a coincidence of ranges, not a test** (the fitted coefficient moves by −8.1 per unit of the
  assumed c; with c pinned at T_d's own 0.2035 the fit gives −0.127). Whether the rim term bends, and so whether
  −0.196·√A is an asymptotic form at all, is open: the fall in marginal cost rests on the two smallest sizes
  (without them −0.02 ± 0.04 per period²). A T_d ensemble at A = 759 would speak to it (forecasts 26.2–26.4 if
  linear, 25.65 ± 0.25 if T_d keeps its slope; only 1.9σ apart), and needs a GPU.
- **The factor between centrings** is not one object: asymmetric faces already differ, vertex-centred minus
  cube-centred = +0.75, +0.73, +0.66 at A = 30, 45, 63 (review: +0.754 ± 0.013, +0.725 ± 0.009, +0.655 ± 0.017),
  falling with size (χ² 21 on 2 against a constant); with lockstep rims a part grows (D2h: 0.505, 0.645, 0.830 at
  A = 63, 84, 108). For O_h a constant factor is excluded by the line's fit (χ² 60.8 on 10; not refitted by the
  review). So "about 1.5 times tougher" (S3) is a snapshot of a slowly changing difference.
- Forecasts: 40 statements counted per size; 25 held, 1 on its limit, 14 failed; each committed before the output
  it is scored on (one block while its runs were in progress, disclosed).
- Not checked: nothing beyond A = 63 was rerun by the review (the rim figures are refits of the line's data); each
  number is one job with one seed; the mechanism was never looked at directly (no occupancy maps of dying faces);
  group O lying far below T_h, T_d's two sub-series moving apart, and mirror strips two cells wide keeping a slope
  of 0.186 are unexplained. `research/audit/REVIEW-symmetric.md`; eleven corrections are being applied to the
  write-up.

## 2026-11-15: the audit of the rows nobody had re-run

The ledger had 30 claims whose best grade was C ("has a command, not re-run") and a dozen more with a C part. An
auditor (a second agent, not the producer of any of them) ran what could be run in a few minutes each.
`research/AUDIT-2026-11-15.md` has the table; its helpers are in `research/audit/c_rows/`.

- **Result [measured].** 41 rows read, 28 re-run in whole or in part, **26 matched, 2 differ** (P4 and a sentence
  of ZL2), 13 not run. The ledger now reads **133 claims: A 56, B 66, C 10, D 1** (was A 56, B 46, C 30, D 1);
  `python3 research/audit/claims_tally.py`.
- **What a match means here.** Eight rows were re-run on the producer's own seeds (F10, K2, P5, Z5, Z10, SW3, SW4,
  SW7): that checks the code and the transcription, not the statistics. Four were rebuilt from the producers' raw
  records, which are not in git, without repeating the simulations (F11, S1, C7, L3: "B (table)"). One was repeated
  on fresh seeds (K1, the thickness of a living slab: every mean within 2 combined standard errors, the largest gap
  2.0σ at N = 32, m = 2).
- **Three matches rest on a choice the claim did not record**, now written into the level cells: F2's plateau
  heights (ratios 0.770, 0.604, 0.454 over whole plateaus against the claimed 0.79, 0.61, 0.48; a trimmed window
  moves them by about 0.03); P6's {110} front speed (0.165 only if the fit window ends by generation 80; 0.154 over
  generations 60–110, because **that front slows down**, which nobody had noted); F11's fit (the stated
  coefficients need weights by the firewall-first counts; unweighted, −2.00 + 0.533·N·m + 0.356·N).
- **P4, the correlation length of the chaotic phase, was wrong in its error and slightly in its value
  [measured, corrected].** The notebook's "ξ = 0.68 ± 0.01 cube" could not be reproduced as stated: no fit was
  recorded. The lead's own fit (`python3 research/audit/p4_lead_check.py [file]`, written without the auditor's
  script) finds where it came from: the Ornstein–Zernike form fitted to k ≤ 3 per cube gives 0.681 ± 0.009 on the
  producer's file, exactly the old number, but the form does not fit that far (χ² 53 on 19 with corrected errors;
  59 on 19 on the auditor's snapshots). It fits for k ≤ 2.5 (χ² 8.2 on 15 and 22.8 on 15), where **ξ = 0.638 ±
  0.013 on the producer's 12 snapshots and 0.659 ± 0.014 on the auditor's** (8 of its 12 are new); windows from
  k ≤ 1.5 to k ≤ 2.5 give 0.61–0.69 (the short windows carry errors of 0.035–0.06). Recorded now as **ξ = 0.65 ± 0.03 cube**, S(0) = 3.04–3.18. The error bars of
  `research/phase/sk.py` were too small by √24: it divided the scatter over modes of the snapshot-averaged S by
  modes × snapshots, counting the 12 snapshots twice (the auditor's find), and it counted both members of each
  ±k pair, which are equal for a real field (the lead's addition). With that mended the isotropy statement
  survives, which with the old errors it did not: cones about ⟨100⟩, ⟨110⟩, ⟨111⟩ against the sphere average for
  k ≤ 1.5 give χ² 5.4, 11.9, 10.9 on 11, 11, 10 bins (producer's snapshots) and 15.5, 12.6, 3.9 (auditor's), every
  p ≥ 0.16. `sk.py`
  is fixed; files written before the fix are recognised by the check script and rescaled. Not checked: sizes other
  than N = 64; anisotropy at larger k, where the lattice must show.
- **The restated value was then refitted by a second agent with its own code** (`research/audit/REVIEW-p4.md`,
  `python3 research/audit/p4_second_fit.py`): every figure above reproduced, with two corrections that are already
  in the text above. The windows reach 0.69, not 0.67 (first written as 0.61–0.67). The cone comparison first
  treated cone and sphere as independent (χ² 6.6, 6.2, 6.7 and 17.8, 5.4, 2.3); a cone's modes are a subset of the
  sphere's, and the figures above use the right variance. Also from that review: the factor √24 is exact for these
  bins and shows in the data (the difference of the two snapshot sets gives χ² per bin 1.06 with corrected errors,
  25.4 with the old ones); the second set's fit at k ≤ 2.5 is marginal (p = 0.09); with the old errors the k ≤ 3
  fit has χ² 1276 on 19, so "0.68 ± 0.01" was never tested against its own fit.
- **ZL2: a slip of the lead's in the ledger.** "others ≤ 2.1 × 10⁻³" left out slab 4×9×8, whose bound is
  4.2 × 10⁻³ (against a statistical error of 0.042, so no number moves). The README table had it right.
- **Two commands did not run as written.** `portrait.py OID NS` failed with a NameError (the seed was set only in
  one branch): fixed, and the lead re-ran Z10's basin count with it (`cd research/clockwork && python3 portrait.py
  P66.27a 1000000`, 76 s: 414 of 10⁶, as claimed, seed 1). SW3's command needs a binary that no script builds; the
  build line is now in its row.
- **Still C (ten rows):** F12, S4, K5 (the ledger gives no arguments), Q4 (names no run), G3, G4, K7 (an hour or
  more each), K8 (several scripts of unstated length), L2 (re-run only by repeating the lead's own arithmetic), and
  Z13 (the wires, added after the audit began). With a C part: Z2 at n = 16, Z4's period-3 search, TH5's segment
  n = 7 and its percentages, TH2, TH4, C2, C4, C8, Z3's flip property, Z10's phase shifts, Z12, S9, X3's 6.94, ZL2's
  other runs. (The tally script had read the
  object names C44.26a and C35.29a in the rows Z8 and Z9 as grades; fixed, no best grade changes.)
- Not checked by the lead beyond P4 and Z10: the other 24 matches are the auditor's alone. No proof was re-read
  in this audit.

## 2026-11-15: how a face dies (the first look, reviewed)

The symmetric study had explained the short lives of symmetric soups by ties across edges without anyone looking
at a face. `research/dying/` looks: 11,930 first face deaths at R = 11 cube-centred (faces of 63 cells) in c1, csz,
c2v, D2h (no, one, two, three edges shared with a face in lockstep), each with the 512 generations before it, and a
stationary control. Review with an independent stepper and fresh seeds: `research/audit/REVIEW-dying.md` (stepper
`research/audit/dying/dy.c`, matched to the oracle at every generation on twelve systems). The lead's recomputation
from the study's table: `python3 research/audit/dying_lead_check.py`. Figure: `research/figures/dying_face.png`.
The lead's forecasts were committed before the runs (`research/dying/PREDICTIONS.md`, 75e5212).

- **The mean face does not erode from an edge [measured; study and review agree].** It stays at its stationary
  density until about 20 generations before death and then fades over the whole face; relative to its own
  stationary value a band along a tied edge empties no earlier than one along a free edge. The final plunge takes
  the same time in all four groups (median 6, 6, 7, 7 generations in both codes) while the lifetimes differ by
  e^6.5: whatever a tie does, it does not change how the end runs.
- **A single death is not a uniform fade [measured, the review's correction].** At half population a third of
  single deaths (32–39%) are more lopsided than 95% of stationary faces thinned at random to the same count (9–11%
  in a control 64 generations earlier). The lopsided side is not the tied edge and does not persist beyond what
  thinning implies. The mean map hides this.
- **A tied edge is thinner at all times [measured; reproduced to three digits].** Stationary occupancy of the rim
  row: 0.512 along a free edge; 0.349, 0.323, 0.298 along a tied one (csz, c2v, D2h). The stationary face population
  is 31.25, 28.90, 26.28, 23.50 (review, ± 0.004–0.02; study 31.29, 28.83, 26.29, 23.77), and cube-centred the loss
  sits in the rim row itself (−1.77 of csz's −2.35). The loss per tied rim cell is the same at R = 13 (0.149–0.186
  against 0.148–0.185), so the loss per tied edge grows with the rim; vertex-centred faces spread it over rows 1
  and 2.
- **Two readings of that, withdrawn after the review.** The study wrote that the population falls in steps as equal
  as those of ln τ; the steps are −2.35, −2.62, −2.77 while ln τ's are −2.18, −2.17, −2.12. The lead wrote that a
  live cell lost at a tied edge costs 0.86 in ln τ, "twice the 0.436 per live cell of the untied face": it is 0.93,
  0.83, 0.77 along the ladder (0.64–1.00 over the three vessels the review measured), and 0.436 was an average, not
  a marginal. What survives [measured, one comparison at two sizes]: growing the untied face from 63 to 84 cells
  buys 0.40 in ln τ per stationary live cell gained, re-centring at equal area 0.23, and a cell lost at a tied edge
  costs about twice the first. **ln τ is not a function of the mean population**: the vertex-centred csz face has
  more live cells (31.60) than the cube-centred untied one (31.25) and lives 1.45 shorter in ln τ.
- **The neighbour [measured, mostly a tautology].** The study found the neighbour's band along the shared edge at
  0.21 of stationary when an untied face dies. Adjacent faces share their rim row (the same 12 cells), so most of
  that is the dying face's own cells. What survives: the neighbour's own second row falls to 0.56–0.61 of
  stationary and the rest of it stays at 0.95.
- **The lead's forecasts L2–L7 failed** (the rim is not the late survivor: ratio 1.06–1.22 against a forecast of
  1.5; the tied edge is not where emptying begins; the neighbour does not stay within 10%; the plunge is not
  faster with more ties). The review confirms the definitions were fixed before the data and the scores stand; L4
  becomes undecided with another choice of band. L1, the deduction that a tied edge cannot be a separate local
  route to death because the ladder's steps multiply rather than add, is consistent with everything seen.
- **A caveat on D2h [measured by the review].** 36.5% of old living D2h states are in lives that have settled
  (none in c1 and csz, 1.2% in c2v); their faces hold 15.45 cells. The stationary control leaves them out, the
  ln τ rung counts their exposure (its estimator spread 7.02–7.29 is that), so the D2h point of the population
  ladder and the D2h rung of the lifetime ladder are not taken over the same lives.
- Not checked: other sizes for deaths (the review's other vessels are stationary sampling only); c2e and O_h; the
  layers beneath the face and the last-alive maps (the study's `explore.py`); differences of 1.8σ between the two
  codes in the csz and D2h populations and 2.7σ in the L6 fraction are unresolved. Rounds 2 and 3 of the same
  study (what starts a collapse; the same across sizes) are not in this entry.

## 2026-11-15: a death is a dip that keeps going (round 2 of the dying-face study, reviewed)

`research/dying/README.md`, "Round 2" (forecasts 6d40e72 before the runs; results 3bf2f21, 4b41de0); review with an
independent stepper and fresh seeds, `research/audit/REVIEW-dying.md`, "Round 2" (e5153ea); the lead's
recomputation from the study's tables, `python3 research/audit/dying_lead_check.py`. Figure:
`research/figures/dying_excursions.png`. Same vessel as round 1 (R = 11 cube-centred, 63 cells; c1, csz, c2v, D2h),
plus stationary sampling at R = 13 (84 cells).

For a face with stationary mean population P̄, let ν(p) be the rate per face per generation of excursions that
start above the mean and reach p·P̄, and q(p) the fraction of those that end in the face's death before the
population is back above the mean. Then 1/τ_face = ν(p)·q(p) at every level, by bookkeeping.

- **The bookkeeping closes on the lifetimes measured before [measured, two codes].** −ln(νq) = 13.632, 11.454,
  9.274 for c1, csz, c2v in the study and 13.614, 11.473, 9.275 in the review, against 13.634, 11.456, 9.291 from
  the symmetric study. D2h depends on what is done with lives that settle: 7.32 with them, 6.86 without, 7.168 in
  the study.
- **Nothing special starts a collapse [measured, two codes].** A face dips all the time. Dips to 0.7 P̄ come about
  once per 60 generations per face and equally often whatever the ties (ln ν = −4.16, −3.80, −3.77, −3.74 in the
  study; −4.16, −3.80, −3.78, −3.88 in the review). At 0.9 P̄ the untied face even dips more often. The four groups
  part only below about 0.6 P̄.
- **The point of no return is a handful of cells [measured, two codes].** q = 1/2 at p = 0.079, 0.114, 0.152,
  0.245 of the mean for c1, csz, c2v, D2h: about 2.5 live cells of 31 in the untied face. An untied face that has
  lost half its cells recovers 99.92% of the time (q(0.5) = 0.0008). So the face population is a fair coordinate
  for the death, and the plunge of round 1 (the last 20 generations) is the end of a dip, not a separate event.
- **Where the ladder lives depends on the level asked [measured].** From c1 to D2h ln τ falls by 6.46: at p = 0.5
  that is 1.59 in ν and 4.88 in q; at p = 0.1, 5.38 and 1.09. What does not depend on the level: ties do not make
  dips start more often, they make each further step down from about 0.6 P̄ more likely (ln q higher by 1.5–2.7 per
  tied edge between 0.9 and 0.4 P̄).
- **The shape of ln ν [measured; the lead's reading corrected by the review].** Gaussian with the stationary
  variance down to about 0.6 P̄ (residuals −0.15, −0.43, −0.27 at 0.8, 0.7, 0.6 in c1; the lead's forecast A2, the
  only one of seven that held), and fatter than Gaussian below (+4.1 at p = 0.1). The lead fitted a straight line
  over 0.1 ≤ p ≤ 0.45 (0.499 per live cell lost in c1; 0.436, 0.350, 0.231 with one, two, three tied edges; per
  unit p 15.6, 12.6, 9.2, 5.5) and read it as "a constant price per further cell lost, 5.5 + 3.4 per free edge".
  The review reproduces the slopes (15.55, 12.57, 9.19, 5.51) and does not confirm the reading: the tail is close
  to straight but not straight (the local slope per cell drifts 0.51 → 0.45 → 0.34 in c1), there is no change of
  regime at half the mean, and the step per free edge ranges from 3.0 to 4.5 with the fit window and with the
  treatment of settled lives. **What stands: over the last 3–12 cells the price per further cell lost is nearly
  constant, and it is higher the more free edges a face has. [conjectured, weakened]** The lead's picture of a live
  clump and a hole coexisting on a depleted face is not supported by the clumping: at equal count, dying untied
  faces are less lopsided than stationary faces that are low by chance (2.47 against 3.09), dying D2h faces more
  (2.94 against 2.70).
- **Births fail before survival [measured, two codes], mostly for a plain reason.** On a dying untied face births
  per empty cell are 0.90–0.91 of stationary at lag 16 while survival is 0.98–0.99; at lag 8, 0.45 and 0.88. Much
  of the birth deficit is what the face's own lower population predicts (review: births 0.61 at lag 8 where the
  face's own population predicts 0.77).
- **Depleted faces are lopsided whether or not they die [measured for c1].** The survivors' centroid sits 1.6 times
  further from the centre than in a face thinned at random, in dying faces and in stationary faces that are low by
  chance alike. The single-death lopsidedness of round 1 is this.
- **A two-constant fit to the stationary state is not a law [measured].** ln τ = 3.43 + 0.582·P̄²/(2σ_P²) fits the
  eight lifetimes at 63 and 84 cells within 0.31 (review: 3.42, 0.584, leave-one-out 0.50); a + b·A + c·P̄ with no
  variance in it fits as well (0.27). Stationary values at 84 cells: P̄ = 42.49, 39.81, 36.86, 33.48; σ_P = 5.96,
  6.18, 6.50, 7.05.
- **The lead's round-2 forecasts: one of seven held** (A2). Failed: the point of no return at 0.25–0.5 of the mean
  (it is 0.08); the ladder in ν rather than q at half population (the reverse); uniform fades inside single deaths;
  survival holding while births fail (survival clause); 2.8–3.1 cells lost per tied edge at 84 cells (2.68, 2.95,
  3.38) with 0.86 per cell (0.98, 0.90, 0.84); and that no function of the stationary mean and width would fit
  (one does, though see above). Definitions were committed before the runs; the review reproduces every score.
- Not checked: excursions at other sizes or centrings (round 3 is on sizes); one seed per group in the study (the
  review adds a second); every D2h exposure quantity depends on the settled lives; births by neighbour count;
  whether the position of the surviving clump predicts recovery.

## 2026-11-15: the 4 × 5 empty patch, rerun on the CPU (addendum to "empty patches on a face too large to die")

The review of GPU pull request 18 had the 4 × 5 rhombus at ln P = −23.75 ± 0.16 on 43 CPU hits against the GPU's
−23.318 ± 0.047, and the last perimeter-free cost per cell rested on that point. The reviewer reran it: plan
committed before the first run (dac1634), 16 new chunks with fresh seeds, 18 CPU runs in all, 2.76 × 10¹⁰
replica-generations (0.9 of the GPU's exposure). `research/audit/REVIEW-gpu-pr18.md`, dated follow-up;
`python3 research/audit/gpu_pr18/followup.py research/scratch/pr18 research/data/gpu_patches/patches_s81*_A10G.csv`
(the lead reran it: same figures; the raw CPU runs are in scratch, not in git).

- **The disagreement is gone [measured].** 4 × 5: CPU −23.412 ± 0.049 (541 hits) against GPU −23.318 ± 0.047, 1.4σ;
  combined −23.364 ± 0.034. 3 × 4: −15.3979 ± 0.0011 against −15.3999 ± 0.0011. 4 × 4: −19.4183 ± 0.0072 against
  −19.4233 ± 0.0071. The first CPU value was a low fluctuation on 43 hits. Nothing points at the GPU's counter.
- **The last cost per cell moves up, and one sentence is withdrawn [measured].** Perimeter-free cost per cell
  (second differences along similar shapes) at middle shapes of 12, 18, 27, 36 cells: CPU 0.2729, 0.2513 ± 0.0002,
  0.2359 ± 0.0012, 0.2349 ± 0.0082; GPU 0.2729, 0.2517, 0.2368, 0.2185 ± 0.0079. At 36 cells the two combined give
  **0.226 ± 0.006**. The earlier "0.219 ± 0.008, already inside the range of the lifetime laws (0.205–0.221)" is
  withdrawn: it is about 1σ above that range. The sequence is still falling; extrapolations are unchanged (0.208 if
  the correction goes as 1/n, 0.156 as 1/√n), and the asymptote stays open at 0.16–0.24.
- **The errors were right [measured].** Hits come in clusters (1.19–1.40 hits per event; corrected 2026-11-15, the first figures given here were the error factors), so the
  true error is 1.13–1.28 times the Poisson one; batch means capture that, and the scatter over 18 runs equals the
  batch-means error. The reviewer withdraws its earlier remark that its errors were 1.4 times too small.
- The two orientation classes of rhombus differ in ln P (−0.52 ± 0.07 at 4 × 5) and agree in the cost per cell
  within 0.008.
- Not checked: run-to-run scatter per class; no firewall test in the CPU runs; 5 × 5 and beyond remain GPU only
  (queued for a second card, `research/GPU-QUEUE.md` item 5).

## 2026-11-15: a second card (the GTX 1080: acceptance, a guard against settled lives, and an anchor that was a high draw)

The owner's GTX 1080 now carries the GPU arm (its session works from `research/GPU-QUEUE.md`; its files are under
`research/gpu-local/` on branch `claude/gpu-local-1080`, pull request 23, not yet merged). Its first report covered
the acceptance bar, the guard that every earlier GPU run lacked, and one calibration. Reviewed with independent code
and no GPU: `research/audit/REVIEW-gpu-local-pr23.md` (code in `research/audit/gpu_local_pr23/`). The lead
recomputed the calibration figure from the branch's csv row (exposure 76,418,398,524 replica-generations, 7,478,823
face deaths).

- **Acceptance passes on the card [measured by the producer; the port checked by the reviewer].** Both kernels are
  bit-exact against the engine every generation on the cases of `research/gpu/README.md`; the reviewer confirmed
  that every check of the Modal acceptance is called with the same functions and arguments, and noted one omission
  (the face-law driver's own calibration). Throughput 7–10 × 10¹¹ node-updates per second on the faster kernel;
  not checkable here.
- **A guard against unrecognised settled lives exists [measured on a CPU stand-in; B].** `research/gpu/guard.py`:
  one snapshot per replica at doubling ages, compared at every launch boundary; a replica equal to its snapshot is
  in a cycle and its life ends as censored (kind 5). Off by default, and the reviewer checked line by line that
  nothing changes when it is off. On the CPU, against about 7,600 planted lives with cycles of period 1 to 12,345
  and both kernels' layouts, it recognised no chaotic life and missed no cycle, and two deliberately broken guards
  were caught. One claim of the producer's README does not hold: for an odd period above 128 the delay between
  settling and recognition is period × launch length, at least 3.4 × 10⁷ generations at the longest launch, which
  is a mean life or more at A ≤ 93. Guarded results therefore have to cut the kind-5 exposure at the snapshot age,
  or give both figures. CLAIMS GL2.
- **The 4 × 4 torus anchor on file was 0.0075 too high [measured, three codes; A].** GPU: ln τ_face = 9.9251 ±
  0.0004. The reviewer's own bit-sliced stepper (checked against the engine every generation, with two negative
  controls): 9.9246 ± 0.0006 over 2.9 million deaths. The original `research/shape2` pipeline on 152 fresh seeds:
  9.9240 ± 0.0014. The file's 9.9324 ± 0.0020 reproduces bit for bit from its 76 seeds, so it was a high draw
  (3.4σ once the between-job scatter, χ² 100 on 75, is allowed for), not an error in the pipeline. **Best value
  9.9249 ± 0.0003.** Consequences: the census gap at loop² 16 against 12 becomes 0.0135 ± 0.0020 (SH4; 0.0138 against the reviewer's own stepper value; the tension with that
  review's 0.0135 is gone); the loop² 16 slope from A = 48 to 60 becomes about 0.2131 (SH3); the forecasts of
  `research/constant/PREDICTIONS.md` part C keep their committed text, with a dated note giving what they become
  with the anchor replaced. CLAIMS GL1.
- **A caution that follows [measured].** The shape2 pipeline's per-job scatter is mildly larger than Poisson (χ² per
  degree of freedom 1.33 and 1.12 on the two sets), so its quoted errors are 5–15% small. One 3.4σ draw among the
  24 torus values of the census is unlucky rather than alarming (about one chance in sixty), but it was a value
  used as an anchor. Where a
  single torus value carries an argument it should be measured twice.
- **Also confirmed by the reviewer:** `fwslab.py` undercounts firewalls where lives settle (18% at 4 × 4; first found
  in `REVIEW-gpu-pr14.md`; on the ledger it touches only small-slab ln τ_fw, by at most 0.034 at 4×5×8); the effect
  of launch length on earlier GPU runs is at most 0.003 wherever per-life data exist, and unbounded but probably
  0.003–0.005 for the s = 3 slabs.
- Not checked: nothing was run on a GPU; the GPU-side guard tests and the throughput are the producer's word; the
  5 × 5 anchor has one measurement (queued on the card); the hull-face forecast in the producer's file centres on
  the value it re-measures, and its premise "no settled lives at A ≥ 90" is false (both to be corrected in a new
  block there).
- Five corrections are asked of the producer before the merge (`research/GPU-QUEUE.md`, note of 05:30 UTC).

## 2026-11-15: what the dips say about the price of a cell (round 3 of the dying-face study, reviewed)

Round 3 (`research/dying/README.md`, "Round 3"; forecasts T1–T4 committed first; figure
`research/figures/dying_ratefunction.png`) measured the rate ν(p) of dips to a fraction p of the usual population
on free (c1) hull faces of 45, 63, 84 and 108 cells and on one rim-free face (the equilateral torus n = 21, 63
cells), and looked at what a depleted face looks like. Reviewed with its own stepper on fresh seeds, with 135 cells
added: `research/audit/REVIEW-dying.md`, "Round 3" (code `research/audit/dying/r3_*`). The lead recomputed the tail
slopes and the shallow part from the study's table (`python3 research/audit/dying_tangent.py`) and the end-effect
line by hand from the GPU's lifetimes and the study's ln ν(0.9) (7.481, 11.324, 15.789, 20.871 at the four sizes:
slope 0.2125, offset 2.08).

- **The dip curve per cell is one curve only down to about half the population [measured; A].** −ln ν(0.5)/A =
  0.120, 0.103, 0.093, 0.089, 0.086 at A = 45 … 135: the raw curve does not collapse (forecast T1a failed). Measured
  from the rate of shallow dips, [ln ν(0.9) − ln ν(0.5)]/A = 0.065–0.067 at every size. Below p ≈ 0.55 the curves
  of different sizes differ by a fixed number of nats K(p), not by a number per cell: K grows smoothly from 0 at
  p ≈ 0.55 to 2.1 at p = 0, half of it below p = 0.15. ln ν(0.9) itself is not size-independent: it falls by about
  0.002 per cell. DY8.
- **The end effect, and what the dips do not settle [measured; A for the line, B for the estimate].**
  ln τ_face + ln ν(0.9) = 0.2125·A − 2.07 to within 0.01 nats over A = 45–108. The slope depends on which dip rate
  is called the attempt (0.218 for every crossing of the mean, 0.213 for ν(0.9), 0.204 for ν(0.8)), because the
  shallow rates carry a part proportional to A. The dips at p ≥ 0.2 alone, extrapolated in size and then to p = 0,
  give **c = 0.215 ± 0.005**: they cannot separate 0.207 from 0.219 and add nothing to what the lifetimes' own
  local slopes say (0.212–0.221). Withdrawn: the study's "levelling off near 0.19–0.20, below c" (the end points
  follow c − K/A and are still rising at 135 cells); the lead's K ≈ 2.4 paired with c = 0.21–0.22 (not constant:
  2.37 → 2.78); the lead's formula for c from the density and the Fano factor (arithmetic whose two terms each miss
  what is measured). DY9.
- **The tail [measured; A].** Over 0.1–0.45 of the usual population the price is 0.50–0.52 per live cell at A ≥ 63,
  rising slowly with size (0.44–0.47 at 45 cells); locally it runs from 0.53 deep down to 0.40 near half. Forecast
  T1b failed as registered (a count-weighted fit, which integer thresholds break); the unweighted fit would have
  held. DY10.
- **What a depleted face looks like [measured; B].** c1 faces of 63 cells caught at 0.3 of their usual population
  (8.3 live cells on average): near a survivor the face is at about half its stationary density (0.46–0.54 by
  measures that do not align on the face's own centroid; the study's 0.6 was a quarter alignment), the excess
  reaches about 3.5 doubled units (under two cubes), and the rest of the face sits at 0.15–0.20 of stationary:
  thinner far away, not emptied. Thinner faces have a looser patch (0.54 at 7–9 cells, 0.38 at 3–6). A thin csz
  face is depleted at its tied edge beyond the stationary deficit (centroid nearest the tied edge in 22.4% of
  faces against 29.8% for thinned stationary faces; the tied third holds 0.82 of the face's mean relative
  occupancy against 0.99). T2 failed (no patch at 0.8 of stationary), T3 held. "Refills from its patch" (T4,
  held) has no content: a rule-aware baseline gives 0.991 against the observed 0.994. DY11.
- **The rim-free face lives longer than every forecast for it [measured by one code at this precision; B].** The
  equilateral torus n = 21 (63 cells; the study's vessel is its mirror image) has ln τ_face = 13.176 ± 0.011
  (reviewer, two seeds, 7,746 deaths; the study has 13.13 ± 0.04). The forecasts of
  `research/constant/PREDICTIONS.md` part C for this torus were 13.115 ± 0.004 (flat), 13.128 ± 0.006 (massive),
  13.107 and 13.100 (rising); with the corrected 4 × 4 anchor they are lower still. So it lies 0.05–0.07 above all
  of them, 5σ above the flat reading. The three anchors of part C are tori whose shortest loops run along the
  lattice rows and whose slabs have many layers between possible firewalls (4 × 4, 5 × 5, 6 × 6); this is the
  first measured of the other kind: its shortest loops are oblique (4 rows and 1 across), and its transverse layer
  period is 4, so there are only two classes of layer and no dead layer anywhere. Which of the two differences
  carries the 0.05 is not known; in the massive reading the excess would need an effective loop of 4.39 against
  the Euclidean 4.58. [conjectured, the lead; forecast in a dated block under part C] The tori of this second
  kind (n = 19, 21, 31, 37) sit above the readings anchored on the first kind, and those of the first kind
  (n = 27, 28) do not. Queued on the graphics card: this torus and n = 19, beside the A = 93 run (n = 31) already
  going there. No firewall can form on this torus. Its dips differ from the hull face of the
  same area: shallow dips 1.4 times as frequent and dearer per cell (0.077 against 0.067), tail cheaper (0.43
  against 0.50 per live cell). DY12.
- **Forecasts.** T1a, T1b, T2 failed; T3, T4 held (T4 nearly forced by the rule). Over the three rounds three of
  the lead's eighteen held.
- **Next [conjectured, the lead; forecasts committed before the review arrived].** Gump's rule is cooperative, so
  a face cannot be thinned uniformly below some density and live; a deeply depleted face would then be a mixture
  of a void and a remnant at fixed density, and the dip curve a parabola joined to its tangent
  (`research/dying/PREDICTIONS.md`, "Round 4", F1–F6: a lever rule). The review's alignment-free figures cut both
  ways: half density near survivors is where the tangent construction puts the remnant (0.55–0.62), but the far
  field is not empty and the patch loosens as it shrinks. Round 4 measures it on larger faces at several depths.
- Not checked: one fresh seed per hull size (two for the torus); the lifetimes at 108 and 135 cells are the GPU's;
  the study's own runs were not rerun; the patch in csz and D2h and its change with depth were not measured.

## 2026-11-15: the 93-cell torus lands below every reading (GTX 1080; recomputed by the lead; not yet reviewed)

Branch `claude/gpu-local-1080` at dcb61c8 (pull request 23): `research/gpu-local/README.md`, "Equilateral face
tori"; rows `research/data/gpu_local_eqtorus/eqtorus_1_5_31.csv`. The lead recomputed the figure from the four
rows (exposure 4.796 × 10¹² replica-generations, 35,521 face deaths, per-seed values 19.408, 19.418, 19.412,
19.419, χ² 0.70 on 3): `git show origin/claude/gpu-local-1080:research/data/gpu_local_eqtorus/eqtorus_1_5_31.csv`
and ln(2E/F).

- **n = 31 (A = 93): ln τ_face = 19.4141 ± 0.0053 [measured by the producer; C until reviewed].** Guard on; no life
  settled in any way (45,761 lives); the hazard is flat by age within errors and shows no burn-in.
- **Against part C of `research/constant/PREDICTIONS.md`.** Flat 19.479 ± 0.010 (19.484 with the corrected anchor):
  the measurement is 0.065–0.070 below, about 6σ, and below the forecast's own refutation line (19.445).
  Rising 19.506–19.530: refuted (line 19.488). Massive 19.437 ± 0.019: 0.023 below, 1.2σ of the forecast's error.
  So of the three readings only the one in which the price per cell falls with size survives, and the torus sits
  on its low side. The lead's N1 (written at 05:49 UTC without having fetched the branch, on which the result had
  been pushed two minutes earlier: "above the flat reading by at least 0.03") failed outright, and with it the
  idea that tori without a cut sit above the others.
- **Local slopes in the family [measured].** 4 × 4 → 5 × 5: 0.2124 ± 0.0001. 5 × 5 → n = 31: 0.2085 ± 0.0003.
  n = 31 → 6 × 6: 0.2103 ± 0.0028. At constant shape the price per cell is lower on the larger faces. The hull
  family's local slopes at the same areas are 0.2146–0.2181 and its dips give 0.215 ± 0.005, so the two families
  are now further apart at 75–108 cells than at 48–75; one constant for both needs one of them to turn.
- **n = 21 does not fit this picture.** The CPU value 13.176 ± 0.011 (DY12) is 0.064 above the chord from 4 × 4 to
  5 × 5 (13.112); with it the slopes would run 0.2167, 0.2071, 0.2085, 0.2103. Either the family is not smooth in
  n, or that value is wrong. The card will measure n = 19, n = 21 and 5 × 5 with the driver that measured 4 × 4
  and n = 31; its own forecast for n = 21 is 13.124 ± 0.008 (its `PREDICTIONS.md`, section 2).
- **A bias in the CPU census pipeline, found on the way [measured by the producer's subagent on the same lives; not
  reviewed].** `rep.c` looks at a layer's last-alive generation every 16 generations, so ends are rounded up and
  0.09% of face deaths are booked as something else: +0.0016 on ln τ at A = 48 (mean life 8,200 generations),
  negligible from about 60 cells up. With 1,024 fresh seeds the 4 × 4 torus is 9.9270 ± 0.0005 under that rule and
  9.9255 ± 0.0005 counted every generation (the card: 9.9251 ± 0.0004). So GL1's best value is the per-generation
  one, the value on file was 2.6σ high under its own rule, and every A = 48 census value carries about +0.0016 in
  common (differences between classes at one area are not touched; slopes from 48 to 60 are low by 0.0001).
- Not checked: no second stepper at A = 93 (the kernel is engine-exact on this torus for 2,000 generations; the
  driver's counting is checked through the 4 × 4 comparison only); the bias figures are the producer's; an
  adversarial review will take this together with the three tori now running.

## 2026-11-15: five wrapped faces on one driver: a straight line from 63 cells up (GTX 1080; recomputed by the lead; review started)

Branch `claude/gpu-local-1080` at b843883; rows `research/data/gpu_local_eqtorus/eqtorus_*.csv` there. The lead
recomputed every value and the per-seed χ² from the rows (ln(2E/F), ± 1/√F).

| n | lattice | A | face deaths | ln τ_face | seeds |
|---:|---|---:|---:|---|---|
| 16 | (4,0),(0,4) | 48 | 7,478,823 | 9.9251 ± 0.0004 | 1 |
| 19 | (1,7),(0,19) | 57 | 3,283,133 | 11.8756 ± 0.0006 | 2, apart by 2.6σ (11.8742, 11.8771) |
| 21 | (1,4),(0,21) | 63 | 1,811,510 | 13.1622 ± 0.0007 | 2, χ² 0.07 |
| 25 | (5,0),(0,5) | 75 | 183,954 | 15.6630 ± 0.0023 | 2, χ² 0.39 (on file 15.6614 ± 0.0026) |
| 31 | (1,5),(0,31) | 93 | 35,521 | 19.4141 ± 0.0053 | 4, χ² 0.70 on 3 |

- **n = 21 is confirmed by a second code [measured; A].** The CPU review's 13.176 ± 0.011 and the card's
  13.1622 ± 0.0007 are 1.25σ apart. So that torus does lie above every reading of part C (0.034 above the massive
  one, 0.047–0.051 above the flat one), and n = 19 does too (0.021 above massive, 0.034–0.039 above flat).
- **Local slopes [measured]:** 0.2167 (48 → 57), 0.2144 (57 → 63), 0.2084 (63 → 75), 0.2084 (75 → 93). The three
  tori from 63 to 93 cells lie on one line, ln τ = 0.033 + 0.2084·A, to within their errors (0.002–0.005); the
  smaller ones lie below it, by 0.111 at 48 cells and 0.036 at 57. So at constant shape the bend is all below 63
  cells, and it is the small tori that are short-lived, not the large ones that are cheap. The three readings of
  part C were all anchored on the 4 × 4 torus and tilted with it.
- **What it suggests [conjectured].** The price per cell of a periodic face is 0.2084 from a shortest loop of about
  4.6 cube steps up. The 6 × 6 value on file (22.568 ± 0.041) is 0.7σ above the line. The card's forecast for the
  four tori now running (81, 84, 108, 111 cells: 16.913, 17.539, 22.540, 23.165) is that line, committed before
  those rows existed; the lead has none better.
- **Against the hull family.** Free hull faces of the same areas live longer by 0.41, 0.47, 0.60, 0.84 at 45, 63,
  84, 108 cells (against the line), and their local slopes run 0.2119, 0.2146, 0.2181, moving away from 0.2084,
  not toward it. One constant for both families now needs the hull slope to turn round beyond 108 cells and fall
  by 0.01; the other reading is that a face held by living neighbours along its rim and a face wrapped onto itself
  have different prices per cell. CN1's range (0.207–0.219) is the two families, not an uncertainty in one number.
- **The lead's forecasts.** N1 (n = 31 above flat by 0.03) failed; N2 (n = 19 above flat by 0.03) held, at 0.034
  to 0.039, though the reason given for both (tori without a cut sit above) is ended by n = 31 and by 5 × 5 lying on
  the same line as its neighbours. N3 (n = 27, 28) is open.
- Not checked: no second stepper at 57 cells or at 75 and above on this driver (5 × 5 agrees with the CPU value on
  file); the two seeds at 57 cells differ by 2.6σ; whether lattice direction matters is confounded with size in
  this family (5 × 5 on the line says not much). An adversarial review with a CPU stepper is running.

## 2026-11-15: the five tori, reviewed: confirmed at 57 and 75 cells; a kink, not a fading correction; the 16-generation rule measured

`research/audit/REVIEW-gpu-local-tori.md` (code `research/audit/gpu_local_tori/`; a stepper built from
`docs/AUTOMATON.md` alone, equal to the oracle every generation on both tori, three negative controls). The branch
reviewed is `claude/gpu-local-1080` at b843883.

- **Second codes [measured; A].** 57 cells: 11.8744 ± 0.0015 on the CPU (445,165 deaths, 4 seeds) against the
  card's 11.8756 ± 0.0006; the card's two seeds, 2.6σ apart, look like a fluctuation in the higher one. 75 cells:
  15.667 ± 0.010 against 15.6630 ± 0.0023 (and 15.6614 ± 0.0026 on file). With 48 and 63 cells checked earlier,
  only the 93-cell value still rests on one code.
- **The line [measured].** Through 63, 75, 93: slope 0.20840 ± 0.00014, χ² 0.0002 on 1. Deficits below it: 0.111 at
  48 cells, 0.036 at 57.
- **The bend is a kink [measured, on one degree of freedom].** No smooth correction fits the five values: a term
  decaying in the shortest loop, in 1/A, in 1/A and 1/A², a massive-like sum, a stretched exponential all give χ²
  of 15 to 117 on 1 (59–70 with the 57-cell error inflated). The deficit goes 0.111, 0.036, then below 0.01 between
  shortest loops of 4.00, 4.36 and 4.58 cube steps: that takes an abrupt change near 61 cells, not a finite-size
  term fading. At 2σ the data still allow a residual of 0.01 at 63 cells or a slope change of 0.0009 above it.
  The 81-cell torus, running on the card, separates the line from every smooth form by 0.014 against a planned
  ± 0.003 (the reviewer's table of predictions by form is committed at 720ee7e, before any of those rows).
  [conjectured, the lead] The loop at which the bend ends is about the width of what is left of a dying face plus
  its reach (round 3: a remnant about 3.5 cube steps across): a wrapped face stops being short-lived once its last
  patch cannot feel itself round the loop.
- **The 16-generation rule of the census pipeline [measured on the same lives; B].** `rep.c` run at stamping
  intervals of 16 and of 1 on the same seeds (the 16-interval jobs are bit-identical to the files, 196 of 196):
  the census reads ln τ high by 0.00167 ± 0.00006 at 4 × 4 (as the card's session found), by 0.0008 and 0.0003 for
  two long-lived classes at A = 60, but by **0.0174 and 0.0184 ± 0.0011 for the classes whose shortest loop² is 4**
  (A = 48 and 60), where face deaths tie with firewalls inside one 16-generation window. So the card's "negligible
  from 60 cells up" is false for those rows; `REVIEW-shape2.md` claim 1 had estimated 0.018 at A = 48 from 2,048
  lives. Consequences: the 4 × 4 value on file was high by 0.0017 from the rule and 0.0058 (2.9σ) from the draw
  (the earlier review's "no systematic cause" is amended by this); differences between long-lived classes at
  A = 60 move by less than 0.001; a loop² 4 class against a long-lived one moves by 0.016–0.018; cost-per-cell
  figures (SH3) move by 0.0003 per cell at most.
- **Bookkeeping.** The card's forecast blocks were committed before their rows by its own clock (no server time to
  check against); settled lives are censored correctly; launch caps are 0.25–3.2% of a mean life; the rows'
  `code_commit` is the head at the end of a run without a dirty mark (harmless here: the stepping code did not
  change).
- Not checked: anything on the GPU; the per-run files that exist only on the card's machine (hazard by age); the
  63- and 93-cell values were not re-measured here; the bias at A = 72 and for the classes not run.
- Six items for the card before its pull request is merged (`research/GPU-QUEUE.md`, note of 08:15 UTC).

## 2026-11-15: gump carries signals: pulses on free-standing wires, a transmission, an interaction (sustained push on open problem 13; the lead's check from the oracle; adversarial review running)

Open problem 13 asked whether any oscillator can pass a signal to another. A finite pattern cannot move through
empty space (the hull theorem), so a signal needs a medium. The first push of a sustained search
(`research/signals/README.md`; objects in `research/signals/objects/`; commits ec389ef..bcd5844 and 896f44b) found
carriers by constraint search, in under a second, in the first tube it tried; none is among the objects that soup
had given us. The lead re-ran every verifier and wrote a separate check from `reference/oracle.py` alone
(`python3 research/audit/signals_lead_check.py research/signals/objects/pulse-B.json`, likewise pulse-A, pulse-S,
pulse-B-left: all pass for 60 periods on a ring of 40 cubes).

- **Travelling pulses [measured; B].** Wire B is a free-standing period-2 wire of 5 cells per cube along (1,0,−1).
  Flip two of its cells and the flip moves one cube every two generations, half the speed limit, for as long as it
  was followed; the wire behind is exactly as it was, and the state is the bare wire plus the two moved cells.
  The mirror pulse runs the other way. Pulse A is 5 cells on another period-2 wire (6 cells per cube); pulse S is
  32 cells on a still wire. Every pulse found has period 2 and shift 1.
  `python3 research/signals/verify_pulse.py research/signals/objects/pulse-B.json` (100 periods, ring of 40).
- **An emitter [measured by the producer; C].** Removing one never-changing cell of wire B at an even generation
  makes the wire heal and send one pulse. Of its 84 one-cell flips, 74 heal, 2 leave a standing defect, 2 emit a
  pulse (one each way), 6 start fronts.
- **A transmission, with a caveat [measured by the producer; the lead re-ran its verifier; C].** Flipping one cell
  at A sends a pulse along wire B; 36 cubes away a standing defect swallows it and is changed; six shots in a row,
  and a control run with A untouched never changes. The line between is left exactly as it was and reused, but the
  receiver moves one cube toward the sender per signal: it is a counter that uses up wire, not yet a memory cell.
  Of 1,000 standing defects tried as receivers, 636 catch fire, 109 swallow pulses unchanged, 255 are such
  creeping walls, none toggles. `python3 research/signals/verify_transmission.py research/signals/objects/transmission-B.json`.
- **An interaction [measured by the producer; the lead re-ran its verifier; C].** Two pulses of wire B meeting
  head-on pass through each other with no delay, or stop each other and leave a 3-cell standing mark, according
  to the parity of their separation. `python3 research/signals/verify_interaction.py research/signals/objects/interaction-B.json`.
- **Fronts on the wires we had [measured by the producer; C].** In 17 of the 21 wires on file a single flipped
  cell starts a front that runs the whole wire and converts it (the period-19 wire W00 into a still wire, one
  repeat every 19 generations; speeds 0.21–0.36 of the limit). No single flip of those wires makes a pulse.
- **Bounds [C; they rest on a SAT encoding and two solvers agreeing].** Closed tubes along (1,0,−1), background
  repeat of one cube: no pulse of any (period, shift) tried in the 2 × 2 tube; (2,1) pulses in the 2 × 3 and 3 × 3
  tubes and none at the other pairs decided; three or four pairs undecided (`research/signals/bounds_table.txt`).
  At least 30 backgrounds carry a (2,1) pulse in the 3 × 3 tube, all of period 2.
- **Forecasts.** The lead's S1 (the wires on file carry nothing; nothing moves more than six cells) failed: fronts
  run the whole wire. S2 (a travelling defect exists in some background; speed at most half) held. S3 (a
  transmission in this push, given one chance in five) held, with the caveat above. S4, S5 untested.
- Not checked: the "none" rows are not certified by a proof checker; only seven objects went to the oracle; whether
  wires A, B, S ever arise from soup; two-cell flips; sheets; other directions; tubes wider than 3 × 3.
- Running: an adversarial review with its own code (`research/audit/REVIEW-signals.md`), and a second push
  (bounded or closed tracks, a receiver that stays put, a gate with an output; the lead's forecasts S6–S10).

## 2026-11-15: a depleted face thins as one thing: the two-phase reading fails (round 4 of the dying-face study; scores recomputed by the lead; review started)

**Narrowed by the review the same morning (next entry): the numbers below stand, but "no remnant" does not
follow from them; on faces this small a remnant at fixed density would read the same way.**

The lead's reading before this round (`research/dying/PREDICTIONS.md`, "Round 4", F1–F6, committed before any
run): the rule is cooperative, so a deeply depleted face should be a void beside a remnant held at a fixed
density, the remnant shrinking as the population falls (a lever rule), and the dip curve a parabola joined to its
tangent. Round 4 (`research/dying/README.md`, "Round 4"; `data/r4_*.csv`; figure
`research/figures/dying_two_phase.png`; stepper `ex4.c`, equal to the oracle every generation and byte-identical in
output to the reviewer's `r3_ex.c`) caught free hull faces of 63, 84 and 108 cells at six depths, 0.9 to 0.15 of
their usual population, with a control of stationary faces thinned at random to the same count. The lead
recomputed every score from the table (`research/dying/data/r4_company.csv`) and looked at the figure.

- **No lever rule [measured; C until reviewed].** The company C (occupancy within two steps of a live cell, over
  its stationary value) falls steadily with depth: at 108 cells 0.833, 0.738, 0.646, 0.542, 0.439, 0.288 from
  p = 0.9 to 0.15. C(0.15)/C(0.45) is 0.38, 0.49, 0.53 at 63, 84, 108 cells, where a remnant at fixed density would
  give about 1. Even the nearest-neighbour company thins (0.71 → 0.43 from p = 0.6 to 0.15), and the distribution of
  local company over cells moves down as a whole rather than keeping its place and losing weight. F1, F2, F3, F5
  failed; F4 failed (the void grows faster than linearly: ratio 1.85, not 1); F6, the clause that would have
  ended the reading by itself, was not met only because the void is far larger than in the control.
- **But it is far from random thinning [measured; C].** Against the control at 108 cells a caught face has 1.15,
  1.35, 1.69, 2.43 times the company at p = 0.6, 0.45, 0.3, 0.15, three times the void at p = 0.3, fewer and larger
  groups (2.3 groups, the largest holding 77% of the live cells, against 3.3 and 66%), and a company that falls
  with distance from a live cell (0.56, 0.39, 0.27, 0.21 at graph distance 1, 2, 3, 4 and more at p = 0.3) where
  the control is flat. At p = 0.9 caught and control are the same; the clustering builds from about 0.75 down. So
  a depleted face is one loose cluster that keeps thinning, with a correlation of two or three cells, not two
  phases.
- **The tangent construction misses [measured; C].** From this round's own dips: g = 0.308, 0.304, 0.302 and tail
  slope 0.249, 0.261, 0.269 per site at 63, 84, 108 cells give a tangent point of 0.60, 0.57, 0.56 and an end point
  of 0.196, 0.202, 0.206, which overshoots the true end point (0.179, 0.188, 0.193) by 1.06, 1.20, 1.37 nats; and the
  remnant density it implies (0.55–0.60) is not there (mean C at p ≤ 0.3: 0.29, 0.34, 0.36). The agreement the
  lead saw before the round was a coincidence of curve shapes.
- **Two things round 3 and its review each had half of.** The far field depends on depth: at p = 0.3 cells four or
  more steps from any survivor hold 0.16–0.21 of stationary (the review's "not emptied"); at p = 0.15 they hold
  0.04–0.07 (round 3's "emptied"). And faces that go on to die are looser at the catch than faces that recover
  (C 0.152 against 0.204 at 63 cells, p = 0.15; counts not matched: 2.97 against 3.61 live cells).
- **Size.** At the same depth larger faces are denser round a survivor (C(0.3) = 0.387, 0.413, 0.439); at the same
  count they are looser. Whether C(0.15)/C(0.45) would reach the lever rule's value on much larger faces is not
  known; from 0.38 to 0.53 over these sizes there is no sign that it is close.
- **Forecasts.** F1–F5 failed. With rounds 1–3 the lead's tally on this study is three of twenty-three.
- **What follows.** There is no model for the shape of the dip curve below half the population, so the
  measurement of dips on faces too big to die (held in `research/GPU-QUEUE.md`) has nothing to extrapolate with
  and is dropped. The price per cell stays with the lifetimes, where the card's tori now give 0.2084 for wrapped
  faces.
- Not checked: one seed per size (two at 108 cells); the bootstrap treats caught faces as independent; counts are
  not matched in the dies-against-recovers split; only free hull faces; an adversarial review is running.

## 2026-11-15: round 4 reviewed: the numbers stand, "no remnant" does not follow; the lead's test could not have told the two apart

`research/audit/REVIEW-dying.md`, "Round 4" (own stepper `research/audit/dying4/st4.c` and geometry `geom.py`
written from `docs/AUTOMATON.md`, equal to the oracle every generation; seeds the study did not use;
`bash research/audit/dying4/run.sh` redoes it in about 20 minutes on one core).

- **The measurements reproduce [measured, two codes].** C(0.15)/C(0.45) = 0.383 and 0.481 at 63 and 84 cells (study
  0.384, 0.486); company against the random-thinning control at 108 cells 1.15, 1.35, 1.70 at p = 0.6, 0.45, 0.3;
  void at p = 0.3 against the control 2.3, 2.7, 3.2 times at 63, 84, 108 cells; far field 0.163, 0.181, 0.205 at
  p = 0.3 and 0.039, 0.060 at 0.15; ln τ_face = 13.626 ± 0.012 at 63 cells (study 13.633 ± 0.005). Not a rim
  effect: the 33 of 63 cells shared with a neighbouring face are the rim, survivors are slightly rarer there, and
  the company over unshared cells falls faster.
- **The inference from them was wrong [the reviewer's null; the lead checked it by hand].** The reviewer built the
  thing the lead's reading describes, a compact patch held at a fixed relative density p_t and filled from
  stationary faces, with nothing outside, and put it through the same code. It gives C(0.15)/C(0.45) = 0.45–0.48
  at 63 cells, 0.58–0.61 at 84 and 0.65–0.69 at 108, for any p_t from 0.45 to 0.8: at four to eight live cells
  the patch is about the size of the two-step neighbourhood the company is counted in, so its cells look out
  on the emptied face. The registered "against" clause of F1 (ratio below 0.6) is met by an exact lever rule at 63
  and 84 cells; "a lever rule needs the ratio near 1" holds only on faces far larger than any that can be caught
  this deep. (By hand at 63 cells, p_t = 0.55: four cells in a patch of stationary mass 7.3 leave the other three
  at 0.44 of stationary inside it, and about half of a two-step neighbourhood lies inside, so C ≈ 0.22; at fourteen
  cells the patch is four fifths of the face and C ≈ 0.46; ratio 0.48, the null's value.) So F1, F2 and F6 failing as
  registered is not evidence against the two-phase reading. They were the lead's tests and they could not test it.
- **What does separate a caught face from such a patch [measured, the reviewer].** The ratio at first passage sits
  0.07–0.14 below the null's. And the shape differs: at four live cells on the 63-cell face the null with
  p_t = 0.8 matches C and V (0.254 and 0.490 against 0.253 and 0.488), but its profile against distance is 0.33,
  0.22, 0.08, 0.005 where the caught face has 0.45, 0.16, 0.04, 0.03: a tighter knot and a thin scatter beyond it, not
  an even patch with an edge. Faces sampled at a random moment at a given population are tighter than faces at
  first passage with the same count (C 0.576, 0.457, 0.253 against 0.538, 0.413, 0.219 at 14, 9, 4 cells), and
  their C and V fit one effective p_t of 0.7–0.8 at every depth and both sizes, with the wrong profile for a
  plateau. No measure tried shows a core at fixed density that the random-thinning control does not also show.
- **What ends the two-phase reading is its number, not its picture [measured, two codes].** The
  parabola-plus-tangent construction overshoots the true end point by 1.07, 1.21, 1.34 nats (the reviewer's
  redoing from `data/r4_tangent.csv`; 1.37 at 108 cells with the card's lifetime; 1.07 from the reviewer's own run
  at 63 cells), and the straight tail alone already overshoots by 0.53, 0.51, 0.46 nats. The tangent point (0.56–0.60)
  is also not the effective density the structure fits (0.7–0.8).
- **Dying against recovering, with counts matched [measured, the reviewer, 63 cells].** Most of the gap was the live
  count. What is left: C = 0.145 against 0.166 at p = 0.15 (difference 0.021 ± 0.001) and 0.303 against 0.320 at
  p = 0.3 (0.017 ± 0.003); dying faces are looser at every single count.
- **Standing of the claim.** "A depleted face thins as one thing; there is no remnant" is withdrawn as stated. What
  stands: no plateau is seen; C cannot test a lever rule on faces of 108 cells or fewer; a caught face is neither a
  random thinning nor an even patch; the quantitative construction fails by more than a nat. Whether a remnant in
  some looser sense exists is open and is not reachable at sizes where faces can be caught this deep.
- Six corrections for the study's README are listed at the end of the review (the null's values beside the
  observed ratios; the figure's guides are infinite-face idealisations; the count-matched gap; first passage
  against random moment).
- Not checked by the reviewer: one seed per size; 108 cells ran 1.5 M generations (no catch at 0.15, no deaths);
  the null is one patch shape (a ball); 84 cells had 82 deaths, so the dying-against-recovering comparison is tested
  properly only at 63.

## 2026-11-15: how much of its state space a seed explores (the owner's question; exact for small vessels; review started)

The owner's journal (`docs/OWNER-JOURNAL.md`): within a hull there are finitely many states; for the longest-lived
seeds, how many are hit, and is there a pattern as size goes up? Study: `research/statespace/` (README is the
account; forecasts before any enumeration in `PREDICTIONS.md`; figure `research/figures/statespace.png`).

- **The states a seed visits are its settling time plus its final period [proved].** An orbit of a deterministic
  map cannot repeat a state before it reaches its cycle. So the question is the lifetime question in other units.
- **Every state listed, for 301 vessels of up to 30 cells [proved by enumeration; one row re-derived by the lead].**
  Diagonal hulls (every one of 2–29 cells at most 6 layers wide, 262 of them, and six of 30 cells), slab tori of 1,
  2 and 3 layers, 3D tori. `enum.c` builds the whole map on 2^N states; it is matched to the oracle on every vessel,
  and agrees with another agent's older enumerator (`research/theory/exhaust.c`) on eight tori. **The lead's own
  check:** all 65,536 states of the 16-cell hull `hull_-1_1_-5_-1_-5_3_-3_5`, each stepped once by
  `reference/oracle.py` in empty space, give the same eight statistics as the study's row (60,751 states with no
  predecessor, 39 cycles on 46 states, longest transient 9 from 8 seeds, mean transient 2.3142242431640625, 46,716
  seeds draining to the empty state): `python3 research/audit/statespace_lead_check.py hull_-1_1_-5_-1_-5_3_-3_5`
  (40 s).
- **What the small vessels say [proved within N ≤ 30].** A typical seed visits 8–14 states at 27–30 cells and the
  most patient seed of all 40–94 (a random map on 2^30 states would wander through about 41,000 before repeating).
  Between 57% and 98% of all states have no predecessor, and the states that have one number 2^(0.95–0.98·N): a
  constant fraction goes at the first step, not a rate per cell. The states on cycles number 2^(0.2–0.6·N), nine
  tenths of them still or of period 2 (there is one period-70 pair in a 30-cell 2-layer slab). The longest
  transient grows about linearly in N (61 in a 30-cell hull, 88 in the 2-layer slab). In no vessel of 19 or more
  cells is a champion fixed by a symmetry of the vessel (first 64 champions each, lattice symmetries only). **At
  these sizes nothing is chaotic yet:** the faces have 9–30 cells, under the 36 or so where lifetimes turn
  exponential.
- **The owner's cubes, counted [proved from the runs on file].** Side 16: 2,919,617,676 states (2^31.44) of the
  2^51,888 of its hull. Sides 8–16 all come to 0.0005–0.0008 bits per hull cell. Side 14 enters its period-2 cycle
  at generation 4,460,296 (the notebook's 4,460,298 was the generation of detection).
- **The pattern that extrapolates is the face law [measured; follows from the ledger's F4].** A seed lives as
  long as its faces, a face of A cells lives e^(0.209·A) generations, so an asymmetric seed visits about 2^(0.30·A)
  states: 0.30 bits per face cell. The symmetric cubes reach 0.15–0.29 bits per cell of their effective face
  (A/7.7), rising with size.
- **A share of what [measured; C until reviewed].** A living face is close to random: by a conditional-entropy
  estimate on an 8-layer face slab (16 × 16 torus, 256,000 snapshots; the estimator recovers two fields of known
  entropy to four figures) its top layer alone carries 0.986 bits per cell and the slab at most 0.958, still
  falling slowly with the size of the context. So a face could be in about 2^(0.95–0.99·A) states per layer and a
  seed sees 2^(0.30·A) of them before the face dies: the share falls as about 2^(−0.69·A), and it is also less than
  a random map's 2^(A/2). The states exist; what ends the exploration is the face going quiet.
- **The lead's forecasts E1–E7** (written 07:54 UTC, before any enumeration): E1 failed (57–98% without a
  predecessor is "most", but the exponent 0.95–0.98 is above the forecast band), E2 half held (the exponent is in
  band for three families of five; the periods are as said), E3 held in four families of five, E4 failed (no
  exponential rise yet at these sizes), E5 held, E6 failed as a general rule (true of hulls and kagome tori, not
  of slabs), E7 held with one exception at 27 cells. Three and a half of seven.
- Not checked: hulls wider than 6 layers; eight of the fourteen 30-cell hulls; anything above 30 cells exactly; the
  junction between the linear regime and the exponential one (conjectured near 30–40 face cells); the entropy has
  no lower bound, and the large slab stands in for small faces conditioned on survival; each cube is one run. An
  adversarial review with its own enumerator and a second entropy estimate is running
  (`research/audit/REVIEW-statespace.md`).

## 2026-11-15: a clock of every length, a gate, a register, a tape; and what chaos does to a wire (second signals push; the lead's own checks; review started)

`research/signals/README.md` sections 8–14 (the second investigator; forecasts J1–J10 and the lead's S6–S10 scored
at the end of `research/signals/PREDICTIONS.md`). The lead re-ran every oracle-judged verifier (all pass, 10:27
UTC) and checked four things from `reference/oracle.py` alone with separate code.

- **A clock whose period is set by its length [oracle-verified at ten lengths by two codes; claimed proved for
  every length, proof under review].** Wire C (five cells per unit along (1,0,−1)) between two caps is a
  free-standing still object of 32 + 5N cells with period 2. Add one cell and a "rake" (one extra live cell that
  moves a unit every 2 generations) shuttles between the caps for ever: period exactly 4N + 2. The lead:
  `python3 research/audit/signals_clock_lead_check.py 1 2 3 4 7 12` (cycle found by comparing whole states, not
  assumed: periods 6, 10, 14, 18, 30, 50; population 32 + 5N or one more; nothing within 13 units of the array
  edge). The study: `verify_clock.py` at N = 1, 5, 16, 17, 30 on the oracle, N = 1..200 with its own stepper, and
  `prove_clock.py 8 4`, a surgery on one oracle-computed cycle that is claimed to give every N ≥ 8. **This answers
  open problem 12:** gump has free-standing oscillators of every period 6, 10, 14, … (2 mod 4); no period 0 mod 4
  was found in the family and no reason is known.
- **A collision gate [oracle, two codes].** Two pulses of wire C meeting head-on: exactly one survives, undelayed
  and unchanged, and the wire is as it was; the survivor is the left-mover at even separation and the right-mover
  at odd. The lead: `python3 research/audit/signals_gate_lead_check.py 6 7 8 9 14 15 20 21` (twelve separations,
  whole-state equality with the single-pulse run after 40 generations). As logic: outputs (L, R and not L) or
  (L and not R, R), leaving along the two input lines; there is no third line and no crossing.
- **A rake [oracle, the study's verifier re-run].** One added cell on wire C moves one unit per 2 generations
  and emits a left-moving pulse every 2 generations; a head-on pulse is swallowed or stops it, by parity.
- **A register [oracle, the study's verifier re-run].** The wall between wire B and wire B′ moves one unit towards
  whichever side a pulse arrives from; ten operations in sequence leave it where the count says. No receiver that
  toggles on pulses from one side was found (complete census of caps of wire B inside small bounds: none
  reflects, none toggles).
- **A tape [oracle, two codes for one ring; "every word" by a light-cone argument, under review].** Any sequence
  of units of wire B and wire C moves rigidly towards −v at one unit per 2 generations. A 40-unit ring whose
  word contains all 32 runs of five passes the lead's `research/audit/signals_lead_check.py
  research/signals/objects/tape-BC.json 20`. Read this way a left-moving pulse of wire C is one unit of B in it,
  and a wall between B and C is a front. Of all 120 pairs of unit types only {B, C} moves.
- **Wires are born from soup [measured, the study's stepper].** Of 100,000 soups in the tube 12,780 settle into
  uniform wires of period ≤ 2 (366 distinct); ten of those carry a 2-cell pulse, born in 279 soups: wire B in
  106, wire C in 99, a third in 74.
- **Chaos destroys a wire it touches, and two empty layers isolate it for ever [measured, the study's stepper].**
  A wire run through a block of living soup: a front reached the far probe on 800 of 800 sides, at pulse speed
  (2 generations per unit) on 798. A capped end beside soup with 0 or 1 empty diagonal layers between: destroyed
  40 of 40; with 2 empty layers: untouched 40 of 40 for 3,000 generations, and the study says no cell can couple
  the two sides there (at 3 or more it is T3). On 33 of 400 sides of wire C (none of wire B) a clean pulse left
  the chaos ahead of the fire: the first pulses here to come out of anything random. Nothing could be sent into
  chaos and read on the far side, because nothing survives the contact.
- **Negatives inside stated bounds [SAT, one encoding, one solver].** No restoring reflector for a pulse of wire B
  or C at the sizes listed in the README; every cap of wire C that reflects a pulse is changed by it and burns at
  the next. Two more pulses of wire C reach outside the 3 × 3 tube and break the clock's caps (found leaving the
  chaos): the closed tube was too tight a search space.
- **The lead's forecasts.** S6 (45%) half held: the object whose period is set by its length exists, but what
  comes back is a rake, not a pulse, and there is no corner. S7 (25%) held to the letter (a collision gate; not a
  circuit element with its own output line). S8 (35%) failed. S9 (30%) held. S10 (60%) held.
- Not checked: the proofs (clock for every N, tape for every word) are the producer's; the soup and chaos counts
  rest on the study's stepper (checked against the oracle by `check_stepper.py`) with one block size and density;
  the SAT negatives rest on one encoding. A reviewer with its own code has these as its priorities
  (`research/audit/REVIEW-signals-2.md`).
