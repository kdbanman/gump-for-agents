#!/bin/sh
# batch 3: does the picture change with size? 45/48 cells (seconds), 75 and 84 cells (minutes). One core, about 20 minutes.
S=../../scratch/blast/anatomy
for v in "hull 9" "slab 1 9 25" "slab 1 4 28" "hull 13"; do python3 validate.py $v 1100 >> $S/val_batch3.txt 2>&1; done
nice -n 10 $S/an $S/slab_4_0_4.bin  run 31 0.4   300000 1000 23 128 100000 $S/t48  > $S/t48.log
nice -n 10 $S/an $S/hull_9.bin      run 32 0.4   100000 1000 21 128 100000 $S/h45  > $S/h45.log
nice -n 10 $S/an $S/slab_1_9_25.bin run 33 0.4  7000000 1000 36 128 100000 $S/t75  > $S/t75.log
nice -n 10 $S/an $S/slab_1_4_28.bin run 34 0.4 14000000 1000 40 128 100000 $S/t84  > $S/t84.log
nice -n 10 $S/an $S/hull_13.bin     run 35 0.4  6000000 1000 40 128 100000 $S/h84  > $S/h84.log
date -u > $S/run3.done
