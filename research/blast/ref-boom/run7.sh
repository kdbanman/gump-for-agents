#!/bin/sh
# 05:54 UTC: look-ahead run at 108 cells (no deaths expected): tests the forecast far from the fit sizes
S=../../scratch/blast/ref-boom
nice -n 10 ./rba ahead 6 0 6 306 2500 $S/a108.txt
# 05:56 UTC: the 84-cell tube (1,12),(0,28), loop^2 12 (anchor 17.3175): is its discount in the static term or in the kill?
nice -n 10 ./rba ahead 1 12 28 307 2000 $S/atube84.txt
