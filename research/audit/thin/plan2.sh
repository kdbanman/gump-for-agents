#!/bin/bash
# Amendment to plan.sh (2026-11-15 00:06), decided on wall-clock alone (the machine is shared and runs at about half the
# speed timed when plan.sh was written), before any of the affected tags had a chunk: same tags and seeds, fewer chunks;
# s45 and r36 dropped. Chunks already made are skipped by tt.py.
T="python3 $(dirname "$0")/tt.py run"
c() { local tag=$1 mode=$2 b=$3 w=$4 wall=$5 gens=$6 n=$7 s0=$8 prof=${9:-0}
      for ((k=0;k<n;k++)); do $T $tag $mode $b $w $wall $gens $((s0+k)) $prof; done; }
if [ "$1" = A ]; then
  c s29   det   32 0 3 2000000  4 1400 1500
  c r24   det   24 0 0 1500000  4 1500
  c r28   det   28 0 0 3000000  4 1600
  c r32   det   32 0 0 3000000  5 1700 1500
fi
if [ "$1" = B ]; then
  c r30   det   30 0 0 3000000  6 2100
  c s37   det   40 0 3 3000000  4 2200
fi
