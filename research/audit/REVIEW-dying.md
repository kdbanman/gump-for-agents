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

---

# Round 2: excursions, births, lopsidedness, A = 84

Object: `research/dying/README.md` from the round-2 "Short answer" (line 171) on, the "Round 2" block of
`PREDICTIONS.md` (6d40e72), commits 3bf2f21 and 4b41de0, `data/r2_*.csv`, `research/figures/dying_excursions.png`,
and the lead's round-2 lines in `research/audit/dying_lead_check.py`. Round 3 is not reviewed. `ex.c` and
`round2*.py` were read, never run or imported.

**Own code and runs.** `ex2.c` is round 1's `dy.c` plus an online excursion table:
- every face orbit's population P (one face per orbit), every generation;
- excursions as the study defines them (start below P̄ after a generation at or above it, both at age > 512; end
  recovered, dead or censored);
- the tally is kept per life and added, at the life's end, to the table of that life's end type, so settled lives
  can be put in or left out afterwards.

Thresholds are the study's P̄ (31.29, 28.83, 26.29, 23.77), which give the same integer thresholds as this review's
own P̄. The lives file is byte-identical to `st.c`'s (checked on v11c d2h, 20,000 generations); the dynamics code is
`dy.c`'s, validated against the oracle in round 1.

Runs, all with fresh seeds, 256 lanes, events every generation and the Brent settled test:
- seeds 9301–9304 at R = 11 c: c1 1.6 M generations, csz 0.8 M, c2v and D2h 0.4 M each;
- seeds 9311–9314 at R = 13 c: stationary samples, 300,000 generations.

Births, survival and lopsidedness use round 1's death histories (seeds 9201–9204) and samples. The plan was
committed before the runs (b615744).

    bash research/audit/dying/plan.sh 4; bash research/audit/dying/plan.sh 5     # two cores, ~4 min each
    python3 research/audit/dying/ana2.py     # -> ana2_out.txt: A tables, tail windows, D fits, B ratios, C rates
    python3 research/audit/dying/ana2b.py    # -> ana2b_out.txt: lead's tail fit on these tables, births against own P,
                                             #    lopsidedness at matched k, the fit with three D2h lifetimes

## Summary (round 2)

| claim | verdict |
|---|---|
| 1. ln τ = −ln(ν q) at every level; reproduces the four lifetimes | **Confirmed, but it is bookkeeping, not a test.** Every death ends an excursion, so ν·q is the death rate up to censoring. c1, csz, c2v: 13.614, 11.473, 9.275 at every level within 0.02 (study 13.632, 11.454, 9.274). D2h depends on how settled lives are counted: 7.32 with them (Brent detection; censoring up to 13% at p = 0.2, so −ln(νq) wanders over 7.20–7.34), **6.86 without them** (exact at every level), and the study's 7.168 with its ladder detection. |
| 2. Dips to 0.7 P̄ about equally frequent; groups part below 0.6 | **Confirmed, with a crossover the README omits.** ln ν(0.7) = −4.164, −3.802, −3.779, −3.883 (D2h without settled lives −3.714); study −4.16, −3.80, −3.77, −3.74. At 0.9 the order is reversed: c1 is the most frequent (−2.31), D2h the least (−2.79). |
| 3. p* = 0.08 P̄ in c1; 0.12, 0.15, 0.25; q(0.5) = 0.0008 | **Confirmed.** p* = 0.079 (2.48 cells), 0.114, 0.152, 0.245 (0.265 without settled lives). q(0.5) = 0.000824 ± 0.000013. |
| 4. Tail Gaussian, then straight; 15.6, 12.6, 9.2, 5.5 = 5.5 + 3.4 per free edge | **Slopes reproduce exactly. "Straight" is an approximation. "Per free edge" is fragile.** Lead's fit on fresh seeds: 15.55, 12.57, 9.19, 5.51, line 5.68 + 3.35. There is no break at P̄/2: the slope per cell drifts smoothly. Steps per free edge range over 3.0–4.5 with window and settled lives. |
| 5. Births fail before survival | **Confirmed; much of it is the face's own population.** Lag 16: births 0.911 ± 0.012, survival 0.988 ± 0.005. Lag 8: 0.481, 0.882 (study 0.903/0.983 and 0.454/0.877). Stationary births depend strongly on P and survival does not. Beyond what its own P predicts, births still fall first, but by less (c1 lag 8: 0.61 against 0.77 predicted). |
| 6. Chance-low faces as lopsided as dying ones (1.59 vs 1.61) | **c1: confirmed and stronger. D2h: not confirmed.** Thinned ratios at P ≤ 0.6 P̄: c1 1.53 ± 0.03, D2h 1.51 ± 0.03. Deaths at t_h: 1.60 ± 0.02, 1.73 ± 0.02. At matched count, c1 dying faces are *less* lopsided than chance-low ones; D2h dying faces are *more*. |
| 7. A = 84 state; ln τ = 3.43 + 0.582·P̄²/(2σ²) within 0.31 | **Numbers confirmed; the fit is real but weakly tested.** Own fit: 3.42 + 0.584, max residual 0.31, leave-one-out max 0.50; it predicts the GPU's c1 at A = 84 as 18.33 (18.141). P̄/σ fits to 0.42 and P̄ alone to 2.60. a + b·A + c·P̄ (no σ) fits to 0.27. The D2h estimator moves the fit between 0.23 and 0.50. |
| 8. Scoring of A1–A3, B1, C1, D1, D2 | **Definitions were fixed before the data; every score reproduces.** |
| 9. Constant price per cell below half; clump and hole; free edges raise the price | **Partly.** For: a near-constant price over 3–12 cells, thin faces lopsided, price higher with free edges. Against: no change of regime at P̄/2, no additivity in free edges, and in c1 the faces that die are less clumped than those that recover. |

