# Is there one cost per cell? What the lifetimes in hand can and cannot say about c_inf

Analyst on the constant, 2026-11-14; corrected the same day after an adversarial review
(`research/audit/REVIEW-constant.md`; what changed is listed under "Corrections after review"). Confined chaos in
gump ends when a boundary face of A cells goes extinct, after a mean wait τ_face with ln τ_face ≈ 0.21·A. The
question: is there a single cost per cell c_inf of an unbounded face, what is it, and with what error. No new
simulation was run; every number below is recomputed from tracked data by the scripts of this directory
(`load.py --check` prints each value beside the one quoted in the READMEs and the ledger). Tags: **[measured]** a
statistic of tracked data; **[fitted: …]** with what was free; **[conjectured]**; **[judgement]**.

## Verdict

**The data in hand do not define c_inf. One constant for both families is allowed anywhere from about 0.207 to
0.219; where in that range it lies depends on forms the data cannot choose between.**

1. **What holds without a model** [measured]: the hull's local slopes, 0.2119 ± 0.0002 (A = 45 → 63),
   0.2146 ± 0.0003 (63 → 84), 0.2182 ± 0.0013 (84 → 108), rising at every step, lie above the slopes of periodic
   faces at fixed width, 0.2072 ± 0.0001 (width 4, A = 60 to 108) and 0.2082 ± 0.0006 (width 5, A = 75 to 120).
   Width 6 has two sizes: 0.2131 ± 0.0062. One c needs either the hull's slope to stop rising at once (and c to
   lie below it), or periodic strips to keep getting dearer with width well beyond width 6.
2. **Periodic slab faces alone** (rectangular, widths 4 to 6, 11 classes, A = 60 to 126) [fitted]: the cost per
   cell is 0.2072 ± 0.0001 if the width only shifts the offset, and **0.2086 ± 0.0008 to 0.2127 ± 0.0031** if the
   cost per cell of a strip depends on its width (exponential, 1/s², 1/s; each with χ² 5 on 6). Envelope
   **0.207 to 0.216**; the statistical error is about ± 0.003 once the width law is free. On another fitting set
   (the 26 wide classes of every shape, 0.015 added to every error) the capillary-wave form gives 0.2108 ± 0.0003
   and the massive loop sum 0.2063 ± 0.0008.
3. **Hull faces alone** [fitted]: with one correction term (A ≥ 45) the cost per cell is 0.2181 ± 0.0005 (q/A),
   0.2193 ± 0.0007 (q/k), 0.2226 ± 0.0010 (p·ln A), 0.2317 ± 0.0019 (r·k, the rim), all with χ² ≤ 3.0 on 2: **0.218 to
   0.232**. Four-parameter forms fit all six sizes with 0.2156 ± 0.0004 (a deficit of the slope that dies out over
   12 cells), 0.2069 ± 0.0029 (ln A and 1/k), 0.2047 ± 0.0044 (k and 1/k²), 0.1917 ± 0.0057 (k and 1/k), at
   p = 0.07 to 0.03.
4. **One c for both families** [fitted: c, the hull's correction, the periodic family's]: of 84 pairings of a
   hull form with a periodic form, **36 pass** (each form fits its own family, joint χ² with p ≥ 0.01, and the
   penalty for one c, one degree of freedom, with p ≥ 0.01). Their c runs from **0.2072 to 0.2190** (13 pass at
   p ≥ 0.05: 0.2072 to 0.2179). They are of two kinds:
   - **c = 0.207 to 0.214** (30 pairings): c is the periodic family's, and the hull's correction has two terms
     (k and 1/k², ln A and 1/k, k and 1/k). The hull's local slope then levels at 0.215 to 0.217 from A = 84 on.
   - **c = 0.2155 to 0.2190** (6 pairings): the hull's correction dies out fast (saturating, q/A, q/k), and the
     cost per cell of a periodic strip of width s is c − D/s with D = 0.034 to 0.048: 0.2071 at width 4, 0.210 to
     0.211 at width 6, still 0.003 to 0.004 short of c at width 12. With a faster width law (1/s², exponential)
     none of these passes (penalty ≥ 9.1).

   Every one of the 36 puts the hull's 84 → 108 slope at 0.2153 to 0.2163 (measured 0.2182 ± 0.0013); the largest
   residual is hull A = 108 (+1.5 to +2.0σ) in 25 of them and hull A = 84 (−1.6 to −2.0σ) in 9.
5. **Withdrawn** (first version of this page): "c_hull − c_periodic is +0.0109 ± 0.0010 at the least" and "one c
   fits only with two hull terms, p ≈ 0.01". Those held for the forms I had tried. Over the pairings in which
   both forms fit their own family the difference runs from −0.021 ± 0.006 to +0.0245 ± 0.0019 and the penalty
   from 0.0 to 1179.
6. **If one number must be quoted**: **c_inf = 0.213 ± 0.006**, the midpoint and half-width of the single-c
   readings that pass (a range, not a standard error). **[judgement]** I lean to its lower half, the periodic
   family's 0.207 to 0.213: that family has no boundary; the upper readings need the slowest width law tried;
   and, carried to the equilateral tori with a smooth offset, they sit 2.7 to 3.2σ from the 6 × 6 run (below).
   Against that leaning: the lower readings need the hull's slope, which has risen at every step measured, to
   stop where the data end. Each side of the argument is a 2 to 3σ matter. "About 0.21" survives as a rounding;
   "0.2077 + 0.55/A" (retired) was a hull-face fit whose constant no hull fit of this page reproduces.
