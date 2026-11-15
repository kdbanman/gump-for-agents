#!/bin/bash
# Review of dying round 4: every run behind research/audit/REVIEW-dying.md "Round 4". One core, about 20 minutes.
#   bash research/audit/dying4/run.sh
set -e
ROOT=/home/user/gump-for-agents; D=$ROOT/research/scratch/dying4; A=$ROOT/research/audit/dying4
python3 $A/validate.py                                   # builds st4, g11/g13; ALL OK
cd $D
python3 $A/geom.py 15 g15.txt
# st4 GRAPH run SEED GENS PBAR LEVELS(0.6,0.45,0.3,0.15) KEEP ATLEVEL SAMPK OUT   (seeds the study did not use)
./st4 g11.txt run 5101 3000000 31.29 18,14,9,4 0.005,0.02,0.3,1 0.0002,0.002,0.02,0.2 1000 r11     # ~4 min
./st4 g13.txt run 5103 3000000 42.49 25,19,12,6 0.002,0.005,0.1,1 0.0001,0.001,0.01,0.3 1500 r13   # ~6 min
./st4 g15.txt run 5105 1500000 55.14 33,24,16,8 0.01,0.5,1,1 0.0005,0.01,0.3,1 750 r15             # ~3 min
python3 $A/ana.py r11 11 31.29; python3 $A/ana.py r13 13 42.49; python3 $A/ana.py r15 15 55.14
python3 $A/null.py r11 11 31.29; python3 $A/null.py r13 13 42.49; python3 $A/null.py r15 15 55.14
python3 $A/dies.py
