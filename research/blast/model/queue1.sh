#!/bin/bash
# population histograms and excursion tables of wrapped and hull faces (blast/model). One job at a time.
cd "$(dirname "$0")"
G=../../../theory/symmetric/geom.py
run() { # spec seed gens pbar
  [ -f graph_$1.txt ] || python3 $G write $1 graph_$1.txt > geom_$1.log 2>&1
  [ -s ex_$1.json ] && return
  nice -n 10 ./ex3 graph_$1.txt run $2 0.4 $3 4 lives_$1.bin $4 512 hist_$1.txt -1 deep_$1.bin 512 > ex_$1.json.tmp 2> ex_$1.err && mv ex_$1.json.tmp ex_$1.json
  rm -f lives_$1.bin deep_$1.bin
  echo "$(date -u +%H:%M:%S) done $1" >> queue1.log
}
run gen_4_0_4_c1   181101 1000000 24.8
run gen_1_7_19_c1  181102 3000000 29.5
run gen_1_4_21_c1  181103 6000000 32.6
run gen_1_8_20_c1  181104 4000000 31.0
run gen_1_5_22_c1  181105 6000000 34.1
run gen_1_4_22_c1  181106 6000000 34.1
run oct_11_c_c1    181109 1200000 31.29
run gen_1_12_28_c1 181107 8000000 43.4
run gen_1_4_28_c1  181108 8000000 43.4
run oct_9_c_c1     181110 400000 21.67
run oct_13_c_c1    181111 1200000 42.49
