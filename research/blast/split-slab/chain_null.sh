#!/bin/bash
# the null of README section 9: 16-generation windows of LIVING faces (plain gump, face 0 of one lane every 256 generations)
cd "$(dirname "$0")"
S=../../scratch/blast/split-slab
while [ ! -e $S/chain_cells.done ]; do sleep 3; done
for L in 1_30_64 8_0_8 1_22_48 1_16_36 6_0_6 1_18_40 1_12_28 1_4_21; do
  nice -n 10 $S/ss_null $S/g_$L.bin lag 8 80000 - - $S/cells/null_$L.txt > /dev/null
done
touch $S/chain_null.done
