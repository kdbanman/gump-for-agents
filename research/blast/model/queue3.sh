#!/bin/bash
# ex5 runs (lag-before-death and joint histograms), one job at a time.
cd "$(dirname "$0")"
run() { # spec seed gens pbar
  [ -s hist5_$1.txt ] && return
  nice -n 10 ./ex5 graph_$1.txt run $2 0.4 $3 4 l5_$1.bin $4 512 hist5_$1.txt.tmp -1 d5_$1.bin 512 > ex5_$1.json 2> ex5_$1.err && mv hist5_$1.txt.tmp hist5_$1.txt
  echo "$(date -u +%H:%M:%S) done $1" >> queue3.log
}
run oct_9_c_c1    183011 200000 21.67
run gen_4_0_4_c1  183001 1000000 24.8
run oct_11_c_c1   183012 500000 31.29
run gen_1_4_21_c1 183002 2500000 32.6
run gen_1_5_22_c1 183003 2500000 34.1
run gen_1_4_22_c1 183004 2500000 34.1
run gen_1_8_20_c1 183013 2000000 31.0
