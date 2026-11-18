#!/bin/sh
# after queue B: thin rods (both bookings), more of (5 rows, L=5), then (5 rows, L=6) until 13:58 UTC
S=/home/user/gump-for-agents/research/scratch/blast/strips
until [ -f $S/runs/queueB.done ]; do sleep 5; done
r() { nice -n 10 $S/strips2 life $1 $2 $3 $4 $5 $6 $7 1 > $S/runs/${1}_${2}_${3}_s$4.txt 2> $S/runs/${1}_${2}_${3}_s$4.err; }
for L in 3 4 5 6 7 8; do r prism 5 $L 50$L 1000 100000 20; done
for L in 3 4 5 6 7 8; do r prism 3 $L 30$L 300 100000 10; done
r prism 9 5 915 1000 20000 420
left=$(( $(date -u -d '13:58' +%s) - $(date -u +%s) ))
[ $left -gt 60 ] && r prism 9 6 926 400 100000 $left
echo done > $S/runs/queueC.done
