# Rimmed hull faces dying: forecasts and definitions (written before any production table)

2026-11-18, about 03:30 UTC. Written after the recorder `hd.c` was built and checked on 300 generations against the
engine, and before any production run was looked at. Probabilities are mine.

## System and definitions

- Vessel: the exact hull of the soup region |p|_1 <= R, cube-centred (research/gpu/facelaw.py, hullface.py `vessel(R)`):
  R = 11 (876 cells, 8 faces of 63 cells, 366 face-layer cells) and R = 13 (1,386 cells, faces of 84, 510 face-layer
  cells). Adjacent faces share their rim row. Soup p = 0.35 on every cell. A life ends at the first generation some
  face is empty (a face death) or when it settles (period 1-2, or a cycle caught by snapshots as in fr.c). Deaths
  count at age > T0 = 200.
- Definitions follow `research/dying/README.md` and its PREDICTIONS.md: P = live cells of a face; lag l = l
  generations before t_d, the first generation with that face empty. Excursion (round 2): starts at the first
  P < U after a generation with P >= U (both at age > T0), ends recovered at P >= U, dead at P = 0, censored if the
  life ends otherwise; U = ceil(P bar) with P bar from round 1/2 (31.25 at A = 63, 42.49 at A = 84): U = 32, 43.
- q(k): among excursions whose minimum is <= k and that are not censored, the fraction that end dead. The point of no
  return k* is where q crosses 1/2 (linear interpolation in k, live cells).
- Row of a face cell: layers to the nearest edge plane (0 = the shared rim row). Corner distance: Euclidean distance
  (cube units) to the nearest of the face's three corners (the mean position of the cells on two edge planes).
- "Last living cells": the face's live cells at lag 1 (the last non-empty generation). Stationary comparison: null
  samples (every lane at age > T0 + 1 every 997 generations), live cells counted with equal weight.
- Equal depth: recovered excursions with minimum exactly k, against deaths, both aligned at their first generation
  with P <= k in that excursion.

## Forecasts

| | forecast | p |
|---|---|---|
| H1 | ln tau_face from my lives (ln(8E/F), T0 = 200) agrees with the GPU's within 2 sigma: 13.636 (R = 11), 18.141 (R = 13) | 0.9, 0.85 |
| H2 | P bar within 0.15 of 31.25 (R = 11) and 0.25 of 42.49 (R = 13) | 0.85 |
| H3 | R = 11 mean dying face reproduces round 1 (c1): P/P bar at lag 4 in 0.26-0.36, at lag 8 in 0.60-0.74, at lag 16 >= 0.90 | 0.75 |
| H4 | the plunge (first generation with P <= P bar / 2 in the final excursion, to t_d) has median 6-8 at R = 11 and is longer at R = 13 by 0 to 2 generations | 0.65 |
| H5 | k* (q = 1/2) is 2-3.5 live cells at R = 11 (round 2: 0.079 P bar = 2.5) and 2-4 at R = 13; k*/P bar smaller at R = 13 | 0.75, 0.6 |
| H6 | q(3) at R = 13 within a factor 1.5 of q(3) at R = 11 (the decision is in the last few cells, whatever the size) | 0.55 |
| H7 | the last living cells are over-represented in the rim row: (share of lag-1 live cells in row 0) / (share of stationary live cells in row 0) in 1.05-1.40 at both sizes | 0.55 |
| H8 | the last living cells are under-represented within 1.5 cube units of a corner, relative to stationary live cells | 0.6 |
| H9 | the dying face is uniform over the 8 faces (chi2 at 5%) | 0.95 |
| H10 | at t_d the three edge neighbours are at 0.70-0.88 of their stationary population (their shared rim row is the dying face's), the three vertex neighbours and the opposite face at >= 0.93 | 0.7 |
| H11 | at equal depth k (3 <= k <= 6), the descent from P bar to k is faster in dips that die than in dips that recover (median time from the last P >= U to the first P <= k smaller for deaths) | 0.55 |
| H12 | at equal count, the minimum of a recovered dip is more clumped (smaller mean pairwise distance of live cells) than a dying face passing that count | 0.6 |

What would be against my reading (the rim is where a dying hull face holds on, fed by the living neighbour, and
the nearly empty corners do not matter): H7 failing low (rim row under-represented at the end) or the corner share
of the last cells at or above stationary.
