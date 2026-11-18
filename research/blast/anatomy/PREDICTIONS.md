# Forecasts of agent `anatomy`, frozen before any of its data

## Block 1: 03:26 UTC (machine clock, `date -u`) on 2026-11-18, before any run and before any stepper is written

Known to me: BRIEF-COMMON.md, docs/AUTOMATON.md, the one-line summary of `research/dying/README.md` given in my
brief (mean face fades over ~20 generations; single deaths lopsided; point of no return ~2.5 cells; depleted face
thinner far away, not emptied). I have not opened `research/dying/README.md` or any death record.

Definitions used below (fixed now): T_i = last generation at which face cell i was alive, relative to the death,
looked for in the 128 generations before it. Plane fit on a torus: unwrap the cells' positions to the nearest
image around a centre cell c, least-squares T = a + g·x, take the best c; the null is the same procedure on T
shuffled over cells (so the maximisation over c is in the null too). Cone fit: T = a + b·|x − c|, best c.
Speed = 1/|g| in hexagonal lattice units per generation (1 unit = 2 kagome nearest-neighbour spacings; the
63-cell torus (1,4),(0,21) is √21 ≈ 4.6 units across).

| # | quantity | forecast | probability I give |
|---|---|---|---|
| 1 | fraction of single deaths on the 63-cell torus (1,4),(0,21) whose plane fit beats 95% of shuffles | 0.50 | 60% that it lies in 0.35–0.65; 15% that it is below 0.15 (flash) |
| 2 | median R² of the plane fit, deaths vs shuffles | 0.30 vs 0.12 | 50% that the death median is in 0.22–0.40 |
| 3 | median sweep speed 1/abs(g) among deaths that beat the null | 0.35 units/generation | 55% that it lies in 0.2–0.6 |
| 4 | cone vs plane on the torus: the cone with b < 0 (a remnant shrinking to a point, latest at the centre) fits better than the plane | in 60% of deaths | 55% that the fraction is above one half |
| 5 | hull face of 63 cells (R = 11): position of the last living cell: corner (3 cells) / other cells of the outermost line (30 cells with a zero coordinate) / inside (30 cells) | 0.02 / 0.60 / 0.38 | 65% that the outer line is enriched over its share by count × stationary occupancy; 80% that corners are below their count share 0.048 |
| 6 | tube of 63 cells, loop² 9, (1,6),(0,21): variance of T in the lowest mode along the axis exceeds that in the lowest mode round the girth | in 70% of deaths | 65% |
| 7 | where hull (ln τ 13.633) and wide torus (13.162) part, in the decomposition 1/τ = ν(p)·q(p): share of the 0.47 that is already present in ν at p = 10 live cells (dips to 10 or fewer, from 63) | under one half (the shapes part late, in the last 10 cells) | 55% |
| 8 | the same for tube (loop² 9) against wide torus | over one half already present at p = 10 (the tube parts early: its living state is emptier) | 60% |
| 9 | speed at which living chaos retakes a cleared disc of ~37 cells in a 300-cell face (time for half the replicas to have re-touched a cell, per unit depth) | 0.4 units/generation | 50% within 0.25–0.6 |
| 10 | a cleared hole grows (cells outside the cleared disc, at distance > 1 unit, emptied beyond the stationary rate) | no measurable growth | 80% |
| 11 | living island left in an otherwise cleared face (living chaos beneath): probability the face regrows, for islands of 3 / 7 / 12 cells | 0.5 / 0.9 / 0.99 | 50% that the 3-cell number is within 0.3–0.7 |

My record on this kind of forecast is unknown; I expect at most half to land.

## Block 2: 03:35 UTC (machine clock), after the PI's request for a band test, before any death record has been analysed

Seen so far: only the lifetimes printed by my runs (wide torus 63: 13.155 ± 0.011; tube loop² 9, 63 cells: 12.845 ±
0.011 with as many lives ended by a transverse firewall (7811) as by a face death (8023), which I did not expect).
The PI's forecast (research/blast/PREDICTIONS.md block 1 item 1): share of deaths in which some band of width ≥ 1
right round the girth is finally empty ≥ 4 generations before the last cell dies ≈ 9% at 54 cells, 12% at 63
(loop² 12), below 5% on the wide torus control. There is no loop²-12 lattice at 63 cells; I use 54 (1,4),(0,18),
60 (1,8),(0,20) and 72 cells.

| # | quantity | my forecast | probability |
|---|---|---|---|
| 12 | share of deaths with a width-1 girth band finally empty ≥ 4 generations before the end, loop²-12 tube of 60 cells | 0.45 (much more than the PI's 0.1: the mean face takes ~20 generations to fade and single deaths are lopsided, so 12 cells empty 4 generations early should be common) | 60% that it is above 0.25 |
| 13 | the same on the wide 63-cell torus (best of three directions, strips of ~16 cells) | 0.30 | 55% within 0.15–0.45 |
| 14 | a compact patch (the 12 cells nearest some cell) on the tube is finally empty ≥ 4 generations early at least as often as a band | yes | 65% |
| 15 | the tube's excess of band-first deaths over what the compact-patch control and the torus control give is real (ratio band share tube / torus above 1.3) | yes | 50% |
