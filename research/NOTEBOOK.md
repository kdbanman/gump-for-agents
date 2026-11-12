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

Code, catalogue (1146 objects, every one re-stepped by the oracle) and exact search spaces:
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
- **[proved, exhaustive]** Period 2: the smallest union is 9 cells; classes by union size 9, 10, 11, 12: **3, 6, 4, 11**
  (`$S/osc 2 12`). The smallest phase is 6 cells (`P2.6a`: 3 stator cells plus a 3-fold "propeller" rotor of 6).
  All 13 with union ≤ 11 are *flips* (phase 1 is congruent to phase 0), and their rotors are perfect matchings of **hinges**:
  a live face swings 90° onto a face sharing an edge. For larger p2 from soups this holds for about half (88/170).
- **[proved, exhaustive]** No period-3 oscillator has union ≤ 11 (`$S/osc 3 11`), and none of period 4 has union ≤ 10. The smallest from soups:
  p3 union 13, p4 union 14.
- **[measured]** Soups in octahedral vessels (18,900 soups, L1 radius 5–9, ρ = 0.25–0.6, `harvest.py`) leave oscillators in 11%
  of runs. Object periods seen: **1–16, 20, 22, 48, 66**. Recurrent high-period objects: `P14.17a` (union 24, 64 times),
  `P16.15a` (30 cells, 28 times), `P10.15a` (11 times), `P5.17a` (99 times). `P11.23a` and `P13.22a` have prime periods.
  `P48.34a` (56 cells) and `P66.27a` (45 cells) are single neighbour-connected objects whose rotors are not composites:
  50 of 56 and 40 of 45 cells carry the full period. `P10.17a` and `P14.20a` have no stator at all (36 cells, all moving).
- **[measured]** The most common ash (3D soups): cube `S6a` (2825), vertex star `S12a` (1923), `S12i` (654), `S9a` (296), the hexagon.

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
