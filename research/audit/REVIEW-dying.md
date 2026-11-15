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

---

# Round 3: one curve across sizes, depleted faces, the slab

Object: `research/dying/README.md` from the third "Short answer" (line 310) to the end, the "Round 3" block of
`PREDICTIONS.md` (27890b4), the results commit aef6d86, `data/r3_*.csv` and `research/figures/dying_ratefunction.png`
(looked at; its panels match the tables, and the kinks in panels A and B, e.g. A = 45 between p = 0.6 and 0.55, are
integer thresholds: that step skips P = 12). Nothing from `research/dying/` or `research/theory/symmetric/` was run or
imported.

**Own code and runs.** `r3_ex.c` is round 2's `ex2.c` with 7-bit face counts (faces to 127 cells) and dumps of every
deep excursion (face states from the first generation with P ≤ M3 to the end). `r3_geo.py` builds the slab torus from
the lattice (1,4),(0,21) of `research/constant/PREDICTIONS.md` part C, independently of `geom.py`. Validation
(`r3_val.py` → `r3_val_out.txt`, ALL OK): lane 0's whole live set equals `reference/oracle.py` at every generation
(600; 400 at R = 15) on v9c, v11c, v13c, v15c c1, v11c csz, the slab (replicated on the oracle's 42³ array torus) and
the 4 × 4 calibration torus (24³); the lives file is byte-identical to `st.c`'s on every system (20,000 generations ×
256 lanes). The dumps pass the checks: 698,446 c1 records, equal to the table's count of excursions with min ≤ 9;
first state ≤ 9, recorded minimum, recovered ends ≥ P̄ and dead ends 0, no failure. Runs: 256 lanes, events every
generation, T0 = 512, fresh seeds 9411–9419. The plan was committed before the runs (01077ba); part 3 was committed
before its own run (513b6c2). Thresholds are the study's P̄, which give the same integer thresholds as this review's
pilot (21.60, 31.25, 42.45, 55.19, csz 28.90, slab 32.58). A = 135 (R = 17, P̄ 69.49) is this review's addition.

    python3 research/audit/dying/r3_val.py                       # -> r3_val_out.txt
    bash research/audit/dying/r3_pilot.sh 1 & bash research/audit/dying/r3_pilot.sh 2 & wait
    bash research/audit/dying/r3_plan.sh 1 & bash research/audit/dying/r3_plan.sh 2 & wait   # ~25 min on 2 cores
    bash research/audit/dying/r3_plan.sh 3                       # second slab seed, 4 x 4 torus (~3 min)
    (python3 research/audit/dying/r3_ana.py; python3 research/audit/dying/r3_ana.py extra) > research/audit/dying/r3_ana_out.txt
    python3 research/audit/dying/r3_dump.py > research/audit/dying/r3_dump_out.txt            # claims 5-7, ~25 min

Exposure (face-generations) and deaths: A = 45 1.64e9 / 89,096 (ln τ 9.820 ± 0.003); 63 8.15e9 / 9,838 (13.627 ±
0.010); 84 1.64e10 / 214 (18.153 ± 0.068); 108 1.23e10 / 1; 135 3.1e9 / 0; csz 11.454 ± 0.008. "Threshold-free"
below means ln ν(min ≤ y) interpolated linearly between integers y and read at y = pP̄ − ½. That removes the
integer-threshold jitter of the study's levels (min < pP̄).

## Summary (round 3)

| claim | verdict |
|---|---|
| 1. Raw curve does not collapse; shallow dips at a size-independent rate | **Confirmed with a correction.** −ln ν(0.5)/A = 0.1199, 0.1034, 0.0926, 0.0893 (study identical to 3–4 digits), and 0.0862 at A = 135. ln ν(0.9) = −2.339, −2.311, −2.352, −2.505, −2.541 (135). Threshold-free it is −2.34, −2.38, −2.40, −2.48, −2.53, so it is not size-independent: it falls by about 0.002 per cell. |
| 2. Collapse of [ln ν(0.9) − ln ν(p)]/A for p ≥ 0.4; fan below | **Confirmed; the post-hoc choice matters little.** 0.0679, 0.0667, 0.0646, 0.0661, 0.0674 (135); threshold-free 0.0648, 0.0646, 0.0654, 0.0660, 0.0666. Within ±4% for references 0.85–0.95. The fan is the same 1/A convergence seen at every p, not a change at p = 0.4. |
| 3. Tail price per live cell independent of size | **Numbers confirmed; the statement needs narrowing.** Unweighted 0.438, 0.498, 0.505, 0.508; weighted 0.432, 0.536, 0.568, 0.434. The weighted fit is broken by integer thresholds (max residual 0.44, 0.79, 1.07). Supported: at A ≥ 63 the price is 0.50–0.52 per cell, rising slowly with A; the local slope falls from about 0.53 near 3 cells to 0.40 near P̄/2. |
| 4. End effect: ln τ = attempt + cA − K, K ≈ 2.4; c the p = 0 limit; dips point to 0.19–0.20 | **The form holds; the numbers do not.** With ν(0.9) as the attempt, ln τ + ln ν(0.9) = 0.2125·A − 2.07 to within 0.010 nats over A = 45–108 (135 within its error). At K ≈ 2.4 (c = 0.219) K is not constant (2.37 → 2.78). The constant-K slope depends on the reference level (0.218 for all crossings, 0.213 at 0.9, 0.204 at 0.8), because ν(ref) itself has a part ∝ A. The shortfall is spread below p ≈ 0.55 and is not concentrated in the last cells. Own estimate from dips at p ≥ 0.2 alone: **c = 0.215 ± 0.005**. It cannot separate 0.207 from 0.219. The lead's ρ, F formula is arithmetic. |
| 5. Depleted face = one patch at 0.6 of stationary in an emptied face | **Numbers confirmed; the picture needs correcting.** Inner 0.514, shells 0.420, 0.184, 0.080; profile 0.58–0.61; thinned control 0.338. The control is fair for the contrast, not for the levels: ρ-weighted random points read 0.33 at their own centroid against a true 0.264. Without alignment the patch is at **0.46–0.54** of stationary, and the far face is at about 0.15, not empty. |
| 6. csz holds on away from the tied edge (22.3% vs 29.9%) | **Confirmed.** 0.2239 ± 0.0007 against thinned 0.2983 and ρ-random 0.311. Without a centroid: the tied-edge third holds 0.82 of the face's mean relative occupancy, against 0.99 in thinned faces. |
| 7. Refill from the patch (99.4% vs 68.4%) | **Numbers confirmed; almost no content left.** 0.9942 against random 0.6832. A rule-aware baseline (empty cells with ≥ 1 live in-face neighbour) gives **0.9912**. Every birth has a live in-face neighbour (1.00000), as the rule requires. |
| 8. Slab: ln τ 13.13 ± 0.04, costlier shallow dips, cheaper tail | **Vessel confirmed (mirror image of (1,4),(0,21), the same torus). Dips confirmed. Lifetime revised: 13.176 ± 0.011** (two seeds). That is above every part-C forecast (flat 13.115 by 5σ, massive 13.128 by 3.8σ). No firewall can form on this torus, so the "missing test" is vacuous. |
| 9. Forecast scores, order of commits | **Definitions fixed before the data; every score reproduces.** T1a, T1b, T2 failed; T3, T4 held; K9, K10, K12 failed; K11 held. T1b's registered fit and T4 were weak tests (claims 3, 7). |

