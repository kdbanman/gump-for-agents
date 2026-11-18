# research/dying2: forecasts, written before the first table

Written 2026-11-18 03:20 UTC, before any analysis of the death or dip records was run (the only numbers seen were
the pilot stationary means below and the run logs' death counts). The hull-face share (research/dying2/hull/) has
its own forecasts there.

## Faces and fixed inputs

Wrapped faces, 8-layer slabs of `research/shape/tslab.py`, density-0.4 soups, as research/gpu-local/eqtorus.py:
W63 = (1,4),(0,21) (63 cells); E84 = (2,4),(0,14) (84, equilateral); T84 = (1,12),(0,28) (84, loop² 12 tube);
T96 = (1,17),(0,32) (96, loop² 12 tube). P̄ (the excursion threshold, fixed now, from `dy.py pbar`, 200,000
generations x 256 lanes, age > 512): 32.58, 43.48, 43.30, 49.48.

## Definitions (research/dying/README.md where they carry over)

- t_d = first generation with the face empty; lag l = t_d - t. Only deaths at age > T0 = 512.
- t_h = earliest t <= t_d with P(t') < P̄/2 for every t' in [t, t_d]; plunge Δ = t_d - t_h (round 1, L6/L7).
- Excursions, q, ν: round 2's definitions, with this study's P̄. "Reaches k" = min P <= k (integer live cells).
  q(k) = dead / (dead + recovered) among excursions with min <= k. k* = the k at which q crosses 1/2 (linear
  interpolation in k). ν(k) per face per generation at age > T0.
- There is no rim. Instead of distance to rim and corners: for every face the "axis" direction is the in-plane
  direction perpendicular to its shortest loop vector s; u = position along it, periodic with period
  Lax = covolume / |s|. G = the largest circular gap between the u values of the live cells, as a fraction of Lax;
  X = 1 - G, the axial extent of the survivors. "Cut": an empty band, G·Lax >= 1 cube edge. Random-thinning
  null: null samples (stationary faces) thinned uniformly at random to the same count.

## Forecasts (probability that each holds)

1. **Same collapse as a hull face (70%).** On W63 the mean P/P̄ at lag 16, 8, 4 lies within 0.08 of the c1 hull
   face's 0.95, 0.67, 0.31 (round 1), and the median plunge Δ is 5-8 generations on all four faces.
2. **Plunge length does not depend on shape (65%).** Median Δ of T84 and E84 differ by at most 1 generation, and
   T96's median is within 1 of T84's.
3. **Point of no return (65%).** k* lies in 2-4 live cells on W63 and in 2-5 on the other three.
4. **Last cells (70%).** Mean live cells at lag 1 is 1.4-1.9 on every face (c1 hull: 1.61).
5. **Shallow dips (60%).** On W63, ln ν at 0.7 P̄ (min <= floor(0.7 P̄)) lies in [-4.8, -4.2] (c1 hull: -4.16; the
   wrapped face's narrower σ_P should make it rarer).
6. **Where the tube's discount lives (55%).** Between E84 and T84 (ln τ 17.55 against 17.32): at least half of
   the 0.23 is in ln ν at P̄/2 (dips reaching half the mean) and less than half in ln q at P̄/2.
7. **No moving band on tubes (65%).** On T96, in the median death the final cut (the start of the last unbroken
   run of generations with a cut before t_d) begins at most 12 generations before t_d: a tube does not open in
   one place and spread over tens of generations; it thins and the cut comes with the last few cells.
8. **But the survivors are clumped along the axis (70%).** At t_h, on T96, the survivors' mean axial extent X is
   at least 10% below the random-thinning null at the same count.
9. **A tube is not special in this (50%).** The same ratio X / X_null at t_h on E84 (along its own shortest-loop
   axis) is within 0.05 of T84's.
10. **Dying against recovered at equal depth (60%).** At equal count k (2 <= k <= 5), the survivors of faces that
    go on to die (taken at their first generation at k) have a larger mean axial extent X than recovered dips at
    their minimum k: dying faces are more spread out (round 4's direction on hull faces).
11. **The layer beneath (65%).** On W63, the layer beneath the dying face at lag 4 is at 0.6-0.85 of its own
    stationary population.
12. **Code checks (95%).** No co-death of the two faces of a slab in more than 1 in 1,000 deaths; ν·q equals the
    face death rate at every k to within the censored share.
