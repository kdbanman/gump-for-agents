# blast/tube1d: forecasts frozen before the data

Disclosure: before writing anything here I had read the PI's block 0 in `research/blast/PREDICTIONS.md` (it is
shown by `head` of that file), including its 120-cell forecast 24.56 ± 0.03. I have seen no measurement of the
120-cell tube, nor "Chain 3" of `research/gpu-local/README.md`.

## Block A, 03:41 UTC (machine clock), before the long `bandp` run and before any reactive path of a tube

Known to me: a 20,000-generation pilot of `tube1d bandp 1 22 48 8 0 5 20000 500 12` (deterministic gump, 144-cell
tube of loop² 12): −ln P(band of width w empty) = 5.49, 6.84, 8.26, 9.71, 11.14 at w = 1, 1.5, 2, 2.5, 3 units
(slope 0.238 per cell) and noisy beyond (12.39 ± 0.09, 13.44 ± 0.16, 14.3 ± 0.26 at 3.5, 4, 4.5); complete
emptiness of a band lasts about 2 generations. Reactive paths seen: only the 48-cell torus (cells' last live
generations are spread over the 3–10 generations before the death).

- A1. Local slope of −ln P(band empty) between w = 4 and w = 6 units (loop² 12, long run): 0.205 ± 0.015 per cell.
  P(within) = 50%. P(it is lower than the slope from 1.5 to 3 units by more than 0.015 per cell) = 75%.
- A2. Band-first share by the PI's criterion (some 0.5-unit band right round the girth with every cell's last live
  generation ≥ 4 generations before the last cell's), 84-cell tube (1,12),(0,28), deterministic gump: 85%
  (PI's forecast for his reading: 20%). P(share > 50%) = 85%. Reason: at 48 cells nearly every cell is last alive
  4–7 generations before the end, so the criterion is met by a flash too. P(the same statistic on the 84-cell wide
  torus (1,4),(0,28) is within 15 points of the tube's) = 65% — i.e. I expect it not to discriminate.
- A3. The last live cells of a dying tube are one clump: P(the cells alive in the last 2 living generations span
  less than 2 units of the tube's length in more than 70% of deaths) = 70%.

### Block A scored (03:45 UTC)

- A1 **hit**: slope from w = 4 to w = 6 units is (18.678 − 13.682)/24 = 0.2082 ± 0.0024 per cell (forecast 0.205 ±
  0.015), and it is 0.0255 below the slope from 1.5 to 3 units (0.2337). `bandp_g12_L12.txt`.
- A2, A3: pending (paths of the 84-cell tube).

## Block B, 03:47 UTC: the 120-cell tube (1,18),(0,40), and the long tubes — before any measurement of them

What it rests on. (i) The anchors of the brief only: local prices of the loop²-12 tube 0.20192 per cell from 84 to
96 cells and 0.20127 from 96 to 108. (ii) My measurement in a living 144-cell tube of the marginal price of an
empty band right round the girth (deterministic gump, `tube1d bandp`): 0.2365 per cell at 2–2.5 units, then
falling steadily, 0.2181 ± 0.0009 at 4, 0.2103 ± 0.0033 at 5, 0.2044 ± 0.005 at 5–6 units, with no sign yet of
levelling, and the band empties as a flash (every 0.5-unit bin of a 5-unit band has been empty for 2.7–3.2
generations when the band first is, edge and middle alike). So nothing says the price turns back up by 10 units,
and nothing says it has levelled. (iii) NOT a measurement of the tube: my sampler (forward flux on the honest-dice
surrogate) failed, see README; this forecast is an extrapolation and is not independent of the PI's block 0, which
I had read.

| quantity | forecast | P(within) |
|---|---|---:|
| ln τ_face, 120-cell tube (1,18),(0,40) | **24.563 ± 0.030** (22.1557 + 12 × 0.2006) | 55% |
| local price 108 → 120 cells | 0.2006 ± 0.0025 | 55% |
| asymptotic price of loop²-12 tubes (if someone reaches 240+ cells) | 0.197 ± 0.005: levels, neither returns to 0.2087 nor keeps falling as a parabola | 45% |

P(local price at 240 cells below 0.193, "quadratic for ever") = 10%. P(price returns above 0.2060 anywhere beyond
120 cells) = 7%.

Band prices at other girths (jobs queued, not seen): P(marginal band price from 4 to 6 units at loop² 16 is above
loop² 12's 0.2082) = 70%; P(at loop² 9 it is below) = 65%; P(at every girth the age profile is flat, i.e. a flash,
edge-to-middle difference under 1 generation at 5 units) = 80%.

### Blocks A2, A3 scored (03:47 UTC; `python3 paths.py EXE 1 12 28 8 paths_1_12_28.txt`, 106 then 203 deaths of the 84-cell tube)

- A2 **hit on the sign, point value high**: band-first share by the PI's criterion 72% (0.5-unit band) / 60% (1-unit
  band); I said 85%, P(> 50%) = 85%. The criterion is met by a flash because a last clump of about 6 cells lingers
  5–6 generations: measured against the MEDIAN cell's last live generation the share is 2% / 1%. Second half (wide
  84-cell torus within 15 points): pending.
- A3 **miss**: the cells alive in the last 2 living generations span under 2 units in 53% of deaths, not > 70%.

## Block C, 03:54 UTC: boom and bust against tube length — before any population series of a dying tube

Known: PI's message (anatomy: 51–59% of deaths of wrapped faces at 63 cells contain a one-generation fall of at
least half the face); my 48-cell 4×4 torus: 59.3 ± 2.0% (`pops.py 48 p48b.txt.pop`, 597 deaths); my pilot in bands
of a living 144-cell tube (200,000 generations): the share of band-emptying events with the band's density ≥ 0.70
one to three generations before falls with width: 58% at 2 units, 41% at 3, 32% at 4, 24% at 5 (45 events).

