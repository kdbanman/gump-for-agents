#!/bin/sh
# STAGE C. 135 cells (R = 17): the frozen sampler at eps = 1/4, 1/16, 1/64 (M = 1024, 256, 64 of B = 4096).
#   sh research/blast/noisy/prod_C_135.sh [ROUND=1]  4 cores, about 9 hours per round; rounds use fresh seeds and add up
# Per round: eps = 1/4: 10 runs x 10 replications; eps = 1/16: 2 x 18 runs x 10; eps = 1/64: 40 runs x 10.
# Output usable at any time. Analyse: python3 research/blast/noisy/fit.py  (running values show whether the tail is met).
HERE=$(cd "$(dirname "$0")" && pwd); RD=${1:-1}
sh $HERE/run_sub.sh 17 1024 $((17800 + 1000 * RD)) 10 & sh $HERE/run_sub.sh 17 256 $((17100 + 1000 * RD)) 18 & sh $HERE/run_sub.sh 17 256 $((17200 + 1000 * RD)) 18 & sh $HERE/run_sub.sh 17 64 $((17400 + 1000 * RD)) 40 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
