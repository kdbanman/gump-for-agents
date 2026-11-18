#!/bin/bash
# after queue4: the wide 96-cell face (its graph file was missing when queue4 started)
cd "$(dirname "$0")"
while pgrep -f queue4.sh > /dev/null; do sleep 2; done
nice -n 10 ./ex3 graph_gen_1_13_32_c1.txt run 184001 0.4 150000 4 lives_s_gen_1_13_32_c1.bin 49.7 512 hist_s_gen_1_13_32_c1.txt.tmp -1 deep_s_gen_1_13_32_c1.bin 512 > ex_s_gen_1_13_32_c1.json 2> ex_s_gen_1_13_32_c1.err && mv hist_s_gen_1_13_32_c1.txt.tmp hist_s_gen_1_13_32_c1.txt && echo "$(date -u +%H:%M:%S) done s_gen_1_13_32_c1 (rerun)" >> queue4.log
