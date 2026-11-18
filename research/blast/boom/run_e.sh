#!/bin/sh
# how deep is the boom: layers 3 and 4 beneath the face in the histories of the deaths (binary boom4 = current boom.c)
S=../../scratch/blast/boom
nice -n 10 $S/boom4 $S/slab_4_0_4.bin run 61 0.4 300000 200 39 10 $S/e48 $S/slab_4_0_4.layers > $S/e48.log 2>&1
nice -n 10 $S/boom4 $S/slab_1_4_21.bin run 62 0.4 1500000 200 51 10 $S/e63 $S/slab_1_4_21.layers > $S/e63.log 2>&1
nice -n 10 $S/boom4 $S/slab_1_8_20.bin run 63 0.4 1000000 200 49 10 $S/e60 $S/slab_1_8_20.layers > $S/e60.log 2>&1
date -u > $S/run_e.done
