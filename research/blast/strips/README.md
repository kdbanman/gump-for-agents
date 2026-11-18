# blast/strips: rimmed faces without corners, and the tetrahedron (agent `strips`, 2026-11-18, second phase)

**Interim (12:45 UTC); runs in progress. Results below are being filled in; see the end for what exists now.**

Task (from the PI, as corrected at 12:35): referee agent `rim`'s table of corner-free strips with independent code,
extend it to (4 unit rows, L = 7) and (5 unit rows, L = 6), compare a strip's row with a closed tube's row of the
same girth, time the tetrahedron's faces, and say whether a strip's width price and length price meet and where.

Code: `strips.c` (own AVX-512 bit-sliced graph stepper, 512 replicas; vessels cut by diagonal half-spaces,
optionally periodic), `validate.py`/`validate.sh` (state for state against `reference/oracle.py`, with a negative
control), `table.py` (all tables from the `LIFE` lines under `data/runs/`). Forecasts: `PREDICTIONS.md`
(block A, commit 993537c, 12:36 UTC, before any lifetime).

Calibration on the octahedron (all first deaths, T0 = 200 / 300): R = 7: 6.8067 ± 0.0016 (anchor 6.804 ± 0.003);
R = 9: 9.8270 ± 0.0026 (anchor 9.819 ± 0.003; rim's code 9.8214 ± 0.0009).
First strip: (4 rows, L = 4) 11.0983 ± 0.0041 at T0 = 200 (rim 11.0912 ± 0.0032); by age the hazard is not steady
before about 1,000 generations (11.19, 11.14, 11.11 in the age bins from 200, 400, 800; 11.09–11.10 after), so
T0 = 1000 is used from here on.
