#!/usr/bin/env bash
# item 1: hex9 B456/S3456 (b = 4, c = 7) strips between two sealed walls, depth 2n + 7 (about 50 min, one core)
cd "$(dirname "$0")"
O=../../../scratch/class_followup; mkdir -p $O
for spec in 8:1000000 10:1000000 12:2000000 14:4000000 16:10000000 18:20000000 20:40000000; do
  n=${spec%%:*}; g=${spec##*:}
  python3 two_d.py slab hex9 7 B $n $((2 * n + 7)) $g
done >> $O/hex9_c7_slab.jsonl
