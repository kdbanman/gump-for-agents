# Forecasts for research/shape2 (committed before the production runs)

2026-11-14. Question: at fixed face area A, what is ln τ_face of a periodic gump slab face (m = 8) a function of?
Every class of index-n period lattices is measured (n = 16, 20; and the five n = 24 classes research/shape did not
run). Classes: `python3 research/shape2/lattice2.py n` (9 at n = 16, 10 at n = 20, 15 at n = 24).

**What was seen before these forecasts.** The published values (research/shape/data/A72.csv, A60.csv) and a pilot of
256 lives per class (`research/scratch/shape2/pilot/`, cap 32768, used only to choose caps and job counts in
`drive2.py`; it is not used in any result and nothing below was fitted to it). The pilot showed, roughly: systole 1
fires a transverse firewall within ~20 generations; systole² 3 tori hold chaos (A = 48: ln τ ≈ 8.7); systole² 4
tori are firewall-dominated (65–99%). So "thin" will mean systole 1 only, unless the production runs say otherwise.

**Fitted on published values only.** Each law has a free constant c(A) per area and two shape parameters (three for
L4), fitted by least squares to the 15 published classes (presentations pooled per class: 10 at A = 72, 5 at
A = 60). `python3 research/shape2/laws.py --json research/shape2/data/predictions.json`. Lengths in units of |u1|.

- **L1** (shortest loop): f = −B e^{−K s₁}.
- **L2** (two successive minima): f = −B (e^{−K s₁} + e^{−K s₂}).
- **L3** (sum over primitive loop classes): f = −B Σ_{v primitive, mod ±} e^{−K|v|}; **L3p** the same with |v|^{−K}.
- **L4** (my candidate: a loop sum that sees the rows, extensive in area): f = −B (A/72) Σ_v e^{−K|v|(1 + E cos 6θ_v)},
  θ_v the angle of v from the row direction u1 (θ = 0 along a kagome row, 30° across).
- Amplitude scaling across areas: "const" (same B at every A) or "area" (B ∝ A, as the finite-size free energy of a
  gapped field on a torus would be). Both are given for L1–L3.

None of them fits the published data well (table below: χ² 40–81 on 10–11). Every one is driven by the A = 60 pair
(16,4,19) vs (16,12,21), which all of them put within 0.006 of each other where 0.019 ± 0.004 was measured, and by
systole² 21 at A = 72, which they put 0.04–0.08 too low. The anisotropy E of L4 fits to −0.01: the published data
see no row direction. So **I forecast that none of these laws will pass at either area**, and that the systole
will remain the main variable. The A = 48 forecasts are differences from the hexagonal 4×4 torus (c(48) is not fitted).

## Refutation criteria (fixed now)

- At each area, over **distinct chaotic classes** (systole² ≥ 7, plus systole² 3 and 4 tested separately), with c(A)
  free and the other parameters **fixed at their published-fit values**: a law is refuted at that area if χ² has
  p < 0.01. A refit of B, K (E) on the new data at one area is reported separately as "the law's form survives".
- "Same law at both areas": one refit to all classes at 48 and 60 (and 72 published) with one B, K (scaling as named)
  and a free c(A) per area; refuted if p < 0.01.
- Ordering: if two classes with equal s₁ differ by > 3σ, L1 is refuted at that area. If two classes with equal
  (s₁, s₂) differ by > 3σ, L2 is refuted (e.g. none exist at A = 48/60, so L2 is tested only through its form).
- For thin classes (systole² 3, 4) every law extrapolates far out of the range it was fitted on; the numbers below
  are given, but a miss there refutes only the functional form's tail, not the law at systole² ≥ 7.

## Fits on the published values

| law | B | K | E | χ² / dof on published classes |
|---|---|---|---|---|
| L1-const | 4795 | 3.154 | 0.000 | 81.0 / 11 |
| L1-area | 1444 | 2.743 | 0.000 | 64.7 / 11 |
| L2-const | 1707 | 2.804 | 0.000 | 71.1 / 11 |
| L2-area | 301.6 | 2.205 | 0.000 | 50.8 / 11 |
| L3-const | 10.91 | 0.655 | 0.000 | 51.9 / 11 |
| L3-area | 10.76 | 0.704 | 0.000 | 44.1 / 11 |
| L3p-const | 2668 | 8.010 | 0.000 | 65.9 / 11 |
| L3p-area | 295.5 | 5.870 | 0.000 | 47.9 / 11 |
| L4-area | 54.31 | 1.593 | -0.010 | 40.3 / 10 |


