# How chaos dies: peeling, cuts, and the face law

Findings are in `research/NOTEBOOK.md` (entry "peeling"). This directory holds the code and the curated tables.

## Engine: `rep.c` (bit-sliced replicas on an arbitrary finite cell graph)

gump's cubic torus ties a slab's face area to its ring length (area ≥ 3(m+3)²), and faces of area ≥ 147 never peel
in 10⁶ generations, so the face law needs smaller, edge-free faces. `rep.c` runs 64·W independent replicas of
B45/S345 on any finite cell graph (one replica per bit; ≈1×10¹⁰ cell-updates/s per core on 100–3000-cell
vessels) and records, per replica, the last generation each `{111}` layer was alive (resolution K) and the
generation the replica became periodic. Layer deaths of outer layers are final by T2; three consecutive dead
layers are final by T3, so whole peel/firewall histories are reconstructed from these last-alive times.
`geom.py` builds the vessels:

- `slab(N1, m, N2)`: m layers normal to (1,1,1) on a **skewed in-plane torus** (periods (N1,0,−N1), (0,N2,−N2) in
  cubes): two flat faces of A = 3·N1·N2 cells, no edges, any thickness.
- `torus(N[, m])`: gump's cubic torus (whole-torus soup, or a slab soup in it).
- `octa(R, sym, vertex)`: the octahedron |p − c|₁ ≤ R in open space (its own hull, exact by T2); `sym`: O_h-symmetric
  soup about c (a cube centre, or the vertex (1,1,1) like even closed cubes).

Validation: `rep` reproduces gump's population exactly for 3000 generations on a 6³ torus soup, a 5-layer slab
in a 9³ torus and an R = 15 octahedral soup (`python3 research/peeling/validate.py`). Slab neighbour
counts are 9 / 11 / 12 for face / sub-face / interior cells as they must be.

## Experiments (all append to `research/scratch/peeling/*.jsonl`; seeds are fixed by the arguments)

| script | what |
|---|---|
| `slabs.py N1 N2 m cap` | 512 slab soups (p = 0.4): peel history, first transverse T3 firewall, settle time |
| `octa.py R p cap [--sym] [--vertex]` | octahedral soups: full hull history (8 face offsets over time) |
| `torus.py N p cap` | whole-torus soups: first firewall per diagonal, settle, extinction |
| `faceocc.py`, `lastcells.py` | time-averaged occupancy of a cube's outer face; where its last cells sit (via gump) |
| `slab_report.py`, `octa_hazard.py` + `octa_report.py`, `cubes_report.py` | curated tables below |
| `figures.py` | `research/figures/peel_face_law.png`, `research/figures/peel_cuts.png` |

Job lists used: `research/scratch/peeling/jobs_*.txt`, `thin*.txt`, `vtx.txt` (one script call per line).

## Tables

- `slab_area.csv` — first peel per slab batch: events, frozen/censored, MLE mean with 95% CI, CV, KS p.
- `slab_thickness.csv` — wait for the next peel at each current thickness m′, pooled over histories.
- `slab_fw.csv` — competing first events (transverse firewall / peel / freeze), cut size, lifetime.
- `slab_end.csv` — thickness at which slab histories stop.
- `octa_first.csv`, `octa_hazard.csv` — first peel after t0 = 200 per batch; per-face hazard by current face area
  (sym: 1 = O_h about a cube centre, 2 = about a vertex; symmetric hazards are per 8-face family).
- `cube_residence.csv`, `cube_lifetime.csv` — closed cubes: residence per radius vs the symmetric face law.
- `torus.csv` — whole-torus soups.