## Claims 1 and 2: the rate of dips across sizes

`r3_ana_out.txt`, blocks "Claim 1" and "Claim 2". Every number the study gives reproduces on fresh seeds to the third
decimal (the c1 R = 11 run here is 1.6× the study's exposure, and is independent of it).

**The shallow-dip rate is not size-independent.** The study's levels give ln ν(0.9) = −2.339, −2.311, −2.352,
−2.505, and −2.541 at A = 135. They jump because pP̄ crosses integers differently at each size: 0.9P̄ means P ≤ 19,
28, 38, 49, 62. Threshold-free the values are −2.339, −2.382, −2.401, −2.484, −2.534: a steady fall of about 0.0022
per cell from 45 to 135, 0.0026 from 84 to 135. The Gaussian cost of the first tenth of a dip,
0.01·P̄²/(2σ_P²)/A, is 0.0025–0.0032 per cell, so most of that fall is a part of ν(0.9) proportional to A. The rate
of every downward crossing of P̄ (the true attempt rate) instead rises slowly: ln ν(all) = −1.895, −1.795, −1.748,
−1.702, −1.679. "About one dip every ten generations" is right in size: 10.4 generations at A = 45, 12.7 at 135.

**The collapse for p ≥ 0.4 is robust to the post-hoc choice.** [ln ν(ref) − ln ν(0.5)]/A, threshold-free:

| ref | A = 45 | 63 | 84 | 108 | 135 |
|---|---|---|---|---|---|
| 0.95 | 0.0705 | 0.0694 | 0.0697 | 0.0699 | 0.0703 |
| 0.90 | 0.0648 | 0.0646 | 0.0654 | 0.0660 | 0.0666 |
| 0.85 | 0.0586 | 0.0591 | 0.0603 | 0.0611 | 0.0620 |
| 0.80 | 0.0518 | 0.0529 | 0.0543 | 0.0554 | 0.0563 |

On the study's levels the 0.9 row is 0.0679, 0.0667, 0.0646, 0.0661, 0.0674. The 3% equality at 0.9 was partly
luck of the thresholds, but every reference gives a spread under 9%, and 0.90–0.95 under 3%. What the extra size
shows is a slow upward drift (0.0646 → 0.0666 from 63 to 135).

- **It is not Gaussian scaling.** The Gaussian value 0.24·P̄²/(2σ_P²)/A rises 0.060, 0.068, 0.072, 0.076, 0.078 with
  the measured P̄ and σ_P, while the measured value stays at 0.065–0.067.
- **Deeper, the fan reproduces.** At p = 0.3: 0.108, 0.112, 0.117, 0.117, 0.119 (135). At p = 0.1: 0.151, 0.161,
  0.167.
- **"Collapse above 0.4, fan below" is one effect.** At every p the curves converge as 1/A to a limit, with an offset
  K(p) that is zero above p ≈ 0.55 and grows below it (claim 4). So the post-hoc statistic is sound as a way of
  removing an O(1) prefactor. Its "for p ≥ 0.4" marks where K(p)/A drops below the noise, not a regime.

## Claim 3: the tail

`r3_ana_out.txt`, "Claim 3":

| | A = 45 | 63 | 84 | 108 | 135 |
|---|---|---|---|---|---|
| levels 0.10–0.45, unweighted (max residual) | 0.438 (0.03) | 0.498 (0.20) | 0.505 (0.22) | 0.508 (0.25; 0.15–0.45) | 0.518 (0.16; 0.30–0.45) |
| levels, count-weighted (registered) | 0.432 (0.05) | 0.536 (0.44) | 0.568 (0.79) | 0.434 (1.07) | 0.530 |
| integer grid k ∈ [0.1P̄, 0.45P̄], unweighted (max residual) | 0.472 (0.02) | 0.498 (0.05) | 0.513 (0.08) | 0.519 (0.07) | 0.497 (0.07; k ≥ 20) |

- **Most of the level fits' residuals are integer thresholds.** The 0.2–0.25 residuals of the level fits, and the
  0.44–1.07 of the weighted fits, are mostly integer thresholds. On the integer grid the tail is straight to
  0.02–0.08 nats over 0.1–0.45 P̄. The round-2 "close to straight but not straight" stands, but at that smaller size.
- **The count weighting is what makes the registered fit wander.** The 0.45 level (often a full integer further
  down than 0.4) carries most of the weight. The 0.566 at A = 84 and the 0.432 at A = 108 are artefacts of where
  0.45P̄ falls between integers. They are not tail slopes.
- **Local slope by window of k** (4 integers):
  - A = 63: 0.40 (k 0–3), then 0.51, 0.52, 0.51, 0.50, 0.48, 0.46, 0.44, 0.40 (k 16–19);
  - A = 84: 0.42, then 0.53 through k ≈ 14, falling to 0.39 at k 24–27;
  - A = 108: 0.54 at k 12–17, falling to 0.39 at k 32–35.

  At a fixed window (k 4–7) the slope is 0.479, 0.515, 0.531 at A = 45, 63, 84.

**Supported across sizes:** for A ≥ 63, over 0.1–0.45 P̄, the price is 0.50–0.52 per live cell, ±0.03 by window and
threshold handling, rising slowly with A; at A = 45 it is 0.44–0.47. The tail is one smooth curve, about 0.53 per cell
in the deep part and falling to about 0.40 by P̄/2. The last three cells are cheaper (0.39–0.42). "A price per live
cell that does not depend on size" holds to about ±3% between 63 and 108, not exactly.

## Claim 4: what the dips say about the limiting price per cell

`r3_ana_out.txt`, "Claim 4" and "Claim 4, continued". Lifetimes are the GPU's (`research/gpu/README.md`: 9.820,
13.635, 18.141, 23.376 ± 0.031, 29.34 ± 0.25); the own values at 45–84 agree.

