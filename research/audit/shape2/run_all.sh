#!/bin/bash
# Production runs of the review of research/shape2 (ts.c, renewal, W=16 -> 1,024 replicas, cap 5e5, checks every 8).
# Seeds and sizes fixed here before any run; no stopping rule; restartable (a finished job is skipped).
#   nohup bash research/audit/shape2/run_all.sh > research/scratch/audit_shape2/run_all.log 2>&1 &
cd "$(dirname "$0")/../../.."
T=research/audit/shape2/drv.py; S=research/scratch/audit_shape2
job() { core=$1; a=$2; k=$3; b=$4; g=$5; s=$6; f=$S/sum_${a}_${k}_${b}_c500000_s$s.txt
        [ -s "$f" ] || taskset -c $core python3 $T run $a $k $b 16 $g $s; }
# lane 0: A = 60 pair of claim 4, (16;19); then A = 60 systole^2 12 (12;25)
( for s in 101 102 103; do job 0 1 5 20 11000000 $s; done; for s in 131 132; do job 0 1 8 20 5000000 $s; done ) &
# lane 1: A = 60 pair of claim 4, (16;21); then A = 60 systole^2 12 (12;28)
( for s in 111 112 113; do job 1 1 4 20 11000000 $s; done; for s in 141 142; do job 1 2 2 10 5000000 $s; done ) &
# lane 2: A = 48 claim 3/4 classes; thin tori at 48 and 60
( for L in "2 2 8 201" "1 6 16 211" "1 3 16 221" "4 0 4 231"; do set -- $L
    for i in 0 1 2; do job 2 $1 $2 $3 1500000 $(( $4 + i )); done; done
  job 2 1 0 16 20000 301; job 2 1 0 20 20000 302
  for L in "1 1 16 311" "2 0 8 321" "1 7 16 331"; do set -- $L; for i in 0 1; do job 2 $1 $2 $3 1000000 $(( $4 + i )); done; done
  for i in 0 1; do job 2 1 2 16 1500000 $(( 341 + i )); done
  for i in 0 1; do job 2 1 1 20 1000000 $(( 351 + i )); done
  for L in "1 9 20 361" "2 0 10 371"; do set -- $L; for i in 0 1 2; do job 2 $1 $2 $3 1200000 $(( $4 + i )); done; done
  for i in 0 1 2; do job 2 1 2 20 3000000 $(( 381 + i )); done ) &
wait; echo ALL DONE
