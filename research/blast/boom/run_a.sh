#!/bin/sh
# steps 1-2: validation, plain runs (nu, return map, deaths, parents) and clones on seven vessels; one core.
# usage: sh run_a.sh   (from research/blast/boom; output under research/scratch/blast/boom)
S=../../scratch/blast/boom
gcc -O3 -march=native -o $S/boom boom.c -lm
one() {  # name H K D gens seed
  A=$((3*$2*$4)); L=$(( (58*A+99)/100 ))   # parents kept for P >= 0.58 A
  python3 validate.py slab $2 $3 $4 1000 > $S/$1.val 2>&1
  nice -n 10 $S/boom $S/slab_$2_$3_$4.bin run $6 0.4 $5 200 $L 20000 $S/$1 > $S/$1.log 2>&1
  nice -n 10 $S/boom $S/slab_$2_$3_$4.bin clone $S/$1.par $S/slab_$2_$3_$4.deep 16 40 $6 $S/$1.clone >> $S/$1.log 2>&1
  date -u >> $S/$1.log
}
one t63 1 4 21 1500000 11
one t48 4 0 4 1000000 12
one t84 1 4 28 1500000 13
one tube84 1 12 28 1500000 14
one tube60 1 8 20 1000000 15
one t75 1 9 25 1500000 16
one tube72 1 10 24 1500000 17
date -u > $S/run_a.done
