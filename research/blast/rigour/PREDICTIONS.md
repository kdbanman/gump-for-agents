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

## Added 03:58 UTC (before the second-pass rows of (1,1),(0,14) and (1,1),(0,16) were read)

Two-branch reading of the surrogate's tube (1,1),(0,D): deaths split into "bust" (a fall of half the face in one of
the last 6 generations) and "starve"; the bust share p(D) falls from 0.81 (D = 6) to 0.42 (D = 12); with each branch
exponential in D the step of ln tau is c_s + p (c_b - c_s), c_b - c_s = 0.29 per unit of length from the shares,
c_s = 0.585 from the steps at D = 9..13.
- **R7 (65%).** ln tau of (1,1),(0,16), 48 cells: 12.43 +- 0.07 (the step 14 -> 16 is 2 x 0.66, not 2 x 0.69 or more).
- **R8 (60%).** Bust share at D = 16: 0.22 +- 0.06.
- **R9 (gump; a test for agent anatomy's files, 55%).** If the fall of a tube's price with length is this crossover,
  then on the loop^2 12 tubes of 84, 96, 108 cells the share of deaths with a half-face fall changes by 3 to 6
  points per 12 cells (curvature of ln tau = -(d ln odds/dA)^2 p(1-p); the measured second difference
  -0.008 per 12 cells needs |d ln odds/dA| = 0.015 per cell). If the share is flat to 1 point, the reading is dead.

## Scores (04:04 UTC)

| | forecast | outcome | |
|---|---|---|---|
| R1 | triangle of 30 cells at least 0.3 below the wide wrapped line (60%); same sign at 45 (55%) | 6.889 ± 0.005 against 7.985 ± 0.005: 1.10 below; 45 cells: 10.582 ± 0.010 against 11.76: 1.18 below | **hit, hit** |
| R2 | girth-2 tube (2,0),(0,D): step falls with D at every D (55%) | steps 1.356, 1.598, 1.669, 1.579 (± 0.01–0.03): rises first | **miss** |
| R3 | wide wrapped slope 0.20–0.30 per cell (65%) | 0.2524 (least squares, 27–48 cells) | **hit** |
| R4 | girth-one tube of 36 cells below 6.5 (50%) | 6.308 ± 0.007 | **hit** |
| R5 | strip 2 x 3 above 4.9 (60%) and above 4.69 (75%) | 6.1754024793 (exact) | **hit, hit** (and far too timid: I expected about 5) |
| R6 | gump's 120-cell tube 24.570 ± 0.025 | not yet measured | open |
| R7 | surrogate tube (1,1),(0,16): 12.43 ± 0.07 (65%) | 12.445 ± 0.032 (984 deaths, `mc` seed 77); 12.451 ± 0.019 (2,853 deaths, `mcrun2.py`) | **hit** |
| R8 | its bust share 0.22 ± 0.06 (60%) | 0.229 ± 0.013 | **hit** |
| R9 | gump's long tubes: bust share moves 3–6 points per 12 cells | not measured here | open |

6 of 7 scored forecasts hit (two of them double). The miss is the one that assumed thin tubes behave alike: girth one
saturates, girth two does not. The first exact rows had no forecast on file (stated above).
