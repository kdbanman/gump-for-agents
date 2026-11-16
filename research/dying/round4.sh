#!/bin/bash
# Round 4 run plan (fixed with the "Round 4 definitions" note of PREDICTIONS.md, before any production run).
#   bash research/dying/round4.sh 1 & bash research/dying/round4.sh 2 & bash research/dying/round4.sh 3 & wait
# (three cores, about 2 hours). Needs research/scratch/dying/r4/ex4 and the graph files g_v1{1,3,5}c_c1.txt, both
# written by `python3 research/dying/validate4.py` (which must print ALL OK first).
# ex4 = the review's r3_ex.c (validated against reference/oracle.py) with catches at six levels; 256 lanes, soup 0.4,
# events every generation, Brent settled test, T0 = 512. Fresh seeds 4411, 4413, 4415, 4416 (keep stream: seed + 1000).
# PBAR: the study's 31.29, 42.49, 55.14 (same integer thresholds as the review's 31.25, 42.45, 55.19).
# Levels p = 0.9, 0.75, 0.6, 0.45, 0.3, 0.15 -> P <= floor(p PBAR). Keep probabilities sized from data/r3_excursions.csv
# for about 150,000 catches per level (all catches where fewer are expected).
D=/home/user/gump-for-agents/research/scratch/dying/r4; cd $D || exit 1
x() { # name seed gens pbar levels probs sampk
  b=r4_$1_s$2; [ -s $b.json ] && return
  ./ex4 g_$1_c1.txt run $2 0.4 $3 $b.lives /dev/null $b.smp $7 /dev/null 0 1 512 $4 $b.x $b.cat $5 $6 $(( $2 + 1000 )) > $b.json.tmp && mv $b.json.tmp $b.json; }
if [ "$1" = 1 ]; then
  x v15c 4415 45000000 55.14 49,41,33,24,16,8 2e-5,1.2e-4,2e-3,0.1,1,1 77000
elif [ "$1" = 2 ]; then
  x v15c 4416 45000000 55.14 49,41,33,24,16,8 2e-5,1.2e-4,2e-3,0.1,1,1 77000
elif [ "$1" = 3 ]; then
  x v13c 4413 40000000 42.49 38,31,25,19,12,6 2e-5,1e-4,8e-4,0.011,0.35,1 68000
  x v11c 4411 20000000 31.29 28,23,18,14,9,4 4e-5,1.3e-4,7e-4,4e-3,0.15,0.6 34000
fi
