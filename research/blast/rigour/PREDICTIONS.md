# blast/rigour: forecasts frozen before data

Written 2026-11-18 03:45 UTC, before any row of `data/mc.csv` existed or was read (the Monte Carlo of the
one-layer surrogate was queued, not started) and before the exact rows of the 18-cell tori (1,1),(0,6) and
(1,2),(0,6) and the strip 2 x 3 existed. **Breach, stated plainly:** the first exact rows (9 to 18 cells, already in
`data/exact.csv` at this time) were run with no forecast on file.

Surrogate = one face layer on gump's rule over private coins (0.44, 0.42); see THEOREMS.md.

- **R1 (60%).** The rimmed triangle of 30 cells (hull R = 7) has ln tau at least 0.3 *below* the least-squares line
  of the wide wrapped faces (A >= 27) at 30 cells: in the one-layer surrogate the order is wrapped > rimmed, the
  reverse of gump's. Same sign at 45 cells (R = 9): 55%.
- **R2 (55%).** Tubes of girth two unit cells, (2,0),(0,D), D = 3..8: the step of ln tau per unit of length falls
  with D at every D (ln tau concave in the length), within the errors.
- **R3 (65%).** Wide wrapped faces of 27 to 48 cells: slope of ln tau between 0.20 and 0.30 per cell.
- **R4 (50%).** Girth-one tube (1,0),(0,12), 36 cells: ln tau < 6.5 (the thin tube saturates: its quasi-stationary
  law is a patch that wanders, density falling with length).
- **R5 (60%).** Free strip 2 x 3 (18 cells, exact): ln tau > 4.9 (above the 18-cell patch 2 x 3 at 4.473 and within
  reach of the girth-one tube at 4.995); strips two unit cells wide grow with length (step > 0.2 per unit cell
  from 2 x 2 to 2 x 3, i.e. ln tau(2 x 3) > 4.69): 75%.
- **R6 (gump, the blind 120-cell tube (1,18),(0,40), loop^2 12).** ln tau_face = 24.570, 68% interval +- 0.025. Reason:
  Theorem 3 says a tube of fixed girth has a per-cell price that converges (a discount is per cell and bounded),
  so the step per 12 cells stays at 2.415 +- 0.02 (it was 2.423, then 2.415); a discount growing like length^2
  would put the step at 2.407 and the value at 24.563, which this forecast cannot tell apart. I do not expect the
  step to fall below 2.39 (80%).
