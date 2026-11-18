# Forecasts of agent split-slab, frozen before the data

## Block 1: 2026-11-18 03:50 UTC, before any run of mine on the 120-cell tube (1,18),(0,40)

Known to me: the anchors of BRIEF-COMMON.md, the PI's update of 03:32 UTC ((1,17),(0,32) 19.7446 ± 0.0042;
(1,16),(0,36) 22.1599 ± 0.0086), my own runs on 48 and 63 cells. Not known: anything measured on the 120-cell tube.

**Prior (no measurement of mine at 120 cells; plain extrapolation of the tube's local slope 0.20226 (84 to 96),
0.20128 (96 to 108), next 0.2008 ± 0.003):**

    ln tau_face, torus (1,18),(0,40), 120 cells = 24.57 ± 0.04      P(truth within the error) = 60%

**Procedure for the measured forecast (fixed now, before the 120-cell run):** the multilevel-splitting sampler does
not beat brute force on gump (README, "Why splitting fails"), so the number of record will come from the exact
bookkeeping 1/tau = nu(p) q(p): nu_A(p) = rate per face-generation of excursions (first passage to <= LAM0 after
>= PA, until the return to >= PA) whose minimum population is <= p, measured by a plain run at each size with
PA = round(0.515 A - s), LAM0 = round(0.515 A - 3 s), s = sqrt(0.415 A); ln q_A(p) = -ln tau_A - ln nu_A(p) from the
anchors at 84, 96, 108 cells (loop^2 12 tubes); ln q_120(p) by the straight line in A through those three;
ln tau_120 = -ln nu_120(p) - ln q_120(p), at the deepest level p with at least 400 excursions at 120 cells, and at
two shallower levels as a check. The same procedure is first run blind on a known case: the 108-cell tube from
78, 84, 96 cells. P(the procedure's 108-cell value lands within 0.04 of 22.1599) = 65%.
P(the 120-cell value so obtained lands within 0.05 of the GPU's) = 55%.
