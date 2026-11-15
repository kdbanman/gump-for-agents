# The wrapping law under test

2026-11-15. The lead fitted an additive "wrapping law" to 32 wrapped faces (`research/audit/wrap_law_lead.py`,
forecasts W1–W6 in `PREDICTIONS.md`):

    ln τ_face = a + c·(A − 63) − (A − A0)·Σ_v k(|v|²),   k(12, 13, 16, 19) free, k(≥ 21) = 0,

one term per loop direction ±v of the face torus. This directory rebuilds it from the primary data, attacks it on the
data on file, and scores it on 20 new face classes (plus a re-measured pair and a calibration) measured here after the forecasts were
committed (93540eb, 13:09 UTC; first
run 13:11 UTC). Marks: [proved], [measured], [fitted], [post hoc] (a form chosen after seeing data).

## Verdict

- **Inside its stated range (A ≥ 48) the law forecasts new faces to its own margin [measured].** All 11 new classes
  at A = 51–69 pass W1 (|forecast − measured| ≤ max(0.010, 3σ)); the largest miss is the single loop² 12 face at
  A = 66, −0.0122 ± 0.0048 (−2.5σ). Σ z² = 19.4 on 11 (p ≈ 0.05). The two new faces with no loop² ≤ 20 (A = 75, 78) lie on the no-short-loop
  line within 1.5σ (W2 passes).
