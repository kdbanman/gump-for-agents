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
  (0.78 expected); the sum of T/τ is 26.5 against 16 (P = 0.011). **[conjecture]** Residences of whole cubes are
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
