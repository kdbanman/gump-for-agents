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

## Block 3: 03:41 UTC, before prism(8,10,4), prism(8,10,5) (8-row faces beside 10-row faces) and par 1

- **R8.** An 8-row face beside 10-row faces (depth 10) outlives the same face beside 8-row faces:
  (8,10,4) 8-row class > 11.0896 by 0.02 to 0.15: 55%; within +-0.02: 35%. At L = 5, > 13.864 by more than 0.04: 50%.
  (Beside 6-row faces it lived 0.04, 0.22, 1.17 less at L = 4, 5, 6, but the 8 x 6 rod may be dying as a rod.)
- **R9.** par 1 (obtuse rim row sparse, sharp rim row dense), (8,8,4,1) against (8,8,4,0) = 11.090: lower, by 0.2
  to 1.2: 60% (the dense sharp row was cheap in the odd widths: 0.107 a cell).

## Block 4: 03:47 UTC, before (9,9,5), the second seeds, (12,12,4), (14,14,3)

Known now: (10,10,4) 13.433, (10,10,5) 16.900 +- 0.028. The cost of two more rows at length L, g(L) =
ln tau(w+2, L) - ln tau(w, L): 1.52 to 1.56 (L = 3), 2.344 (L = 4), 3.036 +- 0.032 (L = 5); the mixed second
difference over w 8 -> 10, L 4 -> 5 is 0.692 +- 0.034, per cell 0.231 +- 0.011.

- **R10.** (9,9,5): 14.91 +- 0.06, i.e. g(5) from the odd widths 7 -> 9 equals 3.04 +- 0.06 (the even widths'). 65%.
- **R11.** (12,12,4): 15.78 +- 0.05, i.e. g(4) from 10 -> 12 rows equals the 2.344 of 8 -> 10 within 0.05 (no
  zone: a row costs the same wherever it is added). 60%. If there is a support zone narrower than 5 rows it comes
  out LOWER (P = 25%); higher: 15%.

## Block 5: 03:47 UTC. The 135-cell and 165-cell hull faces (k = 9, 10), before reading any other agent's value

What I have: the hull's own values (second differences 0.800, 0.692, 0.692 +- 0.015) and my strips. In corner-free
strips of 8 to 10 rows the mixed second difference per cell is 0.231 +- 0.011 at L 4 -> 5 (0.273 at 3 -> 4,
where a tube of girth 3 is cheap), and at L = 3 the cost of a row does not fall as the strip widens from 8 to 12
rows (1.525, 1.561): no sign of a support zone that ends. So the hull's 0.2307 is not made by corners and is not
bending at the widths I can reach. I extrapolate the hull by a constant second difference 0.692, shaded a little
towards the wrapped value because the strip measurement is only 2 sigma from 0.2087.

- **ln tau_face(135 cells, k = 9) = 29.222 +- 0.030.** (2 x 23.3392 - 18.1407 = 28.5377 +- 0.021, plus a second
  difference 0.684 +- 0.020.) P(nearer 29.230 than 29.163) = 72%; P(nearer 29.163) = 28%.
- **ln tau_face(165 cells, k = 10) = 35.79 +- 0.08** (second difference 0.68 +- 0.03 again; 35.813 if 0.692 holds
  twice, 35.61 if the wrapped price took over from k = 8).
- P(the second difference at k = 8 lies in 0.66 to 0.72) = 65%.

## Block 6: 03:58 UTC. Revision of block 5 after the long (8,8,6) run and (12,12,4); still before any 135-cell value

New since block 5: (8,8,6) = 16.4735 +- 0.026 (two runs), so the length price at 8 rows goes 0.2455, 0.2308,
0.2177 +- 0.0023 per cell over L 3->4->5->6: it is still falling at 72 cells. (12,12,4) = 15.774: the cost of a row
pair at L = 4 is 2.343 (8->10) and 2.340 (10->12): linear in width, so ln tau = a(L) + (w/2) g(L) with
g = 1.54, 2.342, 3.039 at L = 3, 4, 5 and a = 1.97, 1.72, 1.71. If a(6) = 1.71 too, g(6) = 3.69 and the
increments of g are 0.80, 0.70, 0.65: the strips' analogue of the hull's second differences (0.80, 0.69, 0.69)
would be bending towards 0.626. That is an inference with one assumption, not a measurement. Block 5 stands as
frozen; this is what I would say now:

- **ln tau_face(135) = 29.210 +- 0.035** (second difference at k = 8: 0.672 +- 0.025). P(nearer 29.230) = 62%,
  P(nearer 29.163) = 38%.
- **ln tau_face(165) = 35.74 +- 0.09.**

## Block 7: 03:58 UTC, before the death rings of (10,10,4), (12,12,3), (14,14,3), hull 9, (10,10,5)

Known: share of deaths with a one-generation fall of at least half the face in the last 12 generations:
(8,8,4) 0.203 +- 0.004, (8,8,5) 0.158 +- 0.003. (Wrapped 0.51 to 0.60 and hull 0.016 to 0.022 at 63 to 84 cells,
agent anatomy.)
- **R12.** The share rises with width at fixed length: (10,10,4) above 0.203 by more than 0.03: 55%.
  (12,12,3) and (14,14,3) (girth 3) above 0.25: 50%.
- **R13.** Hull R = 9 (45 cells) by my code: below 0.06: 75%.
