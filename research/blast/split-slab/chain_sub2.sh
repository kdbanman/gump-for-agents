#!/bin/bash
# subset sampler v2, second chain (04:12 UTC): calibration tori first, then 120, then the long tubes and a wide 192-cell torus
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
python3 run_sub.py 1 18 40 32 2 paths
python3 run_sub.py 1 16 36 32 3
python3 run_sub.py 1 17 32 32 3
python3 run_sub.py 1 22 48 8 2 paths
python3 run_sub.py 1 30 64 8 2 paths
python3 run_sub.py 8 0 8 6 2 paths
python3 run_sub.py 1 38 80 5 2 paths
python3 run_sub.py 1 18 40 32 3
python3 run_sub.py 1 12 28 32 3
touch $S/chain_sub.done
