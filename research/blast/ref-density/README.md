# research/blast/ref-density: referee of research/blast/density (commit 9a105d3)

The findings are in `REVIEW.md`; forecasts in `PREDICTIONS.md` (written before the rows they score).

Files:
- `rd.c` — independent stepper and dart process (bit-sliced, 512 lanes), written from `reference/oracle.py` and the
  READMEs' prose; header = the exact law. `validate.py` — bit-for-bit check against the oracle with a negative
  control (`validate_1200.txt`).
- `row.sh` (one row of `rd`), `nzdrow.sh` (`nzd.c` at 9a105d3 as a black box), `worker.sh` (two workers on one
  queue file), `collect.py` (all tables), `lagdump.py` (lagged and Granger analysis of a time-series dump),
  `seedstream.py` (nzd.c's second random stream for consecutive seeds), `skin2.py` (second review: the skin rows at
  full replacement, `RD_FULL=1`; its redraw's validation in `data/fulltest.txt`).
- `data/rows/` (my rows' full outputs), `data/nzd/` (nzd.c's outputs: R = 9 rows, fair at R = 11, and its layer
  diagnostics on the whole-layer copy chain), `data/lagdump_gump_R11_s1101.txt`.
- Bulk (the 77 MB dump): `research/scratch/blast/ref-density/`.
