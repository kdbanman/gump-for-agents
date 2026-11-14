# Predictions of the repaired first clause for lattices class.md's table dismisses or mis-rows

*Auditor, 2026-11-14. Written after `seal.py` (exact, no dynamics) and after the face12e runs; before any dynamics
on kagome4 with b = 2 or on bond10 with b = 3 by me, and I have seen none by anyone (class.md's scans ran kagome4
at b = 3 and bond10 at b = 4 only; I have read those rows of `data/scan_table.md`).*

`seal.py` says that with sealing judged per half-space (direction and plane position), four table rows change:

| lattice | class.md | position-aware |
|---|---|---|
| kagome4 (plain kagome, 4 nearest) | b = 3, every direction sealed, "finite sealed sets" | **b = 2**, six directions, plane just outside a sparse row |
| kagome8 | b = 5, "finite sealed sets" | b = 4, twelve directions |
| hex9 | b = 5, "finite sealed sets" | b = 4, six directions |
| bond10 | b = 4, octahedron | **b = 3**, box with walls at odd coordinates; at b = 4 the hull is octahedron and box together |

and face8 (b = 3) gains the six box walls in addition to its octahedron.

## kagome4, b = 2 (K = 4): rules B2/S12 (c = 3) and B23/S123 (c = 4)

Exact (theorems, tested only as a sanity check):
- **K1.** A finite pattern never leaves the hexagon bounded by the six lines u.p = C, u in {+-(1,0), +-(0,1), +-(1,1)}
  (doubled triangular coordinates), each pushed out to the next sparse row. Generic directions leak.
- **K2.** No finite sealed set in the full lattice (generic forward count 2 = b for every type).
- **K3.** A permanent edge death is two rows at once (the sparse wall row, degree 2, and the dense row beneath).
  The wall row alone can come back.

Not predicted by the criterion (parts 4 and 5), my guesses:
- **K4.** B2/S12 is chaotic on the torus (as on the von Neumann lattice, the other K = 4, b = 2 lattice):
  60% confidence. The stage-5 rule of class.md (b/K = 0.5 > 3/8) says no.
- **K5.** If K4 holds: part 5 with K_f = 2 (the wall-row cell) gives sigma = rho, about 0.45, far below 0.85:
  "starved, no law". With K_f = 4 (dense row) sigma is about 0.9. I guess a law exists (the face12e outcome),
  50% confidence.

## bond10, b = 3 (K = 10): rules B3/S23 (c = 4), B34/S234 (5), B345/S2345 (6), ...

Exact:
- **B1.** Never leaves the box with odd walls; leaves the diagonal hull (c(u) = 3 on body diagonals, not sealed for b = 3).
- **B2.** No finite sealed set in the full lattice (3 <= 5).
- **B3.** Wall sheet cells have degree 5 and no in-sheet neighbours (a0 = 0); the layer beneath has degree 10 with
  6 in-layer neighbours.

Guesses:
- **B4.** Chaotic on the torus at some cap c <= 6 (class.md stage-5 rule: b/K = 0.3 <= 3/8): 65%.
- **B5.** If chaotic at a cap <= 6: boxes live longer the bigger they are, by more than e per cube of side: 50%.
