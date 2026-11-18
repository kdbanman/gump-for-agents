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