## Claims 1 and 2: the excursion table, independently

`ana2.py`, block A. Errors in ln ν are 1/√n, under 0.015 everywhere; q errors are binomial.

| p | c1 ln ν, q | csz | c2v | D2h (all lives) | D2h (no settled lives) |
|---|---|---|---|---|---|
| 0.9 | −2.311, 1.23e−5 | −2.527, 1.3e−4 | −2.620, 1.28e−3 | −2.785, 0.0105 | −2.615, 0.0141 |
| 0.7 | −4.164, 7.9e−5 | −3.802, 4.7e−4 | −3.779, 4.1e−3 | −3.883, 0.032 | −3.714, 0.042 |
| 0.5 | −6.513, 8.2e−4 | −5.819, 3.5e−3 | −5.185, 0.0168 | −5.059, 0.106 | −4.890, 0.137 |
| 0.3 | −9.365, 0.0143 | −8.312, 0.0425 | −7.213, 0.129 | −6.032, 0.296 | −5.859, 0.361 |
| 0.1 | −12.415, 0.302 | −10.955, 0.597 | −8.952, 0.728 | −7.198, 0.892 | −6.791, 0.916 |
| ln(E/D) | 13.615 ± 0.016 | 11.474 ± 0.011 | 9.275 ± 0.008 | 7.318 ± 0.005 | 6.855 ± 0.005 |

The study's table agrees with this one within 0.02 in ln ν for c1, csz and c2v at every level shown. Its D2h values
lie between the two D2h columns.

**What the D2h column means.** With settled lives counted:
- the exposure includes generations in which the face sits frozen or periodic at low P (time-averaged P over the
  D2h exposure is 20.31 with them, 23.25 without);
- excursions that run into a settling state are censored, up to 12.8% of excursions at p = 0.2, so there ν·q is not
  the death rate (−ln(νq) = 7.20 against ln(E/D) = 7.32).

Without them the identity is exact and ln τ_face = 6.86. The study's 7.168 lies between because its ladder detects
settling sooner than this review's Brent test.

Every D2h number of round 2 that involves exposure carries this 0.2–0.45 ambiguity: ln ν, ln τ, the last ladder
step, and the D2h point of every fit. Within one estimator the identity is exact, so the identity cannot decide
which estimator is right.

## Claim 3

p* is where q crosses 1/2, by linear interpolation on the 0.05 grid. It is 0.079, 0.114, 0.152 and 0.245 (0.265
without settled lives); in cells, 2.48, 3.29, 4.01 and 5.82.

On the integer grid the crossing lies between 2 and 3 live cells in c1 and csz (c1: q(min ≤ 2) = 0.505,
q(min ≤ 3) = 0.302). It lies between 3 and 4 in c2v, and between 4 and 5 in D2h (5 and 6 without settled lives).

## Claim 4: the tail of ln ν

**The lead's numbers reproduce on fresh seeds.** With the lead's method (an unweighted line through ln ν(p) for
p = 0.10, 0.15, …, 0.45) the slopes are 15.55, 12.57, 9.19 and 5.51 per unit p. Per live cell that is 0.497,
0.436, 0.350 and 0.232. The line across groups is 5.68 + 3.35 per free edge, maximum residual 0.19
(`ana2b.py` part 1).

