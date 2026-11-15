#!/bin/bash
# Run plan of the review (fixed before any production run). Usage: bash plan.sh 1 | bash plan.sh 2  (two cores)
# Each job: st.c, 256 replicas, GENS generations per replica, fresh 0.4 soups drawn per orbit, seed as given.
D=/home/user/gump-for-agents/research/scratch/audit_symmetric; A=/home/user/gump-for-agents/research/audit/symmetric
cd $D && gcc -O3 -march=native -o st $A/st.c
job() { python3 $A/geo.py write $1 $2 g_$1_$2.txt > g_$1_$2.info && ./st g_$1_$2.txt run $4 0.4 $3 lives_$1_$2_s$4.bin > lives_$1_$2_s$4.json; }
if [ "$1" = 1 ]; then
  job v11c c1 4000000 9101; job v11c csz 1000000 9102; job v11c d2h 100000 9103
else
  job v11c ci 4000000 9104; job v11c c2e 1200000 9105; job v11c c2v 300000 9106
  job s4x2 c1 400000 9107; job s8x2 cs 1000000 9108
fi
