# Forecasts of the blast (2026-11-18), frozen before the data

Each block: who, UTC time, what was known, the numbers with errors and probabilities. Scored below each block
when the data arrive. Agents' own forecasts are in `research/blast/<agent>/PREDICTIONS.md`.

## Block 0: the PI, 03:50 UTC, before reading "Chain 3" of research/gpu-local/README.md and before any agent has run

Known to me: the anchors in BRIEF-COMMON.md and nothing about the 96-cell faces with loop² 16 and 13 or the extra
seeds on the long tubes. These are quick, by hand, and I hold them weakly.

| face | cells | my forecast | reasoning | P(within my error) |
|---|---:|---|---|---:|
| (1,3),(0,32), one loop² 13 | 96 | 19.820 ± 0.012 | 15.5250 at 75 cells, slope bending from 0.2060 to about 0.2045 as the 12-tube's did | 45% |
| (4,0),(0,8) or (1,8),(0,32), one loop² 16 | 96 | 19.935 ± 0.012 | wide line less 0.054 at 63 cells, slope 0.2072 with a slight bend (length 6.9 units) | 45% |
| (1,18),(0,40), one loop² 12 | 120 | 24.56 ± 0.03 | 22.1557 at 108 cells plus 12 × 0.2005; I expect the local slope to keep falling slowly (0.2019 from 84 to 96, 0.2013 from 96 to 108) | 50% |

Qualitative, same time:
- P(the local slope of the loop-12 tube from 108 to 120 cells is below 0.2030) = 85%; below 0.2000: 35%.
- P(tubes of loop² 13 and 16 also fall below their 54–84-cell lines by 96 cells, by more than 0.010) = 65% and 45%.
- P(the 135-cell hull face, once someone reaches it to ± 0.03, is nearer 29.230 than 29.163) = 50%. I have no view
  yet; a prefactor A^(−1.5) on the wrapped price would put it at 29.205.
