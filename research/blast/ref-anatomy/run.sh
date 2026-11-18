#!/bin/sh
# production runs of the referee (one core, about 9 minutes of wall time in all); output under research/scratch
cd "$(dirname "$0")"
S=../../scratch/blast/ref-anatomy
gcc -O3 -march=native -o fd fd.c
for n in t63 tube60 h63; do python3 vessel.py $n > /dev/null; done
#            geom               mode seed      seconds LGAP OSUB CSUB out
nice -n 10 ./fd $S/geom_t63.txt    run 2026111801 200 1000 1000 64 $S/t63
nice -n 10 ./fd $S/geom_tube60.txt run 2026111802 120 1000 1000 64 $S/tube60
nice -n 10 ./fd $S/geom_h63.txt    run 2026111803 200 300  1000 1  $S/h63