Forecast, share of deaths with a one-generation fall of at least half the face, loop²-12 tubes:
60 cells (1,8),(0,20): 48 ± 8%; 72 cells (4,4),(0,6): 37 ± 8%; 84 cells (1,12),(0,28): 27 ± 8%. P(all three
within) = 30%; P(the share falls monotonically from 60 to 84 cells by at least 10 points in all) = 65%.
Alternative I give 15%: the share is what my fitted tube form would say if its correction term were the boom
route, 2e^(−L/2)/(1 + 2e^(−L/2)) = 14%, 9%, 6%. Alternative I give 20%: no trend (all three within 6 points of 55%).
Wide tori (1,4),(0,21) (63 cells) and (1,4),(0,28) (84 cells): 57 ± 5% and 52 ± 8%.

### Block C scored (04:05 UTC; `python3 pops.py A data/paths_*.pop`)

Share of deaths with a one-generation fall of at least half the face: 60 cells 56.7 ± 1.1% (forecast 48 ± 8: miss),
72 cells 56.3 ± 1.7% (37 ± 8: miss), 84 cells 51.3 ± 4.7% (113 deaths; 27 ± 8: miss). No fall of 10 points: **miss**;
the "no trend" alternative I gave 20% is the nearest. The mixture reading (14, 9, 6%), which I gave 15%, is dead.
Wide tori: not measured (dropped for time).
A2, second half (wide 84-cell torus within 15 points of the tube's band-first share): not measured.

## Block D, 04:07 UTC: tails of the living tube's population against length — before any histogram

`tube1d pophist` for loop²-12 tubes of length 5, 7, 9, 12, 16 (3·10⁶ generations each). The band's price falls
with width and that is a property of the living state at one time; do the population's own tails show it?
Local price per cell = Δ(−ln P)/ΔA between consecutive lengths at fixed density threshold x.

- D1. Upper tail P(pop ≥ 0.70 A): the price between 7 and 12 units is below the price between 5 and 7 by more
  than 0.002 per cell: P = 55%. (If the over-full fluctuation is a sum of nearly independent pieces it is flat
  to 0.001: P = 35%.)
- D2. Lower tail P(pop ≤ 0.32 A): same statement: P = 60%.
- D3. The sum of the upper-tail price at x = 0.74 and whatever the rest costs is not checkable today; no forecast.

### Block D scored (04:19 UTC; `python3 tails.py data/ph_L*.txt`)

- D1 **miss by a hair**: upper tail, price 7→12 units below price 5→7 by 0.0018 at pop ≥ 2A/3 and by 0.0018 ± 0.001
  at pop ≥ 3A/4 (I said more than 0.002 at 55%). The fall is that of an A^(−1/2) prefactor.
- D2 **hit**: lower tail at pop ≤ A/3: 0.0397 against 0.0373, lower by 0.0024.

### Block A1 and B, note (04:16 UTC)

The band numbers quoted in block B were from the first run. Pooled over five runs the price from 4.5 to 5 units is
0.2141 ± 0.0024 (not 0.2103 ± 0.0033) and from 4 to 6 units 0.2117 ± 0.0021 (A1 still a hit). The forecast for the
120-cell tube stands as frozen: 24.563 ± 0.030. Fits made after it: 24.545 (bands + tubes, exponential), 24.56–24.57
(tubes, two-route form), 24.557 (tubes, power law p = 0.75), 24.584 (p = 1/2), 24.530 (p = 1).

### Block B, band forecasts at other girths (04:23 UTC)

- "Marginal band price from 4 to 6 units at loop² 16 above loop² 12's" (70%): **void**. At loop² 16 the band
  statistic measures transverse firewalls and the dead stretches between them (price 0.02–0.08 per cell, bands
  lasting 30–110 generations), not flashes.
- "At loop² 9 it is below" (65%): not measured.
- "At every girth the age profile is flat, a flash" (80%): **miss** at loop² 16 for the same reason (every bin has
  been empty for 32–63+ generations); at loop² 12 it is flat.

## Block E, 04:24 UTC: bands at loop² 13 (tube (1,3),(0,50), length 12.0, one run of 1.2·10⁷ generations) — before its output

- E1. Price per cell of an empty band from 3.5 to 4 units: 0.2200 ± 0.0020 (loop² 12: 0.2190 ± 0.0005). P(within) =
  55%; P(above loop² 12's) = 65%.
- E2. A flash again (age profile flat, edge-to-middle difference under 1 generation at 5 units; durations of
  complete emptiness under 3 generations): 90%.
- E3. Boom share at 5 units within 5 points of loop² 12's 52.6%: 60%.
- E4. −ln P(band of 6 units) − ln τ_face((1,3),(0,25), length 6.005, 15.5250) = 3.9 ± 0.3: 60%.
