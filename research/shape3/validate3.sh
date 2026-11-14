#!/bin/bash
# Validate ts3 on every torus of the run plan: (1) population x copies equals the engine's on the cubic N-torus
# (N = index) at every generation for 4,000 generations, AVX-512 path (W = 8, replica 0); (2) ts3 and the review's
# unmodified ts.c write identical event files for 512 replicas (W = 8) over a short renewal run.
#   bash research/shape3/validate3.sh > research/scratch/shape3/validate.log 2>&1
cd "$(dirname "$0")/../.."
D=research/shape3/drv3.py
for L in "1 6 24" "2 4 12" "1 5 24" "2 2 12" "1 10 24" "1 5 20" "1 4 20" "1 8 20" "2 2 10" "2 2 8" "1 6 16" \
         "1 4 12" "1 3 12" "1 5 15" "1 4 15" "3 0 6" "1 5 18" "1 6 21" "1 7 21"; do
  set -- $L; N=$(( $1 * $3 ))
  taskset -c 3 python3 $D validate $1 $2 $3 4000 $N || echo "VALIDATE FAIL $L"
  taskset -c 3 python3 $D same $1 $2 $3 60000 7 || echo "SAME FAIL $L"
done
echo VALIDATION DONE
