#!/bin/sh
# One row of rd: sh research/blast/ref-density/row.sh TAG R SEED GENS M D0 COIN [LAGGENS]  -> scratch rows/TAG.txt
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/ref-density; mkdir -p $S/rows
[ -x $S/rd ] || gcc -O3 -march=native -o $S/rd $HERE/rd.c -lm
OUT=$S/rows/$1.txt; grep -q '^RESULT' $OUT 2>/dev/null && exit 0
nice -n 10 $S/rd $2 run $3 $4 $5 $6 $7 ${8:-0} 500000 > $OUT.part && mv $OUT.part $OUT
