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

## Corrections after review (appended 2026-11-13T23:04Z, commit 3df47dd; `research/audit/REVIEW-gpu-pr8.md`)

Nothing above is edited; these restate two outcome lines.
- **A = 108 / 135 (first entry):** "above, by 0.39 nats (13σ) and 0.75 nats (3σ)" measured the distance from
  0.2077·A + 0.55, a quasi-stationary endpoint fit that already misses verified lifetimes by 0.08 nats at A = 45 and
  84. Against lifetimes: A = 108 is 0.21 ± 0.04 nats above the straight line through the verified A = 45–84 points;
  local slopes 0.201, 0.212, 0.212, 0.218, 0.221; curvature 2.6σ from GPU points alone, ≈ 5σ with the CPU points.
  The expectation in the lead's message (1.2e9, 3e11) was still missed on the high side.
- **τ(R = 40 v) "+21%":** the 7.1e7 in the lead's message pools soups with copies of the side-16 cube; the soup-only
  value on file is 8.2e7 ± 15%, which 8.63e7 matches. So the "±10% of the lead's values" sub-forecast missed only
  against the pooled number; against soups it held.

## 2026-11-13T23:14Z (commit 3b3ceb7) — the lead's experiments a, b, c (after review of PR 8); before any of the runs

Kernel B with settle detection (kind 2: period 1–2; kind 3: periods to 128, or to 1024 where said); settled lives are
censored out of every statistic and counted; lives alive at the end of a run are censored with their exposure.

**a. Do rim-free slab faces cost more per cell beyond A = 90?** Flat slabs, m = 8 layers, p = 0.4, near-square in-plane
tori (`vessels.SlabVessel`, the statistic of `research/peeling/face_law_fit.py`: ln τ_face = ln(2 × mean wait from
generation 0 to the first extinct outer layer); the CPU line is −0.091 + 0.2088·A for A = 27–90). Sizes: 6×6 (A = 108)
and 6×7 (A = 126). The line predicts ln τ_face = 22.46 and 26.22. **Forecast: on the line within ±0.15 at both**
(0.2088 per cell holds; the octahedral rise to 0.218–0.221 is a rim effect). Probability I give it: 0.6. The
alternative I would read as "the bulk constant rises": both points above the line by > 0.2, with the excess growing.
Octahedral A = 165 is not affordable (≈ 10⁶ GPU-seconds per death at the octahedral rate); not run.

**b. Does the cube-centred hazard really fall with age?** One long run, O_h cube-centred R = 43 (A = 759), 2,304
replicas (WB = 1, so each ages ≈ 2× faster), settle window 1,024, 3 hours: ages to ≈ 3 τ. **Forecast: the hazard is
flat beyond the first 0.05 τ — a Weibull fit to ages ≥ 0.05 τ gives a shape 0.95–1.05 — and τ = 3.25 × 10⁹ within
± 10%.** Probability 0.6; the alternative (k < 0.95 over the whole range) would mean young cube-centred soups die
faster and the side-17 mean is above 3.2 × 10¹⁰.

**c. Plateaus of cube-like seeds at vertex-centred R = 40.** 7,807 deterministic O_h seeds: closed cube 14 plus the
shell of side 16 minus 1, 2 or 3 shell orbits (`cubelike.py`); a 1,000-generation burst (fl.c, local) leaves 3,857
distinct lineages at exactly R = 40; each is followed through its plateau at 40, then (state kept at the peel) 38, then
36, with a cap of 12 τ. τ(40, 38, 36) = 8.63e7, 1.254e7, 2.247e6 (fresh soups, this directory). **Forecast: memoryless
at all three radii — mean T/τ within 1.00 ± 0.06 at 40 (± 0.08 at 38, 36), CV of uncensored waits within ± 0.05 of an
exponential's, P(> 4τ) 1.8% ± 0.6%, P(< 0.05τ) 4.9% ± 1%, KS below the 5% critical value.** I.e. cube-like lineages
do not reproduce the cubes' long plateaus (3 of 16 beyond 4τ) at R = 40 either. Probability 0.75.

## Outcome of experiment a (appended 2026-11-14T01:05Z)

