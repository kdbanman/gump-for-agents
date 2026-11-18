#!/bin/sh
# 05:54 UTC: look-ahead run at 108 cells (no deaths expected): tests the forecast far from the fit sizes
S=../../scratch/blast/ref-boom
nice -n 10 ./rba ahead 6 0 6 306 2500 $S/a108.txt
