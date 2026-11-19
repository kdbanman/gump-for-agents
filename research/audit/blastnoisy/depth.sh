#!/bin/sh
# The depth series of research/blast/noisy/data/depth.txt repeated with this directory's chain (nb.c) on other seeds:
# 63 cells, coins at eps = 1/4 at depth >= d under the watched face (d = 6 ... 1) and >= 3 under the other seven.
#   sh research/audit/blastnoisy/depth.sh        (needs `sh research/audit/blastnoisy/run.sh check` once; 4 cores)
#   python3 research/audit/blastnoisy/depth.py   (the table, from the committed rows)
cd "$(dirname "$0")/../../.." || exit 1
A=research/audit/blastnoisy; S=research/scratch/audit_noisy; O=$A/data/brute
gcc -O3 -march=native -o $S/nb $A/nb.c -lm || exit 1
for d in 6 5 4 3 2 1; do
  B=$(NB_DW=$d $S/nb $S/hull_11.bin info | awk '{print $8}'); M=$((B / 4))
  echo "NB_DW=$d $S/nb $S/hull_11.bin run $((1400 + d)) 12000000 $M F | tail -1 | sed 's/^/DW $d /' > $O/lead_depth_d${d}_s$((1400 + d)).txt"
done | xargs -P 4 -I{} sh -c '{}'
