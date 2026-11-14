# Review of research/constant/ (is there one cost per cell c_inf?)

Adversarial review, 2026-11-14. Subject: `research/constant/README.md`, `PREDICTIONS.md`, `fit.py`, `load.py`,
`shape_models.py`, `out/main_table.txt` (commits 5dd18b9, 1f6a8c9, 2e06618). I read their code to look for errors;
every number below comes from my own scripts under `research/audit/constant/`, which use none of theirs:

    python3 research/audit/constant/data.py        # own loader + point-by-point comparison  -> out_data.txt
    python3 research/audit/constant/fits.py        # own WLS: claims 2-5                       -> out_fits.txt   (2 s)
    python3 research/audit/constant/extra.py       # 1-dof penalties, forms not tried, claim 6, claim 8 -> out_extra.txt
    python3 research/audit/constant/forecasts.py   # claim 7                                   -> out_forecasts.txt

No simulation was run.

## Verdicts

| # | claim | verdict | theirs | mine |
|---|---|---|---|---|
| 1 | points equal the tracked data; 3×6×8 runs disagree at 3.5σ | **stands** | 64 points | all 64 reproduced to 1e-4 (one at +0.0003); 3×6×8 11.0845 ± 0.0007 vs 11.0813 ± 0.0005, 3.5σ |
| 2 | periodic c = 0.2085 ± 0.0035 (models) ± 0.001 (stat) | **stands with corrections** | 0.205–0.212 | 0.207–0.213, but ± 0.003 stat. once the width law is not assumed |
| 3 | hull c = 0.2226 ± 0.0010 (log) or 0.2317 ± 0.0019 (rim) | **stands with corrections** | 0.2226–0.2317 | reproduced; other one-term forms fit as well and give 0.218–0.219; a saturating form fits all six sizes with 0.2156 |
| 4 | tension ≥ +0.0109 ± 0.0010; Δχ² 110–238; one c only with two hull terms, p ≈ 0.01 | **does not stand** | ≥ 10σ | 1.7σ to 15σ depending on forms; single-c fits with p > 0.05 exist (one hull term and ordinary parameters) |
| 5 | wrap-around laws fail; ξ = 0.71–0.74; κ = −1.01 ± 0.01 | **failures and ξ stand; κ does not** | κ = −1.01 ± 0.01 | κ = −1.0 ± 0.3 (jackknife); −0.72, −1.18, −1.43 at A = 48, 60, 72 |
| 6 | out-of-sample table | **stands** | | every entry reproduced (one: 1.4/2 against 1.3/2) |
| 7 | forecasts committed before their data | **(A) stands; (B) the "blind" list is overstated** | | P3, T01, T12, N72 rows were in the tree when B was committed |
| 8 | three measurements | **(1) useful, for a reason the write-up does not give; (2) useful if the corners are controlled; (3) does not decide** | | better: equal-area hexagonal hull faces; drop (3) |

## 1. The data points — stands

`data.py` reads the raw exposure and death counts (fwslab*.json, shape/A60/A72.csv, shape2/A48/A60/A72x.csv,
fluct qsd_summary.json, R*_A10G.json, sym_residence.csv, sym*_A10G.json). It pools tori by the theta series of the
period lattice, computed by brute force (for rank-2 lattices the theta series fixes the isometry class), not by Gauss
reduction. I checked the metric Q = x² + xy + y² against research/shape/lattice.py's translations u1 = (1,0,−1),
u2 = (0,1,−1) (60°). Result: the same 42 periodic classes with Q1 ≥ 3, and every ln τ, error and death count
identical to `out/points.txt` to 1e-4. That includes the largest point of each family: 6×7 26.4045, 5×8 25.0456,
4×9 22.3727, 6×6 22.5684, the twisted A = 72 classes, hull A = 135 29.3411 (16 deaths), cube-centred symmetric
A = 828 24.1746, vertex-centred A = 759 22.4091. All 6 hull sizes and all 16 symmetric sizes also match.

