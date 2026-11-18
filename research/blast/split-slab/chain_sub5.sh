#!/bin/bash
# subset sampler v2, fifth chain (04:36 UTC; replaces the tail of chain 4): a wide calibration torus at 108 cells, the anchor (6,0),(0,6),
# then more 120. The 240-cell tube was dropped (5 replications would have said nothing).
cd "$(dirname "$0")"
while pgrep -f "run_sub.py 8 0 8 6 3" > /dev/null; do sleep 2; done
python3 run_sub.py 6 0 6 24 2 paths
python3 run_sub.py 1 18 40 16 3
