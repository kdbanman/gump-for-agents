#!/bin/bash
# the independent SAT runs of REVIEW-signals-5, one after another, each cut at 1500 s
cd "$(dirname "$0")"
OUT=../../scratch/audit/signals5/mysat.txt
for args in "33" "33 --solver kissat404" "31 --mult 2 --multB 2" "35" "33 --word 0,1" "33 --word 0,2,4" "33 --mult 2 --multB 2" "37"; do
  ( timeout 1500 python3 mysat5.py $args ) >> $OUT 2>&1 || echo "  CUT or error: $args" >> $OUT
done
