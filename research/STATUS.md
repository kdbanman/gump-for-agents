# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-13 by the lead._

## Built and verified
- `reference/` oracle — matches the original's logs, sides 8–12 (13 via the engine on the legacy torus).
- `engine/` — Rust, bit-exact vs oracle and all legacy logs; ≈4×10¹⁰ cell-updates/s/core.
  Round two: `gump show` (text renderings, kagome layers), `png`, `describe` (re-derives all 1,307
  atlas objects), packed ensembles (≈4× for small boxes), `--sym` symmetric soups. Not built: a
  symmetry-reduced stepper (would buy closed cubes beyond side 16).
  Round three: `--sym` torus soups fixed, `ensemble --layer-deaths` (exact peel times),
  `gump occupancy` (time-averaged maps), `--checkpoint` for restartable runs.
- `web/` v1 — WebGL2 bit-packed stepper + three.js views; 49/49 tests.
- `research/atlas/` — exhaustive still lifes ≤16 cells, oscillators, vertex star, legacy ash, critical thickness.
- `research/peeling/` — the face law, cuts, symmetric effective area, account of the cube series.
- `web/` rounds two and three — kymograph, `{111}` slicer, editor, atlas gallery, guided tour, static build.
- `research/phase/` — the chaotic state as a phase; 960-rule survey (`research/figures/phase_rulemap.png`).

## In flight
- `research/lineage/` (agent): are plateau lengths of structured symmetric seeds memoryless, or over-dispersed
  like the cubes'? (OPEN-PROBLEMS 6.)
- `research/theory/` (agent): audit of the threshold lemma (PROGRAM S5) and a proof attempt for critical
  thickness (S6). Not yet checked by the lead.
- Next when a core frees: the 2D toy search (PROGRAM G1).

## The storyline so far
1. Birth cannot cross a `{111}` plane (T2) ⇒ finite seeds are trapped in octahedral hulls; no
   spaceships. Measured front speeds into vacuum: 0.177 cube/gen on {100}, 0.165 on {110},
   exactly 0 on {111} — the octahedron is the growth shape.
2. The lattice is an ABC stack of kagome layers; ≥3 layers are needed to sustain chaos.
3. The chaotic state is a genuine phase: bulk density **0.4155** (tori of any size), isotropic,
   correlation length ≈0.7 cube, damage spreads as a sphere at ≈0.85 cube/gen. Mean field
   alone gives a 4-cycle; a small neighbour–neighbour correlation stabilises it.
   **O_h-symmetric seeds are different**: cells on mirror planes are depleted (≈0.31), so
   symmetric octahedra run at ≈0.39. Every legacy cube run is of this kind.
4. Chaos is metastable and dies only by irreversible `{111}` events, each a rare, sudden,
   memoryless collapse whose cost is exponential in the number of cells that must die:
   - **a face layer goes extinct (peeling)** — mean wait τ_face ≈ exp(−0.09 + 0.209·A)
     generations, A = sites in the outer layer; one line over six decades for flat slab
     faces, octahedral faces (≈1.5× tougher), symmetric soups and the closed cubes
     (`research/figures/peel_face_law.png`; independently re-checked by the lead,
     `research/experiments/verify_face_law.py`: CV of waits 1.0, slope 0.199 ± 0.006);
   - **an interior 3-layer firewall** — ≈0.12 per cell of the band (≈0.36 per unit of
     cross-section), so it wins only where a cross-section is much smaller than a face:
     thin slabs (crossover at thickness ≈ width), never octahedra;
   - the bulk without faces (whole torus) is effectively immortal above ≈600 cells.
   **Symmetry is fatal**: an O_h-symmetric state has one fundamental domain of independent
   chaos (regions die in lockstep), effective face area A/7.7. The side-13 cube lasts ~10⁵
   generations because it is symmetric; the same hull filled asymmetrically would hold each
   face ~10⁴¹. The legacy cube lifetimes n = 11–15 fall at unremarkable quantiles of the law's
   prediction. **n = 16 was predicted at 2.4×10⁸ (90%: 3.9×10⁷–6.3×10⁸) and lived
   2,919,617,676** (first face 2.36×10⁹, second 5.2×10⁸; ends as 12 × S8b on the axes;
   `research/data/cube16_*`). What was wrong: the cost per site in a symmetric face rises with
   face size, so "A/7.7" under-predicts beyond its fitted range; cube-centred O_h faces follow
   ln τ ≈ 0.69 + (0.209/6)·A − 0.195·√A to A = 693 (`research/fluct/sym_fit.py`), and
   vertex-centred ones (even cubes) are ≈1.5× tougher (A = 360–630; 2.0 ± 0.4 at A = 693).
   **Face death is the stationary tail, measured to one cell** (`research/fluct/README.md`):
   ln P(n = k) is straight down to k = 1, the death rate is its next point (h ≈ 0.6·P(n = 1)),
   62% of deaths are from a single cell, the usual 3-cell ember is one kagome triangle;
   −ln h/A → 0.2077 ± 0.0014 + 0.55/A. Path-splitting (FFS) does not help: the plunge takes
   ~10 generations. Brute force on an O_h orbit-reduced stepper (`research/fluct/fl.c`) does.
