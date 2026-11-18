#!/bin/sh
# Replications of the sampler with another lag and number of flips (not the frozen setting; for the bias study).
#   sh research/blast/split-hull/variant.sh R FIRSTSEED NREP LAG NFLIP TAG [MODE]   -> scratch runs/R<R>_<TAG>.txt
# MODE 1: donor swap (everything at depth >= 2 LAG + 1 beneath the watched face replaced by an independent hull's).
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/../../scratch/blast/split-hull
mkdir -p $OUT/runs
R=$1; S=$2; N=$3; LAG=$4; NF=$5; TAG=$6; MODE=${7:-0}
[ -x $OUT/shs ] || gcc -O3 -march=native -o $OUT/shs $HERE/sh.c -lm
i=0
while [ $i -lt $N ]; do
  seed=$((S + i))
  nice -n 10 $OUT/shs $R $seed 300000 $LAG $NF 3 0.5 $OUT/runs/paths_R${R}_${TAG}_s${seed}.txt 100000 $MODE >> $OUT/runs/R${R}_$TAG.txt
  i=$((i + 1))
done
