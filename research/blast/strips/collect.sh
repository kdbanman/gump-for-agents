#!/bin/sh
# sh collect.sh : copy the run outputs (LIFE lines, age bins, lags) from scratch into data/runs and rebuild data/table_out.txt
S=${S:-/home/user/gump-for-agents/research/scratch/blast/strips}; D=$(dirname "$0")
mkdir -p $D/data/runs $D/data/other
for f in $S/runs/*.txt; do [ -s $f ] && cp $f $D/data/runs/; done
# not pooled: the first (4 rows, L=4) run at T0 = 200 (ageing-in bias), kept for the record
[ -f $D/data/runs/p_7_4_s704.txt ] && mv $D/data/runs/p_7_4_s704.txt $D/data/other/
python3 $D/table.py > $D/data/table_out.txt
