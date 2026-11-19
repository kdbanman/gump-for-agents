#!/bin/sh
# The depth series of research/blast/noisy/data/depth.txt repeated with this directory's chain (nb.c) on other seeds:
# 63 cells, coins at eps = 1/4 at depth >= d under the watched face (d = 6 ... 1) and >= 3 under the other seven.
#   sh research/audit/blastnoisy/depth.sh        (needs `sh research/audit/blastnoisy/run.sh check` once; 4 cores, 13 min)
#   python3 research/audit/blastnoisy/depth.py   (the table, from the committed rows)
# GENS and O (output directory) can be set in the environment for a short trial.
cd "$(dirname "$0")/../../.." || exit 1
A=research/audit/blastnoisy; S=research/scratch/audit_noisy; O=${O:-$A/data/brute}; GENS=${GENS:-12000000}
gcc -O3 -march=native -o $S/nb $A/nb.c -lm || exit 1
one() { d=$1; B=$(NB_DW=$d $S/nb $S/hull_11.bin info | awk '{print $8}')
  NB_DW=$d $S/nb $S/hull_11.bin run $((1400 + d)) $GENS $((B / 4)) F | grep '^RES' | tail -1 > $O/lead_depth_d${d}_s$((1400 + d)).txt; }
for d in 6 5 4 3; do one $d & done; wait
for d in 2 1; do one $d & done; wait