- One small difference. load.py drops CPU hull sizes with fewer than 10 deaths, which throws away the R = 15 run
  (1 death, 2.4e9 exposure). Keeping it moves hull A = 108 from 23.3761 to 23.3764. That is negligible, but dropping
  exposure because it has few deaths biases the estimate. The cleaner rule keeps every run.
- 3×6×8: s601 gives 11.0845 ± 0.0007 and s711 gives 11.0813 ± 0.0005, so +0.0032 ± 0.0009, 3.5σ, χ² 12.6 on 1. That
  confirms the claim. s601 has no `max_launch` field (launches up to 2^18) and s711 has max_launch 2048. The run with
  longer launches is the higher one, which is the sign of the firewall detection lag that fwslab.py documents
  (+0.006 at 3×6×8). The explanation is consistent, though I did not quantify it here.

## 2. Periodic slab faces — stands with corrections

I reproduce the fits: PO 0.2072 ± 0.0001 (χ² 8.3/7), PM 0.2117 ± 0.0002 (5.3/8), PS 0.2072 ± 0.0001,
PSM 0.2121 ± 0.0028 (5.3/7), Pcw 0.2105 (38.0/8, fails). Per-width slopes are 0.2072 ± 0.0001 (s = 4),
0.2082 ± 0.0006 (s = 5) and 0.2131 ± 0.0062 (s = 6).

Corrections:
- **The statistical error is ± 0.003, not ± 0.001, once the width law is left free.** PO (one offset per width) and
  PM (a cost per cell c − β/(3s)) are special cases of a(s) + A(c − D/s). That union fits (χ² 5.1/6) with
  **c = 0.2127 ± 0.0031**. With D/s² it gives 0.2103 ± 0.0017, with D·e^{−s/0.72} 0.2086 ± 0.0008, and with
  D·e^{−s/1} 0.2089 ± 0.0010. PSM's ± 0.0028 says the same thing. Within these families the 1σ envelope is 0.207 to
  **0.216**, not 0.205 to 0.212.
- Two of the five values quoted in the verdict, "0.2108 ± 0.0003 (capillary wave)" and "0.2063 ± 0.0008 (massive)",
  come from the 26 wide classes with a 0.015 error floor, not from the rectangular family. On the rectangular family
  Pcw fails (χ² 38/8). The list mixes fitting sets and should say so.
- The 0.205 lower end rests on that floored massive fit only. I did not recompute the lattice-sum fits (see "Not
  checked").

## 3. Hull faces — stands with corrections

At A ≥ 45 I reproduce HL c = 0.2226 ± 0.0010 (χ² 1.9/2) and H1 c = 0.2317 ± 0.0019 (1.3/2), the local slopes
0.2010, 0.2119, 0.2146, 0.2182 ± 0.0013 and 0.2209 ± 0.0093, and the hold-outs. The H0 and six-size failures are
also reproduced.

Corrections:
- **The one-term list is incomplete, and its range is biased upward.** A correction q/k fits as well (χ² 2.5/2,
  **c = 0.2193 ± 0.0007**, hold-outs Σz² 0.3/1 and 2.6/2), and so does q/A (χ² 3.0/2, **c = 0.2181 ± 0.0005**, 0.4/1
  and 3.1/2). √A is the same as the rim (0.2316). The defensible one-term range is **0.218 to 0.232**.
- **"No three-parameter form fits all six sizes" is true, but four parameters do not have to leave c anywhere from
  0.19 to 0.26.** A saturating slope, ln τ = a + cA − Dλ(1 − e^{−A/λ}), fits all six sizes (χ² 5.4/2, p 0.066) with
  **c = 0.2156 ± 0.0004** (D = 0.34, λ = 11.6 cells). k + 1/k² gives 0.2047 ± 0.0044 (p 0.055), and lnA + 1/k gives
  0.2069 ± 0.0029 (p 0.045). Weakness of the saturating form: it puts the 84 → 108 slope at 0.2155, which is 2.1σ
  below the measured 0.2182 ± 0.0013. A deficit decaying in the side, A(c − D·e^{−k/ξ}), fails (χ² 10.7/2).

## 4. The tension — does not stand as stated

I reproduce the write-up's six pairings exactly: penalties of 110.3, 117.7, 124.1, 146.4, 165.9 and 238.3 for one c,
and the two-term H2 joints (22.6/10, p 0.012; 24.4/11, p 0.011). The penalty has one degree of freedom, and it is the
right test. The joint χ² dilutes it, and the write-up's "p ≈ 0.01" is a joint p. Attacks (`out_fits.txt` §3,
`out_extra.txt` A, B, G):

