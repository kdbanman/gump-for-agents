#!/usr/bin/env bash
# item 3: bond10 at b = 3.  Slab law at c = 5 with cuts censored, columns, boxes, c = 6 boxes (one core, ~1 h)
cd "$(dirname "$0")"
O=../../../scratch/class_followup; mkdir -p $O
{ python3 three_d.py slab bond10 5 3 3 4 200000 2
  python3 three_d.py slab bond10 5 3 4 4 300000 2
  python3 three_d.py slab bond10 5 4 4 4 600000 2
  python3 three_d.py slab bond10 5 4 5 4 2000000 2
  python3 three_d.py slab bond10 5 5 5 4 4000000 2
  python3 three_d.py slab bond10 5 5 6 4 12000000 2
} >> $O/bond10_slab.jsonl
{ python3 three_d.py column bond10 5 3 3 2000000 2
  python3 three_d.py column bond10 5 3 4 4000000 2
  python3 three_d.py column bond10 5 4 4 6000000 2
} >> $O/bond10_column.jsonl
{ python3 three_d.py box bond10 5 3 1000000 2
  python3 three_d.py box bond10 5 4 10000000 2 64
  python3 three_d.py bond10c6 3 200000
  python3 three_d.py bond10c6 4 200000
} >> $O/bond10_box.jsonl
