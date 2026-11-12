# Status (overwritten as things change; history is in git and NOTEBOOK.md)

_Last updated 2026-11-12 by the lead._

## Built and verified
- `reference/` oracle — matches the original's logs, sides 8–12 (13 via the engine on the legacy torus).
- `engine/` — Rust, bit-exact vs oracle and all legacy logs; ≈4×10¹⁰ cell-updates/s/core.
- `web/` v1 — WebGL2 bit-packed stepper + three.js views; 49/49 tests.
- `research/atlas/` — exhaustive still lifes ≤16 cells, oscillators, vertex star, legacy ash, critical thickness.

## In flight
- Engine round two: text/PNG renders and `describe`, faster ensembles, (stretch) mirror-symmetric stepping.
- Web round two: layer kymograph, `{111}` slicer, colour modes, seed constructor, render scaling.
- Peeling study (`research/peeling/`): statistics of face extinction and of transverse firewalls;
  the "cheapest `{111}` cut" hypothesis.
- Bulk-phase and rule-neighbourhood study (`research/phase/`).
- Closed cubes of side 15, 16 (`research/experiments/cubes.sh`).

## The storyline so far
1. Birth cannot cross a `{111}` plane (T2) ⇒ finite seeds are trapped in octahedral hulls; no spaceships.
2. The lattice is an ABC stack of kagome layers; ≥3 layers are needed to sustain chaos.
3. Chaos (density ≈0.39) is metastable. It dies by irreversible `{111}` events: a face layer
   going extinct (peeling — the staircase in the original's plots), or an interior 3-layer firewall.
   Which one happens is, conjecturally, whichever cut is cheapest.
4. Debris is built from a small fauna: cubes, kagome hexagons, vertex stars (a sealed
   12-cell universe), hinged period-2 flippers, and rare clockwork up to period 66.

## Ideas not yet started
- Web: a gallery of atlas objects; a guided tour of the storyline.
- A write-up for humans (and one for agents) once the peeling law is quantitative.
- Side 17+ closed cubes if symmetric stepping lands.