| hull form (A ≥ 45 unless said) | periodic form | c_hull − c_per | penalty (1 dof) | joint χ²/dof, p | one c |
|---|---|---|---|---|---|
| log | long side (theirs, "at least") | +0.0109 ± 0.0010 | 117.7 (10.8σ) | 124.9/11 | 0.2120 |
| log | a(s) + A(c − D/s) | +0.0098 ± 0.0032 | 9.2 (3.0σ) | 16.1/9, 0.065 | 0.2217 |
| 1/k | a(s) + A(c − D/s) | +0.0066 ± 0.0032 | 4.3 (2.1σ) | 11.9/9, 0.22 | 0.2190 |
| 1/A | PSM (both sides) | +0.0060 ± 0.0028 | 4.6 (2.1σ) | 12.8/10, 0.23 | 0.2179 |
| **1/A** | **a(s) + A(c − D/s)** | **+0.0054 ± 0.0031** | **2.9 (p 0.09)** | **10.9/9, 0.28** | **0.2179** |
| **saturating, all six sizes** | **a(s) + A(c − D/s)** | — | **0.8 (p 0.37)** | **11.3/9, 0.26** | **0.2155** |
| saturating, all six sizes | PSM | — | 1.6 (p 0.21) | 12.3/10, 0.27 | 0.2155 |
| k + 1/k², all six sizes | long side | — | — | 13.6/11, 0.26 | 0.2117 |
| lnA + 1/k, all six sizes | long side | — | — | 14.2/11, 0.22 | 0.2117 |
| any two-term form, A ≥ 45 | long side or PSM | — | — | 8–10/9–10, 0.4–0.6 | 0.212–0.213 |

- **Forms.** The 10 to 15σ figures come from pairing slowly decaying hull corrections (rim, ln A), which put c_hull
  above every measured slope, with periodic forms that fix c to the s = 4 slope (offsets, short side) or to one
  assumed width law (long side). With the periodic width dependence left free, which is the error that should be
  propagated, the one-term hull forms are 2 to 3.6σ from the periodic value. With a fast hull correction (1/A,
  saturating), one c passes outright.
- **Plausible parameters?** In the bold 1/A row everything is ordinary. The hull prefactor is e^{17/A}. The strip cost
  is c − 0.043/s, which gives slopes 0.2071, 0.2093 and 0.2107 at s = 4, 5, 6 against measured 0.2072, 0.2082 ± 0.0006
  and 0.2131 ± 0.006. Every residual is ≤ 1.6σ; the largest is hull A = 108 at +1.6σ. **So a single-c description
  passes at p > 0.05 without implausible parameters, with c ≈ 0.218.** Its price is that periodic strips must still
  be getting dearer with width at s = 6. The two-term readings with c ≈ 0.212 are the other single-c family. They pass
  at p 0.2–0.26 with k + 1/k² or lnA + 1/k, so "only marginally, p ≈ 0.01" is specific to the k + 1/k form.
- **Size cut.** At A ≥ 63 the one-term pairings are 2.4 to 5.3σ, and those with PSM or D/s are 2.4 to 2.9σ.
  The A ≥ 45 cut sharpens the tension, because the A = 45 point is ± 0.0027.
