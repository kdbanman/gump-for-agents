#!/bin/bash
# subset sampler v2, fourth chain (04:22 UTC; replaces the tails of chains 2 and 3): the 192-cell tube against the wide 192-cell torus
# first, the PI's path check at 63 and 84 cells, more 120, the 240-cell tube last. Stopped at 04:44 UTC wherever it is.
cd "$(dirname "$0")"
while pgrep -f "run_sub.py 1 30 64 8 2" > /dev/null; do sleep 2; done
python3 run_sub.py 8 0 8 6 2 paths
python3 run_sub.py 1 4 21 16 4 paths
python3 run_sub.py 1 12 28 16 4 paths
python3 run_sub.py 1 30 64 8 3 paths
python3 run_sub.py 8 0 8 6 3 paths
python3 run_sub.py 1 18 40 16 3
python3 run_sub.py 1 38 80 5 2 paths
