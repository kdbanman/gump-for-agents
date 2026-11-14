#!/usr/bin/env bash
# The face12e measurements of REVIEW-class.md part 2 (one core, about 40 minutes).  Output: research/scratch/audit-class/face12e_*.jsonl
cd "$(dirname "$0")"
O=../../scratch/audit-class
mkdir -p $O
python3 validate.py > $O/validate.log 2>&1 || { echo "validation failed"; exit 1; }
{ python3 face12e.py slab 4x4 2000000 6 4 two
  python3 face12e.py slab 4x5 2000000 6 4 two
  python3 face12e.py slab 5x5 4000000 6 4 two
  python3 face12e.py slab 5x6 6000000 6 4 two
  python3 face12e.py slab 6x6 10000000 6 4 two
  python3 face12e.py slab 5x5 2000000 6 6 two
  python3 face12e.py slab 4x4 1000000 6 4 one
  python3 face12e.py slab 5x5 1000000 6 4 one
  python3 face12e.py slab 4x4 1000000 6 4 second
  python3 face12e.py slab 5x5 1000000 6 4 second
} > $O/face12e_slab.jsonl 2>&1
{ for n in 2 3 4 5; do python3 face12e.py life $n 1000000 6 0.45; done
  python3 face12e.py life 6 6000000 6 0.45
} > $O/face12e_life.jsonl 2>&1
