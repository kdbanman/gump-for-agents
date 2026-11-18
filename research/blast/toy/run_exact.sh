#!/bin/sh
# Exact one-row dice surrogate, rings (xr*) and open segments (xs*), coin density 0.472.  One core, ~10 minutes.
# Usage: sh run_exact.sh     (L <= 16 take seconds: for L in 8..16: ex1d L 1 0.472 8; ex1d L 0 0.472 8)
S=../../scratch/blast/toy; gcc -O2 -march=native -o $S/ex1d ex1d.c -lm
while [ ! -f $S/bf.done ]; do sleep 3; done
x() { nice -n 10 $S/ex1d $1 $2 0.472 $3 > $S/x$4$1.tmp && mv $S/x$4$1.tmp $S/x$4$1.out; }
x 18 1 6 r; x 18 0 6 s; x 20 1 6 r; x 20 0 6 s; x 22 0 6 s; x 22 1 0 r; x 24 0 0 s
x 17 1 6 r; x 17 0 6 s; x 19 1 6 r; x 19 0 6 s; x 21 0 0 s; x 21 1 0 r; x 23 0 0 s
echo done > $S/exact.done
