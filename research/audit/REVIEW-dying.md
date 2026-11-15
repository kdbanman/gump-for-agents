# Review of research/dying/, round 1: how a hull face dies

Adversarial review, 2026-11-15. Object: `research/dying/` at 616212f (README, `PREDICTIONS.md` at 75e5212, `data/`,
`research/figures/dying_face.png`). Round 2, in progress in the same directory, is not reviewed. Code and small
outputs in `research/audit/dying/`; bulk output in `research/scratch/audit_dying/` (git-ignored). Nothing is imported
from `research/dying/` or `research/theory/symmetric/`; `sd.c` was read, never compiled or run.

**Stepper.** `dy.c` is the earlier review's `st.c` (full, unreduced system; symmetric 0.4 soup drawn per orbit;
256 lanes; events checked every generation; Brent settled test) with three outputs added: the lane and generation
of every life record, the face cells of every lane every SAMPK generations, and 512 generations of face history
before each of the first 1,500 F/X deaths at age > 512. Geometry from `research/audit/symmetric/geo.py`.
Validated (`val.py` → `val_out.txt`, ALL OK): lane 0's whole live set against `reference/oracle.py` at every one of
600 generations for v11c, v13c and v12v (R = 11 and 13 cube-centred, R = 12 vertex-centred) × c1, csz, c2v, d2h;
and `dy`'s lives file byte-identical to `st`'s for the same arguments on all twelve systems (20,000 generations ×
256 lanes). In the analysis every dumped history is checked against the samples written independently at the same
lane and generation (32,000 matches, no mismatch), lag 0 has the dying face empty and lag 1 has no face empty.

Plan fixed before the runs (ae387dd; part 3 in the commit after it, before its run). Seeds 9201–9205, 9211–9214,
9221–9224.

    gcc -O3 -march=native -o research/scratch/audit_dying/st research/audit/symmetric/st.c
    bash research/audit/dying/plan.sh 1; bash research/audit/dying/plan.sh 2    # two cores, ~1 min each (builds dy)
    bash research/audit/dying/plan.sh 3                                           # second csz job, 20 s
    python3 research/audit/dying/val.py        # -> val_out.txt (40 s)
    python3 research/audit/dying/ana.py        # -> ana_out.txt (1 min): every number below unless marked
    python3 research/audit/dying/l6check.py    # -> l6check_out.txt

Conventions as the study's: canonical face q = d⊙(p − c); row k along edge a is q_a = k − 1; row 1 (12 cells at
R = 11 c, apexes included) is shared with the neighbouring face. "Rim row occupancy" excludes the two apexes, as
the study's panel C does. Errors on stationary quantities are from per-lane means (lanes independent); on death
quantities a bootstrap over deaths or binomial.

## Summary

| claim | verdict |
|---|---|
| 1. A tied edge is thinner at all times; −2.5 cells per tied edge, "mirroring the equal steps of ln τ"; 0.86 per live cell, twice 0.436 | **confirmed with corrections.** The rim depletion reproduces exactly and generalises. The equal steps do not: P̄ = 31.25, 28.90, 26.28, 23.50 (± 0.004, 0.01, 0.01, 0.02), steps −2.35, −2.62, −2.77. "Almost all in the rim row" holds cube-centred only. The cost per live cell is not a constant of the face: it is 0.93 → 0.77 along the ladder, 0.40 per cell gained by size, 0.23 by centring. |
| Null control | **sound for c1–c2v; D2h with a caveat.** Stationary by age 64–128 in every group. Conditioning on surviving ≥ 64 generations shifts P̄ by ≤ 0.03 cells (c1–c2v) and by 0.26 (1.1%) in D2h. Excluding settled lives matters only for D2h (36.5% of old living states; with them P̄ = 20.40). |
| 2. No erosion from an edge; a uniform fade; plunge 6–7 in all groups | **confirmed for the mean and for edges; "fades everywhere at once" is not true of single deaths.** A third of single deaths at half population are more lopsided than 95% of matched, uniformly thinned stationary faces (9–11% in a lag-64 control). The lopsidedness does not stay on one side beyond what thinning implies. Plunge medians 6, 6, 7, 7. |
| 3. The c1 neighbour is dragged down (band 0.21 at death) | **numbers confirmed, mostly a tautology.** The neighbour's shared row *is* the dying face's rim row (12 identical cells, checked). 10 of the band's 16 cells are the dying face's own. What survives: the neighbour's own row 2 falls to 0.56–0.61 of stationary, and the rest of it stays at 0.95. Of the whole neighbour's 23.5% loss, 17.5 points are the shared cells. |
| 4. Scoring of L2–L7 | **definitions were fixed before the data; scores stand, with two notes.** L2, L3, L5, L6 (csz), L7 fail under every band choice. L4 becomes *undecided* with the 12-cell band (0.790 ± 0.028 against 0.8). "Against the reading" (c1 ratio < 1.1) holds with the registered band (1.063) and fails with the 12-cell band (1.222). L5a and L5b were partly decided by the shared cells; without them L5a would hold (0.951). |

