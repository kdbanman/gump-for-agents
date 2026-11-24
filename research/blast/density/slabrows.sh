#!/bin/sh
# Wrapped-face rows (third task, item 4) on one core, one after another: each argument "TAG:SEED:GENS:L:P".
#   sh research/blast/density/slabrows.sh gump63:7001:2000000:8:0 one63_p0.37:7101:1000000:1:0.37 ...
# Geometry: the torus (H,K),(0,D) of env HKD (default 1_4_21: 63 cells; 1_4_15: 45 cells) from slabgeom.py;
# output scratch rows/slab_TAG_sSEED.txt.
HERE=$(cd "$(dirname "$0")" && pwd); S=$HERE/../../scratch/blast/density; mkdir -p $S/rows
[ -x $S/slab ] || gcc -O3 -march=native -o $S/slab $HERE/slab.c -lm
G=${HKD:-1_4_21}; [ -f $S/slab_$G.bin ] || python3 $HERE/slabgeom.py $(echo $G | tr _ ' ') $S/slab_$G.bin
for spec in "$@"; do
  IFS=: read tag seed gens L p <<E2
$spec
E2
  OUT=$S/rows/slab_${tag}_s$seed.txt; [ -s $OUT ] && continue
  nice -n 10 $S/slab $S/slab_$G.bin brute $seed $gens $L $p > $OUT.part && mv $OUT.part $OUT
done
