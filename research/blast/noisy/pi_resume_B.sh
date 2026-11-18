#!/bin/sh
# The PI's continuation of stage B (108 cells, blind) after the container was restarted at about 14:07 UTC on
# 2026-11-18 and the four detached processes of prod_B_108.sh died with it. Same frozen sampler (run_sub.sh), the
# seeds that prod_B_108.sh had not finished; a seed that was cut short is run again from the start (same seed, same
# replications, the file is overwritten). Four cores, about 105 minutes.
#   sh research/blast/noisy/pi_resume_B.sh ; python3 research/blast/noisy/fit.py
HERE=$(cd "$(dirname "$0")" && pwd)
( sh $HERE/run_sub.sh 15 128 15108 14 ; sh $HERE/run_sub.sh 15 128 15219 3 ) &
sh $HERE/run_sub.sh 15 128 15201 18 &
sh $HERE/run_sub.sh 15 64 15301 23 &
( sh $HERE/run_sub.sh 15 32 15414 22 ; sh $HERE/run_sub.sh 15 64 15324 6 ) &
wait
echo "stage B continuation done"
