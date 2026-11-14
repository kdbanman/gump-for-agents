#!/usr/bin/env bash
# Last pieces of REVIEW-class.md (one core, about 6 minutes): how a face12e box dies, competing endings in its
# slabs, and class.md's octahedron lifetimes for gump (caps 6, 7) and fcc (cap 6) with the audit stepper.
cd "$(dirname "$0")"
O=../../scratch/audit-class
{ python3 face12e.py layers 4 6000 1; python3 face12e.py layers 5 80000 1; } > $O/face12e_layers.txt 2>&1
{ python3 face12e.py cuts 4 4096 8; python3 face12e.py cuts 5 65536 3; } > $O/face12e_cuts.txt 2>&1
{ for R in 4 5; do python3 face12e.py life $R 200000 6 0.45 gump; done
  python3 face12e.py life 4 200000 7 0.45 gump
  for R in 4 5 6; do python3 face12e.py life $R 200000 6 0.42 fcc; done
} > $O/hulls_check.jsonl 2>&1
