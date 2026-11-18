#!/bin/bash
# the splitting sampler's table (section 3 of the README), committed code; 48-cell torus, anchor 9.9251
S=$(dirname "$0")/../../scratch/blast/split-slab
D=$(dirname "$0")/data
while [ ! -e $S/chain_paths.done ]; do sleep 5; done
for cfg in "1 5 6" "1 3 4" "6 3 4" "1 2 2"; do set -- $cfg
  nice -n 10 $S/ss $S/g_4_0_4.bin ffs 11 256 24 17 3 8192 8192 $1 $2 $3 0 | grep -v "^REP\|^RATE" > $D/split_4_0_4_nf$1_d$2$3.txt
done
touch $S/chain_split.done
