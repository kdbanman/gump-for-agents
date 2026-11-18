#!/bin/bash
# short stationary runs for the equal-area pairs at 96 and 120 cells (blast/model, block M5). One job at a time.
cd "$(dirname "$0")"
run() { # tag spec seed gens pbar
  [ -s hist_$1$2.txt ] && return
  nice -n 10 ./ex3 graph_$2.txt run $3 0.4 $4 4 lives_$1$2.bin $5 512 hist_$1$2.txt.tmp -1 deep_$1$2.bin 512 > ex_$1$2.json 2> ex_$1$2.err && mv hist_$1$2.txt.tmp hist_$1$2.txt
  echo "$(date -u +%H:%M:%S) done $1$2" >> queue4.log
}
run s_  gen_1_13_32_c1 184001 150000 49.7
run s_  gen_1_11_40_c1 184002 400000 62.1
run s2_ gen_1_18_40_c1 184003 400000 62.1
