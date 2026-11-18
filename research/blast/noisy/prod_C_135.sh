#!/bin/sh
# STAGE C. 135 cells (R = 17): the frozen sampler at eps = 1/16, 1/32, 1/64 (M = 256, 128, 64 of B = 4096).
#   sh research/blast/noisy/prod_C_135.sh [ROUND=1]  4 cores, about 8 hours per round; rounds use fresh seeds and add up
# Per round: eps = 1/16: 2 x 15 runs x 10 replications (about 185 s each, estimated); eps = 1/32: 25 runs x 10 (110 s);
# eps = 1/64: 40 runs x 10 (70 s).
# Output usable at any time. Analyse: python3 research/blast/noisy/fit.py  (running values show whether the tail is met).
HERE=$(cd "$(dirname "$0")" && pwd); RD=${1:-1}
sh $HERE/run_sub.sh 17 256 $((17100 + 1000 * RD)) 15 & sh $HERE/run_sub.sh 17 256 $((17200 + 1000 * RD)) 15 & sh $HERE/run_sub.sh 17 128 $((17300 + 1000 * RD)) 25 & sh $HERE/run_sub.sh 17 64 $((17400 + 1000 * RD)) 40 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
