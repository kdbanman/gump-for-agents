#!/bin/bash
# Round 2 runs (seeds and lengths fixed in PREDICTIONS.md, round 2). Usage: bash research/dying/round2.sh LANE (1 or 2)
set -e
cd "$(dirname "$0")/../scratch/dying"
gcc -O3 -march=native -o ex ../../dying/ex.c; gcc -O3 -march=native -o sd ../../dying/sd.c
SY=../../symmetric/sy; G=../../symmetric; mkdir -p r2; cd r2
ex() { ../ex $G/graph_oct_11_c_$1.txt run $2 0.4 $3 4 exl_$1.bin $4 512 exh_$1.txt > ex_$1.json; $SY $G/graph_oct_11_c_$1.txt run $2 0.4 $3 4 sy_ex_$1.bin > /dev/null; cmp exl_$1.bin sy_ex_$1.bin && echo "ex $1 lives identical to sy"; rm sy_ex_$1.bin; }
sd() { ../sd $G/graph_oct_11_c_$1.txt run $2 0.4 $3 4 lives_$1.bin dump_$1.bin null_$1.bin 3000 512 512 > sd_$1.json 2> sd_$1.err; $SY $G/graph_oct_11_c_$1.txt run $2 0.4 $3 4 sy_sd_$1.bin > /dev/null; cmp lives_$1.bin sy_sd_$1.bin && echo "sd $1 lives identical to sy"; rm sy_sd_$1.bin; }
sd84() { ../sd ../graph_oct_13_c_$1.txt run 31 0.4 200000 4 lives84_$1.bin dump84_$1.bin null84_$1.bin 0 4 512 > sd84_$1.json 2> sd84_$1.err; }
if [ "$1" = 1 ]; then ex c1 11 1200000 31.29; sd c1 21 600000; sd84 c1; sd84 csz; fi
if [ "$1" = 2 ]; then ex csz 11 400000 28.83; ex c2v 11 200000 26.29; ex d2h 12 400000 23.77; sd d2h 22 400000; sd csz 21 400000; sd c2v 21 200000; sd84 c2v; sd84 d2h; fi
