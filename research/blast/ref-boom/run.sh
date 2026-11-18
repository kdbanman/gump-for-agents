#!/bin/sh
# what was run (one core, sequential; each job under 6 minutes). Output: research/scratch/blast/ref-boom/
S=../../scratch/blast/ref-boom
nice -n 10 ./rb run 4 0 4 101 2500 $S/r48.txt
nice -n 10 ./rb run 1 4 21 102 5000 $S/r63.txt
nice -n 10 ./rb run 1 7 19 103 3000 $S/r57.txt
nice -n 10 ./rb run 1 9 25 104 5000 $S/r75.txt
