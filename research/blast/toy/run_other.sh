#!/bin/sh
# Item 5: two more one-row capped-threshold dice surrogates, rings and segments, exact (exg.c).  ~3 minutes.
#  A: range 3, 3 coins (rho 0.5), alive iff n + x >= 4 and n <= 6   (segment end cell: n <= 6, never overcrowded)
#  B: range 1, 2 coins (rho 0.5), alive iff n + x >= 2 and n <= 2   (segment end cell: n <= 3, CAN be overcrowded)
S=../../scratch/blast/toy; gcc -O2 -march=native -o $S/exg exg.c -lm
while [ ! -f $S/exact.done ]; do sleep 3; done
for L in 8 10 12 14 16; do
  nice -n 10 $S/exg $L 1 1 2 2 2 0.5 6 > $S/oBr$L.out; nice -n 10 $S/exg $L 0 1 2 2 2 0.5 6 > $S/oBs$L.out; done
for L in 8 10 12 14; do
  nice -n 10 $S/exg $L 1 3 3 4 6 0.5 6 > $S/oAr$L.out; nice -n 10 $S/exg $L 0 3 3 4 6 0.5 6 > $S/oAs$L.out; done
nice -n 10 $S/exg 16 0 3 3 4 6 0.5 6 > $S/oAs16.out; nice -n 10 $S/exg 16 1 3 3 4 6 0.5 0 > $S/oAr16.out
echo done > $S/other.done
