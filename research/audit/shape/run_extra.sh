#!/bin/bash
# Third stage: one job each on three more A = 72 tori (systole^2 9, 12, 19). Restartable.
cd "$(dirname "$0")/../../.."
T=research/audit/shape/ts.py; S=research/scratch/audit_shape
job() { core=$1; shift; f=$S/sum_$1_$2_$3_c500000_s$6.txt; [ -s "$f" ] || taskset -c $core python3 $T run "$@"; }
job 0 3 0 8 16 5500000 41 & job 1 4 4 6 16 5500000 51 & job 2 2 3 12 16 5500000 61 & wait; echo EXTRA DONE
