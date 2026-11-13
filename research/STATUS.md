# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-12 by the lead._

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
- Web: folding the peeling law and density corrections into the tour; face-lifetime readout.
- Closed cube of side 16, checkpointed (`research/experiments/cube_ckpt.sh 16`; re-run to resume).

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
   prediction. **n = 16 was predicted at 2.4×10⁸ (90%: 3.9×10⁷–6.3×10⁸) and missed**: it is
   alive at 1.025×10⁹ with no face lost (checkpoint in `research/data/`). Cause, measured two
   ways (face fluctuations of the cubes; residence times of symmetric soups at R = 37, 39):
   the cost per site in a symmetric face rises with face size, so "A/7.7" under-predicts
   beyond the sizes it was fitted on — by 1.9× at A = 570, 2.3× at A = 630. The data fit
   ln τ ≈ 1.57 + (0.209/6)·A − 0.236·√A: six lockstep domains minus a mirror-line boundary
   term. Revised side-16 first plateau: 4–7×10⁸ (notebook, last entry).
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

- Side 16: alive at generation 1,750,000,000, no face lost; latest checkpoint
  `research/data/cube16_gen1750000000.gump` (resume: `research/experiments/cube_ckpt.sh 16`
  after copying it to `research/scratch/cubes/cube16.ckpt.gump`; ≈7×10⁸ generations per
  2-hour job). A rare-event estimate of its expected stay is in progress (`research/fluct/`).
- Clockwork study done (2026-11-13): 94 new oscillators in `research/clockwork/objects/`
  (ids `C<period>.<minpop><letter>`, not merged into the atlas catalogue); 22 of them are
  compound. Open: periods beyond 66 via 4- or 6-fold boxes; anything that carries a signal.
- Open: the vertex-centred factor at large faces; the asymptotic slope (is it exactly
  0.209/6?); side 15's 33M-generation stay at R = 37, 3.7× even the corrected mean.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17+ closed cubes if symmetric stepping lands.
- B45/S3457 ("super-gump": ~100× lifetime per radius step) and glassy B45/S3456 as rules worth their own look.
