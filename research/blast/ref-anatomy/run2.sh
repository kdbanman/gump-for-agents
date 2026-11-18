#!/bin/sh
# joint-map runs for THEORY.md (one core, about 7 minutes of wall time); output under research/scratch
cd "$(dirname "$0")"
S=../../scratch/blast/ref-anatomy
gcc -O3 -march=native -o fd2 fd2.c -lm
for n in t63 t48 t84 h63 tube60 tube84; do python3 vessel.py $n > /dev/null; done
#             geom                 mode seed       seconds P* B* out
nice -n 10 ./fd2 $S/geom_t63.txt    map 2026111811 110 33 26 $S/map_t63.txt
nice -n 10 ./fd2 $S/geom_t48.txt    map 2026111812 30  25 20 $S/map_t48.txt
nice -n 10 ./fd2 $S/geom_t84.txt    map 2026111813 80  44 35 $S/map_t84.txt
nice -n 10 ./fd2 $S/geom_h63.txt    map 2026111814 90  33 28 $S/map_h63.txt
nice -n 10 ./fd2 $S/geom_tube60.txt map 2026111815 45  31 25 $S/map_tube60.txt
nice -n 10 ./fd2 $S/geom_tube84.txt map 2026111816 45  44 35 $S/map_tube84.txt
