#!/bin/bash
# Every class of index 16 and 20, and the five index-24 classes research/shape did not run, in its canonical
# presentation (research/shape2/lattice2.py): layer-period check and 3,999 generations against the engine.
#   bash research/shape2/validate_all.sh > research/scratch/shape2/validate.log
cd "$(dirname "$0")/../.."
R=research/shape2/run2.py
for t in "1 0 16" "1 1 16" "2 0 8" "1 7 16" "1 2 16" "2 2 8" "1 6 16" "1 3 16" "4 0 4"; do
  python3 $R check $t | tail -1; python3 $R validate $t 4000 16; done
for t in "1 0 20" "1 1 20" "1 9 20" "2 0 10" "1 2 20" "1 8 20" "2 2 10" "1 3 20" "1 5 20" "1 4 20"; do
  python3 $R check $t | tail -1; python3 $R validate $t 4000 20; done
for t in "1 0 24" "1 1 24" "2 0 12" "1 11 24" "1 2 24"; do
  python3 $R check $t | tail -1; python3 $R validate $t 4000 24; done
