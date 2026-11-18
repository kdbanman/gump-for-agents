#!/bin/sh
# second half of the chain, shortened at 04:55 UTC because the machine was loaded (run.sh's lines 3-4 were not run)
S=../../scratch/blast/ref-boom
until [ -f $S/r63.txt ]; do sleep 2; done
nice -n 10 ./rbi island 1 4 21 302 600 $S/i63.txt
nice -n 10 ./rb run 1 7 19 103 2000 $S/r57.txt
nice -n 10 ./rb run 1 9 25 104 3500 $S/r75.txt
