#!/usr/bin/env bash
# item 2: kagome4 B2/S12 (b = 2, c = 3) strips 41 rows deep (depth 40), cuts censored; depth check at n = 10 (~30 min)
cd "$(dirname "$0")"
O=../../../scratch/class_followup; mkdir -p $O
for spec in 6:500000 8:1000000 10:2000000 12:4000000 14:10000000 16:20000000 18:40000000; do
  n=${spec%%:*}; g=${spec##*:}
  python3 two_d.py slab kagome4 3 A $n 40 $g 3
done >> $O/kagome4_slab.jsonl
for d in 24 56; do python3 two_d.py slab kagome4 3 A 10 $d 2000000 3; done >> $O/kagome4_depth.jsonl
