#!/bin/sh
# Brute force of the noisy chain (plain running, no sampler): one line per run appended to scratch brute.txt.
#   sh research/blast/noisy/brute.sh R M GENS SEED [DW DO]      (eps = M / B; B is printed; M = 0 is gump)
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/noisy; mkdir -p $S
[ -x $S/nz ] || gcc -O3 -march=native -o $S/nz $HERE/nz.c -lm
nice -n 10 $S/nz $1 brute $4 $3 $2 ${5:-6} ${6:-3} >> $S/brute.txt
