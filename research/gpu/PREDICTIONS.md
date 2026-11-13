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

## Outcomes (appended 2026-11-13T19:10Z)

Commands: `modal run research/gpu/modal_app.py::facelaw --r R --centre c|v --sym --minutes M --seed S` (A10G);
`python3 research/gpu/facelaw.py summary "research/data/gpu_facelaw/sym*.json"`; kernel with settle detection to
period 128 (kind 3).
- **Symmetric law — all three inside the forecasts.** cube-centred R = 43 (A = 759): **ln τ = 21.903 ± 0.031**
  (1,057 deaths; forecast 21.8 ± 0.2). cube-centred R = 45 (A = 828): **ln τ = 24.175 ± 0.072** (192 deaths; the
  lead's 24.0 ± 0.4, my 24.2 ± 0.4) — so the side-17 first-plateau mean is **3.2 × 10¹⁰** (68%: 2.9–3.4 × 10¹⁰),
  inside the lead's 1.8–4.0 × 10¹⁰. vertex-centred R = 44 (A = 759): **ln τ = 22.409 ± 0.040** (637 deaths; forecast
  22.3 ± 0.4); vertex/cube factor at A = 759: e^(0.506 ± 0.05) = 1.66.
- **Lineages — memoryless, as forecast**, but one τ missed the ±10% band: vertex R = 36, 38, 40: τ = 2.247e6,
  1.254e7, **8.63e7** (± 0.3–0.5%; the lead's 2.2e6, 1.2e7, 7.1e7: +2%, +4%, **+21%**). Complete lives (10 τ window;
  5 τ at R = 40): CV 0.998 / 1.002 / 0.966 (exponential 0.9996 / 0.9996 / 0.972); P(> 4τ) 0.0179 / 0.0189 / 0.0169
  (0.0183); P(< 0.05τ) 0.0495 / 0.0482 / 0.0480 (0.0488); hazard flat to 10 τ. (Before settle detection reached period
  128, R = 36 read CV 1.012 and a hazard of 0.61 at 6–10 τ: stuck replicas, the lead's caveat.)

## Corrections after review (appended 2026-11-13T23:20Z; `research/audit/REVIEW-gpu-pr8.md`)

Nothing above is edited; these restate two outcome lines.
- **A = 108 / 135 (first entry):** "above, by 0.39 nats (13σ) and 0.75 nats (3σ)" measured the distance from
  0.2077·A + 0.55, a quasi-stationary endpoint fit that already misses verified lifetimes by 0.08 nats at A = 45 and
  84. Against lifetimes: A = 108 is 0.21 ± 0.04 nats above the straight line through the verified A = 45–84 points;
  local slopes 0.201, 0.212, 0.212, 0.218, 0.221; curvature 2.6σ from GPU points alone, ≈ 5σ with the CPU points.
  The expectation in the lead's message (1.2e9, 3e11) was still missed on the high side.
- **τ(R = 40 v) "+21%":** the 7.1e7 in the lead's message pools soups with copies of the side-16 cube; the soup-only
  value on file is 8.2e7 ± 15%, which 8.63e7 matches. So the "±10% of the lead's values" sub-forecast missed only
  against the pooled number; against soups it held.
