# Forecasts for the twisted-slab test (written and committed before any production run)

2026-11-14. Object: gump slabs of m = 8 {111} layers whose in-plane period lattice is a general index-24 sublattice
(face area A = 72), HNF generators (a, k), (0, b) in cube coordinates (i, j). Soup p = 0.4, no burn-in, one life per
replica ending at its first event (face death, or a T3 firewall across one of the three transverse diagonals;
settling and the cap censor). ln τ_face = ln(2E/F) ± 1/√F. Invariants from `python3 research/shape/models.py`.

## Geometry, verified before forecasting (not taken from the brief)

`python3 research/shape/lattice.py 24` enumerates all 60 index-24 lattices and sorts them into 15 shapes (isometry
classes of the reduced Gram matrix; the in-plane point group of the slab, with the flip, is the full hexagonal group
of order 12, so isometric lattices give equivalent slabs). Corrections to the brief's arithmetic:

- systole² of (4,k),(0,6): 16, 21, 16, 13, 12, 13 for k = 0…5: as stated.
- **(3,1),(0,8) is not a second shape with systole² 13.** It is the same torus as (4,3),(0,6) and (4,5),(0,6)
  (reduced Gram (13, 12, 36) for all three). It becomes a presentation control, like (4,2),(0,6) for 4×6.
- (4,3) and (4,5) are mirror images of each other (a control too).
- There *are* other shapes at equal systole, which test "systole alone" directly:
  systole² 16: three shapes, (16,8,28) = 4×6, (16,0,27) = (6,1),(0,4), (16,16,31) = (6,3),(0,4);
  systole² 12: two shapes, (12,0,36) = (4,4),(0,6) and (12,12,39) = (2,5),(0,12);
  systole² 9: two shapes, (9,6,49) = 3×8 and (9,0,48) = (8,2),(0,3). Also systole² 19: (2,3),(0,12).

| torus (HNF) | shape (Gram) | systole² | hex systole | row closures (u1, u2, u1−u2) | cheapest firewall cut |
|---|---|---:|---:|---|---:|
| (3,0),(0,8) = 3×8 | (9,6,49) | 9 | 3 | 3, 8, 24 | 108 |
| (8,2),(0,3) | (9,0,48) | 9 | 3 | 24, 3, 24 | 108 |
| (4,4),(0,6) | (12,0,36) | 12 | 4 | 12, 6, 12 | 216 |
| (2,5),(0,12) | (12,12,39) | 12 | 4 | 24, 12, 24 | 432 |
| (4,3),(0,6); (4,5),(0,6); (3,1),(0,8) | (13,12,36) | 13 | 4 | 8, 6, 24 (permuted) | 216 |
| (4,0),(0,6) = 4×6; (4,2),(0,6) | (16,8,28) | 16 | 4 | 4, 6, 12 | 144 |
| (6,1),(0,4) | (16,0,27) | 16 | 4 | 24, 4, 24 | 144 |
| (6,3),(0,4) | (16,16,31) | 16 | 4 | 24, 4, 24 | 144 |
| (2,3),(0,12) | (19,18,27) | 19 | 5 | 8, 12, 24 | 288 |
| (4,1),(0,6) | (21,6,21) | 21 | 5 | 24, 6, 24 | 216 |