- **But it is not the right form, and with all the precise data on file it does not fit [fitted].** On the 48 faces
  with A ≥ 48 (on file + new, research/shape3's cap-free values included) the law has χ² 111.6 on 41
  (p ≈ 10⁻⁸); leave-one-out Σ z² 195 on 48. Just outside W1's areas, the single loop² 12 face at A = 78 misses its
  forecast by −0.033 ± 0.009 (−3.6σ; outside W1's margin, inside twice it). It fails in three ways, each seen before the new runs and confirmed by
  them: (1) the discount of a loop is not linear in A with one common A0: it is convex, and its growth with A falls
  with the loop length (in the rate form below, g = 0.036, 0.032, 0.025, 0.019 ± 0.008 per cell for loop² 12, 13,
  16, 19); (2) two short loops discount *less* than the sum
  of their single discounts (faces with ≥ 2 short directions lie +0.004 above the law, single ones −0.004 below);
  (3) the single loop² 12 faces fall further and further below it as A grows: 0.016 ± 0.003 at A = 72
  (research/shape3 data the lead's fit did not use), 0.033 ± 0.009 at A = 78 (new).
- **Below its range it fails outright [measured].** Forecast for the equilateral faces of 36 and 39 cells (three
  loops of 12, of 13): 7.4016 and 8.0356; measured 7.3643 ± 0.0023 and 8.0085 ± 0.0031 (−16σ, −9σ; 0.037 and
  0.027). A = 42 (loops 12, 13, 19) −0.0115 (−4.3σ); A = 45 (two loops of 13) passes. W5 (one more k for loop² 9
  and 7) fails: χ²/dof 63, where it asked for < 2.
- **W6 fails [measured]:** re-measured, the A = 60 loop² 12 pair differs by +0.0021 ± 0.0035 (on file −0.0077 ±
  0.0026); pooled −0.0042 ± 0.0021. No second effect at loop² > 20 is needed at that size.
- **A better description, found after the fact [post hoc]:** hazards add, not log-discounts. Each short loop direction
  opens a second way for the face to die, at a share of the bulk rate that grows like e^{g_q (A − 63)}:

      ln τ_face = a + c·(A − 63) − ln(1 + Σ_v r_q e^{g_q (A − 63)})        (HAZ, 10 parameters)

  On the 48 faces with A ≥ 48: χ² 49.6 on 38 (p 0.10), leave-one-out Σ z² 62, leave-one-area-out 66 (law: 195,
  203), no residual beyond 2.4σ. Fitted on the faces on file only, in the form committed (e2ed1c1, 13:17 UTC) before
  any run at A ≥ 57 existed, it forecast those 15 faces with Σ z² 10.3 (the law refitted the same way: 22.5),
  including the A = 78 loop² 12 face (+0.5σ). Below the range it fails too (A = 36: −5.8σ blind, −3.2σ fitted), so
  it is a better summary of A ≥ 48, not a law.

## The rebuild (claim 1 of the brief)

Own lattice code (`lattices.py`: HNF lattices, reduced Gram triple, loop lists), own loader from the primary files
(`faces.py`: the card's CSVs, the fwslab JSONs, research/shape and research/shape2 CSVs, research/shape3's
`runs.csv`), own weighted fit (`fit.py`).

    python3 research/wrap/fit.py lead          # → data/fit_onfile_out.txt, first block
    python3 research/wrap/loopcheck.py         # lead's loop counting vs mine on 1,099 lattices: 0 differ

- The lead's table and parameters are reproduced to every printed digit (χ² 41.7 here against 42.0: the lead pooled
  the two 6 × 7 runs by summed counts, I by inverse variance). Loop counts are right [checked on every lattice of
  A = 36–126 with loop² ≥ 7].
- **Data the fit did not use:** research/shape3's cap-free values (events every 8 generations, 512 replicas) for
  ten classes in the fit, at A = 48 (two), 60 (three) and 72 (two loop² 12, three loop² 16): errors 0.0013–0.0043
  where the census values used have 0.002–0.014. With them, and with the stamping bias removed, the law's χ² on the
  same 32 classes is **86.3 on 25** (p ≈ 10⁻⁸; `python3 research/wrap/fit.py all --corr --onfile`).
- **Stamping bias:** rep.c (research/shape, research/shape2) books lives in 16-generation windows; the review measured
  +0.00167 at 4 × 4 on the same lives (REVIEW-gpu-local-tori, section 2). `faces.py --corr` subtracts 17 / (mean
  life) from rep.c rows (0.0017 at A = 48, ≤ 0.00014 at A ≥ 60) and 3.5 / (mean life) from shape3 rows. It moves χ²
  by 8 and no parameter by more than its error: not what breaks the law.
- **Firewalls:** the GPU slab driver books a firewall at its detection (up to one launch later) or at the face death
  that follows it; this inflates ln τ for firewall-prone rectangles (4 × 7, 4 × 8, 4 × 9, 5 × 8; estimated
  negligible at A ≥ 84 by the review of PR 14). Not corrected; these faces carry errors 0.005–0.07.
- The lead's check "fitted without the small equilateral faces it forecasts the 57-cell face to 0.001 and the 4 × 4
  to about 0.01" is right: +0.0009 and −0.0087 ± 0.0021 (`python3 research/wrap/eqout.py`). The 4 × 4 miss is 4σ.

## Attacks on the data on file (claim 2)

`python3 research/wrap/attack.py --corr` → `data/attack_onfile_out.txt`; `python3 research/wrap/models.py --onfile`
→ `data/models_onfile_out.txt`.

- **Forms with no more parameters do worse:** a discount per cell with no offset (A0 = 0) χ² 314 on 26; an offset per
  loop length plus one per-cell term 529 on 25 (on the 32 classes with shape3, corrected). A free line per loop
  length (own A0 for each, 10 parameters) 36.8 on 22: the common A0 costs Δχ² 50 for 3 parameters. Its own A0's are
  28 (loop² 12), 23 (13), 19 (16) — the lines do not meet.
- **Leave-one-out:** on the lead's own data Σ z² = 91 (on 32), leave-one-area-out 118; the 4 × 4 is forecast −5.3σ
  (−7.6σ with A = 48 left out). Seven parameters are not too many for 32 faces, but the A = 48 faces are not
  forecast from the rest: the form is wrong at small A, which the new faces then confirmed.
- **Equal-area pairs (SH2, SH4, SH6), frozen law:** A = 48 (12,16) − (12,19,19): measured −0.0143 ± 0.0016, law
  −0.0181 (+2.4σ, the pair is sub-additive); 4 × 4 − (12,19,19): −0.0140 vs −0.0124 (−1.3σ); A = 60 (16,19) − 4 × 5:
  −0.0130 vs −0.0131; the A = 72 triple and pair: law 0, measured +0.006 ± 0.003, 0.000, −0.002. So the law
  *explains* SH2 and SH6 — the "second variable" at loop² ≥ 12 is mostly the second and third loops being ≤ 19 —
  to about 2σ per pair. It says nothing about SH7 (loop² 9), where W5 fails.
- **Against the refuted candidates:** SH9's K2 (Σ e^{−1.41|v|}, amplitude ∝ A) is the A0 = 0 form with an exponential
  k. Its ratios k(13)/k(12) = 0.82 and k(16)/k(12) = 0.47 match the fitted 0.78 and 0.46; it fails on k(19)/k(12)
  (0.28 against 0.12) and on the offset (A0 = 0 costs Δχ² ≈ 120). The new law would have passed SH9's loop² ≥ 12 test
  (it forecasts 0 at A = 72, as measured) and fails its loop² 9 test like every candidate.

## New faces (claim 3)

Stepper: research/shape3's `ts3.c` (AVX-512 carry-save kernel; renewal lives from a 0.4 soup, no cap, no burn-in;
settled lives censored at the start of their cycle; transverse firewalls censoring), run here with **events every
generation** (K = 1), 512 replicas per job, two jobs (seeds) per torus. ln τ_face = ln(2E/F) ± 1/√F as the card's
equilateral rows. Validation (`validate.py`, `bash validate_all.sh` → `data/validate.log`): for every torus run,
the vessel file is decoded and its faces and transverse layers re-derived from coordinates; a soup tiled into the
cubic N-torus runs in `reference/oracle.py` and must equal, **as a set of cells at every one of 1,500
generations**, a numpy stepper on ts3's neighbour graph, and ts3 itself (W = 8, the production path) must give the
same population at every generation: MATCH on all 22 tori; a swapped neighbour entry fails at generation 4.
Calibration: 4 × 4 measured here 9.9229 ± 0.0014 against the card's 9.9251 ± 0.0004 (−1.5σ).

    python3 research/wrap/run.py plan 0; python3 research/wrap/run.py plan 1     # (about 1 core-hour each)
    python3 research/wrap/run.py job 1 6 26 110000000 158001  (etc., see data/runs.csv for every job)
    python3 research/wrap/run.py table; python3 research/wrap/score.py           # → data/score_out.txt

ln τ_face per class; σ is the statistical error (1/√F); z for mine and HAZ includes the forecast's own error.
Verdicts in brackets are outside W1's areas (51–69, excluding 60, which was in the fit). Two jobs per torus except
A = 75 (1,3,25), (1,9,25) and A = 78 (one job each, ± 0.009–0.012). Seed χ² (`run.py table`): one torus is
out of line, (1,4,25), 8.0 on 1 (15.680 ± 0.014 against 15.623 ± 0.014; no settled or unusually old life in
either job's event file; reported as measured). Hazard in three age bins of equal exposure (`data/hazard_out.txt`):
within 3σ of flat; the youngest third reads 0.010–0.011 lower at A = 36 and 51 (the soup's transient; the card's
rows use the same no-burn-in convention).

| A | HNF | loops² ≤ 20 | measured | frozen law | (m − f)/σ | W1 margin | verdict | mine (OFF2) | z | HAZ, fit on file | z |
|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| 36 | (2, 2, 6) | 12, 12, 12 | 7.3643 ± 0.0023 | 7.4016 | -16.4 | 0.0100 | (refutes) | 7.4452 | -11.3 | 7.3875 | -5.8 |
| 39 | (1, 3, 13) | 13, 13, 13 | 8.0085 ± 0.0031 | 8.0356 | -8.6 | 0.0100 | (refutes) | 8.0403 | -2.7 | 8.0201 | -1.5 |
| 42 | (1, 3, 14) | 12, 13, 19 | 8.6561 ± 0.0026 | 8.6676 | -4.3 | 0.0100 | (miss) | 8.6751 | -4.4 | 8.6634 | -2.0 |
| 45 | (1, 3, 15) | 13, 13 | 9.2986 ± 0.0023 | 9.3002 | -0.7 | 0.0100 | (pass) | 9.3012 | -0.5 | 9.2973 | +0.3 |
| 48 | (4, 0, 4) calibration | 16, 16, 16 | 9.9229 ± 0.0014 | 9.9253 | -1.7 | 0.0100 | (pass) | — | — | 9.9251 | -1.5 |
| 51 | (1, 3, 17) | 13, 19 | 10.5838 ± 0.0028 | 10.5821 | +0.6 | 0.0100 | pass | 10.5800 | +1.2 | 10.5813 | +0.7 |
| 54 | (1, 4, 18) | 12 | 11.1935 ± 0.0030 | 11.1899 | +1.2 | 0.0100 | pass | 11.1909 | +0.8 | 11.1926 | +0.3 |
| 54 | (1, 3, 18) | 13, 19 | 11.2047 ± 0.0030 | 11.2001 | +1.6 | 0.0100 | pass | 11.1981 | +1.9 | 11.2005 | +1.2 |
| 57 | (1, 3, 19) | 13 | 11.8283 ± 0.0030 | 11.8301 | -0.6 | 0.0100 | pass | 11.8282 | +0.0 | 11.8301 | -0.5 |
| 60 | (1, 8, 20) | 12 | 12.4230 ± 0.0025 | 12.4240 | -0.4 | 0.0100 | (pass) | 12.4203 | +1.0 | 12.4237 | -0.3 |
| 60 | (2, 2, 10) | 12 | 12.4210 ± 0.0025 | 12.4240 | -1.2 | 0.0100 | (pass) | 12.4203 | +0.2 | 12.4237 | -1.0 |
| 63 | (1, 3, 21) | 13 | 13.0616 ± 0.0038 | 13.0681 | -1.7 | 0.0114 | pass | 13.0649 | -0.7 | 13.0665 | -1.0 |
| 63 | (1, 8, 21) | 19, 19 | 13.1402 ± 0.0039 | 13.1347 | +1.4 | 0.0118 | pass | 13.1374 | +0.7 | 13.1357 | +1.1 |
| 66 | (1, 5, 22) | 12 | 13.6459 ± 0.0048 | 13.6581 | -2.5 | 0.0144 | pass | 13.6497 | -0.8 | 13.6505 | -0.9 |
| 66 | (1, 3, 22) | 13 | 13.6832 ± 0.0049 | 13.6871 | -0.8 | 0.0146 | pass | 13.6833 | -0.0 | 13.6836 | -0.1 |
| 66 | (1, 4, 22) | 19 | 13.7710 ± 0.0051 | 13.7736 | -0.5 | 0.0153 | pass | 13.7755 | -0.9 | 13.7740 | -0.6 |
| 69 | (1, 3, 23) | 13 | 14.2996 ± 0.0049 | 14.3061 | -1.3 | 0.0147 | pass | 14.3016 | -0.3 | 14.3000 | -0.1 |
| 69 | (1, 4, 23) | 19 | 14.3940 ± 0.0051 | 14.3984 | -0.9 | 0.0154 | pass | 14.4009 | -1.3 | 14.3991 | -0.9 |
| 75 | (1, 3, 25) | 13 | 15.5363 ± 0.0104 | 15.5440 | -0.7 | 0.0313 | (pass) | 15.5383 | -0.2 | 15.5303 | +0.5 |
| 75 | (1, 9, 25) | 19 | 15.6575 ± 0.0106 | 15.6479 | +0.9 | 0.0318 | (pass) | 15.6518 | +0.5 | 15.6492 | +0.8 |
| 75 | (1, 4, 25) | — | 15.6515 ± 0.0098 | 15.6661 | -1.5 | 0.0293 | (pass) | 15.6656 | -1.4 | 15.6657 | -1.4 |
| 78 | (1, 6, 26) | 12 | 16.0932 ± 0.0093 | 16.1263 | -3.6 | 0.0279 | (miss) | 16.1085 | -1.6 | 16.0878 | +0.5 |
| 78 | (1, 4, 26) | — | 16.2769 ± 0.0120 | 16.2919 | -1.3 | 0.0359 | (pass) | 16.2913 | -1.2 | 16.2917 | -1.2 |


## Scores (claims 3 and 4)

`python3 research/wrap/score.py` → `data/score_out.txt`.

| forecast | outcome | evidence |
|---|---|---|
| **W1** new faces at A = 51–69 within max(0.010, 3σ) | **passes**: 11 of 11 | largest −2.5σ (A = 66, loop² 12); Σ z² 19.4 on 11 |
| **W2** faces with every loop² ≥ 21 within max(0.006, 3σ) of the line | **passes** (2 faces, ± 0.010–0.012 only) | A = 75: −0.0146 ± 0.0098; A = 78: −0.0150 ± 0.0120 |
| **W3** free k(21) < 0.00008 with the new faces | **passes as worded, by a hair; the tail is form-dependent** | law form, A ≥ 48: k(21) = 0.000079 ± 0.000016 (5σ from 0); with k(25) also free k(21) = 0.00016, k(25) = 0.00008, Δχ² 23. In the HAZ form a constant share for loop² 21 is −0.0013 ± 0.0010: no tail (`data/tail_out.txt`) |
| **W4** residuals with ≥ 2 short directions no larger than with one | **passes as worded; the signs differ** | new faces, frozen law: one direction (8) rms 0.0060, mean −0.0043; two or more (3) rms 0.0043, mean +0.0040; difference of means 0.008 ± 0.003 |
| **W5** one more k for loop² 9 (and 7), same A0, χ²/dof < 2 | **fails** | χ²/dof 63 (with k(9)), 70 (with k(7)); residuals ± 15σ of both signs |
| **W6** the A = 60 loop² 12 pair still differs by > 0.004 | **fails** | here +0.0021 ± 0.0035; on file −0.0077 ± 0.0026; pooled −0.0042 ± 0.0021 |
| X1 (mine) A = 66 loop² 12 below the frozen law by more than W1's margin | fails (below, −2.5σ, but inside the margin) | 13.6459 ± 0.0048 against 13.6581 |
| X2 (mine) OFF2 forecasts at least as well as the frozen law on W1's faces | passes | Σ z² 9.8 against 19.4 (11 faces) |
| X3 (mine) A = 36 above the frozen law by > 0.02 | **fails, the other way**: 0.037 *below* | 7.3643 ± 0.0023 against 7.4016 (mine 7.4452) |
| X4 (mine) the A = 60 pair differs by < 0.004 | passes | +0.0021 ± 0.0035 |

Below the law's range (A = 36–45, scored for the form only): the frozen law is −16σ, −9σ, −4σ and −0.7σ off; the
discount it misses grows with the number of short directions and falls with A. At A = 36 the face with three loops
of 12 (7.3643) dies *sooner* than the two loop² 9 faces of the same area on file (7.4099, 7.3874): the ordering by
shortest loop inverts when a face has several short directions.

## What is established (claim 5)

All on A ≥ 48 and loop² ≥ 12; errors are statistical, not scaled by √(χ²/dof).

- **[measured] Short loops shorten a face's life, and the effect ends between loop² 19 and 21.** Per direction, at
  63 cells: loop² 12 lowers ln τ_face by 0.125, 13 by 0.096, 16 by 0.054, 19 by 0.013, 21 by less than 0.001 (HAZ,
  ln(1 + r_q), A ≥ 48; a constant share for loop² 21, r_21 = −0.0013 ± 0.0010). The no-short-loop faces (63–126 cells, 14 faces) fit one line,
  price per cell **c = 0.2086 ± 0.0001** (0.20859–0.20864 in every form tried).
- **[fitted] The wrapping law's discounts** (A ≥ 48, everything): k(12) = 0.00314 ± 0.00008, k(13) = 0.00246 ±
  0.00007, k(16) = 0.00147 ± 0.00004, k(19) = 0.00036 ± 0.00001, A0 = 23.1 ± 0.9, c = 0.20859 ± 0.00007,
  a = 13.164 ± 0.0007, at χ² 111.6 on 41; the lead's frozen k(12) is 2.8σ below this (the shape3 values pull it up).
  As a tool, the frozen law forecasts faces of 48–78 cells to about ± 0.01 (worse for loop² 12 above 72 cells).
- **[post hoc] The better description (HAZ):** ln τ = a + c(A − 63) − ln(1 + Σ_v r_q e^{g_q (A − 63)}) with
  a = 13.162 ± 0.0007, c = 0.20861 ± 0.00008, r(12, 13, 16, 19) = 0.1329 ± 0.0013, 0.1005 ± 0.0018, 0.0550 ±
  0.0007, 0.0134 ± 0.0007 and g = 0.0355 ± 0.0011, 0.0316 ± 0.0020, 0.0247 ± 0.0010, 0.019 ± 0.008; χ² 49.6 on 38.
  Read literally: a short loop of length² q adds a second way to die whose price per cell is c − g_q = 0.173,
  0.177, 0.184, 0.190 (against 0.2086 for the bulk), and the ways add as rates. This predicts that a face with a
  loop² 12 eventually has slope 0.173 per cell; nothing on file reaches far enough to test it.
- **[measured] Additivity:** log-discounts are not additive (A = 48 (12,16) vs (12,19,19) +2.4σ; the new faces'
  sign pattern under W4); rates add better (HAZ against the same form with log-discounts adding, EXPA: χ² 49.6
  against 59.7 with equal parameters). Neither form holds below 48 cells.
- **Largest residuals.** In range, HAZ: the loop² 12 class (12, 0, 25) at A = 60, −2.4σ (it carries the W6
  discrepancy). The law: (12, 0, 16) at A = 48 +3.9σ, (12, 0, 36) at A = 72 −3.1σ, A = 78 loop² 12 −2.9σ. Out of
  range: A = 36 (three loops of 12), which no form tried here gets (HAZ −3.2σ in a fit that includes it).
- **What this does to the open questions.** The "kink near 61 cells" in the equilateral family is the end of the
  discount (loop² 19 at 57 cells, 21 at 63): confirmed in every form. The "second variable" of the shape studies at
  loop² ≥ 12 is, to about 2σ per pair, the second and third loops being ≤ 19; the A = 60 loop² 12 pair (W6) is no
  longer significant. Loop² 9 (SH7) remains unexplained.

## Not checked

- The census and slab values on file were not rerun here (except the 4 × 4 and the A = 60 pair); the 72-cell faces
  with only census values (loop² 13, 19, 21) carry ± 0.008–0.014.
- The firewall-detection convention of the GPU slab driver was not corrected (it matters only for the rectangles
  with a firewall channel).
- The bias model of `faces.py --corr` is scaled from one measured point (4 × 4); it changes nothing important.
- The post-hoc forms (EXPA, HAZ) were chosen after the A ≤ 54 runs; only their forecasts at A ≥ 57 are blind.
- ts3's event logic (face death, firewall, settled test) is the code reviewed in research/shape3; here only its
  dynamics were checked against the oracle, its event counts were not recomputed from snapshots.
- Faces of A = 75 and 78 other than those listed, and A > 78, were not run.
- Cut for time: A = 78 (1,3,26) and (1,7,26) (forecasts in `data/forecast_out.txt`) and every A > 78 were not run;
  the A = 75 and 78 faces have one job each (or two, (1,4,25)) at ± 0.009–0.012 instead of ± 0.005, so W2 rests on
  two faces at that precision.
- Event files (one line per life) are in `research/scratch/wrap/` (git-ignored); `data/runs.csv` keeps the counts.

## Files

`lattices.py` (classes, loops), `faces.py` (loader), `fit.py` (linear forms, LOO, forecasts), `models.py` (nonlinear
forms LAW, EXPA, HAZ), `attack.py`, `eqout.py`, `tail.py`, `additivity.py`, `loopcheck.py`, `validate.py` +
`validate_all.sh`, `run.py` (jobs, table), `hazard.py`, `score.py`; outputs in `data/*_out.txt`, per-job counts in
`data/runs.csv`, validation log `data/validate.log`.
