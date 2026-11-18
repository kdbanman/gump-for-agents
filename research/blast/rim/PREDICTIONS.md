# Forecasts of agent `rim` (research/blast/rim), frozen before the data

## Block 1: 2026-11-18 03:33 UTC, before any strip (prism) lifetime has been run

Known to me: the anchors of BRIEF-COMMON.md, research/hulllocal/README.md. Nothing has been stepped on a prism
except the oracle validation (states only, no lifetimes).

Vessel: prism(T1, T2, L, par): two families d1 = (1,1,1), d2 = (1,1,-1), T1 and T2 layers, period L*(2,-2,0).
A d1 face is a strip of T2 rows (alternately 2L and L cells) and length L.

- **R1.** ln tau of a face of prism(8,8,5,0) (60 cells, 8 rows, L = 5; one obtuse and one sharp rim):
  12.9 +- 0.6 (wrapped line at 60 cells: 12.536; hull triangle at 63: 13.63). P(inside) = 60%.
- **R2.** The corner-free bulk price, read as the mixed second difference of ln tau over width and length
  (rows w in 5..8, L in 5..8, faces up to about 63 cells), per cell: P(0.200 to 0.217) = 35%,
  P(0.217 to 0.240) = 45%, P(outside both) = 20%. (I lean to "the hull's 0.231 is already in strips": a strip
  of 6 rows is all rim, and the rim profile is three rows deep.)
- **R3.** The slope in L at fixed width exceeds 0.2087 x (cells per unit length), i.e. the two rims together
  cost something positive: 75%.
- **R4.** A sharp rim (70.5 degrees, which no hull has) is cheaper to kill along than an obtuse one, so faces
  whose sharp rim is the dense row live less long than their mirror with the obtuse rim dense, at equal cells:
  55% (weak).

## Block 2: 03:38 UTC (machine clock; block 1 was in fact written at 03:28), before (10,10,4), (10,10,5), (12,12,4), (14,14,3) and the long (8,8,6)

Known now: symmetric prisms (w,w,L,0), ln tau: (8,8,3) 8.145, (8,8,4) 11.090, (8,8,5) 13.864, (8,8,6) 16.52 +- 0.07,
(10,10,3) 9.669, (12,12,3) 11.231; thin rods (6,6,L) saturate near 10.2 (a rod death, not a face death), and faces
beside narrower faces die sooner. At L = 3 a row costs 0.169 to 0.174 per cell from 8 to 12 rows (a tube of girth 3).

- **R5.** ln tau of (10,10,5) (75 cells): 17.09 +- 0.15, i.e. the 15 cells of two more rows at L = 5 cost
  0.215 +- 0.010 each. P(per-cell price of width at L = 5 below 0.220) = 60%; P(above 0.226, "the hull's 0.231 is
  in strips") = 25%.
- **R6.** ln tau of (10,10,4) (60 cells): 13.55 +- 0.12 (12 cells at about 0.205). ln tau of (12,12,4): 16.0 +- 0.2.
- **R7.** (8,8,6) long run: 16.55 +- 0.06 (length price at 8 rows, 5 -> 6: 0.224 +- 0.005 per cell). 70%.
