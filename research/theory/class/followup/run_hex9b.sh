#!/usr/bin/env bash
# item 1, second part: hex9 c = 7 at n = 18 (depth 41), c = 8 strips (armour), hull lifetimes c = 7; kagome8 c = 7 strip
cd "$(dirname "$0")"
O=../../../scratch/class_followup
python3 two_d.py slab hex9 7 B 18 41 20000000 >> $O/hex9_c7_slab.jsonl
{ python3 two_d.py slab hex9 8 B 10 27 2000000; python3 two_d.py slab hex9 8 B 14 35 2000000
  python3 two_d.py slab kagome8 8 A 10 24 2000000; python3 two_d.py slab kagome8 8 B 10 24 2000000
  python3 two_d.py slab kagome8 7 A 10 24 2000000; python3 two_d.py slab kagome8 7 B 10 24 2000000
} >> $O/item1_other.jsonl
for R in 2 3 4 5 6 7; do python3 two_d.py life hex9 7 $R 4000000; done >> $O/hex9_c7_life.jsonl