5. Debris is built from a small fauna: cubes, kagome hexagons, vertex stars (a sealed
   12-cell universe), hinged period-2 flippers, and rare clockwork up to period 66.
   **Long periods are short loops closed by a symmetry of their own box** (period = twist ×
   loop, twist ∈ {2, 3, 4, 6}): P66.27a = 2 × 33 (mirror), C48.24a = 6 × 8 (a screw),
   C36.33a = 4 × 9. Twisted loops are a steady 3–8% at every loop length, so the twist
   multiplies rather than selects; the longest plain loop is 35. Compound objects (249 of
   9,700 in the box census) are non-communicating sub-clocks on one frame
   (`research/clockwork/README.md`; notebook 2026-11-13).
6. In rule space (960 rules, B ⊆ {4..7}, S ⊆ {2..7}) torus chaos is common, but long-lived
   *confined* chaos is not, and gump is a **minimal** member of that region: remove any one
   count from B45/S345 and lifetimes collapse; add S2 or S7 and they grow ≥30×.

## Most recent
- PR #1 merged to main (everything above). The lead measured the fluctuations of living faces
  (`research/experiments/face_fluct.py`): the face law's 0.209 looks like the value at zero of
  a size-independent large-deviation curve (≈0.20 by extrapolation) — notebook, last entry.

- Side 16 is finished (2026-11-13). Forecasts from perturbed copies of the running cube
  (`research/fluct/PREDICTIONS.md`): first peel hit (median 2.2×10⁹, actual 2.362×10⁹);
  second peel missed by the clone run (mean 7×10⁷ confirmed three ways, actual stay 5.2×10⁸)
  and caught at the 95th percentile by the fit-only forecast. Side 17 is forecast at a
  first-plateau mean of 2.6×10¹⁰ (not run).
- **Open puzzle:** whole cubes are over-dispersed against the memoryless ensembles — 3 of 16
  large plateaus beyond 4 means, 3 under 0.05 (`research/experiments/cube_vs_ensemble.py`;
  P ≈ 0.01); side 16's four largest plateaus ran 2.8, 7.4, 2.6 and 1.2 means. Hull radius 42
  itself is an ordinary size (fresh soups: τ = 7.1×10⁸, 45 deaths). No mechanism known.
- `research/fluct/qsd.py` is unreliable for symmetric soups below R = 30 (settled debris
  counted as a living face); use the engine there.
- Clockwork study done (2026-11-13): 94 new oscillators in `research/clockwork/objects/`
  (ids `C<period>.<minpop><letter>`, not merged into the atlas catalogue); 22 of them are
  compound. Open: periods beyond 66 via 4- or 6-fold boxes; anything that carries a signal.
- Open: the asymptotic symmetric slope (is it exactly 0.209/6?); whether 0.208 per site
  holds for asymmetric faces beyond A = 84.

- 2026-11-13: prior-art survey and adversarial second pass (`research/PRIOR-ART.md`): no automaton on this
  lattice found, no lifetime-versus-symmetry result found; cite Eppstein (arXiv 0911.2890) for confinement.
  Open problems consolidated in `research/OPEN-PROBLEMS.md`. Theory programme started
  (`research/theory/PROGRAM.md`); first result, the threshold lemma: gump is a symmetric threshold automaton
  except at overcrowded cells (n ≥ 6), so all non-period-2 behaviour needs overcrowding.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17 closed cube (forecast written down; days on the engine, or a single-state
  symmetry-reduced stepper — `fl.c` is fast only for 64 states at once).
- B45/S3457 ("super-gump": ~100× lifetime per radius step) and glassy B45/S3456 as rules worth their own look.
