# The wrapping law: forecasts written before any new face is measured

The lead, 2026-11-15 13:02 UTC. The law and how it was found are in `research/NOTEBOOK.md` (entry "the kink is the
wrapping") and `research/audit/wrap_law_lead.py`. In one line: a wrapped face of A cells whose closed loops all have
squared length ≥ 12 lives

    ln τ_face = 13.1629 + 0.20860·(A − 63) − (A − 21.25) · Σ over loop directions v of k(|v|²),
    k(12) = 0.002918, k(13) = 0.002271, k(16) = 0.001353, k(19) = 0.000338, k(q ≥ 21) = 0,

one direction per ±v. These seven numbers are frozen (`wrap_law_lead.py`, `FROZEN`); the forecast for any torus is
`python3 research/audit/wrap_law_lead.py --predict H K D`. They were fitted to 32 faces (χ² 42.0 on 25), so the fit
itself is not a test. What would be:

- **W1 (65%).** New faces: every class with shortest loop² ≥ 12 at areas not in the fit (A = 51 to 69 on the CPU),
  measured to ± 0.005 or better, lands within 0.010 of its frozen forecast, or within 3 standard errors if that is
  wider. One class outside by more than twice that margin and the law, as an additive law, is refuted.
- **W2 (70%).** New faces with every loop² ≥ 21 (no discount) land within 0.006, or 3 standard errors, of the line
  13.1629 + 0.20860·(A − 63).
- **W3 (65%).** With the new faces in, a free k(21) stays below 0.00008 (a quarter of k(19)): the discount ends
  between loop² 19 and 21 and does not tail off.
- **W4 (40%).** Additivity holds for pairs of short loops at new areas to the same accuracy as for single ones: the
  residuals of faces with two or more short directions are no larger than those with one.
- **W5 (35%).** The law extends below its range with one more number each: adding k(9) (and k(7)) with the same A0
  describes the classes of shortest loop² 9 (and 7) at χ² per degree of freedom below 2, including the sign changes
  of SH7.
- **W6 (50%).** The pairs already on file that the law gets wrong keep getting it wrong when re-measured: the two
  loop² 12 classes at A = 60 (law: equal; measured 0.0069 ± 0.0024 apart) still differ by more than 0.004. If so
  there is a second, smaller effect of loops longer than 20 at small areas.

What I expect to be wrong about: the form (A − A0). Fitted on faces of 60 cells and more it gives A0 = 27 and
puts all four 48-cell faces 0.003 to 0.013 too high, so the discount is probably not exactly linear in area.

---

## The adversarial test (research/wrap), forecasts written before any new face is run

2026-11-15 13:09 UTC (commit 93540eb). Code: `research/wrap/lattices.py` (own lattice classes and loop lists), `faces.py` (own loader
from the primary data files), `fit.py`. Table: `python3 research/wrap/fit.py forecast` → `data/forecast_out.txt`
(committed with this section). Columns: the lead's frozen law (`wrap_law_lead.py --predict`, identical numbers);
the same law refitted on every face on file (research/shape3's cap-free runs added, the 16- and 8-generation
stamping bias removed as in `faces.py`; χ² 86 on 25); and **mine: model OFF2**, a free line per loop length
(discount of a direction of length² q = u_q + w_q·A, no common A0; χ² 37 on 22, same data).

Measurement: research/shape3's `ts3` (re-validated here against `reference/oracle.py`), events every generation,
512 replicas of renewed lives from a 0.4 soup, no cap, ln τ_face = ln(2E/F) ± 1/√F, firewalls and settled lives
censoring (exactly as the card's equilateral rows when no firewall occurs).

Forecasts (ln τ_face):

| A | HNF | loops² ≤ 20 | frozen law | mine (OFF2) ± model error |
|---:|---|---|---:|---:|
| 36 | (2,2,6) | 12,12,12 | 7.4016 | 7.4452 ± 0.0068 |
| 39 | (1,3,13) | 13,13,13 | 8.0356 | 8.0403 ± 0.0112 |
| 42 | (1,3,14) | 12,13,19 | 8.6676 | 8.6751 ± 0.0034 |
| 45 | (1,3,15) | 13,13 | 9.3002 | 9.3012 ± 0.0049 |
| 51 | (1,3,17) | 13,19 | 10.5821 | 10.5800 ± 0.0018 |
| 54 | (1,4,18) | 12 | 11.1899 | 11.1909 ± 0.0009 |
| 54 | (1,3,18) | 13,19 | 11.2001 | 11.1981 ± 0.0017 |
| 57 | (1,3,19) | 13 | 11.8301 | 11.8282 ± 0.0020 |
| 63 | (1,3,21) | 13 | 13.0681 | 13.0649 ± 0.0031 |
| 63 | (1,8,21) | 19,19 | 13.1347 | 13.1374 ± 0.0011 |
| 66 | (1,5,22) | 12 | 13.6581 | 13.6497 ± 0.0015 |
| 66 | (1,3,22) | 13 | 13.6871 | 13.6833 ± 0.0037 |
| 66 | (1,4,22) | 19 (21) | 13.7736 | 13.7755 ± 0.0009 |
| 69 | (1,3,23) | 13 | 14.3061 | 14.3016 ± 0.0044 |
| 69 | (1,4,23) | 19 (21) | 14.3984 | 14.4009 ± 0.0012 |
| 75 | (1,4,25) | none (21, 25) | 15.6661 | 15.6656 ± 0.0010 |
| 60 | (1,8,20) and (2,2,10) | 12 | both 12.4240 | both 12.4203 ± 0.0010 |

(A = 75 other classes and A = 78 are in `data/forecast_out.txt`; they will be run only if time allows.)

What I expect, written now:
- **X1.** The frozen law passes W1 at A = 51–63 but misses the single loop² 12 face at A = 66 (1,5,22) by
  more than its W1 margin: measured below the frozen 13.6581, near 13.650. On file the two loop² 12 classes at
  A = 72 already lie 0.016 ± 0.003 below the law (research/shape3 values the lead's fit did not use).
- **X2.** Scored with z = (measured − forecast)/√(se² + model error²), OFF2 gives Σz² over the A = 51–69 faces no
  larger than the frozen law's.
- **X3.** A = 36 (three loops² 12) lies above the frozen 7.4016 by more than 0.02: the (A − A0) form overstates
  the discount at small A (outside the fitted range, so this scores the form, not W1).
- **X4.** W6: the A = 60 pair re-measured differs by less than 0.004 (I expect no second effect at that size).

## The lead's note after the test (2026-11-15 15:05 UTC)

Scored by the tester in `README.md` and accepted: **W1 held** (11 of 11 new faces of 51–69 cells inside the margin),
**W2 held** on two faces at ± 0.010–0.012, **W3 held as worded and only just** (the answer depends on the form),
**W4 held as worded** (but faces with one short direction sit below the law and faces with two or more above it),
**W5 failed** (nothing of this kind reaches loop² 9 or 7), **W6 failed** (the 60-cell pair no longer differs).
Four of six held, and the law is still the wrong form: with the precise values it had left out it does not fit
faces of 48 cells and up (χ² 120–141 on 41–48 by my own loader, `python3 research/audit/wrap_haz_lead.py`), and
below 48 cells it is 4 to 16σ off. A forecast that holds inside a margin of 0.010 says little about a form whose
errors are 0.003.

What my own refit adds to the tester's reading. Its replacement (HAZ: a short loop adds a second death rate whose
share grows like an exponential of the area) fits, χ² 51.8 on 38 here against its 49.6. **But two other forms with
the same number of parameters fit the same 48 faces as well or better**, and on the 39 faces with at most one short
direction the three are indistinguishable (χ² 32.8, 33.0, 36.8 on 29):

| form | discount of one loop direction | χ² on 38 |
|---|---|---:|
| LINES | k_q·(A − z_q): a straight line per loop length, zeros at 28.6, 26.3, 18.7 cells for loop² 12, 13, 16 | 46.7 |
| POW | ln(1 + r_q·(A/63)^m_q), m = 2.11, 1.91, 1.44, 0.55 | 41.3 |
| HAZ | ln(1 + r_q·e^(g_q·(A − 63))), g = 0.036, 0.033, 0.025, 0.019 | 51.8 |

So what is established is narrower than "a second way to die at 0.173 per cell": short loops discount, the
discount of one loop grows faster than my common-A0 line allowed, the lines for different loop lengths do not meet
at one area, and nothing on file says whether the growth is a straight line (a tube of fixed girth has its own
price per cell: 0.2048 for loop² 12), a power of the area, or an exponential (a price that keeps falling towards
0.173). The three part company above 80 cells, where only the card can measure.

**Forecasts for the card, frozen now** (`python3 research/audit/wrap_haz_lead.py --predict H K D`; the frozen
numbers are in that file, commit of this note):

| torus | cells | loops² ≤ 20 | old law | LINES | POW | HAZ |
|---|---:|---|---:|---:|---:|---:|
| (1, 12), (0, 28) | 84 | 12 | 17.3604 | 17.3361 | 17.3207 | 17.2941 |
| (1, 17), (0, 32) | 96 | 12 | 19.8286 | 19.7939 | 19.7608 | 19.6850 |
| (1, 16), (0, 36) | 108 | 12 | 22.2968 | 22.2518 | 22.1960 | 22.0366 |
| (1, 3), (0, 25) | 75 | 13 | 15.5440 | 15.5352 | 15.5321 | 15.5270 |
| (1, 3), (0, 28) | 84 | 13 | 17.4010 | 17.3881 | 17.3795 | 17.3614 |
| (1, 9), (0, 25) | 75 | 19 | 15.6479 | 15.6516 | 15.6512 | 15.6485 |
| (1, 5), (0, 28) | 84 | 19 | 17.5223 | 17.5277 | 17.5275 | 17.5228 |
| (4, 0), (0, 7) | 84 | 16 | 17.4586 | 17.4604 | 17.4600 | 17.4544 |
| (1, 4), (0, 26) | 78 | none | 16.2919 | 16.2908 | 16.2911 | 16.2912 |

Each form's own error on the 84-cell loop² 12 face is about ± 0.005, growing to ± 0.02 for HAZ at 108 cells.

- **W7 (40%).** The 84-cell face with one loop of 12 lands within 0.008 of LINES (17.336): the tube already has its
  own straight line. **POW 30%, HAZ 15%, the old law 5%, none of the four 10%.**
- **W8 (70%).** Whatever the form at 84 cells, the 96-cell face lands within 0.02 of the same form's forecast.
- **W9 (65%).** The face with no short loop at 78 cells, (1, 4), (0, 26), lands within 0.008 of 16.291. The tester's
  two such faces (75 and 78 cells) both came out 0.015 low, at 1.5σ and 1.2σ; if the card repeats that at ± 0.003,
  a loop of 21 does something after all.
- **W10 (75%).** The card's values for the three faces the tester also measured, (1, 3), (0, 25), (1, 9), (0, 25) and
  (1, 4), (0, 26), agree with the tester's (15.5363 ± 0.0104, 15.6575 ± 0.0106, 16.2769 ± 0.0120) to within 2.5 of
  the combined errors, all three. This is the cross-check of the tester's stepper by independent code.
