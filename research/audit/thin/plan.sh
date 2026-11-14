#!/bin/bash
# Run plan of the review of research/theory/thin/ (fixed before any production run; 2026-11-14 23:40).
# One chunk = one process = one seed; chunks are files research/scratch/audit_thin/TAG/s<seed>.txt and are
# skipped if present, so the queues can be killed and restarted. 2048 lanes per chunk (tt.c compiled with W=32).
# usage: bash plan.sh A   or   bash plan.sh B      (one core each)
#   tt.py run TAG MODE b w wall gens seed [maxprof]
T="python3 $(dirname "$0")/tt.py run"
c() { local tag=$1 mode=$2 b=$3 w=$4 wall=$5 gens=$6 n=$7 s0=$8 prof=${9:-0}
      for ((k=0;k<n;k++)); do $T $tag $mode $b $w $wall $gens $((s0+k)) $prof; done; }
if [ "$1" = A ]; then
  c r16   det   16 0 0  250000  4 1000          # ring b = 16 (claim 4 baseline)
  c m16w5 model 16 5 0  400000  4 1100          # M(5), ring b = 16 (claim 4)
  c m16w4 model 16 4 0  400000  2 1200          # M(4), ring b = 16 (claim 4, reference)
  c s21   det   24 0 3  500000  2 1300          # segment n = 21
  c s29   det   32 0 3 2000000  4 1400 1500     # segment n = 29 (+ death profiles)
  c r24   det   24 0 0 1500000  4 1500          # ring b = 24
  c r28   det   28 0 0 3000000  6 1600          # ring b = 28
  c r32   det   32 0 0 3000000 10 1700 1500     # ring b = 32 (+ death profiles)
  c s45   det   48 0 3 3000000 12 1800          # segment n = 45
fi
if [ "$1" = B ]; then
  c r26   det   26 0 0 2500000  4 2000          # ring b = 26
  c r30   det   30 0 0 3000000  8 2100          # ring b = 30
  c s37   det   40 0 3 3000000  8 2200          # segment n = 37
  c r36   det   36 0 0 3500000 12 2300          # ring b = 36
fi