`python3 research/gpu/facelaw.py summary "research/data/gpu_facelaw/slab*.json"` (A10G; slab 6×7 as two 60-min runs,
seeds 411–412, spawned through `jobs.py` after a worker restart lost the first attempt — nothing from it was kept).
**Rim-free slabs stay on the line — forecast held.** 6×6 (A = 108): ln τ_face = **22.470 ± 0.047** (447 peels;
line 22.46, +0.01); 6×7 (A = 126): **26.138 ± 0.091** (122 peels; line 26.22, −0.08). Cost per cell 0.2081, 0.2074;
local slope 108 → 126: 0.204 ± 0.006. No settling recorded (kinds 2, 3: 0). So the bulk constant does not rise to
A = 126; the octahedral faces' 0.218–0.221 is a rim effect (at A = 108 an octahedral face is 0.91 nats tougher than a
rim-free one). Caveat: ages ≤ 1.5 × 10⁹, ≈ 1/75 of the A = 126 mean; the estimate assumes the hazard stays flat beyond,
as at every size where it could be checked.

## Outcome of experiment b (appended 2026-11-14T03:15Z)

`python3 research/gpu/weibull.py research/data/gpu_facelaw/symcR43_s501_A10G.json` (A10G, 3 h, 2,304 replicas,
settle window 1,024; spawned through `jobs.py`, fetched through `relay_remote`). **The cube-centred death rate does
not fall with age — forecast held.** 5,971 deaths, ages to 2.6 τ, 1 settle: τ = **3.201 × 10⁹** (ln 21.887 ± 0.013;
the earlier run's 3.253 × 10⁹, 0.5σ). Censored Weibull shape: **1.020** (95% 1.000–1.041) over all ages, **1.030**
(1.002–1.059) over ages ≥ 0.05 τ (forecast 0.95–1.05). Hazard × τ by age, deaths / expected: 0.03–0.1 τ 0.99,
0.1–0.2 0.93, 0.2–0.3 1.03, 0.3–0.5 0.99, 0.5–0.75 0.99, 0.75–1 1.04, 1–1.5 1.00, 1.5–2 1.13, 2–3 1.02. The earlier
runs' falling hazards (k = 0.94 at R = 43, 0.84 at R = 45, re-derived here with the same numbers as the review) were
noise at R = 43; R = 45 was not re-run, so its k = 0.84 is untested, but nothing at R = 43 supports it. The side-17
mean (3.2 × 10¹⁰ from R = 45) stands as a long-run mean to the extent R = 43 is a guide.

## Correction to the outcome of experiment a (appended 2026-11-14T06:40Z, commit 3cfab59, after `research/audit/REVIEW-gpu-pr12.md`)

Nothing above is edited. The forecast's numbers held (+0.01 at A = 108, −0.08 at A = 126, ±0.15 allowed); **its reading
does not follow at A = 126.** The GPU statistic counts the first outer-layer extinction, and in an 8-layer slab a
transverse firewall also ends the chaos and is soon followed by a face death; the CPU line excludes sizes where
firewall-first exceeds 6%. At 6×7×8 (one cheapest transverse direction, cut 216) the review expects ≈ 25 of the 122
deaths (18–34; range to ≈ half) to follow a firewall, so 26.138 ± 0.091 is a lower bound on the face channel
(central corrected value ≈ 26.36; slope 108 → 126 ≈ 0.216, the octahedral value). Withdrawn: "local slope
108 → 126: 0.204 ± 0.006", "the bulk constant does not rise to A = 126", "a rim effect". What stands: through A = 108
rim-free slab faces stay on the line fitted to A = 27–90, and octahedral faces at A = 108 are 0.91 ± 0.06 nats
tougher; what makes them tougher (rim, eight faces sharing edges, interior thickness, shape) is not separated.
Experiment b's outcome line "the hazard is flat" means: flat to ±13% per bin from age 0, Weibull k = 1.02 (1.00–1.04).

## Before the firewall-resolved slab runs (appended 2026-11-14T06:42Z, commit 60846f8)

`fwslab.py`: kernel B with states kept at face deaths; every launch boundary and every face death tested for a
transverse 3-layer firewall (three cyclically consecutive dead layers of a transverse ring); a firewall ends the
life as kind 4; τ_face = 2E/(face deaths), τ_fw = E/(firewalls), exposure E from generation 0 (the convention of
`research/peeling/slab_fw.csv`). Local check with `fl.c` on 3×6×8: firewalls never disappear once seen; 58 of 512
firewall-first (the table: 74).
- **Validation, before the main run (must hold, else the main run is not interpreted):** 3×6×8 (cut 108, one cheapest
  direction): ln τ_face = 11.10 ± 0.1 and ln τ_fw = 12.18 ± 0.2 (slab_fw.csv: 438 peels, 74 firewalls); 4×7×8 (cut 144,
  one cheapest direction): ln τ_face = 17.43–17.51 ± 0.12 (slab_fw.csv 17.43; the review's independent CPU run 17.506
  ± 0.091) and ln τ_fw = 17.16 ± 0.2. Firewalls by direction: all in the cheapest one.
- **Main run, 6×7×8 (A = 126, cut 216 in one direction), two A10G-hours: forecast** firewall-first share **10–30%**
  of first events (the lead's 15–35%); face channel **ln τ_face(126) = 26.30 ± 0.15**, i.e. local slope 108 → 126 in
  0.205–0.222 (the lead's 0.210–0.222); ln τ_fw(216) = 27.0 ± 0.4 (the review's extrapolation 27.05 ± 0.30). I give a
  slope below 0.2088 + 0.006 (the slab line holding) probability 0.35, and one at or above the octahedral 0.216
  probability 0.4.

## 2026-11-14T07:51Z — control: square slab 6×6×8 with the firewall channel resolved (before the run)

`fwslab.py`, 6×6×8 (A = 108; cheapest transverse cut 216 in **three** directions), 15 A10G-minutes, seed 621.
The committed 22.470 ± 0.047 (first outer-layer extinction, no firewall screening) should be nearly unchanged:
**forecast** firewall-first share **0.5–4%** of first events (the review expects ≈ 7 of 447, 1.6%), spread over all
three cheapest directions; face channel **ln τ_face(108) = 22.49 ± 0.07** (on the slab line 22.46 within 0.1); first-event
statistic within 0.05 of 22.470. If the face channel at 108 lands on the line while 126 stays at 26.405, the slope
108 → 126 (≈ 0.219) mixes a square and a non-square slab (the review's caution); I will say so rather than read it as
the bulk constant rising.

## 2026-11-14T07:51Z — outcome of the firewall-resolved runs (forecast: commit 60846f8)

`python3 research/gpu/fwslab.py summary "research/data/gpu_facelaw/fwslab*.json"` (per-life data — age, kind, birth,
firewall direction — in each file's `raw`). Exposure from generation 0; settled lives (period 1–2, kind 2; period
3–128, kind 3) censored at detection; periods > 128 are not detected (none was ever seen); lives open at the end censored.
- **Validation — both hold, so the production run is interpreted.** 3×6×8 (cut 108): ln τ_face = 11.084 ± 0.001
  (target 11.10 ± 0.1), ln τ_fw = 12.327 ± 0.002 (12.18 ± 0.2); 12.6% firewall-first (table: 74/512 = 14.5%); 1,127
  settled. 4×7×8 (cut 144): ln τ_face = 17.465 ± 0.005 (17.43–17.51), ln τ_fw = 17.106 ± 0.006 (17.16 ± 0.2); first-event
  statistic 16.925 (the review's independent CPU 16.934 ± 0.068); 41.7% firewall-first; 11 settled. Firewalls in the
  cheapest direction: 276,540 of 276,769 and 32,817 of 32,840.
- **6×7×8 (A = 126, cut 216 in one direction), two 60-min runs, seeds 611–612 — all three forecasts hit.**
  Exposure 1.349 × 10¹³; first events: 92 face deaths, **29 transverse firewalls (24.0%; forecast 10–30%)**, all on
  diagonal 2 (the cut-216 ring); 0 settled; 9,216 open at the end. **ln τ_face = 26.405 ± 0.104** (forecast 26.30 ±
  0.15; slab line 26.218: +0.19, 1.8σ); **ln τ_fw(216) = 26.866 ± 0.186** (forecast 27.0 ± 0.4; the review's
  extrapolation 27.05 ± 0.30); first-event statistic 26.131 (the earlier unscreened runs: 26.138). Slope 108 → 126 with
  the committed (unscreened) 22.470: 0.219 ± 0.006 — at or above the octahedral 0.216, the case I gave 0.4. Interior
  {111} firewalls are not a channel here (they split the slab; its faces live on and are still counted).
