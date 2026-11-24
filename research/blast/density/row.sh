#!/bin/sh
# One row of the control: nzd brute, full output (BRUTE, BIAS, REC lines) to scratch rows/TAG_sSEED.txt.
#   sh research/blast/density/row.sh TAG R SEED GENS M DW BIAS          (DO = 3 unless env DO is set; env NZD_* passes through)
# Binary: scratch nzd_prod (built once from nzd.c), or $NZD_BIN (nzd_lay for the layer diagnostics, NZD_LAYERS=1).
# eps = 1/4 at R = 11: M = 256 for DW = 1 (B = 1024), M = 128 for DW = 2..5 (B = 512), M = 64 for DW = 6 (B = 256).
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/density; mkdir -p $S/rows
BIN=${NZD_BIN:-nzd_prod}; [ -x $S/$BIN ] || gcc -O3 -march=native -o $S/$BIN $HERE/nzd.c -lm
OUT=$S/rows/$1_s$3.txt
[ -s $OUT ] && grep -q '^REC' $OUT && { echo "have $OUT"; exit 0; }
nice -n 10 $S/$BIN $2 brute $3 $4 $5 $6 ${DO:-3} $7 > $OUT.part && mv $OUT.part $OUT
