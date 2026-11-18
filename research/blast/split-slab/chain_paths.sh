#!/bin/bash
# natural deaths (plain gump, no flips): layer populations by lag before the death, and per-cell last-alive lags
S=$(dirname "$0")/../../scratch/blast/split-slab
D=$(dirname "$0")/data
mkdir -p $D
while [ ! -e $S/chain_tube.done ]; do sleep 5; done
nice -n 10 $S/ss_lag $S/g_4_0_4.bin lag 3 30000 $D/paths_4_0_4.txt > $D/lag_4_0_4.txt
nice -n 10 $S/ss_lag $S/g_1_4_21.bin lag 3 400000 $D/paths_1_4_21.txt > $D/lag_1_4_21.txt
nice -n 10 $S/ss_lag $S/g_1_12_28.bin lag 3 4000000 $D/paths_1_12_28.txt > $D/lag_1_12_28.txt
nice -n 10 $S/ss_lag $S/g_1_4_28.bin lag 3 4000000 $D/paths_1_4_28.txt > $D/lag_1_4_28.txt
touch $S/chain_paths.done