## Predictions

Systole² 1 (thin) is not expected to hold chaos; numbers there are meaningless and given only for completeness.

**A = 48** — predicted ln τ(class) − ln τ(4×4 hexagonal, (4,0),(0,4))

| class | loops Q | L1-const | L1-area | L2-const | L2-area | L3-const | L3-area | L3p-const | L3p-area | L4-area |
|---|---|---|---|---|---|---|---|---|---|---|
| (1, 0, 16) | 1 192 193 193 | -205 | -61.975 | -103 | -22.112 | -2.869 | -2.070 | -2668 | -197 | -7.282 |
| (1, 1, 16) | 3 64 67 67 | -20.338 | -8.307 | -13.218 | -4.355 | -1.017 | -0.773 | -32.629 | -7.659 | -2.027 |
| (2, 0, 8) | 4 48 52 52 | -8.728 | -3.975 | -6.211 | -2.386 | -0.648 | -0.504 | -10.226 | -3.196 | -1.348 |
| (1, 7, 16) | 4 49 49 57 | -8.728 | -3.975 | -6.211 | -2.386 | -0.653 | -0.506 | -10.226 | -3.196 | -1.348 |
| (1, 2, 16) | 7 28 31 39 | -1.125 | -0.662 | -0.978 | -0.531 | -0.186 | -0.150 | -0.987 | -0.499 | -0.340 |
| (2, 2, 8) | 12 16 28 28 | -0.070 | -0.055 | -0.080 | -0.067 | -0.010 | -0.012 | -0.054 | -0.037 | -0.019 |
| (1, 6, 16) | 12 19 19 43 | -0.070 | -0.055 | -0.066 | -0.051 | -0.006 | -0.009 | -0.047 | -0.031 | -0.006 |
| (1, 3, 16) | 13 16 21 37 | -0.039 | -0.032 | -0.046 | -0.041 | -0.003 | -0.006 | -0.026 | -0.018 | -0.011 |
| (4, 0, 4) | 16 16 16 48 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

**A = 60** — predicted ln τ_face (c(A) fitted on the published values)

| class | loops Q | L1-const | L1-area | L2-const | L2-area | L3-const | L3-area | L3p-const | L3p-area | L4-area |
|---|---|---|---|---|---|---|---|---|---|---|
| (1, 0, 20) | 1 300 301 301 | -192 | -64.985 | -90.826 | -15.180 | 8.806 | 9.340 | -2655 | -234 | 3.262 |
| (1, 1, 20) | 3 100 103 103 | -7.855 | 2.100 | -0.751 | 7.017 | 10.885 | 11.087 | -20.204 | 2.820 | 9.831 |
| (1, 9, 20) | 4 75 79 79 | 3.756 | 7.515 | 6.257 | 9.478 | 11.353 | 11.490 | 2.200 | 8.401 | 10.682 |
| (2, 0, 10) | 4 76 76 84 | 3.756 | 7.515 | 6.257 | 9.478 | 11.356 | 11.492 | 2.200 | 8.402 | 10.682 |
| (1, 2, 20) | 7 43 48 52 | 11.358 | 11.655 | 11.490 | 11.798 | 12.066 | 12.108 | 11.445 | 11.789 | 11.956 |
| (1, 8, 20) | 12 25 37 37 | 12.413 | 12.414 | 12.409 | 12.409 | 12.411 | 12.420 | 12.410 | 12.413 | 12.421 |
| (2, 2, 10) | 12 28 28 52 | 12.413 | 12.414 | 12.410 | 12.411 | 12.421 | 12.424 | 12.410 | 12.414 | 12.423 |
| (1, 3, 20) | 13 25 28 48 | 12.444 | 12.443 | 12.443 | 12.442 | 12.442 | 12.446 | 12.443 | 12.443 | 12.441 |
| (1, 5, 20) | 16 19 31 39 | 12.483 | 12.483 | 12.482 | 12.481 | 12.481 | 12.480 | 12.482 | 12.481 | 12.482 |
| (1, 4, 20) | 16 21 25 49 | 12.483 | 12.483 | 12.486 | 12.487 | 12.484 | 12.483 | 12.485 | 12.485 | 12.482 |