7. Out-of-sample forecasts of the largest one or two sizes **do not discriminate** between the one-term forms: the
   held-out sizes are the least precise points (± 0.03 to ± 0.25). They reject the area-only line in both
   families, and they are harder on the four-parameter hull forms (fitted to four sizes, these under-forecast
   A = 108 by 0.07 to 0.09, 2.2 to 2.5σ) than on the one-term ones (0.04 to 0.06, 1.1 to 1.6σ).
8. O_h-symmetric faces (A = 360 to 828) put no constraint on c_inf: six times their cost per cell is 0.218 ± 0.007
   or 0.249 ± 0.015 (cube-centred, log or rim correction), 0.2065 or 0.2294 (vertex-centred, neither form fits),
   and equating it with c_inf is itself a conjecture ("lockstep").

## Data

`python3 research/constant/load.py --check` (→ `out/points.txt`). ln τ_face = ln(faces × exposure / deaths),
error 1/√deaths; faces = 2 (slab), 8 (asymmetric hull), 1 (O_h hull: the eight die together).

| family | points | source files | notes |
|---|---|---|---|
| periodic, rectangular s × M × 8 | 15 slabs (14 shapes), A = 54 to 126 | `research/data/gpu_facelaw/fwslab*.json` | firewall channel resolved; ln(2E/F) |
| periodic, twisted | 8 + 9 + 14 classes at A = 48, 60, 72 (shortest loop² ≥ 3) | `research/shape/data/A60.csv, A72.csv`; `research/shape2/data/A48.csv, A60.csv, A72x.csv` | recomputed from exposure and deaths |
| hull, asymmetric | A = 30, 45, 63, 84, 108, 135 | `research/fluct/data/qsd_summary.json` (R = 7 to 19), `gpu_facelaw/R*_A10G.json` (R = 11 to 17, T0 = 200) | pooled by size; every run kept |
| hull, O_h-symmetric | 8 + 8 sizes, A = 360 to 828 | `research/fluct/data/sym_residence.csv` (fresh soups only), `gpu_facelaw/sym[cv]R*.json` (T0 = 1000) | copies of the side-16 cube excluded |

