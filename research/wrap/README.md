# The wrapping law under test

2026-11-15. The lead fitted an additive "wrapping law" to 32 wrapped faces (`research/audit/wrap_law_lead.py`,
forecasts W1–W6 in `PREDICTIONS.md`):

    ln τ_face = a + c·(A − 63) − (A − A0)·Σ_v k(|v|²),   k(12, 13, 16, 19) free, k(≥ 21) = 0,

one term per loop direction ±v of the face torus. This directory rebuilds it from the primary data, attacks it on the
data on file, and scores it on 18 faces measured here after the forecasts were committed (93540eb, 13:09 UTC; first
run 13:11 UTC). Marks: [proved], [measured], [fitted], [post hoc] (a form chosen after seeing data).

## Verdict

- **Inside its stated range (A ≥ 48) the law forecasts new faces to its own margin [measured].** All 11 new classes
  at A = 51–69 pass W1 (|forecast − measured| ≤ max(0.010, 3σ)); the largest miss is the single loop² 12 face at
  A = 66, −0.0122 ± 0.0048 (−2.5σ). Σ z² = 19.4 on 11 (p ≈ 0.05). `[[W2/W78 line]]`
- **But it is not the right form, and with all the precise data on file it does not fit [fitted].** On the 43 faces
  with A ≥ 48 (on file + new, research/shape3's cap-free values included) the law has χ² 97.9 on 36
  (p ≈ 10⁻⁷); leave-one-out Σ z² 176 on 43. It fails in three ways, each seen before the new runs and confirmed by
  them: (1) the discount of a loop is not linear in A with one common A0: it is convex, and its growth with A falls
  with the loop length (loop² 19 barely grows from 48 to 69 cells); (2) two short loops discount *less* than the sum
  of their single discounts (faces with ≥ 2 short directions lie +0.004 above the law, single ones −0.004 below);
  (3) the two loop² 12 classes at A = 72 lie 0.016 ± 0.003 below it (research/shape3 data the lead's fit did not use).
- **Below its range it fails outright [measured].** Forecast for the equilateral faces of 36 and 39 cells (three
  loops of 12, of 13): 7.4016 and 8.0356; measured 7.3643 ± 0.0023 and 8.0085 ± 0.0031 (−16σ, −9σ; 0.037 and
  0.027). A = 42 (loops 12, 13, 19) −0.0115 (−4.3σ); A = 45 (two loops of 13) passes. W5 (one more k for loop² 9
  and 7) fails by a factor 40 in χ²/dof.
- **W6 fails [measured]:** re-measured, the A = 60 loop² 12 pair differs by +0.0021 ± 0.0035 (on file −0.0077 ±
  0.0026); pooled −0.0042 ± 0.0021. No second effect at loop² > 20 is needed at that size.
- **A better description, found after the fact [post hoc]:** hazards add, not log-discounts. Each short loop direction
  opens a second way for the face to die, at a share of the bulk rate that grows like e^{g_q (A − 63)}:

      ln τ_face = a + c·(A − 63) − ln(1 + Σ_v r_q e^{g_q (A − 63)})        (HAZ, 10 parameters)

  On the 43 faces with A ≥ 48: χ² 44.2 on 33 (p 0.09), leave-one-out Σ z² 58, leave-one-area-out 62 (law: 176,
  175). Fitted on the faces on file only and committed (e2ed1c1, 13:17 UTC) before the runs at A ≥ 57 existed, it
  forecast those 10 faces with Σ z² 5.6 (the law: 8.3). It still misses A = 36 by −3σ and the (12, 16) face at
  A = 48 by +5σ, so it is a better summary, not a law.

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
  seven classes in the fit, at A = 48 (two), 60 (three) and 72 (two loop² 12, two loop² 16): errors 0.0013–0.0043
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

[[TABLE]]

## Scores (claims 3 and 4)

[[SCORES]]

## What is established (claim 5)

[[ESTABLISHED]]

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
