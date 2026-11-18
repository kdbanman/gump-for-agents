#!/bin/bash
# subset sampler v2, third chain: more replications on the long tubes and the wide torus (stopped at 04:44 UTC wherever it is)
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
while [ ! -e $S/chain_sub.done ]; do sleep 3; done
python3 run_sub.py 1 30 64 8 3
python3 run_sub.py 8 0 8 6 3
python3 run_sub.py 1 38 80 5 3
python3 run_sub.py 1 22 48 8 3
