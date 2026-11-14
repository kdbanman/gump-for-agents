#!/bin/bash
# Production runs of the review (independent stepper ts.c). Three cores; each job ~5 min; restartable (seeds fixed).
#   bash research/audit/shape/run_all.sh > research/scratch/audit_shape/run_all.log 2>&1 &
cd "$(dirname "$0")/../../.."
T=research/audit/shape/ts.py
job() { core=$1; shift; f=research/scratch/audit_shape/sum_$1_$2_$3_c500000_s$6.txt; [ -s "$f" ] || taskset -c $core python3 $T run "$@"; }
( for s in 1 2 3; do job 0 4 0 5 16 4800000 $s; done ) &
( for s in 11 12 13; do job 1 5 1 4 16 4800000 $s; done ) &
( for s in 21 22; do job 2 4 1 6 16 5500000 $s; done; for s in 31 32; do job 2 4 0 6 16 5500000 $s; done ) &
wait
echo ALL DONE
