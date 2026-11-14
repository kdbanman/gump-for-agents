# Prediction for `face12e`, written before anything was run on it

*Auditor of `research/theory/class.md`, 2026-11-14. Committed before any code (the author's or mine) was run on
this lattice and before reading anyone's results for it. Everything below was derived by hand from the offsets,
using the definitions in class.md section 1 and the functions of `research/theory/class/theory.py` as written.*

**What I had seen.** `docs/AUTOMATON.md` section 2 carries one sentence about this rule ("With the edge-sharing
four the theorems below change: the hull is a box, not an octahedron"). I read it because the brief told me to read
that file first; it is a leak of the hull shape, disclosed here. I have not read the notebook entry it cites, the
branch `origin/claude/edge-neighbour-tangent`, or any number for this rule.

## The lattice

Cells: faces of the cubic honeycomb, doubled coordinates, exactly one odd coordinate (three types, by normal axis).
A face with normal a and in-plane axes b, c has the 12 offsets

    +-e_a +- e_b, +-e_a +- e_c     (8 perpendicular, sharing an edge: as in gump)
    +-2e_b, +-2e_c                 (4 coplanar, sharing an edge: gump has +-2e_b +-2e_c instead)

Rule B45/S345 = capped threshold (b, c) = (4, 6), K = 12. Each type's offset set is centrally symmetric.

## A. What class.md and theory.py say (the criterion as written)

`theory.rays` gives 26 rays: 6 axes, 12 face diagonals, 8 body diagonals. Counts (a-, a0, a+) per type:

| ray | type with normal along x | normal y | normal z | c(u) = max a- |
|---|---|---|---|---|
| (1,0,0) | (4, 4, 4) | (3, 6, 3) | (3, 6, 3) | **4** |
| (1,1,1) | (4, 4, 4) | (4, 4, 4) | (4, 4, 4) | **4** |
| (1,1,0) | (4, 4, 4) | (4, 4, 4) | (6, 0, 6) | **6** |

Generic direction: 6 for every type.

1. **Part 1 (outside sealed) fails for b = 4.** No ray has c(u) <= 3, so by Theorem A(iii) no direction at all is
   sealed. `theory.sealed_rays(L, 4)` is empty; `theory.py table` would print tight b = 5 (the 14 axis and
   body-diagonal rays, hull = cube cut by an octahedron) and, asked about b = 4, has no confining set.
   Theorem A(v) gives hull_4(X) = the whole space. Section 5 calls N1 "proved necessary ... (Thm A, an iff)" and the
   summary says "proved iff; the hull is the polytope of those rays".
   **So the criterion as written says: face12e B45/S345 is not confined to any polytope, and is not a gump.**
2. Part 2 holds (4 <= 6; generic forward count 6 for every type, so no finite sealed set in the full lattice).
3. Part 3 cannot be evaluated: with no sealed ray there is no face, no K_f, no reach, no c_arm.
   `theory.firewall_width(L, (1,0,0), 4)` would run to its limit (200): started on a layer of x-faces it never
   finds a sealed band.
4. Part 4: "not predicted". The stage-5 regularity (chaos at a low cap iff b/K <= 3/8) says chaotic: b/K = 1/3.
5. Part 5: undefined (no K_f).

For the tight b = 5 on this lattice the table numbers would be K = 12, a0 = 4, a- = 4, K_f = 8, reach 6..8,
b/K = 0.417: the same row as star2 and tristar2, for which class.md found no chaotic cap within reach.

## B. What I expect to be true instead (my own derivation; this is the test of part 1)

Sealing depends on where the plane sits, not only on its direction. Layers along x alternate: odd x holds only
x-faces, even x holds only y- and z-faces.

- Plane at odd C (through a sheet of x-faces), outside = {x > C}: a y- or z-face at x = C+1 has 2 neighbours at
  x = C and 1 at x = C-1: 3 < 4. An x-face at x = C+2 has neighbours only at x = C+1, C+2, C+3: 0. So
  **{x <= C} with C odd is sealed for b = 4** although c(u) = 4.
- Plane at even C: an x-face at x = C+1 has 4 neighbours at x = C. Not sealed (this is Theorem A(ii)'s witness).
- Body diagonals: every layer holds all three types and each has 4 neighbours one layer back. Never sealed.

Predictions:

- **P1 (confinement, exact).** A finite pattern never leaves the smallest axis-parallel box with all six walls at
  odd coordinates that contains it (a box of whole cubes, wall faces included), and the box never grows. It can
  leave its tight bounding box by one half-step (a wall face born outside a pattern whose extreme cells are y/z
  faces). It does leave its diagonal hull.
- **P2 (permanent death goes two layers at a time).** A dead wall layer of x-faces alone is not sealed (4
  neighbours beneath); the wall layer plus the layer of y/z-faces beneath it is. A firewall is three layers
  (even, odd, even). So a "face death" is the simultaneous emptiness of two layers.
- **P3 (no piecewise death).** In a half-space with an odd wall, and in a slab one cube thick with both walls
  (layers odd, even, odd), a nearly in-plane generic v gives every cell at least 4 forward neighbours (wall cells
  2 in-plane + 2 beneath = 4; cells beneath 5 or 6). So no finite sealed set: critical thickness one cube.
- **P4 (reach, repaired).** The wall cell has degree K_f = 8 (4 in-plane, 4 beneath), a0 = 4 >= b - 1. Caps within
  reach 5..8; a fully live wall is immortal from c = 9. In a box the least vessel-degree is 6 (wall corner cells)
  and the three such cells at a corner have only 2 neighbours among themselves, so no armour at c = 6 or 7.
- **P5 (dynamics; the criterion gives no prediction, these are guesses with the reason).** Torus chaotic with
  density 0.39-0.42 (the two other K = 12, B45/S345 rules, gump and fcc, are at 0.419 and 0.394; stage-5 rule
  b/K = 1/3).
- **P6 (part 5 of the criterion, the falsifiable one).** With K_f = 8, sigma = K_f*rho/b = 2*rho = 0.78-0.84,
  below the 0.85 line: part 5 says the wall is starved or its law is weak (class.md S2: "every law with
  sigma <= 0.88 is weak", slope 0.03-0.12 per face cell, vn the exception). **If face12e shows a memoryless
  two-layer death with slope >= 0.15 per wall cell and sigma < 0.85, part 5 is refuted as a threshold.**
  My own guess, low confidence: there is a law, weaker than gump's 0.21 per cell.

## What would count against me

- A birth outside the odd box in any run: P1 wrong (and my reading of Theorem A wrong).
- No birth outside the diagonal hull, or none outside the tight bounding box, in many soups: the box is not the
  right hull.
- Face deaths that are single layers and permanent: P2 wrong.
