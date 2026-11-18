#!/bin/sh
# Subset simulation on the hull dice chain, frozen parameters (PREDICTIONS.md block 4).
#   sh research/blast/split-hull/dice.sh R SEED NREP   -> research/scratch/blast/split-hull/dice/sub_R<R>_s<SEED>.txt
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/split-hull; mkdir -p $S/dice
[ -x $S/hd ] || gcc -O3 -march=native -o $S/hd $HERE/hd.c -lm
R=$1; SEED=$2; NREP=$3
G=$S/dice/hg_${R}_$SEED.bin      # one graph file per run, so that runs in parallel never read a half-written file
set -- $(python3 $HERE/hullgeom.py $R $G); A=$2; NR=$3
case $R in 9) LAM=10;; 11) LAM=18;; 13) LAM=28;; 15) LAM=38;; 17) LAM=51;; 19) LAM=65;; 21) LAM=80;; esac
NSW=$(python3 -c "print(round($A / 6))")
WD=6 NR=$NR nice -n 10 $S/hd $G sub $SEED $NREP $LAM 3 8 $NSW 5 32 24 - 12 > $S/dice/sub_R${R}_s$SEED.txt
rm -f $G
grep SUMMARY $S/dice/sub_R${R}_s$SEED.txt