**A = 72** — predicted ln τ_face (c(A) fitted on the published values)

| class | loops Q | L1-const | L1-area | L2-const | L2-area | L3-const | L3-area | L3p-const | L3p-area | L4-area |
|---|---|---|---|---|---|---|---|---|---|---|
| (1, 0, 24) | 1 432 433 433 | -190 | -77.985 | -88.340 | -18.229 | 10.833 | 10.836 | -2653 | -280 | 3.874 |
| (1, 1, 24) | 3 144 147 147 | -5.364 | 2.518 | 1.735 | 8.407 | 12.987 | 12.977 | -17.726 | 3.346 | 11.757 |
| (2, 0, 12) | 4 108 112 112 | 6.246 | 9.016 | 8.743 | 11.361 | 13.499 | 13.493 | 4.677 | 10.045 | 12.778 |
| (1, 11, 24) | 4 109 109 117 | 6.246 | 9.016 | 8.743 | 11.361 | 13.503 | 13.495 | 4.677 | 10.046 | 12.778 |
| (1, 2, 24) | 7 63 64 76 | 13.849 | 13.984 | 13.977 | 14.145 | 14.354 | 14.347 | 13.923 | 14.115 | 14.309 |
| (1, 7, 24) | 9 48 57 57 | 14.616 | 14.617 | 14.621 | 14.624 | 14.631 | 14.627 | 14.621 | 14.621 | 14.616 |
| (1, 8, 24) | 9 49 52 64 | 14.616 | 14.617 | 14.621 | 14.624 | 14.636 | 14.630 | 14.621 | 14.622 | 14.616 |
| (2, 2, 12) | 12 36 48 48 | 14.903 | 14.894 | 14.896 | 14.882 | 14.861 | 14.859 | 14.894 | 14.881 | 14.886 |
| (1, 10, 24) | 12 39 39 63 | 14.903 | 14.894 | 14.896 | 14.883 | 14.859 | 14.858 | 14.894 | 14.881 | 14.886 |
| (1, 3, 24) | 13 36 37 61 | 14.934 | 14.929 | 14.930 | 14.921 | 14.905 | 14.905 | 14.928 | 14.920 | 14.914 |
| (1, 6, 24) | 16 27 43 43 | 14.974 | 14.978 | 14.976 | 14.981 | 14.987 | 14.989 | 14.977 | 14.982 | 14.982 |
| (2, 4, 12) | 16 28 36 52 | 14.974 | 14.978 | 14.976 | 14.981 | 14.990 | 14.991 | 14.977 | 14.983 | 14.981 |
| (1, 5, 24) | 16 31 31 63 | 14.974 | 14.978 | 14.976 | 14.982 | 14.990 | 14.992 | 14.977 | 14.983 | 14.981 |
| (1, 9, 24) | 19 27 28 64 | 14.985 | 14.993 | 14.990 | 15.005 | 15.028 | 15.031 | 14.994 | 15.007 | 15.023 |
| (1, 4, 24) | 21 21 36 48 | 14.987 | 14.997 | 14.991 | 15.004 | 15.026 | 15.029 | 14.994 | 15.007 | 15.016 |

## Plan (fixed before the runs; `drive2.py`)

Lives: soup p = 0.4, one life per replica, first event (face death or transverse firewall; ties to the firewall),
settled lives and the cap censor, ln τ_face = ln(2E/F) ± 1/√F (tslab.stats). Caps are shorter than research/shape's
5 × 10⁵ (about one to two mean lives); on research/shape's own A = 60 raw data, censoring at 65,536 or 131,072
changes ln τ by ≤ 0.005 (within the subset's error), so the estimator is the same. Per area, jobs × 4,096 lives:
A = 48: 76 jobs at cap 16,384 for systole² 7–16 (target ± 0.002); A = 60: 50 jobs at cap 65,536 (target ± 0.0035);
systole² 3 and 4 and A = 72 extras as in `drive2.py`. Seeds new (BASE 1e6, 2e6, 3e6). No top-ups.
