# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-12 by the lead._

## Built and verified
- `reference/` oracle — matches the original's logs, sides 8–12 (13 via the engine on the legacy torus).
- `engine/` — Rust, bit-exact vs oracle and all legacy logs; ≈4×10¹⁰ cell-updates/s/core.
- `web/` v1 — WebGL2 bit-packed stepper + three.js views; 49/49 tests.
- `research/atlas/` — exhaustive still lifes ≤16 cells, oscillators, vertex star, legacy ash, critical thickness.
- `research/phase/` — the chaotic state as a phase; 960-rule survey (`research/figures/phase_rulemap.png`).

## In flight
- Engine round two: text/PNG renders and `describe`, faster ensembles, (stretch) mirror-symmetric stepping.
- Web round two: layer kymograph, `{111}` slicer, colour modes, seed constructor, render scaling.
- Peeling study (`research/peeling/`): statistics of face extinction and of transverse firewalls;
  the "cheapest `{111}` cut" hypothesis.
- Phase study follow-up: why mirror planes deplete density, and what that does to symmetric seeds.
- Closed cubes of side 15, 16 (`research/experiments/cubes.sh`).

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
4. Chaos is metastable. It dies by irreversible `{111}` events: a face layer going extinct
   (peeling — the staircase in the original's plots) or an interior 3-layer firewall;
   conjecturally whichever cut is cheapest. Being quantified in `research/peeling/`.
5. Debris is built from a small fauna: cubes, kagome hexagons, vertex stars (a sealed
   12-cell universe), hinged period-2 flippers, and rare clockwork up to period 66.
6. In rule space (960 rules, B ⊆ {4..7}, S ⊆ {2..7}) torus chaos is common, but long-lived
   *confined* chaos is not, and gump is a **minimal** member of that region: remove any one
   count from B45/S345 and lifetimes collapse; add S2 or S7 and they grow ≥30×.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17+ closed cubes if symmetric stepping lands.
- B45/S3457 ("super-gump": ~100× lifetime per radius step) and glassy B45/S3456 as rules worth their own look.