## Claim 1: the stationary face

### R = 11 cube-centred, the study's vessel (v11c)

| | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| P̄, this review (study null) | 31.25 ± 0.004 | 28.90 ± 0.01 | 26.28 ± 0.01 | 23.50 ± 0.02 |
| P̄, study | 31.29 ± 0.03 | 28.83 ± 0.04 | 26.29 ± 0.07 | 23.77 ± 0.15 |
| rim row (no apex) free / tied | 0.512 | 0.489 / 0.349 | 0.466 / 0.323 | — / 0.298 |
| study (README) | 0.51 | — / 0.35 | — / 0.32 | — / 0.30 |
| row 2 free / tied | 0.434 | 0.410 / 0.395 | 0.385 / 0.365 | — / 0.337 |

- **Rim depletion: confirmed exactly.** Measured against c1, the loss by row from the nearest tied edge (rows 1–4)
  is csz −1.77, −0.23, −0.24, −0.08; c2v −4.01, −0.52, −0.33, −0.08; D2h −6.67, −0.85, −0.22, −0.01. The lead's
  "−1.8 of −2.5 in the rim row" reproduces. The rim row's loss per tied edge is −1.77, −2.01, −2.22; per tied rim
  cell that is −0.148, −0.167, −0.185.
- **The steps are not equal.** They are −2.35, −2.62, −2.77 (errors ≈ 0.02), growing with the number of tied edges,
  while the ln τ steps are −2.18, −2.17, −2.12. Against the study, c1 and c2v agree. csz differs by +0.07 and D2h by
  −0.27, 1.7 and 1.8 of the study's σ. The study's own errors (steps 2.46 ± 0.05, 2.54 ± 0.08, 2.52 ± 0.17) could
  not have shown equality to the precision the README states ("as equal as the ln τ steps").
