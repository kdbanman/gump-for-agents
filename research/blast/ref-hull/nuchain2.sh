#!/bin/sh
# nuchain2.sh OUTDIR : second, longer batch of plain-running dip rates (seeds 11..18), appended to the same files
O=$1
while [ ! -f $O/nu19.done ]; do python3 -c "import time; time.sleep(2)"; done
run() { R=$1; G=$2; LA=$3; for s in 11 12 13 14 15 16 17 18; do nice -n 10 ./rh nu $R $s $G $LA >> $O/nu$R.txt; done; echo $R >> $O/nu2.progress; }
run 17 500000 70
run 15 500000 56
run 13 300000 43
run 21 250000 103
run 19 300000 86
run 11 300000 32
run 9 300000 22
echo done > $O/nu2.done