**Not a straight line, though close to one.** On the integer grid, a straight line through c1 over 0.10–0.45
leaves residuals of +0.13 at both ends and −0.25 in the middle; the ln ν errors there are 0.001–0.009.

The local slope per live cell in c1, from the density of excursion minima (independent counts), by window of k:

| k | 1–4 | 3–6 | 5–8 | 7–10 | 9–12 | 11–14 | 13–16 | 15–18 | 17–20 |
|---|---|---|---|---|---|---|---|---|---|
| slope per cell | 0.62 | 0.51 | 0.51 | 0.49 | 0.48 | 0.45 | 0.42 | 0.39 | 0.34 |

The other groups behave the same way (`ana2.py`, "tail shape"). There is no corner at half the mean: the slope
changes smoothly from the Gaussian-like top down to about 3 cells, then steepens again. "Straight below half" is a
fair description of 0.1–0.4 P̄ to within ±0.25 in ln ν, but it is not a second regime.

**"5.5 + 3.4 per free edge" depends on the window and on the estimator.** Steps per free edge (c1→csz, csz→c2v,
c2v→D2h):

| window | steps | D2h slope per unit p |
|---|---|---|
| 0.10–0.45 | 2.98, 3.38, 3.68 | 5.51 |
| 0.05–0.30 | 2.96, 4.18, 3.40 | |
| 0.20–0.50 | 3.12, 3.09, 3.52 | |
| 0.10–0.45, no settled D2h lives | 2.98, 3.39, 4.19 | 4.99 |
| 0.05–0.30, no settled D2h lives | 2.96, 4.22, 4.53 | 3.79 |

The increments mostly grow along the ladder and spread over 3.0–4.5. As with round 1's population steps, "equal
steps" describes one window and one estimator. What is robust is the ordering: the price per cell is highest in c1
and falls with each tied edge.

## Claim 5: births and survival

Births per empty cell and survival per live cell on the dying face, each over its stationary rate (from lags
256–500 of the same histories; 1,000–1,500 deaths per group; `ana2.py` block C):

| | lag 40 | 16 | 8 | 4 | t_8 |
|---|---|---|---|---|---|
| c1 births / survival | 1.007 / 1.001 | 0.911 ± 0.012 / 0.988 ± 0.005 | 0.481 / 0.882 | 0.139 / 0.623 | 0.373 / 0.634 |
| D2h | 0.919 / 0.994 | 0.631 / 0.988 | 0.364 / 0.934 | 0.175 / 0.715 | 0.503 / 0.712 |

The study's values (c1 0.903/0.983 at lag 16, 0.454/0.877 at lag 8, 0.377/0.639 at t_8; D2h births 0.93 at lag 40)
all reproduce.

**What it means** (`ana2b.py` part 2). In stationary faces, births per empty cell depend strongly on the face's own
population: 0.60 of the mean at 0.6 P̄, 0.86 at 0.8 P̄, 1.15 at 1.2 P̄. Survival does not: 0.98–1.02 over the same
range. So a face that has simply lost cells already shows "births failing first".

Measured against the rates its own P predicts, the dying face is still low in both, and births are hit harder
(deaths whose P has a stationary bin):

| | births observed / predicted | survival observed / predicted |
|---|---|---|
| c1, lag 16 | 0.927 / 0.968 | 0.988 / 1.001 |
| c1, lag 8 | 0.61 / 0.77 | 0.89 / 1.00 |
| D2h, lag 16 | 0.632 / 0.698 | 0.988 / 1.012 |

The surroundings (the layer beneath) thin first, and births feel it first. The README should say that most of the
birth deficit at a given lag comes from the face's own lower population, and give the excess beyond it.

## Claim 6: lopsidedness

S is the distance from the live-cell centroid to the ρ-weighted centroid: the study's statistic, and round 1's
"dipole". The ratio below is S over the same S for stationary faces thinned at random to the same count, 20 per
state (`ana2.py` block B):

| | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| chance-low stationary faces, P ≤ 0.6 P̄ (mean k) | 1.53 ± 0.03 (16.2) | 1.66 ± 0.03 (14.7) | 1.58 ± 0.03 (12.5) | 1.51 ± 0.03 (11.2) |
| stationary faces, P in 0.6–0.8 P̄ / 0.8–1.2 P̄ | 1.25 / 1.06 | 1.23 / 1.13 | 1.32 / 1.11 | 1.32 / 1.12 |
| living states within 64 generations of death, P ≤ 0.6 P̄ | 1.76 ± 0.10 (11.9) | 1.73 (11.4) | 1.91 (9.2) | 1.91 (8.3) |
| deaths at t_h (mean k) | 1.60 ± 0.02 (11.7) | 1.59 (10.9) | 1.64 (10.4) | 1.73 ± 0.02 (8.8) |

