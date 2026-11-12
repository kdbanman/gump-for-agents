# Atlas of small objects

Still lifes, oscillators, ash, and slab lifetimes for gump (B45/S345 on the faces of the cubic honeycomb).
Findings and their status live in `research/NOTEBOOK.md` (entry "atlas"); this file describes the
code, the search spaces, and the catalogue.

## Catalogue: `catalogue.jsonl`

One JSON object per line, for 1307 objects, each re-stepped with `reference/oracle.py` (`oracle_ok`,
all true). Fields:
- `id`: `S<n><letter>` still life, `P<p>.<minpop><letter>` oscillator; prefix `K` = confined to one `{111}` layer.
- `cells`: phase 0 in doubled coordinates, canonical orientation (later phases follow by stepping).
- `period`, `pops` (per phase), `union` (cells live in some phase), `sym` (stabiliser of phase 0 in
  translations × O_h), `spacetime_sym` (pairs (g, phase shift) mapping the orbit to itself; `= 2·sym` for a flip p2).
- `layers`: `{111}` layers spanned by the union along d = (1,1,1), (1,1,−1), (1,−1,1), (−1,1,1).
- `strict` (still lifes), `nbr_components`, and `sources`: exhaustive search tag(s), `soup_octa` / `soup_kagome` counts, legacy runs.

Contents: every strict still life with ≤ 12 cells, every one-layer strict still life with ≤ 16 cells,
every oscillator found by the exhaustive searches, and the soup ash (oscillators of period ≥ 3, p2 seen twice or
≤ 20 cells, still lifes ≤ 30 cells seen ≥ 3 times), plus the legacy ash pieces. Bulk lists (all 47,578
strict still lifes of 16 cells, and so on) are regenerated into `research/scratch/atlas/` by the commands below.

## Search spaces (what "exhaustive" means here)

| tool | space searched completely | notes |
|---|---|---|
| `slsearch.c N` | every still life with ≤ N cells whose cells are **R-connected** (R: graph distance ≤ 2) | every still life is a disjoint union of R-separated such pieces |
| `slsearch.c N -s` | every still life with ≤ N cells that is **strongly connected** (neighbours, or sharing a dead cell with ≥ 6 live neighbours) | contains every strict still life (proof in source header) |
| `oscsearch.c P N` | every orbit of exact period P whose **union of phases** has ≤ N cells and is R-connected | P=1 reproduces `slsearch` exactly (checked to N=11) |
| `oscsearch.c P N -k` | the same, inside one `{111}` layer (the kagome automaton), with symmetry group D6 (order 12) | matches the 3D one-layer still lifes to N=14 |
| `osc_sat.py` | all patterns inside an L1 ball (octahedral vessel) or a hexagonal kagome vessel; exact by T2 | "UNSAT" bounds hold only for that vessel |
| `vertex_star.py` | all 2^12 subsets of the 12 faces at a vertex | the star is a closed vessel (outside cells see ≤ 2 star cells) |

Canonical forms: minimum over the 48 elements of O_h (and, for orbits, the phases) of the sorted cell list
after an even translation that puts each coordinate's minimum in {0, 1}. Every search output is re-checked
by `lattice.step` (an independent sparse stepper) in `still_stats.py` / `build_catalogue.py`.

## Reproduce (from the repo root; binaries go to `research/scratch/atlas/`)

    S=research/scratch/atlas; mkdir -p $S
    gcc -O2 -o $S/sl research/atlas/slsearch.c; gcc -O2 -o $S/osc research/atlas/oscsearch.c
    $S/sl 14 > $S/sl_R_14.txt                       # R-connected still lifes <= 14 (2 min)
    $S/sl 16 -s > $S/sl_strong_16.txt               # strongly connected still lifes <= 16 (~30 CPU-min; split by axis: `sl 16 2 -s`)
    $S/osc 2 13 > $S/osc_P2_N13.txt                 # period-2 oscillators, union <= 13 (11 min); also: osc 3 12 (20 min), osc 4 10
    $S/osc 1 24 -k > $S/kag_still_24.txt            # kagome still lifes <= 24 (1 min)
    $S/osc 2 18 -k > $S/kag_osc_P2_N18.txt          # kagome p2, union <= 18
    python3 research/atlas/still_stats.py $S/sl_strong_16.txt
    python3 research/atlas/harvest.py cube 5 3000 0.4 11          # octahedral soups + ash census (also face 6, vertex 6/8, edge 7, cube 7/9)
    python3 research/atlas/kagome_soup.py 24 300 3 --census       # kagome density sweep
    python3 research/atlas/legacy_ash.py                          # legacy sides 8-11
    python3 research/atlas/thickness.py N m NSOUPS 0.4 SEED --maxgen 1000000
    python3 research/atlas/slab_firewall.py 5 3 30 0.4 31
    python3 research/atlas/vertex_star.py
    python3 research/atlas/build_catalogue.py

`vessel.c` steps soups on any finite cell graph (octahedra, m-layer slabs on an N × N in-plane torus) and finds
the exact transient and period with Brent's algorithm. `vessel.py` builds the graphs; `lattice.py` holds the
shared geometry.
