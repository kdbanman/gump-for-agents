#!/bin/sh
# nzd.c (commit 9a105d3) as a black box: sh research/blast/ref-density/nzdrow.sh TAG R SEED GENS M DW BIAS -> scratch nzd/TAG.txt
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/ref-density; mkdir -p $S/nzd
[ -x $S/nzd_9a105d3 ] || { (cd $HERE/../../.. && git show 9a105d3:research/blast/density/nzd.c) > $S/nzd_9a105d3.c && gcc -O3 -march=native -o $S/nzd_9a105d3 $S/nzd_9a105d3.c -lm; }
OUT=$S/nzd/$1.txt; grep -q '^REC' $OUT 2>/dev/null && exit 0
nice -n 10 $S/nzd_9a105d3 $2 brute $3 $4 $5 $6 3 $7 > $OUT.part && mv $OUT.part $OUT