Lopsidedness grows steadily as a face thins. The study therefore compares faces at different counts: about 16
cells for chance-low faces, against about 12 (c1) and 9 (D2h) for deaths at t_h.

At matched count (null reweighted to the deaths' k, no thinning; `ana2b.py` part 3), S for dying faces against
chance-low stationary faces:

| k | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| 5–9 | 2.47 ± 0.08 vs 3.09 | 2.41 vs 2.97 | 2.65 vs 2.82 | 2.94 ± 0.04 vs 2.70 |
| 10–12 | 2.21 vs 2.43 | 2.15 vs 2.36 | 2.34 vs 2.31 | 2.61 vs 2.29 |

The chance-low faces are, by the null's definition, states whose life lasted at least 64 more generations. So at
equal count, in c1 and csz the faces about to die are *less* lopsided than those that recover; in D2h they are
*more*.

- **"Not a mark of dying" holds for c1.** The opposite is closer to true there: a thin face that keeps a clump tends
  to come back.
- **It does not hold for D2h.** The study's own D2h pair (1.51 against 1.76) already differs by 0.25.
- **Round 1 agrees.** This review's round-1 finding (single deaths lopsided against uniform thinning) and the
  study's measure the same thing: depletion, not dying.

## Claim 7: A = 84 and the (P̄, σ_P) fit

| | c1 | csz | c2v | D2h |
|---|---|---|---|---|
| A = 84 P̄, this review | 42.45 ± 0.004 | 39.80 ± 0.01 | 36.86 ± 0.01 | 33.58 ± 0.03 |
| A = 84 P̄, study | 42.49 ± 0.09 | 39.81 ± 0.09 | 36.86 ± 0.10 | 33.48 ± 0.12 |
| A = 84 σ_P, this review / study | 5.961 / 5.96 | 6.194 / 6.18 | 6.552 / 6.50 | 7.21 ± 0.05 / 7.05 |
| A = 63 σ_P, this review / study | 5.248 / 5.24 | 5.499 / 5.56 | 5.900 / 5.96 | 6.31 ± 0.02 / 6.37 |

Fits over the eight points (`ana2.py` block D). Columns: maximum residual; maximum leave-one-out residual; c1 at
A = 84 predicted from the other seven (the GPU measured 18.141).

| form | own numbers | study's numbers |
|---|---|---|
| a + b·P̄²/(2σ²) | 0.31, 0.50, 18.33 (a 3.42, b 0.584) | 0.31, 0.51, 18.28 |
| a + b·[P̄²/(2σ²) + ln σ] | 0.30, 0.50, 18.37 | 0.32, 0.52 |
| a + b·P̄/σ | 0.42, 0.79, 17.35 | 0.44, 0.83 |
| a + b·(P̄ − 2σ) | 1.48, 1.70 | 1.57 |
| a + b·P̄ | 2.60, 2.98 | 2.54 |
| a + b·P̄ + c·σ (three constants) | 0.47, 0.87, 17.27 | 0.52, 0.96 |
| a + b·A + c·P̄ (three constants, no σ) | 0.27, 0.50, 17.65 | 0.19, 0.37 |

The D2h lifetime at A = 63 matters (`ana2b.py` part 4). Taken as 7.318 (with settled lives, Brent), the
Gaussian-exponent fit's maximum residual is 0.23; taken as 6.855 (without them), 0.50.

**How much it means.**
- For the fit: the Gaussian-exponent form is the best two-constant form tried, and it predicts the one GPU-measured
  point from the other seven within 0.2. Its b = 0.58 says ln τ is a fixed fraction of the Gaussian exponent.
- Against reading much into it: the eight points form two clusters of four nearly collinear rungs, so any form that
  orders them and has a size term does almost as well. Area plus P̄ fits as well without σ.
- The worst point is always D2h at A = 63, the one whose lifetime depends on the settled-life estimator.

The README should say "a two-constant fit, leave-one-out 0.5; a form without σ fits as well".

## Claim 8: the forecasts

The round-2 block of PREDICTIONS.md was committed at 04:24:12 (6d40e72). The graph files were written at
04:24:55–04:25:05 and the binaries (`ex`, `sd`) built at 04:25:19. All outputs are later: `research/scratch/dying/r2/`,
with logs at 04:26–04:32. The README's definitions match the registered ones, and the low-P control for B is marked
as added afterwards.

| forecast | this review | study | score |
|---|---|---|---|
| A1: c1 p* in 0.25–0.5 | 0.079 | 0.079 | failed |
| A2: c1 Gaussian within 1.0 at 0.8, 0.7, 0.6 | −0.15, −0.43, −0.27 | same | held |
| A3: q ratio within ×3, ν ratio > e⁴, at 0.5 | q c1/D2h 0.0078; ln ν D2h − c1 1.45 (no settled 1.62) | 0.008; 1.59 | failed both parts |
| B1: S ratio within 15% (c1, D2h) | 1.60, 1.73 | 1.61, 1.76 | failed |
| C1: at t_8 births ≤ 0.70, survival ≥ 0.85 | 0.373, 0.634 | 0.377, 0.639 | failed (survival) |
| D1: A = 84 steps 2.8–3.1; Δln τ/ΔP̄ 0.76–0.96 | steps 2.65, 2.94, 3.28; ratios 0.994, 0.901, 0.864 | 2.68, 2.95, 3.38; 0.983, 0.898, 0.838 | failed |
| D2: no (P̄, σ) fit within 0.5 | 0.31 (Gaussian exponent); 0.47 (P̄ + σ) | 0.31; 0.52 | failed |

No score changes with the D2h settled-life choice; it only moves A3's ν gap within 1.45–1.62.

## Claim 9: the lead's conjecture

What speaks for it:
- In c1, ln ν loses an almost constant 0.49–0.51 per live cell between 3 and 10 cells.
- Thin faces are lopsided (ratio 1.5 at P ≤ 0.6 P̄, rising as P falls), so a live clump and an empty region do
  coexist.
- The price per cell falls with every tied edge: 0.50, 0.44, 0.35, 0.23.

What speaks against it:
- The price is not constant. It drifts from 0.51 to 0.45 per cell across 0.1–0.45 P̄, then on to 0.34, and nothing
  changes at P̄/2.
- A free edge does not add a fixed amount to the price (claim 4).
- In c1 and csz, the faces that go on to die from a given count are less clumped than the ones that recover. If
  clump-and-hole states were the route to death, the dying faces should be at least as clumped; that holds only
  in D2h.
- A birth–death chain whose down/up ratio does not depend on P also gives a straight log-tail. A straight tail is
  therefore no evidence for any particular spatial picture.

What would test it: how the excursion minimum depends on where the clump sits (rim or centre, tied edge or free
edge), and the committor q conditioned on S at fixed count.

## What the round-2 README should change, most important first

1. **D2h depends on the settled-life estimator.** Every D2h quantity that involves exposure (ln τ 6.86 / 7.17 /
   7.32, ln ν, p*, the last step, the per-edge increments, the A = 63 fit point) should say so.
2. **Split claim 6 by group.** In c1, dying faces are no more lopsided than chance-low ones, and at equal count less.
   In D2h they are more. "The same ratio" compares faces of different counts, and 1.51 against 1.76 is not the
   same ratio.
3. **The tail.** Say "close to straight between 0.1 and 0.45 P̄ (residuals up to 0.25 in ln ν; slope per cell
   drifting from 0.51 to 0.45), no break at half the mean". Drop "5.5 + 3.4 per free edge", or give it with its
   window and the 3.0–4.5 spread of the increments.
4. **Births first.** Add that stationary births depend on P and survival does not, so most of the deficit is the
   face's own lower population. Give the excess beyond it (c1 lag 8: 0.61 against 0.77).
5. **The (P̄, σ_P) fit.** Give the leave-one-out residual of 0.50, the competing forms, and the D2h sensitivity
   (0.23–0.50).
6. **Claim 2.** Mention the crossover: c1 dips to 0.9 P̄ most often and to 0.7 P̄ least often.

## Not checked (round 2)

- Excursions only at R = 11 c, with one seed per group (c1: 3,985 deaths). A = 84 was sampled stationary only, and
  there is no excursion table at A = 84 or for a vertex-centred vessel.
- The study's own excursion runs, `round2.py`, `round2_lowp.py` and the r2 histories were not rerun or reread.
- Births and survival were not split by neighbour count. The layer beneath was not measured; its role is only
  inferred from the excess over the own-P prediction.
- Whether the clump's position predicts recovery, the test claim 9 needs, was not measured. The matched-count
  comparison's null faces recover by construction (at least 64 more generations), and their errors (about ±0.05)
  were not computed.
- The figure was looked at, and its panels match the tables. Panel C is the thinned comparison, which the
  matched-count result above qualifies.
