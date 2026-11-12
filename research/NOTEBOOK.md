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
  filled the whole torus: ≈0.30 live fraction of 500k cells. So the chaotic phase has a
  density near 0.30 and, unconfined on a torus that size, outlives 3×10⁵ generations.
- **[measured]** Side-13's plateau (≈8000) is the same density: its hull holds ≈ R³/2 ≈ 25k cells.
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
  ≈123 live cells — density ≈0.39, *higher* than the bulk's ≈0.30. The surface is hot, not cold.
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
