#!/bin/sh
# 05:27 UTC: static mode (binary rbs = final rb.c). One core, sequential.
S=../../scratch/blast/ref-boom
nice -n 10 ./rbs static 1 4 21 201 4000 $S/s63.txt
nice -n 10 ./rbs static 4 0 4 202 1500 $S/s48.txt
nice -n 10 ./rbs static 1 9 25 203 3000 $S/s75.txt
nice -n 10 ./rbs static 1 4 28 204 3000 $S/s84.txt
nice -n 10 ./rbs static 1 7 19 205 1500 $S/s57.txt
nice -n 10 ./rbs static 6 0 6 206 2500 $S/s108.txt
