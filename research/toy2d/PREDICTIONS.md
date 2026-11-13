# Forecasts committed before measuring (toy2d)

Written 2026-11-13, after the rule search had started and before any symmetric run or any lifetime-vs-L fit.
Stated for whichever rule comes out best; τ = mean wait for an edge row to empty (QSD with restarts) in a
periodic strip of length L, and ln τ(L) ≈ a + I·L the asymmetric law (if one exists).

F1. **Mirror perpendicular to the edge (strip, x → −x).** The edge is its own mirror image, so only ~L/2 of its
    cells fluctuate independently. Forecast: ln τ_mx(L) has slope I/2 (ratio of slopes 0.5 ± 0.1), with an
    intercept shifted by a mirror-line term of either sign (gump: mirror planes are depleted, which made
    symmetric faces cost *more* per independent site as they grew).
F2. **Translation by L/k (strip).** Exact, not a forecast: the state *is* a strip of length L/k, so
    τ_tk(L) = τ(L/k). Used as a check of the machinery.
F3. **Mirror y → −y (strip; swaps the two edges).** The two edges die together, so the first-death rate halves:
    τ_first(my) = 2 τ_first(asym) = τ_edge; slope unchanged.
F4. **Square box, full D4 symmetry.** The stabiliser of an edge in D4 is one mirror (order 2), not 8: the
    exponent drops by a factor **1/2, not 1/8**; the four edges die in lockstep. In gump the stabiliser of an
    octahedral face in O_h has order 6 (C3v), hence the slope 0.209/6; the 2D analogue of "1/|stabiliser|" is 1/2.
F5. **Square box, C4 rotation or the diagonal mirror alone.** No edge is mapped to itself, so the exponent is
    *unchanged*; only the number of independent edges drops (4 → 1 for C4, 4 → 2 for the diagonal mirror), so
    the first-edge wait grows by ≈4× and ≈2× respectively. Symmetry is fatal only when it fixes an edge.

## Outcomes (measured after the above was committed; details in README.md section 5)

- F1 hit at the low edge of the band: slope ratio 0.42 (cross2 B34/S234), 0.46 (Moore B45/S23467).
- F2 hit: 1,631 +- 25 vs 1,679 +- 26.
- F3 hit within 25%: ratio 2.22, 2.41, 2.50 at L = 16, 20, 24.
- F4 hit: box slope 0.171 vs 0.343, ratio 0.50.
- F5 diagonal mirror: exponent unchanged (hit) but waits x1.0-1.16, not x2 (miss).
- F5 C4: miss -- slope 0.274 vs 0.343 and waits shorter than asymmetric boxes.
