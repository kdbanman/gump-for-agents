# blast/holes: forecasts (agent `holes`)

## Block A. Frozen 2026-11-18 11:25 UTC, before any code of mine has run

Written after reading the common brief, the report (short version, items 2, 5, 6, the 135-cell section), the
`tube1d` README section 3, `pi/patch_vs_torus.py` and the two notebook entries on empty patches. Not read: the PI's
block 5, anything under `research/blast/noisy/`.

Not blind (computable from numbers on file, said here so that nobody counts them as forecasts): on the 12 × 12
torus the mixed second difference of −ln P over rhombi, per cell, is 0.265 at (2.5, 2.5) and 0.250 at (3.5, 3.5)
(from 6.254, 8.793, 12.128, 15.399, 19.421), and 0.282 at (1.5, 2.5).

Notation: f(a, b) = −ln P(rhombus of a × b unit cells is empty at an instant); M(a+½, b+½) = f(a+1, b+1) −
f(a+1, b) − f(a, b+1) + f(a, b); "bulk cost per cell" = M/3.

**A1. Wide torus, bulk cost.** At the largest sizes plain running reaches (M at (3.5, 4.5); (4.5, 4.5) will be too
noisy) the bulk cost per cell reads 0.240 ± 0.012 (P = 0.6), in any case above 0.225 (P = 0.85): the direct
measurement will NOT show 0.2087; it will show a number still falling with size. M(2.5, 4.5)/3 = 0.250 ± 0.012
(P = 0.55). M depends mainly on min(a, b) (same within 0.008 per cell along a row from b = a+1 on): P = 0.5.
An exponential approach fitted to the M's (one length for all) extrapolates to 0.2087 ± 0.015: P = 0.55; to
something outside 0.19–0.23: P = 0.15.

**A2. How a patch empties.** By a one-generation fall of at least half the patch's cells within its last 9
generations ("bust"): share 0.65 ± 0.12 at 3 × 3, 0.55 ± 0.15 at 4 × 4 (each P = 0.6); falling with patch size
(P = 0.75). The layer beneath an emptied 3 × 3 patch is depleted too (density of the cells of the second layer
adjacent to the patch below 0.30 at the instant of emptiness, where 0.435 is normal): P = 0.7.

**A3. Hull interior against torus.** Rhombi 2 × 2, 2 × 3, 3 × 3 with every unit cell three or more rows from every
rim of a large hull face have the torus's ln P to within 0.03 (P = 0.7). Two rows from the rim: within 0.05
(P = 0.5).

**A4. The rim map.** A rhombus with a side on the rim is likelier to be empty than the same rhombus in the
interior (P = 0.7; for 3 × 3: rim − interior = −1.0 ± 1.0 in −ln P). A corner rhombus is likelier still (P = 0.65).
The cost against distance from the rim is monotone and within 0.05 of the interior value from distance 2 on
(P = 0.55).

**A5. Rim rows.** The rim row itself (strips one unit cell wide along the rim): 0.45 ± 0.05 per cell of added
length, against 0.55 in the interior (P = 0.5). Row prices from the mixed second difference of rim strips (w rows
by l units, l about 3 to 4): 0.27 ± 0.03 going from 1 to 2 rows, 0.245 ± 0.02 from 2 to 3 (P = 0.5 each). "The
rim-zone M exceeds the torus M at the same (w, l)": P = 0.5, a coin: I do not know. "The static row prices equal
the hull lifetimes' second differences, 0.266 for the second row and 0.231 for the third, both within 0.015":
P = 0.3.

A remark made before data, because it shapes the model I will try in step 3: if a face's price is a sum over
cells of a price that depends only on the cell's row r = distance from the nearest rim, then the second
difference of ln τ in the side k is exactly 3·c_r with r = floor(k/3) (the number of cells in row r is 9(k − 3r −
1) for k − 3r ≥ 2 and 3 for k − 3r = 1; its second difference in k is 3 for k − 3r in {0, 1, 2} and 0 otherwise).
The anchors then read c_1 = 0.266 (k = 5) and c_2 = 0.231, 0.230 (k = 6, 7), the 135-cell face (k = 8 uses c_2
again) is "the second difference repeats", 29.230, and only from 165 cells on does a new row price c_3 enter.

**A6. The hypothesis as a whole.** At hand-back I will write "the living state supports one bulk price 0.2087 ±
0.01 with the surplus in the rim rows": P = 0.4; "the data reject it": P = 0.15; undecided: P = 0.45.

**A7. The forecast I expect to freeze.** ln τ(135 cells) within 29.23 ± 0.04: P = 0.7.

## Block B. Frozen 2026-11-18 11:55 UTC: ln τ of hull faces of 135, 165, 198 cells

Frozen before reading anything under `research/blast/noisy/` (never opened) and before reading the PI's block 5.
What I had seen when freezing: my own interim tables (torus 12 × 12 at about 2·10⁷ generations of 256 lanes, hull
R = 29 at about 3·10⁶), my lifetime of the 18-cell hull face (4.855 ± 0.015, `data/life.txt`), the anchors of the
common brief, and the night's forecasts quoted in `REPORT.md` (29.22 ± 0.02 by the dip-rate route, 29.30 ± 0.09
and 29.34 on the surrogate, 35.780 and 43.011 at 165 and 198 cells by the dip-rate route). So these are NOT
independent of the night's extrapolations: the static measurement gave me no number that enters them (see README:
the living state shows no surplus in the rim rows, and its cost of emptiness is not converged at the sizes plain
running reaches). They are the anchors, plus one new anchor of mine at 18 cells, extrapolated by formula S of
`model.py` (a rim term, one asymptotic price left free, one geometric transient), with the rows formula R as the
upper companion.

| face | forecast (ln τ_face) | how |
|---|---|---|
| 135 cells (R = 17) | **29.21 ± 0.03** | S, price free, anchors 18–108 cells: 29.207 (29.177 … 29.232); anchors 30–108: 29.225; R: 29.231 ± 0.025 |
| 165 cells (R = 19) | **35.75 ± 0.06** | S: 35.746 (35.677 … 35.801); R with ρ = 0.6 ± 0.3: 35.787 ± 0.048 |
| 198 cells (R = 21) | **42.96 ± 0.11** | S: 42.954 (42.830 … 43.051); R: 43.010 ± 0.087 |

Probabilities: 135-cell face inside 29.21 ± 0.03: 0.6; above 29.26: 0.12; below 29.165 (the wrapped price taking
over at once): 0.08. The asymptotic price per cell of a hull face, if formula S is the right family: 0.223 (0.2175
to 0.227), neither 0.2087 (χ² 6.4 on 2) nor 0.2307 (χ² 4.1 on 2); P(the true asymptote is within 0.003 of 0.2087):
0.3; within 0.003 of 0.2307: 0.25.

Forecast inside block B that can be scored today from my own run: the corner triangle of side 6 (63 cells, two
real rims) will read −ln P = 18.75 ± 0.15 when the hull run ends (interim 18.79 ± 0.17 on 78 hits; "the same
object as the 63-cell hull face plus an edge linear in its length" would be 18.55).
