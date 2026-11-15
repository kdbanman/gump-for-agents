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
# part 3 (added after parts 1-2, before its run): a second csz job, to test the 3.3 sigma difference in L6 (0.255 here, 0.211 in the study)
if [ "$1" = 3 ]; then
  b=r_v11c_csz_s2; $DY g_v11c_csz.txt run 9205 0.4 400000 $b.lives $b.ext $b.smp 128 $b.dmp 3000 512 512 > $b.json
fi
# Round 2 of the review (added before its runs): excursion tables (ex2.c) at R = 11 c with fresh seeds, and longer
# stationary sampling at R = 13 c. PBAR thresholds are the study's (31.29, 28.83, 26.29, 23.77; the same integer
# thresholds as this review's own 31.25, 28.90, 26.28, 23.50).
if [ "$1" = 4 ]; then
  gcc -O3 -march=native -o $D/ex2 $A/ex2.c
  x() { b=x_v11c_$1; $D/ex2 g_v11c_$1.txt run $3 0.4 $2 $b.lives $b.ext $b.smp 100000000 $b.dmp 0 1 512 $4 $b.x > $b.json; }
  x c1 1600000 9301 31.29; x d2h 400000 9304 23.77
elif [ "$1" = 5 ]; then
  gcc -O3 -march=native -o $D/ex2b $A/ex2.c
  x() { b=x_v11c_$1; $D/ex2b g_v11c_$1.txt run $3 0.4 $2 $b.lives $b.ext $b.smp 100000000 $b.dmp 0 1 512 $4 $b.x > $b.json; }
  x csz 800000 9302 28.83; x c2v 400000 9303 26.29
  for g in c1:9311 csz:9312 c2v:9313 d2h:9314; do G=${g%:*}; S=${g#*:}; b=s_v13c_$G
    $DY g_v13c_$G.txt run $S 0.4 300000 $b.lives $b.ext $b.smp 256 $b.dmp 0 1 512 > $b.json; done
fi
