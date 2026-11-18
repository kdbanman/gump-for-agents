#!/bin/sh
# is a tube's discount the more frequent four-layer over-fill? Equal area, 72 cells (binary boom5 = current boom.c)
S=../../scratch/blast/boom
nice -n 10 $S/boom5 $S/slab_1_10_24.bin run 71 0.4 1500000 200 58 10 $S/f72tube $S/slab_1_10_24.layers > $S/f72tube.log 2>&1
nice -n 10 $S/boom5 $S/slab_1_4_24.bin run 72 0.4 1500000 200 58 10 $S/f72wide $S/slab_1_4_24.layers > $S/f72wide.log 2>&1
date -u > $S/run_f.done
