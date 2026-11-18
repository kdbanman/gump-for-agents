#!/bin/bash
# subset sampler v2, third chain: the PI's path check at 63 and 84 cells (share of sampled deaths with a one-generation fall >= A/2),
# then more replications on the long tubes and the wide torus (stopped at 04:44 UTC wherever it is)
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
while [ ! -e $S/chain_sub.done ]; do sleep 3; done
python3 run_sub.py 1 4 21 16 4 paths
python3 run_sub.py 1 12 28 16 4 paths
python3 run_sub.py 1 30 64 8 3
python3 run_sub.py 8 0 8 6 3
python3 run_sub.py 1 38 80 5 3
