#!/bin/bash
# Second stage (after run_all.sh's A = 60 jobs): more A = 72 lives on cores 0 and 1. Restartable.
cd "$(dirname "$0")/../../.."
T=research/audit/shape/ts.py; S=research/scratch/audit_shape
job() { core=$1; shift; f=$S/sum_$1_$2_$3_c500000_s$6.txt; [ -s "$f" ] || taskset -c $core python3 $T run "$@"; }
( while [ ! -s $S/sum_4_0_5_c500000_s3.txt ]; do python3 -c "import time; time.sleep(10)"; done
  for s in 33 34; do job 0 4 0 6 16 5500000 $s; done ) &
( while [ ! -s $S/sum_5_1_4_c500000_s13.txt ]; do python3 -c "import time; time.sleep(10)"; done
  for s in 23 24; do job 1 4 1 6 16 5500000 $s; done ) &
wait; echo MORE DONE
