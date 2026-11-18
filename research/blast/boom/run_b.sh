#!/bin/sh
# step 3-4: plain runs at 108 and 120 cells (nu(p), variance, parents; no deaths expected). Waits for run_a.sh.
S=../../scratch/blast/boom
while [ ! -f $S/run_a.done ]; do sleep 5; done
one() {  # name H K D gens seed
  A=$((3*$2*$4)); L=$(( (66*A+99)/100 ))
  python3 validate.py slab $2 $3 $4 1000 > $S/$1.val 2>&1
  nice -n 10 $S/boom $S/slab_$2_$3_$4.bin run $6 0.4 $5 200 $L 4000 $S/$1 > $S/$1.log 2>&1
  date -u >> $S/$1.log
}
one tube108 1 16 36 1000000 21
one t108 6 0 6 1000000 22
one tube120 1 18 40 1000000 23
date -u > $S/run_b.done
