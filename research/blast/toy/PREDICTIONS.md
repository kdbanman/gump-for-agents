# blast/toy — forecasts (frozen before the measurement they concern)

## Block 1 — 2026-11-18 04:22 UTC, before any run of mine (only `research/toy2d/README.md` read)

Definitions. "Bust" = an edge death whose last 12 generations contain a one-generation fall of the edge-row
population of at least L/2 cells. Ring = edge row of a strip 16 × L periodic along the edge. Box = edge of an
L × L box (first death of the vessel). Rule cross2 B34/S234.

1. Bust share, ring edge, L = 16–20: **0.30** (50%: within 0.15–0.45). The cap needs 5 of the 6 neighbours an
   edge cell has (gump: 6 of 9), so over-filling is dearer in 2D than in gump and I expect less bust than
   gump's 0.57–0.67.
2. Bust share, box edge, same L: **0.15** (50%: within 0.07–0.25); ring/box ratio ≥ 1.5 with probability 0.6. The
   2D rim is 2 corner cells (4 neighbours: never overcrowded) and 2 next-to-corner cells (5 neighbours), a
   fraction 4/L of the row, so I expect a weaker contrast than gump's 0.6 against 0.016.
3. Last-alive times: flat on the ring (spread < 2 generations, no tilt by symmetry); on the box the last cell is
   at an end (within 2 of a corner) more often than 4/L: probability 0.6.
4. Prices (the file already says ring 0.416 ± 0.001, box τ_first slope 0.343 at L = 12–28). My runs will
   reproduce both within 0.02 (0.8), i.e. in 2D the ORDER IS REVERSED relative to gump: the rimmed edge is
   cheaper per cell than the wrapped one, with a positive offset (box edge outlives ring edge at L ≤ 24).
5. Exact 1D dice surrogate (row over private coins, density 0.472): ring and open-segment local slopes
   d ln τ/dL agree to within 0.01 at L = 18–20 (probability 0.75): two prices is a small-size effect in one
   dimension; the difference ln τ_seg(L) − ln τ_ring(L) tends to a constant, approached like e^(−L/ξ) with
   ξ = 2–4 cells. Sign of the constant: positive (segment outlives ring), probability 0.55.
6. Exact bust share of the death flux in the surrogate: ring > segment (0.7), but both below 0.5 at L ≥ 16 (0.6).
7. Upper tail of the quasi-stationary row population in the surrogate: per-cell rate ψ(x) the same on ring and
   segment to 0.005 per cell at L = 20 (0.7).

## Scoring of block 1 (04:32 UTC; numbers in README.md)

1. Ring bust share (12 steps), L = 16, 20: forecast 0.30; measured 0.876, 0.802. **Miss** (far too low).
2. Box bust share: forecast 0.15; measured 0.472, 0.403. **Miss** in level; ratio ring/box 1.9–2.0 ≥ 1.5: **hit**.
3. Ring flat (spread 1.1–1.3 generations), box last cell at an end twice as often as uniform: **hit**.
4. Ring slope 0.42–0.44 falling to 0.40, box 0.33–0.35, order reversed relative to gump, box outlives ring below
   L ≈ 25: **hit** (it was on file).
5. Surrogate slopes within 0.01 at L = 18–20: **miss**. They differ by 0.063–0.068 (ring 0.524–0.527, segment
   0.459–0.461). Sign of the offset positive: hit (segment outlives ring by 0.67 at L = 20), but it is not a
   constant: it shrinks by 0.065 per cell.
6. Exact bust share ring > segment: **hit** (0.88 against 0.51 at L = 20, 6 steps); both below 0.5 at L ≥ 16: **miss**.
7. Upper tail the same to 0.005 per cell at L = 20: **miss by the letter** (0.007 at x = 0.75, 0.014 at x = 1); the
   difference is a constant 0.15 in −ln P at x = 0.75 (L = 8 … 20), i.e. a prefactor, not a rate.

## Block 2 — 2026-11-18 04:33 UTC, frozen before reading the exact L = 21–24 outputs and with no data beyond L = 36

From the two-exit split of the ring edge (flash ln τ = 0.296 + 0.4550·L, other 4.033 + 0.3274·L; README §3):
- 2D ring edge (strip 16 × L): bust share (6 steps) 0.30 at L = 36, 0.20 at L = 40, 0.08 at L = 48;
  ln τ_edge(40) = 16.90 ± 0.10, ln τ_edge(48) = 19.66 ± 0.15; local slope 40–48 = 0.345 ± 0.010, i.e. the ring's
  price falls to the box's (0.34) and "two prices" disappears in 2D above L ≈ 40 (probability 0.65).
  Retrodiction on file data I had seen: L = 36 gives 15.47 against the file's 15.58 ± 0.045.
