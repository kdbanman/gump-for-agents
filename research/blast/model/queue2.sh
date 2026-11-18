#!/bin/bash
# short runs for the stationary mean and variance of P (many faces), then the long equal-area pairs. One job at a time.
cd "$(dirname "$0")"
G=../../../theory/symmetric/geom.py
run() { # tag spec seed gens pbar
  [ -f graph_$2.txt ] || python3 $G write $2 graph_$2.txt > geom_$2.log 2>&1
  [ -s hist_$1$2.txt ] && return
  nice -n 10 ./ex3 graph_$2.txt run $3 0.4 $4 4 lives_$1$2.bin $5 512 hist_$1$2.txt.tmp -1 deep_$1$2.bin 512 > ex_$1$2.json 2> ex_$1$2.err && mv hist_$1$2.txt.tmp hist_$1$2.txt
  rm -f lives_$1$2.bin deep_$1$2.bin
  echo "$(date -u +%H:%M:%S) done $1$2" >> queue2.log
}
i=182000
for s in "1 4 22" "1 12 28" "1 4 28" "1 5 22" "1 4 18" "1 6 26" "1 17 32" "1 16 36" "6 0 6" "1 18 40" "5 0 5" "1 5 31" "1 3 25" "1 3 32" "4 0 8" "1 10 37" "1 38 80" "8 0 8" "1 4 21" "1 8 20" "4 0 4" "1 7 19" "2 2 6" "1 3 13"; do
  set -- $s; i=$((i+1)); A=$((3*$1*$3))
  run s_ gen_$1_$2_$3_c1 $i 150000 $(python3 -c "print(0.5177*$A)")
done
run "" gen_1_12_28_c1 181107 5000000 43.4
run "" gen_1_4_28_c1  181108 5000000 43.4
run "" gen_1_4_22_c1  181106 4000000 34.1
run "" oct_11_c_c1    181109 600000 31.29
