#!/bin/bash
# r3 pilot: 200,000 generations x 256 lanes per system (fresh seeds 9401-9407), no excursion dumps; only the P
# histogram over the exposure (age > 512) is used, to fix each system's PBAR threshold before the production runs.
# Usage: bash r3_pilot.sh 1 & bash r3_pilot.sh 2 & wait    (needs the graph files written by r3_val.py and geo.py v17c)
D=/home/user/gump-for-agents/research/scratch/audit_dying/r3; cd $D
p() { ./r3_ex g_$1.txt run $2 0.4 200000 /dev/null /dev/null /dev/null 100000000 /dev/null 0 1 512 1000 pilot_$1.x -1 /dev/null > pilot_$1.json; }
if [ "$1" = 1 ]; then p v9c_c1 9401; p v11c_c1 9402; p v13c_c1 9403
else p v15c_c1 9404; p v17c_c1 9405; p v11c_csz 9406; p slab21 9407; fi
