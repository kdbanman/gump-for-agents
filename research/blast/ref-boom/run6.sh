#!/bin/sh
# 05:50 UTC: ahead mode (binary rba = final rb.c). One core, sequential.
S=../../scratch/blast/ref-boom
nice -n 10 ./rba ahead 1 4 21 301 2500 $S/a63.txt
nice -n 10 ./rba ahead 4 0 4 302 1500 $S/a48.txt
nice -n 10 ./rba ahead 1 7 19 303 1500 $S/a57.txt
nice -n 10 ./rba ahead 1 9 25 304 2500 $S/a75.txt
nice -n 10 ./rba ahead 1 4 28 305 2000 $S/a84.txt
