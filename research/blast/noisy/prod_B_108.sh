#!/bin/sh
# STAGE B. 108 cells (R = 15), blind: the frozen sampler at eps = 1/16, 1/32, 1/64 (M = 128, 64, 32 of B = 2048).
#   sh research/blast/noisy/prod_B_108.sh            4 cores, about 2.5 hours (39, 29, 24 s per replication, estimated from 84 cells)
# Forecast frozen in PREDICTIONS.md block 2. Gump on file: 23.3392 +- 0.0099.
# Cores: two at eps = 1/16 (2 x 22 runs x 10 replications), one at eps = 1/32 (30 runs x 10), one at eps = 1/64 (36 runs x 10).
# Analyse: python3 research/blast/noisy/fit.py   (per-eps values, the line in eps, intercept minus gump).
HERE=$(cd "$(dirname "$0")" && pwd)
sh $HERE/run_sub.sh 15 128 15100 22 & sh $HERE/run_sub.sh 15 128 15200 22 & sh $HERE/run_sub.sh 15 64 15300 30 & sh $HERE/run_sub.sh 15 32 15400 36 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
