#!/bin/sh
# PI's test (04:15 UTC): absolute rates of deaths by class on loop-12 tubes and wide faces as functions of area.
# Plain runs (deaths with their 32-generation histories). run_b.sh and run_c.sh were stopped unrun to make room.
S=../../scratch/blast/boom
one() {  # name H K D gens seed
  A=$((3*$2*$4)); L=$(( (80*A+99)/100 ))
  [ -f $S/slab_$2_$3_$4.bin ] || python3 validate.py slab $2 $3 $4 1000 > $S/$1.val 2>&1
  nice -n 10 $S/boom $S/slab_$2_$3_$4.bin run $6 0.4 $5 200 $L 10 $S/$1 > $S/$1.log 2>&1
  date -u >> $S/$1.log
}
one t57 1 7 19 1000000 51
one tube54 1 4 18 1000000 52
one w72 1 4 24 2000000 53
one tube60b 1 8 20 1000000 54
one t63b 1 4 21 2000000 55
date -u > $S/run_d1.done
# step 5 closure (48-cell torus, binary with the (P,U) counts) and step 6 hull faces
nice -n 10 $S/boom2 $S/slab_4_0_4.bin run 31 0.4 1000000 200 28 100 $S/c48 > $S/c48.log 2>&1
for R in 9 11; do python3 validate.py hull $R 1000 > $S/h$R.val 2>&1; done
nice -n 10 $S/boom $S/hull_9.bin run 41 0.4 250000 200 27 2000 $S/h45 > $S/h45.log 2>&1
nice -n 10 $S/boom $S/hull_11.bin run 42 0.4 500000 200 37 2000 $S/h63 > $S/h63.log 2>&1
date -u > $S/run_d.done
