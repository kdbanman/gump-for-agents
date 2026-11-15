#!/bin/bash
# Run plan of the review of research/dying (fixed before any production run). Usage: bash plan.sh 1; bash plan.sh 2 (two cores)
# dy.c (st.c + histories + samples), 256 lanes, symmetric 0.4 soups, events every generation, Brent settled test.
# Samples every SAMPK generations of every lane; first 1500 deaths (F/X at age > 512) dumped with 512 generations of history.
D=/home/user/gump-for-agents/research/scratch/audit_dying; A=/home/user/gump-for-agents/research/audit/dying
mkdir -p $D && cd $D && DY=$D/dy && gcc -O3 -march=native -o $DY $A/dy.c
job() { python3 /home/user/gump-for-agents/research/audit/symmetric/geo.py write $1 $2 g_$1_$2.txt > g_$1_$2.info
  b=r_$1_$2; $DY g_$1_$2.txt run $4 0.4 $3 $b.lives $b.ext $b.smp $5 $b.dmp 1500 512 512 > $b.json; }
if [ "$1" = 1 ]; then
  job v11c c1 400000 9201 256; job v11c csz 200000 9202 128; job v11c c2v 100000 9203 64; job v11c d2h 100000 9204 64
elif [ "$1" = 2 ]; then
  job v13c c1 60000 9211 128; job v13c csz 60000 9212 128; job v13c c2v 60000 9213 128; job v13c d2h 100000 9214 64
  job v12v c1 60000 9221 128; job v12v csz 60000 9222 128; job v12v c2v 60000 9223 128; job v12v d2h 100000 9224 64
fi
