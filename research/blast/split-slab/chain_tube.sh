#!/bin/bash
# plain runs (exact bookkeeping nu(p)) on the loop^2 12 tubes; the 120-cell tube last.
S=$(dirname "$0")/../../scratch/blast/split-slab
run() { nice -n 10 $S/ss $S/g_$1.bin plain $2 $3 $4 $5 > $S/plain_$1_s$2.txt; }
run 1_6_26 101 5000000 34 23
run 1_12_28 101 5000000 37 26
run 1_17_32 101 6000000 43 31
run 1_16_36 101 7000000 49 36
run 1_18_40 101 11000000 55 41
