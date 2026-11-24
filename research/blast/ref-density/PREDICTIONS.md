# ref-density: forecasts, written before any production row (2026-11-24, 14:10 UTC)

Probability that each headline row of `research/blast/density/README.md` (commit 9a105d3) reproduces in my own code
(`rd.c`, validated against the oracle) within 3 combined standard errors. Rows at 63 cells, ε = 1/4, d = 1 unless noted.

Already seen before writing (honesty): one 20,000-generation gump test run (`rd 11 run 1 20000 0 1 f 0 10000`) printed
core-1 density 0.4301, core-2 0.4093, face mean 31.26, sd 5.24, and a thin by-population line at F = 10 (0.383).
The two layer-density rows below are therefore not blind.

| # | row | theirs | P(within 3σ) |
|---|---|---|---:|
| 1 | gump baseline, ln τ | 13.633 ± 0.001 (their seed 13.644 ± 0.012) | 0.95 |
| 2 | fair coins, Δ ln τ | +0.678 ± 0.016 | 0.85 |
| 3 | coins at each replaced layer's mean density, Δ | +0.532 ± 0.011 | 0.80 |
| 4 | copy from the replaced cells (core shuffle), Δ | −0.434 ± 0.013 | 0.65 (the copy's timing — sequential or snapshot — and whether the source may be the cell itself are definitional; I copy the current, sequentially updated state, self included) |
| 5 | scan p = 0.1, Δ | −0.322 ± 0.022 | 0.80 |
| 6 | scan p = 0.2, Δ | +0.043 ± 0.024 | 0.80 |
| 7 | sign change of the scan between 0.1 and 0.2 | p* ≈ 0.19 | 0.80 |
| 8 | layer-1 core density, all time | 0.4301 | (seen: 0.4301) |
| 9 | layer-1 core density, face ≤ 10 | 0.3836 | 0.85 (partly seen) |
| 10 | P_1 (a face down to one cell dies) | 0.77, the same with and without coins (± 0.02) | 0.75 |
| 11 | lag: corr(full layer 1 at t−L, face at t) ≈ +0.30 at L = 1–2, ≈ +0.09 the other way | as stated | 0.70 |
| 12 | R = 9, my chain against `nzd.c` run by me at the same settings (gump and fair d = 1) | — | 0.90 |

Conjectured before looking: the asymmetry of row 11, if it reproduces, follows from the face being far more
persistent than layer 1 (different autocorrelations), not from a lead in time of one over the other (P = 0.6).
The "density part = 0.15 of 0.68" depends on the path: the mean-density coin chain's layer is denser than gump's
(P = 0.7 that its replaced layer-1 core sits above 0.435 all-time).

## Added 14:28 UTC, before these rows started (the gump baseline and R = 9 rows had been seen; no other R = 11 row finished)

| # | row | theirs | P(within 3σ) |
|---|---|---|---:|
| 13 | copy from the whole layer, d = 1, Δ | −0.169 ± 0.011 | 0.80 |
| 14 | in that chain, the replaced layer-1 core's density under a low face (F ≤ 10, after darts) lies between the core-copy chain's and gump's, so the four-chain ordering by that density survives a fifth chain | — | 0.60 |
| 15 | LOW10 coins, d = 1, Δ | +0.463 ± 0.010 | 0.80 |
| 16 | mean-density coins, d = 2, Δ | +0.244 ± 0.013 | 0.80 |
| 17 | the scan chain at p = 0.2 has its replaced layer-1 core above 0.35 after the darts (so "worth coins of 0.19" is not the density of an equivalent support) | — | 0.80 |

(Row 17 is not blind: the R = 9 chain at p = 0.2, seen before writing it, has 0.393 after the darts.)

## Added 14:56 UTC, before these rows started (seen by then: gump, fair, mean, core copy, scan p = 0.1 at 63 cells)

| # | row | theirs | P(within 3σ) |
|---|---|---|---:|
| 18 | fair coins, d = 2, Δ | +0.332 ± 0.014 | 0.80 |
| 19 | mean-density coins at ε = 1/16, d = 1, Δ | +0.164 ± 0.013 | 0.80 |
| 20 | my second fair seed (d = 1) lands above my first (14.264), i.e. the first was low | — | 0.65 |

## Added 15:24 UTC, before these runs report

| # | forecast | P |
|---|---|---:|
| 21 | my second whole-layer copy seed (1014): replaced core 1 after the darts at face ≤ 10 within 0.005 of gump's 0.384, and Δ ln τ < −0.10 | 0.80 |
| 22 | nzd.c's own layer diagnostics on the whole-layer copy chain (seed 9301, 10⁶ generations): LAYER core1 at pop ≤ 10 within 0.01 of gump's 0.384 | 0.80 |

## Second review (17:14 UTC): the skin depth at full replacement (density README, section 2 at 2d67675); before any row

Seen before writing: their table; my R = 9 gump densities by depth (0.41448, 0.41678, 0.41677, 0.41448 at depths 3–6,
theirs 0.41451, 0.41679, 0.41679, 0.41451); three 20,000–50,000-generation timing runs of the full mode.

| # | forecast | P |
|---|---|---:|
| S1 | 45 cells, A, d = 3: my Δ within 3σ of +0.169 ± 0.008 | 0.85 |
| S2 | 45 cells, A, d = 4: my Δ within 3σ of +0.004 ± 0.007 | 0.85 |
| S3 | 63 cells, A, d = 4: my Δ within 3σ of +0.016 ± 0.012 | 0.85 |
| S4 | 63 cells, A, d = 3: my Δ within 3σ of +0.295 ± 0.023 | 0.80 |
| S5 | at d = 4, P₁ and the dips' frequency and deadliness within 3σ of my gump's, at both sizes | 0.80 |
| S6 | 45 cells, d = 4 with every bias +0.01: Δ between +0.01 and +0.06 (the density still matters a little below the skin) | 0.55 |
