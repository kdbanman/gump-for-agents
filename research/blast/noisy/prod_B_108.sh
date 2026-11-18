#!/bin/sh
# STAGE B. 108 cells (R = 15), blind: the frozen sampler at eps = 1/4, 1/16, 1/64 (M = 512, 128, 32 of B = 2048).
#   sh research/blast/noisy/prod_B_108.sh            4 cores, about 3.5 hours
# Forecast frozen in PREDICTIONS.md block 2. Gump on file: 23.3392 +- 0.0099.
# Cores: one at eps = 1/4 (12 runs x 10), two at eps = 1/16 (2 x 20 runs x 10), one at eps = 1/64 (45 runs x 10).
# Analyse: python3 research/blast/noisy/fit.py   (per-eps values, the line in eps, intercept minus gump).
HERE=$(cd "$(dirname "$0")" && pwd)
sh $HERE/run_sub.sh 15 512 15800 12 & sh $HERE/run_sub.sh 15 128 15100 20 & sh $HERE/run_sub.sh 15 128 15200 20 & sh $HERE/run_sub.sh 15 32 15400 45 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
