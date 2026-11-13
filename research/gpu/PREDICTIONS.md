# Timestamped predictions (append-only)

Format as in `research/fluct/PREDICTIONS.md`: written before the run that resolves it finishes; outcomes appended
below, never edited in.

## 2026-11-13T18:05Z — record of an earlier expectation (asymmetric faces, A = 108 and 135)

This file did not exist when these ran; recorded for completeness, not as a forecast of mine. The lead's message
(queued 14:31Z, read by this session only at 17:54Z) gave the expectation **first-peel mean ≈ 1.2e9 at R = 15
(A = 108) and ≈ 3e11 at R = 17 (A = 135)**, from ln τ_face = 0.2077 A + 0.55 with eight faces. The runs started
15:05Z (R = 15) and 15:42Z / 16:35Z (R = 17), after that message was queued.
**Outcome:** 1.774e9 ± 0.055e9 (1,059 peels) and 6.9e11 ± 1.7e11 (16 peels): both above, by 0.39 nats (13σ) and
0.75 nats (3σ). Details in `README.md`.

## 2026-11-13T18:05Z — symmetric law at A = 759 and 828 (O_h soups, p = 0.35, T0 = 1000, mean residence τ)

Before any run at these sizes. Inputs: the lead's forecasts on file (`research/fluct/PREDICTIONS.md`, side-17 entry;
`research/fluct/sym_fit.py`) and the vertex/cube factor ≈ 1.5 (A = 360–630) to 2.0 ± 0.4 (A = 693).
- cube-centred R = 43 (A = 759, 1,078 orbits): **ln τ = 21.8 ± 0.2** (the lead's 21.6–22.0).
- cube-centred R = 45 (A = 828, 1,222 orbits): the lead's **ln τ = 24.0 ± 0.4**. My own lean, from the asymmetric
  faces curving upward (`README.md`): the upper half, **ln τ = 24.2 ± 0.4**.
- vertex-centred R = 44 (A = 759, 1,078 orbits): cube-centred value + ln(1.5 … 2.0): **ln τ = 22.3 ± 0.4**.

## 2026-11-13T18:05Z — are single lineages memoryless? (O_h vertex-centred R = 36, 38, 40)

Before the runs. Fresh O_h soups, T0 = 1000, residence = age at the face death − T0, complete lives only (born at
least 10 τ before the end of the run). Exponential expectations: CV = 1, P(> 4τ) = e⁻⁴ = 0.0183,
P(< 0.05τ) = 1 − e^(−0.05) = 0.0488, hazard flat in age. **My forecast: all three consistent with exponential**
(CV within ±0.03 of 1, both fractions within 2σ of the exponential values, hazard flat beyond the first ~1,000
generations after T0), τ = 2.2e6, 1.2e7, 7.1e7 (lead's values) within ±10%. I.e. fresh-soup lineages are
memoryless, and the cubes' over-dispersion (OPEN-PROBLEMS 6) is not a property of single soup lineages at these sizes.
