#!/bin/sh
# batch 1: deaths at 63 cells, three vessels, same code (about 5 minutes on one core)
# usage: sh run1.sh   (from research/blast/anatomy; output under research/scratch/blast/anatomy)
S=../../scratch/blast/anatomy
python3 geom.py slab 1 4 21; python3 geom.py slab 1 6 21; python3 geom.py hull 11
nice -n 10 $S/an $S/slab_1_4_21.bin run 11 0.4 4000000 1000 30 128 100000 $S/t63   > $S/t63.log
nice -n 10 $S/an $S/slab_1_6_21.bin run 12 0.4 3000000 1000 30 128 100000 $S/tube63 > $S/tube63.log
nice -n 10 $S/an $S/hull_11.bin     run 13 0.4 1500000 1000 30 128 100000 $S/h63   > $S/h63.log
date -u > $S/run1.done