"Hex systole": the shortest non-contractible loop counted in in-plane cube steps (±u1, ±u2, ±(u1−u2)), i.e. in
the graph metric in which information spreads (the speed limit's hexagon). "Row closure": the length after which a
kagome row closes on itself; a transverse layer is a set of such rows, so the cheapest firewall cut is 36 × the
shortest row closure. On the twisted tori the firewall channel is mostly closed (cut ≥ 216), which removes the
confound of the rectangular series (width and firewall-proneness were one variable there).

## Controls (any failure means a bug, not physics)

- C1: (4,2),(0,6) agrees with (4,0),(0,6) within 3σ.
- C2: (4,3),(0,6), (4,5),(0,6) and (3,1),(0,8) agree with each other within 3σ.
- C3: my untwisted runs reproduce the known values within 3σ: 4×6×8 14.970 ± 0.002 (GPU; CPU review 14.955 ± 0.009),
  3×8×8 14.621 ± 0.003 (GPU; CPU 14.611 ± 0.017).

## H1 (the lead's conjecture): ln τ_face is an increasing function of the Euclidean systole alone

Numbers (interpolation through 3 → 14.621, 4 → 14.970, then +0.07 per unit of systole):
systole² 9: 14.621 (both shapes); 12: 14.78 (both shapes); 13: 14.83; 16: 14.970 (all three shapes);
19: 15.00; 21: 15.01 (the brief: about +0.04 over 4×6).
Refuted if any of: (a) two different shapes of equal systole (the three at 16, the two at 12, the two at 9) differ
by more than 3σ; (b) the systole² 12 or 13 tori are not below 14.970 by more than 3σ; (c) the ordering in systole is
violated by more than 3σ (e.g. 12 above 13 or 13 above 16).

## H0 (what I think more likely): the lifetime follows the graph (hex) systole, not the Euclidean one

A line-like object on a lattice costs per cell, and a closed line that runs off the row directions is a staircase
whose cell count is its hex length, not its Euclidean length. In the hex metric the systole² 12 and 13 tori have
systole 4, the same as 4×6. Numbers: hex systole 3 → 14.62; **4 → 14.97 (this includes systole² 12, 13 and all
three 16 shapes)**; 5 → about 15.04 (systole² 19 and 21).
Refuted if the systole² 12 or 13 tori lie more than 3σ below 14.970, or the shapes of equal hex systole differ by
more than 3σ.

A second alternative, H0′ (rows / firewall-proneness): the lifetime follows the shortest row closure r, i.e. what
makes a face cheap is a short straight kagome row (the same thing that makes a firewall cheap). Numbers: r = 3 →
14.62, 4 → 14.97, 6 → about 15.11, 12 → well above 15.1. It predicts the systole² 12 and 13 tori (r = 6, 12) *above*
4×6, opposite to H1. Refuted if they are not above 14.970 by more than 3σ.

Common to all three: the three systole-16 shapes are equal. If they differ, the lifetime depends on the shape in a
way none of these invariants captures (the second reduced vector, the number of short directions, …).

My credences before the runs: H1 0.35, H0 0.35, H0′ 0.15, something else 0.15.

## Run plan

All 13 HNFs above at A = 72, rep.c stepper validated against the engine for each (`research/shape/tslab.py validate
a k b 4000 24`: MATCH for all 13; a deliberately wrong tiling gives MISMATCH), target ≈ 5,000 face deaths each
(± 0.014), caps of 5 × 10⁵ generations, 1,024 lives per run. Then, time permitting, A = 60 (index 20).

## Addendum, A = 60 (index 20), written while the A = 72 runs were in progress and before looking at any of their output

Shapes at index 20 (`python3 research/shape/lattice.py 20`): there is no systole² 21 and no width 3. Tori to run,
with invariants from `models.invariants`:

| torus (HNF) | Gram | systole² | hex systole | row closures | cheapest cut |
|---|---|---:|---:|---|---:|
| (4,0),(0,5) = 4×5 | (16,12,21) | 16 | 4 | 4, 5, 20 | 144 |
| (5,1),(0,4) | (16,4,19) | 16 | 4 | 20, 4, 10 | 144 |
| (4,2),(0,5) | (13,10,25) | 13 | 4 | 20, 5, 20 | 180 |
| (4,3),(0,5) | (12,0,25) | 12 | 4 | 20, 5, 20 | 180 |
| (2,2),(0,10) | (12,12,28) | 12 | 4 | 10, 10, 10 | 360 |

Known: 4×5×8 = 12.486 (GPU; 12.487 ± 0.001 in the review's age bins). Forecasts, as differences from 4×5:
- H1: (5,1) 0 (equal systole); (4,2) −0.14; (4,3) and (2,2) −0.19, and equal to each other.
- H0 (hex systole): all four 0.
- H0′ (rows): (5,1) 0; (4,2) and (4,3) about +0.07; (2,2) well above (+0.3 or more).
Refutation criteria as at A = 72.
