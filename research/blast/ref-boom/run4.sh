#!/bin/sh
# 05:06 UTC: slab-lifetime distribution (binary rbt = rb.c with the T/TH accumulators; run output otherwise identical)
S=../../scratch/blast/ref-boom
until [ -f $S/t48.txt ]; do sleep 1; done
nice -n 10 ./rbt run 1 4 21 122 5000 $S/t63.txt
