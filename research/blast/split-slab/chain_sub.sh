#!/bin/bash
# subset sampler on the dice chain WD=6, version 2 (focused proposals, WBACK=12): calibration tori, 120, long tubes, a wide 192-cell torus
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
python3 run_sub.py 1 17 32 16 2
python3 run_sub.py 1 16 36 16 2 paths
python3 run_sub.py 1 18 40 16 2 paths
python3 run_sub.py 1 22 48 8 2 paths
python3 run_sub.py 1 30 64 8 2 paths
python3 run_sub.py 8 0 8 8 2 paths
python3 run_sub.py 1 38 80 6 2 paths
touch $S/chain_sub.done
