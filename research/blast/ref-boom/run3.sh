#!/bin/sh
# repeats with new seeds (05:00 UTC): is the 63-cell lifetime low and the 75-cell one high by chance?
S=../../scratch/blast/ref-boom
nice -n 10 ./rb run 1 4 21 112 5000 $S/r63b.txt
nice -n 10 ./rb run 1 9 25 114 3500 $S/r75b.txt
