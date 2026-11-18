#!/bin/sh
# step 5 (closure counts M3, M4 on the 48- and 63-cell tori; binary boom2 = boom.c with those counters) and
# step 6 (hull faces of 45, 63, 84 cells, plain runs). Waits for run_b.sh.
S=../../scratch/blast/boom
while [ ! -f $S/run_b.done ]; do sleep 5; done
gcc -O3 -march=native -o $S/boom2 boom.c -lm
nice -n 10 $S/boom2 $S/slab_4_0_4.bin run 31 0.4 1000000 200 28 100 $S/c48 > $S/c48.log 2>&1
nice -n 10 $S/boom2 $S/slab_1_4_21.bin run 32 0.4 1500000 200 37 100 $S/c63 > $S/c63.log 2>&1
date -u > $S/run_c1.done
for R in 9 11 13; do
  python3 validate.py hull $R 1000 > $S/h$R.val 2>&1
done
nice -n 10 $S/boom $S/hull_9.bin run 41 0.4 250000 200 27 2000 $S/h45 > $S/h45.log 2>&1
nice -n 10 $S/boom $S/hull_11.bin run 42 0.4 500000 200 37 2000 $S/h63 > $S/h63.log 2>&1
nice -n 10 $S/boom $S/hull_13.bin run 43 0.4 1000000 200 49 2000 $S/h84 > $S/h84.log 2>&1
date -u > $S/run_c.done