- Exact surrogate, read after this commit: ring L = 22: 11.787 ± 0.006; segment L = 22: 12.331 ± 0.004;
  segment L = 24: 13.249 ± 0.008; ring − segment slope difference still ≥ 0.055 at 20–22 (0.8); segment bust
  share (6 steps) at L = 22: 0.475 ± 0.01.
- gump (not measurable by me tonight; conjecture from the 2D relative): the bust share of HULL-face deaths rises
  with face size (its logit linear in A with slope ≈ +0.022 per cell minus a rim term), so 1.6% is not a
  constant: at 108 cells I would expect a higher share than at 63 (probability 0.6).

## Scoring of block 2, exact part (04:40 UTC)

- Ring L = 22: forecast 11.787 ± 0.006, exact 11.7800: **miss by 0.001** (the ring's slope fell to 0.520, faster
  than my two-exit extrapolation). Segment L = 22: forecast 12.331 ± 0.004, exact 12.3311: **hit**. Segment L = 24:
  forecast 13.249 ± 0.008, exact 13.2497: **hit**. Slope difference at 20–22 ≥ 0.055: 0.0618: **hit**. Segment
  flash share (6 steps) at L = 22: forecast 0.475 ± 0.01, exact 0.476: **hit**.
- The 2D items (ring at L = 36, 40, 48) and the gump item are NOT scored: no data.

## Block 3 — 2026-11-18 04:42 UTC, frozen while the runs are in progress and unread

- Exact ring L = 23 and 24 (`ex1d 23 1 0.472`, `ex1d 24 1 0.472`): local slopes 22–23 = 0.518 ± 0.003 and
  23–24 = 0.516 ± 0.004, i.e. ln τ = 12.298 ± 0.003 and 12.814 ± 0.006; both slopes below 0.5198 (the bend has
  begun, not a wobble): probability 0.55. Ring − segment slope difference at 23–24 still ≥ 0.05: probability 0.85.
- 2D ring edge L = 36 (`ed run 16 36 1 21 400 9e8`, ~300 deaths): bust share (6 steps) 0.30 ± 0.04 (block 2);
  boom share (≥ 0.8 L in the last 6 generations) 0.24 ± 0.04; ln τ = 15.47 ± 0.08.

## Scoring of blocks 2–3, 2D ring at L = 36 (04:45 UTC; 348 deaths)

- Bust share (6 steps): forecast 0.30 ± 0.04 (two-exit fit: 0.298); measured 0.290 ± 0.024. **Hit.**
- Boom share: forecast 0.24 ± 0.04; measured 0.224 ± 0.022. **Hit.**
- ln τ: forecast 15.47 ± 0.08; measured 15.441 ± 0.054 (the file: 15.581 ± 0.045). **Hit.**

## Block 4 — 2026-11-18 04:46 UTC: is the ring's second exit made by the strip's width? (frozen before the run)

Worry: the strip is 16 rows wide at every L, and 3-column cuts (cost 48 cells) outnumber edge deaths 6:1 at
L = 28 and 150:1 at L = 36. A strip that is nearly cut gives its edge row two ends, so the ring's "no-flash exit
at the box's price" could be an artefact of W = 16 rather than a property of a ring edge.
Test: `ed run 32 28 1 31 1200 3.2e8` (strip 32 × 28: a cut costs 96 cells). W = 16 gave bust6 = 0.536 ± 0.011, boom
share 0.448 ± 0.011, ln τ = 12.416 ± 0.022.
- Forecast: unchanged within errors (bust6 0.536 ± 0.05, ln τ 12.42 ± 0.06): probability 0.55.
- Otherwise (0.45): bust6 ≥ 0.62 and ln τ ≥ 12.50, i.e. the exit is partly the cut channel's doing and §3 of the
  README must say so.

## Scoring of block 4 (04:47 UTC)

Strip 32 × 28, 1200 deaths, no cut: ln τ = 12.436 ± 0.029 (W = 16: 12.416), bust6 = 0.532 ± 0.014 (0.536), boom share
0.443 ± 0.014 (0.448). **Hit**: unchanged; the second exit is the ring edge's own.
