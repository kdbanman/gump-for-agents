#!/usr/bin/env bash
# Part 3 of REVIEW-class.md: slab face laws re-measured with the audit stepper ({111} slabs, 8 layers, periodic faces).
#   ./run_measured.sh gump    gump's lattice, caps 6 and 7 (B45/S345, B456/S3456), A = 27, 36, 48, 60, 75   (~25 min)
#   ./run_measured.sh fcc     fcc, cap 6, A = 25, 36, 49, 64, 81; caps 9 and 10 (the wall cap) at A = 25, 49 (~15 min)
cd "$(dirname "$0")"
O=../../scratch/audit-class
mkdir -p $O
if [ "$1" = gump ]; then
  for c in 6 7; do
    python3 face12e.py slab 3x3 2000000 $c 4 two gump
    python3 face12e.py slab 3x4 2000000 $c 4 two gump
    python3 face12e.py slab 4x4 4000000 $c 4 two gump
    python3 face12e.py slab 4x5 10000000 $c 4 two gump
    python3 face12e.py slab 5x5 20000000 $c 4 two gump
  done > $O/measured_gump.jsonl 2>&1
else
  { python3 face12e.py slab 5x5 2000000 6 4 two fcc
    python3 face12e.py slab 6x6 2000000 6 4 two fcc
    python3 face12e.py slab 7x7 4000000 6 4 two fcc
    python3 face12e.py slab 8x8 10000000 6 4 two fcc
    python3 face12e.py slab 9x9 20000000 6 4 two fcc
    for c in 9 10; do
      python3 face12e.py slab 5x5 1000000 $c 4 two fcc
      python3 face12e.py slab 7x7 1000000 $c 4 two fcc
    done
  } > $O/measured_fcc.jsonl 2>&1
fi