- **Errors.** A floor of 0.005 added to every point (the write-up's own bound on soup transients is ≤ 0.005) brings
  log × PSM to p 0.16. A floor of 0.01 makes log × PSM pass (p 0.52) and rim × long side reach p 0.017. An exact
  Poisson likelihood changes nothing (128.0 against 124.9). Dropping A = 135 (16 deaths) moves c_hull by 0.0001. That
  point is not a lever.
- **CPU against GPU.** There is no sign of an offset. At A = 63 the CPU gives 13.6317 ± 0.0078 and the GPU
  13.6347 ± 0.0011. At A = 84 the CPU is 0.065 ± 0.054 lower. The GPU-only hull points (63 to 135) give
  c_hull = 0.2296 ± 0.0054 (log), so the CPU A = 45 point does not create the tension. A free GPU offset would fit at
  −0.074 ± 0.007, but the A = 63 comparison excludes it at 9σ. The large-A points of *both* families are GPU, so a
  GPU systematic would have to depend on geometry to matter.
- **What is robust (no model needed):** the hull local slopes 63 → 84 (0.2146 ± 0.0003) and 84 → 108
  (0.2182 ± 0.0013) are above both within-width periodic slopes, 0.2072 ± 0.0001 (s = 4) and 0.2082 ± 0.0006 (s = 5).
  One c needs either the hull slope to overshoot c later (c ≈ 0.21) or periodic strips to keep getting dearer with
  width (c ≈ 0.216–0.219). The data do not exclude either. "The data in hand do not define c_inf" stands. "Two
  families give two values that disagree" does not, as a form-independent statement.

## 5. Wrap-around models — the failures and ξ stand with a caveat; the κ number does not stand

- I reproduce the failures: Pcw 320.1/23 on the wide classes and 48,004/14 on the census.
- I reproduce ξ: 0.715 ± 0.008 (48 → 60) and 0.742 ± 0.020 (60 → 72), χ² 353 and 95, against 770 and 175 for D/s².
  **But the value is set by the thin tori.** Without loop² 3 the fits give 0.57 and 0.52. On loop² ≥ 7 alone they
  give 1.05 ± 0.10 and 0.42 ± 0.09, which differ by 4.8σ, with asymptotes 0.2206 and 0.2081. "ξ = 0.71–0.74" should be
  reported as "0.4 to 1.05, depending on the classes", and loop² 4 carries the known tie bias.
- **κ.** I reproduce −1.008 ± 0.008 (census A = 48 and 60, loop² ≥ 7, χ² 859.5/8). Tested hard:
  - *Error.* Inflated by √(χ²/dof) it is ± 0.08. The jackknife over the 11 classes gives **± 0.28**. Leaving out the
    single A = 60 loop² 7 class gives −0.77, and leaving out the A = 48 one gives −1.18. Those two classes sit at
    F = 0.70 and 0.84 against 0.52–0.57 for every other class, so κ is a two-point lever arm, and their residuals are
    +19σ and −15σ.
  - *Area.* With one offset per area, κ = −0.72 ± 0.05 (A = 48), −1.18 ± 0.03 (A = 60) and −1.43 ± 0.03 (A = 72)
    (errors inflated). With the 0.015 floor: −0.72 ± 0.10, −1.16 ± 0.06, −1.41 ± 0.04. κ drifts with area by 6σ (floored) to 12σ, so
    the form is wrong. −1.01 is the average of A = 48 and 60.
  - *Selection.* Census loop² ≥ 12 gives −1.29; wide gives −1.37; loop² ≥ 13 gives −1.50; loop² ≥ 7 over all areas
    gives −1.22.
  - *Error model.* With the 0.015 floor: −1.05 ± 0.05 (census loop² ≥ 7) and −1.19 ± 0.11 (wide).
  - Inside the one selection, the scaled χ² profile disfavours −0.8 at 2.5σ and −1.3 at 3.5σ. Against the jackknife
    and the area drift that means nothing. **−1 cannot be told from −0.8 or −1.3.** The Ising comparison should be
    removed, or stated as "κ between −0.7 and −1.5; the form does not hold at fixed area."

## 6. Out-of-sample table — stands

Recomputed: periodic PA 6.2/3, 0.16 and 6.5/6, 0.15; PO 3.5/3, 0.11; PM 2.2/3, 0.06 and 2.7/6, 0.06; PS 3.6/3 and
3.7/6; PSM 2.3/3 and 2.4/6; Pcw 0.3/3, 0.02 and 4.4/6, 0.05; s = 4 1.8/1 and 1.8/2; s = 5 0.1/1 and 0.2/2; wide PA
15.1/5, 0.19; wide Pcw 8.4/5, 0.09; hull H0 2.1/1, 0.38 and 9.7/2, 0.39; H1 0.1/1, 0.10 and 1.4/2 (theirs 1.3/2;
the A = 108 death); HL 0.2/1, 0.12 and 1.9/2, 0.14. The conclusion, that the hold-outs do not discriminate, holds,
and it extends to the forms the write-up did not try (1/k: 2.6/2; 1/A: 3.1/2).

## 7. Forecasts — (A) stands; (B) overstated blindness

- PREDICTIONS.md has one commit, 5dd18b9 (22:02:22). There are no empty-patch data in the tree, then or now (only
  patch_geom.py), so **(A) is blind**. Its numbers follow from the stated form, −ln P = c·3ab + (σ/4)(16a − 4) with
  c = 0.212 and σ = 0.34. I recomputed 1.66, 4.92, 9.46, 15.28, 22.36 and 30.72, the ranges, the strip step 1.32,
  σ_b = 0.0863 and the per-cell values 0.55 to 0.28. All agree.
- **(B).** Refitting the capillary wave on set W myself (κ = −1.368) gives every forecast d in the table: +0.0039,
  +0.0043, +0.0006, +0.0008, +0.0008, +0.0001, +0.0029, +0.0005, +0.0001, 0.0000. They use no shape3 data, so the
  numbers cannot have been tuned. **But** `research/shape3/data/runs.csv` already held P3 when the forecast was
  committed (added f30c27c, 21:14, before the analyst read report.txt at 831947a), and T72 (the T01/T12 tori) and N72
  (added 13b4000, 21:56:44, 5.5 minutes before 5dd18b9). "Blind: T01, T12, N72, P3" rests on the analyst's word, not
  on git. Only P2 and Q63 were absent. The disclosure should list these rows. For what it is worth, scoring the data
  in the tree now: T01 +0.0038 ± 0.0064, T12 −0.0040 ± 0.0064, N72 +0.0018 ± 0.0061 (Σz² 0.85 on 3), consistent with
  "zero within ± 0.001". P3 is +0.0075 ± 0.0033 (z = +2.1).

## 8. Proposed measurements

1. **Equilateral tori.** This one is useful, but the reason should change. The equilateral torus has the largest
   shortest loop possible at a given area, so it is the widest periodic lever there is. The question it decides is
   whether the periodic slope still rises with width. The single-c reading of §4 (strip cost c − 0.043/s) predicts
   slopes rising from 0.208 (n = 19) to 0.211 (n = 37). The "periodic constant reached" reading predicts flat. The
   difference is about 0.003 across the plan: about 3σ at ± 0.001 per slope. The shape-model distinction the
   write-up draws (massive falling, capillary wave flat) is smaller than that. The loop-slope deficit fits give a
   deficit of 0.003 at n = 19 and 0.0003 at n = 37, and its sign is opposite to that of mexp, so "massive" makes no
   single prediction.
2. **Equal-area hulls with different rims.** This discriminates strongly: ± 0.01 per vessel at 10⁴ deaths, against
   about 0.7 nats between the rim readings for six rim cells. That holds only if the corners are held fixed. A
   truncated face changes the corner count (3 → 6) and the angle (60° → 120°) along with the rim. **Better design:**
   hexagonal faces of equal area with different side ratios (a, b, a, b, a, b). These have the same six 120° corners
   and different rim lengths, and two such pairs separate a per-rim-cell term from a per-corner one. The design does
   not test the 1/A or saturating single-c readings, which have no rim term.
3. **Width 6.** This **does not decide.** With 6×7 at 800 deaths (15 GPU-hours) the 108 → 126 slope is ± 0.0023. The
   D/s single-c reading predicts 0.2090 there and the flat reading 0.2082, 0.3σ apart. The error on c under
   a(s) + A(c − D/s) improves only from 0.0031 to 0.0029 (0.0026 at 3,000 deaths). Drop it. A cheaper variant also
   fails (`out_extra.txt` E, F). Hull A = 108 at 10⁴ deaths (about 4 GPU-hours) would measure the 84 → 108 slope to
   ± 0.0005. That separates the saturating reading (0.2155) from the others (0.2161–0.2171) at 1 to 3σ only, so it is
   not decisive either. The decisive measurements are (1), (2) with controlled corners, and the empty-patch
   experiment, which has neither a wrap nor a rim.

## Corrections the write-up needs

1. Verdict 1, and the "0.205–0.212" range: give the periodic c as 0.207–0.213 with statistical ± 0.003 when the width
   law is free (a(s) + A(c − D/s): 0.2127 ± 0.0031; PSM 0.2121 ± 0.0028). Say which fitting set each listed value
   comes from (the capillary-wave and massive values are wide classes with a 0.015 floor).
2. Verdict 2: add the 1/k (0.2193 ± 0.0007) and 1/A (0.2181 ± 0.0005) one-term hull forms. The one-term range is
   0.218–0.232. Mention the saturating four-parameter form, which fits all six sizes with c = 0.2156.
3. Verdict 3 and the joint table: "+0.0109 ± 0.0010 at the least" and "Δχ² = 110 to 238" hold only for the forms
   chosen. Give the range over defensible pairs (+0.0054 ± 0.0031, 1.7σ, to +0.0245 ± 0.0019). Report the penalty as
   a 1-dof test.
4. Verdict 4: "one c fits only if the hull correction has two terms … p ≈ 0.01" is wrong. One-term 1/A with
   a(s) + A(c − D/s) gives one c = 0.2179 (penalty p 0.09, joint p 0.28). The saturating form gives 0.2155 (p 0.37).
   The two-term forms k + 1/k² and lnA + 1/k give joint p 0.22–0.26. State the robust fact instead: the hull's local
   slope at A = 63–108 lies above every periodic within-width slope, and single-c readings need either an overshoot of
   the hull slope or periodic strips that keep getting dearer with width.
5. Verdict 5, "c_inf = 0.2085 ± 0.004 with a one-sided +0.02": the data allow one c anywhere from about 0.207 to
   0.219. "Prefer the periodic value" remains a judgement, and it should be labelled as one.
6. Wrap-around section: replace "κ = −1.01 ± 0.01 (Ising −1)" with the area dependence (−0.72, −1.18, −1.43) and the
   jackknife error (± 0.28). Report ξ as dependent on the classes (0.4–1.05 without the thin tori).
7. PREDICTIONS.md (B): list the shape3 rows that were in the tree at 5dd18b9 (P3, T72, N72).
8. Measurement 3: withdraw it, or restate what it can decide. Measurement 2: specify corner-matched pairs.
9. load.py: keep CPU hull runs with fewer than 10 deaths (dropping their exposure is a bias, here +0.0003 at A = 108).

## Not checked

- The massive lattice-sum fits (mexp, mk0, mexp2) and the 0.2063 ± 0.0008 they give; the pair table's mexp and K₀
  columns (I recomputed only the capillary-wave column).
- Symmetric-face fits, the 2D toy, patch_geom.py's perimeter counts, extras.py's costs and equilateral lattices.
- The README's statement that the hull points at A = 84 and 108 lie 0.04–0.06 and 0.17–0.24 above the forced fits;
  the equilateral slope change (−0.0029 ± 0.0013).
- Data production: firewall-resolved estimators at firewall shares of 91–99% (4×8, 4×9, 5×8), detection lag, soup
  transients in slabs (no T0), thickness 8 at A ≥ 108, and whether the GPU kernel's settled-state test misses
  "zombie" lives as research/shape3 found for ts.c. That last one would inflate the exposure of long lives and bias
  the large-A points of both families upward. It is worth a check by whoever owns the kernel.
- Whether lattices with equal theta series but different orientation relative to the crystal have equal hazards. The
  pooled χ² values are small (≤ 3.9 on 3), and I relied on that.
