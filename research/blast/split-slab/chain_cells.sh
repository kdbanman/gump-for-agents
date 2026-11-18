#!/bin/bash
# 04:45 UTC, for the PI's follow-up (README section 9): dying paths with every face cell recorded for the last 16 generations.
# Subset sampler on the dice chain (seed 5; these replications also enter table_sub.py), then natural deaths of gump itself.
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
python3 run_sub.py 1 30 64 10 5 cells
python3 run_sub.py 8 0 8 6 5 cells
python3 run_sub.py 1 22 48 10 5 cells
python3 run_sub.py 1 16 36 16 5 cells
python3 run_sub.py 6 0 6 16 5 cells
python3 run_sub.py 1 18 40 16 5 cells
python3 run_sub.py 1 12 28 16 5 cells
python3 run_sub.py 1 4 21 16 5 cells
nice -n 10 $S/ss_lag $S/g_1_4_21.bin lag 5 400000 - $S/cells/gump_1_4_21.txt > data/lag_cells_1_4_21.txt
nice -n 10 $S/ss_lag $S/g_1_12_28.bin lag 5 4000000 - $S/cells/gump_1_12_28.txt > data/lag_cells_1_12_28.txt
nice -n 10 $S/ss_lag $S/g_4_0_4.bin lag 5 30000 - $S/cells/gump_4_0_4.txt > data/lag_cells_4_0_4.txt
touch $S/chain_cells.done
