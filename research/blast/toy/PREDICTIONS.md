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
