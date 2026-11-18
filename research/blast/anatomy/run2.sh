#!/bin/sh
# batch 2: loop^2-12 tubes of 54 and 60 cells (validated first), about 2 minutes on one core
S=../../scratch/blast/anatomy
python3 validate.py slab 1 4 18 1200 > $S/val_1_4_18.txt 2>&1
python3 validate.py slab 1 8 20 1200 > $S/val_1_8_20.txt 2>&1
nice -n 10 $S/an $S/slab_1_4_18.bin run 21 0.4  700000 1000 26 128 100000 $S/tube54 > $S/tube54.log
nice -n 10 $S/an $S/slab_1_8_20.bin run 22 0.4 2000000 1000 29 128 100000 $S/tube60 > $S/tube60.log
date -u > $S/run2.done
