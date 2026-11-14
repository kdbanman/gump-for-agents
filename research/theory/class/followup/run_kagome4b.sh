#!/usr/bin/env bash
# item 2, production: kagome4 B2/S12 strips 41 rows deep, cuts censored AND replicas whose wall band froze
# (x(t) = x(t-2) on the two wall rows for 128 consecutive checks of 8 generations) censored (~35 min, one core)
cd "$(dirname "$0")"
O=../../../scratch/class_followup
for spec in 6:500000 8:1000000 10:2000000 12:4000000 14:8000000 16:16000000 18:30000000; do
  n=${spec%%:*}; g=${spec##*:}
  python3 two_d.py slab kagome4 3 A $n 40 $g 4 128
done >> $O/kagome4_frozen_censored.jsonl
for d in 24 56; do python3 two_d.py slab kagome4 3 A 10 $d 2000000 4 128; done >> $O/kagome4_depth.jsonl
