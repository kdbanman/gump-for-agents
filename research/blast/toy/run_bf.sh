#!/bin/sh
# Brute force: ring edges (strip 16 x L periodic along the edge) and box edges (L x L), cross2 B34/S234.
# Usage: sh run_bf.sh   (one core, about 8 minutes in all; output under research/scratch/blast/toy/)
S=../../scratch/blast/toy; mkdir -p $S; gcc -O2 -march=native -o $S/ed ed.c -lm 2>/dev/null
run() { # L deaths samp
  nice -n 10 $S/ed run 16 $1 1 11 $2 4e9 $S/r$1.rec 300 $3 > $S/r$1.out
  nice -n 10 $S/ed run $1 $1 0 12 $2 4e9 $S/b$1.rec 300 $3 > $S/b$1.out
}
run 12 6000 23; run 16 6000 97; run 20 6000 499; run 24 4000 2003; run 28 2000 9973; run 32 600 19997
echo done > $S/bf.done
