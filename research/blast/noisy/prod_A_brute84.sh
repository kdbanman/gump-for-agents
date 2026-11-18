#!/bin/sh
# STAGE A1. Brute force of the noisy chain at 84 cells (R = 13): the offset against eps where gump is known (18.141).
#   sh research/blast/noisy/prod_A_brute84.sh        4 cores, about 2.5 hours (the eps = 1/16 part 1.5); no attention needed
# Three processes at eps = 1/16 (M = 64) and one at eps = 1/64 (M = 16), each in chunks of 5,000,000 generations x 512
# hulls with its own seeds; every finished chunk is one line in research/scratch/blast/noisy/brute84/<name>.txt, so the
# run can be stopped at any time. Target: about 2,000 lives ended by the watched face per eps (+- 0.022 in ln tau).
# Analyse: python3 research/blast/noisy/fit.py   (part 1: ln tau_watched minus gump's anchor at R = 13).
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; mkdir -p $S/brute84
[ -x $S/nz ] || gcc -O3 -march=native -o $S/nz $HERE/nz.c -lm
one() { M=$1; SEED0=$2; CHUNKS=$3; i=0; while [ $i -lt $CHUNKS ]; do nice -n 10 $S/nz 13 brute $((SEED0 + i)) 5000000 $M >> $S/brute84/M${M}_s$SEED0.txt; i=$((i + 1)); done; }
one 64 84100 20 & one 64 84200 20 & one 64 84300 20 & one 16 84400 59 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
