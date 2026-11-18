#!/bin/sh
# hchain.sh OUTDIR : referee runs for the claims of agent `holes` (after the torus hole run `sl hole 12 0 12 s 250000`, s = 1..8)
O=$1
while [ ! -f $O/h.progress ]; do python3 -c "import time; time.sleep(2)"; done
L() { nice -n 10 ./sl life $1 0 $2 $3 $4 300 200000 0.5 >> $O/h_slablife.txt 2>/dev/null; }
L 2 8 11 600000; L 3 3 11 100000; L 3 4 11 200000; L 3 5 11 600000; L 4 4 11 1200000; L 3 6 11 2500000; L 4 5 11 2500000; L 2 6 11 300000
echo slablife >> $O/h.progress
for d in 0.35 0.50; do nice -n 10 ./rh life 5 21 400000 160 $d 1 >> $O/h_hulllife.txt; done
nice -n 10 ./rh life 5 22 400000 160 0.50 0 >> $O/h_hulllife.txt
nice -n 10 ./rh life 7 23 600000 1200 0.35 1 >> $O/h_hulllife.txt
nice -n 10 ./rh life 7 23 600000 1200 0.35 0 >> $O/h_hulllife.txt
nice -n 10 ./rh life 9 24 300000 3000 0.35 1 >> $O/h_hulllife.txt
echo hulllife >> $O/h.progress
for s in 1 2 3 4; do nice -n 10 ./rh hole 21 $s 250000 >> $O/h_hull21.txt; done
echo hullhole >> $O/h.progress
echo done > $O/h.done
