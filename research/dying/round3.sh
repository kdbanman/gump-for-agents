#!/bin/bash
# Round 3 runs (seeds, lengths, thresholds fixed in PREDICTIONS.md, round 3). Usage: bash research/dying/round3.sh LANE (1 or 2)
set -e
D="$(cd "$(dirname "$0")" && pwd)"; cd "$D/../scratch/dying"
gcc -O3 -march=native -o ex3 "$D/ex3.c"; gcc -O3 -march=native -o sd "$D/sd.c"
SY=../symmetric/sy; mkdir -p r3; cd r3
null() { ../sd ../graph_$1.txt run 41 0.4 100000 4 nl_$1.bin nd_$1.bin null_$1.bin 0 4 512 > /dev/null 2>&1; python3 "$D/round3_pbar.py" $1 null_$1.bin > pbar_$1.txt; cat pbar_$1.txt; }
ex3() { ../ex3 ../graph_$1.txt run $2 0.4 $3 4 exl_$1.bin $4 512 exh_$1.txt $5 deep_$1.bin 512 > ex_$1.json 2> ex_$1.err
        $SY ../graph_$1.txt run $2 0.4 $3 4 sy_$1.bin > /dev/null; cmp exl_$1.bin sy_$1.bin && echo "$1 lives identical to sy"; rm sy_$1.bin; }
if [ "$1" = 1 ]; then
  null oct_9_c_c1; ex3 oct_9_c_c1 51 400000 $(cut -d' ' -f1 pbar_oct_9_c_c1.txt) -1
  null oct_15_c_c1; ex3 oct_15_c_c1 54 1200000 $(cut -d' ' -f1 pbar_oct_15_c_c1.txt) -1
fi
if [ "$1" = 2 ]; then
  ex3 oct_11_c_c1 52 1200000 31.29 9
  ex3 oct_11_c_csz 52 400000 28.83 8
  ex3 oct_13_c_c1 53 1200000 42.49 -1
  null hex_4_1_c1; ex3 hex_4_1_c1 55 400000 $(cut -d' ' -f1 pbar_hex_4_1_c1.txt) -1
fi