**The end-effect form holds, with c = 0.2125, not 0.219, and K = 2.1, not 2.4.** M(A) = ln τ + ln ν(0.9) =
−ln q(0.9) reads 7.481, 11.324, 15.789, 20.871, 26.799. Its increments per cell are 0.2135, 0.2126, 0.2117 and
0.2196 ± 0.009 (108 → 135). A line through A = 45–108 gives c = 0.2125, K = 2.07, maximum residual 0.010 nats
(threshold-free 0.2130, 2.13, 0.032). K(A) at trial c:

| c | A = 45 | 63 | 84 | 108 | 135 |
|---|---|---|---|---|---|
| 0.207 | 1.83 | 1.72 | 1.60 | 1.49 | 1.15 |
| 0.212 | 2.06 | 2.03 | 2.02 | 2.03 | 1.82 ± 0.25 |
| 0.219 | 2.37 | 2.47 | 2.61 | 2.78 | 2.77 |

So the shortfall is a fixed number of nats (2.1), but only at c ≈ 0.2125. The lead's pairing of K ≈ 2.4 with
c = 0.21–0.22 is not consistent.

**But c in this form depends on the reference level, so "c is the limit of the collapsed curve at p = 0" is not true
as stated.** Lines through A = 45–108 of ln τ + ln ν(ref), threshold-free:

| ref | all crossings | 0.95 | 0.9 | 0.85 | 0.8 | 0.7 |
|---|---|---|---|---|---|---|
| slope (45–108) | 0.2181 | 0.2157 | 0.2130 | 0.2092 | 0.2042 | 0.1900 |
| K | 1.90 | 2.00 | 2.13 | 2.24 | 2.32 | 2.35 |
| maximum residual (nats) | 0.028 | 0.033 | 0.032 | 0.029 | 0.026 | 0.015 |

Every reference fits equally well, because ln ν(ref) has its own part proportional to A (claim 1). The slope of ln τ
is the slope for a reference whose rate does not scale with A. The crossing rate is the only candidate: it grows
only like a log, by +0.0009 per cell at 108 → 135. With it, the slope is 0.218 (45–108; 0.2173 weighted to 135),
which is just the slope of ln τ again. With ν(0.9) as the attempt, the p = 0 limit of the collapsed curve is
c minus the drift of ln ν(0.9), 0.002–0.003 below c.

**Where the shortfall sits.** Fitting G_A(p) = ln ν(0.9) − ln ν(p) = A·f∞(p) − K(p) separately at each p (3–5 sizes,
threshold-free) leaves a maximum residual of 0.01–0.05 nats at every p:

| p | 0 | 0.05 | 0.1 | 0.15 | 0.2 | 0.25 | 0.3 | 0.35 | 0.4 | 0.5 | ≥ 0.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| f∞(p) | 0.2130 | 0.2019 | 0.1837 | 0.1664 | 0.1528 | 0.1381 | 0.1222 | 0.1081 | 0.0942 | 0.0677 | |
| K(p) | 2.13 | 1.76 | 1.33 | 1.04 | 0.97 | 0.84 | 0.63 | 0.52 | 0.40 | 0.17 | −0.04 to −0.18 |

K(p) builds up smoothly from p ≈ 0.55 down to 0. About half of it lies below p = 0.15, and the rest is spread over
0.15–0.55. It is a fixed amount at a fixed *fraction* of P̄, so it spans more cells on larger faces (from p = 0.55 down
it covers 17 cells at A = 63 and 30 at 108). It is not "the last few cells". Separately, the last three cells cost
nearly the same at every size: H_A(k) = ln ν(≤ k) + ln τ = 0.25, 0.67, 1.17 (A = 45); 0.26, 0.69, 1.20 (63); 0.29,
0.69, 1.27 (84) for k = 1, 2, 3. Both descriptions fit the data, and neither puts the shortfall only at the bottom.

**Own estimate from the dips at p ≥ 0.2 alone.** With every crossing as the reference, f∞(p) = slope in A of
ln ν(all) − ln ν(p) over the sizes that reach p, fitted linearly in p and extrapolated to p = 0:
- **Calibration where the bottom is known** (A = 45–84): the extrapolation from 0.2–0.45 gives 0.2167, and the
  measured slope of ln τ + ln ν(all) is 0.2171. A quadratic in p overshoots (0.2241), so it is not used.
- **Result:** 0.2157 over A = 45–135 (window 0.2–0.45). Other windows give 0.208–0.219. The crossing-rate drift
  (≤ 0.001) is subtracted.
- **The ν(0.9) route gives the same:** 0.2108 + 0.002–0.003 (calibrated 0.2108 against 0.2130).
- **Best estimate c = 0.215 ± 0.005.** The error is the window spread; the model error of the linear-in-A step
  beyond A = 135 is not included. It is 1.6σ above 0.207 and 0.8σ below 0.219. **The dips cannot tell the two
  apart.** They mildly disfavour the low end, and add no information beyond ln τ's own local slopes (0.212–0.221).