Periodic runs of one torus are pooled by isometry class of the period lattice (reduced Gram matrix, `lat.py`;
`python3 research/constant/lat.py selftest` checks it against research/shape2's class tables), summing exposure
and deaths; 42 classes with shortest loop² ≥ 3 in all. "Wide" = shortest loop² ≥ 12 (26 classes). The reviewer's
independent loader reproduces all 64 points to 1e-4.

Where sources disagree, or my value differs from a quoted one:

- Hull A = 84: CPU 18.077 ± 0.054 (342 deaths) against GPU 18.141 ± 0.005; pooled 18.1407 is used. Hull A = 108:
  23.3764 ± 0.0307 with the CPU run of one death pooled in (23.3761 without). The CPU runs at A = 135 and 165 saw
  no death; the first adds exposure to the pool, the second is a bound (ln τ > 22.2), not a point. Local slopes
  on the pooled values: 0.2010, 0.2119, 0.2146, 0.2182 ± 0.0013, 0.2209 ± 0.0093.
- 6 × 6 × 8: I use the firewall-resolved run alone, 22.568 ± 0.041 (592 deaths). CLAIMS GP8's "pooled 22.537"
  adds the earlier run, whose statistic is the first event of either kind.
- 3 × 6 × 8: its two GPU runs give 11.0845 ± 0.0007 and 11.0813 ± 0.0005 (χ² 12.6 on 1; the launch caps differ).
  Width 3 enters no fit of c here.
- Width families: one slope with an offset per width gives 0.2072 ± 0.0001 with offsets 0.055, 0.123, 0.206,
  χ² 8.3 on 7 (ledger GP9: 0.053, 0.121, 0.203, 8.4 on 8; I pool the GPU's 4 × 5 and 4 × 6 with the CPU runs of the
  same tori and count 6 × 4 with 4 × 6). a + cA − βM: 0.2117, β = 0.054, χ² 5.3 on 8 (ledger: 5.6 on 9).
- Cost per cell by shortest loop between areas (`shape_models.py slopes`): 48 → 60: 0.1148, 0.1414, 0.1918, 0.2074,
  0.2090, 0.2127 at loop² 3, 4, 7, 12, 13, 16; 60 → 72: 0.1107, 0.1353, 0.1872, 0.2047, 0.2062, 0.2072 (ledger
  SH3: 0.2125 and 0.208 at loop² 16; mine include the GPU's 4 × 5 and 4 × 6).
- Not used: `research/peeling/slab_area.csv` (first peels not screened for firewalls), the mirror-cut hulls of the
  swarm's exam (three values, no tracked data file), research/shape3 (in flight; see PREDICTIONS.md).

## Models

ln τ_face = c_inf·A + (correction of the family) + constant. A fit **fails** if its χ² has p < 0.01 at the
statistical errors. H0 to H2, PA to PSM, Pcw and the massive forms were stated before fitting; the forms marked †
were added after the review, which had found that they fit.

Hull faces (triangle of side k, A = 3k(k + 1)/2; 6k − 3 of its cells lie on the hull's edges and belong to two
faces, three of them to four):

| | form | parameters | meaning of the correction |
|---|---|---|---|
| H0 | a + cA | 2 | none |
| H1 | a + cA + r·k | 3 | rim cells cost c + r/6 each instead of c (r < 0: fewer neighbours, cheaper; r > 0: held up by the neighbouring faces) |
| HL | a + cA + p·ln A | 3 | a power of A in the prefactor of the rate (entropy of where the collapse starts, or a fluctuating edge) |
| Hk † | a + cA + q/k | 3 | a correction that dies out as the inverse side |
| HA † | a + cA + q/A | 3 | one that dies out as the inverse area (no rim term at all) |
| H2 | a + cA + r·k + q/k | 4 | rim plus the next order (corners interacting with the rim) |
| H2b †, HLk † | a + cA + r·k + q/k²; a + cA + p·ln A + q/k | 4 | two terms, other pairs |
| Hsat † | a + cA − Dλ(1 − e^{−A/λ}) | 4 | the slope is c − D·e^{−A/λ}: a deficit that dies out over λ cells |
| Hside † | a + A(c − D·e^{−k/ξ}) | 4 | a deficit of the cost per cell decaying with the side |

Periodic faces (no rim; period lattice with sides s ≤ M for rectangular slabs, shape modulus τ in general):

| | form | parameters | meaning |
|---|---|---|---|
| PA | a + cA | 2 | none |
| PO | a(s) + cA | 4 (three widths) | transfer-matrix picture: a strip of width s has its own prefactor, one cost per cell |
| PM | a + cA − βM | 3 | the cost per cell of a strip of width s is c − β/(3s) |
| PS | a + cA + αs | 3 | an offset growing with the short side |
| PSM | a + cA + αs + βM | 4 | both |
| PD † | a(s) + A(c − D/s) | 5 | an offset per width and a cost per cell approaching c as 1/s (PO and PM are special cases) |
| PD2 †, PDe † | the same with D/s², D·e^{−s/0.72} (and e^{−s/1}) | 5 | faster width laws; 0.72 cube steps is the decay length of the loop-deficit fits |
| Pcw | a + cA + κF(τ) | 3 | **massless (capillary wave)**: F = −½ ln Im τ − 2 ln\|η(τ)\|, the log of the free-boson partition function of the face torus (Caselle, Gliozzi, Vinti 1993) |
| mexp, mk0 | a + A[c − g·Σ_v f(\|v\|/ξ)] | 4 | **massive**: each nonzero period vector v lowers the cost per cell; f = e^{−r} or K₀(r); ξ ≤ 3 cube steps |
| mexp2 | the same + h·Σ_v f | 5 | the intercept moves with the same sum |

Lengths are in cube steps of the face plane (the unit in which a slab's side is counted; one step = √2 cube sides).

## Results, family by family

`python3 research/constant/fit.py` (→ `out/main_table.txt`: every fit with the residual of every point; 100 s).
[fitted: all parameters of each form.] "−1", "−2": the form fitted without the largest one or two sizes (of each
width, for the rectangular family) and scored on them, Σz² / points and the largest residual,
z = residual/√(error² + forecast error²):

| family | model | par. | χ²/dof | verdict | c | −1 | −2 |
|---|---|---:|---:|---|---:|---|---|
| hull, six sizes | H0 | 2 | 1492.0/4 | fails | 0.2090 | 5.3/1, 0.66 | 14.3/2, 0.67 |
| | H1 rim | 3 | 106.9/3 | fails | 0.2480 | 0.2/1, 0.12 | 0.5/2, 0.14 |
| | HL log | 3 | 69.1/3 | fails | 0.2293 | 0.0/1, 0.05 | 0.3/2, 0.06 |
| | Hk, HA | 3 | 36.1/3, 21.5/3 | fail | 0.2225, 0.2201 | 0.0/1, 0.1/1 | 0.1/2, 0.1/2 |
| | H2 rim + 1/k | 4 | 7.0/2 | fits (p 0.03) | 0.1917 ± 0.0057 | 0.8/1, 0.24 | 7.6/2, 0.31 |
| | H2b rim + 1/k² | 4 | 5.8/2 | fits (p 0.055) | 0.2047 ± 0.0044 | 0.6/1, 0.21 | 6.2/2, 0.27 |
| | HLk log + 1/k | 4 | 6.2/2 | fits (p 0.045) | 0.2069 ± 0.0029 | 0.7/1, 0.22 | 6.6/2, 0.28 |
| | **Hsat** | 4 | 5.4/2 | fits (p 0.066) | **0.2156 ± 0.0004** | 0.7/1, 0.21 | 5.6/2, 0.23 |
| | Hside | 4 | 10.7/2 | fails | 0.1996 | 1.1/1, 0.30 | 11.6/2, 0.39 |
| hull, A ≥ 45 | H0 | 2 | 100.5/3 | fails | 0.2128 | 2.1/1, 0.38 | 9.7/2, 0.39 |
| | **H1 rim** | 3 | 1.3/2 | fits | **0.2317 ± 0.0019** | 0.1/1, 0.10 | 1.4/2, 0.11 |
| | **HL log** | 3 | 1.9/2 | fits | **0.2226 ± 0.0010** | 0.2/1, 0.12 | 1.9/2, 0.14 |
| | **Hk 1/k** | 3 | 2.5/2 | fits | **0.2193 ± 0.0007** | 0.3/1, 0.14 | 2.6/2, 0.16 |
| | **HA 1/A** | 3 | 3.0/2 | fits | **0.2181 ± 0.0005** | 0.4/1, 0.15 | 3.1/2, 0.17 |
| | H2, H2b, HLk | 4 | 0.0/1 | fit | 0.263 ± 0.028, 0.257 ± 0.022, 0.242 ± 0.015 | 0.0/1, 0.02 | – |
| periodic, s = 4 alone | PA | 2 | 4.3/3 | fits | 0.2072 ± 0.0001 | 1.8/1, 0.06 | 1.8/2, 0.06 |
| periodic, s = 5 alone | PA | 2 | 0.3/2 | fits | 0.2082 ± 0.0006 | 0.1/1, 0.02 | 0.2/2, 0.02 |
| periodic, s = 4, 5, 6 (11 classes) | PA | 2 | 515.5/9 | fails | 0.2085 | 6.2/3, 0.16 | 6.5/6, 0.16 |
| | **PO offsets** | 4 | 8.3/7 | fits | **0.2072 ± 0.0001** | 3.5/3, 0.11 | – |
| | **PM long side** | 3 | 5.3/8 | fits | **0.2117 ± 0.0002** | 2.2/3, 0.06 | 2.7/6, 0.06 |
| | PS short side | 3 | 8.4/8 | fits | 0.2072 ± 0.0001 | 3.6/3, 0.11 | 3.7/6, 0.11 |
| | PSM both | 4 | 5.3/7 | fits | 0.2121 ± 0.0028 | 2.3/3, 0.06 | 2.4/6, 0.06 |
| | **PD, 1/s** | 5 | 5.1/6 | fits | **0.2127 ± 0.0031** (D = 0.022 ± 0.013) | 2.4/3, 0.08 | – |
| | PD2, 1/s² | 5 | 5.1/6 | fits | 0.2103 ± 0.0017 | 2.4/3, 0.08 | – |
| | PDe, e^{−s/0.72}; e^{−s/1} | 5 | 5.2/6; 5.1/6 | fit | 0.2086 ± 0.0008; 0.2089 ± 0.0010 | 2.5/3, 0.09 | – |
| | Pcw | 3 | 38.0/8 | fails | 0.2105 | 0.3/3, 0.02 | 4.4/6, 0.05 |
| | mexp | 4 | 7.8/7 | fits (degenerate) | 0.2080 ± 0.0003 | 3.3/3, 0.13 | 3.9/6, 0.13 |
| periodic, wide (26 classes) | PA | 2 | 1902.7/24 | fails | 0.2104 | 15.1/5, 0.19 | – |
| | Pcw | 3 | 320.1/23 | fails | 0.2114 | 8.4/5, 0.09 | – |
| | mexp | 4 | 205.5/22 | fails | 0.2050 | 7.7/5, 0.19 | – |
| | mk0 | 4 | 209.0/22 | fails | 0.2048 | 7.7/5, 0.19 | – |

(For the wide set the held-out points are the five classes with A ≥ 105. On the rectangular family alone mexp
runs to ξ = 0.14 with g at its bound: it has become the offset model. With D free the width-law forms hold the
measured slopes of widths 4 and 5 and differ only in the extrapolation: the cost per cell of a strip of width 12
is 0.2109, 0.2099, 0.2086 under 1/s, 1/s², exponential.)

Further [measured / fitted]:

- **No three-parameter form fits all six hull sizes** (χ² 21 to 107 on 3): the A = 30 face (21 of its 30 cells on
  the rim) lies 0.06 to 0.10 above the forms that fit A ≥ 45 (3.5 to 10σ with the forecast error included).
- **Local slopes the hull forms imply** (84 → 108 measured 0.2182 ± 0.0013): one-term forms 0.2162 to 0.2168, then
  0.2169 to 0.2185 at 108 → 135; the four-parameter forms 0.2153 to 0.2155, then flat or falling. ln τ(A = 165)
  is 35.7 to 35.8 under the first and 35.5 to 35.6 under the second.
- **Wide periodic faces at the level where shape is understood.** No global form fits the 26 wide classes at their
  statistical errors (± 0.001 to 0.003 at A ≤ 75). Two equal-area, equal-loop pairs differ by 0.015 for a reason
  nobody has found (CLAIMS SH2); with 0.015 added in quadrature to every error, Pcw fits (χ² 18.6 on 23, c =
  0.2108 ± 0.0003, κ = −1.19 ± 0.11) and so does the massive form (15.4 on 22, c = 0.2063 ± 0.0008, ξ = 0.79 ± 0.16
  cube steps); the area-only line does not (134.9 on 24).
- **Equilateral tori**, the one family of constant shape (4 × 4, 5 × 5, 6 × 6: only the size changes): local slopes
  0.2122 ± 0.0001 (A = 48 → 75) and 0.2093 ± 0.0012 (75 → 108), a change of −0.0029 ± 0.0013 (2.3σ). The fall
  rests on two things: the 6 × 6 run (592 deaths), and the 4 × 4 torus lying 0.068 below the line of the
  width-4 rectangles (4 × 5 to 4 × 9) continued to A = 48 (5 × 5 is on the line of its width: −0.006 ± 0.033).
- **Symmetric faces** (c₆ per cell of the symmetric face): cube-centred, H1: 6c₆ = 0.249 ± 0.015, χ² 2.9 on 5; HL:
  0.218 ± 0.007, 2.8 on 5; both forecast the held-out A = 759 and 828 within 0.04. Vertex-centred: neither fits
  (χ² 158 and 162 on 5). The ledger's S2 fixes the slope at 0.209/6; left free, it is not determined.
- **The 2D relative has the same disease, larger** (`extras.py toy`, from research/toy2d's tables): rings have local
  slopes 0.44 to 0.38 (falling), edges of boxes 0.33 to 0.36, at L = 12 to 36. There the cornered family is
  *below* the wrapped one; in gump the rimmed family is above.

## One c for both families

Section 4 of the table. Each pairing: the hull form on hull faces (A ≥ 45 for one-term forms, all six sizes for
four-parameter forms, and the two-term forms also at A ≥ 45), the periodic form on the 11 rectangular classes,
separately and with one c. The test of one c is the **penalty** χ²(joint) − χ²(hull) − χ²(periodic), one degree
of freedom; the joint χ² dilutes it.

| hull form | periodic form | c_hull − c_per | penalty (1 dof) | joint χ²/dof, p | one c |
|---|---|---:|---:|---|---:|
| rim | offsets | +0.0245 ± 0.0019 | 165.9 | 175.5/10 | fails |
| log | offsets | +0.0154 ± 0.0010 | 238.3 | 248.5/10 | fails |
| rim | long side | +0.0200 ± 0.0019 | 110.3 | 116.9/11 | fails |
| log | long side | +0.0109 ± 0.0010 | 117.7 | 124.9/11 | fails |
| log | a(s), D/s | +0.0098 ± 0.0032 | 9.2 (p 0.0025) | 16.1/9, 0.065 | fails on the penalty |
| 1/A | a(s), D/s² | +0.0079 ± 0.0018 | 19.0 | 27.1/9 | fails |
| 1/A | a(s), D·e^{−s/0.72} | +0.0095 ± 0.0010 | 92.2 | 100.3/9 | fails |
| 1/k | a(s), D/s | +0.0066 ± 0.0032 | 4.3 (p 0.038) | 11.9/9, 0.22 | 0.2190 ± 0.0007 |
| **1/A** | **a(s), D/s** | +0.0054 ± 0.0031 | 2.9 (p 0.088) | 10.9/9, 0.28 | **0.2179 ± 0.0005** |
| 1/A | both sides | +0.0060 ± 0.0028 | 4.6 (p 0.033) | 12.8/10, 0.23 | 0.2179 ± 0.0005 |
| **saturating** (six sizes) | **a(s), D/s** | +0.0028 ± 0.0031 | 0.8 (p 0.37) | 11.3/9, 0.26 | **0.2155 ± 0.0004** |
| saturating (six sizes) | a(s), D/s² | +0.0053 ± 0.0018 | 9.1 (p 0.0025) | 19.6/9, 0.02 | fails on the penalty |
| k + 1/k² (six sizes) | long side | −0.0070 ± 0.0044 | 2.5 (p 0.11) | 13.6/11, 0.26 | 0.2117 ± 0.0002 |
| ln A + 1/k (six sizes) | long side | −0.0048 ± 0.0029 | 2.7 (p 0.10) | 14.2/11, 0.22 | 0.2117 ± 0.0002 |
| k + 1/k² (six sizes) | offsets | −0.0025 ± 0.0044 | 0.3 (p 0.57) | 14.4/10, 0.16 | 0.2072 ± 0.0001 |
| k + 1/k (six sizes) | offsets | −0.0155 ± 0.0057 | 7.3 (p 0.007) | 22.6/10, 0.012 | fails on the penalty |
| k + 1/k (A ≥ 45) | a(s), D/s | (+0.05 ± 0.03) | 3.3 (p 0.07) | 8.4/8, 0.40 | 0.2134 ± 0.0031 |

The full matrix (84 pairings, and 28 more with hull A ≥ 63), the 36 that pass with every residual, and what each
implies beyond the data are in `out/main_table.txt`. From it:

- In the readings with c ≥ 0.2155 the offsets a(s) fall with the width (+0.06, −0.04, −0.18 at widths 4, 5, 6 for
  c = 0.2179); in those with c ≤ 0.214 they rise or stay level (+0.055, +0.123, +0.206 for offsets alone).
- Error floors (0.005 is the sources' bound on soup transients): with 0.005 added to every error the pairings of
  the first write-up still fail (rim or log × long side: penalty 36 and 40), log × D/s has penalty 7.1 (p 0.0075),
  1/A × D/s 2.6. With 0.01: log × D/s 4.5 (p 0.034).
- Cut at A ≥ 63 (four hull sizes): the one-term forms are 2.4 to 5.3σ from the periodic value; 1/A and 1/k with
  D/s pass (c = 0.218).

**The single-c readings carried to the equilateral tori** [fitted; `eq_forecast.py`]. For tori of constant shape
s = √(A/3), so a(s) + A(c − D/s) with an offset at most linear in s is a + cA + ρ√A. With c fixed at 0.2155,
0.2179, 0.2190 and (a, ρ) fitted to 4 × 4, 5 × 5, 6 × 6: χ² = 7.7, 9.7, 10.7 on 1; the 6 × 6 run lies 0.11 to 0.13
(2.7 to 3.2σ) below. With c free the three tori give c = 0.196 ± 0.007 and ρ = +0.25 ± 0.11. The flat line
(c = 0.2121) is 2.3σ from the same run. An offset that is not smooth in s escapes this test.

## The two wrap-around models asked for by the lead

`python3 research/constant/shape_models.py tests` (→ `out/shape_tests.txt`), `slopes` (→ `out/slopes.txt`),
`kappa` (→ `out/kappa.txt`), `pairs` (→ `out/pairs.txt`). All [fitted: a, c and the model's own parameters].

| model | par. | census A = 48, 60 (17 classes): χ²/dof | → A = 72 (14 classes): rms residual | wide (26): χ²/dof | wide → thin: rms | thin → wide: rms | all 42: χ²/dof |
|---|---:|---:|---:|---:|---:|---:|---:|
| area only | 2 | 1,128,759/15 | 1.23 | 1902.7/24 | 1.49 | 1.57 | 1,983,098/40 |
| (a) capillary wave | 3 | 48,004/14 | 0.27 | 320.1/23 | 0.29 | 0.58 | 89,799/39 |
| (b) massive, e^{−r} | 4 | 20,925/13 (ξ at its bound) | 0.14 | 205.5/22 | 0.58 | 0.11 (ξ at bound) | 25,598/38 |
| (b) massive, K₀ | 4 | 33,260/13 (ξ at bound) | 0.15 | 209.0/22 | 0.52 | 0.32 | 47,172/38 |
| (b) + intercept term | 5 | 9,304/12 | 0.18 | 180.7/21 | 0.52 | 0.48 | 19,039/37 |

- **Neither model, nor any variant tried, fits at any scope, and none carries from thin faces to wide ones or
  back.** Thin tori (shortest loop² 3, 4, 7) differ from wide ones in the intercept as well as in the cost per cell
  (the line through a loop class at A = 48 and 60 has intercept +3.13, +2.70, +0.61, against −0.03 to −0.28 for
  the wide classes; `out/slopes.txt`), which a correction to the cost per cell alone cannot give; with the thin
  tori in, the massive fits run to the bound on ξ, where the lattice sum is degenerate with a + cA. The
  five-parameter variant brings the rms residual over all 42 classes (ln τ from 8.6 to 26.4) to 0.08 with
  ξ = 0.51 cube steps, but its χ² is 19,039 on 37.
- **The deficit of the cost per cell falls faster than the inverse square of the shortest loop, and its decay
  length is not determined.** Fitted to the six loop classes, c − D·e^{−s/ξ} gives ξ = 0.71 ± 0.01 (A = 48 → 60)
  and 0.74 ± 0.02 (60 → 72) cube steps with half the χ² of c − D/s² (353 against 770, 95 against 175); a free
  power is 2.3 to 2.4. But the value is set by the thinnest tori: without loop² 3 it is 0.57 and 0.52, and on
  loop² ≥ 7 alone 1.05 ± 0.10 and 0.42 ± 0.09, with asymptotes 0.2206 and 0.2081. **ξ = 0.4 to 1.05 cube steps
  depending on the classes fitted; this route does not give c_inf to better than 0.01.**
- **The capillary-wave term does much of the work among wide faces with one parameter, but its coefficient is not
  a constant.** κ = −1.37 ± 0.13 (wide, error inflated by √(χ²/dof)), −1.19 ± 0.11 (with the 0.015 floor). On the
  census classes with loop² ≥ 7 it is −1.01 with a jackknife error of ± 0.28 over the 11 classes (two classes of
  loop² 7 carry it: −0.77 and −1.17 without one or the other), and at fixed area it is −0.72 ± 0.05 (A = 48),
  −1.18 ± 0.03 (A = 60), −1.43 ± 0.03 (A = 72): it drifts with the area, which the form forbids. So κ lies
  somewhere between −0.7 and −1.5, and no comparison with the value −1 of an Ising interface can be drawn. The
  form forecasts the held-out A ≥ 105 classes best (largest residual 0.09 against 0.19). The massive form fits
  the wide faces slightly better in-sample with ξ = 0.95 ± 0.07 cube steps and a lower c (0.205), and
  under-forecasts every A ≥ 105 class (+0.03 to +0.19). The two differ by 0.005 in c; the wide data do not choose.
- **The second variable has the models' sign and about four times their size.** For the equal-area, equal-loop
  pairs both models give d ≥ 0 always and nearly the same number (+0.004 for P1 and P2, +0.0006 for P3), against
  the measured +0.0151 ± 0.0017, +0.0142 ± 0.0019, +0.0063 ± 0.0035: 6σ and 5σ low. Forecasts for every pair of
  research/shape3's plan, what of that experiment I had already seen, and which of its rows were in the tree
  when the forecast was committed, are in `PREDICTIONS.md` (B).

## Forecasts committed before results

`PREDICTIONS.md`: (A) empty patches on the 12 × 12 × 8 slab (commit 5dd18b9): c = 0.212 ± 0.015, σ > 0, σ = 0.34
per cube step of perimeter (0.15 to 0.6); the reviewer recomputed its numbers and confirmed that no empty-patch
data existed. (B) the wrap-around models on research/shape3's pairs; by commit order only P2 and Q63 are blind.
(C) the equilateral tori under three readings (commit 6c21dbd), with an addendum for the single-c readings.

## Three measurements that would shrink the uncertainty most

Costs from the recorded runs (`extras.py costs`; `gpu_facelaw/R15_s1_A10G.json`: 1,059 deaths in 1,800 s).

1. **Equilateral face tori**: n = 19, 21, 27, 28, 31, 37 columns (A = 57 to 111; lattices and forecasts in
   `PREDICTIONS.md` C), firewall channel resolved, 10⁵ face deaths each for A ≤ 84, 3 × 10⁴ at A = 93, 2,000 at
   A = 111, and 6 × 6 × 8 topped up to 2,000; about 3 GPU-hours. The equilateral torus has the longest shortest
   loop of its area, so this is the widest periodic lever there is. *Decides*, in the fit of a + cA + ρ√A to the
   nine tori (c to ± 0.0016, ρ to ± 0.026; now ± 0.0069 and ± 0.11): whether the slope of the constant-shape family
   falls (ρ > 0, now +0.25 ± 0.11), is flat (ρ = 0, c = 0.2121), or rises as the single-c readings with c = 0.2155
   to 0.2190 need (ρ = −0.05 to −0.11: 2 to 4σ from flat).
2. **Hull faces of equal area and different rim, with the corners matched.** The first version proposed
   truncated triangular faces; that changes the number of corners (3 → 6) and their angle (60° → 120°) together
   with the rim. Instead: pairs of hexagonal faces (sides a, b, a, b, a, b; six 120° corners) of equal area and
   different side ratio, two pairs, 10⁴ deaths per face type (± 0.01). *Decides* the sign and size of a per-rim-cell
   term apart from a per-corner one: the one-term rim reading needs −0.06 per rim cell (c = 0.232), the two-term
   readings with c ≤ 0.214 that have a rim term need +0.02 to +0.06, and the readings with a q/A or saturating
   correction need none.
   [conjectured geometry, not built] such faces occur on hulls cut by the eight {111} planes at two offsets (a
   truncated tetrahedron); their two side types meet neighbours at different dihedral angles (70.5° and 109.5°), so
   a pair must match the count of each or carry it as a second unknown, and the hull's small triangular faces die
   first, so hexagon deaths are counted as competing risks. Needs a vessel builder and its check against the engine.
3. **Hull A = 108 to 10⁴ deaths** (about 4.2 GPU-hours more at the recorded 2,118 deaths per hour), which
   measures the 84 → 108 slope to ± 0.0005. *Decides* one way (section 6 of the table): if the value stays at
   its present centre (slope 0.2182), 35 of the 36 single-c readings fail (the survivor: q/k with D/s, c = 0.220,
   p 0.013), the hull's own q/A, saturating and two-term forms fail, and the rim, log and q/k forms survive
   (c_hull = 0.2205 to 0.234): the hull's constant would then lie above 0.22 whatever the form. If the value
   comes down by 0.05 (slope 0.2161) all 36 still pass and nothing is decided. The present point is 1.5 to 2.0σ
   above the single-c readings.

Withdrawn: the slope of width 6 (6 × 7 × 8 to 800 deaths, 15 GPU-hours). It measures the 108 → 126 slope to
± 0.0023, and the readings differ there by 0.0005 to 0.004 (0.2072 to 0.2094 for c ≤ 0.214, 0.2099 to 0.2111 for
c ≥ 0.2155). More hull deaths at A = 135 or 165 would not decide either: the readings forecast 29.1 to 29.25 and
35.5 to 35.8.

## Where the analysis and the review differ

Points of substance on which my numbers are not the review's; both are given.

1. **What the single-c readings predict for the equilateral tori** (review §8.1). Review: "slopes rising from
   0.208 (n = 19) to 0.211 (n = 37)", about 3σ across the plan. Mine: 0.208 to 0.211 is c − D/s, the cost per cell
   of a strip of that width (the slope at fixed width); the local slope between equilateral tori is
   c − D/(2s) plus the offset's change, 0.2117 → 0.2136 for c = 0.2179 fitted to the three anchors; the slope
   difference across the plan is +0.0009 to +0.0018 (1.1 to 2.2σ at ± 0.0008), and the three-parameter fit
   separates these readings from flat at 2.0 to 4.1σ. The existing tori already put them 2.7 to 3.2σ from the
   6 × 6 run, which the review does not use. *Decides*: measurement 1 (criteria in `PREDICTIONS.md` C and its
   addendum).
2. **Hull A = 108 at 10⁴ deaths** (review §8.3: "separates the saturating reading from the others at 1 to 3σ
   only, so it is not decisive either"). Mine: that compares the readings with one another; against the data it is
   decisive in one of its two outcomes (measurement 3 above: 35 of 36 single-c readings fail if the centre
   stays). *Decides*: the run.
3. **Width 6** (review §8.3: the D/s reading predicts 0.2090 at width 6, 0.3σ from flat). Mine: 0.2090 is the
   periodic-only fit (D = 0.022); the single-c readings that pass with D/s have D = 0.034 to 0.048 and put the
   width-6 slope at 0.2099 to 0.2111, 0.2 to 1.7σ from the lower readings (0.2072 to 0.2094) at ± 0.0023. The
   conclusion is the same (withdrawn).

On everything else I checked (the hull one-term forms, the saturating form, the width laws, the joint matrix and
its penalties, the floors, κ by area and by jackknife, ξ by selection) my code reproduces the review's numbers to
the last digit quoted, and the write-up now follows it.

## Corrections after review (2026-11-14)

1. Verdict restated: one c is allowed from 0.207 to 0.219; the tension "+0.0109 ± 0.0010 at the least", "Δχ² 110
   to 238" as a general statement, and "one c only with two hull terms, p ≈ 0.01" are withdrawn. The model-free
   statement (hull local slopes above periodic within-width slopes) replaces them. The preference for the periodic
   value is labelled a judgement; the quoted number is now 0.213 ± 0.006 (a range) in place of 0.2085 ± 0.004.
2. Periodic c: 0.207 to 0.216 with a statistical error of about ± 0.003 once the width law is free (was 0.205 to
   0.212, ± 0.001); each value now names its fitting set (the capillary-wave 0.2108 and massive 0.2063 are from
   the 26 wide classes with the 0.015 floor, not the rectangular family).
3. Hull c: one-term forms q/k (0.2193 ± 0.0007) and q/A (0.2181 ± 0.0005) added, range 0.218 to 0.232; the
   saturating form (0.2156 ± 0.0004, all six sizes) and two more two-term forms added. "With four parameters the
   hull's c is free between 0.19 and 0.26" is replaced by the four values found.
4. Joint fits: the penalty is reported as a one-degree-of-freedom test with its p-value; the matrix has 84
   pairings (was 9).
5. κ = −1.01 ± 0.01 and the Ising comparison are replaced by the area dependence (−0.72, −1.18, −1.43) and the
   jackknife error (± 0.28); ξ is reported as 0.4 to 1.05 depending on the classes, and the loop route as not
   giving c_inf to 0.01 (was 0.005).
6. `PREDICTIONS.md` (B) lists the shape3 rows that were in the tree when it was committed (P3, T72, N72; only P2
   and Q63 were absent).
7. Measurement 3 (width 6) withdrawn; measurement 2 restated as corner-matched hexagonal pairs; a new
   measurement 3 (hull A = 108) with a design check; measurement 1 restated.
8. `load.py` keeps every CPU hull run (hull A = 108: 23.3764, was 23.3761; A = 135: 29.3413, was 29.3411); all
   outputs regenerated.
9. Out-of-sample statement amended: the four-parameter hull forms forecast A = 108 worse than the one-term ones.
10. The remark that a massive correction "predicts a fall" of the equilateral slope is dropped from the results;
    the review notes that the loop-deficit fits give a deficit of the other sign there. The forecasts of
    `PREDICTIONS.md` C stand as committed, with their forms stated there.

## Methods that failed, and why

- **Out-of-sample forecasting as an arbiter.** Every defensible one-term form passes; the held-out sizes are too
  imprecise.
- **Deciding "one c or two" by fitting.** The answer follows the forms chosen (penalty 0 to 1179); the first
  version of this page mistook the forms it had tried for the defensible set.
- **One global shape law for periodic faces** (capillary wave, loop sums with two kernels, shortest loop only, an
  added intercept term): all fail at the statistical errors, as research/shape2's laws did; a + cA is forced on
  lattices of different shape at different areas, and the unexplained 0.015 is ten error bars.
- **Reading c_inf off the loop dependence** (asymptote of the cost per cell against the shortest loop): unstable
  at 0.01 between pairs of areas and between selections of classes.
- **The massive form on the rectangular family alone**: degenerate (ξ → 0.14, g at its bound); three widths cannot
  fix a decay length, nor a width law (D = 0.022 ± 0.013 under 1/s).
- **Symmetric faces as a lever** (large A, cheap): the slope depends on the correction's form by 15% and its link
  to c_inf is a conjecture.

## Not checked

- No new run; nothing here tests the GPU kernel or the steppers. The hull values at A ≥ 108 and the slab values
  at A ≥ 96 come from one GPU implementation (ledger grade B−). The review asks whether the GPU kernel's
  settled-state test can miss "zombie" lives as research/shape3 found for ts.c; that would bias the large-A points
  of both families upward. I did not look.
- Thickness: every periodic value is for 8 layers. That 8 layers suffice at A ≥ 108 is not tested anywhere; one
  6 × 6 × 12 run of 600 deaths would test it.
- Soup transients and caps: ages below T0 are excluded for hulls (200) but not for slabs; the sources bound the
  effect at ≤ 0.005 in ln τ, which is larger than the statistical error of the best points. I did not re-derive
  those bounds. The 0.015 floor is a round number taken from the pair differences, not a fitted variance.
- The list of forms is still a list: 9 hull corrections and 7 periodic ones. A form outside it could move either
  end of the 0.207 to 0.219 range.
- The design check of measurement 3 moves one point and refits; it does not simulate the run. The hexagonal-face
  geometry of measurement 2 is derived on paper, not built.
- Loop² 4 tori are multigraphs and carry a tie-resolution bias of about −0.018 (research/shape2); they are in the
  thin set as measured.
- Classes pooled across codes (GPU, rep.c) assume equal hazards; the pooled χ² are printed by `load.py` (worst:
  3 × 6 × 8, 12.6 on 1).
- The reviewer did not recompute the massive lattice-sum fits, the symmetric-face fits, the 2D table or
  `patch_geom.py`; those rest on my code alone.
- The 2D relative was not fitted, only its local slopes printed. The mirror-cut hulls and research/shape3 were not
  used. The lifetimes of research/peeling's CPU slabs (A = 12 to 84) were not compared point by point.
- Forecast errors use the parameter covariance inflated by χ²/dof and treat points as independent.
- Whether "cost per cell" is the right asymptotic notion at all (an extensive large-deviation rate) is assumed, not
  tested; the empty-patch experiment is the first test of it for gump.

## Reproduce

    python3 research/constant/lat.py selftest            # lattice code against research/shape2's class tables
    python3 research/constant/load.py --check            # every point, and quoted values against data
    python3 research/constant/fit.py                     # the main table (100 s) -> out/main_table.txt
    python3 research/constant/shape_models.py tests      # wrap-around models (4 min) -> out/shape_tests.txt
    python3 research/constant/shape_models.py slopes     # cost per cell against the shortest loop; xi by selection
    python3 research/constant/shape_models.py kappa      # the capillary-wave coefficient by area, jackknife
    python3 research/constant/shape_models.py pairs      # pair forecasts -> out/pairs.txt
    python3 research/constant/eq_forecast.py             # equilateral tori under each reading -> out/eq_forecast.txt
    python3 research/constant/extras.py toy; python3 research/constant/extras.py equilateral
    python3 research/constant/extras.py costs            # recorded GPU death rates of the widest slabs
    python3 research/constant/patch_geom.py              # perimeter measures of a rhombic patch
