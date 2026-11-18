#!/bin/sh
# As dice.sh, but also writes every dying chain's population series (S lines) and, for 8 dying chains per batch, the
# face's cells in the 16 generations before the death (C lines).
#   sh research/blast/split-hull/dice_paths.sh R SEED NREP  -> scratch dice/paths_R<R>_s<SEED>.txt, dice/cells_R<R>_s<SEED>.txt
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/split-hull; mkdir -p $S/dice
[ -x $S/hd ] || gcc -O3 -march=native -o $S/hd $HERE/hd.c -lm
R=$1; SEED=$2; NREP=$3
set -- $(python3 $HERE/hullgeom.py $R $S/hgp_$R.bin); A=$2; NR=$3
case $R in 9) LAM=10;; 11) LAM=18;; 13) LAM=28;; 15) LAM=38;; 17) LAM=51;; 19) LAM=65;; 21) LAM=80;; esac
NSW=$(python3 -c "print(round($A / 6))")
WD=6 NR=$NR nice -n 10 $S/hd $S/hgp_$R.bin sub $SEED $NREP $LAM 3 8 $NSW 5 32 24 $S/dice/paths_R${R}_s$SEED.txt 12 $S/dice/cells_R${R}_s$SEED.txt > $S/dice/pathrun_R${R}_s$SEED.txt
grep SUMMARY $S/dice/pathrun_R${R}_s$SEED.txt