**The ρ, F formula is arithmetic.** c ≈ 0.24·ρ/(2F) + m·ρ/2 is the Gaussian value of the 0.9 → 0.5 part plus a
straight tail from 0.5 to 0 at slope m. Each term misses what is measured:
- The Gaussian term is 0.0724 and 0.0755 at A = 84 and 108, while the measured shallow part is 0.0654 and 0.0660.
- The straight tail overshoots the true bottom by 0.22–0.56 nats (0.005–0.009 per site at A = 45–84).

With this review's ρ and F the formula gives 0.200, 0.205, 0.211 at A = 84, 108, 135. Its approach to 0.21 comes
from two errors that partly cancel and from extrapolating ρ and F. It estimates at most the end point
(c − K/A with ν(0.9) as reference), not c.

**"Levelling off near 0.19–0.20, below c".** The end points 0.1662, 0.1797, 0.1880, 0.1932 and 0.1985 (135) follow
0.2125 − 2.07/A. That curve does not level off; it is still rising at A = 135.

## Claim 5: what a depleted face looks like

`r3_dump_out.txt`, "Claim 5". This review has 698,446 caught c1 faces (238 with k < 3 skipped), mean k 8.26;
150,000 are used for the profiles. Its own ρ comes from 7.96 M stationary face samples, with P̄ 31.252 and σ 5.244.

**Reproduction.** T2 inner 0.514, shells 0.420, 0.184, 0.080 (study 0.513; 0.421, 0.184, 0.080). Radial profile
0.584, 0.599, 0.609, 0.589, 0.521 over 0–3 units (study 0.581, 0.601, 0.606, 0.586, 0.521). Thinned 0.338 flat
(study 0.334).

**The alignment bias, measured.** The face's mean relative occupancy is k/Σρ = 0.264 in every set:

| distance from own centroid (doubled units) | 0–2.4 | 3.4 | 5.2 | 7.0 | 9.5 |
|---|---|---|---|---|---|
| caught, aligned on own centroid | 0.58–0.61 | 0.43 | 0.20 | 0.09 | 0.02 |
| thinned stationary, same | 0.34 | 0.34 | 0.27 | 0.17 | 0.05 |
| ρ-weighted random points, same | 0.33 | 0.32 | 0.27 | 0.19 | 0.07 |
| caught, split-half (centroid from one half, the other half counted) | 0.46–0.48 | 0.39 | 0.24 | 0.15 | 0.09 |
| thinned, split-half | 0.26 | 0.26 | 0.27 | 0.27 | 0.24 |

Around a live cell (no centroid at all), the relative occupancy of the other cells is:

| distance | 1.3–2.5 | 2.5–3.75 | 3.75–5 | 5–7.5 | > 7.5 |
|---|---|---|---|---|---|
| caught | 0.537 | 0.330 | 0.230 | 0.183 | 0.157 |
| thinned | 0.265 | 0.244 | 0.239 | 0.237 | 0.234 |
| ratio | 2.03 | 1.36 | 0.96 | 0.77 | 0.67 |

At k = 7–9 the caught value within 2.5 is 0.54; at k = 3–6 it is 0.38.

- **The comparison is fair for the contrast, not for the levels.** The control carries the same self-alignment bias,
  which lifts even random points from 0.264 to 0.33 at the centre. The caught/control contrast (1.75 aligned, 1.8
  split-half, 2.0 around a live cell) is robust. The absolute 0.6 is not: about a quarter of it is the alignment.
- **Bias-free picture.**
  - Near the survivors the face is at about half its stationary density (0.46–0.54; split-half blurs downward,
    self-alignment inflates upward).
  - The excess extends about 3.5 units (under two cubes) from a survivor.
  - Beyond that the face sits at 0.15–0.20 of stationary, about 0.7 of a uniformly thinned face. It is "thinner far
    away", not "emptied".
  - Thinner faces have a looser patch.
- **Off-centre.** Caught centroids lie 2.65 units from the face centre, against 1.55 for thinned faces. The
  "rim side of its centroid" asymmetry in panel C was not measured.

## Claim 6: csz, the tied edge

`r3_dump_out.txt`, "Claim 6". 394,680 caught csz faces (mean k 7.27); ρ from 3.13 M samples (tied rim row 0.308,
free rows 0.431). The fraction whose corrected centroid is nearest the tied edge is **0.2239 ± 0.0007**. The thinned
control gives 0.2983, and ρ-weighted random points 0.3109 (study 0.223, 0.299).

A statistic without a centroid gives the same answer: the relative occupancy of the third of the face nearest the
tied edge (cells split on ties), over the face's mean relative occupancy. It is 0.820 for caught faces, 0.991 for
thinned and 1.005 for random. A thin csz face is depleted at its tied edge about 18% beyond the stationary rim
depletion. Confirmed.

## Claim 7: refill

`r3_dump_out.txt`, "Claim 7". 688,022 recovered, untruncated excursions; 8.83 M births counted.

| | fraction |
|---|---|
| births within two cells of the bottom's survivors | **0.9942** (study 0.994) |
| random over empty cells | 0.6832 (study 0.684) |
| **rule-aware**: random over empty cells with ≥ 1 live in-face neighbour at t | **0.9912** |
| births with ≥ 1 live in-face neighbour at t | 1.00000 |

A face cell has 9 neighbours inside the vessel, only 3 of them off the face, so a birth needs a live in-face neighbour.
Graph distance of births from the bottom set: 0 (a bottom cell reborn) 11.7%, 1 71.7%, 2 16.0%, 3 0.55%,
4 0.02%.

**What is left beyond the rule:** an excess of 0.003. T4 tested the rule. Its "held" and K12's "failed" stand as
registered. As a finding, "a thin face refills from its patch" should be stated as a consequence of B45 on a face,
not as an observation.

## Claim 8: the rim-free face

`r3_geo.py info`; `r3_ana_out.txt`, "Claim 8".

**The vessel.** The study's hex_4_1 lattice, v = (10,−8,−2) and Rv, is not equal to (1,4),(0,21) = {(2,8,−10),
(0,42,−42)}. It is equal after the mirror x ↔ y, an automorphism of the honeycomb that preserves the slab. So it is
the same torus, part C's n = 21. It is equilateral: six shortest vectors of length √21 = 4.58 cube steps.