- **ln τ per live cell lost:** whole ladder 0.835 (lead 0.86 with the study's D2h). Step by step it is 0.93, 0.83,
  0.77, so it is not constant.

### Other vessels (stationary sampling only; ln τ from the symmetric study)

| vessel | P̄ c1, csz, c2v, D2h | steps | Δln τ / ΔP̄ (ladder; steps) | rim row, free / tied |
|---|---|---|---|---|
| R = 13 c (A = 84; rim 14 cells) | 42.45, 39.81, 36.87, 33.28 (± 0.01–0.08) | −2.64, −2.94, −3.59 | 0.885; 1.00, 0.90, 0.79 | 0.523 / 0.361, 0.338, 0.314 |
| R = 12 v (A = 63; rim 6 cells) | 34.20, 31.60, 28.54, 24.90 (± 0.01–0.02) | −2.60, −3.06, −3.64 | 0.714; 0.82, 0.71, 0.64 | 0.550 / 0.362, 0.325, 0.288 |

(ln τ: R = 13 c 18.141 (GPU), 15.506, 12.857, 10.022; R = 12 v 14.310, 12.182, 9.997, 7.673.)

- **Depletion per tied rim cell is the same in both cube-centred sizes.** The rim row loses 0.149, 0.167, 0.186 per
  tied rim cell at R = 13 against 0.148, 0.167, 0.185 at R = 11. The total loss per tied rim cell is 0.188, 0.199,
  0.218 against 0.196, 0.207, 0.215. The loss per tied edge therefore grows with the rim's length (csz 2.35 → 2.64).
  It is "about 2.5" only at R = 11.
- **Vertex-centred faces carry the loss on two rows.** Their rim row has 6 cells and row 2 has 12. In csz the loss
  is −1.13 on row 1 and −1.08 on row 2 (c2v −2.70, −2.42; D2h −4.72, −4.06). "Almost all of the loss sits in the rim
  row" is a cube-centred statement. Per cell of rows 1–2 (18 cells in both centrings), csz loses 0.111 (c) and
  0.123 (v).
- **"0.86 per live cell lost, twice the 0.436 per live cell" does not stand as an exchange rate.** 0.436 is an
  average (ln τ / P̄), not a marginal. The marginals now in hand are as follows:
  - Growing the c1 face from R = 11 to 13 c gives Δln τ / ΔP̄ = 4.507 / 11.20 = **0.40** per stationary live cell.
  - Re-centring at equal area (c1, R = 11 c → R = 12 v) gives 0.676 / 2.95 = **0.23**.
  - Tying an edge costs **0.64–1.00**, depending on vessel and rung.

  So ln τ is not a function of P̄. For example, R = 12 v csz has more live cells (31.60) than R = 11 c c1 (31.25)
  and lives 1.45 shorter in ln τ. A cell lost at a tied edge costs about twice what a cell gained by growing the
  face buys. The "twice" survives only in that form, as one measurement at two sizes. This also answers the
  README's surprise 2 ("whether the ladder is a function of the stationary state … at A = 84"). At the level of the
  mean it is not: at A = 84 the ln τ steps are −2.64, −2.65, −2.84 while the P̄ steps are −2.64, −2.94, −3.59.

### The null control

`ana.py`, "Null control" block (v11c; samples every 64–256 generations of every lane):

- **Stationarity.** Among lives that do not settle, the mean face population is flat from age 64–128 on in all four
  groups (D2h: 23.93 at age 0–64, then 23.22–23.31 from 64 to 4,096). Generation 512 is well past the transient.
- **Conditioning on the future.** States within 64 generations of a death are low (c1 30.36, csz 27.77, c2v 23.69,
  D2h 19.52); they are the run-ups. Dropping them, as the study's null does, raises P̄ by < 0.01 (c1, csz), 0.03
  (c2v) and 0.26 (D2h; 23.24 → 23.50). Every "relative to stationary" number of the study is biased upward by at most
  about 1%, and only in D2h. That is small against the effects claimed.
- **Settled lives.** None in c1 and csz; 1.2% of old living states in c2v; **36.5% in D2h** (study: 27% of
  exposure; protocols differ). Their face population is 15.45 ± 0.07. With them D2h's P̄ is 20.40, and the D2h
  step becomes −5.76. Deaths come only from lives that do not settle, so the study's choice is the right comparator
  for its death curves. The ln τ it is set beside, however, counts the exposure of settled lives (the D2h rung's
  estimator spread, 7.02–7.29, is that). The README should say that the D2h point of the P̄ ladder and the D2h rung
  of the ln τ ladder are not taken over the same lives.

## Claim 2: how a death runs

**Means: confirmed.** From 1,000 / 1,500 / 1,503 / 1,500 independent deaths (c1, csz, c2v, D2h), face over P̄:

| lag | 20 | 16 | 8 | 4 | 1 |
|---|---|---|---|---|---|
| c1 | 0.985 | 0.960 | 0.693 | 0.330 | 0.051 |
| csz | 0.963 | 0.921 | 0.640 | 0.303 | 0.055 |
| c2v | 0.903 | 0.831 | 0.562 | 0.302 | 0.059 |
| D2h | 0.821 | 0.756 | 0.520 | 0.312 | 0.066 |

Median plunge 6, 6, 7, 7 (quartiles 4–8, 4–9, 4–10, 4–12), none censored (study: identical medians and quartiles
except c2v 4–11).

- **No edge goes first, confirmed.** Relative to its own stationary value the tied band tracks the free band within
  0.01 at every lag 1–16 (csz lag 4: tied 0.322, free 0.312, interior 0.277; c2v 0.309, 0.315, 0.288). Bands lag the
  interior slightly at lags 1–4 on both kinds of edge.
- **L6 as registered, csz:** 0.255 ± 0.011 (job 1) and 0.226 ± 0.008 (job 2, 3,000 deaths). Pooled 0.236 ± 0.006,
  against the study's 0.211 ± 0.007 (2.7σ apart; the two jobs here differ by 2.1σ). It is far below 0.45 either way.

**Single deaths are not uniform fades.** I took each death at the last time its population crossed f·P̄. There I
measured the distance between the centroid of its live cells and the centroid of the stationary profile (the
"dipole"). The null is that same distance for stationary states (same group) from which cells were removed
uniformly at random down to the same count. That is exactly a uniform fade that keeps stationary correlations.

| | f = 0.75 | f = 0.5 | f = 0.25 | control: lag 64 |
|---|---|---|---|---|
| share of deaths above the null's 95th percentile (c1, csz, c2v, D2h) | 0.17, 0.17, 0.20, 0.20 | **0.34, 0.32, 0.34, 0.39** | 0.35, 0.37, 0.36, 0.36 | 0.09, 0.10, 0.11, 0.11 |
| above the 99th | 0.05–0.07 | 0.14–0.17 | 0.17–0.20 | — |
| mean dipole, deaths / matched null (doubled units; the face's side is 15.6) | 1.4–1.9 / 1.1–1.4 | 2.2–2.8 / 1.3–1.7 | 3.3–3.8 / 1.9–2.2 | |

The lag-64 control shows the null runs about twice hot (9–11% instead of 5%). Against it, deaths at half
population are lopsided about three times as often as healthy faces. Within a death, the cells on the rich side of
the 0.75 P̄ state outlive those on the poor side: per death, the correlation between position along the dipole and
the last generation alive is 0.195 ± 0.012, 0.169 ± 0.010, 0.163 ± 0.011, 0.172 ± 0.012. With the dipole of another
death the baseline is 0.00 ± 0.01.

**But not one hole spreading from a fixed side.** The direction at 0.25 P̄ agrees with that at 0.75 P̄ with mean
cosine 0.53, 0.52, 0.51, 0.52. Thinning the death's own 0.75 state at random to the 0.25 count gives 0.57, 0.62,
0.65, 0.67. The deficit wanders a little more than thinning alone would make it. The passage from 0.75 to 0.25 P̄
takes a median of 3–4 generations (D2h 7). The picture is a fast, uneven collapse whose depleted side is set early
and shifts as cells are reborn. It is neither a uniform fade nor a steady front, and the depleted side is not the
tied edge (L6 and the relative bands).

## Claim 3: the neighbour of a dying c1 face

Checked geometrically for every face and edge: the neighbour's row q_a = 0 is the same set of 12 cells as the dying
face's own row q_a = 0. So the study's neighbour band (16 cells) holds 10 of the dying face's own cells, which are
empty at lag 0 by definition.

Neighbour over its own stationary value (c1, mean of the three neighbours; `ana.py` "Neighbour" block):

| lag | 0 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| whole face | 0.765 | 0.762 | 0.771 | 0.821 | 0.904 | 0.981 |
| band16 (study's) | 0.207 | 0.227 | 0.278 | 0.442 | 0.727 | 0.956 |
| shared row (the dying face's own cells) | 0 | 0.058 | 0.131 | 0.346 | 0.693 | 0.948 |
| **row 2 (neighbour's own, along the edge)** | 0.613 | 0.559 | 0.567 | 0.629 | 0.787 | 0.955 |
| neighbour minus the shared row | 0.928 | 0.911 | 0.906 | 0.922 | 0.949 | 0.987 |
| beyond row 2 | 0.963 | 0.951 | 0.945 | 0.955 | 0.967 | 0.991 |

Study: band 0.21 and whole face 0.77 at lag 0. Both reproduce.

What survives is a real but local drag. The neighbour's own strip next to the edge (6 cells) falls to 0.56 of
stationary. The rest of it hardly moves (0.95). Of the whole face's 23.5% loss at lag 0, 17.5 points are the shared
row (5.47 of 31.25 stationary cells); about 6 points are the neighbour's own. Free neighbours in csz and c2v behave
the same (row 2 at 0.52–0.57, without the shared row 0.85–0.90). "Holding up" is refuted. "Dragged down" is true of
one row; "the whole neighbour face loses 23%" is mostly bookkeeping. Panel A's dashed curve ("c1 neighbour: its
band on the shared edge") is mostly the dying face's own rim and should be replaced by row 2.

## Claim 4: the forecasts

**Order.** PREDICTIONS.md was committed in 75e5212 at 04:08:01. `sd` was built at 04:08:42, and every lives, dump
and null file is stamped 04:09:06–04:09:30 (`research/scratch/dying/`). Between 75e5212 and 616212f the file only
gained the dated "Notes added after the data". The definitions in `load.py` and `analyze.py` match the registered
ones: band, interior, lag 0, the null with its 64-generation and settled exclusions, L5's lags 1–16, L6's centroid,
and L7's censoring.

**Rescoring with this review's deaths, both bands** (lag 4, raw band/interior; "rel" = over the null's ratio):

| | registered band (16) | corner-free band (12) | score |
|---|---|---|---|
| L2 c1 pooled ≥ 1.5 | 1.063 (study 1.076 ± 0.018) | 1.222 (edges 1.18–1.29; lead 1.22–1.27) | failed either way |
| L3 csz z < 1.2; x/z, y/z ≥ 1.3 | 0.818; 1.21, 1.22 | 0.934; 1.23, 1.23 | failed either way |
| L4 D2h all in 0.8–1.2 | 0.715–0.765 (study 0.697–0.721) | 0.790 ± 0.028, 0.801, 0.843 | failed; **undecided** with band12 (registered rule: flips within 1σ) |
| L5a, L5b | 0.895, 0.682 (study 0.893, 0.668) | — | failed; without the shared cells L5a = 0.951 (holds), L5b on row 2 = 0.778 (fails) |
| L6 csz 0.45–0.70 | 0.236 ± 0.006 pooled | — | failed |
| L7 | medians 6 and 7 | — | failed |
| "against the reading": c1 ratio < 1.1 | 1.063 (met) | 1.222 (**not met**) | depends on the band |
| K4 D2h < 1 | 0.72–0.77 | 0.79–0.84 | held either way |

**Which band is fairer?** For a raw ratio, the 12-cell band. The 16-cell band includes the two cells at each end
next to the corner (q_a ≤ 1 and q_b ≤ 1). They border an apex, count in two bands, and have low stationary
occupancy, so they pull every raw band ratio down by about 0.12. That is why the stationary c1 ratio is 0.925
(band16) but 1.04 (band12). The question L2 asks ("does the rim outlive the interior?") is best answered against
the stationary ratio, and that answer barely depends on the band: c1 1.11–1.20 (band16), 1.13–1.24 (band12). The
registered score should stand as registered. The README should report the null-normalised ratio beside it, and
should note that the first "against the reading" criterion is met only because of the corner cells.

## What the README should change, most important first

1. "The stationary population falls in equal steps … as equal as the ln τ steps" → "falls by 2.35, 2.62, 2.77 cells
   per tied edge (independent review; steps grow, the ln τ steps do not); the loss per tied *rim cell* is the same
   at R = 11 and 13 (0.19–0.22)". Drop "mirroring" from any summary.
2. "In plain words: … fades everywhere at once" and "keeps the face's stationary profile" → "on average the face
   fades everywhere at once; single deaths are uneven (a third at half population are more lopsided than 95% of
   equally thinned stationary faces), with no preference for the tied edge".
3. Claim 3 → "the neighbour's own row along the shared edge falls to about 0.56 of stationary; the rest of it stays
   at 0.95. (The band and whole-face numbers include the 12 shared cells, which are the dying face's own.)" L5a/L5b
   should carry that caveat in the scoring table.
4. The ln τ-per-cell comparison should not be stated as "twice the 0.436 per live cell". It should say: "0.64–1.00
   per tied-edge cell against 0.40 per cell gained by size and 0.23 by centring: ln τ is not a function of P̄".
5. The table's lag-4 ratios should be given null-normalised beside the raw ones, with a note that the band includes
   corner cells. "Against the reading, first criterion met" should note that it flips with the band.
6. The D2h stationary value should state that it excludes the 27–37% of exposure in settled lives, which the ln τ
   rung includes.

## Not checked

- The layers beneath the face (s = 9, 7), the last-alive maps and the relative-deficit L6 (`explore.py`): not
  recomputed.
- Deaths only at R = 11 c. R = 13 c and R = 12 v were sampled stationary only, so claims 2–4 are not tested there.
- The study's 11,930 dumped histories and `validate.py` were not rerun. This review checks the study's numbers by
  independent replication, not by rereading its data.
- c2e and the remaining groups (O_h, T, …) were not run. The mechanism for the rim depletion (paired counts) was not
  tested.
- The dipole is one statistic of lopsidedness. Other shapes of depletion (a ring, a band through the middle) were
  not tested for, and the matched-thinning null is mildly anti-conservative (the lag-64 control, 9–11%).
- The 1.7–1.8σ differences in csz and D2h P̄ and the 2.7σ difference in L6 between this review and the study were
  not resolved. The protocols differ (events every generation here against every 4; Brent against ladder
  snapshots; samples every 64–256 generations here against 10 per job).
