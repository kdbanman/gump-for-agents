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
