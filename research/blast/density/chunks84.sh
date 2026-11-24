#!/bin/sh
# Item 3 of the third task: 84 cells (R = 13), coins alone (full replacement, DO = 1) at p = 0.385, in chunks of
# 5,000,000 generations on fresh seeds (8890, 8891, ...), one after another on one core, until the file STOP exists in
# scratch or the clock passes $UNTIL (epoch seconds). Each chunk is a row file R13_fullDO1_p0.385_s<seed>.txt.
#   UNTIL=$(( $(date +%s) + 8000 )) sh research/blast/density/chunks84.sh
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/density; seed=8890
while [ ! -f $S/STOP ] && [ $(date +%s) -lt ${UNTIL:-0} ]; do
  DO=1 NZD_FULL=1 NZD_BIN=nzd_prod4 sh $HERE/row.sh R13_fullDO1_p0.385 13 $seed 5000000 0 1 0.385
  seed=$((seed + 1))
done
