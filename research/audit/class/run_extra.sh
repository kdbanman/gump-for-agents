#!/usr/bin/env bash
# Short follow-ups of REVIEW-class.md (one core, about 15 minutes): kagome4 b = 2, bond10 b = 3, vn boxes, face12e caps.
cd "$(dirname "$0")"
O=../../scratch/audit-class
{ python3 others.py kagome 3; python3 others.py kagome 4
  for n in 4 6 8 10 12; do python3 others.py kagome slab $n 2000000 3 two; done
  for n in 6 10; do python3 others.py kagome slab $n 500000 3 one; done
  for R in 2 3 4 5 6 7 8 10; do python3 others.py kagome life $R 2000000 3; done
} > $O/kagome.txt 2>&1
{ python3 others.py bond10
  for c in 5 6; do for n in 4 5 6; do python3 others.py bond10 slab $c $n 500000; done; done
  for c in 5 6; do for n in 2 3 4 5; do python3 others.py bond10 life $c $n 300000; done; done
} > $O/bond10.txt 2>&1
python3 vnbox.py 3000000 > $O/vnbox.jsonl 2>&1
{ for c in 5 7 8 9 10; do python3 face12e.py bulk $c; done
  for c in 7 8 9; do python3 face12e.py slab 4x4 500000 $c 4 two; python3 face12e.py slab 5x5 500000 $c 4 two; done
} > $O/face12e_caps.txt 2>&1
