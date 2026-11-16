# The living state of a hull face (research/hulllocal)

2026-11-16. Question: is the face layer of a living octahedral hull (radius 15, faces of 108 cells; radius 13, 84)
occupied differently from a wrapped face (a face torus on an 8-layer slab), in its interior or near its rim, enough
to join the two prices per cell (rimmed 0.2307 ± 0.0047, wrapped 0.2087; CLAIMS CN2) through the tube relation
discount = 1.85 × density deficit (research/wraplocal)? That relation would need the hull interior denser by 0.012.

## Forecasts (written and committed before any stepping was run)

Nothing had been stepped or measured when these were written; only the cell counts of the vessels were known
(hull R = 15: 2,064 cells, face 108; R = 13: 1,386, face 84).

- **P1 (65%).** The face-layer density in the interior of the R = 15 hull face (cells three or more layers from
  every other face) equals that of a long-loop wrapped face measured by the same code within 0.001.
- **P2 (25%).** It exceeds the wrapped value by more than 0.004.
- **P3 (10%).** The excess is between 0.008 and 0.018.
- **P4 (70%).** The rim cells (in the face layer of a second face as well, or one layer from it) differ in density
  from the interior by more than 0.01, either sign.
- **P5 (60%).** The rim is *less* dense than the interior (against the lead's H5).
- **P6 (80%).** Wrapped faces on slabs of 8, 12 and 16 layers have face densities equal within 0.0005; the layer
  beneath likewise.
- **P7 (60%).** The rim's density excess or deficit, summed over the face, per unit of rim length, is the same at
  R = 13 and R = 15 within two standard errors.
- **P8 (65%).** Occupation explains less than a quarter of the price difference: 1.85 × |interior excess| < 0.0055.