**Firewalls.** The transverse layer period is 4 in all three directions, so each direction has only two layer
classes. Three consecutive dead layers would mean every cell dead. No firewall can form, so there was nothing to
count; the README's "could in principle continue past a firewall" should go.

**Lifetime: revised upward.**
- Seeds 9416 and 9418 give 13.180 ± 0.016 (3,859 deaths) and 13.173 ± 0.016 (3,887). Pooled: **13.176 ± 0.011**.
- The study has 13.13 ± 0.04, 1.1σ away.
- **Protocol check:** the 4 × 4 torus, part C's anchor, gives 9.9268 ± 0.0065 against the GPU's 9.9324 ± 0.0020.

**Against the part-C forecasts this is a finding for `research/constant/`.** The torus lies above every reading:
- flat 13.115 ± 0.004: +0.061, 5σ;
- massive 13.128 ± 0.006: +0.048, 3.8σ;
- rising 13.107 and 13.100: +0.07.

It is one torus, one protocol (soup 0.4, T0 = 512) and two seeds of one stepper.

**Dips, against the hull face of the same area.**

| | shallow part [ln ν(0.9) − ln ν(0.5)]/A | tail slope, levels 0.1–0.45 | tail slope, integer grid | ln ν(0.9) |
|---|---|---|---|---|
| slab | 0.0774 (threshold-free 0.0783; study 0.077) | 0.426 | 0.425 | −1.95 (shallow dips 1.4× as frequent) |
| hull | 0.0667 | 0.498 | 0.498 | −2.31 |

The slab's local tail slope *rises* toward the mean (0.42 → 0.45), while the hull's falls (0.51 → 0.40).

## Claim 9: order and scoring

- **Order.** Forecasts, definitions and `ex3.c` were committed at 04:40:22 (27890b4). After that came `round3.sh` and
  `round3_pbar.py` (snapshot 04:41:05), `round3.py` (04:43:47; `round3.sh` changed only by a skip-if-done guard and
  a path) and the data (04:53:40). `round3_persite.py` (04:53:40) is labelled as written afterwards. The README's
  definitions match the registered ones. `round3.py` was not read line by line, but every registered number
  reproduces here from independent code.
- **Scores with this review's numbers:**
  - T1a: 0.0926/0.1034 = 0.896, failed.
  - T1b: weighted 0.568, ×1.14, failed. The unweighted 0.505 and the integer-grid 0.513 would hold.
  - T2: inner 0.514, failed; the edge clause holds (0.184).
  - T3: 0.224, held.
  - T4: 0.994, held.
  - K9 failed, K10 failed, K11 held, K12 failed.
  - "Against the reading": neither met.
- **Notes on the tests.** T1b's registered weighting made it a test of where 0.45P̄ falls between integers, and T4
  is nearly forced by the rule. Neither weakness changes a score; both limit what a score means.

## What the round-3 README should change, most important first

1. **"What it points to at p = 0"** should be rewritten. The end points follow ln τ + ln ν(0.9) = 0.2125·A − 2.07 to
   0.01 nats (A = 45–108), so the shortfall below the slope is a constant 2.1 nats. It is spread below p ≈ 0.55 (half
   of it below 0.15) and is not in the last cells. The slope depends on which dip rate is called the attempt (0.218
   for all crossings, 0.213 for ν(0.9)), so "c is the p = 0 limit" holds only with the crossing rate. The dips at
   p ≥ 0.2 alone give **c = 0.215 ± 0.005**, which cannot separate 0.207 from 0.219. Drop "levelling off near
   0.19–0.20, below c": the end points follow c − K/A and still rise at A = 135 (0.1985).
2. **The slab lifetime** should read 13.176 ± 0.011 (this review, two seeds; study 13.13 ± 0.04). Say that this lies
   above all part-C forecasts for this torus (flat by 5σ), and that no transverse firewall can form on it.
3. **The depleted-face picture.** "About 0.6 of stationary … in an otherwise emptied face" should become "about half
   the stationary density near the survivors (0.46–0.54 by alignment-free measures; aligning on a face's own
   centroid lifts even random points by a quarter), the rest of the face at 0.15–0.2 of stationary".
4. **Refill.** Give the rule-aware baseline (0.991 against 0.994). The finding is the rule.
5. **The tail.** "Price per live cell independent of size" should become "0.50–0.52 per cell at A ≥ 63 over
   0.1–0.45 P̄, rising slowly with A; 0.44–0.47 at A = 45; locally 0.53 deep, falling to 0.40 by P̄/2". Say that the
   weighted fit's spread and most of both fits' residuals are integer thresholds.
6. **"Size-independent rate of shallow dips"** should read: ln ν(0.9) falls by about 0.002 per cell (a Gaussian
   part); the crossing rate rises slowly.
7. **The collapse for p ≥ 0.4** should be described as the same 1/A convergence seen at every p, with an offset that
   vanishes above p ≈ 0.55. The ρ, F formula should not be given as evidence about c.

## Not checked (round 3)

- One fresh seed per hull size (two for the slab). A = 108 had one death here, so its lifetime is the GPU's. A = 135
  reaches only p ≥ 0.3 here.
- The study's own runs, dumps and scripts were not rerun. `round3.py` was read only for the order of commits.
- The rim-side asymmetry of the patch (panel C), the patch in csz and D2h, and its change with depth (beyond the two
  k bins above) were not measured.
