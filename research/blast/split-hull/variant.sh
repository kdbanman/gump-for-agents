#!/bin/sh
# Replications of the sampler with another lag and number of flips (not the frozen setting; for the bias study).
#   sh research/blast/split-hull/variant.sh R FIRSTSEED NREP LAG NFLIP TAG   -> scratch runs/R<R>_<TAG>.txt
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/../../scratch/blast/split-hull
mkdir -p $OUT/runs
R=$1; S=$2; N=$3; LAG=$4; NF=$5; TAG=$6
i=0
while [ $i -lt $N ]; do
  seed=$((S + i))
  nice -n 10 $OUT/shf $R $seed 300000 $LAG $NF 3 0.5 - 100000 >> $OUT/runs/R${R}_$TAG.txt
  i=$((i + 1))
done
