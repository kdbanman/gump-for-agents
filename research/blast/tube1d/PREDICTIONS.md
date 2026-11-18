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
