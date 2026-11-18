#!/bin/sh
# STAGE A2. The frozen sampler at 84 cells (R = 13) at eps = 1/64, 1/32 and 1/4 (eps = 1/16 was run during the build).
#   sh research/blast/noisy/prod_A_sub84.sh          3 cores, about 1.5 hours (9, 11, 30 s per replication)
# eps = 1/64 (M = 16): 60 runs x 10 replications (its replications scatter by half the mean: many are needed);
# eps = 1/32 (M = 32): 40 runs x 10; eps = 1/4 (M = 256): 16 runs x 10. Compare with gump (18.141) and with stage A1.
# Analyse: python3 research/blast/noisy/fit.py   (part 2) and  python3 research/blast/noisy/ana.py
HERE=$(cd "$(dirname "$0")" && pwd)
sh $HERE/run_sub.sh 13 16 13400 60 & sh $HERE/run_sub.sh 13 32 13300 40 & sh $HERE/run_sub.sh 13 256 13800 16 &
wait
echo "done; analyse with: python3 research/blast/noisy/fit.py"
