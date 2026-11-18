#!/bin/sh
# One replication after another of the frozen sampler (parameters fixed at 03:52 UTC on R = 9 and 11 only).
#   sh research/blast/split-hull/chain.sh R FIRSTSEED NREP     -> research/scratch/blast/split-hull/runs/R<R>.txt
# and one file of dying paths per replication, runs/paths_R<R>_s<seed>.txt
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/../../scratch/blast/split-hull
mkdir -p $OUT/runs
[ -x $OUT/shf ] || gcc -O3 -march=native -o $OUT/shf $HERE/sh.c -lm
R=$1; S=$2; N=$3
i=0
while [ $i -lt $N ]; do
  seed=$((S + i))
  nice -n 10 $OUT/shf $R $seed 300000 2 -6 3 0.5 $OUT/runs/paths_R${R}_s${seed}.txt 100000 >> $OUT/runs/R$R.txt
  i=$((i + 1))
done
