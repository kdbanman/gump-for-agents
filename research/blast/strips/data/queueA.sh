#!/bin/sh
# core A: after the first (5 rows, L=6) run, a second seed until 13:58 UTC
S=/home/user/gump-for-agents/research/scratch/blast/strips
until [ -s $S/runs/p_9_6_s906.txt ]; do sleep 5; done
left=$(( $(date -u -d '13:58' +%s) - $(date -u +%s) ))
[ $left -gt 60 ] && nice -n 10 $S/strips2 life prism 9 6 916 400 100000 $left 1 > $S/runs/prism_9_6_s916.txt 2> $S/runs/prism_9_6_s916.err
echo done > $S/runs/queueA.done
