#!/bin/bash
# plain runs (exact bookkeeping nu(p)) on the loop^2 12 tubes; the 120-cell tube last.
# (lengths halved at 03:50 UTC: the machine gives this job under half a core)
S=$(dirname "$0")/../../scratch/blast/split-slab
run() { nice -n 10 $S/ss $S/g_$1.bin plain $2 $3 $4 $5 > $S/plain_$1_s$2.txt; }
# run 1_6_26 101 5000000 34 23      (started 03:46 UTC by the first version of this script)
while pgrep -f "g_1_6_26.bin plain" > /dev/null; do sleep 2; done
run 1_12_28 101 2500000 37 26
run 1_17_32 101 3000000 43 31
run 1_16_36 101 3500000 49 36
run 1_18_40 101 5500000 55 41
touch $S/chain_tube.done
