# research/blast/ref-hull: referee's second measurement of the hull-face lifetime (independent code)

Standing account. Code written from `reference/oracle.py` and `docs/AUTOMATON.md` alone; split-hull's code,
calibration table, results and PREDICTIONS were not opened before the numbers below were committed.

## 1. Validation of the stepper [measured]

`rh.c` (bit-sliced, 256 hulls per step; cells = doubled coordinates with exactly one odd, |x|+|y|+|z| ≤ R; twelve
neighbours built from the oracle's offsets; outside the hull = dead). Cell counts 510, 876, 1,386, 2,064, 2,934
for R = 9 … 17 (`./rh val R 1 0 | head -1`).

    gcc -O3 -march=native -o rh rh.c -lm
    python3 validate.py 11 1 1200      # PASSED: 3 lanes x 1,200 generations identical to the oracle, state for state
    python3 validate.py 15 2 1200      # PASSED: same
    python3 validate.py 11 1 1200 1    # negative control (one neighbour of one cell swapped): FAILED at generation 1-5
    python3 validate.py 15 2 1200 1    # negative control: FAILED at generation 1-2

The oracle runs the same soup (density 0.35 inside the hull) in a padded box of side 2R+10; the check also asserts
that the oracle has no live cell outside the hull. Output kept in `out/validation.txt`.
Not checked: R = 9, 13, 17 against the oracle (same code path, only R differs).