- The thinned controls draw from all stationary samples at age > 512, without dropping the 64 generations before a
  death (the study's null rule; in c1 the effect is ≤ 0.01 cells, round 1).
- The c = 0.215 ± 0.005 error covers fit windows only. It assumes G_A(p) stays linear in A beyond 135, which was tested
  only within 45–135 (residuals ≤ 0.05 nats).
- The slab lifetime's tension with part C was not chased: other tori of that family, other soups or T0, and
  the engine. The 4 × 4 check agrees to 0.006.

# Round 4: a mixture or a thinning? The lever rule tested

Object: `research/dying/README.md` from "# Round 4" to the end, `PREDICTIONS.md` ("Round 4", "Round 4 definitions",
the scoring note), `data/r4_*.csv`, `research/figures/dying_two_phase.png` (looked at), `ex4.c`, `round4.py`,
`round4_score.py`, `validate4.py`, `round4.sh` (read, not run or imported), ledger row DY13, the last notebook entry.

**Own code and runs** (`research/audit/dying4/`; `bash research/audit/dying4/run.sh` redoes everything, one core,
about 20 minutes). `geom.py` builds the octahedral vessel |p|₁ ≤ R and its eight faces from `docs/AUTOMATON.md`
alone, each face in the canonical order q = d ⊙ p. `st4.c` is a new bit-sliced stepper (256 lanes, soup 0.4 per
cell, T0 = 512, a life ends at the first empty face or a repeat of a power-of-two-age snapshot) that records, per
excursion, the face at first passage through 0.6, 0.45, 0.3, 0.15 and at the bottom, and separately the face at
*random moments* when P equals the level exactly (time-weighted), and stationary samples. `validate.py` →
`validate_out.txt`: lane 0 equals `reference/oracle.py` at every generation (R = 11, 600 generations; R = 13, 400),
ALL OK. Runs: seeds 5101 (A = 63, 3 M generations), 5103 (A = 84, 3 M), 5105 (A = 108, 1.5 M); the study used
4411–4416. Integer levels are the study's (P ≤ ⌊pP̄⌋). `ana.py` → `ana_r{11,13,15}.txt`, `company_r*.csv`;
`null.py` → `null_r*.txt`; `dies.py` → `dies_out.txt`.

**Protocol reproduced.** P̄ = 31.251, 42.451, 55.189; S = 1.0434, 1.0377, 1.0341 (study 1.0436, 1.0377, 1.0340);
ln τ_face (A = 63) = 13.626 ± 0.012 (study 13.633 ± 0.005); threshold-free ln ν(0.9) = −2.382 (study −2.382).

## Summary (round 4)

| claim | verdict |
|---|---|
| 1. C falls with depth; C(0.15)/C(0.45) = 0.38, 0.49, 0.53; "so no remnant held at a fixed density" | **Numbers reproduce; the inference fails.** Own C(0.15)/C(0.45) = 0.383 (63), 0.481 (84). But a face that *is* an exact lever-rule remnant (fixed relative density p_t in a compact patch, empty elsewhere) gives 0.45–0.48 (63), 0.58–0.61 (84), 0.65–0.69 (108) for any p_t in 0.45–0.8. The registered F1 "against" clause (< 0.6) is met by the lever rule itself at 63 and 84 cells. Not shared rows, not rim position. |
| 2. Far from random thinning (1.15–2.4× the company, ~3× the void at 0.3, falling profile) | **Stands.** Own A = 108: 1.15, 1.35, 1.70 at p = 0.6, 0.45, 0.3; V(0.3)/control 2.3, 2.7, 3.2 at 63, 84, 108. "A profile that falls where the control is flat" separates the face from random thinning only: a lever-rule remnant's profile falls too. |
| 3. Tangent construction overshoots the end point by 1.06, 1.20, 1.37 nats | **Stands (arithmetic).** Recomputed from `data/r4_tangent.csv`; own run at A = 63 gives g 0.3081, s 0.2487, p_t 0.596, end point 0.1954 against 0.1785: 1.07 nats. The end point compared against is the right one. |
| 4. Dying faces looser than recovering at the catch | **Stands with a correction.** Count-matched (A = 63), most of the gap is count: p = 0.15, 0.145 against 0.166, difference 0.021 ± 0.001 (unmatched 0.151 against 0.204); p = 0.3, 0.303 against 0.320, 0.017 ± 0.003 (unmatched 0.324 against 0.387). |
| 5. Far field (gd ≥ 4) 0.16–0.21 at p = 0.3, 0.04–0.07 at 0.15 | **Stands.** Own 0.163, 0.181, 0.205 at p = 0.3 (63, 84, 108); 0.039, 0.060 at 0.15 (63, 84). |

## Claims 1, 2 and 5: the numbers, independently

`ana_r11.txt`, `ana_r13.txt`, `ana_r15.txt`, first table. Caught at first passage (C ± bootstrap s.e.; V; random-
thinning control C and V; company at gd = 1, 2, 3, ≥ 4):

| A | p | faces | k̄ | C | V | control C | control V | profile |
|---|---|---|---|---|---|---|---|---|
| 63 | 0.6 | 159,293 | 16.93 | 0.5969 ± 0.0002 | 0.056 | 0.522 | 0.022 | 0.660 0.569 0.513 0.467 |
| 63 | 0.45 | 115,617 | 13.08 | 0.5115 ± 0.0003 | 0.109 | 0.398 | 0.040 | 0.602 0.472 0.380 0.325 |
| 63 | 0.3 | 156,885 | 8.26 | 0.3865 ± 0.0003 | 0.235 | 0.240 | 0.101 | 0.511 0.331 0.207 0.163 |
| 63 | 0.15 | 40,578 | 3.50 | 0.1959 ± 0.0005 | 0.488 | 0.087 | 0.342 | 0.336 0.133 0.049 0.039 |
| 84 | 0.6 | 28,222 | 23.75 | 0.6254 ± 0.0005 | 0.052 | 0.545 | 0.017 | 0.686 0.600 0.548 0.505 |
| 84 | 0.45 | 4,977 | 17.95 | 0.5323 ± 0.0012 | 0.109 | 0.406 | 0.032 | 0.623 0.494 0.408 0.352 |
| 84 | 0.3 | 3,215 | 11.21 | 0.4136 ± 0.0022 | 0.244 | 0.245 | 0.090 | 0.536 0.361 0.239 0.181 |
| 84 | 0.15 | 1,295 | 5.40 | 0.2562 ± 0.0038 | 0.470 | 0.107 | 0.282 | 0.404 0.192 0.086 0.060 |
| 108 | 0.6 | 26,128 | 31.60 | 0.6454 ± 0.0005 | 0.048 | 0.562 | 0.014 | 0.705 0.621 0.572 0.531 |
| 108 | 0.45 | 24,423 | 22.88 | 0.5416 ± 0.0006 | 0.116 | 0.401 | 0.029 | 0.634 0.504 0.417 0.357 |
| 108 | 0.3 | 834 | 15.08 | 0.4398 ± 0.0036 | 0.239 | 0.259 | 0.074 | 0.566 0.388 0.274 0.205 |

Every entry agrees with the README's table to within its errors (A = 108 at 0.15 not reached here). C_pair, which
replaces ρ_j by the stationary conditional occupancy P(x_j = 1 | x_i = 1) of each pair (so it is exactly 1 in the
stationary ensemble and needs no S), agrees with C to 0.002 everywhere: the normalisation is not doing anything.

## Attack 1: what a lever rule would read on these faces (claim 1 fails as an inference)

`null.py`, `null_r*.txt`; `ana_r*.txt`, "Lever-rule null". The null builds the object the lever rule describes: a
compact patch (graph ball about a random cell, grown until its stationary mass Σρ reaches k/p_t), filled with the
live cells of a random stationary face inside it, thinned to exactly k; nothing outside. Same C, V and profile code.

C(L(0.15))/C(L(0.45)) at fixed k = L(p):

| A | k at 0.45, 0.15 | null p_t = 0.45 | 0.55 | 0.65 | 0.8 | caught, random moment at P = L | caught, first passage (k̄) |
|---|---|---|---|---|---|---|---|
| 63 | 14, 4 | 0.482 | 0.483 | 0.466 | 0.449 | 0.439 | 0.383 |
| 84 | 19, 6 | 0.592 | 0.613 | 0.608 | 0.577 | 0.553 | 0.481 |
| 108 | 24, 8 | 0.654 | 0.682 | 0.686 | 0.663 | – | (study 0.532) |

With the caught faces' own k distribution (first passage) the null gives 0.45 (63) and 0.58 (84).

- **The test could not pass.** At 3.5–8 live cells, a patch at any fixed density is about the size of the radius-2
  ball the company is counted in. Its live cells sit mostly at the patch's edge and see the emptied face. So C falls
  with depth for a remnant held at fixed density too. The registered "against" clause (< 0.6) is met by an exact
  lever rule at 63 and 84 cells and nearly at 108. The README's "a lever rule needs C(0.15)/C(0.45) ≈ 1" holds only
  on faces much larger than these. The size trend 0.38 → 0.48 → 0.53 follows the null's own 0.45 → 0.58 → 0.67.
  The figure's guides (panel A: C = max(p, p_t); panel B: V = 1 − p/p_t) are that infinite-face idealisation; the
  null's V at p = 0.15 is 0.44–0.54, not 0.73–0.81.
- **What does separate the caught faces from the null.** (a) The first-passage ratio sits 0.07–0.10 below the null at
  63 and 84 cells (roughly 0.14 at 108 against the study's number). (b) The profile shape. At k = 4 (A = 63) the null
  with p_t = 0.8 matches the caught C and V (0.254 and 0.490 against 0.253 and 0.488, random-moment faces). But the
  profiles differ: 0.330, 0.220, 0.078, 0.005 for the null against 0.449, 0.163, 0.043, 0.032 caught. A caught face
  is more peaked than a flat patch, with a tail that reaches the far face. The same holds at every level and size
  in `null_r*.txt`.
  So "no plateau at fixed density inside the patch" is supported by the profile, not by C. On C and V alone, the
  random-moment faces are fitted by a constant effective p_t ≈ 0.7–0.8 at all three depths on both sizes.
- **Narrowed claim.** On these faces C cannot tell a lever rule from a thinning; a depleted face is a peaked clump
  with a tail (claim 2 stands), and its C falls a little faster with depth than a fixed-density remnant's would.
  The registered F2 (mean C at p ≤ 0.3 in 0.47–0.63) also compared C with a density that C does not measure: a
  p_t = 0.55 remnant reads C = 0.41 (k = 16) and about 0.33 (k = 8) at A = 108. F1 and F2 fail as registered;
  their failure is not evidence against the two-phase reading.

## Attack 2: rim, shared rows, position

33 of the 63 cells (39 of 84, 45 of 108) lie on the octahedron's edges and belong to two faces. They are exactly
the rim (in-face degree < 6). `ana_r*.txt`, "Where the survivors sit", "Unshared cells only":

- **Survivors do not sit in the shared rows.** The survivors' relative occupancy (x/ρ over the face mean) in shared
  cells is 0.92–0.95 at p = 0.6–0.3 at every size, against 0.99–1.01 for the control. At 0.15 it is 1.03 (63) and
  1.04 (84). The healthy neighbour does not hold up a remnant on the shared rows.
- **C on the unshared cells alone** (live cell and companions both unshared, normalised by the same restriction on
  stationary faces) falls faster, not slower. A = 63: 0.586, 0.492, 0.348, 0.149; control 0.523, 0.399, 0.242,
  0.086. Ratio 0.15/0.45 = 0.30 (63), 0.40 (84).
- The pair-normalised C_pair (position-exact) equals C. Claim 1's numbers are not a rim artefact.

## Attack 3: when the face is caught

`ana_r*.txt`, rows `bottom` and `atlevel`.

- **At the bottom** C is within 0.008 of the catch (A = 63: 0.5035, 0.3805, 0.1953 against 0.5115, 0.3865, 0.1959),
  as the README says.
- **At a random moment with P = L(p)** (time-weighted), faces are clearly more clustered than first-passage faces of
  the same count. A = 63, k = 14, 9, 4: 0.576, 0.457, 0.253 against 0.538, 0.413, 0.219 at first passage with the
  same k. A first passage catches faces mid-fall; time at a level favours faces that linger. The qualitative
  picture is unchanged: C still falls, and the control contrast is a little larger (2.6× at k = 4). The C ratio moves
  toward the lever null: 0.44 (63) and 0.55 (84) against the null's 0.45–0.48 and 0.58–0.61.

## Attack 4: the control

Read in `round4.py` (`thin_control`) and redone in `ana.py`. For each caught face with k live cells, it takes a
uniformly drawn stationary sample of any face (mapped to the canonical face) with P ≥ k and keeps k random live
cells. Counts match face by face. The samples are from the same size and run. The draw over-weights samples with
P ≫ k only through the P ≥ k condition, which is the registered rule. The control reproduces (0.522, 0.398, 0.240,
0.087 at A = 63 against the README's 0.522, 0.398, 0.241, 0.087). No fault found.

## Claim 3: the tangent arithmetic

From `data/r4_tangent.csv`: p_t = 1 − s/2g = 0.5961, 0.5709, 0.5550; end point g(1 − p_t²) − 0.01g = 0.1955, 0.2020,
0.2061. True end point [ln τ + ln ν(0.9)]/A: (13.633 − 2.3822)/63 = 0.1786; (18.166 − 2.4009)/84 = 0.1877;
(23.4 − 2.4845)/108 = 0.1937. Overshoot × A: 1.07, 1.21, 1.34 nats (1.37 with the GPU's 23.376). I(p) = [ln ν(0.9) −
ln ν(p)]/A at p = 0 is ln ν(0.9) + ln τ_face over A, because ν(min ≤ 0) is the face-death rate, so the comparison
quantity is right. The 0.01g offset is applied on both sides. Own run (A = 63): 1.07 nats. A side remark: the
straight tail line alone (`straight_tail_at_0`) also overshoots, by 0.53, 0.63, 0.72 nats. Half the miss is in the
last cells, before any tangency is imposed.

## Claim 4: dying against recovering, count-matched

`dies_out.txt` (A = 63; k = 1 is left out because a lone cell has C = 0 by definition; the k weights are the dying
faces'):

| p | dying / recovering faces | unmatched C | matched C (dying, recovering) | difference |
|---|---|---|---|---|
| 0.15 | 7,385 / 33,310 | 0.151 / 0.204 | 0.145 ± 0.001 / 0.166 ± 0.001 | 0.021 ± 0.001 |
| 0.3 | 2,240 / 154,502 | 0.324 / 0.387 | 0.303 ± 0.004 / 0.320 ± 0.002 | 0.017 ± 0.003 |

At every single k the dying faces are looser (e.g. k = 3 at 0.15: 0.136 against 0.157). At equal k their void is
*smaller* (0.437 against 0.455 at k = 4): the survivors of a dying face are more spread out. About 60–75% of the
README's gap is count. The direction stands. A = 84 had 82 face deaths here, too few to repeat this.

## Attack 5: is there a measure on which a fixed-density core appears?

`ana_r*.txt`, "Core and group densities".

- **Cores** (live cells with ≥ 3 live in-face neighbours): the occupancy over ρ in their distance-1 shells is roughly
  flat or rising with depth: 1.13, 1.15, 1.24, 1.56 at A = 63, p = 0.6 … 0.15, relative to stationary. But the
  random-thinning control does the same (1.21, 1.27, 1.35, 1.40), because the condition selects dense spots. It
  is not a remnant. The share of caught faces that have any core collapses: 0.96, 0.87, 0.59, 0.08 (63); 0.99, 0.99,
  0.90 (108, to 0.3). At 0.15 most depleted 63-cell faces have no cell with three live neighbours.
- **The largest connected group** (gd = 1 links): the density over its closed neighbourhood falls with depth (0.68,
  0.63, 0.57, 0.45 at 63, against control 0.61, 0.54, 0.45, 0.36).
- **On C and V together** the random-moment faces match a lever-rule remnant at p_t ≈ 0.7–0.8 at every depth and
  both sizes (Attack 1). This is the one place where something like a fixed density appears. It does not survive
  the profile, which is peaked rather than flat.
- **Verdict.** I found no measure on which a core at fixed density shows and the control does not. But nothing used
  here can exclude one at these sizes. "No remnant" should be stated as "no plateau seen; C cannot test for one on
  faces of ≤ 108 cells".

## What the round-4 README should change, most important first

1. **The short answer's first bullet and DY13.** "A lever rule needs C flat below the tangent point
   (C(0.15)/C(0.45) ≈ 1)" is false on these faces. An exact lever-rule remnant gives 0.45–0.48, 0.58–0.61, 0.65–0.69
   at A = 63, 84, 108. State the observed ratios beside the null's. Say that the falling C, and F1's "against"
   clause, do not discriminate. What does: the ratio lies 0.07–0.14 below the null, and the profile is peaked
   rather than plateaued. Narrow "a depleted face is not a mixture" to "no plateau at fixed density is seen; on
   faces this small C cannot test the lever rule".
2. **The figure** (panels A and B): replace or label the guides C = max(p, p_t) and V = 1 − p/p_t as infinite-face
   idealisations, or draw the finite-face null instead.
3. **F2 and F6 scoring notes.** F2 compared mean C with p_t, but a p_t remnant does not read C = p_t at these k. Its
   failure says nothing about the remnant's density. F6's "ends the reading" rested on F1's clause, which a lever
   rule also meets.
4. **Dies/recovers:** give the count-matched gap (0.021 ± 0.001 at p = 0.15, 0.017 ± 0.003 at 0.3, A = 63) beside
   the unmatched one; most of the unmatched gap is count.
5. **"The excess grows with size, the reverse of F5"** and the closing "no sign it is close [to ≈ 1]": the reference
   should be the null, which itself rises with A. Against it the caught ratio trails by a roughly constant
   0.07–0.14.
6. Add the random-moment ensemble as a caveat. First-passage faces are looser than time-weighted faces of the same
   count (by 0.03–0.04 in C at A = 63), so "the" depleted face depends on how it is caught.

## Not checked (round 4)

- One fresh seed per size. A = 108 was run only 1.5 M generations: no catch at 0.15, 834 at 0.3, no deaths.
  Claims 1 and 3 at A = 108 rest on the README's numbers and the null's fixed-k value. A = 84 had 82 deaths, so
  claim 4 was checked at A = 63 only.
- The lever null is one model: a ball-shaped patch, uniformly occupied relative to ρ. Other remnant shapes (elongated,
  attached to the rim) were not tried. Their C at small k would differ, but the edge effect would not go away.
- The groups-and-voids exploratory numbers, the per-cell distribution (only its median, in the null comparison) and
  the "interior C" (3 cells at A = 63) were not recomputed. The bootstrap treats faces as independent.
- The study's runs and scripts were not rerun. `round4.py`, `round4_score.py` and `ex4.c` were read: no fault was
  found in the definitions as coded.
